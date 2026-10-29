import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import verify_dashboard_data as verifier


class PublishedDataTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.root = Path(workspace.name)
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
        (self.root / "social_nlp.json").write_text(
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
        path = self.root / "social_nlp.json"
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
        path = self.root / "social_nlp.json"
        config = json.loads(path.read_text())
        config["input_file"] = str(merged.relative_to(self.root))
        path.write_text(json.dumps(config))
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, "Published source workbooks"):
            verifier.verify()

    def test_active_topic_count_and_coherence_threshold_are_enforced(self):
        path = self.root / "social_nlp.json"
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
        path = self.root / "social_nlp.json"
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
