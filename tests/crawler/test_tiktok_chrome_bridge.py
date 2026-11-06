"""Task isolation, real loopback transport and streamed export contracts."""

import json
import re
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from Crawler.Backend import tiktok_crawler as t
from Crawler.Backend.crawler_config import read_config
from Crawler.Backend.Tiktok.chrome_bridge import (
    COMMENT_PROTOCOL,
    LIVE_METHOD,
    ChromeLiveWorker,
)


def post():
    return dict(
        id="100",
        link="https://www.tiktok.com/@example/video/100",
        description="Kuliah kampus",
        created_at="2026-06-01T00:00:00Z",
        stats={"like_count": "15"},
    )


class ChromeBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.worker = ChromeLiveWorker()
        self.worker.cooldown_file = Path(self.temporary.name) / "cooldown.json"
        self.addCleanup(self.worker.close)
        self.settings = SimpleNamespace(
            **{**t.DEFAULTS, "max_comments": None, "max_replies": None}
        )
        self.rows = []

    def api(
        self,
        path,
        data=None,
        *,
        origin=None,
        code=None,
        method=None,
        client_headers=None,
    ):
        headers = {
            "Origin": origin or self.worker.extension_origin,
            "Authorization": "Bearer " + (code or self.worker.nonce),
            "Content-Type": "application/json",
            "X-BeeSense-Connector-Version": "1.3.0",
            "X-BeeSense-Connector-Build": "test-comments-v2",
            "X-BeeSense-Comment-Policy": COMMENT_PROTOCOL,
        }
        if client_headers is not None:
            headers = {
                k: v for k, v in headers.items() if not k.startswith("X-BeeSense-")
            }
            headers.update(client_headers)
        return urlopen(
            Request(
                self.worker.origin + path,
                data=json.dumps(data).encode() if data is not None else None,
                headers=headers,
                method=method,
            )
        )

    def test_extension_pairing_auth_and_live_json_result(self):
        self.worker.extension_mode = True
        for origin, code in [("https://www.tiktok.com", None), (None, "invalid")]:
            with self.assertRaises(HTTPError) as error:
                self.api("/api/task", origin=origin, code=code)
            self.assertEqual(error.exception.code, 403)
        self.assertFalse(self.worker.connected.is_set())
        with self.api("/api/task", method="OPTIONS") as response:
            self.assertEqual(response.status, 204)
            self.assertEqual(
                response.headers["Access-Control-Allow-Origin"],
                self.worker.extension_origin,
            )
        oid = self.begin()
        with self.api("/api/task") as response:
            task = json.load(response)
            self.assertEqual(task["operation_id"], oid)
            self.assertTrue(task["collect_all_comments"])
        self.assertTrue(self.worker.connected.is_set())
        self.worker.wait_for_extension(seconds=0.1)
        with self.api(
            "/api/result",
            dict(
                operation_id=oid,
                done=True,
                collection_status="exhausted",
                events=[dict(kind="record", payload=post())],
            ),
        ) as response:
            self.assertEqual(response.status, 200)
        self.runner.join(2)
        self.assertEqual(self.rows[0][1]["id"], "100")

    def test_reconnected_connector_resumes_same_task_without_duplicate_ids(self):
        self.worker.extension_mode = True
        oid = self.begin()
        events = [dict(kind="record", payload=post())]
        with self.api(
            "/api/result", dict(operation_id=oid, done=False, events=events)
        ) as response:
            self.assertEqual(response.status, 200)
        headers = {
            "X-BeeSense-Connector-Version": "1.3.0",
            "X-BeeSense-Connector-Build": "20261106-throughput-v6",
            "X-BeeSense-Comment-Policy": COMMENT_PROTOCOL,
        }
        with self.api("/api/task", client_headers=headers) as response:
            self.assertEqual(json.load(response)["operation_id"], oid)
        with self.api(
            "/api/result",
            dict(
                operation_id=oid,
                done=True,
                events=events,
                collection_status="exhausted",
            ),
            client_headers=headers,
        ) as response:
            self.assertEqual(response.status, 200)
        self.runner.join(2)
        self.assertEqual([row[1]["id"] for row in self.rows], ["100"])
        self.assertEqual(self.result[0]["status"], "FINISHED_BEST_EFFORT")
        self.assertEqual(self.worker.client_info["version"], "1.3.0")

    def test_old_or_manifest_only_connector_cannot_start_crawl_clock(self):
        self.worker.extension_mode = True
        for headers in (
            {},
            {"X-BeeSense-Connector-Version": "1.1.0"},
            {
                "X-BeeSense-Connector-Version": "1.2.3",
                "X-BeeSense-Connector-Build": "20261105-comment-viewport-v5",
                "X-BeeSense-Comment-Policy": COMMENT_PROTOCOL,
            },
            {"X-BeeSense-Connector-Version": "1.3.0"},
        ):
            with self.assertRaises(HTTPError) as error:
                self.api("/api/task", client_headers=headers)
            self.assertEqual(error.exception.code, 409)
            self.assertFalse(self.worker.connected.is_set())
        with self.api("/api/task") as response:
            self.assertIsNone(json.load(response))
        self.assertTrue(self.worker.connected.is_set())
        self.assertEqual(self.worker.client_info["comment_policy"], COMMENT_PROTOCOL)

    def test_uncapped_idle_or_missing_completion_evidence_never_counts_as_success(self):
        self.worker.extension_mode = True
        for warnings, evidence, expected in (
            (["visible_pagination_idle"], "exhausted", "CLIENT_UPGRADE_REQUIRED"),
            ([], "pending", "COMMENTS_INCOMPLETE"),
            ([], "exhausted", "FINISHED_BEST_EFFORT"),
        ):
            oid = self.begin()
            self.send(
                oid,
                warnings=warnings,
                collection_status=evidence,
                events=[dict(kind="record", payload=post())],
            )
            self.runner.join(2)
            self.assertEqual(self.result[0]["status"], expected)
            self.assertEqual(self.rows[-1][1]["id"], "100")

    def test_stagnation_receipt_retains_partial_rows_without_stopping_run(self):
        self.worker.extension_mode = True
        oid = self.begin()
        self.assertEqual(self.worker.active["task"]["comment_stagnation_seconds"], 75)
        self.send(
            oid,
            events=[dict(kind="record", payload=post())],
            status="PARTIAL",
            collection_status="stagnated",
            warnings=["comment_stagnation_timeout", "server_error_backoff"],
        )
        self.runner.join(2)
        self.assertEqual(self.result[0]["status"], "PARTIAL")
        self.assertEqual(self.rows[0][1]["id"], "100")
        from Crawler.Backend.social_crawler import STOP_STATUSES

        self.assertNotIn("PARTIAL", STOP_STATUSES)

    def test_extension_api_is_disabled_in_agent_mode(self):
        with self.assertRaises(HTTPError) as error:
            self.api("/api/task")
        self.assertEqual(error.exception.code, 403)

    def test_live_progress_counts_data_before_thread_finishes(self):
        progress = []
        self.worker.progress = progress.append
        oid = self.begin()
        child = dict(
            id="200",
            video_id="100",
            kind="comment",
            text="comment",
            link=post()["link"] + "?comment_id=200",
        )
        self.send(
            oid,
            done=False,
            events=[
                dict(kind="record", payload=post()),
                dict(kind="record", payload=child),
            ],
        )
        deadline = time.monotonic() + 1
        while not progress and time.monotonic() < deadline:
            time.sleep(0.005)
        self.assertEqual(progress[-1]["posts_observed"], 1)
        self.assertEqual(progress[-1]["comments_observed"], 1)
        self.assertEqual(progress[-1]["replies_observed"], 0)
        self.assertIsNotNone(self.worker.active)
        self.send(oid)
        self.runner.join(2)

    def test_rate_limit_survives_next_operation_without_browser_task(self):
        oid = self.begin()
        self.send(oid, status="RATE_LIMITED", retry_after_seconds=120)
        self.runner.join(2)
        self.assertEqual(self.result[0]["retry_after_seconds"], 120)
        receipt = self.worker(
            "search",
            '{"query":"kuliah"}',
            self.settings,
            1,
            lambda *e: self.fail("Unexpected content"),
        )
        self.assertEqual(receipt["status"], "RATE_LIMITED")
        self.assertGreaterEqual(receipt["retry_after_seconds"], 119)
        self.assertIsNone(self.worker.active)

    def test_unlimited_time_task_is_valid_json(self):
        oid = self.begin(seconds=float("inf"))
        task = self.worker.active["task"]
        self.assertIsNone(task["expires_at_unix"])
        json.dumps(task, allow_nan=False)
        self.send(oid)
        self.runner.join(2)

    def test_pairing_timeout_does_not_create_a_crawl_task(self):
        with self.assertRaises(TimeoutError):
            self.worker.wait_for_extension(seconds=0.01)
        self.assertIsNone(self.worker.active)

    def begin(self, operation="thread", seconds=3):
        self.result = []
        target = (
            {"video_id": "100", "cached_root": post()}
            if operation != "search"
            else json.dumps({"query": "kuliah"})
        )
        self.runner = threading.Thread(
            target=lambda: self.result.append(
                self.worker(
                    operation,
                    target,
                    self.settings,
                    seconds,
                    lambda *e: self.rows.append(e),
                )
            )
        )
        self.runner.start()
        deadline = time.monotonic() + 2
        while self.worker.active is None and time.monotonic() < deadline:
            time.sleep(0.005)
        self.assertIsNotNone(self.worker.active)
        return self.worker.active["task"]["operation_id"]

    def send(self, operation_id, events=(), done=True, **kwargs):
        self.worker.submit(
            dict(operation_id=operation_id, events=list(events), done=done, **kwargs)
        )

    def test_http_streams_real_batch_and_retains_rows_on_deadline(self):
        oid = self.begin(seconds=0.3)
        with urlopen(self.worker.bridge_url) as response:
            page = response.read().decode()
        nonce = re.search(r'name="nonce" value="([^"]+)"', page)[1]
        batch = dict(
            operation_id=oid, events=[dict(kind="record", payload=post())], done=False
        )
        body = urlencode(dict(nonce=nonce, batch=json.dumps(batch))).encode()
        request = Request(
            self.worker.origin + "/result",
            data=body,
            headers={"Origin": self.worker.origin},
        )
        with urlopen(request) as response:
            self.assertEqual(response.status, 200)
        self.runner.join(2)
        self.assertEqual(len(self.rows), 1)
        self.assertEqual(self.rows[0][1]["stats"]["like_count"], 15)
        self.assertEqual(self.result[0]["status"], "TIMEOUT")

    def test_http_rejects_foreign_origin_and_bad_nonce(self):
        for origin, nonce in [
            ("https://www.tiktok.com", self.worker.nonce),
            (self.worker.origin, "wrong"),
        ]:
            request = Request(
                self.worker.origin + "/result",
                data=urlencode(dict(nonce=nonce, batch="{}")).encode(),
                headers={"Origin": origin},
            )
            with self.subTest(origin=origin), self.assertRaises(HTTPError) as error:
                urlopen(request)
            self.assertEqual(error.exception.code, 403)
        self.assertEqual(self.worker.received, 0)

    def test_stale_and_wrong_post_batches_are_rejected_atomically(self):
        oid = self.begin()
        for operation_id, events in [
            ("old", []),
            (
                oid,
                [
                    dict(
                        kind="record",
                        payload={
                            **post(),
                            "link": "https://www.tiktok.com/@example/video/999",
                        },
                    )
                ],
            ),
        ]:
            with self.assertRaises(ValueError):
                self.send(operation_id, events)
        self.assertEqual(self.worker.received, 0)
        self.send(oid, [dict(kind="record", payload=post())])
        self.runner.join(2)
        self.assertEqual(len(self.rows), 1)
        with self.assertRaises(ValueError):
            self.send(oid)

    def test_caps_parent_relations_and_duplicate_records(self):
        self.settings.max_replies_per_thread = 1
        oid = self.begin()
        comment = dict(
            id="200",
            video_id="100",
            kind="comment",
            link=post()["link"] + "?comment_id=200",
            text="Komentar",
        )

        def reply(ident, parent="200"):
            return dict(
                id=ident,
                video_id="100",
                kind="reply",
                parent_comment_id=parent,
                link=post()["link"] + "?comment_id=" + ident,
                text="Balasan",
            )

        self.send(
            oid,
            [
                dict(kind="record", payload=p)
                for p in [
                    post(),
                    post(),
                    comment,
                    reply("201"),
                    reply("202"),
                    reply("203", "999"),
                ]
            ],
        )
        self.runner.join(2)
        self.assertEqual([r[1]["id"] for r in self.rows], ["100", "200", "201"])

    def test_streamed_live_worker_uses_common_excel_and_live_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            config = read_config()
            config.update(total_seconds=10, exclude_existing_datasets=[])
            config["delay"]["seconds"] = 0
            config["platforms"]["tiktok"].update(queries=["kuliah"], min_posts=1)
            crawler = t.TikTokCrawler(config, workers={"tiktok": self.worker})
            results = []
            runner = threading.Thread(
                target=lambda: results.append(crawler.run(Path(directory) / "bundle"))
            )
            runner.start()
            handled = set()
            deadline = time.monotonic() + 8
            while runner.is_alive() and time.monotonic() < deadline:
                active = self.worker.active
                if active and active["task"]["operation_id"] not in handled:
                    task = active["task"]
                    oid = task["operation_id"]
                    handled.add(oid)
                    event = (
                        dict(
                            kind="candidate",
                            payload=dict(url=post()["link"], cached_root=post()),
                        )
                        if task["operation"] == "search"
                        else dict(kind="record", payload=post())
                    )
                    self.send(oid, [event])
                time.sleep(0.01)
            runner.join(2)
            self.assertFalse(runner.is_alive())
            self.assertEqual(results[0]["platforms"]["tiktok"]["posts_exported"], 1)
            row = json.loads(
                (Path(directory) / "bundle/Contents.jsonl").read_text().splitlines()[0]
            )
            self.assertEqual(row["extraction_method"], LIVE_METHOD)
            self.assertEqual(row["native_id"], "100")
            self.assertTrue((Path(directory) / "bundle/social_data.xlsx").is_file())
            self.assertEqual(
                crawler.plan()["browser_acquisition"],
                "live_connected_browser_agent_bridge",
            )


if __name__ == "__main__":
    unittest.main()
