# PRD Machine Learning

**Status: belum disusun.** Folder ini disiapkan untuk PRD pipeline machine learning. PRD frontend **NLP Machine Learning** nantinya tetap berada di folder PRD Frontend; folder ini membahas kebutuhan pemrosesan dan model.

Dependensi dari Crawler yang perlu disepakati:

- Input selalu menunjuk `dataset_id`, versi, checksum, dan versi skema yang tetap. Dataset parsial memerlukan penerimaan eksplisit.
- Bedakan sumber sosial dan survei, post/komentar/reply dan jawaban survei, serta peran responden yang dideklarasikan. Pengguna sosial tidak otomatis diklasifikasikan sebagai calon mahasiswa atau orang tua.
- Bawa provenance, konteks pertanyaan, status kelayakan, dan relasi parent. Tentukan pemisahan teks jawaban dari metadata pertanyaan agar prompt survei tidak dianggap sebagai pendapat responden.
- Dataset survei memerlukan kontrak baru; workbook sosial ringkas sepuluh kolom saat ini tidak cukup untuk seluruh metadata survei. Ketidakcocokan skema harus terlihat sebelum training.
- Validasi normalisasi skema sosial untuk Instagram, TikTok, Threads, Facebook, dan X/Twitter sebelum mengaktifkan handoff NLP. Tersedianya pilihan UI tidak membuktikan dukungan adapter NLP.
- Tetapkan aturan normalisasi, deduplikasi lanjutan, teks kosong, jawaban nonteks, dan pembandingan antar sumber. Penyatuan korpus harus menghasilkan versi dataset baru.
- Permintaan sebelumnya mengenai **20 topik** dan **coherence minimal 0,4** perlu dirinci sebagai kriteria model di PRD ini, termasuk definisi agregasi metriknya. Keduanya bukan kriteria keberhasilan akuisisi Crawler.
- Training menghasilkan snapshot baru. Akuisisi data tidak otomatis melatih model atau mengganti snapshot Dashboard.

Rujukan: [PRD Frontend Crawler](<../PRD Frontend/PRD Frontend Crawler.md>), [metodologi NLP saat ini](../../docs/machine-learning/SOCIAL_NLP.md), dan [catatan Obsidian](<../../graphify-out/obsidian/Metodologi Machine Learning Social NLP.md>).

[Kembali ke indeks PRD](../README.md)
