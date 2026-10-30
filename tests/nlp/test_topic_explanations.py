from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from MachineLearning.social_nlp import SocialNLPClusterer as Model


def model_from_counts(totals, hits, *, fixed_topic_root=False):
    model = Model()
    rows = []
    for month, (denominators, numerators) in enumerate(zip(totals, hits), 1):
        for platform, total in denominators.items():
            for i in range(total):
                row = len(rows) + 2
                cid = 0 if i < numerators.get(platform, 0) else -1
                stamp = f"2026-{month:02d}-15T10:00:00" + (
                    ".123000" if platform == "reddit" else ""
                )
                root = (
                    "same"
                    if fixed_topic_root and cid == 0
                    else f"p{month}{platform[0]}{i % 5}"
                )
                url = (
                    f"https://www.reddit.com/comments/{root}/_/c{row}/"
                    if platform == "reddit"
                    else f"https://www.youtube.com/watch?v={root}&lc=c{row}"
                )
                text = (
                    f"Beasiswa membantu biaya kuliah untuk pendidikan nomor {row}."
                    if cid == 0
                    else f"Percakapan di luar topik contoh {row}."
                )
                rows.append(
                    dict(
                        occurrence_id=f"o{row}",
                        sentence_id=f"s{row}",
                        source_row=row,
                        platform=platform,
                        kind="comment",
                        sentence=text,
                        cluster_id=cid,
                        post_title=f"Post {root}",
                        url=url,
                        post_date="2026-01-01T00:00:00"
                        if fixed_topic_root and cid == 0
                        else stamp,
                        content_date=stamp,
                        post_date_accuracy="pasti",
                        content_date_accuracy="pasti",
                    )
                )
    model.occurrences = pd.DataFrame(rows)
    model.sentences = model.occurrences[
        ["sentence_id", "sentence", "cluster_id"]
    ].copy()
    model.sentences["embedding_text"] = model.sentences.sentence
    model.sentences["centroid_similarity"] = np.where(
        model.sentences.cluster_id == 0, 0.9, 0.1
    )
    model.embeddings = np.array(
        [[1, 0] if cid == 0 else [0, 1] for cid in model.sentences.cluster_id],
        dtype=np.float32,
    )
    model.topics = [
        dict(
            cluster_id=0,
            label="beasiswa / biaya / kuliah",
            terms=["beasiswa", "biaya kuliah", "pendidikan", "kuliah"],
        )
    ]
    model.model_info = {"test_encoder": True}
    model.input_sha256 = "a" * 64
    model.source_run_manifest_sha256 = "b" * 64
    return model


def profile(values):
    return model_from_counts(
        [{"reddit": 100} for _ in values], [{"reddit": n} for n in values]
    )


