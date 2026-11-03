"""Publish one globally unique social dataset partitioned by platform and crawl day."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import date, datetime, timezone
from hashlib import file_digest
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo

from openpyxl import Workbook, load_workbook
from openpyxl.cell import WriteOnlyCell

from Crawler.Backend.social_export import COMPACT_COLUMNS
from Crawler.Backend.social_identity import identity

SCHEMA = "beesense-social-archive:1"
WIB = ZoneInfo("Asia/Jakarta")


def sha(path):
    with Path(path).open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def stamp(value):
    # Audit Excel writers remove timezone only after converting to UTC.
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(value)
    return (
        parsed.replace(tzinfo=timezone.utc)
        if parsed.tzinfo is None
        else parsed.astimezone(timezone.utc)
    )


def _native(value, platform):
    value = str(value)
    if platform == "reddit":
        value = value.removeprefix("t1_").removeprefix("t3_")
    return value


def _audit_key(row):
    platform = row["platform"]
    kind = row["object_type"]
    return (
        platform,
        "status"
        if platform == "twitter"
        else "post"
        if kind in {"post", "video"}
        else "comment",
        _native(row["native_id"], platform),
    )


def crawl_day(record):
    return (
        record.get("crawl_day_wib")
        or stamp(record["first_seen"]).astimezone(WIB).date().isoformat()
    )


def historical_records(workbook, source_index, campaign_date):
    """Recover a verified merge's source range with honest day-only precision."""
    date.fromisoformat(campaign_date)
    workbook = Path(workbook).resolve()
    evidence = workbook.with_name("merge_report.json")
    report = json.loads(evidence.read_text())
    if report.get("status") != "PASS" or report.get("output_sha256") != sha(workbook):
        raise ValueError("Historical merge checksum mismatch")
    source = report["source_workbooks"][source_index]
    first, last = source["first_excel_row"], source["last_excel_row"]
    book = load_workbook(workbook, read_only=True, data_only=False)
    records = []
    try:
        rows = book["Data"].iter_rows()
        if tuple(c.value for c in next(rows)) != tuple(COMPACT_COLUMNS):
            raise ValueError("Historical merge columns changed")
        for index, cells in enumerate(rows, 2):
            if first <= index <= last:
                if any(c.data_type == "f" for c in cells):
                    raise ValueError("Formula found in historical merge")
                values = [c.value for c in cells]
                key, root = identity(dict(zip(COMPACT_COLUMNS, values)))
                records.append(
                    {
                        "native_key": list(key),
                        "root": root[1],
                        "values": [
                            v.isoformat() if isinstance(v, datetime) else v
                            for v in values
                        ],
                        "first_seen": None,
                        "last_seen": None,
                        "crawl_day_wib": campaign_date,
                        "timestamp_precision": "historical_campaign_day",
                        "source": str(workbook),
                        "source_row": index,
                        "campaign_evidence": str(evidence),
                        "original_source": source["path"],
                    }
                )
    finally:
        book.close()
    if len(records) != source["rows"] or sha(workbook) != report["output_sha256"]:
        raise ValueError("Historical source range mismatch")
    return records, {
        "path": str(workbook) + "#source=" + str(source_index),
        "workbook_sha256": sha(workbook),
        "evidence_sha256": sha(evidence),
        "date_wib": campaign_date,
        "timestamp_precision": "historical_campaign_day",
    }


