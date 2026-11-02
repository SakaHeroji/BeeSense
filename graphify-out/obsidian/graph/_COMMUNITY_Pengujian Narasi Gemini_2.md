---
type: community
cohesion: 0.24
members: 12
---

# Pengujian Narasi Gemini

**Cohesion:** 0.24 - loosely connected
**Members:** 12 nodes

## Members
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[Bind a separately published relevance dataset to the active fitted mask.]] - rationale - scripts/verify_dashboard_data.py
- [[Validate separately published X evidence without treating it as an NLP run.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[main()_15]] - code - scripts/verify_dashboard_data.py
- [[published_crawl_files()]] - code - scripts/verify_dashboard_data.py
- [[published_relevance_files()]] - code - scripts/verify_dashboard_data.py
- [[published_source_files()]] - code - scripts/verify_dashboard_data.py
- [[verify()_1]] - code - scripts/verify_dashboard_data.py
- [[verify_dashboard_data.py]] - code - scripts/verify_dashboard_data.py
- [[verify_native_dataset()]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Narasi_Gemini
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 2 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 1 edge to [[_COMMUNITY_topic_sentence_export.py]]
- 1 edge to [[_COMMUNITY_Model dan Pengujian NLP]]
- 1 edge to [[_COMMUNITY_Panduan Pipeline BeeSense]]

## Top bridge nodes
- [[verify_dashboard_data.py]] - degree 12, connects to 5 communities
- [[verify()_1]] - degree 8, connects to 1 community
- [[published_crawl_files()]] - degree 4, connects to 1 community
- [[published_relevance_files()]] - degree 4, connects to 1 community
- [[published_source_files()]] - degree 4, connects to 1 community