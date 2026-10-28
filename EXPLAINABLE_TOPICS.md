# Penjelasan dan tren topik BeeSense

Revisi 28 Oktober 2026, producer `1.1.0`. `SocialNLPClusterer` pada [social_nlp.py](social_nlp.py) kini menghasilkan penjelasan yang dapat ditelusuri untuk setiap cluster. `SocialNLPStreamlitApp` pada [nlp_dashboard.py](nlp_dashboard.py) menampilkannya melalui **Penjelasan topik**, serta detail topik pada tampilan lain. Pemisahan class ML dan UI tetap berlaku.

## Isi penjelasan

Setiap topik mempunyai istilah pembeda, deskripsi ekstraktif, tiga contoh kalimat asli beserta source_row Excel/tanggal/tautan, label pola, narasi perbandingan waktu, porsi bulanan gabungan/per platform, perubahan frasa, dan alasan keterbatasan. Kutipan berstatus **EXTRACTED**; pemilihan contoh, interpretasi cluster, dan arah merupakan **INFERRED**. Noise tidak diperlakukan sebagai satu topik koheren.

Deskripsi menggabungkan kosakata c-TF-IDF model penuh dengan kalimat representatif. Relevansi kandidat berbobot kedekatan centroid (0,45), kecocokan istilah pembeda (0,40), dan panjang informatif (0,15). Dari maksimal 200 kandidat, **Maximal Marginal Relevance (MMR)** menyeimbangkan relevansi dan redundansi cosine embedding dengan lambda 0,75. Bila tersedia, kalimat berisi istilah dan minimal enam kata didahulukan; sumber dari post/komentar berbeda diprioritaskan. Tanpa embedding, redundansi memakai token Jaccard. Ringkasan mengambil cuplikan maksimal 260 karakter; kalimat lengkap tetap tersedia pada bukti. Metode ini tidak menghasilkan parafrasa abstraktif atau diagnosis/sentimen/penyebab yang tidak dibuktikan sumber. Mutu label semantik tetap belum divalidasi dengan anotasi manusia.

## Mengukur pola waktu

Unit utama adalah **komentar/balasan yang menyumbang kalimat**: identitas platform + source_row Excel, bukan jumlah kalimat atau pengguna. Satu komentar dihitung sekali per topik per bulan, walaupun memiliki beberapa kalimat atau kalimat berulang. Komentar dapat memuat beberapa topik sehingga porsi antar topik tidak harus berjumlah 100%.

`porsi_topik_bulan = jumlah komentar terwakili yang memuat topik / seluruh komentar terwakili bulan itu`

Penyebut memasukkan komentar dengan kalimat noise. Baris yang seluruh isinya tidak lolos segmentasi tidak termasuk populasi ini. Parent post dideteksi lewat ID video YouTube atau ID thread Reddit pada URL. URL komentar Reddit dikembalikan ke thread induk. Jika ID tidak tersedia, hash konteks judul/tanggal digunakan dan diberi catatan.

Default memakai **tanggal post/video asal** (`post_date`). Ini distribusi komentar menurut tanggal sumber induknya, bukan riwayat kapan komentarnya ditulis. Pilihan `content_date` tersedia, tetapi tanggal komentar YouTube berupa perkiraan. Bulan kalender pada tepi rentang yang hanya teramati sebagian tidak menentukan arah. Bulan tanpa data mempunyai porsi `null`, bukan nol. Bulan tanpa topik tetapi memiliki pengamatan cukup mempunyai porsi nol yang sah. Grafik meninggalkan celah pada bulan parsial, tanpa pengamatan, atau dukungan kecil.

Arah memakai tiga komponen:

1. **Theil–Sen**: median kemiringan seluruh pasangan porsi bulanan, dalam poin persentase per bulan. Jarak bulan sebenarnya dipakai meskipun ada bulan kosong.
2. **Kendall tau-b**: konsistensi urutan porsi terhadap waktu; nilai ini tidak digunakan sebagai p-value atau probabilitas kebenaran.
3. **Dua jendela kalender lengkap terakhir**: default April–Juni dibanding Juli–September 2026 pada snapshot ini. Porsi jendela dihitung dari jumlah komentar, bukan rata-rata porsi bulanan.

Aturan default untuk “Indikasi meningkat”: perubahan jendela minimal +2 poin persentase, kemiringan minimal +0,25 poin/bulan, dan tau minimal +0,25. “Indikasi menurun” memakai batas negatif yang setara. Bila perubahan jendela memenuhi ambang tetapi arah sepanjang rentang tidak menguatkannya, labelnya “Menguat/Melemah belakangan”. Perubahan jendela kecil dengan rentang porsi bulanan minimal 10 poin menjadi “Fluktuatif”; selain itu “Relatif stabil belakangan”. Label stabil merujuk ambang dan jendela tersebut, bukan bukti tidak adanya perubahan.

