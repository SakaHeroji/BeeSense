"""Native TikTok browser crawler with the shared Excel and native-ID contract."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import math
import multiprocessing as mp
import os
import re
import signal
import time
import uuid
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, urlencode, urlsplit

from Crawler.Backend import social_crawler as core
from Crawler.Backend.crawler_config import (
    DEFAULT_CONFIG_PATH,
    expand_config,
    read_config,
)
from Crawler.Backend.crawler_limits import reached
from Crawler.Backend.Reddit import crawl_reddit_single as contract
from Crawler.Backend.social_export import SocialExportMixin

VERSION = "2.6.1"
SOURCE_VERSION = "BeeSenseNative:1.3.0;Playwright:1.64.1"
METHOD = "beesense_native_browser"
CHROME_METHOD = "beesense_existing_chrome_capture"
CHROME_VERSION = "BeeSenseChromeCapture:1.0.0"
ROOT = Path(__file__).resolve().parents[2]
DEFAULTS = dict(
    enabled=True,
    urls=[],
    queries=[],
    hashtags=[],
    min_posts=1000,
    min_comments_per_post=0,
    max_posts=None,
    max_candidates=None,
    max_comments=None,
    max_replies=None,
    max_replies_per_thread=None,
    search_results=500,
    sort="relevance",
    headless=True,
    browser="chromium",
    auth_file="config/auth.json",
    request_interval_seconds=3,
    scroll_pause_seconds=3,
    idle_scroll_limit=3,
    manual_wait_seconds=0,
    manual_poll_seconds=2,
    manual_profile_dir=".cache/tiktok/chromium-profile",
)


class AuthError(ValueError):
    """A local token is missing or ambiguous; no secret enters the message."""


def native_id(value):
    value = str(value)
    if not re.fullmatch(r"[1-9][0-9]{0,24}", value):
        raise ValueError("TikTok native ID must be a positive decimal string")
    return value


def parse_url(value):
    if not isinstance(value, str):
        raise ValueError("TikTok URL must be a string")
    url = urlsplit(value)
    match = re.fullmatch(
        r"/@([A-Za-z0-9_.]{1,40})/(?:video|photo)/([1-9][0-9]{0,24})/?", url.path
    )
    if (
        url.scheme != "https"
        or url.netloc not in {"www.tiktok.com", "tiktok.com"}
        or not match
        or url.fragment
    ):
        raise ValueError("Expected a canonical HTTPS TikTok video or photo URL")
    params = parse_qs(url.query, keep_blank_values=True)
    if params and (set(params) != {"comment_id"} or len(params["comment_id"]) != 1):
        raise ValueError("Unsupported TikTok URL query")
    comment = native_id(params["comment_id"][0]) if params else None
    return match[2], match[1], comment


def post_url(value):
    """Stable internal root identity; the Excel hyperlink keeps the source author."""
    ident, _, comment = parse_url(value)
    if comment:
        raise ValueError("Expected a TikTok post URL")
    return f"https://www.tiktok.com/@_/video/{ident}"


def platform_configuration(value):
    if not isinstance(value, dict) or set(value) - set(DEFAULTS):
        raise ValueError(
            "TikTok settings must contain known fields; credentials belong in auth.json"
        )
    p = {**deepcopy(DEFAULTS), **deepcopy(value)}
    if (
        type(p["manual_wait_seconds"]) is not int
        or not 0 <= p["manual_wait_seconds"] <= 3600
    ):
        raise ValueError("Invalid tiktok.manual_wait_seconds")
    if (
        type(p["manual_poll_seconds"]) is not int
        or not 1 <= p["manual_poll_seconds"] <= 30
    ):
        raise ValueError("Invalid tiktok.manual_poll_seconds")
    if (
        not isinstance(p["manual_profile_dir"], str)
        or not p["manual_profile_dir"].strip()
    ):
        raise ValueError("Invalid tiktok.manual_profile_dir")
    profile = (ROOT / p["manual_profile_dir"]).resolve()
    if not profile.is_relative_to((ROOT / ".cache/tiktok").resolve()):
        raise ValueError(
            "TikTok profile must be in the private .cache/tiktok directory"
        )
    if p["manual_wait_seconds"] and (p["headless"] or p["browser"] != "chromium"):
        raise ValueError("Manual validation requires visible Chromium")
    if type(p["enabled"]) is not bool:
        raise ValueError("tiktok.enabled must be boolean")
    for key in (
        "min_posts",
        "min_comments_per_post",
        "max_posts",
        "max_candidates",
        "max_comments",
        "max_replies",
        "max_replies_per_thread",
        "search_results",
    ):
        v = p[key]
        nullable = key.startswith("max_")
        low = (
            0
            if key
            in {
                "min_comments_per_post",
                "max_comments",
                "max_replies",
                "max_replies_per_thread",
            }
            else 1
        )
        if not (nullable and v is None) and (
            type(v) is not int or not low <= v <= 1000000
        ):
            raise ValueError("Invalid tiktok." + key)
    if p["max_posts"] is not None and p["max_posts"] < p["min_posts"]:
        raise ValueError("tiktok.max_posts must be at least min_posts")
    if p["max_comments"] is not None and p["max_comments"] < p["min_comments_per_post"]:
        raise ValueError("TikTok minimum comments exceeds acquisition cap")
    for key in (
        "request_interval_seconds",
        "scroll_pause_seconds",
        "idle_scroll_limit",
    ):
        if type(p[key]) is not int or not 1 <= p[key] <= 3600:
            raise ValueError("Invalid tiktok." + key)
    for key in ("urls", "queries", "hashtags"):
        if (
            not isinstance(p[key], list)
            or len(p[key]) > 100
            or any(
                not isinstance(s, str)
                or not s.strip()
                or len(s) > 300
                or any(ord(c) < 32 for c in s)
                for s in p[key]
            )
        ):
            raise ValueError("Invalid tiktok." + key)
        p[key] = list(dict.fromkeys(s.strip() for s in p[key]))
    for url in p["urls"]:
        post_url(url)
    if any(not re.fullmatch(r"[\w]{1,100}", tag, re.UNICODE) for tag in p["hashtags"]):
        raise ValueError("TikTok hashtags must omit # and spaces")
    if p["sort"] != "relevance":
        raise ValueError("TikTok browser exposes source relevance ordering only")
    if type(p["headless"]) is not bool:
        raise ValueError("tiktok.headless must be boolean")
    if p["browser"] not in {"chromium", "firefox", "webkit"}:
        raise ValueError("tiktok.browser must be chromium, firefox or webkit")
    if not isinstance(p["auth_file"], str) or not p["auth_file"].strip():
        raise ValueError("tiktok.auth_file must be a path")
    if p["enabled"] and not (p["urls"] or p["queries"] or p["hashtags"]):
        raise ValueError("TikTok requires queries, hashtags or URLs")
    return p


def auth_material(path):
    """Read exactly one TikTok token without serializing any authentication data."""
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    try:
        if p.stat().st_size > 1000000:
            raise ValueError
        data = json.loads(p.read_text(encoding="utf-8"))
        entries = [
            a
            for a in data
            if isinstance(a, dict) and str(a.get("sosmed", "")).casefold() == "tiktok"
        ]
        if len(entries) != 1:
            raise ValueError
        values = {
            entries[0][key].strip()
            for key in ("msToken", "ms_token", "mstoken", "sessionid")
            if isinstance(entries[0].get(key), str) and entries[0][key].strip()
        }
        if len(values) != 1:
            raise ValueError
        token = values.pop()
        if len(token) > 4096 or any(ord(c) < 33 for c in token):
            raise ValueError
        return token
    except (OSError, ValueError, TypeError, KeyError):
        raise AuthError(
            "TikTok auth requires one entry with msToken (or sessionid containing msToken)"
        ) from None


def normalize_item(item, *, discovered_from=None, method=METHOD):
    ident = native_id(item["id"])
    root = native_id(item.get("video_id", ident))
    kind = item.get("kind", "post")
    if kind not in {"post", "comment", "reply"} or (kind == "post") != (ident == root):
        raise ValueError("Inconsistent TikTok root identity")
    url = item["link"]
    url_root, _, url_comment = parse_url(url)
    if url_root != root or (
        url_comment != ident if kind != "post" else url_comment is not None
    ):
        raise ValueError("TikTok native ID and URL disagree")
    text = item.get("description") if kind == "post" else item.get("text")
    if text is None:
        text = ""
    if not isinstance(text, str):
        raise ValueError("TikTok text must be a string")
    stamp = item.get("created_at")
    stamp = contract.utc_datetime(stamp).isoformat() if stamp else None
    parent = native_id(item["parent_comment_id"]) if kind == "reply" else root
    namespace = "video" if kind == "post" else "comment"
    return contract.ContentInput(
        platform="tiktok",
        namespace=namespace,
        native_id=ident,
        object_type=kind,
        canonical_url=url,
        page_url=url.split("?", 1)[0],
        thread_root_key=f"tiktok:video:{root}",
        parent_key=None
        if kind == "post"
        else f"tiktok:{'comment' if kind == 'reply' else 'video'}:{parent}",
        text_source=text,
        title=None,
        published_at=stamp,
        published_display=item.get("published_display") or item.get("created_at"),
        timestamp_quality="exact" if stamp else "unknown",
        observed_at=item.get("observed_at") or contract.now_iso(),
        text_complete=False,
        discovered_from=discovered_from,
        extraction_method=method,
        adapter_version=VERSION,
        quality_flags=("upstream_text_completeness_unknown",),
    )


class TikTokAdapter:
    def __init__(self, factory, dataset, version=None):
        self.dataset, self.seen = dataset, set()
        self.method = CHROME_METHOD if version == CHROME_VERSION else METHOD
        if version in {
            "BeeSenseChromeLive:1.0.0",
            "BeeSenseChromeLive:1.1.0",
            "BeeSenseChromeLive:1.2.0",
            "BeeSenseChromeLive:1.2.1",
        }:
            self.method = "beesense_existing_chrome_live"

    def accept(self, kind, item, url, origin):
        raw = normalize_item(item, discovered_from=origin, method=self.method)
        if native_id(parse_url(url)[0]) != raw.thread_root_key.rsplit(":", 1)[1]:
            raise ValueError("TikTok event belongs to another video")
        key = (raw.namespace, raw.native_id)
        if key in self.seen:
            return
        self.seen.add(key)
        stats = (
            item.get("stats", {})
            if raw.object_type == "post"
            else {
                "like_count": item.get("like_count"),
                "reply_count": item.get("reply_count"),
            }
        )
        self.dataset.add_content(
            raw,
            [
                (k, v, "count")
                for k, v in stats.items()
                if k
                in {
                    "play_count",
                    "like_count",
                    "comment_count",
                    "share_count",
                    "save_count",
                    "repost_count",
                    "reply_count",
                }
            ],
        )


class AccessBarrier(RuntimeError):
    pass


class SearchUnavailable(RuntimeError):
    """The browser observed no native video candidates on the search page."""


def source_has_more(body):
    """Missing pagination metadata never proves that all comments were loaded."""
    data = body.get("data") if isinstance(body.get("data"), dict) else body
    if not isinstance(data.get("comments"), list):
        return None
    value = data.get("has_more")
    if value in (False, 0, "0"):
        return False
    if value in (True, 1, "1"):
        return True
    return None


def error_receipt(error):
    """Exception messages may contain signed URLs; emit only fixed reason codes."""
    name = type(error).__name__
    if isinstance(error, ImportError):
        status, reason = "DEPENDENCY_MISSING", "install_requirements_tiktok"
    elif isinstance(error, SearchUnavailable):
        status, reason = (
            "CLIENT_UPGRADE_REQUIRED",
            "tiktok_browser_no_visible_search_results",
        )
    elif isinstance(error, AccessBarrier):
        status, reason = "ACCESS_BLOCKED", "tiktok_access_barrier"
    elif isinstance(error, AuthError):
        status, reason = "SESSION_INVALID", "tiktok_auth_missing_or_ambiguous"
    elif isinstance(error, TimeoutError) or name == "TimeoutError":
        status, reason = "TIMEOUT", "tiktok_request_deadline"
    else:
        status, reason = "SOURCE_ERROR", "tiktok_source_call_failed"
    return dict(
        status=status, reason=reason, warnings=[name], source_version=SOURCE_VERSION
    )


def embedded_videos(data):
    """Find video objects in hydration and browser response JSON."""
    if isinstance(data, dict):
        if (
            "id" in data
            and "author" in data
            and ("desc" in data or "createTime" in data)
        ):
            yield data
        else:
            for value in data.values():
                yield from embedded_videos(value)
    elif isinstance(data, list):
        for value in data:
            yield from embedded_videos(value)


def retry_after(value, *, now=None):
    """Honor server seconds or an HTTP date; never put headers in receipts."""
    from email.utils import parsedate_to_datetime

    try:
        seconds = float(value)
    except (TypeError, ValueError):
        try:
            stamp = parsedate_to_datetime(value).timestamp()
            seconds = stamp - (time.time() if now is None else now)
        except (TypeError, ValueError, OverflowError):
            return 60
    return max(0, math.ceil(seconds)) if math.isfinite(seconds) else 60


class NativeTikTokClient(SocialExportMixin):
    """One ordinary Playwright session; observe public UI traffic, never forge APIs."""

    API_PATHS = ("/api/search/", "/api/comment/", "/api/item/", "/api/challenge/")

    def __init__(self, config, *, factory=None):
        self.config = config
        self.settings = config["platforms"]["tiktok"]
        self.include = contract.KeywordMatcher(config["include_keywords"])
        self.exclude = contract.KeywordMatcher(config["exclude_keywords"])
        self.factory = factory
        self.playwright = self.browser = self.context = self.page = None
        self.barrier = None
        self.barrier_reason = None
        self.retry_after_seconds = None
        self.deadline = math.inf
        self.last_request = None
        delay = config["delay"]
        self.interval = max(
            self.settings["request_interval_seconds"],
            delay.get("seconds", delay.get("max_seconds", 0)),
        )
        self.requests, self.statuses = 0, Counter()
        self.endpoints = Counter()
        self.invalid_candidates = 0
        self.pending = set()
        self.comment_pages, self.reply_expected = {}, {}
        self.request_epochs = {}
        self.epoch = 0
        self.capture_error = None
        self.operation = None
        self.operation_warnings = []
        self.video_buffer, self.comment_buffer = [], []
        self.seen, self.comments, self.replies = set(), 0, 0
        self.per_thread = Counter()
        self.root = None
        self.emit = None
        self.pacing_lock = asyncio.Lock()
        self.cooldown_file = ROOT / ".cache/tiktok/native_cooldown.json"
        self.manual_pending = False
        self.manual_validated = False
        self.resume_url = None
        self.control_file = ROOT / f".cache/tiktok/manual_control_{os.getpid()}.json"

    def remaining(self):
        left = self.deadline - time.monotonic()
        if left <= 0:
            raise TimeoutError
        return left

    def check(self):
        self.remaining()
        if self.barrier:
            raise AccessBarrier
        if self.capture_error:
            raise self.capture_error

    async def pause(self, seconds):
        self.check()
        if seconds >= self.remaining():
            raise TimeoutError
        await asyncio.sleep(seconds)
        self.check()

    def load_cooldown(self):
        try:
            until = json.loads(self.cooldown_file.read_text())["not_before"]
            left = float(until) - time.time()
            if math.isfinite(left) and left > 0:
                self.barrier = "RATE_LIMITED"
                self.barrier_reason = "persisted_server_retry_after"
                self.retry_after_seconds = math.ceil(left)
                raise AccessBarrier
        except (OSError, ValueError, KeyError, TypeError):
            pass

    def save_cooldown(self):
        self.cooldown_file.parent.mkdir(parents=True, exist_ok=True)
        temp = self.cooldown_file.with_suffix(f".{os.getpid()}.tmp")
        temp.write_text(
            json.dumps({"not_before": time.time() + self.retry_after_seconds})
        )
        os.chmod(temp, 0o600)
        temp.replace(self.cooldown_file)

    @classmethod
    def relevant(cls, request):
        url = urlsplit(request.url)
        return url.hostname in {"www.tiktok.com", "tiktok.com"} and (
            request.resource_type == "document" or url.path.startswith(cls.API_PATHS)
        )

    async def route(self, route):
        if self.manual_pending and self.barrier != "RATE_LIMITED":
            await route.continue_()
            return
        if self.barrier:
            await route.abort()
            return
        if self.relevant(route.request):
            async with self.pacing_lock:
                if self.last_request is not None:
                    wait = max(
                        0, self.interval - (time.monotonic() - self.last_request)
                    )
                    if wait:
                        await self.pause(wait)
                self.check()
                self.last_request = time.monotonic()
        if self.barrier:
            await route.abort()
        else:
            await route.continue_()

    def requested(self, request):
        if self.relevant(request):
            self.request_epochs[request] = self.epoch

    def response(self, response):
        if not self.relevant(response.request):
            return
        self.requests += 1
        self.statuses[str(response.status)] += 1
        path = urlsplit(response.url).path
        self.endpoints[
            next((p for p in self.API_PATHS if path.startswith(p)), "document")
        ] += 1
        if response.status in {401, 403, 429}:
            self.barrier = (
                "RATE_LIMITED"
                if response.status == 429
                else "LOGIN_REQUIRED"
                if response.status == 401
                else "ACCESS_BLOCKED"
            )
            self.barrier_reason = "http_access_status"
            if response.status == 429:
                self.retry_after_seconds = retry_after(
                    response.headers.get("retry-after")
                )
                self.save_cooldown()
        elif response.status >= 500:
            self.interval = max(self.interval * 2, 5)
            self.operation_warnings.append("server_error_slowed_pacing")
        epoch = self.request_epochs.pop(response.request, None)
        path = urlsplit(response.url).path
        if (
            epoch == self.epoch
            and path.startswith(self.API_PATHS)
            and response.status == 200
        ):
            task = asyncio.create_task(self.capture(response, epoch))
            self.pending.add(task)
            task.add_done_callback(self.captured)

    def captured(self, task):
        self.pending.discard(task)
        if not task.cancelled() and task.exception() is not None:
            self.capture_error = task.exception()

    async def capture(self, response, epoch):
        if epoch != self.epoch:
            return
        try:
            body = await response.json()
        except Exception as error:
            if epoch != self.epoch:
                return
            if isinstance(error, (ValueError, TypeError)):
                self.barrier = "ACCESS_BLOCKED"
                self.barrier_reason = "native_api_empty_or_invalid_json"
                return
            raise
        if epoch != self.epoch:
            return
        if not isinstance(body, dict):
            self.capture_error = ValueError("Unexpected TikTok response shape")
            return
        if body.get("type") == "verify":
            self.barrier = "CAPTCHA_REQUIRED"
            self.barrier_reason = "native_api_verification_required"
            return
        code = body.get("status_code", body.get("statusCode", 0))
        if code in {2483, 2484}:
            self.barrier = "LOGIN_REQUIRED" if code == 2483 else "RATE_LIMITED"
            self.barrier_reason = "native_api_access_status"
            if code == 2484:
                self.retry_after_seconds = 60
                self.save_cooldown()
            return
        parsed = urlsplit(response.url)
        params = parse_qs(parsed.query)
        if self.operation == "search":
            expected = self.spec.get("query")
            supplied = params.get("keyword", [expected])[0]
            if expected is None or supplied == expected:
                self.video_buffer.extend(embedded_videos(body))
        elif parsed.path.startswith("/api/comment/"):
            root = params.get("aweme_id", params.get("item_id", [None]))[0]
            if root is not None and root != self.target_id:
                return
            parent = (
                params.get("comment_id", [None])[0]
                if "/reply/" in parsed.path
                else None
            )
            self.comment_pages[parent] = source_has_more(body)
            data = body.get("data") if isinstance(body.get("data"), dict) else body
            self.comment_buffer.extend(
                (row, parent) for row in data.get("comments") or []
            )
        else:
            self.video_buffer.extend(embedded_videos(body))

    async def start(self):
        self.load_cooldown()
        token = auth_material(self.settings["auth_file"])
        if self.factory is None:
            from playwright.async_api import async_playwright

            self.factory = async_playwright
        self.playwright = await self.factory().start()
        if self.settings["manual_wait_seconds"]:
            profile = ROOT / self.settings["manual_profile_dir"]
            profile.mkdir(parents=True, exist_ok=True)
            os.chmod(profile, 0o700)
            self.context = await self.playwright.chromium.launch_persistent_context(
                str(profile), headless=False
            )
        else:
            self.browser = await getattr(
                self.playwright, self.settings["browser"]
            ).launch(headless=self.settings["headless"])
            self.context = await self.browser.new_context()
        await self.context.add_cookies(
            [
                dict(
                    name="msToken",
                    value=token,
                    domain=".tiktok.com",
                    path="/",
                    secure=True,
                )
            ]
        )
        self.context.on("request", self.requested)
        self.context.on("response", self.response)
        await self.context.route("**/*", self.route)
        self.page = await self.context.new_page()
        self.page.set_default_navigation_timeout(self.config["timeout_seconds"] * 1000)

    async def manual_validation(self):
        """Pause automation until the human confirms in the local control channel."""
        if self.barrier == "RATE_LIMITED":
            raise AccessBarrier
        self.manual_pending = True
        wait_id = uuid.uuid4().hex
        self.control_file.parent.mkdir(parents=True, exist_ok=True)
        self.control_file.write_text(
            json.dumps({"wait_id": wait_id, "action": "waiting"})
        )
        os.chmod(self.control_file, 0o600)
        self.emit(
            "manual_validation",
            dict(
                wait_id=wait_id,
                control_file=str(self.control_file),
                wait_seconds=self.settings["manual_wait_seconds"],
                reason=self.barrier_reason or "initial_manual_session_check",
            ),
        )
        until = min(
            self.deadline, time.monotonic() + self.settings["manual_wait_seconds"]
        )
        try:
            while time.monotonic() < until:
                if self.barrier == "RATE_LIMITED":
                    raise AccessBarrier
                try:
                    control = json.loads(self.control_file.read_text())
                except (OSError, ValueError):
                    control = {}
                if control.get("wait_id") == wait_id:
                    if control.get("action") == "cancel":
                        self.barrier = self.barrier or "ACCESS_BLOCKED"
                        self.barrier_reason = "manual_validation_cancelled"
                        raise AccessBarrier
                    if control.get("action") == "continue":
                        # Confirmation never counts as data acquisition success.
                        old = self.barrier
                        self.barrier = None
                        try:
                            await self.inspect()
                        except AccessBarrier:
                            pass
                        else:
                            self.capture_error = None
                            self.manual_validated = True
                            self.resume_url = self.page.url
                            self.epoch += 1
                            self.request_epochs.clear()
                            self.operation_warnings.append(
                                "human_confirmed_browser_session"
                            )
                            self.emit("manual_validated", {"wait_id": wait_id})
                            return
                        self.barrier = self.barrier or old
                await asyncio.sleep(
                    min(
                        self.settings["manual_poll_seconds"],
                        max(0, until - time.monotonic()),
                    )
                )
            self.barrier = self.barrier or "ACCESS_BLOCKED"
            self.barrier_reason = "manual_validation_timeout"
            raise AccessBarrier
        finally:
            self.manual_pending = False
            self.control_file.unlink(missing_ok=True)

    async def inspect(self):
        self.check()
        path = urlsplit(self.page.url).path
        if re.search(r"/(?:captcha|verify)(?:/|$)", path):
            self.barrier = "CAPTCHA_REQUIRED"
            self.barrier_reason = "visible_verification_page"
        elif re.search(r"/login(?:/|$)", path):
            self.barrier = "LOGIN_REQUIRED"
            self.barrier_reason = "visible_login_page"
        selector = (
            "#captcha_container, #captcha-verify-container, #captcha-verify-image, "
            '[data-e2e="captcha-verify-container"]'
        )
        challenge = self.page.locator(selector)
        if await challenge.count() and await challenge.first.is_visible():
            self.barrier = "CAPTCHA_REQUIRED"
            self.barrier_reason = "visible_captcha"
        self.check()

    async def hydration(self):
        texts = await self.page.locator(
            "#__UNIVERSAL_DATA_FOR_REHYDRATION__, #SIGI_STATE"
        ).all_text_contents()
        for text in texts:
            try:
                self.video_buffer.extend(embedded_videos(json.loads(text)))
            except (ValueError, TypeError):
                self.operation_warnings.append("invalid_embedded_json")

    async def navigate(self, url):
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc not in {
            "www.tiktok.com",
            "tiktok.com",
        }:
            raise ValueError("TikTok navigation requires a TikTok URL")
        if self.resume_url != url or self.page.url != url:
            await self.page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=min(self.config["timeout_seconds"], self.remaining()) * 1000,
            )
        self.resume_url = None
        await self.pause(self.settings["scroll_pause_seconds"])
        await self.inspect()
        await self.hydration()

    def candidates(self):
        while self.video_buffer:
            source = self.video_buffer.pop(0)
            try:
                item = project_video(source)
                normalize_item(item)
            except (ValueError, TypeError, KeyError, OverflowError, AttributeError):
                self.invalid_candidates += 1
                continue
            self.candidate(item["link"], item)

    def candidate(self, url, item=None):
        try:
            ident, _, comment = parse_url(url)
            if (
                comment
                or ident in self.seen
                or reached(len(self.seen), self.options.search_results)
            ):
                return
        except ValueError:
            self.invalid_candidates += 1
            return
        self.seen.add(ident)
        self.emit(
            "candidate",
            dict(
                url=url,
                cached_root=item,
                discovered_from=self.spec.get("query") or "#" + self.spec["hashtag"],
            ),
        )

    async def search(self):
        url = (
            "https://www.tiktok.com/search?" + urlencode({"q": self.spec["query"]})
            if "query" in self.spec
            else "https://www.tiktok.com/tag/" + self.spec["hashtag"]
        )
        await self.navigate(url)
        idle = 0
        while True:
            self.check()
            before = len(self.seen)
            self.candidates()
            links = await self.page.locator(
                'a[href*="/video/"],a[href*="/photo/"]'
            ).evaluate_all("els => els.map(el => el.href)")
            for link in links:
                # Strip tracking parameters from links actually observed in the page.
                self.candidate(link.split("?", 1)[0].split("#", 1)[0])
            if reached(len(self.seen), self.options.search_results):
                break
            idle = idle + 1 if len(self.seen) == before else 0
            if idle >= self.settings["idle_scroll_limit"]:
                self.operation_warnings.append(
                    "visible_search_exhausted_non_exhaustive"
                )
                break
            await self.page.mouse.wheel(0, 900)
            await self.pause(self.settings["scroll_pause_seconds"])
            await self.inspect()
            await self.hydration()
        if not self.seen:
            raise SearchUnavailable

    def drain_comments(self):
        while self.comment_buffer:
            source, parent = self.comment_buffer.pop(0)
            try:
                item = project_comment(
                    source, self.target_id, self.root["link"], parent=parent
                )
            except (ValueError, TypeError, KeyError, OverflowError):
                self.invalid_candidates += 1
                continue
            cid = item["id"]
            if cid in self.seen:
                continue
            if parent:
                if reached(self.replies, self.options.max_replies) or reached(
                    self.per_thread[parent], self.options.max_replies_per_thread
                ):
                    continue
                # Preserve relations only when the native parent was observed.
                if parent not in self.seen:
                    self.operation_warnings.append("reply_parent_not_observed")
                    continue
                self.replies += 1
                self.per_thread[parent] += 1
            else:
                if reached(self.comments, self.options.max_comments):
                    continue
                self.comments += 1
                self.reply_expected[cid] = item["reply_count"]
            self.seen.add(cid)
            self.emit("record", item)
            if not parent:
                self.comment_buffer.extend(
                    (reply, cid) for reply in source.get("reply_comment") or []
                )

    def comments_exhausted(self):
        if self.pending or self.comment_pages.get(None) is not False:
            return False
        if self.options.max_replies == 0 or self.options.max_replies_per_thread == 0:
            return True
        return all(
            self.comment_pages.get(parent) is False
            or (expected is not None and self.per_thread[parent] >= expected)
            for parent, expected in self.reply_expected.items()
        )

    async def thread(self, target):
        self.target_id = target["video_id"]
        item = target.get("cached_root")
        url = (
            item["link"]
            if item
            else next(
                (u for u in self.options.urls if parse_url(u)[0] == self.target_id),
                "https://www.tiktok.com/@_/video/" + self.target_id,
            )
        )
        if item is None:
            await self.navigate(url)
            source = next(
                (v for v in self.video_buffer if str(v.get("id")) == self.target_id),
                None,
            )
            if source is None:
                raise ValueError("TikTok video metadata unavailable")
            item = project_video(source)
        raw = normalize_item(item)
        if raw.native_id != self.target_id:
            raise ValueError("TikTok lookup identity mismatch")
        self.root = item
        self.emit("record", item)
        root = dict(
            object_type="post",
            object_key=raw.thread_root_key,
            title=None,
            text_source=raw.text_source,
            published_at=raw.published_at,
        )
        if not self._select({"Contents": [root]})[0] or self.options.max_comments == 0:
            return
        if target.get("cached_root") is not None:
            await self.navigate(url)
        button = self.page.locator('[data-e2e="comment-icon"]')
        pane = self.page.locator(
            '[data-e2e="comment-list"],[class*="DivCommentListContainer"],[data-e2e="comment-level-1"]'
        )
        pane_open = await pane.count() and await pane.first.is_visible()
        if not pane_open and await button.count() and await button.first.is_visible():
            await button.first.click(timeout=min(3000, self.remaining() * 1000))
            await self.pause(self.settings["scroll_pause_seconds"])
        idle = 0
        reply_control = 0
        while True:
            self.check()
            before = len(self.seen)
            self.drain_comments()
            idle = idle + 1 if len(self.seen) == before else 0
            if self.comments_exhausted():
                self.operation_warnings.append("source_comment_pagination_exhausted")
                break
            expanded = False
            if (
                self.options.max_comments is not None
                and idle >= self.settings["idle_scroll_limit"]
            ):
                self.operation_warnings.append(
                    "visible_comments_exhausted_non_exhaustive"
                )
                break
            if (
                self.options.max_replies != 0
                and self.options.max_replies_per_thread != 0
            ):
                more = self.page.locator(
                    '[data-e2e*="comment-more"],[data-e2e*="view-more"],button'
                ).filter(has_text=re.compile(r"(view|lihat).*(repl|balasan)", re.I))
                count = await more.count()
                if count:
                    control = more.nth(reply_control % count)
                    reply_control += 1
                    if await control.is_visible():
                        await control.click(timeout=min(3000, self.remaining() * 1000))
                        expanded = True
            if not expanded:
                # Scroll the comments, never the video/feed under the panel.
                await self.page.locator(
                    '[data-e2e="comment-list"],[class*="DivCommentListContainer"]'
                ).evaluate_all(
                    "els => els.forEach(el => {el.scrollTop = "
                    + ("0" if idle and idle % 6 == 0 else "el.scrollHeight")
                    + "})"
                )
            await self.pause(max(self.settings["scroll_pause_seconds"], min(idle, 10)))
            await self.inspect()
        self.drain_comments()

    async def collect(self, operation, target, settings, seconds, emit):
        self.deadline = time.monotonic() + seconds
        self.epoch += 1
        self.operation, self.options, self.emit = operation, settings, emit
        self.video_buffer, self.comment_buffer = [], []
        self.seen, self.comments, self.replies = set(), 0, 0
        self.per_thread = Counter()
        self.comment_pages, self.reply_expected = {}, {}
        self.operation_warnings = []
        self.capture_error = None
        self.root = None
        if self.page is None:
            await self.start()
        if operation == "search":
            self.spec = json.loads(target)
        if self.settings["manual_wait_seconds"] and not self.manual_validated:
            self.manual_pending = True
            initial_url = (
                "https://www.tiktok.com/search?" + urlencode({"q": self.spec["query"]})
                if operation == "search" and "query" in self.spec
                else "https://www.tiktok.com/tag/" + self.spec["hashtag"]
                if operation == "search"
                else "https://www.tiktok.com/"
            )
            await self.page.goto(
                initial_url,
                wait_until="domcontentloaded",
                timeout=min(self.config["timeout_seconds"], self.remaining()) * 1000,
            )
            await self.manual_validation()
        self.check()
        if operation == "search":
            await self.search()
        else:
            await self.thread(target)
        self.check()

    async def close(self):
        for task in list(self.pending):
            task.cancel()
        if self.pending:
            await asyncio.gather(*self.pending, return_exceptions=True)
        for resource in [self.context, self.browser]:
            if resource is not None:
                await resource.close()
        if self.playwright is not None:
            await self.playwright.stop()


def project_video(data):
    ident = native_id(data["id"])
    author = data.get("author") or {}
    username = (
        author
        if isinstance(author, str)
        else author.get("uniqueId") or author.get("unique_id")
    )
    if not isinstance(username, str) or not re.fullmatch(
        r"[A-Za-z0-9_.]{1,40}", username
    ):
        raise ValueError("TikTok author URL unavailable")
    stats = data.get("statsV2") or data.get("stats") or {}
    names = {
        "play_count": "playCount",
        "like_count": "diggCount",
        "comment_count": "commentCount",
        "share_count": "shareCount",
        "save_count": "collectCount",
        "repost_count": "repostCount",
    }
    return dict(
        id=ident,
        link=f"https://www.tiktok.com/@{username}/video/{ident}",
        description=data.get("desc") or "",
        created_at=source_time(data.get("createTime", data.get("create_time"))),
        stats={name: metric_number(stats.get(key)) for name, key in names.items()},
    )


def metric_number(value):
    if type(value) is int and value >= 0:
        return value
    if isinstance(value, str) and re.fullmatch(r"[0-9]{1,30}", value):
        return int(value)
    return None


def source_time(value):
    if value is None:
        return None
    if isinstance(value, str) and not value.isdecimal():
        return contract.utc_datetime(value).isoformat()
    return datetime.fromtimestamp(int(value), timezone.utc).isoformat()


def project_comment(data, root, url, *, parent=None):
    ident = native_id(data["cid"])
    if data.get("aweme_id") and native_id(data["aweme_id"]) != root:
        raise ValueError("TikTok comment video ID mismatch")
    return dict(
        id=ident,
        video_id=root,
        kind="reply" if parent else "comment",
        link=url + "?comment_id=" + ident,
        text=data.get("text") or "",
        created_at=source_time(data.get("create_time")),
        parent_comment_id=parent,
        like_count=metric_number(data.get("digg_count")),
        reply_count=metric_number(data.get("reply_comment_total")),
    )


def worker_main(config, pipe):
    logging.disable(logging.CRITICAL)
    if hasattr(os, "setsid"):
        os.setsid()
    client = None
    loop = asyncio.new_event_loop()
    try:
        with (
            open(os.devnull, "w") as quiet,
            redirect_stdout(quiet),
            redirect_stderr(quiet),
        ):
            while True:
                command = pipe.recv()
                if command is None:
                    break
                operation, target, options, seconds = command
                try:
                    if client is None:
                        client = NativeTikTokClient(config)

                    loop.run_until_complete(
                        asyncio.wait_for(
                            client.collect(
                                operation,
                                target,
                                SimpleNamespace(**options),
                                seconds,
                                lambda kind, item: pipe.send((kind, item)),
                            ),
                            timeout=None if math.isinf(seconds) else seconds,
                        )
                    )
                    result = dict(
                        status="FINISHED_BEST_EFFORT",
                        reason="native_browser_visible_data",
                        warnings=list(client.operation_warnings),
                        source_version=SOURCE_VERSION,
                    )
                except Exception as error:
                    result = error_receipt(
                        AccessBarrier() if client and client.barrier else error
                    )
                    if client and client.barrier:
                        result["status"] = client.barrier
                        result["reason"] = (
                            client.barrier_reason or "tiktok_access_barrier"
                        )
                    elif (
                        client
                        and client.page is None
                        and result["status"] == "SOURCE_ERROR"
                    ):
                        result.update(
                            status="CLIENT_BROWSER_BLOCK",
                            reason="native_browser_start_failed",
                        )
                if client and client.retry_after_seconds is not None:
                    result["retry_after_seconds"] = client.retry_after_seconds
                if client:
                    result["network"] = dict(
                        requests=client.requests,
                        http_status_counts=dict(client.statuses),
                        response_endpoint_counts=dict(client.endpoints),
                        invalid_candidates=client.invalid_candidates,
                    )
                pipe.send(("done", result))
    except (EOFError, BrokenPipeError):
        pass
    finally:
        if client:
            try:
                loop.run_until_complete(asyncio.wait_for(client.close(), timeout=5))
            except Exception:
                pass
        loop.close()
        pipe.close()


class TikTokWorker:
    """Keep a single library session; retain streamed rows on a hard deadline."""

    def __init__(self, config, *, target=worker_main, progress=None):
        self.config, self.target = config, target
        self.progress = progress or (lambda event: None)
        self.process = self.pipe = None

    def __call__(self, operation, target, settings, seconds, emit):
        if self.process is None:
            ctx = mp.get_context("spawn")
            self.pipe, child = ctx.Pipe()
            self.process = ctx.Process(
                target=self.target, args=(self.config, child), daemon=True
            )
            self.process.start()
            child.close()
        self.pipe.send((operation, target, vars(settings), seconds))
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if self.pipe.poll(min(0.25, max(0, deadline - time.monotonic()))):
                try:
                    kind, item = self.pipe.recv()
                except EOFError:
                    break
                if kind == "done":
                    return item
                if kind in {"manual_validation", "manual_validated"}:
                    self.progress({"event": kind, **item})
                    continue
                emit(kind, item)
            elif not self.process.is_alive():
                break
        self.close()
        return dict(
            status="TIMEOUT",
            reason="tiktok_operation_deadline",
            warnings=["partial_operation_rows_only"],
            source_version=SOURCE_VERSION,
        )

    def close(self):
        if self.process is not None:
            if self.process.is_alive():
                try:
                    self.pipe.send(None)
                except (BrokenPipeError, EOFError, OSError):
                    pass
                self.process.join(1)
            if self.process.is_alive():
                if hasattr(os, "killpg"):
                    try:
                        if os.getpgid(self.process.pid) == self.process.pid:
                            os.killpg(self.process.pid, signal.SIGTERM)
                    except (OSError, ProcessLookupError):
                        pass
                self.process.terminate()
                self.process.join(2)
            if self.process.is_alive():
                self.process.kill()
                self.process.join(2)
            self.pipe.close()
            self.process = self.pipe = None


class ChromeCaptureWorker:
    """Import public records observed through the connected Chrome UI.

    This consumes a saved capture, never connects to Chrome, reads cookies or
    launches a browser. Live UI acquisition remains the connected agent's job.
    """

    extraction_method = CHROME_METHOD
    access_mode = "existing_chrome;agent_observed_public_page;saved_capture_only"

    def __init__(self, path):
        path = Path(path)
        if path.stat().st_size > 50_000_000:
            raise ValueError("Chrome capture is too large")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or (
            data.get("schema_version") != 1
            or data.get("source") != "existing_chrome_public_page"
            or not isinstance(data.get("query"), str)
            or not isinstance(data.get("records"), list)
        ):
            raise ValueError("Invalid Chrome capture format")
        self.query = data["query"]
        self.observed_at = contract.utc_datetime(data["captured_at"]).isoformat()
        self.roots, self.children = {}, {}
        seen = set()
        for supplied in data["records"]:
            if not isinstance(supplied, dict) or not isinstance(
                supplied.get("id"), str
            ):
                raise ValueError("Chrome capture requires native IDs as strings")
            item = {**supplied, "observed_at": self.observed_at}
            if item.get("kind", "post") == "post":
                if not isinstance(item.get("stats", {}), dict):
                    raise ValueError("Chrome capture statistics must be an object")
                item["stats"] = {
                    key: metric_number(value)
                    for key, value in item.get("stats", {}).items()
                }
            else:
                item["like_count"] = metric_number(item.get("like_count"))
            raw = normalize_item(item, method=CHROME_METHOD)
            key = (raw.namespace, raw.native_id)
            if key in seen:
                continue
            seen.add(key)
            root = raw.thread_root_key.rsplit(":", 1)[-1]
            if raw.object_type == "post":
                self.roots[root] = item
            else:
                self.children.setdefault(root, []).append(item)
        for root, children in self.children.items():
            if root not in self.roots:
                raise ValueError("Chrome capture comment has no post")
            parents = {item["id"] for item in children if item["kind"] == "comment"}
            if any(
                item["kind"] == "reply" and item["parent_comment_id"] not in parents
                for item in children
            ):
                raise ValueError("Chrome capture reply has no observed parent")

    def requires_network(self, operation, target, settings, cached=None):
        return False

    def __call__(self, operation, target, settings, seconds, emit):
        if operation == "search":
            if json.loads(target) == {"query": self.query}:
                for item in list(self.roots.values())[: settings.search_results]:
                    emit(
                        "candidate",
                        dict(url=item["link"], discovered_from=self.query),
                    )
        else:
            root = native_id(target["video_id"])
            if root in self.roots:
                emit("record", self.roots[root])
                comments = replies = 0
                parents = set()
                per_parent = Counter()
                for item in sorted(
                    self.children.get(root, []), key=lambda row: row["kind"] == "reply"
                ):
                    reply = item["kind"] == "reply"
                    if reached(
                        replies if reply else comments,
                        settings.max_replies if reply else settings.max_comments,
                    ):
                        continue
                    if reply and item["parent_comment_id"] not in parents:
                        continue
                    if reply and reached(
                        per_parent[item["parent_comment_id"]],
                        settings.max_replies_per_thread,
                    ):
                        continue
                    emit("record", item)
                    if reply:
                        replies += 1
                        per_parent[item["parent_comment_id"]] += 1
                    else:
                        comments += 1
                        parents.add(item["id"])
        return dict(
            status="FINISHED_BEST_EFFORT",
            reason="saved_chrome_capture_only",
            warnings=["comments_completeness_unverified", "capture_not_refreshed"],
            source_version=CHROME_VERSION,
        )


def live_chrome_plan(extension=False):
    """Describe the selected transport without starting a browser or reading auth."""
    from Crawler.Backend.Tiktok.chrome_bridge import COMMENT_PROTOCOL, LIVE_VERSION

    manifest = json.loads(
        (ROOT / "Crawler/Backend/Tiktok/chrome_extension/manifest.json").read_text()
    )
    return dict(
        keyword_search="live_connected_chrome_ui",
        browser_acquisition="existing_chrome_extension"
        if extension
        else "live_connected_browser_agent_bridge",
        browser_backend_version=f"ChromeExtension:{manifest['version']};{LIVE_VERSION}"
        if extension
        else LIVE_VERSION,
        manual_validation=False,
        extension_pairing_required=extension,
        run_clock_starts_after_extension_pairing=extension,
        comment_stop_policy="source_pagination_exhausted_or_run_deadline",
        required_connector_version="1.2.1" if extension else None,
        required_comment_protocol=COMMENT_PROTOCOL if extension else None,
    )


class TikTokCrawler(core.SocialCrawler):
    def __init__(self, config=None, *, workers=None, **kwargs):
        supplied = expand_config(read_config(config))
        if "tiktok" not in supplied.get("platforms", {}):
            raise ValueError("Missing TikTok platform configuration")
        supplied["platforms"] = {
            "tiktok": {**supplied["platforms"]["tiktok"], "enabled": True}
        }
        supplied.pop("scweet", None)
        super().__init__(supplied, workers=workers, **kwargs)

    def plan(self):
        capture = isinstance(self.workers["tiktok"], ChromeCaptureWorker)
        live = getattr(self.workers["tiktok"], "live_chrome", False)
        return {
            **super().plan(),
            "platform_scope": "tiktok_only",
            "upstream_library": None,
            "browser_backend_version": "Playwright:1.64.1",
            "keyword_search": "live_connected_chrome_ui"
            if live
            else "saved_chrome_capture_only"
            if capture
            else "rendered_search_network_and_dom",
            "browser_acquisition": "live_connected_browser_agent_bridge"
            if live
            else "connected_agent_required"
            if capture
            else "owned_playwright_browser",
            "retry_after_policy": "stop_and_persist_server_cooldown",
            "progress_recovery": "saved_partial_bundles_and_existing_native_id_archive",
            "session_rotation": False,
            "automatic_captcha_solving": False,
            "manual_validation": not capture
            and bool(self.config["platforms"]["tiktok"]["manual_wait_seconds"]),
            "comments_complete": False,
            **(
                live_chrome_plan(
                    extension=getattr(self.workers["tiktok"], "extension_mode", False)
                )
                if live
                else {}
            ),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--target-posts", type=int)
    parser.add_argument("--total-seconds", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--install-browser", action="store_true")
    parser.add_argument(
        "--chrome-live",
        action="store_true",
        help="Stream tasks/results through an already-connected Chrome browser agent",
    )
    parser.add_argument(
        "--chrome-extension",
        action="store_true",
        help="Automatic Chrome extension transport; wait for explicit pairing before the run timer starts",
    )
    parser.add_argument(
        "--bridge-port",
        type=int,
        default=0,
        help="Loopback bridge port; 0 chooses a free port",
    )
    parser.add_argument(
        "--chrome-capture",
        type=Path,
        help="Export a saved public-page capture from connected Chrome; no browser launch",
    )
    parser.add_argument(
        "--manual-validation",
        action="store_true",
        help="Wait for human CAPTCHA/login confirmation in visible Chromium",
    )
    parser.add_argument(
        "--manual-wait-seconds",
        type=int,
        default=600,
        help="Wait for extension pairing or human Chromium validation; crawl timer starts afterwards",
    )
    parser.add_argument(
        "--headed", action="store_true", help="Show the browser for this run"
    )
    args = parser.parse_args()
    live_worker = None
    try:
        config = read_config(args.config)
        if args.chrome_extension:
            if not 1 <= args.manual_wait_seconds <= 3600:
                raise ValueError("Extension pairing wait must be 1 to 3600 seconds")
            args.chrome_live = True
        if (args.chrome_capture or args.chrome_live) and (
            args.manual_validation or args.headed or args.install_browser
        ):
            raise ValueError("Chrome capture cannot launch a browser")
        if args.chrome_capture and args.chrome_live:
            raise ValueError("Choose live Chrome or saved capture")
        if args.manual_validation:
            config["platforms"]["tiktok"].update(
                headless=False,
                browser="chromium",
                manual_wait_seconds=args.manual_wait_seconds,
            )
        if args.headed:
            config["platforms"]["tiktok"]["headless"] = False
        if args.install_browser:
            from Crawler.Backend.Tiktok.browser_runtime import install_browser

            options = platform_configuration(
                expand_config(config)["platforms"]["tiktok"]
            )
            install_browser(options["browser"])
            print(json.dumps(dict(status="BROWSER_READY")))
            return 0
        if args.target_posts is not None:
            config["platforms"]["tiktok"].update(
                min_posts=args.target_posts, max_posts=None
            )
        if args.total_seconds is not None:
            config["total_seconds"] = args.total_seconds
        if args.chrome_live and not args.dry_run:
            from Crawler.Backend.Tiktok.chrome_bridge import ChromeLiveWorker

            live_worker = ChromeLiveWorker(
                port=args.bridge_port,
                extension_mode=args.chrome_extension,
                progress=lambda event: print(json.dumps(event), flush=True),
                selection={
                    k: config.get(k)
                    for k in (
                        "since",
                        "until",
                        "include_keywords",
                        "exclude_keywords",
                        "include_mode",
                    )
                },
            )
            print(
                json.dumps(
                    dict(stage="chrome_bridge_ready", bridge_url=live_worker.bridge_url)
                ),
                flush=True,
            )
            if args.chrome_extension:
                print(
                    json.dumps(
                        dict(
                            stage="waiting_for_chrome_extension",
                            action="Open local bridge page, pair the extension on a TikTok tab",
                        )
                    ),
                    flush=True,
                )
                try:
                    live_worker.wait_for_extension(seconds=args.manual_wait_seconds)
                except TimeoutError:
                    print(
                        json.dumps(
                            dict(
                                status="CHROME_PAIRING_TIMEOUT",
                                reason="extension_not_connected_before_pairing_deadline",
                                crawling_started=False,
                            )
                        )
                    )
                    return 2
                print(
                    json.dumps(
                        dict(
                            stage="chrome_extension_connected",
                            platform="tiktok",
                            run_clock="starts_now",
                            total_seconds=config.get("total_seconds"),
                            connector=getattr(live_worker, "client_info", None),
                        )
                    ),
                    flush=True,
                )
        crawler = TikTokCrawler(
            config,
            workers={"tiktok": live_worker}
            if live_worker
            else {"tiktok": ChromeCaptureWorker(args.chrome_capture)}
            if args.chrome_capture
            else None,
            progress=lambda e: print(json.dumps(e, ensure_ascii=False), flush=True),
        )
        # The shared runner treats injected workers as test fixtures. This CLI
        # creates a real live bridge; its observed records are not synthetic.
        # Keep fixture injection behavior unchanged for library/offline tests.
        if live_worker is not None:
            crawler._synthetic = False
        result = crawler.plan() if args.dry_run else crawler.run(args.output_dir)
        if args.dry_run and args.chrome_live:
            result.update(live_chrome_plan(extension=args.chrome_extension))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if args.dry_run or result["status"] == "TARGET_MET" else 2
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(
            json.dumps(
                dict(
                    status="CONFIG_OR_RUNTIME_ERROR",
                    error_type=type(error).__name__,
                    reason="tiktok_configuration_or_output_failed",
                )
            )
        )
        return 2
    finally:
        if live_worker is not None:
            live_worker.close()


if __name__ == "__main__":
    mp.freeze_support()
    raise SystemExit(main())
