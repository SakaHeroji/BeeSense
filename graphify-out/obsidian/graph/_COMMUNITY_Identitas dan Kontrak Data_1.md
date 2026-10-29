---
type: community
cohesion: 0.29
members: 6
---

# Identitas dan Kontrak Data

**Cohesion:** 0.29 - loosely connected
**Members:** 6 nodes

## Members
- [[.setUp()_5]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_input_integrity_remains_enforced()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_missing_preserved_audit_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_preserved_audit_and_excel_owner_files_are_supported()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[.test_unexpected_workbook_is_rejected()]] - code - tests/nlp/test_dashboard_data_verifier.py
- [[PublishedDataTests]] - code - tests/nlp/test_dashboard_data_verifier.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Identitas_dan_Kontrak_Data
SORT file.name ASC
```
