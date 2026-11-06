---
type: "query"
date: "2026-11-06T05:40:31.529147+00:00"
question: "Di frontend crawler yang menggunakan session id, tambahkan informasi cara mengambil sesi untuk masing-masing sosmed dengan Graphify, Obsidian, frontend-design dan web-design-guidelines."
contributor: "graphify"
outcome: "useful"
source_nodes: ["AuthSettings()", "SessionGuide()", "sessionCookies", "TikTokChromePreparation()"]
---

# Q: Di frontend crawler yang menggunakan session id, tambahkan informasi cara mengambil sesi untuk masing-masing sosmed dengan Graphify, Obsidian, frontend-design dan web-design-guidelines.

## Answer

Implemented frontend session instructions on 6 November 2026. Native SessionGuide details/summary appears in AuthSettings before account inputs and in TikTokChromePreparation. sessionCookies metadata in shared/auth.ts supplies both guide and input hint: Instagram sessionid at https://www.instagram.com; X auth_token at https://x.com is pasted into the sessionid field accepted by backend auth_material alias. Steps explain own-account login, macOS/Windows DevTools shortcuts, Application > Storage > Cookies > origin, Name, copying only the full Value, and matching username. Session on Expires is not the cookie value. External documentation links open a new tab. TikTok uses existing Chrome login plus sidebar pairing with no Session ID input. Threads/Facebook explicitly have no implemented crawler/session format; no claim of usable cookies. YouTube/Reddit show no session guide. No cookie inspection, new API, payload, permissions, storage semantics, auth.json or DB change. Development frontend remains labeled demo; auth gateway is pending.
Tests: npm run check passed lint,50Vitest,2sync,TypeScript and API build; npm run format:check passed. Real local Chromium tested at1440desktop/390mobile with all external requests blocked and blank credentials, Enter/Space disclosure and visible focus, scrollWidth390=viewport390,min guide font13px,console0errors/0warnings. Screenshots output/playwright/session-guides/. Vite running on127.0.0.1:5173 for review. Docker daemon inactive, image unbuilt; remaining docker build -t beesense-crawler-frontend:api Crawler/Frontend. No migration required.
Graphify now2599nodes/5229edges/202communities,289files/~305481words; merged graph has no missing/dangling/self-loop/collapsed edges. HTML,report,JSON and generated Obsidian graph exported; manual Panduan Session ID Frontend 20261106 note and HOME linked. Token usage unknown. Main documentation Crawler/Frontend/docs/SESSION_GUIDE.md. Existing X/IG/TikTok changes and live trial history preserved.

## Outcome

- Signal: useful

## Source Nodes

- AuthSettings()
- SessionGuide()
- sessionCookies
- TikTokChromePreparation()