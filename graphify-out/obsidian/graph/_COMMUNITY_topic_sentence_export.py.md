---
type: community
cohesion: 0.15
members: 21
---

# topic_sentence_export.py

**Cohesion:** 0.15 - loosely connected
**Members:** 21 nodes

## Members
- [[.data()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_export_preserves_original_variants_and_excludes_noise()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_shipped_dashboard_and_explanations_need_no_training_environment()]] - code - tests/cloud/test_dashboard_runtime.py
- [[.test_unknown_or_empty_topic_membership_is_rejected()]] - code - tests/nlp/test_topic_sentence_export.py
- [[CloudRuntimeTests]] - code - tests/cloud/test_dashboard_runtime.py
- [[Keep original variants; remove repeated occurrences of the same text.]] - rationale - scripts/topic_sentence_export.py
- [[Prepare an original-sentence export and seal it into a new NLP snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[Run in an isolated Cloud environment, using only root requirements.txt.]] - rationale - tests/cloud/test_dashboard_runtime.py
- [[Start the local relevance experiment, or its preserved baseline snapshot.]] - rationale - scripts/relevance_dashboard.py
- [[TopicSentenceExportTests]] - code - tests/nlp/test_topic_sentence_export.py
- [[Verify every Excel membership before publishing the complete snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[export_payload()]] - code - scripts/topic_sentence_export.py
- [[json_write()]] - code - MachineLearning/social_nlp.py
- [[main()_14]] - code - scripts/relevance_dashboard.py
- [[main()_7]] - code - scripts/topic_sentence_export.py
- [[relevance_dashboard.py]] - code - scripts/relevance_dashboard.py
- [[seal()]] - code - scripts/topic_sentence_export.py
- [[social_nlp.py]] - code - MachineLearning/social_nlp.py
- [[test_dashboard_runtime.py]] - code - tests/cloud/test_dashboard_runtime.py
- [[test_topic_sentence_export.py]] - code - tests/nlp/test_topic_sentence_export.py
- [[topic_sentence_export.py]] - code - scripts/topic_sentence_export.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/topic_sentence_exportpy
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 8 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 6 edges to [[_COMMUNITY_Akuisisi YouTube]]
- 5 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 3 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 1 edge to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 1 edge to [[_COMMUNITY_Penggabungan Dataset]]
- 1 edge to [[_COMMUNITY_app.py]]
- 1 edge to [[_COMMUNITY_Pengujian Narasi Gemini_1]]

## Top bridge nodes
- [[social_nlp.py]] - degree 20, connects to 9 communities
- [[json_write()]] - degree 10, connects to 2 communities
- [[topic_sentence_export.py]] - degree 9, connects to 2 communities
- [[seal()]] - degree 8, connects to 2 communities
- [[main()_7]] - degree 7, connects to 2 communities