---
type: community
members: 21
---

# Konfigurasi Crawler Universal

**Members:** 21 nodes

## Members
- [[.__init__()_15]] - code - Crawler/Backend/social_crawler_selenium.py
- [[.__init__()_30]] - code - Crawler/Backend/reddit_crawler.py
- [[.setUp()_9]] - code - tests/crawler/test_social_crawler_instagram.py
- [[.test_cli_rejects_unimplemented_database_output_before_network_or_export()]] - code - tests/crawler/test_storage_config.py
- [[.test_every_runner_reads_changes_from_the_same_custom_file()]] - code - tests/crawler/test_crawler_config.py
- [[.test_expansion_rejects_non_object_and_oversized_files()]] - code - tests/crawler/test_crawler_config.py
- [[.test_invalid_schema_defaults_queries_and_limits_are_rejected()]] - code - tests/crawler/test_crawler_config.py
- [[.test_legacy_config_retains_strict_adapter_validation()]] - code - tests/crawler/test_crawler_config.py
- [[.test_legacy_coordinator_configuration_does_not_require_version()]] - code - tests/crawler/test_crawler_config.py
- [[.test_shared_queries_limits_and_platform_overrides_are_independent()]] - code - tests/crawler/test_crawler_config.py
- [[.test_standalone_selects_disabled_platform_without_mutating_input()]] - code - tests/crawler/test_crawler_config.py
- [[Apply shared defaults; an explicit platform value always wins, even .]] - rationale - Crawler/Backend/crawler_config.py
- [[Read a bounded JSON object without touching authentication or runtime state.]] - rationale - Crawler/Backend/crawler_config.py
- [[Scweet-only trial; uses the existing shared sink, filters and Excel format.]] - rationale - Crawler/Backend/twitter_crawler.py
- [[SocialExportMixin_2]] - code
- [[TwitterCrawler]] - code - Crawler/Backend/twitter_crawler.py
- [[Universal configuration contracts across the coordinator and standalone CLIs.]] - rationale - tests/crawler/test_crawler_config.py
- [[UniversalConfigTests]] - code - tests/crawler/test_crawler_config.py
- [[expand_config()]] - code - Crawler/Backend/crawler_config.py
- [[read_config()]] - code - Crawler/Backend/crawler_config.py
- [[test_crawler_config.py]] - code - tests/crawler/test_crawler_config.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Konfigurasi_Crawler_Universal
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_Konfigurasi Crawler Universal_1]]
- 9 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_6]]
- 8 edges to [[_COMMUNITY_Batas Crawler Opsional_1]]
- 6 edges to [[_COMMUNITY_Wrapper RedditCrawler_1]]
- 6 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi]]
- 4 edges to [[_COMMUNITY_Akuisisi YouTube_2]]
- 4 edges to [[_COMMUNITY_Worker Instaloader_1]]
- 2 edges to [[_COMMUNITY_Crawler Selenium]]
- 1 edge to [[_COMMUNITY_Batas Crawler Opsional_2]]
- 1 edge to [[_COMMUNITY_Worker Instaloader_2]]
- 1 edge to [[_COMMUNITY_Crawler Selenium_2]]
- 1 edge to [[_COMMUNITY_Crawler Selenium_1]]
- 1 edge to [[_COMMUNITY_Kuota Harian Scweet_1]]

## Top bridge nodes
- [[read_config()]] - degree 20, connects to 7 communities
- [[test_crawler_config.py]] - degree 17, connects to 7 communities
- [[UniversalConfigTests]] - degree 13, connects to 4 communities
- [[expand_config()]] - degree 10, connects to 4 communities
- [[.test_every_runner_reads_changes_from_the_same_custom_file()]] - degree 7, connects to 4 communities