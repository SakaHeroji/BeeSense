"""Daily partitions must be globally unique and bound to native crawl evidence."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openpyxl import load_workbook

from Crawler.Backend.social_archive import organize, sha, verify
from Crawler.Backend.social_crawler import SocialCrawler
from tests.crawler.test_social_crawler import START, Clock, receipt, yt_events


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.archive = self.root / "organized"

    def crawler(self, video="AAAAAAAAAAA", title="Kuliah kampus"):
        cfg = {
            "project_id": "archive-test",
            "include_keywords": ["kuliah"],
            "output_root": str(self.archive),
            "delay": {"mode": "fixed", "seconds": 0},
            "platforms": {
                "youtube": {"urls": ["https://youtu.be/" + video], "min_posts": 1}
            },
        }
        clock = Clock()

        def worker(operation, target, settings, seconds, emit):
            for kind, value in yt_events(video, title=title, timestamp=START):
                if kind == "comment":
                    value["id"] += video
                emit(kind, value)
            return receipt()

        return SocialCrawler(
            cfg, workers={"youtube": worker}, sleep=clock.sleep, monotonic=clock.clock
        )

    def source(self, name, observed, *, video="AAAAAAAAAAA", title="Kuliah kampus"):
        directory = self.root / name
        self.crawler(video, title).run(directory)
        audit = directory / "Contents.jsonl"
        records = [json.loads(line) for line in audit.read_text().splitlines()]
        for record in records:
            record["observed_at"] = observed
        audit.write_text("".join(json.dumps(r) + "\n" for r in records))
        path = directory / "manifest.json"
        descriptor = json.loads(path.read_text())
        descriptor["files_sha256"][audit.name] = sha(audit)
        path.write_text(json.dumps(descriptor))
        return directory / "social_data.xlsx"

    def test_global_dedup_keeps_first_wib_day_and_latest_observation(self):
        first = self.source("first", "2026-10-27T18:00:00+00:00")
        latest = self.source(
            "latest", "2026-10-29T00:00:00+00:00", title="Kuliah kampus terbaru"
        )
        result = organize([latest, first], self.archive, allow_synthetic=True)
        self.assertEqual(
            (
                result["rows"],
                result["duplicates_removed"],
                result["duplicate_native_ids"],
            ),
            (3, 3, 0),
        )
        self.assertEqual(result["partitions"][0]["date_wib"], "2026-10-28")
        self.assertEqual(len(result["partitions"]), 1)
        book = load_workbook(result["primary_files"][0], read_only=True)
        rows = list(book["Data"].values)
        book.close()
        self.assertIn("Kuliah kampus terbaru", [row[2] for row in rows[1:]])
        again = organize([first, latest], self.archive, allow_synthetic=True)
        self.assertEqual((again["rows"], again["observations"]), (3, 6))
        self.assertEqual(verify(self.archive)["rows"], 3)

    def test_dates_use_audit_wib_midnight_instead_of_publication_dates(self):
        first = self.source("before", "2026-10-27T16:59:59+00:00")
        second = self.source("after", "2026-10-27T17:00:00+00:00", video="BBBBBBBBBBB")
        result = organize([first, second], self.archive, allow_synthetic=True)
        self.assertEqual(
            [p["date_wib"] for p in result["partitions"]], ["2026-10-27", "2026-10-28"]
        )
        self.assertEqual((result["rows"], result["duplicate_native_ids"]), (6, 0))

    def test_synthetic_and_changed_sources_fail_without_replacing_archive(self):
        source = self.source("source", "2026-10-27T18:00:00+00:00")
        with self.assertRaisesRegex(ValueError, "Synthetic"):
            organize([source], self.archive)
        self.assertFalse(self.archive.exists())
        organize([source], self.archive, allow_synthetic=True)
        before = sha(self.archive / "archive.json")
        source.write_bytes(source.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            organize([source], self.archive, allow_synthetic=True)
        self.assertEqual(sha(self.archive / "archive.json"), before)

    def test_default_crawler_writes_private_bundle_and_organized_outputs(self):
        with patch("Crawler.Backend.social_crawler.ROOT", self.root):
            report = self.crawler().run()
        self.assertTrue(
            Path(report["output_dir"]).is_relative_to(
                self.root.resolve() / "output/crawler_runs"
            )
        )
        self.assertEqual(report["organized_duplicate_native_ids"], 0)
        self.assertTrue(
            all(
                Path(p).is_relative_to(self.archive.resolve() / "youtube")
                for p in report["primary_files"]
            )
        )
        self.assertEqual(verify(self.archive)["rows"], 3)

    def test_unmanaged_output_directory_is_preserved(self):
        self.archive.mkdir()
        sentinel = self.archive / "keep.txt"
        sentinel.write_text("user data")
        with self.assertRaisesRegex(ValueError, "not a managed"):
            organize([], self.archive)
        self.assertEqual(sentinel.read_text(), "user data")

    def test_historical_recovery_keeps_day_precision_and_checks_merge_hash(self):
        source = self.source("history", "2026-10-27T18:00:00+00:00")
        evidence = source.with_name("merge_report.json")
        evidence.write_text(
            json.dumps(
                {
                    "status": "PASS",
                    "output_sha256": sha(source),
                    "source_workbooks": [
                        {
                            "path": "unavailable-original/social_data.xlsx",
                            "first_excel_row": 2,
                            "last_excel_row": 4,
                            "rows": 3,
                        }
                    ],
                }
            )
        )
        options = {"workbook": source, "source_index": 0, "campaign_date": "2026-10-30"}
        report = organize([], self.archive, historical_sources=[options])
        self.assertEqual((report["rows"], report["day_only_records"]), (3, 3))
        self.assertEqual(report["partitions"][0]["date_wib"], "2026-10-30")
        records = [
            json.loads(line)
            for line in (self.archive / "records.jsonl").read_text().splitlines()
        ]
        self.assertTrue(
            all(r["first_seen"] is None and r["last_seen"] is None for r in records)
        )
        before = sha(self.archive / "archive.json")
        source.write_bytes(source.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "Historical merge checksum mismatch"):
            organize([], self.archive, historical_sources=[options])
        self.assertEqual(sha(self.archive / "archive.json"), before)
