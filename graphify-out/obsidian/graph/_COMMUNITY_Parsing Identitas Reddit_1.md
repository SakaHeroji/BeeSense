---
type: community
cohesion: 0.50
members: 4
---

# Parsing Identitas Reddit

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[.__init__()_11]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[RedditAdapter]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[RedditRecordFactory]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[Verified Reddit native identity and parentroot relationships]] - rationale - docs/crawler/REDDIT_CRAWLER.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Parsing_Identitas_Reddit
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Pengujian Parser Reddit]]
- 3 edges to [[_COMMUNITY_Parsing Identitas Reddit]]
- 3 edges to [[_COMMUNITY_Kontrak Record Reddit]]
- 2 edges to [[_COMMUNITY_Kontrak Record Reddit_1]]
- 2 edges to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit_2]]
- 1 edge to [[_COMMUNITY_Koordinator Backend Sosial]]

## Top bridge nodes
- [[RedditRecordFactory]] - degree 8, connects to 5 communities
- [[RedditAdapter]] - degree 8, connects to 4 communities
- [[Verified Reddit native identity and parentroot relationships]] - degree 5, connects to 2 communities