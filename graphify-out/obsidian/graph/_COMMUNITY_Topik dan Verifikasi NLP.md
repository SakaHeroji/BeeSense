---
type: community
cohesion: 0.08
members: 40
---

# Topik dan Verifikasi NLP

**Cohesion:** 0.08 - loosely connected
**Members:** 40 nodes

## Members
- [[.run_merge()]] - code - tests/nlp/test_dataset_merge.py
- [[.setUp()_10]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.setUp()_8]] - code - tests/nlp/test_dataset_merge.py
- [[.source()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_active_topic_count_and_coherence_threshold_are_enforced()]] - code - tests/nlp/test_dashboard_data_verifier.py
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
- [[.test_unexpected_file_in_archive_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_unexpected_workbook_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[Atomic baseline-then-new workbook merge preserves native identity and provenance]] - rationale - docs/crawler/SOCIAL_CRAWLER.md
- [[Combined workbook provenance PASS with immutable source hashes and row lineage]] - document - output/combined_dataset_20261029.json
- [[Keep the latest supplied observation per native ID, with full row lineage.]] - rationale - scripts/merge_social_datasets.py
- [[Merge compact crawl workbooks, rejecting repeated native content identities.]] - rationale - scripts/merge_social_datasets.py
- [[MergeTests]] - code - tests/nlp/test_dataset_merge.py
- [[Merged corpus 29, 099 rows, 1, 517 roots and 27, 582 commentsreplies]] - concept - graphify-out/obsidian/Crawling 1000 Post Baru.md
- [[NativeDatasetTests]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[PublishedDataTests]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[Return global native object ID plus its root; text never defines identity.]] - rationale - scripts/merge_social_datasets.py
- [[identity()]] - code - scripts/merge_social_datasets.py
- [[main()_8]] - code - scripts/merge_social_datasets.py
- [[merge()]] - code - scripts/merge_social_datasets.py
- [[merge_social_datasets.py]] - code - scripts/merge_social_datasets.py
- [[merge_unique()]] - code - scripts/merge_social_datasets.py
- [[sha()]] - code - scripts/merge_social_datasets.py
- [[test_dashboard_data_verifier.py]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[test_dataset_merge.py]] - code - tests/nlp/test_dataset_merge.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Topik_dan_Verifikasi_NLP
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Ringkasan Topik Gemini]]
- 2 edges to [[_COMMUNITY_Akuisisi Instagram Terintegrasi_3]]
- 2 edges to [[_COMMUNITY_Pipeline dan Persistensi NLP_2]]
- 1 edge to [[_COMMUNITY_Topik dan Verifikasi NLP_1]]
- 1 edge to [[_COMMUNITY_Coherence dan Quality Gate_2]]
- 1 edge to [[_COMMUNITY_Alur Akuisisi Sosial Terpadu_4]]

## Top bridge nodes
- [[identity()]] - degree 10, connects to 2 communities
- [[Merged corpus 29, 099 rows, 1, 517 roots and 27, 582 commentsreplies]] - degree 4, connects to 2 communities
- [[merge()]] - degree 14, connects to 1 community
- [[merge_social_datasets.py]] - degree 9, connects to 1 community
- [[merge_unique()]] - degree 6, connects to 1 community