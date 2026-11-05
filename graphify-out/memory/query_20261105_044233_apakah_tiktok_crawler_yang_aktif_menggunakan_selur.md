---
type: "query"
date: "2026-11-05T04:42:33.988547+00:00"
question: "apakah tiktok crawler yang aktif menggunakan seluruh keyword di konfigurasi yang ada?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialCrawler", "NativeTikTokClient", "ChromeLiveWorker"]
---

# Q: apakah tiktok crawler yang aktif menggunakan seluruh keyword di konfigurasi yang ada?

## Answer

Expanded from original query via vocab: [tiktok, configuration, query, keyword, include, exclude, search]. Graph traversal identifies SocialCrawler, NativeTikTokClient and ChromeLiveWorker. Verified live task and configuration: all 25 root queries are inherited and queued; include_keywords kuliah/kampus/universitas/beasiswa/jurusan use include_mode any, all 40 exclude phrases apply to root posts. comment_exclude_keywords is empty, so comments and replies do not need matching keywords. All query entries being queued does not mean they have already executed: sequential scheduling finishes discovered post threads before proceeding and may stop at target or three-hour deadline. Active 2026-11-05 run 6cd0ad73 remains ongoing; observed counts are not a success claim.

## Outcome

- Signal: useful

## Source Nodes

- SocialCrawler
- NativeTikTokClient
- ChromeLiveWorker