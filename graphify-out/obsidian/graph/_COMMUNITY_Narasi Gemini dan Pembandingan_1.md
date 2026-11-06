---
type: community
cohesion: 0.12
members: 25
---

# Narasi Gemini dan Pembandingan

**Cohesion:** 0.12 - loosely connected
**Members:** 25 nodes

## Members
- [[.evaluate_run_coherence()]] - code - MachineLearning/social_nlp.py
- [[.explain_artifacts()]] - code - MachineLearning/social_nlp.py
- [[.load_explanations()]] - code - MachineLearning/social_nlp.py
- [[.load_run()]] - code - MachineLearning/social_nlp.py
- [[.test_artifacts_roundtrip_without_pickle_and_verify_checksums()]] - code - tests/nlp/test_social_nlp.py
- [[.test_excel_extension_loads_without_gemini_and_binds_membership_and_bytes()]] - code - tests/nlp/test_social_nlp.py
- [[.test_legacy_v1_artifact_and_explanations_remain_readable()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_run_coherence_reproduces_the_published_score()]] - code - tests/nlp/test_social_nlp.py
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[Bind a separately published relevance dataset to the active fitted mask.]] - rationale - scripts/verify_dashboard_data.py
- [[Explain already verified artifacts without encoding or fitting again.]] - rationale - MachineLearning/social_nlp.py
- [[Start the local relevance experiment, or its preserved baseline snapshot.]] - rationale - scripts/relevance_dashboard.py
- [[Validate separately published X evidence without treating it as an NLP run.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[file_hash()]] - code - MachineLearning/social_nlp.py
- [[main()_6]] - code - scripts/relevance_dashboard.py
- [[main()_7]] - code - scripts/verify_dashboard_data.py
- [[published_crawl_files()]] - code - scripts/verify_dashboard_data.py
- [[published_relevance_files()]] - code - scripts/verify_dashboard_data.py
- [[published_source_files()]] - code - scripts/verify_dashboard_data.py
- [[relevance_dashboard.py]] - code - scripts/relevance_dashboard.py
- [[verify()_2]] - code - scripts/verify_dashboard_data.py
- [[verify_dashboard_data.py]] - code - scripts/verify_dashboard_data.py
- [[verify_native_dataset()]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Narasi_Gemini_dan_Pembandingan
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_3]]
- 10 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 7 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 7 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 3 edges to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik]]
- 1 edge to [[_COMMUNITY_Encoding dan Penyimpanan Model_2]]

## Top bridge nodes
- [[file_hash()]] - degree 22, connects to 6 communities
- [[.load_run()]] - degree 12, connects to 3 communities
- [[.evaluate_run_coherence()]] - degree 5, connects to 3 communities
- [[verify_dashboard_data.py]] - degree 10, connects to 2 communities
- [[.explain_artifacts()]] - degree 5, connects to 2 communities