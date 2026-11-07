---
type: "query"
date: "2026-11-07T04:01:59.001239+00:00"
question: "Update frontend crawler menjadi Conversation-first, pisahkan tabel dan form, dukung Gemini dari judul, prompt Markdown, import Excel, parallel/single selection, dan ekspor Obsidian"
contributor: "graphify"
outcome: "useful"
source_nodes: ["crawler_frontend_src_features_conversationworkspace_conversationworkspace", "crawler_frontend_src_shared_conversation_workbook", "crawler_frontend_readme_local_excel_conversation_exchange", "crawler_frontend_docs_api_contract_local_excel_browser_contract", "prd_prd_frontend_prd_frontend_crawler_conversation_first_product_model"]
---

# Q: Update frontend crawler menjadi Conversation-first, pisahkan tabel dan form, dukung Gemini dari judul, prompt Markdown, import Excel, parallel/single selection, dan ekspor Obsidian

## Answer

Frontend memakai Conversation berversi sebagai konteks riset terpisah dari operasi crawling. ConversationWorkspace menampilkan tabel dan form pada view berbeda; generator HTTP hanya menerima title. conversation-workbook.ts membuat prompt Markdown dan memvalidasi workbook tiga sheet secara lokal sebelum menyimpan origin excel. ParallelWorkspace dan setiap PlatformWorkspace memilih satu ConversationSnapshot yang dibekukan. Graphify incremental dan vault Obsidian diperbarui.

## Outcome

- Signal: useful

## Source Nodes

- crawler_frontend_src_features_conversationworkspace_conversationworkspace
- crawler_frontend_src_shared_conversation_workbook
- crawler_frontend_readme_local_excel_conversation_exchange
- crawler_frontend_docs_api_contract_local_excel_browser_contract
- prd_prd_frontend_prd_frontend_crawler_conversation_first_product_model