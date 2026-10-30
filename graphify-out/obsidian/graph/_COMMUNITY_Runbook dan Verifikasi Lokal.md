---
type: community
cohesion: 0.26
members: 13
---

# Runbook dan Verifikasi Lokal

**Cohesion:** 0.26 - loosely connected
**Members:** 13 nodes

## Members
- [[CI discovers shared-core Reddrix integration regressions]] - concept - .github/workflows/ci.yml
- [[CI verifies full Python 3.12 tooling separately from dashboard-only Python 3.123.14 matrix]] - document - .github/workflows/ci.yml
- [[Frozen full NLP and offline development environment]] - document - requirements/nlp.lock
- [[Frozen macOS Intel native SBERT training environment]] - document - requirements/sbert-macos-intel.lock
- [[Full Python3.12 tooling uses requirementsdev.txt and relocated package paths]] - concept - .github/workflows/ci.yml
- [[NLP, Streamlit and Plotly dependency ranges]] - document - requirements/nlp.txt
- [[Native SBERT training requirements include coherence evaluation]] - document - requirements/sbert.txt
- [[New-corpus native SBERT encoding or exact verified cache reuse]] - concept - graphify-out/obsidian/Menjalankan BeeSense.md
- [[Platform-specific macOS Intel Torch and numerical compatibility]] - rationale - requirements/sbert.txt
- [[Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12]] - rationale - docs/machine-learning/SOCIAL_NLP.md
- [[Separate Python 3.12 developmenttraining regression dependency entry]] - rationale - requirements/dev.txt
- [[Separate SBERT training and artifact-only dashboard environments]] - rationale - README.md
- [[Trainingevaluation-only Gensim coherence requirements]] - document - requirements/coherence.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Runbook_dan_Verifikasi_Lokal
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Coherence dan Quality Gate_3]]
- 2 edges to [[_COMMUNITY_Snapshot NLP dan Arsip_3]]
- 2 edges to [[_COMMUNITY_Snapshot NLP dan Arsip_1]]
- 2 edges to [[_COMMUNITY_Akuisisi Reddit Reddrix_7]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix]]
- 1 edge to [[_COMMUNITY_Ringkasan Topik Gemini_1]]
- 1 edge to [[_COMMUNITY_Akuisisi Reddit Reddrix_8]]
- 1 edge to [[_COMMUNITY_Arsitektur Crawler dan Dependensi]]
- 1 edge to [[_COMMUNITY_Coherence dan Quality Gate]]
- 1 edge to [[_COMMUNITY_Pipeline dan Persistensi NLP]]
- 1 edge to [[_COMMUNITY_Snapshot NLP dan Arsip_2]]

## Top bridge nodes
- [[CI verifies full Python 3.12 tooling separately from dashboard-only Python 3.123.14 matrix]] - degree 5, connects to 3 communities
- [[Separate SBERT training and artifact-only dashboard environments]] - degree 5, connects to 3 communities
- [[Separate Python 3.12 developmenttraining regression dependency entry]] - degree 9, connects to 2 communities
- [[Saved-model dashboard uses a separate runtime;full refitting stays Python 3.12]] - degree 3, connects to 2 communities
- [[Trainingevaluation-only Gensim coherence requirements]] - degree 6, connects to 1 community