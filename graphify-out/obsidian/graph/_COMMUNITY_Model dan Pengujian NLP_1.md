---
type: community
cohesion: 0.15
members: 15
---

# Model dan Pengujian NLP

**Cohesion:** 0.15 - loosely connected
**Members:** 15 nodes

## Members
- [[.test_shipped_dashboard_and_explanations_need_no_training_environment()]] - code - tests/cloud/test_dashboard_runtime.py
- [[CloudRuntimeTests]] - code - tests/cloud/test_dashboard_runtime.py
- [[DashboardTests]] - code - tests/nlp/test_social_nlp.py
- [[No modelnetwork calls policy, provenance and integration regressions.]] - rationale - tests/nlp/test_context_relevance.py
- [[Resolve one editable NLP config and optional legacy partial overrides.      Expl]] - rationale - MachineLearning/social_nlp.py
- [[Run in an isolated Cloud environment, using only root requirements.txt.]] - rationale - tests/cloud/test_dashboard_runtime.py
- [[Start the local relevance experiment, or its preserved baseline snapshot.]] - rationale - scripts/relevance_dashboard.py
- [[load_config()]] - code - MachineLearning/social_nlp.py
- [[main()_7]] - code - scripts/relevance_dashboard.py
- [[relevance_dashboard.py]] - code - scripts/relevance_dashboard.py
- [[social_nlp.py]] - code - MachineLearning/social_nlp.py
- [[test_context_relevance.py]] - code - tests/nlp/test_context_relevance.py
- [[test_dashboard_runtime.py]] - code - tests/cloud/test_dashboard_runtime.py
- [[test_social_nlp.py]] - code - tests/nlp/test_social_nlp.py
- [[test_streamlit_app.py]] - code - tests/nlp/test_streamlit_app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Model_dan_Pengujian_NLP
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 7 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 5 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 5 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 3 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 2 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 2 edges to [[_COMMUNITY_Arsip Data Harian]]
- 1 edge to [[_COMMUNITY_Pengujian UI Streamlit]]
- 1 edge to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 1 edge to [[_COMMUNITY_thread_url]]
- 1 edge to [[_COMMUNITY_thread_url_1]]
- 1 edge to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_2]]
- 1 edge to [[_COMMUNITY_app.py]]

## Top bridge nodes
- [[social_nlp.py]] - degree 21, connects to 8 communities
- [[test_social_nlp.py]] - degree 10, connects to 4 communities
- [[test_context_relevance.py]] - degree 9, connects to 3 communities
- [[test_streamlit_app.py]] - degree 6, connects to 3 communities
- [[DashboardTests]] - degree 4, connects to 3 communities