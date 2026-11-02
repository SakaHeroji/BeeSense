---
type: community
cohesion: 0.20
members: 17
---

# topic_sentence_export.py

**Cohesion:** 0.20 - loosely connected
**Members:** 17 nodes

## Members
- [[.data()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_export_preserves_original_variants_and_excludes_noise()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_unknown_or_empty_topic_membership_is_rejected()]] - code - tests/nlp/test_topic_sentence_export.py
- [[Keep original variants; remove repeated occurrences of the same text.]] - rationale - scripts/topic_sentence_export.py
- [[Prepare an original-sentence export and seal it into a new NLP snapshot.]] - rationale - scripts/topic_sentence_export.py
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
- [[test_topic_sentence_export.py]] - code - tests/nlp/test_topic_sentence_export.py
- [[topic_sentence_export.py]] - code - scripts/topic_sentence_export.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/topic_sentence_exportpy
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 5 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 3 edges to [[_COMMUNITY_Kontrak Record Reddit]]
- 3 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 3 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 2 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 2 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 1 edge to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 1 edge to [[_COMMUNITY_Model dan Pengujian NLP_2]]
- 1 edge to [[_COMMUNITY_Penggabungan Dataset]]
- 1 edge to [[_COMMUNITY_app.py]]
- 1 edge to [[_COMMUNITY_Pengujian Narasi Gemini_2]]

## Top bridge nodes
- [[social_nlp.py]] - degree 20, connects to 10 communities
- [[json_write()]] - degree 10, connects to 3 communities
- [[topic_sentence_export.py]] - degree 9, connects to 2 communities
- [[seal()]] - degree 8, connects to 2 communities
- [[main()_7]] - degree 7, connects to 2 communities