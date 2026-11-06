"""Small access barriers shared by the bounded YouTube and Reddit workers."""

import asyncio
import hashlib
import json
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


class SourceBarrier(Exception):
    def __init__(self, status, reason, retry_after_seconds=None):
        super().__init__(reason)
        self.status = status
        self.reason = reason
        self.retry_after_seconds = retry_after_seconds


def http_barrier(code, headers=None):
    status = (
        "RATE_LIMITED"
        if code == 429
        else "ACCESS_BLOCKED"
        if code in {401, 403}
        else "SERVER_UNAVAILABLE"
        if isinstance(code, int) and 500 <= code <= 599
        else None
    )
    if not status:
        return None
    headers = headers or {}
    value = headers.get("Retry-After") or headers.get("retry-after")
    if isinstance(value, (bytes, bytearray, memoryview)):
        value = bytes(value).decode("ascii", errors="ignore")
    wait = None
    if value is not None:
        try:
            wait = max(0, int(value))
        except (ValueError, TypeError):
            try:
                date = parsedate_to_datetime(str(value))
                wait = max(0, (date - datetime.now(timezone.utc)).total_seconds())
            except (ValueError, TypeError, OverflowError):
                pass
    return SourceBarrier(status, f"upstream_http_{code}", wait)


class RedditRequestGate:
    """Serialize requests, wait after responses and latch the first barrier.

    Reddrix 1.2.14's decorated get/post methods retry access barriers internally.
    Call their wrapped implementations once; the coordinator owns any retry.
    """

    def __init__(self, delay, *, clock=time.monotonic, sleep=asyncio.sleep):
        self.delay = max(1.0, delay)
        self.clock, self.sleep = clock, sleep
        self.lock = asyncio.Lock()
        self.finished = None
        self.barrier = None
        self.seen = set()
        self.last_progress = clock()

    def progress(self):
        self.last_progress = self.clock()

    async def request(self, source, method, url, kwargs):
        async with self.lock:
            if self.barrier:
                raise self.barrier
            if not source.is_running:
                return None
            if self.clock() - self.last_progress >= 75:
                self.barrier = SourceBarrier("PARTIAL", "reddit_native_ids_stagnated")
                raise self.barrier
            if self.finished is not None:
                await self.sleep(max(0, self.finished + self.delay - self.clock()))
            if not source.is_running:
                return None
            if self.clock() - self.last_progress >= 75:
                self.barrier = SourceBarrier("PARTIAL", "reddit_native_ids_stagnated")
                raise self.barrier
            # Retain only a digest; cursor/form values never appear in receipts.
            key = hashlib.sha256(
                json.dumps([method.__name__, url, kwargs], sort_keys=True).encode()
            ).digest()
            if key in self.seen:
                self.barrier = SourceBarrier(
                    "PARTIAL", "repeated_reddit_request_cursor"
                )
                raise self.barrier
            self.seen.add(key)
            try:
                return await method(source, url, **kwargs)
            except SourceBarrier as error:
                self.barrier = error
                raise
            except Exception as error:
                if type(error).__name__ in {
                    "AntiBotBlockError",
                    "FatalAntiBotBlockError",
                }:
                    self.barrier = SourceBarrier(
                        "ACCESS_BLOCKED", "reddrix_access_barrier_http_status_unknown"
                    )
                    raise self.barrier from None
                raise
            finally:
                self.finished = self.clock()


class RedditClientGuard:
    """Inspect HTTP status before Reddrix discards it as an anti-bot error."""

    def __init__(self, client, gate):
        self.client, self.gate = client, gate

    def __getattr__(self, name):
        return getattr(self.client, name)

    async def _send(self, method, *args, **kwargs):
        if self.gate.barrier:
            raise self.gate.barrier
        response = await method(*args, **kwargs)
        error = http_barrier(response.status.as_int(), response.headers)
        if error:
            self.gate.barrier = error
            raise error
        return response

    async def get(self, *args, **kwargs):
        return await self._send(self.client.get, *args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self._send(self.client.post, *args, **kwargs)


def controlled_reddrix(upstream):
    get = getattr(getattr(upstream, "get", None), "__wrapped__", None)
    post = getattr(getattr(upstream, "post", None), "__wrapped__", None)
    if get is None or post is None:
        raise ImportError("Unsupported Reddrix request hooks; verify pinned SDK")

    class ControlledReddrix(upstream):
        async def __aenter__(self):
            self.request_gate = RedditRequestGate(getattr(self, "request_delay", 2))
            result = await super().__aenter__()
            client = getattr(self, "_Reddrix__client", None)
            if client is None:
                await super().__aexit__(None, None, None)
                raise ImportError("Unsupported Reddrix HTTP client; verify pinned SDK")
            self._Reddrix__client = RedditClientGuard(client, self.request_gate)
            return result

        async def get(self, url, params=None):
            return await self.request_gate.request(
                self, get, url, {"params": params or {}}
            )

        async def post(self, url, params=None, json_data=None, form_data=None):
            return await self.request_gate.request(
                self,
                post,
                url,
                dict(
                    params=params or {},
                    json_data=json_data or {},
                    form_data=form_data or {},
                ),
            )

    return ControlledReddrix
