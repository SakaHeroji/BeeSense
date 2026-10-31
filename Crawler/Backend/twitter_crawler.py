"""Standalone Twitter/X acquisition with Scweet and BeeSense's Excel contract."""

from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import json
import logging
import multiprocessing as mp
import os
import re
import tempfile
import time
import uuid
from collections import Counter, deque
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit

from Crawler.Backend.Reddit import crawl_reddit_single as contract
from Crawler.Backend.social_export import (
    COMPACT_COLUMNS,
    COMPACT_FILE,
    SocialExportMixin,
)

ROOT = Path(__file__).resolve().parents[2]
VERSION = "1.0.1"
METHOD = "scweet_saved_web_session"
NAMESPACE = "x_post"
BARRIERS = {"RATE_LIMITED", "LOGIN_REQUIRED", "ACCESS_BLOCKED", "CHALLENGE_REQUIRED"}


def upstream_version():
    try:
        return importlib.metadata.version("Scweet")
    except importlib.metadata.PackageNotFoundError:
        return None


def read_json(path):
    path = Path(path)
    if path.stat().st_size > 1_000_000:
        raise ValueError("Local JSON exceeds 1 MB")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError):
        raise ValueError("Invalid local JSON") from None


def native_id(value):
    text = str(value or "")
    if not re.fullmatch(r"[1-9][0-9]{0,24}", text):
        raise ValueError("Invalid native X post ID")
    return text


def post_url(value):
    parts = urlsplit(str(value))
    if parts.scheme != "https" or parts.hostname not in {
        "x.com",
        "www.x.com",
        "twitter.com",
        "www.twitter.com",
    }:
        raise ValueError("Expected an HTTPS X/Twitter post URL")
    match = re.fullmatch(
        r"/(?:[A-Za-z0-9_]{1,15}|i/web)/status/([1-9][0-9]{0,24})/?", parts.path
    )
    if not match or parts.username or parts.password or parts.port:
        raise ValueError("Invalid X/Twitter post URL")
    return "https://x.com/i/web/status/" + match[1]


def object_key(value):
    return f"twitter:{NAMESPACE}:{native_id(value)}"


def normalize_item(item, *, root_id=None, discovered_from=None):
    """Keep native parent IDs; never infer a reply parent from screen position."""
    if hasattr(item, "model_dump"):
        item = item.model_dump()
    ident = native_id(item.get("tweet_id"))
    root_id = native_id(root_id or ident)
    supplied_url = item.get("tweet_url")
    url = "https://x.com/i/web/status/" + ident
    if supplied_url and post_url(supplied_url) != url:
        raise ValueError("X native ID and permalink disagree")
    parent = item.get("in_reply_to_tweet_id")
    if root_id != ident and not parent:
        raise ValueError("Reply has no native parent ID")
    kind = (
        "post"
        if root_id == ident
        else "comment"
        if native_id(parent) == root_id
        else "reply"
    )
    stamp, quality = None, "unknown"
    display = item.get("timestamp")
    if display:
        try:
            parsed = parsedate_to_datetime(display)
            if parsed.tzinfo is None:
                raise ValueError("Timestamp needs timezone")
            stamp, quality = parsed.astimezone(timezone.utc).isoformat(), "exact"
        except (ValueError, TypeError):
            try:
                stamp, quality = contract.utc_datetime(display).isoformat(), "exact"
            except (ValueError, TypeError):
                pass
    text = item.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Post text is absent")
    return contract.ContentInput(
        platform="twitter",
        namespace=NAMESPACE,
        native_id=ident,
        object_type=kind,
        canonical_url=url,
        page_url="https://x.com/i/web/status/" + root_id,
        thread_root_key=object_key(root_id),
        text_source=text,
        parent_key=object_key(parent) if kind != "post" else None,
        title=text.splitlines()[0][:240] if kind == "post" else None,
        published_at=stamp,
        published_display=display,
        timestamp_quality=quality,
        # Scweet's curated schema does not certify whether a caption is truncated.
        text_complete=False,
        discovered_from=discovered_from,
        extraction_method=METHOD,
        adapter_version="scweet:" + str(upstream_version()),
        quality_flags=("upstream_text_completeness_unknown",),
    )


