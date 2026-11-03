"""Install the browser required by the native TikTok backend."""

import subprocess
import sys


def install_browser(browser="chromium"):
    if browser not in {"chromium", "firefox", "webkit"}:
        raise ValueError("Unsupported Playwright browser")
    subprocess.run([sys.executable, "-m", "playwright", "install", browser], check=True)
