---
type: community
cohesion: 0.10
members: 33
---

# Alur Akuisisi Sosial Terpadu

**Cohesion:** 0.10 - loosely connected
**Members:** 33 nodes

## Members
- [[._browser_call()]] - code - Crawler/Backend/social_crawler.py
- [[._delay()]] - code - Crawler/Backend/social_crawler.py
- [[._dom_events()]] - code - Crawler/Backend/social_crawler.py
- [[._execute()_1]] - code - Crawler/Backend/social_crawler.py
- [[._legacy_settings()_1]] - code - Crawler/Backend/social_crawler.py
- [[._normalize()_1]] - code - Crawler/Backend/social_crawler.py
- [[._pace()]] - code - Crawler/Backend/social_crawler.py
- [[._source_metadata()_1]] - code - Crawler/Backend/social_crawler.py
- [[.export_compact()]] - code - Crawler/Backend/social_crawler.py
- [[.plan()_3]] - code - Crawler/Backend/social_crawler.py
- [[.setUp()_7]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_default_uses_one_json_and_plan_does_not_access_sources()]] - code - tests/crawler/test_social_crawler.py
- [[.test_discovery_retains_bounded_cursor()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_expanded_youtube_search_budget_reaches_worker_without_old_cli_cap()]] - code - tests/crawler/test_social_crawler.py
- [[.test_instagram_429_honors_server_wait_and_retries_same_post()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_default_cooldown_matches_reddit_policy()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_only_never_calls_youtube_or_reddit_and_matches_excel_contract()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_instagram_retry_cap_and_global_deadline_stop_additional_requests()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_invalid_config_is_rejected_before_output_or_requests()]] - code - tests/crawler/test_social_crawler.py
- [[.test_mixed_export_keeps_native_platform_provenance()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_native_baseline_skips_instagram_before_worker()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_reddit_cooldown_rejects_invalid_config_values()]] - code - tests/crawler/test_social_crawler.py
- [[.test_unused_instagram_settings_cannot_leak_credentials_in_other_platform_runs()]] - code - tests/crawler/test_social_crawler_instagram.py
- [[Compose platform workers with one configuration, scheduler and export bundle.]] - rationale - Crawler/Backend/social_crawler.py
- [[Describe the acquisition backend independently of the shared export.]] - rationale - Crawler/Backend/social_crawler.py
- [[Exercise Instagram through the combined coordinator, without network access.]] - rationale - tests/crawler/test_social_crawler_instagram.py
- [[InstagramIntegrationTests]] - code - tests/crawler/test_social_crawler_instagram.py
- [[Mixed bundle retains source-specific backend provenance]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Re-export saved Contents without network or modifying the source bundle.]] - rationale - Crawler/Backend/social_crawler.py
- [[SocialCrawler_1]] - code - Crawler/Backend/social_crawler.py
- [[Validate and return the effective plan without browsernetwork access.]] - rationale - Crawler/Backend/social_crawler.py
- [[main()_5]] - code - Crawler/Backend/social_crawler.py
- [[test_social_crawler_instagram.py]] - code - tests/crawler/test_social_crawler_instagram.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Alur_Akuisisi_Sosial_Terpadu
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu]]
- 10 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi]]
- 8 edges to [[_COMMUNITY_Crawler Selenium Terisolasi]]
- 8 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_2]]
- 7 edges to [[_COMMUNITY_Akuisisi Reddit Reddrix_1]]
- 6 edges to [[_COMMUNITY_Akuisisi Reddit Reddrix_3]]
- 6 edges to [[_COMMUNITY_Konfigurasi SocialCrawler_1]]
- 5 edges to [[_COMMUNITY_Akuisisi Reddit Reddrix]]
- 5 edges to [[_COMMUNITY_Konfigurasi SocialCrawler]]
- 4 edges to [[_COMMUNITY_Topik dan Verifikasi NLP_1]]
- 4 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_3]]
- 3 edges to [[_COMMUNITY_Arsitektur Crawler dan Dependensi]]
- 3 edges to [[_COMMUNITY_Ringkasan Topik Gemini]]
- 3 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_7]]
- 3 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_9]]
- 2 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_5]]
- 2 edges to [[_COMMUNITY_Snapshot NLP dan Arsip_1]]
- 2 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_3]]
- 2 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_4]]
- 2 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_6]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_5]]
- 1 edge to [[_COMMUNITY_Akses dan Parsing HTML]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip_5]]
- 1 edge to [[_COMMUNITY_Operasi dan Verifikasi BeeSense]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_5]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip]]
- 1 edge to [[_COMMUNITY_Pipeline dan Persistensi NLP_1]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_8]]

## Top bridge nodes
- [[SocialCrawler_1]] - degree 104, connects to 24 communities
- [[test_social_crawler_instagram.py]] - degree 7, connects to 3 communities
- [[main()_5]] - degree 6, connects to 3 communities
- [[InstagramIntegrationTests]] - degree 13, connects to 2 communities
- [[.export_compact()]] - degree 5, connects to 2 communities