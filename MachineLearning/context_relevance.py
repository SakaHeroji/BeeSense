"""Local, auditable zero-shot relevance decisions before topic clustering.

Model scores are uncalibrated heuristics, not measured accuracy. Raw source
records are retained. Uncertain and generic sentences never enter clustering.
Torch/Transformers are imported only when the inference backend is constructed.
"""

from __future__ import annotations

import json
import math
import re
import sqlite3
from collections import Counter
from copy import deepcopy
from hashlib import file_digest, sha256
from pathlib import Path

import numpy as np
import pandas as pd

from MachineLearning.relevance_semantic import DEFAULTS, LocalSemanticBackend

VERSION = "1.0.0"
EXTENSION = "beesense-context-relevance:1"
DECISIONS_FILE = "relevance_decisions.parquet"
REPORT_FILE = "relevance_report.json"
LABELS = ("relevant", "generic", "irrelevant")


def checksum(path):
    with Path(path).open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def digest(value):
    return sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()


class ContextRelevanceFilter:
    """Classify target sentences; parent context may rescue only ambiguous text.

    Use ``classify_many`` while acquiring data, or ``filter_snapshot`` for an
    existing source/model snapshot. Clustering receives original target text.
    """

    def __init__(self, config=None, *, predictor=None, progress=None):
        if isinstance(config, (str, Path)):
            config = json.loads(Path(config).read_text())
        if config is not None and (
            not isinstance(config, dict) or set(config) - set(DEFAULTS)
        ):
            raise ValueError("Unknown relevance settings")
        self.config = {**deepcopy(DEFAULTS), **deepcopy(config or {})}
        self._validate()
        self.progress = progress or (lambda event: None)
        self.predictor = predictor
        self.fingerprint = digest({"version": VERSION, "config": self.config})
        self.labels = LABELS
        cache = Path(self.config["cache_dir"])
        cache.mkdir(parents=True, exist_ok=True)
        self.database = sqlite3.connect(cache / "semantic_scores_v1.sqlite3")
        self.database.execute(
            "CREATE TABLE IF NOT EXISTS scores (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )

    def _validate(self):
        c = self.config
        if (
            not isinstance(c["keywords"], list)
            or not c["keywords"]
            or any(not isinstance(t, str) or not t.strip() for t in c["keywords"])
        ):
            raise ValueError("Search keywords must be nonempty strings")
        if not isinstance(c["scope"], str) or not c["scope"].strip():
            raise ValueError("A research scope is required")
        if (
            not isinstance(c["references"], dict)
            or set(c["references"]) != set(LABELS)
            or any(
                not isinstance(values, list)
                or not values
                or any(not isinstance(t, str) or not t.strip() for t in values)
                for values in c["references"].values()
            )
        ):
            raise ValueError("Provide reference examples for every relevance label")
        for keyword in c["keywords"]:
            pattern = r"(?<!\w)" + re.escape(keyword.casefold()) + r"(?!\w)"
            if not any(
                re.search(pattern, text.casefold())
                for text in c["references"]["relevant"]
            ):
                raise ValueError(
                    "A search keyword has no relevant context example: " + keyword
                )
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", c["model"]) or not re.fullmatch(
            r"[a-f0-9]{40}", c["revision"]
        ):
            raise ValueError("Use a pinned public relevance model")
        for key in (
            "batch_size",
            "threads",
            "max_tokens",
            "context_max_words",
            "stride",
        ):
            if type(c[key]) is not int or c[key] < 1:
                raise ValueError("Invalid relevance " + key)
        if c["max_tokens"] < 128:
            raise ValueError("Relevance max_tokens must be at least 128")
        if c["stride"] >= c["max_tokens"] - 2:
            raise ValueError("Relevance stride exceeds token window")
        for key in (
            "accept_score",
            "accept_margin",
            "other_score",
            "context_score",
            "context_direct_floor",
        ):
            if (
                type(c[key]) not in (int, float)
                or not math.isfinite(c[key])
                or not 0 <= c[key] <= 1
            ):
                raise ValueError("Invalid relevance " + key)
        if c["context_direct_floor"] > c["accept_score"]:
            raise ValueError("Context floor exceeds acceptance threshold")

    def _scores(self, premises):
        results, missing = {}, []
        for premise in dict.fromkeys(premises):
            key = digest([self.fingerprint, premise, self.labels])
            row = self.database.execute(
                "SELECT value FROM scores WHERE key=?", (key,)
            ).fetchone()
            if row:
                results[premise] = np.asarray(json.loads(row[0]), dtype=float)
            else:
                missing.append((premise, key))
        if missing:
            if self.predictor is None:
                self.predictor = LocalSemanticBackend(self.config)
            values = np.asarray(
                self.predictor([p for p, _ in missing], self.labels), dtype=float
            )
            if (
                values.shape != (len(missing), 3)
                or not np.isfinite(values).all()
                or (values < 0).any()
                or (values > 1).any()
            ):
                raise ValueError("Semantic predictor returned invalid scores")
            for (premise, key), value in zip(missing, values):
                results[premise] = value
                self.database.execute(
                    "INSERT OR REPLACE INTO scores VALUES (?, ?)",
                    (key, json.dumps(value.tolist())),
                )
            self.database.commit()
        values = [results[p] for p in premises]
        if any(
            v.shape != (3,)
            or not np.isfinite(v).all()
            or (v < 0).any()
            or (v > 1).any()
            for v in values
        ):
            raise ValueError("Cached semantic scores are invalid")
        return values

    def classify_many(self, units):
        """Units contain target ``sentence`` and optional audited parent/post text."""
        if not units:
            return []
        direct = self._scores([u["sentence"] for u in units])
        decisions, contextual, indices = [], [], []
        c = self.config
        for i, (unit, scores) in enumerate(zip(units, direct)):
            relevant, generic, irrelevant = map(float, scores)
            margin = relevant - max(generic, irrelevant)
            decision, reason = "uncertain", "scores_below_decision_threshold"
            if relevant >= c["accept_score"] and margin >= c["accept_margin"]:
                decision, reason = "relevant", "target_semantically_matches_scope"
            elif generic >= c["other_score"] and generic > max(relevant, irrelevant):
                decision, reason = "generic", "target_is_general_interaction"
            elif irrelevant >= c["other_score"] and irrelevant > max(relevant, generic):
                decision, reason = "irrelevant", "target_is_outside_scope"
            if (
                decision == "relevant"
                and relevant < 0.60
                and len(unit["sentence"].split()) <= c["context_max_words"]
            ):
                decision, reason = "uncertain", "weak_short_target_requires_context"
            item = {
                **unit,
                "decision": decision,
                "reason": reason,
                "relevant_score": relevant,
                "generic_score": generic,
                "irrelevant_score": irrelevant,
                "direct_margin": margin,
                "context_score": None,
                "context_used": False,
            }
            decisions.append(item)
            # A relevant root cannot rescue a clearly unrelated/generic target.
            if (
                decision == "uncertain"
                and relevant >= c["context_direct_floor"]
                and len(unit["sentence"].split()) <= c["context_max_words"]
                and (unit.get("parent_text") or unit.get("post_text"))
            ):
                indices.append(i)
                contextual.append(
                    "Kalimat yang dinilai: "
                    + unit["sentence"]
                    + "\nKonteks komentar induk: "
                    + unit.get("parent_text", "")[:400]
                    + "\nKonteks post asal: "
                    + unit.get("post_text", "")[:650]
                )
        for i, scores in zip(indices, self._scores(contextual) if contextual else []):
            relevant, generic, irrelevant = map(float, scores)
            item = decisions[i]
            item.update(context_used=True, context_score=relevant)
            if (
                relevant >= c["context_score"]
                and relevant - max(generic, irrelevant) >= c["accept_margin"]
            ):
                item.update(
                    decision="relevant", reason="ambiguous_target_resolved_with_context"
                )
        return decisions

    @staticmethod
    def build_units(data):
        """Resolve roots from native URLs; never match conversations by title."""
        from scripts.merge_social_datasets import identity

        sources = data["social_data"].to_dict("records")
        twitter = {}
        for row in sources:
            if row["platform"] == "twitter":
                ident = row["url"].rstrip("/").rsplit("/", 1)[-1]
                twitter[ident] = row["thread_root_key"].rsplit(":", 1)[-1]
        roots, metadata = {}, {}
        for row in sources:
            key, root = identity(row, twitter=twitter)
            metadata[row["source_row"]] = (key, root, row)
            if row["jenis"] in {"post", "video"}:
                text = (
                    str(row.get("judul_post") or "") + "\n" + str(row.get("teks") or "")
                )
                roots[root] = text
        by_native = {
            (key[0], key[2]): (root, row) for key, root, row in metadata.values()
        }
        parents = {}
        audit_directory = Path(data["summary"]["source_file"]).parent.parent
        # Use only hash-verified native relationships whose target text matches
        # the compact source. Conflicting observations cannot invent a parent.
        for audit in sorted(audit_directory.glob("*/Contents.jsonl")):
            manifest_path = audit.parent / "manifest.json"
            if not manifest_path.is_file():
                continue
            manifest = json.loads(manifest_path.read_text())
            expected = manifest.get("files_sha256", {}).get(audit.name)
            if expected is None or checksum(audit) != expected:
                continue
            with audit.open() as stream:
                for line in stream:
                    record = json.loads(line)
                    key = (record.get("platform"), str(record.get("native_id")))
                    if key not in by_native or not record.get("parent_key"):
                        continue
                    root, original = by_native[key]
                    if (
                        str(record.get("thread_root_key", "")).rsplit(":", 1)[-1]
                        != root[1]
                        or str(record.get("text_source", "")).strip()
                        != str(original["teks"]).strip()
                    ):
                        continue
                    parent = (key[0], record["parent_key"].rsplit(":", 1)[-1])
                    if parent in by_native and by_native[parent][0] == root:
                        parents.setdefault(key, set()).add(parent)
        units = []
        for occurrence in data["occurrences"].to_dict("records"):
            key, root, row = metadata[occurrence["source_row"]]
            options = parents.get((key[0], key[2]), set())
            parent = by_native[next(iter(options))][1] if len(options) == 1 else None
            parent_text = (
                str(parent["teks"])
                if parent and parent["jenis"] in {"comment", "reply"}
                else ""
            )
            units.append(
                {
                    "occurrence_id": occurrence["occurrence_id"],
                    "sentence_id": occurrence["sentence_id"],
                    "source_row": occurrence["source_row"],
                    "platform": occurrence["platform"],
                    "sentence": occurrence["sentence"],
                    "url": occurrence["url"],
                    "root_key": ":".join(root),
                    "parent_text": parent_text,
                    "post_text": roots.get(root, ""),
                    "context_quality": (
                        ("native_root" if root in roots else "root_unavailable")
                        + (";audited_parent" if parent_text else ";parent_unavailable")
                    ),
                }
            )
        return units

    def filter_snapshot(self, data, output_dir, *, chunk_size=128):
        """Write a new, checksum-bound decision dataset; never overwrite input."""
        import shutil
        import tempfile

        output = Path(output_dir)
        if output.exists():
            raise FileExistsError("Use a new relevance output directory")
        units = self.build_units(data)
        decisions = []
        for start in range(0, len(units), chunk_size):
            decisions.extend(self.classify_many(units[start : start + chunk_size]))
            self.progress(
                {
                    "event": "relevance_progress",
                    "complete": len(decisions),
                    "total": len(units),
                    "counts": dict(Counter(x["decision"] for x in decisions)),
                }
            )
        frame = pd.DataFrame(decisions)
        accepted = set(frame.loc[frame.decision == "relevant", "occurrence_id"])
        retained = data["occurrences"][
            data["occurrences"].occurrence_id.isin(accepted)
        ].copy()
        output.parent.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix=".relevance-", dir=output.parent))
        report = {
            "schema": EXTENSION,
            "version": VERSION,
            "source_sha256": data["summary"]["source_sha256"],
            "source_run_manifest_sha256": data["artifact_manifest_sha256"],
            "configuration": self.config,
            "policy_sha256": self.fingerprint,
            "model": getattr(self.predictor, "identity", {"test_predictor": True}),
            "total_occurrences": len(frame),
            "accepted_occurrences": len(retained),
            "accepted_unique_sentences": int(retained.sentence_id.nunique()),
            "decisions": frame.decision.value_counts().to_dict(),
            "per_platform": frame.groupby(["platform", "decision"])
            .size()
            .unstack(fill_value=0)
            .to_dict("index"),
            "parent_context": {
                "audited_parent_occurrences": int(
                    frame.context_quality.str.contains("audited_parent").sum()
                ),
                "rule": "Native root from source URL; parent only from checksum-verified matching source audit. Missing/conflicting parents are not inferred.",
            },
            "validation": "Automatic semantic prototype labels; cosine thresholds are provisional, not human-calibrated; no measured precision/recall.",
        }
        try:
            frame.to_parquet(stage / DECISIONS_FILE, index=False)
            retained.drop(
                columns=["cluster_id", "dbscan_cluster_id"], errors="ignore"
            ).to_parquet(stage / "filtered_sentences.parquet", index=False)
            (stage / REPORT_FILE).write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n"
            )
            (stage / "manifest.json").write_text(
                json.dumps(
                    {
                        "schema": EXTENSION,
                        "files_sha256": {p.name: checksum(p) for p in stage.iterdir()},
                    },
                    indent=2,
                )
                + "\n"
            )
            stage.rename(output)
        except BaseException:
            shutil.rmtree(stage, ignore_errors=True)
            raise
        return output

    @staticmethod
    def load_decisions(directory, source_sha256, occurrence_ids):
        directory = Path(directory)
        manifest = json.loads((directory / "manifest.json").read_text())
        if manifest.get("schema") != EXTENSION or set(
            manifest.get("files_sha256", {})
        ) != {DECISIONS_FILE, REPORT_FILE, "filtered_sentences.parquet"}:
            raise ValueError("Invalid relevance artifact manifest")
        for name, expected in manifest["files_sha256"].items():
            if checksum(directory / name) != expected:
                raise ValueError("Relevance checksum mismatch: " + name)
        report = json.loads((directory / REPORT_FILE).read_text())
        decisions = pd.read_parquet(directory / DECISIONS_FILE)
        if report["source_sha256"] != source_sha256:
            raise ValueError(
                "Relevance decisions belong to a different source workbook"
            )
        if decisions.occurrence_id.duplicated().any() or set(
            decisions.occurrence_id
        ) != set(occurrence_ids):
            raise ValueError(
                "Relevance decisions must cover every occurrence exactly once"
            )
        if not set(decisions.decision) <= {*LABELS, "uncertain"}:
            raise ValueError("Invalid relevance decision labels")
        if (
            len(decisions) != report["total_occurrences"]
            or int((decisions.decision == "relevant").sum())
            != report["accepted_occurrences"]
            or decisions.decision.value_counts().to_dict() != report["decisions"]
        ):
            raise ValueError("Relevance report counts disagree")
        filtered = pd.read_parquet(directory / "filtered_sentences.parquet")
        accepted = decisions[decisions.decision == "relevant"]
        if (
            filtered.occurrence_id.duplicated().any()
            or len(filtered) != len(accepted)
            or set(filtered.occurrence_id) != set(accepted.occurrence_id)
            or filtered.sentence_id.nunique() != report["accepted_unique_sentences"]
        ):
            raise ValueError(
                "Filtered sentence dataset differs from relevance decisions"
            )
        return decisions, report

    def close(self):
        self.database.close()
