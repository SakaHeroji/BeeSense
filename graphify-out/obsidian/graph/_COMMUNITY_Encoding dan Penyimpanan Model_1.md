---
type: community
cohesion: 0.13
members: 24
---

# Encoding dan Penyimpanan Model

**Cohesion:** 0.13 - loosely connected
**Members:** 24 nodes

## Members
- [[.evaluate_run_coherence()]] - code - MachineLearning/social_nlp.py
- [[.explain_artifacts()]] - code - MachineLearning/social_nlp.py
- [[.load_explanations()]] - code - MachineLearning/social_nlp.py
- [[.load_run()]] - code - MachineLearning/social_nlp.py
- [[.save_explanations()]] - code - MachineLearning/social_nlp.py
- [[.test_artifacts_roundtrip_without_pickle_and_verify_checksums()]] - code - tests/nlp/test_social_nlp.py
- [[.test_excel_extension_loads_without_gemini_and_binds_membership_and_bytes()]] - code - tests/nlp/test_social_nlp.py
- [[.test_legacy_v1_artifact_and_explanations_remain_readable()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_run_coherence_reproduces_the_published_score()]] - code - tests/nlp/test_social_nlp.py
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[Explain already verified artifacts without encoding or fitting again.]] - rationale - MachineLearning/social_nlp.py
- [[Publish a new versioned sidecar; never modify the original run.]] - rationale - MachineLearning/social_nlp.py
- [[Validate separately published X evidence without treating it as an NLP run.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[file_hash()]] - code - MachineLearning/social_nlp.py
- [[main()_11]] - code - MachineLearning/social_nlp.py
- [[main()_13]] - code - scripts/verify_dashboard_data.py
- [[published_crawl_files()]] - code - scripts/verify_dashboard_data.py
- [[published_source_files()]] - code - scripts/verify_dashboard_data.py
- [[verify()_1]] - code - scripts/verify_dashboard_data.py
- [[verify_dashboard_data.py]] - code - scripts/verify_dashboard_data.py
- [[verify_native_dataset()]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Encoding_dan_Penyimpanan_Model
SORT file.name ASC
```

## Connections to other communities
- 15 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 9 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 9 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 4 edges to [[_COMMUNITY_app.py]]
- 4 edges to [[_COMMUNITY_Penggabungan Dataset]]
- 3 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 2 edges to [[_COMMUNITY_Bukti Ekstraktif Topik]]
- 2 edges to [[_COMMUNITY_Bukti Ekstraktif Topik_1]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Pengujian UI Streamlit]]
- 1 edge to [[_COMMUNITY_Eksekusi dan Ekspor Crawler]]
- 1 edge to [[_COMMUNITY_Model dan Pengujian NLP_1]]

## Top bridge nodes
- [[file_hash()]] - degree 30, connects to 10 communities
- [[.load_run()]] - degree 15, connects to 7 communities
- [[main()_11]] - degree 10, connects to 4 communities
- [[verify_dashboard_data.py]] - degree 11, connects to 3 communities
- [[.explain_artifacts()]] - degree 6, connects to 3 communities