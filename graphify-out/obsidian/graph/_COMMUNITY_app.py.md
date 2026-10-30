---
type: community
members: 10
---

# app.py

**Members:** 10 nodes

## Members
- [[Dashboard build context includes root shim and artifact-reader packages]] - rationale - deployment/docker/Dockerfile.dashboard.dockerignore
- [[Relocated dashboard image uses root Streamlit shim and runtime-only wheels]] - rationale - deployment/docker/Dockerfile.dashboard
- [[Root Docker context allowlist for relocated dashboard runtime]] - rationale - .dockerignore
- [[Streamlit Community Cloud entry point; UI implementation lives in Dashboard.]] - rationale - streamlit_apps.py
- [[Streamlit entry point for local and Community Cloud dashboards.  Training lives]] - rationale - Dashboard/app.py
- [[_load_artifacts()]] - code - Dashboard/app.py
- [[app.py]] - code - Dashboard/app.py
- [[main()_8]] - code - Dashboard/app.py
- [[streamlit_apps.py]] - code - streamlit_apps.py
- [[test_dashboard_analysis.py]] - code - tests/nlp/test_dashboard_analysis.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/apppy
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Render Dashboard Streamlit]]
- 4 edges to [[_COMMUNITY_Struktur Runtime Dashboard]]
- 3 edges to [[_COMMUNITY_thread_url]]
- 3 edges to [[_COMMUNITY_Konfigurasi Model Aktif]]
- 2 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 2 edges to [[_COMMUNITY_Verifikasi Artefak Dataset]]
- 2 edges to [[_COMMUNITY_.render]]
- 1 edge to [[_COMMUNITY_Bukti Ekstraktif Topik]]
- 1 edge to [[_COMMUNITY_.topic_figure]]
- 1 edge to [[_COMMUNITY_Generator Narasi Gemini]]
- 1 edge to [[_COMMUNITY_Pengujian Analisis Dashboard]]

## Top bridge nodes
- [[app.py]] - degree 16, connects to 7 communities
- [[streamlit_apps.py]] - degree 12, connects to 3 communities
- [[Root Docker context allowlist for relocated dashboard runtime]] - degree 5, connects to 2 communities
- [[main()_8]] - degree 4, connects to 2 communities
- [[_load_artifacts()]] - degree 3, connects to 2 communities