"""Start the local relevance experiment, or its preserved baseline snapshot."""

import argparse
import json
import os
import sys
from pathlib import Path

from MachineLearning.social_nlp import ROOT, SocialNLPClusterer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline", action="store_true", help="Open the pre-filter snapshot"
    )
    parser.add_argument("--port", type=int, default=8502)
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "config/social_nlp.json",
    )
    parser.add_argument(
        "--baseline-run",
        type=Path,
        help="Override the matching before snapshot in config/dashboard.json",
    )
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("Choose a local port between 1024 and 65535")
    config = json.loads(args.config.read_text())
    filtered = Path(config["output_dir"])
    filtered = filtered if filtered.is_absolute() else ROOT / filtered
    baseline = args.baseline_run
    if baseline is None:
        comparison_path = ROOT / "config/dashboard.json"
        comparison = (
            json.loads(comparison_path.read_text()).get("snapshot_comparison", {})
            if comparison_path.exists()
            else {}
        )
        if (
            comparison.get("after")
            and comparison.get("before")
            and (ROOT / comparison["after"]).resolve() == filtered.resolve()
        ):
            baseline = Path(comparison["before"])
    if baseline is not None and not baseline.is_absolute():
        baseline = ROOT / baseline
    if args.baseline and baseline is None:
        parser.error("No matching baseline configured; pass --baseline-run explicitly")
    directory = baseline if args.baseline else filtered
    SocialNLPClusterer.load_run(directory)
    env = dict(os.environ)
    env["BEESENSE_NLP_RUN_DIR"] = str(directory.resolve())
    if args.baseline or baseline is None:
        env.pop("BEESENSE_BASELINE_RUN_DIR", None)
    else:
        SocialNLPClusterer.load_run(baseline)
        env["BEESENSE_BASELINE_RUN_DIR"] = str(baseline.resolve())
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(ROOT / "streamlit_apps.py"),
        "--server.address",
        "127.0.0.1",
        "--server.port",
        str(args.port),
        "--browser.gatherUsageStats",
        "false",
    ]
    os.execvpe(sys.executable, command, env)


if __name__ == "__main__":
    main()
