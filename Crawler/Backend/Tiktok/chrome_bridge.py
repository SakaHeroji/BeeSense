"""Live, loopback-only task/result bridge for an already-connected Chrome agent.

The browser agent drives the user's tab through its existing connector. This
worker streams observed public records into SocialCrawler; it never owns Chrome,
reads a profile, or turns saved captures into pretend live acquisition.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import math
import queue
import re
import secrets
import threading
import time
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

LIVE_METHOD = "beesense_existing_chrome_live"
LIVE_VERSION = "BeeSenseChromeLive:1.2.1"
COMMENT_PROTOCOL = "source-pagination-v3"
STATUSES = {
    "FINISHED_BEST_EFFORT",
    "CAPTCHA_REQUIRED",
    "LOGIN_REQUIRED",
    "ACCESS_BLOCKED",
    "RATE_LIMITED",
    "SOURCE_ERROR",
    "INTERRUPTED",
    "COMMENTS_INCOMPLETE",
    "CLIENT_UPGRADE_REQUIRED",
}
WARNINGS = {
    "comments_completeness_unverified",
    "comment_ids_not_in_dom",
    "post_metadata_unavailable",
    "visible_pagination_idle",
    "reply_parent_not_observed",
    "human_validation_required",
    "native_json_unavailable",
    "comments_pagination_not_exhausted",
    "uncapped_comments_stopped_on_idle",
    "source_comment_pagination_exhausted",
    "comments_count_below_source_total",
    "comment_control_error",
    "tiktok_view_changed",
    "chrome_command_timeout",
}
FIELDS = {
    "id",
    "video_id",
    "kind",
    "link",
    "description",
    "text",
    "created_at",
    "published_display",
    "parent_comment_id",
    "like_count",
    "reply_count",
    "stats",
}


class ChromeLiveWorker:
    """One pending operation at a time, with streamed batches and stale-task rejection."""

    extraction_method = LIVE_METHOD
    access_mode = "existing_chrome;live_connected_browser_agent;loopback_task_bridge"
    live_chrome = True

    def __init__(self, *, port=0, selection=None, extension_mode=False, progress=None):
        if type(port) is not int or not 0 <= port <= 65535:
            raise ValueError("Invalid Chrome bridge port")
        self.lock = threading.Lock()
        self.active = None
        self.closed = False
        self.received = 0
        self.selection = deepcopy(selection or {})
        self.extension_mode = extension_mode
        if extension_mode:
            self.access_mode = (
                "existing_chrome;automatic_local_extension;ui_network_capture"
            )
        self.progress = progress or (lambda event: None)
        self.connected = threading.Event()
        self.client_info = None
        self.client_error = None
        self.cooldown_file = (
            Path(__file__).resolve().parents[3] / ".cache/tiktok/native_cooldown.json"
        )
        manifest = json.loads(
            (Path(__file__).parent / "chrome_extension/manifest.json").read_text()
        )
        digest = hashlib.sha256(base64.b64decode(manifest["key"])).hexdigest()[:32]
        self.extension_origin = "chrome-extension://" + "".join(
            chr(ord("a") + int(c, 16)) for c in digest
        )
        self.nonce = secrets.token_urlsafe(32)
        worker = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass  # Never log request bodies, source URLs or form credentials.

            def send(self, status, body, kind="text/html; charset=utf-8"):
                body = body.encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                if self.headers.get("Origin") == worker.extension_origin:
                    self.send_header(
                        "Access-Control-Allow-Origin", worker.extension_origin
                    )
                    self.send_header(
                        "Access-Control-Allow-Headers",
                        "Authorization,Content-Type,X-BeeSense-Comment-Policy,X-BeeSense-Connector-Version,X-BeeSense-Connector-Build",
                    )
                    self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
                    self.send_header("Vary", "Origin")
                self.send_header("Referrer-Policy", "same-origin")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header(
                    "Content-Security-Policy",
                    "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'",
                )
                self.end_headers()
                self.wfile.write(body)

            def host_allowed(self):
                return self.headers.get("Host") == worker.origin.removeprefix("http://")

            def extension_allowed(self):
                return (
                    worker.extension_mode
                    and self.host_allowed()
                    and self.headers.get("Origin") in {None, worker.extension_origin}
                    and hmac.compare_digest(
                        self.headers.get("Authorization", ""), "Bearer " + worker.nonce
                    )
                )

            def compatible_client(self):
                version = self.headers.get("X-BeeSense-Connector-Version", "")
                build = self.headers.get("X-BeeSense-Connector-Build", "")
                return (
                    re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}", version) is not None
                    and tuple(map(int, version.split("."))) >= (1, 2, 1)
                    and self.headers.get("X-BeeSense-Comment-Policy")
                    == COMMENT_PROTOCOL
                    and re.fullmatch(r"[a-zA-Z0-9._-]{1,80}", build) is not None
                )

            def do_OPTIONS(self):
                if (
                    self.host_allowed()
                    and worker.extension_mode
                    and self.headers.get("Origin") == worker.extension_origin
                ):
                    return self.send(204, "")
                self.send(403, "Rejected origin")

            def do_GET(self):
                if self.path == "/api/task":
                    if not self.extension_allowed():
                        return self.send(403, "Rejected client")
                    if not self.compatible_client():
                        if worker.client_error is None:
                            worker.client_error = "Reload BeeSense TikTok Connector 1.2.1 from this project"
                            worker.progress(
                                dict(
                                    stage="connector_upgrade_required",
                                    minimum_version="1.2.1",
                                    crawling_started=False,
                                )
                            )
                        return self.send(
                            409, "Reload connector 1.2.1: comment protocol required"
                        )
                    worker.client_info = {
                        "version": self.headers["X-BeeSense-Connector-Version"],
                        "build": self.headers["X-BeeSense-Connector-Build"],
                        "comment_policy": COMMENT_PROTOCOL,
                    }
                    worker.client_error = None
                    worker.connected.set()
                    with worker.lock:
                        task = (
                            deepcopy(worker.active["task"])
                            if worker.active and not worker.active["finished"]
                            else None
                        )
                    return self.send(
                        200, json.dumps(task, ensure_ascii=False), "application/json"
                    )
                if not self.host_allowed() or self.path != "/":
                    return self.send(404, "Not found")
                self.send(200, worker.page())

            def do_POST(self):
                if self.path in {"/api/result", "/api/progress"}:
                    if not self.extension_allowed():
                        return self.send(403, "Rejected client")
                    if not self.compatible_client():
                        return self.send(
                            409, "Reload connector 1.2.1: comment protocol required"
                        )
                    try:
                        size = int(self.headers.get("Content-Length", "0"))
                        if not 0 < size <= 4_000_000:
                            raise ValueError
                        data = json.loads(self.rfile.read(size))
                        if self.path == "/api/result":
                            worker.submit(data)
                        else:
                            with worker.lock:
                                if (
                                    not worker.active
                                    or data.get("operation_id")
                                    != worker.active["task"]["operation_id"]
                                    or data.get("stage")
                                    not in {
                                        "captcha_required",
                                        "login_required",
                                        "browser_detached",
                                    }
                                ):
                                    raise ValueError
                            worker.progress(
                                {"stage": data["stage"], "platform": "tiktok"}
                            )
                    except (ValueError, TypeError, KeyError):
                        return self.send(400, "Invalid or stale batch")
                    return self.send(200, '{"accepted":true}', "application/json")
                origin = self.headers.get("Origin")
                same_site_form = (
                    origin in {None, "null"}
                    and self.headers.get("Sec-Fetch-Site") == "same-origin"
                )
                if (
                    not self.host_allowed()
                    or (origin != worker.origin and not same_site_form)
                    or self.path != "/result"
                ):
                    return self.send(403, "Rejected origin")
                try:
                    size = int(self.headers.get("Content-Length", "0"))
                    if not 0 < size <= 4_000_000:
                        raise ValueError
                    form = parse_qs(
                        self.rfile.read(size).decode("utf-8"),
                        max_num_fields=3,
                        keep_blank_values=True,
                    )
                    nonce = form.get("nonce", [""])[0]
                    if not hmac.compare_digest(nonce, worker.nonce):
                        return self.send(403, "Rejected form")
                    worker.submit(json.loads(form["batch"][0]))
                except (ValueError, TypeError, KeyError, UnicodeError):
                    return self.send(400, "Invalid or stale batch; no rows accepted")
                self.send(200, worker.page("Batch accepted"))

        self.server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        self.server.daemon_threads = True
        self.origin = f"http://127.0.0.1:{self.server.server_port}"
        self.bridge_url = self.origin + "/"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def page(self, notice=""):
        with self.lock:
            task = deepcopy(self.active["task"]) if self.active else None
            count = self.received
        return f"""<!doctype html><html lang="en"><meta charset="utf-8">
