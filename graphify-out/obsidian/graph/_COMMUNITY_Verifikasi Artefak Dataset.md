---
type: community
members: 15
---

# Verifikasi Artefak Dataset

**Members:** 15 nodes

## Members
- [[.load_explanations()]] - code - MachineLearning/social_nlp.py
- [[.load_run()]] - code - MachineLearning/social_nlp.py
- [[.test_artifacts_roundtrip_without_pickle_and_verify_checksums()]] - code - tests/nlp/test_social_nlp.py
- [[.test_excel_extension_loads_without_gemini_and_binds_membership_and_bytes()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_run_coherence_reproduces_the_published_score()]] - code - tests/nlp/test_social_nlp.py
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[file_hash()]] - code - MachineLearning/social_nlp.py
- [[main()_12]] - code - scripts/verify_dashboard_data.py
- [[published_source_files()]] - code - scripts/verify_dashboard_data.py
- [[verify()_1]] - code - scripts/verify_dashboard_data.py
- [[verify_dashboard_data.py]] - code - scripts/verify_dashboard_data.py
- [[verify_native_dataset()]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Verifikasi_Artefak_Dataset
SORT file.name ASC
```

## Connections to other communities
- 14 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 10 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 5 edges to [[_COMMUNITY_Generator Narasi Gemini]]
- 5 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 3 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 2 edges to [[_COMMUNITY_Eksekusi dan Ekspor Crawler]]
- 2 edges to [[_COMMUNITY_app.py]]
- 2 edges to [[_COMMUNITY_Penggabungan Dataset]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_.render]]
- 1 edge to [[_COMMUNITY_Bukti Ekstraktif Topik]]
- 1 edge to [[_COMMUNITY_Pengujian UI Streamlit]]

## Top bridge nodes
- [[file_hash()]] - degree 29, connects to 10 communities
- [[.load_run()]] - degree 16, connects to 7 communities
- [[verify_dashboard_data.py]] - degree 9, connects to 2 communities
- [[verify_native_dataset()]] - degree 5, connects to 2 communities
- [[.load_explanations()]] - degree 3, connects to 2 communities