---
type: "query"
date: "2026-11-03T03:28:40.686169+00:00"
question: "Buat seluruh konfigurasi crawler minimal 1000 post tanpa batas jam dan daily request limit, seluruh komentar diambil semua"
contributor: "graphify"
outcome: "useful"
source_nodes: ["SocialCrawler", "configure_daily_quotas", "InstaloaderAdapter", "SocialCrawlerSelenium"]
---

# Q: Buat seluruh konfigurasi crawler minimal 1000 post tanpa batas jam dan daily request limit, seluruh komentar diambil semua

## Answer

Expanded via graph vocabulary: crawler, config, limit, request, daily, comment, replies, posts, target, duration, budget, pagination. Implemented SocialCrawler 1.9.0 defaults in config/social_crawler.json: four platforms enabled; min_posts 1000 each, min_comments_per_post 0, total_seconds null, nullable post/candidate/comment/reply/search/thread caps, Scweet daily request and tweet quota null. crawler_limits handles nullable counts and deadlines with JSON progress remaining_seconds null. Independent comment_exclude_keywords [] preserves all comment context while root filters remain. Scweet account repository quota predicates are optional without resetting counters or bypassing auth, leases or cooldowns. Instaloader paginates answers beyond previews; yt-dlp receives empty caps and Scweet replies limit None. Selenium projects the same universal config to supported YouTube/Reddit. Coverage still depends on source access and exhaustion. No live crawling started. 189 crawler tests ran: 188 passed and one optional browser skipped; 29 Reddit self-tests, 12 Reddit runner tests and 10 JS parser tests passed. Existing snapshot verified. No database migration required. Docker daemon unavailable. Graph update healthy with 1994 nodes and 4287 edges.

## Outcome

- Signal: useful

## Source Nodes

- SocialCrawler
- configure_daily_quotas
- InstaloaderAdapter
- SocialCrawlerSelenium