"""Offline SDK boundaries; no social network requests are made here."""

import asyncio
import unittest
from copy import deepcopy
from dataclasses import asdict
from types import SimpleNamespace
from unittest.mock import Mock, patch

import yt_dlp
from yt_dlp.extractor.youtube import YoutubeIE

from Crawler.Backend.crawler_network import (
    RedditClientGuard,
    RedditRequestGate,
    SourceBarrier,
    controlled_reddrix,
    http_barrier,
)
from Crawler.Backend.social_crawler import (
    SocialCrawler,
    collect_reddrix,
    reddrix_error_receipt,
)
from Crawler.Backend.Youtube import crawl_youtube as yt
from Crawler.Backend.Youtube.youtube_runtime import controlled_youtube_dl
from tests.crawler.test_reddit_crawler import CONFIG, URL, FakeReddrix, item, records

SELECTION = {k: deepcopy(CONFIG[k]) for k in ("since", "until", "include_keywords")}
SELECTION.update(exclude_keywords=[], include_mode="any")
VIDEO = dict(
    id="00000000000", title="Kuliah", description="Kampus", timestamp=1780297200
)


def youtube_fixture(rows, *, selection=None, cap=100, metadata=None):
    events, options = [], []
    pipe = Mock()
    pipe.send.side_effect = events.append
    settings = asdict(yt.Settings(max_comments=cap, selection=selection))

    def extract(client, *args, **kwargs):
        options.append(client.params)
        return dict(
            VIDEO if metadata is None else metadata,
            __post_extractor=client.get_info_extractor("Youtube").extract_comments(),
        )

    with (
        patch.object(yt_dlp.YoutubeDL, "extract_info", extract),
        patch.object(
            YoutubeIE, "_get_comments", side_effect=lambda *args, **kw: iter(rows)
        ),
        patch.object(yt.os, "setsid"),
    ):
        yt.worker("video", "https://youtu.be/00000000000", settings, pipe)
    return events, options


class YouTubePerformanceTests(unittest.TestCase):
    def test_root_filters_do_not_consume_comment_generator(self):
        for change, reason in [
            (
                {"title": "Other", "description": "Other"},
                "root_missing_include_keyword",
            ),
            ({"timestamp": 0}, "root_outside_date_window"),
            ({"timestamp": None}, "root_publication_date_unknown"),
        ]:
            with self.subTest(reason=reason):
                consumed = []

                def rows():
                    consumed.append(True)
                    yield {"id": "c1", "text": "comment"}

                events, _ = youtube_fixture(
                    rows(), selection=SELECTION, metadata={**VIDEO, **change}
                )
                self.assertEqual(consumed, [])
                self.assertEqual(events[-1][1]["reason"], reason)
                self.assertEqual(events[0][0], "video")

    def test_exclude_and_all_keywords_share_export_policy(self):
        for policy in [
            dict(SELECTION, exclude_keywords=["kampus"]),
            dict(
                SELECTION, include_mode="all", include_keywords=["kuliah", "beasiswa"]
            ),
        ]:
            events, _ = youtube_fixture([], selection=policy)
            self.assertIn("root_filtered_before_comments", events[-1][1]["warnings"])

    def test_streamed_comments_survive_failure_without_buffering(self):
        def rows():
            yield {"id": "c1", "text": "first", "parent": "root"}
            raise TimeoutError("timeout")

        events, _ = youtube_fixture(rows())
        self.assertEqual([kind for kind, _ in events], ["video", "comment", "done"])
        self.assertEqual(events[1][1]["id"], "c1")
        self.assertEqual(events[-1][1]["status"], "NETWORK_TIMEOUT")

    def test_dedup_and_limit_stop_before_fetching_another_page(self):
        consumed = []

        def rows():
            for native in ["c1", "c1", "c2", "c3"]:
                consumed.append(native)
                yield {"id": native, "text": "comment"}

        events, options = youtube_fixture(rows(), cap=2)
        self.assertEqual(consumed, ["c1", "c1", "c2"])
        self.assertEqual([r["id"] for k, r in events if k == "comment"], ["c1", "c2"])
        self.assertEqual(events[-1][1]["status"], "LIMIT_REACHED")
        self.assertEqual(options[0]["sleep_interval_requests"], 2)
        self.assertEqual(options[0]["extractor_retries"], 0)

    def test_zero_comments_is_metadata_only(self):
        yt.Settings(max_comments=0).validate()
        events, options = youtube_fixture([], cap=0)
        self.assertFalse(options[0]["getcomments"])
        self.assertEqual([k for k, _ in events], ["video", "done"])
        self.assertEqual(events[-1][1]["reason"], "metadata_only_requested")

    def test_lazy_search_does_not_request_an_extra_entry(self):
        consumed = []

        def entries():
            for native in ["00000000000", "00000000001", "00000000002"]:
                consumed.append(native)
                yield {"id": native}

        pipe = Mock()
        options = []

        def extract(client, *args, **kwargs):
            options.append(client.params)
            return {"entries": entries()}

        with (
            patch.object(yt_dlp.YoutubeDL, "extract_info", extract),
            patch.object(yt.os, "setsid"),
        ):
            yt.worker("search", "kuliah", asdict(yt.Settings(search_results=2)), pipe)
        self.assertEqual(len(consumed), 2)
        self.assertTrue(options[0]["lazy_playlist"])

    def test_http_barrier_prevents_fallback_requests(self):
        cls, _ = controlled_youtube_dl(
            asdict(yt.Settings()), yt.SafeLogger(), lambda *x: None
        )
        response = Mock(status=503, headers={"Retry-After": "30"})
        with (
            cls({"quiet": True}) as client,
            patch.object(yt_dlp.YoutubeDL, "urlopen", return_value=response) as send,
        ):
            for _ in range(2):
                with self.assertRaises(SourceBarrier) as caught:
                    client.urlopen("https://www.youtube.com/watch?v=00000000000")
                self.assertEqual(caught.exception.status, "SERVER_UNAVAILABLE")
                self.assertEqual(caught.exception.retry_after_seconds, 30)
            self.assertEqual(send.call_count, 1)
            response.close.assert_called_once()

    def test_stagnation_stops_before_another_network_request(self):
        cls, _ = controlled_youtube_dl(
            asdict(yt.Settings()), yt.SafeLogger(), lambda *x: None
        )
        with (
            cls({"quiet": True}) as client,
            patch.object(yt_dlp.YoutubeDL, "urlopen") as send,
        ):
            client.last_progress -= 76
            with self.assertRaises(SourceBarrier) as caught:
                client.urlopen("https://www.youtube.com/watch?v=00000000000")
            self.assertEqual(caught.exception.status, "PARTIAL")
            send.assert_not_called()


