---
type: community
cohesion: 0.08
members: 33
---

# Pengujian Client Instagram

**Cohesion:** 0.08 - loosely connected
**Members:** 33 nodes

## Members
- [[.crawler()_2]] - code - tests/crawler/test_instagram_crawler.py
- [[.hashtag_medias_v1_chunk()]] - code - tests/crawler/test_instagram_crawler.py
- [[.media_comment_replies_chunk()]] - code - tests/crawler/test_instagram_crawler.py
- [[.media_comments_chunk()]] - code - tests/crawler/test_instagram_crawler.py
- [[.media_info_v1()]] - code - tests/crawler/test_instagram_crawler.py
- [[.media_pk_from_code()]] - code - tests/crawler/test_instagram_crawler.py
- [[.setUp()_16]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_actual_instagram_worker_missing_session_stops_without_network()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_auth_file_login_selects_instagram_and_never_exports_credentials()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_authentication_barrier_keeps_partial_records_without_retry()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_baseline_dedup_before_request_and_source_remains_unchanged()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_browser_cookie_is_opaque_and_device_survives_stale_auth_removal()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_complete_bundle_matches_social_excel_contract_and_checksums()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_credentials_cannot_be_embedded_in_config()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_filtering_dates_keywords_and_minimum_uses_unique_comments()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_global_deadline_prevents_late_requests_and_keeps_partial()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_invalid_input_fails_before_any_worker()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_local_session_cookie_is_used_without_password_login()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_password_mode_restores_settings_and_ignores_browser_cookie()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_password_recovery_is_one_relogin_and_propagates_failure()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_password_recovery_retains_explicit_verification_code()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_password_upgrade_challenge_and_rate_limit_are_not_retried()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_real_collector_deduplicates_and_bounds_pages_and_replies()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_repeated_source_errors_stop_after_three_operations()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_saved_settings_are_atomic_owner_only_and_retry_settings_are_reset()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_search_uses_explicit_hashtag_cursor()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_standalone_inherits_main_duration_and_keeps_combined_enabled_scope()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_upgrade_gate_is_distinct_from_throttling_and_unknown_source_errors()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_url_canonicalization_and_identity()]] - code - tests/crawler/test_instagram_crawler.py
- [[.test_verified_429_respects_retry_after_and_budget()]] - code - tests/crawler/test_instagram_crawler.py
- [[FakeClient]] - code - tests/crawler/test_instagram_crawler.py
- [[InstagramCrawlerTests]] - code - tests/crawler/test_instagram_crawler.py
- [[stream()]] - code - tests/crawler/test_tiktok_crawler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Client_Instagram
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Pengujian Client Instagram_1]]
- 5 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi]]
- 2 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_2]]
- 1 edge to [[_COMMUNITY_Capture Reddit Playwright]]
- 1 edge to [[_COMMUNITY_Arsip Data Harian_1]]

## Top bridge nodes
- [[InstagramCrawlerTests]] - degree 32, connects to 4 communities
- [[FakeClient]] - degree 9, connects to 2 communities
- [[stream()]] - degree 3, connects to 2 communities
- [[.crawler()_2]] - degree 13, connects to 1 community
- [[.test_verified_429_respects_retry_after_and_budget()]] - degree 3, connects to 1 community