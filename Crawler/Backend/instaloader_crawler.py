"""Standalone Instaloader experiment using BeeSense's shared Excel contract."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import multiprocessing as mp
import os
import re
import tempfile
import time
import traceback
from collections import OrderedDict
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from itertools import islice
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlsplit

from Crawler.Backend import instagram_crawler as ig

METHOD = "instaloader_saved_web_session"
COOKIE_NAMES = {"sessionid", "csrftoken", "ds_user_id", "mid", "ig_did", "rur"}


def upstream_version():
    try:
        return importlib.metadata.version("instaloader")
    except importlib.metadata.PackageNotFoundError:
        return None


class AccessBarrier(RuntimeError):
    def __init__(self, status, http_status=None, retry_after=None, upstream_code=None):
        self.status, self.http_status, self.retry_after = (
            status,
            http_status,
            retry_after,
        )
        self.upstream_code = upstream_code


def retry_after_seconds(value):
    if not isinstance(value, str):
        return None
    if value.strip().isdigit():
        return int(value.strip())
    try:
        stamp = parsedate_to_datetime(value)
        if stamp.tzinfo is not None:
            return max(0, int((stamp - datetime.now(timezone.utc)).total_seconds()) + 1)
    except (ValueError, TypeError, OverflowError):
        pass
    return None


def error_receipt(error):
    chain, current = [], error
    while current is not None and current not in chain:
        chain.append(current)
        current = current.__cause__ or current.__context__
    names = {c.__name__ for e in chain for c in type(e).__mro__}
    barrier = next((e for e in chain if isinstance(e, AccessBarrier)), None)
    status = "SOURCE_ERROR"
    if barrier:
        status = barrier.status
    elif names & {"TooManyRequestsException"}:
        status = "RATE_LIMITED"
    elif names & {"LoginRequiredException", "LoginException", "FileNotFoundError"}:
        status = "LOGIN_REQUIRED"
    elif "AbortDownloadException" in names:
        status = "ACCESS_BLOCKED"
    elif isinstance(error, ig.SessionInvalid):
        status = "SESSION_INVALID"
    elif isinstance(error, ImportError):
        status = "DEPENDENCY_MISSING"
    elif isinstance(error, KeyboardInterrupt):
        status = "INTERRUPTED"
    return dict(
        status=status,
        reason="instaloader_" + status.lower(),
        warnings=[type(error).__name__]
        + (
            [f"http_status_{barrier.http_status}"]
            if barrier and barrier.http_status
            else []
        ),
        source_version=upstream_version(),
        http_status=barrier.http_status if barrier else None,
        retry_after_seconds=barrier.retry_after if barrier else None,
        upstream_code=barrier.upstream_code if barrier else None,
        code_locations=[
            dict(file=Path(frame.filename).name, line=frame.lineno, function=frame.name)
            for frame in traceback.extract_tb(error.__traceback__)
        ],
    )


@dataclass(frozen=True)
class InstaloaderSettings:
    username: str
    auth_file: str | None
    session_file: str
    request_interval_seconds: float = 5
    request_timeout_seconds: int = 30
    search_results: int = 10
    max_comments: int = 20
    max_replies: int = 10
    max_replies_per_thread: int = 5
    search_tab: str = "recent"
    comments_transport: str = "query_hash"
    timeout_seconds: int = 60


def _json(path):
    path = Path(path)
    if path.stat().st_size > 1_000_000:
        raise ig.SessionInvalid("Local settings exceed 1 MB")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as error:
        raise ig.SessionInvalid("Invalid local JSON settings") from error


def session_cookies(settings):
    """Load JSON cookies only; never unpickle a session or replay a password."""
    if Path(settings.session_file).is_file():
        data = _json(settings.session_file)
        if not isinstance(data, dict) or data.get("username") != settings.username:
            raise ig.SessionInvalid("Saved session identity mismatch")
        cookies = data.get("cookies")
    else:
        data = _json(settings.auth_file) if settings.auth_file else []
        entries = data if isinstance(data, list) else [data]
        entries = [
            e
            for e in entries
            if isinstance(e, dict)
            and str(e.get("sosmed", "")).casefold() == "instagram"
        ]
        if len(entries) != 1:
            raise ig.SessionInvalid("Exactly one Instagram auth entry required")
        cookies = {k: v for k, v in entries[0].items() if k in COOKIE_NAMES}
    if not isinstance(cookies, dict) or set(cookies) - COOKIE_NAMES:
        raise ig.SessionInvalid("Invalid session cookie object")
    if not cookies.get("sessionid") or any(
        not isinstance(v, str)
        or not v
        or len(v) > 4096
        or any(ord(c) < 33 or ord(c) > 126 for c in v)
        for v in cookies.values()
    ):
        raise ig.SessionInvalid("Missing or malformed local session cookies")
    # Instaloader.load_session requires this key; an absent token is fetched by
    # upstream when needed. Empty here does not assert that a token was captured.
    return {"csrftoken": "", **cookies}


def save_session(loader, settings):
    path = Path(settings.session_file)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    cookies = {
        k: v for k, v in loader.save_session().items() if k in COOKIE_NAMES and v
    }
    fd, temporary = tempfile.mkstemp(prefix=".instaloader-", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(dict(username=settings.username, cookies=cookies), stream)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextmanager
def observe_requests(interval):
    """Observe all upstream sessions inside the dedicated, single-thread worker.

    Instaloader copies requests sessions for some queries, so a hook on only its
    primary session would miss responses. No headers, bodies or cookies are logged.
    """
    import requests

    original, previous = requests.Session.send, None

    def send(session, request, **kwargs):
        nonlocal previous
        host = urlsplit(request.url).hostname or ""
        instagram = host == "instagram.com" or host.endswith(".instagram.com")
        if instagram and previous is not None:
            time.sleep(max(0, previous + interval - time.monotonic()))
        if instagram:
            previous = time.monotonic()
        response = original(session, request, **kwargs)
        if not instagram:
            return response
        code = response.status_code
        retry = retry_after_seconds(response.headers.get("Retry-After"))
        status = {
            429: "RATE_LIMITED",
            401: "LOGIN_REQUIRED",
            403: "ACCESS_BLOCKED",
        }.get(code)
        location = urlsplit(response.headers.get("Location", "")).path
        if 300 <= code < 400 and location.startswith("/accounts/login"):
            status = "LOGIN_REQUIRED"
        elif 300 <= code < 400 and location.startswith(("/challenge", "/checkpoint")):
            status = "CHALLENGE_REQUIRED"
        upstream_code = None
        if not status and response.headers.get("Content-Type", "").startswith(
            "application/json"
        ):
            try:
                data = response.json()
            except ValueError:
                data = None
            if isinstance(data, dict):
                message = data.get("message")
                if message == "login_required":
                    status = "LOGIN_REQUIRED"
                elif message == "feedback_required":
                    status = "ACCESS_BLOCKED"
                elif isinstance(message, str) and message in {
                    "challenge_required",
                    "checkpoint_required",
                }:
                    status = "CHALLENGE_REQUIRED"
                if status:
                    upstream_code = message
        if status:
            response.close()
            raise AccessBarrier(status, code, retry, upstream_code)
        return response

    requests.Session.send = send
    try:
        yield
    finally:
        requests.Session.send = original


def _utc(value):
    # Instaloader explicitly documents date_utc/created_at_utc as UTC, but returns
    # naive datetime objects. This conversion is specific to these upstream fields.
    if not isinstance(value, datetime):
        return None
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def configure_web_graphql(loader):
    """Apply the supplied runtime patch to this worker's context only."""
    from Crawler.Backend.instaloader_browser_patch import apply_browser_patch

    apply_browser_patch(loader.context)


