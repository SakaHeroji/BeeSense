---
type: runbook
tags: [beesense, github, verification]
---

# Menjalankan BeeSense

Instal Python 3.12 (direkomendasikan) atau 3.14 dan requirements.txt dalam virtualenv khusus dashboard. Dari root proyek:

    python -m scripts.verify_dashboard_data
    python -m streamlit run main.py --server.address=127.0.0.1 --server.port=8501

Dashboard langsung membaca [[Dataset Dashboard]] tanpa login, browser crawler atau model download. README menjelaskan training/crawl baru, tes offline dan opsi Docker.

[GitHub Actions](../../.github/workflows/ci.yml) menguji dataset/checksum, NLP/UI, crawler dan helper parser. Kode, tes dan satu dataset aktif dilacak Git untuk repository [SakaHeroji/BeeSense](https://github.com/SakaHeroji/BeeSense), branch main. Status lokal dapat diperiksa dengan git status; hasil CI tersedia pada tab Actions. Environment, browser profile, cache dan run lain diabaikan.

[Dockerfile](../../Dockerfile.nlp) memakai user non-root dan artifact read-only. Build/runtime Docker lokal sudah diverifikasi: `beesense-nlp:main`, container `beesense-dashboard`, health `healthy`, user 10001 dan artifact read-only pada http://127.0.0.1:8501. Tidak perlu migrasi database.

## Streamlit Community Cloud

Entry point repository adalah [main.py](../../main.py). Setelah source dan dataset di-push ke GitHub, pilih repository `SakaHeroji/BeeSense`, branch `main`, **Main file path `main.py`**, serta Python **3.12** pada Advanced settings. Cloud memasang `requirements.txt` → `requirements-dashboard.txt`, khusus pemuatan artifact dan UI. Python 3.14 juga didukung; environment training/crawler penuh tetap terpisah pada Python 3.12 melalui `requirements-dev.txt`/`requirements-sbert.txt`.

Sertakan `social_nlp.py`, `social_nlp.json`, `.streamlit/config.toml` dan seluruh snapshot aktif pada [[Dataset Dashboard]]. Biarkan `BEESENSE_NLP_RUN_DIR` tidak diatur; app membaca `output_dir` relatif dari JSON. `/data/nlp_run` adalah mount Docker lokal. Secrets dan training tidak diperlukan untuk membuka dashboard. [Panduan lengkap dan sumber resmi](../../README.md#deploy-ke-streamlit-community-cloud).

[README](../../README.md) · [[Arsitektur BeeSense]] · [[HOME]]

Training memakai `.venv-sbert` dan `requirements-sbert.txt`; Mac Intel dapat
memakai `requirements-sbert-macos-intel.lock`. Evaluasi c_v memakai Gensim pada
`requirements-coherence.txt`. Dashboard membaca artifact tanpa mengimpor Gensim/Torch.

    .venv-sbert/bin/python social_nlp.py --output-dir outputs/nlp_run_baru

Konfigurasi aktif menunjuk `outputs/nlp_20261029_combined_topics20_01` dan `outputs/social_20261029_combined/social_data.xlsx`; target 20 topik, rata-rata c_v 0,4720. Empat Parquet baru dan empat snapshot sebelumnya dipertahankan. Dashboard akhir diverifikasi non-root/read-only pada port 8501.

Jalur `--reuse-embeddings-from` memerlukan requirements-dev.txt pada Python 3.12 dan memverifikasi input/model/checksum sebelum refitting; tidak memerlukan Torch.

Reuse embedding dari arsip korpus lama ditolak untuk input gabungan yang berbeda. Gunakan environment SBERT untuk encoding baru, atau cache yang lolos pemeriksaan kecocokan seluruh korpus.

## Kegagalan deployment Python 3.14

Log pengguna 29 Oktober 2026 menunjukkan Python 3.14.10, ONNX Runtime 1.23.2 tanpa wheel cp314, serta Numba 0.61.2 yang menolak Python 3.14. Root requirements lama memuat lock training. Perbaikannya memisahkan dependency dashboard, memakai NumPy 2.3.5 pada Python ≥3.14 dan mempertahankan NumPy 2.2.6 pada versi lebih lama. Artifact/model tetap memakai checksum sebelumnya dan tidak di-training ulang.

Job CI `dashboard-runtime` menginstal wheel saja pada Python 3.12/3.14, memeriksa konsistensi paket, lalu membuka kelima tampilan/topik terpilih dari snapshot terbitan tanpa library training. Root requirements harus dipakai dalam environment bersih. Setelah push, biarkan Cloud memperbarui dependency; Reboot app jika masih menampilkan error lama. [Analisis dan perintah](../../README.md#error-instalasi-pada-python-314).
