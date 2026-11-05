---
type: community
members: 12
---

# app.py

**Members:** 12 nodes

## Members
- [[Dashboard build context includes root shim and artifact-reader packages]] - rationale - deployment/docker/Dockerfile.dashboard.dockerignore
- [[Dashboard-only artifactexplanationUI dependency boundary]] - rationale - requirements/dashboard.txt
- [[NumPy 2.2.6 below Python 3.14;2.3.5 on Python 3.14 and later]] - rationale - requirements/dashboard.txt
- [[Relocated dashboard image uses root Streamlit shim and runtime-only wheels]] - rationale - deployment/docker/Dockerfile.dashboard
- [[Root Cloud requirements include relocated dashboard-only runtime]] - document - requirements.txt
- [[Root Docker context allowlist for relocated dashboard runtime]] - rationale - .dockerignore
- [[Root streamlit_apps.py delegates to Dashboard.app]] - rationale - graphify-out/obsidian/Struktur Proyek.md
- [[Streamlit Community Cloud entry point; UI implementation lives in Dashboard.]] - rationale - streamlit_apps.py
- [[Streamlit entry point for local and Community Cloud dashboards.  Training lives]] - rationale - Dashboard/app.py
- [[app.py]] - code - Dashboard/app.py
- [[main()_15]] - code - Dashboard/app.py
- [[streamlit_apps.py]] - code - streamlit_apps.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/apppy
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Render Dashboard Streamlit]]
- 3 edges to [[_COMMUNITY_thread_url]]
- 3 edges to [[_COMMUNITY_thread_url_1]]
- 2 edges to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube_2]]
- 1 edge to [[_COMMUNITY_Pengujian Analisis Dashboard]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler]]
- 1 edge to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 1 edge to [[_COMMUNITY_app.py_1]]
- 1 edge to [[_COMMUNITY_Encoding dan Penyimpanan Model]]

## Top bridge nodes
- [[app.py]] - degree 16, connects to 7 communities
- [[streamlit_apps.py]] - degree 10, connects to 3 communities
- [[main()_15]] - degree 4, connects to 2 communities
- [[Dashboard build context includes root shim and artifact-reader packages]] - degree 3, connects to 1 community
- [[Root streamlit_apps.py delegates to Dashboard.app]] - degree 3, connects to 1 community