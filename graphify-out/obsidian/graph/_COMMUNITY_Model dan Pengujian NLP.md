---
type: community
cohesion: 0.13
members: 33
---

# Model dan Pengujian NLP

**Cohesion:** 0.13 - loosely connected
**Members:** 33 nodes

## Members
- [[.__init__()_39]] - code - MachineLearning/social_nlp.py
- [[._validate_config()]] - code - MachineLearning/social_nlp.py
- [[._validate_explanation_options()]] - code - MachineLearning/social_nlp.py
- [[.select_candidate()]] - code - MachineLearning/social_nlp.py
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
- [[.test_noise_is_not_counted_as_a_coherent_cluster_or_shared_stability()]] - code - tests/nlp/test_social_nlp.py
- [[.test_real_umap_projections_and_cache_are_validated()]] - code - tests/nlp/test_social_nlp.py
- [[.test_retraining_reduces_topics_and_persists_original_dbscan_ids()]] - code - tests/nlp/test_social_nlp.py
- [[.test_saved_embeddings_require_matching_source_model_and_sentence_order()]] - code - tests/nlp/test_social_nlp.py
- [[.test_scores_are_in_original_embedding_geometry_and_coverage_penalized()]] - code - tests/nlp/test_social_nlp.py
- [[.test_sparse_dbscan_preserves_zero_distance_neighbors()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_reduction_preserves_groups_noise_and_uses_sentence_weights()]] - code - tests/nlp/test_social_nlp.py
- [[.test_twitter_prepare_preserves_audited_roots_without_embedding_titles()]] - code - tests/nlp/test_social_nlp.py
- [[Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count.]] - rationale - MachineLearning/social_nlp.py
- [[NLPTests]] - code - tests/nlp/test_social_nlp.py
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
- 21 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 17 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 10 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 10 edges to [[_COMMUNITY_Model dan Pengujian NLP_1]]
- 5 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 5 edges to [[_COMMUNITY_Penggabungan Dataset]]
- 5 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 4 edges to [[_COMMUNITY_Pengujian UI Streamlit]]
- 3 edges to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 3 edges to [[_COMMUNITY_Model dan Pengujian NLP_2]]
- 3 edges to [[_COMMUNITY_Pengujian Narasi Gemini_1]]
- 2 edges to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 2 edges to [[_COMMUNITY_Alur Dataset Model Dashboard_1]]
- 2 edges to [[_COMMUNITY_thread_url_1]]
- 1 edge to [[_COMMUNITY_Pengambilan HTML Reddit]]
- 1 edge to [[_COMMUNITY_thread_url]]
- 1 edge to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_7]]
- 1 edge to [[_COMMUNITY_Pengujian Narasi Gemini_2]]

## Top bridge nodes
- [[SocialNLPClusterer_2]] - degree 101, connects to 17 communities
- [[test_social_nlp.py]] - degree 10, connects to 5 communities
- [[NLPTests]] - degree 29, connects to 2 communities
- [[test_streamlit_app.py]] - degree 6, connects to 2 communities
- [[fixture()]] - degree 7, connects to 1 community