---
type: runbook
tags: [beesense, github, verification]
---

# Menjalankan BeeSense

Instal Python 3.12 dan requirements.txt dalam virtualenv. Dari root proyek:

    python -m scripts.verify_dashboard_data
    python -m streamlit run nlp_dashboard.py --server.address=127.0.0.1 --server.port=8501

Dashboard langsung membaca [[Dataset Dashboard]] tanpa login, browser crawler atau model download. README menjelaskan training/crawl baru, tes offline dan opsi Docker.

[GitHub Actions](../../.github/workflows/ci.yml) menguji dataset/checksum, NLP/UI, crawler dan helper parser. Kode, tes dan satu dataset aktif dilacak Git untuk repository [SakaHeroji/BeeSense](https://github.com/SakaHeroji/BeeSense), branch main. Status lokal dapat diperiksa dengan git status; hasil CI tersedia pada tab Actions. Environment, browser profile, cache dan run lain diabaikan.

[Dockerfile](../../Dockerfile.nlp) memakai user non-root dan artifact read-only. Build/runtime Docker belum diverifikasi karena daemon lokal belum aktif. Tidak perlu migrasi database.

[README](../../README.md) · [[Arsitektur BeeSense]] · [[HOME]]