def source_records(workbook, *, allow_synthetic=False):
    """Bind compact rows to real acquisition timestamps and native roots."""
    workbook = Path(workbook).resolve()
    directory = workbook.parent
    descriptor = directory / "manifest.json"
    manifest = json.loads(descriptor.read_text()) if descriptor.exists() else {}
    if manifest.get("synthetic") and not allow_synthetic:
        raise ValueError("Synthetic crawler output cannot enter the real archive")
    if (
        manifest.get("mode") == "compact_projection_of_two_verified_audit_bundles"
        or (directory / "merge_report.json").exists()
    ):
        raise ValueError("Use original crawl bundles instead of a derived merge")
    audit = directory / "Contents.jsonl"
    audit = audit if audit.exists() else directory / "dataset.xlsx"
    before = {p.name: sha(p) for p in (workbook, audit)}
    for name, digest in before.items():
        expected = manifest.get("files_sha256", {}).get(name)
        if expected and digest != expected:
            raise ValueError("Crawl source checksum mismatch: " + name)
    book = None
    evidence, twitter = {}, {}
    try:
        if audit.suffix == ".xlsx":
            book = load_workbook(audit, read_only=True, data_only=True)
            rows = book["Contents"].values
            headers = next(rows)
            records = (dict(zip(headers, values)) for values in rows)
        else:
            records = (
                json.loads(line)
                for line in audit.read_text(encoding="utf-8").splitlines()
            )
        for row in records:
            key = _audit_key(row)
            observed = stamp(row["observed_at"]).isoformat()
            root = _native(row["thread_root_key"].rsplit(":", 1)[-1], row["platform"])
            previous = evidence.get(key)
            if previous and previous["root"] != root:
                raise ValueError("Conflicting audited root identity")
            evidence[key] = {
                "first_seen": min(observed, previous["first_seen"])
                if previous
                else observed,
                "last_seen": max(observed, previous["last_seen"])
                if previous
                else observed,
                "root": root,
            }
            if row["platform"] == "twitter":
                twitter[key[2]] = root
    finally:
        if book is not None:
            book.close()
    compact = load_workbook(workbook, read_only=True, data_only=False)
    result = []
    try:
        rows = compact["Data"].iter_rows()
        if tuple(c.value for c in next(rows)) != tuple(COMPACT_COLUMNS):
            raise ValueError("Unexpected compact crawler columns")
        for row_number, cells in enumerate(rows, 2):
            if any(c.data_type == "f" for c in cells):
                raise ValueError("Formula found in crawl source")
            values = [c.value for c in cells]
            key, root = identity(dict(zip(COMPACT_COLUMNS, values)), twitter=twitter)
            observed = evidence.get(key)
            if not observed or observed["root"] != root[1]:
                raise ValueError("Compact row has no matching native acquisition audit")
            result.append(
                {
                    "native_key": list(key),
                    "values": [
                        v.isoformat() if isinstance(v, datetime) else v for v in values
                    ],
                    **observed,
                    "source": str(workbook),
                    "source_row": row_number,
                }
            )
    finally:
        compact.close()
    if any(sha(directory / name) != digest for name, digest in before.items()):
        raise ValueError("Crawl source changed while reading")
    return result, {
        "path": str(workbook),
        "files_sha256": before,
        "rows": len(result),
        "synthetic": bool(manifest.get("synthetic", False)),
    }