class ExplanationTests(unittest.TestCase):
    def explain(self, model, **kwargs):
        return model.explain_topics(
            date_start="2026-01-01", date_end="2026-06-30", **kwargs
        )

    def test_known_increasing_and_decreasing_shares(self):
        for values, direction, slope, delta in [
            ([10, 20, 30, 40, 50, 60], "rising", 10, 30),
            ([60, 50, 40, 30, 20, 10], "falling", -10, -30),
        ]:
            topic = self.explain(profile(values))["topics"][0]
            self.assertEqual(topic["trend"]["direction"], direction)
            self.assertAlmostEqual(topic["trend"]["slope_pp_per_month"], slope)
            self.assertAlmostEqual(topic["trend"]["comparison"]["delta_pp"], delta)
            self.assertEqual(topic["trend"]["eligible_months"], 6)
            self.assertFalse(topic["trend"]["blockers"])

    def test_stable_and_episodic_patterns(self):
        stable = self.explain(profile([20] * 6))["topics"][0]
        spike = self.explain(profile([20, 20, 80, 20, 20, 20]))["topics"][0]
        self.assertEqual(stable["trend"]["direction"], "stable")
        self.assertEqual(stable["trend"]["slope_pp_per_month"], 0)
        self.assertEqual(spike["trend"]["direction"], "recent_decrease")
        self.assertEqual(spike["trend"]["peak_share_period"], "2026-03")
        self.assertEqual(spike["trend"]["slope_pp_per_month"], 0)

    def test_sentence_repetition_does_not_inflate_comment_trend(self):
        model = profile([10, 20, 30, 40, 50, 60])
        original = self.explain(model)["topics"][0]
        duplicate = pd.concat(
            [model.occurrences, model.occurrences[model.occurrences.cluster_id == 0]]
            * 3,
            ignore_index=True,
        )
        repeated = model.explain_topics(
            duplicate, date_start="2026-01-01", date_end="2026-06-30"
        )["topics"][0]
        self.assertEqual(original["monthly"], repeated["monthly"])
        self.assertEqual(original["trend"], repeated["trend"])
        self.assertEqual(original["comments"], repeated["comments"])
        self.assertGreater(repeated["occurrences"], original["occurrences"])

    def test_missing_month_is_unknown_not_zero_and_calendar_gap_is_preserved(self):
        model = profile([10, 20, 30, 40, 50, 60])
        filtered = model.occurrences[
            ~model.occurrences.post_date.str.startswith("2026-03")
        ]
        result = model.explain_topics(
            filtered, date_start="2026-01-01", date_end="2026-06-30"
        )
        topic = result["topics"][0]
        self.assertIsNone(topic["monthly"][2]["share"])
        self.assertFalse(topic["monthly"][2]["eligible_for_trend"])
        self.assertAlmostEqual(topic["trend"]["slope_pp_per_month"], 10)
        self.assertEqual(topic["trend"]["direction"], "inconclusive")

    def test_partial_edge_month_does_not_drive_slope(self):
        result = profile([10, 20, 30, 40, 50, 60, 100]).explain_topics(
            date_start="2026-01-01", date_end="2026-07-20"
        )
        self.assertEqual(result["partial_months_excluded"], ["2026-07"])
        topic = result["topics"][0]
        self.assertEqual(topic["monthly"][-1]["share"], 1)
        self.assertFalse(topic["monthly"][-1]["eligible_for_trend"])
        self.assertAlmostEqual(topic["trend"]["slope_pp_per_month"], 10)
        self.assertEqual(
            topic["trend"]["comparison"]["recent"]["periods"][-1], "2026-06"
        )

    def test_platform_composition_can_reverse_pooled_direction(self):
        totals = [{"reddit": 80, "youtube": 20}] * 3 + [
            {"reddit": 20, "youtube": 80}
        ] * 3
        hits = [{"reddit": 8, "youtube": 12}] * 3 + [{"reddit": 1, "youtube": 40}] * 3
        topic = self.explain(model_from_counts(totals, hits))["topics"][0]
        comparison = topic["trend"]["comparison"]
        self.assertGreater(comparison["delta_pp"], 0)
        self.assertLess(comparison["platform_standardized_delta_pp"], 0)
        self.assertEqual(topic["trend"]["direction"], "fluctuating")
        self.assertTrue(
            any(
                "komposisi platform dibuat tetap" in c
                for c in topic["trend"]["cautions"]
            )
        )

    def test_single_thread_and_small_sample_are_not_declared_a_trend(self):
        model = model_from_counts(
            [{"reddit": 100}] * 6,
            [{"reddit": n} for n in [10, 20, 30, 40, 50, 60]],
            fixed_topic_root=True,
        )
        topic = self.explain(model, options={"date_basis": "content_date"})["topics"][0]
        self.assertEqual(topic["trend"]["roots"], 1)
        self.assertEqual(topic["trend"]["direction"], "inconclusive")
        self.assertTrue(topic["trend"]["blockers"])
        small = self.explain(
            model_from_counts([{"reddit": 5}] * 6, [{"reddit": 1}] * 6)
        )["topics"][0]
        self.assertEqual(small["trend"]["direction"], "inconclusive")
        self.assertEqual(small["trend"]["eligible_months"], 0)

    def test_extractive_evidence_preserves_source_and_diversifies_roots(self):
        model = profile([20] * 6)
        result = self.explain(model)
        self.assertTrue(result["synthetic"])
        evidence = result["topics"][0]["evidence"]
        self.assertEqual(len(evidence), 3)
        self.assertEqual(len({row["parent_post_key"] for row in evidence}), 3)
        for row in evidence:
            original = model.occurrences[
                model.occurrences.source_row == row["source_row"]
            ].iloc[0]
            self.assertEqual(row["sentence"], original.sentence)
            self.assertEqual(row["url"], original.url)
            self.assertEqual(row["confidence"], "EXTRACTED")
            self.assertTrue(row["matched_terms"])
        json.dumps(result, allow_nan=False)

    def test_parent_keys_separate_native_threads_from_comments(self):
        a = Model.parent_post_key(
            {"platform": "youtube", "url": "https://www.youtube.com/watch?v=abc&lc=one"}
        )
        b = Model.parent_post_key(
            {"platform": "youtube", "url": "https://youtu.be/abc?lc=two"}
        )
        self.assertEqual(a, b)
        a = Model.parent_post_key(
            {
                "platform": "reddit",
                "url": "https://www.reddit.com/r/test/comments/abc/title/one/",
            }
        )
        b = Model.parent_post_key(
            {"platform": "reddit", "url": "https://www.reddit.com/comments/abc/_/two/"}
        )
        self.assertEqual(a, b)
        self.assertEqual(
            Model.parent_post_key(
                {
                    "platform": "reddit",
                    "url": "https://evilreddit.com/comments/abc/",
                    "post_title": "x",
                }
            )[1],
            "context_fallback",
        )

    def test_unknown_dates_estimates_empty_and_invalid_inputs(self):
        model = profile([20] * 6)
        frame = model.occurrences.copy()
        frame.loc[frame.cluster_id == 0, "content_date_accuracy"] = "perkiraan"
        result = model.explain_topics(
            frame,
            date_start="2026-01-01",
            date_end="2026-06-30",
            options={"date_basis": "content_date", "include_estimated_dates": False},
        )
        self.assertEqual(result["topics"][0]["dated_comments"], 0)
        self.assertEqual(result["topics"][0]["trend"]["direction"], "inconclusive")
        empty = model.explain_topics(frame.head(0))
        self.assertEqual(empty["topics"], [])
        bad = frame.copy()
        bad.loc[0, "cluster_id"] = 99
        with self.assertRaises(ValueError):
            self.explain(model, occurrences=bad)
        with self.assertRaises(ValueError):
            self.explain(model, options={"mmr_lambda": float("nan")})
        with self.assertRaises(ValueError):
            model.explain_topics(date_start="2000-01-01", date_end="2026-01-01")
        with self.assertRaises(ValueError):
            model.explain_topics(date_start="2026-07-01", date_end="2026-01-01")

    def test_sidecar_roundtrip_checksum_and_source_binding(self):
        model = profile([20] * 6)
        result = self.explain(model)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "explanation"
            Model.save_explanations(result, output)
            loaded = Model.load_explanations(
                output, expected_source_manifest_sha256="b" * 64
            )
            self.assertEqual(loaded, result)
            with self.assertRaises(FileExistsError):
                Model.save_explanations(result, output)
            with self.assertRaises(ValueError):
                Model.load_explanations(
                    output, expected_source_manifest_sha256="c" * 64
                )
            (output / "topic_explanations.json").write_text("{}")
            with self.assertRaises(ValueError):
                Model.load_explanations(output)

    def test_saved_artifact_explanations_never_encode_or_train(self):
        model = profile([20] * 6)
        data = dict(
            topics=model.topics,
            sentences=model.sentences,
            occurrences=model.occurrences,
            embeddings=model.embeddings,
            summary={
                "config": model.config,
                "source_sha256": model.input_sha256,
                "synthetic": True,
            },
            artifact_manifest_sha256="b" * 64,
        )
        with (
            patch.object(
                Model, "encode", side_effect=AssertionError("must not encode")
            ),
            patch.object(
                Model, "fit_excel", side_effect=AssertionError("must not train")
            ),
        ):
            result = Model.explain_artifacts(
                data, date_start="2026-01-01", date_end="2026-06-30"
            )
        self.assertEqual(result["source_run_manifest_sha256"], "b" * 64)
        self.assertEqual(result["topics"][0]["trend"]["direction"], "stable")


if __name__ == "__main__":
    unittest.main()
