---
type: community
cohesion: 0.22
members: 10
---

# Model dan Pengujian NLP

**Cohesion:** 0.22 - loosely connected
**Members:** 10 nodes

## Members
- [[._apply_context_relevance()]] - code - MachineLearning/social_nlp.py
- [[._clean()]] - code - MachineLearning/social_nlp.py
- [[._explanation_evidence()]] - code - MachineLearning/social_nlp.py
- [[.load_decisions()]] - code - MachineLearning/context_relevance.py
- [[.prepare_excel()]] - code - MachineLearning/social_nlp.py
- [[.sentence_spans()]] - code - MachineLearning/social_nlp.py
- [[.test_long_segments_cover_text_without_silent_truncation()]] - code - tests/nlp/test_social_nlp.py
- [[.test_span_offsets_and_abbreviations_are_source_faithful()]] - code - tests/nlp/test_social_nlp.py
- [[Extract real sentences using relevance plus MMR diversity.]] - rationale - MachineLearning/social_nlp.py
- [[Rule-based segmentation preserving exact offsets in the original text.]] - rationale - MachineLearning/social_nlp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Model_dan_Pengujian_NLP
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 5 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 2 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik_1]]
- 2 edges to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 2 edges to [[_COMMUNITY_Penyaringan Relevansi dan Narasi Topik]]

## Top bridge nodes
- [[.prepare_excel()]] - degree 10, connects to 4 communities
- [[._apply_context_relevance()]] - degree 5, connects to 3 communities
- [[.load_decisions()]] - degree 4, connects to 2 communities
- [[.sentence_spans()]] - degree 5, connects to 1 community
- [[._clean()]] - degree 4, connects to 1 community