---
type: community
cohesion: 0.07
members: 57
---

# Penggabungan Dataset

**Cohesion:** 0.07 - loosely connected
**Members:** 57 nodes

## Members
- [[.run_merge()]] - code - tests/nlp/test_dataset_merge.py
- [[.setUp()_11]] - code - tests/nlp/test_dataset_merge.py
- [[.source()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_instagram_comment_identity_conflict_and_fake_host_are_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_instagram_latest_record_wins_without_removing_equal_text_distinct_ids()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_latest_policy_audits_updated_comment_reply_classification()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_latest_policy_still_rejects_comment_attached_to_different_root()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_merge_preserves_identical_text_distinct_ids_and_formula_like_text()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_orphan_comment_is_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_same_native_id_different_kind_is_rejected_without_publication()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_twitter_comment_without_root_evidence_is_rejected()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_twitter_native_dedup_and_audited_roots_survive_merge()]] - code - tests/nlp/test_dataset_merge.py
- [[.test_twitter_sidecar_cannot_be_reused_for_changed_workbook()]] - code - tests/nlp/test_dataset_merge.py
- [[20-topiccoherence gate passed; active configuration switched]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[27–30October inclusiverefers tosourceacquisitiondate,notpostdate]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Active artifacts outputsnlp_20261030_instagram_topics20_02]] - concept - config/social_nlp.json
- [[Active20-topic Instagram-inclusive model configuration]] - document - config/social_nlp.json
- [[Active20-topic Instagram-inclusive model configuration_1]] - concept - config/social_nlp_instagram_20261030.json
- [[All20 actual contextual Gemini narratives validated]] - concept - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Bounded Instagram recovery does not override user stop]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Complete contextual20-row Gemini CSV passes bundle gate]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Configured c_v threshold 0.4 with topn 10 and window 110]] - concept - config/social_nlp.json
- [[Configured final topic target 20]] - concept - config/social_nlp.json
- [[Configured33034-record final merged workbook]] - concept - config/social_nlp.json
- [[Current active Gemini enabled; historical disabled state retained]] - concept - config/social_nlp.json
- [[Final Instagram-inclusive20-topicGemini configuration]] - concept - config/social_nlp_instagram_20261030_final.json
- [[Final audited33034-record Instagram-inclusive corpus]] - concept - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Fiveintegrationtests plus76NLP andoneisolateddashboardtestpassed]] - concept - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Historical30658-record preflight superseded by33034-record final corpus]] - concept - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Instagram acquisition stopped; audited modelGemini release live; pacing updated offline]] - document - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Instagram1.5.1 rate-limit recovery andstagedrun chronology]] - rationale - graphify-out/obsidian/InstagramCrawler instagrapi.md
- [[Keep the latest supplied observation per native ID, with full row lineage.]] - rationale - scripts/merge_social_datasets.py
- [[Latestnative-ID observation dedupwithrootconflict rejection]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Merge compact crawl workbooks, rejecting repeated native content identities.]] - rationale - scripts/merge_social_datasets.py
- [[MergeTests]] - code - tests/nlp/test_dataset_merge.py
- [[Published194e0b1 dashboard and byte-identical contextual CSV]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Read a workbook-bound sidecar, or the original hash-verified crawl audit.]] - rationale - MachineLearning/source_roots.py
- [[Resolve X conversation roots from audited native IDs, never caption similarity.]] - rationale - MachineLearning/source_roots.py
- [[RetainedSBERTrevision,UMAPDBSCANbudget andexplanationgates]] - rationale - config/social_nlp_instagram_20261030.json
- [[Return global native object ID plus its root; text never defines identity.]] - rationale - scripts/merge_social_datasets.py
- [[User stopped Instagram acquisition; no subsequent crawl]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Verified model configuration enables contextual Gemini CSV]] - concept - config/social_nlp_instagram_20261030.json
- [[Verified20-topic Instagram-inclusive modelmacro c_v0.4315219014]] - concept - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Verifieddashboard publication precedes offlinecrawlerpacing]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[Versionedmergepublishesrecordlineageduplicateauditandchecksums]] - rationale - docs/crawler/INSTAGRAM_PIPELINE_20261030.md
- [[checksum()]] - code - MachineLearning/source_roots.py
- [[identity()]] - code - scripts/merge_social_datasets.py
- [[main()_10]] - code - scripts/merge_social_datasets.py
- [[merge()]] - code - scripts/merge_social_datasets.py
- [[merge_social_datasets.py]] - code - scripts/merge_social_datasets.py
- [[merge_unique()]] - code - scripts/merge_social_datasets.py
- [[native()]] - code - MachineLearning/source_roots.py
- [[sha()]] - code - scripts/merge_social_datasets.py
- [[source_roots.py]] - code - MachineLearning/source_roots.py
- [[test_dataset_merge.py]] - code - tests/nlp/test_dataset_merge.py
- [[twitter_roots()]] - code - MachineLearning/source_roots.py
- [[write_roots()]] - code - MachineLearning/source_roots.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Penggabungan_Dataset
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Model dan Pengujian NLP]]
- 1 edge to [[_COMMUNITY_Penjadwalan dan Riwayat Akuisisi]]
- 1 edge to [[_COMMUNITY_app.py]]
- 1 edge to [[_COMMUNITY_Riwayat Sesi Instagram]]
- 1 edge to [[_COMMUNITY_topic_sentence_export.py]]
- 1 edge to [[_COMMUNITY_Model dan Pengujian NLP_1]]

## Top bridge nodes
- [[Active20-topic Instagram-inclusive model configuration]] - degree 11, connects to 2 communities
- [[test_dataset_merge.py]] - degree 9, connects to 2 communities
- [[MergeTests]] - degree 15, connects to 1 community
- [[Instagram acquisition stopped; audited modelGemini release live; pacing updated offline]] - degree 11, connects to 1 community
- [[write_roots()]] - degree 10, connects to 1 community