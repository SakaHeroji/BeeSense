---
type: community
cohesion: 0.14
members: 18
---

# Pengambilan HTML Reddit

**Cohesion:** 0.14 - loosely connected
**Members:** 18 nodes

## Members
- [[.check_session()]] - code - Crawler/Backend/instagram_crawler.py
- [[.plan()]] - code - Crawler/Backend/instagram_crawler.py
- [[.test_browser_429_passes_retry_after_and_keeps_chrome_open()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_browser_bundle_keeps_backend_provenance_and_fixture_is_not_live()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_browser_is_real_backend_but_injected_workers_remain_synthetic()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_cli_error_never_exposes_auth_redirect_or_input()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_configuration_rejects_secrets_and_invalid_limits()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_document_parser_rejects_unrelated_posts_and_preserves_reply_parent()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_navigation_observes_429_even_when_chrome_throws_before_response()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_timeout_preserves_browser_for_manual_inspection()]] - code - tests/crawler/test_instagram_browser.py
- [[InstagramBrowserTests]] - code - tests/crawler/test_instagram_browser.py
- [[InstagramCrawler]] - code - Crawler/Backend/instagram_crawler.py
- [[Offline checks for the Chrome boundary, native identity, and provenance.]] - rationale - tests/crawler/test_instagram_browser.py
- [[Standalone trial. The production SocialCrawler backend stays unchanged.]] - rationale - Crawler/Backend/instagram_crawler.py
- [[main()_2]] - code - Crawler/Backend/instagram_crawler.py
- [[run_instagram_worker()]] - code - Crawler/Backend/instagram_crawler.py
- [[run_worker()]] - code - Crawler/Backend/Reddit/crawl_reddit_single.py
- [[test_instagram_browser.py]] - code - tests/crawler/test_instagram_browser.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengambilan_HTML_Reddit
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Pengambilan HTML Reddit]]
- 4 edges to [[_COMMUNITY_Pengambilan HTML Reddit_2]]
- 3 edges to [[_COMMUNITY_Pengambilan HTML Reddit_3]]
- 2 edges to [[_COMMUNITY_Riwayat Sesi Instagram]]
- 1 edge to [[_COMMUNITY_Parsing Identitas Reddit]]
- 1 edge to [[_COMMUNITY_Validasi Record Reddit_1]]
- 1 edge to [[_COMMUNITY_Pengambilan HTML Reddit_4]]
- 1 edge to [[_COMMUNITY_Pengujian Client Instagram]]
- 1 edge to [[_COMMUNITY_Model dan Pengujian NLP]]

## Top bridge nodes
- [[InstagramCrawler]] - degree 16, connects to 5 communities
- [[test_instagram_browser.py]] - degree 6, connects to 3 communities
- [[main()_2]] - degree 9, connects to 2 communities
- [[run_worker()]] - degree 3, connects to 2 communities
- [[InstagramBrowserTests]] - degree 11, connects to 1 community