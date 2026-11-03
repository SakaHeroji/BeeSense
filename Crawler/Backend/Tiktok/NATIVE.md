# Active backend: BeeSense native TikTok browser crawler

TikTokCrawler 2.5.0 / NativeTikTokClient / BeeSenseNative 1.2.0.
Dependencies: Playwright 1.64.1 (Apache-2.0), OpenPyXL 3.1.5 (MIT).
Written in BeeSense; no third-party TikTok SDK is imported. No Chinel0 repository
code was imported after the user cancelled that integration.

The ordinary browser reads hydration, rendered video links and JSON responses
made by the search/comment UI. Only observed native video/comment IDs enter the
shared Dataset/Excel exporter. Scroll and reply controls trigger ordinary loading;
no forged/signed API requests, fingerprint patches, proxy/account rotation or
CAPTCHA solver. Invalid source metadata stays unknown rather than synthesized.

One context receives the local TikTok cookie before navigation. Request pacing
honors shared delay, and server 5xx increases it. HTTP429 persists Retry-After in
an ignored operational cache; subsequent processes stop until that time. Access
barriers terminate acquisition and preserve partial output. Auth is not changed,
profile cookies are not read, and debug bodies/credential values are not exported.

Primary Playwright references consulted:
- https://playwright.dev/python/docs/network
- https://playwright.dev/python/docs/api/class-browsercontext#browser-context-add-cookies
- https://playwright.dev/python/docs/api/class-page#page-goto

Live tests on 2026-11-03: headless 0/500 after 4.79 seconds, headed 0/500 after
11.05 seconds; PARTIAL / ACCESS_BLOCKED. The headed search response was empty or
invalid JSON despite HTTP200. Fixture browser acquisition passed separately.
See docs/crawler/TIKTOK_NATIVE_TRIAL_20261103.md. No promise of unblocked access.


Optional manual preflight2.1 supports an owned visible persistent Chromium profile,
private control-file human confirmation, cancellation and global time budget.
The user cancelled that browser trial and requested their already-open Chrome.
It is not the transport used by the successful small Chrome observation.

ChromeCaptureWorker1.0 imports public records previously observed by the connected
browser agent in the user's existing Chrome tab. It never connects to Chrome,
launches a browser, reads auth/cookies or sends network requests. Same shared
Dataset/Excel/native-ID archive; explicit source beesense_existing_chrome_capture.
Captured1post+10comments,0replies on3November2026; target500 not reached, comments
completeness unverified. Not an unattended Python-to-Chrome integration.
Captures remain in ignored .cache; no credential/profile material is indexed.
See docs/crawler/TIKTOK_CHROME_TRIAL_20261103.md. No migration required.

ChromeLiveWorker1.1 adds a loopback task/result bridge and optional local Chrome
extension. Agent-driven live trial exported2posts,30comments,13replies (45unique)
in638.85seconds before interruption;500target not reached. Source for that trial
was BeeSenseChromeLive1.0.0. New extension1.0.0 captures UI-generated public JSON
through Chrome.debugger and automates the selected TikTok tab. At initial
implementation it was not installed/live-tested; current user-reported
installation and pairing requirements are described in Update2.4.1 below.
Pairing precedes global crawl timer. Public native IDs remain strings; stale
responses, wrong roots and unobserved parents are rejected. See
docs/crawler/TIKTOK_CHROME_LIVE.md for exact permission scope and test evidence.

Update2.4.1: user reports extension installed. Browser policy prevents agent
inspection of chrome://extension/popup pages; pair manually in the selected TikTok
popup. CLI now distinguishes the actual extension transport/version and emits
connection-ready and waiting heartbeats without starting the crawl clock early.
Pairing timeout is explicit and leaves the crawler unstarted.36crawler+10bridge
Python tests pass. Prior45-record trial remains historical, not a new run result.

## Status akhir 3 November 2026 — crawler dihentikan

Uji ekstensi terpasang dengan TikTokCrawler 2.4.1 / BeeSenseChromeLive 1.1.0
menyimpan **13 post, 93 komentar, 261 balasan (367 record unik)** dalam 656,6 detik.
Run `social_20261103T094828Z_23fb8a79` berstatus INTERRUPTED; target 500 belum
tercapai (kurang 487). Dua belas kandidat di luar tanggal dan dua kandidat tanpa
include keyword disaring. `comments_complete: false`; angka komentar pada TikTok
bukan jumlah yang sudah diperoleh. Excel: `outputs/crawling/tiktok/2026-11-03/social_data.xlsx`.
Arsip gabungan setelah run: **35.197 ID unik, 0 duplikat native ID**.

TikTokCrawler **2.5.0**, BeeSenseNative **1.2.0**, dan Connector **1.1.0** memperbaiki
penghentian tiga putaran idle pada komentar tanpa cap. Komentar menunggu akhir
pagination `has_more: false` dari sumber dan balasan tiap parent sampai habis;
metadata yang tidak tersedia tetap belum membuktikan lengkap. Kontrol balasan yang
lambat dicoba kembali dengan jeda, bukan dilewati permanen. Deadline global,
Stop, CAPTCHA/login dan pembatasan sumber tetap berlaku; hasil parsial disimpan.
Tanpa deadline, proses dapat terus menunggu sumber sampai operator menghentikannya.
Batas idle pencarian serta cap eksplisit tetap berlaku. Deduplikasi memakai ID asli.

Status terhubung kini ditampilkan setelah GET tugas lolos autentikasi. Kesalahan
pairing tidak ditimpa status pelepasan debugger normal. Izin dan ID ekstensi sama.
**Reload ekstensi lokal sebelum penggunaan berikutnya.** Perbaikan terbaru diuji
offline; tidak dilakukan uji live baru karena pengguna meminta proses berhenti.
Tidak ada migrasi database, perubahan auth.json, atau redeploy Streamlit.
Seluruh perubahan diterbitkan melalui branch terpisah dari main agar branch
Streamlit yang tercatat di README tidak diperbarui.
