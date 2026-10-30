#!/usr/bin/env python3
"""Selenium YouTube/Reddit crawler using SocialCrawler's unchanged Excel contract.

Only public rendered pages are read. Each operation owns an isolated Chrome
session in a bounded child process; no personal profile or cookies are imported.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import re
import sys
import time
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, quote, urlencode, urljoin, urlsplit

from Crawler.Backend.social_crawler import ROOT, SocialCrawler, reddit, youtube

VERSION = "0.1.0"
METHOD = "selenium_rendered_dom"
SOURCE_VERSION = "selenium-dom:" + VERSION

PAGE_STATE = """
const content = !!document.querySelector(
  'shreddit-post, .thing.link, ytd-watch-flexy[video-id], ytd-video-renderer, '
  + 'search-telemetry-tracker, h2 a[href*="/comments/"]');
return {url: location.href, title: document.title, content,
  text: (content ? Array.from(document.querySelectorAll('header,[role=banner]'))
    .map(e => e.innerText).join('\\n') : document.body?.innerText || '').slice(0,20000),
  challenge: !!document.querySelector(
    'form input[name=jsc_token],form input[name=js_challenge],iframe[src*="recaptcha/api2/bframe"]'),
  status: performance.getEntriesByType('navigation')[0]?.responseStatus || null};
"""

SEARCH_LINKS = """
const selector = arguments[0] === 'youtube'
  ? 'ytd-video-renderer a#video-title,ytd-rich-item-renderer a[href*="/watch?"]'
  : 'shreddit-post a[href*="/comments/"],search-telemetry-tracker a[href*="/comments/"],'
    + 'h2 a[href*="/comments/"],.search-result-link a.search-title';
return Array.from(document.querySelectorAll(selector)).map(e => e.href);
"""

YOUTUBE_VIDEO = """
const text = selector => document.querySelector(selector)?.innerText?.trim() || '';
const meta = selector => document.querySelector(selector)?.content || null;
const canonical = document.querySelector('link[rel=canonical]')?.href || '';
let structured = [];
for (const element of document.querySelectorAll('script[type="application/ld+json"]')) {
  try {const item = JSON.parse(element.textContent);
    structured.push(...(Array.isArray(item) ? item : item['@graph'] || [item]));} catch {}
}
const video = structured.find(item => item['@type'] === 'VideoObject') || {};
const id = document.querySelector('ytd-watch-flexy')?.getAttribute('video-id')
  || (document.querySelector('video') ? new URL(canonical || location.href).searchParams.get('v') : null);
return {id, title: text('h1.ytd-watch-metadata') || text('h1.title') || meta('meta[property="og:title"]'),
  description: text('#description-inline-expander #expanded')
    || text('#description-inline-expander #attributed-snippet-text')
    || text('#description yt-formatted-string') || video.description || meta('meta[name=description]') || '',
  published: meta('meta[itemprop=datePublished]') || video.datePublished
    || meta('meta[itemprop=uploadDate]') || video.uploadDate || null,
  channel_url: document.querySelector('ytd-channel-name a')?.href || null};
"""

YOUTUBE_COMMENTS = """
const commentSelector = 'ytd-comment-view-model,ytd-comment-renderer';
const nodes = Array.from(document.querySelectorAll(commentSelector));
const own = (element, selector) => Array.from(element.querySelectorAll(selector))
  .find(child => child.closest(commentSelector) === element);
