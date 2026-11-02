---
type: community
cohesion: 0.10
members: 39
---

# Koordinator Backend Sosial

**Cohesion:** 0.10 - loosely connected
**Members:** 39 nodes

## Members
- [[.__init__()_30]] - code - tests/crawler/test_social_crawler.py
- [[._browser_call()]] - code - Crawler/Backend/social_crawler.py
- [[._delay()]] - code - Crawler/Backend/social_crawler.py
- [[._dom_events()]] - code - Crawler/Backend/social_crawler.py
- [[._event()]] - code - Crawler/Backend/social_crawler.py
- [[._execute()_1]] - code - Crawler/Backend/social_crawler.py
- [[._legacy_settings()_1]] - code - Crawler/Backend/social_crawler.py
- [[._pace()]] - code - Crawler/Backend/social_crawler.py
- [[._wait_for_captcha()]] - code - Crawler/Backend/social_crawler.py
- [[.clock()_1]] - code - tests/crawler/test_social_crawler.py
- [[.setUp()_6]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.setUp()_5]] - code - tests/crawler/test_social_crawler.py
- [[.sleep()_1]] - code - tests/crawler/test_social_crawler.py
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
- [[.worker()]] - code - tests/crawler/test_instagram_crawler.py
- [[Clock_1]] - code - tests/crawler/test_social_crawler.py
- [[Compose platform workers with one configuration, scheduler and export bundle.]] - rationale - Crawler/Backend/social_crawler.py
- [[InstagramIntegrationTests]] - code - tests/crawler/test_social_crawler_instagram.py
- [[SocialCrawler]] - code - Crawler/Backend/social_crawler.py
- [[SocialExportMixin_2]] - code

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Koordinator_Backend_Sosial
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 12 edges to [[_COMMUNITY_Worker Reddrix]]
- 10 edges to [[_COMMUNITY_Pengujian Client Instagram]]
- 9 edges to [[_COMMUNITY_Crawler Selenium]]
- 8 edges to [[_COMMUNITY_Koordinator Backend Sosial_1]]
- 8 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_1]]
- 7 edges to [[_COMMUNITY_Worker Instaloader]]
- 5 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 5 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi]]
- 2 edges to [[_COMMUNITY_Wrapper RedditCrawler_1]]
- 2 edges to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 2 edges to [[_COMMUNITY_Alur Dataset Model Dashboard_1]]
- 1 edge to [[_COMMUNITY_Panduan Pipeline BeeSense_5]]
- 1 edge to [[_COMMUNITY_Batas Akuisisi Reddit_2]]
- 1 edge to [[_COMMUNITY_Parsing Identitas Reddit_1]]
- 1 edge to [[_COMMUNITY_Panduan Pipeline BeeSense_1]]
- 1 edge to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 1 edge to [[_COMMUNITY_Panduan Pipeline BeeSense_3]]

## Top bridge nodes
- [[SocialCrawler]] - degree 97, connects to 18 communities
- [[Clock_1]] - degree 18, connects to 3 communities
- [[InstagramIntegrationTests]] - degree 21, connects to 2 communities
- [[.worker()]] - degree 11, connects to 1 community
- [[.test_instaloader_is_default_and_owns_one_persistent_worker()]] - degree 4, connects to 1 community