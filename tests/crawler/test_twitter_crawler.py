"""Offline contracts for Twitter/X acquisition; no live credentials required."""

import asyncio
import json
import os
import tempfile
import time
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from openpyxl import load_workbook

from Crawler.Backend import twitter_crawler as x
from Crawler.Backend.social_crawler import SocialCrawler


def tweet(ident="100", text="Kuliah kampus", parent=None, comments=0):
    return dict(
        tweet_id=ident,
        text=text,
        timestamp="Fri Oct 30 10:00:00 +0000 2026",
        tweet_url=f"https://x.com/example/status/{ident}",
        in_reply_to_tweet_id=parent,
        comments=comments,
        likes=2,
    )


def persistent_worker(options, pipe):
    count = 0
    while pipe.recv() is not None:
        count += 1
        pipe.send(
            ("done", dict(status="FINISHED_BEST_EFFORT", count=count, pid=os.getpid()))
        )


def hanging_worker(options, pipe):
    pipe.recv()
    pipe.send(("record", tweet()))
    time.sleep(20)


class TwitterCrawlerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.cfg = x.standalone_config(None, "twitter")
        self.cfg["total_seconds"] = 1800
        self.cfg["until"] = "2026-11-03T00:00:00+07:00"
        self.cfg["exclude_existing_datasets"] = []
        self.cfg["delay"]["seconds"] = 0
        self.cfg["platforms"]["twitter"].update(
            queries=["kuliah"], min_posts=1, max_posts=2, max_searches=1
        )
        self.cfg["scweet"].update(
            auth_file=str(self.path / "auth.json"), state_dir=str(self.path / "state")
        )

    def test_plan_never_reads_auth_or_contacts_network(self):
        with patch.object(x, "auth_material", side_effect=AssertionError("auth read")):
            plan = x.TwitterCrawler(self.cfg).plan()
        self.assertEqual(plan["config"]["total_seconds"], 1800)
        self.assertFalse(plan["live_access_verified"])
        self.assertTrue(plan["integrated_into_social_crawler"])
        self.assertEqual(plan["primary_output"]["columns"], list(x.COMPACT_COLUMNS))

    def test_calendar_windows_have_no_duplicate_days_or_coverage_gaps(self):
        from datetime import date, timedelta

        cfg = deepcopy(self.cfg)
        cfg.update(since="2026-01-01T10:17:00Z", until="2026-01-29T10:17:00Z")
        cfg["platforms"]["twitter"].update(
            max_searches=None, queries=["kuliah", "kampus"]
        )
        targets = list(x.search_targets(x.configuration(cfg)))
        for query in ("kuliah", "kampus"):
            windows = [t for t in targets if t["query"] == query]
            self.assertEqual(len(windows), 4)
            days = []
            for current, following in zip(windows, windows[1:]):
                self.assertEqual(current["since"], following["until"])
            for window in windows:
                begin, end = (
                    date.fromisoformat(window["since"]),
                    date.fromisoformat(window["until"]),
                )
                days.extend(
                    begin + timedelta(days=i) for i in range((end - begin).days)
                )
            self.assertEqual(len(days), 29)
            self.assertEqual(len(set(days)), 29)
            self.assertEqual(
                (min(days), max(days)), (date(2026, 1, 1), date(2026, 1, 29))
            )

    def test_social_filters_cached_roots_before_requesting_replies(self):
        for field, value, reason in (
            ("timestamp", "2024-01-01T00:00:00Z", "root_outside_date_window"),
            ("text", "jual ikan segar", "root_missing_include_keyword"),
        ):
            with self.subTest(field=field):
                calls = []

                def worker(operation, target, seconds, emit):
                    calls.append(operation)
                    self.assertEqual(
                        operation, "search", "filtered roots must not fetch replies"
                    )
                    emit({**tweet(comments=100), field: value})
                    emit(tweet("200"))
                    return dict(status="FINISHED_BEST_EFFORT", warnings=[])

                adapter = x.TwitterCoordinatorWorker({}, worker=worker)
                report = SocialCrawler(self.cfg, workers={"twitter": adapter}).run(
                    self.path / ("filter-" + field)
                )
                self.assertEqual(calls, ["search"])
                self.assertEqual(report["platforms"]["twitter"]["posts_exported"], 1)
                self.assertEqual(
                    report["platforms"]["twitter"]["filtered_roots"], {reason: 1}
                )

    def test_social_server_pause_retains_root_and_stops_before_next_post(self):
        calls = []
        cfg = deepcopy(self.cfg)
        cfg["platforms"]["twitter"].update(min_posts=2, max_posts=2)

        def worker(operation, target, seconds, emit):
            calls.append(operation)
            if operation == "search":
                emit(tweet(comments=100))
                emit(tweet("200"))
                return dict(status="FINISHED_BEST_EFFORT", warnings=[])
            return dict(
                status="SERVER_UNAVAILABLE", retry_after_seconds=120, warnings=[]
            )

        adapter = x.TwitterCoordinatorWorker({}, worker=worker)
        report = SocialCrawler(cfg, workers={"twitter": adapter}).run(
            self.path / "server-pause"
        )
        self.assertEqual(calls, ["search", "replies"])
        self.assertEqual(report["platforms"]["twitter"]["posts_exported"], 1)
        self.assertEqual(
            report["platforms"]["twitter"]["stop_reason"], "SERVER_UNAVAILABLE"
        )

    def test_server_failure_honors_retry_after_and_stops_further_requests(self):
        from curl_cffi.requests import Session

        options = x.configuration(self.cfg)["scweet"]
        Path(options["state_dir"]).mkdir()
        response = SimpleNamespace(
            status_code=503, url="https://x.com/test", headers={"retry-after": "120"}
        )
        with patch.object(Session, "request", return_value=response) as original:
            with x.guarded_transport(options) as state:
                Session().get("https://x.com/test")
                with self.assertRaises(x.AccessBarrier) as raised:
                    Session().get("https://x.com/test")
        self.assertEqual(raised.exception.status, "SERVER_UNAVAILABLE")
        self.assertEqual(state["requests"], 1)
        original.assert_called_once()
        saved = json.loads((Path(options["state_dir"]) / "barrier.json").read_text())
        self.assertEqual(saved["status"], "SERVER_UNAVAILABLE")
        self.assertGreater(saved["not_before"], time.time() + 119)

    def test_expired_server_pause_allows_client_without_resetting_account_state(self):
        options = x.configuration(self.cfg)["scweet"]
        directory = Path(options["state_dir"])
        directory.mkdir()
        Path(options["auth_file"]).write_text(
            json.dumps(
                [dict(sosmed="twitter", username="example", sessionid="fixture")]
            )
        )
        x.private_json(
            directory / "barrier.json",
            dict(status="SERVER_UNAVAILABLE", not_before=time.time() - 1),
        )
        client = Mock()
        client._accounts_repo.eligibility_diagnostics.return_value = {"eligible": 1}
        with (
            patch("Scweet.Scweet", return_value=client),
            patch("Crawler.Backend.scweet_limits.configure_daily_quotas"),
        ):
            self.assertIs(x.create_client(options), client)

    def test_social_coordinator_uses_cached_search_root_and_native_replies(self):
        calls = []

        def worker(operation, target, seconds, emit):
            calls.append(operation)
            if operation == "search":
                emit(tweet(comments=2))
                emit(tweet("101", parent="100"))  # Not a new root.
            else:
                self.assertEqual(target["tweet_id"], "100")
                emit(tweet("101", parent="100"))
                emit(tweet("102", parent="101"))
            return dict(status="FINISHED_BEST_EFFORT", warnings=[])

        adapter = x.TwitterCoordinatorWorker({}, worker=worker)
        crawler = SocialCrawler(self.cfg, workers={"twitter": adapter})
        report = crawler.run(self.path / "social")
        self.assertEqual(calls, ["search", "replies"])
        summary = report["platforms"]["twitter"]
        self.assertEqual(
            (summary["qualified_posts"], summary["comments"], summary["replies"]),
            (1, 1, 1),
        )
        rows = [
            json.loads(line)
            for line in (self.path / "social/Contents.jsonl").read_text().splitlines()
        ]
        self.assertEqual(
            {row["object_key"] for row in rows},
            {x.object_key(n) for n in ("100", "101", "102")},
        )
        self.assertEqual(rows[2]["parent_key"], x.object_key("101"))
        book = load_workbook(self.path / "social/social_data.xlsx", read_only=True)
        self.assertEqual(len(list(book["Data"].values)), 4)
        book.close()

    def test_social_coordinator_stops_on_actual_rate_limit_with_partial_root(self):
        def worker(operation, target, seconds, emit):
            if operation == "search":
                emit(tweet(comments=1))
                return dict(status="FINISHED_BEST_EFFORT", warnings=[])
            return dict(status="RATE_LIMITED", retry_after_seconds=900, warnings=[])

        adapter = x.TwitterCoordinatorWorker({}, worker=worker)
        report = SocialCrawler(self.cfg, workers={"twitter": adapter}).run(
            self.path / "limited"
        )
        self.assertEqual(report["platforms"]["twitter"]["stop_reason"], "RATE_LIMITED")
        self.assertEqual(report["platforms"]["twitter"]["posts_exported"], 1)
        self.assertEqual(report["status"], "PARTIAL")

    def test_social_cooldown_keeps_partial_root_and_resumes_new_children_once(self):
        now, reply_calls = [0], []
        cfg = deepcopy(self.cfg)
        cfg["platforms"]["twitter"].update(min_posts=2, max_posts=2)

        def worker(operation, target, seconds, emit):
            if operation == "search":
                emit(tweet(comments=1))
                emit(tweet("200"))
            else:
                reply_calls.append(target["tweet_id"])
                if len(reply_calls) == 1:
                    return dict(status="COOLDOWN", retry_after_seconds=20, warnings=[])
                emit(tweet("101", parent="100"))
                emit(tweet("101", text="Updated duplicate", parent="100"))
            return dict(status="FINISHED_BEST_EFFORT", warnings=[])

        adapter = x.TwitterCoordinatorWorker(
            {}, worker=worker, monotonic=lambda: now[0]
        )
        crawler = SocialCrawler(
            cfg,
            workers={"twitter": adapter},
            monotonic=lambda: now[0],
            sleep=lambda seconds: now.__setitem__(0, now[0] + seconds),
        )
        report = crawler.run(self.path / "cooldown")
        summary = report["platforms"]["twitter"]
        self.assertEqual(
            (summary["posts_exported"], summary["comments"], summary["cooldown_waits"]),
            (2, 1, 1),
        )
        self.assertEqual(reply_calls, ["100", "100"])
        self.assertEqual(now[0], 20)
        self.assertEqual(report["status"], "TARGET_MET")

    def test_cached_root_without_comments_does_not_consume_network_delay(self):
        cfg = deepcopy(self.cfg)
        cfg["delay"]["seconds"] = 15
        sleeps = []

        def worker(operation, target, seconds, emit):
            self.assertEqual(operation, "search")
            emit(tweet())
            return dict(status="FINISHED_BEST_EFFORT", warnings=[])

        adapter = x.TwitterCoordinatorWorker({}, worker=worker)
        report = SocialCrawler(
            cfg, workers={"twitter": adapter}, sleep=sleeps.append
        ).run(self.path / "cache")
        self.assertEqual(report["status"], "TARGET_MET")
        self.assertEqual(sleeps, [])

    def test_social_comment_thread_budget_prioritizes_root_acquisition(self):
        cfg = deepcopy(self.cfg)
        cfg["platforms"]["twitter"].update(
            min_posts=2, max_posts=2, max_comment_threads=1
        )
        calls = []

        def worker(operation, target, seconds, emit):
            calls.append(operation)
            if operation == "search":
                emit(tweet("100", comments=2))
                emit(tweet("200", comments=2))
            else:
                emit(tweet("101", parent="100"))
            return dict(status="FINISHED_BEST_EFFORT", warnings=[])

        adapter = x.TwitterCoordinatorWorker({}, worker=worker)
        crawler = SocialCrawler(cfg, workers={"twitter": adapter})
        # Effective settings remain valid input, including coordinator defaults.
        SocialCrawler(crawler.config, workers={"twitter": adapter}).plan()
        report = crawler.run(self.path / "sampled")
        self.assertEqual(calls, ["search", "replies"])
        self.assertEqual(report["platforms"]["twitter"]["posts_exported"], 2)
        self.assertEqual(report["platforms"]["twitter"]["comments"], 1)

    def test_social_baseline_excludes_x_ids_previously_exported_as_comments(self):
        def first_worker(operation, target, seconds, emit):
            if operation == "search":
                emit(tweet(comments=1))
            else:
                emit(tweet("101", parent="100"))
            return dict(status="FINISHED_BEST_EFFORT", warnings=[])

        original = self.path / "historical"
        SocialCrawler(
            self.cfg,
            workers={"twitter": x.TwitterCoordinatorWorker({}, worker=first_worker)},
        ).run(original)
        cfg = deepcopy(self.cfg)
        cfg["exclude_existing_datasets"] = [str(original)]
        cfg["platforms"]["twitter"].update(
            queries=[], urls=["https://x.com/i/web/status/101"]
        )
        forbidden = Mock(
            side_effect=AssertionError("Existing native ID must not be fetched")
        )
        report = SocialCrawler(cfg, workers={"twitter": forbidden}).run(
            self.path / "excluded"
        )
        forbidden.assert_not_called()
        self.assertEqual(report["platforms"]["twitter"]["existing_posts_skipped"], 1)
        self.assertEqual(report["platforms"]["twitter"]["posts_exported"], 0)

    def test_validation_rejects_embedded_secrets_and_other_platforms(self):
        for change in (
            {"auth_token": "secret"},
            {"scweet": {"sessionid": "secret"}},
            {"platforms": {"instagram": {}}},
            {"total_seconds": True},
            {"since": "2027-01-01T00:00:00Z"},
        ):
            with self.subTest(change=list(change)), self.assertRaises(ValueError):
                x.configuration({**self.cfg, **change})

    def test_auth_alias_and_local_secret_errors_are_not_values(self):
        path = self.path / "auth.json"
        path.write_text(
            json.dumps(
                [
                    dict(sosmed="instagram", sessionid="other"),
                    dict(
                        sosmed="twitter", username="@example", sessionid="local-secret"
                    ),
                ]
            )
        )
        self.assertEqual(
            x.auth_material(path), ("example", {"auth_token": "local-secret"})
        )
        path.write_text(
            json.dumps(
                [dict(sosmed="twitter", username="example", sessionid="bad\nsecret")]
            )
        )
        with self.assertRaises(ValueError) as caught:
            x.auth_material(path)
        self.assertNotIn("bad", str(caught.exception))

    def test_native_identity_parentage_and_unknown_dates(self):
        root = x.normalize_item(tweet())
        direct = x.normalize_item(tweet("101", parent="100"), root_id="100")
        nested = x.normalize_item(tweet("102", parent="101"), root_id="100")
        self.assertEqual(root.published_at, "2026-10-30T10:00:00+00:00")
        self.assertEqual(direct.object_type, "comment")
        self.assertEqual(nested.object_type, "reply")
        self.assertEqual(nested.parent_key, x.object_key("101"))
        self.assertEqual(nested.thread_root_key, x.object_key("100"))
        self.assertFalse(root.text_complete)
        with self.assertRaises(ValueError):
            x.normalize_item(tweet("101"), root_id="100")
        bad = tweet()
        bad["timestamp"] = "recently"
        self.assertEqual(x.normalize_item(bad).timestamp_quality, "unknown")
        bad["tweet_url"] = "https://x.com/example/status/999"
        with self.assertRaises(ValueError):
            x.normalize_item(bad)

    def test_shared_workbook_baseline_excludes_posts_and_replies_and_checks_identity(
        self,
    ):
        from openpyxl import Workbook

        folder = self.path / "baseline"
        folder.mkdir()
        path = folder / "dataset.xlsx"
        book = Workbook()
        sheet = book.active
        sheet.title = "Contents"
        sheet.append(["platform", "object_type", "native_id", "canonical_url"])
        sheet.append(["youtube", "post", "AAAAAAAAAAA", "https://youtu.be/AAAAAAAAAAA"])
        for native, kind in (("100", "post"), ("101", "comment"), ("102", "reply")):
            sheet.append(
                ["twitter", kind, native, "https://x.com/i/web/status/" + native]
            )
        book.save(path)
        for supplied in (path, folder):
            with self.subTest(baseline=supplied):
                cfg = deepcopy(self.cfg)
                cfg["exclude_existing_datasets"] = [str(supplied)]
                keys, sources = x.TwitterCrawler(cfg)._baseline()
                self.assertEqual(keys, {x.object_key(n) for n in ("100", "101", "102")})
                self.assertEqual(sources[0]["path"], str(path.resolve()))
                self.assertEqual(len(sources[0]["sha256"]), 64)
        sheet.cell(3, 4).value = "https://x.com/i/web/status/999"
        book.save(path)
        book.close()
        with self.assertRaisesRegex(ValueError, "native ID and URL disagree"):
            x.TwitterCrawler(cfg)._baseline()

    def test_url_canonicalization_rejects_foreign_hosts_and_credentials(self):
        self.assertEqual(
            x.post_url("https://twitter.com/example/status/100?s=20"),
            "https://x.com/i/web/status/100",
        )
        for url in (
            "https://x.com.evil.org/example/status/100",
            "http://x.com/example/status/100",
            "https://secret@x.com/example/status/100",
            "https://x.com/example/status/not-id",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                x.post_url(url)

    def test_shared_excel_dedup_formula_safety_parent_relations_and_manifest(self):
        def worker(operation, target, seconds, emit):
            if operation == "search":
                for row in [tweet(text="=kuliah kampus", comments=3)] * 2 + [
                    tweet("110", "politik kuliah"),
                    tweet("111", parent="109"),
                ]:
                    emit(row)
            else:
                for row in [
                    tweet("101", "Biaya kuliah?", "100"),
                    tweet("102", "Beasiswa", "101"),
                    tweet("101", "edit duplicate", "100"),
                ]:
                    emit(row)
            return dict(status="FINISHED_BEST_EFFORT", reason="fixture", warnings=[])

        output = self.path / "export"
        summary = x.TwitterCrawler(self.cfg, worker=worker).run(output)
        self.assertEqual(
            (summary["posts_exported"], summary["comments"], summary["replies"]),
            (1, 1, 1),
        )
        self.assertEqual(summary["duplicates_skipped"], 2)
        self.assertFalse(summary["live_access_verified"])
        self.assertFalse(summary["trial_passed"])
        compact = load_workbook(output / x.COMPACT_FILE)
        self.assertEqual(compact.sheetnames, ["Data"])
        self.assertEqual(tuple(c.value for c in compact["Data"][1]), x.COMPACT_COLUMNS)
        self.assertEqual(compact["Data"]["H2"].data_type, "s")
        self.assertEqual(compact["Data"].max_row, 4)
        compact.close()
        audit = load_workbook(output / "dataset.xlsx", read_only=True)
        self.assertEqual(audit.sheetnames, list(x.contract.TABLES))
        audit.close()
        rows = [
            json.loads(line)
            for line in (output / "Contents.jsonl").read_text().splitlines()
        ]
        self.assertEqual(len({r["native_id"] for r in rows}), 3)
        relations = [
            json.loads(line)
            for line in (output / "Relations.jsonl").read_text().splitlines()
        ]
        self.assertTrue(
            all(r["resolution_status"] == "resolved_in_export" for r in relations)
        )
        manifest = json.loads((output / "manifest.json").read_text())
        for name, digest in manifest["files_sha256"].items():
            self.assertEqual(x.sha256((output / name).read_bytes()).hexdigest(), digest)
        again = deepcopy(self.cfg)
        again["exclude_existing_datasets"] = [str(output)]
        skipped = x.TwitterCrawler(again, worker=worker).run(self.path / "baseline")
        self.assertEqual(skipped["posts_exported"], 0)
        self.assertGreater(skipped["existing_records_skipped"], 0)

    def test_barrier_keeps_partial_records_and_stops_remaining_operations(self):
        worker = Mock(
            side_effect=lambda operation, target, seconds, emit: (
                emit(tweet(comments=1))
                or dict(
                    status="RATE_LIMITED",
                    reason="fixture",
                    warnings=[],
                    http_status=429,
                )
            )
        )
        summary = x.TwitterCrawler(self.cfg, worker=worker).run(self.path / "limited")
        self.assertEqual(worker.call_count, 1)
        self.assertEqual(summary["stop_reason"], "RATE_LIMITED")
        self.assertEqual(summary["posts_exported"], 1)
        self.assertFalse(summary["trial_passed"])
        self.assertTrue((self.path / "limited/social_data.xlsx").exists())

    def test_time_budget_caps_operations_and_preserves_records(self):
        now = [0.0]
        self.cfg["total_seconds"] = 2

        def worker(operation, target, seconds, emit):
            self.assertEqual(seconds, 2)
            emit(tweet())
            now[0] += seconds
            return dict(status="FINISHED_BEST_EFFORT", reason="fixture", warnings=[])

        summary = x.TwitterCrawler(
            self.cfg, worker=worker, monotonic=lambda: now[0]
        ).run(self.path / "budget")
        self.assertEqual(summary["stop_reason"], "TIME_BUDGET_EXHAUSTED")
        self.assertEqual(summary["posts_exported"], 1)

    def test_library_cooldown_waits_then_retries_same_operation_within_budget(self):
        now, calls = [0.0], []

        def worker(operation, target, seconds, emit):
            calls.append((operation, target))
            if len(calls) == 1:
                return dict(
                    status="COOLDOWN",
                    reason="scweet_account_cooldown",
                    retry_after_seconds=3,
                    warnings=[],
                )
            emit(tweet())
            return dict(status="FINISHED_BEST_EFFORT", reason="fixture", warnings=[])

        summary = x.TwitterCrawler(
            self.cfg,
            worker=worker,
            monotonic=lambda: now[0],
            sleep=lambda seconds: now.__setitem__(0, now[0] + seconds),
        ).run(self.path / "cooldown")
        self.assertEqual(calls[0], calls[1])
        self.assertEqual(summary["cooldown_waits"], 1)
        self.assertEqual(summary["cooldown_seconds"], 3)
        self.assertEqual(summary["posts_exported"], 1)
        self.assertEqual(now[0], 3)

    def test_interrupt_during_delay_finalizes_partial_excel(self):
        self.cfg["delay"]["seconds"] = 15

        def worker(operation, target, seconds, emit):
            emit(tweet(comments=1))
            return dict(status="FINISHED_BEST_EFFORT", reason="fixture", warnings=[])

        crawler = x.TwitterCrawler(
            self.cfg, worker=worker, sleep=Mock(side_effect=KeyboardInterrupt)
        )
        summary = crawler.run(self.path / "interrupt")
        self.assertEqual(summary["stop_reason"], "INTERRUPTED")
        self.assertTrue(summary["interrupted"])
        self.assertEqual(summary["posts_exported"], 1)
        self.assertTrue((self.path / "interrupt/social_data.xlsx").exists())

    def test_pool_diagnostics_expose_wait_only_and_keep_daily_cap_terminal(self):
        client = Mock()
        client._accounts_repo.eligibility_diagnostics.return_value = dict(
            blocked_counts={"cooldown": 1},
            blocked_samples=[dict(available_til=time.time() + 60, username="hidden")],
        )
        result = x.account_cooldown(client, dict(status="ACCOUNT_UNAVAILABLE"))
        self.assertEqual(result["status"], "COOLDOWN")
        self.assertNotIn("hidden", json.dumps(result))
        client._accounts_repo.eligibility_diagnostics.return_value["blocked_counts"][
            "daily_limit"
        ] = 1
        self.assertEqual(
            x.account_cooldown(client, dict(status="ACCOUNT_UNAVAILABLE"))["status"],
            "ACCOUNT_UNAVAILABLE",
        )

    def test_persistent_subprocess_reuses_one_pid(self):
        worker = x.ScweetWorker({}, target=persistent_worker)
        self.addCleanup(worker.close)
        first = worker("search", {}, 5, Mock())
        second = worker("search", {}, 5, Mock())
        self.assertEqual(first["pid"], second["pid"])
        self.assertEqual(second["count"], 2)

    def test_deadline_kills_owned_worker_and_retains_streamed_rows(self):
        worker = x.ScweetWorker({}, target=hanging_worker)
        self.addCleanup(worker.close)
        rows = []
        result = worker("search", {}, 1, rows.append)
        self.assertEqual(result["status"], "TIMEOUT")
        self.assertEqual(len(rows), 1)
        self.assertIsNone(worker.process)

    def test_429_retry_headers_and_http200_challenge(self):
        response = SimpleNamespace(
            status_code=429,
            url="https://x.com/i/api/graphql/test",
            headers={"Retry-After": "360"},
        )
        barrier = x.response_barrier(response)
        self.assertEqual(
            (barrier.status, barrier.retry_after_seconds), ("RATE_LIMITED", 360)
        )
        response.status_code = 200
        response.headers = {"content-type": "application/json"}
        response.json = lambda: {"errors": [{"code": 326, "message": "sensitive"}]}
        self.assertEqual(x.response_barrier(response).status, "CHALLENGE_REQUIRED")
        self.assertNotIn(
            "sensitive", json.dumps(x.error_receipt(x.response_barrier(response)))
        )

    def test_saved_state_reuses_account_without_resetting_counters(self):
        options = x.configuration(self.cfg)["scweet"]
        directory = Path(options["state_dir"])
        directory.mkdir()
        Path(options["auth_file"]).write_text(
            json.dumps(
                [dict(sosmed="twitter", username="example", sessionid="test-token")]
            )
        )
        (directory / "state.db").touch()
        x.private_json(
            directory / "identity.json",
            dict(username="example", token_sha256=x.sha256(b"test-token").hexdigest()),
        )
        client = Mock()
        client._accounts_repo.eligibility_diagnostics.return_value = {"eligible": 1}
        with (
            patch("Scweet.Scweet", return_value=client) as constructor,
            patch("Crawler.Backend.scweet_limits.configure_daily_quotas") as quotas,
        ):
            self.assertIs(x.create_client(options), client)
        quotas.assert_called_once_with(client, None, None)
        self.assertFalse(constructor.call_args.kwargs["provision"])
        self.assertIsNone(constructor.call_args.kwargs["cookies"])
        x.private_json(
            directory / "identity.json", dict(username="other", token_sha256="other")
        )
        with patch("Scweet.Scweet") as constructor, self.assertRaises(ValueError):
            x.create_client(options)
        constructor.assert_not_called()

    def test_saved_429_and_login_barriers_prevent_new_network_clients(self):
        options = x.configuration(self.cfg)["scweet"]
        directory = Path(options["state_dir"])
        directory.mkdir()
        Path(options["auth_file"]).write_text(
            json.dumps(
                [dict(sosmed="twitter", username="example", sessionid="test-token")]
            )
        )
        for status, not_before in [
            ("RATE_LIMITED", time.time() + 600),
            ("LOGIN_REQUIRED", time.time() - 600),
        ]:
            x.private_json(
                directory / "barrier.json",
                dict(
                    status=status,
                    http_status=429 if status == "RATE_LIMITED" else 401,
                    not_before=not_before,
                ),
            )
            with (
                self.subTest(status=status),
                patch("Scweet.Scweet") as constructor,
                self.assertRaises(x.AccessBarrier),
            ):
                x.create_client(options)
            constructor.assert_not_called()

    def test_transport_stops_all_network_after_first_429_sync_and_async(self):
        from curl_cffi.requests import AsyncSession, Session

        options = x.configuration(self.cfg)["scweet"]
        Path(options["state_dir"]).mkdir()
        response = SimpleNamespace(
            status_code=429, url="https://x.com/test", headers={"retry-after": "1200"}
        )
        original = Mock(return_value=response)
        with (
            patch.object(Session, "request", original),
            x.guarded_transport(options) as state,
        ):
            Session().get("https://x.com/test")
            with self.assertRaises(x.AccessBarrier):
                Session().get("https://x.com/test")
            with self.assertRaises(x.AccessBarrier):
                asyncio.run(AsyncSession().get("https://x.com/test"))
        self.assertEqual(original.call_count, 1)
        self.assertEqual(state["http_status_counts"], {"429": 1})
        saved = json.loads((Path(options["state_dir"]) / "barrier.json").read_text())
        self.assertGreater(saved["not_before"], time.time() + 1190)


if __name__ == "__main__":
    unittest.main()
