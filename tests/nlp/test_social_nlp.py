from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch

import numpy as np
from openpyxl import Workbook

from MachineLearning.social_nlp import REQUIRED_COLUMNS, SocialNLPClusterer, file_hash


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
            "gemini": {"enabled": False},
            "target_topics": None,
            "cache_dir": str(cls.root / "cache"),
            "dbscan": {"eps": [0.05, 0.1, 0.2], "min_samples": [3]},
            "umap": {"n_neighbors": 4, "n_components": 2},
            "evaluation": {"sample_size": 100, "max_largest_cluster": 0.6},
        }

        def known_projection(instance):
            # Isolate DBSCAN from UMAP variability for the known-group tests.
            # A separate test exercises real UMAP and its projection cache.
            features = instance.embeddings[:, :2].copy()
            instance.reduced_embeddings = [features, features.copy()]
            instance.reduction_info = {
                "algorithm": "UMAP",
                "synthetic_fixture": True,
                "parameters": {"n_components": 2},
                "seeds": [42, 43],
            }
            return instance.reduced_embeddings

        with patch.object(SocialNLPClusterer, "_reduce_embeddings", known_projection):
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
        self.assertEqual(p.selected["parameters"]["algorithm"], "DBSCAN")
        self.assertEqual(p.selected["parameters"]["metric"], "euclidean")
        self.assertTrue(
            all(
                row["candidate"].startswith("sbert_umap_dbscan_")
                for row in p.comparisons
            )
        )
        self.assertTrue(p.sentences["membership_strength"].isna().all())
        self.assertEqual(p.sentences["dbscan_core_point"].dtype, bool)
        self.assertGreaterEqual(p.selected["coherence_cv"], 0.4)
        self.assertEqual(p.coherence["topics_evaluated"], 3)
        self.assertEqual(p.coherence["reference_documents"], 36)

    def test_cv_distinguishes_coherent_terms_and_rejects_missing_topics(self):
        import pandas as pd

        p = SocialNLPClusterer()
        p.sentences = pd.DataFrame(
            {
                "embedding_text": ["apple orange banana orchard fruit"] * 20
                + ["engine motor wheel vehicle road"] * 20
            }
        )
        coherent = p.score_coherence(
            {0: ["apple", "orange", "banana"], 1: ["engine", "motor", "wheel"]}
        )
        mixed = p.score_coherence(
            {0: ["apple", "engine", "banana"], 1: ["engine", "orange", "wheel"]}
        )
        self.assertGreater(coherent["macro_mean"], mixed["macro_mean"] + 0.2)
        self.assertEqual(coherent["reference_sha256"], mixed["reference_sha256"])
        invalid = p.score_coherence(
            {0: ["apple", "orange"], 1: ["not_in_reference", "engine"]}
        )
        self.assertIsNone(invalid["macro_mean"])
        self.assertFalse(invalid["target_met"])
        self.assertEqual(invalid["topics_total"], 2)
        self.assertEqual(invalid["topics_evaluated"], 1)

    def test_ctfidf_never_pads_short_topics_with_zero_weight_terms(self):
        import pandas as pd

        p = SocialNLPClusterer()
        p.sentences = pd.DataFrame(
            {"embedding_text": ["orchard", "orchard", "engine", "engine"]}
        )
        self.assertEqual(p._ctfidf_terms([0, 0, 1, 1]), {0: ["orchard"], 1: ["engine"]})

    def test_coherence_gate_rejects_below_target_and_blocks_publication(self):
        p = SocialNLPClusterer(self.config, encoder=encoder).prepare_excel(self.input)
        p.encode()

        def projection():
            features = p.embeddings[:, :2]
            p.reduction_info = {"parameters": {}, "seeds": [42, 43]}
            return [features, features.copy()]

        with (
            patch.object(p, "_reduce_embeddings", side_effect=projection),
            patch.object(
                p,
                "score_coherence",
                return_value={
                    "macro_mean": 0.39,
                    "topics_evaluated": 3,
                    "target_met": False,
                },
            ),
            self.assertRaisesRegex(ValueError, "No candidate"),
        ):
            p.compare()
        self.assertTrue(all(row["geometry_eligible"] for row in p.comparisons))
        self.assertTrue(all(not row["eligible"] for row in p.comparisons))
        with (
            patch.object(self.pipeline, "coherence", {"target_met": False}),
            self.assertRaisesRegex(ValueError, "coherence threshold"),
        ):
            self.pipeline.save(self.root / "rejected")
        self.assertFalse((self.root / "rejected").exists())

    def test_saved_run_coherence_reproduces_the_published_score(self):
        result = SocialNLPClusterer.evaluate_run_coherence(self.output)
        self.assertAlmostEqual(
            result["macro_mean"], self.pipeline.coherence["macro_mean"]
        )
        self.assertEqual(
            result["reference_sha256"], self.pipeline.coherence["reference_sha256"]
        )
        self.assertEqual(result["topn"], 10)
        self.assertEqual(result["window_size"], 110)
        self.assertEqual(result["source_sha256"], file_hash(self.input))
        result["reference_sha256"] = "different_reference"
        with (
            patch.object(self.pipeline, "coherence_baseline", result, create=True),
            self.assertRaisesRegex(ValueError, "reference corpus differs"),
        ):
            self.pipeline.save(self.root / "different_corpus")

    def test_coherence_search_evaluates_all_near_ties_and_skips_lower_scores(self):
        p = SocialNLPClusterer(self.config, encoder=encoder).prepare_excel(self.input)
        p.encode()

        def projection():
            features = p.embeddings[:, :2]
            p.reduction_info = {"parameters": {}, "seeds": [42, 43]}
            return [features, features.copy()]

        original = p._evaluate
        composite_scores = iter([0.3, 0.299, 0.28])

        def evaluate(*args):
            result = original(*args)
            result["selection_score"] = next(composite_scores)
            return result

        with (
            patch.object(p, "_reduce_embeddings", side_effect=projection),
            patch.object(p, "_evaluate", side_effect=evaluate),
            patch.object(p, "score_coherence", wraps=p.score_coherence) as scoring,
        ):
            p.compare()
        self.assertEqual(scoring.call_count, 2)
        self.assertTrue(all(row["eligible"] for row in p.comparisons[:2]))
        self.assertIsNone(p.comparisons[2]["coherence_cv"])
        self.assertEqual(
            p.comparisons[2]["coherence_status"],
            "not_evaluated_below_passing_score_band",
        )

    def test_noise_is_not_counted_as_a_coherent_cluster_or_shared_stability(self):
        first = np.array([-1] * 20)
        self.assertEqual(SocialNLPClusterer.stability(first, first), 0)
        a = np.array([0] * 5 + [1] * 5 + [-1] * 10)
        b = np.array([3] * 5 + [7] * 5 + [-1] * 10)
        self.assertEqual(SocialNLPClusterer.stability(a, b), 1)
        b[:5] = -1
        self.assertLess(SocialNLPClusterer.stability(a, b), 1)

    def test_topic_reduction_preserves_groups_noise_and_uses_sentence_weights(self):
        p = SocialNLPClusterer({"target_topics": 2})
        # Two nearby large groups should stay separate: merging the small
        # groups adds less total squared error despite their larger distance.
        p.embeddings = np.array(
            [[1.0, 0.0]] * 100
            + [[0.99, 0.1]] * 100
            + [[-1.0, 0.0], [-0.8, -0.6], [0.0, 1.0]],
            dtype=np.float32,
        )
        original = np.array([4] * 100 + [8] * 100 + [12, 20, -1])
        labels, info = p._merge_topics(original)
        self.assertEqual(set(labels), {-1, 0, 1})
        self.assertEqual(info["original_topics"], 4)
        self.assertEqual(info["final_topics"], 2)
        self.assertEqual(info["merges"][0]["left"], [12])
        self.assertEqual(info["merges"][0]["right"], [20])
        self.assertTrue(np.array_equal(labels == -1, original == -1))
        for cid in set(original) - {-1}:
            self.assertEqual(len(set(labels[original == cid])), 1)
        repeated, _ = p._merge_topics(original)
        self.assertTrue(np.array_equal(labels, repeated))
        with self.assertRaisesRegex(ValueError, "fewer groups"):
            p._merge_topics(np.zeros(len(original), dtype=int))
        with self.assertRaisesRegex(ValueError, "pairwise memory"):
            p._merge_topics(np.arange(2049))

    def test_retraining_reduces_topics_and_persists_original_dbscan_ids(self):
        p = (
            SocialNLPClusterer(
                {
                    **self.config,
                    "target_topics": 2,
                    "evaluation": {"max_largest_cluster": 0.8},
                },
                encoder=encoder,
            )
            .prepare_excel(self.input)
            .encode()
        )

        def projection():
            features = p.embeddings[:, :2]
            p.reduced_embeddings = [features, features.copy()]
            p.reduction_info = {"parameters": {}, "seeds": [42, 43]}
            return p.reduced_embeddings

        with patch.object(p, "_reduce_embeddings", side_effect=projection):
            p.compare().describe_topics()
        output = p.save(self.root / "two_topics")
        data = p.load_run(output)
        self.assertEqual(data["summary"]["clusters"], 2)
        self.assertEqual(data["summary"]["topic_reduction"]["original_topics"], 3)
        self.assertEqual(data["summary"]["topic_reduction"]["final_topics"], 2)
        self.assertGreaterEqual(data["summary"]["coherence"]["macro_mean"], 0.4)
        self.assertEqual(set(data["sentences"]["cluster_id"]), {0, 1})
        self.assertEqual(set(data["occurrences"]["dbscan_cluster_id"]), {0, 1, 2})
        mapped = data["occurrences"].merge(
            data["sentences"][["sentence_id", "cluster_id"]],
            on="sentence_id",
            suffixes=("_occurrence", "_sentence"),
        )
        self.assertTrue(
            (mapped.cluster_id_occurrence == mapped.cluster_id_sentence).all()
        )
        with (
            patch.dict(p.config, {"target_topics": 3}),
            self.assertRaisesRegex(ValueError, "differs from target_topics"),
        ):
            p.save(self.root / "wrong_count")

    def test_saved_embeddings_require_matching_source_model_and_sentence_order(self):
        p = SocialNLPClusterer(self.config).prepare_excel(self.input)
        with patch.object(p, "_encode_sbert", side_effect=AssertionError("must reuse")):
            p.encode(reuse_run=self.output)
        self.assertTrue(np.array_equal(p.embeddings, self.pipeline.embeddings))
        self.assertTrue(p.model_info["test_encoder"])
        self.assertIn("reused_manifest_sha256", p.model_info)
        with patch.dict(p.config["model"], {"max_tokens": 64}):
            with self.assertRaisesRegex(ValueError, "model configuration differs"):
                p.encode(reuse_run=self.output)
        p.input_sha256 = "different workbook"
        with self.assertRaisesRegex(ValueError, "source workbook differs"):
            p.encode(reuse_run=self.output)
        p.input_sha256 = self.pipeline.input_sha256
        p.sentences = p.sentences.iloc[::-1]
        with self.assertRaisesRegex(ValueError, "Prepared sentences differ"):
            p.encode(reuse_run=self.output)

    def test_real_umap_projections_and_cache_are_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            p = SocialNLPClusterer(
                {"cache_dir": directory, "umap": {"n_neighbors": 4, "n_components": 2}}
            )
            p.embeddings = self.pipeline.embeddings.copy()
            projections = p._reduce_embeddings()
            self.assertEqual([x.shape for x in projections], [(36, 2), (36, 2)])
            self.assertTrue(all(np.isfinite(x).all() for x in projections))
            self.assertFalse(p.reduction_info["cache_hit"])
            self.assertEqual(p.reduction_info["seeds"], [42, 43])
            with patch(
                "umap.UMAP",
                side_effect=AssertionError("Projection cache should be used"),
            ):
                repeated = p._reduce_embeddings()
            self.assertTrue(p.reduction_info["cache_hit"])
            self.assertTrue(
                all(np.array_equal(a, b) for a, b in zip(projections, repeated))
            )

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
        self.assertEqual(
            len(data["social_data"]), data["summary"]["preparation"]["input_rows"]
        )
        self.assertTrue(REQUIRED_COLUMNS <= set(data["social_data"].columns))
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

    def test_legacy_v1_artifact_and_explanations_remain_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "legacy"
            shutil.copytree(self.output, copied)
            (copied / "social_data.parquet").unlink()
            (copied / "umap_embeddings.npz").unlink()
            summary = json.loads((copied / "summary.json").read_text())
            summary["schema_version"] = "beesense-sentence-clusters:1"
            summary["config"].pop("dbscan")
            summary["config"]["umap"] = {"n_neighbors": 4, "n_components": 2}
            summary["config"]["hdbscan"] = {
                "min_cluster_sizes": [5],
                "min_samples": [2],
            }
            (copied / "summary.json").write_text(json.dumps(summary))
            manifest = json.loads((copied / "manifest.json").read_text())
            manifest["schema_version"] = "beesense-sentence-clusters:1"
            manifest["files_sha256"].pop("social_data.parquet")
            manifest["files_sha256"].pop("umap_embeddings.npz")
            manifest["files_sha256"]["summary.json"] = file_hash(
                copied / "summary.json"
            )
            (copied / "manifest.json").write_text(json.dumps(manifest))
            with patch.object(
                SocialNLPClusterer,
                "encode",
                side_effect=AssertionError("No retraining"),
            ):
                data = SocialNLPClusterer.load_run(copied)
                explained = SocialNLPClusterer.explain_artifacts(data)
            self.assertEqual(len(explained["topics"]), 3)

    def test_sparse_dbscan_preserves_zero_distance_neighbors(self):
        import pandas as pd

        p = SocialNLPClusterer({"dbscan": {"eps": [0.01], "min_samples": [3]}})
        p.embeddings = np.repeat(np.eye(3, dtype=np.float32), 4, axis=0)
        p.sentences = pd.DataFrame({"sentence_id": [f"s{i}" for i in range(12)]})
        p.occurrences = p.sentences.copy()
        p.window_counts = [1] * 12
        from sklearn.cluster import DBSCAN

        graph = p._filter_radius(p._radius_graph(), 0.01)
        model = DBSCAN(eps=0.01, min_samples=3, metric="precomputed").fit(graph)
        self.assertEqual(len(set(model.labels_)), 3)
        self.assertTrue((model.labels_ >= 0).all())
        self.assertEqual(len(model.core_sample_indices_), 12)

    def test_dbscan_memory_guard_and_no_eligible_candidate_are_explicit(self):
        p = SocialNLPClusterer({"dbscan": {"max_neighbor_edges": 1}})
        p.embeddings = np.repeat(np.eye(3, dtype=np.float32), 4, axis=0)
        with self.assertRaisesRegex(ValueError, "max_neighbor_edges"):
            p._radius_graph()
        with self.assertRaisesRegex(ValueError, "No candidate"):
            SocialNLPClusterer.select_candidate([{"eligible": False}], 0.005)

    def test_bad_input_and_configuration_are_rejected(self):
        for config in [
            {"unknown": 1},
            {"graph": {"max_nodes": 20000}},
            {"model": {"revision": "main"}},
            {"model": {"backend": "unsupported"}},
            {"dbscan": {"eps": [float("nan")]}},
            {"dbscan": {"eps": []}},
            {"dbscan": {"min_samples": [True]}},
            {"coherence": {"metric": "u_mass"}},
            {"coherence": {"min_score": float("nan")}},
            {"coherence": {"topn": 1}},
            {"include_kinds": ["user"]},
            {"target_topics": True},
            {"target_topics": 1},
            {"target_topics": 20.0},
            {"target_topics": 501},
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

        from streamlit_apps import SocialNLPStreamlitApp

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

        from streamlit_apps import SocialNLPStreamlitApp

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
