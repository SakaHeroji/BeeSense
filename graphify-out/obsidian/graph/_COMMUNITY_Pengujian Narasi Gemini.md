---
type: community
cohesion: 0.13
members: 29
---

# Pengujian Narasi Gemini

**Cohesion:** 0.13 - loosely connected
**Members:** 29 nodes

## Members
- [[.load_explanations()]] - code - MachineLearning/social_nlp.py
- [[.load_run()]] - code - MachineLearning/social_nlp.py
- [[.narrative_source()]] - code - tests/nlp/test_topic_narratives.py
- [[.tearDownClass()_3]] - code - tests/nlp/test_topic_narratives.py
- [[.test_artifacts_roundtrip_without_pickle_and_verify_checksums()]] - code - tests/nlp/test_social_nlp.py
- [[.test_csv_manifest_and_roundtrip_bind_every_topic_and_keyword_weight()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_dashboard_displays_generated_sentence_without_network_or_training()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_legacy_v1_artifact_and_explanations_remain_readable()]] - code - tests/nlp/test_social_nlp.py
- [[.test_narrative_snapshot_gate_and_source_changes_fail_before_publication()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_narrative_snapshot_preserves_fitted_files_and_original_bundle()]] - code - tests/nlp/test_topic_narratives.py
- [[A merge report binds its small, explicit audit sidecars to the input.]] - rationale - scripts/verify_dashboard_data.py
- [[A visibly synthetic fixture exercising the saved-bundle path.]] - rationale - tests/nlp/test_topic_narratives.py
- [[Add Gemini descriptions to a verified fitted run, preserving its clustering.]] - rationale - scripts/generate_topic_narratives.py
- [[GeminiArtifactTests]] - code - tests/nlp/test_topic_narratives.py
- [[Publish a new atomic bundle; never overwrite or refit the source run.]] - rationale - scripts/generate_topic_narratives.py
- [[Validate separately published X evidence without treating it as an NLP run.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[Verify record identity independently of sentence-text deduplication.]] - rationale - scripts/verify_dashboard_data.py
- [[enrich_run()]] - code - scripts/generate_topic_narratives.py
- [[file_hash()]] - code - MachineLearning/social_nlp.py
- [[generate_topic_narratives.py]] - code - scripts/generate_topic_narratives.py
- [[main()_3]] - code - scripts/generate_topic_narratives.py
- [[main()_4]] - code - scripts/verify_dashboard_data.py
- [[published_crawl_files()]] - code - scripts/verify_dashboard_data.py
- [[published_source_files()]] - code - scripts/verify_dashboard_data.py
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
- 19 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 7 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 7 edges to [[_COMMUNITY_Model dan Pengujian NLP_1]]
- 6 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 4 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 4 edges to [[_COMMUNITY_Pengujian Narasi Gemini_1]]
- 2 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 2 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Pengujian UI Streamlit]]

## Top bridge nodes
- [[file_hash()]] - degree 30, connects to 6 communities
- [[.load_run()]] - degree 19, connects to 6 communities
- [[test_topic_narratives.py]] - degree 10, connects to 4 communities
- [[generate_topic_narratives.py]] - degree 9, connects to 4 communities
- [[verify_dashboard_data.py]] - degree 11, connects to 3 communities