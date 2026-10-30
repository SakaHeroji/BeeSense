import copy
import unittest

import pandas as pd

from scripts.topic_sentence_export import HEADERS, export_payload


class TopicSentenceExportTests(unittest.TestCase):
    def data(self):
        return {
            "topics": [
                {"cluster_id": 0, "label": "beasiswa", "coherence_cv": 0.5},
                {"cluster_id": 1, "label": "karier", "coherence_cv": 0.4},
            ],
            "occurrences": pd.DataFrame(
                [
                    [0, "Beasiswa membantu!", 2, 0],
                    [0, "Beasiswa membantu!", 3, 0],
                    [0, "beasiswa membantu!", 4, 0],
                    [1, "Karier setelah kuliah.", 5, 0],
                    [-1, "Noise tetap dilaporkan.", 6, 0],
                ],
                columns=["cluster_id", "sentence", "source_row", "span_start"],
            ),
            "summary": {
                "source_sha256": "source digest",
                "coherence": {"macro_mean": 0.45, "min_score": 0.4},
                "config": {"input_file": "outputs/source/social_data.xlsx"},
            },
        }

    def test_export_preserves_original_variants_and_excludes_noise(self):
        result = export_payload(self.data())
        self.assertEqual(result["headers"], list(HEADERS))
        self.assertEqual(len(result["rows"]), 3)
        self.assertEqual(
            [row[1] for row in result["rows"]],
            ["Beasiswa membantu!", "beasiswa membantu!", "Karier setelah kuliah."],
        )
        self.assertEqual([row["sentences"] for row in result["topics"]], [2, 1])
        self.assertEqual(result["noise_occurrences"], 1)
        self.assertEqual(result["macro_coherence"], 0.45)

    def test_unknown_or_empty_topic_membership_is_rejected(self):
        data = self.data()
        original = copy.deepcopy(data["topics"])
        data["topics"] = original[:1]
        with self.assertRaisesRegex(ValueError, "every fitted topic"):
            export_payload(data)
        data["topics"] = original + [
            {"cluster_id": 2, "label": "kosong", "coherence_cv": 0.3}
        ]
        with self.assertRaisesRegex(ValueError, "every fitted topic"):
            export_payload(data)


if __name__ == "__main__":
    unittest.main()
