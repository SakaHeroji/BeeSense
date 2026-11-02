---
type: community
cohesion: 0.18
members: 20
---

# Pengujian Narasi Gemini

**Cohesion:** 0.18 - loosely connected
**Members:** 20 nodes

## Members
- [[.generate()]] - code - tests/nlp/test_topic_narratives.py
- [[.setUp()_11]] - code - tests/nlp/test_topic_narratives.py
- [[.setUpClass()_2]] - code - tests/nlp/test_topic_narratives.py
- [[.tearDown()_1]] - code - tests/nlp/test_topic_narratives.py
- [[.tearDownClass()_2]] - code - tests/nlp/test_topic_narratives.py
- [[.test_changed_representative_sentence_invalidates_cache_and_tampering_fails()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_credentials_stay_out_of_configuration_and_gate_precedes_api()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_csv_manifest_and_roundtrip_bind_every_topic_and_keyword_weight()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_dashboard_displays_generated_sentence_without_network_or_training()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_http_429_is_bounded_and_error_does_not_leak_server_body_or_key()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_invalid_generated_text_and_changed_keyword_receipt_are_rejected()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_prompt_revision_refreshes_cache_and_preserves_legacy_csv()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_script_path_entry_point_remains_available()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_twenty_requests_rank_weights_and_resume_without_repeating_api()]] - code - tests/nlp/test_topic_narratives.py
- [[GeminiArtifactTests]] - code - tests/nlp/test_topic_narratives.py
- [[GeminiTests]] - code - tests/nlp/test_topic_narratives.py
- [[Nine Gemini offline tests and all20 actual contextual CSV rows validated]] - rationale - docs/machine-learning/GEMINI_TOPIC_NARRATIVES.md
- [[response()_2]] - code - tests/nlp/test_topic_narratives.py
- [[test_topic_narratives.py]] - code - tests/nlp/test_topic_narratives.py
- [[topic()]] - code - tests/nlp/test_topic_narratives.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Narasi_Gemini
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 3 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube]]
- 1 edge to [[_COMMUNITY_topic_sentence_export.py]]
- 1 edge to [[_COMMUNITY_Konteks dan Provenance Gemini]]

## Top bridge nodes
- [[test_topic_narratives.py]] - degree 8, connects to 4 communities
- [[GeminiTests]] - degree 13, connects to 1 community
- [[GeminiArtifactTests]] - degree 7, connects to 1 community
- [[Nine Gemini offline tests and all20 actual contextual CSV rows validated]] - degree 3, connects to 1 community
- [[.setUpClass()_2]] - degree 3, connects to 1 community