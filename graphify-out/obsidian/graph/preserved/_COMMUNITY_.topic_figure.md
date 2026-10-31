---
type: community
members: 10
---

# .topic_figure

**Members:** 10 nodes

## Members
- [[._date_label()]] - code - Dashboard/app.py
- [[._sidebar()]] - code - Dashboard/app.py
- [[.filter_occurrences()]] - code - Dashboard/app.py
- [[.test_filters_are_literal_and_respect_platform_dates()]] - code - tests/nlp/test_social_nlp.py
- [[.test_topic_graph_is_bounded_and_noise_is_not_a_topic()]] - code - tests/nlp/test_social_nlp.py
- [[.topic_figure()]] - code - Dashboard/app.py
- [[Bounded topic graph volume from filtered rows, semantic edges from the full mod]] - rationale - Dashboard/app.py
- [[DashboardTests]] - code - tests/nlp/test_social_nlp.py
- [[Keep the full-model layout stable while volume and edge filters change.]] - rationale - Dashboard/app.py
- [[_graph_positions()]] - code - Dashboard/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/topic_figure
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_thread_url]]
- 2 edges to [[_COMMUNITY_.render]]
- 2 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 1 edge to [[_COMMUNITY_app.py]]
- 1 edge to [[_COMMUNITY_Render Dashboard Streamlit]]

## Top bridge nodes
- [[.topic_figure()]] - degree 6, connects to 3 communities
- [[._sidebar()]] - degree 3, connects to 2 communities
- [[DashboardTests]] - degree 4, connects to 1 community
- [[_graph_positions()]] - degree 3, connects to 1 community
- [[.filter_occurrences()]] - degree 3, connects to 1 community