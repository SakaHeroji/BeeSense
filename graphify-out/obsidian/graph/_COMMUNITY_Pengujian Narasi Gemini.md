---
type: community
cohesion: 0.13
members: 25
---

# Pengujian Narasi Gemini

**Cohesion:** 0.13 - loosely connected
**Members:** 25 nodes

## Members
- [[.generate()]] - code - tests/nlp/test_topic_narratives.py
- [[.narrative_source()]] - code - tests/nlp/test_topic_narratives.py
- [[.setUp()_14]] - code - tests/nlp/test_topic_narratives.py
- [[.setUpClass()_3]] - code - tests/nlp/test_topic_narratives.py
- [[.tearDown()_2]] - code - tests/nlp/test_topic_narratives.py
- [[.tearDownClass()_3]] - code - tests/nlp/test_topic_narratives.py
- [[.test_changed_representative_sentence_invalidates_cache_and_tampering_fails()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_credentials_stay_out_of_configuration_and_gate_precedes_api()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_csv_manifest_and_roundtrip_bind_every_topic_and_keyword_weight()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_dashboard_displays_generated_sentence_without_network_or_training()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_http_429_is_bounded_and_error_does_not_leak_server_body_or_key()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_invalid_generated_text_and_changed_keyword_receipt_are_rejected()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_narrative_snapshot_gate_and_source_changes_fail_before_publication()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_narrative_snapshot_preserves_fitted_files_and_original_bundle()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_prompt_revision_refreshes_cache_and_preserves_legacy_csv()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_script_path_entry_point_remains_available()]] - code - tests/nlp/test_topic_narratives.py
- [[.test_twenty_requests_rank_weights_and_resume_without_repeating_api()]] - code - tests/nlp/test_topic_narratives.py
- [[A visibly synthetic fixture exercising the saved-bundle path.]] - rationale - tests/nlp/test_topic_narratives.py
- [[GeminiArtifactTests]] - code - tests/nlp/test_topic_narratives.py
- [[GeminiTests]] - code - tests/nlp/test_topic_narratives.py
- [[Publish a new atomic bundle; never overwrite or refit the source run.]] - rationale - scripts/generate_topic_narratives.py
- [[enrich_run()]] - code - scripts/generate_topic_narratives.py
- [[main()_10]] - code - scripts/generate_topic_narratives.py
- [[response()_1]] - code - tests/nlp/test_topic_narratives.py
- [[topic()]] - code - tests/nlp/test_topic_narratives.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Narasi_Gemini
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Narasi Gemini dan Pembandingan]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube_1]]

## Top bridge nodes
- [[enrich_run()]] - degree 7, connects to 2 communities
- [[GeminiTests]] - degree 11, connects to 1 community
- [[GeminiArtifactTests]] - degree 8, connects to 1 community
- [[topic()]] - degree 7, connects to 1 community
- [[response()_1]] - degree 6, connects to 1 community