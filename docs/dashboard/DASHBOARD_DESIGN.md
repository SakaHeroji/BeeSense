# Dashboard BeeSense

[SocialNLPStreamlitApp](../../Dashboard/app.py) membaca snapshot aktif dari [social_nlp.json](../../config/social_nlp.json). Dashboard tidak melakukan crawling atau training. Jumlah topik, coherence, volume, tanggal, dan bukti selalu dibaca dari artifact terverifikasi, bukan angka yang ditulis di UI.

## Alur eksplorasi

1. **Ringkasan:** komentar dan kalimat pada filter, 12 topik terbesar per platform, cakupan/noise, serta distribusi menurut bulan post induk. Pilihan topik mempunyai tombol **Jelaskan topik ini**.
2. **Peta topik:** posisi model penuh tetap di bawah filter. Ukuran menunjukkan kemunculan kalimat; warna menunjukkan campuran YouTube/Reddit. Garis adalah kemiripan semantik. Dropdown memberikan alternatif keyboard untuk pemilihan node.
3. **Penjelasan topik:** fokus pada topik terpilih terlebih dahulu. Empat card merangkum komentar unik, porsi komentar, post asal, dan coherence topik dengan rata-rata model sebagai pembanding. Grafik menunjukkan istilah, platform, lima post penyumbang, serta porsi bulanan. Kutipan asli dan tautan sumber membantu memeriksa penjelasan. Perbandingan seluruh topik berada dalam panel terlipat.
4. **Kalimat & sumber:** tabel maksimal 1.000 baris, detail tanggal/judul/URL, unduhan seluruh hasil filter, serta graf maksimal 100 kalimat representatif.
5. **Metode & data:** protokol coherence, skor per topik, evaluasi kandidat, konfigurasi, checksum, bagian terlewat, dan keterbatasan. Catatan pembentukan topik juga tersedia di bagian bawah halaman.

## Arti angka

Kemunculan, kalimat unik, komentar, dan post asal adalah unit berbeda. Komentar memakai platform + source_row Excel; satu komentar dapat menyumbang beberapa kalimat dan topik. Porsi topik memakai komentar bertopik dibagi seluruh komentar terwakili pada filter, termasuk noise, sehingga porsi antar topik tidak harus berjumlah 100%.

Grafik istilah menghitung kalimat unik terfilter yang memuat istilah c-TF-IDF model penuh dengan batas kata/frasa. Ini frekuensi kehadiran, bukan bobot c-TF-IDF atau probabilitas. Grafik sumber menghitung komentar unik per video/thread; ID induk menjaga dua post dengan judul sama tetap terpisah. Jika identitas induk memakai hash konteks, UI memberi catatan. Sumber dominan >60% juga mendapat catatan.

Coherence c_v model penuh dan coherence topik terpilih ditampilkan terpisah. Target rata-rata ≥0,4 tidak menjamin setiap topik mencapai 0,4. Filter mengubah jumlah serta bukti; keanggotaan dan skor model tidak dihitung ulang. Skema artifact lama tetap terbaca. Coherence adalah keselarasan leksikal pada korpus, bukan akurasi, validasi manusia, atau ukuran keterwakilan platform.

Distribusi default memakai tanggal post/video asal, bukan riwayat penulisan komentar. Tanggal perkiraan diberi tanda. Grafik porsi meninggalkan celah pada bulan parsial, tanpa pengamatan, atau dengan dukungan kecil. Narasi arah mengikuti dukungan dan pemeriksaan campuran platform dalam [EXPLAINABLE_TOPICS.md](../machine-learning/EXPLAINABLE_TOPICS.md).

## Interaksi dan aksesibilitas

Kontrol native Streamlit memakai binding query-params untuk platform, tanggal, pencarian literal, topik, tampilan, dan slider. Memilih grafik/tabel atau membuka penjelasan mempertahankan filter. Reset mengembalikan lingkup data. Nilai slider dibatasi sebelum dibuat saat hasil mengecil; kasus satu/nol topik aman. Kondisi kosong menyertakan tindakan pemulihan.

Palet putih, latar #F4F7FB, tinta #172D43, teks sekunder #52657B, aksen #116D78; warna platform tetap konsisten. Avenir Next memakai fallback sistem tanpa unduhan font. Angka menggunakan locale Indonesia melalui Babel dan tabular numerals. Fokus keyboard terlihat, reduced motion dihormati, judul/teks panjang membungkus, dan card menjadi dua kolom pada layar sempit. Grafik memiliki deskripsi dan tabel alternatif. Kutipan HTML di-escape; link sumber hanya HTTP(S).

Review memakai [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md). Pemeriksaan mencakup label, struktur heading, skip link bawaan Streamlit, fokus, URL state, kondisi kosong, bounded tables, reduced motion, dan overflow. Pengujian ini bukan sertifikasi aksesibilitas penuh terhadap seluruh komponen pihak ketiga.

## Verifikasi dan runtime

Tes unit memeriksa identitas komentar/post, istilah berbatas kata, judul sumber identik, noise, filter, posisi stabil, dan pemisahan data/model. Streamlit AppTest mencakup seluruh tampilan, navigasi ke penjelasan dengan topik/filter tetap, URL/reset, serta guard tanpa training. Pemeriksaan browser desktop dan layar sempit memastikan card/grafik/bukti tampil dan tidak terjadi overflow horizontal.

Image `deployment/docker/Dockerfile.dashboard` telah dibangun dan container lokal `beesense-dashboard` diganti pada `http://127.0.0.1:8501`. Runtime non-root UID 10001 membaca snapshot melalui bind mount read-only, healthcheck aktif, dan hanya port loopback yang diterbitkan. Runtime akhir telah diverifikasi memakai run gabungan `outputs/nlp_20261029_combined_topics20_01`: 20 topik dan rata-rata c_v 0,4720. Grafik/card/bukti mengikuti filter pada snapshot tersebut. Tidak ada migrasi database.