Penentuan arah memerlukan minimal enam bulan layak, 20 komentar bertopik pada bulan layak, dan tiga post induk. Setiap bulan pembanding memerlukan minimal 20 komentar terwakili. Minimal salah satu jendela mempunyai lima komentar topik; jendela dengan topik nonnol memerlukan tiga post induk. Jika syarat gagal, labelnya **“Arah belum cukup jelas”**, sementara angka mentah tetap dapat diperiksa. Dukungan dibatasi bila satu post menyumbang >60% komentar topik atau identitas/tanggal sumber tidak pasti.

Perubahan campuran platform diperiksa: bobot YouTube/Reddit dari jendela pembanding dipertahankan dan dibandingkan dengan porsi aktual. Pemeriksaan ini memerlukan dukungan minimal 20 komentar untuk setiap platform aktif pada kedua jendela. Pergeseran komposisi ≥15 poin mendapat catatan. Bila arah aktual dan arah berbobot tetap berlawanan dan keduanya melewati ambang dua poin, label menjadi fluktuatif. Ini pemeriksaan sensitivitas sumber, bukan koreksi seluruh bias crawl.

Perubahan istilah membandingkan kehadiran frasa per komentar **dalam topik**, menggunakan maksimal 12 istilah c-TF-IDF model penuh. Minimal lima komentar pada dua jendela menyebut istilah dan perubahan frekuensi minimal dua poin. Peringkat memakai selisih log-odds dengan smoothing 0,5. Hasil tidak membuktikan isu baru lahir; istilah langka dan kosakata di luar model penuh tidak dianalisis.

## Konfigurasi dan API

Semua opsi berada dalam bagian `explanation` pada [social_nlp.json](social_nlp.json). Opsi mencakup dasar tanggal, penyertaan tanggal perkiraan, panjang jendela, dukungan minimum, ambang perubahan/slope/tau, dominasi sumber, pergeseran platform, serta MMR/jumlah bukti. Opsi tidak dikenal, rentang terbalik, nilai nonfinite dan rentang >120 bulan ditolak.

```python
from social_nlp import SocialNLPClusterer

data = SocialNLPClusterer.load_run("outputs/nlp_20261028_coherence_01")
options = SocialNLPClusterer("social_nlp.json").config["explanation"]
result = SocialNLPClusterer.explain_artifacts(data, options=options)
# Bisa dipakai setelah pipeline.fit_excel() / describe_topics():
# result = pipeline.explain_topics()
# Bisa mengirim subset occurrences dan batas tanggal khusus:
# result = SocialNLPClusterer.explain_artifacts(
#     data, subset, date_start="2026-01-01", date_end="2026-09-30", options=options
# )
SocialNLPClusterer.save_explanations(
    result, "outputs/penjelasan_baru", source_run="outputs/nlp_20261028_coherence_01"
)
```

Subset occurrence menentukan lingkup deskripsi, bukti, dan penyebut. `date_start/date_end` selanjutnya membatasi penghitungan waktu; keduanya tidak memotong contoh kalimat pada subset secara otomatis. Kosakata/centroid/keanggotaan tetap milik model penuh. Dashboard mengirim subset sesuai filter platform/kata/tanggal post asal dan rentang tanggal aktif. Pengaturan `content_date` akan tetap mengikuti filter awal tanggal post asal dashboard, lalu batas tambahan waktu komentar tersebut. Untuk analisis waktu komentar dengan lingkup lain, gunakan API Python.

```bash
# Tidak mengunduh model, meng-encode, melatih ulang, atau crawling:
.venv-nlp/bin/python social_nlp.py --explain-run outputs/nlp_20261028_coherence_01 \
  --output-dir outputs/penjelasan_baru
# Batas eksplisit opsional: --trend-start 2026-01-01 --trend-end 2026-09-30

.venv-nlp/bin/python -m streamlit run nlp_dashboard.py \
  --server.address=127.0.0.1 --server.port=8501
```

Dashboard menghitung penjelasan ketika tampilan penjelasan dibuka atau topik dipilih. Cache mengikat checksum manifest sumber, ID occurrence terfilter, rentang waktu, opsi dan hash kode algoritma. Tabel perbandingan, grafik porsi, narasi, dan bukti dapat ditelusuri. Panel **Mengapa penjelasan ini muncul?** memuat slope, tau, dukungan, aturan, perubahan istilah, serta tabel bulanan. Unduhan JSON mencakup penjelasan sesuai filter; state tampilan/topik/filter tersimpan di URL. Hasil fit lama tidak dimodifikasi atau dimuat dari pickle.

