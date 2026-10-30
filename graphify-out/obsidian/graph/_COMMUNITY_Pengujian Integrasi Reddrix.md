---
type: community
members: 8
---

# Pengujian Integrasi Reddrix

**Members:** 8 nodes

## Members
- [[.crawler()_2]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_invalid_display_and_checkpoint_mix_fail_before_acquisition()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_missing_reddrix_exports_partial_and_keeps_youtube_running()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_mixed_baseline_skips_both_platforms_before_worker_requests()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_mixed_default_workers_publish_one_bundle_with_correct_provenance()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_reddrix_retry_uses_coordinator_cooldown_and_same_worker()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[.test_spawned_worker_imports_shared_implementation_without_live_access()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[SocialCrawlerReddrixTests]] - code - tests/crawler/test_social_crawler_reddrix.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Integrasi_Reddrix
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Koordinator Backend Sosial]]
- 5 edges to [[_COMMUNITY_Worker Reddrix]]
- 1 edge to [[_COMMUNITY_Wrapper RedditCrawler]]
- 1 edge to [[_COMMUNITY_Runtime Docker dan Display]]
- 1 edge to [[_COMMUNITY_Pengujian Koordinator Crawler]]

## Top bridge nodes
- [[SocialCrawlerReddrixTests]] - degree 16, connects to 5 communities
- [[.test_missing_reddrix_exports_partial_and_keeps_youtube_running()]] - degree 4, connects to 2 communities
- [[.crawler()_2]] - degree 7, connects to 1 community
- [[.test_mixed_default_workers_publish_one_bundle_with_correct_provenance()]] - degree 3, connects to 1 community
- [[.test_spawned_worker_imports_shared_implementation_without_live_access()]] - degree 3, connects to 1 community