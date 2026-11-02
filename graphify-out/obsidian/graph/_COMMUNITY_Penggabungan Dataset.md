---
type: community
cohesion: 0.08
members: 48
---

# Penggabungan Dataset

**Cohesion:** 0.08 - loosely connected
**Members:** 48 nodes

## Members
- [[.run_merge()]] - code - tests/nlp/test_dataset_merge.py
- [[.setUp()_9]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.setUp()_14]] - code - tests/nlp/test_dataset_merge.py
- [[.source()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_active_topic_count_and_coherence_threshold_are_enforced()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_append_only_merge_sidecars_are_required_and_checksum_bound()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_archived_nlp_snapshot_and_separate_crawl_output_are_supported()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_input_integrity_remains_enforced()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_instagram_comment_identity_conflict_and_fake_host_are_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_instagram_latest_record_wins_without_removing_equal_text_distinct_ids()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_latest_policy_audits_updated_comment_reply_classification()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_latest_policy_still_rejects_comment_attached_to_different_root()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_merge_preserves_identical_text_distinct_ids_and_formula_like_text()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_merged_input_preserves_and_checks_both_baseline_workbooks()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_missing_baseline_compact_is_rejected_for_merged_input()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_missing_preserved_audit_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_native_uniqueness_is_independent_of_equal_text_and_kind()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_orphan_comment_is_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_preserved_audit_and_excel_owner_files_are_supported()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_preserved_baseline_hash_is_checked_after_switching_to_merged_input()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_published_merge_audit_is_bound_to_its_file_checksums()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_same_native_id_different_kind_is_rejected_without_publication()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_twitter_comment_without_root_evidence_is_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_twitter_native_dedup_and_audited_roots_survive_merge()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_twitter_sidecar_cannot_be_reused_for_changed_workbook()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_unexpected_file_in_archive_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_unexpected_workbook_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[Keep the latest supplied observation per native ID, with full row lineage.]] - rationale - scripts/merge_social_datasets.py
- [[Merge compact crawl workbooks, rejecting repeated native content identities.]] - rationale - scripts/merge_social_datasets.py
- [[MergeTests]] - code - tests/nlp/test_dataset_merge.py
- [[NativeDatasetTests]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[PublishedDataTests]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[Read a workbook-bound sidecar, or the original hash-verified crawl audit.]] - rationale - MachineLearning/source_roots.py
- [[Resolve X conversation roots from audited native IDs, never caption similarity.]] - rationale - MachineLearning/source_roots.py
- [[Return global native object ID plus its root; text never defines identity.]] - rationale - scripts/merge_social_datasets.py
- [[checksum()]] - code - MachineLearning/source_roots.py
- [[identity()]] - code - scripts/merge_social_datasets.py
- [[main()_12]] - code - scripts/merge_social_datasets.py
- [[merge()]] - code - scripts/merge_social_datasets.py
- [[merge_social_datasets.py]] - code - scripts/merge_social_datasets.py
- [[merge_unique()]] - code - scripts/merge_social_datasets.py
- [[native()]] - code - MachineLearning/source_roots.py
- [[sha()]] - code - scripts/merge_social_datasets.py
- [[source_roots.py]] - code - MachineLearning/source_roots.py
- [[test_dashboard_data_verifier.py]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[test_dataset_merge.py]] - code - tests/nlp/test_dataset_merge.py
- [[twitter_roots()]] - code - MachineLearning/source_roots.py
- [[write_roots()]] - code - MachineLearning/source_roots.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Penggabungan_Dataset
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 4 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model_1]]
- 2 edges to [[_COMMUNITY_Konteks dan Provenance Gemini]]
- 2 edges to [[_COMMUNITY_topic_sentence_export.py]]
- 1 edge to [[_COMMUNITY_Bukti Ekstraktif Topik_1]]
- 1 edge to [[_COMMUNITY_Bukti Ekstraktif Topik]]

## Top bridge nodes
- [[twitter_roots()]] - degree 13, connects to 3 communities
- [[test_dataset_merge.py]] - degree 9, connects to 2 communities
- [[MergeTests]] - degree 15, connects to 1 community
- [[merge_social_datasets.py]] - degree 12, connects to 1 community
- [[write_roots()]] - degree 10, connects to 1 community