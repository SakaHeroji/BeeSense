---
type: community
cohesion: 0.33
members: 7
---

# Pipeline dan Persistensi NLP

**Cohesion:** 0.33 - loosely connected
**Members:** 7 nodes

## Members
- [[._ctfidf_terms()]] - code - MachineLearning/social_nlp.py
- [[._topic_vectorizer()]] - code - MachineLearning/social_nlp.py
- [[.build_topic_graph()]] - code - MachineLearning/social_nlp.py
- [[.describe_topics()]] - code - MachineLearning/social_nlp.py
- [[.score_coherence()]] - code - MachineLearning/social_nlp.py
- [[Macro c_v on ALL non-noise topics and a fixed full-corpus reference.          Un]] - rationale - MachineLearning/social_nlp.py
- [[Use the same class TF-IDF vocabulary for selection and publication.]] - rationale - MachineLearning/social_nlp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pipeline_dan_Persistensi_NLP
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP]]
- 4 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_1]]
- 1 edge to [[_COMMUNITY_Ringkasan Topik Gemini]]
- 1 edge to [[_COMMUNITY_Pipeline dan Persistensi NLP_2]]

## Top bridge nodes
- [[.score_coherence()]] - degree 7, connects to 3 communities
- [[.describe_topics()]] - degree 6, connects to 3 communities
- [[._ctfidf_terms()]] - degree 5, connects to 2 communities
- [[._topic_vectorizer()]] - degree 3, connects to 1 community
- [[.build_topic_graph()]] - degree 2, connects to 1 community