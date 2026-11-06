# Panduan sesi per sosmed

Pembaruan 6 November 2026. Buka **Konfigurasi crawling → Akun & sesi**, lalu
pilih **Cara mengambil Session ID**. Panduan berada sebelum input akun dan
dapat dibuka tanpa menyimpan isian atau memulai crawling. TikTok menempatkan
petunjuk sesi pada bagian **Gunakan Chrome Anda**.

| Sosmed           | Panduan yang tersedia                                                                     | Kontrak yang diverifikasi                                                          |
| ---------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Instagram        | Login di `https://www.instagram.com`, pilih cookie `sessionid`, salin Value ke Session ID | `instaloader_crawler.session_cookies` menerima `sessionid`                         |
| X / Twitter      | Login di `https://x.com`, pilih cookie `auth_token`, salin Value ke Session ID            | `twitter_crawler.auth_material` memetakan field `sessionid` ke cookie `auth_token` |
| TikTok           | Login pada tab Chrome, lalu pilih tab dan pairing di sidebar BeeSense                     | Frontend menggunakan plugin; tidak menyediakan input Session ID TikTok             |
| Threads          | Penjelasan bahwa backend dan format sesi belum tersedia; isian dapat dikosongkan          | Tidak menjanjikan cookie Instagram dapat dipakai di Threads                        |
| Facebook         | Penjelasan bahwa backend dan format sesi belum tersedia; isian dapat dikosongkan          | Tidak menjanjikan satu cookie tertentu sudah diterima crawler                      |
| YouTube / Reddit | Tidak menampilkan panduan atau input sesi                                                 | Konfigurasi frontend saat ini tidak memerlukan Session ID kedua sumber ini         |

## Langkah Instagram dan X

1. Buka situs yang sesuai di Chrome dan login ke akun Anda sendiri.
2. Buka DevTools dengan `Cmd + Option + I` pada macOS atau `Ctrl + Shift + I`
   pada Windows/Linux.
3. Pilih **Application → Storage → Cookies**, kemudian origin situs yang sesuai.
4. Cari **Name** `sessionid` untuk Instagram atau `auth_token` untuk X.
5. Salin **Value** utuh dan tempel ke **Session ID**, lalu isi username akun yang sama.

Nama cookie, tanda kutip, cookie lain dan tulisan **Session** pada kolom Expires
bukan bagian nilai yang ditempel. Panduan menyertakan langkah bila cookie belum
terlihat serta tautan ke [dokumentasi cookie Chrome](https://developer.chrome.com/docs/devtools/application/cookies/)
dan [shortcut DevTools](https://developer.chrome.com/docs/devtools/open/).
Frontend tidak menjalankan JavaScript di sosmed atau membaca cookie pengguna.

## Desain dan batas integrasi

Disclosure HTML `details/summary` membuat petunjuk tersedia di samping tugas
pengisian tanpa memperpanjang form saat tertutup. Palet mengikuti BeeSense:
putih `#ffffff`, teks `#000000`, oranye `#e97818`, bidang informasi `#fff6ed`,
garis `#ead8c8`. Font Plus Jakarta Sans tetap digunakan; teks panduan 14 px,
pendukung 13 px, nomor langkah hanya untuk urutan kerja yang sebenarnya.
Domain dan nama cookie berada dalam satu daftar definisi; teks rata kiri dan
tautan eksternal diberi keterangan tab baru bagi pembaca layar.

`sessionCookies` dalam `shared/auth.ts` menjadi sumber metadata bagi panduan
dan hint input. `SessionGuide` dipakai oleh `AuthSettings` dan persiapan Chrome
TikTok. Tidak ada perubahan payload `{username, sessionid}`, endpoint, izin,
penyimpanan atau konfigurasi crawler. Nilai sesi tetap tersembunyi; membuka
panduan tidak menampilkan atau mengirim nilai input.

Frontend saat ini memakai simulasi pada runtime dev. Penyimpanan `auth.json`
nyata tetap menunggu layanan akun/gateway; demo hanya menyimpan metadata akun.
Tidak ada akses ke file autentikasi, perubahan database atau crawling baru.
**No migration required.**

## Verifikasi

- `npm run check`: lint, 50 Vitest, 2 tes sinkronisasi, TypeScript dan build API lulus.
- `npm run format:check`: lulus.
- Browser lokal: disclosure terbuka dengan Enter dan tertutup dengan Space;
  fokus terlihat, desktop 1440 px dan mobile 390 px diperiksa. Pada mobile,
  scrollWidth=390, viewport=390, teks panduan terkecil=13 px.
- Instagram dan X memiliki screenshot panel di `output/playwright/session-guides/`;
  input kredensial kosong dan semua permintaan ke domain luar diblokir.
- Console: 0 error, 0 warning. Tests memverifikasi mapping cookie, isian tetap
  tersembunyi, tidak ada auto-save/start, status Threads/Facebook, serta TikTok
  tanpa input Session ID.
- Daemon Docker tidak aktif. Image frontend revisi ini belum dibangun ulang.
  Saat tersedia: `docker build -t beesense-crawler-frontend:api Crawler/Frontend`.

Review [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md),
diambil 6 November 2026:

```text
src/shared/SessionGuide.tsx:1 - pass
src/shared/AuthSettings.tsx:1 - pass untuk integrasi panduan dan hint sesi
src/features/TikTokConnector.tsx:1 - pass untuk petunjuk sesi Chrome
src/styles.css:3550 - pass untuk disclosure, fokus, wrapping dan ukuran teks
```
