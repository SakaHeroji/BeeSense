---
type: community
cohesion: 0.17
members: 16
---

# app.py

**Cohesion:** 0.17 - loosely connected
**Members:** 16 nodes

## Members
- [[.with_source_titles()]] - code - Dashboard/app.py
- [[Dashboard build context includes root shim and artifact-reader packages]] - rationale - deployment/docker/Dockerfile.dashboard.dockerignore
- [[Dashboard-only artifactexplanationUI dependency boundary]] - rationale - requirements/dashboard.txt
- [[NumPy 2.2.6 below Python 3.14;2.3.5 on Python 3.14 and later]] - rationale - requirements/dashboard.txt
- [[Relocated dashboard image uses root Streamlit shim and runtime-only wheels]] - rationale - deployment/docker/Dockerfile.dashboard
- [[Resolve display captions from verified roots, leaving fitted files intact.]] - rationale - Dashboard/app.py
- [[Root Docker context allowlist for relocated dashboard runtime]] - rationale - .dockerignore
- [[Root streamlit_apps.py delegates to Dashboard.app]] - rationale - graphify-out/obsidian/Struktur Proyek.md
- [[Streamlit Community Cloud entry point; UI implementation lives in Dashboard.]] - rationale - streamlit_apps.py
- [[Streamlit entry point for local and Community Cloud dashboards.  Training lives]] - rationale - Dashboard/app.py
- [[_explain_filtered()]] - code - Dashboard/app.py
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
- 7 edges to [[_COMMUNITY_thread_url]]
- 5 edges to [[_COMMUNITY_Render Dashboard Streamlit]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube_1]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler_2]]
- 1 edge to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]
- 1 edge to [[_COMMUNITY_app.py_1]]
- 1 edge to [[_COMMUNITY_Pengujian Analisis Dashboard]]

## Top bridge nodes
- [[app.py]] - degree 14, connects to 4 communities
- [[streamlit_apps.py]] - degree 10, connects to 2 communities
- [[main()_8]] - degree 4, connects to 1 community
- [[_load_artifacts()]] - degree 3, connects to 1 community
- [[.with_source_titles()]] - degree 3, connects to 1 community