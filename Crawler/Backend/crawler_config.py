"""One editable crawler configuration, expanded before adapter validation."""

import json
from copy import deepcopy
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config/social_crawler.json"
SHARED_FIELDS = {
    "storage",
    "project_id",
    "since",
    "until",
    "include_keywords",
    "exclude_keywords",
    "comment_exclude_keywords",
    "include_mode",
    "delay",
    "timeout_seconds",
    "total_seconds",
    "exclude_existing_datasets",
}
PLATFORM_DEFAULT_FIELDS = {
    "min_posts",
    "min_comments_per_post",
    "max_posts",
    "max_candidates",
    "max_comments",
    "search_results",
}


def read_config(value=None):
    """Read a bounded JSON object without touching authentication or runtime state."""
    if value is None:
        value = DEFAULT_CONFIG_PATH
    if isinstance(value, (str, Path)):
        path = Path(value)
        if path.stat().st_size > 1_000_000:
            raise ValueError("config exceeds 1 MB")
        value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("config must be an object")
    return deepcopy(value)


def expand_config(value):
    """Apply shared defaults; an explicit platform value always wins, even []."""
    cfg = read_config(value)
    if "schema_version" in cfg:
        version = cfg.pop("schema_version")
        if type(version) is not int or version != 1:
            raise ValueError("schema_version must be 1")
    has_queries = "queries" in cfg
    queries = cfg.pop("queries", None)
    if has_queries and (
        not isinstance(queries, list)
        or len(queries) > 100
        or any(
            not isinstance(q, str)
            or not q.strip()
            or len(q) > 300
            or any(ord(c) < 32 for c in q)
            for q in queries
        )
    ):
        raise ValueError("queries must contain at most 100 nonempty search strings")
    defaults = cfg.pop("platform_defaults", {})
    if not isinstance(defaults, dict) or set(defaults) - PLATFORM_DEFAULT_FIELDS:
        raise ValueError("platform_defaults must contain known shared limits")
    platforms = cfg.get("platforms")
    if isinstance(platforms, dict):
        for name, settings in platforms.items():
            if isinstance(settings, dict):
                settings = {**deepcopy(defaults), **settings}
                if queries is not None and name in {
                    "youtube",
                    "reddit",
                    "twitter",
                    "tiktok",
                }:
                    settings.setdefault("queries", deepcopy(queries))
                platforms[name] = settings
    return cfg


def standalone_config(value, platform, *, backend=None):
    """Project the versioned universal file to a legacy standalone adapter contract.

    Legacy caller-supplied dictionaries still use their original strict validators.
    Standalone entry points explicitly select their platform, even when disabled
    in the combined run. Instagram classes keep their respective adapter identity.
    """
    raw = read_config(value)
    if "schema_version" not in raw:
        return raw
    from Crawler.Backend.social_crawler import _config

    if isinstance(raw.get("platforms"), dict) and isinstance(
        raw["platforms"].get(platform), dict
    ):
        raw["platforms"][platform]["enabled"] = True
    cfg = _config(raw)
    if platform not in cfg["platforms"]:
        raise ValueError("Missing platform configuration: " + platform)
    settings = deepcopy(cfg["platforms"][platform])
    settings["enabled"] = True
    result = {key: deepcopy(cfg[key]) for key in SHARED_FIELDS}
    result["platforms"] = {platform: settings}
    if platform == "reddit":
        result["output_root"] = cfg["output_root"]
        result["reddrix"] = deepcopy(cfg["reddrix"])
        result["platform_execution"] = cfg["platform_execution"]
    elif platform == "twitter":
        for key in (
            "min_comments_per_post",
            "max_candidates",
            "max_comment_threads",
            "max_replies",
        ):
            settings.pop(key, None)
        result["scweet"] = deepcopy(cfg["scweet"])
    elif platform == "instagram":
        selected = settings.pop("backend")
        if backend and not (backend == "instagrapi" and selected == "browser"):
            selected = backend
        result["backend"] = selected
        if selected == "instaloader":
            result["instaloader"] = deepcopy(cfg["instaloader"])
        elif selected == "browser":
            result["browser"] = deepcopy(cfg["instagram_browser"])
        else:
            result["instagrapi"] = deepcopy(cfg["instagrapi"])
    return result
