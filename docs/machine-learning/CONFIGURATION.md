# Satu konfigurasi NLP

Semua pengaturan `SocialNLPClusterer` berada di
[`config/social_nlp.json`](../../config/social_nlp.json). Lima salinan preset
Instagram/Twitter/relevansi bertanggal sudah dihapus. Launcher dashboard relevansi
juga membaca file utama ini. Tidak ada parameter fitting atau snapshot aktif yang
diubah oleh perapian konfigurasi.

## Bagian yang dikustom

| Bagian | Kegunaan |
| --- | --- |
| `input_file` | Workbook social crawler yang menjadi sumber kalimat. |
| `output_dir` | Direktori hasil NLP; untuk fitting baru wajib memakai direktori baru. Dashboard default membaca direktori ini. |
| `relevance_artifact` | Direktori keputusan relevansi yang cocok dengan checksum workbook; isi `null` untuk clustering tanpa mask. |
| `include_kinds`, `min_words`, `min_characters`, `max_segment_characters`, `max_unique_sentences` | Seleksi komentar/balasan, pemisahan kalimat dan batas korpus. |
| `model`, `seed`, `cache_dir` | Encoder SBERT, revision tetap, jendela token, batch/thread dan cache. |
| `umap`, `dbscan` | Proyeksi dan grid pencarian parameter kepadatan. |
| `target_topics`, `evaluation`, `coherence` | Jumlah topik akhir, evaluasi dan ambang publikasi. |
| `gemini` | Aktivasi narasi, model, batas request dan path auth lokal. |
| `graph`, `explanation` | Batas graf kemiripan serta opsi bukti/tren topik. |

Nilai awal tetap 20 topik, mean c_v minimum 0,4, Gemini aktif dan snapshot setelah
penyaringan. Tahap narasi Gemini tetap memerlukan 20 topik dan gate coherence;
ambang tidak diturunkan otomatis. API key tetap di auth lokal yang diabaikan Git.
`config/context_relevance.json` mengatur proses penyaringan yang terpisah;
`config/dashboard.json` memilih pasangan snapshot sebelum/sesudah untuk dibaca UI.

## Memeriksa dan menjalankan

```sh
python -m MachineLearning.social_nlp --dry-run
python -m MachineLearning.social_nlp --prepare-only
python -m MachineLearning.social_nlp --output-dir outputs/nlp_run_baru
```

`--dry-run` memvalidasi dan menampilkan konfigurasi efektif tanpa membaca workbook,
memuat model, fitting atau membaca kredensial. Flag `--input` dan `--output-dir`
tetap dapat menimpa path satu kali. Flag tersebut tidak menonaktifkan mask; ketika
mengganti korpus, pilih artifact relevansi yang sesuai atau set
`relevance_artifact: null` dalam file utama.

`--config <path>` tetap menerima file override parsial untuk kompatibilitas.
Penggunaan Python dengan dictionary parsial juga tetap tersedia:

```python
from MachineLearning.social_nlp import SocialNLPClusterer

pipeline = SocialNLPClusterer({
    "target_topics": 20,
    "model": {"batch_size": 16},
    "relevance_artifact": None,
})
```

Field nested yang tidak disebut tetap diwarisi; field asing ditolak. Konfigurasi
eksplisit parsial tanpa `relevance_artifact` memakai `null`, sehingga keputusan
untuk korpus aktif tidak diwariskan ke korpus lain. Pemanggilan tanpa argumen atau
dengan path file utama tetap mengikuti artifact relevansi di file utama.

## Riwayat dan reproduksi

Snapshot dan data hasil lama tetap dipertahankan. Setiap bundle model menyimpan
konfigurasi efektif pada `summary.json` bagian `config`; tidak perlu menyimpan
salinan JSON konfigurasi lengkap di `config/` untuk setiap eksperimen.

```python
from pathlib import Path
import json
from MachineLearning.social_nlp import SocialNLPClusterer

run = Path("outputs/nlp_20261102_twitter_topics20_gemini_01")
saved = json.loads((run / "summary.json").read_text())["config"]
pipeline = SocialNLPClusterer(saved)
# Jika memang ingin fitting ulang, simpan ke direktori baru.
```

Untuk melihat baseline lama cukup pilih **Sebelum penyaringan** pada dashboard,
atau jalankan `python -m scripts.relevance_dashboard --baseline`. Tidak perlu
menyalin preset lama ke file utama. Bundle yang diberi narasi tanpa fitting ulang
dapat mempertahankan `config.output_dir` dari run sumber; direktori bundle yang
sedang dibuka dan manifest-nya tetap menjadi identitas hasil.

**No migration required.** Skema artifact, hasil fitting, model, workbook dan
konfigurasi container dipertahankan.
