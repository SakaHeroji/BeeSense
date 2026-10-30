---
type: community
cohesion: 0.13
members: 17
---

# Pipeline dan Persistensi NLP

**Cohesion:** 0.13 - loosely connected
**Members:** 17 nodes

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
- [[.stability()]] - code - MachineLearning/social_nlp.py
- [[.test_noise_is_not_counted_as_a_coherent_cluster_or_shared_stability()]] - code - tests/nlp/test_social_nlp.py
- [[Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un]] - rationale - MachineLearning/social_nlp.py
- [[Merge entire DBSCAN groups using sentence-weighted Ward linkage.          Minimi]] - rationale - MachineLearning/social_nlp.py
- [[Preserve explicit zero distances, including identical sentence vectors.]] - rationale - MachineLearning/social_nlp.py
- [[Select DBSCAN parameters on UMAP; evaluate in original SBERT geometry.]] - rationale - MachineLearning/social_nlp.py
- [[Use the same class TF-IDF vocabulary for selection and publication.]] - rationale - MachineLearning/social_nlp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pipeline_dan_Persistensi_NLP
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP]]
- 8 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_1]]
- 3 edges to [[_COMMUNITY_Ringkasan Topik Gemini]]
- 1 edge to [[_COMMUNITY_Coherence dan Quality Gate]]
- 1 edge to [[_COMMUNITY_Coherence dan Quality Gate_1]]

## Top bridge nodes
- [[.compare()]] - degree 13, connects to 3 communities
- [[.describe_topics()]] - degree 6, connects to 3 communities
- [[._merge_topics()]] - degree 5, connects to 3 communities
- [[._radius_graph()]] - degree 4, connects to 3 communities
- [[.score_coherence()]] - degree 7, connects to 2 communities