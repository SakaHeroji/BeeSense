# Kontrak frontend Crawler 1.3

**Rancangan integrasi, belum layanan HTTP nyata.** Lingkup saat ini frontend terlebih dahulu. Prefix `/api/v1/projects/:projectId`, sesi same-origin dengan credentials include. Backend wajib memeriksa izin proyek, validasi, idempotensi dan keterikatan sumber; role selector demo tidak memberikan otorisasi server.

## Conversation riset

Conversation adalah sumber konteks riset yang berdiri sendiri dari eksekusi crawling. Versi conversation yang dipilih dibekukan ke `Config.conversation` saat review; job tidak membaca conversation terbaru secara dinamis.

| Endpoint                               | Kontrak                                                                                                              |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| GET `/crawler/conversations`           | Daftar conversation yang dapat diakses, diurutkan menurut `updatedAt`; tanpa rahasia atau API key.                   |
| GET `/crawler/conversations/:id`       | Satu versi conversation lengkap berdasarkan ID proyek.                                                               |
| POST `/crawler/conversations/generate` | Body tepat `{title}`. Gemini dipanggil server-side; respons `ConversationDraft`, belum tersimpan dan wajib ditinjau. |
| POST `/crawler/conversations`          | Body `{conversation}` untuk conversation baru; server memvalidasi, memberi ID, versi 1 dan timestamp.                |
| PUT `/crawler/conversations/:id`       | Body `{conversation}`; optimistic concurrency memakai versi lama dan menghasilkan versi baru.                        |

`ConversationDraft` memuat title, objective, since, until, include, exclude, includeMode (`any`/`all`), queries, hashtags, subreddits, relevance (`scope`, contoh relevant/generic/irrelevant, threshold), serta origin (`manual`/`gemini`/`excel`). `Conversation` menambah id, version, createdAt dan updatedAt. Title maksimum 120 karakter. Rentang waktu harus valid; query, scope dan setidaknya satu contoh relevan wajib tersedia; threshold berada pada 0–1.

Endpoint generator tidak menerima field lain, cookie, data job, atau kredensial. Prompt, model, rate limit, sanitasi output dan `GEMINI_API_KEY` menjadi tanggung jawab backend. Frontend tidak menganggap output model benar: origin hanya menandai asal draf, bukan status persetujuan.

Snapshot pada rencana menyertakan seluruh conversation ditambah `frozenAt`. Semua platform pada mode parallel harus menerima snapshot ID/versi yang sama. Backend menolak conversation yang tidak dimiliki proyek dan tidak boleh mengganti snapshot dengan versi terbaru setelah validasi.

### Pertukaran prompt dan Excel lokal

Download prompt Markdown dan pembacaan `.xlsx` berlangsung sepenuhnya di browser, bukan endpoint baru. Prompt mengikat judul ke workbook tanpa formula/macro dengan tiga sheet: `conversation` (satu baris metadata), `discovery` (`type`, `value`), dan `relevance_examples` (`classification`, `text`). Parser hanya menerima tipe discovery `include_keyword`, `exclude_keyword`, `query`, `hashtag`, `subreddit` serta kelas `relevant`, `generic`, `irrelevant`. Setelah lolos validasi, frontend mengirim draft ber-origin `excel` melalui POST/PUT conversation yang sama. Rentang tanggal tetap berasal dari form dan tidak ditimpa workbook.

## Crawling dan dataset

