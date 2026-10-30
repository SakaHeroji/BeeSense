---
type: architecture
tags: [beesense, crawler, instagram, instagrapi, playwright, trial]
---

# InstagramCrawler instagrapi

## Integrasi SocialCrawler dan pipeline tiga jam

Instruksi pengguna terbaru mengizinkan integrasi Instagram ke SocialCrawler 1.5 dan
run **hanya Instagram** melalui `config/social_crawler_instagram_3h.json`, 10.800 detik,
target 1.000 root/minimum 10 komentar. Run baru dimulai **13.28 WIB, 30 Oktober 2026**,
deadline sekitar 16.28 WIB. Hasil akhir belum ditetapkan. Worker/adapter Instagram
memakai scheduler, filter dan ekspor bersama; 5 tes integrasi baru lulus. YouTube dan
Reddit tidak diambil ulang. Trial lama yang dihentikan di bawah adalah riwayat.

Pengguna mengonfirmasi penggabungan berdasarkan hasil crawling **27–30 Oktober**.
ID native berulang disatukan, observasi terbaru dan perubahan comment/reply diaudit,
teks sama dengan ID berbeda dipertahankan. Dataset baru → SBERT/UMAP/DBSCAN/Ward →
20 topik dengan rata-rata c_v ≥0,4 → artifact/tes UI → commit/push GitHub untuk Streamlit.
Konfigurasi aktif baru beralih setelah model baru lolos. Instagram kini didukung pada
identitas root, tren, hitungan dan grafik/filter/bukti dashboard.

[Runbook pipeline](../../docs/crawler/INSTAGRAM_PIPELINE_20261030.md) ·
[[Arsitektur BeeSense]] · [[Dataset Dashboard]]

## Perkembangan terkini: Chrome

Pengguna menyetujui backend Chrome/Playwright dengan login manual setelah mobile API
tetap ditolak. [Konfigurasi browser](../../config/instagram_browser_crawler.json)
memilih `InstagramBrowserWorker` lewat class InstagramCrawler yang sama. CLI dipatok
0.1.22; satu profil lokal persisten di output/, terpisah dari Chrome pribadi dan Git.
Login `researchinnovationsocs` berhasil; preflight worker membaca **1 post/15 komentar**.
Trial `_02` mulai sekitar **13.08 WIB, 30 Oktober 2026**, lalu dihentikan atas instruksi
pengguna setelah **718.82 detik**: **76 post/910 komentar/0 balasan**, 59 post memenuhi
minimum 10 komentar. Status INTERRUPTED; live_access_verified true, trial_passed false.
Excel 986 baris dan 12 checksum manifest terverifikasi; root unik, baseline tidak berubah.
Trial 30 menit belum selesai dan integrasi belum dilakukan. `_01` dihentikan untuk memperbaiki pemuatan komentar, bukan trial lulus.

Hydration JSON caption dan komentar dapat berada di script terpisah. Komentar hanya
diikat ke root setelah ID aslinya cocok dengan permalink DOM untuk shortcode yang sama.
Native ID, tanggal, filter dan baseline dedup tetap memakai kontrak bersama. Provenance
`playwright_chrome_rendered_document`; komentar awal best effort, tidak diklaim lengkap.
Tidak ada ekstraksi cookie/password/inbox atau solver CAPTCHA. Integrasi gabungan
tetap menunggu hasil trial. Paragraf di bawah merekam diagnosis instagrapi sebelumnya.

[Worker Chrome](../../Crawler/Backend/instagram_browser.py) ·
[Parser dokumen](../../Crawler/Backend/instagram_browser_capture.mjs) ·
[Tes browser offline](../../tests/crawler/test_instagram_browser.py)

[Class standalone](../../Crawler/Backend/instagram_crawler.py) memakai instagrapi
3.2.2 dan [config](../../config/instagram_crawler.json) 1800 detik. Discovery hashtag,
caption media/album, komentar dan balasan memakai native ID/shortcode/parent,
filter tanggal/keyword dan deduplikasi baseline. Foto/video tidak diunduh.

`InstagramAdapter` → kontrak `ContentInput`/`Dataset`/`BundleSink` → JSONL delapan
tabel dan `dataset.xlsx` → `SocialExportMixin` → `social_data.xlsx` satu sheet Data,
10 kolom, tanggal WIB dan teks formula aman. Mixin berasal dari tiga metode
SocialCrawler yang dipindahkan tanpa perubahan perilaku. [[RedditCrawler Reddrix]]
tetap memakai scheduler, backend dan konfigurasi semula.

Setiap operasi instagrapi berada dalam subprocess spawn dengan hard deadline;
deadline global mencakup pengambilan/cooldown. Pagination/cursor dan jumlah unik
komentar/balasan dibatasi. Root sejak `since` inklusif sampai `until` eksklusif,
komentar konteks kecuali exclude. Baseline read-only dipertahankan. Source timestamp
tanpa zona tetap unknown; kelengkapan teks/komentar dan peran penulis tidak ditebak.

