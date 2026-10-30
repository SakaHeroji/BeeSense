---
type: community
cohesion: 0.15
members: 18
---

# Operasi dan Verifikasi BeeSense

**Cohesion:** 0.15 - loosely connected
**Members:** 18 nodes

## Members
- [[._calendar_date()]] - code - Crawler/Backend/social_export.py
- [[._select()]] - code - Crawler/Backend/social_export.py
- [[._write_compact()]] - code - Crawler/Backend/social_export.py
- [[Crawler root-context allowlist preserves packageconfigdependency layout]] - rationale - deployment/docker/Dockerfile.crawler.dockerignore
- [[Isolated Reddrix 1.2.14 crawler dependency pins]] - concept - requirements/reddrix.txt
- [[Isolated local environment and separately downloaded browser]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Project the full audit rows into one sheet, applying current filters.]] - rationale - Crawler/Backend/social_export.py
- [[Relocated Selenium image preserves included requirements and package modules]] - rationale - deployment/docker/Dockerfile.selenium
- [[Relocated combined crawler image runs package module as UID10001]] - rationale - deployment/docker/Dockerfile.crawler
- [[Requires config, include and exclude matchers; performs no acquisition.]] - rationale - Crawler/Backend/social_export.py
- [[Return a local date for display; relative source dates stay estimates.]] - rationale - Crawler/Backend/social_export.py
- [[Selenium build context allows the newly included dependency manifest]] - rationale - deployment/docker/Dockerfile.selenium.dockerignore
- [[Shared crawler pins include yt-dlp and isolated Reddrix manifest]] - document - requirements/crawler.txt
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
- 3 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_3]]
- 2 edges to [[_COMMUNITY_Akuisisi Reddit Reddrix]]
- 2 edges to [[_COMMUNITY_Runbook dan Verifikasi Lokal]]
- 2 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_1]]
- 1 edge to [[_COMMUNITY_Parser dan Runner Reddit]]
- 1 edge to [[_COMMUNITY_Crawler Selenium Terisolasi]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_1]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_2]]
- 1 edge to [[_COMMUNITY_Arsitektur Crawler dan Dependensi]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip_1]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_8]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_10]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_9]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_6]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_4]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi]]

## Top bridge nodes
- [[SocialExportMixin]] - degree 14, connects to 5 communities
- [[Shared crawler pins include yt-dlp and isolated Reddrix manifest]] - degree 6, connects to 3 communities
- [[social_export.py]] - degree 5, connects to 3 communities
- [[Relocated combined crawler image runs package module as UID10001]] - degree 5, connects to 3 communities
- [[Isolated Reddrix 1.2.14 crawler dependency pins]] - degree 6, connects to 1 community