class InstaloaderAdapter:
    def __init__(self, settings, *, loader=None, module=None, comments=None):
        if module is None:
            import instaloader as module
        self.module, self.settings = module, settings
        self.loader = loader or module.Instaloader(
            quiet=True,
            sleep=True,
            max_connection_attempts=1,
            request_timeout=settings.request_timeout_seconds,
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            save_metadata=False,
            iphone_support=False,
        )
        if loader is None:
            self.loader.load_session(settings.username, session_cookies(settings))
            configure_web_graphql(self.loader)
        self.searches = {}
        self.posts = OrderedDict()
        self.comments = comments or (
            self.legacy_comments
            if settings.comments_transport == "query_hash"
            else self.web_comments
        )

    def legacy_comments(self, post):
        """Prefer the library's GraphQL iterator, as upstream PR #2692 does.

        Avoid Post.get_comments()'s unconditional mobile path for larger threads.
        Pagination remains bounded by the export cap and the worker deadline.
        """
        if post.comments == 0:
            return

        def wrap(node):
            item = self.web_comment(node)
            edges = (node.get("edge_threaded_comments") or {}).get("edges", [])
            item.answers = (self.web_comment(edge["node"]) for edge in edges)
            return item

        yield from self.module.NodeIterator(
            self.loader.context,
            "97b41c52301f77ce508f55e66d17620e",
            lambda response: response["data"]["shortcode_media"][
                "edge_media_to_parent_comment"
            ],
            wrap,
            {"shortcode": post.shortcode},
            f"https://www.instagram.com/p/{post.shortcode}/",
        )

    def web_comments(self, post):
        """Bounded web comments through Instaloader's patched context.

        Query shape is documented in upstream issue #2651. Replies are limited
        to previews returned with the parent, with no claim of full coverage.
        """
        from instaloader.exceptions import BadResponseException

        if post.comments == 0:
            return
        cursor, cursors, seen = None, set(), set()
        while len(seen) < self.settings.max_comments:
            response = self.loader.context.doc_id_graphql_query(
                "25060748103519434",
                dict(
                    media_id=str(post.mediaid),
                    first=min(20, self.settings.max_comments),
                    after=cursor,
                    before=None,
                    last=None,
                    sort_order="popular",
                    __relay_internal__pv__PolarisIsLoggedInrelayprovider=True,
                ),
                referer=f"https://www.instagram.com/p/{post.shortcode}/",
                web_api=True,
            )
            connection = (response.get("data") or {}).get(
                "xdt_api__v1__media__media_id__comments__connection"
            )
            if not isinstance(connection, dict) or not isinstance(
                connection.get("edges"), list
            ):
                raise BadResponseException("Web comment connection is unavailable")
            for edge in connection["edges"]:
                node = edge["node"]
                item = self.web_comment(node)
                native = ig.native_pk(item.id)
                if native in seen:
                    continue
                seen.add(native)
                item.answers = (
                    self.web_comment(child)
                    for child in node.get("preview_child_comments", []) or []
                )
                yield item
                if len(seen) >= self.settings.max_comments:
                    return
            page = connection.get("page_info") or {}
            next_cursor = page.get("end_cursor")
            if (
                not page.get("has_next_page")
                or not next_cursor
                or next_cursor in cursors
            ):
                return
            cursors.add(next_cursor)
            cursor = next_cursor

    @staticmethod
    def web_comment(node):
        author = node.get("user") or node.get("owner") or {}
        stamp = node.get("created_at")
        return SimpleNamespace(
            id=node.get("pk") or node.get("id"),
            text=node["text"],
            created_at_utc=datetime.fromtimestamp(stamp, timezone.utc)
            if type(stamp) in (int, float)
            else None,
            owner=SimpleNamespace(userid=author.get("pk") or author.get("id")),
            likes_count=node.get(
                "comment_like_count",
                node.get("like_count", (node.get("edge_liked_by") or {}).get("count")),
            ),
        )

    def collect(self, operation, target, emit):
        settings, module = self.settings, self.module
        result = dict(
            status="FINISHED_BEST_EFFORT",
            reason="instaloader_" + operation,
            warnings=["comments_not_exhaustive"],
            source_version=upstream_version(),
        )
        if operation == "check_session":
            if self.loader.test_login() != settings.username:
                raise AccessBarrier("LOGIN_REQUIRED")
            save_session(self.loader, settings)
        elif operation == "search":
            query = json.loads(target)
            tag, cursor = query["hashtag"], query.get("cursor")
            if cursor is None:
                hashtag = module.Hashtag.from_name(self.loader.context, tag)
                iterator = iter(
                    hashtag.get_posts_resumable()
                    if settings.search_tab == "recent"
                    else hashtag.get_top_posts()
                )
                self.searches[tag] = (iterator, 0)
            iterator, offset = self.searches[tag]
            if cursor is not None and cursor != str(offset):
                raise ValueError("Unexpected hashtag cursor")
            found = 0
            for post in islice(iterator, settings.search_results):
                url = ig.media_url(f"https://www.instagram.com/p/{post.shortcode}/")
                self.posts[url] = post
                if len(self.posts) > 1000:
                    self.posts.popitem(last=False)
                emit(
                    "candidate",
                    dict(
                        url=url,
                        discovered_from=f"https://www.instagram.com/explore/tags/{tag}/",
                    ),
                )
                found += 1
            offset += found
            self.searches[tag] = (iterator, offset)
            result["next_cursor"] = (
                str(offset) if found == settings.search_results else None
            )
        elif operation == "media":
            url = ig.media_url(target)
            post = self.posts.pop(url, None)
            if post is None:
                post = module.Post.from_shortcode(
                    self.loader.context, url.strip("/").split("/")[-1]
                )
            media = dict(
                pk=post.mediaid,
                code=post.shortcode,
                caption_text=post.caption or "",
                taken_at=_utc(post.date_utc),
                user=dict(pk=post.owner_id),
                like_count=post.likes,
                comment_count=post.comments,
            )
            emit("record", ig.normalize_item(media, url))
            seen, replies, parents = set(), 0, 0
            for comment in self.comments(post):
                native = ig.native_pk(comment.id)
                if native in seen:
                    continue
                seen.add(native)
                emit("record", self.comment(comment, url, media))
                parents += 1
                cap = min(
                    settings.max_replies_per_thread, settings.max_replies - replies
                )
                thread_count = 0
                if cap:
                    for answer in comment.answers:
                        key = ig.native_pk(answer.id)
                        if key in seen:
                            continue
                        seen.add(key)
                        emit("record", self.comment(answer, url, media, native))
                        replies += 1
                        thread_count += 1
                        if thread_count >= cap:
                            break
                if parents >= settings.max_comments:
                    break
            if parents:
                save_session(self.loader, settings)
        else:
            raise ValueError("Unknown Instaloader operation")
        return result

    @staticmethod
    def comment(item, url, media, parent=None):
        value = dict(
            pk=item.id,
            text=item.text,
            created_at_utc=_utc(item.created_at_utc),
            user=dict(pk=item.owner.userid),
            like_count=item.likes_count,
        )
        return ig.normalize_item(value, url, media=media, parent=parent)


