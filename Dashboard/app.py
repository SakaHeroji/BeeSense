"""Streamlit entry point for local and Community Cloud dashboards.

Training lives in SocialNLPClusterer; this app reads saved artifacts.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from datetime import datetime
from functools import partial
from hashlib import sha256
from pathlib import Path
from textwrap import wrap

import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from babel.dates import format_date, format_datetime
from babel.numbers import format_decimal, format_percent

from MachineLearning.social_nlp import ROOT, SocialNLPClusterer, file_hash

PALETTE = {
    "ink": "#172D43",
    "teal": "#116D78",
    "youtube": "#C64D36",
    "reddit": "#3568B3",
    "instagram": "#A93A82",
    "paper": "#FFFFFF",
    "line": "#DCE5EE",
    "muted": "#52657B",
    "noise": "#D3DBE5",
}
VIEWS = [
    "Ringkasan",
    "Peta topik",
    "Penjelasan topik",
    "Kalimat & sumber",
    "Metode & data",
]
PLATFORM_LABELS = {"youtube": "YouTube", "reddit": "Reddit", "instagram": "Instagram"}


def number(value):
    return format_decimal(int(value), locale="id_ID")


def percent(value):
    return format_percent(float(value), format="0.0%", locale="id_ID")


@st.cache_data(show_spinner=False)
def _graph_positions(ids, edges):
    """Keep the full-model layout stable while volume and edge filters change."""
    network = nx.Graph()
    network.add_nodes_from(ids)
    for edge in edges:
        a, b = int(edge["source"]), int(edge["target"])
        if a in network and b in network:
            network.add_edge(a, b, weight=edge["similarity"])
    connected = [cid for cid in ids if network.degree(cid)]
    isolated = [cid for cid in ids if not network.degree(cid)]
    positions = (
        nx.spring_layout(
            network.subgraph(connected),
            seed=42,
            weight="weight",
            k=2 / np.sqrt(len(connected)),
            iterations=180,
        )
        if connected
        else {}
    )
    for i, cid in enumerate(isolated):
        angle = 2 * np.pi * i / len(isolated)
        positions[cid] = (1.35 if connected else 1) * np.array(
            [np.cos(angle), np.sin(angle)]
        )
    # Plotly markers have a screen-space radius. Keep nearby labels apart
    # without recomputing a different semantic layout for each filter.
    if 1 < len(ids) <= 200:
        coordinates = np.array([positions[cid] for cid in ids])
        for _ in range(100):
            delta = coordinates[:, None, :] - coordinates[None, :, :]
            distances = np.linalg.norm(delta, axis=2)
            np.fill_diagonal(distances, np.inf)
            overlaps = np.maximum(0.30 - distances, 0)
            if overlaps.max() < 0.001:
                break
            shift = (
                delta / np.maximum(distances[:, :, None], 1e-8) * overlaps[:, :, None]
            ).sum(axis=1)
            coordinates += (
                0.55 * shift / np.maximum((overlaps > 0).sum(axis=1, keepdims=True), 1)
            )
        positions = dict(zip(ids, coordinates))
    return positions


@st.cache_resource(show_spinner="Membaca hasil clustering…")
def _load_artifacts(path, manifest_version):
    # Includes immutable manifest identity used by the explanation export.
    data = SocialNLPClusterer.load_run(path, verify=True)
    return data


@st.cache_data(show_spinner="Menyusun penjelasan topik…", max_entries=16)
def _explain_filtered(cache_key, start, end, options_json, _data, _frame):
    return SocialNLPClusterer.explain_artifacts(
        _data, _frame, date_start=start, date_end=end, options=json.loads(options_json)
    )


class SocialNLPStreamlitApp:
    """Read-only exploration of completed NLP runs; no training on page reruns."""

    def __init__(self, run_dir=None):
        config = json.loads((ROOT / "config/social_nlp.json").read_text())
        directory = Path(
            run_dir or os.environ.get("BEESENSE_NLP_RUN_DIR") or config["output_dir"]
        )
        self.run_dir = directory if directory.is_absolute() else ROOT / directory

    @staticmethod
    def filter_occurrences(
        frame, platforms, start=None, end=None, query="", cluster_id=None
    ):
        selected = frame[frame["platform"].isin(platforms)].copy()
        dates = pd.to_datetime(
            selected["post_date"], errors="coerce", format="mixed"
        ).dt.date
        if start is not None:
            selected = selected[dates >= start]
        if end is not None:
            selected = selected[
                pd.to_datetime(
                    selected["post_date"], errors="coerce", format="mixed"
                ).dt.date
                <= end
            ]
        if query:
            selected = selected[
                selected["sentence"].str.contains(
                    query, case=False, regex=False, na=False
                )
            ]
        if cluster_id is not None:
            selected = selected[selected["cluster_id"] == cluster_id]
        return selected

    @staticmethod
    def topic_figure(
        topics, graph, occurrences, threshold, max_nodes=120, selected=None
    ):
        """Bounded topic graph: volume from filtered rows, semantic edges from the full model."""
        counts = (
            occurrences[occurrences["cluster_id"] >= 0]
            .groupby("cluster_id")
            .size()
            .to_dict()
        )
        visible = sorted(counts, key=lambda key: (-counts[key], key))[:max_nodes]
        by_id = {topic["cluster_id"]: topic for topic in topics}
        if selected in counts and selected not in visible:
            visible[-1:] = [selected]
        network = nx.Graph()
        network.add_nodes_from(visible)
        for edge in graph["edges"]:
            a, b = int(edge["source"]), int(edge["target"])
            if a in visible and b in visible and edge["similarity"] >= threshold:
                network.add_edge(a, b, weight=edge["similarity"])
        positions = _graph_positions(
            tuple(topic["cluster_id"] for topic in topics), graph["edges"]
        )
        edge_x, edge_y = [], []
        for a, b in network.edges:
            edge_x.extend([float(positions[a][0]), float(positions[b][0]), None])
            edge_y.extend([float(positions[a][1]), float(positions[b][1]), None])
        traces = [
            go.Scatter(
                x=edge_x,
                y=edge_y,
                mode="lines",
                line={"width": 1.0, "color": "#9CB8C7"},
                hoverinfo="skip",
                showlegend=False,
            )
        ]
        hover, colors, sizes, labels = [], [], [], []
        platform_counts = (
            occurrences.groupby(["cluster_id", "platform"]).size().to_dict()
        )
        three_platforms = bool((occurrences.platform == "instagram").any())
        largest = max(counts.values(), default=1)
        for cid in visible:
            youtube = platform_counts.get((cid, "youtube"), 0)
            reddit = platform_counts.get((cid, "reddit"), 0)
            instagram = platform_counts.get((cid, "instagram"), 0)
            dominant = max(
                PLATFORM_LABELS, key=lambda p: platform_counts.get((cid, p), 0)
            )
            colors.append(
                {"reddit": 0, "youtube": 1, "instagram": 2}[dominant]
                if three_platforms
                else youtube / max(1, youtube + reddit)
            )
            sizes.append(22 + 32 * np.sqrt(counts[cid] / largest))
            label = by_id[cid]["label"]
            labels.append(f"T{cid + 1:02d}")
            hover.append(
                f"<b>T{cid + 1:02d} · {html.escape(label)}</b><br>{number(counts[cid])} kemunculan kalimat<br>"
                f"YouTube {number(youtube)} / Reddit {number(reddit)} / Instagram {number(instagram)}<br>Klik untuk menelusuri topik"
            )
        traces.append(
            go.Scatter(
                x=[float(positions[cid][0]) for cid in visible],
                y=[float(positions[cid][1]) for cid in visible],
                mode="markers+text",
                text=labels,
                textposition="middle center",
                textfont={"size": 10, "color": "white"},
                marker={
                    "size": sizes,
                    "color": colors,
                    **(
                        {
                            "cmin": -0.5,
                            "cmax": 2.5,
                            "colorscale": [
                                [0, PALETTE["reddit"]],
                                [1 / 3, PALETTE["reddit"]],
                                [1 / 3, PALETTE["youtube"]],
                                [2 / 3, PALETTE["youtube"]],
                                [2 / 3, PALETTE["instagram"]],
                                [1, PALETTE["instagram"]],
                            ],
                            "colorbar": {
                                "title": {"text": "Platform terbanyak"},
                                "tickvals": [0, 1, 2],
                                "ticktext": ["Reddit", "YouTube", "Instagram"],
                                "len": 0.55,
                                "thickness": 10,
                            },
                        }
                        if three_platforms
                        else {
                            "cmin": 0,
                            "cmax": 1,
                            "colorscale": [
                                [0, PALETTE["reddit"]],
                                [0.5, PALETTE["teal"]],
                                [1, PALETTE["youtube"]],
                            ],
                            "colorbar": {
                                "title": {"text": "Asal kalimat"},
                                "tickvals": [0, 0.5, 1],
                                "ticktext": ["Reddit", "Seimbang", "YouTube"],
                                "len": 0.55,
                                "thickness": 10,
                            },
                        }
                    ),
                    "line": {
                        "color": [
                            PALETTE["ink"] if cid == selected else "white"
                            for cid in visible
                        ],
                        "width": [3 if cid == selected else 1.8 for cid in visible],
                    },
                    "opacity": 1,
                },
                customdata=[[int(cid)] for cid in visible],
                hovertext=hover,
                hoverinfo="text",
                showlegend=False,
            )
        )
        figure = go.Figure(traces)
        figure.update_layout(
            height=380 if len(visible) <= 4 else 560,
            margin={"l": 15, "r": 25, "t": 25, "b": 15},
            paper_bgcolor=PALETTE["paper"],
            plot_bgcolor=PALETTE["paper"],
            xaxis={"visible": False},
            yaxis={"visible": False, "scaleanchor": "x", "scaleratio": 1},
            dragmode="pan",
            clickmode="event+select",
            font={"family": "Trebuchet MS, Arial, sans-serif", "color": PALETTE["ink"]},
            uirevision="topic-map",
        )
        return figure, {
            "nodes": len(visible),
            "edges": network.number_of_edges(),
            "available_topics": len(counts),
        }

    @staticmethod
    def sentence_figure(sentences, embeddings, occurrences, cluster_id, limit=100):
        from sklearn.neighbors import NearestNeighbors

        selected = sentences[
            (sentences["cluster_id"] == cluster_id)
            & sentences["sentence_id"].isin(occurrences["sentence_id"])
        ]
        selected = selected.sort_values("centroid_similarity", ascending=False).head(
            limit
        )
        indices = selected.index.to_numpy()
        network = nx.Graph()
        network.add_nodes_from(range(len(indices)))
        if len(indices) > 1:
            neighbors = NearestNeighbors(
                n_neighbors=min(4, len(indices)), metric="cosine"
            ).fit(embeddings[indices])
            distances, positions = neighbors.kneighbors(embeddings[indices])
            for i in range(len(indices)):
                for distance, j in zip(distances[i], positions[i]):
                    if i != j and 1 - distance >= 0.60:
                        network.add_edge(i, int(j), weight=float(1 - distance))
        layout = (
            nx.spring_layout(network, seed=42, weight="weight", iterations=70)
            if len(indices)
            else {}
        )
        xs, ys = [], []
        for a, b in network.edges:
            xs.extend([layout[a][0], layout[b][0], None])
            ys.extend([layout[a][1], layout[b][1], None])
        figure = go.Figure(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                line={"width": 0.6, "color": "#BDD3DB"},
                hoverinfo="skip",
            )
        )
        figure.add_trace(
            go.Scatter(
                x=[layout[i][0] for i in network],
                y=[layout[i][1] for i in network],
                mode="markers",
                marker={
                    "size": 9,
                    "color": PALETTE["teal"],
                    "line": {"color": "white", "width": 1},
                },
                text=[
                    html.escape(str(selected.iloc[i]["sentence"])[:300])
                    for i in network
                ],
                hoverinfo="text",
            )
        )
        figure.update_layout(
            height=390,
            showlegend=False,
            margin={"l": 10, "r": 10, "t": 10, "b": 10},
            xaxis={"visible": False},
            yaxis={"visible": False},
            paper_bgcolor=PALETTE["paper"],
            plot_bgcolor=PALETTE["paper"],
        )
        return figure

    @staticmethod
    def _date_label(row):
        stamp = row["content_date"]
        if not isinstance(stamp, str) or not stamp:
            return "Tidak diketahui"
        if row["content_date_accuracy"] == "perkiraan":
            return stamp[:10] + " (perkiraan)"
        return stamp[:16].replace("T", " ")

    @staticmethod
    def topic_summary(topics, occurrences):
        """Count sentence occurrences; never confuse them with distinct comments."""
        labels = {t["cluster_id"]: t["label"] for t in topics}
        rows = []
        for cid, group in occurrences[occurrences.cluster_id >= 0].groupby(
            "cluster_id"
        ):
            rows.append(
                {
                    "cluster_id": int(cid),
                    "code": f"T{cid + 1:02d}",
                    "label": labels[cid],
                    "total": len(group),
                    "unique": group.sentence_id.nunique(),
                    "comments": group.source_row.nunique(),
                    "youtube": int((group.platform == "youtube").sum()),
                    "reddit": int((group.platform == "reddit").sum()),
                    "instagram": int((group.platform == "instagram").sum()),
                    "share": len(group) / len(occurrences),
                }
            )
        return (
            pd.DataFrame(
                rows,
                columns=[
                    "cluster_id",
                    "code",
                    "label",
                    "total",
                    "unique",
                    "comments",
                    "youtube",
                    "reddit",
                    "instagram",
                    "share",
                ],
            )
            .sort_values(["total", "cluster_id"], ascending=[False, True])
            .reset_index(drop=True)
        )

    @staticmethod
    def platform_summary(occurrences):
        rows = []
        for platform in PLATFORM_LABELS:
            group = occurrences[occurrences.platform == platform]
            assigned = int((group.cluster_id >= 0).sum())
            rows.append(
                {
                    "platform": platform,
                    "total": len(group),
                    "comments": group.source_row.nunique(),
                    "assigned": assigned,
                    "noise": len(group) - assigned,
                    "coverage": assigned / len(group) if len(group) else 0,
                }
            )
        return pd.DataFrame(rows)

    @staticmethod
    def monthly_summary(occurrences):
        dates = pd.to_datetime(occurrences.post_date, errors="coerce", format="mixed")
        frame = occurrences.loc[dates.notna(), ["platform"]].copy()
        frame["month"] = dates[dates.notna()].dt.to_period("M").dt.to_timestamp()
        if frame.empty:
            return pd.DataFrame(columns=["month", *PLATFORM_LABELS])
        grouped = frame.groupby(["month", "platform"]).size().unstack(fill_value=0)
        grouped = grouped.reindex(
            pd.date_range(grouped.index.min(), grouped.index.max(), freq="MS"),
            fill_value=0,
        )
        return (
            grouped.reindex(columns=list(PLATFORM_LABELS), fill_value=0)
            .rename_axis("month")
            .reset_index()
        )

    @staticmethod
    def topic_profile(frame, selected, terms):
        """Count evidence in the filter, keeping sentences/comments/parents distinct."""
        subset = frame[frame.cluster_id == selected]
        comments = subset.drop_duplicates(["platform", "source_row"])
        all_comments = frame.drop_duplicates(["platform", "source_row"])
        roots = {}
        for row in comments.to_dict("records"):
            key, method = SocialNLPClusterer.parent_post_key(row)
            record = roots.setdefault(
                key,
                {
                    "key": key,
                    "title": str(row.get("post_title") or "Judul tidak tersedia"),
                    "platform": row["platform"],
                    "comments": 0,
                    "identity_method": method,
                },
            )
            record["comments"] += 1
        sources = pd.DataFrame(
            list(roots.values()),
            columns=[
                "key",
                "title",
                "platform",
                "comments",
                "identity_method",
            ],
        )
        if len(sources):
            sources = sources.sort_values(["comments", "key"], ascending=[False, True])
        sentences = subset.drop_duplicates("sentence_id")
        text = (
            sentences.sentence.fillna("").map(SocialNLPClusterer._clean).str.casefold()
        )
        mentions = []
        for term in terms[:12]:
            pattern = re.compile(r"(?<!\w)" + re.escape(term.casefold()) + r"(?!\w)")
            count = int(
                text.map(
                    lambda value, pattern=pattern: bool(pattern.search(value))
                ).sum()
            )
            mentions.append(
                {
                    "term": term,
                    "sentences": count,
                    "share": count / max(1, len(sentences)),
                }
            )
        return {
            "occurrences": len(subset),
            "unique_sentences": len(sentences),
            "comments": len(comments),
            "comment_share": len(comments) / max(1, len(all_comments)),
            "roots": len(sources),
            "fallback_roots": int(
                (sources.identity_method == "context_fallback").sum()
            ),
            "dominant_share": float(sources.comments.max() / len(comments))
            if len(comments)
            else 0,
            "platforms": {
                p: int((comments.platform == p).sum())
                for p in PLATFORM_LABELS
                if p != "instagram" or bool((frame.platform == "instagram").any())
            },
            "sources": sources,
            "terms": pd.DataFrame(mentions, columns=["term", "sentences", "share"]),
        }

    @staticmethod
    def term_figure(terms):
        table = terms.head(8).iloc[::-1]
        figure = go.Figure(
            go.Bar(
                x=table.sentences,
                y=[html.escape(t) for t in table.term],
                orientation="h",
                marker_color=PALETTE["teal"],
                text=[number(n) for n in table.sentences],
                textposition="outside",
                cliponaxis=False,
                customdata=[[percent(s)] for s in table.share],
                hovertemplate="%{y}<br>%{x} kalimat unik (%{customdata[0]})<extra></extra>",
            )
        )
        SocialNLPStreamlitApp._chart_style(figure, 310)
        figure.update_layout(margin={"l": 0, "r": 40, "t": 8, "b": 8}, showlegend=False)
        figure.update_xaxes(
            title="Kalimat unik pada filter", rangemode="tozero", automargin=True
        )
        figure.update_yaxes(showgrid=False, automargin=True)
        return figure

    @staticmethod
    def topic_platform_figure(counts):
        platforms = list(PLATFORM_LABELS)
        figure = go.Figure(
            go.Bar(
                x=[counts.get(p, 0) for p in platforms],
                y=[PLATFORM_LABELS[p] for p in platforms],
                orientation="h",
                marker_color=[PALETTE[p] for p in platforms],
                text=[number(counts.get(p, 0)) for p in platforms],
                textposition="outside",
                cliponaxis=False,
                hovertemplate="%{y}: %{x} komentar/balasan<extra></extra>",
            )
        )
        SocialNLPStreamlitApp._chart_style(figure, 210)
        figure.update_layout(margin={"l": 0, "r": 38, "t": 8, "b": 8}, showlegend=False)
        figure.update_xaxes(title="Komentar & balasan", rangemode="tozero")
        figure.update_yaxes(showgrid=False, autorange="reversed", automargin=True)
        return figure

    @staticmethod
    def source_figure(sources):
        table = sources.head(5).iloc[::-1]
        figure = go.Figure(
            go.Bar(
                x=table.comments,
                y=table.key,
                orientation="h",
                marker_color=[PALETTE[p] for p in table.platform],
                text=[number(n) for n in table.comments],
                textposition="outside",
                cliponaxis=False,
                customdata=[
                    [html.escape(t), PLATFORM_LABELS[p]]
                    for t, p in zip(table.title, table.platform)
                ],
                hovertemplate="%{customdata[0]}<br>%{customdata[1]} · %{x} komentar topik<extra></extra>",
            )
        )
        SocialNLPStreamlitApp._chart_style(figure, max(200, 58 * len(table) + 60))
        figure.update_layout(margin={"l": 0, "r": 38, "t": 8, "b": 8}, showlegend=False)
        figure.update_xaxes(title="Komentar topik per post asal", rangemode="tozero")
        figure.update_yaxes(
            showgrid=False,
            automargin=True,
            tickvals=table.key,
            ticktext=[
                "<br>".join(html.escape(line) for line in wrap(t, 37)[:2])
                for t in table.title
            ],
        )
        return figure

    @staticmethod
    def _chart_style(figure, height=400):
        figure.update_layout(
            height=height,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font={
                "family": "Avenir Next, Segoe UI, sans-serif",
                "size": 13,
                "color": PALETTE["ink"],
            },
            margin={"l": 8, "r": 24, "t": 8, "b": 8},
            separators=",.",
            legend={"orientation": "h", "y": 1.14, "x": 0},
            hoverlabel={"bgcolor": "white", "font_color": PALETTE["ink"]},
            dragmode=False,
        )
        figure.update_xaxes(
            showline=False, zeroline=False, gridcolor="#EDF2F8", fixedrange=True
        )
        figure.update_yaxes(
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickfont={"color": PALETTE["ink"], "size": 12},
        )
        return figure

    @staticmethod
    def ranking_figure(table, selected=None, limit=12):
        table = table.head(limit).iloc[::-1]
        figure = go.Figure()
        for platform in PLATFORM_LABELS:
            figure.add_bar(
                name=PLATFORM_LABELS[platform],
                orientation="h",
                y=table.code,
                x=table[platform],
                marker_color=PALETTE[platform],
                marker_line_width=0,
                customdata=[
                    [int(cid), html.escape(label), number(total)]
                    for cid, label, total in zip(
                        table.cluster_id, table.label, table.total
                    )
                ],
                hovertemplate="<b>%{customdata[1]}</b><br>"
                + PLATFORM_LABELS[platform]
                + ": %{x} kalimat<br>Total: %{customdata[2]}<extra></extra>",
                marker_opacity=[
                    1 if selected is None or cid == selected else 0.55
                    for cid in table.cluster_id
                ],
            )
        figure.add_trace(
            go.Scatter(
                x=table.total,
                y=table.code,
                mode="text",
                text=["  " + number(n) for n in table.total],
                textposition="middle right",
                textfont={"size": 12},
                cliponaxis=False,
                hoverinfo="skip",
                showlegend=False,
            )
        )
        figure.update_layout(barmode="stack", bargap=0.35, clickmode="event+select")
        SocialNLPStreamlitApp._chart_style(figure, max(340, 28 * len(table) + 50))
        figure.update_layout(dragmode="pan", margin={"l": 0, "r": 45, "t": 28, "b": 10})
        figure.update_yaxes(
            tickvals=table.code,
            ticktext=[
                "<br>".join(
                    html.escape(line)
                    for line in wrap(
                        label.replace(" / ", " · "), 26, break_long_words=False
                    )
                )
                for label in table.label
            ],
            automargin=True,
            showgrid=False,
        )
        maximum = max(table.total.max(), 1) if len(table) else 1
        ticks = np.linspace(0, maximum, 5).astype(int)
        figure.update_xaxes(
            range=[0, maximum * 1.20],
            tickvals=ticks,
            ticktext=[number(n) for n in ticks],
            title="Kemunculan kalimat",
        )
        return figure

    @staticmethod
    def coverage_figure(platforms):
        figure = go.Figure()
        for row in platforms.itertuples(index=False):
            figure.add_bar(
                x=[row.assigned],
                y=[PLATFORM_LABELS[row.platform]],
                orientation="h",
                name=PLATFORM_LABELS[row.platform],
                marker_color=PALETTE[row.platform],
                text=[number(row.assigned)],
                textposition="inside",
                insidetextfont={"color": "white", "size": 13},
                hovertemplate="%{y}: %{x} terkelompok<extra></extra>",
            )
            figure.add_bar(
                x=[row.noise],
                y=[PLATFORM_LABELS[row.platform]],
                orientation="h",
                name="Belum terkelompok",
                legendgroup="noise",
                showlegend=row.platform == "youtube",
                marker_color=PALETTE["noise"],
                text=[number(row.noise)],
                textposition="inside",
                insidetextfont={"color": PALETTE["ink"], "size": 13},
                hovertemplate="%{y}: %{x} belum terkelompok<extra></extra>",
            )
        figure.update_layout(barmode="stack", bargap=0.5, showlegend=False)
        SocialNLPStreamlitApp._chart_style(figure, max(165, 60 * len(platforms) + 45))
        maximum = max(platforms.total.max(), 1)
        ticks = np.linspace(0, maximum, 3).astype(int)
        figure.update_xaxes(tickvals=ticks, ticktext=[number(n) for n in ticks])
        figure.update_yaxes(autorange="reversed", showgrid=False)
        return figure

    @staticmethod
    def trend_figure(months):
        figure = go.Figure()
        labels = [
            format_date(value, "MMM yy", locale="id_ID") for value in months.month
        ]
        for platform in PLATFORM_LABELS:
            figure.add_bar(
                x=labels,
                y=months[platform],
                name=PLATFORM_LABELS[platform],
                marker_color=PALETTE[platform],
                hovertemplate="%{x}<br>"
                + PLATFORM_LABELS[platform]
                + ": %{y} kalimat<extra></extra>",
            )
        SocialNLPStreamlitApp._chart_style(figure, 265)
        figure.update_layout(
            barmode="stack", legend={"orientation": "h", "y": 1.15}, bargap=0.35
        )
        figure.update_yaxes(title="Kalimat", showgrid=True, tickformat=",.0f")
        return figure

    @staticmethod
    def selected_cluster(event, valid):
        for point in event.get("selection", {}).get("points", []):
            custom = point.get("customdata")
            if isinstance(custom, (list, tuple)) and custom:
                try:
                    cid = int(custom[0])
                except (ValueError, TypeError):
                    continue
                if cid in valid:
                    return cid
        return None

    @staticmethod
    def _chart_selection(key, options):
        cid = SocialNLPStreamlitApp.selected_cluster(
            st.session_state.get(key, {}), options
        )
        if cid is not None:
            st.session_state["topic_select"] = options[cid]

    @staticmethod
    def _reset_filters(start, end, platforms=None):
        st.session_state["platforms"] = platforms or ["YouTube", "Reddit"]
        st.session_state["post_dates"] = (start, end)
        st.session_state["query"] = ""
        st.session_state["topic_select"] = "Semua topik"

    @staticmethod
    def _go_to_sentences():
        st.session_state["view"] = "Kalimat & sumber"

    @staticmethod
    def _go_to_explanations():
        st.session_state["view"] = "Penjelasan topik"

    def _selected_context(self, data, frame, selected):
        if selected is None:
            return
        subset = frame[frame.cluster_id == selected]
        label = (
            "Kalimat yang belum terkelompok"
            if selected < 0
            else self._topic_option(
                selected,
                next(t["label"] for t in data["topics"] if t["cluster_id"] == selected),
            )
        )
        with st.container(key="selected_context"):
            left, right = st.columns([4, 1.4], vertical_alignment="center")
            with left:
                st.markdown("**" + html.escape(label) + "**")
                narrative = next(
                    (
                        row
                        for row in data.get("topic_narratives", [])
                        if row["cluster_id"] == selected
                    ),
                    None,
                )
                if narrative:
                    st.subheader(narrative["topic_sentence"])
                    st.write(narrative["topic_description"])
                    st.caption(
                        "Ringkasan Gemini dari "
                        + self._gemini_inputs(narrative)
                        + " model penuh."
                    )
                st.caption(
                    f"{number(len(subset))} kemunculan dari {number(subset.sentence_id.nunique())} kalimat unik pada filter ini."
                )
            with right:
                if selected >= 0:
                    st.button(
                        "Jelaskan topik ini",
                        on_click=self._go_to_explanations,
                        width="stretch",
                    )
                elif st.session_state.get("view") != "Kalimat & sumber":
                    st.button(
                        "Baca kalimat", on_click=self._go_to_sentences, width="stretch"
                    )

    @staticmethod
    def _human_date(stamp, estimated=False):
        if not isinstance(stamp, str) or not stamp:
            return "Tidak diketahui"
        try:
            value = datetime.fromisoformat(stamp)
        except ValueError:
            return "Tidak diketahui"
        return (
            format_date(value, "long", locale="id_ID") + " (perkiraan)"
            if estimated
            else format_datetime(value, "d MMM y, HH:mm", locale="id_ID") + " WIB"
        )

    @staticmethod
    def _css():
        st.markdown(
            """<style>
        .stApp{background:#F4F7FB;color:#172D43}
        .stApp,.stApp input,.stApp button,.stApp textarea{font-family:'Avenir Next','Segoe UI',sans-serif}
        h1,h2,h3{font-family:'Avenir Next','Segoe UI',sans-serif!important;letter-spacing:-.025em;text-wrap:balance;scroll-margin-top:5rem;color:#172D43}
        h1{font-size:2.1rem!important;font-weight:650!important;line-height:1.18!important}
        h2{font-size:1.25rem!important;font-weight:700!important}
        h3{font-size:1.05rem!important;line-height:1.4!important}
        .block-container{padding:1.5rem 2.6rem 3rem;max-width:1600px}
        [data-testid='stSidebar']{background:#EDF2F8;border-right:1px solid #DCE5EE}
        [data-testid='stSidebar'] .block-container{padding:1.6rem 1.1rem}
        [data-testid='stCaptionContainer']{opacity:1!important}
        [data-testid='stCaptionContainer'] p{color:#52657B!important;font-size:.83rem!important;line-height:1.6}
        [data-testid='stSidebar'] hr{margin:.9rem 0}
        .stApp a{color:#116D78;text-underline-offset:3px}
        .stApp a:hover{color:#172D43;text-decoration:underline}
        .stApp :is(button,a,input,textarea,[role='combobox']):focus-visible{outline:3px solid #116D78!important;outline-offset:3px!important}
        .stApp button,.stApp a{touch-action:manipulation;-webkit-tap-highlight-color:#DCE5EE}
        .st-key-summary_metrics{border-top:1px solid #DCE5EE;border-bottom:1px solid #DCE5EE;padding:.75rem 0;margin:.5rem 0 .7rem}
        .st-key-summary_metrics p{margin:0}
        .metric-value{font-size:2rem;font-weight:720;letter-spacing:-.04em;font-variant-numeric:tabular-nums;line-height:1.25}
        .metric-label{font-size:.81rem;color:#52657B;margin-bottom:.3rem}
        .metric-detail{font-size:.76rem;color:#52657B;margin-top:.22rem;overflow-wrap:anywhere}
        .st-key-selected_context{background:#E8F3F4;border-left:4px solid #116D78;border-radius:0 8px 8px 0;padding:.85rem 1rem;margin:.2rem 0 1.1rem}
        .st-key-selected_context p{margin-bottom:.3rem}
        .st-key-topic_focus{background:#FFFFFF;border-top:4px solid #116D78;border-radius:8px;padding:1.3rem 1.4rem;margin:.4rem 0 1rem}
        .st-key-topic_metrics{border-top:1px solid #DCE5EE;padding:.9rem 0 .5rem;margin-top:.7rem}
        .st-key-topic_terms,.st-key-topic_origin,.st-key-topic_sources{background:#FFFFFF;padding:.3rem .4rem}
        .st-key-topic_sources{margin:.3rem 0 .7rem}
        .st-key-view [role='radiogroup']{gap:.25rem;flex-wrap:wrap;margin-bottom:.7rem}
        .st-key-view [role='radiogroup'] label{border:1px solid transparent;border-radius:6px;padding:.42rem .72rem;margin:0!important}
        .st-key-view [role='radiogroup'] label:has(input:checked){background:#FFFFFF;border-color:#B8CCD9;color:#116D78}
        .st-key-view [role='radiogroup'] label:hover{background:#E3EBF3}
        .st-key-view [role='radiogroup'] label:focus-within{outline:3px solid #116D78;outline-offset:2px}
        .st-key-overview_topics,.st-key-overview_coverage,.st-key-network_panel,.st-key-trend_panel,.st-key-source_panel{background:white;border:1px solid #DCE5EE;border-radius:10px;padding:1.15rem 1.15rem .7rem}
        .coverage-note{border-left:3px solid #116D78;background:#EDF5F6;padding:.85rem 1rem;font-size:.87rem;line-height:1.6;margin:.4rem 0 .8rem;overflow-wrap:anywhere}
        .coverage-note strong{font-size:1.15rem;font-variant-numeric:tabular-nums}
        .source-quote{font-size:.95rem;line-height:1.7;overflow-wrap:anywhere;white-space:pre-wrap;margin:.5rem 0 .75rem}
        .source-meta{font-size:.76rem;color:#52657B;line-height:1.7;overflow-wrap:anywhere}
        .stApp [data-testid='stText']{white-space:pre-wrap;overflow-wrap:anywhere}
        .sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
        .stApp [data-testid='stMarkdownContainer'] p{overflow-wrap:anywhere;max-width:85ch}
        @media(max-width:700px){.block-container{padding:1.25rem 1rem 2rem}h1{font-size:1.85rem!important}.st-key-summary_metrics [data-testid='stHorizontalBlock'],.st-key-topic_metrics [data-testid='stHorizontalBlock']{display:grid;grid-template-columns:1fr 1fr;gap:1rem}.st-key-summary_metrics [data-testid='stColumn'],.st-key-topic_metrics [data-testid='stColumn']{width:100%!important;min-width:0!important}.metric-value{font-size:1.7rem}.st-key-topic_focus{padding:.9rem 1rem}.st-key-selected_context [data-testid='stHorizontalBlock']{flex-wrap:wrap}.st-key-view [role='radiogroup'] label{padding:.35rem .4rem}.st-key-overview_topics,.st-key-overview_coverage,.st-key-network_panel,.st-key-trend_panel{padding:.85rem .6rem .5rem}}
        @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
        </style>""",
            unsafe_allow_html=True,
        )

    def _sidebar(self, occurrences):
        available_platforms = [
            label
            for key, label in PLATFORM_LABELS.items()
            if key in set(occurrences.platform)
        ]
        dates = (
            pd.to_datetime(occurrences.post_date, errors="coerce", format="mixed")
            .dropna()
            .dt.date
        )
        bounds = (dates.min(), dates.max()) if len(dates) else (None, None)
        with st.sidebar:
            st.header("BeeSense")
            st.caption("Eksplorasi percakapan")
            st.divider()
            st.subheader("Filter data")
            current = st.session_state.get("platforms")
            if isinstance(current, list):
                migrated = [PLATFORM_LABELS.get(item, item) for item in current]
                if migrated != current:
                    st.session_state["platforms"] = migrated
            platform_labels = st.multiselect(
                "Platform",
                available_platforms,
                default=available_platforms,
                key="platforms",
                bind="query-params",
            )
            start, end = bounds
            if start is not None:
                chosen = st.date_input(
                    "Tanggal post asal",
                    value=bounds,
                    min_value=start,
                    max_value=end,
                    key="post_dates",
                    bind="query-params",
                    help="Menyaring tanggal video/post induk. Tanggal komentar bisa berbeda atau berupa perkiraan.",
                )
                if len(chosen) == 2:
                    start, end = chosen
                elif len(chosen) == 1:
                    start = end = chosen[0]
                    st.caption(
                        "Rentang satu hari. Pilih tanggal akhir untuk memperluas."
                    )
                else:
                    start = end = None
            query = st.text_input(
                "Cari isi kalimat",
                placeholder="Misalnya: biaya, beasiswa…",
                autocomplete="off",
                key="query",
                bind="query-params",
            )
            st.button(
                "Hapus semua filter",
                on_click=self._reset_filters,
                args=(*bounds, available_platforms),
                width="stretch",
            )
            st.caption(
                "Filter berlaku untuk semua tampilan. Hasil berasal dari snapshot yang sama."
            )
        return self.filter_occurrences(
            occurrences,
            [value.casefold() for value in platform_labels],
            start,
            end,
            query,
        )

    def _metrics(self, frame):
        coverage = float((frame.cluster_id >= 0).mean())
        st.markdown(
            f'<span class="sr-only" role="status" aria-live="polite">Filter menampilkan {number(len(frame))} kemunculan kalimat, {number(frame.source_row.nunique())} komentar atau balasan, {percent(coverage)} kalimat terkelompok.</span>',
            unsafe_allow_html=True,
        )
        metrics = [
            (
                "Kalimat dianalisis",
                number(len(frame)),
                number(frame.sentence_id.nunique()) + " kalimat unik",
            ),
            (
                "Komentar & balasan",
                number(frame.source_row.nunique()),
                "Yang menyumbang kalimat pada filter",
            ),
            (
                "Topik pada filter",
                number(frame.loc[frame.cluster_id >= 0, "cluster_id"].nunique()),
                "Label otomatis dari isi kalimat",
            ),
            (
                "Kalimat terkelompok",
                percent(coverage),
                number(int((frame.cluster_id < 0).sum())) + " belum terkelompok",
            ),
        ]
        with st.container(key="summary_metrics"):
            for column, (label, value, detail) in zip(st.columns(4), metrics):
                column.markdown(
                    f'<div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-detail">{detail}</div>',
                    unsafe_allow_html=True,
                )

    @staticmethod
    def _topic_option(cid, label):
        return f"T{cid + 1:02d} · {label}"

    def _topic_selector(self, frame, topics):
        table = self.topic_summary(topics, frame)
        choices = {"Semua topik": None}
        choices.update(
            {
                self._topic_option(row.cluster_id, row.label): row.cluster_id
                for row in table.itertuples()
            }
        )
        if (frame.cluster_id < 0).any():
            choices["Belum terkelompok"] = -1
        current = st.session_state.get("topic_select")
        if current is not None and current not in choices:
            st.session_state["topic_select"] = "Semua topik"
        with st.sidebar:
            st.divider()
            st.subheader("Telusuri topik")
            value = st.selectbox(
                "Pilih topik",
                list(choices),
                key="topic_select",
                bind="query-params",
                help="Alternatif keyboard untuk klik graf. Pilihan ini menyaring detail dan tabel kalimat; ringkasan tetap menampilkan seluruh konteks filter.",
            )
        return choices[value]

    @staticmethod
    def _gemini_inputs(row):
        basis = "10 keyword c-TF-IDF"
        if row.get("representative_sentences_json"):
            count = len(json.loads(row["representative_sentences_json"]))
            basis += f" dan {count} kalimat representatif"
        return basis

    @staticmethod
    def _gemini_overview(data):
        rows = data.get("topic_narratives", [])
        if not rows:
            return
        with st.expander("Kalimat dan deskripsi 20 topik · Gemini"):
            st.caption(
                "Ringkasan AI dari "
                + SocialNLPStreamlitApp._gemini_inputs(rows[0])
                + " pada setiap topik. "
                "Deskripsi berlaku untuk model penuh dan tetap sama saat filter berubah. "
                "Gunakan kutipan sumber untuk meninjau bukti percakapan."
            )
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Topik": f"T{row['cluster_id'] + 1:02d}",
                            "Kalimat topik": row["topic_sentence"],
                            "Deskripsi": row["topic_description"],
                        }
                        for row in rows
                    ]
                ),
                hide_index=True,
                width="stretch",
            )
            st.download_button(
                "Unduh CSV topik Gemini",
                data["topic_narratives_csv"],
                file_name="topic_narratives.csv",
                mime="text/csv",
                key="gemini_topics_download",
            )
            st.caption(
                "Model: "
                + data["summary"]["topic_narratives"]["model"]
                + " · CSV memuat keyword, bobot, dan metadata pembentukan ringkasan."
            )

    def _overview(self, data, frame, selected):
        topics = self.topic_summary(data["topics"], frame)
        platforms = self.platform_summary(frame)
        left, right = st.columns([1.8, 1], gap="large")
        with left, st.container(key="overview_topics"):
            st.header("Topik yang paling banyak dibicarakan")
            st.caption(
                "12 topik terbesar berdasarkan kemunculan kalimat. Klik batang untuk melihat sumbernya."
            )
            if topics.empty:
                st.info(
                    "Kalimat pada filter ini belum mendapat topik. Buka Kalimat & sumber untuk meninjaunya."
                )
            else:
                st.plotly_chart(
                    self.ranking_figure(topics, selected),
                    width="stretch",
                    key="topic_ranking",
                    on_select=partial(
                        self._chart_selection,
                        "topic_ranking",
                        {
                            row.cluster_id: self._topic_option(
                                row.cluster_id, row.label
                            )
                            for row in topics.itertuples()
                        },
                    ),
                    selection_mode="points",
                    config={"displaylogo": False, "scrollZoom": False},
                    alt="Peringkat topik dengan batang bertumpuk menurut platform. Panjang batang menunjukkan jumlah kemunculan kalimat.",
                )
        with right, st.container(key="overview_coverage"):
            st.header("Dua platform, dua percakapan")
            st.caption(
                "Bagian berwarna sudah memiliki topik. Abu-abu belum terkelompok."
            )
            st.plotly_chart(
                self.coverage_figure(platforms),
                width="stretch",
                key="coverage_chart",
                config={"displayModeBar": False},
                alt="Jumlah kalimat terkelompok dan belum terkelompok untuk setiap platform.",
            )
            noise = int((frame.cluster_id < 0).sum())
            st.markdown(
                f'<div class="coverage-note" role="status" aria-live="polite"><strong>{percent(noise / len(frame))}</strong> kalimat belum terkelompok. Semuanya tetap tersedia untuk ditinjau.</div>',
                unsafe_allow_html=True,
            )
            for row in platforms.itertuples(index=False):
                st.markdown(
                    f"**{PLATFORM_LABELS[row.platform]}** · {number(row.total)} kalimat"
                )
                st.caption(
                    f"{number(row.comments)} komentar/balasan terwakili; {percent(row.coverage)} kalimat mendapat topik."
                )
            st.caption(
                "Persentase memakai kemunculan kalimat. Satu komentar dapat memuat beberapa kalimat; label topik belum divalidasi manusia."
            )
        with st.container(key="trend_panel"):
            st.header("Sebaran menurut bulan post asal")
            st.caption(
                "Mengelompokkan kalimat berdasarkan tanggal video/post induk, bukan waktu penulisan komentar. Snapshot parsial tidak menunjukkan tren aktivitas seluruh platform."
            )
            monthly = self.monthly_summary(frame)
            if not monthly.empty:
                st.plotly_chart(
                    self.trend_figure(monthly),
                    width="stretch",
                    key="monthly_chart",
                    config={"displaylogo": False},
                    alt="Distribusi jumlah kalimat menurut bulan publikasi video atau post induk, dibagi menurut platform.",
                )
            else:
                st.info("Tidak ada tanggal post asal yang dapat ditampilkan.")
        with st.expander("Lihat angka di balik grafik"):
            st.caption(
                "Tabel menyediakan seluruh topik dan angka yang sama dengan grafik, termasuk topik di luar peringkat 12 terbesar."
            )
            st.dataframe(
                topics.rename(
                    columns={
                        "code": "Kode",
                        "label": "Topik",
                        "total": "Kalimat",
                        "unique": "Kalimat unik",
                        "comments": "Komentar",
                    }
                ).drop(columns=["cluster_id", "share"]),
                hide_index=True,
                width="stretch",
            )
            st.dataframe(
                platforms.rename(
                    columns={
                        "platform": "Platform",
                        "total": "Kalimat",
                        "comments": "Komentar",
                        "assigned": "Terkelompok",
                        "noise": "Belum terkelompok",
                        "coverage": "Cakupan",
                    }
                ),
                hide_index=True,
                width="stretch",
            )
            st.dataframe(monthly, hide_index=True, width="stretch")

    def _network(self, data, frame, selected):
        st.header("Peta hubungan antar topik")
        st.caption(
            "Ukuran node mengikuti jumlah kalimat; legenda warna menunjukkan asal platform, atau platform terbanyak ketika Instagram disertakan. Kode T menghubungkan node dengan daftar topik."
        )
        count = int(frame.loc[frame.cluster_id >= 0, "cluster_id"].nunique())
        if not count:
            st.info(
                "Belum ada topik untuk filter ini. Pilih Belum terkelompok untuk membaca kalimatnya."
            )
            return
        floor = float(data["summary"]["config"]["graph"]["min_similarity"])
        # Filters change the slider's bounds, while page-persisted state can
        # still contain the previous limit. Reconcile it before registration;
        # this also covers a one-topic result where the slider is hidden.
        stored_limit = st.session_state.get("node_limit", count)
        bounded_limit = max(1, min(count, stored_limit))
        if stored_limit != bounded_limit:
            st.session_state["node_limit"] = bounded_limit
        with st.expander("Atur keterhubungan & jumlah topik"):
            threshold = (
                st.slider(
                    "Kemiripan minimum antar topik",
                    floor,
                    1.0,
                    floor,
                    0.01,
                    key="similarity",
                    bind="query-params",
                    persist_state="page",
                )
                if floor < 1
                else 1.0
            )
            limit = (
                st.slider(
                    "Jumlah topik pada peta",
                    1,
                    count,
                    count,
                    key="node_limit",
                    bind="query-params",
                    persist_state="page",
                )
                if count > 1
                else 1
            )
            st.caption(
                "Ambang menyaring hubungan yang tersimpan. Posisi peta tetap saat filter berubah; jarak bukan ukuran makna yang terkalibrasi."
            )
        with st.container(key="network_panel"):
            figure, stats = self.topic_figure(
                data["topics"], data["graph"], frame, threshold, limit, selected
            )
            st.plotly_chart(
                figure,
                width="stretch",
                key="topic_map",
                on_select=partial(
                    self._chart_selection,
                    "topic_map",
                    {
                        t["cluster_id"]: self._topic_option(t["cluster_id"], t["label"])
                        for t in data["topics"]
                        if t["cluster_id"] in set(frame.cluster_id)
                    },
                ),
                selection_mode="points",
                config={"displaylogo": False, "scrollZoom": False},
                alt="Jaringan topik berlabel kode T. Ukuran adalah volume; legenda warna menjelaskan asal platform; garis adalah kemiripan makna yang disimpulkan model.",
            )
            st.caption(
                f"{number(stats['nodes'])} dari {number(stats['available_topics'])} topik; {number(stats['edges'])} hubungan kemiripan. Garis adalah inferensi isi, bukan hubungan antar akun. Topik tanpa garis tetap ditampilkan."
            )
        st.header("Seluruh topik pada filter")
        table = self.topic_summary(data["topics"], frame).rename(
            columns={
                "code": "Kode",
                "label": "Istilah topik",
                "total": "Kalimat",
                "unique": "Kalimat unik",
                "comments": "Komentar",
                "youtube": "YouTube",
                "reddit": "Reddit",
                "instagram": "Instagram",
            }
        )
        st.dataframe(
            table[
                [
                    "Kode",
                    "Istilah topik",
                    "Kalimat",
                    "Kalimat unik",
                    "Komentar",
                    "YouTube",
                    "Reddit",
                    "Instagram",
                ]
            ],
            hide_index=True,
            width="stretch",
            height=350,
        )
        st.caption(
            "Gunakan Pilih topik di panel filter untuk menelusuri setiap kode dengan keyboard."
        )

    def _source_quote(self, row):
        label = PLATFORM_LABELS[row["platform"]]
        date_label = self._human_date(
            row["content_date"], row["content_date_accuracy"] == "perkiraan"
        )
        st.markdown(
            f'<div class="source-meta">{label} · {html.escape(date_label)}</div><div class="source-quote">{html.escape(row["sentence"])}</div>',
            unsafe_allow_html=True,
        )
        st.caption(str(row["post_title"]))
        url = str(row["url"] or "")
        if url.startswith(("https://", "http://")):
            st.link_button(f"Buka percakapan di {label}", url)

    @staticmethod
    def explanation_figure(explanation):
        rows = explanation["monthly"]
        figure = go.Figure()
        labels = [
            format_date(
                pd.Period(row["period"], freq="M").start_time, "MMM yy", locale="id_ID"
            )
            for row in rows
        ]
        for key, label, color in [
            ("combined", "Gabungan", PALETTE["ink"]),
            ("youtube", "YouTube", PALETTE["youtube"]),
            ("reddit", "Reddit", PALETTE["reddit"]),
            ("instagram", "Instagram", PALETTE["instagram"]),
        ]:
            shares, details = [], []
            for row in rows:
                counts = (
                    row
                    if key == "combined"
                    else row["platforms"].get(
                        key, {"all_comments": 0, "topic_comments": 0, "share": None}
                    )
                )
                valid = (
                    row["eligible_for_trend"]
                    and counts["all_comments"] >= explanation["min_monthly_comments"]
                )
                shares.append(
                    counts["share"] * 100
                    if valid and counts["share"] is not None
                    else None
                )
                details.append(
                    [number(counts["topic_comments"]), number(counts["all_comments"])]
                )
            figure.add_trace(
                go.Scatter(
                    x=labels,
                    y=shares,
                    name=label,
                    mode="lines+markers",
                    connectgaps=False,
                    line={"color": color, "width": 2.5 if key == "combined" else 1.5},
                    marker={"size": 7},
                    customdata=details,
                    hovertemplate="%{x}<br>"
                    + label
                    + ": %{y:.1f}%<br>%{customdata[0]} dari %{customdata[1]} komentar terwakili<extra></extra>",
                )
            )
        SocialNLPStreamlitApp._chart_style(figure, 290)
        figure.update_yaxes(
            title="Porsi komentar bertopik (%)", rangemode="tozero", tickformat=".1f"
        )
        figure.update_layout(
            legend={"orientation": "h", "y": 1.2},
            margin={"l": 12, "r": 20, "t": 35, "b": 8},
        )
        return figure

    @staticmethod
    def _explanation_row_selection(ids, labels):
        event = st.session_state.get("explanation_rows", {})
        rows = event.get("selection", {}).get("rows", [])
        if rows and 0 <= rows[0] < len(ids):
            st.session_state["topic_select"] = labels[ids[rows[0]]]

    def _explanations_view(self, data, frame, selected):
        if selected is None:
            st.header("Kenali topik percakapan")
            st.write(
                "Pilih satu topik untuk melihat apa yang dibicarakan, dari mana buktinya, dan bagaimana porsinya berubah."
            )
        else:
            self._topic_detail(data, frame, selected)
        with st.expander("Bandingkan seluruh topik", expanded=selected is None):
            self._explanation_index(data, frame, selected)

    def _explanation_index(self, data, frame, selected):
        st.caption(
            "Pilih baris atau gunakan Pilih topik di panel filter. Semua angka mengikuti filter aktif."
        )
        result = data["explanations"]
        records = []
        for item in result["topics"]:
            comparison = item["trend"]["comparison"]
            records.append(
                {
                    "cluster_id": item["cluster_id"],
                    "Kode": f"T{item['cluster_id'] + 1:02d}",
                    "Topik": item["label"],
                    "Pola teramati": item["trend"]["label"],
                    "Dukungan": "Terbatas"
                    if item["trend"]["support"] == "terbatas"
                    else "Deskriptif memadai",
                    "Perubahan (poin %)": comparison["delta_pp"]
                    if comparison
                    else None,
                    "Komentar": item["comments"],
                    "Post pendukung tren": item["trend"]["roots"],
                }
            )
        table = pd.DataFrame(records)
        if not len(table):
            st.info(
                "Belum ada topik yang dapat dijelaskan pada filter ini. Kalimat belum terkelompok tetap dapat dibaca di Kalimat & sumber."
            )
            return
        table = table.sort_values(
            ["Komentar", "cluster_id"], ascending=[False, True]
        ).reset_index(drop=True)
        labels = {
            t["cluster_id"]: self._topic_option(t["cluster_id"], t["label"])
            for t in data["topics"]
        }
        st.dataframe(
            table.drop(columns=["cluster_id"]),
            hide_index=True,
            width="stretch",
            height=350,
            key="explanation_rows",
            on_select=partial(
                self._explanation_row_selection, table.cluster_id.tolist(), labels
            ),
            selection_mode="single-row",
            column_config={
                "Perubahan (poin %)": st.column_config.NumberColumn(format="%+.1f")
            },
        )
        st.caption(
            "Pola adalah deskripsi snapshot, bukan ramalan atau tren seluruh platform. Komentar yang sama dapat masuk beberapa topik; porsi antar topik tidak harus berjumlah 100%."
        )
        st.download_button(
            "Unduh penjelasan pada filter ini",
            json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False),
            file_name="penjelasan_topik.json",
            mime="application/json",
            icon=":material/download:",
        )
        if selected is None:
            st.info(
                "Pilih satu topik untuk membaca narasi, grafik porsi, perubahan istilah, dan bukti kalimatnya."
            )

    def _explanation_detail(self, data, selected):
        result = data.get("explanations")
        if result is None:
            return None
        item = next(
            (topic for topic in result["topics"] if topic["cluster_id"] == selected),
            None,
        )
        if item is None:
            return None
        trend = item["trend"]
        st.subheader(trend["label"])
        st.write(item["trend_explanation"])
        comparison = trend["comparison"]
        if comparison and comparison["delta_pp"] is not None:
            a, b, c = st.columns(3)
            a.metric(
                "Porsi periode pembanding", percent(comparison["previous"]["share"])
            )
            b.metric("Porsi periode terakhir", percent(comparison["recent"]["share"]))
            c.metric(
                "Perubahan porsi",
                format_decimal(
                    comparison["delta_pp"], format="+0.0;-0.0", locale="id_ID"
                )
                + " poin %",
            )
            adjusted = comparison["platform_standardized_delta_pp"]
            if adjusted is not None:
                st.caption(
                    "Dengan komposisi platform periode pembanding dipertahankan, perubahan terukur "
                    + format_decimal(adjusted, format="+0.0;-0.0", locale="id_ID")
                    + " poin persentase. Ini pemeriksaan sensitivitas, bukan koreksi bias crawl secara menyeluruh."
                )
        reasons = trend["blockers"] + trend["cautions"]
        if reasons:
            st.info("Dukungan terbatas. " + " ".join(reasons[:2]))
        date_basis = (
            "tanggal post/video asal"
            if result["period"]["date_basis"] == "post_date"
            else "tanggal komentar, termasuk tingkat kepastiannya"
        )
        st.caption(
            "Dasar waktu: "
            + date_basis
            + ". Porsi = komentar terwakili yang memuat topik / seluruh komentar terwakili pada bulan yang sama, termasuk yang belum terkelompok. Satu komentar dihitung sekali per topik."
        )
        if any(row["eligible_for_trend"] for row in item["monthly"]):
            st.plotly_chart(
                self.explanation_figure(
                    {
                        **item,
                        "min_monthly_comments": result["options"][
                            "min_monthly_comments"
                        ],
                    }
                ),
                width="stretch",
                key=f"trend_topic_{selected}",
                config={"displaylogo": False},
                alt="Perubahan porsi komentar yang memuat topik, untuk gabungan dan setiap platform. Bulan tanpa dukungan cukup menjadi celah.",
            )
        st.caption(
            "Bulan parsial, bulan tanpa komentar, atau dukungan platform terlalu kecil menjadi celah pada grafik. Contoh kalimat merangkum seluruh filter; penentuan arah memakai bulan kalender lengkap."
        )
        with st.expander("Mengapa penjelasan ini muncul?"):
            st.write(
                "Ringkasan menyeleksi kalimat asli memakai kesesuaian istilah c-TF-IDF, kedekatan embedding, panjang informatif, dan keragaman MMR. Prioritas diberikan pada post induk yang berbeda bila tersedia."
            )
            st.write(
                "Arah memadukan median kemiringan pasangan bulan Theil–Sen, konsistensi peringkat Kendall, dan dua jendela bulan lengkap terakhir. Angka ini tidak digunakan sebagai uji signifikansi atau probabilitas kebenaran."
            )
            st.json(
                {
                    "slope_poin_persen_per_bulan": trend["slope_pp_per_month"],
                    "kendall_tau": trend["kendall_tau"],
                    "bulan_layak": trend["eligible_months"],
                    "komentar_pendukung": trend["support_comments"],
                    "post_induk_pendukung": trend["roots"],
                    "porsi_post_dominan": trend["dominant_root_share"],
                    "bulan_parsial_dikeluarkan": result["partial_months_excluded"],
                    "aturan": result["options"],
                },
                expanded=False,
            )
            if reasons:
                for reason in reasons:
                    st.write("• " + reason)
            changes = item["term_changes"]
            if changes:
                st.write(
                    "Frasa yang berubah dalam komentar topik pada dua jendela pembanding:"
                )
                st.dataframe(
                    pd.DataFrame(changes)[
                        [
                            "term",
                            "previous_comments",
                            "previous_total",
                            "recent_comments",
                            "recent_total",
                            "delta_pp",
                            "smoothed_log_odds_delta",
                        ]
                    ],
                    hide_index=True,
                    width="stretch",
                )
                st.caption(
                    "Hitungan adalah komentar yang menyebut frasa. Penyebutnya komentar topik pada masing-masing jendela; frasa tidak saling eksklusif. Ini tidak membuktikan lahirnya isu baru."
                )
            else:
                st.caption(
                    "Tidak ada perubahan frasa yang melewati ambang deskriptif dan dukungan sampel."
                )
            monthly = []
            for row in item["monthly"]:
                monthly.append(
                    {
                        "Bulan": row["period"],
                        "Komentar topik": row["topic_comments"],
                        "Seluruh komentar": row["all_comments"],
                        "Porsi": row["share"],
                        "Kalender lengkap": row["full_calendar_month"],
                        "Masuk penghitungan arah": row["eligible_for_trend"],
                    }
                )
            st.dataframe(pd.DataFrame(monthly), hide_index=True, width="stretch")
        return item

    def _topic_detail(self, data, frame, selected):
        if selected is None:
            return
        subset = frame[frame.cluster_id == selected]
        item = next(
            (
                t
                for t in data.get("explanations", {}).get("topics", [])
                if t["cluster_id"] == selected
            ),
            None,
        )
        if selected < 0:
            st.header("Kalimat yang belum terkelompok")
            st.caption(
                "Model belum menemukan kelompok yang cukup kuat. Daftar ini dapat memuat beragam topik."
            )
        else:
            topic = next(t for t in data["topics"] if t["cluster_id"] == selected)
            profile = self.topic_profile(frame, selected, topic["terms"])
            with st.container(key="topic_focus"):
                st.header(f"T{selected + 1:02d} · {topic['label']}")
                narrative = next(
                    (
                        row
                        for row in data.get("topic_narratives", [])
                        if row["cluster_id"] == selected
                    ),
                    None,
                )
                if narrative:
                    st.subheader(narrative["topic_sentence"])
                    st.write(narrative["topic_description"])
                    st.caption(
                        "Ringkasan Gemini berdasarkan "
                        + self._gemini_inputs(narrative)
                        + " model penuh. Ringkasan AI ini perlu ditinjau bersama kutipan sumber."
                    )
                    with st.expander("10 keyword yang dikirim ke Gemini"):
                        st.dataframe(
                            pd.DataFrame(json.loads(narrative["keywords_json"])).rename(
                                columns={"term": "Keyword", "weight": "Bobot c-TF-IDF"}
                            ),
                            hide_index=True,
                            width="stretch",
                        )
                    if narrative.get("representative_sentences_json"):
                        representatives = json.loads(
                            narrative["representative_sentences_json"]
                        )
                        with st.expander(
                            f"{len(representatives)} kalimat yang dikirim ke Gemini"
                        ):
                            st.caption(
                                "Diurutkan dari kedekatan tertinggi dengan pusat topik. "
                                "Contoh ini berasal dari model penuh dan tetap sama saat filter berubah. "
                                "Skor kedekatan bukan ukuran kebenaran atau persetujuan."
                            )
                            st.dataframe(
                                pd.DataFrame(representatives)[
                                    ["sentence", "centroid_similarity"]
                                ].rename(
                                    columns={
                                        "sentence": "Kalimat",
                                        "centroid_similarity": "Kedekatan dengan pusat topik",
                                    }
                                ),
                                hide_index=True,
                                width="stretch",
                            )
                if item:
                    st.write(item["description"])
                coherence = topic.get("coherence_cv")
                global_score = data["summary"].get("coherence", {}).get("macro_mean")
                quality_detail = (
                    "Rata-rata model "
                    + format_decimal(global_score, format="0.0000", locale="id_ID")
                    if global_score is not None
                    else "Skor model penuh, bukan akurasi"
                )
                metrics = [
                    (
                        "Komentar dalam topik",
                        number(profile["comments"]),
                        "Komentar & balasan unik pada filter",
                    ),
                    (
                        "Porsi komentar",
                        percent(profile["comment_share"]),
                        "Dari seluruh komentar terwakili pada filter",
                    ),
                    (
                        "Post asal",
                        number(profile["roots"]),
                        "Video atau thread pendukung",
                    ),
                    (
                        "Coherence topik (c_v)",
                        format_decimal(coherence, format="0.0000", locale="id_ID")
                        if coherence is not None
                        else "Belum dihitung",
                        quality_detail,
                    ),
                ]
                with st.container(key="topic_metrics"):
                    for column, (label, value, detail) in zip(st.columns(4), metrics):
                        column.markdown(
                            f'<div class="metric-label">{html.escape(label)}</div>'
                            f'<div class="metric-value">{html.escape(value)}</div>'
                            f'<div class="metric-detail">{html.escape(detail)}</div>',
                            unsafe_allow_html=True,
                        )
                st.caption(
                    "Coherence mengukur keselarasan istilah pada model penuh. Filter mengubah jumlah dan bukti; skor model tidak dihitung ulang. Satu komentar dapat memuat beberapa topik."
                )
            left, right = st.columns([1.25, 1], gap="large")
            with left, st.container(key="topic_terms", border=True):
                st.subheader("Istilah yang mewakili topik")
                st.caption(
                    "Kosakata c-TF-IDF model penuh, dihitung kemunculannya pada kalimat unik di filter ini."
                )
                if len(profile["terms"]):
                    st.plotly_chart(
                        self.term_figure(profile["terms"]),
                        width="stretch",
                        key=f"topic_terms_{selected}",
                        config={"displayModeBar": False},
                        alt="Jumlah kalimat unik yang memuat masing-masing istilah pembeda topik. Istilah dapat tumpang tindih.",
                    )
                else:
                    st.info(
                        "Istilah belum tersedia. Gunakan kutipan sumber untuk meninjau isi topik."
                    )
            with right, st.container(key="topic_origin", border=True):
                st.subheader("Dari mana percakapannya?")
                st.caption(
                    "Setiap komentar dihitung sekali, meskipun menyumbang beberapa kalimat."
                )
                st.plotly_chart(
                    self.topic_platform_figure(profile["platforms"]),
                    width="stretch",
                    key=f"topic_platforms_{selected}",
                    config={"displayModeBar": False},
                    alt="Jumlah komentar dan balasan topik terpilih pada setiap platform.",
                )
                st.caption(
                    f"{number(profile['unique_sentences'])} kalimat unik dari {number(profile['comments'])} komentar. Hitungan mengikuti filter aktif."
                )
            with st.container(key="topic_sources", border=True):
                st.subheader("Post asal yang paling banyak menyumbang")
                st.caption(
                    "Maksimal 5 post menurut jumlah komentar dalam topik. Ini membantu melihat apakah satu percakapan mendominasi bukti."
                )
                st.plotly_chart(
                    self.source_figure(profile["sources"]),
                    width="stretch",
                    key=f"topic_sources_{selected}",
                    config={"displayModeBar": False},
                    alt="Lima video atau thread asal dengan komentar topik terbanyak, dibagi menurut platform.",
                )
                if profile["dominant_share"] > 0.6:
                    st.info(
                        f"Satu post menyumbang {percent(profile['dominant_share'])} komentar topik pada filter ini. Pertimbangkan keragaman sumber saat membaca ringkasannya."
                    )
                if profile["fallback_roots"]:
                    st.caption(
                        f"Identitas {number(profile['fallback_roots'])} post memakai konteks judul/tanggal karena ID URL tidak tersedia."
                    )
            with st.expander("Lihat angka istilah dan sumber"):
                st.dataframe(
                    profile["terms"]
                    .assign(share=profile["terms"]["share"].map(percent))
                    .rename(
                        columns={
                            "term": "Istilah",
                            "sentences": "Kalimat unik",
                            "share": "Porsi kalimat unik",
                        }
                    ),
                    hide_index=True,
                    width="stretch",
                )
                st.dataframe(
                    profile["sources"][
                        ["title", "platform", "comments", "identity_method"]
                    ]
                    .assign(
                        platform=lambda table: table.platform.map(PLATFORM_LABELS),
                        identity_method=lambda table: table.identity_method.map(
                            {
                                "native_url": "ID video/thread",
                                "context_fallback": "Judul & tanggal",
                            }
                        ),
                    )
                    .rename(
                        columns={
                            "title": "Post asal",
                            "platform": "Platform",
                            "comments": "Komentar",
                            "identity_method": "Dasar identitas",
                        }
                    ),
                    hide_index=True,
                    width="stretch",
                )
        st.write(
            f"{number(len(subset))} kemunculan dari {number(subset.sentence_id.nunique())} kalimat unik, dalam {number(subset.source_row.nunique())} komentar/balasan."
        )
        explanation = (
            self._explanation_detail(data, selected) if selected >= 0 else None
        )
        if explanation and explanation["evidence"]:
            examples = pd.DataFrame(explanation["evidence"])
        else:
            scores = data["sentences"].set_index("sentence_id").centroid_similarity
            examples = (
                subset.assign(score=subset.sentence_id.map(scores))
                .sort_values("score", ascending=False, na_position="last")
                .drop_duplicates("sentence_id")
                .head(3)
            )
        st.subheader("Bukti kalimat dari sumber")
        st.caption(
            "Kalimat asli dipilih karena kesesuaian isi dan keragaman sumber. Buka percakapan untuk memeriksa konteksnya."
        )
        for column, (_, row) in zip(st.columns(3), examples.iterrows()):
            with column, st.container(border=True):
                self._source_quote(row)
                if isinstance(row.get("matched_terms"), list) and row["matched_terms"]:
                    st.caption("Memuat istilah: " + ", ".join(row["matched_terms"][:4]))
        if st.session_state.get("view") != "Kalimat & sumber":
            st.button("Lihat seluruh kalimat topik", on_click=self._go_to_sentences)

    def _sentences(self, data, frame, selected):
        shown = frame if selected is None else frame[frame.cluster_id == selected]
        by_id = {t["cluster_id"]: t["label"] for t in data["topics"]}
        table = shown.copy()
        table["topic"] = table.cluster_id.map(by_id).fillna("Belum terkelompok")
        table["date_label"] = [
            self._human_date(r.content_date, r.content_date_accuracy == "perkiraan")
            for r in table.itertuples()
        ]
        table["root_date_label"] = [
            self._human_date(value) for value in table.post_date
        ]
        table["source_link"] = table.url.where(
            table.url.str.startswith(("https://", "http://")), ""
        )
        st.header("Kalimat & sumber percakapan")
        st.caption(
            f"{number(len(table))} kemunculan sesuai filter. Pilih satu baris untuk membaca kalimat lengkap dan sumbernya."
        )
        with st.container(key="source_panel"):
            preview = table.head(1000)
            event = st.dataframe(
                preview[
                    [
                        "sentence",
                        "topic",
                        "platform",
                        "post_title",
                        "root_date_label",
                        "date_label",
                        "source_link",
                        "source_row",
                    ]
                ],
                column_config={
                    "sentence": st.column_config.TextColumn("Kalimat", width="large"),
                    "topic": "Topik",
                    "platform": "Platform",
                    "post_title": st.column_config.TextColumn(
                        "Post asal", width="medium"
                    ),
                    "root_date_label": "Tanggal post (WIB)",
                    "date_label": "Tanggal kalimat",
                    "source_link": st.column_config.LinkColumn(
                        "Sumber", display_text="Buka percakapan"
                    ),
                    "source_row": "Baris Excel",
                },
                hide_index=True,
                width="stretch",
                height=450,
                on_select="rerun",
                selection_mode="single-row",
                key="source_rows",
            )
            selected_rows = event.get("selection", {}).get("rows", [])
            if selected_rows and selected_rows[0] < len(preview):
                with st.container(border=True):
                    self._source_quote(preview.iloc[selected_rows[0]])
            st.caption(
                f"Tabel menampilkan maksimal 1.000 baris. Unduhan mencakup seluruh {number(len(table))} baris pada filter; tanggal perkiraan tetap ditandai."
            )
            st.download_button(
                "Unduh seluruh kalimat hasil filter",
                table.drop(columns=["source_link"]).to_json(
                    orient="records", lines=True, force_ascii=False
                ),
                file_name="kalimat_cluster.jsonl",
                mime="application/x-ndjson",
                icon=":material/download:",
            )
        if selected is not None and selected >= 0:
            with st.expander("Graf kalimat di dalam topik"):
                st.plotly_chart(
                    self.sentence_figure(
                        data["sentences"], data["embeddings"], frame, selected
                    ),
                    width="stretch",
                    key="sentence_map",
                    config={"displaylogo": False},
                    alt="Kemiripan antarcontoh kalimat dalam topik terpilih.",
                )
                st.caption(
                    "Maksimal 100 kalimat unik terdekat ke pusat topik. Garis cosine minimal 0,60. Baca kalimat melalui tabel sebagai alternatif graf."
                )

    def _methods(self, data):
        summary = data["summary"]
        st.header("Seberapa kuat kelompoknya?")
        st.write(
            "Hasil ini membantu eksplorasi percakapan. Label topik dibuat otomatis; belum ada label acuan untuk mengukur akurasi semantik."
        )
        selected = summary["selected"]
        coherence = summary.get("coherence")
        cols = st.columns(4 if coherence else 3)
        for col, label, value in zip(
            cols,
            ["Cakupan kalimat unik", "Pemisahan cosine", "Kestabilan ARI"],
            [
                percent(selected["coverage"]),
                format_decimal(
                    selected["silhouette_cosine"], format="0.000", locale="id_ID"
                ),
                format_decimal(
                    selected["stability_ari"], format="0.000", locale="id_ID"
                ),
            ],
        ):
            col.metric(label, value)
        if coherence:
            cols[3].metric(
                "Coherence c_v",
                format_decimal(
                    coherence["macro_mean"], format="0.0000", locale="id_ID"
                ),
            )
            target = format_decimal(coherence["min_score"], locale="id_ID")
            status = "tercapai" if coherence["target_met"] else "belum tercapai"
            st.write(
                f"Target rata-rata c_v ≥ {target} **{status}**. "
                f"{coherence['topics_below_target']} dari {coherence['topics_total']} topik "
                "berada di bawah target secara individual. Skor ini mengukur keterkaitan istilah, bukan akurasi label."
            )
            st.caption(
                f"Protokol tetap: maksimum {coherence['topn']} istilah c-TF-IDF per topik, "
                f"window {coherence['window_size']} token unigram/bigram, "
                f"{number(coherence['reference_documents'])} kalimat unik termasuk noise; "
                "rata-rata semua topik tanpa pembobotan. Evaluasi memakai korpus training."
            )
            baseline = summary.get("coherence_baseline")
            if baseline:
                st.write(
                    "Sebelum retrain: **"
                    + format_decimal(
                        baseline["macro_mean"], format="0.0000", locale="id_ID"
                    )
                    + "** dengan protokol dan korpus referensi yang sama."
                )
            with st.expander("Coherence setiap topik"):
                st.dataframe(
                    pd.DataFrame(
                        [
                            {
                                "Topik": topic["label"],
                                "c_v": topic.get("coherence_cv"),
                                "Kalimat unik": topic["unique_sentences"],
                            }
                            for topic in data["topics"]
                        ]
                    ),
                    hide_index=True,
                    width="stretch",
                )
        st.write(
            f"Metode terpilih: **{selected['candidate']}**; {number(selected['clusters'])} topik pada korpus penuh."
        )
        parameters = selected.get("parameters", {})
        is_dbscan = parameters.get("algorithm") == "DBSCAN"
        topic_reduction = summary.get("topic_reduction")
        if is_dbscan:
            st.write(
                f"**SBERT multilingual → UMAP → DBSCAN → c-TF-IDF** · Jarak Euclidean pada UMAP · eps {parameters['eps']:g} · "
                f"min_samples {parameters['min_samples']}. Kalimat yang tidak memenuhi kepadatan tetap menjadi noise."
            )
            if topic_reduction:
                st.write(
                    f"**{topic_reduction['original_topics']} kelompok DBSCAN → {topic_reduction['final_topics']} topik**. "
                    "Penggabungan hierarkis Ward berbobot jumlah kalimat memakai embedding SBERT asli. "
                    "Setiap langkah memilih kenaikan variasi dalam topik terkecil; kelompok asal tetap utuh dan noise dipertahankan. "
                    "Label, centroid, coherence dan metrik evaluasi dihitung ulang untuk topik akhir."
                )
            if selected["silhouette_cosine"] < 0:
                st.warning(
                    "Silhouette pada embedding SBERT asli bernilai negatif: beberapa kelompok masih tumpang tindih secara semantik. Cakupan tinggi tidak berarti label sudah akurat; periksa kalimat sumber dan validasi topik secara manual."
                )
        comparisons = pd.DataFrame(data["comparison"]).sort_values(
            "selection_score", ascending=False, na_position="last"
        )
        st.dataframe(
            comparisons[
                [
                    "candidate",
                    *(["dbscan_clusters"] if "dbscan_clusters" in comparisons else []),
                    "clusters",
                    "coverage",
                    "noise_fraction",
                    "silhouette_cosine",
                    "stability_ari",
                    *(["coherence_cv"] if "coherence_cv" in comparisons else []),
                    *(
                        ["coherence_status"]
                        if "coherence_status" in comparisons
                        else []
                    ),
                    "selection_score",
                    "eligible",
                ]
            ],
            hide_index=True,
            width="stretch",
            column_config={
                "candidate": "Kandidat",
                "dbscan_clusters": "Kelompok DBSCAN asal",
                "clusters": "Topik",
                "coverage": st.column_config.NumberColumn("Cakupan", format="percent"),
                "noise_fraction": st.column_config.NumberColumn(
                    "Belum terkelompok", format="percent"
                ),
                "silhouette_cosine": "Silhouette cosine",
                "stability_ari": "Stabilitas ARI",
                "coherence_cv": "Coherence c_v",
                "coherence_status": "Status evaluasi c_v",
                "selection_score": "Skor",
                "eligible": "Memenuhi syarat",
            },
        )
        st.caption(
            "Silhouette diukur pada embedding SBERT asli. ARI membandingkan topik akhir dari dua seed UMAP, termasuk penggabungan bila dikonfigurasi; cakupan dan noise tetap dilaporkan. DBSCAN tidak menghasilkan probabilitas keanggotaan."
            if is_dbscan
            else "Silhouette seluruh kandidat diukur pada embedding asli. ARI membandingkan dua seed; cakupan tetap dilaporkan agar noise tidak tersembunyi."
        )
        policy = summary.get("selection_policy", {})
        if policy:
            st.write(
                f"Dalam toleransi skor {format_decimal(policy['score_tolerance'], locale='id_ID')}, pemilihan mengutamakan pemisahan cosine yang lebih tinggi, lalu kestabilan dan cakupan. Toleransi ini heuristik, bukan uji signifikansi."
            )
            if policy.get("coherence_search"):
                st.caption(
                    "c_v dihitung mulai dari skor komposit tertinggi. Semua kandidat dalam toleransi skor terbaik yang lolos c_v diperiksa; kandidat di bawah rentang itu ditandai belum dievaluasi, bukan gagal coherence."
                )
        with st.expander("Aturan evaluasi & metadata model"):
            st.code(summary["selection_rule"], language=None)
            st.json(
                {
                    "model": summary["model"],
                    "source_sha256": summary["source_sha256"],
                    "created_at": summary["created_at"],
                    "evaluation": summary["evaluation_scope"],
                },
                expanded=False,
            )
            if coherence:
                st.json(coherence, expanded=False)
        st.divider()
        st.header("Apa yang tercakup dalam snapshot?")
        prep = summary["preparation"]
        st.write(
            f"{number(prep['input_rows'])} baris sumber mencakup {number(prep['eligible_source_rows'])} komentar/balasan. Setelah segmentasi: {number(prep['sentence_occurrences'])} kemunculan, {number(prep['unique_sentences'])} kalimat unik, dan {number(prep['duplicate_occurrences'])} pengulangan yang tetap dapat ditelusuri."
        )
        st.write(
            f"{number(prep['skipped_segments'])} potongan terlalu pendek/tidak cukup berupa kata disimpan terpisah. Jumlah komentar di ringkasan hanya menghitung baris yang menyumbang kalimat layak, sehingga bisa lebih kecil dari input."
        )
        st.caption(
            "Judul, platform, dan tanggal menjadi konteks sumber. Clustering memakai isi kalimat; filter tidak melatih ulang model. Tanggal komentar YouTube berupa perkiraan; tanggal kalender tidak berarti cakupan crawl menyeluruh."
        )
        with st.expander("Lihat potongan yang tidak masuk clustering"):
            st.dataframe(data["skipped"].head(1000), hide_index=True, width="stretch")
        st.markdown(
            "[Model SBERT multilingual](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) · [SBERT](https://sbert.net/) · [DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)"
        )

    def render(self):
        st.set_page_config(
            page_title="BeeSense | Analisis percakapan",
            page_icon="◉",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        self._css()
        title_slot = st.empty()
        st.write(
            "Lihat topik yang muncul, bandingkan platform, lalu telusuri kalimat aslinya."
        )
        manifest = self.run_dir / "manifest.json"
        if not manifest.exists():
            title_slot.title("Percakapan sosial")
            st.info(
                "Hasil clustering belum tersedia. Jalankan pemrosesan NLP terlebih dahulu."
            )
            st.code(
                ".venv-nlp/bin/python -m MachineLearning.social_nlp", language="bash"
            )
            return
        try:
            data = _load_artifacts(str(self.run_dir), manifest.stat().st_mtime_ns)
        except (ValueError, OSError, KeyError) as error:
            title_slot.title("Percakapan sosial")
            st.error(
                "Hasil tidak dapat dibaca atau checksum berubah. Pulihkan artifact dari run yang valid, lalu muat ulang. Detail: "
                + str(error)
            )
            return
        labels = [
            label
            for key, label in PLATFORM_LABELS.items()
            if key in set(data["occurrences"].platform)
        ]
        title = (
            " & ".join(labels)
            if len(labels) < 3
            else ", ".join(labels[:-1]) + " & " + labels[-1]
        )
        title_slot.title("Percakapan " + title)
        pipeline_note = None
        if (
            data["summary"]["selected"].get("parameters", {}).get("algorithm")
            == "DBSCAN"
        ):
            reduction = data["summary"].get("topic_reduction")
            pipeline_note = (
                "Topik dibentuk dengan SBERT multilingual → UMAP → DBSCAN"
                + (
                    f" → penggabungan menjadi {reduction['final_topics']} topik"
                    if reduction
                    else ""
                )
                + "; label memakai c-TF-IDF."
            )
        coherence = data["summary"].get("coherence")
        if coherence:
            st.caption(
                "Coherence c_v korpus penuh: "
                + format_decimal(
                    coherence["macro_mean"], format="0.0000", locale="id_ID"
                )
                + f" · {number(len(data['topics']))} topik pada model penuh. Rincian pada Metode & data."
            )
        frame = self._sidebar(data["occurrences"])
        if frame.empty:
            st.info(
                "Tidak ada kalimat untuk filter ini. Pilih platform, perluas tanggal, atau hapus kata pencarian melalui Hapus semua filter."
            )
            return
        dates = pd.to_datetime(
            frame.post_date, errors="coerce", format="mixed"
        ).dropna()
        if len(dates):
            st.caption(
                format_date(dates.min(), "long", locale="id_ID")
                + " – "
                + format_date(dates.max(), "long", locale="id_ID")
                + " · Tanggal post asal, WIB · Snapshot percakapan parsial"
            )
        selected = self._topic_selector(frame, data["topics"])
        self._gemini_overview(data)
        view = st.radio(
            "Tampilan analisis",
            VIEWS,
            horizontal=True,
            key="view",
            bind="query-params",
            label_visibility="collapsed",
        )
        if view in {"Ringkasan", "Peta topik"}:
            self._metrics(frame)
        else:
            with st.expander("Ringkasan seluruh data pada filter"):
                self._metrics(frame)
        if view == "Penjelasan topik" or (selected is not None and selected >= 0):
            options = json.loads((ROOT / "config/social_nlp.json").read_text())[
                "explanation"
            ]
            context_dates = st.session_state.get("post_dates", ())
            start = context_dates[0] if len(context_dates) else None
            end = context_dates[-1] if len(context_dates) else None
            fingerprint = sha256(
                "\n".join(frame.occurrence_id.astype(str)).encode()
            ).hexdigest()
            cache_key = (
                data.get("artifact_manifest_sha256"),
                str(self.run_dir),
                fingerprint,
                file_hash(ROOT / "MachineLearning/social_nlp.py"),
            )
            try:
                result = _explain_filtered(
                    cache_key,
                    start,
                    end,
                    json.dumps(options, sort_keys=True),
                    data,
                    frame,
                )
                data = {**data, "explanations": result}
            except (ValueError, TypeError, OSError, KeyError) as error:
                st.error(
                    "Penjelasan topik belum dapat dihitung. Periksa konfigurasi dan rentang tanggal. Detail: "
                    + str(error)
                )
                if view == "Penjelasan topik":
                    return
        if view not in {"Penjelasan topik", "Metode & data"}:
            self._selected_context(data, frame, selected)
        if view == "Ringkasan":
            self._overview(data, frame, selected)
        elif view == "Peta topik":
            self._network(data, frame, selected)
        elif view == "Penjelasan topik":
            self._explanations_view(data, frame, selected)
        elif view == "Kalimat & sumber":
            self._sentences(data, frame, selected)
        else:
            self._methods(data)
        if pipeline_note:
            with st.expander("Bagaimana topik dibentuk?"):
                st.caption(pipeline_note)
        st.divider()
        st.caption(
            "BeeSense · Analisis snapshot tersimpan. Keanggotaan topik mengikuti model penuh; filter mengubah data yang ditampilkan. Tanggal perkiraan tetap diberi tanda."
        )


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--run-dir", type=Path)
    args, _ = parser.parse_known_args()
    SocialNLPStreamlitApp(args.run_dir).render()


if __name__ == "__main__":
    main()
