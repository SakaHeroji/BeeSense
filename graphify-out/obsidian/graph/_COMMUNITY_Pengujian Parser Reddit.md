---
type: community
cohesion: 0.25
members: 22
---

# Pengujian Parser Reddit

**Cohesion:** 0.25 - loosely connected
**Members:** 22 nodes

## Members
- [[.discover()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.fullname()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.has_class()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.own_body()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.parent()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_01_shreddit_extracts_body_not_buttons_or_templates()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_02_old_nested_comments_do_not_merge_text_or_guess_role()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_03_relative_date_only_and_exact_are_distinct()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_04_deleted_and_truncated_are_not_full_original_text()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_05_http_200_javascript_challenge_not_empty_comments()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_06_block_login_and_legitimate_quoted_error()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_07_wrong_thread_is_rejected_not_relabelled()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_09_search_uses_recognized_cards_not_sidebar_links()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_10_reply_cap_includes_nested_replies_and_preserves_roots()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.test_11_missing_parent_remains_unknown()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[.thread()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[RedditHtmlParser]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[RedditTests]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[Whole-post comment budget includes replies; nested replies share thread cap.]] - rationale - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[bounded_events()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[fixture_page()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[worker()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Parser_Reddit
SORT file.name ASC
```

## Connections to other communities
- 17 edges to [[_COMMUNITY_Parsing Identitas Reddit]]
- 9 edges to [[_COMMUNITY_Pengujian Integrasi Reddrix]]
- 8 edges to [[_COMMUNITY_Validasi Record Reddit]]
- 5 edges to [[_COMMUNITY_Validasi Record Reddit_1]]
- 3 edges to [[_COMMUNITY_Kontrak Record Reddit_1]]
- 2 edges to [[_COMMUNITY_Worker Reddrix]]
- 1 edge to [[_COMMUNITY_Kontrak Record Reddit]]

## Top bridge nodes
- [[RedditTests]] - degree 20, connects to 6 communities
- [[.thread()]] - degree 22, connects to 4 communities
- [[fixture_page()]] - degree 15, connects to 4 communities
- [[worker()]] - degree 10, connects to 3 communities
- [[RedditHtmlParser]] - degree 20, connects to 2 communities