"""Offline browser fixtures for comment controls; never navigates to TikTok."""

import subprocess
import unittest
from pathlib import Path


class CommentDomTests(unittest.IsolatedAsyncioTestCase):
    async def test_comments_tab_is_selected_instead_of_you_may_like(self):
        await self.page.set_content("""
            <button role="tab" id="tab" aria-selected="false"
              onclick="this.setAttribute('aria-selected','true');pane.style.display='block';recs.style.display='none'">Comments (600)</button>
            <button role="tab" aria-selected="true">You may like</button>
            <div class="DivCommentListContainer">
              <div id="recs"><button onclick="window.wrong++">View 5 more</button></div>
              <div id="pane" data-e2e="comment-list" style="display:none">
                <p data-e2e="comment-level-1">Parent</p>
                <button onclick="window.reply++">View 5 more replies</button>
              </div>
            </div><script>window.wrong=window.reply=0</script>
        """)
        self.assertTrue((await self.operation("comments"))["tab_selected"])
        self.assertEqual(
            await self.page.locator("#tab").get_attribute("aria-selected"), "true"
        )
        self.assertTrue((await self.operation("expand"))["clicked"])
        self.assertEqual(
            await self.page.evaluate("[window.wrong,window.reply]"), [0, 1]
        )

    async def asyncSetUp(self):
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            self.skipTest("Playwright is not installed")
        self.playwright = await async_playwright().start()
        self.addAsyncCleanup(self.playwright.stop)
        try:
            self.browser = await self.playwright.chromium.launch(headless=True)
        except Exception as error:
            if "Executable doesn't exist" in str(error):
                self.skipTest("Offline Chromium fixture is not installed")
            raise
        self.addAsyncCleanup(self.browser.close)
        self.page = await self.browser.new_page()
        await self.page.route("**/*", lambda route: route.abort())
        root = Path(__file__).resolve().parents[2]
        self.source = subprocess.check_output(
            [
                "node",
                "--input-type=module",
                "-e",
                "import {pageOperation} from './Crawler/Backend/Tiktok/chrome_extension/core.mjs';"
                "process.stdout.write(pageOperation.toString())",
            ],
            cwd=root,
            text=True,
        )

    async def operation(self, action, **kwargs):
        return await self.page.evaluate(
            "(" + self.source + ")", {"action": action, "id": "100", **kwargs}
        )

    async def test_comment_toggle_does_not_close_an_already_open_panel(self):
        await self.page.set_content("""
            <button aria-label="Comments" onclick="window.clicks++;pane.style.display=pane.style.display==='none'?'block':'none'">Comments</button>
            <div id="pane" data-e2e="comment-list" style="height:100px;overflow:auto">Parent</div>
            <script>window.clicks=0</script>
        """)
        self.assertTrue((await self.operation("comments"))["already_open"])
        self.assertEqual(await self.page.evaluate("window.clicks"), 0)
        await self.page.evaluate("pane.style.display='none'")
        self.assertTrue((await self.operation("comments"))["clicked"])
        self.assertEqual(await self.page.evaluate("window.clicks"), 1)
        self.assertNotEqual(
            await self.page.locator("#pane").evaluate("e=>getComputedStyle(e).display"),
            "none",
        )

    async def test_identical_reply_labels_belong_to_different_parent_controls(self):
        await self.page.set_content("""<div data-e2e="comment-list">
            <div data-e2e="comment-level-1">Parent A<div>
                <button onclick="window.first++">View 2 replies</button>
            </div></div>
            <div data-e2e="comment-level-1">Parent B<div>
                <button onclick="window.second++">View 2 replies</button>
            </div></div>
            </div><script>window.first=window.second=0</script>""")
        first = await self.operation("expand")
        second = await self.operation("expand", blocked=[first["key"]])
        self.assertTrue(second["clicked"])
        self.assertNotEqual(first["key"], second["key"])
        self.assertEqual(
            await self.page.evaluate("[window.first,window.second]"), [1, 1]
        )

    async def test_expansion_prefers_actual_list_over_broad_layout_wrapper(self):
        await self.page.set_content("""<div class="DivCommentListItemWrapper">
                <button onclick="window.wrong++">View 2 replies</button>
            </div><div data-e2e="comment-list">
                <div data-e2e="comment-level-1">Parent</div>
                <button onclick="window.correct++">View 2 replies</button>
            </div><script>window.wrong=window.correct=0</script>""")
        self.assertTrue((await self.operation("expand"))["clicked"])
        self.assertEqual(
            await self.page.evaluate("[window.wrong,window.correct]"), [0, 1]
        )

    async def test_expansion_does_not_jump_back_to_offscreen_reply_controls(self):
        await self.page.set_content("""<div id="pane" data-e2e="comment-list"
            style="height:180px;overflow-y:auto">
            <div style="height:500px"><p data-e2e="comment-level-1">Parent A</p>
                <button onclick="window.first++">View 2 replies</button></div>
            <div style="height:500px"><p data-e2e="comment-level-1">Parent B</p>
                <button onclick="window.second++">View 2 replies</button></div>
            </div><script>window.first=window.second=0</script>""")
        await self.page.locator("#pane").evaluate("e=>e.scrollTop=500")
        self.assertTrue((await self.operation("expand"))["clicked"])
        self.assertEqual(
            await self.page.evaluate("[window.first,window.second]"), [0, 1]
        )
        self.assertGreaterEqual(
            await self.page.locator("#pane").evaluate("e=>e.scrollTop"), 480
        )

    async def test_thread_scroll_targets_comment_container_and_rewinds_it(self):
        await self.page.set_content("""<body style="height:4000px">
            <div id="pane" data-e2e="comment-list" style="height:160px;overflow-y:auto">
                <div style="height:2400px"><p data-e2e="comment-level-1">Parent</p></div>
            </div></body>""")
        result = await self.operation("scroll")
        self.assertTrue(result["scrolled"])
        self.assertGreater(
            await self.page.locator("#pane").evaluate("e=>e.scrollTop"), 0
        )
        self.assertEqual(await self.page.evaluate("window.scrollY"), 0)
        await self.operation("scroll", rewind=True)
        self.assertEqual(await self.page.locator("#pane").evaluate("e=>e.scrollTop"), 0)
        await self.page.locator("#pane").evaluate("e=>e.remove()")
        self.assertTrue((await self.operation("scroll"))["comment_pane_missing"])
        self.assertEqual(await self.page.evaluate("window.scrollY"), 0)

    async def test_reply_controls_expand_in_both_languages_without_repeating_blocked_control(
        self,
    ):
        await self.page.set_content("""<div data-e2e="comment-list">
            <p data-e2e="comment-level-1">Parent</p>
            <button onclick="window.first++">View 5 more replies</button>
            <button onclick="window.second++">Lihat 2 balasan</button>
            </div><script>window.first=window.second=0</script>""")
        first = await self.operation("expand")
        self.assertTrue(first["clicked"])
        second = await self.operation("expand", blocked=[first["key"]])
        self.assertTrue(second["clicked"])
        self.assertNotEqual(first["key"], second["key"])
        self.assertEqual(
            await self.page.evaluate("[window.first,window.second]"), [1, 1]
        )