| Endpoint                                                  | Kontrak                                                                                                                                                 |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GET /session                                              | Session: nama, role, canExport                                                                                                                          |
| GET /crawler/capabilities                                 | Platforms, batas form, baseline, verificationAvailable, authAvailable dan migrationsAvailable. Dua capability terakhir hanya true setelah layanan siap. |
| GET /acquisition-jobs                                     | Daftar metadata job; tanpa kredensial                                                                                                                   |
| GET /acquisition-jobs/:id                                 | Snapshot job monotonik: status, startedAt, updatedAt, platform counts, series, events, konfigurasi publik dan dataset                                   |
| POST /acquisition-plans/validate                          | Body config; menormalisasi dan memvalidasi. Plan berumur pendek, snapshot publik tanpa DSN/token                                                        |
| POST /acquisition-jobs                                    | Body plan_id, header Idempotency-Key; job persisten                                                                                                     |
| POST /acquisition-jobs/:id/stop                           | Penghentian dan finalisasi aman                                                                                                                         |
| POST /acquisition-jobs/:id/verification-session           | Sesi browser worker terotorisasi; tidak menandai CAPTCHA selesai hanya karena tautan dibuka                                                             |
| GET /datasets/:id/versions/:version?page=&search=&source= | DatasetDetail: maksimal 50 preview, total, manifest dan unduhan terotorisasi. source tetap dibatasi menurut izin.                                       |
| POST /nlp-input-selections                                | dataset_id/version/checksum/accept_partial; pemilihan input tanpa menjalankan training                                                                  |

Statistik per transaksi menggunakan PlatformProgress.counts: roots, qualified, comments, replies, candidates, duplicates dan rejected, beserta target. Jangan menghitung statistik penuh dari 50 baris preview. `roots + comments + replies` adalah total konten unik per sumber menurut snapshot server. Pencapaian target memakai qualified/target, bukan komentar. Tanggal transaksi berasal dari startedAt dalam Asia/Jakarta; job antre belum mempunyai tanggal eksekusi.

Storage: destination excel/postgresql/both, postgresql.host/port/connectionEnv, dan connectionString sementara saat validasi. Nilai awal berasal dari JSON universal. URI tidak boleh masuk plan publik, log, URL atau browser storage. Backend penulisan langsung belum tersedia; runner Python menolak database sebelum crawling.

Endpoint pembuatan URL manual/survei dan migrasi Excel umum dikeluarkan dari kontrak frontend aktif. Tidak ada route `/crawler/manual`, `/migrations/excel` atau `/migrations/:id`.

## Akun dan sesi opsional

GET `/crawler/platforms/:platform/auth` mengembalikan `AuthStatus`: platform, username, hasSession, file `config/auth.json`; **tidak mengembalikan session ID**. POST pada route sama menerima `{username, sessionid}` dan mengembalikan metadata yang sama. Izin operator wajib; form aktif untuk Instagram, X, Threads dan Facebook. TikTok memakai sesi Chrome melalui plugin. Nilai kosong berarti mempertahankan nilai lama, bukan menghapusnya. Simpan setidaknya satu nilai baru yang valid.

Server tahap berikutnya harus melakukan update atomik pada entri `{sosmed, username, sessionid}` yang sesuai, memetakan x ke twitter, menjaga semua entri/field lain termasuk kredensial provider lain, dan tidak mengambil path arbitrer dari klien. Terapkan permission file privat, serialization terhadap update bersamaan, pembatasan ukuran dan error tanpa token. Jangan membuka isi auth.json melalui static assets atau bundel frontend. Form kini hanya simulasi dan file nyata tidak berubah.

## TikTok Connector dalam server dashboard

Ini kontrak frontend untuk gateway/worker berikutnya, bukan endpoint bridge CLI yang sudah tersedia. `tiktokConnectorAvailable` default tidak tersedia; server mengaktifkannya setelah seluruh transport plugin siap. Dashboard, API proyek dan HTTP penghubung plugin dilayani origin yang sama. Gateway mengadaptasi protokol Connector yang ada, dengan job/server-side ownership dan single active owner per tab; tidak meminta operator menjalankan bridge kedua atau memasukkan port secara manual.

| Endpoint                                            | Perilaku                                                                                                      |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| GET /acquisition-jobs/:id/tiktok-connector          | Operator proyek menerima TikTokConnectorSession privat, `Cache-Control: no-store`.                            |
| POST /acquisition-jobs/:id/tiktok-connector/pairing | Rotasi kode hanya saat menunggu, terputus atau kedaluwarsa. Tolak transaksi final/terhubung/menunggu CAPTCHA. |
| POST /acquisition-jobs/:id/tiktok-connector/resume  | Minta worker memeriksa halaman setelah validasi manual. Tetap VALIDATION_REQUIRED bila belum terverifikasi.   |