def instaloader_worker(settings, pipe):
    try:
        with (
            open(os.devnull, "w") as quiet,
            redirect_stdout(quiet),
            redirect_stderr(quiet),
        ):
            with observe_requests(settings["request_interval_seconds"]):
                adapter = None
                while True:
                    command = pipe.recv()
                    if command is None:
                        break
                    try:
                        adapter = adapter or InstaloaderAdapter(
                            InstaloaderSettings(**settings)
                        )
                        result = adapter.collect(
                            *command, lambda kind, row: pipe.send((kind, row))
                        )
                    except (Exception, KeyboardInterrupt) as error:
                        result = error_receipt(error)
                    pipe.send(("done", result))
                    if result["status"] in ig.STOP_STATUSES - {"RATE_LIMITED"}:
                        break
                if adapter:
                    adapter.loader.close()
    except (EOFError, BrokenPipeError):
        pass
    finally:
        pipe.close()


class InstaloaderWorker:
    """One subprocess and rate controller, with killable per-operation deadlines."""

    def __init__(self, entry=instaloader_worker):
        self.entry, self.process, self.pipe, self.stopped = entry, None, None, False

    def __call__(self, operation, target, settings, seconds, emit):
        if self.stopped:
            return dict(
                status="WORKER_FAILED", reason="worker_already_stopped", warnings=[]
            )
        deadline = time.monotonic() + seconds
        if self.process is None:
            context = mp.get_context("spawn")
            self.pipe, child = context.Pipe()
            self.process = context.Process(
                target=self.entry, args=(asdict(settings), child), daemon=True
            )
            self.process.start()
            child.close()
        try:
            self.pipe.send((operation, target))
            while time.monotonic() < deadline:
                if self.pipe.poll(min(0.2, max(0, deadline - time.monotonic()))):
                    kind, payload = self.pipe.recv()
                    if kind == "done":
                        return payload
                    emit(kind, payload)
                elif not self.process.is_alive():
                    break
            status = "TIMEOUT" if self.process.is_alive() else "WORKER_FAILED"
            self.close()
            return dict(
                status=status,
                reason="worker_deadline_or_exit",
                warnings=[],
                source_version=upstream_version(),
            )
        except (EOFError, BrokenPipeError):
            self.close()
            return dict(
                status="WORKER_FAILED",
                reason="worker_connection_closed",
                warnings=[],
                source_version=upstream_version(),
            )

    def close(self):
        self.stopped = True
        if self.pipe:
            try:
                self.pipe.send(None)
            except (BrokenPipeError, OSError):
                pass
            self.pipe.close()
            self.pipe = None
        if self.process:
            self.process.join(timeout=0.2)
            if self.process.is_alive():
                self.process.terminate()
                self.process.join(timeout=0.5)
            if self.process.is_alive():
                self.process.kill()
                self.process.join(timeout=0.5)


