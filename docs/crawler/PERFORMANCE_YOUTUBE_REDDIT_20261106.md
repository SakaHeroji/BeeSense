# Optimasi YouTube dan Reddit — 6 November 2026

Implementasi: SocialCrawler 1.11.0, adapter YouTube 0.2.0, yt-dlp 2026.10.21,
Reddrix 1.2.14. Konfigurasi bisnis dan auth tidak diubah. Analisis dimulai dari
query Graphify, kemudian diverifikasi pada source aplikasi dan SDK terpasang.

## Kelemahan dan perubahan

| Jalur | Kelemahan sebelumnya | Perubahan |
| --- | --- | --- |
| YouTube | Komentar dibuffer penuh oleh yt-dlp sebelum dikirim; timeout dapat kehilangan seluruh komentar yang telah dibaca | Extractor turunan mengirim komentar native satu per satu, deduplikasi ID, tanpa menyimpan ulang seluruh body dalam list SDK |
| YouTube | `request_delay` tidak diteruskan ke extractor; pencarian dapat merealisasikan seluruh playlist | `sleep_interval_requests` memakai delay konfigurasi, minimum 1 detik; pencarian lazy dan `islice` berhenti tepat pada batas |
| Keduanya | Tanggal dan keyword root diperiksa setelah komentar diambil | Pakai kebijakan `root_rejection` yang sama dengan exporter sebelum komentar; Reddit juga menyaring metadata kandidat pencarian |
| Reddit | Setelah cap tercapai collector tetap menguras iterator; SDK dapat meneruskan kunjungan halaman tanpa mengeluarkan item | Tutup generator secara eksplisit segera setelah cap, root ditolak, atau metadata-only |
| Reddit | SDK dapat menjalankan 10 request bersamaan, mencoba ulang barrier hingga 5 kali, dan memperbarui sesi | Serialisasi GET/POST, tunggu setelah respons selesai, panggil implementasi sekali tanpa retry tersembunyi; inisialisasi hanya satu percobaan |
| Keduanya | Operasi tanpa cap dapat terlalu lama berada pada thread yang tidak memberi ID baru | Setelah 75 detik tanpa progres native ID, hentikan sebelum request berikutnya dengan `PARTIAL`; Reddit juga mendeteksi request/cursor berulang |
| Keduanya | Status HTTP bisa hilang di dalam fallback SDK | Barrier melekat pada worker: 401/403, 429 dan 5xx mencegah request lanjutan; `Retry-After` angka/tanggal dipertahankan |

`max_comments: 0` kini valid untuk metadata-only. `null` tetap tanpa cap.
Pembatasan balasan dan normalisasi ID/parent yang ada tetap berlaku.
Kontrak event dan tabel ekspor tidak berubah; coordinator tetap menyimpan hasil
yang telah diterima ketika child timeout atau operasi menjadi parsial.

## Kebijakan request

YouTube memakai opsi jeda extractor resmi yt-dlp; bukan jeda download media.
Reddit memakai satu lock per worker dan interval minimum 1 detik setelah respons
sebelumnya selesai. Mode delay acak memakai batas atas konfigurasi untuk interval
internal, sementara scheduler tetap mengatur jeda antaroperasi.

Pada 429, YouTube berhenti untuk run tersebut. Reddit menyerahkan retry kepada
scheduler yang sudah mempunyai cooldown, batas retry dan anggaran waktu; server
`Retry-After` tidak dipendekkan. Pada 5xx, platform berhenti dengan
`SERVER_UNAVAILABLE`, sehingga tidak ada pelipatan backoff tanpa batas. Barrier
akses/challenge tidak memicu refresh sesi atau retry otomatis di transport.

Stagnasi diperiksa pada batas request; ini bukan timer yang memutus I/O tepat
pada detik ke-75. Socket timeout SDK dan hard deadline subprocess tetap berlaku.
Tidak ada rotasi akun/proxy atau peningkatan paralelisme.

## Bukti offline

Baseline berasal dari fungsi worker/collector pada commit yang dicatat lengkap
dalam `output/youtube_reddit_performance_20261106/benchmark.json`. Script mengambil
fungsi tersebut melalui AST dan membandingkannya dengan fungsi sekarang.