@contextmanager
def _lock(root):
    import fcntl

    root.parent.mkdir(parents=True, exist_ok=True)
    with root.with_name("." + root.name + ".lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _write_day(stage, platform, day, records):
    directory = stage / platform / day
    directory.mkdir(parents=True)
    book = Workbook(write_only=True)
    sheet = book.create_sheet("Data")
    sheet.append(COMPACT_COLUMNS)
    twitter = {}
    with (directory / "record_lineage.jsonl").open("w", encoding="utf-8") as audit:
        for excel_row, record in enumerate(records, 2):
            values = record["values"][:]
            for index in (3, 5):
                if isinstance(values[index], str):
                    values[index] = datetime.fromisoformat(values[index])
            cells = []
            for value in values:
                cell = WriteOnlyCell(sheet, value=value)
                if isinstance(value, str):
                    cell.data_type = "s"
                if isinstance(value, datetime):
                    cell.number_format = "yyyy-mm-dd hh:mm:ss"
                cells.append(cell)
            sheet.append(cells)
            audit.write(
                json.dumps(
                    {k: v for k, v in record.items() if k != "values"}
                    | {"excel_row": excel_row},
                    ensure_ascii=False,
                )
                + "\n"
            )
            if platform == "twitter":
                twitter[record["native_key"][2]] = record["root"]
    target = directory / "social_data.xlsx"
    book.save(target)
    book.close()
    if twitter:
        (directory / "native_roots.json").write_text(
            json.dumps(
                {
                    "schema": "beesense-native-roots:1",
                    "workbook_sha256": sha(target),
                    "twitter": twitter,
                },
                indent=2,
            )
        )
    return {
        "platform": platform,
        "date_wib": day,
        "rows": len(records),
        "path": f"{platform}/{day}/social_data.xlsx",
        "sha256": sha(target),
    }


def organize(sources, output_root, *, allow_synthetic=False, historical_sources=()):
    """Upsert observations, retain latest values and assign each ID its first WIB day.

    Daily files are disjoint partitions, so parents may live in an earlier day's
    file. The original audit bundles preserve the complete acquisition contract.
    """
    root = Path(output_root).resolve()
    with _lock(root):
        old, registry, observations = {}, {}, []
        if root.exists():
            manifest = root / "archive.json"
            if (
                not manifest.is_file()
                or json.loads(manifest.read_text()).get("schema") != SCHEMA
            ):
                raise ValueError("Output root is not a managed social archive")
            info = json.loads(manifest.read_text())
            for name, digest in info["files_sha256"].items():
                if sha(root / name) != digest:
                    raise ValueError("Organized archive checksum mismatch")
            for line in (root / "records.jsonl").read_text().splitlines():
                record = json.loads(line)
                old[tuple(record["native_key"])] = record
            registry = {r["path"]: r for r in info["sources"]}
            observations = [
                json.loads(line)
                for line in (root / "observations.jsonl").read_text().splitlines()
            ]
        for source in dict.fromkeys(str(Path(p).resolve()) for p in sources):
            records, descriptor = source_records(
                source, allow_synthetic=allow_synthetic
            )
            if registry.get(source) == descriptor:
                continue
            if source in registry:
                raise ValueError("Previously registered immutable crawl bundle changed")
            registry[source] = descriptor
            for record in records:
                key = tuple(record["native_key"])
                previous = old.get(key)
                if previous and previous["root"] != record["root"]:
                    raise ValueError("Conflicting native root across crawl bundles")
                observations.append({k: v for k, v in record.items() if k != "values"})
                if previous:
                    winner = (
                        record
                        if (
                            record["last_seen"] or "",
                            record["source"],
                            record["source_row"],
                        )
                        >= (
                            previous["last_seen"] or "",
                            previous["source"],
                            previous["source_row"],
                        )
                        else previous
                    )
                    record = {
                        **winner,
                        "first_seen": min(record["first_seen"], previous["first_seen"])
                        if previous["first_seen"]
                        else None,
                        "last_seen": max(
                            record["last_seen"], previous["last_seen"] or ""
                        ),
                        "crawl_day_wib": min(crawl_day(record), crawl_day(previous)),
                    }
                old[key] = record
        for supplied in historical_sources:
            records, descriptor = historical_records(**supplied)
            if (
                descriptor["path"] in registry
                and registry[descriptor["path"]] != descriptor
            ):
                raise ValueError("Previously registered historical merge changed")
            registry[descriptor["path"]] = descriptor
            known = {
                (r["source"], r["source_row"], r.get("timestamp_precision"))
                for r in observations
            }
            for record in records:
                key = tuple(record["native_key"])
                observation = (
                    record["source"],
                    record["source_row"],
                    record.get("timestamp_precision"),
                )
                if observation not in known:
                    observations.append(
                        {k: v for k, v in record.items() if k != "values"}
                    )
                    known.add(observation)
                if key not in old:
                    old[key] = record
        grouped = defaultdict(list)
        for key, record in sorted(old.items()):
            day = crawl_day(record)
            grouped[key[0], day].append(record)
        stage = Path(tempfile.mkdtemp(prefix="." + root.name + "-", dir=root.parent))
        backup = None
        try:
            partitions = [
                _write_day(stage, platform, day, records)
                for (platform, day), records in sorted(grouped.items())
            ]
            with (stage / "records.jsonl").open("w", encoding="utf-8") as stream:
                for record in old.values():
                    stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            with (stage / "observations.jsonl").open("w", encoding="utf-8") as stream:
                for record in observations:
                    stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            counts = Counter(key[0] for key in old)
            report = {
                "schema": SCHEMA,
                "timezone": "Asia/Jakarta",
                "date_basis": "first_audited_observation",
                "value_policy": "latest_audited_observation",
                "rows": len(old),
                "duplicate_native_ids": 0,
                "observations": len(observations),
                "duplicates_removed": len(observations) - len(old),
                "platform_counts": dict(counts),
                "day_only_records": sum(
                    r.get("timestamp_precision") == "historical_campaign_day"
                    for r in old.values()
                ),
                "partitions": partitions,
                "sources": list(registry.values()),
            }
            (stage / "README.md").write_text(
                "# Data social media per platform dan tanggal\n\nTanggal folder adalah pengamatan pertama dalam WIB. Setiap ID asli hanya muncul sekali di seluruh partisi; versi terbaru dipertahankan. Root percakapan dapat berada di tanggal lebih awal. `record_lineage.jsonl` menghubungkan baris ke sumber asli.\n\n| Platform | Tanggal crawling WIB | Record unik | File |\n|---|---|---:|---|\n"
                + "\n".join(
                    f"| {p['platform']} | {p['date_wib']} | {p['rows']} | [Excel]({p['path']}) |"
                    for p in partitions
                )
                + "\n"
            )
            report["files_sha256"] = {
                str(p.relative_to(stage)): sha(p)
                for p in stage.rglob("*")
                if p.is_file()
            }
            (stage / "archive.json").write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n"
            )
            verify(stage)
            if root.exists():
                backup = root.with_name("." + root.name + "-previous-" + uuid4().hex)
                os.replace(root, backup)
            try:
                os.replace(stage, root)
            except BaseException:
                if backup:
                    os.replace(backup, root)
                raise
            if backup:
                shutil.rmtree(backup)
            return {
                **report,
                "output_root": str(root),
                "primary_files": [str(root / p["path"]) for p in partitions],
            }
        finally:
            if stage.exists():
                shutil.rmtree(stage)


