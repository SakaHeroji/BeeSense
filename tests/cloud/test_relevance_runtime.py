"""Opt-in verification of an unpublished local relevance experiment."""

import importlib.util
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from MachineLearning import topic_narratives
from MachineLearning.social_nlp import ROOT, SocialNLPClusterer


@unittest.skipUnless(
    os.environ.get("BEESENSE_RELEVANCE_RUN_DIR"), "Local experiment snapshot is opt-in"
)
class RelevanceRuntimeTests(unittest.TestCase):
    def test_filtered_dashboard_all_views_and_baseline_switch(self):
        for name in ("torch", "sentence_transformers", "gensim", "umap"):
            self.assertIsNone(importlib.util.find_spec(name), name + " installed")
        run = Path(os.environ["BEESENSE_RELEVANCE_RUN_DIR"])
        baseline = ROOT / "outputs/nlp_20261102_twitter_topics20_gemini_01"
        data = SocialNLPClusterer.load_run(run)
        self.assertEqual(len(data["topics"]), 20)
        self.assertEqual(len(data["topic_narratives"]), 20)
        self.assertTrue(data["summary"]["topic_narratives"]["clustering_unchanged"])
        self.assertGreaterEqual(data["summary"]["coherence"]["macro_mean"], 0.4)
        self.assertEqual(
            set(data["occurrences"].occurrence_id),
            set(
                data["relevance_decisions"]
                .query("decision == 'relevant'")
                .occurrence_id
            ),
        )
        with (
            patch.dict(
                os.environ,
                {
                    "BEESENSE_NLP_RUN_DIR": str(run),
                    "BEESENSE_BASELINE_RUN_DIR": str(baseline),
                },
            ),
            patch.object(
                topic_narratives,
                "request_topic",
                side_effect=AssertionError("No external API in local preview"),
            ),
            patch.object(
                SocialNLPClusterer,
                "fit_excel",
                side_effect=AssertionError("No training on rerun"),
            ),
        ):
            app = AppTest.from_file(
                str(ROOT / "streamlit_apps.py"), default_timeout=120
            ).run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertTrue(any("Model eksperimen" in item.value for item in app.info))
            self.assertIn(
                "Kalimat dan deskripsi 20 topik · Gemini",
                [item.label for item in app.expander],
            )
            for view in app.radio(key="view").options:
                with self.subTest(view=view):
                    app.radio(key="view").set_value(view).run()
                    self.assertFalse(app.exception)
                    self.assertFalse(app.error)
            self.assertIn(
                "Unduh audit relevansi CSV",
                [x.label for x in app.get("download_button")],
            )
            app.radio(key="snapshot_comparison").set_value("Sebelum penyaringan").run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertFalse(any("Model eksperimen" in item.value for item in app.info))
            self.assertTrue(any("0,4243" in item.value for item in app.caption))
            app.radio(key="snapshot_comparison").set_value("Setelah penyaringan").run()
            self.assertFalse(app.exception)
            self.assertTrue(any("0,4733" in item.value for item in app.caption))
        self.assertNotIn("torch", sys.modules)


if __name__ == "__main__":
    unittest.main()
