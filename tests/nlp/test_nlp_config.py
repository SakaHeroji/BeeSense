"""Configuration consolidation without fitting, model downloads or API requests."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from MachineLearning.social_nlp import ROOT, SocialNLPClusterer, main
from scripts import relevance_dashboard


class NLPConfigTests(unittest.TestCase):
    def test_default_and_primary_path_load_configuration_once(self):
        primary = ROOT / "config/social_nlp.json"
        original = Path.read_text
        for supplied in (None, primary, "config/social_nlp.json"):
            with (
                self.subTest(config=supplied),
                patch.object(
                    Path, "read_text", autospec=True, side_effect=original
                ) as read,
            ):
                cfg = SocialNLPClusterer(supplied).config
                self.assertEqual(read.call_count, 1)
                self.assertEqual(cfg, json.loads(original(primary)))

    def test_partial_overrides_preserve_siblings_and_do_not_mutate_input(self):
        base = SocialNLPClusterer().config
        supplied = {"model": {"batch_size": 8}, "coherence": {"min_score": 0.5}}
        before = deepcopy(supplied)
        cfg = SocialNLPClusterer(supplied).config
        self.assertEqual(cfg["model"], {**base["model"], "batch_size": 8})
        self.assertEqual(cfg["coherence"], {**base["coherence"], "min_score": 0.5})
        self.assertIsNone(cfg["relevance_artifact"])
        cfg["model"]["batch_size"] = 16
        self.assertEqual(supplied, before)
        self.assertEqual(SocialNLPClusterer().config, base)

    def test_custom_file_remains_a_partial_override_with_explicit_mask(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "custom.json"
            path.write_text(
                json.dumps({"relevance_artifact": "outputs/custom-mask", "seed": 7})
            )
            cfg = SocialNLPClusterer(path).config
            self.assertEqual(cfg["seed"], 7)
            self.assertEqual(cfg["relevance_artifact"], "outputs/custom-mask")
            self.assertEqual(
                cfg["target_topics"], SocialNLPClusterer().config["target_topics"]
            )

    def test_falsey_non_objects_and_unknown_settings_are_rejected(self):
        for value in (False, 0, [], {"unknown": 1}, {"model": {"unknown": 1}}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                SocialNLPClusterer(value)

    def test_explanation_validation_does_not_reread_the_editable_file(self):
        options = SocialNLPClusterer().config["explanation"]
        with patch.object(
            Path, "read_text", side_effect=AssertionError("unexpected file read")
        ):
            SocialNLPClusterer._validate_explanation_options(options)
            for invalid in ({**options, "unknown": 1}, {}, []):
                with self.subTest(options=invalid), self.assertRaises(ValueError):
                    SocialNLPClusterer._validate_explanation_options(invalid)

    def test_dry_run_shows_effective_paths_without_loading_data_or_fitting(self):
        stdout = io.StringIO()
        with (
            patch.object(
                sys,
                "argv",
                [
                    "nlp",
                    "--dry-run",
                    "--input",
                    "new.xlsx",
                    "--output-dir",
                    "outputs/new",
                ],
            ),
            patch.object(
                SocialNLPClusterer,
                "prepare_excel",
                side_effect=AssertionError("data read"),
            ),
            patch.object(
                SocialNLPClusterer, "fit_excel", side_effect=AssertionError("training")
            ),
            redirect_stdout(stdout),
        ):
            self.assertEqual(main(), 0)
        data = json.loads(stdout.getvalue())
        self.assertEqual(data["status"], "CONFIG_VALID")
        self.assertEqual(data["config"]["input_file"], "new.xlsx")
        self.assertEqual(data["config"]["output_dir"], "outputs/new")

    def test_dashboard_launcher_reads_the_single_primary_file(self):
        active = SocialNLPClusterer().config
        with (
            patch.object(sys, "argv", ["relevance_dashboard"]),
            patch.object(SocialNLPClusterer, "load_run") as load,
            patch.object(relevance_dashboard.os, "execvpe") as launch,
        ):
            relevance_dashboard.main()
        self.assertEqual(load.call_args_list[0].args[0], ROOT / active["output_dir"])
        env = launch.call_args.args[2]
        self.assertEqual(
            env["BEESENSE_NLP_RUN_DIR"], str((ROOT / active["output_dir"]).resolve())
        )

    def test_dashboard_launcher_follows_new_snapshot_pair_and_drops_stale_comparison(
        self,
    ):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "config").mkdir()
            primary = root / "config/social_nlp.json"
            (root / "config/dashboard.json").write_text(
                json.dumps(
                    {
                        "snapshot_comparison": {
                            "after": "outputs/new_after",
                            "before": "outputs/new_before",
                        }
                    }
                )
            )
            cases = [
                ("outputs/new_after", [], "outputs/new_after", "outputs/new_before"),
                ("outputs/new_after", ["--baseline"], "outputs/new_before", None),
                ("outputs/custom", [], "outputs/custom", None),
            ]
            for configured, flags, expected, comparison in cases:
                primary.write_text(json.dumps({"output_dir": configured}))
                with (
                    self.subTest(configured=configured, flags=flags),
                    patch.object(relevance_dashboard, "ROOT", root),
                    patch.object(sys, "argv", ["relevance_dashboard", *flags]),
                    patch.object(SocialNLPClusterer, "load_run") as load,
                    patch.object(relevance_dashboard.os, "execvpe") as launch,
                    patch.dict(
                        relevance_dashboard.os.environ,
                        {"BEESENSE_BASELINE_RUN_DIR": "outputs/stale"},
                    ),
                ):
                    relevance_dashboard.main()
                    self.assertEqual(load.call_args_list[0].args[0], root / expected)
                    env = launch.call_args.args[2]
                    self.assertEqual(
                        env["BEESENSE_NLP_RUN_DIR"], str((root / expected).resolve())
                    )
                    if comparison:
                        self.assertEqual(
                            env["BEESENSE_BASELINE_RUN_DIR"],
                            str((root / comparison).resolve()),
                        )
                    else:
                        self.assertNotIn("BEESENSE_BASELINE_RUN_DIR", env)
