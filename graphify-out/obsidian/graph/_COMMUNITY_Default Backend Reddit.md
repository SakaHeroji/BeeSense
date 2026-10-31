---
type: community
cohesion: 0.22
members: 10
---

# Default Backend Reddit

**Cohesion:** 0.22 - loosely connected
**Members:** 10 nodes

## Members
- [[Async Reddrix to validated records to existing Excel pipeline]] - rationale - graphify-out/obsidian/RedditCrawler Reddrix.md
- [[Default Reddit Reddrix with YouTube yt-dlp since SocialCrawler 1.4]] - concept - docs/crawler/SOCIAL_CRAWLER.md
- [[Explicit legacy HTML, Playwright and checkpoint selections]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Folder moves preserve data paths, artifact bytes and historical crawl results]] - rationale - graphify-out/obsidian/Struktur Proyek.md
- [[Hard-deadline subprocess retains streamed records]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Integrated SocialCrawler Reddrix with thin Reddit-only wrapper]] - document - graphify-out/obsidian/RedditCrawler Reddrix.md
- [[Main config now selects Reddit backend=reddrix]] - concept - config/social_crawler.json
- [[No databasemodelpersistent-contract migration]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[RedditCrawler wrapper delegates to the shared coordinator]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Reddrix trial preserves existing model and frontend boundaries]] - rationale - graphify-out/obsidian/RedditCrawler Reddrix.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Default_Backend_Reddit
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Batas Akuisisi Reddit]]
- 3 edges to [[_COMMUNITY_Koordinator Backend Sosial]]
- 3 edges to [[_COMMUNITY_Runtime Docker dan Display]]
- 2 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 2 edges to [[_COMMUNITY_Worker Reddrix]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit_1]]
- 1 edge to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 1 edge to [[_COMMUNITY_Validasi Record Reddit]]
- 1 edge to [[_COMMUNITY_Arsitektur Model dan Dashboard]]
- 1 edge to [[_COMMUNITY_Struktur Runtime Dashboard]]
- 1 edge to [[_COMMUNITY_Eksekusi dan Ekspor Crawler]]

## Top bridge nodes
- [[Default Reddit Reddrix with YouTube yt-dlp since SocialCrawler 1.4]] - degree 9, connects to 5 communities
- [[Integrated SocialCrawler Reddrix with thin Reddit-only wrapper]] - degree 11, connects to 4 communities
- [[RedditCrawler wrapper delegates to the shared coordinator]] - degree 5, connects to 3 communities
- [[Async Reddrix to validated records to existing Excel pipeline]] - degree 5, connects to 3 communities
- [[Hard-deadline subprocess retains streamed records]] - degree 3, connects to 2 communities