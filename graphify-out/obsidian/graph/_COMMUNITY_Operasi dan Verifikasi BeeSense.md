---
type: community
cohesion: 0.22
members: 11
---

# Operasi dan Verifikasi BeeSense

**Cohesion:** 0.22 - loosely connected
**Members:** 11 nodes

## Members
- [[._calendar_date()]] - code - Crawler/Backend/social_export.py
- [[._select()]] - code - Crawler/Backend/social_export.py
- [[._write_compact()]] - code - Crawler/Backend/social_export.py
- [[Project the full audit rows into one sheet, applying current filters.]] - rationale - Crawler/Backend/social_export.py
- [[Requires config, include and exclude matchers; performs no acquisition.]] - rationale - Crawler/Backend/social_export.py
- [[Return a local date for display; relative source dates stay estimates.]] - rationale - Crawler/Backend/social_export.py
- [[Shared root selection and formula-safe Excel projection for social crawlers.]] - rationale - Crawler/Backend/social_export.py
- [[SocialExportMixin]] - code - Crawler/Backend/social_export.py
- [[Standalone Instagram uses existing auditcompact Excel contract]] - concept - docs/crawler/INSTAGRAM_CRAWLER.md
- [[Three unchanged SocialCrawler methods moved to SocialExportMixin]] - rationale - docs/crawler/INSTAGRAM_CRAWLER.md
- [[social_export.py]] - code - Crawler/Backend/social_export.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Operasi_dan_Verifikasi_BeeSense
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_1]]
- 3 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_5]]
- 2 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_1]]
- 2 edges to [[_COMMUNITY_Akuisisi Reddit Reddrix_7]]
- 1 edge to [[_COMMUNITY_Parser dan Runner Reddit]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_9]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_8]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_6]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_2]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi]]

## Top bridge nodes
- [[SocialExportMixin]] - degree 16, connects to 8 communities
- [[social_export.py]] - degree 5, connects to 3 communities
- [[._write_compact()]] - degree 5, connects to 1 community
- [[Three unchanged SocialCrawler methods moved to SocialExportMixin]] - degree 3, connects to 1 community
- [[Standalone Instagram uses existing auditcompact Excel contract]] - degree 2, connects to 1 community