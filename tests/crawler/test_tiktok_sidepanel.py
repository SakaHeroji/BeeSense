"""Real Chromium UI with local files and synthetic Chrome APIs; no social traffic."""

import unittest
from pathlib import Path


class SidePanelTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        from playwright.async_api import async_playwright

        self.playwright = await async_playwright().start()
        self.addAsyncCleanup(self.playwright.stop)
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.addAsyncCleanup(self.browser.close)
        self.page = await self.browser.new_page(viewport={"width": 380, "height": 860})
        root = Path(__file__).resolve().parents[2]
        self.extension = root / "Crawler/Backend/Tiktok/chrome_extension"
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        await self.page.add_init_script(
            path=Path(__file__).parent / "fixtures/tiktok_sidepanel_chrome.js"
        )
        await self.page.route("**/*", self.route)
        await self.page.goto("http://beesense.test/sidepanel.html")
        await self.page.wait_for_function(
            "document.querySelector('#tab').options.length === 2"
        )

    async def route(self, route):
        from urllib.parse import urlsplit

        url = urlsplit(route.request.url)
        allowed = {"sidepanel.html", "sidepanel.css", "sidepanel.mjs", "core.mjs"}
        name = url.path.removeprefix("/")
        if url.hostname == "beesense.test" and name in allowed:
            await route.fulfill(path=self.extension / name)
        else:
            await route.abort()

    async def connect(self):
        await self.page.locator("#origin").fill("http://127.0.0.1:8765/")
        await self.page.locator("#code").fill("a" * 43)
        await self.page.locator("#start").click()

    async def test_invalid_origin_and_code_focus_first_error_without_message(self):
        await self.page.locator("#origin").fill("https://external.test/")
        await self.page.locator("#code").fill("short")
        await self.page.locator("#start").click()
        self.assertEqual(
            await self.page.evaluate("document.activeElement.id"), "origin"
        )
        self.assertEqual(
            await self.page.locator("#origin").get_attribute("aria-invalid"), "true"
        )
        self.assertTrue(await self.page.locator("#code-error").is_visible())
        self.assertEqual(await self.page.evaluate("uiFixture.messages"), [])

    async def test_pairing_uses_active_selected_tab_and_clears_secret(self):
        self.assertEqual(await self.page.locator("#tab").input_value(), "7")
        await self.connect()
        await self.page.locator("#monitor").wait_for(state="visible")
        self.assertEqual(
            await self.page.evaluate("uiFixture.messages[0]"),
            dict(
                action="start", tabId=7, origin="http://127.0.0.1:8765/", code="a" * 43
            ),
        )
        self.assertEqual(await self.page.locator("#code").input_value(), "")
        self.assertEqual(
            await self.page.locator("#code").get_attribute("type"), "password"
        )
        self.assertFalse(await self.page.locator("#continue").is_visible())
        self.assertFalse(self.errors)

    async def test_human_validation_continue_and_stop_follow_storage_state(self):
        await self.page.evaluate(
            "uiFixture.update({running:true, phase:'human', message:'Selesaikan CAPTCHA', counts:{posts:10, comments:1348, replies:481}, updatedAt:Date.now()})"
        )
        await self.page.locator("#continue").wait_for(state="visible")
        self.assertEqual(await self.page.locator("#comments").inner_text(), "1.348")
        await self.page.locator("#continue").click()
        await self.page.locator("#continue").wait_for(state="hidden")
        await self.page.locator("#stop").click()
        await self.page.locator("#setup").wait_for(state="visible")
        self.assertEqual(
            await self.page.evaluate("uiFixture.messages.map(m=>m.action)"),
            ["continue", "stop"],
        )
        self.assertEqual(await self.page.locator("#posts").inner_text(), "10")

    async def test_reopening_panel_restores_progress_and_human_controls(self):
        await self.page.evaluate(
            "uiFixture.update({running:true, phase:'human', message:'Selesaikan CAPTCHA', counts:{posts:2, comments:12, replies:4}, tabTitle:'TikTok aktif'})"
        )
        await self.page.reload()
        await self.page.locator("#continue").wait_for(state="visible")
        self.assertEqual(await self.page.locator("#comments").inner_text(), "12")
        self.assertEqual(
            await self.page.locator("#selected-tab").inner_text(), "TikTok aktif"
        )
        self.assertEqual(await self.page.evaluate("uiFixture.messages"), [])

    async def test_empty_tab_state_opens_tiktok_then_can_select_it(self):
        await self.page.evaluate("uiFixture.setTabs([])")
        await self.page.locator("#refresh-tabs").click()
        await self.page.locator("#open-tiktok").wait_for(state="visible")
        await self.page.locator("#open-tiktok").click()
        await self.page.locator("#open-tiktok").wait_for(state="hidden")
        self.assertEqual(await self.page.locator("#tab").input_value(), "8")

    async def test_navigated_foreign_tab_is_rejected_before_start(self):
        await self.page.evaluate(
            "uiFixture.setTabs([{id:7,active:true,title:'Changed',url:'https://www.tiktok.com.evil.test/'}])"
        )
        await self.connect()
        self.assertEqual(await self.page.evaluate("uiFixture.messages"), [])
        self.assertIn(
            "pilih ulang tab TikTok", await self.page.locator("#status").inner_text()
        )
        self.assertTrue(await self.page.locator("#start").is_enabled())

    async def test_failed_command_keeps_actionable_error_and_allows_retry(self):
        await self.page.evaluate("uiFixture.fail = true")
        await self.connect()
        self.assertIn(
            "Periksa crawler lokal", await self.page.locator("#status").inner_text()
        )
        self.assertTrue(await self.page.locator("#start").is_enabled())
        await self.page.evaluate("uiFixture.fail = false")
        await self.page.locator("#start").click()
        await self.page.locator("#monitor").wait_for(state="visible")
        await self.page.evaluate("uiFixture.fail = true")
        await self.page.locator("#stop").click()
        self.assertIn(
            "Perintah belum diterima", await self.page.locator("#status").inner_text()
        )
        self.assertTrue(await self.page.locator("#stop").is_enabled())
        await self.page.evaluate("uiFixture.fail = false")
        await self.page.locator("#stop").click()
        await self.page.locator("#setup").wait_for(state="visible")

    async def test_narrow_and_zoomed_layout_preserves_keyboard_focus_and_no_overflow(
        self,
    ):
        for width, zoom in ((280, 1), (380, 1), (600, 2)):
            await self.page.set_viewport_size({"width": width, "height": 860})
            await self.page.evaluate("z=>document.documentElement.style.zoom=z", zoom)
            self.assertTrue(
                await self.page.evaluate(
                    "document.documentElement.scrollWidth <= document.documentElement.clientWidth"
                )
            )
        await self.page.evaluate("document.documentElement.style.zoom=1")
        await self.page.locator("#origin").focus()
        await self.page.keyboard.press("Tab")
        self.assertEqual(await self.page.evaluate("document.activeElement.id"), "code")
        self.assertEqual(
            await self.page.locator("#code").evaluate(
                "e=>getComputedStyle(e).outlineStyle"
            ),
            "solid",
        )
        self.assertFalse(self.errors)
