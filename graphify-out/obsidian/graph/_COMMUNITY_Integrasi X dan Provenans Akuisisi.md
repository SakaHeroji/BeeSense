---
type: community
cohesion: 0.08
members: 46
---

# Integrasi X dan Provenans Akuisisi

**Cohesion:** 0.08 - loosely connected
**Members:** 46 nodes

## Members
- [[.__init__()_16]] - code - Crawler/Backend/social_crawler_selenium.py
- [[._browser_call()]] - code - Crawler/Backend/social_crawler.py
- [[._checkpoint_items()_1]] - code - Crawler/Backend/social_crawler.py
- [[._delay()]] - code - Crawler/Backend/social_crawler.py
- [[._dom_events()]] - code - Crawler/Backend/social_crawler.py
- [[._event()_1]] - code - Crawler/Backend/social_crawler.py
- [[._execute()_1]] - code - Crawler/Backend/social_crawler.py
- [[._existing_posts()]] - code - Crawler/Backend/social_crawler.py
- [[._legacy_settings()_1]] - code - Crawler/Backend/social_crawler.py
- [[._normalize()_1]] - code - Crawler/Backend/social_crawler.py
- [[._pace()]] - code - Crawler/Backend/social_crawler.py
- [[._source_metadata()_1]] - code - Crawler/Backend/social_crawler.py
- [[._wait_for_captcha()]] - code - Crawler/Backend/social_crawler.py
- [[.clock()_1]] - code - tests/crawler/test_instagram_crawler.py
- [[.export_compact()]] - code - Crawler/Backend/social_crawler.py
- [[.plan()_6]] - code - Crawler/Backend/social_crawler.py
- [[.run()_4]] - code - Crawler/Backend/social_crawler.py
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
- [[.test_thousand_unique_posts_finish_beyond_old_hours_and_keep_all_comments()]] - code - tests/crawler/test_unlimited_crawling.py
- [[.test_unused_instagram_settings_cannot_leak_credentials_in_other_platform_runs()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[Clock_1]] - code - tests/crawler/test_instagram_crawler.py
- [[Compose platform workers with one configuration, scheduler and export bundle.]] - rationale - Crawler/Backend/social_crawler.py
- [[Describe the acquisition backend independently of the shared export.]] - rationale - Crawler/Backend/social_crawler.py
- [[InstagramIntegrationTests]] - code - tests/crawler/test_social_crawler_instagram.py
- [[Re-export saved Contents without network or modifying the source bundle.]] - rationale - Crawler/Backend/social_crawler.py
- [[Read roots and all global X IDs; never alter historical workbooks.]] - rationale - Crawler/Backend/social_crawler.py
- [[Relocated combined crawler image runs package module as UID10001]] - rationale - deployment/docker/Dockerfile.crawler
- [[SocialCrawler]] - code - Crawler/Backend/social_crawler.py
- [[SocialExportMixin_1]] - code
- [[Validate and return the effective plan without browsernetwork access.]] - rationale - Crawler/Backend/social_crawler.py
- [[Write an audit bundle; default runs also publish platformday partitions.]] - rationale - Crawler/Backend/social_crawler.py
- [[_url()]] - code - Crawler/Backend/social_crawler.py
- [[deadline_after()]] - code - Crawler/Backend/crawler_limits.py
- [[main()_18]] - code - Crawler/Backend/social_crawler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Integrasi_X_dan_Provenans_Akuisisi
SORT file.name ASC
```

## Connections to other communities
- 17 edges to [[_COMMUNITY_Pengujian Client Instagram_1]]
- 16 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_2]]
- 16 edges to [[_COMMUNITY_Kuota Harian Scweet]]
- 13 edges to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 10 edges to [[_COMMUNITY_Konfigurasi Crawler Universal]]
- 9 edges to [[_COMMUNITY_Crawler Selenium]]
- 6 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 5 edges to [[_COMMUNITY_Pengujian Client Instagram]]
- 4 edges to [[_COMMUNITY_Kontrak Record Reddit]]
- 3 edges to [[_COMMUNITY_Wrapper RedditCrawler_1]]
- 3 edges to [[_COMMUNITY_Worker Instaloader]]
- 3 edges to [[_COMMUNITY_Arsip Data Harian]]
- 2 edges to [[_COMMUNITY_Panduan Pipeline BeeSense_2]]
- 2 edges to [[_COMMUNITY_Akuisisi TikTok dan Ekspor_3]]
- 1 edge to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 1 edge to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik]]
- 1 edge to [[_COMMUNITY_Akuisisi TikTok dan Ekspor_1]]
- 1 edge to [[_COMMUNITY_Akuisisi TikTok dan Ekspor_6]]

## Top bridge nodes
- [[SocialCrawler]] - degree 110, connects to 15 communities
- [[InstagramIntegrationTests]] - degree 20, connects to 3 communities
- [[Clock_1]] - degree 15, connects to 3 communities
- [[_url()]] - degree 5, connects to 3 communities
- [[.test_thousand_unique_posts_finish_beyond_old_hours_and_keep_all_comments()]] - degree 5, connects to 3 communities