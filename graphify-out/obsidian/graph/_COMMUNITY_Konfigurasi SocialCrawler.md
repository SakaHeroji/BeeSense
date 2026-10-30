---
type: community
cohesion: 0.15
members: 16
---

# Konfigurasi SocialCrawler

**Cohesion:** 0.15 - loosely connected
**Members:** 16 nodes

## Members
- [[._event()]] - code - Crawler/Backend/social_crawler.py
- [[._wait_for_captcha()]] - code - Crawler/Backend/social_crawler.py
- [[1000 qualified-root targets per platform within shared three-hour budget]] - rationale - graphify-out/obsidian/Crawling 1000 Post Baru.md
- [[Atomic sibling .progress.json snapshots during acquisition]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Configured Reddit policy cooldown360seconds]] - concept - config/social_crawler.json
- [[Configured Reddit retry capthreeperrun]] - concept - config/social_crawler.json
- [[Configured global acquisition budget 10800 seconds]] - concept - config/social_crawler.json
- [[Configured platform_execution=round_robin]] - concept - config/social_crawler.json
- [[Coordinator waits for manual CAPTCHA without automated clicks]] - rationale - Crawler/Backend/Reddit/README_playwright.md
- [[Historical or explicitly selected Playwright CAPTCHA wait]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Main config now selects Reddit backend=reddrix]] - concept - config/social_crawler.json
- [[Main root reddrix.display_mode=auto]] - concept - config/social_crawler.json
- [[Original deadline stopped acquisition; no operation started afterward]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Retained Playwright-only CAPTCHA fields600-second wait and five-second poll]] - rationale - config/social_crawler.json
- [[Retained defaulthistorical round-robin deadline;newInstagram-onlyrun separate]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[configsocial_crawler.json]] - document - config/social_crawler.json

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Konfigurasi_SocialCrawler
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Konfigurasi SocialCrawler_1]]
- 5 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_1]]
- 4 edges to [[_COMMUNITY_Topik dan Verifikasi NLP_1]]
- 4 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_3]]
- 1 edge to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_5]]
- 1 edge to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_4]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip_5]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_2]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix]]

## Top bridge nodes
- [[configsocial_crawler.json]] - degree 14, connects to 4 communities
- [[Retained defaulthistorical round-robin deadline;newInstagram-onlyrun separate]] - degree 10, connects to 3 communities
- [[._event()]] - degree 4, connects to 2 communities
- [[Original deadline stopped acquisition; no operation started afterward]] - degree 3, connects to 2 communities
- [[._wait_for_captcha()]] - degree 4, connects to 1 community