"""Verify the supplied browser-style patch without sending network requests."""

import unittest
from types import SimpleNamespace as Obj
from unittest.mock import Mock

import requests
from instaloader import InstaloaderContext
from instaloader.exceptions import AbortDownloadException, TooManyRequestsException

from Crawler.Backend import instaloader_browser_patch as bp


def response(code=200, data=None, text=""):
    result = Mock(status_code=code, text=text)
    result.json.return_value = data or {}
    return result


def context(label):
    cookies = requests.cookies.cookiejar_from_dict(
        dict(sessionid=label, csrftoken="csrf-" + label)
    )
    html = f'"LSD",[],{{"token":"lsd-{label}"}} "DTSGInitialData",[],{{"token":"dtsg-{label}"}} jazoest=123 "actorID":"9" "rev":1'
    session = Mock(cookies=cookies)
    session.get.return_value = response(text=html)
    session.post.return_value = response(data={"data": {}})
    return Obj(
        _session=session,
        user_agent="Mozilla/5.0 (Macintosh) Chrome/142.0.0.0",
        request_timeout=5,
        do_sleep=Mock(),
        _rate_controller=Mock(),
    )


class BrowserPatchTests(unittest.TestCase):
    def test_required_web_tokens_headers_endpoint_and_four_argument_signature(self):
        original = InstaloaderContext.doc_id_graphql_query
        ctx = context("first")
        bp.apply_browser_patch(ctx)
        ctx.doc_id_graphql_query(
            "27128499623469141",
            {"shortcode": "B"},
            "https://www.instagram.com/p/B/",
            True,
        )
        call = ctx._session.post.call_args
        self.assertEqual(call.args[0], "https://www.instagram.com/api/graphql")
        body, headers = call.kwargs["data"], call.kwargs["headers"]
        self.assertEqual(
            (body["fb_dtsg"], body["lsd"], body["jazoest"]),
            ("dtsg-first", "lsd-first", "123"),
        )
        self.assertEqual(headers["x-fb-lsd"], "lsd-first")
        self.assertEqual(headers["x-fb-friendly-name"], "PolarisPostRootQuery")
        self.assertEqual(headers["x-csrftoken"], "csrf-first")
        self.assertEqual(headers["sec-ch-ua-platform"], '"macOS"')
        self.assertIn("x-asbd-id", headers)
        self.assertIs(InstaloaderContext.doc_id_graphql_query, original)
        ctx._rate_controller.wait_before_query.assert_any_call("other")
        ctx._rate_controller.wait_before_query.assert_any_call("27128499623469141")

    def test_token_cache_is_scoped_to_context_and_invalidated_by_cookie_change(self):
        one, two = context("one"), context("two")
        for ctx in (one, two):
            bp.apply_browser_patch(ctx)
            ctx.doc_id_graphql_query("doc", {})
        one.doc_id_graphql_query("doc", {})
        one._session.get.assert_called_once()
        self.assertEqual(two._session.post.call_args.kwargs["data"]["lsd"], "lsd-two")
        one._session.cookies.set("sessionid", "changed")
        one.doc_id_graphql_query("doc", {})
        self.assertEqual(one._session.get.call_count, 2)

    def test_no_retry_and_no_response_body_in_errors(self):
        for code, exception in (
            (429, TooManyRequestsException),
            (400, AbortDownloadException),
        ):
            with self.subTest(code=code):
                ctx = context("fixture")
                ctx._session.post.return_value = response(
                    code, {"message": "feedback_required"}, "sensitive-private-response"
                )
                bp.apply_browser_patch(ctx)
                with self.assertRaises(exception) as caught:
                    ctx.doc_id_graphql_query("doc", {})
                ctx._session.post.assert_called_once()
                self.assertNotIn("sensitive-private-response", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