<title>BeeSense · Live Chrome bridge</title>
<style>body{{font:16px system-ui;max-width:900px;margin:36px auto;padding:0 24px}}textarea{{width:100%;min-height:160px;font:14px monospace}}button{{font:inherit;padding:12px 20px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}</style>
<h1>Live Chrome bridge</h1><p>Connected browser agent required. This process never launches or closes Chrome.</p>
<p role="status">{escape(notice)} · {count} events accepted</p>
<p>{escape(self.client_error or "")}</p>
<p>Verified connector: {escape(json.dumps(self.client_info))}</p>
<h2>Current task</h2><pre id="task">{escape(json.dumps(task, ensure_ascii=False))}</pre>
{('<details><summary>Connect BeeSense extension</summary><p>Use this URL and the temporary pairing code in the extension popup. The code is local and expires when this process stops.</p><label>Pairing code <input readonly value="' + escape(self.nonce) + '"></label></details>') if self.extension_mode else ""}
<form method="post" action="/result"><input type="hidden" name="nonce" value="{escape(self.nonce)}">
<label for="batch">Batch JSON</label><textarea id="batch" name="batch" required></textarea>
<button type="submit">Send live batch</button></form></html>"""

    def submit(self, data):
        from Crawler.Backend.tiktok_crawler import native_id, normalize_item, parse_url

        if (
            not isinstance(data, dict)
            or type(data.get("done")) is not bool
            or not isinstance(data.get("events"), list)
            or len(data["events"]) > 2000
        ):
            raise ValueError("Invalid live batch")
        status = data.get("status", "FINISHED_BEST_EFFORT")
        warnings = data.get("warnings", [])
        if (
            status not in STATUSES
            or not isinstance(warnings, list)
            or any(w not in WARNINGS for w in warnings)
        ):
            raise ValueError("Invalid live receipt")
        with self.lock:
            active = self.active
            if (
                active is None
                or active["finished"]
                or data.get("operation_id") != active["task"]["operation_id"]
            ):
                raise ValueError("Stale live operation")
            task = active["task"]
        if (
            self.extension_mode
            and data["done"]
            and task["operation"] == "thread"
            and task["collect_all_comments"]
            and status == "FINISHED_BEST_EFFORT"
        ):
            collection_status = data.get("collection_status")
            if "visible_pagination_idle" in warnings:
                status = "CLIENT_UPGRADE_REQUIRED"
                warnings = [*warnings, "uncapped_comments_stopped_on_idle"]
            elif collection_status not in {"exhausted", "root_filtered"}:
                status = "COMMENTS_INCOMPLETE"
                warnings = [*warnings, "comments_pagination_not_exhausted"]
            elif collection_status == "exhausted":
                warnings = [*warnings, "source_comment_pagination_exhausted"]
        events = []
        for event in data["events"]:
            if not isinstance(event, dict) or not isinstance(
                event.get("payload"), dict
            ):
                raise ValueError("Invalid live event")
            kind, supplied = event.get("kind"), event["payload"]
            if kind == "candidate" and task["operation"] == "search":
                ident, _, comment = parse_url(supplied["url"])
                if comment:
                    raise ValueError("Candidate must be a post")
                payload = {"url": supplied["url"], "discovered_from": task["target"]}
                cached = supplied.get("cached_root")
                if cached is not None:
                    cached = {k: v for k, v in cached.items() if k in FIELDS}
                    if normalize_item(cached).native_id != ident:
                        raise ValueError("Candidate metadata ID mismatch")
                    payload["cached_root"] = cached
            elif kind == "record" and task["operation"] != "search":
                if not isinstance(supplied.get("id"), str):
                    raise ValueError("Native ID must be a string")
                payload = {k: v for k, v in supplied.items() if k in FIELDS}
                raw = normalize_item(payload)
                if raw.thread_root_key.rsplit(":", 1)[-1] != native_id(
                    task["video_id"]
                ):
                    raise ValueError("Record belongs to another post")
                payload["observed_at"] = datetime.now(timezone.utc).isoformat()
                if raw.object_type == "post":
                    from Crawler.Backend.tiktok_crawler import metric_number

                    if not isinstance(payload.get("stats", {}), dict):
                        raise ValueError("Invalid live statistics")
                    payload["stats"] = {
                        key: metric_number(value)
                        for key, value in payload.get("stats", {}).items()
                    }
                else:
                    from Crawler.Backend.tiktok_crawler import metric_number

                    for key in ("like_count", "reply_count"):
                        payload[key] = metric_number(payload.get(key))
            else:
                raise ValueError("Wrong event for operation")
            events.append((kind, payload))
        with self.lock:
            if self.active is not active or active["finished"]:
                raise ValueError("Stale live operation")
            active["finished"] = data["done"]
            if status == "RATE_LIMITED":
                wait = data.get("retry_after_seconds", 60)
                if (
                    type(wait) not in (int, float)
                    or not math.isfinite(wait)
                    or wait <= 0
                ):
                    wait = 60
                active["retry_after_seconds"] = math.ceil(wait)
                self.cooldown_file.parent.mkdir(parents=True, exist_ok=True)
                temporary = self.cooldown_file.with_suffix(".live.tmp")
                temporary.write_text(json.dumps({"not_before": time.time() + wait}))
                temporary.chmod(0o600)
                temporary.replace(self.cooldown_file)
            self.received += len(events)
            active["queue"].put((events, data["done"], status, warnings))

    def __call__(self, operation, target, settings, seconds, emit):
        from Crawler.Backend.crawler_limits import reached

        try:
            left = (
                json.loads(self.cooldown_file.read_text())["not_before"] - time.time()
            )
            if left > 0:
                return dict(
                    status="RATE_LIMITED",
                    reason="persisted_server_retry_after",
                    retry_after_seconds=math.ceil(left),
                    warnings=[],
                    source_version=LIVE_VERSION,
                )
        except (OSError, ValueError, TypeError, KeyError):
            pass

        task = dict(
            operation_id=uuid.uuid4().hex,
            operation=operation,
            target=target if operation == "search" else None,
            search_results=settings.search_results,
            max_comments=settings.max_comments,
            collect_all_comments=settings.max_comments is None,
            max_replies=settings.max_replies,
            max_replies_per_thread=settings.max_replies_per_thread,
            selection=self.selection,
            expires_at_unix=None if math.isinf(seconds) else time.time() + seconds,
            scroll_pause_seconds=settings.scroll_pause_seconds,
            request_interval_seconds=settings.request_interval_seconds,
            idle_scroll_limit=settings.idle_scroll_limit,
        )
        if operation != "search":
            cached = target.get("cached_root") or {}
            task.update(
                video_id=target["video_id"],
                url=cached.get("link")
                or next(
                    (
                        u
                        for u in settings.urls
                        if u.rstrip("/").endswith("/" + target["video_id"])
                    ),
                    "https://www.tiktok.com/@_/video/" + target["video_id"],
                ),
                cached_root=cached or None,
            )
        active = dict(task=task, queue=queue.Queue(), finished=False)
        with self.lock:
            if self.closed or self.active is not None:
                raise ValueError("Chrome bridge unavailable")
            self.active = active
        deadline = time.monotonic() + seconds
        seen, parents, per_parent = set(), set(), {}
        comments = replies = candidates = 0
        root_observed = False
        try:
            while time.monotonic() < deadline:
                try:
                    events, done, status, warnings = active["queue"].get(
                        timeout=min(0.25, max(0, deadline - time.monotonic()))
                    )
                except queue.Empty:
                    if self.closed:
                        break
                    continue
                for kind, item in events:
                    if kind == "candidate":
                        if item["url"] in seen or reached(
                            candidates, settings.search_results
                        ):
                            continue
                        seen.add(item["url"])
                        candidates += 1
                    else:
                        ident = item["id"]
                        if ident in seen:
                            continue
                        content_kind = item.get("kind", "post")
                        if content_kind == "post":
                            root_observed = True
                        if content_kind == "comment":
                            if reached(comments, settings.max_comments):
                                continue
                            comments += 1
                            parents.add(ident)
                        elif content_kind == "reply":
                            parent = item["parent_comment_id"]
                            if (
                                parent not in parents
                                or reached(replies, settings.max_replies)
                                or reached(
                                    per_parent.get(parent, 0),
                                    settings.max_replies_per_thread,
                                )
                            ):
                                continue
                            replies += 1
                            per_parent[parent] = per_parent.get(parent, 0) + 1
                        seen.add(ident)
                    emit(kind, item)
                if events:
                    self.progress(
                        dict(
                            stage="chrome_capture_progress",
                            platform="tiktok",
                            operation=operation,
                            operation_id=task["operation_id"],
                            video_id=task.get("video_id"),
                            posts_observed=int(root_observed),
                            comments_observed=comments,
                            replies_observed=replies,
                            candidates_observed=candidates,
                        )
                    )
                if done:
                    return dict(
                        status=status,
                        reason="live_chrome_ui_operation",
                        warnings=list(
                            dict.fromkeys(
                                [*warnings, "comments_completeness_unverified"]
                            )
                        ),
                        source_version=LIVE_VERSION,
                        **(
                            {"retry_after_seconds": active["retry_after_seconds"]}
                            if active.get("retry_after_seconds")
                            else {}
                        ),
                    )
            return dict(
                status="TIMEOUT",
                reason="live_chrome_operation_deadline",
                warnings=["partial_operation_rows_only"],
                source_version=LIVE_VERSION,
            )
        finally:
            with self.lock:
                if self.active is active:
                    self.active = None

    def close(self):
        if self.closed:
            return
        self.closed = True
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(2)

    def wait_for_extension(self, seconds=600):
        deadline = time.monotonic() + seconds
        next_notice = time.monotonic() + 15
        while time.monotonic() < deadline and not self.closed:
            if self.connected.wait(min(1, max(0, deadline - time.monotonic()))):
                return
            if time.monotonic() >= next_notice:
                self.progress(
                    dict(
                        stage="waiting_for_chrome_extension",
                        platform="tiktok",
                        crawling_started=False,
                        pairing_seconds_remaining=max(
                            0, math.ceil(deadline - time.monotonic())
                        ),
                    )
                )
                next_notice = time.monotonic() + 15
        raise TimeoutError("Chrome extension pairing timed out")