DTO privat memuat jobId, state, bridgeUrl, minimumVersion; pairingCode/pairingExpiresAt hanya bila diperlukan; version/build/lastSeenAt setelah handshake. State: WAITING, CONNECTED, VALIDATION_REQUIRED, DISCONNECTED, EXPIRED, FINISHED. `bridgeUrl` harus origin dashboard dengan path `/`, tanpa query, fragment atau userinfo. Kode acak berumur pendek (32–128 karakter base64url) terikat sesi/proyek/job, dirotasi server, tidak dimasukkan URL/log/error atau Job publik. Pastikan pemeriksaan CSRF/origin, izin operator dan batas percobaan pairing pada server.

`thread` opsional berisi postId, comments, replies, sourceTotal?, lastActivityAt, activity (comments/replies/scrolling/waiting) dan pagination (pending/exhausted/unverified). Hitungan menggunakan native ID unik yang diterima server. Ini data sementara operasi aktif, terpisah dari PlatformProgress.counts; sourceTotal bukan bukti lengkap. Akhir pagination terverifikasi diperlukan sebelum menandai seluruh komentar/balasan tersedia telah ditelusuri; batas waktu/stop menghasilkan data parsial.

Job publik hanya membawa connector.state/version/lastSeenAt. Job TikTok dibuat WAITING_CONNECTOR dengan startedAt/deadlineAt kosong. Handshake versi/build/policy yang sesuai memulai waktu tepat sekali. Reconnect tidak mereset startedAt, deadline atau dedup. Sesi kedaluwarsa/putus tidak menambah hitungan; deadline yang sudah dimulai tetap berjalan. Finalisasi menutup pairing sambil mempertahankan data parsial. Endpoint privat wajib memeriksa job benar-benar milik proyek, sumber TikTok, izin operator dan transisi state secara atomik.

Demo menyimpan pairing dalam Map memori; metadata job saja tersimpan lokal. Tombol pengujian demo tidak mengakses Chrome/bridge nyata. Tidak ada implementasi gateway/backend baru atau perubahan proses crawling aktif pada perubahan frontend ini.

## Migrasi per transaksi dan sosmed

1. POST `/acquisition-jobs/:jobId/platforms/:platform/migration-plans` menerima `{dataset_id, version, checksum, postgresql}`. Server harus mengambil dataset milik job/proyek tersebut dan hanya sumber tersebut. Tidak ada multipart atau unggah file. Sumber memuat seluruh post/komentar/reply dalam versi final, bukan preview browser. Respons `TransactionMigrationPlan`: id, expiry, jobId, platform, datasetId, version, checksum, crawlDate, total, host, port. Rahasia tidak dikembalikan.
2. POST `/acquisition-jobs/:jobId/platforms/:platform/migrations` menerima `{plan_id}` dan Idempotency-Key. Plan terikat sesi/proyek/versi/checksum/target. Client tidak mengirim ulang baris atau kredensial. Respons TransactionMigration.
3. GET `/transaction-migrations/:id` memeriksa izin sumber yang sama, mengembalikan metadata plan ditambah status/phase/createdAt/updatedAt/processed/inserted/skipped/error. Frontend menolak hasil yang tidak sesuai job/platform/dataset/version yang sedang dibuka.

Antrean, pemeriksaan dan penyalinan harus terlihat pada progres. inserted hanya menghitung data yang benar-benar committed; processed bukan bukti data tersimpan. Native ID yang sudah ada dilewati tanpa ditimpa, tetap unik pada target meski diulang atau paralel. Jangan mengandalkan hitungan dari klien untuk identitas/deduplikasi. Jalankan migrasi hanya untuk dataset diterbitkan dengan konten; pekerjaan berjalan atau sumber yang tidak mempunyai data harus ditolak.

Saat ini hanya adapter demo memodelkan review, idempotensi dan progres di memori. Tidak ada implementasi penulis PostgreSQL, SQL baru atau perubahan skema. **No migration required** dalam lingkup frontend.
