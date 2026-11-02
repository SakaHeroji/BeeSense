---
type: community
cohesion: 0.26
members: 14
---

# topic_sentence_export.py

**Cohesion:** 0.26 - loosely connected
**Members:** 14 nodes

## Members
- [[.data()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_export_preserves_original_variants_and_excludes_noise()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_unknown_or_empty_topic_membership_is_rejected()]] - code - tests/nlp/test_topic_sentence_export.py
- [[Keep original variants; remove repeated occurrences of the same text.]] - rationale - scripts/topic_sentence_export.py
- [[Prepare an original-sentence export and seal it into a new NLP snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[TopicSentenceExportTests]] - code - tests/nlp/test_topic_sentence_export.py
- [[Verify every Excel membership before publishing the complete snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[export_payload()]] - code - scripts/topic_sentence_export.py
- [[json_write()]] - code - MachineLearning/social_nlp.py
- [[main()_7]] - code - scripts/topic_sentence_export.py
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
- 9 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 4 edges to [[_COMMUNITY_Akuisisi YouTube]]
- 4 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 3 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 2 edges to [[_COMMUNITY_Penggabungan Dataset]]
- 1 edge to [[_COMMUNITY_Pengujian Penjelasan Topik]]
- 1 edge to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 1 edge to [[_COMMUNITY_app.py]]
- 1 edge to [[_COMMUNITY_Model dan Pengujian NLP_1]]

## Top bridge nodes
- [[social_nlp.py]] - degree 15, connects to 8 communities
- [[topic_sentence_export.py]] - degree 9, connects to 2 communities
- [[json_write()]] - degree 8, connects to 2 communities
- [[seal()]] - degree 8, connects to 2 communities
- [[main()_7]] - degree 7, connects to 2 communities