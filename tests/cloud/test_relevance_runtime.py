"""Verify the published relevance comparison in the minimal Cloud runtime."""

import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from MachineLearning import topic_narratives
from MachineLearning.social_nlp import ROOT, SocialNLPClusterer


@unittest.skipUnless(
    os.environ.get("BEESENSE_RELEVANCE_RUN_DIR"),
    "Versioned relevance snapshot is opt-in",
)
class RelevanceRuntimeTests(unittest.TestCase):
    def test_filtered_dashboard_all_views_and_baseline_switch(self):
        for name in ("torch", "sentence_transformers", "gensim", "umap"):
            self.assertIsNone(importlib.util.find_spec(name), name + " installed")
        run = Path(os.environ["BEESENSE_RELEVANCE_RUN_DIR"])
        data = SocialNLPClusterer.load_run(run)
        comparison = json.loads((ROOT / "config/dashboard.json").read_text())[
            "snapshot_comparison"
        ]
        self.assertEqual(run.resolve(), (ROOT / comparison["after"]).resolve())
        baseline = SocialNLPClusterer.load_run(ROOT / comparison["before"])
        before_score = f"{baseline['summary']['coherence']['macro_mean']:.4f}".replace(
            ".", ","
        )
        after_score = f"{data['summary']['coherence']['macro_mean']:.4f}".replace(
            ".", ","
        )
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
                {},
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
            # Reproduce Community Cloud: no local launcher or environment setup.
            os.environ.pop("BEESENSE_NLP_RUN_DIR", None)
            os.environ.pop("BEESENSE_BASELINE_RUN_DIR", None)
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
            self.assertTrue(any(before_score in item.value for item in app.caption))
            app.radio(key="snapshot_comparison").set_value("Setelah penyaringan").run()
            self.assertFalse(app.exception)
            self.assertTrue(any(after_score in item.value for item in app.caption))
        self.assertNotIn("torch", sys.modules)


if __name__ == "__main__":
    unittest.main()
