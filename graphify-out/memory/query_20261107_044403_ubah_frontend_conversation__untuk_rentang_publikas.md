---
type: "query"
date: "2026-11-07T04:44:03.842369+00:00"
question: "ubah frontend Conversation. Untuk rentang publikasi tanggal harusnya ada di transaksi crawlingnya. perbaiki"
contributor: "graphify"
outcome: "useful"
source_nodes: ["Conversation", "Config", "PlatformWorkspace.tsx", "ParallelWorkspace.tsx", "ConversationWorkspace.tsx"]
---

# Q: ubah frontend Conversation. Untuk rentang publikasi tanggal harusnya ada di transaksi crawlingnya. perbaiki

## Answer

Expanded from original query via graph vocabulary: [conversation, config, crawl, crawler, date, parallel, platform, publication, review, snapshot, transaction, until]. Conversation no longer owns since/until. Config owns the publication range per crawling transaction; PlatformWorkspace and ParallelWorkspace render and validate those fields, while applyConversation preserves transaction dates and removes legacy dates from the frozen Conversation snapshot. Documentation and tests record the same boundary.

## Outcome

- Signal: useful

## Source Nodes

- Conversation
- Config
- PlatformWorkspace.tsx
- ParallelWorkspace.tsx
- ConversationWorkspace.tsx