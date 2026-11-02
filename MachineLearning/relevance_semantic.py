"""Reference profile and lazy local SBERT backend for relevance filtering."""

from __future__ import annotations

from hashlib import file_digest
from pathlib import Path

import numpy as np

DEFAULTS = {
    "keywords": ["kuliah", "kampus", "universitas", "beasiswa", "jurusan"],
    "scope": "Pendidikan tinggi: pilihan kuliah, kampus dan universitas, jurusan, beasiswa, biaya kuliah, penerimaan mahasiswa, pengalaman mahasiswa dan prospek kerja lulusan.",
    "references": {
        "relevant": [
            "Saya ingin daftar beasiswa kuliah tahun depan.",
            "Biaya kuliah dan uang UKT di universitas ini mahal.",
            "Orang tua saya tidak sanggup membayar biaya pendidikan kuliah.",
            "Bagaimana syarat pendaftaran beasiswa KIP Kuliah?",
            "Saya bingung memilih universitas swasta atau negeri.",
            "Prospek kerja lulusan jurusan teknik informatika bagaimana?",
            "Saya memilih jurusan kuliah sesuai minat dan peluang kerja.",
            "Cara mendaftar penerimaan mahasiswa baru lewat SNBP SNBT UTBK.",
            "Berapa nilai rapor dan skor ujian agar diterima di kampus?",
            "Apakah ada batas usia untuk mendaftar kuliah atau beasiswa?",
            "Kuliah sambil bekerja, kelas karyawan atau kuliah online.",
            "Saya mau melanjutkan pendidikan sarjana, magister atau doktor.",
            "Ibu tidak setuju saya kuliah di luar kota.",
            "Kualitas dosen, akreditasi jurusan dan fasilitas kampus.",
            "Saya sudah lulus SMA SMK dan ingin melanjutkan kuliah.",
            "Memilih kampus karena biaya kos dan transportasi mahasiswa.",
            "Kebijakan pemerintah tentang biaya pendidikan tinggi dan beasiswa.",
            "Saya kesulitan mengerjakan tugas kuliah dan skripsi.",
            "Pengalaman menjadi mahasiswa dan kehidupan perkuliahan.",
            "Saya mencari beasiswa kuliah di luar negeri.",
            "Setelah lulus sarjana saya mencari pekerjaan atau magang.",
            "Jurusan psikologi, kedokteran, ekonomi atau teknik di universitas.",
            "Saya ingin kuliah di BINUS, UI, UGM, ITB atau universitas lainnya.",
            "Mental saya tertekan karena beban tugas kuliah dan skripsi.",
        ],
        "generic": [
            "Terima kasih kak atas informasinya.",
            "Makasih banyak bang.",
            "Semoga sehat selalu dan sukses.",
            "Semangat ya, semoga sukses.",
            "Aamiin, semoga dimudahkan semuanya.",
            "Saya setuju sekali.",
            "Betul sekali, sama seperti saya.",
            "Wkwkwk lucu banget.",
            "Saya baru tahu informasi ini.",
            "Salam kenal dan salam sehat.",
            "Mantap, keren, bagus sekali.",
            "Saya suka video ini.",
            "Saya menonton videonya sampai selesai.",
            "Semoga bermanfaat bagi semua orang.",
        ],
        "irrelevant": [
            "Presiden dan pejabat korupsi harus dihukum berat.",
            "Partai politik dan pemerintah sedang berebut kekuasaan.",
            "MU kalah lagi semalam, pelatih sepak bolanya payah.",
            "Pertandingan sepak bola dan pemain favorit saya.",
            "Suami saya selingkuh dengan tetangga.",
            "Istri dan suami bertengkar soal rumah tangga dan perceraian.",
            "Saya sedang menonton drama film dan alur ceritanya menarik.",
            "Saya ingin makan nasi goreng dan makanan enak.",
            "Anak dan ibunya sedang bermain di rumah.",
            "Saya bermain game online di telepon genggam.",
            "Saya ingin membeli sabun dan produk perawatan kulit.",
            "Dokter memberi obat untuk penyakit dan perawatan pasien.",
            "Saya berobat ke psikolog atau psikiater karena gangguan mental.",
            "Hubungan pacaran dan pernikahan yang tidak harmonis.",
            "Artis dan selebriti terlibat skandal hiburan.",
            "Saya melihat foto, video lucu dan konten di media sosial.",
            "Pertikaian antarnegara, perang dan senjata nuklir.",
            "Harga barang dan keadaan ekonomi negara memburuk.",
            "Saya kecewa dengan presiden dan parlemen negara ini.",
            "Resep masakan dan cara memasak makanan di rumah.",
            "Saya membeli baju, sepatu dan barang belanjaan.",
            "Anak saya masih balita dan belajar di sekolah dasar.",
            "Cara mengedit foto dan video menggunakan aplikasi.",
            "Saya sedang bercerita tentang pengalaman pribadi dan keluarga.",
        ],
    },
    "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "revision": "e8f8c211226b894fcb81acc59f3b34ba3efd5f42",
    "model_cache_dir": ".cache/social_nlp/models",
    "stride": 24,
    "cache_dir": ".cache/context_relevance",
    "batch_size": 32,
    "threads": 4,
    "max_tokens": 128,
    "accept_score": 0.42,
    "accept_margin": 0.035,
    "other_score": 0.42,
    "context_score": 0.50,
    "context_direct_floor": 0.22,
    "context_max_words": 14,
}


