---
type: community
cohesion: 0.31
members: 9
---

# Konfigurasi Trial Reddit

**Cohesion:** 0.31 - loosely connected
**Members:** 9 nodes

## Members
- [[Configured rootcommentcandidatetime budgets]] - rationale - config/reddit_crawler.json
- [[Original date boundary and university-topic query scope]] - rationale - config/reddit_crawler.json
- [[Original historical date window, keywords and read-only baseline]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Read-only historical baseline exclusion]] - rationale - config/reddit_crawler.json
- [[Thin Reddit-only wrapper selects shared Reddrix explicitly]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Thirty-minute bounded trial with non-guaranteed target]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Tracked Reddit trial configuration]] - concept - config/reddit_crawler.json
- [[Tracked reddrix.display_mode=auto]] - concept - config/reddit_crawler.json
- [[Trial config now explicitly selects Reddrix; wrapper preserves legacy compatibility]] - rationale - config/reddit_crawler.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Konfigurasi_Trial_Reddit
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 2 edges to [[_COMMUNITY_Runtime Docker dan Display]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler]]

## Top bridge nodes
- [[Tracked Reddit trial configuration]] - degree 10, connects to 2 communities
- [[Thin Reddit-only wrapper selects shared Reddrix explicitly]] - degree 3, connects to 2 communities
- [[Original historical date window, keywords and read-only baseline]] - degree 4, connects to 1 community
- [[Thirty-minute bounded trial with non-guaranteed target]] - degree 3, connects to 1 community
- [[Tracked reddrix.display_mode=auto]] - degree 2, connects to 1 community