def instaloader_options(options):
    """Validate shared Instaloader settings without loading credentials or networking."""
    defaults = dict(
        username="researchinnovationsocs",
        auth_file="config/auth.json",
        session_file="output/instaloader/session.json",
        request_interval_seconds=5,
        request_timeout_seconds=30,
        comments_transport="query_hash",
    )
    if not isinstance(options, dict) or set(options) - set(defaults):
        raise ValueError("Unknown Instaloader setting")
    options = {**defaults, **options}
    if options["comments_transport"] not in {"query_hash", "web_doc_id"}:
        raise ValueError("comments_transport must be query_hash or web_doc_id")
    if not isinstance(options["username"], str) or not re.fullmatch(
        r"[A-Za-z0-9_.]{1,30}", options["username"]
    ):
        raise ValueError("Instaloader username must be an Instagram handle")
    for key in ("session_file", "auth_file"):
        value = options[key]
        if value is None and key == "auth_file":
            continue
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Invalid local " + key)
        options[key] = str((ig.ROOT / value).resolve())
    for key, low, high in (
        ("request_interval_seconds", 5, 300),
        ("request_timeout_seconds", 5, 120),
    ):
        value = options[key]
        if type(value) is not int or not low <= value <= high:
            raise ValueError(f"{key} must be an integer in {low}..{high}")
    return options


