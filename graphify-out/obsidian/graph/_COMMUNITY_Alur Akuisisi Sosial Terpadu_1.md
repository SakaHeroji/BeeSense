---
type: community
cohesion: 0.11
members: 32
---

# Alur Akuisisi Sosial Terpadu

**Cohesion:** 0.11 - loosely connected
**Members:** 32 nodes

## Members
- [[._checkpoint_items()_1]] - code - Crawler/Backend/social_crawler.py
- [[.runner()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_default_config_selects_reddrix_without_loading_browser()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_display_mode_propagates_through_process_boundary()]] - code - tests/crawler/test_reddit_crawler.py
- [[Configure initial and refreshed sessions inside an isolated worker module.]] - rationale - Crawler/Backend/social_crawler.py
- [[Exercise the default Reddrix route with YouTube and the shared export pipeline.]] - rationale - tests/crawler/test_social_crawler_reddrix.py
- [[FixtureReddrix]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[Guard Python entry points for multiprocessing spawn]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Main coordinator owns Reddrix normalization, display and worker]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Map Reddrix 1.2.14 dictionaries without inventing identity or dates.]] - rationale - Crawler/Backend/social_crawler.py
- [[Omitted retry setting defaults to zero]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Reddrix anti-bot exceptions do not expose an authoritative HTTP status.]] - rationale - Crawler/Backend/social_crawler.py
- [[Spawn boundary retains streamed records when the hard deadline expires.]] - rationale - Crawler/Backend/social_crawler.py
- [[Validate shared Instaloader settings without loading credentials or networking.]] - rationale - Crawler/Backend/instaloader_crawler.py
- [[Virtual displays require Linux and Xvfb; other environments use headless.]] - rationale - Crawler/Backend/social_crawler.py
- [[_config()]] - code - Crawler/Backend/social_crawler.py
- [[_keywords()]] - code - Crawler/Backend/social_crawler.py
- [[_number()]] - code - Crawler/Backend/social_crawler.py
- [[_url()]] - code - Crawler/Backend/social_crawler.py
- [[collect_reddrix()]] - code - Crawler/Backend/social_crawler.py
- [[instaloader_options()]] - code - Crawler/Backend/instaloader_crawler.py
- [[load_reddrix()]] - code - Crawler/Backend/social_crawler.py
- [[normalize_reddrix_item()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_error_receipt()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_receipt()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_version()]] - code - Crawler/Backend/social_crawler.py
- [[reddrix_worker()]] - code - Crawler/Backend/social_crawler.py
- [[resolve_reddrix_display()]] - code - Crawler/Backend/social_crawler.py
- [[run_reddrix_worker()]] - code - Crawler/Backend/social_crawler.py
- [[social_crawler.py]] - code - Crawler/Backend/social_crawler.py
- [[spawn_reddrix_fixture()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[test_social_crawler_reddrix.py]] - code - tests/crawler/test_social_crawler_reddrix.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Alur_Akuisisi_Sosial_Terpadu
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_1]]
- 8 edges to [[_COMMUNITY_Akuisisi Reddit Reddrix_1]]
- 7 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_2]]
- 7 edges to [[_COMMUNITY_Akuisisi Reddit Reddrix]]
- 5 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu]]
- 2 edges to [[_COMMUNITY_Crawler Selenium Terisolasi]]
- 2 edges to [[_COMMUNITY_Operasi dan Verifikasi BeeSense]]
- 2 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_4]]
- 2 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_3]]
- 1 edge to [[_COMMUNITY_Parser dan Runner Reddit]]
- 1 edge to [[_COMMUNITY_Adapter Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_3]]
- 1 edge to [[_COMMUNITY_Eksperimen Instaloader dan GraphQL Web]]
- 1 edge to [[_COMMUNITY_Konfigurasi SocialCrawler_1]]

## Top bridge nodes
- [[social_crawler.py]] - degree 31, connects to 9 communities
- [[test_social_crawler_reddrix.py]] - degree 17, connects to 4 communities
- [[FixtureReddrix]] - degree 6, connects to 3 communities
- [[reddrix_worker()]] - degree 11, connects to 2 communities
- [[Main coordinator owns Reddrix normalization, display and worker]] - degree 10, connects to 2 communities