class RedditPerformanceTests(unittest.TestCase):
    def collect(self, rows, **settings):
        class Source(FakeReddrix):
            consumed = 0
            closed = False

            async def get_items(self):
                try:
                    for row in rows:
                        type(self).consumed += 1
                        yield row
                finally:
                    type(self).closed = True

        events = []
        config = dict(
            asdict(
                SocialCrawler(CONFIG)._legacy_settings(
                    "reddit", SocialCrawler(CONFIG).config["platforms"]["reddit"]
                )
            ),
            **settings,
        )
        result = asyncio.run(
            collect_reddrix(
                "thread", URL, config, lambda *e: events.append(e), factory=Source
            )
        )
        return result, events, Source

    def test_root_filtered_before_advancing_comments(self):
        result, events, source = self.collect(
            [dict(item(), title="Other", bodyText="Unrelated"), *records()[1:]]
        )
        self.assertEqual(source.consumed, 1)
        self.assertTrue(source.closed)
        self.assertEqual(result["reason"], "root_missing_include_keyword")
        self.assertEqual(len(events), 1)

    def test_cap_closes_iterator_without_reading_next_item(self):
        result, events, source = self.collect(
            [*records(), item("extra1", "t3_abc123")], max_comments=2
        )
        self.assertEqual(source.consumed, 3)
        self.assertTrue(source.closed)
        self.assertEqual(result["status"], "LIMIT_REACHED")
        self.assertEqual(
            [r["fullname"] for _, r in events], ["t3_abc123", "t1_com123", "t1_rpl123"]
        )

    def test_zero_comments_disables_sdk_comments(self):
        result, events, source = self.collect(records(), max_comments=0)
        self.assertFalse(source.options["include_comments"])
        self.assertEqual(source.consumed, 1)
        self.assertEqual(result["reason"], "metadata_only_requested")
        self.assertEqual(len(events), 1)

    def test_search_filters_candidates_before_thread_startup(self):
        class Source(FakeReddrix):
            items = [dict(item(), title="Other", bodyText="Other"), item()]

        events = []
        settings = asdict(yt.Settings(selection=SELECTION))
        settings["subreddits"] = ["indonesia"]
        asyncio.run(
            collect_reddrix(
                "search",
                "https://www.reddit.com/r/indonesia/search/?q=kuliah",
                settings,
                lambda *e: events.append(e),
                factory=Source,
            )
        )
        # The rejected observation must not poison dedupe for a later valid one.
        self.assertEqual(
            events,
            [
                (
                    "candidate",
                    {
                        "url": "https://www.reddit.com/comments/abc123/",
                        "discovered_from": "https://www.reddit.com/r/indonesia/search/?q=kuliah",
                    },
                )
            ],
        )


