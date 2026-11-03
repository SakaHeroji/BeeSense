# PyTok source provenance — historical trial

Dependency: https://github.com/MEOMcGill/pytok
Pinned revision: `e6ad007bc66919e03c63334c75b985ed3e1daadd`, package version 0.3.0.
Browser integration: `camoufox==0.5.9`.

Install via requirements/tiktok.txt. The PyPI package with the same name is a
different project; never substitute `pip install pytok` for the pinned Git URL.
The source repository declares PolyForm Noncommercial 1.0.0 AND MIT; see its
[LICENSE](https://github.com/MEOMcGill/pytok/blob/e6ad007bc66919e03c63334c75b985ed3e1daadd/LICENSE).
Its noncommercial license is a material deployment constraint; this task performs
local development and testing, with no publication or production deployment.

BeeSense uses one browser instance with the supplied local msToken. AccountsPool,
automatic login, account rotation and automatic CAPTCHA solving are not used.
The wrapper replaces the CAPTCHA entry point with a terminal CAPTCHA_REQUIRED
receipt, bounds requests/deadlines and keeps only normalized text/IDs/statistics.
The isolated browser cache avoids Camoufox 0.5 deleting a cache from another
project. The retired Omkar sources are removed from the active implementation;
its unsuccessful trial audit remains as history.

The user subsequently restored davidteather/TikTok-Api. This dependency is no longer active; see TIKTOK_API.md.
