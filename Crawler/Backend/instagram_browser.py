"""Serial Chrome acquisition using a persistent profile and manual login.

The same named Playwright CLI session stays open for every operation. No mobile
API login, credential replay, CAPTCHA solver, or browser-profile copying occurs.
"""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI_VERSION = "0.1.22"
BROWSER_METHOD = "playwright_chrome_rendered_document"


def browser_configuration(value):
    if not isinstance(value, dict) or set(value) - {
        "profile_dir",
        "session",
        "headed",
        "max_scrolls",
        "scroll_delay_seconds",
    }:
        raise ValueError("Unknown browser setting; never store credentials in config")
    options = {
        "profile_dir": "output/instagram_browser/chrome_profile",
        "session": "beesense-instagram",
        "headed": True,
        "max_scrolls": 12,
        "scroll_delay_seconds": 2,
        **value,
    }
    if (
        not isinstance(options["profile_dir"], str)
        or not options["profile_dir"].strip()
    ):
        raise ValueError("profile_dir must be a local path")
    options["profile_dir"] = str((ROOT / options["profile_dir"]).resolve())
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,60}", options["session"]):
        raise ValueError("Invalid browser session name")
    if type(options["headed"]) is not bool:
        raise ValueError("headed must be boolean")
    if type(options["max_scrolls"]) is not int or not 0 <= options["max_scrolls"] <= 30:
        raise ValueError("max_scrolls must be 0..30")
    delay = options["scroll_delay_seconds"]
    if (
        type(delay) not in (int, float)
        or not math.isfinite(delay)
        or not 1 <= delay <= 15
    ):
        raise ValueError("scroll_delay_seconds must be 1..15")
    return options


