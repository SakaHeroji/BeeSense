"""Offline integration and failure contracts for the native TikTok browser crawler."""

import asyncio
import json
import tempfile
import time
import unittest
from copy import deepcopy
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from openpyxl import load_workbook

from Crawler.Backend import tiktok_crawler as t
from Crawler.Backend.crawler_config import read_config
from Crawler.Backend.social_archive import organize, verify
from Crawler.Backend.social_identity import identity


def video(ident="100", text="Kuliah kampus", date="2026-06-01T00:00:00Z"):
    return dict(
        id=ident,
        link=f"https://www.tiktok.com/@example/video/{ident}",
        description=text,
        created_at=date,
        stats={"play_count": 250, "like_count": 10, "comment_count": 2},
    )


def comment(ident="200", kind="comment", root="100", parent=None):
    return dict(
        id=ident,
        video_id=root,
        kind=kind,
        link=f"https://www.tiktok.com/@example/video/{root}?comment_id={ident}",
        text="Komentar konteks",
        created_at="2026-06-01T01:00:00Z",
        parent_comment_id=parent,
        like_count=1,
    )


async def stream(items):
    for item in items:
        yield item


def source_comment(ident="200", root="100", replies=0):
    return dict(
        cid=ident,
        aweme_id=root,
        text="Komentar konteks",
        create_time=1780272000,
        digg_count=1,
        reply_comment_total=replies,
    )


def source_video(ident="100", text="Kuliah kampus"):
    return dict(
        id=ident,
        desc=text,
        createTime=1780272000,
        author=dict(uniqueId="example"),
        stats=dict(playCount=250),
    )


def hanging_worker(config, pipe):
    pipe.send(("ready", None))
    pipe.recv()
    pipe.send(("record", video()))
    time.sleep(10)


