"""Compare real worker functions against a pinned git baseline using offline pages.

Counts are synthetic page visits / iterator advances, never live HTTP throughput.
Run: python -m scripts.benchmark_youtube_reddit --baseline <40-char commit SHA>
"""

import argparse
import ast
import asyncio
import json
import re
import subprocess
from dataclasses import asdict
from pathlib import Path
from unittest.mock import Mock, patch

import yt_dlp
from yt_dlp.extractor.youtube import YoutubeIE

from Crawler.Backend import social_crawler as social
from Crawler.Backend.Youtube import crawl_youtube as youtube
from Crawler.Backend.Youtube.youtube_runtime import root_filter

ROOT = Path(__file__).resolve().parents[1]
POLICY = dict(
    since=None,
    until=None,
    include_keywords=["kuliah"],
    exclude_keywords=[],
    include_mode="any",
)
URL = "https://www.reddit.com/comments/abc123/"


def baseline_function(revision, path, name, namespace):
    source = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    tree = ast.parse(source)
    function = next(
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == name
    )
    target = dict(namespace)
    exec(compile(ast.Module(body=[function], type_ignores=[]), path, "exec"), target)
    return target[name]


def youtube_case(worker, *, fail=False):
    pages, events = [], []
    settings = asdict(youtube.Settings(max_comments=100, selection=POLICY))
    targets = ["00000000000"] if fail else ["00000000000", "00000000001"]
    exported = set()
    for native in targets:
        events.clear()
        pipe = Mock()
        pipe.send.side_effect = events.append

        def rows(*args, **kwargs):
            for page in range(10):
                pages.append((native, page))
                for number in range(10):
                    if fail and number == 2:
                        raise TimeoutError("timeout")
                    yield {
                        "id": f"{native}.c{page * 10 + number}",
                        "text": "comment",
                        "parent": "root",
                    }

        def extract(client, *args, **kwargs):
            return dict(
                id=native,
                title="Kuliah" if native.endswith("0") else "Other",
                description="",
                __post_extractor=client.get_info_extractor(
                    "Youtube"
                ).extract_comments(),
            )

        def process(client, raw, **kwargs):
            return dict(raw, **raw["__post_extractor"]())

        with (
            patch.object(yt_dlp.YoutubeDL, "extract_info", extract),
            patch.object(yt_dlp.YoutubeDL, "process_ie_result", process),
            patch.object(YoutubeIE, "_get_comments", rows),
            patch.object(youtube.os, "setsid"),
        ):
            worker("video", f"https://youtu.be/{native}", settings, pipe)
        root = next(row for kind, row in events if kind == "video")
        if root_filter(root, POLICY) is None:
            exported.add(native)
            exported.update(row["id"] for kind, row in events if kind == "comment")
    return dict(
        simulated_comment_pages=len(pages), retained_native_ids=sorted(exported)
    )


def reddit_case(collect):
    pages, events = [], []

    class Source:
        def __init__(self, **options):
            self.options = options

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def get_items(self):
            def item(native, post):
                return dict(
                    submissionId=native,
                    submissionIdPrefixed=("t3_" if post else "t1_") + native,
                    submissionType="post" if post else "comment",
                    submissionUrl=URL,
                    parentId=None if post else "t3_abc123",
                    parentPostId=None if post else "t3_abc123",
                    submittedAt="2026-06-01T07:00:00+00:00",
                    title="Kuliah" if post else None,
                    bodyText="context",
                    subreddit="r/indonesia",
                    depth=0,
                )

            yield item("abc123", True)
            emitted = 0
            # Model sequential continuation pages that still exist after the
            # SDK's own emitted-item cap. The old SDK traverses those pages.
            for page in range(20):
                pages.append(page)
                for number in range(10):
                    if emitted < self.options["max_comments_per_post"]:
                        emitted += 1
                        yield item(f"c{page * 10 + number:04d}", False)

    settings = dict(
        max_comments=10,
        max_replies=0,
        max_replies_per_thread=0,
        search_results=3,
        subreddits=["indonesia"],
        sort="new",
        request_delay=2,
        selection=POLICY,
    )
    asyncio.run(
        collect(
            "thread", URL, settings, lambda *event: events.append(event), factory=Source
        )
    )
    return dict(
        simulated_comment_pages=len(pages),
        retained_native_ids=sorted(row["fullname"] for _, row in events),
    )


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--baseline", required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "output/youtube_reddit_performance_20261106/benchmark.json",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[a-f0-9]{40}", args.baseline):
        parser.error("baseline must be the full commit SHA")
    old_youtube = baseline_function(
        args.baseline,
        "Crawler/Backend/Youtube/crawl_youtube.py",
        "worker",
        vars(youtube),
    )
    old_reddit = baseline_function(
        args.baseline,
        "Crawler/Backend/social_crawler.py",
        "collect_reddrix",
        vars(social),
    )
    cases = {}
    for name, before, after in [
        (
            "youtube_early_filter",
            youtube_case(old_youtube),
            youtube_case(youtube.worker),
        ),
        (
            "reddit_cap_cancels_pagination",
            reddit_case(old_reddit),
            reddit_case(social.collect_reddrix),
        ),
        (
            "youtube_timeout_retention",
            youtube_case(old_youtube, fail=True),
            youtube_case(youtube.worker, fail=True),
        ),
    ]:
        same = before["retained_native_ids"] == after["retained_native_ids"]
        if name != "youtube_timeout_retention" and not same:
            raise AssertionError(f"Native identity regression in {name}")
        cases[name] = dict(before=before, after=after, same_native_ids=same)
    result = dict(
        kind="OFFLINE_SYNTHETIC_PAGE_BENCHMARK",
        baseline_commit=args.baseline,
        live_requests=0,
        elapsed_speedup_measured=False,
        cases=cases,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                name: {
                    "before_pages": case["before"]["simulated_comment_pages"],
                    "after_pages": case["after"]["simulated_comment_pages"],
                    "before_ids": len(case["before"]["retained_native_ids"]),
                    "after_ids": len(case["after"]["retained_native_ids"]),
                    "same_native_ids": case["same_native_ids"],
                }
                for name, case in cases.items()
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
