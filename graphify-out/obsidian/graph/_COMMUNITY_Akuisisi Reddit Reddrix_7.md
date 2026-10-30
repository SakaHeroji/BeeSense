---
type: community
cohesion: 0.43
members: 7
---

# Akuisisi Reddit Reddrix

**Cohesion:** 0.43 - moderately connected
**Members:** 7 nodes

## Members
- [[Crawler root-context allowlist preserves packageconfigdependency layout]] - rationale - deployment/docker/Dockerfile.crawler.dockerignore
- [[Isolated Reddrix 1.2.14 crawler dependency pins]] - concept - requirements/reddrix.txt
- [[Isolated local environment and separately downloaded browser]] - rationale - docs/crawler/REDDIT_CRAWLER.md
- [[Relocated Selenium image preserves included requirements and package modules]] - rationale - deployment/docker/Dockerfile.selenium
- [[Relocated combined crawler image runs package module as UID10001]] - rationale - deployment/docker/Dockerfile.crawler
- [[Selenium build context allows the newly included dependency manifest]] - rationale - deployment/docker/Dockerfile.selenium.dockerignore
- [[Shared crawler pins include yt-dlp and isolated Reddrix manifest]] - document - requirements/crawler.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Akuisisi_Reddit_Reddrix
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Runbook dan Verifikasi Lokal]]
- 2 edges to [[_COMMUNITY_Operasi dan Verifikasi BeeSense]]
- 1 edge to [[_COMMUNITY_Crawler Selenium Terisolasi]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_2]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_6]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_8]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_1]]
- 1 edge to [[_COMMUNITY_Arsitektur Crawler dan Dependensi]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip_3]]

## Top bridge nodes
- [[Shared crawler pins include yt-dlp and isolated Reddrix manifest]] - degree 6, connects to 3 communities
- [[Relocated combined crawler image runs package module as UID10001]] - degree 5, connects to 3 communities
- [[Isolated Reddrix 1.2.14 crawler dependency pins]] - degree 6, connects to 1 community
- [[Relocated Selenium image preserves included requirements and package modules]] - degree 4, connects to 1 community
- [[Crawler root-context allowlist preserves packageconfigdependency layout]] - degree 3, connects to 1 community