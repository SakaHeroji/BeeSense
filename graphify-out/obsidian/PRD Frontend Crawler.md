---
type: product-requirements
status: frontend-implemented-backend-pending
tags: [beesense, prd, crawler, react, survey]
---

# PRD Frontend Crawler

Spesifikasi produk tanggal 29 Oktober 2026. Implementasi ReactJS tersedia pada [[Frontend React Crawler]], dengan mode simulasi dan typed API adapter. Backend worker/API untuk antarmuka ini masih perlu dibangun. Dashboard aktif tetap menggunakan Streamlit.

[Indeks PRD](../../PRD/README.md) · [PRD utama](<../../PRD/PRD Frontend/PRD Frontend Crawler.md>) · [Rancangan layar](<../../PRD/PRD Frontend/Rancangan Layar Crawler.md>) · [Acceptance criteria](<../../PRD/PRD Frontend/Acceptance Criteria Crawler.md>)

Sistem direncanakan mempunyai tiga frontend: Crawler, NLP Machine Learning, dan Dashboard. Frontend Crawler mempunyai dua menu utama:

- **Crawler Otomatis**: discovery melalui query/platform/filter, target qualified, satu deadline, monitor, dan hasil.
- **Crawler Manual**: Input URL tertentu tanpa discovery tambahan, serta Data Survei calon mahasiswa/orang tua melalui form operator atau impor CSV/XLSX.

[[Crawler Selenium]] dan [[Crawling 1000 Post Baru]] memberikan dasar perilaku akuisisi sosial: deduplikasi historis, angka post/komentar terpisah, CAPTCHA manusia pada sesi worker, cooldown 429, serta hasil parsial. API persisten dan wrapper job untuk React masih perlu dibuat; browser operator tidak menjalankan crawler tiga jam.

Survei merupakan kemampuan baru. Provenance, peran yang dideklarasikan, ID respons/pertanyaan, versi survei, dan izin pemanfaatan harus dipertahankan dalam skema berversi. Data sosial tidak otomatis mempunyai peran calon mahasiswa/orang tua. Workbook ringkas sosial sepuluh kolom belum memenuhi seluruh metadata survei.

Dataset terbit immutable dengan versi/checksum. Handoff NLP membawa referensi dataset dan penerimaan parsial, tanpa otomatis training atau mengganti snapshot [[Dataset Dashboard]]. Target 20 topik/coherence dibahas terpisah di kebutuhan machine learning dan [[Metodologi Machine Learning Social NLP]].

Struktur dokumentasi: `PRD/PRD Frontend`, `PRD/PRD Backend`, dan `PRD/PRD Machine Learning`. Hanya PRD frontend Crawler yang dirinci sekarang; dua folder lain menampung dependensi untuk PRD berikutnya.

Graphify menelusuri kemampuan crawler yang menjadi dasar PRD dan pemetaan implementasi React. Catatan kurasi ini membedakan kebutuhan produk dari integrasi backend yang belum tersedia.

[[Arsitektur BeeSense]] · [[HOME]]

## Revisi visual dan kanal

PRD 1.1 memuat tema putih–oranye, teks hitam minimum 13 px, serta tujuh sumber: YouTube, Reddit, Instagram, TikTok, Threads, Facebook, dan X/Twitter. Rincian token pada §14.1 dan dukungan adapter pada §6.4. [[Frontend React Crawler]] telah mengikuti kontrak UI ini; integrasi lima adapter baru tetap menjadi pekerjaan backend.
