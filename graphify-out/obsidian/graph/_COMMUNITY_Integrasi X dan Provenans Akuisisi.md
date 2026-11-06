---
type: community
cohesion: 0.10
members: 36
---

# Integrasi X dan Provenans Akuisisi

**Cohesion:** 0.10 - loosely connected
**Members:** 36 nodes

## Members
- [[._checkpoint_items()_1]] - code - Crawler/Backend/social_crawler.py
- [[._legacy_settings()_1]] - code - Crawler/Backend/social_crawler.py
- [[.ig()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.setUp()_5]] - code - tests/crawler/test_instagram_crawler.py
- [[.setUp()_3]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.setUp()_6]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_calendar_month_boundary_date_only_and_unrecognized_dates()]] - code - tests/crawler/test_social_crawler.py
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
- [[.test_mixed_export_keeps_native_platform_provenance()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_native_baseline_skips_instagram_before_worker()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_owned_instaloader_worker_is_closed_when_combined_run_finishes()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_reddit_cooldown_rejects_invalid_config_values()]] - code - tests/crawler/test_social_crawler.py
- [[.test_relative_calendar_dates_use_source_capture_timezone_and_edit_suffix()]] - code - tests/crawler/test_social_crawler.py
- [[.test_unused_instagram_settings_cannot_leak_credentials_in_other_platform_runs()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.worker()_1]] - code - tests/crawler/test_instagram_crawler.py
- [[Clock_1]] - code - tests/crawler/test_instagram_crawler.py
- [[Compose platform workers with one configuration, scheduler and export bundle.]] - rationale - Crawler/Backend/social_crawler.py
- [[InstagramIntegrationTests]] - code - tests/crawler/test_social_crawler_instagram.py
- [[InstaloaderSettings]] - code - Crawler/Backend/instaloader_crawler.py
- [[Nullable crawl limits and complete comment intent]] - rationale - graphify-out/memory/query_20261103_032840_buat_seluruh_konfigurasi_crawler_minimal_1000_post.md
- [[Relocated combined crawler image runs package module as UID10001]] - rationale - deployment/docker/Dockerfile.crawler
- [[SocialCrawler]] - code - Crawler/Backend/social_crawler.py
- [[Universal crawler configuration consolidation]] - rationale - graphify-out/memory/query_20261103_015614_rapikan_folder_config_social_crawler__universal_da.md
- [[WIB archive and native identity deduplication]] - rationale - graphify-out/memory/query_20261103_023514_rapikan_config_social_nlp_py_dan_output_social_cra.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Integrasi_X_dan_Provenans_Akuisisi
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_2]]
- 12 edges to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 12 edges to [[_COMMUNITY_Konfigurasi Crawler Universal]]
- 10 edges to [[_COMMUNITY_Pengujian Client Instagram]]
- 9 edges to [[_COMMUNITY_Crawler Selenium]]
- 9 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_1]]
- 7 edges to [[_COMMUNITY_Kuota Harian Scweet]]
- 7 edges to [[_COMMUNITY_Kuota Harian Scweet_1]]
- 6 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 5 edges to [[_COMMUNITY_Wrapper RedditCrawler_1]]
- 3 edges to [[_COMMUNITY_Wrapper RedditCrawler_2]]
- 3 edges to [[_COMMUNITY_Worker Instaloader_2]]
- 3 edges to [[_COMMUNITY_Arsip Data Harian_1]]
- 3 edges to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]
- 2 edges to [[_COMMUNITY_Optimasi Crawler Sosial]]
- 2 edges to [[_COMMUNITY_Integrasi Default Instaloader_1]]
- 1 edge to [[_COMMUNITY_Pengujian Koordinator Crawler_1]]
- 1 edge to [[_COMMUNITY_Panduan Pipeline BeeSense_4]]
- 1 edge to [[_COMMUNITY_Integrasi Default Instaloader_6]]
- 1 edge to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 1 edge to [[_COMMUNITY_Akuisisi TikTok dan Ekspor]]
- 1 edge to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 1 edge to [[_COMMUNITY_Akuisisi TikTok dan Ekspor_1]]
- 1 edge to [[_COMMUNITY_Worker Instaloader_1]]
- 1 edge to [[_COMMUNITY_Sidebar TikTok Chrome_1]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit]]
- 1 edge to [[_COMMUNITY_Optimasi Crawler Sosial_4]]

## Top bridge nodes
- [[SocialCrawler]] - degree 122, connects to 24 communities
- [[InstaloaderSettings]] - degree 7, connects to 4 communities
- [[Clock_1]] - degree 11, connects to 3 communities
- [[InstagramIntegrationTests]] - degree 20, connects to 2 communities
- [[.worker()_1]] - degree 11, connects to 1 community