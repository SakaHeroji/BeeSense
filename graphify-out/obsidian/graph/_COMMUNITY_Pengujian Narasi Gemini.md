---
type: community
cohesion: 0.11
members: 32
---

# Pengujian Narasi Gemini

**Cohesion:** 0.11 - loosely connected
**Members:** 32 nodes

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
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[A visibly synthetic fixture exercising the saved-bundle path.]] - rationale - tests/nlp/test_topic_narratives.py
- [[Add Gemini descriptions to a verified fitted run, preserving its clustering.]] - rationale - scripts/generate_topic_narratives.py
- [[Bind a separately published relevance dataset to the active fitted mask.]] - rationale - scripts/verify_dashboard_data.py
- [[GeminiArtifactTests]] - code - tests/nlp/test_topic_narratives.py
- [[Publish a new atomic bundle; never overwrite or refit the source run.]] - rationale - scripts/generate_topic_narratives.py
- [[Validate separately published X evidence without treating it as an NLP run.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[enrich_run()]] - code - scripts/generate_topic_narratives.py
- [[file_hash()]] - code - MachineLearning/social_nlp.py
- [[generate_topic_narratives.py]] - code - scripts/generate_topic_narratives.py
- [[main()_13]] - code - scripts/generate_topic_narratives.py
- [[main()_15]] - code - scripts/verify_dashboard_data.py
- [[published_crawl_files()]] - code - scripts/verify_dashboard_data.py
- [[published_relevance_files()]] - code - scripts/verify_dashboard_data.py
- [[published_source_files()]] - code - scripts/verify_dashboard_data.py
- [[verify()_1]] - code - scripts/verify_dashboard_data.py
- [[verify_dashboard_data.py]] - code - scripts/verify_dashboard_data.py
- [[verify_native_dataset()]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Narasi_Gemini
SORT file.name ASC
```

## Connections to other communities
- 17 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 12 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 9 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 5 edges to [[_COMMUNITY_Pengujian Narasi Gemini_1]]
- 2 edges to [[_COMMUNITY_Akuisisi YouTube]]
- 2 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 2 edges to [[_COMMUNITY_Model dan Pengujian NLP_1]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit_1]]
- 1 edge to [[_COMMUNITY_Pengujian UI Streamlit]]
- 1 edge to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_1]]
- 1 edge to [[_COMMUNITY_Panduan Pipeline BeeSense]]

## Top bridge nodes
- [[file_hash()]] - degree 32, connects to 8 communities
- [[.load_run()]] - degree 19, connects to 5 communities
- [[verify_dashboard_data.py]] - degree 12, connects to 4 communities
- [[generate_topic_narratives.py]] - degree 9, connects to 4 communities
- [[enrich_run()]] - degree 9, connects to 2 communities