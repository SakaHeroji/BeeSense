---
type: community
cohesion: 0.28
members: 13
---

# topic_sentence_export.py

**Cohesion:** 0.28 - loosely connected
**Members:** 13 nodes

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
- [[main()_1]] - code - scripts/topic_sentence_export.py
- [[seal()]] - code - scripts/topic_sentence_export.py
- [[test_topic_sentence_export.py]] - code - tests/nlp/test_topic_sentence_export.py
- [[topic_sentence_export.py]] - code - scripts/topic_sentence_export.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/topic_sentence_exportpy
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 5 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 3 edges to [[_COMMUNITY_Kontrak Record Reddit]]
- 2 edges to [[_COMMUNITY_Model dan Pengujian NLP_1]]

## Top bridge nodes
- [[json_write()]] - degree 10, connects to 3 communities
- [[topic_sentence_export.py]] - degree 9, connects to 3 communities
- [[seal()]] - degree 8, connects to 2 communities
- [[main()_1]] - degree 7, connects to 2 communities
- [[export_payload()]] - degree 8, connects to 1 community