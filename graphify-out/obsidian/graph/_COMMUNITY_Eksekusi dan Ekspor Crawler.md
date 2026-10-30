---
type: community
members: 9
---

# Eksekusi dan Ekspor Crawler

**Members:** 9 nodes

## Members
- [[._normalize()]] - code - Crawler/Backend/social_crawler.py
- [[._source_metadata()]] - code - Crawler/Backend/social_crawler.py
- [[.export_compact()]] - code - Crawler/Backend/social_crawler.py
- [[.plan()_3]] - code - Crawler/Backend/social_crawler.py
- [[Describe the acquisition backend independently of the shared export.]] - rationale - Crawler/Backend/social_crawler.py
- [[Mixed bundles retain backend-specific provenance]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Re-export saved Contents without network or modifying the source bundle.]] - rationale - Crawler/Backend/social_crawler.py
- [[Validate and return the effective plan without browsernetwork access.]] - rationale - Crawler/Backend/social_crawler.py
- [[main()_6]] - code - Crawler/Backend/social_crawler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Eksekusi_dan_Ekspor_Crawler
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Koordinator Backend Sosial]]
- 2 edges to [[_COMMUNITY_Generator Narasi Gemini]]
- 2 edges to [[_COMMUNITY_Worker Reddrix]]
- 1 edge to [[_COMMUNITY_Pengambilan HTML Reddit]]
- 1 edge to [[_COMMUNITY_Fixture dan Pengujian Reddit]]
- 1 edge to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 1 edge to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 1 edge to [[_COMMUNITY_Default Backend Reddit]]

## Top bridge nodes
- [[main()_6]] - degree 7, connects to 5 communities
- [[.export_compact()]] - degree 5, connects to 3 communities
- [[.plan()_3]] - degree 5, connects to 2 communities
- [[._normalize()]] - degree 4, connects to 2 communities
- [[._source_metadata()]] - degree 5, connects to 1 community