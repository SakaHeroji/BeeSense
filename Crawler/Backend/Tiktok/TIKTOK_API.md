# Historical direct TikTok-Api backend

Historical backend: https://github.com/davidteather/TikTok-Api
Pinned package: `TikTokApi==7.3.3`, `playwright==1.64.1`, `openpyxl==3.1.5`.
Upstream license: MIT. Install from requirements/tiktok.txt.

`api.search.search_type(query, "item")` has an item parser in the pinned source,
but the supported public search API is users-only. Keyword video discovery in
BeeSense is therefore explicitly experimental. Hashtag discovery uses the
supported hashtag.videos iterator; optional seeds are configured in the same JSON.
No automatic CAPTCHA solver, account rotation or proxy is used.

The user restored this direct backend after the unsuccessful Omkar and
MEOMcGill/PyTok trials. Those trial audits are retained; their dependencies and
vendor sources are not active. No authentication values are stored in this file.

This direct backend was first superseded by dfreelon/Pyktok, then by the current
BeeSense native Playwright backend. TikTokApi is no longer imported, including
transitively. All corresponding failed trial reports remain historical evidence.
