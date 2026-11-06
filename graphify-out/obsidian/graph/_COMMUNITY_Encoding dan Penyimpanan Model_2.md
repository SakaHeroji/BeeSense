---
type: community
cohesion: 0.11
members: 20
---

# Encoding dan Penyimpanan Model

**Cohesion:** 0.11 - loosely connected
**Members:** 20 nodes

## Members
- [[._ctfidf_terms()]] - code - MachineLearning/social_nlp.py
- [[._evaluate()]] - code - MachineLearning/social_nlp.py
- [[._filter_radius()]] - code - MachineLearning/social_nlp.py
- [[._merge_topics()]] - code - MachineLearning/social_nlp.py
- [[._radius_graph()]] - code - MachineLearning/social_nlp.py
- [[._topic_vectorizer()]] - code - MachineLearning/social_nlp.py
- [[.build_topic_graph()]] - code - MachineLearning/social_nlp.py
- [[.compare()]] - code - MachineLearning/social_nlp.py
- [[.describe_topics()]] - code - MachineLearning/social_nlp.py
- [[.score_coherence()]] - code - MachineLearning/social_nlp.py
- [[.select_candidate()]] - code - MachineLearning/social_nlp.py
- [[.stability()]] - code - MachineLearning/social_nlp.py
- [[.test_close_scores_prefer_separation_without_hardcoding_algorithm()]] - code - tests/nlp/test_social_nlp.py
- [[.test_dbscan_memory_guard_and_no_eligible_candidate_are_explicit()]] - code - tests/nlp/test_social_nlp.py
- [[.test_noise_is_not_counted_as_a_coherent_cluster_or_shared_stability()]] - code - tests/nlp/test_social_nlp.py
- [[Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un]] - rationale - MachineLearning/social_nlp.py
- [[Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi]] - rationale - MachineLearning/social_nlp.py
- [[Preserve explicit zero distances, including identical sentence vectors.]] - rationale - MachineLearning/social_nlp.py
- [[Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.]] - rationale - MachineLearning/social_nlp.py
- [[Use the same class TF-IDF vocabulary for selection and publication.]] - rationale - MachineLearning/social_nlp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Encoding_dan_Penyimpanan_Model
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 7 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_3]]
- 4 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 3 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 1 edge to [[_COMMUNITY_Narasi Gemini dan Pembandingan_1]]

## Top bridge nodes
- [[.score_coherence()]] - degree 7, connects to 3 communities
- [[.describe_topics()]] - degree 6, connects to 3 communities
- [[._radius_graph()]] - degree 4, connects to 3 communities
- [[.compare()]] - degree 12, connects to 2 communities
- [[.select_candidate()]] - degree 5, connects to 2 communities