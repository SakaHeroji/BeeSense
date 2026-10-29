# PRD BeeSense

Kumpulan kebutuhan produk BeeSense, dipisahkan menurut tanggung jawab frontend, backend, dan machine learning. Dokumen pertama yang disusun adalah **frontend Crawler berbasis ReactJS**.

| Folder | Isi dan status |
| --- | --- |
| [PRD Frontend](<PRD Frontend/README.md>) | PRD Crawler, rancangan layar, dan acceptance criteria tersedia sebagai draf v1.1. |
| [PRD Backend](<PRD Backend/README.md>) | Tempat PRD backend berikutnya; saat ini berisi dependensi yang perlu dirinci. |
| [PRD Machine Learning](<PRD Machine Learning/README.md>) | Tempat PRD machine learning berikutnya; saat ini berisi batas integrasi data. |

Sistem direncanakan memiliki tiga frontend: **Crawler**, **NLP Machine Learning**, dan **Dashboard**. PRD frontend NLP Machine Learning dan Dashboard akan disusun terpisah. Pembagian frontend merupakan pembagian pengalaman pengguna; keputusan apakah ketiganya memakai satu aplikasi React atau deployment terpisah belum ditetapkan.

## Mulai membaca

1. [PRD Frontend Crawler](<PRD Frontend/PRD Frontend Crawler.md>): tujuan, ruang lingkup, kebutuhan, aturan data, dan integrasi ReactJS.
2. [Rancangan Layar Crawler](<PRD Frontend/Rancangan Layar Crawler.md>): navigasi, wireframe, interaksi, dan contoh pesan.
3. [Acceptance Criteria Crawler](<PRD Frontend/Acceptance Criteria Crawler.md>): skenario untuk menerima implementasi.

Status **draf spesifikasi**, tanggal 29 Oktober 2026. Dokumen membedakan kemampuan Python yang sudah ada dari antarmuka React, API, dan akuisisi survei yang masih direncanakan. Penyusunan PRD ini tidak menjalankan crawling, training, atau mengubah dashboard produksi.

Implementasi frontend berikutnya tersedia di [Crawler/Frontend](../Crawler/Frontend/README.md): ReactJS dengan mode simulasi dan adapter API. Backend untuk akuisisi web masih perlu dibangun; lihat catatan delivery pada folder implementasi untuk batas integrasinya.

Revisi frontend Crawler: tema putih–oranye, seluruh teks hitam minimum 13 px, serta tujuh pilihan platform sosial sesuai PRD.
