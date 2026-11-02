---
type: community
cohesion: 0.10
members: 36
---

# Worker Reddrix

**Cohesion:** 0.10 - loosely connected
**Members:** 36 nodes

## Members
- [[.__init__()_31]] - code - Crawler/Backend/social_crawler.py
- [[._checkpoint_items()_1]] - code - Crawler/Backend/social_crawler.py
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
- [[Map Reddrix 1.2.14 dictionaries without inventing identity or dates.]] - rationale - Crawler/Backend/social_crawler.py
- [[Reddrix anti-bot exceptions do not expose an authoritative HTTP status.]] - rationale - Crawler/Backend/social_crawler.py
- [[SocialCrawlerReddrixTests]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[Spawn boundary retains streamed records when the hard deadline expires.]] - rationale - Crawler/Backend/social_crawler.py
- [[Virtual displays require Linux and Xvfb; other environments use headless.]] - rationale - Crawler/Backend/social_crawler.py
- [[_config()]] - code - Crawler/Backend/social_crawler.py
- [[_integer()_1]] - code - Crawler/Backend/twitter_crawler.py
- [[_keywords()]] - code - Crawler/Backend/social_crawler.py
- [[_number()]] - code - Crawler/Backend/social_crawler.py
- [[_url()]] - code - Crawler/Backend/social_crawler.py
- [[collect_reddrix()]] - code - Crawler/Backend/social_crawler.py
- [[configuration()]] - code - Crawler/Backend/twitter_crawler.py
- [[normalize_reddrix_item()]] - code - Crawler/Backend/social_crawler.py
- [[post_url()]] - code - Crawler/Backend/twitter_crawler.py
- [[reddrix_error_receipt()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_receipt()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_worker()]] - code - Crawler/Backend/social_crawler.py
- [[resolve_reddrix_display()]] - code - Crawler/Backend/social_crawler.py
- [[run_reddrix_worker()]] - code - Crawler/Backend/social_crawler.py
- [[social_crawler.py]] - code - Crawler/Backend/social_crawler.py
- [[spawn_reddrix_fixture()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[test_social_crawler_reddrix.py]] - code - tests/crawler/test_social_crawler_reddrix.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Worker_Reddrix
SORT file.name ASC
```

## Connections to other communities
- 17 edges to [[_COMMUNITY_Eksekusi dan Ekspor Crawler]]
- 6 edges to [[_COMMUNITY_InstaloaderCrawler]]
- 6 edges to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 4 edges to [[_COMMUNITY_Koordinator Backend Sosial]]
- 4 edges to [[_COMMUNITY_Runtime Docker dan Display_1]]
- 4 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_1]]
- 2 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 2 edges to [[_COMMUNITY_Crawler Selenium]]
- 2 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_4]]
- 2 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_9]]
- 2 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_11]]
- 1 edge to [[_COMMUNITY_Capture Reddit Playwright]]
- 1 edge to [[_COMMUNITY_Parsing Identitas Reddit]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Pengambilan HTML Reddit]]
- 1 edge to [[_COMMUNITY_Pengambilan HTML Reddit_4]]
- 1 edge to [[_COMMUNITY_Pengujian Client Instagram]]
- 1 edge to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 1 edge to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi]]
- 1 edge to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_8]]

## Top bridge nodes
- [[social_crawler.py]] - degree 34, connects to 15 communities
- [[test_social_crawler_reddrix.py]] - degree 17, connects to 4 communities
- [[SocialCrawlerReddrixTests]] - degree 15, connects to 4 communities
- [[post_url()]] - degree 7, connects to 3 communities
- [[FixtureReddrix]] - degree 6, connects to 3 communities