def _integer(value, name, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in {low}..{high}")
    return value


def configuration(value):
    cfg = deepcopy(value if isinstance(value, dict) else read_json(value))
    allowed = {
        "project_id",
        "since",
        "until",
        "include_keywords",
        "exclude_keywords",
        "include_mode",
        "delay",
        "timeout_seconds",
        "total_seconds",
        "platforms",
        "scweet",
        "exclude_existing_datasets",
    }
    if not isinstance(cfg, dict) or set(cfg) - allowed:
        raise ValueError(
            "Unknown TwitterCrawler configuration field; credentials belong in auth_file"
        )
    if not isinstance(cfg.get("project_id"), str) or not cfg["project_id"].strip():
        raise ValueError("project_id is required")
    for name in ("since", "until"):
        if not isinstance(cfg.get(name), str):
            raise ValueError("Explicit since/until timestamps are required")
        cfg[name] = contract.utc_datetime(cfg[name]).isoformat()
    if cfg["since"] >= cfg["until"]:
        raise ValueError("since must precede until")
    for key in ("include_keywords", "exclude_keywords", "exclude_existing_datasets"):
        cfg.setdefault(key, [])
        if not isinstance(cfg[key], list) or any(
            not isinstance(x, str) or not x.strip() for x in cfg[key]
        ):
            raise ValueError("Invalid " + key)
    if cfg.get("include_mode", "any") not in {"any", "all"}:
        raise ValueError("include_mode must be any or all")
    cfg.setdefault("include_mode", "any")
    _integer(cfg.get("total_seconds", 1800), "total_seconds", 1, 10800)
    cfg.setdefault("total_seconds", 1800)
    cfg.setdefault("timeout_seconds", 180)
    _integer(cfg["timeout_seconds"], "timeout_seconds", 1, 300)
    cfg.setdefault("delay", {"mode": "fixed", "seconds": 15})
    if (
        not isinstance(cfg["delay"], dict)
        or set(cfg["delay"]) != {"mode", "seconds"}
        or cfg["delay"]["mode"] != "fixed"
    ):
        raise ValueError("delay must use fixed seconds")
    _integer(cfg["delay"]["seconds"], "delay.seconds", 0, 300)
    platforms = cfg.get("platforms")
    if (
        not isinstance(platforms, dict)
        or set(platforms) != {"twitter"}
        or not isinstance(platforms["twitter"], dict)
    ):
        raise ValueError("This standalone crawler supports only twitter")
    p = platforms["twitter"]
    defaults = dict(
        enabled=True,
        urls=[],
        queries=[],
        min_posts=1000,
        max_posts=1000,
        max_comments=10,
        search_results=20,
        search_window_days=7,
        max_searches=200,
        lang="id",
    )
    if set(p) - set(defaults):
        raise ValueError("Unknown Twitter platform option")
    for key, default in defaults.items():
        p.setdefault(key, default)
    if p["enabled"] is not True:
        raise ValueError("Twitter must be enabled")
    for key in ("queries", "urls"):
        if not isinstance(p[key], list) or any(
            not isinstance(x, str) or not x.strip() for x in p[key]
        ):
            raise ValueError("Invalid Twitter " + key)
    p["urls"] = [post_url(url) for url in p["urls"]]
    if not p["queries"] and not p["urls"]:
        raise ValueError("At least one query or URL is required")
    if p["lang"] is not None and not re.fullmatch(r"[a-z]{2,3}", str(p["lang"])):
        raise ValueError("Invalid language")
    for key, low, high in (
        ("min_posts", 1, 10000),
        ("max_posts", 1, 10000),
        ("max_comments", 0, 100),
        ("search_results", 1, 100),
        ("search_window_days", 1, 365),
        ("max_searches", 1, 1000),
    ):
        _integer(p[key], key, low, high)
    if p["min_posts"] > p["max_posts"]:
        raise ValueError("min_posts exceeds max_posts")
    options = cfg.setdefault("scweet", {})
    defaults = dict(
        auth_file="config/auth.json",
        state_dir="output/scweet",
        request_interval_seconds=5,
        request_timeout_seconds=30,
        daily_requests_limit=120,
        daily_tweets_limit=2000,
        window_request_limit=20,
        rate_limit_cooldown_seconds=900,
        manifest_scrape_on_init=True,
    )
    if not isinstance(options, dict) or set(options) - set(defaults):
        raise ValueError("Unknown Scweet option; do not embed credentials")
    for key, default in defaults.items():
        options.setdefault(key, default)
    for key in ("auth_file", "state_dir"):
        if not isinstance(options[key], str) or not options[key].strip():
            raise ValueError("Invalid local path")
        options[key] = str((ROOT / options[key]).resolve())
    if Path(options["auth_file"]).is_relative_to(Path(options["state_dir"])):
        raise ValueError("Authentication file must be separate from runtime state")
    for key, low, high in (
        ("request_interval_seconds", 5, 300),
        ("request_timeout_seconds", 5, 120),
        ("daily_requests_limit", 1, 300),
        ("daily_tweets_limit", 1, 6000),
        ("window_request_limit", 1, 40),
        ("rate_limit_cooldown_seconds", 360, 86400),
    ):
        _integer(options[key], key, low, high)
    if type(options["manifest_scrape_on_init"]) is not bool:
        raise ValueError("manifest_scrape_on_init must be boolean")
    return cfg


def auth_material(path):
    data = read_json(path)
    entries = data if isinstance(data, list) else [data]
    entries = [
        x
        for x in entries
        if isinstance(x, dict)
        and str(x.get("sosmed", "")).casefold()
        in {"twitter", "x", "twitter x", "x twitter"}
    ]
    if len(entries) != 1:
        raise ValueError("Exactly one Twitter/X auth entry is required")
    entry = entries[0]
    username = entry.get("username")
    token = entry.get("auth_token") or entry.get("sessionid")
    if not isinstance(username, str) or not re.fullmatch(
        r"@?[A-Za-z0-9_]{1,15}", username
    ):
        raise ValueError("Twitter username must be a handle")
    cookies = {"auth_token": token}
    if entry.get("ct0"):
        cookies["ct0"] = entry["ct0"]
    if any(
        not isinstance(v, str)
        or not v
        or len(v) > 4096
        or any(ord(c) < 33 or ord(c) > 126 for c in v)
        for v in cookies.values()
    ):
        raise ValueError("Missing or malformed local Twitter cookies")
    return username.lstrip("@"), cookies


def private_json(path, value):
    descriptor, temporary = tempfile.mkstemp(prefix=".scweet-", dir=path.parent)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


class AccessBarrier(RuntimeError):
    def __init__(self, status, http_status=None, retry_after_seconds=None):
        self.status, self.http_status, self.retry_after_seconds = (
            status,
            http_status,
            retry_after_seconds,
        )
        super().__init__(status)


def response_barrier(response):
    code = int(response.status_code)
    headers = {k.lower(): v for k, v in response.headers.items()}
    status = {
        429: "RATE_LIMITED",
        401: "LOGIN_REQUIRED",
        403: "ACCESS_BLOCKED",
        400: "ACCESS_BLOCKED",
    }.get(code)
    path = urlsplit(str(response.url)).path
    if path.startswith(("/i/flow/login", "/login")):
        status = "LOGIN_REQUIRED"
    if path.startswith(("/account/access", "/i/flow/challenge")):
        status = "CHALLENGE_REQUIRED"
    if "json" in headers.get("content-type", ""):
        try:
            data = response.json()
            errors = data.get("errors", []) if isinstance(data, dict) else []
            codes = {x.get("code") for x in errors if isinstance(x, dict)}
            if 326 in codes:
                status = "CHALLENGE_REQUIRED"
            elif codes & {32, 89, 215}:
                status = "LOGIN_REQUIRED"
            elif 88 in codes:
                status = "RATE_LIMITED"
        except (ValueError, TypeError):
            pass
    retry = None
    if status == "RATE_LIMITED":
        value = str(headers.get("retry-after", ""))
        if value.isdigit():
            retry = int(value)
        else:
            try:
                retry = max(
                    0, int(parsedate_to_datetime(value).timestamp() - time.time()) + 1
                )
            except (ValueError, TypeError, OverflowError):
                pass
        try:
            reset = max(
                0, int(headers.get("x-rate-limit-reset", 0)) - int(time.time()) + 1
            )
            retry = max(retry or 0, reset) or None
        except (TypeError, ValueError):
            pass
    return AccessBarrier(status, code, retry) if status else None


@contextmanager
def guarded_transport(options):
    """Child-only guard: pace curl requests and prohibit network after a barrier."""
    from curl_cffi.requests import AsyncSession, Session

    state = dict(requests=0, http_status_counts=Counter(), barrier=None, previous=None)
    original_sync, original_async = Session.request, AsyncSession.request

    def prepare(url, kwargs):
        if state["barrier"]:
            raise state["barrier"]
        previous = state["previous"]
        kwargs["timeout"] = min(
            float(kwargs.get("timeout") or options["request_timeout_seconds"]),
            options["request_timeout_seconds"],
        )
        return max(
            0, (previous or 0) + options["request_interval_seconds"] - time.monotonic()
        )

    def observe(response):
        state["requests"] += 1
        state["http_status_counts"][str(response.status_code)] += 1
        state["barrier"] = response_barrier(response)
        if state["barrier"]:
            cooldown = max(
                options["rate_limit_cooldown_seconds"],
                state["barrier"].retry_after_seconds or 0,
            )
            private_json(
                Path(options["state_dir"]) / "barrier.json",
                dict(
                    status=state["barrier"].status,
                    http_status=state["barrier"].http_status,
                    not_before=time.time() + cooldown,
                ),
            )
        return response

    def sync(session, method, url, *args, **kwargs):
        time.sleep(prepare(url, kwargs))
        state["previous"] = time.monotonic()
        return observe(original_sync(session, method, url, *args, **kwargs))

    async def asynchronous(session, method, url, *args, **kwargs):
        await asyncio.sleep(prepare(url, kwargs))
        state["previous"] = time.monotonic()
        return observe(await original_async(session, method, url, *args, **kwargs))

    Session.request, AsyncSession.request = sync, asynchronous
    try:
        yield state
    finally:
        Session.request, AsyncSession.request = original_sync, original_async


def create_client(options):
    from Scweet import Scweet, ScweetConfig

    username, cookies = auth_material(options["auth_file"])
    directory = Path(options["state_dir"])
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    directory.chmod(0o700)
    barrier_path = directory / "barrier.json"
    if barrier_path.exists():
        barrier = read_json(barrier_path)
        if (
            barrier.get("status") != "RATE_LIMITED"
            or barrier["not_before"] > time.time()
        ):
            raise AccessBarrier(
                barrier["status"],
                barrier.get("http_status"),
                max(0, int(barrier["not_before"] - time.time())),
            )
    database, identity = directory / "state.db", directory / "identity.json"
    fingerprint = dict(
        username=username.casefold(),
        token_sha256=sha256(cookies["auth_token"].encode()).hexdigest(),
    )
    if database.exists() and (
        not identity.exists() or read_json(identity) != fingerprint
    ):
        raise ValueError("Saved Scweet state and local credentials disagree")
    provision = not database.exists()
    # State is reused without provisioning, preserving leases and daily counters.
    cfg = ScweetConfig(
        concurrency=1,
        n_splits=1,
        api_http_mode="sync",
        min_delay_s=options["request_interval_seconds"],
        window_request_limit=options["window_request_limit"],
        daily_requests_limit=options["daily_requests_limit"],
        daily_tweets_limit=options["daily_tweets_limit"],
        max_empty_pages=1,
        max_task_attempts=1,
        max_fallback_attempts=1,
        max_account_switches=0,
        pool_wait_max_s=0,
        request_404_retries=0,
        network_error_retries=0,
        transaction_init_attempts=1,
        manifest_scrape_on_init=False,
    )
    previous_umask = os.umask(0o077)
    try:
        if provision:
            private_json(identity, fingerprint)
        client = Scweet(
            db_path=str(database),
            cookies=[dict(username=username, cookies=cookies)] if provision else None,
            config=cfg,
            provision=provision,
        )
    finally:
        os.umask(previous_umask)
    diagnostics = client._accounts_repo.eligibility_diagnostics()
    if not diagnostics["eligible"]:
        blocked = set(diagnostics.get("blocked_counts", {}))
        if blocked & {
            "rejected_auth_token",
            "missing_auth_token",
            "missing_csrf",
            "missing_cookies",
            "missing_bearer",
        }:
            raise AccessBarrier("LOGIN_REQUIRED")
        if blocked == {"cooldown"}:
            waits = [
                max(1, int(row["available_til"] - time.time()) + 1)
                for row in diagnostics.get("blocked_samples", [])
                if isinstance(row.get("available_til"), (int, float))
            ]
            if waits:
                raise AccessBarrier("COOLDOWN", retry_after_seconds=min(waits))
        raise AccessBarrier("ACCOUNT_UNAVAILABLE")
    if options["manifest_scrape_on_init"]:
        client.refresh_manifest()
    return client


def error_receipt(error):
    names = {c.__name__ for c in type(error).__mro__}
    status = "SOURCE_ERROR"
    if isinstance(error, AccessBarrier):
        status = error.status
    elif "RateLimitError" in names:
        status = "RATE_LIMITED"
    elif names & {"AuthError", "AccountSessionAuthError", "FileNotFoundError"}:
        status = "LOGIN_REQUIRED"
    elif "AccountPoolExhausted" in names:
        status = "ACCOUNT_UNAVAILABLE"
    elif isinstance(error, ImportError):
        status = "DEPENDENCY_MISSING"
    return dict(
        status=status,
        reason="scweet_" + status.lower(),
        warnings=[type(error).__name__],
        http_status=getattr(error, "http_status", None),
        retry_after_seconds=getattr(error, "retry_after_seconds", None),
    )


def account_cooldown(client, result):
    """Expose only wait duration; never return account records or cookies."""
    if result["status"] != "ACCOUNT_UNAVAILABLE":
        return result
    diagnostics = client._accounts_repo.eligibility_diagnostics()
    blocked = diagnostics.get("blocked_counts", {})
    if blocked and set(blocked) == {"cooldown"}:
        waits = [
            max(1, int(row["available_til"] - time.time()) + 1)
            for row in diagnostics.get("blocked_samples", [])
            if isinstance(row.get("available_til"), (int, float))
        ]
        if waits:
            return {
                **result,
                "status": "COOLDOWN",
                "reason": "scweet_account_cooldown",
                "retry_after_seconds": min(waits),
            }
    return result


def worker_main(options, pipe):
    """One isolated process owns Scweet state and transport for the whole trial."""
    logging.disable(logging.CRITICAL)
    client = None
    try:
        with (
            open(os.devnull, "w") as quiet,
            redirect_stdout(quiet),
            redirect_stderr(quiet),
            guarded_transport(options) as network,
        ):
            while True:
                command = pipe.recv()
                if command is None:
                    break
                operation, target = command
                try:
                    if client is None:
                        client = create_client(options)
                    if network["barrier"]:
                        raise network["barrier"]
                    if operation == "search":
                        rows = client.search(**target, save=False, max_empty_pages=1)
                    elif operation == "replies":
                        rows = client.get_tweet_replies(
                            target["tweet_id"],
                            limit=target["limit"],
                            max_empty_pages=1,
                            save=False,
                        )
                    elif operation == "lookup":
                        rows = client.get_tweet_info([target["tweet_id"]], save=False)
                    else:
                        raise ValueError("Unsupported Scweet operation")
                    for row in rows:
                        pipe.send(("record", row))
                    if network["barrier"]:
                        raise network["barrier"]
                    result = dict(
                        status="FINISHED_BEST_EFFORT",
                        reason="bounded_scweet_read",
                        warnings=[],
                    )
                except Exception as error:
                    result = error_receipt(network["barrier"] or error)
                    if client is not None and network["barrier"] is None:
                        result = account_cooldown(client, result)
                result["network"] = {
                    key: dict(value) if isinstance(value, Counter) else value
                    for key, value in network.items()
                    if key in {"requests", "http_status_counts"}
                }
                pipe.send(("done", result))
    except Exception as error:
        try:
            pipe.send(("done", error_receipt(error)))
        except (BrokenPipeError, EOFError):
            pass
    finally:
        pipe.close()


class ScweetWorker:
    def __init__(self, options, *, target=worker_main):
        self.options, self.target = options, target
        self.process = self.pipe = None

    def __call__(self, operation, target, seconds, emit):
        if self.process is None:
            context = mp.get_context("spawn")
            self.pipe, child = context.Pipe()
            self.process = context.Process(
                target=self.target, args=(self.options, child), daemon=True
            )
            self.process.start()
            child.close()
        self.pipe.send((operation, target))
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if self.pipe.poll(min(0.25, max(0, deadline - time.monotonic()))):
                try:
                    kind, payload = self.pipe.recv()
                except EOFError:
                    break
                if kind == "done":
                    return payload
                if kind == "record":
                    emit(payload)
            elif not self.process.is_alive():
                break
        self.close()
        return dict(
            status="TIMEOUT",
            reason="scweet_operation_deadline",
            warnings=["partial_operation_rows_only"],
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
                self.process.terminate()
                self.process.join(2)
            if self.process.is_alive():
                self.process.kill()
                self.process.join(2)
            self.pipe.close()
            self.process = self.pipe = None


class TwitterCrawler(SocialExportMixin):
    """Scweet-only trial; uses the existing shared sink, filters and Excel format."""

    def __init__(
        self,
        config=None,
        *,
        worker=None,
        progress=None,
        monotonic=time.monotonic,
        sleep=time.sleep,
    ):
        self.config = configuration(config or ROOT / "config/twitter_crawler.json")
        self.include = contract.KeywordMatcher(self.config["include_keywords"])
        self.exclude = contract.KeywordMatcher(self.config["exclude_keywords"])
        self.worker = worker or ScweetWorker(self.config["scweet"])
        self.synthetic = worker is not None
        self.progress = progress or (lambda event: None)
        self.clock, self.sleep = monotonic, sleep

    def plan(self):
        return dict(
            config=deepcopy(self.config),
            upstream_version=upstream_version(),
            acquisition_backend=METHOD,
            platform_scope="twitter_only",
            live_access_verified=False,
            trial_passed=False,
            integrated_into_social_crawler=False,
            date_scope="root_publication;until_exclusive",
            comments_complete=False,
            primary_output=dict(
                file=COMPACT_FILE, sheets=["Data"], columns=list(COMPACT_COLUMNS)
            ),
        )

    def _baseline(self):
        keys, sources = set(), []
        for supplied in self.config["exclude_existing_datasets"]:
            path = (ROOT / supplied).resolve()
            if path.is_dir():
                path /= "Contents.jsonl"
            with path.open("rb") as stream:
                digest = sha256(stream.read()).hexdigest()
            if path.suffix != ".jsonl":
                raise ValueError(
                    "Twitter baseline must be an audit bundle or Contents.jsonl"
                )
            for line in path.read_text(encoding="utf-8").splitlines():
                row = json.loads(line)
                contract.validate_row("Contents", row)
                if row["platform"] == "twitter":
                    key = object_key(row["native_id"])
                    if (
                        post_url(row["canonical_url"])
                        != "https://x.com/i/web/status/" + row["native_id"]
                    ):
                        raise ValueError("Baseline native ID and URL disagree")
                    keys.add(key)
            sources.append(dict(path=str(path), sha256=digest))
        return keys, sources

    def _searches(self):
        p = self.config["platforms"]["twitter"]
        start, end = (
            contract.utc_datetime(self.config["since"]),
            contract.utc_datetime(self.config["until"]),
        )
        emitted = 0
        while end > start:
            lower = max(start, end - timedelta(days=p["search_window_days"]))
            # Date-only search bounds enclose the precise local timestamp window.
            upper_date = (
                (end + timedelta(days=bool(end.time().isoformat() != "00:00:00")))
                .date()
                .isoformat()
            )
            for query in p["queries"]:
                if emitted >= p["max_searches"]:
                    return
                emitted += 1
                yield dict(
                    query=query,
                    since=lower.date().isoformat(),
                    until=upper_date,
                    lang=p["lang"],
                    display_type="Latest",
                    limit=p["search_results"],
                )
            end = lower

    def close(self):
        if not self.synthetic:
            self.worker.close()

    def run(self, output_dir):
        excluded, baselines = self._baseline()
        output = Path(output_dir).resolve()
        run_id = str(uuid.uuid4())
        factory = contract.RecordFactory(
            self.config["project_id"], run_id, self.include
        )
        sink = contract.BundleSink(output, self.config["project_id"], run_id)
        dataset = contract.Dataset(factory, sink)
        p = self.config["platforms"]["twitter"]
        began = self.clock()
        deadline = began + self.config["total_seconds"]
        counts = dict(
            posts_exported=0,
            comments=0,
            replies=0,
            duplicates_skipped=0,
            existing_records_skipped=0,
            invalid_rows=0,
            search_calls=0,
            operations=0,
            cooldown_waits=0,
            cooldown_seconds=0,
        )
        seen, selected_roots, reply_queued = set(), set(), set()
        searches = iter(self._searches())
        work = deque(
            ("lookup", dict(tweet_id=url.rsplit("/", 1)[1])) for url in p["urls"]
        )
        stop, last_finished, network, interrupted = (
            "CANDIDATES_EXHAUSTED",
            None,
            {},
            False,
        )
        filtered, receipts = Counter(), Counter()
        progress_path = output.with_name(output.name + ".progress.json")

        def event(stage, **extra):
            payload = dict(
                stage=stage,
                platform="twitter",
                observed_at=contract.now_iso(),
                elapsed_seconds=round(self.clock() - began, 2),
                remaining_seconds=round(max(0, deadline - self.clock()), 2),
                **counts,
                **extra,
            )
            private_json(progress_path, payload)
            self.progress(payload)

        def accept(item, root_id=None, origin=None):
            try:
                raw = normalize_item(item, root_id=root_id, discovered_from=origin)
                key = object_key(raw.native_id)
                if key in seen:
                    counts["duplicates_skipped"] += 1
                    return
                if key in excluded:
                    counts["existing_records_skipped"] += 1
                    return
                row, _ = factory.content(raw)
                if raw.object_type == "post":
                    if item.get("in_reply_to_tweet_id") or item.get("is_retweet"):
                        filtered["search_reply_or_repost"] += 1
                        return
                    selected, reason = self._select({"Contents": [row]})
                    if not selected:
                        filtered[reason] += 1
                        return
                    if counts["posts_exported"] >= p["max_posts"]:
                        return
                elif raw.thread_root_key not in selected_roots or any(
                    self.exclude.find(raw.text_source)
                ):
                    filtered["unselected_reply_context"] += 1
                    return
                metrics = [
                    (key, item.get(key), "count")
                    for key in (
                        "likes",
                        "comments",
                        "retweets",
                        "views",
                        "quotes",
                        "bookmarks",
                    )
                ]
                if dataset.add_content(raw, metrics):
                    seen.add(key)
                    counts[
                        {
                            "post": "posts_exported",
                            "comment": "comments",
                            "reply": "replies",
                        }[raw.object_type]
                    ] += 1
                    if raw.object_type == "post":
                        selected_roots.add(key)
                        if (
                            p["max_comments"]
                            and item.get("comments", 0) > 0
                            and key not in reply_queued
                        ):
                            reply_queued.add(key)
                            work.append(
                                (
                                    "replies",
                                    dict(
                                        tweet_id=raw.native_id, limit=p["max_comments"]
                                    ),
                                )
                            )
            except (ValueError, TypeError, KeyError, AttributeError):
                counts["invalid_rows"] += 1

        try:
            event("started")
            while self.clock() < deadline:
                if counts["posts_exported"] >= p["min_posts"] and not work:
                    stop = "TARGET_MET"
                    break
                if work:
                    operation, target = work.popleft()
                else:
                    try:
                        target = next(searches)
                    except StopIteration:
                        break
                    operation = "search"
                    counts["search_calls"] += 1
                if last_finished is not None:
                    try:
                        self.sleep(
                            min(
                                max(
                                    0,
                                    last_finished
                                    + self.config["delay"]["seconds"]
                                    - self.clock(),
                                ),
                                max(0, deadline - self.clock()),
                            )
                        )
                    except KeyboardInterrupt:
                        stop, interrupted = "INTERRUPTED", True
                        break
                if self.clock() >= deadline:
                    stop = "TIME_BUDGET_EXHAUSTED"
                    break
                event("operation_started", operation=operation)
                started = contract.now_iso()
                before = dataset.contents
                try:
                    result = self.worker(
                        operation,
                        target,
                        min(self.config["timeout_seconds"], deadline - self.clock()),
                        lambda row: accept(
                            row,
                            root_id=target["tweet_id"]
                            if operation == "replies"
                            else None,
                            origin=target.get("query"),
                        ),
                    )
                except KeyboardInterrupt:
                    result, interrupted = (
                        dict(status="INTERRUPTED", reason="operator_stop", warnings=[]),
                        True,
                    )
                except Exception as error:
                    result = error_receipt(error)
                last_finished = self.clock()
                counts["operations"] += 1
                receipts[result["status"]] += 1
                network = result.get("network", network)
                sink.write(
                    "Runs",
                    factory.row(
                        "Runs",
                        unit_id=str(uuid.uuid4()),
                        source="twitter",
                        operation=operation,
                        target=json.dumps(target, ensure_ascii=False),
                        status=result["status"],
                        reason=result.get("reason", "scweet_read"),
                        coverage="PARTIAL",
                        contents_written=dataset.contents - before,
                        comments_seen=counts["comments"],
                        replies_seen=counts["replies"],
                        duplicates_skipped=counts["duplicates_skipped"],
                        invalid_rows=counts["invalid_rows"],
                        max_comments=p["max_comments"],
                        max_replies=p["max_comments"],
                        timeout_seconds=self.config["timeout_seconds"],
                        keywords=self.config["include_keywords"],
                        source_version=upstream_version(),
                        warning_codes=result.get("warnings", []),
                        started_at=started,
                        finished_at=contract.now_iso(),
                    ),
                )
                event("operation_finished", operation=operation, receipt=result)
                if result["status"] == "COOLDOWN":
                    wait = result["retry_after_seconds"]
                    if wait >= deadline - self.clock():
                        stop = "COOLDOWN_EXCEEDS_TIME_BUDGET"
                        break
                    counts["cooldown_waits"] += 1
                    counts["cooldown_seconds"] += wait
                    event("cooldown_wait", wait_seconds=wait)
                    try:
                        self.sleep(wait)
                    except KeyboardInterrupt:
                        stop, interrupted = "INTERRUPTED", True
                        break
                    work.appendleft((operation, target))
                    continue
                if result["status"] != "FINISHED_BEST_EFFORT":
                    stop = result["status"]
                    break
            else:
                stop = "TIME_BUDGET_EXHAUSTED"
            dataset.finish_relations()
            live = bool(dataset.contents and not self.synthetic)
            summary = dict(
                status="TARGET_MET"
                if counts["posts_exported"] >= p["min_posts"]
                else "PARTIAL"
                if dataset.contents
                else stop,
                stop_reason=stop,
                producer_version=VERSION,
                upstream_version=upstream_version(),
                acquisition_backend=METHOD,
                live_access_verified=live,
                trial_passed=bool(
                    live
                    and not interrupted
                    and stop not in BARRIERS
                    and stop
                    not in {
                        "TIMEOUT",
                        "SOURCE_ERROR",
                        "ACCOUNT_UNAVAILABLE",
                        "COOLDOWN_EXCEEDS_TIME_BUDGET",
                    }
                ),
                synthetic=self.synthetic,
                interrupted=interrupted,
                integrated_into_social_crawler=False,
                run_id=run_id,
                output_dir=str(output),
                primary_file=str(output / COMPACT_FILE),
                elapsed_seconds=round(self.clock() - began, 2),
                configured_seconds=self.config["total_seconds"],
                comments_complete=False,
                filtered_roots=dict(filtered),
                receipt_status_counts=dict(receipts),
                network=network,
                deduplication_sources=baselines,
                posts_shortfall=max(0, p["min_posts"] - counts["posts_exported"]),
                **counts,
            )
            sink.write(
                "Sources",
                factory.row(
                    "Sources",
                    source="twitter",
                    producer_version="twitter-crawler:" + VERSION,
                    upstream_version=upstream_version(),
                    extraction_method=METHOD,
                    access_mode="saved_web_session;read_only;no_password_replay",
                    config={**deepcopy(self.config), "summary": summary},
                    schema_fingerprint=contract.schema_fingerprint(),
                    observed_at=contract.now_iso(),
                ),
            )
            for stream in sink.files.values():
                stream.flush()
            summary["compact"] = self._write_compact(
                sink.stage, sink.stage / COMPACT_FILE
            )
            contract.add_readme(
                sink,
                factory,
                [
                    (
                        "TwitterCrawler",
                        "Scweet bounded search and replies; shared native-ID audit contract and formula-safe Excel.",
                    ),
                    (
                        "Cakupan",
                        "Replies are capped, not exhaustive. Missing native parents remain unresolved references. Curated text completeness is unknown.",
                    ),
                    (
                        "Autentikasi",
                        "Local auth.json sessionid maps to auth_token. Runtime SQLite contains secrets and stays outside Git. First HTTP429/login/challenge stops network without identity rotation.",
                    ),
                    ("Ringkasan", json.dumps(summary, ensure_ascii=False)),
                ],
            )
            (sink.stage / "summary.json").write_text(
                json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            sink.finish(
                dict(
                    source="twitter",
                    mode="twitter_crawler",
                    producer_version=VERSION,
                    synthetic=self.synthetic,
                    primary_file=COMPACT_FILE,
                    trial_passed=summary["trial_passed"],
                )
            )
            event("finished", status=summary["status"], stop_reason=stop)
            return summary
        except BaseException:
            if not sink.closed:
                sink.abort()
            raise
        finally:
            self.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=ROOT / "config/twitter_crawler.json"
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    crawler = TwitterCrawler(
        args.config,
        progress=lambda event: print(json.dumps(event, ensure_ascii=False), flush=True),
    )
    try:
        result = (
            crawler.plan()
            if args.dry_run
            else crawler.run(
                args.output_dir
                or ROOT
                / "outputs"
                / (
                    "twitter_scweet_"
                    + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                )
            )
        )
    finally:
        crawler.close()
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return 0 if args.dry_run or result.get("trial_passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
