"""Add Gemini descriptions to a verified fitted run, preserving its clustering."""

import argparse
import copy
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from MachineLearning import topic_narratives
from MachineLearning.social_nlp import ROOT, SocialNLPClusterer, file_hash, json_write


def enrich_run(source, output, config, *, progress=lambda *args, **kwargs: None):
    """Publish a new atomic bundle; never overwrite or refit the source run."""
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.exists():
        raise FileExistsError("Use a new narrative output directory")
    if source in output.parents:
        raise ValueError("Narrative output must be outside the source bundle")
    data = SocialNLPClusterer.load_run(source)
    summary = copy.deepcopy(data["summary"])
    if (
        len(data["topics"]) != 20
        or not summary["coherence"]["target_met"]
        or summary["coherence"]["macro_mean"] < 0.4
        or summary.get("synthetic")
    ):
        raise ValueError(
            "Gemini requires a real fitted run with 20 topics and c_v >= 0.4"
        )
    options = config["gemini"]
    topic_narratives.validate_options(options)
    if not options["enabled"]:
        raise ValueError("Enable Gemini explicitly in the supplied configuration")
    manifest = json.loads((source / "manifest.json").read_text())
    cache = Path(config["cache_dir"])
    rows = topic_narratives.generate(
        data["topics"],
        summary["source_sha256"],
        options,
        sentences=data["sentences"],
        root=ROOT,
        cache_dir=cache if cache.is_absolute() else ROOT / cache,
        progress=progress,
    )
    # Recheck the source after network requests, before copying any fitted file.
    if file_hash(source / "manifest.json") != data["artifact_manifest_sha256"]:
        raise ValueError("Source manifest changed during narrative generation")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".nlp-narratives-", dir=output.parent))
    try:
        for name, expected in manifest["files_sha256"].items():
            if file_hash(source / name) != expected:
                raise ValueError("Source artifact changed: " + name)
            shutil.copyfile(source / name, stage / name)
            if file_hash(stage / name) != expected:
                raise ValueError("Artifact copy checksum mismatch: " + name)
        topic_narratives.write_csv(stage / topic_narratives.CSV_NAME, rows)
        summary["created_at"] = datetime.now(timezone.utc).isoformat()
        summary["config"]["gemini"] = copy.deepcopy(options)
        summary["config"]["output_dir"] = str(output)
        summary["topic_narratives"] = {
            **summary["topic_narratives"],
            "enabled": True,
            "model": options["model"],
            "prompt_version": topic_narratives.PROMPT_VERSION,
            "csv": topic_narratives.CSV_NAME,
            "derived_from_run": str(source),
            "derived_from_manifest_sha256": data["artifact_manifest_sha256"],
            "clustering_unchanged": True,
        }
        json_write(stage / "summary.json", summary)
        manifest["extensions"] = [
            item
            for item in manifest.get("extensions", [])
            if item
            not in (topic_narratives.EXTENSION, topic_narratives.LEGACY_EXTENSION)
        ] + [topic_narratives.EXTENSION]
        manifest["files_sha256"] = {
            name: file_hash(stage / name)
            for name in set(manifest["files_sha256"]) | {topic_narratives.CSV_NAME}
        }
        json_write(stage / "manifest.json", manifest)
        SocialNLPClusterer.load_run(stage)
        stage.chmod(0o755)
        stage.rename(output)
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = SocialNLPClusterer(args.config).config
    output = enrich_run(
        args.source_run,
        args.output_dir,
        config,
        progress=lambda event, **fields: print(
            json.dumps({"event": event, **fields}), flush=True
        ),
    )
    print(json.dumps({"status": "saved", "output_dir": str(output)}), flush=True)


if __name__ == "__main__":
    main()
