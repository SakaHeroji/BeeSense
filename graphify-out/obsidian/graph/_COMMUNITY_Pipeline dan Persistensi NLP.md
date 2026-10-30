---
type: community
cohesion: 0.12
members: 36
---

# Pipeline dan Persistensi NLP

**Cohesion:** 0.12 - loosely connected
**Members:** 36 nodes

## Members
- [[._evaluate()]] - code - MachineLearning/social_nlp.py
- [[.select_candidate()]] - code - MachineLearning/social_nlp.py
- [[.setUpClass()_2]] - code - tests/nlp/test_social_nlp.py
- [[.setUpClass()_3]] - code - tests/nlp/test_streamlit_app.py
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
- [[.test_shipped_dashboard_and_explanations_need_no_training_environment()]] - code - tests/cloud/test_dashboard_runtime.py
- [[.test_sparse_dbscan_preserves_zero_distance_neighbors()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_reduction_preserves_groups_noise_and_uses_sentence_weights()]] - code - tests/nlp/test_social_nlp.py
- [[CloudRuntimeTests]] - code - tests/cloud/test_dashboard_runtime.py
- [[DashboardTests]] - code - tests/nlp/test_social_nlp.py
- [[Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count.]] - rationale - MachineLearning/social_nlp.py
- [[NLPTests]] - code - tests/nlp/test_social_nlp.py
- [[Run in an isolated Cloud environment, using only root requirements.txt.]] - rationale - tests/cloud/test_dashboard_runtime.py
- [[SocialNLPClusterer]] - code - MachineLearning/social_nlp.py
- [[encoder()]] - code - tests/nlp/test_social_nlp.py
- [[fixture()]] - code - tests/nlp/test_social_nlp.py
- [[social_nlp.py]] - code - MachineLearning/social_nlp.py
- [[test_dashboard_runtime.py]] - code - tests/cloud/test_dashboard_runtime.py
- [[test_social_nlp.py]] - code - tests/nlp/test_social_nlp.py
- [[test_streamlit_app.py]] - code - tests/nlp/test_streamlit_app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pipeline_dan_Persistensi_NLP
SORT file.name ASC
```

## Connections to other communities
- 29 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_1]]
- 12 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_2]]
- 9 edges to [[_COMMUNITY_Ringkasan Topik Gemini]]
- 7 edges to [[_COMMUNITY_Ringkasan Topik Gemini_1]]
- 5 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_4]]
- 4 edges to [[_COMMUNITY_Coherence dan Quality Gate]]
- 4 edges to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 4 edges to [[_COMMUNITY_Pengujian UI Streamlit]]
- 3 edges to [[_COMMUNITY_Snapshot NLP dan Arsip_1]]
- 2 edges to [[_COMMUNITY_Eksplorasi Dashboard Streamlit_2]]
- 2 edges to [[_COMMUNITY_Eksplorasi Dashboard Streamlit_1]]
- 2 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_3]]
- 2 edges to [[_COMMUNITY_Eksplorasi Dashboard Streamlit]]
- 2 edges to [[_COMMUNITY_Coherence dan Quality Gate_1]]
- 2 edges to [[_COMMUNITY_Coherence dan Quality Gate_2]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip_3]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip_5]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_9]]
- 1 edge to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_8]]
- 1 edge to [[_COMMUNITY_Ringkasan Topik Gemini_2]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip]]
- 1 edge to [[_COMMUNITY_Runbook dan Verifikasi Lokal]]
- 1 edge to [[_COMMUNITY_Eksplorasi Dashboard Streamlit_4]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip_2]]
- 1 edge to [[_COMMUNITY_Eksplorasi Dashboard Streamlit_5]]

## Top bridge nodes
- [[SocialNLPClusterer]] - degree 98, connects to 22 communities
- [[social_nlp.py]] - degree 12, connects to 6 communities
- [[NLPTests]] - degree 27, connects to 2 communities
- [[.select_candidate()]] - degree 5, connects to 2 communities
- [[.test_shipped_dashboard_and_explanations_need_no_training_environment()]] - degree 4, connects to 2 communities