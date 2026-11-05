# Retraining seluruh sosmed dengan TikTok — 5 November 2026

Status: **kedua fitting selesai, masing-masing 20 topik dan mean c_v ≥0,4**.
Sebanyak 40 narasi Gemini tersimpan dalam dua snapshot final. Konfigurasi aktif
memakai pasangan baru; paket diverifikasi sebelum commit/push ke main.

## Sumber dan penggabungan

`outputs/social_20261105_combined_tiktok_01/social_data.xlsx` menggabungkan workbook
aktif sebelumnya dengan seluruh 11 partisi platform/tanggal WIB pada
`outputs/crawling`. Dua belas workbook sumber diverifikasi sebelum/sesudah merge.
Urutan kemunculan native pertama dipertahankan dan observasi terakhir yang
diberikan menang ketika ID berulang; tidak ada crawling ulang saat merge.

Hasil: **36.233 record unik**, **2.552 root** dan **33.681 komentar/balasan**.
Sebanyak **34.764 pengulangan antarfile** disisihkan; **nol duplikat native ID** dan
nol komentar yatim pada workbook gabungan. `merge_report.json`,
`record_lineage.jsonl`, `duplicate_records.jsonl` dan `native_roots.json` mengikat
asal, identitas percakapan X dan checksum. Workbook sumber lama dipertahankan.

| Platform | Post/video | Komentar | Balasan | Total |
| --- | ---: | ---: | ---: | ---: |
| YouTube | 1.238 | 19.770 | 4.150 | 25.158 |
| Reddit | 297 | 2.409 | 1.808 | 4.514 |
| Instagram | 626 | 3.680 | 138 | 4.444 |
| X / Twitter | 366 | 198 | 105 | 669 |
| TikTok | 25 | 617 | 806 | 1.448 |

Rangkaian TikTok hari ini menyimpan 7 post, 492 komentar dan 537 balasan unik.
Run terakhir sampai 16.00 WIB menyimpan nol record yang lolos seleksi: dua root
berada di luar periode dan satu gagal include keyword. Pada root terakhir sempat
teramati 115 komentar dan 196 balasan; angka tersebut **bukan hasil tersimpan**.
Target 1.000 post serta seluruh komentar tidak tercapai. Tanggal partisi adalah
tanggal crawling WIB, sedangkan kolom tanggal publikasi tetap mengikuti sumber.

## Pipeline dan dukungan TikTok

Producer SocialNLP **2.6.1** menerima TikTok pada penjelasan/tren. Root percakapan
memakai native video/photo ID dari URL HTTPS TikTok, sehingga komentar dan balasan
pada post yang sama tidak dianggap post terpisah. Judul, tanggal dan platform
merupakan provenans; teks komentar/balasan saja menjadi fitur embedding.
Dashboard menambahkan TikTok pada filter, tabel topik, cakupan/noise, bulanan,
warna/hover jaringan dan tren penjelasan. Launcher membaca pasangan snapshot
terbaru dari `config/dashboard.json`, bukan direktori baseline bertanggal tetap.

Persiapan korpus: **55.257 kemunculan**, **53.967 kalimat unik**, **1.290 pengulangan
kalimat**, dan **6.136 segmen dilewati** menurut aturan min panjang/kata yang ada.
Encoder SBERT multilingual tetap pralatih dan dipin pada revision yang sama;
embedding korpus baru dihitung lokal. UMAP dua seed, DBSCAN dan penggabungan Ward
berbobot dijalankan kembali. Target tepat **20 topik**, gate mean **c_v ≥ 0,4**,
top-10 istilah dan window 110. Ambang tidak diturunkan. Coherence adalah evaluasi
in-sample, bukan akurasi berlabel atau jaminan setiap topik mencapai 0,4.

| Snapshot | Sebelum filter | Setelah filter |
| --- | ---: | ---: |
| Jumlah topik | 20 | 20 |
| Mean c_v | 0,4346102845 | 0,4666033620 |
| Topik dengan c_v <0,4 individual | 10 | 6 |
| Kalimat unik | 53.967 | 10.795 |
| Kemunculan | 55.257 | 11.185 |
| Coverage kalimat unik | 95,75% | 81,81% |
| Silhouette cosine | -0,011752 | 0,062782 |
| ARI dua seed | 0,803763 | 0,641173 |
| DBSCAN eps / min_samples | 0,2 / 3 | 0,2 / 5 |
| Kelompok DBSCAN sebelum Ward | 508 | 154 |

