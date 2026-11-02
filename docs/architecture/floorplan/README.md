# Peta cara kerja BeeSense

Folder ini menyimpan salinan peta yang ikut Git. Unduh [beesense-map.html](beesense-map.html), lalu buka di browser. Seluruh diagram, font, dan alur tersedia dalam satu berkas yang bisa dibuka tanpa server. GitHub menampilkan HTML sebagai berkas; unduh untuk memakai peta interaktifnya.

Menu **Flows** menyediakan enam alur:

1. Crawling sampai dashboard.
2. Semua platform dan status backendnya.
3. Dari Excel menjadi korpus kalimat.
4. Clustering sebelum penyaringan.
5. Penyaringan konteks dan clustering setelah penyaringan.
6. Dua snapshot ke dashboard.

YouTube, Reddit, Instagram, dan X mempunyai backend Python. TikTok, Threads, dan Facebook masih pilihan UI/simulasi. Dua jalur clustering memperlihatkan SBERT, UMAP, DBSCAN, Ward, evaluasi coherence, deskripsi Gemini, serta snapshot yang dipilih melalui radio dashboard.

[Catatan Obsidian](../../../graphify-out/obsidian/Alur%20Clustering%20Sebelum%20dan%20Setelah%20Penyaringan.md) memuat diagram dan rincian setiap tahap. [Laporan Graphify](../../../graphify-out/GRAPH_REPORT.md) memuat hubungan kode serta batas ekstraksinya.

## Sumber dan pembaruan

`architecture.json` menyimpan susunan modul, sambungan, enam flow, dan pengantar. `descriptions/` memberi nama dan penjelasan untuk seluruh 139 berkas. `recent-work.json` mencatat bagian peta yang terakhir diperjelas.

Folder kerja `floorplan/` tetap lokal dan diabaikan Git. Untuk membangun ulang setelah clone, gunakan skill Floorplan untuk memindai repository, salin tiga sumber di atas ke folder kerja tersebut, lalu jalankan build melalui skill yang terpasang. Setelah peta diperbarui, sinkronkan kembali sumbernya dan buat ekspor:

```bash
node floorplan/serve.mjs --export docs/architecture/floorplan/beesense-map.html --include flows,notes
```

Salinan HTML menghapus path root komputer, alamat Git remote, dan akses Ask ke agent lokal. Folder salinan ini dikecualikan dari pemindaian agar peta tidak memasukkan dirinya sendiri. Publikasi dokumentasi tidak menjalankan crawling, training, Gemini, reboot, atau deployment dashboard.
