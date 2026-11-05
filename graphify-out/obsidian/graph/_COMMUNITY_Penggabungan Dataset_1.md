---
type: community
members: 22
---

# Penggabungan Dataset

**Members:** 22 nodes

## Members
- [[.setUp()_17]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.setUp()_18]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_active_topic_count_and_coherence_threshold_are_enforced()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_append_only_merge_sidecars_are_required_and_checksum_bound()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_archived_nlp_snapshot_and_separate_crawl_output_are_supported()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_input_integrity_remains_enforced()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_merged_input_preserves_and_checks_both_baseline_workbooks()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_missing_baseline_compact_is_rejected_for_merged_input()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_missing_preserved_audit_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_native_uniqueness_is_independent_of_equal_text_and_kind()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_old_relevance_dataset_remains_verified_and_tracked_after_switching_runs()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_preserved_audit_and_excel_owner_files_are_supported()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_preserved_baseline_hash_is_checked_after_switching_to_merged_input()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_published_filter_is_bound_to_the_fitted_decisions_and_source()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_published_merge_audit_is_bound_to_its_file_checksums()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_tampered_relevance_file_cannot_be_published()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_unexpected_file_in_archive_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_unexpected_workbook_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[NativeDatasetTests]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[PublishedDataTests]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[PublishedRelevanceTests]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[test_dashboard_data_verifier.py]] - code - tests/nlp/test_dashboard_data_verifier.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Penggabungan_Dataset
SORT file.name ASC
```
