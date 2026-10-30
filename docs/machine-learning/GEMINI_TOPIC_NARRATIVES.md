# Kalimat dan deskripsi topik melalui Gemini

## Snapshot terbaru

Konfigurasi aktif kini memakai `outputs/nlp_20261030_instagram_500_topics20_01` dari `outputs/social_20261030_combined_instagram_500_2h_02/social_data.xlsx`: 20 topik, rata-rata c_v 0,4386500025. Excel snapshot lengkap berisi 45.556 pasangan topik–kalimat asli unik; label run ini c-TF-IDF lokal. Lihat [README](../../README.md) dan metode Social NLP untuk data serta batas interpretasi. Catatan hasil/narasi Gemini berikut merupakan riwayat snapshot sebelumnya.


`SocialNLPClusterer` 2.4 menambahkan ringkasan berbahasa Indonesia setelah training,
clustering dan penggabungan menghasilkan **20 topik** dengan **rata-rata coherence
c_v minimal 0,4**. Gemini tidak mengubah keanggotaan cluster, keyword, bobot,
coherence atau pengukuran stabilitas model.

## Alur dan konfigurasi

`MachineLearning/social_nlp.py` menghitung dan menyimpan 12 istilah positif beserta
bobot c-TF-IDF pada `topics.json`. Ketika `gemini.enabled` aktif, `save()` memanggil
`generate_topic_narratives()`. Transport dan validasi berada di
`MachineLearning/topic_narratives.py`, terpisah dari Streamlit.

Setiap topik mengirim **10 keyword dengan bobot tertinggi** dan **10 kalimat
representatif** ke satu request `generateContent`. Kalimat diambil dari
`sentences.parquet` pada cluster yang sama, diurutkan menurut cosine similarity
dengan centroid secara menurun; ID kalimat menjadi pemecah seri yang stabil.
Jika cluster kecil berisi kurang dari 10 kalimat unik, seluruh kalimatnya dipakai.
Pada model 30 Oktober, setiap topik memiliki 10 contoh. Kalimat asli dikirim
sesuai permintaan pengguna; kredensial, profil browser, serta metadata akun tidak
disertakan. Kalimat dan keyword diperlakukan sebagai data, termasuk bila berisi
permintaan atau instruksi.

Prompt `beesense-topic-id:2` meminta satu kalimat topik lengkap dan alami
(idealnya 12–25 kata, maksimal 40) serta deskripsi 2–3 kalimat yang meneruskan
gagasannya (maksimal 120 kata). Model diminta menyarikan inti pembahasan,
mengabaikan kata pengisi dan variasi ejaan, serta tidak memaksakan semua keyword
ke dalam satu kalimat. Konteks pendidikan, hubungan antarnama, sentimen, statistik,
tren, dan sebab akibat hanya boleh disebut jika didukung masukan; contoh kalimat
bukan sampel acak yang mewakili seluruh platform. Keterbatasan dijelaskan bila
perlu tanpa penyangkalan yang berulang. Contoh gaya dan peninjauan bahasa sebelum
menjawab membantu menghindari daftar keyword yang menyamar sebagai kalimat.

Konfigurasi menggunakan blok berikut tanpa menyimpan API key:

```json
"gemini": {
  "enabled": true,
  "model": "gemini-3.5-flash-lite",
  "auth_file": "config/auth.json",
  "timeout_seconds": 60,
  "max_attempts": 3,
  "request_interval_seconds": 5
}
```

Key dibaca dari field `gemini_api_key` pada objek JSON lokal atau satu objek dalam
array `config/auth.json`. File ini diabaikan Git dan dikecualikan dari image.
Header `x-goog-api-key` dipakai; key tidak masuk URL, konfigurasi model, CSV,
manifest, log atau Graphify. Dashboard Cloud tidak memerlukan key ini.

HTTP 429/5xx dan gangguan jaringan memakai maksimum tiga percobaan, timeout
terbatas dan jeda. Kesalahan akses, respons terblokir/terpotong, JSON tidak valid,
lebih dari satu kalimat topik atau cakupan topik yang kurang menggagalkan
publikasi. Tidak ada label buatan lokal sebagai pengganti respons Gemini gagal.
Receipt lokal pada cache mengikat sumber, model, prompt dan keyword; pengulangan
publikasi identik memakai receipt tanpa memanggil ulang topik yang sudah selesai.

## CSV dan dashboard

`topic_narratives.csv` memakai UTF-8 BOM agar mudah dibuka di Excel, satu baris per
topik: `cluster_id`, `topic_sentence`, `topic_description`, `keywords_json`, provider,
`representative_sentences_json` (ID, teks dan skor), hash kalimat representatif,
model/version, waktu UTC, versi/hash prompt, hash keyword/sumber/respons dan token
usage bila diberikan API. `cluster_id` 0–19 tampil sebagai T01–T20 pada UI.

