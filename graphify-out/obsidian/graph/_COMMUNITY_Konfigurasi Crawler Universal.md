---
type: community
cohesion: 0.10
members: 42
---

# Konfigurasi Crawler Universal

**Cohesion:** 0.10 - loosely connected
**Members:** 42 nodes

## Members
- [[.__init__()_9]] - code - Crawler/Backend/reddit_crawler.py
- [[.__init__()_8]] - code - Crawler/Backend/social_crawler_selenium.py
- [[.plan()_1]] - code - Crawler/Backend/reddit_crawler.py
- [[.test_cli_rejects_unimplemented_database_output_before_network_or_export()]] - code - tests/crawler/test_storage_config.py
- [[.test_custom_storage_reaches_coordinator_and_standalone_projections()]] - code - tests/crawler/test_storage_config.py
- [[.test_every_runner_reads_changes_from_the_same_custom_file()]] - code - tests/crawler/test_crawler_config.py
- [[.test_excel_default_and_isolated_nested_defaults()]] - code - tests/crawler/test_storage_config.py
- [[.test_expansion_rejects_non_object_and_oversized_files()]] - code - tests/crawler/test_crawler_config.py
- [[.test_invalid_schema_defaults_queries_and_limits_are_rejected()]] - code - tests/crawler/test_crawler_config.py
- [[.test_legacy_config_retains_strict_adapter_validation()]] - code - tests/crawler/test_crawler_config.py
- [[.test_legacy_coordinator_configuration_does_not_require_version()]] - code - tests/crawler/test_crawler_config.py
- [[.test_rejects_credentials_and_unknown_values_in_public_config()]] - code - tests/crawler/test_storage_config.py
- [[.test_shared_queries_limits_and_platform_overrides_are_independent()]] - code - tests/crawler/test_crawler_config.py
- [[.test_standalone_selects_disabled_platform_without_mutating_input()]] - code - tests/crawler/test_crawler_config.py
- [[Apply shared defaults; an explicit platform value always wins, even .]] - rationale - Crawler/Backend/crawler_config.py
- [[Exercise Instagram through the combined coordinator, without network access.]] - rationale - tests/crawler/test_social_crawler_instagram.py
- [[Offline checks for the Chrome boundary, native identity, and provenance.]] - rationale - tests/crawler/test_instagram_browser.py
- [[One editable crawler configuration, expanded before adapter validation.]] - rationale - Crawler/Backend/crawler_config.py
- [[Project the versioned universal file to a legacy standalone adapter contract.]] - rationale - Crawler/Backend/crawler_config.py
- [[Public storage configuration must be explicit and never silently ignored.]] - rationale - tests/crawler/test_storage_config.py
- [[Read a bounded JSON object without touching authentication or runtime state.]] - rationale - Crawler/Backend/crawler_config.py
- [[Reddit-only compatibility entry point for the integrated SocialCrawler Reddrix b]] - rationale - Crawler/Backend/reddit_crawler.py
- [[RedditCrawler]] - code - Crawler/Backend/reddit_crawler.py
- [[Run only Reddit through the shared Reddrix implementation in SocialCrawler.]] - rationale - Crawler/Backend/reddit_crawler.py
- [[Storage settings shared with the frontend; DSNs stay in server environment.]] - rationale - Crawler/Backend/storage_config.py
- [[StorageConfigTests]] - code - tests/crawler/test_storage_config.py
- [[Universal configuration contracts across the coordinator and standalone CLIs.]] - rationale - tests/crawler/test_crawler_config.py
- [[UniversalConfigTests]] - code - tests/crawler/test_crawler_config.py
- [[_config()]] - code - Crawler/Backend/social_crawler.py
- [[crawler_config.py]] - code - Crawler/Backend/crawler_config.py
- [[expand_config()]] - code - Crawler/Backend/crawler_config.py
- [[main()_4]] - code - Crawler/Backend/reddit_crawler.py
- [[read_config()]] - code - Crawler/Backend/crawler_config.py
- [[reddit_crawler.py]] - code - Crawler/Backend/reddit_crawler.py
- [[require_excel_storage()]] - code - Crawler/Backend/storage_config.py
- [[standalone_config()]] - code - Crawler/Backend/crawler_config.py
- [[storage_config()]] - code - Crawler/Backend/storage_config.py
- [[storage_config.py]] - code - Crawler/Backend/storage_config.py
- [[test_crawler_config.py]] - code - tests/crawler/test_crawler_config.py
- [[test_instagram_browser.py]] - code - tests/crawler/test_instagram_browser.py
- [[test_social_crawler_instagram.py]] - code - tests/crawler/test_social_crawler_instagram.py
- [[test_storage_config.py]] - code - tests/crawler/test_storage_config.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Konfigurasi_Crawler_Universal
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Kuota Harian Scweet]]
- 12 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi]]
- 8 edges to [[_COMMUNITY_Batas Crawler Opsional]]
- 8 edges to [[_COMMUNITY_Akuisisi TikTok dan Ekspor_1]]
- 6 edges to [[_COMMUNITY_Crawler Selenium]]
- 5 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 4 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_3]]
- 3 edges to [[_COMMUNITY_Worker Instaloader_3]]
- 3 edges to [[_COMMUNITY_Batas Crawler Opsional_2]]
- 3 edges to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]
- 2 edges to [[_COMMUNITY_Pengujian Client Instagram]]
- 1 edge to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler_2]]
- 1 edge to [[_COMMUNITY_Worker Instaloader_2]]
- 1 edge to [[_COMMUNITY_Integrasi Default Instaloader_1]]

## Top bridge nodes
- [[test_crawler_config.py]] - degree 17, connects to 6 communities
- [[test_social_crawler_instagram.py]] - degree 12, connects to 6 communities
- [[crawler_config.py]] - degree 19, connects to 5 communities
- [[UniversalConfigTests]] - degree 13, connects to 4 communities
- [[test_instagram_browser.py]] - degree 8, connects to 4 communities