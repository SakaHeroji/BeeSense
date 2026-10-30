"""Runtime web GraphQL compatibility patch, adapted from the user's reference.

No installed package is edited. InstaloaderCrawler patches only its own context;
running this module directly patches the separate upstream CLI process instead.
"""

from __future__ import annotations

import hashlib
import json
import re
from types import MethodType

NAMES = {
    "28975909992013618": "PolarisProfilePostsTabContentQuery_connection",
    "29104886249145907": "PolarisProfilePostsTabContentQuery_connection",
    "27128499623469141": "PolarisPostRootQuery",
    "25060748103519434": "PolarisPostCommentsPaginationQuery",
}


def _cookie(context, name):
    return next(
        (c.value for c in context._session.cookies if c.name == name and c.value), ""
    )


def _hints(context):
    agent = context.user_agent
    version = re.search(r"(?:Chrome|Chromium)/(\d+)", agent)
    major = version[1] if version else "142"
    platform = (
        "macOS"
        if "Macintosh" in agent
        else "Windows"
        if "Windows" in agent
        else "Linux"
    )
    return {
        "sec-ch-ua": f'"Chromium";v="{major}", "Not(A:Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": f'"{platform}"',
        "accept-language": "en-US,en;q=0.9",
    }


def _check(response):
    """Keep server response bodies out of upstream CLI exception messages."""
    from instaloader.exceptions import (
        AbortDownloadException,
        ConnectionException,
        QueryReturnedBadRequestException,
        TooManyRequestsException,
    )

    if response.status_code == 429:
        raise TooManyRequestsException("HTTP 429; stop and respect the server cooldown")
    if response.status_code in (401, 403):
        raise AbortDownloadException(f"HTTP {response.status_code}; access rejected")
    if response.status_code == 400:
        try:
            message = response.json().get("message")
        except (ValueError, AttributeError):
            message = None
        if message in (
            "feedback_required",
            "checkpoint_required",
            "challenge_required",
            "login_required",
        ):
            raise AbortDownloadException("GraphQL access rejected: " + message)
        raise QueryReturnedBadRequestException("HTTP 400 from web GraphQL")
    if response.status_code != 200:
        raise ConnectionException(f"HTTP {response.status_code} from Instagram web")


def _pace(context, query_type):
    context.do_sleep()
    context._rate_controller.wait_before_query(query_type)


def _load_tokens(context, fingerprint):
    import requests
    from instaloader.exceptions import BadResponseException, ConnectionException

    _pace(context, "other")
    try:
        page = context._session.get(
            "https://www.instagram.com/",
            headers={
                **_hints(context),
                "accept": "text/html,application/xhtml+xml,*/*",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "upgrade-insecure-requests": "1",
            },
            timeout=context.request_timeout,
            allow_redirects=False,
        )
    except requests.exceptions.RequestException as error:
        raise ConnectionException("Web session page transport failed") from error
    _check(page)

    def grab(*patterns):
        return next((m[1] for p in patterns if (m := re.search(p, page.text))), "")

    tokens = dict(
        lsd=grab(r'"LSD",\[\],\{"token":"([^"]+)"'),
        dtsg=grab(
            r'"DTSGInitialData",\[\],\{"token":"([^"]+)"', r'"dtsg":\{"token":"([^"]+)"'
        ),
        jazoest=grab(r"jazoest=(\d+)", r'"jazoest":"?(\d+)'),
        av=grab(r'"actorID":"(\d+)"', r'"IG_USER_EIMU":"?(\d+)'),
        rev=grab(r'"rev":(\d+)'),
    )
    if not tokens["lsd"] or not tokens["dtsg"]:
        raise BadResponseException("Logged-in page did not supply required web tokens")
    # Scoped to one context and invalidated when its session cookie changes.
    context._beesense_browser_tokens = (fingerprint, tokens)
    return tokens


def browser_graphql_query(context, doc_id, variables, referer=None, web_api=False):
    """Signature accepts the fourth argument added by Instaloader 4.16."""
    import requests
    from instaloader.exceptions import BadResponseException, ConnectionException

    fingerprint = hashlib.sha256(_cookie(context, "sessionid").encode()).hexdigest()
    cached = getattr(context, "_beesense_browser_tokens", None)
    tokens = (
        cached[1]
        if cached and cached[0] == fingerprint
        else _load_tokens(context, fingerprint)
    )
    _pace(context, str(doc_id))
    name = NAMES.get(str(doc_id), "")
    body = {
        "av": tokens["av"],
        "__d": "www",
        "__user": "0",
        "__a": "1",
        "__req": "1",
        "__comet_req": "7",
        "fb_dtsg": tokens["dtsg"],
        "jazoest": tokens["jazoest"],
        "lsd": tokens["lsd"],
        "__rev": tokens["rev"],
        "__spin_r": tokens["rev"],
        "__spin_b": "trunk",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": name,
        "server_timestamps": "true",
        "variables": json.dumps(variables, separators=(",", ":")),
        "doc_id": str(doc_id),
    }
    headers = {
        **_hints(context),
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.instagram.com",
        "referer": referer or "https://www.instagram.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-asbd-id": "359341",
        "x-csrftoken": _cookie(context, "csrftoken"),
        "x-fb-friendly-name": name,
        "x-fb-lsd": tokens["lsd"],
        "x-ig-app-id": "936619743392459",
        "x-ig-max-touch-points": "0",
    }
    try:
        response = context._session.post(
            "https://www.instagram.com/api/graphql",
            data=body,
            headers=headers,
            timeout=context.request_timeout,
            allow_redirects=False,
        )
    except requests.exceptions.RequestException as error:
        raise ConnectionException("Web GraphQL transport failed") from error
    _check(response)
    try:
        data = response.json()
    except ValueError as error:
        raise BadResponseException("Web GraphQL returned non-JSON data") from error
    if not isinstance(data, dict):
        raise BadResponseException("Web GraphQL returned an unexpected JSON shape")
    return data


def apply_browser_patch(context):
    context.doc_id_graphql_query = MethodType(browser_graphql_query, context)


def main():
    from instaloader import InstaloaderContext
    from instaloader.__main__ import main as upstream_main

    InstaloaderContext.doc_id_graphql_query = browser_graphql_query
    return upstream_main()


if __name__ == "__main__":
    raise SystemExit(main())
