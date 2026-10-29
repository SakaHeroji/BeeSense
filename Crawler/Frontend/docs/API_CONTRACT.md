# Kontrak Integrasi Crawler Frontend

Kontrak **yang diharapkan frontend**, belum merupakan backend yang sudah berjalan. Tipe lengkap berada di [`src/shared/types.ts`](../src/shared/types.ts), transport di [`src/shared/api.ts`](../src/shared/api.ts). PRD Backend perlu menetapkan OpenAPI dan penyimpanan berdasarkan kontrak ini.

## Transport

Prefix: `${VITE_API_BASE_URL}/projects/${VITE_PROJECT_ID}`, bawaan `/api/v1/projects/university-intelligence`. Semua respons JSON. Sesi memakai cookie HTTP dengan `credentials: include`; jika beda origin, backend harus mengatur CORS allowlist, cookie, CSRF/origin validation, dan kebijakan sesi yang sesuai. Tidak ada token dalam URL atau localStorage.

| Metode dan path sesudah prefix                              | Bentuk respons                                                                                                                                                                                                                          |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET /session`                                              | `Session`: nama, role operator/observer, canExport.                                                                                                                                                                                     |
| `GET /crawler/capabilities`                                 | `Capabilities`: platform tersedia, batas konfigurasi/upload, daftar baseline dengan required/ready, dukungan sesi worker dan skema survei NLP.                                                                                          |
| `GET /acquisition-jobs`                                     | `Job[]`, riwayat yang dapat diakses; backend harus membatasi dan merancang paginasi ketika koleksi bertambah.                                                                                                                           |
| `GET /acquisition-jobs/:id`                                 | `Job` snapshot penuh, `snapshotVersion` meningkat, status dan `canStop` otoritatif.                                                                                                                                                     |
| `POST /acquisition-plans/validate`                          | Body `{config}`; `Plan` dengan ID, konfigurasi efektif, expiry, warnings. Tanpa request crawling.                                                                                                                                       |
| `POST /acquisition-jobs`                                    | Body `{plan_id}`, header Idempotency-Key. Respons Job. Replay key yang sama mengembalikan Job yang sama; konfigurasi plan disimpan server.                                                                                              |
| `POST /acquisition-jobs/:id/stop`                           | Body `{}`; idempoten, mengembalikan Job. STOP_REQUESTED tidak berarti finalisasi selesai.                                                                                                                                               |
| `POST /acquisition-jobs/:id/verification-session`           | `{url?,message}`; URL pendek umur ke sesi worker yang benar, atau penjelasan mengapa belum tersedia. Meminta sesi tidak mengubah status akses menjadi pulih.                                                                            |
| `POST /crawler/urls/validate`                               | Body `{urls,baselines}`; `UrlReview[]` normalisasi dan hasil deduplikasi. Ini endpoint pendukung tambahan dari PRD.                                                                                                                     |
| `POST /survey-imports/validate`                             | Body `{rows:SurveyAnswer[]}`; staging+validasi terpadu, respons `SurveyReview` dengan ID, fingerprint/expiry, kategori respons, issue dan validRows. Mendetailkan langkah staging PRD menjadi satu permintaan untuk frontend awal.      |
| `POST /survey-imports/:id/commit`                           | Body `{validation_id,fingerprint,accept_valid_only:true}`, header Idempotency-Key. Respons Job, dataset sesudah finalisasi. Server mengikat review ke sesi/proyek, memvalidasi ulang konflik, tidak mempercayai validRows dari browser. |
| `GET /datasets/:id/versions/:version?page=&search=&source=` | `DatasetDetail`: metadata, halaman maksimal 50 PreviewRow, total hasil filter, daftar berkas tervalidasi dan URL unduh terotorisasi.                                                                                                    |
| `POST /nlp-input-selections`                                | Body `{dataset_id,version,checksum,accept_partial}`; respons `{id}`. Tidak menjalankan training.                                                                                                                                        |

Frontend API mengirim tanggal konfigurasi dari input lokal WIB (`YYYY-MM-DDTHH:mm`). Wrapper backend harus mengubahnya ke ISO dengan offset `+07:00`; jangan menafsirkan sebagai zona server. Snapshot menggunakan ISO dengan zona. Nama field payload mengikuti tipe TypeScript camelCase; wrapper Python perlu pemetaan eksplisit ke nama parameter crawler snake_case.

## Aturan server

- Mode `url` mengeksekusi daftar URL saja. Jangan memakai fallback query crawler ketika tidak ada URL efektif; tolak permintaan kosong.
- Target social dipisah dari roots/qualified/comments/replies; tanpa URL tambahan tersembunyi. Baseline wajib tidak dapat dihapus operator.
- Job QUEUED belum mempunyai deadline; worker menetapkan startedAt/deadlineAt. Durasi menunggu CAPTCHA/429 tetap mengurangi batas global.
- FINALIZING belum memiliki dataset publik; dataset_ref/`dataset` diisi sesudah ekspor dan validasi manifest berhasil. Job FAILED tidak menawarkan file setengah jadi.
- Snapshot menyertakan counts, event ringkas, seri progres, alasan, dan hak tindakan. Pola polling tidak memberi wewenang pada tab untuk menjalankan atau mempertahankan worker.
- Survei memakai satu baris per jawaban, commit atomik satu respons lengkap, peran dideklarasikan, izin granted, dan metadata provenance berversi. Teks pertanyaan tidak digabung ke teks jawaban.
- Query/body diakses hanya oleh proyek dan pengguna berizin. Pembatasan host/redirect URL, file, formula, dan deduplikasi harus ditegakkan server, meski frontend sudah memvalidasi.

Error JSON: `{message, code?, fields?:[{field,message}], correlation_id?}`. Jangan mengirim stack trace, cookie, token, atau isi jawaban pada pesan umum. Bedakan 401/403, 409 konflik, 422 invalid, 429 API BeeSense, dan 429 platform di snapshot worker. Respons non-JSON diperlakukan sebagai backend belum tersedia.

Perluasan berikutnya: paginasi riwayat di server, SSE dengan event ID/replay, template survei dinamis, dan login organisasi. Endpoint/tipe yang berubah harus mengubah adapter beserta tes kontraknya, bukan membuat komponen menebak payload.

## Kontrak tujuh sumber

ID platform: `youtube`, `reddit`, `instagram`, `tiktok`, `threads`, `facebook`, `x`. Backend hanya mengembalikan ID dengan adapter siap pada `Capabilities.platforms`; UI menampilkan sumber lainnya dalam keadaan nonaktif disertai alasan. Tidak ada fallback dari sumber yang belum tersedia ke YouTube/Reddit. Konfigurasi membawa tujuh entri `platforms`, tetapi worker hanya mengeksekusi yang `enabled`; default lima sumber baru nonaktif. Backend harus mengabaikan field nonaktif atau memvalidasi strukturnya tanpa menjalankan sumbernya.

`Job.platforms` berisi sumber yang dipilih. Setiap titik `Job.series` berbentuk `{at, youtube?, reddit?, instagram?, tiktok?, threads?, facebook?, x?}`; nilai adalah qualified kumulatif per sumber, tidak menjumlahkan roots/komentar/reply. Semua filter sumber dan preview memakai ID yang sama. Batas/rate limit berbeda per platform; status alasan tetap berasal dari worker.

Validasi URL lokal hanya mengenali permalink lengkap dan menghapus tracking; tidak membuka tautan atau mengikuti redirect. Short link TikTok, profil, Story Instagram, dan tautan share Facebook ditolak dengan petunjuk meminta permalink lengkap. `UrlReview.locatorKey` adalah kunci normalisasi lokal. Shortcode Instagram/Threads dan locator Facebook **bukan bukti native ID final**; `nativeId` boleh kosong sampai backend menyelesaikan ID tersebut. Backend wajib deduplikasi kembali dengan native ID final lintas alias, termasuk username/numeric owner Facebook. `valid` menyatakan format dapat diproses, bukan jaminan konten dapat diakses.

`Dataset.nlpSupported` harus dihitung dari versi skema dan seluruh sumber dataset yang telah diuji adapter NLP. Jangan menandainya true hanya karena label platform tersedia pada UI. Mode demo menolak handoff dataset survei dan dataset dengan salah satu dari lima sumber baru.

Referensi format permalink: [Meta official embed plugin](https://github.com/facebook/meta-embeds-for-wordpress/blob/main/README.md) dan [TikTok embed player](https://developers.tiktok.com/docs/en/embed-player). Pola yang belum didukung tetap ditolak, lalu perluasan kontrak harus disertai validasi backend.