Snapshot fitted asli: `outputs/nlp_20261105_all_social_topics20_01/` dan
`outputs/nlp_20261105_relevance_topics20_01/`. Snapshot bernarasi yang dipakai UI:
`outputs/nlp_20261105_all_social_topics20_gemini_01/` dan
`outputs/nlp_20261105_relevance_topics20_gemini_01/`. Mask baru terikat checksum
workbook: `outputs/relevance_20261105_01/`. Keputusan 55.257 kemunculan mencakup
11.185 relevan, 19.739 interaksi umum, 3.833 di luar lingkup dan 20.500 meragukan.
Embedding subset hanya digunakan kembali setelah sumber, model, teks serta
sentence ID diverifikasi; proyeksi/clustering/evaluasi tetap diulang. Skor memakai
korpus referensi berbeda dan tidak membuktikan kenaikan kualitas secara langsung.

## Narasi, verifikasi dan publikasi

Fitting dijalankan **lokal tanpa Gemini**. Setelah melihat preview ekspor, pengguna
secara eksplisit mengizinkan **400 keyword dan 400 kalimat representatif** dikirim
ke Google Gemini `gemini-3.5-flash-lite` untuk **40 narasi**. Pengayaan berhasil;
prompt hash seluruh CSV cocok dengan payload yang disetujui. Dua snapshot final
masing-masing memuat tepat 20 kalimat topik/deskripsi dengan provenance, token dan
checksum. Seluruh file fitted selain summary identik dengan snapshot tanpa narasi.
Narasi adalah sintesis AI dari contoh terpilih, bukan ukuran popularitas. API key
hanya dibaca dari auth lokal; dashboard tidak meminta API pada rerun.

Validasi: **122 tes NLP/dashboard lulus**, lint/format Ruff lulus. Crawler diuji
pada environment sesuai dependensinya: **229 tes proyek lulus (10 skip opsional)**,
**24 tes Twitter**, **7 fixture DOM TikTok** dan **11 tes Node ekstensi** lulus.
Frontend: **45 Vitest + 2 tes proyeksi Node**, lint, typecheck, API build dan demo
production build lulus; desktop/mobile tidak overflow dan teks utama minimal 13px.
UI TikTok mengikat flow konfigurasi, pairing dan progress pada satu transaksi.
HTTP gateway/worker masih kontrak untuk implementasi berikutnya; mode demo diberi
label dan tidak mengendalikan Chrome nyata.

Snapshot baru diperiksa pada kelima tampilan dan filter TikTok tanpa training/API;
environment Cloud minimal juga menguji pergantian snapshot dan CSV Gemini.
Pemeriksaan data publik memverifikasi workbook aktif, mask baru/lama, seluruh
manifest model dan baseline, serta kesesuaian allowlist Git. Snapshot lama dan
sumber asli dipertahankan. Rollback pembacaan: pilih Sebelum penyaringan pada
sidebar; untuk rollback versi sebelumnya, ubah pointer config ke bundle arsip
beserta pasangan/mask yang sesuai, tanpa menimpa artifact.

Dashboard native lokal sesi ini menggunakan http://127.0.0.1:8502. Tidak ada
migrasi database atau penulisan PostgreSQL. Konfigurasi produksi/dashboard Docker
serta environment produksi tidak diubah dalam sesi ini. **No migration required.**
Docker daemon tidak berjalan: image baru **belum diverifikasi**, meskipun aplikasi
native lulus uji. Pemeriksaan yang masih perlu dilakukan ketika Docker tersedia:

```sh
docker build -f deployment/docker/Dockerfile.dashboard -t beesense-dashboard:local .
```

Publikasi memakai commit lalu fast-forward branch main dan push origin main sesuai
permintaan pengguna. Tidak ada deploy manual atau perubahan pengaturan Streamlit
Cloud. Status CI/commit aktual dilaporkan setelah push; catatan ini bukan bukti
bahwa deployment produksi telah berjalan.
