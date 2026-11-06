# Sidebar TikTok Connector 1.4.0

UI ekstensi kini memakai Chrome Side Panel, dibuka melalui ikon BeeSense pada
toolbar. `action.default_popup` dan tiga file popup dihapus; manifest memakai
`side_panel.default_path`, izin `sidePanel`, serta
`setPanelBehavior({openPanelOnActionClick:true})`. Tidak ada jendela baru.
Minimum Chrome tetap 118. Build aktif `20261106-sidebar-v7`.

## Penggunaan

1. Buka `chrome://extensions`, lalu Reload BeeSense dari
   `Crawler/Backend/Tiktok/chrome_extension`.
2. Jalankan crawler lokal dan buka TikTok yang sudah login.
3. Klik ikon BeeSense untuk membuka sidebar, kemudian pilih tab TikTok.
4. Salin alamat `http://127.0.0.1:PORT/` dan kode dari proses crawler aktif.
5. Tekan **Hubungkan & mulai**. Form berganti menjadi monitor sesi.
6. Selesaikan CAPTCHA di tab TikTok jika diminta, lalu tekan tombol lanjut.
7. Tekan **Hentikan pengambilan** untuk melepas debugger dan mempertahankan data.

Sidebar dapat dibuka kembali tanpa mengirim perintah start ulang. Posisi panel
ditentukan pengguna di Chrome. Untuk sisi kanan pilih **Setelan → Tampilan →
Panel samping → Kanan**; Side Panel API menyediakan pembacaan layout dan tidak
menyediakan setter posisi. Lihat [dokumentasi Chrome](https://developer.chrome.com/docs/extensions/reference/api/sidePanel).

## Keputusan desain

Panel menggunakan alur vertikal: identitas/status → tab → alamat/kode → aksi
utama → aktivitas → bantuan. Setelah tersambung, form diganti dengan monitor
dan penghitung sesi. Tombol lanjut hanya muncul saat CAPTCHA; berhenti tetap
tersedia saat sesi aktif. Status kosong, kesalahan dan tab yang hilang memberi
langkah berikutnya. Tidak ada persentase selesai yang dibuat tanpa target sumber.

Palet: putih `#ffffff`, teks `#202020`, oranye aksi `#b84212`, aksen `#f2772a`,
permukaan `#f3f4f5`, hijau status `#16724b`. Trebuchet MS/Segoe UI lokal digunakan
agar panel tidak mengambil font dari luar. Ukuran teks minimum 12 px; angka
tabular memakai `Intl.NumberFormat('id-ID')`. Tata letak kiri, satu kolom,
tanpa animasi otomatis, kartu berulang atau scrollbar horizontal.

Review brief mempertahankan putih/oranye BeeSense, satu aksi utama dan informasi
yang diperlukan operator. Bentuk heksagon pada identitas menjadi aksen visual;
progres memakai label biasa dan tiga kolom, tanpa grafik dekoratif.

## Status dan data

`background.mjs` menyimpan `connectorState` di `chrome.storage.session`: fase,
running, pesan, timestamp, judul tab, target aktif serta jumlah post/komentar/
balasan. `status` string lama tetap tersedia. UI berlangganan perubahan storage,
bukan melakukan polling. Kode pairing hanya berada di memori worker dan
dikosongkan dari formulir setelah pesan start diterima.

Hitungan bertambah setelah bridge mengakui batch record, dengan deduplikasi
native ID per sesi. Kandidat pencarian tidak dihitung sebagai post terkirim.
Angka ini bukan jumlah qualified/hasil final ekspor; filter Python tetap berlaku.
Pairing baru mereset penghitung sesi; deduplikasi dan arsip Python tetap pemilik
hasil kampanye. Tutup panel tidak menutup worker. Restart worker membatalkan
klaim running yang tersimpan dan memberi instruksi menghubungkan ulang.

Perubahan versi 1.4.0 juga diperkenalkan pada provenance bridge, plan dan default
frontend. Minimum protokol throughput tetap 1.3.0; tidak ada migrasi database,
perubahan autentikasi, interval crawler atau host tambahan.

## Verifikasi

- 71 tes Python TikTok/bridge/DOM/sidebar lulus, termasuk 8 tes UI Chromium.
- 14 tes Node controller lulus, termasuk pemulihan state dan penghitung batch.
- Frontend: lint, 45 tes Vitest, 2 tes sinkronisasi dan build produksi lulus.
- Side Panel API asli diuji pada Chromium terisolasi dengan ekstensi lokal:
  permission terdaftar, path `sidepanel.html`, toolbar behavior aktif dan
  `sidePanel.open()` dari klik pengguna berhasil. Semua HTTP/HTTPS diblokir.
- UI diuji pada lebar 280/380 px dan zoom 200%, formulir tidak valid, pemilihan
  tab, kegagalan perintah/retry, status CAPTCHA, berhenti dan buka ulang.
- Screenshot di `output/playwright/sidebar/`; preview memakai data/API tiruan
  dan bukan hasil crawl live. Catatan native API: `native-api.json`.
- Daemon Docker tidak aktif: image belum dibangun ulang. Tidak ada deployment.

Perintah:

```sh
.venv-tiktok/bin/python -m unittest discover -s tests/crawler -p 'test_tiktok*.py' -q
node --test tests/crawler/test_tiktok_chrome_extension.mjs
cd Crawler/Frontend && npm run check
docker build -f deployment/docker/Dockerfile.tiktok -t beesense-tiktok:local .
docker run --rm beesense-tiktok:local --dry-run
```

## Review Web Interface Guidelines

Mengikuti [pedoman Vercel](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md):

```text
Crawler/Backend/Tiktok/chrome_extension/sidepanel.html:1 - pass
Crawler/Backend/Tiktok/chrome_extension/sidepanel.css:1 - pass
Crawler/Backend/Tiktok/chrome_extension/sidepanel.mjs:1 - pass
```

Label input, error inline, fokus error pertama, skip link, fokus keyboard,
pengumuman status, state tombol, word wrapping, bahasa/angka lokal dan tata
letak sempit diperiksa. Tidak ada font remote, animasi, gambar tanpa dimensi,
kontrol berbasis div atau navigasi berbasis klik nonsemantik.