| Fixture | Sebelum | Sesudah | Identitas hasil |
| --- | --- | --- | --- |
| Dua video, satu tidak cocok keyword | 20 halaman komentar sintetis | 10 halaman, turun 50% | 101 ID hasil sama |
| Reddit cap 10 komentar, 20 halaman continuation sintetis | 20 kunjungan halaman | 1 halaman, turun 95% | 11 ID hasil sama |
| YouTube gagal setelah dua komentar | Hanya 1 root tersimpan | 1 root + 2 komentar tersimpan | Progres komentar terselamatkan |

Fixture Reddit memodelkan pagination berurutan yang tetap tersedia setelah SDK
mencapai cap item. Cabang SDK nyata dapat sudah terjadwal sebelum collector
menerima root; penghentian iterator dan gate mencegah request berikutnya, tetapi
tidak membatalkan respons yang sudah terlanjur diterima. Angka di atas adalah
penghematan pekerjaan sintetis, **bukan pengukuran request HTTP atau throughput
live**, dan tidak menjamin seluruh thread turun 95%.

Reproduksi dengan SHA `baseline_commit` dari JSON:

```sh
.venv-reddrix/bin/python -m scripts.benchmark_youtube_reddit --baseline <SHA-40-karakter>
PYTHONPATH=.:tests/crawler .venv-reddrix/bin/python -m unittest tests.crawler.test_youtube_reddit_performance tests.crawler.test_reddit_crawler tests.crawler.test_social_crawler_reddrix tests.crawler.test_social_crawler tests.crawler.test_unlimited_crawling tests.crawler.test_crawler_config -q
```

Validasi: 96 tes dijalankan, **94 lulus dan 2 SDK opsional dilewati**, termasuk
21 tes baru untuk streaming, filter, metadata-only, cursor berulang, pacing,
stagnasi, status/Retry-After, serta kompatibilitas hook SDK nyata tanpa jaringan.
Ruff lint/format untuk modul baru, coordinator, script dan tes terkait lulus;
kompilasi kedua adapter lama lulus. Dry-run SocialCrawler dan wrapper Reddit,
serta entry point CLI YouTube langsung lulus. Tidak ada crawl sosial live baru.

## Batas dan pekerjaan lanjutan

- Tidak ada cara menjamin akun/IP tidak diblokir. Pacing dan penghentian barrier
  mengurangi request yang sia-sia; kebijakan platform tetap menentukan akses.
- Reddrix masih membutuhkan startup browser per operasi. Cache sesi lintas
  worker belum ditambahkan. Backend HTML/Playwright lama tidak menggunakan gate
  Reddrix ini.
- Hook `_get_comments`, `__post_extractor`, `get/post.__wrapped__` dan client SDK
  bersifat internal. Dependency tetap dipin; upgrade wajib melewati tes ini.
  Reddrix dengan hook tak dikenal ditolak sebelum crawling.
- Tanggal YouTube yang hanya berupa `upload_date` tetap tidak dianggap waktu
  publikasi exact. Jika filter tanggal aktif, tanggal tak diketahui ditolak,
  sama dengan kebijakan exporter sebelumnya.
- Cooldown tidak dipersistenkan lintas restart untuk dua backend ini. Setelah
  barrier, operator perlu mengikuti `Retry-After` sebelum memulai run baru.
- Pencarian Reddrix masih mengikuti relevance hardcoded upstream; perubahan sort
  pencarian dan pemakaian API resmi memerlukan pekerjaan terpisah.

## Delivery

**No migration required.** Tidak ada perubahan skema atau semantik data tersimpan.
Allowlist konteks Docker crawler disesuaikan agar dua modul baru ikut image;
Dockerfile, environment dan startup produksi tidak diubah. Daemon Docker tidak
tersedia; image belum dibangun atau dijalankan ulang. Status: **Not fully verified**
untuk image dan performa live. Pemeriksaan setelah Docker aktif:

```sh
docker build -f deployment/docker/Dockerfile.crawler -t beesense-crawler:local .
docker run --rm beesense-crawler:local --dry-run
```

Rujukan primer: [opsi yt-dlp](https://github.com/yt-dlp/yt-dlp#workarounds),
[source Reddrix](https://github.com/Coding-Doctor-Omar/reddrix).

Peta lokal: [[Optimasi Crawler YouTube dan Reddit 20261106]] di vault
`graphify-out/obsidian`; node source dan hubungan impor ada di subfolder `graph/`.
