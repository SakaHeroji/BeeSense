---
type: community
members: 67
---

# Arsip Data Harian

**Members:** 67 nodes

## Members
- [[.crawler()_1]] - code - tests/crawler/test_social_archive.py
- [[.run_merge()]] - code - tests/nlp/test_dataset_merge.py
- [[.setUp()_4]] - code - tests/nlp/test_dataset_merge.py
- [[.setUp()_10]] - code - tests/crawler/test_social_archive.py
- [[.source()]] - code - tests/nlp/test_dataset_merge.py
- [[.source()_1]] - code - tests/crawler/test_social_archive.py
- [[.test_dates_use_audit_wib_midnight_instead_of_publication_dates()]] - code - tests/crawler/test_social_archive.py
- [[.test_default_crawler_writes_private_bundle_and_organized_outputs()]] - code - tests/crawler/test_social_archive.py
- [[.test_global_dedup_keeps_first_wib_day_and_latest_observation()]] - code - tests/crawler/test_social_archive.py
- [[.test_historical_recovery_keeps_day_precision_and_checks_merge_hash()]] - code - tests/crawler/test_social_archive.py
- [[.test_instagram_comment_identity_conflict_and_fake_host_are_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_instagram_latest_record_wins_without_removing_equal_text_distinct_ids()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_latest_policy_audits_updated_comment_reply_classification()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_latest_policy_still_rejects_comment_attached_to_different_root()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_merge_preserves_identical_text_distinct_ids_and_formula_like_text()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_orphan_comment_is_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_same_native_id_different_kind_is_rejected_without_publication()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_synthetic_and_changed_sources_fail_without_replacing_archive()]] - code - tests/crawler/test_social_archive.py
- [[.test_twitter_comment_without_root_evidence_is_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_twitter_native_dedup_and_audited_roots_survive_merge()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_twitter_sidecar_cannot_be_reused_for_changed_workbook()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_unmanaged_output_directory_is_preserved()]] - code - tests/crawler/test_social_archive.py
- [[ArchiveTests]] - code - tests/crawler/test_social_archive.py
- [[Bind compact rows to real acquisition timestamps and native roots.]] - rationale - Crawler/Backend/social_archive.py
- [[Consolidate original crawl bundles by platformday without repeated native IDs.]] - rationale - scripts/organize_social_outputs.py
- [[Daily partitions must be globally unique and bound to native crawl evidence.]] - rationale - tests/crawler/test_social_archive.py
- [[Keep the latest supplied observation per native ID, with full row lineage.]] - rationale - scripts/merge_social_datasets.py
- [[Merge compact crawl workbooks, rejecting repeated native content identities.]] - rationale - scripts/merge_social_datasets.py
- [[MergeTests]] - code - tests/nlp/test_dataset_merge.py
- [[Native social record identity shared by merge and organized crawler outputs.]] - rationale - Crawler/Backend/social_identity.py
- [[Publish one globally unique social dataset partitioned by platform and crawl day]] - rationale - Crawler/Backend/social_archive.py
- [[Read a workbook-bound sidecar, or the original hash-verified crawl audit.]] - rationale - MachineLearning/source_roots.py
- [[Read every exported row back; fail on repeated IDs, wrong days or lost rows.]] - rationale - Crawler/Backend/social_archive.py
- [[Recover a verified merge's source range with honest day-only precision.]] - rationale - Crawler/Backend/social_archive.py
- [[Resolve X conversation roots from audited native IDs, never caption similarity.]] - rationale - MachineLearning/source_roots.py
- [[Return global native object ID plus its root; text never defines identity.]] - rationale - Crawler/Backend/social_identity.py
- [[Upsert observations, retain latest values and assign each ID its first WIB day.]] - rationale - Crawler/Backend/social_archive.py
- [[_audit_key()]] - code - Crawler/Backend/social_archive.py
- [[_lock()]] - code - Crawler/Backend/social_archive.py
- [[_native()]] - code - Crawler/Backend/social_archive.py
- [[_write_day()]] - code - Crawler/Backend/social_archive.py
- [[checksum()]] - code - MachineLearning/source_roots.py
- [[consolidate()]] - code - scripts/organize_social_outputs.py
- [[crawl_day()]] - code - Crawler/Backend/social_archive.py
- [[discover()]] - code - scripts/organize_social_outputs.py
- [[historical_records()]] - code - Crawler/Backend/social_archive.py
- [[identity()]] - code - Crawler/Backend/social_identity.py
- [[main()_4]] - code - scripts/merge_social_datasets.py
- [[main()_5]] - code - scripts/organize_social_outputs.py
- [[merge()]] - code - scripts/merge_social_datasets.py
- [[merge_social_datasets.py]] - code - scripts/merge_social_datasets.py
- [[merge_unique()]] - code - scripts/merge_social_datasets.py
- [[native()]] - code - MachineLearning/source_roots.py
- [[organize()]] - code - Crawler/Backend/social_archive.py
- [[organize_social_outputs.py]] - code - scripts/organize_social_outputs.py
- [[sha()]] - code - scripts/merge_social_datasets.py
- [[sha()_1]] - code - Crawler/Backend/social_archive.py
- [[social_archive.py]] - code - Crawler/Backend/social_archive.py
- [[social_identity.py]] - code - Crawler/Backend/social_identity.py
- [[source_records()]] - code - Crawler/Backend/social_archive.py
- [[source_roots.py]] - code - MachineLearning/source_roots.py
- [[stamp()]] - code - Crawler/Backend/social_archive.py
- [[test_dataset_merge.py]] - code - tests/nlp/test_dataset_merge.py
- [[test_social_archive.py]] - code - tests/crawler/test_social_archive.py
- [[twitter_roots()]] - code - MachineLearning/source_roots.py
- [[verify()_1]] - code - Crawler/Backend/social_archive.py
- [[write_roots()]] - code - MachineLearning/source_roots.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Arsip_Data_Harian
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi]]
- 2 edges to [[_COMMUNITY_Encoding dan Penyimpanan Model]]
- 2 edges to [[_COMMUNITY_Arsip Data Harian_1]]
- 2 edges to [[_COMMUNITY_Akuisisi TikTok dan Ekspor_2]]
- 1 edge to [[_COMMUNITY_Akuisisi YouTube_2]]
- 1 edge to [[_COMMUNITY_Pengujian Koordinator Crawler]]
- 1 edge to [[_COMMUNITY_Narasi Gemini dan Pembandingan_1]]
- 1 edge to [[_COMMUNITY_Encoding dan Penyimpanan Model_2]]
- 1 edge to [[_COMMUNITY_Integrasi X dan Provenans Akuisisi_6]]
- 1 edge to [[_COMMUNITY_Konfigurasi Crawler Universal_1]]

## Top bridge nodes
- [[test_social_archive.py]] - degree 9, connects to 3 communities
- [[social_archive.py]] - degree 18, connects to 2 communities
- [[identity()]] - degree 11, connects to 2 communities
- [[test_dataset_merge.py]] - degree 8, connects to 2 communities
- [[social_identity.py]] - degree 6, connects to 2 communities