class TikTokTests(unittest.TestCase):
    def test_extension_cli_waits_for_pairing_before_creating_crawler(self):
        from Crawler.Backend.Tiktok.chrome_bridge import ChromeLiveWorker

        worker = Mock(spec=ChromeLiveWorker)
        worker.bridge_url = "http://127.0.0.1:12345/"
        with (
            patch(
                "sys.argv",
                [
                    "tiktok_crawler",
                    "--chrome-extension",
                    "--target-posts",
                    "500",
                    "--total-seconds",
                    "1800",
                    "--manual-wait-seconds",
                    "3600",
                ],
            ),
            patch("sys.stdout", new_callable=StringIO),
            patch(
                "Crawler.Backend.Tiktok.chrome_bridge.ChromeLiveWorker",
                return_value=worker,
            ),
            patch.object(t, "TikTokCrawler") as constructor,
        ):

            def before_pairing(**options):
                constructor.assert_not_called()
                self.assertEqual(options, {"seconds": 3600})

            worker.wait_for_extension.side_effect = before_pairing
            constructor.return_value.run.return_value = {"status": "TARGET_MET"}
            self.assertEqual(t.main(), 0)
            supplied = constructor.call_args.args[0]
            self.assertEqual(supplied["total_seconds"], 1800)
            self.assertEqual(supplied["platforms"]["tiktok"]["min_posts"], 500)
        worker.wait_for_extension.assert_called_once_with(seconds=3600)
        worker.close.assert_called_once()

    def test_pairing_timeout_never_starts_crawler_and_closes_bridge(self):
        from Crawler.Backend.Tiktok.chrome_bridge import ChromeLiveWorker

        worker = Mock(spec=ChromeLiveWorker)
        worker.bridge_url = "http://127.0.0.1:12345/"
        worker.wait_for_extension.side_effect = TimeoutError
        with (
            patch("sys.argv", ["tiktok_crawler", "--chrome-extension"]),
            patch("sys.stdout", new_callable=StringIO) as output,
            patch(
                "Crawler.Backend.Tiktok.chrome_bridge.ChromeLiveWorker",
                return_value=worker,
            ),
            patch.object(t, "TikTokCrawler") as constructor,
        ):
            self.assertEqual(t.main(), 2)
            constructor.assert_not_called()
            receipt = json.loads(output.getvalue().splitlines()[-1])
            self.assertEqual(receipt["status"], "CHROME_PAIRING_TIMEOUT")
            self.assertFalse(receipt["crawling_started"])
        worker.close.assert_called_once()
        with (
            patch("sys.argv", ["tiktok_crawler"]),
            patch("sys.stdout", new_callable=StringIO) as output,
            patch.object(t, "TikTokCrawler") as constructor,
        ):
            constructor.return_value.run.side_effect = TimeoutError
            self.assertEqual(t.main(), 2)
            receipt = json.loads(output.getvalue().splitlines()[-1])
            self.assertEqual(receipt["status"], "CONFIG_OR_RUNTIME_ERROR")

    def test_extension_plan_reports_real_transport_without_browser_or_auth(self):
        with patch.object(t, "auth_material", side_effect=AssertionError("auth read")):
            plan = t.live_chrome_plan(extension=True)
        self.assertEqual(plan["browser_acquisition"], "existing_chrome_extension")
        self.assertIn("ChromeExtension:1.1.0", plan["browser_backend_version"])
        self.assertNotIn("Playwright", plan["browser_backend_version"])
        self.assertTrue(plan["run_clock_starts_after_extension_pairing"])
        self.assertTrue(plan["extension_pairing_required"])
        self.assertFalse(t.live_chrome_plan()["extension_pairing_required"])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.config = read_config()
        self.config.update(exclude_existing_datasets=[], total_seconds=60)
        self.config["delay"]["seconds"] = 0
        self.config["platforms"]["tiktok"].update(
            min_posts=1, queries=["kuliah"], search_results=5
        )

    def client(self):
        crawler = t.TikTokCrawler(self.config)
        self.addCleanup(crawler._tiktok_worker.close)
        client = t.NativeTikTokClient(crawler.config)
        locator = Mock()
        locator.first = locator
        locator.count = AsyncMock(return_value=0)
        locator.is_visible = AsyncMock(return_value=False)
        locator.evaluate_all = AsyncMock(return_value=[])
        locator.all_text_contents = AsyncMock(return_value=[])
        locator.filter = Mock(return_value=locator)
        client.page = SimpleNamespace(
            url="https://www.tiktok.com/search?q=kuliah",
            locator=Mock(return_value=locator),
            mouse=SimpleNamespace(wheel=AsyncMock()),
            goto=AsyncMock(),
        )
        client.pause = AsyncMock()
        client.navigate = AsyncMock()
        client.cooldown_file = self.path / "cooldown.json"
        return client

    def test_default_plan_inherits_queries_and_unlimited_caps_without_reading_auth(
        self,
    ):
        with patch.object(t, "auth_material", side_effect=AssertionError("auth read")):
            crawler = t.TikTokCrawler()
            self.addCleanup(crawler._tiktok_worker.close)
            plan = crawler.plan()
        p = plan["config"]["platforms"]["tiktok"]
        self.assertEqual(p["queries"], read_config()["queries"])
        self.assertEqual(p["min_posts"], 1000)
        self.assertIsNone(plan["config"]["total_seconds"])
        for key in [
            "max_posts",
            "max_candidates",
            "max_comments",
            "max_replies",
            "max_replies_per_thread",
        ]:
            self.assertIsNone(p[key])
        self.assertEqual(plan["platform_scope"], "tiktok_only")
        self.assertFalse(plan["session_rotation"])

    def test_auth_is_tiktok_only_accepts_sessionid_alias_and_does_not_mutate(self):
        path = self.path / "auth.json"
        path.write_text(
            json.dumps(
                [
                    {"sosmed": "instagram", "sessionid": "other"},
                    {"sosmed": "TikTok", "sessionid": "private-token"},
                ]
            )
        )
        before = path.read_bytes()
        self.assertEqual(t.auth_material(path), "private-token")
        self.assertEqual(path.read_bytes(), before)
        path.write_text(
            json.dumps([{"sosmed": "tiktok", "msToken": "a", "sessionid": "b"}])
        )
        with self.assertRaisesRegex(ValueError, "requires one entry"):
            t.auth_material(path)

    def test_strict_identity_and_metrics(self):
        raw = t.normalize_item(video())
        self.assertEqual(raw.thread_root_key, "tiktok:video:100")
        reply = t.normalize_item(comment("201", "reply", parent="200"))
        self.assertEqual(reply.parent_key, "tiktok:comment:200")
        self.assertEqual(
            identity(dict(platform="tiktok", jenis="reply", url=reply.canonical_url))[
                0
            ],
            ("tiktok", "comment", "201"),
        )
        for url in [
            "https://evil.test/@x/video/100",
            "https://www.tiktok.com:443/@x/video/100",
            "https://www.tiktok.com/@x/video/100?secret=a",
        ]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                t.post_url(url)
        with self.assertRaises(ValueError):
            t.normalize_item({**video(), "link": video("101")["link"]})

    def test_export_reuses_search_root_and_deduplicates_native_ids_across_days(self):
        calls = []

        def worker(operation, target, settings, seconds, emit):
            calls.append(operation)
            if operation == "search":
                for item in [video(), video(text="Kuliah versi berubah")]:
                    emit(
                        "candidate",
                        dict(
                            url=item["link"], cached_root=item, discovered_from="kuliah"
                        ),
                    )
            else:
                self.assertEqual(target["cached_root"]["id"], "100")
                for item in [
                    target["cached_root"],
                    comment(),
                    comment(),
                    comment("201", "reply", parent="200"),
                ]:
                    emit("record", item)
            return dict(
                status="FINISHED_BEST_EFFORT",
                reason="fixture",
                warnings=[],
                source_version="fixture",
            )

        crawler = t.TikTokCrawler(self.config, workers={"tiktok": worker})
        output = self.path / "run"
        report = crawler.run(output)
        self.assertEqual(report["platforms"]["tiktok"]["qualified_posts"], 1)
        self.assertEqual(calls, ["search", "thread"])
        rows = [
            json.loads(line)
            for line in (output / "Contents.jsonl").read_text().splitlines()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({r["object_key"] for r in rows}), 3)
        book = load_workbook(output / "social_data.xlsx", read_only=True)
        self.assertEqual(book.sheetnames, ["Data"])
        data = list(book["Data"].values)
        book.close()
        self.assertEqual(len(data), 4)
        self.assertTrue(all("@example/" in row[8] for row in data[1:]))
        metrics = [
            json.loads(line)
            for line in (output / "Metrics.jsonl").read_text().splitlines()
        ]
        self.assertTrue(
            any(m["metric_name"] == "play_count" and m["value"] == 250 for m in metrics)
        )
        archive = self.path / "archive"
        organize([output / "social_data.xlsx"], archive, allow_synthetic=True)
        second = organize([output / "social_data.xlsx"], archive, allow_synthetic=True)
        self.assertEqual(second["rows"], 3)
        self.assertEqual(verify(archive)["duplicate_native_ids"], 0)

    def test_all_comments_and_replies_are_paginated_and_deduplicated(self):
        client = self.client()

        async def first_page(*args):
            client.comment_pages[None] = True
            client.comment_buffer.extend(
                [(source_comment(replies=2), None), (source_comment(), None)]
            )

        async def next_page(*args):
            client.comment_pages[None] = False
            client.comment_pages["200"] = False
            client.comment_buffer.extend(
                [
                    (source_comment("201"), "200"),
                    (source_comment("203"), "200"),
                    (source_comment("202"), None),
                ]
            )

        client.navigate.side_effect = first_page
        client.pause.side_effect = next_page
        events = []
        asyncio.run(
            client.collect(
                "thread",
                dict(video_id="100", cached_root=video()),
                SimpleNamespace(**client.settings),
                30,
                lambda kind, row: events.append(row),
            )
        )
        self.assertEqual([r["id"] for r in events], ["100", "200", "201", "203", "202"])
        self.assertEqual(events[2]["parent_comment_id"], "200")
        self.assertGreater(client.page.mouse.wheel.await_count, 0)
        self.assertIn("source_comment_pagination_exhausted", client.operation_warnings)

    def test_all_comments_survive_more_than_three_idle_rounds_and_wait_for_replies(
        self,
    ):
        client = self.client()
        rounds = 0

        async def initial(*args):
            client.comment_pages[None] = False
            client.comment_buffer.append((source_comment(replies=1), None))

        async def delayed_reply(*args):
            nonlocal rounds
            rounds += 1
            if rounds == 6:
                client.comment_pages["200"] = False
                client.comment_buffer.append((source_comment("201"), "200"))
            if rounds > 6:
                self.fail("Pagination did not finish after all replies arrived")

        client.navigate.side_effect = initial
        client.pause.side_effect = delayed_reply
        rows = []
        asyncio.run(
            client.collect(
                "thread",
                dict(video_id="100", cached_root=video()),
                SimpleNamespace(**client.settings),
                30,
                lambda kind, row: rows.append(row),
            )
        )
        self.assertEqual(rounds, 6)
        self.assertEqual([r["id"] for r in rows], ["100", "200", "201"])

    def test_unknown_pagination_waits_until_deadline_and_retains_partial_rows(self):
        client = self.client()
        rounds = 0

        async def initial(*args):
            client.comment_buffer.append((source_comment(), None))

        async def deadline(*args):
            nonlocal rounds
            rounds += 1
            if rounds == 6:
                raise TimeoutError

        client.navigate.side_effect = initial
        client.pause.side_effect = deadline
        rows = []
        with self.assertRaises(TimeoutError):
            asyncio.run(
                client.collect(
                    "thread",
                    dict(video_id="100", cached_root=video()),
                    SimpleNamespace(**client.settings),
                    30,
                    lambda kind, row: rows.append(row),
                )
            )
        self.assertEqual(rounds, 6)
        self.assertEqual([r["id"] for r in rows], ["100", "200"])
        self.assertNotIn(
            "source_comment_pagination_exhausted", client.operation_warnings
        )

    def test_source_has_more_requires_explicit_valid_comment_page(self):
        for value in (False, 0, "0"):
            self.assertIs(t.source_has_more({"comments": [], "has_more": value}), False)
        for value in (True, 1, "1"):
            self.assertIs(
                t.source_has_more({"data": {"comments": [], "has_more": value}}), True
            )
        for body in (
            {},
            {"comments": []},
            {"has_more": 0},
            {"comments": [], "has_more": "false"},
        ):
            self.assertIsNone(t.source_has_more(body))

    def test_filtered_roots_do_not_fetch_comments(self):
        client = self.client()
        for root in [
            video(text="judi kampus"),
            video(date="2024-01-01T00:00:00Z"),
            video(text="Resep ayam"),
        ]:
            asyncio.run(
                client.collect(
                    "thread",
                    dict(video_id="100", cached_root=root),
                    SimpleNamespace(**client.settings),
                    30,
                    Mock(),
                )
            )
        client.navigate.assert_not_called()
        client.page.mouse.wheel.assert_not_called()

    def test_idle_search_stops_without_requesting_forever(self):
        client = self.client()
        with self.assertRaises(t.SearchUnavailable):
            asyncio.run(
                client.collect(
                    "search",
                    json.dumps({"query": "kuliah"}),
                    SimpleNamespace(**client.settings),
                    30,
                    Mock(),
                )
            )
        self.assertEqual(
            client.page.mouse.wheel.await_count,
            client.settings["idle_scroll_limit"] - 1,
        )
        self.assertIn(
            "visible_search_exhausted_non_exhaustive", client.operation_warnings
        )

    def test_transport_has_deadline_and_stops_on_rate_limit_without_retry(self):
        client = self.client()
        client.deadline = time.monotonic() - 1
        with self.assertRaises(TimeoutError):
            client.remaining()
        client.deadline = float("inf")
        request = Mock(
            url="https://www.tiktok.com/api/search/general/full/", resource_type="xhr"
        )
        client.response(
            SimpleNamespace(
                url=request.url,
                request=request,
                status=429,
                headers={"retry-after": "120"},
            )
        )
        self.assertEqual(client.barrier, "RATE_LIMITED")
        self.assertEqual(client.retry_after_seconds, 120)
        self.assertTrue(client.cooldown_file.exists())
        route = SimpleNamespace(
            request=request, abort=AsyncMock(), continue_=AsyncMock()
        )
        asyncio.run(client.route(route))
        route.abort.assert_awaited_once()
        route.continue_.assert_not_called()
        with self.assertRaises(t.AccessBarrier):
            client.check()
        self.assertNotIn(
            "private-token",
            json.dumps(t.error_receipt(t.AccessBarrier("private-token"))),
        )

    def test_timeout_preserves_already_streamed_records(self):
        worker = t.TikTokWorker({}, target=hanging_worker)
        self.addCleanup(worker.close)
        # Exercise acquisition timeout independently of Python spawn/import time.
        ctx = t.mp.get_context("spawn")
        worker.pipe, child = ctx.Pipe()
        worker.process = ctx.Process(
            target=hanging_worker, args=({}, child), daemon=True
        )
        worker.process.start()
        child.close()
        self.assertTrue(worker.pipe.poll(20), "worker did not become ready")
        self.assertEqual(worker.pipe.recv(), ("ready", None))
        records = []
        result = worker(
            "thread", {}, SimpleNamespace(), 1.5, lambda kind, row: records.append(row)
        )
        self.assertEqual(result["status"], "TIMEOUT")
        self.assertEqual([r["id"] for r in records], ["100"])

    def test_access_barrier_exports_partial_bundle_and_stops_searches(self):
        calls = []

        def worker(operation, target, settings, seconds, emit):
            calls.append(operation)
            return t.error_receipt(t.AccessBarrier("private-token"))

        crawler = t.TikTokCrawler(self.config, workers={"tiktok": worker})
        report = crawler.run(self.path / "blocked")
        self.assertEqual(calls, ["search"])
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual(report["platforms"]["tiktok"]["stop_reason"], "ACCESS_BLOCKED")
        self.assertTrue(Path(report["primary_file"]).is_file())
        self.assertNotIn("private-token", json.dumps(report))

    def test_config_rejects_unknown_secrets_and_invalid_limits(self):
        p = {**t.DEFAULTS, "queries": ["kuliah"]}
        for changes in [
            dict(msToken="private-token"),
            dict(max_comments=-1),
            dict(min_posts=500, max_posts=100),
            dict(country="ID"),
        ]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                t.platform_configuration({**deepcopy(p), **changes})

    def test_search_keeps_query_and_cap_and_skips_invalid_candidates(self):
        client = self.client()

        async def feed(*args):
            client.video_buffer.extend(
                [source_video(), {"id": "invalid"}, source_video(), source_video("101")]
            )

        client.navigate.side_effect = feed
        events = []
        settings = SimpleNamespace(**{**client.settings, "search_results": 2})
        asyncio.run(
            client.collect(
                "search",
                json.dumps({"query": "biaya kuliah"}),
                settings,
                10,
                lambda kind, row: events.append(row),
            )
        )
        self.assertEqual([e["cached_root"]["id"] for e in events], ["100", "101"])
        self.assertEqual(client.invalid_candidates, 1)
        client.navigate.assert_awaited_once_with(
            "https://www.tiktok.com/search?q=biaya+kuliah"
        )

    def test_finite_comment_cap_and_zero_replies_are_honored(self):
        client = self.client()

        async def feed(*args):
            client.comment_buffer.extend(
                [
                    (source_comment(replies=2), None),
                    (source_comment("201"), None),
                    (source_comment("202"), "200"),
                ]
            )

        client.navigate.side_effect = feed
        rows = []
        settings = SimpleNamespace(
            **{**client.settings, "max_comments": 1, "max_replies": 0}
        )
        asyncio.run(
            client.collect(
                "thread",
                dict(video_id="100", cached_root=video()),
                settings,
                10,
                lambda kind, row: rows.append(row),
            )
        )
        self.assertEqual([r["id"] for r in rows], ["100", "200"])

    def test_upstream_parser_preserves_native_ids_dates_and_counts(self):
        data = source_video("7654321098765432100", "Kuliah beasiswa")
        data["statsV2"] = dict(playCount="123456", diggCount="50")
        parsed = t.project_video(data)
        raw = t.normalize_item(parsed)
        self.assertEqual(raw.native_id, "7654321098765432100")
        self.assertEqual(raw.text_source, "Kuliah beasiswa")
        self.assertEqual(parsed["stats"]["play_count"], 123456)
        self.assertEqual(raw.timestamp_quality, "exact")
        self.assertEqual(
            t.project_comment(source_comment(), "100", video()["link"])["id"], "200"
        )
        with self.assertRaises(ValueError):
            t.project_comment(source_comment(root="999"), "100", video()["link"])

    def test_baseline_matches_native_video_even_after_author_rename(self):
        import uuid

        from Crawler.Backend.Reddit import crawl_reddit_single as contract

        out = self.path / "baseline"
        factory = contract.RedditRecordFactory(
            "test", str(uuid.uuid4()), contract.KeywordMatcher([])
        )
        sink = contract.BundleSink(out, "test", factory.run_id)
        dataset = contract.Dataset(factory, sink)
        t.TikTokAdapter(factory, dataset).accept(
            "record", video(), video()["link"], None
        )
        sink.finish(dict(synthetic=True))
        config = deepcopy(self.config)
        config["exclude_existing_datasets"] = [str(out)]
        crawler = t.TikTokCrawler(config)
        self.addCleanup(crawler._tiktok_worker.close)
        excluded, _ = crawler._existing_posts()
        self.assertIn(
            t.post_url(video()["link"].replace("@example", "@renamed")),
            excluded["tiktok"],
        )

    def test_empty_default_run_never_republishes_the_archive(self):
        def worker(*args):
            return t.error_receipt(t.AccessBarrier())

        crawler = t.TikTokCrawler(self.config, workers={"tiktok": worker})
        with (
            patch.object(t.core, "ROOT", self.path),
            patch("Crawler.Backend.social_archive.organize") as organizer,
        ):
            report = crawler.run()
        organizer.assert_not_called()
        self.assertEqual(report["organization_skipped"], "no_selected_records")
        self.assertEqual(report["primary_files"], [])
        self.assertTrue(Path(report["primary_file"]).exists())

    def test_local_auth_error_is_distinct_from_a_source_parse_error(self):
        self.assertEqual(
            t.error_receipt(t.AuthError("secret"))["status"], "SESSION_INVALID"
        )
        self.assertEqual(
            t.error_receipt(ValueError("secret"))["status"], "SOURCE_ERROR"
        )
        self.assertNotIn("secret", json.dumps(t.error_receipt(t.AuthError("secret"))))

    def test_browser_injects_token_before_navigation_and_uses_no_tiktok_sdk(self):
        crawler = t.TikTokCrawler(self.config)
        self.addCleanup(crawler._tiktok_worker.close)
        page = SimpleNamespace(set_default_navigation_timeout=Mock())
        context = SimpleNamespace(
            add_cookies=AsyncMock(),
            on=Mock(),
            route=AsyncMock(),
            new_page=AsyncMock(return_value=page),
            close=AsyncMock(),
        )
        browser = SimpleNamespace(
            new_context=AsyncMock(return_value=context), close=AsyncMock()
        )
        engine = SimpleNamespace(launch=AsyncMock(return_value=browser))
        playwright = SimpleNamespace(chromium=engine, stop=AsyncMock())
        factory = Mock(
            return_value=SimpleNamespace(start=AsyncMock(return_value=playwright))
        )
        client = t.NativeTikTokClient(crawler.config, factory=factory)
        client.cooldown_file = self.path / "cooldown.json"

        async def exercise():
            await client.start()
            await client.close()

        with patch.object(t, "auth_material", return_value="private-token") as auth:
            asyncio.run(exercise())
        auth.assert_called_once()
        cookie = context.add_cookies.call_args.args[0][0]
        self.assertEqual(cookie["domain"], ".tiktok.com")
        self.assertEqual(cookie["name"], "msToken")
        self.assertEqual(cookie["value"], "private-token")
        engine.launch.assert_awaited_once_with(headless=True)
        context.new_page.assert_awaited_once()
        playwright.stop.assert_awaited_once()

    def test_explicit_video_lookup_uses_embedded_metadata_and_keeps_author_url(self):
        client = self.client()
        url = video()["link"]

        async def feed(*args):
            client.video_buffer.append(source_video())

        client.navigate.side_effect = feed
        settings = SimpleNamespace(
            **{**client.settings, "max_comments": 0, "urls": [url]}
        )
        rows = []
        asyncio.run(
            client.collect(
                "thread",
                {"video_id": "100"},
                settings,
                10,
                lambda kind, row: rows.append(row),
            )
        )
        self.assertEqual([r["id"] for r in rows], ["100"])
        client.navigate.assert_awaited_once_with(url)
        self.assertEqual(
            t.platform_configuration({**t.DEFAULTS, "urls": [url]})["urls"], [url]
        )

    def test_hydration_and_network_shapes_preserve_native_ids(self):
        client = self.client()
        client.page.locator.return_value.all_text_contents.return_value = [
            json.dumps({"ItemModule": {"100": source_video()}}),
            "invalid-json",
        ]
        asyncio.run(client.hydration())
        self.assertEqual(client.video_buffer[0]["id"], "100")
        self.assertIn("invalid_embedded_json", client.operation_warnings)

    def test_keyword_page_without_results_is_explicit_without_hashtag_substitution(
        self,
    ):
        client = self.client()
        with self.assertRaises(t.SearchUnavailable):
            asyncio.run(
                client.collect(
                    "search",
                    json.dumps({"query": "biaya kuliah"}),
                    SimpleNamespace(**client.settings),
                    10,
                    Mock(),
                )
            )
        self.assertEqual(
            t.error_receipt(t.SearchUnavailable())["status"], "CLIENT_UPGRADE_REQUIRED"
        )
        client.navigate.assert_awaited_once_with(
            "https://www.tiktok.com/search?q=biaya+kuliah"
        )

    def test_cooldown_survives_restart_and_blocks_network_until_server_time(self):
        client = self.client()
        client.cooldown_file.write_text(json.dumps({"not_before": time.time() + 120}))
        with self.assertRaises(t.AccessBarrier):
            client.load_cooldown()
        self.assertEqual(client.barrier, "RATE_LIMITED")
        self.assertGreater(client.retry_after_seconds, 100)
        self.assertEqual(t.retry_after("120"), 120)
        self.assertEqual(t.retry_after("invalid"), 60)
        self.assertEqual(t.retry_after("Thu, 01 Jan 1970 00:02:00 GMT", now=0), 120)

    def test_hashtag_uses_its_own_rendered_page(self):
        client = self.client()

        async def feed(*args):
            client.video_buffer.append(source_video())

        client.navigate.side_effect = feed
        settings = SimpleNamespace(**{**client.settings, "search_results": 1})
        events = []
        asyncio.run(
            client.collect(
                "search",
                json.dumps({"hashtag": "kuliah"}),
                settings,
                10,
                lambda kind, row: events.append(row),
            )
        )
        self.assertEqual(events[0]["discovered_from"], "#kuliah")
        client.navigate.assert_awaited_once_with("https://www.tiktok.com/tag/kuliah")

    def test_capture_filters_stale_responses_and_other_video_comments(self):
        client = self.client()
        client.epoch = 2
        client.operation = "thread"
        client.target_id = "100"
        response = SimpleNamespace(
            url="https://www.tiktok.com/api/comment/list/?aweme_id=999",
            json=AsyncMock(return_value={"comments": [source_comment(root="999")]}),
        )
        asyncio.run(client.capture(response, 2))
        self.assertEqual(client.comment_buffer, [])
        response.url = "https://www.tiktok.com/api/comment/list/?aweme_id=100"
        asyncio.run(client.capture(response, 1))
        self.assertEqual(client.comment_buffer, [])
        response.json.assert_awaited_once()
        asyncio.run(client.capture(response, 2))
        self.assertEqual(len(client.comment_buffer), 1)

    def test_captcha_is_terminal_and_never_solved(self):
        client = self.client()
        challenge = client.page.locator.return_value
        challenge.count.return_value = 1
        challenge.is_visible.return_value = True
        with self.assertRaises(t.AccessBarrier):
            asyncio.run(client.inspect())
        self.assertEqual(client.barrier, "CAPTCHA_REQUIRED")

    def test_empty_search_response_has_a_specific_redacted_diagnosis(self):
        client = self.client()
        response = SimpleNamespace(
            json=AsyncMock(side_effect=ValueError("signed-secret-url"))
        )
        asyncio.run(client.capture(response, client.epoch))
        self.assertEqual(client.barrier, "ACCESS_BLOCKED")
        self.assertEqual(client.barrier_reason, "native_api_empty_or_invalid_json")
        self.assertNotIn("signed-secret-url", client.barrier_reason)

    def test_manual_validation_requires_current_confirmation_then_reuses_session(self):
        client = self.client()
        client.settings.update(manual_wait_seconds=10, manual_poll_seconds=1)
        client.control_file = self.path / "manual.json"
        client.barrier = "ACCESS_BLOCKED"
        client.inspect = AsyncMock()
        events = []

        def emit(kind, payload):
            events.append(kind)
            if kind == "manual_validation":
                client.control_file.write_text(
                    json.dumps({"wait_id": "old", "action": "continue"})
                )

        async def confirm_after_wait(*args):
            self.assertFalse(client.manual_validated)
            client.inspect.assert_not_awaited()
            control = json.loads(client.control_file.read_text())
            control["wait_id"] = wait_id
            client.control_file.write_text(json.dumps(control))

        client.emit = emit
        wait_id = "current-human-check"
        with (
            patch.object(t.uuid, "uuid4", return_value=SimpleNamespace(hex=wait_id)),
            patch.object(t.asyncio, "sleep", side_effect=confirm_after_wait),
        ):
            asyncio.run(client.manual_validation())
        self.assertEqual(events, ["manual_validation", "manual_validated"])
        self.assertTrue(client.manual_validated)
        self.assertIsNone(client.barrier)
        self.assertEqual(client.resume_url, client.page.url)
        self.assertFalse(client.control_file.exists())

    def test_manual_cancel_stops_and_cleans_control_file(self):
        client = self.client()
        client.settings["manual_wait_seconds"] = 10
        client.control_file = self.path / "manual.json"

        def cancel(kind, payload):
            client.control_file.write_text(
                json.dumps({"wait_id": payload["wait_id"], "action": "cancel"})
            )

        client.emit = cancel
        with self.assertRaises(t.AccessBarrier):
            asyncio.run(client.manual_validation())
        self.assertEqual(client.barrier_reason, "manual_validation_cancelled")
        self.assertFalse(client.manual_pending)
        self.assertFalse(client.control_file.exists())

    def test_manual_mode_never_overrides_rate_limit(self):
        client = self.client()
        client.manual_pending = True
        client.barrier = "RATE_LIMITED"
        route = SimpleNamespace(abort=AsyncMock(), continue_=AsyncMock())
        asyncio.run(client.route(route))
        route.abort.assert_awaited_once()
        route.continue_.assert_not_called()
        with self.assertRaises(t.AccessBarrier):
            asyncio.run(client.manual_validation())

    def test_manual_profile_requires_visible_chromium_and_private_directory(self):
        p = {**t.DEFAULTS, "queries": ["kuliah"]}
        for changes in [
            dict(manual_wait_seconds=-1),
            dict(manual_wait_seconds=10),
            dict(manual_profile_dir="config"),
            dict(manual_poll_seconds=0),
        ]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                t.platform_configuration({**p, **changes})
        self.assertEqual(
            t.platform_configuration(
                {**p, "manual_wait_seconds": 600, "headless": False}
            )["manual_wait_seconds"],
            600,
        )

    def capture_worker(self, records):
        path = self.path / "chrome.json"
        path.write_text(
            json.dumps(
                dict(
                    schema_version=1,
                    source="existing_chrome_public_page",
                    query="kuliah",
                    captured_at="2026-11-03T08:00:00Z",
                    records=records,
                )
            )
        )
        return t.ChromeCaptureWorker(path)

    def test_chrome_capture_exports_native_ids_metrics_and_provenance_without_browser(
        self,
    ):
        root = video()
        root["stats"]["save_count"] = "15"
        worker = self.capture_worker(
            [root, root, comment(), comment("201", "reply", parent="200")]
        )
        with (
            patch.object(t, "auth_material", side_effect=AssertionError("auth read")),
            patch.object(
                t.core.SocialCrawler,
                "_pace",
                side_effect=AssertionError("offline capture paced as network"),
            ),
        ):
            crawler = t.TikTokCrawler(self.config, workers={"tiktok": worker})
            result = crawler.run(self.path / "bundle")
        self.assertEqual(result["platforms"]["tiktok"]["posts_exported"], 1)
        rows = [
            json.loads(line)
            for line in (self.path / "bundle/Contents.jsonl").read_text().splitlines()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["extraction_method"] for row in rows}, {t.CHROME_METHOD})
        self.assertEqual(
            {row["observed_at"] for row in rows}, {"2026-11-03T08:00:00+00:00"}
        )
        self.assertTrue(all(isinstance(row["native_id"], str) for row in rows))
        self.assertEqual(rows[-1]["parent_key"], "tiktok:comment:200")
        sources = [
            json.loads(line)
            for line in (self.path / "bundle/Sources.jsonl").read_text().splitlines()
        ]
        self.assertEqual(sources[0]["extraction_method"], t.CHROME_METHOD)
        self.assertIn("saved_capture_only", sources[0]["access_mode"])
        self.assertEqual(
            crawler.plan()["browser_acquisition"], "connected_agent_required"
        )

    def test_chrome_capture_rejects_wrong_native_identity_and_missing_reply_parent(
        self,
    ):
        bad = comment()
        bad["link"] = "https://www.tiktok.com/@example/video/999?comment_id=200"
        for records in [
            [video(), bad],
            [comment()],
            [video(), comment("201", "reply", parent="999")],
            [{**video(), "stats": []}],
            [{**video(), "id": 100}],
        ]:
            with self.subTest(records=records), self.assertRaises(ValueError):
                self.capture_worker(records)

    def test_chrome_capture_honors_query_and_comment_reply_caps(self):
        worker = self.capture_worker(
            [video(), comment(), comment("201", "reply", parent="200")]
        )
        settings = SimpleNamespace(**{**t.DEFAULTS, "max_comments": 0})
        emitted = []
        worker(
            "search",
            json.dumps({"query": "unrelated"}),
            settings,
            10,
            lambda *e: emitted.append(e),
        )
        self.assertEqual(emitted, [])
        worker(
            "thread", {"video_id": "100"}, settings, 10, lambda *e: emitted.append(e)
        )
        self.assertEqual(len(emitted), 1)
        self.assertEqual(emitted[0][1]["id"], "100")


if __name__ == "__main__":
    unittest.main()