## Hasil aktual dan persistensi

Dashboard menghitung penjelasan dari run aktif outputs/nlp_20261028_coherence_01. File ekspor penjelasan historis telah dibersihkan; gunakan API/CLI di atas bila memerlukan sidecar baru, yang secara default diabaikan Git.

Hasil hitungan dan contoh numerik berikut adalah **historis dari run v1 `outputs/nlp_20261028_02`** (51 topik HDBSCAN), bukan angka untuk 52 topik DBSCAN aktif. Label dan arah run baru dihitung ulang saat dibuka.

| Pola snapshot v1 | Topik |
|---|---:|
| Indikasi meningkat | 1 |
| Indikasi menurun | 1 |
| Menguat belakangan | 2 |
| Melemah belakangan | 3 |
| Fluktuatif | 3 |
| Relatif stabil belakangan | 36 |
| Arah belum cukup jelas | 5 |

Sebanyak 51 topik dijelaskan dari 16.178 kemunculan kalimat dan 7.944 komentar terwakili. Rentang 27 Oktober 2025–26 Oktober 2026; Oktober 2025 dan Oktober 2026 parsial dikeluarkan dari arah sehingga tersedia 11 bulan kalender lengkap. Seluruh topik menerima catatan dukungan terbatas karena campuran platform pada dua jendela berubah; ini tidak sama dengan probabilitas model.

Contoh T38 beasiswa: 52/947 (5,5%) pada April–Juni → 30/1.850 (1,6%) pada Juli–September 2026, **−3,9 poin**, indikasi menurun dalam snapshot. T02 dokter/psikiater/psikolog: 19/947 (2,0%) → 95/1.850 (5,1%), **+3,1 poin**, indikasi meningkat. Angka ini tidak mengukur tren seluruh Reddit/YouTube, frekuensi aktivitas komentar aktual, penyebab, atau prediksi.

Skema sidecar baru **`beesense-topic-explanations:1`** menyimpan `topic_explanations.json`, `summary.json`, dan `manifest.json` dengan dua checksum. Hasil mengikat hash input, manifest run sumber, hash kode algoritma, opsi dan flag sintetis. `load_explanations(..., expected_source_manifest_sha256=...)` memverifikasi integritas dan identitas sumber. Publikasi atomik menolak direktori yang sudah ada, hasil milik run lain, dan output di dalam run sumber. Sembilan artifact lama tetap memakai `beesense-sentence-clusters:1`; producer asli run tersebut tetap `1.0.0`. Tidak ada migrasi database; sidecar berskema terpisah dan kompatibel mundur.

## Verifikasi dan batas deployment

Pengujian NLP/UI mencakup pola naik/turun/stabil, spike, bulan hilang/parsial, duplikasi kalimat, perubahan komposisi platform, dominasi thread, tanggal perkiraan, MMR/provenans, checksum sidecar, filter dan slider, serta guard tanpa training. Dataset, sebelas checksum artifact v2 aktif serta sembilan artifact v1 arsip diperiksa melalui scripts/verify_dashboard_data.py. Log/screenshot eksperimen lama telah dibersihkan; tes memakai fixture sintetis dan tidak memerlukan arsip tersebut.

```bash
.venv-nlp/bin/python -m unittest discover -s tests/nlp -v
.venv-nlp/bin/python -m ruff check --isolated --select E4,E7,E9,F,I social_nlp.py nlp_dashboard.py tests/nlp
.venv-nlp/bin/python -m ruff format --isolated --check social_nlp.py nlp_dashboard.py tests/nlp
.venv-nlp/bin/python -m scripts.verify_dashboard_data
```

Dockerfile.nlp tetap mencakup dua class dan JSON; tidak perlu dependency tambahan. Docker daemon belum aktif, sehingga image/runtime revisi ini **belum diverifikasi**. Perintah tertunda: `docker build -f Dockerfile.nlp -t beesense-nlp .`. Tidak ada deployment production.

## Referensi primer

- [Carbonell & Goldstein, MMR (1998)](https://www.cs.cmu.edu/afs/cs/Web/People/jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf): relevansi dan keragaman pada seleksi ekstraktif. Bobot relevansi dan prioritas sumber di BeeSense merupakan pilihan implementasi.
- [SciPy theilslopes](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.theilslopes.html): kemiringan median pasangan.
- [SciPy kendalltau](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kendalltau.html): ukuran asosiasi urutan. Tidak ada klaim signifikansi statistik untuk sampel crawl ini.
