---
type: community
cohesion: 0.17
members: 12
---

# Konfigurasi SocialCrawler

**Cohesion:** 0.17 - loosely connected
**Members:** 12 nodes

## Members
- [[._event()]] - code - Crawler/Backend/social_crawler.py
- [[._wait_for_captcha()]] - code - Crawler/Backend/social_crawler.py
- [[Advanced connected-browser Reddit campaign helpers]] - document - Crawler/Backend/Reddit/README_browser_campaign.md
- [[Atomic sibling .progress.json snapshots during acquisition]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Checkpoint export to the eight-sheet contract]] - concept - Crawler/Backend/Reddit/README_browser_campaign.md
- [[Coordinator waits for manual CAPTCHA without automated clicks]] - rationale - Crawler/Backend/Reddit/README_playwright.md
- [[Historical or explicitly selected Playwright CAPTCHA wait]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Isolated Chrome profile, manual CAPTCHA wait and access-barrier stops]] - rationale - Crawler/Backend/Reddit/README_playwright.md
- [[Native-ID provenance and bounded public excerpts]] - rationale - Crawler/Backend/Reddit/README_browser_campaign.md
- [[Reddit Playwright CLI runner]] - document - Crawler/Backend/Reddit/README_playwright.md
- [[Retained Playwright-only CAPTCHA fields600-second wait and five-second poll]] - rationale - config/social_crawler.json
- [[Standalone runner stops 429; coordinator 1.3 supports bounded cooldown]] - rationale - Crawler/Backend/Reddit/README_playwright.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Konfigurasi_SocialCrawler
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_2]]
- 3 edges to [[_COMMUNITY_Konfigurasi SocialCrawler]]
- 2 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_2]]
- 1 edge to [[_COMMUNITY_Arsitektur Crawler dan Dependensi]]
- 1 edge to [[_COMMUNITY_Topik dan Verifikasi NLP_1]]

## Top bridge nodes
- [[Reddit Playwright CLI runner]] - degree 6, connects to 2 communities
- [[._event()]] - degree 4, connects to 2 communities
- [[Atomic sibling .progress.json snapshots during acquisition]] - degree 3, connects to 2 communities
- [[Advanced connected-browser Reddit campaign helpers]] - degree 4, connects to 1 community
- [[._wait_for_captcha()]] - degree 4, connects to 1 community