Kredensial lokal `config/auth.json` diabaikan Git, tidak masuk output/graph/Docker.
Login eksplisit menyimpan settings di `output/instagram/session.json` mode 0600
setelah berhasil; session digunakan ulang saat crawling. Tidak ada pengulangan
password login otomatis, solver CAPTCHA atau rotasi identitas. Challenge/login
menghentikan worker; `needs_upgrade` adalah CLIENT_UPGRADE_REQUIRED, bukan 429.
Default retry 429 nol, cooldown terkonfigurasi minimal 360 detik bila retry diaktifkan.

## Bukti percobaan 30 Oktober 2026

Login password ditolak dengan `ClientNeedsUpgradeError` (`needs_upgrade`) pada
instagrapi 3.2.2/profil bawaan Android 449.0.0.52.84. Sesi belum dibuat saat percobaan awal. Pemanggilan
class menghasilkan bundle `outputs/instagram_instagrapi_20261030_30m_01` dengan
PARTIAL/LOGIN_REQUIRED, **0 post/0 komentar/0 balasan**, elapsed **0.23 detik**.
Anggaran 1800 detik telah dikonfigurasi, tetapi **uji akuisisi 30 menit belum dapat
berlangsung**. `trial_passed` dan `live_access_verified` false; bundle bukan fixture.
Tes offline selalu synthetic dan tidak membuktikan akses Instagram.

Setelah pengguna menyediakan cookie lokal, login cookie dan satu baca privat akun
berhasil; settings tersimpan di `output/instagram/session.json`. Percobaan kedua
mulai 11:20:33 WIB dan berhenti LOGIN_REQUIRED pada pencarian hashtag pertama
setelah 5.64 detik: `outputs/instagram_instagrapi_20261030_30m_02`, 0 post/0 komentar/0 balasan.
Baca akun setelah reload juga ditolak. Pemeriksaan lokal membuktikan cookie,
authorization,UUID/header dipulihkan; penyebab penolakan server tetap tidak diketahui.
Cookie browser memang dapat ditolak/dibatalkan API privat menurut upstream.
Probe jalur web library gagal AttributeError get pada public.py467/hashtag.py227,
tanpa data. Tidak ada trial live30 menit selesai atau integrasi backend gabungan.

Pengguna kemudian memilih mencoba **Instaloader4.16**. Preflight cookie gagal
ConnectionException sebelum discovery; satu login normal gagal LoginException
pada instaloadercontext.py344. Tidak ada bukti HTTP 429/password salah/CAPTCHA dari
receipt tersebut dan tidak ada data terambil. Ini pemeriksaan akses terbatas,
bukan uji crawler30 menit atau backend produksi baru. Max connection attempts1,
hard deadline80 detik, rate controller library dipertahankan. Dependency eksperimen
di `requirements/instaloader.txt`. Worker Instaloader masa depan perlu satu
context/rate controller sepanjang run; restart berulang dapat mengganggu pacing.

Pengguna meminta kembali ke instagrapi dan mengonfirmasi login password baru secara
manual berhasil. Diagnostik upstream memakai device tersimpan: CAA HTTP 200 tidak
menerbitkan sesi, fallback legacy HTTP 400 needs_upgrade; tidak ada konteks 2FA
yang dapat dilanjutkan. qe/sync HTTP 405 tercatat tetapi hubungan sebabnya belum
terbukti. Dua pemeriksaan akun dengan transport curl/requests dan hipotesis cookie
URL-decoded sama-sama HTTP 403 login_required. Tidak ada HTTP 429 atau post baru.

