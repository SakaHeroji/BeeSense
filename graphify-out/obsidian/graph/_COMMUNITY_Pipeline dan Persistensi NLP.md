---
type: community
cohesion: 0.07
members: 23
---

# Pipeline dan Persistensi NLP

**Cohesion:** 0.07 - loosely connected
**Members:** 23 nodes

## Members
- [[.setUpClass()_1]] - code - tests/nlp/test_social_nlp.py
- [[.setUpClass()_2]] - code - tests/nlp/test_streamlit_app.py
- [[.tearDownClass()_1]] - code - tests/nlp/test_social_nlp.py
- [[.test_artifacts_roundtrip_without_pickle_and_verify_checksums()]] - code - tests/nlp/test_social_nlp.py
- [[.test_bad_input_and_configuration_are_rejected()]] - code - tests/nlp/test_social_nlp.py
- [[.test_close_scores_prefer_separation_without_hardcoding_algorithm()]] - code - tests/nlp/test_social_nlp.py
- [[.test_dedup_preserves_both_occurrences_and_original_dates()]] - code - tests/nlp/test_social_nlp.py
- [[.test_existing_artifact_directory_and_source_input_are_preserved()]] - code - tests/nlp/test_social_nlp.py
- [[.test_graph_links_are_scored_inferences_not_social_relationships()]] - code - tests/nlp/test_social_nlp.py
- [[.test_long_segments_cover_text_without_silent_truncation()]] - code - tests/nlp/test_social_nlp.py
- [[.test_noise_is_not_counted_as_a_coherent_cluster_or_shared_stability()]] - code - tests/nlp/test_social_nlp.py
- [[.test_scores_are_in_original_embedding_geometry_and_coverage_penalized()]] - code - tests/nlp/test_social_nlp.py
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[.test_span_offsets_and_abbreviations_are_source_faithful()]] - code - tests/nlp/test_social_nlp.py
- [[DashboardTests]] - code - tests/nlp/test_social_nlp.py
- [[NLPTests]] - code - tests/nlp/test_social_nlp.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[encoder()]] - code - tests/nlp/test_social_nlp.py
- [[fixture()]] - code - tests/nlp/test_social_nlp.py
- [[main()_8]] - code - scripts/verify_dashboard_data.py
- [[test_social_nlp.py]] - code - tests/nlp/test_social_nlp.py
- [[test_streamlit_app.py]] - code - tests/nlp/test_streamlit_app.py
- [[verify()_1]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pipeline_dan_Persistensi_NLP
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Ekspor Campaign dan Resume]]
- 2 edges to [[_COMMUNITY_Monitor Akuisisi Sintetis_1]]

## Top bridge nodes
- [[test_streamlit_app.py]] - degree 6, connects to 1 community
- [[DashboardTests]] - degree 4, connects to 1 community
- [[.setUpClass()_2]] - degree 4, connects to 1 community