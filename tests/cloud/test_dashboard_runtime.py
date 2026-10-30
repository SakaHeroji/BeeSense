"""Run in an isolated Cloud environment, using only root requirements.txt."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from MachineLearning.social_nlp import ROOT, SocialNLPClusterer

TRAINING_MODULES = (
    "onnxruntime",
    "numba",
    "llvmlite",
    "umap",
    "torch",
    "sentence_transformers",
    "gensim",
    "yt_dlp",
)


class CloudRuntimeTests(unittest.TestCase):
    def test_shipped_dashboard_and_explanations_need_no_training_environment(self):
        for name in TRAINING_MODULES:
            self.assertIsNone(importlib.util.find_spec(name), name + " installed")
        config = json.loads((ROOT / "config/social_nlp.json").read_text())
        directory = (
            os.environ.get("BEESENSE_NLP_RUN_DIR") or ROOT / config["output_dir"]
        )
        saved = SocialNLPClusterer.load_run(directory)
        self.assertEqual(len(saved["topics"]), config["target_topics"])
        self.assertGreaterEqual(
            saved["summary"]["coherence"]["macro_mean"],
            config["coherence"]["min_score"],
        )
        with patch.object(
            SocialNLPClusterer,
            "fit_excel",
            side_effect=AssertionError("Cloud dashboard must not train"),
        ):
            app = AppTest.from_file(
                str(ROOT / "streamlit_apps.py"), default_timeout=120
            ).run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertEqual(app.title[0].value, "Percakapan YouTube & Reddit")
            topic = next(
                x
                for x in app.selectbox(key="topic_select").options
                if x.startswith("T04")
            )
            app.selectbox(key="topic_select").set_value(topic).run()
            for view in app.radio(key="view").options:
                with self.subTest(view=view):
                    app.radio(key="view").set_value(view).run()
                    self.assertFalse(app.exception)
                    self.assertFalse(app.error)
        for name in TRAINING_MODULES:
            self.assertNotIn(name, sys.modules, name + " imported")


if __name__ == "__main__":
    unittest.main()
