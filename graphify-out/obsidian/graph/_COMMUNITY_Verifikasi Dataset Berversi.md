---
type: community
cohesion: 0.22
members: 9
---

# Verifikasi Dataset Berversi

**Cohesion:** 0.22 - loosely connected
**Members:** 9 nodes

## Members
- [[.setUp()_3]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_archived_nlp_snapshot_and_separate_crawl_output_are_supported()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_input_integrity_remains_enforced()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_missing_preserved_audit_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_preserved_audit_and_excel_owner_files_are_supported()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_unexpected_file_in_archive_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_unexpected_workbook_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[PublishedDataTests]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[test_dashboard_data_verifier.py]] - code - tests/nlp/test_dashboard_data_verifier.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Verifikasi_Dataset_Berversi
SORT file.name ASC
```
