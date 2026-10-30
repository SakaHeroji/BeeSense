---
type: architecture
status: reorganized-paths-verified
tags: [beesense, structure, python, deployment]
---

# Struktur Proyek

Reorganisasi dilakukan setelah integrasi [[RedditCrawler Reddrix]] ke SocialCrawler 1.4.0 selesai. Kode berada di Crawler/Backend, MachineLearning dan Dashboard; frontend React tetap di Crawler/Frontend. Config berada di config/, dependency di requirements/, panduan di docs/, Docker di deployment/docker/. Tes crawler berada di tests/crawler, tes NLP dan Cloud tetap pada folder masing-masing.

streamlit_apps.py tetap di root sebagai entry point Streamlit Cloud dan mendelegasikan ke Dashboard.app. requirements.txt tetap di root dan menyertakan requirements/dashboard.txt. Modul Python menggunakan import package; CLI dijalankan dari root dengan python -m Crawler.Backend.social_crawler atau python -m MachineLearning.social_nlp. ROOT crawler/NLP tetap menunjuk root repository sehingga path input/output tidak mengikuti direktori package.

Dataset outputs/, model/artifact dan hasil crawling historis tidak dipindahkan. Pemindahan tidak memulai crawling atau training. Tidak ada perubahan kontrak data/database: No migration required. Docker build setelah reorganisasi belum diverifikasi karena daemon lokal tidak aktif.

[Peta lengkap dan perintah](../../docs/PROJECT_STRUCTURE.md) · [[Arsitektur BeeSense]] · [[Menjalankan BeeSense]] · [[HOME]]
