---
type: community
cohesion: 0.10
members: 27
---

# Encoding dan Penyimpanan Model

**Cohesion:** 0.10 - loosely connected
**Members:** 27 nodes

## Members
- [[._date_label()]] - code - Dashboard/app.py
- [[.setUpClass()_1]] - code - tests/nlp/test_social_nlp.py
- [[.tearDownClass()_1]] - code - tests/nlp/test_social_nlp.py
- [[.test_bad_input_and_configuration_are_rejected()]] - code - tests/nlp/test_social_nlp.py
- [[.test_coherence_gate_rejects_below_target_and_blocks_publication()]] - code - tests/nlp/test_social_nlp.py
- [[.test_coherence_search_evaluates_all_near_ties_and_skips_lower_scores()]] - code - tests/nlp/test_social_nlp.py
- [[.test_ctfidf_never_pads_short_topics_with_zero_weight_terms()]] - code - tests/nlp/test_social_nlp.py
- [[.test_cv_distinguishes_coherent_terms_and_rejects_missing_topics()]] - code - tests/nlp/test_social_nlp.py
- [[.test_dedup_preserves_both_occurrences_and_original_dates()]] - code - tests/nlp/test_social_nlp.py
- [[.test_existing_artifact_directory_and_source_input_are_preserved()]] - code - tests/nlp/test_social_nlp.py
- [[.test_filters_are_literal_and_respect_platform_dates()]] - code - tests/nlp/test_social_nlp.py
- [[.test_graph_links_are_scored_inferences_not_social_relationships()]] - code - tests/nlp/test_social_nlp.py
- [[.test_real_umap_projections_and_cache_are_validated()]] - code - tests/nlp/test_social_nlp.py
- [[.test_retraining_reduces_topics_and_persists_original_dbscan_ids()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_embeddings_require_matching_source_model_and_sentence_order()]] - code - tests/nlp/test_social_nlp.py
- [[.test_scores_are_in_original_embedding_geometry_and_coverage_penalized()]] - code - tests/nlp/test_social_nlp.py
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[.test_sparse_dbscan_preserves_zero_distance_neighbors()]] - code - tests/nlp/test_social_nlp.py
- [[.test_tiktok_prepare_preserves_native_roots_and_original_comment_text()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_graph_is_bounded_and_noise_is_not_a_topic()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_reduction_preserves_groups_noise_and_uses_sentence_weights()]] - code - tests/nlp/test_social_nlp.py
- [[.test_twitter_prepare_preserves_audited_roots_without_embedding_titles()]] - code - tests/nlp/test_social_nlp.py
- [[DashboardTests]] - code - tests/nlp/test_social_nlp.py
- [[NLPTests]] - code - tests/nlp/test_social_nlp.py
- [[encoder()]] - code - tests/nlp/test_social_nlp.py
- [[fixture()_1]] - code - tests/nlp/test_social_nlp.py
- [[test_social_nlp.py]] - code - tests/nlp/test_social_nlp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Encoding_dan_Penyimpanan_Model
SORT file.name ASC
```

## Connections to other communities
- 19 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 7 edges to [[_COMMUNITY_Narasi Gemini dan Pembandingan_1]]
- 3 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_2]]
- 2 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_4]]
- 2 edges to [[_COMMUNITY_thread_url]]
- 1 edge to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]
- 1 edge to [[_COMMUNITY_Encoding dan Penyimpanan Model_3]]
- 1 edge to [[_COMMUNITY_app.py_1]]

## Top bridge nodes
- [[NLPTests]] - degree 30, connects to 4 communities
- [[test_social_nlp.py]] - degree 7, connects to 3 communities
- [[.test_existing_artifact_directory_and_source_input_are_preserved()]] - degree 5, connects to 2 communities
- [[encoder()]] - degree 8, connects to 1 community
- [[DashboardTests]] - degree 4, connects to 1 community