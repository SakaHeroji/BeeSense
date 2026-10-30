---
type: community
cohesion: 0.26
members: 12
---

# Konfigurasi SocialCrawler

**Cohesion:** 0.26 - loosely connected
**Members:** 12 nodes

## Members
- [[Configured 1000 new posts per platform, shared three-hour campaign]] - rationale - README.md
- [[Configured per-platform min_posts=1000 and min_comments_per_post=10]] - rationale - config/social_crawler.json
- [[Current main configuration platforms.reddit.enabled=true]] - concept - config/social_crawler.json
- [[Explicit partial export and qualified-post shortfall after acquisition]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Historical Reddit pause after HTTP 429, superseded by user-authorized resume]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Historical Reddit pause ten qualified and seventeen exported evidence posts]] - rationale - graphify-out/obsidian/Crawling 1000 Post Baru.md
- [[Historical platforms.reddit.enabled=false during requested pause]] - concept - graphify-out/obsidian/Crawling 1000 Post Baru.md
- [[Per-platform bounds max_posts 4000, max_candidates 6000]] - rationale - config/social_crawler.json
- [[Per-platform qualifying-root targets and shortfalls]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Root-publication date and literal keyword selection]] - concept - docs/crawler/SOCIAL_CRAWLER.md
- [[Target 1000 qualified new roots per platform, bounded attempts and candidates]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[User-authorized Reddit continuations preserve prior bundles and original deadline]] - rationale - docs/crawler/SOCIAL_CRAWLER.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Konfigurasi_SocialCrawler
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Topik dan Verifikasi NLP_1]]
- 6 edges to [[_COMMUNITY_Konfigurasi SocialCrawler]]
- 6 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_1]]
- 2 edges to [[_COMMUNITY_Arsitektur Crawler dan Dependensi]]
- 1 edge to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_4]]
- 1 edge to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_3]]
- 1 edge to [[_COMMUNITY_Eksplorasi Dashboard Streamlit_4]]

## Top bridge nodes
- [[Explicit partial export and qualified-post shortfall after acquisition]] - degree 7, connects to 4 communities
- [[User-authorized Reddit continuations preserve prior bundles and original deadline]] - degree 9, connects to 3 communities
- [[Per-platform qualifying-root targets and shortfalls]] - degree 6, connects to 3 communities
- [[Historical Reddit pause after HTTP 429, superseded by user-authorized resume]] - degree 6, connects to 2 communities
- [[Root-publication date and literal keyword selection]] - degree 3, connects to 2 communities