---
type: architecture
tags: [beesense, frontend, crawler, session, auth]
captured_at: 2026-11-06
---

# Panduan Session ID Frontend 20261106

[[Frontend Social Media Per Platform]] menampilkan panduan sesi lipat pada
bagian Akun & sesi. `SessionGuide` membaca metadata `sessionCookies` yang sama
dengan hint `AuthSettings`; tidak mengubah kontrak input atau membaca cookie.

- [[InstaloaderCrawler]]: cookie `sessionid` dari origin instagram.com.
- [[TwitterCrawler Scweet]]: cookie `auth_token` dari x.com dipasang melalui
  input frontend bernama Session ID; loader memetakan alias `sessionid`.
- [[Sidebar TikTok Connector 20261106]]: gunakan tab Chrome yang sudah login,
  pilih tab dan pairing lewat sidebar; tidak perlu menyalin cookie TikTok.
- Threads/Facebook: backend dan format sesi belum tersedia; petunjuk menandai
  status persiapan, tanpa mengklaim cookie tertentu telah didukung.
- YouTube/Reddit: konfigurasi ini tidak memerlukan Session ID.

Petunjuk Instagram/X: login akun sendiri → DevTools → Application → Storage →
Cookies → pilih origin → salin Value cookie yang tepat → tempel ke Session ID.
Tulisan Session pada Expires bukan nilai cookie. Disclosure native dapat dibuka
dengan Enter dan ditutup dengan Space; input sesi tetap disembunyikan.

50 tes frontend, 2 sinkronisasi, lint, format dan build API lulus. Browser
desktop/mobile diverifikasi tanpa permintaan ke domain luar atau kredensial
nyata; 390 px tanpa overflow, teks minimal 13 px, console 0 error/warning.
Runtime dev tetap simulasi, layanan penyimpanan auth.json belum terhubung.
Tidak ada migrasi atau deployment. Docker daemon tidak aktif.

[Panduan, batas backend dan audit UI](../../Crawler/Frontend/docs/SESSION_GUIDE.md).
