"""Nullable application limits; network timeouts and pacing stay independent."""

import math


def reached(count, limit):
    return limit is not None and count >= limit


def remaining(limit, count=0):
    return None if limit is None else max(0, limit - count)


def cap(*limits):
    finite = [value for value in limits if value is not None]
    return min(finite) if finite else None


def deadline_after(now, seconds):
    return math.inf if seconds is None else now + seconds


def remaining_seconds(deadline, now):
    return None if math.isinf(deadline) else round(max(0, deadline - now), 2)