class RequestGateTests(unittest.IsolatedAsyncioTestCase):
    async def test_stagnation_and_cancellation_prevent_new_requests(self):
        now = [0]
        gate = RedditRequestGate(1, clock=lambda: now[0])
        source = SimpleNamespace(is_running=True)
        sent = []

        async def get(*args, **kwargs):
            sent.append(True)

        now[0] = 76
        with self.assertRaises(SourceBarrier) as caught:
            await gate.request(source, get, URL, {})
        self.assertEqual(caught.exception.status, "PARTIAL")
        self.assertEqual(sent, [])
        gate = RedditRequestGate(1)
        source.is_running = False
        await gate.request(source, get, URL, {})
        self.assertEqual(sent, [])

    async def test_serialized_response_based_pacing(self):
        now = [0]
        starts = []

        async def sleep(seconds):
            now[0] += seconds
            await asyncio.sleep(0)

        gate = RedditRequestGate(2, clock=lambda: now[0], sleep=sleep)
        source = SimpleNamespace(is_running=True)

        async def get(source, url, **kwargs):
            starts.append(now[0])
            await asyncio.sleep(0)
            now[0] += 3
            return "body"

        await asyncio.gather(*(gate.request(source, get, str(i), {}) for i in range(3)))
        self.assertEqual(starts, [0, 5, 10])

    async def test_repeated_cursor_stops_without_another_request(self):
        async def sleep(_):
            pass

        gate = RedditRequestGate(1, sleep=sleep)
        source = SimpleNamespace(is_running=True)
        sent = []

        async def post(*args, **kwargs):
            sent.append(True)

        await gate.request(source, post, URL, {"cursor": "opaque"})
        with self.assertRaises(SourceBarrier) as caught:
            await gate.request(source, post, URL, {"cursor": "opaque"})
        self.assertEqual(caught.exception.status, "PARTIAL")
        self.assertEqual(sent, [True])
        self.assertNotIn("opaque", str(caught.exception))

    async def test_http_status_and_retry_after_survive_sdk(self):
        for code, status in [
            (403, "ACCESS_BLOCKED"),
            (429, "RATE_LIMITED"),
            (503, "SERVER_UNAVAILABLE"),
        ]:
            with self.subTest(code=code):
                gate = RedditRequestGate(1)
                calls = []

                async def get(*args, **kw):
                    calls.append(True)
                    return SimpleNamespace(
                        status=SimpleNamespace(as_int=lambda: code),
                        headers={"Retry-After": "90"},
                    )

                guard = RedditClientGuard(SimpleNamespace(get=get), gate)
                for _ in range(2):
                    with self.assertRaises(SourceBarrier) as caught:
                        await guard.get(URL)
                    result = reddrix_error_receipt(caught.exception)
                    self.assertEqual(result["status"], status)
                    self.assertEqual(result["retry_after_seconds"], 90)
                self.assertEqual(calls, [True])

    async def test_real_sdk_hooks_are_supported_without_network(self):
        from reddrix.reddrix import Reddrix

        cls = controlled_reddrix(Reddrix)
        self.assertTrue(issubclass(cls, Reddrix))
        self.assertIsNotNone(Reddrix.get.__wrapped__)
        self.assertIsNotNone(Reddrix.post.__wrapped__)

    async def test_real_sdk_stops_on_status_without_cookie_refresh(self):
        from reddrix.reddrix import Reddrix
        from wreq import HeaderMap

        cls = controlled_reddrix(Reddrix)
        source = cls(stealth=False, verbose=False)
        source.request_gate = RedditRequestGate(1)
        source.started = True
        calls = []

        async def get(*args, **kwargs):
            calls.append(True)
            return SimpleNamespace(
                status=SimpleNamespace(as_int=lambda: 429),
                headers=HeaderMap({"Retry-After": "90"}),
            )

        source._Reddrix__client = RedditClientGuard(
            SimpleNamespace(get=get), source.request_gate
        )
        for _ in range(2):
            with self.assertRaises(SourceBarrier) as caught:
                await source.get(URL)
            self.assertEqual(caught.exception.retry_after_seconds, 90)
        self.assertEqual(calls, [True])

    async def test_unwrapped_call_does_not_refresh_or_retry(self):
        calls = []

        class AntiBotBlockError(Exception):
            pass

        async def get(source, url, **kwargs):
            calls.append(True)
            raise AntiBotBlockError()

        gate = RedditRequestGate(1)
        source = SimpleNamespace(is_running=True)
        for _ in range(2):
            with self.assertRaises(SourceBarrier):
                await gate.request(source, get, URL, {})
        self.assertEqual(calls, [True])

    async def test_unknown_sdk_is_rejected(self):
        with self.assertRaises(ImportError):
            controlled_reddrix(object)

    async def test_retry_after_http_date(self):
        error = http_barrier(429, {"Retry-After": "Fri, 31 Dec 9999 23:59:59 GMT"})
        self.assertGreater(error.retry_after_seconds, 0)
        self.assertIsNone(http_barrier(200))


if __name__ == "__main__":
    unittest.main()
