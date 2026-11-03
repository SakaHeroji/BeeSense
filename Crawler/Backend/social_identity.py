"""Native social record identity shared by merge and organized crawler outputs."""

import re
from urllib.parse import parse_qs, urlsplit


def identity(row, *, twitter=None):
    """Return global native object ID plus its root; text never defines identity."""
    platform, kind = row["platform"], row["jenis"]
    url = urlsplit(row["url"])
    if (
        platform == "twitter"
        and url.scheme == "https"
        and url.netloc in {"x.com", "www.x.com", "twitter.com", "www.twitter.com"}
    ):
        match = re.fullmatch(
            r"/(?:[A-Za-z0-9_]{1,15}|i/web)/status/([1-9][0-9]{0,24})/?", url.path
        )
        if not match or url.query or url.fragment:
            raise ValueError("Unsupported Twitter native URL")
        native = match[1]
        root_kind = kind == "post"
        root = (twitter or {}).get(native, native if root_kind else None)
        if not root or root_kind != (native == root):
            raise ValueError("Twitter comment requires audited conversation root")
        if kind not in {"post", "comment", "reply"}:
            raise ValueError("Unsupported Twitter kind")
        return (platform, "status", native), (platform, root)
    if platform == "youtube" and url.hostname in {"youtube.com", "www.youtube.com"}:
        params = parse_qs(url.query)
        root = params.get("v", [""])[0]
        native = root if kind == "video" else params.get("lc", [""])[0]
        root_kind = kind == "video"
    elif platform == "tiktok":
        from Crawler.Backend.tiktok_crawler import parse_url

        root, _, comment = parse_url(row["url"])
        root_kind = kind == "post"
        if root_kind and comment or not root_kind and not comment:
            raise ValueError("TikTok content kind and comment identity disagree")
        native = root if root_kind else comment
    elif platform == "reddit" and url.hostname in {"reddit.com", "www.reddit.com"}:
        match = re.fullmatch(
            r"/comments/([a-z0-9]+)/(?:(?:_|[^/]+)/([a-z0-9]+)/)?", url.path
        )
        if not match:
            raise ValueError(f"Unsupported Reddit native URL: {row['url']}")
        root, comment = match.groups()
        root_kind = kind == "post"
        native = root if root_kind else comment
    elif (
        platform == "instagram"
        and url.scheme == "https"
        and url.netloc in {"instagram.com", "www.instagram.com"}
    ):
        match = re.fullmatch(
            r"/(?:[\w.]+/)?(?:p|reel|tv)/([A-Za-z0-9_-]{1,40})/(?:c/([1-9][0-9]{0,29})/?)?",
            url.path,
        )
        if not match:
            raise ValueError("Unsupported Instagram native URL")
        code, path_comment = match.groups()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        root_number = 0
        for char in code:
            root_number = root_number * 64 + alphabet.index(char)
        if root_number <= 0:
            raise ValueError("Invalid Instagram media ID")
        root = str(root_number)
        query = parse_qs(url.query).get("comment_id", [])
        if len(query) > 1 or query and path_comment and query[0] != path_comment:
            raise ValueError("Conflicting Instagram comment identity")
        comment = path_comment or (query[0] if query else None)
        root_kind = kind == "post"
        if root_kind and comment:
            raise ValueError("Instagram root cannot have a comment identity")
        native = root if root_kind else comment
        if native is None or not re.fullmatch(r"[1-9][0-9]{0,29}", native):
            raise ValueError("Missing Instagram native ID")
    else:
        raise ValueError(f"Unsupported platform or URL: {platform}")
    if kind not in (
        {"video", "comment", "reply"}
        if platform == "youtube"
        else {"post", "comment", "reply"}
    ):
        raise ValueError(f"Unsupported content kind: {kind}")
    if not native or not root:
        raise ValueError("Missing native content ID")
    return (platform, "post" if root_kind else "comment", native), (platform, root)
