# PRD Backend

**Status: belum disusun.** Folder ini disiapkan untuk PRD backend BeeSense. Daftar berikut merupakan dependensi frontend Crawler, bukan spesifikasi backend lengkap atau layanan yang sudah tersedia.

| Area yang perlu dirinci | Kebutuhan dari frontend |
| --- | --- |
| API dan akses | Sesi pengguna, izin operator/pengamat, isolasi proyek, validasi, idempotensi, dan kontrak error. |
| Worker akuisisi | Menjalankan crawler Python di server, antrean, deadline persisten, penghentian aman, dan pemulihan status setelah worker gagal. |
| Adapter sosial | Kontrak UI mencakup YouTube, Reddit, Instagram, TikTok, Threads, Facebook, dan X/Twitter. Python saat ini baru memiliki dua adapter pertama. Lima adapter baru memerlukan capability gating, normalisasi native ID/provenance, discovery berdasarkan query, dan mode URL tanpa discovery tersembunyi. |
| Intervensi browser | Menghubungkan operator ke sesi browser worker yang benar untuk CAPTCHA; status verifikasi berasal dari worker. |
| HTTP 429 | Cooldown, Retry-After, batas retry, dan event per platform tanpa memperpanjang deadline. |
| Akuisisi survei | Form/import, template berversi, validasi per baris, identitas pseudonim, deduplikasi, dan transaksi commit. |
| Dataset | Versi immutable, manifest/checksum, indeks deduplikasi, pratinjau, izin unduh, serta penandaan hasil parsial. |
| Operasional | Event/progres, heartbeat, audit, sanitasi log, batas upload, penyimpanan sementara, dan kebijakan retensi. |

Kontrak antarmuka yang **diusulkan** tersedia di [PRD Frontend Crawler](<../PRD Frontend/PRD Frontend Crawler.md#12-kontrak-integrasi-yang-diusulkan>). OpenAPI, skema penyimpanan, strategi deployment, dan migrasi data harus ditetapkan saat menyusun PRD backend.

PRD frontend belum memilih framework API, database, message broker, atau penyedia identitas. Jangan menganggap endpoint contoh sudah diimplementasikan.

[Kembali ke indeks PRD](../README.md)
