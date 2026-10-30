---
type: community
members: 40
---

# Pengujian Koordinator Crawler

**Members:** 40 nodes

## Members
- [[.crawler()_1]] - code - tests/crawler/test_social_crawler.py
- [[.read()]] - code - tests/crawler/test_social_crawler.py
- [[.test_barrier_stops_platform_and_keeps_partial_bundle()]] - code - tests/crawler/test_social_crawler.py
- [[.test_browser_navigation_error_checks_current_page_and_stops_on_429()]] - code - tests/crawler/test_social_crawler.py
- [[.test_candidate_cap_and_post_cap_are_independent_when_minimum_fits()]] - code - tests/crawler/test_social_crawler.py
- [[.test_checkpoint_dom_import_does_not_make_network_calls()]] - code - tests/crawler/test_social_crawler.py
- [[.test_combined_bundle_uses_original_contract_and_separate_platform_minimums()]] - code - tests/crawler/test_social_crawler.py
- [[.test_comment_exclusion_preserves_child_with_unresolved_parent_and_context_comments()]] - code - tests/crawler/test_social_crawler.py
- [[.test_compact_long_unicode_text_is_marked_and_formula_text_stays_literal()]] - code - tests/crawler/test_social_crawler.py
- [[.test_compact_reexport_refilters_saved_data_and_keeps_source_unchanged()]] - code - tests/crawler/test_social_crawler.py
- [[.test_date_window_is_inclusive_start_exclusive_end_and_unknown_is_excluded()]] - code - tests/crawler/test_social_crawler.py
- [[.test_delay_cannot_start_another_request_after_global_budget()]] - code - tests/crawler/test_social_crawler.py
- [[.test_discovery_refills_after_a_filtered_candidate_without_repeating_urls()]] - code - tests/crawler/test_social_crawler.py
- [[.test_historical_posts_are_skipped_before_requests_and_ids_are_canonical()]] - code - tests/crawler/test_social_crawler.py
- [[.test_include_all_across_title_and_description_and_exclude_wins()]] - code - tests/crawler/test_social_crawler.py
- [[.test_interrupt_during_delay_publishes_already_captured_evidence()]] - code - tests/crawler/test_social_crawler.py
- [[.test_invalid_native_identity_does_not_become_a_success()]] - code - tests/crawler/test_social_crawler.py
- [[.test_manual_captcha_wait_only_observes_and_obeys_global_deadline()]] - code - tests/crawler/test_social_crawler.py
- [[.test_minimum_counts_only_roots_with_enough_unique_comments()]] - code - tests/crawler/test_social_crawler.py
- [[.test_minimum_shortage_is_reported_at_hard_post_cap()]] - code - tests/crawler/test_social_crawler.py
- [[.test_original_youtube_process_worker_boundary_works_as_package_import()]] - code - tests/crawler/test_social_crawler.py
- [[.test_partial_metadata_survives_a_worker_timeout()]] - code - tests/crawler/test_social_crawler.py
- [[.test_random_and_fixed_delays_are_between_operations()]] - code - tests/crawler/test_social_crawler.py
- [[.test_reddit_cooldown_honors_longer_server_wait_and_retry_cap()]] - code - tests/crawler/test_social_crawler.py
- [[.test_reddit_cooldown_leaves_youtube_runnable_and_retries_same_thread()]] - code - tests/crawler/test_social_crawler.py
- [[.test_reddit_cooldown_never_waits_or_retries_beyond_global_deadline()]] - code - tests/crawler/test_social_crawler.py
- [[.test_reddit_cooldown_retries_failed_search_without_losing_query()]] - code - tests/crawler/test_social_crawler.py
- [[.test_redirect_to_historical_root_is_not_exported()]] - code - tests/crawler/test_social_crawler.py
- [[.test_round_robin_gives_both_platforms_turns_and_shares_deadline()]] - code - tests/crawler/test_social_crawler.py
- [[.test_single_sheet_compact_export_repeats_root_date_and_keeps_audit_dates()]] - code - tests/crawler/test_social_crawler.py
- [[.test_source_exception_is_sanitized_and_stops_after_three_calls()]] - code - tests/crawler/test_social_crawler.py
- [[.test_topic_exclusions_remove_roots_and_comments_without_excluding_normal_diplomas()]] - code - tests/crawler/test_social_crawler.py
- [[.test_unrepresentable_server_cooldown_preserves_partial_bundle()]] - code - tests/crawler/test_social_crawler.py
- [[.youtube_worker()]] - code - tests/crawler/test_social_crawler_reddrix.py
- [[SocialCrawlerTests]] - code - tests/crawler/test_social_crawler.py
- [[rd_events()]] - code - tests/crawler/test_social_crawler.py
- [[receipt()]] - code - tests/crawler/test_social_crawler.py
- [[spawn_youtube_fixture()]] - code - tests/crawler/test_social_crawler.py
- [[test_social_crawler.py]] - code - tests/crawler/test_social_crawler.py
- [[yt_events()]] - code - tests/crawler/test_social_crawler.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Koordinator_Crawler
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_Koordinator Backend Sosial]]
- 4 edges to [[_COMMUNITY_Worker Reddrix]]
- 2 edges to [[_COMMUNITY_Wrapper RedditCrawler]]
- 1 edge to [[_COMMUNITY_Capture Reddit Playwright]]
- 1 edge to [[_COMMUNITY_Pengujian Client Instagram]]
- 1 edge to [[_COMMUNITY_Crawler Selenium]]
- 1 edge to [[_COMMUNITY_Pengujian Integrasi Reddrix]]

## Top bridge nodes
- [[receipt()]] - degree 25, connects to 4 communities
- [[.crawler()_1]] - degree 32, connects to 2 communities
- [[yt_events()]] - degree 18, connects to 2 communities
- [[test_social_crawler.py]] - degree 10, connects to 2 communities
- [[SocialCrawlerTests]] - degree 42, connects to 1 community