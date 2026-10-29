---
type: implementation
status: frontend-implemented-backend-pending
tags: [beesense, react, crawler, frontend, survey]
---

# Frontend React Crawler

[Crawler/Frontend](../../Crawler/Frontend/README.md) mengimplementasikan [[PRD Frontend Crawler]] dengan ReactJS, TypeScript, Vite, React Router, dan TanStack Query. Dua menu utama tetap Crawler Otomatis dan Crawler Manual; Manual berisi URL, survei, dan riwayat.

## Pemisahan lingkungan

Development memakai adapter simulasi dengan banner tetap. Tidak ada crawling, training, atau perubahan dataset nyata. Metadata pekerjaan sintetis disimpan di browser untuk membuka kembali monitor; jawaban survei dan indeks respons demo hanya berada di memori.

Build produksi memakai mode API secara default dan tidak fallback ke demo saat backend gagal. [`api.ts`](../../Crawler/Frontend/src/shared/api.ts) menyiapkan integrasi berbasis sesi, validasi rencana, idempotency key, polling snapshot, kontrol pekerjaan, validasi/commit survei, dataset berversi, dan handoff NLP. [Kontrak API](../../Crawler/Frontend/docs/API_CONTRACT.md) masih perlu diimplementasikan backend. [[Crawler Selenium]] dan SocialCrawler Python saat ini bukan HTTP server untuk SPA.

## Alur yang tersedia

- Wizard otomatis: query/platform, tanggal WIB, filter/target, baseline wajib, review, validasi, dan mulai.
- Monitor: roots/qualified/comments/replies terpisah, deadline server, stale/reconnect, cooldown/CAPTCHA, finalisasi, stop aman, grafik dan tabel.
- URL: host allowlist, locator/URL kanonik, native ID final tetap diverifikasi backend, deduplikasi dan daftar terpilih tanpa discovery tambahan.
- Survei: template minat-studi v1, formulir atau CSV/XLSX, pemilihan sheet, mapping, review, dan commit respons lengkap. Metadata peran/izin/pertanyaan tetap terpisah dari teks jawaban.
- Hasil: preview, kualitas, konteks, berkas sesuai izin, dan penerimaan eksplisit atas dataset parsial sebelum pemilihan input NLP. Skema survei dan lima sumber sosial baru belum divalidasi adapter NLP, sehingga handoff dataset tersebut diblokir pada simulasi.

Audit UI/UX mengikuti skill frontend-design dan web-design-guidelines: kontras teks, label/error terhubung, validasi per langkah, deep link tab, dialog, dan navigasi mobile berkeyboard. [Catatan delivery](../../Crawler/Frontend/docs/DELIVERY.md) memisahkan hasil verifikasi frontend dari kemampuan backend yang belum ada.

## Menjalankan

`cd Crawler/Frontend && npm ci && npm run dev` membuka http://127.0.0.1:5173. Docker baru memakai Nginx UID 101 pada port 8080, health `/healthz`, dan SPA fallback; terpisah dari Dashboard Streamlit. Tidak ada perubahan skema database atau migrasi.

[[Arsitektur BeeSense]] · [[PRD Frontend Crawler]] · [[Dataset Dashboard]] · [[HOME]]

## Tema dan tujuh sumber

Versi PRD 1.1 menetapkan permukaan putih `#FFFFFF`, canvas `#FAFAFA`, aksen oranye `#FF8A24`, hover `#FF7608`, latar lembut `#FFF3E8`, garis `#E6DDD5`, serta **seluruh teks hitam `#000000`, minimum 13 px**. Body/input 15 px; label/tombol 14 px. Logo, grafik, dan status memakai oranye/hitam/abu-abu tanpa hijau. Label grafik memakai HTML agar ukuran teks tidak menyusut bersama SVG.

Tujuh pilihan UI dan simulasi: YouTube, Reddit, Instagram, TikTok, Threads, Facebook, X/Twitter. Query, target, kartu progres, seri grafik, filter riwayat, dan preview menggunakan daftar platform yang sama. Lima tambahan default nonaktif dan dapat dipilih pada demo. Mode API hanya mengaktifkan capability yang dikirim server. Backend HTTP/worker belum tersedia; SocialCrawler Python tetap baru memiliki adapter YouTube/Reddit. Lima adapter baru dan pemetaan NLP merupakan dependensi terencana, bukan crawler yang sudah berjalan.
