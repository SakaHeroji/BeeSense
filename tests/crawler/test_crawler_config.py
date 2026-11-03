"""Universal configuration contracts across the coordinator and standalone CLIs."""

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from Crawler.Backend.crawler_config import expand_config, read_config, standalone_config
from Crawler.Backend.instagram_crawler import InstagramCrawler
from Crawler.Backend.instaloader_crawler import InstaloaderCrawler
from Crawler.Backend.reddit_crawler import RedditCrawler
from Crawler.Backend.social_crawler import SocialCrawler, _config
from Crawler.Backend.twitter_crawler import TwitterCrawler


class UniversalConfigTests(unittest.TestCase):
    def test_shared_queries_limits_and_platform_overrides_are_independent(self):
        raw = read_config()
        raw["queries"] = ["biaya pendidikan"]
        raw["platform_defaults"].update(min_posts=12, max_posts=24)
        raw["platforms"]["reddit"]["queries"] = ["kampus lokal"]
        raw["platforms"]["youtube"].update(
            queries=[], urls=["https://youtu.be/AAAAAAAAAAA"], max_posts=36
        )
        before = deepcopy(raw)
        cfg = _config(raw)
        self.assertEqual(cfg["platforms"]["twitter"]["queries"], ["biaya pendidikan"])
        self.assertEqual(cfg["platforms"]["reddit"]["queries"], ["kampus lokal"])
        self.assertEqual(cfg["platforms"]["youtube"]["queries"], [])
        for name in cfg["platforms"]:
            self.assertEqual(cfg["platforms"][name]["min_posts"], 12)
            self.assertEqual(
                cfg["platforms"][name]["max_posts"], 36 if name == "youtube" else 24
            )
        self.assertNotIn("queries", cfg["platforms"]["instagram"])
        cfg["platforms"]["twitter"]["queries"].append("changed")
        self.assertEqual(raw, before)

    def test_every_runner_reads_changes_from_the_same_custom_file(self):
        raw = read_config()
        raw.update(total_seconds=600, include_keywords=["pendidikan"])
        raw["platform_defaults"]["min_posts"] = 7
        for settings in raw["platforms"].values():
            settings["enabled"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "crawler.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with (
                patch(
                    "Crawler.Backend.twitter_crawler.auth_material",
                    side_effect=AssertionError("auth read"),
                ),
                patch(
                    "Crawler.Backend.instaloader_crawler._json",
                    side_effect=AssertionError("auth read"),
                ),
            ):
                combined = SocialCrawler(path)
                self.addCleanup(combined._instagram_worker.close)
                self.addCleanup(combined._twitter_worker.close)
                for cls, name in (
                    (RedditCrawler, "reddit"),
                    (InstagramCrawler, "instagram"),
                    (InstaloaderCrawler, "instagram"),
                    (TwitterCrawler, "twitter"),
                ):
                    with self.subTest(runner=cls.__name__):
                        crawler = cls(path)
                        if hasattr(crawler, "close"):
                            self.addCleanup(crawler.close)
                        cfg = crawler.plan()["config"]
                        self.assertEqual(set(cfg["platforms"]), {name})
                        self.assertEqual(cfg["total_seconds"], 600)
                        self.assertEqual(cfg["include_keywords"], ["pendidikan"])
                        self.assertEqual(cfg["platforms"][name]["min_posts"], 7)
                        self.assertEqual(cfg["since"], combined.config["since"])

    def test_standalone_selects_disabled_platform_without_mutating_input(self):
        raw = read_config()
        for settings in raw["platforms"].values():
            settings["enabled"] = False
        before = deepcopy(raw)
        cfg = standalone_config(raw, "twitter")
        self.assertEqual(set(cfg["platforms"]), {"twitter"})
        self.assertTrue(cfg["platforms"]["twitter"]["enabled"])
        self.assertEqual(raw, before)
        with self.assertRaisesRegex(ValueError, "enable at least one platform"):
            _config(raw)

    def test_legacy_config_retains_strict_adapter_validation(self):
        legacy = standalone_config(None, "twitter")
        self.assertEqual(standalone_config(legacy, "twitter"), legacy)
        legacy["password"] = "must not be accepted"
        with self.assertRaisesRegex(ValueError, "Unknown TwitterCrawler"):
            TwitterCrawler(legacy)

    def test_invalid_schema_defaults_queries_and_limits_are_rejected(self):
        for change in (
            {"schema_version": True},
            {"schema_version": 2},
            {"queries": None},
            {"queries": "kuliah"},
            {"queries": ["bad\nquery"]},
            {"platform_defaults": {"enabled": True}},
            {"platform_defaults": {"min_posts": True}},
            {"platform_defaults": {"max_posts": 1}},
            {"unrecognized": "field"},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                _config({**read_config(), **change})

    def test_legacy_coordinator_configuration_does_not_require_version(self):
        cfg = _config(
            {
                "project_id": "legacy",
                "platforms": {"youtube": {"queries": ["kuliah"]}},
            }
        )
        self.assertEqual(cfg["project_id"], "legacy")
        self.assertEqual(cfg["platforms"]["youtube"]["queries"], ["kuliah"])

    def test_expansion_rejects_non_object_and_oversized_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            for content in ("[]", " " * 1_000_001):
                path.write_text(content)
                with self.assertRaises(ValueError):
                    expand_config(path)
