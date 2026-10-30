---
type: community
members: 10
---

# Konfigurasi Trial Reddit

**Members:** 10 nodes

## Members
- [[Configured rootcommentcandidatetime budgets]] - rationale - config/reddit_crawler.json
- [[Original date boundary and university-topic query scope]] - rationale - config/reddit_crawler.json
- [[Original historical date window, keywords and read-only baseline]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Read-only historical baseline exclusion]] - rationale - config/reddit_crawler.json
- [[SocialCrawler Reddrixyt-dlp defaults and Reddit-only wrapper]] - concept - README.md
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
- 6 edges to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 2 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 2 edges to [[_COMMUNITY_Runtime Docker dan Display]]
- 1 edge to [[_COMMUNITY_BeeSense project]]
- 1 edge to [[_COMMUNITY_Default Backend Reddit]]

## Top bridge nodes
- [[SocialCrawler Reddrixyt-dlp defaults and Reddit-only wrapper]] - degree 6, connects to 5 communities
- [[Thin Reddit-only wrapper selects shared Reddrix explicitly]] - degree 3, connects to 2 communities
- [[Tracked Reddit trial configuration]] - degree 10, connects to 1 community
- [[Original historical date window, keywords and read-only baseline]] - degree 4, connects to 1 community
- [[Thirty-minute bounded trial with non-guaranteed target]] - degree 3, connects to 1 community