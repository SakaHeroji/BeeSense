# InstaloaderCrawler

Implementasi di `Crawler/Backend/instaloader_crawler.py`, memakai
Instaloader **4.16**. Class mewarisi coordinator/exporter InstagramCrawler:
filter tanggal/keyword, native ID, deduplikasi baseline, deadline, audit workbook
8 sheet dan `social_data.xlsx`/sheet `Data` tetap memakai kontrak bersama.
SocialCrawler 1.6.0 kini memakai worker Instaloader yang sama sebagai backend Instagram default. Preset tiga jam telah beralih; dataset/dashboard aktif tidak dilatih ulang oleh perubahan backend ini.

## Menjalankan

Jalankan dari root repository:

```bash
python3 -m venv .venv-instaloader
.venv-instaloader/bin/python -m pip install -r requirements/instaloader.txt
.venv-instaloader/bin/python -m Crawler.Backend.instaloader_crawler --dry-run
.venv-instaloader/bin/python -m Crawler.Backend.instaloader_crawler --output-dir outputs/instagram_instaloader_trial
```

`config/instaloader_crawler.json`: maksimal **300 detik/10 post**, hashtag kuliah,
minimum 1 komentar per qualified post, maksimal 20 komentar/10 preview balasan,
jeda HTTP minimal 5 detik, timeout operasi 60 detik, **tanpa retry 429**.
Folder baseline lokal yang disebut konfigurasi harus tersedia; hasil tetap
menyimpan checksum setiap workbook baseline. Output baru harus memakai folder baru.

Autentikasi membaca `sessionid` dari entry Instagram pada `config/auth.json`, atau
memakai JSON sesi di `output/instaloader/session.json` jika sudah ada. File auth
dan seluruh `output/` diabaikan Git. Nilai password tidak dipakai ulang otomatis.
Sesi valid bisa disimpan setelah pembacaan komentar atau `--check-session` berhasil,
dengan mode 0600. File pickle Instaloader tidak dimuat oleh class ini.

## Patch web GraphQL

