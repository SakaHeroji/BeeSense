---
type: community
members: 9
---

# topic_sentence_export.py

**Members:** 9 nodes

## Members
- [[.data()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_export_preserves_original_variants_and_excludes_noise()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_unknown_or_empty_topic_membership_is_rejected()]] - code - tests/nlp/test_topic_sentence_export.py
- [[Keep original variants; remove repeated occurrences of the same text.]] - rationale - scripts/topic_sentence_export.py
- [[Prepare an original-sentence export and seal it into a new NLP snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[TopicSentenceExportTests]] - code - tests/nlp/test_topic_sentence_export.py
- [[export_payload()]] - code - scripts/topic_sentence_export.py
- [[test_topic_sentence_export.py]] - code - tests/nlp/test_topic_sentence_export.py
- [[topic_sentence_export.py]] - code - scripts/topic_sentence_export.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/topic_sentence_exportpy
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 2 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 1 edge to [[_COMMUNITY_Generator Narasi Gemini]]

## Top bridge nodes
- [[topic_sentence_export.py]] - degree 9, connects to 2 communities
- [[export_payload()]] - degree 8, connects to 2 communities