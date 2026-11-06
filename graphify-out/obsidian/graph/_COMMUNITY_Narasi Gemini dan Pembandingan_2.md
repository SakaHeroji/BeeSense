---
type: community
cohesion: 0.29
members: 11
---

# Narasi Gemini dan Pembandingan

**Cohesion:** 0.29 - loosely connected
**Members:** 11 nodes

## Members
- [[.data()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_export_preserves_original_variants_and_excludes_noise()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_unknown_or_empty_topic_membership_is_rejected()]] - code - tests/nlp/test_topic_sentence_export.py
- [[Keep original variants; remove repeated occurrences of the same text.]] - rationale - scripts/topic_sentence_export.py
- [[Prepare an original-sentence export and seal it into a new NLP snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[TopicSentenceExportTests]] - code - tests/nlp/test_topic_sentence_export.py
- [[Verify every Excel membership before publishing the complete snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[export_payload()]] - code - scripts/topic_sentence_export.py
- [[main()_11]] - code - scripts/topic_sentence_export.py
- [[seal()]] - code - scripts/topic_sentence_export.py
- [[topic_sentence_export.py]] - code - scripts/topic_sentence_export.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Narasi_Gemini_dan_Pembandingan
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]
- 3 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 1 edge to [[_COMMUNITY_Akuisisi TikTok dan Ekspor_1]]

## Top bridge nodes
- [[topic_sentence_export.py]] - degree 9, connects to 2 communities
- [[export_payload()]] - degree 8, connects to 2 communities
- [[seal()]] - degree 5, connects to 1 community
- [[main()_11]] - degree 4, connects to 1 community
- [[TopicSentenceExportTests]] - degree 4, connects to 1 community