[Referensi scraper pengguna](https://instagrapi.com/guides/instagram-scraper-python)
dan [persistensi sesi](https://instagrapi.com/guides/instagrapi-session-persistence)
menegaskan load settings sebelum login, perangkat konsisten, request serial,
pagination terbatas dan pacing. Login eksplisit mengikuti pola ini; worker crawl
tidak mengulang password. Nilai cookie opaque dipertahankan persis. Impor cookie
menghapus authorization lama hanya di memori sebelum lookup SDK, mempertahankan
device settings; file sesi hanya diganti setelah validasi privat berhasil.
Referensi belum menyelesaikan hambatan autentikasi; uji live masih tertunda.
Validasi impor cookie asli setelah perbaikan header juga gagal AttributeError
di alur SDK; tidak ada sesi baru tersimpan atau post terambil.

## Pemulihan sesi sesuai pola pengguna

`--login --auth-file config/auth.json --login-method password` memuat settings
sebelum `login(username,password)` dan menyimpan setelah berhasil. Mode ini
mengabaikan field cookie; auto tetap kompatibel dengan pemilihan sebelumnya.
Login eksplisit dapat memulihkan device walau authorization kosong, sedangkan
worker akuisisi tetap membutuhkan sesi terautentikasi dan tidak membaca password.
Helper `login_with_saved_password()` membatasi pemulihan LoginRequired satu kali,
meneruskan kode verifikasi pada relogin eksplisit, serta tidak mengulang upgrade,
challenge atau rate limit. File sesi lama dipertahankan jika login gagal.

Uji live: settings berhasil dimuat, UUID tetap sama, validasi akun HTTP 403
login_required, SDK mencoba login ulang, CAA HTTP 200 tanpa sesi/konteks 2FA dan
fallback legacy HTTP 400 needs_upgrade. Berhenti setelah 27.15 detik pada login;
file sesi tidak berubah. Jadi hambatan terjadi sesudah pemuatan file. Tidak ada
post atau trial 30 menit yang berhasil. Upgrade pip tetap pada instagrapi 3.2.2.

Probe persiapan tanpa password: GET qe/sync HTTP 405 tetap mengandung key ID/RSA
publik yang valid, sementara POST sync_device_features mendapat HTTP 500 tanpa
kunci. Belum ada dasar mengganti request/profil aplikasi. Verifikasi offline:
27 tes Instagram lulus; seluruh crawler 100 tes, 99 lulus/1 browser opsional skip.

Syarat pengguna: integrasikan ke `social_crawler.py` lalu uji ulang hanya jika trial
berhasil. Karena akses belum berhasil, dispatch/config gabungan tetap YouTube dan
Reddit. Tidak ada crawl ulang YouTube/Reddit, penggabungan corpus atau training NLP.
[[Dataset Dashboard]] dan artifact tersimpan tidak berubah. [[Struktur Proyek]]
memetakan package/dependency/path baru. Docker standalone disediakan, build/runtime
memerlukan daemon tersedia. No migration required.

[Panduan dan hasil uji](../../docs/crawler/INSTAGRAM_CRAWLER.md) ·
[Tes kontrak](../../tests/crawler/test_instagram_crawler.py) · [[Arsitektur BeeSense]] · [[HOME]]

## Pemulihan 429 terkini

SocialCrawler 1.5.1 menambahkan jeda Instagram360 detik/maksimum3 retry, mengikuti Retry-After yang lebih lama dan deadline awal16.28WIB. Status main-document/GraphQL429 dipantau tanpa menyimpan cookie/header otentikasi; generic navigation failure tidak diasumsikan429. Chrome dipertahankan ketika429/error/timeout/challenge. Penutupan sebelumnya berasal dari finally crawler, bukan macOS. Run01 menghasilkan248 post/2.128 komentar setelah49 menit, run02kosong. Run03 dimulai setelah cooldown14.47WIB; target 1.000/durasi3 jam belum tercapai. Training sementara ditunda hingga akuisisi selesai.17tes terfokus lulus.

## Pembaruan pacing setelah deployment 30 Oktober

Dashboard pada commit `194e0b1` sudah terverifikasi live di
https://beesense.streamlit.app: 20 topik, c_v 0,4315219014, dan CSV unduhan
identik dengan berkas lokal. Narasi Gemini memakai 10 keyword dan 10 kalimat
representatif per topik. Perbaikan crawler berikut dilakukan setelah verifikasi
tersebut; crawling tetap berhenti dan tidak ada uji jaringan Instagram baru.

`SocialCrawler` 1.5.2 menambahkan `instagram_pacing`. Preset
`config/social_crawler_instagram_3h.json` dan preset pemulihan kini memakai:

- Jeda antaroperasi acak 5–10 detik.
- Istirahat 120 detik setiap 20 operasi Instagram, hanya bila masih ada pekerjaan.
- Cooldown 429 bertahap 360, 720, 1.440, lalu maksimal 3.600 detik. Batas ini
  berlaku pada perhitungan lokal; `Retry-After` yang lebih lama tetap dihormati.
- Maksimum tiga retry dan batas waktu total tetap berlaku. Scheduler memberi
  kesempatan platform lain berjalan selama jeda Instagram pada mode round robin.
- Maksimal delapan scroll per halaman dengan jeda lima detik. Data yang belum
  terkumpul tetap ditandai parsial; target 1.000 post bukan jaminan throughput.

```json
"instagram_pacing": {
  "enabled": true,
  "batch_size": 20,
  "batch_pause_seconds": 120,
  "rate_limit_backoff_multiplier": 2,
  "max_cooldown_seconds": 3600
}
```

Konfigurasi lama yang tidak mengaktifkan blok ini mempertahankan cooldown tetap.
Hitungan `operations_completed` dan `batch_pauses` masuk ringkasan/progress.
Satu operasi browser dapat menghasilkan beberapa request HTTP; angka 20 di atas
merupakan batas batch lokal, bukan kuota resmi Instagram. Sesi Chrome persisten,
penghentian saat challenge/429, dan pengecualian ID post lama tetap dipakai.

Pola jeda acak, istirahat batch dan exponential backoff diadaptasi dari
[referensi DataDwip yang diberikan pengguna](https://www.datadwip.com/blog/how-to-scrape-instagram/).
Klaim kuota dalam artikel bukan jaminan platform. Makna HTTP 429 dan petunjuk
waktu tunggu mengacu pada [RFC 6585 bagian 4](https://www.rfc-editor.org/rfc/rfc6585#section-4)
dan [Retry-After pada RFC 9110](https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3).
Pengaturan ini mengurangi laju akses; tidak menjamin HTTP 429 hilang. Uji jam
simulasi mencakup pertumbuhan/cap backoff, waktu tunggu server yang lebih lama,
jeda batch, dan penghentian pada deadline, tanpa membuka Instagram.
