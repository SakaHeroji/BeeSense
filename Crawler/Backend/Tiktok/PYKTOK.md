# Historical TikTok dependency: dfreelon/Pyktok

Upstream: https://github.com/dfreelon/pyktok
Pinned PyPI package: `pyktok==0.0.31`, BSD-3-Clause license.
Installed `pyktok/pyktok.py` SHA-256:
`882197d90fb1494198edc13937e2179fb6fa06309ed22fe20131ffa19737465f`.
No vendored or modified upstream source. This is not MEOMcGill/PyTok.

Pyktok uses TikTokApi for `get_video_urls()` and `get_comments()`; BeeSense pins
that transitive backend to `TikTokApi==7.3.3` and `playwright==1.64.1`. Its local
adapter supplies one owned, guarded browser context to those Pyktok functions.
Page metadata is parsed by Pyktok `alt_get_tiktok_json()` and `get_tiktok_json()`
with one HTTP response and the configured TikTok cookie. Browser-profile cookie
extraction is not invoked. Auth values are never stored in this provenance note.

Pyktok has no keyword-search API. BeeSense's experimental bridge passes the exact
configured query's TikTok search URL to the page parsers and reads embedded video
objects only. It does not paginate keyword search or silently substitute hashtags.
Hashtag discovery remains optional and explicitly configured. No hidden fallback
to the former TikTok-Api keyword endpoint, CAPTCHA solver, proxy or account pool.

The live 500-post / maximum-30-minute trial on 2026-11-03 failed after 2.69 seconds
with 0/500 posts: HTTP200 JSON contained no embedded video results.
See `docs/crawler/TIKTOK_PYKTOK_TRIAL_20261103.md`.

Superseded by the BeeSense native Playwright backend. Pyktok and TikTokApi are no
longer active TikTok requirements. The failed trial remains historical evidence.
