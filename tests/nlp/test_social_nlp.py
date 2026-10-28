from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

import numpy as np
from openpyxl import Workbook

from social_nlp import REQUIRED_COLUMNS, SocialNLPClusterer, file_hash


def fixture(path, duplicate=False, truncated=False):
    headers = [
        "platform",
        "jenis",
        "judul_post",
        "tanggal_post_wib",
        "akurasi_tanggal_post",
        "tanggal_konten_wib",
        "akurasi_tanggal_konten",
        "teks",
        "url",
        "teks_dipotong",
    ]
    book = Workbook()
    sheet = book.active
    sheet.title = "Data"
    sheet.append(headers)
    groups = [
        "Beasiswa membantu pembayaran uang pendidikan",
        "Karier lulusan memerlukan pengalaman kerja",
        "Komputer menjalankan program algoritma perangkat",
    ]
    for group, text in enumerate(groups):
        for i in range(12):
            sheet.append(
                [
                    "reddit" if i % 2 else "youtube",
                    "comment",
                    "TITLE_NOT_EMBEDDING_FEATURE",
                    datetime(2026, 10, 1, microsecond=123000 if i % 2 else 0),
                    "pasti",
                    datetime(2026, 10, 15),
                    "perkiraan",
                    f"{text} contoh nomor {i}.",
                    f"https://www.reddit.com/comments/thread/comment/{group}{i}/",
                    truncated,
                ]
            )
    if duplicate:
        sheet.append(
            [
                "youtube",
                "reply",
                "TITLE_NOT_EMBEDDING_FEATURE",
                datetime(2026, 10, 1),
                "pasti",
                datetime(2026, 10, 15),
                "perkiraan",
                groups[0] + " contoh nomor 0.",
                "https://youtu.be/abc?lc=duplicate",
                False,
            ]
        )
        sheet.append(
            [
                "youtube",
                "comment",
                "TITLE_NOT_EMBEDDING_FEATURE",
                datetime(2026, 10, 1),
                "pasti",
                datetime(2026, 10, 15),
                "perkiraan",
                "❤😊",
                "https://youtu.be/abc?lc=emoji",
                False,
            ]
        )
    book.save(path)


def encoder(texts):
    vectors = []
    for text in texts:
        assert "TITLE_NOT_EMBEDDING_FEATURE" not in text
        index = 0 if "Beasiswa" in text else 1 if "Karier" in text else 2
        vector = np.zeros(6, dtype=np.float32)
        vector[index] = 1
        vector[3:] = np.random.default_rng(sum(text.encode())).normal(0, 0.01, 3)
        vectors.append(vector)
    return np.asarray(vectors)


class NLPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.input = cls.root / "source.xlsx"
        fixture(cls.input, duplicate=True)
        cls.config = {
            "cache_dir": str(cls.root / "cache"),
            "hdbscan": {"min_cluster_sizes": [5], "min_samples": [2]},
            "kmeans": {"cluster_counts": [3], "n_init": 3},
            "tfidf_baseline_clusters": 3,
            "umap": {"n_neighbors": 4, "n_components": 2},
            "evaluation": {"sample_size": 100, "max_largest_cluster": 0.6},
        }
        cls.pipeline = SocialNLPClusterer(cls.config, encoder=encoder).fit_excel(
            cls.input
        )
        cls.output = cls.pipeline.save(cls.root / "result")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_span_offsets_and_abbreviations_are_source_faithful(self):
        text = "Prof. Dian membayar 3.5 juta. Kuliah di UI?\nDaftar https://a.test/ukt. Saya tidak setuju!"
        spans = SocialNLPClusterer.sentence_spans(text)
        sentences = [text[a:b] for a, b, _ in spans]
        self.assertEqual(
            sentences,
            [
                "Prof. Dian membayar 3.5 juta.",
                "Kuliah di UI?",
                "Daftar https://a.test/ukt.",
                "Saya tidak setuju!",
            ],
        )
        self.assertIn("tidak", SocialNLPClusterer._clean(sentences[-1]))
        self.assertTrue(all(a < b for a, b, _ in spans))

    def test_long_segments_cover_text_without_silent_truncation(self):
        text = " ".join(["biaya kuliah"] * 100)
        spans = SocialNLPClusterer.sentence_spans(text, max_characters=100)
        self.assertTrue(all(kind == "length_window" for _, _, kind in spans))
        self.assertTrue(all(b - a <= 100 for a, b, _ in spans))
        self.assertEqual(" ".join(text[a:b] for a, b, _ in spans), text)

    def test_dedup_preserves_both_occurrences_and_original_dates(self):
        p = self.pipeline
        self.assertEqual(len(p.sentences), 36)
        self.assertEqual(len(p.occurrences), 37)
        self.assertEqual(p.preparation["duplicate_occurrences"], 1)
        self.assertEqual(len(p.skipped), 1)
        self.assertEqual(set(p.occurrences["content_date_accuracy"]), {"perkiraan"})
        self.assertTrue(p.occurrences["post_date"].str.startswith("2026-10-01").all())
        self.assertEqual(p.occurrences["occurrence_id"].nunique(), 37)

    def test_selected_candidate_has_semantic_separation_and_full_provenance(self):
        p = self.pipeline
        self.assertTrue(p.selected["eligible"])
        self.assertEqual(p.selected["clusters"], 3)
        self.assertGreater(p.selected["silhouette_cosine"], 0.9)
        self.assertEqual(len(p.comparisons), 3)
        self.assertTrue(np.allclose(np.linalg.norm(p.embeddings, axis=1), 1))
        self.assertTrue(
            set(p.occurrences["sentence_id"]) <= set(p.sentences["sentence_id"])
        )
        self.assertEqual(p.input_sha256, file_hash(self.input))

    def test_noise_is_not_counted_as_a_coherent_cluster_or_shared_stability(self):
        first = np.array([-1] * 20)
        self.assertEqual(SocialNLPClusterer.stability(first, first), 0)
        a = np.array([0] * 5 + [1] * 5 + [-1] * 10)
        b = np.array([3] * 5 + [7] * 5 + [-1] * 10)
        self.assertEqual(SocialNLPClusterer.stability(a, b), 1)
        b[:5] = -1
        self.assertLess(SocialNLPClusterer.stability(a, b), 1)

    def test_close_scores_prefer_separation_without_hardcoding_algorithm(self):
        candidates = [
            dict(
                candidate="coverage",
                eligible=True,
                selection_score=0.31,
                silhouette_cosine=0.03,
                stability_ari=0.5,
                coverage=1,
            ),
            dict(
                candidate="separation",
                eligible=True,
                selection_score=0.309,
                silhouette_cosine=0.09,
                stability_ari=0.8,
                coverage=0.53,
            ),
        ]
        selected, policy = SocialNLPClusterer.select_candidate(candidates, 0.005)
        self.assertEqual(selected["candidate"], "separation")
        self.assertEqual(len(policy["near_tie_candidates"]), 2)
        selected, _ = SocialNLPClusterer.select_candidate(candidates, 0)
        self.assertEqual(selected["candidate"], "coverage")

    def test_scores_are_in_original_embedding_geometry_and_coverage_penalized(self):
        p = SocialNLPClusterer(self.config, encoder=encoder)
        p.embeddings = self.pipeline.embeddings
        p.evaluation_indices = np.arange(36)
        labels = np.repeat([0, 1, 2], 12)
        good = p._evaluate("all", labels, labels, {}, 0)
        sparse = labels.copy()
        sparse[::2] = -1
        noisy = p._evaluate("half", sparse, sparse, {}, 0)
        self.assertGreater(good["selection_score"], noisy["selection_score"])
        rejected = p._evaluate("none", np.full(36, -1), np.full(36, -1), {}, 0)
        self.assertFalse(rejected["eligible"])
        self.assertIsNone(rejected["selection_score"])

    def test_artifacts_roundtrip_without_pickle_and_verify_checksums(self):
        data = SocialNLPClusterer.load_run(self.output)
        self.assertEqual(len(data["sentences"]), 36)
        self.assertTrue(data["summary"]["synthetic"])
        self.assertTrue(np.allclose(data["embeddings"], self.pipeline.embeddings))
        self.assertEqual(data["summary"]["source_sha256"], file_hash(self.input))
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "copy"
            shutil.copytree(self.output, copied)
            with (copied / "sentences.parquet").open("ab") as stream:
                stream.write(b"changed")
            with self.assertRaisesRegex(ValueError, "checksum"):
                SocialNLPClusterer.load_run(copied)
            manifest = json.loads((copied / "manifest.json").read_text())
            manifest["files_sha256"].pop("sentences.parquet")
            (copied / "manifest.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "required"):
                SocialNLPClusterer.load_run(copied)

    def test_existing_artifact_directory_and_source_input_are_preserved(self):
        before = file_hash(self.input)
        with self.assertRaises(FileExistsError):
            self.pipeline.save(self.output)
        self.assertEqual(before, file_hash(self.input))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "truncated.xlsx"
            fixture(path, truncated=True)
            with self.assertRaisesRegex(ValueError, "truncated"):
                SocialNLPClusterer(self.config, encoder=encoder).prepare_excel(path)

    def test_bad_input_and_configuration_are_rejected(self):
        for config in [
            {"unknown": 1},
            {"graph": {"max_nodes": 20000}},
            {"model": {"revision": "main"}},
            {"model": {"onnx_file": "../model.onnx"}},
            {"include_kinds": ["user"]},
        ]:
            with self.subTest(config=config), self.assertRaises(ValueError):
                SocialNLPClusterer(config)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.xlsx"
            book = Workbook()
            book.active.title = "Data"
            book.active.append(["text"])
            book.save(path)
            with self.assertRaisesRegex(ValueError, "columns"):
                SocialNLPClusterer().prepare_excel(path)
        self.assertIn("teks", REQUIRED_COLUMNS)

    def test_graph_links_are_scored_inferences_not_social_relationships(self):
        p = SocialNLPClusterer({"graph": {"neighbors": 2, "min_similarity": 0.55}})
        p.topics = [{"cluster_id": i, "label": str(i)} for i in range(3)]
        p.centroids = np.array([[1, 0], [0.8, 0.6], [0, 1]], dtype=np.float32)
        p.graph = p.build_topic_graph()
        self.assertEqual(len(p.graph["edges"]), 2)
        for edge in p.graph["edges"]:
            self.assertEqual(edge["confidence"], "INFERRED")
            self.assertEqual(edge["relation"], "semantic_similarity")
            self.assertEqual(edge["score_kind"], "cosine_not_probability")
            self.assertGreaterEqual(
                edge["similarity"], p.config["graph"]["min_similarity"]
            )
        for topic in self.pipeline.topics:
            self.assertTrue(
                set(topic["representative_ids"])
                <= set(self.pipeline.sentences["sentence_id"])
            )


class DashboardTests(unittest.TestCase):
    def test_filters_are_literal_and_respect_platform_dates(self):
        import pandas as pd

        from nlp_dashboard import SocialNLPStreamlitApp

        frame = pd.DataFrame(
            [
                {
                    "platform": "reddit",
                    "post_date": "2026-01-01",
                    "sentence": "[KIP] biaya",
                    "cluster_id": 1,
                },
                {
                    "platform": "youtube",
                    "post_date": "2026-02-01",
                    "sentence": "Biaya lain",
                    "cluster_id": -1,
                },
            ]
        )
        selected = SocialNLPStreamlitApp.filter_occurrences(
            frame, ["reddit"], date(2026, 1, 1), date(2026, 1, 31), "[KIP]", 1
        )
        self.assertEqual(len(selected), 1)
        self.assertEqual(
            SocialNLPStreamlitApp._date_label(
                {
                    "content_date": "2026-01-01T00:00:00",
                    "content_date_accuracy": "perkiraan",
                }
            ),
            "2026-01-01 (perkiraan)",
        )

    def test_topic_graph_is_bounded_and_noise_is_not_a_topic(self):
        import pandas as pd

        from nlp_dashboard import SocialNLPStreamlitApp

        topics = [{"cluster_id": i, "label": f"Topik {i}"} for i in range(30)]
        occurrences = pd.DataFrame(
            [{"cluster_id": i, "platform": "reddit"} for i in range(-1, 30)]
        )
        figure, stats = SocialNLPStreamlitApp.topic_figure(
            topics, {"edges": []}, occurrences, 0.5, 10, 25
        )
        self.assertEqual(stats["nodes"], 10)
        ids = [int(item[0]) for item in figure.data[-1].customdata]
        self.assertIn(25, ids)
        self.assertNotIn(-1, ids)


if __name__ == "__main__":
    unittest.main()
