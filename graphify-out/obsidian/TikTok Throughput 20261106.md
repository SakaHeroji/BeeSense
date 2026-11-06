---
type: architecture
tags: [beesense, crawler, tiktok, chrome, throughput]
captured_at: 2026-11-06
---

# TikTok Throughput 20261106

## Peningkatan throughput — Connector 1.3.0, 6 November 2026

Build `20261106-throughput-v6` menggunakan dua fase per post: kumpulkan komentar
utama sampai akhir pagination sumber (atau cap yang dikonfigurasi), kemudian
rewind panel dan telusuri balasan. Balasan bawaan dalam respons komentar tetap
disimpan; klik balasan ditunda sampai fase kedua.

`platforms.tiktok.comment_stagnation_seconds` default 75 (rentang 60–90).
Hanya ID komentar/balasan baru yang mereset timer; respons berulang atau metadata
post tidak meresetnya. Post yang stagnan mengirim status `PARTIAL` dan warning
`comment_stagnation_timeout`. Koordinator mengekspor progres, melanjutkan kandidat
baru dan pencarian, lalu mencoba ulang post parsial. `partial_retry_limit`
default 1 (rentang 0–3). Retry tetap tunduk target, deadline global dan cap post;
retry tidak menambah hitungan post yang dicoba atau menggandakan native ID.
Antrean belum selesai tersimpan dalam `tiktok_retry_queue.json` di bundle beserta
checksum manifest; tidak otomatis diimpor oleh run baru. `comments_complete`
tetap false. PARTIAL tidak lagi menghentikan seluruh kampanye.

Jeda minimum tetap mengikuti `request_interval_seconds` / `scroll_pause_seconds`.
Penalti idle tambahan dihapus. Setelah aksi, controller menunggu request relevan
beserta body respons, maksimal 10 detik; `Network.loadingFailed` melepaskan request.
Respons post lain tidak memengaruhi barrier, pacing atau data post aktif.
Backoff HTTP 5xx adalah 5/10/15 detik (maksimum 15), reset setelah HTTP 2xx.
Tiga 5xx beruntun memicu pause minimal 30 detik dan menghormati Retry-After yang
lebih panjang. Status pause dibagikan antar tugas agar perpindahan post tidak
melewati cooldown. 401/403/429 dan CAPTCHA tetap memakai penanganan sebelumnya.

Bridge mensyaratkan Connector >=1.3.0 agar timer run tidak dimulai dengan kode
lama. Reload ekstensi dari `Crawler/Backend/Tiktok/chrome_extension` dan pairing
ulang sebelum uji live. Izin dan ID ekstensi tidak berubah. Tidak ada migrasi DB.
Dockerfile native tetap menyalin package lengkap; Docker daemon lokal tidak aktif,
sehingga rebuild belum diverifikasi. Jalankan ketika Docker tersedia:
`docker build -f deployment/docker/Dockerfile.tiktok -t beesense-tiktok:local .`
lalu `docker run --rm beesense-tiktok:local --dry-run`.

Pengujian menggunakan fixture offline, termasuk 1.200 komentar +100 balasan
sintetis, bukan bukti kecepatan TikTok live. Uji yang diminta berikutnya: target
50 post, maksimal 3.600 detik, timer dimulai setelah pairing versi/build terverifikasi.

Terkait: [[TikTok Chrome Live Connector]] · [[Pemantauan TikTok 1000 Post 20261105]]


## Hasil uji live 50 post / 1 jam

Run `social_20261106T023450Z_12916634` memakai handshake Connector 1.3.0 /
`20261106-throughput-v6`, mulai 6 November 2026 pukul 09.34.50 WIB dan mencapai
deadline pukul 10.34.50 WIB. Finalisasi selesai setelah 3.603,53 detik. Hasil
**10 post, 1.348 komentar, 481 balasan** = **1.839 ID native unik**, nol duplikat;
seluruh **13 checksum** bundle cocok. Provenans seluruh record adalah
`beesense_existing_chrome_live`. Status PARTIAL / TIME_BUDGET_EXHAUSTED; target
50 belum tercapai. Dari 22 post yang dicoba, 11 di luar tanggal dan 1 tanpa
include keyword. Enam post parsial masih tercatat pada antrean; thread terakhir
berakhir TIMEOUT karena deadline. `comments_complete` tetap false.

Bundle: `output/crawler_runs/social_20261106T023450Z_12916634/`.
Perbaikan stagnasi tidak membatasi total durasi thread yang masih terus menambah
ID baru; prioritas throughput versus kelengkapan balasan tetap perlu dievaluasi.
