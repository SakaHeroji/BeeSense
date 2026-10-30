"""Offline checks for the Chrome boundary, native identity, and provenance."""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from Crawler.Backend import instagram_browser as browser
from Crawler.Backend.instagram_crawler import InstagramCrawler


class InstagramBrowserTests(unittest.TestCase):
    def test_configuration_rejects_secrets_and_invalid_limits(self):
        for value in (
            {"password": "secret"},
            {"session": "../unsafe"},
            {"max_scrolls": 99},
            {"headed": "yes"},
        ):
            with self.subTest(value=value), self.assertRaises((ValueError, TypeError)):
                browser.browser_configuration(value)

    def test_browser_is_real_backend_but_injected_workers_remain_synthetic(self):
        crawler = InstagramCrawler("config/instagram_browser_crawler.json")
        self.assertFalse(crawler.synthetic)
        self.assertEqual(crawler.method, browser.BROWSER_METHOD)
        self.assertIsInstance(crawler.worker, browser.InstagramBrowserWorker)
        self.assertEqual(crawler.config["total_seconds"], 1800)
        fixture = InstagramCrawler(
            "config/instagram_browser_crawler.json", worker=lambda *args: None
        )
        self.assertTrue(fixture.synthetic)

    def test_cli_error_never_exposes_auth_redirect_or_input(self):
        worker = browser.InstagramBrowserWorker({})
        with (
            patch.object(browser.shutil, "which", return_value="npx"),
            patch.object(
                browser.subprocess,
                "run",
                return_value=SimpleNamespace(
                    returncode=1, stdout="password secret", stderr="sessionid secret"
                ),
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError, "^playwright_cli_operation_failed$"
            ):
                worker.call(["run-code", "async page => null"], 2)

    def test_timeout_preserves_browser_for_manual_inspection(self):
        worker = browser.InstagramBrowserWorker({})
        worker._opened = True
        with patch.object(
            worker, "call", side_effect=subprocess.TimeoutExpired("cli", 1)
        ):
            result = worker(
                "media",
                "https://www.instagram.com/p/B/",
                SimpleNamespace(search_results=10),
                1,
                lambda *args: None,
            )
        self.assertEqual(result["status"], "TIMEOUT")
        self.assertTrue(worker._barrier)

    def test_repeated_cli_error_preserves_browser_without_claiming_access_barrier(self):
        worker = browser.InstagramBrowserWorker({})
        worker._opened = True
        with patch.object(
            worker, "call", side_effect=RuntimeError("playwright_cli_operation_failed")
        ) as call:
            result = worker(
                "media",
                "https://www.instagram.com/p/B/",
                SimpleNamespace(search_results=10),
                5,
                lambda *args: None,
            )
            worker.close()
        self.assertEqual(result["status"], "SOURCE_ERROR")
        self.assertEqual(result["reason"], "browser_cli_operation_failed")
        self.assertTrue(worker._barrier)
        self.assertEqual(call.call_count, 1)

    def test_browser_429_passes_retry_after_and_keeps_chrome_open(self):
        worker = browser.InstagramBrowserWorker({})
        worker._opened = True
        with patch.object(
            worker,
            "call",
            return_value={"status": "RATE_LIMITED", "retry_after_seconds": 720},
        ) as call:
            result = worker(
                "media",
                "https://www.instagram.com/p/B/",
                SimpleNamespace(search_results=10),
                5,
                lambda *args: self.fail("No content on 429"),
            )
            worker.close()
        self.assertEqual(result["status"], "RATE_LIMITED")
        self.assertEqual(result["retry_after_seconds"], 720)
        self.assertEqual(call.call_count, 1)

    @unittest.skipUnless(shutil.which("node"), "Node is required for browser helper")
    def test_navigation_observes_429_even_when_chrome_throws_before_response(self):
        source = (
            browser.ROOT / "Crawler/Backend/instagram_browser_capture.mjs"
        ).as_uri()
        script = f"""
import {{instagramNavigate as navigate,instagramRetryAfter as retry,instagramSourceRateLimit as rate}} from {json.dumps(source)};
import {{EventEmitter}} from 'node:events';
import assert from 'node:assert/strict';
const session=new EventEmitter(); let detached=0;
session.send=async method=>method==='Page.getFrameTree'?{{frameTree:{{frame:{{id:'main'}}}}}}:{{}};
session.detach=async()=>{{detached++}};
const page=new EventEmitter();
page.context=()=>({{newCDPSession:async()=>session}});
page.goto=async()=>{{
 session.emit('Network.requestWillBeSent',{{requestId:'doc',type:'Document',frameId:'main'}});
 session.emit('Network.responseReceivedExtraInfo',{{requestId:'doc',statusCode:429,headers:{{'Retry-After':'720','Set-Cookie':'TEST_SECRET_COOKIE'}}}});
 throw new Error('net::ERR_HTTP_RESPONSE_CODE_FAILURE');
}};
const result=await navigate(page,'https://www.instagram.com/p/B/',1000);
assert.equal(result.http_status,429);assert.equal(result.retry_after_seconds,720);
assert.equal(detached,1);assert.equal(page.listenerCount('response'),0);
assert.equal(JSON.stringify(result).includes('TEST_SECRET_COOKIE'),false);
assert.equal(retry('6.5'),7);assert.equal(retry('invalid'),null);
assert.equal(retry('Thu, 01 Jan 1970 00:00:06 GMT',0),6);
assert.equal(rate({{url:()=> 'https://www.instagram.com/graphql/query',status:()=>429,headers:()=>({{'retry-after':'420'}})}}).retry_after_seconds,420);
assert.equal(rate({{url:()=> 'https://instagram.com.evil.test/',status:()=>429,headers:()=>({{}})}}),null);
page.goto=async()=>{{throw new Error('generic_network_failure')}};
await assert.rejects(navigate(page,'https://www.instagram.com/p/B/',1000),/generic_network_failure/);
"""
        value = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(value.returncode, 0, value.stderr)
        generated = browser.browser_script(
            "media",
            "https://www.instagram.com/p/B/",
            SimpleNamespace(search_results=10),
            browser.browser_configuration({}),
            5,
        )
        parsed = subprocess.run(
            [
                "node",
                "-e",
                "new Function('return (' + process.argv[1] + ')')",
                generated,
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(parsed.returncode, 0, parsed.stderr)

    def test_browser_bundle_keeps_backend_provenance_and_fixture_is_not_live(self):
        from tests.crawler.test_instagram_crawler import URL, records

        cfg = json.loads(
            (browser.ROOT / "config/instagram_browser_crawler.json").read_text()
        )
        cfg["exclude_existing_datasets"] = []
        cfg["platforms"]["instagram"].update(
            urls=[URL], hashtags=[], min_posts=1, min_comments_per_post=2
        )

        def fixture(operation, target, settings, seconds, emit):
            for row in records():
                emit("record", row)
            return {"status": "FINISHED_BEST_EFFORT", "source_version": "fixture"}

        crawler = InstagramCrawler(cfg, worker=fixture)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bundle"
            result = crawler.run(output)
            source = json.loads((output / "Sources.jsonl").read_text())
            rows = [
                json.loads(line)
                for line in (output / "Contents.jsonl").read_text().splitlines()
            ]
        self.assertEqual(result["posts_exported"], 1)
        self.assertEqual(result["comments"], 1)
        self.assertEqual(result["replies"], 1)
        self.assertTrue(result["synthetic"])
        self.assertFalse(result["trial_passed"])
        self.assertEqual(source["extraction_method"], browser.BROWSER_METHOD)
        self.assertTrue(
            all(row["extraction_method"] == browser.BROWSER_METHOD for row in rows)
        )

    @unittest.skipUnless(
        shutil.which("node"), "Node is required for the browser helper"
    )
    def test_document_parser_rejects_unrelated_posts_and_preserves_reply_parent(self):
        source = (
            browser.ROOT / "Crawler/Backend/instagram_browser_capture.mjs"
        ).as_uri()
        script = f"""
import {{instagramDocumentPayload as extract,instagramBarrier as barrier}} from {json.dumps(source)};
import assert from 'node:assert/strict';
const media={{pk:'1',code:'B',taken_at:1790000000,caption:{{text:'Kuliah 😊'}},user:{{pk:'9'}}}};
const comment={{pk:'21',text:'Biaya?',created_at:1790000001,parent_comment_id:null}};
const reply={{pk:'22',text:'Beasiswa',created_at:1790000002,parent_comment_id:'21'}};
const data={{xdt_api__v1__media__shortcode__web_info:{{items:[media]}},
 xdt_api__v1__media__media_id__comments__connection:{{edges:[{{node:comment}},{{node:reply}},{{node:comment}}]}}}};
const actual=extract({{require:[{{data}}]}},'B');
assert.equal(actual.media.pk,'1');
assert.equal(actual.media.caption_text,'Kuliah 😊');
assert.equal(actual.comments.length,2);
assert.equal(actual.comments[1].replied_to_comment_id,'21');
assert.equal(extract({{data}},'C').media,null);
assert.equal(extract({{data:{{xdt_api__v1__media__media_id__comments__connection:data.xdt_api__v1__media__media_id__comments__connection}}}},'B').comments.length,0);
const streamed=[{{data:{{xdt_api__v1__media__shortcode__web_info:data.xdt_api__v1__media__shortcode__web_info}}}},
 {{data:{{xdt_api__v1__media__media_id__comments__connection:data.xdt_api__v1__media__media_id__comments__connection}}}}];
assert.equal(extract(streamed,'B').comments.length,0);
assert.equal(extract(streamed,'B',['21']).comments.length,1);
assert.equal(extract(streamed,'B',['999']).comments.length,0);
assert.equal(extract(streamed,'B',['21','22']).comments[1].replied_to_comment_id,'21');
assert.equal(barrier('/p/B/',0,false,200),null);
assert.equal(barrier('/p/B/',0,false,429),'RATE_LIMITED');
assert.equal(barrier('/accounts/login/',1,false,200),'LOGIN_REQUIRED');
assert.equal(barrier('/challenge/',0,false,200),'CHALLENGE_REQUIRED');
console.log('native identity, matching media context, dedup, parents, barriers: OK');
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "check.mjs"
            path.write_text(script)
            value = subprocess.run(
                ["node", str(path)], capture_output=True, text=True, timeout=10
            )
            self.assertEqual(value.returncode, 0, value.stderr)


if __name__ == "__main__":
    unittest.main()
