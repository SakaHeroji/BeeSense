---
type: community
members: 12
---

# config/social_crawler.json

**Members:** 12 nodes

## Members
- [[Configured 1,000 qualified roots per platform in a shared three-hour campaign]] - rationale - README.md
- [[Configured Reddit policy cooldown360seconds]] - concept - config/social_crawler.json
- [[Configured Reddit retry capthreeperrun]] - concept - config/social_crawler.json
- [[Configured per-platform min_posts=1000 and min_comments_per_post=10]] - rationale - config/social_crawler.json
- [[Main config now selects Reddit backend=reddrix]] - concept - config/social_crawler.json
- [[Main root reddrix.display_mode=auto]] - concept - config/social_crawler.json
- [[Package ROOT preserves repository-relative configuration and artifact paths]] - rationale - docs/PROJECT_STRUCTURE.md
- [[Per-platform bounds max_posts 4000, max_candidates 6000]] - rationale - config/social_crawler.json
- [[Root publication dates and literal keyword selection]] - concept - docs/crawler/SOCIAL_CRAWLER.md
- [[Target 1,000 qualified roots with bounded attempts and candidates]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[YouTube date hint aids discovery; timestamp filter decides eligibility]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[configsocial_crawler.json]] - document - config/social_crawler.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/config/social_crawlerjson
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Koordinator Backend Sosial]]
- 3 edges to [[_COMMUNITY_Round Robin Shared Deadline]]
- 3 edges to [[_COMMUNITY_Historical Reddit continuations preserve bundles and original deadline]]
- 2 edges to [[_COMMUNITY_Read-only nativecanonical index excludes 50 YouTube and 181 Reddit roots]]
- 2 edges to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 2 edges to [[_COMMUNITY_.score_coherence]]
- 2 edges to [[_COMMUNITY_Konfigurasi Model Aktif]]
- 1 edge to [[_COMMUNITY_BeeSense project]]
- 1 edge to [[_COMMUNITY_Default Backend Reddit]]

## Top bridge nodes
- [[configsocial_crawler.json]] - degree 14, connects to 4 communities
- [[Target 1,000 qualified roots with bounded attempts and candidates]] - degree 6, connects to 2 communities
- [[YouTube date hint aids discovery; timestamp filter decides eligibility]] - degree 3, connects to 2 communities
- [[Configured per-platform min_posts=1000 and min_comments_per_post=10]] - degree 3, connects to 1 community
- [[Package ROOT preserves repository-relative configuration and artifact paths]] - degree 3, connects to 1 community