const identity = element => {
  const link = own(element, '#published-time-text a,a[href*="lc="]');
  try {return new URL(link.href).searchParams.get('lc');} catch {return null;}
};
return nodes.slice(0, arguments[0]).map(element => {
  const thread = element.closest('ytd-comment-thread-renderer');
  const top = thread?.querySelector(commentSelector);
  const reply = !!element.closest('ytd-comment-replies-renderer');
  const published = own(element, '#published-time-text');
  return {id: identity(element), text: own(element, '#content-text')?.innerText || '',
    parent: reply ? (top ? identity(top) : null) : thread ? 'root' : null,
    _time_text: published?.innerText || null,
    text_complete: false};
}).filter(item => item.id && item.text);
"""


def _receipt(status="FINISHED_BEST_EFFORT", reason="bounded_rendered_dom", warnings=()):
    return dict(
        status=status,
        reason=reason,
        warnings=list(warnings),
        source_version=SOURCE_VERSION,
    )


def _barrier(state):
    """Content quoting an error is never used to classify an access barrier."""
    text = str(state.get("title", "")) + "\n" + str(state.get("text", ""))
    if state.get("status") == 429 or re.search(
        r"too many requests|request has been rate limited|HTTP (?:ERROR )?429",
        text,
        re.I,
    ):
        return "RATE_LIMITED"
    if state.get("status") in {401, 403}:
        return "ACCESS_BLOCKED"
    if state.get("challenge"):
        return "CHALLENGE_REQUIRED"
    if re.search(r"ERR_CERT_|connection is not private|privacy error", text, re.I):
        return "TLS_ERROR"
    if re.search(r"ERR_BLOCKED_BY_CLIENT|blocked by Chrome", text, re.I):
        return "CLIENT_BROWSER_BLOCK"
    if not state.get("content"):
        if re.search(
            r"verify (?:that )?(?:you.re|you are) human|prove your humanity|captcha|checking your browser",
            text,
            re.I,
        ):
            return "CAPTCHA_REQUIRED"
        if re.search(
            r"blocked by network|you.ve been blocked|request has been blocked",
            text,
            re.I,
        ):
            return "ACCESS_BLOCKED"
        if re.search(
            r"sign in to confirm|log in to continue|login required|consent.youtube|before you continue to youtube",
            text,
            re.I,
        ):
            return "LOGIN_OR_CHALLENGE"
    return None


def _timestamp(value):
    if not isinstance(value, str) or not value.strip():
        return None, None, "unknown"
    value = value.strip()
    try:
        return reddit.utc_datetime(value).isoformat(), value, "exact"
    except (ValueError, TypeError, OverflowError):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return None, value, "date_only"
        return (
            None,
            value,
            "relative"
            if re.search(r"\b(?:ago|lalu|yesterday|kemarin)\b", value, re.I)
            else "unknown",
        )


def _reddit_records(capture, target, subreddits):
    """Convert the shared rendered DOM capture without inventing identities."""
    native = reddit.thread_id(target)
    post = capture.get("post")
    if not post or post.get("native_id") != native or not post.get("title"):
        raise reddit.SourceFailure(
            "LAYOUT_UNSUPPORTED", "expected_post_identity_not_found"
        )
    if reddit.thread_id(capture["page_url"]) != native:
        raise ValueError("Reddit navigation reached a different thread")
    if post.get("subreddit", "").lower() not in subreddits:
        raise reddit.SourceFailure("SOURCE_NOT_ALLOWED", "subreddit_outside_allowlist")
    if reddit.thread_id(urljoin(reddit.BASE, post.get("permalink") or "")) != native:
        raise ValueError("Reddit source permalink mismatch")
    root = "t3_" + native
    stamp = reddit.now_iso()
    base = dict(
        root=root,
        observed_at=stamp,
        page_url=capture["page_url"],
        extraction_method=METHOD,
        author_id=None,
        publisher_ref=None,
        subreddit=post["subreddit"],
        text_complete=False,
        flags=["bounded_rendered_dom", "more_replies_not_expanded"],
        score=None,
        comment_count=None,
    )
    published, display, quality = _timestamp(post.get("published_at"))
    records = [
        {
            **base,
            "fullname": root,
            "kind": "post",
            "title": post["title"],
            "text": post.get("text") or "",
            "parent": None,
            "parent_evidence": None,
            "published_at": published,
            "published_display": display,
            "timestamp_quality": quality,
            "score": reddit.parsed_number(post.get("score_display")),
            "comment_count": reddit.parsed_number(post.get("comment_count_display")),
        }
    ]

    def comment_id(value):
        parsed = reddit.safe_web_url(value)
        match = re.fullmatch(
            r"/r/[^/]+/comments/([a-z0-9]+)/comment/([a-z0-9]{3,16})/?", parsed.path
        )
        if not match or match[1] != native:
            raise ValueError("Comment permalink outside expected thread")
        return "t1_" + match[2]

    for item in capture.get("comments", []):
        if (
            not item.get("url")
            or not isinstance(item.get("text"), str)
            or not item["text"].strip()
        ):
            continue
        fullname = comment_id(item["url"])
        parent = comment_id(item["parent_url"]) if item.get("parent_url") else root
        published, display, quality = _timestamp(
            item.get("published_at") or item.get("published_display")
        )
        records.append(
            {
                **base,
                "fullname": fullname,
                "kind": "reply" if parent.startswith("t1_") else "comment",
                "title": None,
                "text": item["text"],
                "parent": parent,
                "parent_evidence": "dom_nesting",
                "published_at": published,
                "published_display": display,
                "timestamp_quality": quality,
                "flags": [*base["flags"], "parent_from_dom_nesting"],
            }
        )
    return records


class _SeleniumSource:
    """One browser operation. The parent enforces the hard process deadline."""

    def __init__(
        self,
        driver,
        platform,
        settings,
        send,
        config,
        *,
        sleep=time.sleep,
        clock=time.monotonic,
    ):
        self.driver, self.platform, self.settings, self.send = (
            driver,
            platform,
            settings,
            send,
        )
        self.selector = SocialCrawler(config)
        self.sleep, self.clock = sleep, clock
        self.deadline = clock() + settings.timeout_seconds
        self.seen, self.records = set(), {}
        self.comments = self.replies = 0
        self.branches = Counter()
        self.warnings = {"public_rendered_snapshot_non_exhaustive"}

    def state(self):
        state = self.driver.execute_script(PAGE_STATE)
        barrier = _barrier(state)
        if barrier:
            raise reddit.SourceFailure(barrier, "visible_browser_access_barrier")
        parsed = urlsplit(state["url"])
        hosts = (
            {"youtube.com", "www.youtube.com", "m.youtube.com"}
            if self.platform == "youtube"
            else {"reddit.com", "www.reddit.com"}
        )
        if parsed.scheme != "https" or parsed.hostname not in hosts:
            raise reddit.SourceFailure(
                "ACCESS_BARRIER", "navigation_left_public_source"
            )
        return state

    def pause(self):
        remaining = self.deadline - self.clock()
        if remaining <= 0:
            raise TimeoutError("operation_deadline")
        # Pace every scroll/reply expansion as well as the outer operations.
        self.sleep(min(max(0.5, self.settings.request_delay), remaining))

    def navigate(self, url):
        from selenium.webdriver.support.ui import WebDriverWait

        self.driver.set_page_load_timeout(min(40, self.settings.timeout_seconds))
        self.driver.set_script_timeout(min(15, self.settings.timeout_seconds))
        self.driver.get(url)
        WebDriverWait(
            self.driver, min(20, self.settings.timeout_seconds), poll_frequency=0.5
        ).until(lambda _: self.state().get("content"))

    def selected_root(self, title, text, published):
        rows = {
            "Contents": [
                dict(
                    object_type="post",
                    object_key="root",
                    title=title,
                    text_source=text,
                    published_at=published,
                )
            ]
        }
        return bool(self.selector._select(rows)[0])

    def search(self, target):
        url = (
            "https://www.youtube.com/results?" + urlencode({"search_query": target})
            if self.platform == "youtube"
            else target
        )
        if self.platform == "reddit":
            reddit.safe_web_url(url)
        self.navigate(url)
        stalled = 0
        for _ in range(300):
            self.state()
            before = len(self.seen)
            for value in self.driver.execute_script(SEARCH_LINKS, self.platform):
                try:
                    canonical = (
                        youtube.video_url(value)
                        if self.platform == "youtube"
                        else reddit.thread_url(value)
                    )
                except (ValueError, TypeError):
                    continue
                if canonical in self.seen:
                    continue
                self.seen.add(canonical)
                self.send(("candidate", dict(url=canonical, discovered_from=url)))
                if len(self.seen) >= self.settings.search_results:
                    return
            stalled = stalled + 1 if len(self.seen) == before else 0
            if stalled >= 4:
                self.warnings.add("search_scroll_stalled")
                return
            self.driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight)"
            )
            self.pause()

    def youtube(self, target):
        self.navigate(target)
        raw = self.driver.execute_script(YOUTUBE_VIDEO)
        expected = parse_qs(urlsplit(target).query)["v"][0]
        if raw.get("id") != expected or not raw.get("title"):
            raise reddit.SourceFailure(
                "LAYOUT_UNSUPPORTED", "video_identity_or_title_not_verified"
            )
        raw["observed_at"] = reddit.now_iso()
        self.send(("video", raw))
        if not self.selected_root(
            raw["title"],
            raw.get("description") or "",
            _timestamp(raw.get("published"))[0],
        ):
            return
        self.driver.execute_script(
            "document.querySelector('video')?.pause();document.querySelector('ytd-comments')?.scrollIntoView()"
        )
        self.pause()
        self._youtube_sort()
        stalled = 0
        for _ in range(500):
            self.state()
            before = len(self.seen)
            for item in self.driver.execute_script(
                YOUTUBE_COMMENTS, self.settings.max_comments + 200
            ):
                identity = item["id"]
                if identity in self.seen or not youtube.COMMENT_ID.fullmatch(identity):
                    continue
                parent = item.get("parent")
                if parent and parent != "root":
                    if (
                        self.replies >= self.settings.max_replies
                        or self.branches[parent] >= self.settings.max_replies_per_thread
                    ):
                        continue
                    self.replies += 1
                    self.branches[parent] += 1
                item["observed_at"] = reddit.now_iso()
                self.send(("comment", item))
                self.seen.add(identity)
                if len(self.seen) >= self.settings.max_comments:
                    self.warnings.add("comment_cap_reached")
                    return
            stalled = stalled + 1 if len(self.seen) == before else 0
            if stalled >= 5:
                self.warnings.add("comment_scroll_stalled_or_comments_disabled")
                return
            expanded = self._youtube_reply()
            if not expanded:
                self.driver.execute_script(
                    "window.scrollBy(0, Math.max(800, innerHeight))"
                )
            self.pause()

    def _youtube_sort(self):
        from selenium.common.exceptions import WebDriverException
        from selenium.webdriver.common.by import By

        wanted = (
            ("newest first", "terbaru", "paling baru")
            if self.settings.sort == "new"
            else ("top comments", "komentar teratas")
        )
        try:
            buttons = self.driver.find_elements(
                By.CSS_SELECTOR, "ytd-comments-header-renderer #sort-menu"
            )
            if buttons:
                buttons[0].click()
                self.pause()
                for item in self.driver.find_elements(
                    By.CSS_SELECTOR, "tp-yt-paper-listbox a,tp-yt-paper-item"
                ):
                    if item.is_displayed() and item.text.strip().casefold() in wanted:
                        item.click()
                        self.pause()
                        return
        except WebDriverException:
            pass
        self.warnings.add("requested_comment_sort_not_verified")

    def _youtube_reply(self):
        from selenium.common.exceptions import WebDriverException
        from selenium.webdriver.common.by import By

        if self.replies >= self.settings.max_replies:
            return False
        for button in self.driver.find_elements(
            By.CSS_SELECTOR,
            "ytd-comment-replies-renderer #more-replies button,ytd-comment-replies-renderer #more-replies-sub-thread button",
        ):
            try:
                parent = self.driver.execute_script(
                    """
                  const top = arguments[0].closest('ytd-comment-thread-renderer')
                    ?.querySelector('ytd-comment-view-model,ytd-comment-renderer');
                  const link = top?.querySelector('#published-time-text a,a[href*="lc="]');
                  try {return new URL(link.href).searchParams.get('lc');} catch {return null;}
                """,
                    button,
                )
                if (
                    parent
                    and self.branches[parent] < self.settings.max_replies_per_thread
                    and button.is_displayed()
                ):
                    button.click()
                    return True
            except WebDriverException:
                continue
        return False

    def reddit(self, target):
        self.navigate(target)
        source = (ROOT / "Crawler/Backend/Reddit/rendered_thread_dom.mjs").read_text()
        script = (
            source.replace(
                "export function captureRenderedThread",
                "function captureRenderedThread",
            )
            + "\nreturn captureRenderedThread(arguments[0]);"
        )
        stalled = 0
        root_checked = False
        for _ in range(500):
            self.state()
            capture = self.driver.execute_script(
                script,
                dict(
                    nativeId=reddit.thread_id(target),
                    maxComments=self.settings.max_comments,
                ),
            )
            if capture.get("post"):
                rows = _reddit_records(capture, target, self.settings.subreddits)
            else:
                # Older public HTML still uses the existing tested parser.
                html = self.driver.page_source
                page = reddit.HtmlPage(
                    html,
                    self.driver.current_url,
                    reddit.now_iso(),
                    None,
                    len(html.encode()),
                    reddit.digest(html),
                )
                rows, _ = reddit.RedditHtmlParser(page).thread(reddit.thread_id(target))
                for row in rows:
                    row["extraction_method"] = METHOD
                if rows[0].get("subreddit", "").lower() not in self.settings.subreddits:
                    raise reddit.SourceFailure(
                        "SOURCE_NOT_ALLOWED", "subreddit_outside_allowlist"
                    )
            before = len(self.seen)
            for row in rows:
                self.records.setdefault(row["fullname"], row)
            for kind, row in reddit.bounded_events(
                list(self.records.values()), self.settings
            ):
                if kind == "record" and row["fullname"] not in self.seen:
                    self.send((kind, row))
                    self.seen.add(row["fullname"])
            if not root_checked:
                post = rows[0]
                root_checked = True
                if not self.selected_root(
                    post["title"], post["text"], post["published_at"]
                ):
                    return
            if len(self.seen) - 1 >= self.settings.max_comments:
                self.warnings.add("comment_cap_reached")
                return
            stalled = stalled + 1 if len(self.seen) == before else 0
            if stalled >= 5:
                self.warnings.add("more_replies_not_expanded")
                return
            self.driver.execute_script("window.scrollBy(0, Math.max(800, innerHeight))")
            self.pause()


def _create_driver(options):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service

    chrome = webdriver.ChromeOptions()
    chrome.page_load_strategy = "eager"
    if options.get("headless"):
        chrome.add_argument("--headless=new")
    chrome.add_argument("--window-size=1440,1000")
    chrome.add_argument("--lang=en-US")
    chrome.add_argument("--mute-audio")
    chrome.add_argument("--disable-dev-shm-usage")
    if options.get("chrome_binary"):
        chrome.binary_location = options["chrome_binary"]
    if options.get("remote_url"):
        return webdriver.Remote(command_executor=options["remote_url"], options=chrome)
    os.environ.setdefault("SE_CACHE_PATH", str(ROOT / ".cache/selenium"))
    os.environ.setdefault("SE_AVOID_STATS", "true")
    os.environ.setdefault("SE_TIMEOUT", "45")
    return webdriver.Chrome(
        service=Service(
            executable_path=options.get("driver_path"), log_output=os.devnull
        ),
        options=chrome,
    )


def selenium_worker(
    operation, target, settings, pipe, *, platform, browser_options, config
):
    """Stream evidence before completion; the original supervisor can retain it."""
    if os.name == "posix":
        os.setsid()
    driver = source = None
    try:
        driver = _create_driver(browser_options)
        source = _SeleniumSource(
            driver, platform, SimpleNamespace(**settings), pipe.send, config
        )
        if operation == "search":
            source.search(target)
        elif platform == "youtube" and operation == "video":
            source.youtube(target)
        elif platform == "reddit" and operation == "thread":
            source.reddit(target)
        else:
            raise ValueError("Unsupported Selenium operation")
        result = _receipt(warnings=sorted(source.warnings))
    except ImportError:
        result = _receipt("DEPENDENCY_MISSING", "install_requirements_selenium")
    except reddit.SourceFailure as error:
        result = _receipt(error.code, error.reason)
    except Exception as error:
        status = (
            "TIMEOUT"
            if isinstance(error, TimeoutError)
            or type(error).__name__ == "TimeoutException"
            else "SOURCE_ERROR"
        )
        reason = "browser_operation_failed_partial_events_preserved"
        try:
            if driver:
                status = _barrier(driver.execute_script(PAGE_STATE)) or status
        except Exception:
            pass
        result = _receipt(status, reason, [type(error).__name__])
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass
    try:
        pipe.send(("done", result))
    finally:
        pipe.close()


class SocialCrawlerSelenium(SocialCrawler):
    """Drop-in SocialCrawler with Selenium for both platforms and shared exports."""

    def __init__(
        self,
        config=None,
        *,
        headless=False,
        chrome_binary=None,
        driver_path=None,
        remote_url=None,
        workers=None,
        progress=None,
        **kwargs,
    ):
        super().__init__(config, workers=workers, **kwargs)
        self.browser_options = dict(
            headless=headless,
            chrome_binary=chrome_binary,
            driver_path=driver_path,
            remote_url=remote_url,
        )
        if type(headless) is not bool:
            raise ValueError("headless must be boolean")
        if remote_url:
            parsed = urlsplit(remote_url)
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username
                or parsed.password
                or parsed.query
                or parsed.fragment
            ):
                raise ValueError(
                    "remote_url must be a Selenium server URL without credentials/query"
                )
        self.progress = progress
        self._synthetic = bool(workers)
        for name in self.config["platforms"]:
            if self.config["platforms"][name].get("import_checkpoint_dir"):
                raise ValueError(
                    "Selenium uses live pages; remove import_checkpoint_dir"
                )
            if not workers or name not in workers:
                entry = partial(
                    selenium_worker,
                    platform=name,
                    browser_options=self.browser_options,
                    config=self.config,
                )
                self.workers[name] = partial(youtube.run_worker, worker_entry=entry)

    def plan(self):
        return {
            **super().plan(),
            "acquisition_backend": "selenium",
            "selenium_version": self.selenium_version(),
            "browser": deepcopy(self.browser_options),
            "legacy_reddit_backend_overridden": True,
            "isolation": "fresh_guest_profile_per_operation_with_hard_process_deadline",
        }

    @staticmethod
    def selenium_version():
        try:
            return importlib.metadata.version("selenium")
        except importlib.metadata.PackageNotFoundError:
            return None

    def _source_metadata(self, name, settings):
        return dict(
            producer_version="social-crawler-selenium:" + VERSION,
            extraction_method=METHOD,
            access_mode="public_guest_isolated_selenium",
        )

    def _legacy_settings(self, name, settings):
        result = super()._legacy_settings(name, settings)
        delay = self.config["delay"]
        pause = delay["seconds"] if delay["mode"] == "fixed" else delay["max_seconds"]
        from dataclasses import replace

        return replace(result, request_delay=pause)

    def _checkpoint_items(self, settings):
        return []

    def _execute(
        self, name, operation, target, settings, platform, deadline, cached=None
    ):
        if self.progress:
            self.progress(
                dict(
                    event="started",
                    platform=name,
                    operation=operation,
                    target=target,
                    at=reddit.now_iso(),
                )
            )
        events, result = super()._execute(
            name, operation, target, settings, platform, deadline
        )
        result = {**result, "source_version": SOURCE_VERSION}
        if self.progress:
            self.progress(
                dict(
                    event="finished",
                    platform=name,
                    operation=operation,
                    status=result["status"],
                    captured_events=len(events),
                    target=target,
                    at=reddit.now_iso(),
                )
            )
        return events, result

    def _normalize(self, name, events, url, origin, factory, version):
        if name == "reddit":
            return super()._normalize(name, events, url, origin, factory, version)
        rows = {key: [] for key in reddit.TABLES}
        dataset = reddit.Dataset(
            factory, SimpleNamespace(write=lambda table, row: rows[table].append(row))
        )
        vid = parse_qs(urlsplit(url).query)["v"][0]
        root = factory.key("youtube", youtube.VIDEO_NAMESPACE, vid)
        invalid = 0
        for kind, raw in events:
            if kind not in {"video", "comment"}:
                continue
            try:
                identity = raw["id"]
                if (
                    kind == "video"
                    and identity != vid
                    or kind == "comment"
                    and not youtube.COMMENT_ID.fullmatch(identity)
                ):
                    raise ValueError("Source identity mismatch")
                parent = raw.get("parent")
                is_reply = (
                    kind == "comment"
                    and isinstance(parent, str)
                    and parent != "root"
                    and bool(youtube.COMMENT_ID.fullmatch(parent))
                )
                parent_key = (
                    root
                    if parent == "root"
                    else factory.key("youtube", youtube.COMMENT_NAMESPACE, parent)
                    if is_reply
                    else None
                )
                stamp, display, quality = _timestamp(
                    raw.get("published") if kind == "video" else raw.get("_time_text")
                )
                flags = ["bounded_rendered_dom", "hidden_comments_unknown"]
                if kind == "comment":
                    flags.append(
                        "parent_from_dom_nesting"
                        if parent_key
                        else "parent_unknown_not_assumed_root"
                    )
                record = reddit.ContentInput(
                    platform="youtube",
                    namespace=youtube.VIDEO_NAMESPACE
                    if kind == "video"
                    else youtube.COMMENT_NAMESPACE,
                    native_id=identity,
                    object_type="post"
                    if kind == "video"
                    else "reply"
                    if is_reply
                    else "comment",
                    canonical_url=url
                    if kind == "video"
                    else url + "&lc=" + quote(identity, safe=""),
                    page_url=url,
                    title=raw.get("title") if kind == "video" else None,
                    text_source=raw.get("description", "")
                    if kind == "video"
                    else raw["text"],
                    text_complete=False,
                    thread_root_key=root,
                    parent_key=parent_key,
                    published_at=stamp,
                    published_display=display,
                    timestamp_quality=quality,
                    observed_at=raw.get("observed_at") or reddit.now_iso(),
                    discovered_from=origin,
                    extraction_method=METHOD,
                    adapter_version=SOURCE_VERSION,
                    quality_flags=tuple(flags),
                )
                dataset.add_content(record)
            except (ValueError, KeyError, TypeError, OverflowError):
                invalid += 1
        dataset.finish_relations()
        return rows, invalid

    def run(self, output_dir=None):
        if output_dir is None:
            from uuid import uuid4

            output_dir = (
                ROOT
                / "outputs"
                / (
                    "social_selenium_"
                    + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_")
                    + uuid4().hex[:8]
                )
            )
        return super().run(output_dir)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=ROOT / "config/social_crawler.json"
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--from-bundle", type=Path)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--chrome-binary")
    parser.add_argument("--driver-path")
    parser.add_argument("--remote-url", help="Optional Selenium Grid URL")
    args = parser.parse_args()
    try:

        def progress(event):
            print(json.dumps(event, ensure_ascii=False), file=sys.stderr, flush=True)

        crawler = SocialCrawlerSelenium(
            args.config,
            headless=args.headless,
            chrome_binary=args.chrome_binary,
            driver_path=args.driver_path,
            remote_url=args.remote_url,
            progress=progress,
        )
        if args.from_bundle:
            if args.dry_run or args.output_dir is None:
                raise ValueError(
                    "--from-bundle requires a new --output-dir and no --dry-run"
                )
            result = crawler.export_compact(args.from_bundle, args.output_dir)
        else:
            result = crawler.plan() if args.dry_run else crawler.run(args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
        return (
            0
            if args.dry_run or result["status"] in {"TARGET_MET", "EXPORTED"}
            else 130
            if result["status"] == "INTERRUPTED"
            else 2
        )
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(
            json.dumps(
                dict(
                    status="CONFIG_OR_RUNTIME_ERROR",
                    error_type=type(error).__name__,
                    reason=str(error),
                )
            ),
            flush=True,
        )
        return 2


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    raise SystemExit(main())
