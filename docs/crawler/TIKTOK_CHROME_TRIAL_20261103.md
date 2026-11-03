# Uji TikTok melalui Chrome pengguna — 3 November 2026

Hasil: **1 post,10 komentar,0 balasan** diamati dan diimpor ke exporter bersama.
Target500post belum tercapai. Tidak menjalankan pengambilan500post selama30menit;
1800detik merupakan batas maksimum impor, bukan durasi crawling live. Komentar
belum lengkap. Angka15 pada metadata/14 pada UI bukan bukti15komentar berhasil
tersimpan. Ada10ID komentar yang teramati, sisanya tidak dibuatkan ID sintetis.

## Jalur sebenarnya

1. Sesi Chromium mandiri14:49:43WIB dihentikan melalui cancel setelah pengguna
   memilih Chrome yang sudah terbuka. Tidak ada konfirmasi CAPTCHA otomatis.
2. Tab TikTok yang sudah login pada Chrome pengguna dipakai melalui kontrol tab
   Codex. Tidak membuka profil baru, tidak restart/menutup Chrome pribadi.
3. Query pertama konfigurasi, biaya kuliah beasiswa, menghasilkan kartu pencarian.
   Post nuraasyiffa/7685001417442086152 dan10nativeID komentar dibaca bersama teks
   dari DOM overlay pencarian. Balasan tidak diekspor karena parent/ID balasannya
   belum terbaca. Layout detail baru menampilkan komentar tanpa atribut ID yang
   sama; teks tanpa ID tidak diberi identitas rekaan.
4. Navigasi dokumen asli post yang sama menyediakan metadata publik dengan ID
   yang cocok: timestamp2026-09-13T12:50:35Z,18600play,545like,15comment,
   110share,216save. Metadata hydration dari halaman sebelumnya ditolak saat
   ID tidak cocok. Tidak menganggap data rekomendasi sebagai hasil keyword.
5. Data publik disusun menjadi .cache/tiktok/chrome_public_capture_20261103.json.
   captured_at adalah waktu kompilasi; jendela observasi14:53–15:02WIB dicatat.
   Cookie, token, body debug dan URL media bertanda tangan tidak dimasukkan.
6. CLI --chrome-capture memakai ChromeCaptureWorker, source
   beesense_existing_chrome_capture/BeeSenseChromeCapture:1.0.0. Worker melakukan
   impor offline, bukan mengendalikan Chrome atau mengambil500post baru.

## Output dan batas verifikasi

Run nyata: output/crawler_runs/social_20261103T080235Z_374e6c8c/.
Excel ringkas social_data.xlsx mempunyai11baris konten; dataset.xlsx/JSONL berisi
nativeID, relasi dan statistik audit. Organizer default menempatkan data menurut
platform/tanggal crawlingWIB, dengan ID unik lintas hari. Akurasi tanggal komentar
relatif tetap unknown pada audit; waktu post exact memakai metadata sumber.

Tidak ada klaim CAPTCHA diperlukan/diselesaikan dalam sesi Chrome ini. Tidak
ada request TikTok langsung oleh worker impor, penyalinan cookie profil atau
perubahan auth.json. Default1000post/nullcap tetap sama. Mode browser mandiri
sebelumnya gagal0/500; keberhasilan kecil melalui Chrome bukan bukti mode mandiri
sudah berhasil atau target500tercapai.

Pengujian focused33tests lulus, termasuk ekspor, provenance, ID/parent, cap dan
impor tanpa membaca auth/browser. Verifikasi akhir suite/arsip dicatat pada
GRAPH_REPORT.md. No migration required; tidak menulis PostgreSQL/produksi.
Docker belum dibangun/dijalankan karena daemon tidak tersedia.

Untuk mengendalikan Chrome dari Python diperlukan endpoint CDP yang benar-benar
tersedia, bukan sekadar tab terbuka. Koneksi browser agen saat ini tidak diekspos
sebagai endpoint Playwright Python. Tidak mengubah keamanan/debugging Chrome.
Rujukan primer: https://developer.chrome.com/blog/remote-debugging-port dan
https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp.
