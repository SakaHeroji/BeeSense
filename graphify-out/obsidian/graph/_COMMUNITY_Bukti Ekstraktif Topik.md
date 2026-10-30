---
type: community
members: 13
---

# Bukti Ekstraktif Topik

**Members:** 13 nodes

## Members
- [[._clean()]] - code - MachineLearning/social_nlp.py
- [[._explanation_evidence()]] - code - MachineLearning/social_nlp.py
- [[._explanation_term_changes()]] - code - MachineLearning/social_nlp.py
- [[._explanation_trend()]] - code - MachineLearning/social_nlp.py
- [[.explain_topics()]] - code - MachineLearning/social_nlp.py
- [[.parent_post_key()]] - code - MachineLearning/social_nlp.py
- [[.sentence_spans()]] - code - MachineLearning/social_nlp.py
- [[.test_long_segments_cover_text_without_silent_truncation()]] - code - tests/nlp/test_social_nlp.py
- [[.test_span_offsets_and_abbreviations_are_source_faithful()]] - code - tests/nlp/test_social_nlp.py
- [[Evidence-grounded topic descriptions and descriptive, source-aware trends.]] - rationale - MachineLearning/social_nlp.py
- [[Extract real sentences using relevance plus MMR diversity.]] - rationale - MachineLearning/social_nlp.py
- [[Identify the parent thread, not the individual comment URL.]] - rationale - MachineLearning/social_nlp.py
- [[Rule-based segmentation preserving exact offsets in the original text.]] - rationale - MachineLearning/social_nlp.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Bukti_Ekstraktif_Topik
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 4 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 3 edges to [[_COMMUNITY_Generator Narasi Gemini]]
- 1 edge to [[_COMMUNITY_Penjelasan Topik Dashboard]]

## Top bridge nodes
- [[.explain_topics()]] - degree 10, connects to 3 communities
- [[.parent_post_key()]] - degree 5, connects to 3 communities
- [[.sentence_spans()]] - degree 5, connects to 2 communities
- [[._explanation_evidence()]] - degree 5, connects to 2 communities
- [[._clean()]] - degree 4, connects to 2 communities