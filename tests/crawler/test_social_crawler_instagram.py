"""Exercise Instagram through the combined coordinator, without network access."""

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from Crawler.Backend.social_crawler import ROOT, SocialCrawler
from tests.crawler.test_instagram_crawler import URL, records
from tests.crawler.test_social_crawler import Clock, receipt, yt_events


class InstagramIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads(
            (ROOT / "config/social_crawler_instagram_3h.json").read_text()
        )
        self.cfg["exclude_existing_datasets"] = []
        self.cfg["delay"] = {"mode": "fixed", "seconds": 0}
        self.cfg["platforms"]["instagram"].update(
            urls=[URL], hashtags=[], min_posts=1, min_comments_per_post=2
        )
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    def ig(self, operation, target, settings, seconds, emit):
        self.assertEqual(operation, "media")
        for row in records():
            emit("record", row)
        return receipt()

    def test_instagram_only_never_calls_youtube_or_reddit_and_matches_excel_contract(
        self,
    ):
        def forbidden(*args):
            self.fail("Only Instagram may acquire new data")

        crawler = SocialCrawler(
            self.cfg,
            workers={"instagram": self.ig, "youtube": forbidden, "reddit": forbidden},
        )
        result = crawler.run(self.path / "ig")
        self.assertEqual(set(result["platforms"]), {"instagram"})
        self.assertEqual(result["platforms"]["instagram"]["posts_exported"], 1)
        self.assertEqual(result["compact"]["rows"], 3)
        source = json.loads((self.path / "ig/Sources.jsonl").read_text())
        self.assertEqual(
            source["extraction_method"], "playwright_chrome_rendered_document"
        )
        self.assertTrue(
            json.loads((self.path / "ig/manifest.json").read_text())["synthetic"]
        )

    def test_native_baseline_skips_instagram_before_worker(self):
        first = self.path / "first"
        SocialCrawler(self.cfg, workers={"instagram": self.ig}).run(first)
        cfg = deepcopy(self.cfg)
        cfg["exclude_existing_datasets"] = [str(first)]
        crawler = SocialCrawler(
            cfg,
            workers={"instagram": lambda *args: self.fail("Duplicate was requested")},
        )
        report = crawler.run(self.path / "second")
        self.assertEqual(report["platforms"]["instagram"]["existing_posts_skipped"], 1)
        self.assertEqual(report["compact"]["rows"], 0)

    def test_discovery_retains_bounded_cursor(self):
        cfg = deepcopy(self.cfg)
        cfg["platforms"]["instagram"].update(urls=[], hashtags=["kuliah"])
        calls = []

        def worker(operation, target, settings, seconds, emit):
            if operation == "search":
                query = json.loads(target)
                calls.append(query["cursor"])
                if query["cursor"] is None:
                    return {**receipt(), "next_cursor": "2"}
                emit("candidate", {"url": URL})
                return receipt()
            return self.ig(operation, target, settings, seconds, emit)

        report = SocialCrawler(cfg, workers={"instagram": worker}).run(
            self.path / "pages"
        )
        self.assertEqual(calls, [None, "2"])
        self.assertTrue(report["targets_met"])

    def test_instagram_429_honors_server_wait_and_retries_same_post(self):
        clock, calls = Clock(), []
        self.cfg["total_seconds"] = 20
        self.cfg["platforms"]["instagram"].update(
            rate_limit_cooldown_seconds=4, rate_limit_max_retries=1
        )

        def worker(operation, target, settings, seconds, emit):
            calls.append((target, clock.now))
            if len(calls) == 1:
                return {**receipt("RATE_LIMITED"), "retry_after_seconds": 6.5}
            return self.ig(operation, target, settings, seconds, emit)

        report = SocialCrawler(
            self.cfg,
            workers={"instagram": worker},
            sleep=clock.sleep,
            monotonic=clock.clock,
        ).run(self.path / "cooldown")
        self.assertEqual(calls, [(URL, 0), (URL, 7)])
        self.assertTrue(report["targets_met"])
        self.assertEqual(report["platforms"]["instagram"]["rate_limit_events"], 1)
        self.assertEqual(report["platforms"]["instagram"]["rate_limit_retries"], 1)
        self.assertEqual(report["platforms"]["instagram"]["posts_exported"], 1)

    def test_instagram_retry_cap_and_global_deadline_stop_additional_requests(self):
        for budget, expected in [(5, [0]), (30, [0, 7, 14, 21])]:
            with self.subTest(budget=budget):
                clock, calls = Clock(), []
                cfg = deepcopy(self.cfg)
                cfg["total_seconds"] = budget
                cfg["platforms"]["instagram"].update(
                    rate_limit_cooldown_seconds=4, rate_limit_max_retries=3
                )

                def worker(*args):
                    calls.append(clock.now)
                    return {**receipt("RATE_LIMITED"), "retry_after_seconds": 7}

                report = SocialCrawler(
                    cfg,
                    workers={"instagram": worker},
                    sleep=clock.sleep,
                    monotonic=clock.clock,
                ).run(self.path / f"limited{budget}")
                self.assertEqual(calls, expected)
                self.assertEqual(
                    report["platforms"]["instagram"]["stop_reason"], "RATE_LIMITED"
                )

    def test_instagram_default_cooldown_matches_reddit_policy(self):
        cfg = deepcopy(self.cfg)
        cfg["platforms"]["instagram"].pop("rate_limit_cooldown_seconds", None)
        cfg["platforms"]["instagram"].pop("rate_limit_max_retries", None)
        effective = SocialCrawler(cfg).config["platforms"]["instagram"]
        self.assertEqual(effective["rate_limit_cooldown_seconds"], 360)
        self.assertEqual(effective["rate_limit_max_retries"], 3)

    def test_mixed_export_keeps_native_platform_provenance(self):
        cfg = deepcopy(self.cfg)
        cfg["platforms"]["youtube"] = {
            "urls": ["https://youtu.be/AAAAAAAAAAA"],
            "min_posts": 1,
            "min_comments_per_post": 1,
        }

        def youtube(operation, target, settings, seconds, emit):
            for kind, row in yt_events(timestamp="2026-10-01T00:00:00+00:00"):
                emit(kind, row)
            return receipt()

        report = SocialCrawler(
            cfg, workers={"instagram": self.ig, "youtube": youtube}
        ).run(self.path / "mixed")
        self.assertTrue(report["targets_met"])
        sources = [
            json.loads(line)
            for line in (self.path / "mixed/Sources.jsonl").read_text().splitlines()
        ]
        self.assertEqual({row["source"] for row in sources}, {"youtube", "instagram"})

    def test_unused_instagram_settings_cannot_leak_credentials_in_other_platform_runs(
        self,
    ):
        for field in ("instagrapi", "instagram_browser"):
            cfg = {"platforms": {"youtube": {}}, field: {"password": "secret"}}
            with self.subTest(field=field), self.assertRaises(ValueError):
                SocialCrawler(cfg)


if __name__ == "__main__":
    unittest.main()