def browser_script(operation, target, settings, options, seconds=90):
    source = Path(__file__).with_name("instagram_browser_capture.mjs").read_text()
    source = re.sub(r"\bexport\s+(?=(?:async\s+)?function\b)", "", source)
    parameters = {
        "operation": operation,
        "target": target,
        "limit": settings.search_results,
        "maxScrolls": options["max_scrolls"],
        "scrollDelay": options["scroll_delay_seconds"] * 1000,
        "budget": max(1, int(seconds * 1000) - 300),
    }
    return (
        "async page => {\n"
        + source
        + "\nlet operationRateLimit = null;\n"
        + "const onSourceResponse = response => {operationRateLimit = instagramSourceRateLimit(response) || operationRateLimit;};\n"
        + "page.on('response', onSourceResponse);\ntry {\nconst operate = async () => {\nconst p = "
        + json.dumps(parameters)
        + r""";
      const deadline = Date.now() + p.budget;
      const timeout = cap => Math.max(1, Math.min(cap, deadline - Date.now()));
      const barrier = async status => instagramBarrier(new URL(page.url()).pathname,
        await page.locator('input[type=password]').count(),
        await page.locator('iframe[src*="recaptcha"],iframe[src*="hcaptcha"]').count(), status);
      if (p.operation === 'check_session') {
        const loggedIn = await page.locator('a[href="/direct/inbox/"]').count() > 0;
        return {status: await barrier(null) || (loggedIn ? 'FINISHED_BEST_EFFORT' : 'SESSION_INVALID'),
          authenticated_navigation_visible: loggedIn};
      }
      if (p.operation === 'search') {
        const query = JSON.parse(p.target), offset = Number(query.cursor || 0);
        if (!/^[\w]{1,100}$/u.test(query.hashtag) || !Number.isSafeInteger(offset) || offset < 0 || offset > p.maxScrolls)
          throw new Error('invalid_search_target');
        const navigation = await instagramNavigate(page, 'https://www.instagram.com/explore/tags/' + encodeURIComponent(query.hashtag) + '/', timeout(25000));
        if(navigation.http_status === 429) return {status:'RATE_LIMITED', retry_after_seconds:navigation.retry_after_seconds};
        await page.locator('a[href*="/p/"],a[href*="/reel/"],input[type=password]').first().waitFor({timeout:timeout(12000)}).catch(()=>{});
        let status = await barrier(navigation.http_status);
        if (status) return {status};
        const found = new Set();
        const read = async () => {
          for (const href of await page.locator('a[href*="/p/"],a[href*="/reel/"]').evaluateAll(es=>es.map(e=>e.getAttribute('href')))) {
            const match = /^\/(?:[\w.]+\/)?(?:p|reel)\/([\w-]{1,40})\//.exec(href || '');
            if(match) found.add('https://www.instagram.com/p/' + match[1] + '/');
          }
        };
        await read();
        const scrolls = Math.min(offset + 2, p.maxScrolls);
        for(let n=0;n<scrolls;n++) {
          if(operationRateLimit) return operationRateLimit;
          if(Date.now() >= deadline) return {status:'TIMEOUT'};
          await page.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));
          await page.waitForTimeout(timeout(p.scrollDelay));
          await read();
        }
        status = await barrier(null);
        const all = [...found];
        return {status:status || 'FINISHED_BEST_EFFORT',
          candidates:all.slice(offset ? Math.min(offset * 10, all.length) : 0, (offset ? offset * 10 : 0) + p.limit),
          next_cursor:scrolls < p.maxScrolls && all.length ? String(scrolls) : null,
          discovered_from:'https://www.instagram.com/explore/tags/' + query.hashtag + '/'};
      }
      const code = new URL(p.target).pathname.split('/')[2];
      const navigation = await instagramNavigate(page, p.target, timeout(25000));
      if(navigation.http_status === 429) return {status:'RATE_LIMITED', retry_after_seconds:navigation.retry_after_seconds};
      await page.locator('time[datetime],input[type=password]').first().waitFor({timeout:timeout(15000)}).catch(()=>{});
      const status = await barrier(navigation.http_status);
      if(status) return {status};
      const actual = new URL(page.url()).pathname;
      if(!new RegExp('^/(?:[\\w.]+/)?(?:p|reel)/' + code + '/?$').test(actual)) return {status:'SOURCE_ERROR'};
      let media = null;
      const comments = new Map();
      // Caption and comments arrive in separate streamed hydration chunks.
      // Wait for that document stream instead of treating an early caption as
      // a completed page. Nothing is requested outside normal browser navigation.
      const hydrationDeadline = Math.min(Date.now() + 10000, deadline);
      do {
        if(operationRateLimit) return operationRateLimit;
        const payloads = [];
        for(const text of await page.locator('script[type="application/json"]').allTextContents()) {
          if(text.length > 10000000) continue;
          try { payloads.push(JSON.parse(text)); } catch {}
        }
        const ids = await page.locator('a[href*="/c/"]').evaluateAll((es,code)=>es.map(e=>{
          const match=/^\/(?:[\w.]+\/)?(?:p|reel)\/([\w-]+)\/c\/([1-9]\d*)\/?$/.exec(e.getAttribute('href') || '');
          return match && match[1]===code ? match[2] : null;
        }).filter(Boolean),code);
        const data = instagramDocumentPayload(payloads, code, ids);
        if(data.media) media = data.media;
        for(const row of data.comments) comments.set(row.pk,row);
        if(media && (media.comment_count === 0 || comments.size > 0)) break;
        if(Date.now() >= deadline) break;
        await page.waitForTimeout(timeout(500));
      } while(Date.now() < hydrationDeadline);
      return {status:media ? 'FINISHED_BEST_EFFORT' : 'SOURCE_ERROR',media,comments:[...comments.values()]};
    };
    const result = await operate();
    return operationRateLimit || result;
    }
    finally {page.off('response', onSourceResponse);}
    }"""
    )


