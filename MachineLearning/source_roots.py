"""Resolve X conversation roots from audited native IDs, never caption similarity."""

import json
import re
from hashlib import file_digest
from pathlib import Path

ROOTS_FILE = "native_roots.json"
ROOTS_SCHEMA = "beesense-native-roots:1"


def checksum(path):
    with Path(path).open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def native(value):
    value = str(value)
    if not re.fullmatch(r"[1-9][0-9]{0,24}", value):
        raise ValueError("Invalid Twitter native identity")
    return value


def twitter_roots(workbook):
    """Read a workbook-bound sidecar, or the original hash-verified crawl audit."""
    workbook = Path(workbook)
    sidecar = workbook.parent / ROOTS_FILE
    if sidecar.exists():
        data = json.loads(sidecar.read_text())
        if data.get("schema") != ROOTS_SCHEMA or data.get(
            "workbook_sha256"
        ) != checksum(workbook):
            raise ValueError("Native roots sidecar does not match workbook")
        return {native(key): native(value) for key, value in data["twitter"].items()}
    audit = workbook.parent / "Contents.jsonl"
    if not audit.exists():
        return {}
    manifest = json.loads((workbook.parent / "manifest.json").read_text())
    expected_workbook = manifest.get("files_sha256", {}).get(workbook.name)
    if expected_workbook is not None and expected_workbook != checksum(workbook):
        raise ValueError("Twitter source workbook checksum mismatch")
    if manifest.get("files_sha256", {}).get(audit.name) != checksum(audit):
        raise ValueError("Twitter source audit checksum mismatch")
    roots = {}
    for line in audit.read_text().splitlines():
        row = json.loads(line)
        if row["platform"] != "twitter":
            continue
        ident = native(row["native_id"])
        if row["canonical_url"] != "https://x.com/i/web/status/" + ident:
            raise ValueError("Twitter source native ID and canonical URL disagree")
        root_key = row["thread_root_key"]
        if not root_key.startswith("twitter:x_post:"):
            raise ValueError("Invalid Twitter source root")
        root = native(root_key.removeprefix("twitter:x_post:"))
        if (row["object_type"] == "post") != (ident == root):
            raise ValueError("Twitter source kind and conversation root disagree")
        if row["object_key"] != "twitter:x_post:" + ident:
            raise ValueError("Conflicting Twitter source identity")
        if ident in roots and roots[ident] != root:
            raise ValueError("Conflicting Twitter conversation roots")
        roots[ident] = root
    return roots


def write_roots(directory, workbook, roots):
    path = Path(directory) / ROOTS_FILE
    path.write_text(
        json.dumps(
            {
                "schema": ROOTS_SCHEMA,
                "workbook_sha256": checksum(workbook),
                "twitter": roots,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    return path
