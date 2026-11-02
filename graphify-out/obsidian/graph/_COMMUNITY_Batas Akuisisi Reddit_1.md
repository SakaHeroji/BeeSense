---
type: community
cohesion: 0.16
members: 16
---

# Batas Akuisisi Reddit

**Cohesion:** 0.16 - loosely connected
**Members:** 16 nodes

## Members
- [[Configured 360-second policy and three HTTP 429 retries]] - rationale - config/reddit_crawler.json
- [[Configured new sorting differs from Reddrix capability]] - rationale - config/reddit_crawler.json
- [[Configured rootcommentcandidatetime budgets]] - rationale - config/reddit_crawler.json
- [[Keyword search uses relevance; comment sort is unsupported]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Only verified HTTP 429 uses bounded coordinator cooldown]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Original date boundary and university-topic query scope]] - rationale - config/reddit_crawler.json
- [[Original historical date window, keywords and read-only baseline]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Read-only historical baseline exclusion]] - rationale - config/reddit_crawler.json
- [[Thin Reddit-only wrapper selects shared Reddrix explicitly]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Thirty-minute bounded trial with non-guaranteed target]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Tracked Reddit trial configuration]] - concept - config/reddit_crawler.json
- [[Tracked reddrix.display_mode=auto]] - concept - config/reddit_crawler.json
- [[Trial config now explicitly selects Reddrix; wrapper preserves legacy compatibility]] - rationale - config/reddit_crawler.json
- [[Unknown anti-bot exception maps to ACCESS_BLOCKED]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Unknown dates, metrics and actors remain unknown]] - rationale - graphify-out/obsidian/RedditCrawler Reddrix.md
- [[Unknown source fields and upstream capability limits]] - rationale - graphify-out/obsidian/RedditCrawler Reddrix.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Batas_Akuisisi_Reddit
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 2 edges to [[_COMMUNITY_Batas Akuisisi Reddit_2]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler]]

## Top bridge nodes
- [[Thin Reddit-only wrapper selects shared Reddrix explicitly]] - degree 3, connects to 2 communities
- [[Original historical date window, keywords and read-only baseline]] - degree 4, connects to 1 community
- [[Unknown source fields and upstream capability limits]] - degree 4, connects to 1 community
- [[Keyword search uses relevance; comment sort is unsupported]] - degree 3, connects to 1 community
- [[Thirty-minute bounded trial with non-guaranteed target]] - degree 3, connects to 1 community