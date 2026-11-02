---
type: community
cohesion: 0.67
members: 3
---

# Batas Akuisisi Reddit

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[.test_browser_factory_overrides_initial_and_refreshed_sessions()]] - code - tests/crawler/test_reddit_crawler.py
- [[Configure initial and refreshed sessions inside an isolated worker module.]] - rationale - Crawler/Backend/social_crawler.py
- [[load_reddrix()]] - code - Crawler/Backend/social_crawler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Batas_Akuisisi_Reddit
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler_1]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler]]
- 1 edge to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 1 edge to [[_COMMUNITY_Batas Akuisisi Reddit_2]]
- 1 edge to [[_COMMUNITY_Worker Reddrix]]

## Top bridge nodes
- [[load_reddrix()]] - degree 7, connects to 4 communities
- [[.test_browser_factory_overrides_initial_and_refreshed_sessions()]] - degree 3, connects to 2 communities