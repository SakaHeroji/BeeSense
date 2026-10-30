#!/usr/bin/env python3
"""Join verified public web excerpts to the existing browser candidate metadata."""
import argparse
from collections import Counter
import json
from pathlib import Path

from Crawler.Backend.Reddit import crawl_reddit_single as common


def import_sections(directory, config):
    candidates = {row['native_id']: row for row in json.loads((directory/'candidates.json').read_text())}
    allowed = set(config['subreddits'])
    since, until = common.utc_datetime(config['since']), common.utc_datetime(config['until'])
    raw_dir = directory/'raw'
    raw_dir.mkdir(exist_ok=True)
    for filename in sorted((directory/'web_sections').glob('*.json')):
        value = json.loads(filename.read_text())
        native_id = value['native_id']
        candidate = candidates.get(native_id)
        target = raw_dir/(native_id+'.json')
        if not candidate or candidate['subreddit'].lower() not in allowed or target.exists(): continue
        if common.thread_id(value['source_url']) != native_id: raise ValueError('Source identity mismatch')
        if not since <= common.utc_datetime(candidate['published_at']) < until: continue
        raw = {'candidate': candidate, 'post': {
            'native_id': native_id, 'title': candidate['title'], 'text': value['text'],
            'published_at': candidate['published_at'], 'permalink': common.safe_web_url(candidate['canonical_url']).path,
            'subreddit': candidate['subreddit'], 'post_type': 'public_web_post_section',
            'score_display': None, 'comment_count_display': None, 'source_show_full_content': False},
            'comments': [], 'captured_at': value['retrieved_at'], 'method': 'public_web_reader',
            'extractor_version': 'public-web-excerpt:1', 'rss_used': False,
            'coverage': 'PARTIAL_WEB_POST_SECTION', 'source_url': value['source_url'],
            'provider_cache_note': value['cache_note'], 'source_capture_time_known': False,
            'excerpt_truncated': value['excerpt_truncated'], 'publication_date_source': 'browser_search_datetime_attribute'}
        stage = target.with_suffix('.json.tmp')
        stage.write_text(json.dumps(raw, ensure_ascii=False))
        stage.replace(target)
    versions = Counter()
    for filename in raw_dir.glob('*.json'):
        raw = json.loads(filename.read_text())
        if raw['candidate']['subreddit'].lower() in allowed: versions[raw['extractor_version']] += 1
    return {'captured_post_sections':sum(versions.values()), 'versions':dict(versions), 'target':config['max_posts']}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--support-dir',type=Path,required=True)
    parser.add_argument('--config',type=Path,default=Path(__file__).with_name('config_reddit_1000.json'))
    args=parser.parse_args()
    print(json.dumps(import_sections(args.support_dir,json.loads(args.config.read_text())),indent=2))
