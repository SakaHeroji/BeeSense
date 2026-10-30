---
type: community
cohesion: 0.36
members: 8
---

# Pipeline dan Persistensi NLP

**Cohesion:** 0.36 - loosely connected
**Members:** 8 nodes

## Members
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[main()_8]] - code - scripts/verify_dashboard_data.py
- [[published_source_files()]] - code - scripts/verify_dashboard_data.py
- [[verify()_1]] - code - scripts/verify_dashboard_data.py
- [[verify_dashboard_data.py]] - code - scripts/verify_dashboard_data.py
- [[verify_native_dataset()]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pipeline_dan_Persistensi_NLP
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_1]]
- 3 edges to [[_COMMUNITY_Ringkasan Topik Gemini]]
- 2 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP]]
- 2 edges to [[_COMMUNITY_Topik dan Verifikasi NLP]]

## Top bridge nodes
- [[verify_dashboard_data.py]] - degree 9, connects to 3 communities
- [[verify()_1]] - degree 7, connects to 2 communities
- [[published_source_files()]] - degree 5, connects to 2 communities
- [[verify_native_dataset()]] - degree 5, connects to 2 communities