class LocalSemanticBackend:
    """SBERT prototypes; scores are cosine similarities, never probabilities."""

    def __init__(self, config, *, source_data=None):
        import torch
        from huggingface_hub import snapshot_download
        from sentence_transformers import SentenceTransformer

        from MachineLearning.social_nlp import SocialNLPClusterer

        self.torch, self.config = torch, config
        self.clean = SocialNLPClusterer._clean
        torch.set_num_threads(config["threads"])
        snapshot = Path(
            snapshot_download(
                config["model"],
                revision=config["revision"],
                token=False,
                cache_dir=config["model_cache_dir"],
                allow_patterns=[
                    "*.json",
                    "vocab.txt",
                    "1_Pooling/config.json",
                    "model.safetensors",
                ],
                ignore_patterns=["onnx/*", "openvino/*"],
            )
        )
        weights = snapshot / "model.safetensors"
        if not weights.is_file():
            raise ValueError("Relevance inference requires safetensors weights")
        self.encoder = SentenceTransformer(
            str(snapshot),
            device="cpu",
            local_files_only=True,
            trust_remote_code=False,
            model_kwargs={"use_safetensors": True},
        ).eval()
        self.encoder.max_seq_length = config["max_tokens"]
        self.vectors = {}
        if source_data is not None:
            model = source_data["summary"]["config"]["model"]
            if any(
                model[key] != config[other]
                for key, other in [
                    ("repo", "model"),
                    ("revision", "revision"),
                    ("max_tokens", "max_tokens"),
                    ("stride", "stride"),
                ]
            ):
                raise ValueError("Source embeddings differ from relevance encoder")
            vectors = source_data["embeddings"]
            if not np.isfinite(vectors).all() or not np.allclose(
                np.linalg.norm(vectors, axis=1), 1, atol=1e-5
            ):
                raise ValueError("Reused source vectors must be finite and normalized")
            self.vectors.update(zip(source_data["sentences"].embedding_text, vectors))
        self.reference_vectors = {
            label: self.encode(config["references"][label])
            for label in ("relevant", "generic", "irrelevant")
        }
        with weights.open("rb") as stream:
            weights_hash = file_digest(stream, "sha256").hexdigest()
        if (
            source_data is not None
            and source_data["summary"]["model"].get("weights_sha256") != weights_hash
        ):
            raise ValueError(
                "Relevance encoder weights differ from the verified source"
            )
        self.identity = {
            "repo": config["model"],
            "revision": config["revision"],
            "weights_sha256": weights_hash,
            "device": "cpu",
            "score": "maximum cosine to reference examples; NOT probability",
            "pooling": "SBERT overflow windows mean followed by L2 normalization",
            "reused_source_manifest_sha256": source_data["artifact_manifest_sha256"]
            if source_data
            else None,
        }

    def encode(self, texts):
        clean = [self.clean(t) for t in texts]
        missing = [t for t in dict.fromkeys(clean) if t not in self.vectors]
        c = self.config
        for start in range(0, len(missing), c["batch_size"]):
            batch = missing[start : start + c["batch_size"]]
            tokens = self.encoder.tokenizer(
                batch,
                truncation=True,
                max_length=c["max_tokens"],
                stride=c["stride"],
                return_overflowing_tokens=True,
                padding=True,
                return_tensors="pt",
            )
            owners = tokens.pop("overflow_to_sample_mapping").numpy()
            pooled = [[] for _ in batch]
            with self.torch.inference_mode():
                for offset in range(0, len(owners), c["batch_size"]):
                    features = {
                        k: v[offset : offset + c["batch_size"]]
                        for k, v in tokens.items()
                    }
                    vectors = self.encoder(features)["sentence_embedding"].cpu().numpy()
                    for owner, vector in zip(
                        owners[offset : offset + c["batch_size"]], vectors
                    ):
                        pooled[int(owner)].append(vector)
            for text, windows in zip(batch, pooled):
                vector = np.mean(windows, axis=0)
                self.vectors[text] = vector / max(float(np.linalg.norm(vector)), 1e-12)
        return np.asarray([self.vectors[t] for t in clean])

    def __call__(self, texts, labels):
        vectors = self.encode(texts)
        return np.column_stack(
            [
                np.clip((vectors @ self.reference_vectors[label].T).max(axis=1), 0, 1)
                for label in labels
            ]
        )
