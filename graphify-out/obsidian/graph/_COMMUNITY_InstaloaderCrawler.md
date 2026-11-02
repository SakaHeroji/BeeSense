---
type: community
cohesion: 0.23
members: 12
---

# InstaloaderCrawler

**Cohesion:** 0.23 - loosely connected
**Members:** 12 nodes

## Members
- [[.__aenter__()]] - code - tests/crawler/test_reddit_crawler.py
- [[.__aexit__()]] - code - tests/crawler/test_reddit_crawler.py
- [[.__init__()_29]] - code - tests/crawler/test_reddit_crawler.py
- [[.get_items()]] - code - tests/crawler/test_reddit_crawler.py
- [[.test_search_preserves_subreddit_scope_without_fetching_comments()]] - code - tests/crawler/test_reddit_crawler.py
- [[.test_stream_enforces_duplicates_and_reply_budgets()]] - code - tests/crawler/test_reddit_crawler.py
- [[.worker()_1]] - code - tests/crawler/test_reddit_crawler.py
- [[FakeReddrix]] - code - tests/crawler/test_reddit_crawler.py
- [[Reddrix fieldidentity boundaries and the real, shared Excel exporter.]] - rationale - tests/crawler/test_reddit_crawler.py
- [[item()]] - code - tests/crawler/test_reddit_crawler.py
- [[records()_1]] - code - tests/crawler/test_reddit_crawler.py
- [[test_reddit_crawler.py]] - code - tests/crawler/test_reddit_crawler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/InstaloaderCrawler
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 6 edges to [[_COMMUNITY_Worker Reddrix]]
- 3 edges to [[_COMMUNITY_Pengambilan HTML Reddit_3]]
- 2 edges to [[_COMMUNITY_Eksekusi dan Ekspor Crawler]]
- 1 edge to [[_COMMUNITY_Runtime Docker dan Display_1]]
- 1 edge to [[_COMMUNITY_Pengujian Koordinator Crawler]]

## Top bridge nodes
- [[FakeReddrix]] - degree 13, connects to 4 communities
- [[test_reddit_crawler.py]] - degree 10, connects to 3 communities
- [[.worker()_1]] - degree 4, connects to 3 communities
- [[item()]] - degree 6, connects to 1 community
- [[records()_1]] - degree 5, connects to 1 community