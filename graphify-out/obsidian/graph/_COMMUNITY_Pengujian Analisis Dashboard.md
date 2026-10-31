---
type: community
cohesion: 0.17
members: 12
---

# Pengujian Analisis Dashboard

**Cohesion:** 0.17 - loosely connected
**Members:** 12 nodes

## Members
- [[.setUp()_9]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_bar_data_matches_aggregates_and_escapes_topic_hover_text()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_chart_events_ignore_non_topic_points_and_support_cluster_zero()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_indonesian_numbers_dates_and_empty_aggregates()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_instagram_is_included_in_coverage_ranking_months_and_graph_hover()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_months_use_root_dates_and_zero_fill_without_losing_microseconds()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_network_positions_stable_and_platform_ratio_is_numeric()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_platform_coverage_includes_noise_and_preserves_zero_platforms()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_topic_counts_keep_occurrences_unique_sentences_and_comments_separate()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_topic_evidence_profile_deduplicates_units_and_matches_whole_terms()]] - code - tests/nlp/test_dashboard_analysis.py
- [[.test_topic_profile_marks_context_fallback_without_inventing_native_ids()]] - code - tests/nlp/test_dashboard_analysis.py
- [[AnalysisTests]] - code - tests/nlp/test_dashboard_analysis.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Pengujian_Analisis_Dashboard
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Render Dashboard Streamlit]]
- 1 edge to [[_COMMUNITY_Penjelasan Topik Dashboard]]
- 1 edge to [[_COMMUNITY_app.py]]

## Top bridge nodes
- [[.test_indonesian_numbers_dates_and_empty_aggregates()]] - degree 3, connects to 2 communities
- [[AnalysisTests]] - degree 12, connects to 1 community