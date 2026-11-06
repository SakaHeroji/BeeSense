---
type: community
cohesion: 0.25
members: 8
---

# Integrasi Default Instaloader

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[Instagram backend browser ChromePlaywright]] - concept - docs/crawler/INSTAGRAM_CRAWLER.md
- [[Instagram browser thread tersedia pada dokumen, kelengkapan tidak dijamin]] - concept - docs/crawler/INSTAGRAM_CRAWLER.md
- [[Instagram 1000 post, semua komentar tersedia tanpa cap]] - concept - docs/crawler/INSTAGRAM_CRAWLER.md
- [[InstagramCrawler instagrapi atau browser]] - concept - docs/crawler/INSTAGRAM_CRAWLER.md
- [[Komentar dipertahankan seluruhnya; filter root tetap berlaku]] - rationale - docs/crawler/INSTAGRAM_CRAWLER.md
- [[Storage Excel default; PostgreSQL memakai nama env DSN]] - concept - config/social_crawler.json
- [[Target 1000 per platform dengan durasi dan cap nullable]] - concept - config/social_crawler.json
- [[social_crawler.json sumber konfigurasi universal]] - document - config/social_crawler.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Integrasi_Default_Instaloader
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Panduan Pipeline BeeSense_1]]
- 1 edge to [[_COMMUNITY_Konfigurasi Crawler Bersama]]
- 1 edge to [[_COMMUNITY_Integrasi Default Instaloader_6]]

## Top bridge nodes
- [[social_crawler.json sumber konfigurasi universal]] - degree 5, connects to 2 communities
- [[InstagramCrawler instagrapi atau browser]] - degree 5, connects to 1 community