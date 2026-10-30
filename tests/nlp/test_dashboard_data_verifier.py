import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import verify_dashboard_data as verifier


class NativeDatasetTests(unittest.TestCase):
    def test_native_uniqueness_is_independent_of_equal_text_and_kind(self):
        from openpyxl import Workbook

        from scripts.merge_social_datasets import COLUMNS

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "social_data.xlsx"
            book = Workbook()
            sheet = book.active
            sheet.title = "Data"
            sheet.append(COLUMNS)
            for kind, url, text in [
                ("post", "https://www.instagram.com/p/B/", "Kuliah"),
                ("comment", "https://www.instagram.com/p/B/?comment_id=21", "Sama"),
                ("comment", "https://www.instagram.com/p/B/?comment_id=22", "Sama"),
            ]:
                sheet.append(
                    [
                        "instagram",
                        kind,
                        "Kuliah",
                        None,
                        "unknown",
                        None,
                        "unknown",
                        text,
                        url,
                        False,
                    ]
                )
            book.save(path)
            self.assertEqual(
                verifier.verify_native_dataset(path),
                {"rows": 3, "roots": 1, "duplicate_native_ids": 0},
            )
            sheet.append(
                [
                    "instagram",
                    "reply",
                    "Kuliah",
                    None,
                    "unknown",
                    None,
                    "unknown",
                    "Berbeda",
                    "https://www.instagram.com/p/B/?comment_id=21",
                    False,
                ]
            )
            book.save(path)
            book.close()
            with self.assertRaisesRegex(ValueError, "Duplicate native record"):
                verifier.verify_native_dataset(path)

    def test_published_merge_audit_is_bound_to_its_file_checksums(self):
        from openpyxl import Workbook

        from scripts.merge_social_datasets import COLUMNS, merge

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.xlsx"
            book = Workbook()
            sheet = book.active
            sheet.title = "Data"
            sheet.append(COLUMNS)
            sheet.append(
                [
                    "instagram",
                    "post",
                    "Kuliah",
                    None,
                    "unknown",
                    None,
                    "unknown",
                    "Kuliah",
                    "https://www.instagram.com/p/B/",
                    False,
                ]
            )
            book.save(source)
            book.close()
            merge(
                [source],
                root / "merged",
                root / "provenance.json",
                duplicate_policy="prefer_latest",
            )
            files = verifier.published_source_files(root / "merged/social_data.xlsx")
            self.assertEqual(len(files), 4)
            (root / "merged/record_lineage.jsonl").write_text("tampered")
            with self.assertRaisesRegex(ValueError, "merge audit checksum"):
                verifier.published_source_files(root / "merged/social_data.xlsx")

    def test_append_only_merge_sidecars_are_required_and_checksum_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {
                "social_data.xlsx": b"source workbook",
                "instagram_acquisition_verification.json": b"{}",
                "independent_final_audit.json": b"{}",
                "artifact_verification.json": b"{}",
                "preview.png": b"preview",
            }
            for name, contents in files.items():
                (root / name).write_bytes(contents)
            report = {
                "schema_version": "beesense-append-only-merge:1",
                "output_sha256": hashlib.sha256(files["social_data.xlsx"]).hexdigest(),
                "duplicate_native_ids": 0,
                "files_sha256": {
                    name: hashlib.sha256(value).hexdigest()
                    for name, value in files.items()
                },
            }
            (root / "merge_report.json").write_text(json.dumps(report))
            self.assertEqual(
                len(verifier.published_source_files(root / "social_data.xlsx")), 6
            )
            (root / "independent_final_audit.json").write_text("tampered")
            with self.assertRaisesRegex(ValueError, "audit checksum"):
                verifier.published_source_files(root / "social_data.xlsx")
            report["files_sha256"]["../outside.json"] = "digest"
            (root / "merge_report.json").write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, "Unexpected published"):
                verifier.published_source_files(root / "social_data.xlsx")


class PublishedDataTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.root = Path(workspace.name)
        (self.root / "config").mkdir()
        self.source = self.root / "outputs/social_20261028_01/social_data.xlsx"
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(b"dashboard input")
        self.audit = self.source.with_name("dataset.xlsx")
        self.audit.write_bytes(b"full audit source")
        run = self.root / "outputs/nlp_test"
        run.mkdir()
        (run / "summary.json").write_text("{}")
        (run / "manifest.json").write_text(
            json.dumps({"files_sha256": {"summary.json": "verified by load_run"}})
        )
        (self.root / "config/social_nlp.json").write_text(
            json.dumps(
                {
                    "input_file": str(self.source.relative_to(self.root)),
                    "output_dir": str(run.relative_to(self.root)),
                }
            )
        )
        snapshot = {
            "summary": {
                "source_sha256": hashlib.sha256(self.source.read_bytes()).hexdigest()
            },
            "artifact_manifest_sha256": "verified manifest",
            "topics": [1],
            "occurrences": [1, 2],
            "sentences": [1],
        }
        self.addCleanup(patch.stopall)
        patch.object(verifier, "ROOT", self.root).start()
        patch.object(
            verifier.SocialNLPClusterer, "load_run", return_value=snapshot
        ).start()
        # The workbook boundary has separate tests; these cases isolate the
        # publication/manifest rules with small byte fixtures.
        patch.object(
            verifier,
            "verify_native_dataset",
            return_value={"rows": 2, "roots": 1, "duplicate_native_ids": 0},
        ).start()

    def test_preserved_audit_and_excel_owner_files_are_supported(self):
        for name in ["~$social_data.xlsx", "~$dataset.xlsx"]:
            self.source.with_name(name).write_bytes(b"Excel owner file")
        result = verifier.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            result["audit_sha256"], hashlib.sha256(self.audit.read_bytes()).hexdigest()
        )
        self.assertNotEqual(result["input_sha256"], result["audit_sha256"])

    def test_missing_preserved_audit_is_rejected(self):
        self.audit.unlink()
        with self.assertRaisesRegex(ValueError, "Published source workbooks"):
            verifier.verify()

    def test_unexpected_workbook_is_rejected(self):
        self.source.with_name("other_dataset.xlsx").write_bytes(b"unpublished")
        with self.assertRaisesRegex(ValueError, "Published source workbooks"):
            verifier.verify()

    def test_input_integrity_remains_enforced(self):
        self.source.write_bytes(b"changed dashboard input")
        with self.assertRaisesRegex(ValueError, "checksum differs"):
            verifier.verify()

    def test_merged_input_preserves_and_checks_both_baseline_workbooks(self):
        merged = self.root / "outputs/social_combined/social_data.xlsx"
        merged.parent.mkdir()
        merged.write_bytes(b"merged dashboard input")
        path = self.root / "config/social_nlp.json"
        config = json.loads(path.read_text())
        config["input_file"] = str(merged.relative_to(self.root))
        path.write_text(json.dumps(config))
        snapshot = verifier.SocialNLPClusterer.load_run.return_value
        snapshot["summary"]["source_sha256"] = hashlib.sha256(
            merged.read_bytes()
        ).hexdigest()
        self.assertEqual(verifier.verify()["published_data_files"], 5)
        self.source.with_name("unpublished.xlsx").write_bytes(b"unexpected")
        with self.assertRaisesRegex(ValueError, "unexpected files"):
            verifier.verify()

    def test_missing_baseline_compact_is_rejected_for_merged_input(self):
        merged = self.root / "outputs/social_combined/social_data.xlsx"
        merged.parent.mkdir()
        merged.write_bytes(self.source.read_bytes())
        path = self.root / "config/social_nlp.json"
        config = json.loads(path.read_text())
        config["input_file"] = str(merged.relative_to(self.root))
        path.write_text(json.dumps(config))
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, "Published source workbooks"):
            verifier.verify()

    def test_active_topic_count_and_coherence_threshold_are_enforced(self):
        path = self.root / "config/social_nlp.json"
        config = json.loads(path.read_text())
        config.update(target_topics=20, coherence={"min_score": 0.4})
        path.write_text(json.dumps(config))
        snapshot = verifier.SocialNLPClusterer.load_run.return_value
        with self.assertRaisesRegex(ValueError, "target_topics"):
            verifier.verify()
        snapshot["topics"] = list(range(20))
        for score in [None, 0.39, float("nan")]:
            snapshot["summary"]["coherence"] = {"macro_mean": score}
            with (
                self.subTest(score=score),
                self.assertRaisesRegex(ValueError, "coherence threshold"),
            ):
                verifier.verify()
        snapshot["summary"]["coherence"] = {"macro_mean": 0.4}
        self.assertEqual(verifier.verify()["topics"], 20)

    def test_archived_nlp_snapshot_and_separate_crawl_output_are_supported(self):
        archive = self.root / "outputs/nlp_previous"
        archive.mkdir()
        (archive / "summary.json").write_text("{}")
        (archive / "manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": "beesense-sentence-clusters:1",
                    "files_sha256": {"summary.json": "verified by load_run"},
                }
            )
        )
        crawl = self.root / "outputs/social_selenium_test"
        crawl.mkdir()
        (crawl / "dataset.xlsx").write_bytes(b"unrelated local crawl")
        result = verifier.verify()
        self.assertEqual(result["archived_runs"], ["outputs/nlp_previous"])
        self.assertEqual(result["published_data_files"], 6)

    def test_preserved_baseline_hash_is_checked_after_switching_to_merged_input(self):
        merged = self.root / "outputs/social_combined/social_data.xlsx"
        merged.parent.mkdir()
        merged.write_bytes(self.source.read_bytes())
        path = self.root / "config/social_nlp.json"
        config = json.loads(path.read_text())
        config["input_file"] = str(merged.relative_to(self.root))
        path.write_text(json.dumps(config))
        archive = self.root / "outputs/nlp_previous"
        archive.mkdir()
        (archive / "summary.json").write_text("{}")
        (archive / "manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": "beesense-sentence-clusters:2",
                    "files_sha256": {"summary.json": "verified by load_run"},
                }
            )
        )
        active = verifier.SocialNLPClusterer.load_run.return_value
        old = {"summary": {**active["summary"], "source_file": str(self.source)}}
        verifier.SocialNLPClusterer.load_run.side_effect = lambda directory: (
            old if directory == archive else active
        )
        self.source.write_bytes(b"modified historical workbook")
        with self.assertRaisesRegex(ValueError, "Preserved baseline checksum"):
            verifier.verify()

    def test_unexpected_file_in_archive_is_rejected(self):
        archive = self.root / "outputs/nlp_previous"
        archive.mkdir()
        (archive / "summary.json").write_text("{}")
        (archive / "unlisted.parquet").write_bytes(b"unlisted")
        (archive / "manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": "beesense-sentence-clusters:1",
                    "files_sha256": {"summary.json": "verified by load_run"},
                }
            )
        )
        with self.assertRaisesRegex(ValueError, "unexpected files"):
            verifier.verify()


if __name__ == "__main__":
    unittest.main()
