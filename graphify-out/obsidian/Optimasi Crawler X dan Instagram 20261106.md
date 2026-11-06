---
type: architecture
tags: [beesense, crawler, twitter, instagram, performance]
captured_at: 2026-11-06
---

# Optimasi Crawler X dan Instagram 20261106

[[TwitterCrawler Scweet]] dan [[InstaloaderCrawler]] menggunakan konfigurasi serta
kontrak ekspor bersama. Audit dan patch 6 November mengurangi request yang tidak
diperlukan tanpa menurunkan interval request, kuota atau proteksi akses.

- X: jendela tanggal berurutan tidak mengulang hari batas; root hasil pencarian
  disaring tanggal/keyword sebelum meminta replies.
- Instagram: root disaring sebelum komentar; komentar utama mendahului balasan;
  iterator balasan dibuat lazy dan first_data memakai halaman sumber yang valid.
- Cap komentar nol tidak membuka iterator; halaman web terakhir meminta sisa cap.
- Pagination web tanpa kemajuan menghasilkan PARTIAL dan mempertahankan baris;
  cursor berulang tidak menjadi bukti kelengkapan.
- SERVER_UNAVAILABLE berhenti pada 5xx pertama dan menghormati jeda minimal 60
  detik/Retry-After. Cooldown Instagram disimpan antarrun di sidecar schema v1,
  mode 0600, tanpa cookie/token; worker baru tidak dibuat selama cooldown.
- root_rejection dipakai bersama selektor ekspor dan pemeriksaan awal; aturan
  tanggal serta include any/all dan exclude tidak diduplikasi.

Fixture offline membandingkan commit d896cade dengan patch: pencarian X tetap
4 operasi/29 hari, kunjungan hari berulang 3→0. Dua fixture Instagram membutuhkan
2→1 request simulasi dengan ID hasil tetap sama. Ini bukan benchmark live atau
jaminan bebas blokir. Tidak ada fork SDK, rotasi akun/proxy atau bypass CAPTCHA.

[Audit, benchmark dan perintah verifikasi](../../docs/crawler/PERFORMANCE_X_INSTAGRAM_20261106.md).
No migration required. Image Docker dan throughput live harus diverifikasi
terpisah dari tes offline.

Verifikasi: 223 tes relevan lulus, ditambah 6 tes unlimited (2 skip); formatter,
lint dan dry-run X/Instaloader lulus. Dua tes Selenium pada suite tambahan
terhalang dependensi belum terpasang. Daemon Docker tidak aktif.
