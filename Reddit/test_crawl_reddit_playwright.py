import argparse
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import crawl_reddit_playwright as runner
import export_browser_campaign as exporter
import verify_browser_campaign as verifier


class ResumeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.config = dict(max_posts=2, max_comments=2000, request_delay=2, total_seconds=1800,
                           project_id='test-university', keywords=['kuliah'], max_replies=1000, timeout_seconds=300,
                           subreddits=['indonesia'], since='2025-10-27T03:17:00Z', until='2026-10-27T03:17:00Z')
        self.rows = [dict(native_id=key, subreddit='indonesia', title='Kuliah',
                          canonical_url=f'https://www.reddit.com/r/indonesia/comments/{key}/kuliah/',
                          discovered_from='https://www.reddit.com/r/indonesia/search/?q=kuliah',observed_at='2026-10-27T00:00:00Z',
                          published_at='2026-06-01T00:00:00Z') for key in ['aaa', 'bbb', 'ccc']]
        runner.atomic_json(self.directory/'candidates.json', self.rows)

    def capture(self, row):
        return dict(post=dict(native_id=row['native_id'],title=row['title'],text='Isi post',
                              published_at=row['published_at'],subreddit=row['subreddit'],
                              permalink=f"/r/indonesia/comments/{row['native_id']}/kuliah/"),comments=[])

    def save_raw(self, row, version):
        value = dict(candidate=row,**self.capture(row),extractor_version=version,captured_at='2026-10-27T00:00:00Z',
                     method='standalone_playwright_cli' if version=='playwright-dom:1' else 'connected_chrome_rendered_dom')
        runner.atomic_json(self.directory/'raw'/(row['native_id']+'.json'),value)
        return value

    def test_resume_skips_dom_and_prioritizes_missing_before_excerpts(self):
        self.save_raw(self.rows[0], 'browser-dom:2')
        self.save_raw(self.rows[1], 'public-web-excerpt:1')
        _, queue, complete, _ = runner.campaign_plan(self.directory,self.config)
        self.assertEqual(complete, {'aaa'})
        self.assertEqual([row['native_id'] for row in queue], ['ccc','bbb'])

    def test_candidate_rejects_wrong_host_identity_and_window(self):
        self.assertTrue(runner.valid_candidate(self.rows[0],self.config))
        for changed in [dict(canonical_url='https://reddit.com.evil/r/indonesia/comments/aaa/kuliah/'),
                        dict(native_id='bbb'),dict(published_at=self.config['until'])]:
            self.assertFalse(runner.valid_candidate({**self.rows[0],**changed},self.config))

    def test_preserve_excerpt_when_replacing_with_dom_and_resume_after_atomic_write(self):
        original = self.save_raw(self.rows[0], 'public-web-excerpt:1')
        saved = runner.save_capture(self.directory,self.rows[0],self.capture(self.rows[0]),self.config)
        history = list((self.directory/'raw_history').glob('*.json'))
        self.assertEqual(len(history),1)
        self.assertEqual(json.loads(history[0].read_text()),original)
        self.assertEqual(saved['extractor_version'],'playwright-dom:1')
        self.assertIn('aaa',runner.campaign_plan(self.directory,self.config)[2])

    def test_reject_source_mismatch_before_overwriting_evidence(self):
        original = self.save_raw(self.rows[0],'public-web-excerpt:1')
        capture = self.capture(self.rows[0]);capture['post']['subreddit']='other'
        with self.assertRaises(ValueError):
            runner.save_capture(self.directory,self.rows[0],capture,self.config)
        self.assertEqual(json.loads((self.directory/'raw/aaa.json').read_text()),original)
        capture=self.capture(self.rows[0]);capture['page_url']='https://unrelated.example/r/indonesia/comments/aaa/kuliah/'
        with self.assertRaises(ValueError):runner.validate_capture(self.rows[0],capture,self.config)

    def test_parent_must_belong_to_same_thread_and_native_comments_deduplicate(self):
        capture = self.capture(self.rows[0])
        comment = dict(url='https://www.reddit.com/r/indonesia/comments/aaa/comment/xyz/',text='Komentar',parent_url=None)
        capture['comments'] = [comment,comment]
        self.assertEqual(len(runner.validate_capture(self.rows[0],capture,self.config)[1]),1)
        capture['comments'] = [{**comment,'parent_url':'https://www.reddit.com/r/indonesia/comments/bbb/comment/parent/'}]
        with self.assertRaises(ValueError):
            runner.validate_capture(self.rows[0],capture,self.config)

    def test_captcha_detected_but_user_post_discussing_captcha_is_not_a_barrier(self):
        self.assertEqual(runner.barrier_status({'page_title':'Reddit - Prove your humanity','post':None})[0],'CAPTCHA_REQUIRED')
        self.assertEqual(runner.barrier_status({'page_title':'Prove your humanity : r/indonesia','post':{'title':'Prove your humanity'}}),(None,None))
        self.assertEqual(runner.barrier_status({'page_title':'This page has been blocked by Chrome'}),('CLIENT_BROWSER_BLOCK',None))

    def test_rate_limit_honors_longest_header_or_visible_wait(self):
        now = datetime(2026,10,27,tzinfo=timezone.utc)
        self.assertEqual(runner.rate_limit_seconds('take a break for 246 seconds','120',now),246)
        self.assertEqual(runner.rate_limit_seconds('wait 2 minutes','300',now),300)
        self.assertEqual(runner.rate_limit_seconds('','Tue, 27 Oct 2026 00:05:00 GMT',now),300)
        self.assertEqual(runner.barrier_status({'http_status':429,'retry_after':'180'},now),('RATE_LIMITED',180))

    def test_chrome_http_429_error_page_is_a_rate_limit(self):
        self.assertEqual(runner.barrier_status({'page_title':'www.reddit.com','post':False,
            'barrier_text':'This page isn’t working\nHTTP ERROR 429\nReload'}),('RATE_LIMITED',60))
        self.assertEqual(runner.barrier_status({'page_title':'HTTP ERROR 429 : r/indonesia','post':True}),(None,None))

    def test_dom_only_export_does_not_count_public_excerpts(self):
        self.save_raw(self.rows[0],'browser-dom:2');self.save_raw(self.rows[1],'public-web-excerpt:1')
        self.assertEqual(len(exporter.load_campaign(self.directory,self.config)[0]),2)
        with self.assertRaises(ValueError):exporter.load_campaign(self.directory,self.config,dom_only=True)
        self.save_raw(self.rows[2],'playwright-dom:1')
        selected,_=exporter.load_campaign(self.directory,self.config,dom_only=True)
        self.assertEqual([row['native_id'] for row,raw in selected],['aaa','ccc'])

    def test_cli_nested_json_and_error_are_not_mistaken_for_page_data(self):
        self.assertEqual(runner.decode_cli_output('{"result":"{\\"post\\":null}"}'),{'post':None})
        with self.assertRaises(RuntimeError):runner.decode_cli_output('{"error":"failed"}')

    def test_dom_export_uses_playwright_source_and_existing_eight_sheet_contract(self):
        self.save_raw(self.rows[0],'browser-dom:2');self.save_raw(self.rows[1],'public-web-excerpt:1');self.save_raw(self.rows[2],'playwright-dom:1')
        out=self.directory/'bundle'
        summary=exporter.export_campaign(self.directory,self.config,out,dom_only=True)
        checked=verifier.verify(out,self.config)
        self.assertTrue(summary['dom_target_reached'])
        self.assertEqual(checked['unique_posts'],2)
        rows=[json.loads(line) for line in (out/'Contents.jsonl').read_text().splitlines()]
        playwright=next(row for row in rows if row['adapter_version']=='playwright-dom:1')
        self.assertEqual(playwright['extraction_method'],'standalone_playwright_cli')
        self.assertNotIn('paragraph_text_only',playwright['quality_flags'])
        self.assertEqual(checked['checksum_files'],10)

    def test_dry_run_cannot_clear_a_persisted_cooldown(self):
        config_path=self.directory/'config.json';runner.atomic_json(config_path,self.config)
        cooldown=(runner.utcnow()+timedelta(minutes=5)).isoformat()
        runner.atomic_json(self.directory/'playwright_progress.json',{'cooldown_until':cooldown})
        args=argparse.Namespace(config=config_path,total_seconds=None,limit=None,session='test',support_dir=self.directory,
                                dry_run=True,check_only=False,cli=None,artifact_dir=self.directory/'artifacts',headless=False)
        with patch('builtins.print'):
            self.assertEqual(runner.run(args),0)
        self.assertEqual(json.loads((self.directory/'playwright_progress.json').read_text())['cooldown_until'],cooldown)


if __name__ == '__main__':
    unittest.main()
