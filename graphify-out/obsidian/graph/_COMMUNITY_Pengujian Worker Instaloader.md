---
type: community
cohesion: 0.10
members: 39
---

# Pengujian Worker Instaloader

**Cohesion:** 0.10 - loosely connected
**Members:** 39 nodes

## Members
- [[.adapter()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.setUp()_15]] - code - tests/crawler/test_instaloader_crawler.py
- [[.settings()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_all_main_comments_precede_reply_requests_and_global_cap()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_configuration_rejects_retry_or_unbounded_requests()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_coordinator_stops_at_first_429()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_discovered_post_reuses_metadata_instead_of_shortcode_query()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_duplicate_pages_with_new_cursors_preserve_partial_rows_then_stop()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_filtered_roots_do_not_open_comments()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_hard_deadline_preserves_streamed_events_and_stops_worker()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_http_429_observed_on_copied_sessions_and_not_retried()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_http_503_observed_as_temporary_server_pause()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_last_web_page_requests_only_remaining_comments()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_lazy_answers_reuse_embedded_page_without_extra_request()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_legacy_graphql_comments_do_not_take_the_mobile_branch()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_local_session_reuse_and_owner_only_json_persistence()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_login_redirect_and_structured_challenge_stop()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_malformed_saved_cooldown_fails_before_starting_worker()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_mismatched_shortcode_rejected_before_emission()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_normalization_and_caps_preserve_native_parents_and_utc()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_persisted_cooldown_blocks_new_worker_without_network()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_persistent_worker_retains_process_between_operations()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_rate_limited_context_waits_for_coordinator_without_recreating_session()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_real_loader_keeps_builtin_throttling_and_disables_retries()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_repeated_cursor_does_not_report_exhaustion()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_reply_iterator_does_not_query_when_replies_disabled()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_search_retains_iterator_without_fetching_one_extra()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_server_failure_persists_pause_before_any_new_worker()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_shared_excel_export_provenance_and_baseline_deduplication()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_upstream_abort_is_terminal_and_diagnostics_exclude_error_text()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_web_comments_pagination_ids_and_previews_do_not_use_mobile()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_web_graphql_applies_supplied_patch_only_to_owned_context()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.test_zero_comment_cap_does_not_open_comment_iterator()]] - code - tests/crawler/test_instaloader_crawler.py
- [[.web_response()]] - code - tests/crawler/test_instaloader_crawler.py
- [[InstaloaderCrawlerTests]] - code - tests/crawler/test_instaloader_crawler.py
- [[fixture_post()]] - code - tests/crawler/test_instaloader_crawler.py
- [[hanging_fixture()]] - code - tests/crawler/test_instaloader_crawler.py
- [[persistent_fixture()]] - code - tests/crawler/test_instaloader_crawler.py
- [[server_fault_fixture()]] - code - tests/crawler/test_instaloader_crawler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Worker_Instaloader
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]

## Top bridge nodes
- [[InstaloaderCrawlerTests]] - degree 35, connects to 1 community
- [[fixture_post()]] - degree 7, connects to 1 community
- [[hanging_fixture()]] - degree 2, connects to 1 community
- [[persistent_fixture()]] - degree 2, connects to 1 community
- [[server_fault_fixture()]] - degree 2, connects to 1 community