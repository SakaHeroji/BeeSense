---
type: architecture
tags: [beesense, crawler, instagram, instaloader, experiment]
---

# InstaloaderCrawler

Class standalone baru di `Crawler/Backend/instaloader_crawler.py`, Instaloader 4.16,
mewarisi coordinator dan exporter [[InstagramCrawler instagrapi]]. Kontrak Excel,
native ID/parent, dedup baseline dan filter tetap sama. Preset eksperimen maksimal
300 detik/10 post dengan minimal 1 komentar per qualified post dan tanpa retry 429.
SocialCrawler 1.6.0 kini memakai worker Instaloader yang sama sebagai backend Instagram default; [[Dataset Dashboard]] aktif tidak dilatih ulang oleh pergantian backend ini.

Patch runtime `instaloader_browser_patch.py` mengirim GraphQL lewat `/api/graphql`
berdasarkan patch pengguna/issue #2767: token web dan header lengkap, cache token
per context/session, signature 4.16. Satu worker mempertahankan rate controller;
5 detik minimum antarrekuest dan hard deadline tetap berlaku. Metadata discovery
dipakai kembali; komentar default memakai NodeIterator query_hash sesuai PR #2692,
reply dibatasi preview. Opsi web_doc_id dari issue #2651 masih eksperimental dan
tidak memberi connection yang diharapkan pada post uji.
Auth/sesi JSON lokal diabaikan Git; token/password tidak masuk log atau workbook.

Uji 30 Oktober: trial01 discovery berhasil tetapi detail ditolak; trial02 membuktikan
HTTP 400/feedback_required. Ini belum membuktikan akun diblokir atau password salah.
Trial03 membaca metadata melalui web, tetapi post tersaring tanggal dan komentar
mobile gagal. Setelah patch lengkap, trial04 membaca 3 post nyata dalam 27,67 detik,
0 invalid/429. Ketiganya comment_count 0; verifikasi komentar dilakukan terpisah.
Trial05 membaca post tetapi query web_doc_id gagal. **Trial06 berhasil: 1 post dan
20 komentar nyata dalam 26,56 detik**, TARGET_MET/trial_passed true, 0 invalid/429,
0 balasan. Komentar dibatasi 20 dan tidak diklaim lengkap. Patch metadata web +
NodeIterator komentar merupakan jalur teruji singkat, bukan jaminan run panjang.
Uji satu post lama melepaskan filter tanggal hanya di config diagnostik, bukan preset
atau dataset training. Seluruh hasil berada di `outputs/instagram_instaloader_20261030_trial*/`.
Trial05/06 sengaja memakai permalink sama untuk perbandingan, sehingga tetap
merupakan bundle diagnostik terpisah dan harus didedup bila kelak digabung.

21 tes khusus lulus; suite crawler lengkap 144 tes (143 lulus/1 skip). Dockerfile
disediakan, tetapi daemon lokal tidak aktif sehingga build/start belum terverifikasi.
No migration required. Uji singkat tidak menjamin bebas pembatasan pada run panjang.

[Panduan dan bukti](../../docs/crawler/INSTALOADER_CRAWLER.md) ·
[Class](../../Crawler/Backend/instaloader_crawler.py) ·
[Patch](../../Crawler/Backend/instaloader_browser_patch.py) ·
[Config](../../config/instaloader_crawler.json) · [[Arsitektur BeeSense]]

## Backend default gabungan 1.6.0

SocialCrawler memilih InstaloaderWorker/InstaloaderSettings yang sama, dengan provenans instaloader_saved_web_session. Preset full memakai instaloader, target 1.000 post/10.800 detik/minimum 10 komentar. Preset resume historis mempertahankan sisa target 870 qualified post/6.065 detik. Keduanya memakai retry 429 nol. Opsi retry eksplisit memakai cooldown scheduler dengan context tetap hidup tanpa request selama menunggu. Validasi opsi dibagi dengan class standalone. Tes mencakup lifecycle worker, routing default, format Excel, dedup/cursor dan ekspor lintas platform. Dependency dan allowlist Docker crawler/Selenium/browser ikut diperbarui.
