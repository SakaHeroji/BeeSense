---
type: community
cohesion: 0.28
members: 9
---

# Validasi Record Reddit

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[.test_08_urls_reject_credentials_api_and_external_hosts()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_14_settings_bounds_and_no_zero_fill()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_16_hard_timeout_keeps_already_received_event()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.validate()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[Settings]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[load_settings()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[parsed_number()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[thread_url()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[timeout_fixture()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Validasi_Record_Reddit
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Parsing Identitas Reddit]]
- 6 edges to [[_COMMUNITY_Pengujian Parser Reddit]]
- 3 edges to [[_COMMUNITY_Validasi Record Reddit]]
- 2 edges to [[_COMMUNITY_Kontrak Record Reddit]]
- 2 edges to [[_COMMUNITY_Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Pengambilan HTML Reddit_1]]

## Top bridge nodes
- [[load_settings()]] - degree 6, connects to 3 communities
- [[.test_16_hard_timeout_keeps_already_received_event()]] - degree 5, connects to 3 communities
- [[Settings]] - degree 7, connects to 2 communities
- [[.validate()]] - degree 7, connects to 2 communities
- [[thread_url()]] - degree 5, connects to 2 communities