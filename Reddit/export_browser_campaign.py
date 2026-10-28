#!/usr/bin/env python3
"""Export a connected-browser campaign using the existing Reddit table contract."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import re
import uuid

import crawl_reddit_single as common

DOM_VERSIONS = {"browser-dom:2", "playwright-dom:1"}
CAPTURE_VERSIONS = DOM_VERSIONS | {"public-web-excerpt:1"}


def load_campaign(directory, config, allow_metadata=False, dom_only=False):
    allowed = set(config["subreddits"])
    since, until = common.utc_datetime(config["since"]), common.utc_datetime(config["until"])
    candidates = json.loads((directory / "candidates.json").read_text())
    rows, seen, rejected = [], set(), Counter()
    accepted_versions = DOM_VERSIONS if dom_only else CAPTURE_VERSIONS
    for row in candidates:
        try:
            native_id = common.thread_id(row["canonical_url"])
            stamp = common.utc_datetime(row["published_at"])
            if native_id != row["native_id"] or row["subreddit"].lower() not in allowed:
                raise ValueError("identity_or_subreddit")
            if not since <= stamp < until:
                rejected["outside_window"] += 1
                continue
            if native_id in seen:
                rejected["duplicate"] += 1
                continue
            raw_path = directory / "raw" / (native_id + ".json")
            raw = json.loads(raw_path.read_text()) if raw_path.exists() else None
            if raw:
                post = raw["post"]
                if post["native_id"] != native_id or not since <= common.utc_datetime(post["published_at"]) < until:
                    raise ValueError("source_identity_or_date")
            if not allow_metadata and (not raw or raw.get("extractor_version") not in accepted_versions):
                continue
            seen.add(native_id)
            rows.append((row, raw))
        except (KeyError, TypeError, ValueError):
            rejected["invalid_candidate"] += 1
    target = config["max_posts"]
    if len(rows) < target:
        raise ValueError(f"Only {len(rows)} qualifying posts; target is {target}. Use --allow-metadata for an explicit preview.")
    if allow_metadata:
        # Keep all available evidence before filling the remaining preview slots.
        rows.sort(key=lambda item: not bool(item[1] and item[1].get("extractor_version") in CAPTURE_VERSIONS))
    return rows[:target], dict(rejected)


def export_campaign(directory, config, output, allow_metadata=False, dom_only=False):
    if dom_only and allow_metadata:
        raise ValueError('--dom-only cannot be combined with --allow-metadata')
    selected, rejected = load_campaign(directory, config, allow_metadata, dom_only)
    run_id = str(uuid.uuid4())
    factory = common.RedditRecordFactory(config["project_id"], run_id,
        common.KeywordMatcher(config["keywords"]), config["since"], config["until"])
    sink = common.BundleSink(output, config["project_id"], run_id)
    dataset = common.Dataset(factory, sink)
    counts, body_versions, subreddits = Counter(), Counter(), Counter()
    observed = common.now_iso()
    try:
        for candidate, raw in selected:
            native_id, page = candidate["native_id"], candidate["canonical_url"]
            root = factory.key("reddit", "reddit_post", native_id)
            post = raw["post"] if raw else candidate
            stamp = common.utc_datetime(post["published_at"]).isoformat()
            body = post.get("text", "") if raw else ""
            version = raw.get("extractor_version", "paragraph-v1") if raw else "search-metadata-only"
            body_versions[version] += 1
            flags = ["bounded_browser_dom", "post_context_only", "search_cohort_not_semantic_classification"]
            if not raw: flags += ["search_metadata_only", "body_not_acquired"]
            elif version not in DOM_VERSIONS: flags += ["paragraph_text_only"]
            if version == "public-web-excerpt:1":
                flags = [flag for flag in flags if flag not in {"paragraph_text_only", "bounded_browser_dom"}]
                flags += ["public_web_post_section_excerpt", "provider_cache_possible", "original_capture_time_unknown", "comments_not_acquired_by_web_reader"]
            if raw and not body: flags += ["no_rendered_body_text_media_or_link_possible"]
            captured = raw["captured_at"] if raw else candidate["observed_at"]
            shared = dict(platform="reddit", page_url=page, thread_root_key=root,
                discovered_from=candidate["discovered_from"], observed_at=captured,
                extraction_method=raw.get("method", "connected_chrome_rendered_dom") if raw else "connected_chrome_search_metadata",
                adapter_version=version)
            dataset.add_content(common.ContentInput(**shared, namespace="reddit_post", native_id=native_id,
                object_type="post", canonical_url=page, title=post["title"], text_source=body,
                published_at=stamp, timestamp_quality="exact", text_complete=False, quality_flags=tuple(flags)))
            counts["post"] += 1
            subreddits[candidate["subreddit"]] += 1
            per_post = Counter()
            for item in (raw["comments"] if raw else [])[:config["max_comments"]]:
                match = re.search(r"/comments/([a-z0-9]+)/comment/([a-z0-9]+)/", item.get("url", ""))
                if not match or match[1] != native_id or not item.get("text"):
                    counts["invalid_comments"] += 1
                    continue
                parent_match = re.search(r"/comment/([a-z0-9]+)/", item.get("parent_url") or "")
                kind = "reply" if parent_match else "comment"
                if kind == "reply" and per_post["reply"] >= config["max_replies"]: continue
                try:
                    published = common.utc_datetime(item["published_at"]).isoformat() if item.get("published_at") else None
                except ValueError:
                    published = None
                if published and not common.utc_datetime(config["since"]) <= common.utc_datetime(published) < common.utc_datetime(config["until"]):
                    counts["comments_outside_window"] += 1
                    continue
                parent = factory.key("reddit", "reddit_comment", parent_match[1]) if parent_match else root
                record = common.ContentInput(**shared, namespace="reddit_comment", native_id=match[2],
                    object_type=kind, canonical_url=item["url"], parent_key=parent, text_source=item["text"],
                    published_at=published, published_display=item.get("published_display"),
                    timestamp_quality="exact" if published else "unknown", text_complete=False,
                    quality_flags=("bounded_browser_dom", "more_replies_not_expanded", "parent_from_dom_nesting"))
                if dataset.add_content(record): counts[kind] += 1; per_post[kind] += 1
            status = "FINISHED_BEST_EFFORT" if version in DOM_VERSIONS else "PARTIAL_WEB_EXCERPT" if version == "public-web-excerpt:1" else "PARTIAL_PARAGRAPH_CAPTURE" if raw else "METADATA_ONLY_DETAIL_PENDING"
            warning_codes = ["public_web_excerpt", "provider_cache_possible", "comments_not_acquired"] if version == "public-web-excerpt:1" else ["more_replies_not_expanded"] if raw else ["body_not_acquired"]
            reason = "bounded_web_post_excerpt_original_capture_time_unknown" if version == "public-web-excerpt:1" else "bounded_visible_dom_not_complete_thread" if raw else "search_card_verified_detail_pending"
            sink.write("Runs", factory.row("Runs", unit_id=str(uuid.uuid4()), source="reddit", operation="public_thread_export",
                target=page, status=status, reason=reason,
                coverage="PARTIAL_WEB_POST_SECTION" if version == "public-web-excerpt:1" else "PARTIAL_RENDERED_DOM" if raw else "SEARCH_METADATA_ONLY", contents_written=1+sum(per_post.values()),
                comments_seen=per_post["comment"], replies_seen=per_post["reply"], duplicates_skipped=0, invalid_rows=0,
                max_comments=config["max_comments"], max_replies=config["max_replies"], timeout_seconds=config["timeout_seconds"],
                keywords=config["keywords"], source_version=version, warning_codes=warning_codes, started_at=captured, finished_at=observed))
        dataset.finish_relations()
        sink.write("Sources", factory.row("Sources", source="reddit", producer_version="browser-campaign:1", upstream_version="Chrome via CUA; standalone Playwright CLI; public web reader",
            extraction_method="public_browser_and_web_reader", access_mode="public_no_account_authentication",
            config={**config, "allow_metadata_preview":allow_metadata, "require_dom_only":dom_only, "actual_searches":"search_receipts.jsonl", "body_versions":dict(body_versions)},
            schema_fingerprint=common.schema_fingerprint(), observed_at=observed))
        common.add_readme(sink, factory, [("Campaign", f"Target {config['max_posts']} post unik, periode satu tahun, browser publik tanpa RSS."),
            ("Batas isi", "Konten DOM atau cuplikan publik yang berhasil dibaca. text_complete=false; more replies tidak dibuka. Post metadata-only memiliki text_source kosong, tidak direkayasa."),
            ("Batas topik", "Kelompok hasil pencarian kata kunci perkuliahan/karier, bukan klasifikasi semantik semua post."),
            ("Cuplikan web", "public-web-excerpt:1 berisi cuplikan bagian post dari alat baca web publik. Sumber dapat berasal dari cache; waktu capture awal tidak diketahui. Komentar tidak diisi dari sumber ini bila ID tidak tersedia."),
            ("Cakupan isi", json.dumps(dict(body_versions))), ("Periode", config["since"]+" sampai "+config["until"]+" (akhir eksklusif)")])
        pending_details = body_versions["search-metadata-only"]
        sink.finish({"source":"reddit", "mode":"browser_campaign_metadata_preview" if allow_metadata else "browser_campaign",
            "synthetic":False, "rss_used":False, "failed_units":0, "interrupted":bool(pending_details),
            "metadata_target_reached":True, "post_section_target_reached":not bool(pending_details),
            "dom_target_reached":sum(body_versions[version] for version in DOM_VERSIONS) >= config['max_posts'], "require_dom_only":dom_only,
            "pending_detail_units":pending_details, "comments_complete":False,
            "post_counts":dict(counts), "body_versions":dict(body_versions), "limitations":["partial_rendered_dom", "bounded_public_web_excerpts", "web_original_capture_time_unknown", "no_more_replies", "not_exhaustive_population", "no_actor_inference", "no_sentiment_labels"]})
    except BaseException:
        sink.abort()
        raise
    summary={"output_dir":str(sink.path), "counts":dict(counts), "body_versions":dict(body_versions), "subreddits":dict(subreddits),
        "rejected_candidates":rejected, "target_posts":config["max_posts"], "since":config["since"], "until":config["until"], "rss_used":False,
        "metadata_target_reached":True, "post_section_target_reached":not bool(body_versions["search-metadata-only"]), "comments_complete":False,
        "dom_target_reached":sum(body_versions[version] for version in DOM_VERSIONS) >= config['max_posts'], "require_dom_only":dom_only,
        "earliest_post":min(common.utc_datetime((raw["post"] if raw else row)["published_at"]).isoformat() for row,raw in selected),
        "latest_post":max(common.utc_datetime((raw["post"] if raw else row)["published_at"]).isoformat() for row,raw in selected)}
    (sink.path/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    return summary


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--support-dir",type=Path,required=True)
    parser.add_argument("--config",type=Path,default=Path(__file__).with_name("config_reddit_1000.json"))
    parser.add_argument("--output-dir",type=Path,required=True)
    parser.add_argument("--allow-metadata",action="store_true")
    parser.add_argument("--dom-only",action="store_true",help="Require 1000 browser/Playwright DOM records; do not count public excerpts")
    args=parser.parse_args()
    print(json.dumps(export_campaign(args.support_dir,json.loads(args.config.read_text()),args.output_dir,args.allow_metadata,args.dom_only),ensure_ascii=False,indent=2))
