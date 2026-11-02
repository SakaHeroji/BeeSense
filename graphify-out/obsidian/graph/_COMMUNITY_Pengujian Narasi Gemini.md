---
type: community
cohesion: 0.09
members: 38
---

# Pengujian Narasi Gemini

**Cohesion:** 0.09 - loosely connected
**Members:** 38 nodes

## Members
- [[.load_explanations()]] - code - MachineLearning/social_nlp.py
- [[.load_run()]] - code - MachineLearning/social_nlp.py
- [[.narrative_source()]] - code - tests/nlp/test_topic_narratives.py
- [[.setUpClass()_3]] - code - tests/nlp/test_topic_narratives.py
- [[.tearDownClass()_3]] - code - tests/nlp/test_topic_narratives.py
- [[.test_artifacts_roundtrip_without_pickle_and_verify_checksums()]] - code - tests/nlp/test_social_nlp.py
- [[.test_csv_manifest_and_roundtrip_bind_every_topic_and_keyword_weight()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_dashboard_displays_generated_sentence_without_network_or_training()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_excel_extension_loads_without_gemini_and_binds_membership_and_bytes()]] - code - tests/nlp/test_social_nlp.py
- [[.test_narrative_snapshot_gate_and_source_changes_fail_before_publication()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_narrative_snapshot_preserves_fitted_files_and_original_bundle()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_saved_run_coherence_reproduces_the_published_score()]] - code - tests/nlp/test_social_nlp.py
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[A visibly synthetic fixture exercising the saved-bundle path.]] - rationale - tests/nlp/test_topic_narratives.py
- [[Add Gemini descriptions to a verified fitted run, preserving its clustering.]] - rationale - scripts/generate_topic_narratives.py
- [[Bind a separately published relevance dataset to the active fitted mask.]] - rationale - scripts/verify_dashboard_data.py
- [[GeminiArtifactTests]] - code - tests/nlp/test_topic_narratives.py
- [[Publish a new atomic bundle; never overwrite or refit the source run.]] - rationale - scripts/generate_topic_narratives.py
- [[Start the local relevance experiment, or its preserved baseline snapshot.]] - rationale - scripts/relevance_dashboard.py
- [[Validate separately published X evidence without treating it as an NLP run.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[enrich_run()]] - code - scripts/generate_topic_narratives.py
- [[file_hash()]] - code - MachineLearning/social_nlp.py
- [[generate_topic_narratives.py]] - code - scripts/generate_topic_narratives.py
- [[main()_14]] - code - scripts/generate_topic_narratives.py
- [[main()_15]] - code - scripts/relevance_dashboard.py
- [[main()_16]] - code - scripts/verify_dashboard_data.py
- [[published_crawl_files()]] - code - scripts/verify_dashboard_data.py
- [[published_relevance_files()]] - code - scripts/verify_dashboard_data.py
- [[published_source_files()]] - code - scripts/verify_dashboard_data.py
- [[relevance_dashboard.py]] - code - scripts/relevance_dashboard.py
- [[social_nlp.py]] - code - MachineLearning/social_nlp.py
- [[test_topic_narratives.py]] - code - tests/nlp/test_topic_narratives.py
- [[verify()_1]] - code - scripts/verify_dashboard_data.py
- [[verify_dashboard_data.py]] - code - scripts/verify_dashboard_data.py
- [[verify_native_dataset()]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Narasi_Gemini
SORT file.name ASC
```

## Connections to other communities
- 23 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 10 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 10 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 6 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik]]
- 4 edges to [[_COMMUNITY_Pengujian Narasi Gemini_1]]
- 3 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 3 edges to [[_COMMUNITY_app.py]]
- 2 edges to [[_COMMUNITY_Model dan Pengujian NLP_1]]
- 2 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_2]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Pengujian UI Streamlit]]
- 1 edge to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 1 edge to [[_COMMUNITY_Koordinator Backend Sosial]]
- 1 edge to [[_COMMUNITY_Penggabungan Dataset]]
- 1 edge to [[_COMMUNITY_app.py_1]]
- 1 edge to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 1 edge to [[_COMMUNITY_Operasi dan Verifikasi BeeSense]]

## Top bridge nodes
- [[social_nlp.py]] - degree 20, connects to 10 communities
- [[file_hash()]] - degree 34, connects to 8 communities
- [[.load_run()]] - degree 21, connects to 8 communities
- [[generate_topic_narratives.py]] - degree 10, connects to 4 communities
- [[verify_dashboard_data.py]] - degree 12, connects to 3 communities