# Struktur proyek BeeSense

Pemindahan folder dilakukan setelah integrasi Reddrix ke SocialCrawler 1.4.0 selesai. Kode dikelompokkan mengikuti komponen aplikasi; dataset, manifest, model tersimpan, dan isi workbook tidak dipindahkan atau diubah.

```text
BeeSense/
├── streamlit_apps.py                       # Entry point Streamlit Community Cloud
├── requirements.txt              # Entry point dependency Cloud
├── Crawler/
│   ├── Frontend/                 # React, Vite, UI akuisisi
│   └── Backend/
│       ├── social_crawler.py     # YouTube yt-dlp + Reddit Reddrix
│       ├── reddit_crawler.py     # Pembungkus Reddit-only
│       ├── twitter_crawler.py    # Percobaan X/Twitter mandiri, Scweet dan Excel bersama
│       ├── instagram_crawler.py  # Scheduler/filter/Excel Instagram, instagrapi atau Chrome
│       ├── instagram_browser.py  # Worker profil Chrome persisten, login manual
│       ├── instagram_browser_capture.mjs  # Parser ID/komentar dokumen post
│       ├── social_export.py      # Seleksi dan proyeksi Excel bersama
│       ├── social_crawler_selenium.py
│       ├── Reddit/               # Kontrak, parser, helper, resource legacy
│       └── Youtube/              # Adapter yt-dlp dan kontrak
├── MachineLearning/social_nlp.py
├── Dashboard/app.py
├── config/                       # social_crawler.json, reddit_crawler.json, social_nlp.json
├── requirements/                 # dashboard, crawler, reddrix, selenium, dev, nlp, sbert, coherence
├── deployment/docker/            # Dockerfile.dashboard, Dockerfile.crawler, Dockerfile.selenium
├── docs/                         # crawler/, machine-learning/, dashboard/, notes/
├── tests/                        # crawler/, nlp/, cloud/
├── scripts/
├── PRD/
├── outputs/                      # Dataset dan artifact versi tetap
├── output/                       # Log/cache/pekerjaan lokal, diabaikan Git
└── graphify-out/                  # Graf dan vault Obsidian
```

## Perintah dari root repository

```sh
python -m pip install -r requirements.txt
python -m streamlit run streamlit_apps.py

python -m pip install -r requirements/crawler.txt
reddrix install
python -m Crawler.Backend.social_crawler --dry-run
python -m Crawler.Backend.reddit_crawler --dry-run
python -m Crawler.Backend.social_crawler_selenium --dry-run

python -m MachineLearning.social_nlp --help
python -m scripts.verify_dashboard_data --check-git

python -m unittest discover -s tests/crawler -v
python -m unittest discover -s tests/nlp -v
python -m unittest discover -s tests/cloud -v
```

Tes Cloud memakai environment terpisah yang hanya memasang requirements.txt. Tes NLP memerlukan requirements/dev.txt. Untuk menjalankan crawling live, berikan output-dir baru pada module CLI; dry-run tidak mengambil data.

## Import Python dan path

```python
from Crawler.Backend.social_crawler import SocialCrawler
from Crawler.Backend.reddit_crawler import RedditCrawler
from MachineLearning.social_nlp import SocialNLPClusterer
from Dashboard.app import SocialNLPStreamlitApp
```

ROOT pada pipeline crawler/NLP menunjuk root repository berdasarkan lokasi package, sehingga konfigurasi di config/ dan input/output relatif tetap konsisten. Resource adapter yang berdampingan dengan kode, seperti rendered_thread_dom.mjs dan contract.json, tetap disimpan bersama adapternya. Worker spawn mengimpor module package baru. streamlit_apps.py hanya mendelegasikan rendering UI; Streamlit Cloud tetap memakai branch main dan Main file path streamlit_apps.py.

requirements.txt meneruskan ke requirements/dashboard.txt. Include antarfile dependency di requirements/ memakai path relatif dalam folder yang sama. Dockerfile memakai konteks root repository dan mempertahankan direktori package/config di image:

```sh
docker build -f deployment/docker/Dockerfile.dashboard -t beesense-dashboard:local .
docker build -f deployment/docker/Dockerfile.crawler -t beesense-social-crawler:local .
docker build -f deployment/docker/Dockerfile.selenium -t beesense-selenium:local .
```

Tidak ada perubahan schema database atau kontrak data: **No migration required**. Docker build/runtime setelah reorganisasi belum diverifikasi bila daemon lokal tidak tersedia; pemeriksaan path/COPY tidak menggantikan build image.

Percobaan instagrapi memakai `config/instagram_crawler.json`, `requirements/instagram.txt`
dan `deployment/docker/Dockerfile.instagram`. Jalur Chrome memakai
`config/instagram_browser_crawler.json`, `requirements/instagram-browser.txt` dan
`deployment/docker/Dockerfile.instagram-browser`, dengan Node/CLI/Chrome tersendiri. Lihat
[panduan Instagram](crawler/INSTAGRAM_CRAWLER.md). `config/auth.json` berisi rahasia
lokal dan diabaikan Git; sesi di `output/instagram/session.json` baru dibuat setelah
login berhasil. Profil browser khusus berada di `output/instagram_browser/chrome_profile`.
Trial Chrome lama mengambil 76 post/910 komentar sebelum dihentikan pengguna.
Integrasi Instagram dalam SocialCrawler 1.5 kini tersedia; preset Instagram-only
`config/social_crawler_instagram_3h.json` menjalankan target 1.000 post dalam tiga jam.
Model/dashboard tiga platform sedang disiapkan; konfigurasi aktif baru diganti setelah gate model lolos. Pemindahan tiga metode seleksi/Excel ke SocialExportMixin mempertahankan
perilaku exporter YouTube/Reddit.

`MachineLearning/topic_narratives.py` menangani transport/validasi Gemini untuk tahap `SocialNLPClusterer.generate_topic_narratives()`. CSV masuk direktori model versi baru; dashboard membaca hasil tanpa key. Panduan operasional: `docs/machine-learning/GEMINI_TOPIC_NARRATIVES.md`.
