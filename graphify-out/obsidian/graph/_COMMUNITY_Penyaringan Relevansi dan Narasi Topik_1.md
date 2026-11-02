---
type: community
cohesion: 0.08
members: 47
---

# Penyaringan Relevansi dan Narasi Topik

**Cohesion:** 0.08 - loosely connected
**Members:** 47 nodes

## Members
- [[.__call__()_3]] - code - MachineLearning/relevance_semantic.py
- [[.__init__()_37]] - code - MachineLearning/context_relevance.py
- [[.__init__()_38]] - code - MachineLearning/relevance_semantic.py
- [[._scores()]] - code - MachineLearning/context_relevance.py
- [[._validate()]] - code - MachineLearning/context_relevance.py
- [[.build_units()]] - code - MachineLearning/context_relevance.py
- [[.classify_many()]] - code - MachineLearning/context_relevance.py
- [[.close()_7]] - code - MachineLearning/context_relevance.py
- [[.encode()]] - code - MachineLearning/relevance_semantic.py
- [[.filter_snapshot()]] - code - MachineLearning/context_relevance.py
- [[.load_decisions()]] - code - MachineLearning/context_relevance.py
- [[.make()]] - code - tests/nlp/test_context_relevance.py
- [[.predictor()]] - code - tests/nlp/test_context_relevance.py
- [[.setUp()_12]] - code - tests/nlp/test_context_relevance.py
- [[.snapshot()]] - code - tests/nlp/test_context_relevance.py
- [[.tearDown()_1]] - code - tests/nlp/test_context_relevance.py
- [[.test_audit_csv_escapes_formulas_without_changing_stored_text()]] - code - tests/nlp/test_context_relevance.py
- [[.test_cache_resumes_and_configuration_changes_invalidate_it()]] - code - tests/nlp/test_context_relevance.py
- [[.test_checksum_tampering_is_rejected()]] - code - tests/nlp/test_context_relevance.py
- [[.test_direct_relevance_and_unrelated_target_never_inherit_root()]] - code - tests/nlp/test_context_relevance.py
- [[.test_explicit_configuration_does_not_inherit_another_corpus_mask()]] - code - tests/nlp/test_context_relevance.py
- [[.test_filter_dataset_is_immutable_and_bound_to_entire_source()]] - code - tests/nlp/test_context_relevance.py
- [[.test_invalid_configuration_and_scores_fail_closed()]] - code - tests/nlp/test_context_relevance.py
- [[.test_same_ambiguous_sentence_can_have_different_context_decisions()]] - code - tests/nlp/test_context_relevance.py
- [[.test_training_consumes_mask_without_modifying_source_text()]] - code - tests/nlp/test_context_relevance.py
- [[.test_weak_short_match_requires_context()]] - code - tests/nlp/test_context_relevance.py
- [[Classify target sentences; parent context may rescue only ambiguous text.      U]] - rationale - MachineLearning/context_relevance.py
- [[ContextRelevanceFilter]] - code - MachineLearning/context_relevance.py
- [[Filter a verified existing corpus into a new auditable relevance dataset.]] - rationale - scripts/filter_context_relevance.py
- [[Keep original audit data intact; escape spreadsheet formulas on export.]] - rationale - Dashboard/app.py
- [[Local, auditable zero-shot relevance decisions before topic clustering.  Model s]] - rationale - MachineLearning/context_relevance.py
- [[LocalSemanticBackend]] - code - MachineLearning/relevance_semantic.py
- [[No modelnetwork calls policy, provenance and integration regressions.]] - rationale - tests/nlp/test_context_relevance.py
- [[Reference profile and lazy local SBERT backend for relevance filtering.]] - rationale - MachineLearning/relevance_semantic.py
- [[RelevanceTests]] - code - tests/nlp/test_context_relevance.py
- [[Resolve roots from native URLs; never match conversations by title.]] - rationale - MachineLearning/context_relevance.py
- [[SBERT prototypes; scores are cosine similarities, never probabilities.]] - rationale - MachineLearning/relevance_semantic.py
- [[Units contain target ``sentence`` and optional audited parentpost text.]] - rationale - MachineLearning/context_relevance.py
- [[Write a new, checksum-bound decision dataset; never overwrite input.]] - rationale - MachineLearning/context_relevance.py
- [[checksum()_1]] - code - MachineLearning/context_relevance.py
- [[context_relevance.py]] - code - MachineLearning/context_relevance.py
- [[digest()_3]] - code - MachineLearning/context_relevance.py
- [[filter_context_relevance.py]] - code - scripts/filter_context_relevance.py
- [[main()_12]] - code - scripts/filter_context_relevance.py
- [[relevance_csv()]] - code - Dashboard/app.py
- [[relevance_semantic.py]] - code - MachineLearning/relevance_semantic.py
- [[test_context_relevance.py]] - code - tests/nlp/test_context_relevance.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Penyaringan_Relevansi_dan_Narasi_Topik
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 3 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 2 edges to [[_COMMUNITY_Pengujian Narasi Gemini_2]]
- 1 edge to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 1 edge to [[_COMMUNITY_Pengujian Narasi Gemini]]
- 1 edge to [[_COMMUNITY_app.py]]
- 1 edge to [[_COMMUNITY_Render Dashboard Streamlit]]

## Top bridge nodes
- [[ContextRelevanceFilter]] - degree 20, connects to 3 communities
- [[test_context_relevance.py]] - degree 9, connects to 2 communities
- [[filter_context_relevance.py]] - degree 8, connects to 2 communities
- [[relevance_csv()]] - degree 5, connects to 2 communities
- [[.load_decisions()]] - degree 4, connects to 2 communities