def verify(root):
    """Read every exported row back; fail on repeated IDs, wrong days or lost rows."""
    root = Path(root)
    report = json.loads((root / "archive.json").read_text())
    records = list(map(json.loads, (root / "records.jsonl").read_text().splitlines()))
    expected = {tuple(r["native_key"]): r for r in records}
    if len(expected) != len(records):
        raise ValueError("Duplicate native ID in organized catalog")
    for name, digest in report["files_sha256"].items():
        if sha(root / name) != digest:
            raise ValueError("Organized archive checksum mismatch")
    seen = set()
    for partition in report["partitions"]:
        path = root / partition["path"]
        if sha(path) != partition["sha256"]:
            raise ValueError("Daily workbook checksum mismatch")
        twitter = {k[2]: r["root"] for k, r in expected.items() if k[0] == "twitter"}
        book = load_workbook(path, read_only=True, data_only=False)
        count = 0
        try:
            rows = book["Data"].iter_rows()
            if tuple(c.value for c in next(rows)) != tuple(COMPACT_COLUMNS):
                raise ValueError("Daily workbook columns changed")
            for cells in rows:
                if any(c.data_type == "f" for c in cells):
                    raise ValueError("Formula found in organized data")
                key, _ = identity(
                    dict(zip(COMPACT_COLUMNS, (c.value for c in cells))),
                    twitter=twitter,
                )
                if key in seen or key not in expected:
                    raise ValueError(
                        "Duplicate or unexpected native ID across daily files"
                    )
                values = [
                    c.value.isoformat() if isinstance(c.value, datetime) else c.value
                    for c in cells
                ]
                if values != expected[key]["values"]:
                    raise ValueError("Organized workbook changed source values")
                if (
                    key[0] != partition["platform"]
                    or crawl_day(expected[key]) != partition["date_wib"]
                ):
                    raise ValueError(
                        "Record assigned to the wrong platform or crawl day"
                    )
                seen.add(key)
                count += 1
        finally:
            book.close()
        if count != partition["rows"]:
            raise ValueError("Daily row count mismatch")
    if seen != set(expected) or len(seen) != report["rows"]:
        raise ValueError("Organized output lost native IDs")
    return report
