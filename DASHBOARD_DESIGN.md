# Dashboard BeeSense

[SocialNLPStreamlitApp](nlp_dashboard.py) membaca run aktif dari [social_nlp.json](social_nlp.json). Dashboard tidak melakukan crawling atau training. File dataset dan hasil clustering yang dikirim bersama repository dijelaskan dalam [README.md](README.md).

## Lima tampilan

1. **Ringkasan:** volume kalimat/komentar, 12 topik terbesar dalam batang YouTube/Reddit, cakupan/noise tiap platform, serta distribusi menurut bulan post induk.
2. **Peta topik:** kode T01–T51, ukuran menurut kemunculan kalimat dan warna menurut proporsi platform. Biru Reddit, toska seimbang, merah YouTube. Posisi model penuh tetap di bawah filter; topik tanpa edge tetap ada. Garis adalah kemiripan semantik, bukan hubungan antar akun.
3. **Penjelasan topik:** deskripsi ekstraktif, label pola, narasi perbandingan periode, grafik porsi dan bukti sumber. Panel Mengapa penjelasan ini muncul? membuka aturan dan dukungan data.
4. **Kalimat & sumber:** tabel maksimal 1.000 baris, detail kalimat/tanggal/judul/URL dan unduhan seluruh hasil filter. Graf kalimat topik dibatasi 100 representatif.
5. **Metode & data:** evaluasi kandidat, metadata model, bagian terlewat dan keterbatasan.

## Definisi angka

Snapshot: 16.178 kemunculan, 15.878 kalimat unik, 7.944 komentar/balasan terwakili, 51 topik. Cakupan kemunculan 8.628/16.178 = 53,3%; cakupan unik 8.427/15.878 = 53,1%. YouTube 8.337 kemunculan/5.644 komentar/60,4% cakupan; Reddit 7.841/2.300/45,8%.

Occurrence, kalimat unik dan komentar adalah unit berbeda. Komentar memakai identitas platform/source_row; dapat menghasilkan beberapa kalimat dan topik. Porsi penjelasan menggunakan komentar bertopik dibagi seluruh komentar terwakili bulan itu, termasuk noise. Porsi antar topik tidak harus berjumlah 100%.

Distribusi memakai tanggal post/video asal; tanggal komentar YouTube tetap perkiraan. Parser tanggal campuran mempertahankan mikrodetik Reddit. Ringkasan jumlah dapat menampilkan nol bulan kosong dalam snapshot; grafik porsi penjelasan meninggalkan celah pada bulan tanpa dukungan. Bulan kalender parsial tidak menentukan arah.

## Interaksi dan aksesibilitas

Kontrol native Streamlit ≥1.66 memakai binding query-params untuk platform, tanggal, pencarian literal, topik, view dan slider. Klik chart/tabel memperbarui topik sebelum rerun. Dropdown memberi alternatif keyboard. Reset mengembalikan filter. Nilai tersimpan node_limit dibatasi sebelum slider dibuat ketika hasil pencarian mengecil; pilihan yang masih valid dipertahankan dan kasus satu topik tetap aman.

Palet kertas putih, latar #F4F7FB, tinta #172D43, teks sekunder #52657B, aksen #116D78. Angka memakai tabular numerals, locale Indonesia melalui Babel, fokus terlihat, caption berkontras, pembungkusan teks, reduced motion dan susunan ringkasan responsif. Grafik memiliki deskripsi serta tabel alternatif. Kutipan HTML di-escape dan link sumber dibatasi HTTP(S).

Review mengikuti [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md). Grafik tetap membutuhkan penafsiran: sumbu layout bukan ukuran semantik terkalibrasi dan label otomatis belum ditinjau manusia.

## Verifikasi dan batas

Tes mencakup unit/noise, filter literal, timestamp campuran, posisi stabil, proporsi platform, event cluster nol, URL/reset, seluruh view, penjelasan dan guard agar UI tidak training. Regresi slider mencakup hasil dua/satu/nol topik serta URL berisi nilai tidak valid. Pengujian browser mencakup pencarian beasiswa 51→14 dan reload. Perintah pengujian ada pada README.

Cache mengikat identitas artifact serta lingkup filter; penjelasan juga mengikat hash kode dan opsi. Dokumen [EXPLAINABLE_TOPICS.md](EXPLAINABLE_TOPICS.md) menjelaskan algoritma dan batas inferensi. Dockerfile non-root membaca artifact read-only; build/runtime Docker belum diverifikasi karena daemon lokal belum aktif. Tidak perlu migrasi database.
