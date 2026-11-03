"""Consolidate original crawl bundles by platform/day without repeated native IDs."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from Crawler.Backend.social_archive import organize, source_records

ROOT = Path(__file__).resolve().parents[1]


def discover(outputs, raw_root):
    candidates = list(Path(outputs).glob("*/social_data.xlsx"))
    candidates += (
        list(Path(raw_root).rglob("social_data.xlsx"))
        if Path(raw_root).exists()
        else []
    )
    sources, skipped = [], []
    for path in sorted(set(candidates)):
        descriptor = path.with_name("manifest.json")
        metadata = json.loads(descriptor.read_text()) if descriptor.exists() else {}
        reason = None
        if metadata.get("synthetic"):
            reason = "synthetic"
        elif (
            metadata.get("mode") == "compact_projection_of_two_verified_audit_bundles"
            or path.with_name("merge_report.json").exists()
        ):
            reason = "derived_merge"
        elif (
            not path.with_name("Contents.jsonl").exists()
            and not path.with_name("dataset.xlsx").exists()
        ):
            reason = "no_original_acquisition_audit"
        if reason:
            skipped.append({"path": str(path), "reason": reason})
        else:
            sources.append(path)
    return sources, skipped


def consolidate(
    outputs, raw_root, output_root, *, archive_raw=False, historical_sources=()
):
    outputs, raw_root = Path(outputs).resolve(), Path(raw_root).resolve()
    sources, skipped = discover(outputs, raw_root)
    moved = []
    try:
        if archive_raw:
            tracked = subprocess.check_output(
                ["git", "ls-files", "--", str(outputs)], cwd=ROOT, text=True
            ).splitlines()
            protected = {
                ROOT / Path(p).parts[0] / Path(p).parts[1]
                for p in tracked
                if len(Path(p).parts) >= 2
            }
            for index, path in enumerate(sources):
                if path.parent.parent != outputs or path.parent in protected:
                    continue
                records, _ = source_records(path)
                from Crawler.Backend.social_archive import WIB, stamp

                day = min(
                    (
                        stamp(r["first_seen"]).astimezone(WIB).date().isoformat()
                        for r in records
                    ),
                    default="empty",
                )
                destination = raw_root / "legacy" / day / path.parent.name
                if destination.exists():
                    raise ValueError("Raw archive destination already exists")
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(path.parent), str(destination))
                moved.append((path.parent, destination))
                progress = path.parent.with_name(path.parent.name + ".progress.json")
                if progress.exists():
                    target = destination.with_name(destination.name + ".progress.json")
                    shutil.move(str(progress), str(target))
                    moved.append((progress, target))
                sources[index] = destination / path.name
        report = organize(sources, output_root, historical_sources=historical_sources)
    except BaseException:
        for previous, current in reversed(moved):
            previous.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(current), str(previous))
        raise
    if moved:
        mapping = raw_root / "relocations.json"
        history = json.loads(mapping.read_text()) if mapping.exists() else []
        history += [{"previous": str(a), "current": str(b)} for a, b in moved]
        mapping.write_text(json.dumps(history, indent=2) + "\n")
    return {**report, "skipped": skipped, "relocated": len(moved)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT / "outputs")
    parser.add_argument("--raw-root", type=Path, default=ROOT / "output/crawler_runs")
    parser.add_argument("--output-root", type=Path, default=ROOT / "outputs/crawling")
    parser.add_argument(
        "--archive-raw",
        action="store_true",
        help="Relocate unpublished raw bundles; preserve all tracked snapshots",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--historical-merge",
        type=Path,
        help="Recover missing records from a checksum-verified historical merge",
    )
    parser.add_argument("--historical-source-index", type=int)
    parser.add_argument(
        "--campaign-date",
        help="Verified campaign date in WIB; timestamp precision remains day-only",
    )
    args = parser.parse_args()
    historical = []
    if args.historical_merge:
        if args.historical_source_index is None or not args.campaign_date:
            parser.error(
                "Historical recovery requires source index and verified campaign date"
            )
        historical.append(
            {
                "workbook": args.historical_merge,
                "source_index": args.historical_source_index,
                "campaign_date": args.campaign_date,
            }
        )
    if args.dry_run:
        sources, skipped = discover(args.source_root, args.raw_root)
        result = {"sources": [str(p) for p in sources], "skipped": skipped}
    else:
        result = consolidate(
            args.source_root,
            args.raw_root,
            args.output_root,
            archive_raw=args.archive_raw,
            historical_sources=historical,
        )
        result = {
            k: result[k]
            for k in (
                "output_root",
                "rows",
                "observations",
                "duplicates_removed",
                "duplicate_native_ids",
                "platform_counts",
                "day_only_records",
                "partitions",
                "skipped",
                "relocated",
            )
        }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
