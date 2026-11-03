---
type: "query"
date: "2026-11-03T05:43:19.492655+00:00"
question: "tombol statistik dan migrasi postgresqlnya gak kelihatan seperti tombol. perbaiki\nrapikan tabel hasil crawlingnya, masih kurang rapi"
contributor: "graphify"
outcome: "useful"
source_nodes: ["PlatformResults()", "JobStatistics()", "Tabel hasil tujuh kolom tetap dengan angka rata kanan tabular"]
---

# Q: tombol statistik dan migrasi postgresqlnya gak kelihatan seperti tombol. perbaiki
rapikan tabel hasil crawlingnya, masih kurang rapi

## Answer

Query vocabulary: [platformresults jobstatistics button statistik migrasi frontend transactionmigration]. Statistics is now a bordered chart-icon navigation button; migration is orange with a database icon. Results table has seven fixed-proportion columns, right-aligned tabular counts, separate comments/replies, two-line name/time, intact storage labels, and a consistent action grid. Fixed a global CSS specificity conflict that compressed mobile columns; table now remains 1120px wide in its own keyboard-focusable scroller. Buttons are nominally 44px high with 14px text and nowrap labels. 38 Vitest + 1 Node, lint/typecheck/API/demo builds/format pass; desktop and actual mobile 433px verified. No backend/database change. Graph raw targeted extraction has 42 unresolved references; prior full-pass limitations remain documented. Obsidian and HTML updated.

## Outcome

- Signal: useful

## Source Nodes

- PlatformResults()
- JobStatistics()
- Tabel hasil tujuh kolom tetap dengan angka rata kanan tabular