"""Pinned yt-dlp hooks: stream native comments without buffering a full list."""

import math
import re
import time
from datetime import datetime, timezone

from Crawler.Backend.crawler_network import SourceBarrier, http_barrier


def root_projection(raw):
    stamp = None
    value = raw.get("timestamp")
    if type(value) in (int, float) and math.isfinite(value):
        try:
            stamp = datetime.fromtimestamp(value, timezone.utc).isoformat()
        except (ValueError, OverflowError, OSError):
            pass
    return dict(
        published_at=stamp,
        title=raw.get("title"),
        text_source=raw.get("description") or "",
    )


def root_filter(raw, selection):
    if selection is None:
        return None
    from Crawler.Backend.Reddit.crawl_reddit_single import KeywordMatcher
    from Crawler.Backend.social_export import root_rejection

    return root_rejection(
        root_projection(raw),
        selection,
        KeywordMatcher(selection["include_keywords"]),
        KeywordMatcher(selection["exclude_keywords"]),
    )


def controlled_youtube_dl(settings, logger, emit):
    import yt_dlp
    from yt_dlp.extractor.youtube import YoutubeIE

    class StreamingYoutubeIE(YoutubeIE):
        @classmethod
        def ie_key(cls):
            return YoutubeIE.ie_key()

        def extract_comments(self, *args, **kwargs):
            if not self.get_param("getcomments") or settings["max_comments"] == 0:
                return None

            def extract():
                seen = set()
                generator = self._get_comments(*args, **kwargs)
                try:
                    for row in generator:
                        if (
                            not isinstance(row, dict)
                            or not isinstance(row.get("id"), str)
                            or not re.fullmatch(r"[A-Za-z0-9_.-]{1,256}", row["id"])
                            or not isinstance(row.get("text"), str)
                            or row["id"] in seen
                        ):
                            continue
                        seen.add(row["id"])
                        emit(
                            "comment",
                            {
                                k: row.get(k)
                                for k in (
                                    "id",
                                    "text",
                                    "parent",
                                    "timestamp",
                                    "_time_text",
                                    "like_count",
                                    "author_id",
                                )
                            },
                        )
                        self._downloader.streamed_comments += 1
                        self._downloader.progress()
                        cap = settings["max_comments"]
                        if cap is not None and len(seen) >= cap:
                            break
                except self.CommentsDisabled:
                    logger.codes.add("COMMENTS_DISABLED")
                finally:
                    close = getattr(generator, "close", None)
                    if close:
                        close()
                # Metadata was already emitted; do not retain full comment bodies.
                return {"comments": [], "comment_count": len(seen)}

            return extract

    class ControlledYoutubeDL(yt_dlp.YoutubeDL):
        streamed_comments = 0
        barrier = None

        def __init__(self, *args, **kwargs):
            self.last_progress = time.monotonic()
            super().__init__(*args, **kwargs)

        def progress(self):
            self.last_progress = time.monotonic()

        def check_barrier(self):
            if self.barrier:
                raise self.barrier
            for code in (
                "LOGIN_OR_CHALLENGE",
                "ACCESS_BLOCKED",
                "RATE_LIMITED",
                "SERVER_UNAVAILABLE",
            ):
                if code in logger.codes:
                    self.barrier = SourceBarrier(
                        code, "youtube_access_or_server_barrier"
                    )
                    raise self.barrier
            if time.monotonic() - self.last_progress >= 75:
                self.barrier = SourceBarrier("PARTIAL", "youtube_native_ids_stagnated")
                raise self.barrier

        def urlopen(self, request):
            self.check_barrier()
            try:
                response = super().urlopen(request)
            except Exception as error:
                current = error
                for _ in range(6):
                    if current is None:
                        break
                    code = getattr(current, "status", None) or getattr(
                        current, "code", None
                    )
                    barrier = http_barrier(code, getattr(current, "headers", None))
                    if barrier:
                        self.barrier = barrier
                        raise barrier from None
                    current = getattr(current, "cause", None) or current.__cause__
                raise
            error = http_barrier(
                getattr(response, "status", None), getattr(response, "headers", None)
            )
            if error:
                self.barrier = error
                response.close()
                raise error
            return response

    return ControlledYoutubeDL, StreamingYoutubeIE