class InstaloaderCrawler(ig.InstagramCrawler):
    """Separate backend; preserves the existing export and native-ID dedup logic."""

    def __init__(self, config=None, *, worker=None, **kwargs):
        cfg = (
            _json(config or ig.ROOT / "config/instaloader_crawler.json")
            if not isinstance(config, dict)
            else dict(config)
        )
        if not isinstance(cfg, dict):
            raise ValueError("Instaloader config must be an object")
        if (
            cfg.pop("backend", "instaloader") != "instaloader"
            or "instagrapi" in cfg
            or "browser" in cfg
        ):
            raise ValueError("This class requires backend=instaloader")
        options = instaloader_options(cfg.pop("instaloader", {}))
        cfg["instagrapi"] = dict(session_file=options["session_file"])
        owned_worker = InstaloaderWorker() if worker is None else None
        super().__init__(cfg, worker=worker or owned_worker, **kwargs)
        if self.config["platforms"]["instagram"]["search_tab"] not in {"recent", "top"}:
            raise ValueError("Instaloader supports recent or top hashtag searches")
        if self.config["platforms"]["instagram"]["rate_limit_max_retries"] != 0:
            raise ValueError("Instaloader experiment stops at the first HTTP 429")
        self.config.pop("instagrapi")
        self.config.update(backend="instaloader", instaloader=options)
        self.settings = InstaloaderSettings(
            **options,
            timeout_seconds=self.config["timeout_seconds"],
            **{
                k: self.config["platforms"]["instagram"][k]
                for k in (
                    "search_results",
                    "max_comments",
                    "max_replies",
                    "max_replies_per_thread",
                    "search_tab",
                )
            },
        )
        self.synthetic = worker is not None
        self.method, self.backend_version = METHOD, upstream_version()
        self.access_mode = "saved_web_session;no_password_replay;read_only_acquisition"
        self._owned_worker = owned_worker
        self._delegate_worker = self.worker
        self.worker = self._operation

    def _operation(self, operation, target, settings, seconds, emit):
        result = self._delegate_worker(operation, target, settings, seconds, emit)
        self.progress(
            dict(
                stage="instaloader_receipt",
                operation=operation,
                **{
                    k: result.get(k)
                    for k in (
                        "status",
                        "reason",
                        "warnings",
                        "source_version",
                        "http_status",
                        "retry_after_seconds",
                        "upstream_code",
                        "code_locations",
                    )
                },
            )
        )
        return result

    def plan(self):
        return {
            **super().plan(),
            "session_input_present": Path(self.settings.session_file).is_file()
            or bool(
                self.settings.auth_file and Path(self.settings.auth_file).is_file()
            ),
            "search_scope": "Instaloader hashtag iterator; dates and keywords enforced locally",
            "one_rate_controller_per_run": True,
            "automatic_login": False,
        }

    def run(self, output_dir):
        try:
            return super().run(output_dir)
        finally:
            self.close()

    def close(self):
        if self._owned_worker:
            self._owned_worker.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=ig.ROOT / "config/instaloader_crawler.json"
    )
    parser.add_argument("--output-dir", type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--check-session", action="store_true")
    args = parser.parse_args()
    crawler = InstaloaderCrawler(
        args.config, progress=lambda e: print(json.dumps(e), flush=True)
    )
    try:
        if args.dry_run:
            result = crawler.plan()
        elif args.check_session:
            result = crawler.check_session()
        else:
            result = crawler.run(
                args.output_dir
                or ig.ROOT
                / "outputs"
                / (
                    "instagram_instaloader_"
                    + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                )
            )
    finally:
        crawler.close()
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return (
        0
        if args.dry_run
        or result.get("status") in {"TARGET_MET", "FINISHED_BEST_EFFORT"}
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
