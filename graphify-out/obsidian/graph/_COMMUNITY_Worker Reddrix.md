---
type: community
cohesion: 0.13
members: 26
---

# Worker Reddrix

**Cohesion:** 0.13 - loosely connected
**Members:** 26 nodes

## Members
- [[.crawler()_2]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.runner()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_default_config_selects_reddrix_without_loading_browser()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_display_mode_propagates_through_process_boundary()]] - code - tests/crawler/test_reddit_crawler.py
- [[.test_invalid_display_and_checkpoint_mix_fail_before_acquisition()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_missing_reddrix_exports_partial_and_keeps_youtube_running()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_mixed_baseline_skips_both_platforms_before_worker_requests()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_mixed_default_workers_publish_one_bundle_with_correct_provenance()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_reddrix_retry_uses_coordinator_cooldown_and_same_worker()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_spawned_worker_imports_shared_implementation_without_live_access()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[Exercise the default Reddrix route with YouTube and the shared export pipeline.]] - rationale - tests/crawler/test_social_crawler_reddrix.py
- [[FixtureReddrix]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[Hard-deadline subprocess retains streamed records]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Map Reddrix 1.2.14 dictionaries without inventing identity or dates.]] - rationale - Crawler/Backend/social_crawler.py
- [[Reddrix anti-bot exceptions do not expose an authoritative HTTP status.]] - rationale - Crawler/Backend/social_crawler.py
- [[SocialCrawlerReddrixTests]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[Spawn boundary retains streamed records when the hard deadline expires.]] - rationale - Crawler/Backend/social_crawler.py
- [[collect_reddrix()]] - code - Crawler/Backend/social_crawler.py
- [[normalize_reddrix_item()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_error_receipt()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_receipt()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_version()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_worker()]] - code - Crawler/Backend/social_crawler.py
- [[run_reddrix_worker()]] - code - Crawler/Backend/social_crawler.py
- [[spawn_reddrix_fixture()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[test_social_crawler_reddrix.py]] - code - tests/crawler/test_social_crawler_reddrix.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Worker_Reddrix
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_Koordinator Backend Sosial]]
- 9 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi]]
- 5 edges to [[_COMMUNITY_Wrapper RedditCrawler_1]]
- 4 edges to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler]]
- 1 edge to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit_1]]
- 1 edge to [[_COMMUNITY_Batas Akuisisi Reddit_2]]

## Top bridge nodes
- [[test_social_crawler_reddrix.py]] - degree 17, connects to 4 communities
- [[SocialCrawlerReddrixTests]] - degree 15, connects to 3 communities
- [[reddrix_worker()]] - degree 10, connects to 2 communities
- [[collect_reddrix()]] - degree 7, connects to 2 communities
- [[FixtureReddrix]] - degree 6, connects to 2 communities