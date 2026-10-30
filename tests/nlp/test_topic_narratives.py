from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

import numpy as np
import pandas as pd
from openpyxl import Workbook
from streamlit.testing.v1 import AppTest

from MachineLearning import topic_narratives as narratives
from MachineLearning.social_nlp import ROOT, SocialNLPClusterer, file_hash


def response():
    return {
        "candidates": [
            {
                "finishReason": "STOP",
                "content": {
                    "parts": [
                        {
                            "text": json.dumps(
                                {
                                    "topic_sentence": "Mahasiswa membahas pilihan bidang pendidikan tinggi.",
                                    "topic_description": "Keyword menggambarkan pembahasan pilihan pendidikan. Makna terperinci perlu ditinjau bersama sumber percakapan.",
                                }
                            )
                        }
                    ]
                },
            }
        ],
        "modelVersion": "gemini-3.5-flash-lite",
        "usageMetadata": {
            "promptTokenCount": 150,
            "candidatesTokenCount": 60,
            "totalTokenCount": 210,
        },
    }


def topic(cid=0):
    return {
        "cluster_id": cid,
        "term_weights": [
            {"term": "keyword" + str(i), "weight": (i + 1) / 100} for i in range(12)
        ],
    }


class GeminiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "auth.json").write_text(
            json.dumps([{"gemini_api_key": "TEST_SECRET_VALUE"}])
        )
        self.options = {
            **narratives.DEFAULTS,
            "enabled": True,
            "auth_file": "auth.json",
            "request_interval_seconds": 0,
        }
        self.sentences = pd.DataFrame(
            [
                {
                    "sentence_id": f"topic{cid}-sentence{index:02d}",
                    "sentence": f"Contoh kalimat {index} pada kelompok {cid}.",
                    "cluster_id": cid,
                    "centroid_similarity": min(index, 10) / 12,
                }
                for cid in range(20)
                for index in range(12)
            ]
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_script_path_entry_point_remains_available(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "MachineLearning/social_nlp.py"), "--help"],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--config", result.stdout)

    def generate(self, topics=None):
        return narratives.generate(
            topics or [topic()],
            "a" * 64,
            self.options,
            sentences=self.sentences,
            root=self.root,
            cache_dir=self.root / "cache",
            progress=lambda *a, **k: None,
        )

    def test_twenty_requests_rank_weights_and_resume_without_repeating_api(self):
        with patch.object(
            narratives, "request_topic", return_value=response()
        ) as request:
            rows = self.generate([topic(i) for i in range(20)])
            self.assertEqual(request.call_count, 20)
            self.assertEqual(self.generate([topic(i) for i in range(20)]), rows)
            self.assertEqual(request.call_count, 20)
            payload = request.call_args.args[2]
            prompt = json.loads(payload["contents"][0]["parts"][0]["text"])
            self.assertEqual(
                [v["term"] for v in prompt["keywords"]],
                ["keyword" + str(i) for i in range(11, 1, -1)],
            )
            self.assertNotIn("TEST_SECRET_VALUE", json.dumps(payload))
            self.assertNotIn("TEST_SECRET_VALUE", json.dumps(rows))
            self.assertEqual(len(prompt["representative_sentences"]), 10)
            self.assertEqual(
                [r["sentence_id"] for r in prompt["representative_sentences"][:3]],
                ["topic19-sentence10", "topic19-sentence11", "topic19-sentence09"],
            )
            self.assertTrue(
                all(
                    r["sentence_id"].startswith("topic19-")
                    for r in prompt["representative_sentences"]
                )
            )
        path = self.root / narratives.CSV_NAME
        narratives.write_csv(path, rows)
        self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r\n", path.read_bytes())
        loaded = narratives.read_csv(
            path,
            [topic(i) for i in range(20)],
            {
                "source_sha256": "a" * 64,
                "topic_narratives": {"model": self.options["model"]},
            },
            sentences=self.sentences,
        )
        self.assertEqual(loaded[0]["topic_sentence"], rows[0]["topic_sentence"])
        self.assertEqual(len(loaded), 20)

    def test_http_429_is_bounded_and_error_does_not_leak_server_body_or_key(self):
        def reject(*args, **kwargs):
            raise HTTPError(
                "https://example.test",
                429,
                "TEST_SECRET_VALUE",
                {},
                io.BytesIO(b"TEST_SECRET_VALUE"),
            )

        with (
            patch.object(narratives, "urlopen", side_effect=reject) as request,
            patch.object(narratives.time, "sleep"),
        ):
            with self.assertRaisesRegex(ValueError, "HTTP 429") as error:
                narratives.request_topic(
                    self.options["model"], "TEST_SECRET_VALUE", {}, self.options
                )
            self.assertEqual(request.call_count, 3)
            self.assertNotIn("TEST_SECRET_VALUE", str(error.exception))
            req = request.call_args.args[0]
            self.assertNotIn("TEST_SECRET_VALUE", req.full_url)
            self.assertEqual(req.get_header("X-goog-api-key"), "TEST_SECRET_VALUE")

    def test_prompt_revision_refreshes_cache_and_preserves_legacy_csv(self):
        legacy_version = "beesense-topic-id:1"
        with patch.object(narratives, "request_topic", return_value=response()):
            legacy_row = self.generate()[0]
        legacy_row["prompt_version"] = legacy_version
        for field in (
            "representative_sentences_json",
            "representative_sentences_sha256",
        ):
            del legacy_row[field]
        legacy_prompt = narratives.build_prompt(topic(), legacy_version)
        legacy_row["prompt_sha256"] = narratives.digest(legacy_prompt)
        cache = self.root / "cache/gemini_topics"
        for receipt in cache.glob("*.json"):
            receipt.unlink()
        legacy_fingerprint = narratives.digest(
            {
                "prompt": legacy_prompt,
                "model": self.options["model"],
                "source": "a" * 64,
                "version": legacy_version,
            }
        )
        (cache / (legacy_fingerprint + ".json")).write_text(
            narratives.canonical(legacy_row)
        )
        path = self.root / narratives.CSV_NAME
        narratives.write_csv(path, [legacy_row])
        summary = {
            "source_sha256": "a" * 64,
            "topic_narratives": {
                "model": self.options["model"],
                "prompt_version": legacy_version,
            },
        }
        self.assertEqual(
            narratives.read_csv(path, [topic()], summary)[0]["prompt_version"],
            legacy_version,
        )
        with patch.object(
            narratives, "request_topic", return_value=response()
        ) as request:
            revised_rows = self.generate()
            self.assertEqual(request.call_count, 1)
            self.assertEqual(self.generate(), revised_rows)
            self.assertEqual(request.call_count, 1)
            self.assertEqual(
                revised_rows[0]["prompt_version"], narratives.PROMPT_VERSION
            )
            self.assertNotEqual(
                revised_rows[0]["prompt_sha256"], legacy_row["prompt_sha256"]
            )
        narratives.write_csv(path, revised_rows)
        with self.assertRaisesRegex(ValueError, "prompt version differs"):
            narratives.read_csv(path, [topic()], summary, sentences=self.sentences)
        revised_rows[0]["prompt_version"] = "beesense-topic-id:unknown"
        with self.assertRaisesRegex(ValueError, "Unsupported Gemini prompt version"):
            narratives.validate_rows(
                revised_rows, [topic()], "a" * 64, self.options["model"]
            )

    def test_changed_representative_sentence_invalidates_cache_and_tampering_fails(
        self,
    ):
        with patch.object(
            narratives, "request_topic", return_value=response()
        ) as request:
            rows = self.generate()
            selected = json.loads(rows[0]["representative_sentences_json"])
            self.sentences.loc[
                self.sentences.sentence_id == selected[0]["sentence_id"], "sentence"
            ] = "Konteks kalimat telah diperbaiki."
            revised = self.generate()
            self.assertEqual(request.call_count, 2)
            self.assertNotEqual(rows[0]["prompt_sha256"], revised[0]["prompt_sha256"])
        with self.assertRaisesRegex(ValueError, "sentences differ"):
            narratives.validate_rows(
                rows,
                [topic()],
                "a" * 64,
                self.options["model"],
                sentences=self.sentences,
            )
        with self.assertRaisesRegex(ValueError, "fitted representative sentences"):
            narratives.generate(
                [topic()],
                "a" * 64,
                self.options,
                sentences=None,
                root=self.root,
                cache_dir=self.root / "cache",
                progress=lambda *a, **k: None,
            )

    def test_invalid_generated_text_and_changed_keyword_receipt_are_rejected(self):
        for sentence in (
            "Satu. Dua.",
            "=IMPORTDATA()",
            "<script>buruk</script>",
            "Tidak lengkap",
        ):
            with self.assertRaises(ValueError):
                narratives.validate_text(
                    {
                        "topic_sentence": sentence,
                        "topic_description": "Kalimat penjelas pertama. Kalimat penjelas kedua.",
                    }
                )
        with patch.object(narratives, "request_topic", return_value=response()):
            rows = self.generate()
        rows[0]["keywords_json"] = "[]"
        with self.assertRaisesRegex(ValueError, "keywords differ"):
            narratives.validate_rows(
                rows,
                [topic()],
                "a" * 64,
                self.options["model"],
                sentences=self.sentences,
            )

    def test_credentials_stay_out_of_configuration_and_gate_precedes_api(self):
        with self.assertRaisesRegex(ValueError, "Unknown settings"):
            SocialNLPClusterer({"gemini": {"api_key": "TEST_SECRET_VALUE"}})
        pipeline = SocialNLPClusterer({"gemini": {"enabled": True}})
        pipeline.topics = [topic(i) for i in range(19)]
        pipeline.coherence = {"target_met": True, "macro_mean": 0.6}
        with patch.object(
            narratives, "generate", side_effect=AssertionError("No request before gate")
        ):
            with self.assertRaisesRegex(ValueError, "exactly 20"):
                pipeline.generate_topic_narratives()
            pipeline.topics.append(topic(19))
            pipeline.coherence["macro_mean"] = 0.39
            with self.assertRaisesRegex(ValueError, "coherence"):
                pipeline.generate_topic_narratives()


class GeminiArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        root = Path(cls.temp.name)
        source = root / "source.xlsx"
        book = Workbook()
        sheet = book.active
        sheet.title = "Data"
        sheet.append(
            [
                "platform",
                "jenis",
                "judul_post",
                "tanggal_post_wib",
                "akurasi_tanggal_post",
                "tanggal_konten_wib",
                "akurasi_tanggal_konten",
                "teks",
                "url",
                "teks_dipotong",
            ]
        )
        for group in range(20):
            words = " ".join(f"bidang{chr(97 + group)}{chr(97 + i)}" for i in range(10))
            for index in range(3):
                sheet.append(
                    [
                        "instagram",
                        "comment",
                        "Fixture",
                        "2026-10-01",
                        "pasti",
                        "2026-10-01",
                        "pasti",
                        f"{words} contoh {index}.",
                        f"https://www.instagram.com/p/ABC/c/{group * 3 + index + 1}/",
                        False,
                    ]
                )
        book.save(source)
        auth = root / "auth.json"
        auth.write_text(json.dumps({"gemini_api_key": "TEST_SECRET_VALUE"}))
        pipeline = SocialNLPClusterer(
            {
                "gemini": {
                    "enabled": True,
                    "auth_file": str(auth),
                    "request_interval_seconds": 0,
                },
                "cache_dir": str(root / "cache"),
            },
            encoder=lambda texts: np.eye(20, dtype=np.float32)[
                np.repeat(np.arange(20), 3)
            ],
        )
        pipeline.prepare_excel(source).encode()
        pipeline.sentences["cluster_id"] = np.repeat(np.arange(20), 3)
        pipeline.sentences["membership_strength"] = np.nan
        pipeline.occurrences = pipeline.occurrences.merge(
            pipeline.sentences[["sentence_id", "cluster_id"]],
            on="sentence_id",
            validate="many_to_one",
        )
        pipeline.reduced_embeddings = [
            pipeline.embeddings[:, :2],
            pipeline.embeddings[:, :2],
        ]
        pipeline.reduction_info = {"algorithm": "UMAP", "synthetic_fixture": True}
        pipeline.selected = {"candidate": "synthetic_fixture"}
        pipeline.selection_policy = {}
        pipeline.describe_topics()
        with patch.object(narratives, "request_topic", return_value=response()):
            cls.output = pipeline.save(root / "result")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_csv_manifest_and_roundtrip_bind_every_topic_and_keyword_weight(self):
        data = SocialNLPClusterer.load_run(self.output)
        self.assertEqual(len(data["topic_narratives"]), 20)
        self.assertIn(
            narratives.CSV_NAME,
            json.loads((self.output / "manifest.json").read_text())["files_sha256"],
        )
        for t, row in zip(data["topics"], data["topic_narratives"]):
            self.assertEqual(
                t["terms"][:10],
                [item["term"] for item in json.loads(row["keywords_json"])],
            )
        self.assertNotIn(
            "TEST_SECRET_VALUE", (self.output / "summary.json").read_text()
        )
        path = self.output / narratives.CSV_NAME
        before = path.read_bytes()
        try:
            path.write_bytes(before + b"tampered")
            with self.assertRaisesRegex(ValueError, "checksum"):
                SocialNLPClusterer.load_run(self.output)
        finally:
            path.write_bytes(before)
        self.assertEqual(
            file_hash(path),
            json.loads((self.output / "manifest.json").read_text())["files_sha256"][
                narratives.CSV_NAME
            ],
        )

    def test_dashboard_displays_generated_sentence_without_network_or_training(self):
        with (
            patch.dict("os.environ", {"BEESENSE_NLP_RUN_DIR": str(self.output)}),
            patch.object(
                narratives,
                "request_topic",
                side_effect=AssertionError("UI cannot call Gemini"),
            ),
            patch.object(
                SocialNLPClusterer,
                "fit_excel",
                side_effect=AssertionError("UI cannot train"),
            ),
        ):
            app = AppTest.from_file(
                str(ROOT / "streamlit_apps.py"), default_timeout=45
            ).run()
            self.assertFalse(app.exception)
            self.assertTrue(
                any(
                    item.label == "Kalimat dan deskripsi 20 topik · Gemini"
                    for item in app.expander
                )
            )
            choice = next(
                value
                for value in app.selectbox(key="topic_select").options
                if value.startswith("T01 ·")
            )
            app.selectbox(key="topic_select").set_value(choice).run()
            self.assertFalse(app.exception)
            self.assertTrue(
                any(
                    item.value == "Mahasiswa membahas pilihan bidang pendidikan tinggi."
                    for item in app.subheader
                )
            )
            app.radio(key="view").set_value("Penjelasan topik").run()
            self.assertFalse(app.exception)
            self.assertTrue(
                any(
                    item.label == "3 kalimat yang dikirim ke Gemini"
                    for item in app.expander
                )
            )
            self.assertTrue(
                any("3 kalimat representatif" in item.value for item in app.caption)
            )


if __name__ == "__main__":
    unittest.main()