class InstagramBrowserWorker:
    def __init__(self, options):
        self.options = browser_configuration(options)
        self.artifacts = ROOT / "output/playwright/instagram_crawler"
        self.artifacts.mkdir(parents=True, exist_ok=True)
        profile = Path(self.options["profile_dir"])
        profile.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(profile, 0o700)
        self._opened = False
        self._barrier = False
        self._script_path = self.artifacts / ("operation-" + uuid.uuid4().hex + ".js")

    def call(self, args, seconds):
        if not shutil.which("npx"):
            raise ModuleNotFoundError("playwright_cli_requires_node_and_npx")
        command = [
            "npx",
            "--yes",
            "--package",
            "@playwright/cli@" + CLI_VERSION,
            "playwright-cli",
            "-s=" + self.options["session"],
            "--json",
            *args,
        ]
        value = subprocess.run(
            command,
            cwd=ROOT / "output",
            text=True,
            capture_output=True,
            timeout=max(0.1, seconds),
        )
        if value.returncode:
            # Never expose CLI output: it can contain login redirects or input values.
            raise RuntimeError("playwright_cli_operation_failed")
        from Crawler.Backend.Reddit.crawl_reddit_playwright import decode_cli_output

        return decode_cli_output(value.stdout)

    def __call__(self, operation, target, settings, seconds, emit):
        from Crawler.Backend.instagram_crawler import normalize_item

        deadline = time.monotonic() + seconds
        try:
            # Reuse the already logged-in CLI browser; never open a second profile owner.
            if not self._opened:
                try:
                    self.call(
                        ["run-code", "async page => ({active:true})"], min(10, seconds)
                    )
                except RuntimeError:
                    args = [
                        "open",
                        "https://www.instagram.com/",
                        "--browser",
                        "chrome",
                        "--persistent",
                        "--profile",
                        self.options["profile_dir"],
                    ]
                    if self.options["headed"]:
                        args.append("--headed")
                    self.call(args, deadline - time.monotonic())
                self._opened = True
            path = self._script_path
            path.write_text(
                browser_script(
                    operation,
                    target,
                    settings,
                    self.options,
                    deadline - time.monotonic(),
                )
            )
            data = self.call(
                ["run-code", "--filename", str(path)], deadline - time.monotonic()
            )
            status = data.get("status", "SOURCE_ERROR")
            self._barrier = status in {
                "LOGIN_REQUIRED",
                "CHALLENGE_REQUIRED",
                "RATE_LIMITED",
                "ACCESS_BLOCKED",
            }
            if operation == "search":
                for url in data.get("candidates", []):
                    emit(
                        "candidate",
                        {"url": url, "discovered_from": data["discovered_from"]},
                    )
            elif operation == "media" and data.get("media"):
                media = data["media"]
                row = normalize_item(media, target)
                row["quality_flags"] = [
                    "rendered_document_text_completeness_unverified",
                    "instagram_comments_best_effort",
                ]
                emit("record", row)
                seen, replies, per_thread = set(), 0, {}
                for item in data.get("comments", []):
                    if item["pk"] in seen:
                        continue
                    parent = item.get("replied_to_comment_id")
                    if parent:
                        if (
                            replies >= settings.max_replies
                            or per_thread.get(parent, 0)
                            >= settings.max_replies_per_thread
                        ):
                            continue
                        replies += 1
                        per_thread[parent] = per_thread.get(parent, 0) + 1
                    elif len(seen) - replies >= settings.max_comments:
                        continue
                    seen.add(item["pk"])
                    row = normalize_item(item, target, media=media, parent=parent)
                    row["quality_flags"] = [
                        "rendered_document_text_completeness_unverified",
                        "instagram_comments_best_effort",
                    ]
                    emit("record", row)
            return {
                "status": status,
                "source_version": CLI_VERSION,
                "next_cursor": data.get("next_cursor"),
                "retry_after_seconds": data.get("retry_after_seconds"),
                "warnings": ["initial_rendered_comments_only"],
            }
        except subprocess.TimeoutExpired:
            self._barrier = True
            return {
                "status": "TIMEOUT",
                "source_version": CLI_VERSION,
                "reason": "browser_operation_deadline",
            }
        except RuntimeError:
            # A failed CLI operation is not proof of logout/429. Preserve Chrome
            # for inspection when the coordinator stops on repeated errors.
            self._barrier = True
            return {
                "status": "SOURCE_ERROR",
                "source_version": CLI_VERSION,
                "reason": "browser_cli_operation_failed",
                "warnings": ["browser_preserved_for_inspection"],
            }

    def close(self):
        # Leave the browser visible for a manual challenge; never solve it automatically.
        if self._opened and not self._barrier:
            try:
                self.call(["close"], 5)
            except (RuntimeError, subprocess.TimeoutExpired):
                pass
