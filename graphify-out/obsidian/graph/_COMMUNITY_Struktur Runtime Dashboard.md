---
type: community
members: 19
---

# Struktur Runtime Dashboard

**Members:** 19 nodes

## Members
- [[Cloud root requirements install dashboard-only dependencies]] - rationale - README.md
- [[Dashboard build context includes root shim and artifact-reader packages]] - rationale - deployment/docker/Dockerfile.dashboard.dockerignore
- [[Dashboard-only artifactexplanationUI dependency boundary]] - rationale - requirements/dashboard.txt
- [[Historical Python 3.14.10 install failure ONNX wheels and Numba support]] - rationale - README.md
- [[NumPy 2.2.6 below Python 3.14;2.3.5 on Python 3.14 and later]] - rationale - requirements/dashboard.txt
- [[Obsidian Cloud runbook streamlit_apps.py, Python 3.12 and complete artifact publication]] - document - graphify-out/obsidian/Menjalankan BeeSense.md
- [[Obsidian runbook records Python 3.14 failure and dashboard-only packaging fix]] - document - graphify-out/obsidian/Menjalankan BeeSense.md
- [[PyArrow 24.0.0 matches Cloud threaded-import compatibility guard]] - rationale - README.md
- [[Relocated dashboard image uses root Streamlit shim and runtime-only wheels]] - rationale - deployment/docker/Dockerfile.dashboard
- [[Root Cloud requirements include relocated dashboard-only runtime]] - document - requirements.txt
- [[Root Docker context allowlist for relocated dashboard runtime]] - rationale - .dockerignore
- [[Root streamlit_apps.py delegates to Dashboard.app]] - rationale - docs/PROJECT_STRUCTURE.md
- [[Root streamlit_apps.py delegates to Dashboard.app_1]] - rationale - graphify-out/obsidian/Struktur Proyek.md
- [[Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12]] - rationale - docs/machine-learning/SOCIAL_NLP.md
- [[Streamlit Community Cloud entry point; UI implementation lives in Dashboard.]] - rationale - streamlit_apps.py
- [[Streamlit entry point for local and Community Cloud dashboards.  Training lives]] - rationale - Dashboard/app.py
- [[_load_artifacts()]] - code - Dashboard/app.py
- [[app.py]] - code - Dashboard/app.py
- [[streamlit_apps.py]] - code - streamlit_apps.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Struktur_Runtime_Dashboard
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Render Dashboard Streamlit]]
- 5 edges to [[_COMMUNITY_Konfigurasi Model Aktif]]
- 4 edges to [[_COMMUNITY_Riwayat Dataset dan Metodologi]]
- 3 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 2 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 1 edge to [[_COMMUNITY_.topic_figure]]
- 1 edge to [[_COMMUNITY_Generator Narasi Gemini]]
- 1 edge to [[_COMMUNITY_Pengujian Analisis Dashboard]]
- 1 edge to [[_COMMUNITY_Alur Dataset Model Dashboard]]
- 1 edge to [[_COMMUNITY_Audit Akuisisi Instagram]]

## Top bridge nodes
- [[app.py]] - degree 16, connects to 4 communities
- [[streamlit_apps.py]] - degree 12, connects to 3 communities
- [[Root streamlit_apps.py delegates to Dashboard.app]] - degree 4, connects to 3 communities
- [[Obsidian Cloud runbook streamlit_apps.py, Python 3.12 and complete artifact publication]] - degree 5, connects to 2 communities
- [[_load_artifacts()]] - degree 3, connects to 2 communities