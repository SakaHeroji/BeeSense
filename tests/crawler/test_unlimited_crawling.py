"""Offline evidence for target-based runs and nullable comment/daily limits."""

import asyncio
import json
import math
import tempfile
import time
import unittest
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from Crawler.Backend import instagram_crawler as ig
from Crawler.Backend import instaloader_crawler as il
from Crawler.Backend.crawler_config import read_config
from Crawler.Backend.scweet_limits import configure_daily_quotas
from Crawler.Backend.social_crawler import SocialCrawler, collect_reddrix
from Crawler.Backend.social_crawler_selenium import SocialCrawlerSelenium
from Crawler.Backend.Youtube import crawl_youtube as yt
from tests.crawler.test_instagram_crawler import COMMENT, MEDIA, REPLY, URL, Clock
from tests.crawler.test_instaloader_crawler import fixture_post
from tests.crawler.test_reddit_crawler import FakeReddrix, records
from tests.crawler.test_social_crawler import receipt, yt_events


class UnlimitedCrawlingTests(unittest.TestCase):
    def test_ytdlp_receives_no_comment_or_reply_cap_and_emits_every_returned_row(self):
        client = Mock()
        client.extract_info.return_value = {"id": "00000000000", "title": "Kuliah"}
        client.process_ie_result.return_value = {
            "comments": [{"id": "c" + str(i), "text": "context"} for i in range(110)]
        }
        pipe = Mock()
        settings = dict(
            cert_store="system",
            sort="new",
            max_comments=None,
            max_replies=None,
            max_replies_per_thread=None,
        )
        with patch("yt_dlp.YoutubeDL") as constructor, patch.object(yt.os, "setsid"):
            constructor.return_value.__enter__.return_value = client
            yt.worker("video", "https://youtu.be/00000000000", settings, pipe)
        args = constructor.call_args.args[0]["extractor_args"]["youtube"][
            "max_comments"
        ]
        self.assertEqual(args, ["", "", "", "", ""])
        comments = [
            call.args[0]
            for call in pipe.send.call_args_list
            if call.args[0][0] == "comment"
        ]
        self.assertEqual(len(comments), 110)
        self.assertEqual(
            pipe.send.call_args.args[0][1]["status"], "FINISHED_BEST_EFFORT"
        )

    def test_main_plan_applies_target_and_unlimited_caps_to_every_runner(self):
        crawler = SocialCrawler()
        self.addCleanup(crawler._instagram_worker.close)
        self.addCleanup(crawler._twitter_worker.close)
        plan = crawler.plan()
        self.assertIsNone(plan["config"]["total_seconds"])
        self.assertEqual(plan["comment_scope"], "all_visible_context")
        for name, settings in plan["config"]["platforms"].items():
            with self.subTest(platform=name):
                self.assertTrue(settings["enabled"])
                self.assertGreaterEqual(settings["min_posts"], 1000)
                self.assertEqual(settings["min_comments_per_post"], 0)
                for key in (
                    "max_posts",
                    "max_candidates",
                    "max_comments",
                    "max_replies",
                ):
                    self.assertIsNone(settings[key])
        for key in ("daily_requests_limit", "daily_tweets_limit"):
            self.assertIsNone(plan["config"]["scweet"][key])
        selenium = SocialCrawlerSelenium()
        self.assertEqual(set(selenium.config["platforms"]), {"youtube", "reddit"})
        self.assertIsNone(selenium.config["total_seconds"])

    def test_thousand_unique_posts_finish_beyond_old_hours_and_keep_all_comments(self):
        config = read_config()
        config["platforms"] = {"youtube": config["platforms"]["youtube"]}
        config["scweet"] = {}
        config["platforms"]["youtube"].update(
            urls=["https://youtu.be/" + f"{i:011d}" for i in range(1000)], queries=[]
        )
        config["exclude_existing_datasets"] = []
        clock, progress = Clock(), []

        def worker(operation, target, settings, seconds, emit):
            self.assertTrue(math.isinf(seconds))
            native = target.rsplit("=", 1)[-1]
            for kind, row in yt_events(
                vid=native, count=101 if native == "00000000000" else 0
            ):
                if kind == "comment":
                    row["text"] = (
                        "judi"  # Root exclusions must not discard comment context.
                    )
                emit(kind, row)
            clock.now += 10000
            return receipt()

        crawler = SocialCrawler(
            config,
            workers={"youtube": worker},
            monotonic=clock.clock,
            sleep=clock.sleep,
            progress=progress.append,
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            result = crawler.run(output)
            self.assertTrue(result["targets_met"])
            self.assertEqual(result["platforms"]["youtube"]["posts_exported"], 1000)
            self.assertEqual(result["platforms"]["youtube"]["comments"], 101)
            rows = [
                json.loads(line)
                for line in (output / "Contents.jsonl").read_text().splitlines()
            ]
            self.assertEqual(len(rows), len({r["object_key"] for r in rows}))
            snapshot = json.loads(output.with_name("run.progress.json").read_text())
            self.assertIsNone(snapshot["remaining_seconds"])
            json.dumps(snapshot, allow_nan=False)
            self.assertGreater(snapshot["elapsed_seconds"], 86400)

    def test_reddrix_unlimited_preserves_native_replies_and_zero_disables_them(self):
        p = SocialCrawler().config["platforms"]["reddit"]
        FakeReddrix.items = records()
        events = []
        asyncio.run(
            collect_reddrix(
                "thread",
                "https://www.reddit.com/r/indonesia/comments/abc123/",
                p,
                lambda *row: events.append(row),
                factory=FakeReddrix,
            )
        )
        self.assertEqual(len(events), 3)
        self.assertTrue(math.isinf(FakeReddrix.options["max_comments_per_post"]))
        events.clear()
        asyncio.run(
            collect_reddrix(
                "thread",
                "https://www.reddit.com/r/indonesia/comments/abc123/",
                {**p, "max_replies": 0},
                lambda *row: events.append(row),
                factory=FakeReddrix,
            )
        )
        self.assertEqual(len(events), 2)

    def test_instagram_mobile_pages_all_parents_and_replies_without_numeric_caps(self):
        settings = asdict(ig.InstagramCrawler().settings)
        client = Mock()
        client.media_pk_from_code.return_value = "1"
        client.media_info_v1.return_value = MEDIA
        second = {**COMMENT, "pk": "31"}
        client.media_comments_chunk.side_effect = [
            ([COMMENT], "next"),
            ([second], None),
        ]
        client.media_comment_replies_chunk.side_effect = [
            ([REPLY], "next"),
            ([{**REPLY, "pk": "23"}], None),
            ([], None),
        ]
        events = []
        ig.collect(
            "media", URL, settings, lambda kind, row: events.append(row), client=client
        )
        self.assertEqual(
            [r["native_id"] for r in events], ["1", "21", "31", "22", "23"]
        )
        self.assertEqual(client.media_comments_chunk.call_count, 2)
        self.assertEqual(client.media_comment_replies_chunk.call_count, 3)

    def test_instaloader_fetches_full_answer_iterator_when_previews_are_partial(self):
        settings = il.InstaloaderCrawler().settings
        adapter = il.InstaloaderAdapter(
            settings, loader=Mock(), module=SimpleNamespace()
        )
        parent = dict(
            id="21",
            text="test",
            created_at=1790848800,
            owner={"id": "9"},
            edge_threaded_comments={"count": 3, "edges": []},
        )
        answers = [
            {
                **parent,
                "id": str(i),
                "edge_threaded_comments": {"count": 0, "edges": []},
            }
            for i in range(22, 25)
        ]
        calls = []

        def iterator(context, query, extract, wrap, variables, referer):
            calls.append(variables)
            return iter(
                wrap(node)
                for node in (answers if "comment_id" in variables else [parent])
            )

        adapter.module.NodeIterator = iterator
        comments = list(adapter.legacy_comments(fixture_post()))
        self.assertEqual([r.id for r in comments[0].answers], ["22", "23", "24"])
        self.assertIn({"comment_id": "21"}, calls)


class ScweetQuotaTests(unittest.TestCase):
    def test_unlimited_quotas_preserve_counters_and_all_other_eligibility_gates(self):
        try:
            from Scweet.repos import AccountsRepo, _today_string
            from Scweet.schema import AccountTable
            from Scweet.storage import session_scope
            from sqlalchemy import select
        except ImportError:
            self.skipTest("Scweet optional dependency is not installed")
        with tempfile.TemporaryDirectory() as directory:
            db = str(Path(directory) / "state.db")
            old = AccountsRepo(db, require_auth_material=True)
            now = time.time()
            base = dict(
                auth_token="fixture",
                csrf="fixture",
                cookies_json="{}",
                daily_requests=1000000,
                daily_tweets=1000000,
                last_reset_date=_today_string(),
            )
            with session_scope(db) as session:
                for name, extra in [
                    ("available", {}),
                    ("cooldown", {"available_til": now + 600}),
                    ("leased", {"lease_id": "active", "lease_expires_at": now + 600}),
                    ("no_auth", {"csrf": None}),
                ]:
                    session.add(AccountTable(username=name, **{**base, **extra}))
            client = SimpleNamespace(
                _accounts_repo=old,
                _runner=SimpleNamespace(),
                _api_engine=SimpleNamespace(),
            )
            configure_daily_quotas(client, None, None)
            diag = client._accounts_repo.eligibility_diagnostics(now)
            self.assertEqual(diag["eligible"], 1)
            self.assertEqual(
                diag["blocked_counts"], {"cooldown": 1, "leased": 1, "missing_csrf": 1}
            )
            leases = client._accounts_repo.acquire_leases(
                1, "fixture-run", "fixture-worker", now
            )
            self.assertEqual(len(leases), 1)
            with session_scope(db) as session:
                account = session.execute(
                    select(AccountTable).where(AccountTable.username == "available")
                ).scalar_one()
                self.assertEqual(account.daily_requests, 1000000)
                self.assertEqual(account.daily_tweets, 1000000)
            self.assertIs(
                client._runner.accounts_repo, client._api_engine.accounts_repo
            )

    def test_either_finite_daily_quota_still_blocks_independently(self):
        try:
            from Scweet.repos import AccountsRepo, _today_string
            from Scweet.schema import AccountTable
            from Scweet.storage import session_scope
        except ImportError:
            self.skipTest("Scweet optional dependency is not installed")
        with tempfile.TemporaryDirectory() as directory:
            db = str(Path(directory) / "state.db")
            old = AccountsRepo(db)
            with session_scope(db) as session:
                session.add(
                    AccountTable(
                        username="fixture",
                        daily_requests=20,
                        daily_tweets=20,
                        last_reset_date=_today_string(),
                    )
                )
            for requests, tweets in [(None, 10), (10, None), (10, 10)]:
                client = SimpleNamespace(
                    _accounts_repo=old,
                    _runner=SimpleNamespace(),
                    _api_engine=SimpleNamespace(),
                )
                configure_daily_quotas(client, requests, tweets)
                self.assertEqual(
                    client._accounts_repo.eligibility_diagnostics()["blocked_counts"],
                    {"daily_limit": 1},
                )
                self.assertEqual(
                    client._accounts_repo.acquire_leases(1, "fixture", "worker"), []
                )
