---
type: community
members: 42
---

# Model dan Pengujian NLP

**Members:** 42 nodes

## Members
- [[.select_candidate()]] - code - MachineLearning/social_nlp.py
- [[.sentence_spans()]] - code - MachineLearning/social_nlp.py
- [[.setUpClass()_1]] - code - tests/nlp/test_social_nlp.py
- [[.setUpClass()_2]] - code - tests/nlp/test_streamlit_app.py
- [[.stability()]] - code - MachineLearning/social_nlp.py
- [[.tearDownClass()_1]] - code - tests/nlp/test_social_nlp.py
- [[.test_bad_input_and_configuration_are_rejected()]] - code - tests/nlp/test_social_nlp.py
- [[.test_browser_bundle_keeps_backend_provenance_and_fixture_is_not_live()]] - code - tests/crawler/test_instagram_browser.py
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
- [[.test_shipped_dashboard_and_explanations_need_no_training_environment()]] - code - tests/cloud/test_dashboard_runtime.py
- [[.test_span_offsets_and_abbreviations_are_source_faithful()]] - code - tests/nlp/test_social_nlp.py
- [[.test_sparse_dbscan_preserves_zero_distance_neighbors()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_reduction_preserves_groups_noise_and_uses_sentence_weights()]] - code - tests/nlp/test_social_nlp.py
- [[BeeSense application package._5]] - rationale - MachineLearning/__init__.py
- [[CloudRuntimeTests]] - code - tests/cloud/test_dashboard_runtime.py
- [[Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count.]] - rationale - MachineLearning/social_nlp.py
- [[MachineLearning__init__.py]] - code - MachineLearning/__init__.py
- [[NLPTests]] - code - tests/nlp/test_social_nlp.py
- [[Rule-based segmentation preserving exact offsets in the original text.]] - rationale - MachineLearning/social_nlp.py
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
TABLE source_file, type FROM #community/Model_dan_Pengujian_NLP
SORT file.name ASC
```

## Connections to other communities
- 29 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 14 edges to [[_COMMUNITY_Verifikasi Artefak Dataset]]
- 7 edges to [[_COMMUNITY_Generator Narasi Gemini]]
- 7 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 7 edges to [[_COMMUNITY_Pemilihan Topik dan Coherence]]
- 6 edges to [[_COMMUNITY_Bukti Ekstraktif Topik]]
- 4 edges to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 4 edges to [[_COMMUNITY_Pengujian UI Streamlit]]
- 3 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 3 edges to [[_COMMUNITY_Struktur Runtime Dashboard]]
- 2 edges to [[_COMMUNITY_Pengambilan HTML Reddit]]
- 2 edges to [[_COMMUNITY_app.py]]
- 2 edges to [[_COMMUNITY_Penjelasan Topik Dashboard]]
- 2 edges to [[_COMMUNITY_Konfigurasi Model Aktif]]
- 2 edges to [[_COMMUNITY_Riwayat Evaluasi Coherence]]
- 2 edges to [[_COMMUNITY_.topic_figure]]
- 1 edge to [[_COMMUNITY_thread_url]]
- 1 edge to [[_COMMUNITY_Audit Akuisisi Instagram]]
- 1 edge to [[_COMMUNITY_Konteks dan Provenance Gemini]]
- 1 edge to [[_COMMUNITY_Arsitektur Model dan Dashboard]]
- 1 edge to [[_COMMUNITY_Riwayat Dataset dan Metodologi]]

## Top bridge nodes
- [[SocialNLPClusterer]] - degree 98, connects to 20 communities
- [[social_nlp.py]] - degree 14, connects to 7 communities
- [[test_social_nlp.py]] - degree 8, connects to 2 communities
- [[.select_candidate()]] - degree 5, connects to 2 communities
- [[.test_legacy_v1_artifact_and_explanations_remain_readable()]] - degree 5, connects to 2 communities