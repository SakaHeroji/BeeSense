---
type: community
cohesion: 0.08
members: 51
---

# Model dan Pengujian NLP

**Cohesion:** 0.08 - loosely connected
**Members:** 51 nodes

## Members
- [[.__init__()_40]] - code - MachineLearning/social_nlp.py
- [[._clean()]] - code - MachineLearning/social_nlp.py
- [[._explanation_evidence()]] - code - MachineLearning/social_nlp.py
- [[._explanation_term_changes()]] - code - MachineLearning/social_nlp.py
- [[._explanation_trend()]] - code - MachineLearning/social_nlp.py
- [[._validate_config()]] - code - MachineLearning/social_nlp.py
- [[._validate_explanation_options()]] - code - MachineLearning/social_nlp.py
- [[.explain_artifacts()]] - code - MachineLearning/social_nlp.py
- [[.explain_topics()]] - code - MachineLearning/social_nlp.py
- [[.parent_post_key()]] - code - MachineLearning/social_nlp.py
- [[.select_candidate()]] - code - MachineLearning/social_nlp.py
- [[.sentence_spans()]] - code - MachineLearning/social_nlp.py
- [[.setUpClass()_2]] - code - tests/nlp/test_social_nlp.py
- [[.setUpClass()_1]] - code - tests/nlp/test_streamlit_app.py
- [[.stability()]] - code - MachineLearning/social_nlp.py
- [[.tearDownClass()_2]] - code - tests/nlp/test_social_nlp.py
- [[.test_bad_input_and_configuration_are_rejected()]] - code - tests/nlp/test_social_nlp.py
- [[.test_close_scores_prefer_separation_without_hardcoding_algorithm()]] - code - tests/nlp/test_social_nlp.py
- [[.test_coherence_gate_rejects_below_target_and_blocks_publication()]] - code - tests/nlp/test_social_nlp.py
- [[.test_coherence_search_evaluates_all_near_ties_and_skips_lower_scores()]] - code - tests/nlp/test_social_nlp.py
- [[.test_ctfidf_never_pads_short_topics_with_zero_weight_terms()]] - code - tests/nlp/test_social_nlp.py
- [[.test_cv_distinguishes_coherent_terms_and_rejects_missing_topics()]] - code - tests/nlp/test_social_nlp.py
- [[.test_dbscan_memory_guard_and_no_eligible_candidate_are_explicit()]] - code - tests/nlp/test_social_nlp.py
- [[.test_dedup_preserves_both_occurrences_and_original_dates()]] - code - tests/nlp/test_social_nlp.py
- [[.test_existing_artifact_directory_and_source_input_are_preserved()]] - code - tests/nlp/test_social_nlp.py
- [[.test_graph_links_are_scored_inferences_not_social_relationships()]] - code - tests/nlp/test_social_nlp.py
- [[.test_legacy_v1_artifact_and_explanations_remain_readable()]] - code - tests/nlp/test_social_nlp.py
- [[.test_long_segments_cover_text_without_silent_truncation()]] - code - tests/nlp/test_social_nlp.py
- [[.test_noise_is_not_counted_as_a_coherent_cluster_or_shared_stability()]] - code - tests/nlp/test_social_nlp.py
- [[.test_real_umap_projections_and_cache_are_validated()]] - code - tests/nlp/test_social_nlp.py
- [[.test_retraining_reduces_topics_and_persists_original_dbscan_ids()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_embeddings_require_matching_source_model_and_sentence_order()]] - code - tests/nlp/test_social_nlp.py
- [[.test_scores_are_in_original_embedding_geometry_and_coverage_penalized()]] - code - tests/nlp/test_social_nlp.py
- [[.test_span_offsets_and_abbreviations_are_source_faithful()]] - code - tests/nlp/test_social_nlp.py
- [[.test_sparse_dbscan_preserves_zero_distance_neighbors()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_graph_is_bounded_and_noise_is_not_a_topic()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_reduction_preserves_groups_noise_and_uses_sentence_weights()]] - code - tests/nlp/test_social_nlp.py
- [[.test_twitter_prepare_preserves_audited_roots_without_embedding_titles()]] - code - tests/nlp/test_social_nlp.py
- [[DashboardTests]] - code - tests/nlp/test_social_nlp.py
- [[Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count.]] - rationale - MachineLearning/social_nlp.py
- [[Evidence-grounded topic descriptions and descriptive, source-aware trends.]] - rationale - MachineLearning/social_nlp.py
- [[Explain already verified artifacts without encoding or fitting again.]] - rationale - MachineLearning/social_nlp.py
- [[Extract real sentences using relevance plus MMR diversity.]] - rationale - MachineLearning/social_nlp.py
- [[Identify the parent thread, not the individual comment URL.]] - rationale - MachineLearning/social_nlp.py
- [[NLPTests]] - code - tests/nlp/test_social_nlp.py
- [[Rule-based segmentation preserving exact offsets in the original text.]] - rationale - MachineLearning/social_nlp.py
- [[SocialNLPClusterer_2]] - code - MachineLearning/social_nlp.py
- [[encoder()]] - code - tests/nlp/test_social_nlp.py
- [[fixture()]] - code - tests/nlp/test_social_nlp.py
- [[test_social_nlp.py]] - code - tests/nlp/test_social_nlp.py
- [[test_streamlit_app.py]] - code - tests/nlp/test_streamlit_app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Model_dan_Pengujian_NLP
SORT file.name ASC
```

## Connections to other communities
- 29 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 23 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 10 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik]]
- 6 edges to [[_COMMUNITY_Penggabungan Dataset]]
- 4 edges to [[_COMMUNITY_Pengujian UI Streamlit]]
- 4 edges to [[_COMMUNITY_thread_url]]
- 3 edges to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 3 edges to [[_COMMUNITY_Model dan Pengujian NLP_1]]
- 3 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_2]]
- 2 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 2 edges to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 2 edges to [[_COMMUNITY_Batas Akuisisi Reddit_3]]
- 2 edges to [[_COMMUNITY_app.py]]
- 2 edges to [[_COMMUNITY_Pengujian Narasi Gemini_1]]
- 1 edge to [[_COMMUNITY_Pengambilan HTML Reddit]]
- 1 edge to [[_COMMUNITY_app.py_1]]
- 1 edge to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_7]]

## Top bridge nodes
- [[SocialNLPClusterer_2]] - degree 106, connects to 15 communities
- [[test_social_nlp.py]] - degree 10, connects to 3 communities
- [[.parent_post_key()]] - degree 6, connects to 3 communities
- [[.explain_artifacts()]] - degree 6, connects to 2 communities
- [[test_streamlit_app.py]] - degree 6, connects to 2 communities