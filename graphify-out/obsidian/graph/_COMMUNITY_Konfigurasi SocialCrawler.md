---
type: community
cohesion: 0.16
members: 20
---

# Konfigurasi SocialCrawler

**Cohesion:** 0.16 - loosely connected
**Members:** 20 nodes

## Members
- [[1000 qualified-root targets per platform within shared three-hour budget]] - rationale - graphify-out/obsidian/Crawling 1000 Post Baru.md
- [[Configured 1000 new posts per platform, shared three-hour campaign]] - rationale - README.md
- [[Configured Reddit policy cooldown360seconds]] - concept - config/social_crawler.json
- [[Configured Reddit retry capthreeperrun]] - concept - config/social_crawler.json
- [[Configured global acquisition budget 10800 seconds]] - concept - config/social_crawler.json
- [[Configured per-platform min_posts=1000 and min_comments_per_post=10]] - rationale - config/social_crawler.json
- [[Configured platform_execution=round_robin]] - concept - config/social_crawler.json
- [[Current main configuration platforms.reddit.enabled=true]] - concept - config/social_crawler.json
- [[Explicit partial export and qualified-post shortfall after acquisition]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Historical Reddit pause after HTTP 429, superseded by user-authorized resume]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Historical Reddit pause ten qualified and seventeen exported evidence posts]] - rationale - graphify-out/obsidian/Crawling 1000 Post Baru.md
- [[Historical platforms.reddit.enabled=false during requested pause]] - concept - graphify-out/obsidian/Crawling 1000 Post Baru.md
- [[Main config now selects Reddit backend=reddrix]] - concept - config/social_crawler.json
- [[Original deadline stopped acquisition; no operation started afterward]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Per-platform bounds max_posts 4000, max_candidates 6000]] - rationale - config/social_crawler.json
- [[Per-platform qualifying-root targets and shortfalls]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Retained defaulthistorical round-robin deadline;newInstagram-onlyrun separate]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Target 1000 qualified new roots per platform, bounded attempts and candidates]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[User-authorized Reddit continuations preserve prior bundles and original deadline]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[configsocial_crawler.json]] - document - config/social_crawler.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Konfigurasi_SocialCrawler
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Topik dan Verifikasi NLP_1]]
- 8 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_2]]
- 4 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_2]]
- 3 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_4]]
- 3 edges to [[_COMMUNITY_Konfigurasi SocialCrawler_1]]
- 2 edges to [[_COMMUNITY_Snapshot NLP dan Arsip_2]]
- 1 edge to [[_COMMUNITY_Arsitektur Crawler dan Dependensi]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_6]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_3]]

## Top bridge nodes
- [[configsocial_crawler.json]] - degree 14, connects to 5 communities
- [[Retained defaulthistorical round-robin deadline;newInstagram-onlyrun separate]] - degree 10, connects to 3 communities
- [[Explicit partial export and qualified-post shortfall after acquisition]] - degree 7, connects to 3 communities
- [[Per-platform qualifying-root targets and shortfalls]] - degree 6, connects to 3 communities
- [[User-authorized Reddit continuations preserve prior bundles and original deadline]] - degree 9, connects to 2 communities