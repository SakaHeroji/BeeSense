#!/usr/bin/env python3
"""Resume public Reddit DOM acquisition through the standalone Playwright CLI.

No login, RSS, API token, browser-profile copying, or challenge solving.
Existing Chrome DOM records are retained; public web excerpts are backed up before
replacement. A CAPTCHA/access barrier stops the run and leaves its browser open.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import fcntl
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlparse

if __package__:
    from . import crawl_reddit_single as common
else:
    import crawl_reddit_single as common

DOM_VERSIONS = {'browser-dom:2', 'playwright-dom:1'}
ROOT = Path(__file__).resolve().parent.parent


def utcnow():
    return datetime.now(timezone.utc)


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as stream:
        stage = Path(stream.name)
        try:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            stage.unlink(missing_ok=True)
            raise
    try:
        os.replace(stage, path)
    finally:
        stage.unlink(missing_ok=True)


def valid_candidate(row, config):
    url = urlparse(row.get('canonical_url', ''))
    match = re.fullmatch(r'/r/([A-Za-z0-9_]+)/comments/([a-z0-9]+)/[^/]+/?', url.path)
    try:
        stamp = common.utc_datetime(row['published_at'])
        return bool(url.scheme == 'https' and url.netloc == 'www.reddit.com' and not url.query and
                    match and match[1].lower() == row['subreddit'].lower() and match[2] == row['native_id'] and
                    row['subreddit'].lower() in config['subreddits'] and row['title'].strip() and
                    common.utc_datetime(config['since']) <= stamp < common.utc_datetime(config['until']))
    except (KeyError, TypeError, ValueError):
        return False


def campaign_plan(directory, config):
    candidates, seen = [], set()
    for row in json.loads((directory / 'candidates.json').read_text()):
        if valid_candidate(row, config) and row['native_id'] not in seen:
            candidates.append(row)
            seen.add(row['native_id'])
    raw, versions, complete = {}, Counter(), set()
    for row in candidates:
        path = directory / 'raw' / (row['native_id'] + '.json')
        if not path.exists():
            continue
        value = json.loads(path.read_text())
        raw[row['native_id']] = value
        versions[value.get('extractor_version', 'unknown')] += 1
        post = value.get('post', {})
        if value.get('extractor_version') in DOM_VERSIONS:
            validate_capture(row, {'post':post, 'comments':value.get('comments', [])}, config)
            complete.add(row['native_id'])
    # Acquire missing bodies first; then replace bounded web excerpts with DOM.
    queue = sorted((row for row in candidates if row['native_id'] not in complete),
                   key=lambda row: row['native_id'] in raw)
    return candidates, queue, complete, versions


def rate_limit_seconds(text, header=None, now=None):
    now = now or utcnow()
    waits = []
    if header:
        try:
            waits.append(max(0, int(header)))
        except ValueError:
            try:
                stamp = parsedate_to_datetime(header)
                if stamp.tzinfo is None:
                    stamp = stamp.replace(tzinfo=timezone.utc)
                waits.append(max(0, (stamp - now).total_seconds()))
            except (TypeError, ValueError, OverflowError):
                pass
    for number, unit in re.findall(r'(?:break for|try again in|wait)\s+(\d+)\s+(seconds?|minutes?)', text, re.I):
        waits.append(int(number) * (60 if unit.lower().startswith('minute') else 1))
    return max(waits, default=60)


def barrier_status(capture, now=None):
    status = capture.get('http_status')
    text = str(capture.get('page_title', '')) + '\n' + str(capture.get('barrier_text', ''))
    if (status == 429 or re.search(r'request has been rate limited|too many requests', text, re.I)
            or not capture.get('post') and re.search(r'\bHTTP\s+(?:ERROR\s+)?429\b', text, re.I)):
        return 'RATE_LIMITED', rate_limit_seconds(text, capture.get('retry_after'), now)
    if re.search(r'ERR_BLOCKED_BY_CLIENT|This page has been blocked by Chrome', text, re.I):
        return 'CLIENT_BROWSER_BLOCK', None
    # User post/comment text is never used as a CAPTCHA signal when a post exists.
    if not capture.get('post') and re.search(r'prove your humanity|verify (?:that )?you.re human|complete the challenge|recaptcha', text, re.I):
        return 'CAPTCHA_REQUIRED', None
    if status in {401, 403} or re.search(r'you.ve been blocked|blocked by network|log in to continue|login required', text, re.I):
        return 'ACCESS_BARRIER', None
    return None, None


def validate_capture(candidate, capture, config):
    post = capture.get('post')
    if not isinstance(post, dict) or post.get('native_id') != candidate['native_id'] or not post.get('title'):
        raise ValueError('post_identity_or_title_unverified')
    permalink = urlparse(post.get('permalink') or '').path
    path = f"/r/{candidate['subreddit']}/comments/{candidate['native_id']}/"
    if capture.get('page_url'):
        actual = urlparse(capture['page_url'])
        if actual.scheme != 'https' or actual.netloc not in {'www.reddit.com','reddit.com'} or not actual.path.lower().startswith(path.lower()):
            raise ValueError('navigation_did_not_reach_source_permalink')
    if not permalink.lower().startswith(path.lower()) or post.get('subreddit', '').lower() != candidate['subreddit'].lower():
        raise ValueError('source_permalink_or_subreddit_mismatch')
    if not common.utc_datetime(config['since']) <= common.utc_datetime(post['published_at']) < common.utc_datetime(config['until']):
        raise ValueError('source_publication_date_outside_window')
    comments, seen = [], set()
    for item in capture.get('comments', []):
        url = urlparse(item.get('url') or '')
        match = re.fullmatch(r'/r/[^/]+/comments/([a-z0-9]+)/comment/([a-z0-9]+)/?', url.path)
        if (url.scheme != 'https' or url.netloc not in {'www.reddit.com', 'reddit.com'} or not match or
                match[1] != candidate['native_id'] or not item.get('text')):
            continue
        if item.get('parent_url'):
            parent = urlparse(item['parent_url'])
            parent_match = re.fullmatch(r'/r/[^/]+/comments/([a-z0-9]+)/comment/([a-z0-9]+)/?', parent.path)
            if parent.netloc not in {'www.reddit.com', 'reddit.com'} or not parent_match or parent_match[1] != candidate['native_id']:
                raise ValueError('comment_parent_outside_source_thread')
        if match[2] not in seen:
            comments.append(item)
            seen.add(match[2])
    return post, comments[:config['max_comments']]


def save_capture(directory, candidate, capture, config):
    post, comments = validate_capture(candidate, capture, config)
    value = dict(candidate=candidate, post=post, comments=comments, captured_at=utcnow().isoformat(),
                 method='standalone_playwright_cli', extractor_version='playwright-dom:1', rss_used=False,
                 coverage='PARTIAL_RENDERED_DOM', more_replies_expanded=False)
    path = directory / 'raw' / (candidate['native_id'] + '.json')
    if path.exists():
        previous = path.read_bytes()
        history = directory / 'raw_history' / (candidate['native_id'] + '_' + sha256(previous).hexdigest()[:16] + '.json')
        if not history.exists():
            atomic_json(history, json.loads(previous))
    atomic_json(path, value)
    return value


def decode_cli_output(output):
    value = json.loads(output)
    if value.get('isError') or value.get('error'):
        raise RuntimeError('playwright_cli_reported_error')
    result = value.get('result')
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result
    return result


class PlaywrightCLI:
    def __init__(self, cli, session, artifacts, timeout=90):
        path = Path(cli).expanduser()
        if path.suffix in {'.js', '.sh'}:
            path = path.resolve()
        self.command = (['node', str(path)] if path.suffix == '.js' else ['bash', str(path)] if path.suffix == '.sh' else [str(path)])
        self.session, self.artifacts, self.timeout = session, artifacts, timeout
        artifacts.mkdir(parents=True, exist_ok=True)

    def call(self, *arguments, decode=False):
        command = self.command + [f'-s={self.session}', '--json', *map(str, arguments)]
        result = subprocess.run(command, cwd=self.artifacts, capture_output=True, text=True, timeout=self.timeout)
        if result.returncode:
            raise RuntimeError((result.stderr or result.stdout).strip()[-2000:])
        return decode_cli_output(result.stdout) if decode else result.stdout

    def inspect(self):
        return self.call('run-code', 'async page => { const post=!!(await page.locator("shreddit-post").count()); return {page_url:page.url(), page_title:await page.title(), barrier_text:post ? (await page.locator("[role=banner], header").allTextContents()).join("\\n") : await page.locator("body").innerText(), post}; }', decode=True)

    def capture(self, candidate, config):
        source = (Path(__file__).with_name('rendered_thread_dom.mjs')).read_text()
        source = re.sub(r'\bexport\s+(?=function\b)', '', source)
        parameters = json.dumps({'nativeId':candidate['native_id'], 'maxComments':config['max_comments']})
        url = json.dumps(candidate['canonical_url'])
        timeout = min(config['timeout_seconds'] * 1000, 45000)
        script = ('async page => {\n' + source + '\n' +
                  f'const response = await page.goto({url}, {{waitUntil:"domcontentloaded", timeout:{timeout}}});\n' +
                  'await page.waitForFunction(() => document.querySelector("shreddit-post") || /prove your humanity|rate limited|blocked by network/i.test(document.body?.innerText || ""), null, {timeout:10000}).catch(() => {});\n' +
                  'if (Number(await page.locator("shreddit-post").first().getAttribute("comment-count").catch(() => 0)) > 0) await page.locator("[role=article]").first().waitFor({state:"visible",timeout:10000}).catch(() => {});\n' +
                  f'const capture = await page.evaluate(captureRenderedThread, {parameters});\n' +
                  'return {...capture, http_status:response?.status(), retry_after:response?.headers()["retry-after"]};\n}')
        filename = self.artifacts / 'capture-current.js'
        filename.write_text(script)
        capture = self.call('run-code', '--filename', filename, decode=True)
        self.call('snapshot', '--filename', self.artifacts / ('thread-' + candidate['native_id'] + '.yml'))
        return capture

    def evidence(self, label):
        image = self.artifacts / (label + '.png')
        try:
            self.call('snapshot', '--filename', self.artifacts / (label + '.yml'))
            self.call('screenshot', '--filename', image)
            return str(image)
        except (RuntimeError, subprocess.TimeoutExpired):
            return None


def find_cli(explicit=None):
    if explicit:
        return explicit
    installed = shutil.which('playwright-cli')
    if installed:
        return installed
    cached = list((Path.home() / '.npm/_npx').glob('*/node_modules/@playwright/cli/playwright-cli.js'))
    if cached:
        return str(max(cached, key=lambda path:path.stat().st_mtime))
    return str(Path.home() / '.codex/skills/playwright/scripts/playwright_cli.sh')


def run(args):
    config = json.loads(args.config.read_text())
    args.session = args.session or config.get('standalone_playwright', {}).get('session', 'beesense-reddit')
    if args.total_seconds is not None:
        config['total_seconds'] = args.total_seconds
    if config['max_posts'] < 1 or config['max_comments'] < 0 or config['request_delay'] < 0 or config['total_seconds'] <= 0 or args.limit is not None and args.limit < 1:
        raise ValueError('invalid campaign bounds')
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.session):
        raise ValueError('invalid Playwright session name')
    directory = args.support_dir.resolve()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / 'playwright.lock').open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('another Playwright campaign runner holds the checkpoint lock')
        candidates, queue, completed, versions = campaign_plan(directory, config)
        state_path = directory / 'playwright_progress.json'
        previous = json.loads(state_path.read_text()) if state_path.exists() else {}
        state = dict(status='READY', session=args.session, browser='chrome', target_posts=config['max_posts'],
                     candidates=len(candidates), dom_posts=len(completed), pending_dom_posts=max(0,config['max_posts']-len(completed)),
                     previous_source_versions=dict(versions), attempts_this_run=0, captured_this_run=0,
                     since=config['since'], until=config['until'], rss_used=False, comments_complete=False,
                     last_request_at=previous.get('last_request_at'))
        if previous.get('cooldown_until'):
            state['cooldown_until'] = previous['cooldown_until']

        def checkpoint(status, **extra):
            state.update(status=status, updated_at=utcnow().isoformat(), dom_posts=len(completed),
                         pending_dom_posts=max(0,config['max_posts']-len(completed)), **extra)
            atomic_json(state_path, state)
            print(json.dumps(state, ensure_ascii=False), flush=True)

        if args.dry_run:
            checkpoint('DRY_RUN', next_native_ids=[row['native_id'] for row in queue[:5]])
            return 0
        if previous.get('cooldown_until') and common.utc_datetime(previous['cooldown_until']) > utcnow():
            checkpoint('COOLDOWN', cooldown_until=previous['cooldown_until'])
            return 2
        cli_path = find_cli(args.cli)
        cli = PlaywrightCLI(cli_path, args.session, args.artifact_dir.resolve())
        try:
            current = cli.inspect()
        except RuntimeError as error:
            if args.check_only or "is not open" not in str(error):
                checkpoint('BROWSER_NOT_READY', error=str(error))
                return 2
            options = ['open', 'about:blank', '--browser=chrome', '--profile=' + str(cli.artifacts / 'profile')]
            if not args.headless:
                options.append('--headed')
            cli.call(*options)
            current = cli.inspect()
        barrier, wait = barrier_status(current)
        if barrier:
            extra = {'evidence_screenshot':cli.evidence('access-barrier')}
            if wait is not None:
                extra['cooldown_until'] = (utcnow() + timedelta(seconds=wait)).isoformat()
            checkpoint(barrier, **extra)
            return 2
        if args.check_only:
            checkpoint('BROWSER_READY')
            return 0
        deadline, errors = time.monotonic() + config['total_seconds'], 0
        receipt_path = directory / 'playwright_receipts.jsonl'
        checkpoint('RUNNING')
        try:
            for candidate in queue:
                if len(completed) >= config['max_posts']:
                    break
                if (args.limit is not None and state['attempts_this_run'] >= args.limit) or time.monotonic() >= deadline:
                    checkpoint('CHECKPOINT_SAVED')
                    return 0
                if state.get('last_request_at'):
                    remaining = config['request_delay'] - (utcnow() - common.utc_datetime(state['last_request_at'])).total_seconds()
                    if remaining > 0:
                        time.sleep(remaining)
                state['last_request_at'] = utcnow().isoformat()
                state['attempts_this_run'] += 1
                checkpoint('RUNNING', current_native_id=candidate['native_id'])
                receipt = dict(native_id=candidate['native_id'], target=candidate['canonical_url'], started_at=state['last_request_at'])
                try:
                    capture = cli.capture(candidate, config)
                    barrier, wait = barrier_status(capture)
                    if barrier:
                        receipt.update(status=barrier, retry_after_seconds=wait)
                    else:
                        value = save_capture(directory, candidate, capture, config)
                        completed.add(candidate['native_id'])
                        state['captured_this_run'] += 1
                        errors = 0
                        receipt.update(status='CAPTURED', comment_entries=len(value['comments']))
                except (RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
                    receipt.update(status='BROWSER_CAPTURE_ERROR_UNVERIFIED', error_type=type(error).__name__, reason=str(error)[-1000:])
                    errors += 1
                receipt['finished_at'] = utcnow().isoformat()
                with receipt_path.open('a') as stream:
                    stream.write(json.dumps(receipt, ensure_ascii=False) + '\n')
                    stream.flush()
                    os.fsync(stream.fileno())
                if receipt['status'] in {'CAPTCHA_REQUIRED','ACCESS_BARRIER','CLIENT_BROWSER_BLOCK','RATE_LIMITED'}:
                    extra = {'evidence_screenshot':cli.evidence('access-barrier')}
                    if receipt.get('retry_after_seconds') is not None:
                        extra['cooldown_until'] = (utcnow() + timedelta(seconds=receipt['retry_after_seconds'])).isoformat()
                    checkpoint(receipt['status'], **extra)
                    return 2
                if errors >= 3:
                    checkpoint('STOPPED_AFTER_CAPTURE_ERRORS')
                    return 2
                checkpoint('RUNNING')
        except KeyboardInterrupt:
            checkpoint('INTERRUPTED_CHECKPOINT_SAVED')
            return 130
        checkpoint('TARGET_REACHED' if len(completed) >= config['max_posts'] else 'CANDIDATES_EXHAUSTED')
        return 0 if len(completed) >= config['max_posts'] else 2


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--support-dir', type=Path, default=ROOT / 'outputs/_support_reddit_1000_20261027')
    parser.add_argument('--config', type=Path, default=Path(__file__).with_name('config_reddit_1000.json'))
    parser.add_argument('--artifact-dir', type=Path, default=ROOT / 'output/playwright/reddit')
    parser.add_argument('--cli', help='Installed playwright-cli executable, CLI .js, or official wrapper .sh')
    parser.add_argument('--session', help='Defaults to standalone_playwright.session or beesense-reddit')
    parser.add_argument('--headless', action='store_true', help='Applies only when starting a new session')
    parser.add_argument('--total-seconds', type=float)
    parser.add_argument('--limit', type=int, help='Maximum attempted posts for this invocation')
    parser.add_argument('--dry-run', action='store_true', help='Validate checkpoint and show queue without browser access')
    parser.add_argument('--check-only', action='store_true', help='Inspect existing session without navigation or capture')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        raise SystemExit(run(arguments()))
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(json.dumps({'status':'RUNNER_ERROR', 'error_type':type(error).__name__, 'reason':str(error)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
