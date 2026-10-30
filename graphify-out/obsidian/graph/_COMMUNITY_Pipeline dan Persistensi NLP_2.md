---
type: community
cohesion: 0.19
members: 17
---

# Pipeline dan Persistensi NLP

**Cohesion:** 0.19 - loosely connected
**Members:** 17 nodes

## Members
- [[.evaluate_run_coherence()]] - code - MachineLearning/social_nlp.py
- [[.load_explanations()]] - code - MachineLearning/social_nlp.py
- [[.load_run()]] - code - MachineLearning/social_nlp.py
- [[.test_artifacts_roundtrip_without_pickle_and_verify_checksums()]] - code - tests/nlp/test_social_nlp.py
- [[.test_csv_manifest_and_roundtrip_bind_every_topic_and_keyword_weight()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_legacy_v1_artifact_and_explanations_remain_readable()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_run_coherence_reproduces_the_published_score()]] - code - tests/nlp/test_social_nlp.py
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[file_hash()]] - code - MachineLearning/social_nlp.py
- [[main()_9]] - code - scripts/verify_dashboard_data.py
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
- 14 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP]]
- 9 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_1]]
- 5 edges to [[_COMMUNITY_Ringkasan Topik Gemini]]
- 3 edges to [[_COMMUNITY_Eksplorasi Dashboard Streamlit_3]]
- 2 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_3]]
- 2 edges to [[_COMMUNITY_Ringkasan Topik Gemini_1]]
- 2 edges to [[_COMMUNITY_Topik dan Verifikasi NLP]]
- 1 edge to [[_COMMUNITY_Bundle Excel dan Provenans]]
- 1 edge to [[_COMMUNITY_Adapter Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_3]]
- 1 edge to [[_COMMUNITY_Pipeline dan Persistensi NLP_4]]

## Top bridge nodes
- [[file_hash()]] - degree 26, connects to 8 communities
- [[.load_run()]] - degree 12, connects to 4 communities
- [[.evaluate_run_coherence()]] - degree 5, connects to 3 communities
- [[verify_dashboard_data.py]] - degree 9, connects to 2 communities
- [[verify_native_dataset()]] - degree 5, connects to 2 communities