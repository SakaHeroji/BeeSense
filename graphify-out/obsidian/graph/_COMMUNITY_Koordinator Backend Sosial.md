---
type: community
members: 42
---

# Koordinator Backend Sosial

**Members:** 42 nodes

## Members
- [[.__init__()_33]] - code - tests/crawler/test_social_crawler.py
- [[._legacy_settings()]] - code - Crawler/Backend/social_crawler.py
- [[.clock()_1]] - code - tests/crawler/test_social_crawler.py
- [[.crawler()_2]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.setUp()_5]] - code - tests/crawler/test_social_crawler.py
- [[.setUp()_6]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.setUp()_7]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.sleep()_1]] - code - tests/crawler/test_social_crawler.py
- [[.test_calendar_month_boundary_date_only_and_unrecognized_dates()]] - code - tests/crawler/test_social_crawler.py
- [[.test_default_config_selects_reddrix_without_loading_browser()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_default_uses_one_json_and_plan_does_not_access_sources()]] - code - tests/crawler/test_social_crawler.py
- [[.test_discovery_retains_bounded_cursor()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_expanded_youtube_search_budget_reaches_worker_without_old_cli_cap()]] - code - tests/crawler/test_social_crawler.py
- [[.test_instagram_429_honors_server_wait_and_retries_same_post()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_batch_pause_is_bounded_by_global_deadline()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_default_cooldown_matches_reddit_policy()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_exponential_backoff_is_capped_and_retry_count_is_bounded()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_only_never_calls_youtube_or_reddit_and_matches_excel_contract()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_pacing_rejects_unknown_or_unsafe_values()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_retry_cap_and_global_deadline_stop_additional_requests()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_server_wait_is_not_shortened_by_backoff_cap()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instaloader_is_default_and_owns_one_persistent_worker()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_invalid_config_is_rejected_before_output_or_requests()]] - code - tests/crawler/test_social_crawler.py
- [[.test_invalid_display_and_checkpoint_mix_fail_before_acquisition()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_missing_reddrix_exports_partial_and_keeps_youtube_running()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_mixed_baseline_skips_both_platforms_before_worker_requests()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_mixed_default_workers_publish_one_bundle_with_correct_provenance()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_mixed_export_keeps_native_platform_provenance()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_native_baseline_skips_instagram_before_worker()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_owned_instaloader_worker_is_closed_when_combined_run_finishes()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_reddit_cooldown_rejects_invalid_config_values()]] - code - tests/crawler/test_social_crawler.py
- [[.test_reddrix_retry_uses_coordinator_cooldown_and_same_worker()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_relative_calendar_dates_use_source_capture_timezone_and_edit_suffix()]] - code - tests/crawler/test_social_crawler.py
- [[.test_spawned_worker_imports_shared_implementation_without_live_access()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_unused_instagram_settings_cannot_leak_credentials_in_other_platform_runs()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.worker()]] - code - tests/crawler/test_instagram_crawler.py
- [[Clock_1]] - code - tests/crawler/test_social_crawler.py
- [[Compose platform workers with one configuration, scheduler and export bundle.]] - rationale - Crawler/Backend/social_crawler.py
- [[InstagramIntegrationTests]] - code - tests/crawler/test_social_crawler_instagram.py
- [[InstagramSettings]] - code - Crawler/Backend/instagram_crawler.py
- [[SocialCrawler]] - code - Crawler/Backend/social_crawler.py
- [[SocialCrawlerReddrixTests]] - code - tests/crawler/test_social_crawler_reddrix.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Koordinator_Backend_Sosial
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 13 edges to [[_COMMUNITY_Worker Reddrix]]
- 10 edges to [[_COMMUNITY_Worker Instaloader]]
- 10 edges to [[_COMMUNITY_Eksekusi dan Ekspor Crawler]]
- 10 edges to [[_COMMUNITY_Pengujian Client Instagram]]
- 9 edges to [[_COMMUNITY_Crawler Selenium]]
- 6 edges to [[_COMMUNITY_Read-only nativecanonical index excludes 50 YouTube and 181 Reddit roots]]
- 5 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 3 edges to [[_COMMUNITY_Transport GraphQL Instaloader]]
- 3 edges to [[_COMMUNITY_Round Robin Shared Deadline]]
- 3 edges to [[_COMMUNITY_configsocial_crawler.json]]
- 3 edges to [[_COMMUNITY_Riwayat Pacing Instagram]]
- 3 edges to [[_COMMUNITY_InstaloaderCrawler]]
- 2 edges to [[_COMMUNITY_Fixture dan Pengujian Reddit]]
- 2 edges to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 2 edges to [[_COMMUNITY_Historical Reddit continuations preserve bundles and original deadline]]
- 2 edges to [[_COMMUNITY_Runtime Docker dan Display]]
- 2 edges to [[_COMMUNITY_Ekspor dan Provenance Reddit]]
- 2 edges to [[_COMMUNITY_Default Backend Reddit]]
- 2 edges to [[_COMMUNITY_Struktur Runtime Dashboard]]
- 1 edge to [[_COMMUNITY_CI dan Verifikasi Backend]]
- 1 edge to [[_COMMUNITY_Pengambilan HTML Reddit]]
- 1 edge to [[_COMMUNITY_Reddit Playwright CLI runner]]
- 1 edge to [[_COMMUNITY_Instagram Client dan Ekspor]]
- 1 edge to [[_COMMUNITY_.score_coherence]]
- 1 edge to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 1 edge to [[_COMMUNITY_Konfigurasi Model Aktif]]
- 1 edge to [[_COMMUNITY_Arsitektur Model dan Dashboard]]
- 1 edge to [[_COMMUNITY_Panduan Pipeline BeeSense]]

## Top bridge nodes
- [[SocialCrawler]] - degree 111, connects to 27 communities
- [[InstagramSettings]] - degree 7, connects to 5 communities
- [[SocialCrawlerReddrixTests]] - degree 16, connects to 4 communities
- [[Clock_1]] - degree 18, connects to 3 communities
- [[InstagramIntegrationTests]] - degree 21, connects to 2 communities