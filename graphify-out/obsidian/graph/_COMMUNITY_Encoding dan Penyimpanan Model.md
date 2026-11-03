---
type: community
cohesion: 0.09
members: 49
---

# Encoding dan Penyimpanan Model

**Cohesion:** 0.09 - loosely connected
**Members:** 49 nodes

## Members
- [[.__init__()_10]] - code - MachineLearning/social_nlp.py
- [[._apply_context_relevance()]] - code - MachineLearning/social_nlp.py
- [[._cache_dir()]] - code - MachineLearning/social_nlp.py
- [[._ctfidf_terms()]] - code - MachineLearning/social_nlp.py
- [[._encode_sbert()]] - code - MachineLearning/social_nlp.py
- [[._evaluate()]] - code - MachineLearning/social_nlp.py
- [[._event()]] - code - MachineLearning/social_nlp.py
- [[._filter_radius()]] - code - MachineLearning/social_nlp.py
- [[._merge_topics()]] - code - MachineLearning/social_nlp.py
- [[._radius_graph()]] - code - MachineLearning/social_nlp.py
- [[._reduce_embeddings()]] - code - MachineLearning/social_nlp.py
- [[._reuse_embeddings()]] - code - MachineLearning/social_nlp.py
- [[._topic_vectorizer()]] - code - MachineLearning/social_nlp.py
- [[._validate_config()]] - code - MachineLearning/social_nlp.py
- [[._validate_explanation_options()]] - code - MachineLearning/social_nlp.py
- [[.build_topic_graph()]] - code - MachineLearning/social_nlp.py
- [[.compare()]] - code - MachineLearning/social_nlp.py
- [[.describe_topics()]] - code - MachineLearning/social_nlp.py
- [[.encode()_1]] - code - MachineLearning/social_nlp.py
- [[.evaluate_run_coherence()]] - code - MachineLearning/social_nlp.py
- [[.fit_excel()]] - code - MachineLearning/social_nlp.py
- [[.generate_topic_narratives()]] - code - MachineLearning/social_nlp.py
- [[.prepare_excel()]] - code - MachineLearning/social_nlp.py
- [[.save()]] - code - MachineLearning/social_nlp.py
- [[.save_explanations()]] - code - MachineLearning/social_nlp.py
- [[.score_coherence()]] - code - MachineLearning/social_nlp.py
- [[.stability()]] - code - MachineLearning/social_nlp.py
- [[.test_custom_file_remains_a_partial_override_with_explicit_mask()]] - code - tests/nlp/test_nlp_config.py
- [[.test_dashboard_launcher_reads_the_single_primary_file()]] - code - tests/nlp/test_nlp_config.py
- [[.test_default_and_primary_path_load_configuration_once()]] - code - tests/nlp/test_nlp_config.py
- [[.test_dry_run_shows_effective_paths_without_loading_data_or_fitting()]] - code - tests/nlp/test_nlp_config.py
- [[.test_explanation_validation_does_not_reread_the_editable_file()]] - code - tests/nlp/test_nlp_config.py
- [[.test_falsey_non_objects_and_unknown_settings_are_rejected()]] - code - tests/nlp/test_nlp_config.py
- [[.test_noise_is_not_counted_as_a_coherent_cluster_or_shared_stability()]] - code - tests/nlp/test_social_nlp.py
- [[.test_partial_overrides_preserve_siblings_and_do_not_mutate_input()]] - code - tests/nlp/test_nlp_config.py
- [[Configuration consolidation without fitting, model downloads or API requests.]] - rationale - tests/nlp/test_nlp_config.py
- [[Derive Indonesian Gemini labels after topic count and coherence pass.]] - rationale - MachineLearning/social_nlp.py
- [[Encode with SBERT, fit UMAP + DBSCAN and optionally merge to a topic count.]] - rationale - MachineLearning/social_nlp.py
- [[Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un]] - rationale - MachineLearning/social_nlp.py
- [[Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi]] - rationale - MachineLearning/social_nlp.py
- [[NLPConfigTests]] - code - tests/nlp/test_nlp_config.py
- [[Preserve explicit zero distances, including identical sentence vectors.]] - rationale - MachineLearning/social_nlp.py
- [[Publish a new versioned sidecar; never modify the original run.]] - rationale - MachineLearning/social_nlp.py
- [[Reuse immutable SBERT features only after verifying datamodel identity.]] - rationale - MachineLearning/social_nlp.py
- [[Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.]] - rationale - MachineLearning/social_nlp.py
- [[SocialNLPClusterer_1]] - code - MachineLearning/social_nlp.py
- [[Use the same class TF-IDF vocabulary for selection and publication.]] - rationale - MachineLearning/social_nlp.py
- [[main()_6]] - code - MachineLearning/social_nlp.py
- [[test_nlp_config.py]] - code - tests/nlp/test_nlp_config.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Encoding_dan_Penyimpanan_Model
SORT file.name ASC
```

## Connections to other communities
- 22 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 19 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 13 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 12 edges to [[_COMMUNITY_Model dan Pengujian NLP_1]]
- 7 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 5 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 5 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik]]
- 3 edges to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 3 edges to [[_COMMUNITY_Pengujian Narasi Gemini_1]]
- 2 edges to [[_COMMUNITY_Pengujian UI Streamlit]]
- 2 edges to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 2 edges to [[_COMMUNITY_Wrapper RedditCrawler_1]]
- 2 edges to [[_COMMUNITY_Arsip Data Harian]]
- 1 edge to [[_COMMUNITY_thread_url]]
- 1 edge to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_4]]

## Top bridge nodes
- [[SocialNLPClusterer_1]] - degree 109, connects to 15 communities
- [[.encode()_1]] - degree 13, connects to 3 communities
- [[main()_6]] - degree 12, connects to 3 communities
- [[.prepare_excel()]] - degree 10, connects to 3 communities
- [[.compare()]] - degree 13, connects to 2 communities