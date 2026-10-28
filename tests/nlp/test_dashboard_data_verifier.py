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
        with self.assertRaisesRegex(ValueError, "published source workbooks"):
            verifier.verify()

    def test_unexpected_workbook_is_rejected(self):
        self.source.with_name("other_dataset.xlsx").write_bytes(b"unpublished")
        with self.assertRaisesRegex(ValueError, "published source workbooks"):
            verifier.verify()

    def test_input_integrity_remains_enforced(self):
        self.source.write_bytes(b"changed dashboard input")
        with self.assertRaisesRegex(ValueError, "checksum differs"):
            verifier.verify()


if __name__ == "__main__":
    unittest.main()
