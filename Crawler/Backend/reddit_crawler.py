"""Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix backend."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import Crawler.Backend.social_crawler as core
from Crawler.Backend.social_crawler import ROOT, SocialCrawler

VERSION = core.REDDRIX_ADAPTER_VERSION
METHOD = core.REDDRIX_METHOD
collect = core.collect_reddrix
load_reddrix = core.load_reddrix
normalize_item = core.normalize_reddrix_item
reddit = core.reddit
error_receipt = core.reddrix_error_receipt
receipt = core.reddrix_receipt
upstream_version = core.reddrix_version
resolve_display = core.resolve_reddrix_display
run_reddrix_worker = core.run_reddrix_worker

__all__ = [
    "RedditCrawler",
    "VERSION",
    "METHOD",
    "collect",
    "load_reddrix",
    "normalize_item",
    "reddit",
    "error_receipt",
    "receipt",
    "upstream_version",
    "resolve_display",
    "run_reddrix_worker",
]


class RedditCrawler(SocialCrawler):
    """Run only Reddit through the shared Reddrix implementation in SocialCrawler."""

    def __init__(self, config=None, *, display_mode=None, workers=None, **kwargs):
        supplied = ROOT / "config/reddit_crawler.json" if config is None else config
        if isinstance(supplied, (str, Path)):
            path = Path(supplied)
            if path.stat().st_size > 1_000_000:
                raise ValueError("config exceeds 1 MB")
            supplied = json.loads(path.read_text())
        supplied = deepcopy(supplied)
        if not isinstance(supplied, dict) or "reddit" not in supplied.get(
            "platforms", {}
        ):
            raise ValueError("A Reddit platform configuration is required")
        if workers and set(workers) != {"reddit"}:
            raise ValueError("Only a Reddit test worker may be supplied")
        settings = supplied["platforms"]["reddit"]
        if not isinstance(settings, dict):
            raise ValueError("Reddit platform configuration must be an object")
        self._legacy_backend_overridden = (
            settings.get("backend", "reddrix") != "reddrix"
        )
        supplied["platforms"] = {"reddit": {**settings, "backend": "reddrix"}}
        super().__init__(supplied, display_mode=display_mode, workers=workers, **kwargs)
        self.display = self.reddit_display

    def plan(self):
        return {
            **super().plan(),
            "acquisition_backend": "reddrix",
            "reddrix_version": upstream_version(),
            "platform_scope": "reddit_only",
            "display": deepcopy(self.display),
            "legacy_reddit_backend_overridden": self._legacy_backend_overridden,
            "live_access_verified": False,
            "upstream_search_sort": "relevance (Reddrix keyword mode ignores sort)",
            "comment_sort": "Reddrix does not expose comment sorting; configured sort is best effort only",
            "upstream_internal_retries": "Reddrix 1.2.14 has fixed internal retries; hard operation deadline still applies",
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=ROOT / "config/reddit_crawler.json"
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--display-mode", choices=["auto", "headless", "virtual"])
    args = parser.parse_args()
    crawler = RedditCrawler(
        args.config,
        display_mode=args.display_mode,
        progress=lambda e: print(json.dumps(e, ensure_ascii=False), flush=True),
    )
    output = args.output_dir or ROOT / "outputs" / (
        "reddit_reddrix_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    )
    result = crawler.plan() if args.dry_run else crawler.run(output)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
