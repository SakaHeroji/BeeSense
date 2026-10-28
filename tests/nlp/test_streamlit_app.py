from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from streamlit.testing.v1 import AppTest
from test_social_nlp import encoder, fixture

from social_nlp import ROOT, SocialNLPClusterer


class StreamlitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root = Path(cls.temp.name)
        source = root / "source.xlsx"
        fixture(source, duplicate=True)
        pipeline = (
            SocialNLPClusterer({"cache_dir": str(root / "cache")}, encoder=encoder)
            .prepare_excel(source)
            .encode()
        )
        labels = np.repeat([0, 1, 2], 12)
        labels[-1] = -1
        pipeline.sentences["cluster_id"] = labels
        pipeline.sentences["membership_strength"] = np.nan
        pipeline.sentences["embedding_windows"] = 1
        pipeline.occurrences = pipeline.occurrences.merge(
            pipeline.sentences[["sentence_id", "cluster_id"]],
            on="sentence_id",
            validate="many_to_one",
        )
        pipeline.reduced_embeddings = [
            pipeline.embeddings[:, :2].copy(),
            pipeline.embeddings[:, :2].copy(),
        ]
        pipeline.reduction_info = {
            "algorithm": "UMAP",
            "synthetic_fixture": True,
            "seeds": [42, 43],
        }
        pipeline.evaluation_indices = np.arange(36)
        pipeline.selected = pipeline._evaluate(
            "synthetic_dbscan_groups",
            labels,
            labels,
            {
                "algorithm": "DBSCAN",
                "eps": 0.08,
                "min_samples": 3,
                "metric": "euclidean",
            },
            0,
        )
        pipeline.selection_policy = {"score_tolerance": 0.005}
        pipeline.describe_topics()
        pipeline.fit_seconds = 0
        cls.output = pipeline.save(root / "result")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        # Keep both guards active across every AppTest rerun.
        self.environment = patch.dict(
            os.environ, {"BEESENSE_NLP_RUN_DIR": str(self.output)}
        )
        self.training = patch.object(
            SocialNLPClusterer,
            "fit_excel",
            side_effect=AssertionError("UI must not train"),
        )
        self.environment.start()
        self.training.start()

    def tearDown(self):
        self.training.stop()
        self.environment.stop()

    def app(self, query=None):
        app = AppTest.from_file(str(ROOT / "nlp_dashboard.py"), default_timeout=30)
        if query:
            app.query_params.update(query)
        return app.run()

    def test_dashboard_renders_and_topic_selection_works_without_training(self):
        app = self.app()
        self.assertFalse(app.exception)
        self.assertEqual(app.title[0].value, "Percakapan YouTube & Reddit")
        self.assertTrue(any("SBERT" in caption.value for caption in app.caption))
        self.assertEqual(
            app.radio(key="view").options,
            [
                "Ringkasan",
                "Peta topik",
                "Penjelasan topik",
                "Kalimat & sumber",
                "Metode & data",
            ],
        )
        app.radio(key="view").set_value("Kalimat & sumber").run()
        frames = [
            item.value for item in app.dataframe if "platform" in item.value.columns
        ]
        self.assertEqual(set(frames[0]["platform"]), {"reddit", "youtube"})
        self.assertEqual(len(frames[0]), 37)
        choice = next(
            value
            for value in app.selectbox(key="topic_select").options
            if value.startswith("T01 ·")
        )
        app.selectbox(key="topic_select").set_value(choice).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("kalimat unik" in item.value for item in app.markdown))

    def test_search_empty_state_and_platform_filter(self):
        app = self.app()
        app.radio(key="view").set_value("Kalimat & sumber").run()
        app.multiselect(key="platforms").set_value(["Reddit"]).run()
        self.assertFalse(app.exception)
        frames = [
            item.value for item in app.dataframe if "platform" in item.value.columns
        ]
        self.assertTrue(frames)
        self.assertEqual(set(frames[0]["platform"]), {"reddit"})
        app.text_input(key="query").set_value("__no_sentence_can_match_this__").run()
        self.assertFalse(app.exception)
        self.assertIn("Tidak ada kalimat", app.info[0].value)

    def test_coherence_metric_and_per_topic_scores_are_visible(self):
        app = self.app({"view": "Metode & data"})
        self.assertFalse(app.exception)
        self.assertTrue(any(metric.label == "Coherence c_v" for metric in app.metric))
        self.assertTrue(
            any("berada di bawah target" in item.value for item in app.markdown)
        )
        self.assertTrue(any("c_v" in item.value.columns for item in app.dataframe))

    def test_url_initializes_filters_and_reset_clears_state(self):
        # AppTest has no browser to write bound query parameters. Seed the
        # same URL representation; real-browser QA covers updates/reload.
        copied = {
            "view": "Peta topik",
            "platforms": ["Reddit"],
            "query": "Beasiswa",
            "post_dates": ["2026-10-01", "2026-10-01"],
        }
        restored = self.app(query=copied)
        self.assertFalse(restored.exception)
        self.assertEqual(restored.text_input(key="query").value, "Beasiswa")
        self.assertEqual(restored.multiselect(key="platforms").value, ["Reddit"])
        self.assertEqual(restored.radio(key="view").value, "Peta topik")
        restored.button[0].click().run()
        self.assertFalse(restored.exception)
        self.assertEqual(restored.text_input(key="query").value, "")
        self.assertEqual(
            set(restored.multiselect(key="platforms").value), {"YouTube", "Reddit"}
        )

    def test_all_views_and_noise_only_selection(self):
        app = self.app()
        for view in [
            "Peta topik",
            "Penjelasan topik",
            "Metode & data",
            "Kalimat & sumber",
            "Ringkasan",
        ]:
            app.radio(key="view").set_value(view).run()
            self.assertFalse(app.exception, view)
        app.text_input(key="query").set_value("perangkat contoh nomor 11.").run()
        app.radio(key="view").set_value("Peta topik").run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Belum ada topik" in item.value for item in app.info))
        app.radio(key="view").set_value("Kalimat & sumber").run()
        app.selectbox(key="topic_select").set_value("Belum terkelompok").run()
        self.assertFalse(app.exception)
        table = next(
            item.value for item in app.dataframe if "platform" in item.value.columns
        )
        self.assertEqual(len(table), 1)
        self.assertEqual(set(table["topic"]), {"Belum terkelompok"})

    def test_explanation_detail_and_filtered_download_without_training(self):
        app = self.app()
        app.radio(key="view").set_value("Penjelasan topik").run()
        self.assertFalse(app.exception)
        table = next(
            item.value for item in app.dataframe if "Pola teramati" in item.value
        )
        self.assertEqual(len(table), 3)
        choice = next(
            value
            for value in app.selectbox(key="topic_select").options
            if value.startswith("T01 ·")
        )
        app.selectbox(key="topic_select").set_value(choice).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Cuplikan penjelas" in item.value for item in app.markdown))
        self.assertTrue(
            any("Arah belum cukup jelas" in item.value for item in app.subheader)
        )
        self.assertTrue(
            any("Mengapa penjelasan ini muncul?" == item.label for item in app.expander)
        )
        app.multiselect(key="platforms").set_value(["Reddit"]).run()
        self.assertFalse(app.exception)
        # The download and source cards remain available after platform reruns;
        # the fixture's single month must never acquire an invented direction.
        self.assertTrue(
            any("Arah belum cukup jelas" in item.value for item in app.subheader)
        )
        self.assertTrue(
            any("Unduh penjelasan" in item.label for item in app.get("download_button"))
        )

    def test_network_limit_tracks_filter_bounds_and_preserves_valid_choices(self):
        app = self.app(query={"view": "Peta topik"})
        self.assertFalse(app.exception)
        self.assertEqual(app.slider(key="node_limit").value, 3)

        # This search leaves two clusters: the third group's final sentence
        # is noise. The previous limit of three must fit the new maximum.
        app.text_input(key="query").set_value("nomor 11.").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.slider(key="node_limit").max, 2)
        self.assertEqual(app.slider(key="node_limit").value, 2)

        app.text_input(key="query").set_value("").run()
        app.slider(key="node_limit").set_value(1).run()
        app.text_input(key="query").set_value("nomor 11.").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.slider(key="node_limit").value, 1)

        # A one-topic result and an empty result temporarily hide the slider.
        # Page-persisted state must also be safe when it is shown again.
        app.text_input(key="query").set_value("Beasiswa").run()
        self.assertFalse(app.exception)
        self.assertFalse(any(item.key == "node_limit" for item in app.slider))
        app.text_input(key="query").set_value("__no_match__").run()
        self.assertFalse(app.exception)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.slider(key="node_limit").max, 3)
        self.assertGreaterEqual(app.slider(key="node_limit").value, 1)
        self.assertLessEqual(app.slider(key="node_limit").value, 3)
        app.radio(key="view").set_value("Ringkasan").run()
        app.radio(key="view").set_value("Peta topik").run()
        self.assertFalse(app.exception)

    def test_network_url_limits_are_safe_on_initial_filtered_load(self):
        for limit in ["51", "0", "invalid"]:
            with self.subTest(limit=limit):
                app = self.app(
                    query={
                        "view": "Peta topik",
                        "query": "nomor 11.",
                        "node_limit": limit,
                    }
                )
                self.assertFalse(app.exception)
                self.assertEqual(app.slider(key="node_limit").max, 2)
                self.assertIn(app.slider(key="node_limit").value, [1, 2])


if __name__ == "__main__":
    unittest.main()
