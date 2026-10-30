from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from streamlit_apps import SocialNLPStreamlitApp as App
from streamlit_apps import number, percent


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        # One repeated sentence, one multi-sentence comment, two noise rows,
        # and mixed timestamp precision exercise the counting boundaries.
        self.frame = pd.DataFrame(
            [
                (0, "youtube", "a", 2, "2026-01-02T10:00:00"),
                (0, "youtube", "a", 3, "2026-01-02T10:00:00"),
                (0, "reddit", "b", 4, "2026-01-03T10:00:00.123000"),
                (1, "reddit", "c", 4, "2026-03-03T10:00:00.123000"),
                (-1, "reddit", "d", 5, "2026-03-03T10:00:00.123000"),
                (-1, "youtube", "e", 6, "2026-03-03T10:00:00"),
            ],
            columns=[
                "cluster_id",
                "platform",
                "sentence_id",
                "source_row",
                "post_date",
            ],
        )
        self.topics = [
            {"cluster_id": 0, "label": "Biaya / kuliah"},
            {"cluster_id": 1, "label": "Karier / kerja"},
        ]

    def test_topic_counts_keep_occurrences_unique_sentences_and_comments_separate(self):
        table = App.topic_summary(self.topics, self.frame)
        first = table.iloc[0]
        self.assertEqual((first.total, first["unique"], first.comments), (3, 2, 3))
        self.assertEqual((first.youtube, first.reddit), (2, 1))
        self.assertEqual(first.share, 0.5)  # Denominator includes noise.
        self.assertEqual(int(table.total.sum()), 4)
        self.assertNotIn(-1, table.cluster_id.tolist())

    def test_platform_coverage_includes_noise_and_preserves_zero_platforms(self):
        table = App.platform_summary(self.frame).set_index("platform")
        self.assertEqual(int(table.total.sum()), len(self.frame))
        self.assertEqual(int(table.assigned.sum()), 4)
        self.assertEqual(int(table.noise.sum()), 2)
        self.assertAlmostEqual(table.loc["youtube", "coverage"], 2 / 3)
        only = App.platform_summary(
            self.frame[self.frame.platform == "reddit"]
        ).set_index("platform")
        self.assertEqual(only.loc["youtube", "total"], 0)
        self.assertEqual(only.loc["youtube", "coverage"], 0)

    def test_months_use_root_dates_and_zero_fill_without_losing_microseconds(self):
        table = App.monthly_summary(self.frame)
        self.assertEqual(table.month.dt.month.tolist(), [1, 2, 3])
        self.assertEqual((table.youtube + table.reddit).tolist(), [3, 0, 3])
        self.assertEqual(
            int(table[["youtube", "reddit"]].to_numpy().sum()), len(self.frame)
        )

    def test_bar_data_matches_aggregates_and_escapes_topic_hover_text(self):
        table = App.topic_summary(self.topics, self.frame)
        table.loc[0, "label"] = "<script>kalimat</script>"
        figure = App.ranking_figure(table)
        self.assertEqual(sum(figure.data[0].x) + sum(figure.data[1].x), 4)
        self.assertIn("&lt;script&gt;", figure.data[0].customdata[-1][1])
        self.assertEqual(
            App.coverage_figure(App.platform_summary(self.frame)).layout.barmode,
            "stack",
        )

    def test_network_positions_stable_and_platform_ratio_is_numeric(self):
        graph = {"edges": [{"source": "0", "target": "1", "similarity": 0.7}]}
        first, _ = App.topic_figure(self.topics, graph, self.frame, 0.55)
        second, _ = App.topic_figure(
            self.topics, graph, self.frame[self.frame.platform == "reddit"], 0.8
        )
        points = {
            int(cid[0]): (x, y)
            for cid, x, y in zip(
                first.data[-1].customdata, first.data[-1].x, first.data[-1].y
            )
        }
        for cid, x, y in zip(
            second.data[-1].customdata, second.data[-1].x, second.data[-1].y
        ):
            np.testing.assert_allclose(points[int(cid[0])], [x, y])
        self.assertAlmostEqual(first.data[-1].marker.color[0], 2 / 3)
        self.assertEqual(list(second.data[-1].marker.color), [0, 0])

    def test_chart_events_ignore_non_topic_points_and_support_cluster_zero(self):
        self.assertEqual(
            App.selected_cluster(
                {"selection": {"points": [{"x": 2}, {"customdata": [0, "label"]}]}}, {0}
            ),
            0,
        )
        self.assertIsNone(
            App.selected_cluster(
                {"selection": {"points": [{"customdata": [999]}]}}, {0}
            )
        )
        self.assertIsNone(
            App.selected_cluster(
                {"selection": {"points": [{"customdata": ["bad"]}]}}, {0}
            )
        )

    def test_indonesian_numbers_dates_and_empty_aggregates(self):
        self.assertEqual(number(16178), "16.178")
        self.assertEqual(percent(0.5333), "53,3%")
        self.assertIn("Okt", App._human_date("2026-10-28T12:34:00"))
        self.assertTrue(
            App._human_date("2026-10-28T00:00:00", True).endswith("(perkiraan)")
        )
        self.assertEqual(App._human_date("bad"), "Tidak diketahui")
        empty = self.frame.head(0)
        self.assertTrue(App.topic_summary(self.topics, empty).empty)
        self.assertTrue(App.monthly_summary(empty).empty)

    def test_topic_evidence_profile_deduplicates_units_and_matches_whole_terms(self):
        frame = self.frame.copy()
        frame["sentence"] = [
            "Biaya kuliah",
            "Biaya kuliah",
            "Kuliah gratis",
            "Kerja",
            "Lain",
            "Lain",
        ]
        frame["url"] = [
            "https://www.youtube.com/watch?v=AAAAAAAAAAA&lc=a",
            "https://www.youtube.com/watch?v=AAAAAAAAAAA&lc=b",
            "https://www.reddit.com/comments/abc/_/c/",
            "https://www.reddit.com/comments/abc/_/c/",
            "https://www.reddit.com/comments/def/_/d/",
            "https://www.youtube.com/watch?v=BBBBBBBBBBB&lc=e",
        ]
        frame["post_title"] = "Judul sama"
        result = App.topic_profile(frame, 0, ["kuliah", "biaya kuliah", "kuli"])
        self.assertEqual(
            (result["occurrences"], result["unique_sentences"], result["comments"]),
            (3, 2, 3),
        )
        self.assertEqual(result["comment_share"], 3 / 5)
        self.assertEqual((result["roots"], result["fallback_roots"]), (2, 0))
        self.assertEqual(result["platforms"], {"youtube": 2, "reddit": 1})
        self.assertEqual(result["terms"].sentences.tolist(), [2, 1, 0])
        self.assertEqual(result["sources"].comments.tolist(), [2, 1])
        self.assertAlmostEqual(result["dominant_share"], 2 / 3)
        self.assertEqual(list(App.term_figure(result["terms"]).data[0].x), [0, 1, 2])
        # Different native posts with the same title must occupy separate bars.
        figure = App.source_figure(result["sources"])
        self.assertEqual(len(set(figure.data[0].y)), 2)
        self.assertEqual(sum(figure.data[0].x), 3)
        self.assertEqual(
            sum(App.topic_platform_figure(result["platforms"]).data[0].x), 3
        )

    def test_topic_profile_marks_context_fallback_without_inventing_native_ids(self):
        frame = self.frame.copy()
        frame["sentence"] = "Kuliah"
        frame["post_title"] = "Judul tanpa URL"
        frame["url"] = ""
        result = App.topic_profile(frame, 0, ["kuliah"])
        self.assertGreater(result["fallback_roots"], 0)
        empty = App.topic_profile(frame.head(0), 0, ["kuliah"])
        self.assertEqual(
            (empty["comments"], empty["roots"], empty["comment_share"]), (0, 0, 0)
        )


if __name__ == "__main__":
    unittest.main()