`Crawler/Backend/instaloader_browser_patch.py` mengadaptasi patch yang diberikan
pengguna dari [issue resmi #2767](https://github.com/instaloader/instaloader/issues/2767).
Satu context worker dipatch saat runtime; instalasi library tidak diedit.
Request memakai `/api/graphql`, token `fb_dtsg`, `lsd`, `jazoest` dari halaman
login yang sama, serta header friendly-name, LSD dan ASBD. Token disimpan per
context dan cache dibatalkan jika sessionid berubah. Signature menerima argumen
keempat `web_api` yang diperkenalkan Instaloader 4.16. Client hints mengikuti
User-Agent context, bukan pergantian identitas ketika gagal.

Rate controller bawaan dan `do_sleep()` tetap dipanggil, ditambah jeda HTTP minimal.
Satu subprocess mempertahankan context/iterator sepanjang run; deadline parent
bisa menghentikannya tanpa membuang record yang sudah dikirim. HTTP 429,
login/challenge, `feedback_required`, atau upstream AbortDownload menghentikan
crawl. Receipt mencatat tipe error, status HTTP yang benar-benar diamati, kode
error yang diizinkan dan lokasi kode; body respons, cookie dan token tidak dicatat.
`feedback_required` menyatakan penolakan request, tidak membuktikan akun diblokir
atau password salah.

Metadata `Post` dari discovery dipakai kembali melalui cache terbatas. Komentar
default `comments_transport=query_hash` memakai NodeIterator GraphQL Instaloader
sesuai [PR #2692](https://github.com/instaloader/instaloader/pull/2692), sehingga
thread besar tidak dipaksa menuju endpoint mobile. Jalur ini berhasil diuji live.
Opsi eksperimental `web_doc_id`, berdasarkan format pada [issue #2651](https://github.com/instaloader/instaloader/issues/2651),
belum berhasil pada post uji karena respons tidak memuat connection yang diharapkan.
Tidak ada fallback otomatis setelah penolakan. Reply hanya preview yang disertakan
server, dengan parent native eksplisit; tidak ada klaim komentar/reply lengkap.

Patch juga dapat menjalankan CLI native, dengan opsi upstream:

```bash
.venv-instaloader/bin/python -m Crawler.Backend.instaloader_browser_patch --version
```

CLI native mempertahankan aturan output/session dan opsi Instaloader sendiri;
gunakan `InstaloaderCrawler` untuk kontrak Excel BeeSense dan batas eksperimen.

## Bukti uji 30 Oktober 2026

| Run lokal | Hasil |
| --- | --- |
| `instagram_instaloader_20261030_trial01` | 40,96 detik: discovery berhasil; 4 detail post ditolak AbortDownloadException; 0 record. |
| `instagram_instaloader_20261030_trial02` | 6,00 detik: HTTP 400/feedback_required pada detail post; langsung berhenti; 0 record. |
| `instagram_instaloader_20261030_trial03` | Jalur web bawaan 4.16 berhasil membaca metadata; post di luar rentang tanggal disaring; endpoint komentar mobile gagal. |
| `instagram_instaloader_20261030_trial04` | Patch pengguna + jalur komentar web: 3 post nyata/0 komentar, 27,67 detik, 0 invalid/429. Ketiga post memang memiliki comment_count 0; uji komentar belum terwakili. |
| `instagram_instaloader_20261030_trial05` | Satu post dengan komentar: metadata terbaca; query web_doc_id tidak memberikan connection yang diharapkan. 1 post/0 komentar, 11,65 detik; bukan keberhasilan komentar. |
| `instagram_instaloader_20261030_trial06` | Patch lengkap pengguna + NodeIterator query_hash: **1 post/20 komentar/0 balasan**, 26,56 detik, TARGET_MET/trial_passed true, 0 invalid/429. Cap 20 komentar; tidak berarti semua komentar diambil. |

Hasil lengkap tersedia di `outputs/<run>/summary.json`, workbook dan manifest.
Log lokal disanitasi berada pada `output/instagram_work/instaloader_class_live_trial*.log`.
Uji diagnostik satu post lama memakai konfigurasi terpisah dengan filter tanggal
dilepas; hasilnya tidak menjadi dataset training dan tidak mengubah preset aktif.
Trial05 dan trial06 sengaja menguji ulang permalink yang sama untuk membandingkan
implementasi; kedua bundle tidak boleh digabung tanpa deduplikasi native ID.

## Verifikasi pengembangan

`python -m unittest discover -s tests/crawler -p 'test_instaloader*.py' -v`:
**21 tes offline lulus**. Suite crawler lengkap: **144 tes, 143 lulus/1 optional skip**.
Tes mencakup format request patch, isolasi/invalidation cache token, status error,
tanpa retry tersembunyi, preview reply, UTC, dedup, Excel, worker persisten dan
hard deadline. Ruff check/format lulus. Data sintetis tes ditandai synthetic dan
tidak menjadi bukti akses live. No migration required.

Dockerfile: `deployment/docker/Dockerfile.instaloader`, allowlist context memuat
hanya source/config/dependency yang diperlukan dan mengecualikan auth/session.
Daemon Docker lokal tidak aktif, sehingga image belum dibangun atau dijalankan:

```bash
docker build -f deployment/docker/Dockerfile.instaloader -t beesense-instaloader:local .
docker run --rm beesense-instaloader:local --dry-run
```

Mount auth/sesi, baseline dan config lokal saat menjalankan crawl dalam container.
Keberhasilan uji singkat tidak menjamin tidak ada HTTP 429 pada run berikutnya.

## Integrasi SocialCrawler 1.6.0

`social_crawler.py` memilih `InstaloaderWorker` persisten, `InstaloaderSettings`, dan provenans `instaloader_saved_web_session` secara default untuk Instagram. Validator opsi digunakan bersama class standalone. Preset `social_crawler_instagram_3h.json` memakai backend instaloader dengan target 1.000 post/10.800 detik dan minimal 10 komentar. Preset resume historis `social_crawler_instagram_resume_20261030.json` juga beralih backend, dengan sisa target/waktu aslinya tetap 870 qualified post/6.065 detik. Keduanya mempertahankan pacing batch dan retry 429 nol. Kebijakan retry yang secara eksplisit disetel pengguna tetap mengikuti scheduler/cooldown; worker mempertahankan context tanpa mengirim request selama menunggu. Backend browser/instagrapi lama tersedia bila dipilih eksplisit.

Tes integrasi memeriksa pemilihan worker/settings default, lifecycle close, Excel/provenans, baseline dedup, discovery cursor, ekspor lintas platform, jeda, retry/deadline dan penolakan credential di config. `requirements/crawler.txt` membawa dependency Instaloader; allowlist/image crawler, Selenium dan browser telah diperbarui untuk dependency/source baru. Tidak ada migrasi database.
