---
type: community
cohesion: 0.10
members: 27
---

# Model dan Pengujian NLP

**Cohesion:** 0.10 - loosely connected
**Members:** 27 nodes

## Members
- [[.select_candidate()]] - code - MachineLearning/social_nlp.py
- [[.setUpClass()_2]] - code - tests/nlp/test_social_nlp.py
- [[.setUpClass()_1]] - code - tests/nlp/test_streamlit_app.py
- [[.tearDownClass()_2]] - code - tests/nlp/test_social_nlp.py
- [[.test_bad_input_and_configuration_are_rejected()]] - code - tests/nlp/test_social_nlp.py
- [[.test_close_scores_prefer_separation_without_hardcoding_algorithm()]] - code - tests/nlp/test_social_nlp.py
- [[.test_coherence_gate_rejects_below_target_and_blocks_publication()]] - code - tests/nlp/test_social_nlp.py
- [[.test_coherence_search_evaluates_all_near_ties_and_skips_lower_scores()]] - code - tests/nlp/test_social_nlp.py
- [[.test_ctfidf_never_pads_short_topics_with_zero_weight_terms()]] - code - tests/nlp/test_social_nlp.py
- [[.test_cv_distinguishes_coherent_terms_and_rejects_missing_topics()]] - code - tests/nlp/test_social_nlp.py
- [[.test_dbscan_memory_guard_and_no_eligible_candidate_are_explicit()]] - code - tests/nlp/test_social_nlp.py
- [[.test_dedup_preserves_both_occurrences_and_original_dates()]] - code - tests/nlp/test_social_nlp.py
- [[.test_excel_extension_loads_without_gemini_and_binds_membership_and_bytes()]] - code - tests/nlp/test_social_nlp.py
- [[.test_existing_artifact_directory_and_source_input_are_preserved()]] - code - tests/nlp/test_social_nlp.py
- [[.test_graph_links_are_scored_inferences_not_social_relationships()]] - code - tests/nlp/test_social_nlp.py
- [[.test_real_umap_projections_and_cache_are_validated()]] - code - tests/nlp/test_social_nlp.py
- [[.test_retraining_reduces_topics_and_persists_original_dbscan_ids()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_embeddings_require_matching_source_model_and_sentence_order()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_run_coherence_reproduces_the_published_score()]] - code - tests/nlp/test_social_nlp.py
- [[.test_scores_are_in_original_embedding_geometry_and_coverage_penalized()]] - code - tests/nlp/test_social_nlp.py
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[.test_sparse_dbscan_preserves_zero_distance_neighbors()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_reduction_preserves_groups_noise_and_uses_sentence_weights()]] - code - tests/nlp/test_social_nlp.py
- [[.test_twitter_prepare_preserves_audited_roots_without_embedding_titles()]] - code - tests/nlp/test_social_nlp.py
- [[NLPTests]] - code - tests/nlp/test_social_nlp.py
- [[encoder()]] - code - tests/nlp/test_social_nlp.py
- [[fixture()]] - code - tests/nlp/test_social_nlp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Model_dan_Pengujian_NLP
SORT file.name ASC
```

## Connections to other communities
- 22 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 6 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 5 edges to [[_COMMUNITY_Model dan Pengujian NLP_1]]
- 2 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 1 edge to [[_COMMUNITY_Pengujian UI Streamlit]]
- 1 edge to [[_COMMUNITY_Arsip Data Harian]]

## Top bridge nodes
- [[NLPTests]] - degree 29, connects to 4 communities
- [[.test_existing_artifact_directory_and_source_input_are_preserved()]] - degree 5, connects to 2 communities
- [[.test_twitter_prepare_preserves_audited_roots_without_embedding_titles()]] - degree 4, connects to 2 communities
- [[.setUpClass()_1]] - degree 4, connects to 2 communities
- [[.test_saved_run_coherence_reproduces_the_published_score()]] - degree 3, connects to 2 communities