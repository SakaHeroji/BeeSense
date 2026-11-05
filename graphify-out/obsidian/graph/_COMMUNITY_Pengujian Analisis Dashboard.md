---
type: community
members: 17
---

# Pengujian Analisis Dashboard

**Members:** 17 nodes

## Members
- [[.setUp()_19]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_bar_data_matches_aggregates_and_escapes_topic_hover_text()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_chart_events_ignore_non_topic_points_and_support_cluster_zero()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_conflicting_root_captions_are_not_guessed()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_instagram_is_included_in_coverage_ranking_months_and_graph_hover()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_months_use_root_dates_and_zero_fill_without_losing_microseconds()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_network_positions_stable_and_platform_ratio_is_numeric()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_platform_coverage_includes_noise_and_preserves_zero_platforms()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_snapshot_comparison_uses_published_settings_without_local_environment()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_source_caption_fallback_keeps_titles_and_ignores_unverified_matches()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_tiktok_captions_label_comments_replies_and_separate_native_posts()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_tiktok_counts_noise_months_and_network_include_all_records()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_topic_counts_keep_occurrences_unique_sentences_and_comments_separate()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_topic_evidence_profile_deduplicates_units_and_matches_whole_terms()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_topic_profile_marks_context_fallback_without_inventing_native_ids()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_twitter_counts_months_and_network_include_all_records()]] - code - tests/nlp/test_dashboard_analysis.py
- [[AnalysisTests]] - code - tests/nlp/test_dashboard_analysis.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Analisis_Dashboard
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_app.py]]
- 1 edge to [[_COMMUNITY_Render Dashboard Streamlit]]

## Top bridge nodes
- [[AnalysisTests]] - degree 18, connects to 2 communities