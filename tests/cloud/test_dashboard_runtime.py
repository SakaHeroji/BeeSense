"""Run in an isolated Cloud environment, using only root requirements.txt."""

from __future__ import annotations

import html
import importlib.util
import json
import os
import sys
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from MachineLearning import topic_narratives
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
    def test_tiktok_origin_chart_shows_saved_post_captions(self):
        config = json.loads((ROOT / "config/social_nlp.json").read_text())
        directory = (
            os.environ.get("BEESENSE_NLP_RUN_DIR") or ROOT / config["output_dir"]
        )
        saved = SocialNLPClusterer.load_run(directory)
        source = saved.get("social_data")
        if source is None or "tiktok" not in set(source.platform):
            self.skipTest("Snapshot has no TikTok source posts")
        posts = source[(source.platform == "tiktok") & (source.jenis == "post")]
        expected = {
            html.escape(value.strip())
            for column in ("teks", "judul_post")
            for value in posts[column]
            if isinstance(value, str) and value.strip()
        }
        counts = saved["occurrences"].query("platform == 'tiktok' and cluster_id >= 0")
        topic_id = int(counts.groupby("cluster_id").size().idxmax())
        with (
            patch.object(
                topic_narratives,
                "request_topic",
                side_effect=AssertionError("UI must not call Gemini"),
            ),
            patch.object(
                SocialNLPClusterer,
                "fit_excel",
                side_effect=AssertionError("UI must not train"),
            ),
        ):
            app = AppTest.from_file(
                str(ROOT / "streamlit_apps.py"), default_timeout=120
            ).run()
            app.multiselect(key="platforms").set_value(["TikTok"]).run()
            option = next(
                value
                for value in app.selectbox(key="topic_select").options
                if value.startswith(f"T{topic_id + 1:02d}")
            )
            app.selectbox(key="topic_select").set_value(option).run()
            app.radio(key="view").set_value("Penjelasan topik").run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            figures = [
                json.loads(chart.proto.spec) for chart in app.get("plotly_chart")
            ]
            figure = next(
                chart
                for chart in figures
                if chart["layout"].get("xaxis", {}).get("title", {}).get("text")
                == "Komentar topik per post asal"
            )
            labels = [row[0] for row in figure["data"][0]["customdata"]]
            self.assertTrue(labels)
            self.assertTrue(set(labels) <= expected)
            self.assertNotIn("Judul tidak tersedia", labels)

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
        if config.get("gemini", {}).get("enabled"):
            self.assertEqual(len(saved["topic_narratives"]), 20)
        with (
            patch.object(
                topic_narratives,
                "request_topic",
                side_effect=AssertionError("Cloud dashboard must not call Gemini"),
            ),
            patch.object(
                SocialNLPClusterer,
                "fit_excel",
                side_effect=AssertionError("Cloud dashboard must not train"),
            ),
        ):
            app = AppTest.from_file(
                str(ROOT / "streamlit_apps.py"), default_timeout=120
            ).run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            labels = [
                label
                for key, label in {
                    "youtube": "YouTube",
                    "reddit": "Reddit",
                    "instagram": "Instagram",
                    "twitter": "X / Twitter",
                    "tiktok": "TikTok",
                }.items()
                if key in set(saved["occurrences"].platform)
            ]
            expected_title = "Percakapan " + (
                " & ".join(labels)
                if len(labels) < 3
                else ", ".join(labels[:-1]) + " & " + labels[-1]
            )
            self.assertEqual(app.title[0].value, expected_title)
            if saved.get("topic_narratives"):
                self.assertIn(
                    "Kalimat dan deskripsi 20 topik · Gemini",
                    [item.label for item in app.expander],
                )
                self.assertIn(
                    "Unduh CSV topik Gemini",
                    [item.label for item in app.get("download_button")],
                )
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
                    if view == "Penjelasan topik" and saved.get("topic_narratives"):
                        narrative = next(
                            row
                            for row in saved["topic_narratives"]
                            if row["cluster_id"] == 3
                        )
                        self.assertIn(
                            narrative["topic_sentence"],
                            [item.value for item in app.subheader],
                        )
                    if view == "Kalimat & sumber" and saved.get("topic_sentences_xlsx"):
                        self.assertIn(
                            "Unduh Excel topik dan kalimat",
                            [item.label for item in app.get("download_button")],
                        )
            for platform, label in [("twitter", "X / Twitter"), ("tiktok", "TikTok")]:
                if platform in set(saved["occurrences"].platform):
                    app.multiselect(key="platforms").set_value([label]).run()
                    for view in app.radio(key="view").options:
                        with self.subTest(platform=platform, view=view):
                            app.radio(key="view").set_value(view).run()
                            self.assertFalse(app.exception)
                            self.assertFalse(app.error)
        for name in TRAINING_MODULES:
            self.assertNotIn(name, sys.modules, name + " imported")


if __name__ == "__main__":
    unittest.main()
