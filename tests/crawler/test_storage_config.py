"""Public storage configuration must be explicit and never silently ignored."""

import unittest
from copy import deepcopy
from unittest.mock import patch

from Crawler.Backend.crawler_config import read_config, standalone_config
from Crawler.Backend.social_crawler import SocialCrawler, _config
from Crawler.Backend.storage_config import require_excel_storage, storage_config


class StorageConfigTests(unittest.TestCase):
    def test_excel_default_and_isolated_nested_defaults(self):
        first = storage_config()
        first["postgresql"]["host"] = "changed"
        self.assertEqual(storage_config()["postgresql"]["host"], "127.0.0.1")
        self.assertEqual(storage_config()["destination"], "excel")
        self.assertEqual(read_config()["storage"], storage_config())
        require_excel_storage({"storage": storage_config()})

    def test_custom_storage_reaches_coordinator_and_standalone_projections(self):
        config = read_config()
        config["storage"] = {
            "destination": "both",
            "postgresql": {"host": "192.0.2.4", "port": 5433},
        }
        before = deepcopy(config)
        for platform in ("youtube", "reddit", "instagram", "twitter"):
            with self.subTest(platform=platform):
                self.assertEqual(
                    standalone_config(config, platform)["storage"],
                    storage_config(config["storage"]),
                )
        self.assertEqual(
            _config(config)["storage"]["postgresql"]["connection_string_env"],
            "BEESENSE_POSTGRESQL_DSN",
        )
        self.assertEqual(config, before)

    def test_cli_rejects_unimplemented_database_output_before_network_or_export(self):
        config = read_config()
        config["storage"]["destination"] = "postgresql"
        with patch(
            "Crawler.Backend.social_crawler.reddit.verify_descriptor",
            side_effect=AssertionError("must not touch data"),
        ):
            crawler = SocialCrawler(
                config, workers={"youtube": lambda *args: self.fail("network")}
            )
            self.addCleanup(crawler._instagram_worker.close)
            self.addCleanup(crawler._twitter_worker.close)
            with self.assertRaisesRegex(
                ValueError, "standalone CLI currently writes Excel only"
            ):
                crawler.run()

    def test_rejects_credentials_and_unknown_values_in_public_config(self):
        cases = [
            {"destination": "unknown"},
            {"postgresql": {"host": "postgresql://user:password@host/db"}},
            {"postgresql": {"port": True}},
            {"postgresql": {"port": 0}},
            {"postgresql": {"connection_string": "never-commit-a-DSN"}},
            {"postgresql": {"connection_string_env": "password value"}},
        ]
        for config in cases:
            with self.subTest(config=config), self.assertRaises(ValueError):
                storage_config(config)
