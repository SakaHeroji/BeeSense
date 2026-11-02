---
type: community
cohesion: 0.13
members: 23
---

# Koordinator Backend Sosial

**Cohesion:** 0.13 - loosely connected
**Members:** 23 nodes

## Members
- [[.__init__()_30]] - code - tests/crawler/test_social_crawler.py
- [[.clock()_1]] - code - tests/crawler/test_social_crawler.py
- [[.setUp()_6]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.setUp()_7]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.setUp()_5]] - code - tests/crawler/test_social_crawler.py
- [[.sleep()_1]] - code - tests/crawler/test_social_crawler.py
- [[.test_discovery_retains_bounded_cursor()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_429_honors_server_wait_and_retries_same_post()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_batch_pause_is_bounded_by_global_deadline()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_default_cooldown_matches_reddit_policy()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_exponential_backoff_is_capped_and_retry_count_is_bounded()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_only_never_calls_youtube_or_reddit_and_matches_excel_contract()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_pacing_rejects_unknown_or_unsafe_values()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_retry_cap_and_global_deadline_stop_additional_requests()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_server_wait_is_not_shortened_by_backoff_cap()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instaloader_is_default_and_owns_one_persistent_worker()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_mixed_export_keeps_native_platform_provenance()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_native_baseline_skips_instagram_before_worker()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_owned_instaloader_worker_is_closed_when_combined_run_finishes()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_unused_instagram_settings_cannot_leak_credentials_in_other_platform_runs()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.worker()]] - code - tests/crawler/test_instagram_crawler.py
- [[Clock_1]] - code - tests/crawler/test_social_crawler.py
- [[InstagramIntegrationTests]] - code - tests/crawler/test_social_crawler_instagram.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Koordinator_Backend_Sosial
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_1]]
- 6 edges to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 5 edges to [[_COMMUNITY_Pengujian Client Instagram]]
- 4 edges to [[_COMMUNITY_Worker Instaloader]]
- 3 edges to [[_COMMUNITY_Worker Reddrix]]
- 1 edge to [[_COMMUNITY_Crawler Selenium]]

## Top bridge nodes
- [[InstagramIntegrationTests]] - degree 21, connects to 4 communities
- [[Clock_1]] - degree 18, connects to 3 communities
- [[.test_instaloader_is_default_and_owns_one_persistent_worker()]] - degree 4, connects to 2 communities
- [[.test_mixed_export_keeps_native_platform_provenance()]] - degree 3, connects to 2 communities
- [[.worker()]] - degree 11, connects to 1 community