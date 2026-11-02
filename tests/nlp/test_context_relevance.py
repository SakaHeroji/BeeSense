"""No model/network calls: policy, provenance and integration regressions."""

import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from test_social_nlp import fixture

from MachineLearning.context_relevance import (
    DECISIONS_FILE,
    REPORT_FILE,
    ContextRelevanceFilter,
    checksum,
)
from MachineLearning.social_nlp import ROOT, SocialNLPClusterer


class RelevanceTests(unittest.TestCase):
    def test_explicit_configuration_does_not_inherit_another_corpus_mask(self):
        active = json.loads((ROOT / "config/social_nlp.json").read_text())
        active["relevance_artifact"] = "outputs/corpus_specific_mask"
        with patch(
            "MachineLearning.social_nlp.Path.read_text", return_value=json.dumps(active)
        ):
            self.assertEqual(
                SocialNLPClusterer().config["relevance_artifact"],
                "outputs/corpus_specific_mask",
            )
            self.assertIsNone(SocialNLPClusterer({}).config["relevance_artifact"])
            self.assertIsNone(
                SocialNLPClusterer({"target_topics": 20}).config["relevance_artifact"]
            )
            self.assertEqual(
                SocialNLPClusterer(
                    {"relevance_artifact": "outputs/explicit_mask"}
                ).config["relevance_artifact"],
                "outputs/explicit_mask",
            )

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.calls = []

    def tearDown(self):
        self.temp.cleanup()

    def predictor(self, texts, labels):
        self.calls.extend(texts)
        rows = []
        for text in texts:
            if "football" in text:
                rows.append([0.1, 0.1, 0.9])
            elif "thanks" in text:
                rows.append([0.1, 0.9, 0.1])
            elif "ambiguous" in text or "weak" in text:
                rows.append(
                    [0.85, 0.1, 0.1]
                    if "Konteks post asal: campus" in text
                    else [0.3, 0.25, 0.2]
                )
            else:
                rows.append([0.9, 0.1, 0.1])
        return np.asarray(rows)

    def make(self, **options):
        return ContextRelevanceFilter(
            {"cache_dir": str(self.root / "cache"), **options}, predictor=self.predictor
        )

    def test_direct_relevance_and_unrelated_target_never_inherit_root(self):
        f = self.make()
        try:
            result = f.classify_many(
                [
                    {"sentence": "tuition question", "post_text": "campus"},
                    {"sentence": "football question", "post_text": "campus"},
                    {"sentence": "thanks", "post_text": "campus"},
                ]
            )
            self.assertEqual(
                [r["decision"] for r in result], ["relevant", "irrelevant", "generic"]
            )
            self.assertFalse(any(r["context_used"] for r in result))
        finally:
            f.close()

    def test_same_ambiguous_sentence_can_have_different_context_decisions(self):
        f = self.make()
        try:
            rows = f.classify_many(
                [
                    {"sentence": "ambiguous", "post_text": "campus"},
                    {"sentence": "ambiguous", "post_text": "unrelated"},
                    {"sentence": "ambiguous"},
                ]
            )
            self.assertEqual(
                [r["decision"] for r in rows], ["relevant", "uncertain", "uncertain"]
            )
            self.assertTrue(rows[0]["context_used"])
            self.assertFalse(rows[2]["context_used"])
        finally:
            f.close()

    def test_weak_short_match_requires_context(self):
        def weak(texts, labels):
            return np.tile([0.5, 0.1, 0.1], (len(texts), 1))

        f = ContextRelevanceFilter(
            {"cache_dir": str(self.root / "cache")}, predictor=weak
        )
        try:
            self.assertEqual(
                f.classify_many([{"sentence": "short target"}])[0]["decision"],
                "uncertain",
            )
        finally:
            f.close()

    def test_cache_resumes_and_configuration_changes_invalidate_it(self):
        f = self.make()
        f.classify_many([{"sentence": "tuition question"}])
        f.close()
        n = len(self.calls)
        f = self.make()
        f.classify_many([{"sentence": "tuition question"}])
        f.close()
        self.assertEqual(len(self.calls), n)
        f = self.make(accept_score=0.8)
        f.classify_many([{"sentence": "tuition question"}])
        f.close()
        self.assertGreater(len(self.calls), n)

    def test_invalid_configuration_and_scores_fail_closed(self):
        for config in [
            {"unknown": True},
            {"keywords": []},
            {"accept_score": float("nan")},
            {"references": {}},
            {"revision": "main"},
            {"keywords": ["politik"]},
            {"stride": 128},
        ]:
            with self.subTest(config=config), self.assertRaises(ValueError):
                self.make(**config)
        f = self.make()
        f.predictor = lambda texts, labels: [[float("nan"), 0, 0]]
        try:
            with self.assertRaisesRegex(ValueError, "invalid scores"):
                f.classify_many([{"sentence": "new target"}])
        finally:
            f.close()

    def test_audit_csv_escapes_formulas_without_changing_stored_text(self):
        from Dashboard.app import relevance_csv

        original = pd.DataFrame(
            {"sentence": ["=1+1", " @SUM(A1:A2)", "Kuliah di kampus."]}
        )
        rows = list(
            csv.DictReader(io.StringIO(relevance_csv(original).decode("utf-8-sig")))
        )
        self.assertEqual(rows[0]["sentence"], "'=1+1")
        self.assertEqual(rows[1]["sentence"], "' @SUM(A1:A2)")
        self.assertEqual(rows[2]["sentence"], "Kuliah di kampus.")
        self.assertEqual(original.iloc[0, 0], "=1+1")

    def snapshot(self):
        path = self.root / "source.xlsx"
        fixture(path, duplicate=True)
        book = load_workbook(path)
        sheet = book["Data"]
        for row in range(2, sheet.max_row + 1):
            platform = sheet.cell(row, 1).value
            sheet.cell(row, 9).value = (
                f"https://www.youtube.com/watch?v=TestVideo01&lc=c{row}"
                if platform == "youtube"
                else f"https://www.reddit.com/comments/thread/_/c{row}/"
            )
        book.save(path)
        p = SocialNLPClusterer({"gemini": {"enabled": False}}).prepare_excel(path)
        return p, {
            "social_data": p.source_data,
            "occurrences": p.occurrences,
            "summary": {"source_file": str(path), "source_sha256": p.input_sha256},
            "artifact_manifest_sha256": "a" * 64,
        }

    def test_filter_dataset_is_immutable_and_bound_to_entire_source(self):
        p, data = self.snapshot()
        f = self.make()
        output = self.root / "filtered"
        try:
            f.filter_snapshot(data, output)
            decisions, report = f.load_decisions(
                output, p.input_sha256, p.occurrences.occurrence_id
            )
            self.assertEqual(len(decisions), len(p.occurrences))
            self.assertEqual(report["accepted_occurrences"], len(p.occurrences))
            with self.assertRaises(FileExistsError):
                f.filter_snapshot(data, output)
            with self.assertRaisesRegex(ValueError, "different source"):
                f.load_decisions(output, "b" * 64, p.occurrences.occurrence_id)
            with self.assertRaisesRegex(ValueError, "every occurrence"):
                f.load_decisions(
                    output, p.input_sha256, p.occurrences.occurrence_id.iloc[:-1]
                )
        finally:
            f.close()

    def test_checksum_tampering_is_rejected(self):
        p, data = self.snapshot()
        f = self.make()
        try:
            out = f.filter_snapshot(data, self.root / "filtered")
            (out / REPORT_FILE).write_text("{}")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                f.load_decisions(out, p.input_sha256, p.occurrences.occurrence_id)
        finally:
            f.close()

    def test_training_consumes_mask_without_modifying_source_text(self):
        p, data = self.snapshot()
        f = self.make()
        try:
            out = f.filter_snapshot(data, self.root / "filtered")
            audit = pd.read_parquet(out / DECISIONS_FILE)
            audit.loc[audit.index[-2:], "decision"] = "uncertain"
            audit.to_parquet(out / DECISIONS_FILE, index=False)
            report = json.loads((out / REPORT_FILE).read_text())
            report["accepted_occurrences"] -= 2
            report["decisions"] = audit.decision.value_counts().to_dict()
            accepted = audit[audit.decision == "relevant"]
            report["accepted_unique_sentences"] = int(accepted.sentence_id.nunique())
            filtered = pd.read_parquet(out / "filtered_sentences.parquet")
            filtered[filtered.occurrence_id.isin(accepted.occurrence_id)].to_parquet(
                out / "filtered_sentences.parquet", index=False
            )
            (out / REPORT_FILE).write_text(json.dumps(report))
            manifest = json.loads((out / "manifest.json").read_text())
            manifest["files_sha256"] = {
                name: checksum(out / name) for name in manifest["files_sha256"]
            }
            (out / "manifest.json").write_text(json.dumps(manifest))
            new = SocialNLPClusterer(
                {"gemini": {"enabled": False}, "relevance_artifact": str(out)}
            ).prepare_excel(p.input_path)
            self.assertEqual(len(new.occurrences), len(p.occurrences) - 2)
            self.assertEqual(new.source_data.teks.tolist(), p.source_data.teks.tolist())
            self.assertTrue(
                set(new.sentences.sentence_id) <= set(p.sentences.sentence_id)
            )
            saved = {
                "summary": {
                    "source_sha256": p.input_sha256,
                    "config": p.config,
                    "model": {"test_encoder": True},
                },
                "sentences": p.sentences.assign(embedding_windows=1),
                "embeddings": np.eye(len(p.sentences), dtype=np.float32),
                "artifact_manifest_sha256": "c" * 64,
            }
            with patch.object(SocialNLPClusterer, "load_run", return_value=saved):
                new.encode(reuse_run="baseline")
                positions = {sid: i for i, sid in enumerate(p.sentences.sentence_id)}
                expected = saved["embeddings"][
                    [positions[sid] for sid in new.sentences.sentence_id]
                ]
                np.testing.assert_array_equal(new.embeddings, expected)
                self.assertTrue(new.model_info["reused_verified_subset"])
                saved["sentences"].loc[0, "embedding_text"] = "changed text"
                with self.assertRaisesRegex(ValueError, "Prepared sentences differ"):
                    new.encode(reuse_run="baseline")
        finally:
            f.close()


if __name__ == "__main__":
    unittest.main()
