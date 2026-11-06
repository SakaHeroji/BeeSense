---
type: community
cohesion: 0.20
members: 10
---

# Batas Crawler Opsional

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
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

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Batas_Crawler_Opsional
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Konfigurasi Crawler Universal]]
- 3 edges to [[_COMMUNITY_Batas Crawler Opsional]]

## Top bridge nodes
- [[InstagramBrowserTests]] - degree 11, connects to 2 communities
- [[.test_browser_bundle_keeps_backend_provenance_and_fixture_is_not_live()]] - degree 3, connects to 2 communities
- [[.test_browser_is_real_backend_but_injected_workers_remain_synthetic()]] - degree 3, connects to 2 communities