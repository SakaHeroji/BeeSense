---
type: community
cohesion: 0.14
members: 20
---

# app.py

**Cohesion:** 0.14 - loosely connected
**Members:** 20 nodes

## Members
- [[._methods()]] - code - Dashboard/app.py
- [[.test_audit_csv_escapes_formulas_without_changing_stored_text()]] - code - tests/nlp/test_context_relevance.py
- [[Dashboard build context includes root shim and artifact-reader packages]] - rationale - deployment/docker/Dockerfile.dashboard.dockerignore
- [[Dashboard-only artifactexplanationUI dependency boundary]] - rationale - requirements/dashboard.txt
- [[Keep original audit data intact; escape spreadsheet formulas on export.]] - rationale - Dashboard/app.py
- [[NumPy 2.2.6 below Python 3.14;2.3.5 on Python 3.14 and later]] - rationale - requirements/dashboard.txt
- [[Obsidian Cloud runbook streamlit_apps.py, Python 3.12 and complete artifact publication]] - document - graphify-out/obsidian/Menjalankan BeeSense.md
- [[Relocated dashboard image uses root Streamlit shim and runtime-only wheels]] - rationale - deployment/docker/Dockerfile.dashboard
- [[Root Cloud requirements include relocated dashboard-only runtime]] - document - requirements.txt
- [[Root Docker context allowlist for relocated dashboard runtime]] - rationale - .dockerignore
- [[Root streamlit_apps.py delegates to Dashboard.app]] - rationale - graphify-out/obsidian/Struktur Proyek.md
- [[Streamlit Community Cloud entry point; UI implementation lives in Dashboard.]] - rationale - streamlit_apps.py
- [[Streamlit entry point for local and Community Cloud dashboards.  Training lives]] - rationale - Dashboard/app.py
- [[_explain_filtered()]] - code - Dashboard/app.py
- [[_load_artifacts()]] - code - Dashboard/app.py
- [[app.py]] - code - Dashboard/app.py
- [[main()_11]] - code - Dashboard/app.py
- [[relevance_csv()]] - code - Dashboard/app.py
- [[streamlit_apps.py]] - code - streamlit_apps.py
- [[test_dashboard_analysis.py]] - code - tests/nlp/test_dashboard_analysis.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/apppy
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Render Dashboard Streamlit]]
- 5 edges to [[_COMMUNITY_app.py_1]]
- 4 edges to [[_COMMUNITY_thread_url]]
- 3 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 2 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 2 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube_1]]
- 1 edge to [[_COMMUNITY_Alur Dataset Model Dashboard]]
- 1 edge to [[_COMMUNITY_Batas Akuisisi Reddit_3]]
- 1 edge to [[_COMMUNITY_Penggabungan Dataset]]
- 1 edge to [[_COMMUNITY_Pengujian Analisis Dashboard]]

## Top bridge nodes
- [[app.py]] - degree 17, connects to 5 communities
- [[._methods()]] - degree 5, connects to 3 communities
- [[streamlit_apps.py]] - degree 10, connects to 2 communities
- [[main()_11]] - degree 4, connects to 2 communities
- [[_explain_filtered()]] - degree 3, connects to 2 communities