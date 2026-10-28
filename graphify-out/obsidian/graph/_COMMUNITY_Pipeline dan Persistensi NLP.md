---
type: community
cohesion: 0.06
members: 84
---

# Pipeline dan Persistensi NLP

**Cohesion:** 0.06 - loosely connected
**Members:** 84 nodes

## Members
- [[.__init__()_24]] - code - social_nlp.py
- [[._cache_dir()]] - code - social_nlp.py
- [[._clean()]] - code - social_nlp.py
- [[._ctfidf_terms()]] - code - social_nlp.py
- [[._encode_sbert()]] - code - social_nlp.py
- [[._evaluate()]] - code - social_nlp.py
- [[._event()]] - code - social_nlp.py
- [[._explanation_evidence()]] - code - social_nlp.py
- [[._explanation_term_changes()]] - code - social_nlp.py
- [[._explanation_trend()]] - code - social_nlp.py
- [[._filter_radius()]] - code - social_nlp.py
- [[._radius_graph()]] - code - social_nlp.py
- [[._reduce_embeddings()]] - code - social_nlp.py
- [[._topic_vectorizer()]] - code - social_nlp.py
- [[._validate_config()]] - code - social_nlp.py
- [[._validate_explanation_options()]] - code - social_nlp.py
- [[.build_topic_graph()]] - code - social_nlp.py
- [[.compare()]] - code - social_nlp.py
- [[.describe_topics()]] - code - social_nlp.py
- [[.encode()]] - code - social_nlp.py
- [[.evaluate_run_coherence()]] - code - social_nlp.py
- [[.explain_artifacts()]] - code - social_nlp.py
- [[.explain_topics()]] - code - social_nlp.py
- [[.fit_excel()]] - code - social_nlp.py
- [[.load_explanations()]] - code - social_nlp.py
- [[.load_run()]] - code - social_nlp.py
- [[.parent_post_key()]] - code - social_nlp.py
- [[.prepare_excel()]] - code - social_nlp.py
- [[.save()]] - code - social_nlp.py
- [[.save_explanations()]] - code - social_nlp.py
- [[.score_coherence()]] - code - social_nlp.py
- [[.select_candidate()]] - code - social_nlp.py
- [[.sentence_spans()]] - code - social_nlp.py
- [[.setUpClass()_1]] - code - tests/nlp/test_social_nlp.py
- [[.setUpClass()_2]] - code - tests/nlp/test_streamlit_app.py
- [[.stability()]] - code - social_nlp.py
- [[.tearDownClass()_1]] - code - tests/nlp/test_social_nlp.py
- [[.test_artifacts_roundtrip_without_pickle_and_verify_checksums()]] - code - tests/nlp/test_social_nlp.py
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
- [[.test_saved_run_coherence_reproduces_the_published_score()]] - code - tests/nlp/test_social_nlp.py
- [[.test_scores_are_in_original_embedding_geometry_and_coverage_penalized()]] - code - tests/nlp/test_social_nlp.py
- [[.test_selected_candidate_has_semantic_separation_and_full_provenance()]] - code - tests/nlp/test_social_nlp.py
- [[.test_span_offsets_and_abbreviations_are_source_faithful()]] - code - tests/nlp/test_social_nlp.py
- [[.test_sparse_dbscan_preserves_zero_distance_neighbors()]] - code - tests/nlp/test_social_nlp.py
- [[DashboardTests]] - code - tests/nlp/test_social_nlp.py
- [[Encode multilingual sentences with SBERT and fit UMAP + DBSCAN.      Encoder inj]] - rationale - social_nlp.py
- [[Evidence-grounded topic descriptions and descriptive, source-aware trends.]] - rationale - social_nlp.py
- [[Explain already verified artifacts without encoding or fitting again.]] - rationale - social_nlp.py
- [[Extract real sentences using relevance plus MMR diversity.]] - rationale - social_nlp.py
- [[Identify the parent thread, not the individual comment URL.]] - rationale - social_nlp.py
- [[Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un]] - rationale - social_nlp.py
- [[NLPTests]] - code - tests/nlp/test_social_nlp.py
- [[Preserve explicit zero distances, including identical sentence vectors.]] - rationale - social_nlp.py
- [[Publish a new versioned sidecar; never modify the original run.]] - rationale - social_nlp.py
- [[Rule-based segmentation preserving exact offsets in the original text.]] - rationale - social_nlp.py
- [[Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.]] - rationale - social_nlp.py
- [[SocialNLPClusterer]] - code - social_nlp.py
- [[Use the same class TF-IDF vocabulary for selection and publication.]] - rationale - social_nlp.py
- [[Verify published source workbooks and the dashboard artifact bundle.]] - rationale - scripts/verify_dashboard_data.py
- [[_explain_filtered()]] - code - nlp_dashboard.py
- [[encoder()]] - code - tests/nlp/test_social_nlp.py
- [[file_hash()]] - code - social_nlp.py
- [[fixture()]] - code - tests/nlp/test_social_nlp.py
- [[json_write()]] - code - social_nlp.py
- [[main()_2]] - code - scripts/verify_dashboard_data.py
- [[main()_6]] - code - social_nlp.py
- [[social_nlp.py]] - code - social_nlp.py
- [[test_social_nlp.py]] - code - tests/nlp/test_social_nlp.py
- [[test_streamlit_app.py]] - code - tests/nlp/test_streamlit_app.py
- [[verify()_1]] - code - scripts/verify_dashboard_data.py
- [[verify_dashboard_data.py]] - code - scripts/verify_dashboard_data.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pipeline_dan_Persistensi_NLP
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_Eksplorasi Dashboard Streamlit]]
- 4 edges to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 4 edges to [[_COMMUNITY_Pengujian UI Streamlit]]
- 3 edges to [[_COMMUNITY_Coherence dan Quality Gate]]
- 2 edges to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu]]
- 2 edges to [[_COMMUNITY_Dashboard dan Tren Deskriptif]]
- 1 edge to [[_COMMUNITY_Bundle Excel dan Provenans]]
- 1 edge to [[_COMMUNITY_Adapter Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_Runbook dan Verifikasi Lokal]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip]]
- 1 edge to [[_COMMUNITY_Encoder SBERT dan Cache]]

## Top bridge nodes
- [[SocialNLPClusterer]] - degree 71, connects to 8 communities
- [[file_hash()]] - degree 23, connects to 4 communities
- [[social_nlp.py]] - degree 9, connects to 2 communities
- [[NLPTests]] - degree 25, connects to 1 community
- [[test_social_nlp.py]] - degree 9, connects to 1 community