CSV disimpan atomik bersama artefak model dan dicakup checksum manifest. Extension
`gemini-topic-narratives:2` wajib cocok dengan summary dan CSV. Loader memeriksa
20 topik, coherence, keyword, bobot, urutan kalimat representatif dan provenance
terhadap Parquet sebelum menampilkan hasil. Snapshot lama tanpa extension dan
CSV keyword-only `gemini-topic-narratives:1` tetap dapat dibaca memakai prompt
historisnya. Perubahan prompt maupun konteks menghasilkan fingerprint cache baru.

Dashboard menyediakan tabel 20 kalimat/deskripsi, unduhan CSV, kalimat/deskripsi
topik terpilih, tabel 10 keyword beserta bobotnya, serta kalimat yang dikirim ke
Gemini. Ringkasan adalah sintesis AI atas keyword dan contoh kalimat model penuh,
bukan kutipan atau bukti statistik. Filter mengubah
hitungan dan bukti percakapan; ringkasan Gemini tetap sama. Pembukaan halaman dan
rerun tidak memanggil API dan tidak melakukan training.

## Verifikasi 30 Oktober 2026

Uji satu topik dari snapshot historis melalui API nyata berhasil dengan
`gemini-3.5-flash-lite`. Hasilnya disimpan sebagai diagnostik lokal terpisah,
bukan menggantikan model aktif. Sembilan tes offline memeriksa 20 request, urutan
bobot, pemilihan kalimat per cluster, invalidasi cache saat konteks berubah,
kompatibilitas CSV lama, resume, CSV/manifest/checksum, penolakan respons, kerahasiaan key,
batas retry dan tampilan Streamlit tanpa jaringan/training. Hasil Gemini untuk
model Instagram baru sudah lengkap: 20 baris CSV lolos validasi.

Referensi utama: [structured output](https://ai.google.dev/gemini-api/docs/generate-content/structured-output),
[GenerateContent API](https://ai.google.dev/api/generate-content) dan
[daftar model](https://ai.google.dev/gemini-api/docs/models).

Tidak ada perubahan database; CSV merupakan artefak turunan versi model baru.
**No migration required**. Docker dashboard menyertakan modul validasi ini; build
image belum diverifikasi selama daemon Docker lokal tidak tersedia.

## Model 30 Oktober terverifikasi

Input `outputs/social_20261030_combined_3days_02/social_data.xlsx` memuat **33.034 record unik**, **1.859 root**, dan **31.175 komentar/balasan** dari hasil akuisisi 27–30 Oktober. Sebanyak 49.952 pengulangan antarberkas disisihkan; pemeriksaan menemukan 0 ID native ganda. Total Instagram 324 post/3.038 komentar mencakup batch terbaru 248 post/2.128 komentar dan trial sebelumnya 76 post/910 komentar. Pengguna menghentikan crawling setelah HTTP 429; target 1.000 post dan durasi 3 jam belum tercapai.

Run sesi sebelumnya `outputs/nlp_20261030_instagram_topics20_02` menghasilkan **20 topik**, rata-rata **c_v 0,4315219014**, coverage **94,67%**, silhouette cosine **-0,057864**, dan ARI dua seed **0,820417**. DBSCAN eps=0,25/min_samples=10 menghasilkan 165 kelompok primer, lalu Ward berbobot menggabungkannya menjadi 20 topik. Noise terdiri atas 2.751 kalimat unik. Persiapan menghasilkan 52.451 kemunculan/51.612 kalimat unik, 839 pengulangan dan 5.516 segmen dilewati; 28.758 komentar/balasan terwakili. Fitting inti berlangsung 1.195,5 detik sebelum tahap Gemini.

Gemini `gemini-3.5-flash-lite` menghasilkan **20 kalimat topik dan deskripsi bahasa Indonesia**, masing-masing dari 10 keyword c-TF-IDF berbobot tertinggi dan 10 kalimat terdekat dengan pusat topik. `topic_narratives.csv` beserta provenance/checksum masuk bundle model. UI membaca CSV tanpa API atau training saat rerun. Sebanyak 8 dari 20 topik masih memiliki c_v individual <0,4; ambang berlaku pada rata-rata. Evaluasi ini in-sample, bukan akurasi berlabel atau holdout. Skor dari korpus berbeda tidak menjadi perbandingan kualitas langsung.

Publikasi memakai GitHub main, entry `streamlit_apps.py`, target `https://beesense.streamlit.app`. Pemeriksaan lokal mendahului push; API key tidak diperlukan pada Cloud. No migration required. Docker daemon tidak tersedia sehingga build/startup image belum diverifikasi.
