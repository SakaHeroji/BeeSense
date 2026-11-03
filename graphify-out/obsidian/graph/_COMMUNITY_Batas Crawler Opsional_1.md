---
type: community
cohesion: 0.13
members: 19
---

# Batas Crawler Opsional

**Cohesion:** 0.13 - loosely connected
**Members:** 19 nodes

## Members
- [[.check_session()]] - code - Crawler/Backend/instagram_crawler.py
- [[.plan()_3]] - code - Crawler/Backend/instagram_crawler.py
- [[.test_browser_429_passes_retry_after_and_keeps_chrome_open()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_browser_bundle_keeps_backend_provenance_and_fixture_is_not_live()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_browser_is_real_backend_but_injected_workers_remain_synthetic()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_cli_error_never_exposes_auth_redirect_or_input()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_configuration_rejects_secrets_and_invalid_limits()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_document_parser_rejects_unrelated_posts_and_preserves_reply_parent()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_navigation_observes_429_even_when_chrome_throws_before_response()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_repeated_cli_error_preserves_browser_without_claiming_access_barrier()]] - code - tests/crawler/test_instagram_browser.py
- [[.test_timeout_preserves_browser_for_manual_inspection()]] - code - tests/crawler/test_instagram_browser.py
- [[InstagramBrowserTests]] - code - tests/crawler/test_instagram_browser.py
- [[InstagramCrawler]] - code - Crawler/Backend/instagram_crawler.py
- [[Offline checks for the Chrome boundary, native identity, and provenance.]] - rationale - tests/crawler/test_instagram_browser.py
- [[SocialExportMixin_3]] - code
- [[Standalone trial. The production SocialCrawler backend stays unchanged.]] - rationale - Crawler/Backend/instagram_crawler.py
- [[main()_15]] - code - Crawler/Backend/instagram_crawler.py
- [[run_instagram_worker()]] - code - Crawler/Backend/instagram_crawler.py
- [[test_instagram_browser.py]] - code - tests/crawler/test_instagram_browser.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Batas_Crawler_Opsional
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Batas Crawler Opsional]]
- 7 edges to [[_COMMUNITY_Konfigurasi Crawler Universal]]
- 1 edge to [[_COMMUNITY_Batas Crawler Opsional_2]]
- 1 edge to [[_COMMUNITY_Pengujian Client Instagram_1]]

## Top bridge nodes
- [[test_instagram_browser.py]] - degree 8, connects to 4 communities
- [[InstagramCrawler]] - degree 16, connects to 2 communities
- [[main()_15]] - degree 8, connects to 1 community
- [[.test_browser_bundle_keeps_backend_provenance_and_fixture_is_not_live()]] - degree 3, connects to 1 community
- [[.test_browser_is_real_backend_but_injected_workers_remain_synthetic()]] - degree 3, connects to 1 community