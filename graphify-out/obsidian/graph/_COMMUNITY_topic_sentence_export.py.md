---
type: community
cohesion: 0.23
members: 15
---

# topic_sentence_export.py

**Cohesion:** 0.23 - loosely connected
**Members:** 15 nodes

## Members
- [[.data()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.save_explanations()]] - code - MachineLearning/social_nlp.py
- [[.test_export_preserves_original_variants_and_excludes_noise()]] - code - tests/nlp/test_topic_sentence_export.py
- [[.test_unknown_or_empty_topic_membership_is_rejected()]] - code - tests/nlp/test_topic_sentence_export.py
- [[Keep original variants; remove repeated occurrences of the same text.]] - rationale - scripts/topic_sentence_export.py
- [[Prepare an original-sentence export and seal it into a new NLP snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[Publish a new versioned sidecar; never modify the original run.]] - rationale - MachineLearning/social_nlp.py
- [[TopicSentenceExportTests]] - code - tests/nlp/test_topic_sentence_export.py
- [[Verify every Excel membership before publishing the complete snapshot.]] - rationale - scripts/topic_sentence_export.py
- [[export_payload()]] - code - scripts/topic_sentence_export.py
- [[json_write()]] - code - MachineLearning/social_nlp.py
- [[main()_7]] - code - scripts/topic_sentence_export.py
- [[seal()]] - code - scripts/topic_sentence_export.py
- [[test_topic_sentence_export.py]] - code - tests/nlp/test_topic_sentence_export.py
- [[topic_sentence_export.py]] - code - scripts/topic_sentence_export.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/topic_sentence_exportpy
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 4 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 3 edges to [[_COMMUNITY_Akuisisi YouTube_1]]
- 2 edges to [[_COMMUNITY_Model dan Pengujian NLP]]

## Top bridge nodes
- [[.save_explanations()]] - degree 5, connects to 3 communities
- [[json_write()]] - degree 10, connects to 2 communities
- [[topic_sentence_export.py]] - degree 9, connects to 2 communities
- [[seal()]] - degree 8, connects to 2 communities
- [[main()_7]] - degree 7, connects to 2 communities