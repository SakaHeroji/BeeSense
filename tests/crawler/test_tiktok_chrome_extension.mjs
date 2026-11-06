import test from "node:test";
import assert from "node:assert/strict";
import {
  parsePublicJson,
  sourceVideo,
  sourceVideos,
  sourceComments,
  sourceHasMore,
  commentPaginationExhausted,
  tiktokUrl,
  validateTask,
  retryAfter,
  NetworkPacing,
} from "../../Crawler/Backend/Tiktok/chrome_extension/core.mjs";

const root = "7685001417442086152",
  cid = "7693470766678967061";
const url = `https://www.tiktok.com/@example/video/${root}`;
const oid = "a".repeat(32);

test("pagination requires explicit source end and every parent's replies", () => {
  for (const value of [false, 0, "0"])
    assert.equal(sourceHasMore({ comments: [], has_more: value }), false);
  assert.equal(sourceHasMore({ data: { comments: [], has_more: "1" } }), true);
  assert.equal(sourceHasMore({ comments: [] }), null);
  assert.equal(sourceHasMore({ has_more: 0 }), null);
  const pages = new Map(),
    comments = new Map([[cid, { id: cid, kind: "comment", reply_count: 2 }]]);
  assert.equal(commentPaginationExhausted(pages, comments), false);
  pages.set(null, false);
  assert.equal(commentPaginationExhausted(pages, comments), false);
  comments.set("300", { id: "300", kind: "reply", parent_comment_id: cid });
  assert.equal(commentPaginationExhausted(pages, comments), false);
  comments.set("301", { id: "301", kind: "reply", parent_comment_id: cid });
  assert.equal(commentPaginationExhausted(pages, comments), true);
  comments.get(cid).reply_count = null;
  assert.equal(commentPaginationExhausted(pages, comments), false);
  pages.set(cid, false);
  assert.equal(commentPaginationExhausted(pages, comments), true);
  pages.set(null, true);
  assert.equal(commentPaginationExhausted(pages, comments), false);
  assert.equal(
    commentPaginationExhausted(new Map([[null, false]]), new Map(), true, 73),
    false,
  );
});

test("native integers survive JSON parsing without rounding or changing quoted text", () => {
  const body = parsePublicJson(
    '{"id":7685001417442086152,"text":"id 7685001417442086152 \\"ok\\"","count":12,"ratio":1.5,"exponent":1e3}',
  );
  assert.equal(body.id, root);
  assert.equal(body.text, 'id 7685001417442086152 "ok"');
  assert.equal(body.count, 12);
  assert.equal(body.exponent, 1000);
  assert.equal(body.ratio, 1.5);
});
test("source metadata rejects already rounded IDs and keeps only actual metrics", () => {
  assert.throws(
    () => sourceVideo({ id: Number(root), author: "example" }),
    /UNSAFE_NATIVE_ID/,
  );
  const video = sourceVideo({
    id: root,
    author: { uniqueId: "example" },
    desc: "kampus",
    createTime: "1789303835",
    stats: { diggCount: "545" },
  });
  assert.equal(video.id, root);
  assert.equal(video.stats.like_count, "545");
  assert.equal(video.stats.comment_count, null);
  assert.equal(video.created_at, "2026-09-13T12:50:35.000Z");
});
test("recursive videos require real metadata and deduplicate native identities", () => {
  const item = {
    id: root,
    desc: "kampus",
    author: { uniqueId: "example" },
    createTime: 1789303835,
  };
  assert.equal(
    sourceVideos({ rows: [item, item, { id: "12", desc: "missing author" }] })
      .length,
    1,
  );
});
test("comments preserve native reply parents and discard foreign post data", () => {
  const rows = sourceComments(
    parsePublicJson(
      `{"comments":[{"cid":${cid},"aweme_id":${root},"text":"parent","reply_comment":[{"cid":7693470735511290644,"text":"reply"}]},{"cid":"123","aweme_id":"999","text":"foreign"}]}`,
    ),
    root,
    url,
  );
  assert.equal(rows.length, 2);
  assert.equal(rows[0].kind, "comment");
  assert.equal(rows[1].parent_comment_id, cid);
  assert.equal(rows[1].id, "7693470735511290644");
  assert.equal(rows[1].kind, "reply");
});
test("selected browser destination is restricted to canonical TikTok HTTPS", () => {
  for (const value of [
    "http://www.tiktok.com/",
    "https://www.tiktok.com.evil.test/",
    "https://user:secret@www.tiktok.com/",
    "https://www.tiktok.com:444/",
  ])
    assert.throws(() => tiktokUrl(value));
  assert.equal(tiktokUrl(url).href, url);
});
test("task identity and query validation cannot navigate to another destination", () => {
  assert.equal(
    validateTask({
      operation_id: oid,
      operation: "thread",
      video_id: root,
      url,
    }),
    url,
  );
  assert.throws(
    () =>
      validateTask({
        operation_id: oid,
        operation: "thread",
        video_id: "999",
        url,
      }),
    /TASK_ID_MISMATCH/,
  );
  assert.throws(() =>
    validateTask({ operation_id: oid, operation: "execute", url }),
  );
  assert.equal(
    validateTask({
      operation_id: oid,
      operation: "search",
      target: JSON.stringify({ query: "biaya kuliah beasiswa" }),
    }),
    "https://www.tiktok.com/search?q=biaya+kuliah+beasiswa",
  );
  assert.throws(() =>
    validateTask({
      operation_id: oid,
      operation: "search",
      target: '{"hashtag":"../settings"}',
    }),
  );
});
test("Retry-After honors server wait including HTTP dates", () => {
  assert.equal(retryAfter("120"), 120);
  assert.equal(
    retryAfter(
      "Wed, 21 Oct 2026 07:28:00 GMT",
      Date.parse("2026-10-21T07:27:30Z"),
    ),
    30,
  );
  assert.equal(retryAfter(undefined), 60);
});

test("5xx backoff is capped, pauses after three failures, and resets on success", () => {
  const pacing = new NetworkPacing();
  pacing.observe(503, null, 1000);
  assert.equal(pacing.wait(3000, 1000), 5000);
  pacing.observe(502, null, 1000);
  assert.equal(pacing.wait(3000, 1000), 10000);
  for (let i = 0; i < 30; i++) pacing.observe(500, null, 1000);
  assert.equal(pacing.backoff, 15000);
  assert.equal(pacing.wait(3000, 1000), 30000);
  pacing.observe(503, 120, 2000);
  assert.equal(pacing.wait(3000, 2000), 120000);
  pacing.observe(200, null, 3000);
  assert.equal(pacing.wait(3000, 3000), 3000);
  assert.equal(pacing.failures, 0);
});

test("duplicate comment responses cannot keep a stagnant post alive", async () => {
  const prior = {
    chrome: globalThis.chrome,
    fetch: globalThis.fetch,
    timeout: globalThis.setTimeout,
    now: Date.now,
  };
  let listener,
    network,
    detached = false,
    taskSent = false,
    scrolls = 0;
  let now = prior.now();
  const batches = [];
  Date.now = () => now;
  globalThis.setTimeout = (fn, ms, ...args) =>
    prior.timeout(
      () => {
        now += ms;
        fn(...args);
      },
      ms >= 100 ? 1 : ms,
    );
  const respond = () => {
    network({ tabId: 1 }, "Network.requestWillBeSent", {
      requestId: "duplicate",
      request: {
        url: `https://www.tiktok.com/api/comment/list/?aweme_id=${root}`,
      },
    });
    // A stale response for another post must not block the current post.
    network({ tabId: 1 }, "Network.requestWillBeSent", {
      requestId: "foreign",
      request: { url: "https://www.tiktok.com/api/comment/list/?aweme_id=999" },
    });
    network({ tabId: 1 }, "Network.responseReceived", {
      requestId: "foreign",
      response: { status: 403 },
    });
    network({ tabId: 1 }, "Network.loadingFinished", {
      requestId: "duplicate",
    });
  };
  globalThis.chrome = {
    runtime: {
      id: "stagnation",
      getManifest: () => ({ version: "1.3.0" }),
      onMessage: { addListener: (f) => (listener = f) },
    },
    storage: { session: { set: async () => {} } },
    tabs: { get: async () => ({ url }), update: async () => respond() },
    debugger: {
      attach: async () => {},
      detach: async () => {
        detached = true;
      },
      onEvent: { addListener: (f) => (network = f) },
      onDetach: { addListener: () => {} },
      sendCommand: async (_, method, params) => {
        if (method === "Network.getResponseBody")
          return {
            body: JSON.stringify({
              has_more: 1,
              comments: [{ cid, aweme_id: root, text: "same ID" }],
            }),
          };
        if (method !== "Runtime.evaluate") return {};
        const args = JSON.parse(
          params.expression.slice(params.expression.lastIndexOf(")(") + 2, -1),
        );
        assert.notEqual(args.action, "expand", "main comments take priority");
        if (args.action === "scroll") {
          scrolls++;
          respond();
        }
        return {
          result: { value: { ready: true, url, candidates: [], at_end: true } },
        };
      },
    },
  };
  globalThis.fetch = async (value, options) => {
    if (new URL(value).pathname === "/api/task") {
      if (taskSent) throw new Error("Test complete");
      taskSent = true;
      return {
        ok: true,
        json: async () => ({
          operation_id: oid,
          operation: "thread",
          video_id: root,
          url,
          max_comments: null,
          collect_all_comments: true,
          comment_stagnation_seconds: 75,
          expires_at_unix: now / 1000 + 600,
          cached_root: {
            id: root,
            link: url,
            created_at: "2026-09-13T12:50:35Z",
          },
        }),
      };
    }
    batches.push(JSON.parse(options.body));
    return { ok: true, json: async () => ({ accepted: true }) };
  };
  try {
    await import("../../Crawler/Backend/Tiktok/chrome_extension/background.mjs?stagnation");
    listener(
      {
        action: "start",
        origin: "http://127.0.0.1:54321/",
        code: "a".repeat(43),
        tabId: 1,
      },
      { id: "stagnation" },
      () => {},
    );
    const deadline = prior.now() + 3000;
    while (!detached && prior.now() < deadline)
      await new Promise((resolve) => prior.timeout(resolve, 10));
    assert.ok(detached);
    assert.ok(scrolls > 3);
    assert.equal(batches.at(-1).status, "PARTIAL");
    assert.equal(batches.at(-1).collection_status, "stagnated");
    assert.ok(batches.at(-1).warnings.includes("comment_stagnation_timeout"));
    assert.equal(batches.flatMap((b) => b.events).length, 2);
  } finally {
    listener?.({ action: "stop" }, { id: "stagnation" }, () => {});
    globalThis.chrome = prior.chrome;
    globalThis.fetch = prior.fetch;
    globalThis.setTimeout = prior.timeout;
    Date.now = prior.now;
  }
});

test("uncapped controller scrolls past unresponsive reply controls until delayed replies end", async () => {
  const priorChrome = globalThis.chrome,
    priorFetch = globalThis.fetch,
    priorTimeout = globalThis.setTimeout;
  let listener,
    network,
    detachListener,
    detached = false,
    taskSent = false,
    rounds = 0;
  const bodies = new Map(),
    batches = [],
    statuses = [],
    scrollRewinds = [];
  globalThis.setTimeout = (fn, ms, ...args) =>
    priorTimeout(fn, ms >= 1000 ? 5 : ms, ...args);
  const respond = (name, endpoint, body) => {
    bodies.set(name, body);
    network({ tabId: 1 }, "Network.requestWillBeSent", {
      requestId: name,
      request: { url: endpoint },
    });
    network({ tabId: 1 }, "Network.loadingFinished", { requestId: name });
  };
  globalThis.chrome = {
    runtime: {
      id: "thread-test",
      getManifest: () => ({ version: "1.2.1" }),
      onMessage: { addListener: (f) => (listener = f) },
    },
    storage: { session: { set: async (value) => statuses.push(value.status) } },
    tabs: {
      get: async () => ({ url }),
      update: async () =>
        respond(
          "parents",
          `https://www.tiktok.com/api/comment/list/?aweme_id=${root}`,
          {
            has_more: 0,
            comments: [
              { cid, aweme_id: root, text: "parent", reply_comment_total: 1 },
            ],
          },
        ),
    },
    debugger: {
      attach: async () => {},
      detach: async () => {
        detached = true;
        detachListener({ tabId: 1 });
      },
      onEvent: { addListener: (f) => (network = f) },
      onDetach: { addListener: (f) => (detachListener = f) },
      sendCommand: async (_, method, params) => {
        if (method === "Network.getResponseBody")
          return { body: JSON.stringify(bodies.get(params.requestId)) };
        if (method === "Runtime.evaluate") {
          if (params.expression.includes('"action":"expand"')) {
            const controls = Array.from(
              { length: 12 },
              (_, i) => `stalled-${i}`,
            );
            const args = JSON.parse(
              params.expression.slice(
                params.expression.lastIndexOf(")(") + 2,
                -1,
              ),
            );
            const key = controls.find((value) => !args.blocked.includes(value));
            return { result: { value: { clicked: !!key, key } } };
          }
          if (params.expression.includes('"action":"scroll"')) {
            const args = JSON.parse(
              params.expression.slice(
                params.expression.lastIndexOf(")(") + 2,
                -1,
              ),
            );
            scrollRewinds.push(args.rewind);
            rounds++;
            if (rounds === 6)
              respond(
                "reply",
                `https://www.tiktok.com/api/comment/list/reply/?item_id=${root}&comment_id=${cid}`,
                {
                  has_more: false,
                  comments: [
                    { cid: "300", aweme_id: root, text: "late reply" },
                  ],
                },
              );
          }
          return {
            result: {
              value: { ready: true, url, candidates: [], clicked: false },
            },
          };
        }
        return {};
      },
    },
  };
  globalThis.fetch = async (value, options) => {
    if (new URL(value).pathname === "/api/task") {
      if (taskSent) throw new Error("Test bridge completed");
      taskSent = true;
      return {
        ok: true,
        json: async () => ({
          operation_id: oid,
          operation: "thread",
          video_id: root,
          url,
          max_comments: null,
          max_replies: null,
          max_replies_per_thread: null,
          idle_scroll_limit: 3,
          expires_at_unix: Date.now() / 1000 + 3,
          cached_root: {
            id: root,
            link: url,
            description: "kampus",
            created_at: "2026-09-13T12:50:35Z",
          },
        }),
      };
    }
    batches.push(JSON.parse(options.body));
    return { ok: true, json: async () => ({ accepted: true }) };
  };
  try {
    await import("../../Crawler/Backend/Tiktok/chrome_extension/background.mjs?thread-pagination");
    listener(
      {
        action: "start",
        origin: "http://127.0.0.1:54321/",
        code: "a".repeat(43),
        tabId: 1,
      },
      { id: "thread-test" },
      () => {},
    );
    const deadline = Date.now() + 3000;
    while (!detached && Date.now() < deadline)
      await new Promise((resolve) => priorTimeout(resolve, 10));
    assert.ok(detached);
    assert.equal(rounds, 6);
    assert.deepEqual(scrollRewinds, [true, ...Array(5).fill(false)]);
    const events = batches.flatMap((batch) => batch.events);
    assert.deepEqual(
      events.map((event) => event.payload.id),
      [root, cid, "300"],
    );
    assert.ok(
      batches.some(
        (batch) =>
          batch.done && !batch.warnings.includes("visible_pagination_idle"),
      ),
    );
    assert.ok(
      statuses.includes("Terhubung. Menunggu tugas dari crawler lokal…"),
    );
    assert.ok(
      !statuses.includes(
        "Koneksi tab terlepas. Hubungkan kembali untuk melanjutkan.",
      ),
    );
  } finally {
    listener?.({ action: "stop" }, { id: "thread-test" }, () => {});
    globalThis.chrome = priorChrome;
    globalThis.fetch = priorFetch;
    globalThis.setTimeout = priorTimeout;
  }
});

test("failed debugger attachment clears the session and permits another attempt", async () => {
  let listener,
    networkListener,
    attempts = 0;
  const statuses = [];
  globalThis.chrome = {
    runtime: {
      id: "test",
      getManifest: () => ({ version: "1.2.1" }),
      onMessage: { addListener: (f) => (listener = f) },
    },
    storage: { session: { set: async (value) => statuses.push(value.status) } },
    tabs: { get: async () => ({ url }) },
    debugger: {
      attach: async () => {
        attempts++;
        throw new Error("Another debugger attached");
      },
      onEvent: { addListener: (f) => (networkListener = f) },
      onDetach: { addListener: () => {} },
    },
  };
  await import("../../Crawler/Backend/Tiktok/chrome_extension/background.mjs");
  const message = {
    action: "start",
    origin: "http://127.0.0.1:54321/",
    code: "a".repeat(43),
    tabId: 1,
  };
  listener(message, { id: "test" }, () => {});
  await new Promise((resolve) => setImmediate(resolve));
  listener(message, { id: "test" }, () => {});
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(attempts, 2);
  assert.ok(statuses.some((value) => value.includes("Tutup debugger lain")));
  // Exercise the actual controller with a simulated selected TikTok tab and
  // native UI JSON. No browser is attached or external endpoint contacted.
  const batches = [],
    commands = [];
  let taskSent = false,
    detached = false;
  chrome.debugger.attach = async () => {};
  chrome.debugger.detach = async () => {
    detached = true;
  };
  chrome.tabs.update = async () => {
    networkListener({ tabId: 1 }, "Network.requestWillBeSent", {
      requestId: "search",
      request: {
        url: "https://www.tiktok.com/api/search/general/full/?keyword=kampus",
      },
    });
    networkListener({ tabId: 1 }, "Network.loadingFinished", {
      requestId: "search",
    });
  };
  chrome.debugger.sendCommand = async (_, method) => {
    commands.push(method);
    if (method === "Network.getResponseBody")
      return {
        body: Buffer.from(
          `{"items":[{"id":${root},"desc":"kampus 🎓","author":{"uniqueId":"example"},"createTime":1789303835}]}`,
          "utf8",
        ).toString("base64"),
        base64Encoded: true,
      };
    if (method === "Runtime.evaluate")
      return {
        result: {
          value: {
            ready: true,
            url: "https://www.tiktok.com/search?q=kampus",
            candidates: [],
            hydration: null,
          },
        },
      };
    return {};
  };
  const priorFetch = globalThis.fetch;
  globalThis.fetch = async (value, options) => {
    const parsed = new URL(value);
    assert.equal(parsed.origin, "http://127.0.0.1:54321");
    assert.equal(options.headers.Authorization, "Bearer " + message.code);
    if (parsed.pathname === "/api/task") {
      if (taskSent) throw new Error("Test bridge completed");
      taskSent = true;
      return {
        ok: true,
        json: async () => ({
          operation_id: oid,
          operation: "search",
          target: '{"query":"kampus"}',
          search_results: 1,
          scroll_pause_seconds: 1,
          request_interval_seconds: 1,
          idle_scroll_limit: 1,
          expires_at_unix: Date.now() / 1000 + 8,
        }),
      };
    }
    assert.equal(parsed.pathname, "/api/result");
    batches.push(JSON.parse(options.body));
    return { ok: true, json: async () => ({ accepted: true }) };
  };
  try {
    listener(message, { id: "test" }, () => {});
    const deadline = Date.now() + 8000;
    while (!detached && Date.now() < deadline)
      await new Promise((resolve) => setTimeout(resolve, 25));
    assert.ok(detached);
    assert.ok(batches.some((batch) => batch.done));
    const candidate = batches
      .flatMap((batch) => batch.events)
      .find((event) => event.kind === "candidate");
    assert.equal(candidate.payload.cached_root.id, root);
    assert.equal(candidate.payload.url, url);
    assert.equal(candidate.payload.cached_root.description, "kampus 🎓");
    assert.ok(!commands.some((method) => /cookie/i.test(method)));
  } finally {
    globalThis.fetch = priorFetch;
    listener({ action: "stop" }, { id: "test" }, () => {});
  }
});

test("all-comment controller collects 1200 comments and 100 replies across slow pages", async () => {
  const prior = {
    chrome: globalThis.chrome,
    fetch: globalThis.fetch,
    timeout: globalThis.setTimeout,
  };
  let listener,
    network,
    detached = false,
    taskSent = false,
    scrolls = 0,
    replyPages = 0,
    waitingForBody = false,
    firstScrollReplies;
  const bodies = new Map(),
    batches = [],
    states = [];
  globalThis.setTimeout = (fn, ms, ...args) =>
    prior.timeout(fn, ms === 10000 ? 500 : ms >= 1000 ? 5 : ms, ...args);
  const respond = (name, endpoint, body) => {
    bodies.set(name, body);
    network({ tabId: 1 }, "Network.requestWillBeSent", {
      requestId: name,
      request: { url: endpoint },
    });
    network({ tabId: 1 }, "Network.loadingFinished", { requestId: name });
  };
  const parents = (page) =>
    respond(
      "parents" + page,
      `https://www.tiktok.com/api/comment/list/?aweme_id=${root}&cursor=${page * 400}`,
      {
        has_more: page < 2 ? 1 : 0,
        comments: Array.from({ length: 400 }, (_, i) => ({
          cid: String(1000 + page * 400 + i),
          aweme_id: root,
          text: "comment " + i,
          reply_comment_total: page === 0 && i === 0 ? 100 : 0,
        })),
      },
    );
  globalThis.chrome = {
    runtime: {
      id: "large-test",
      getManifest: () => ({ version: "1.2.1" }),
      onMessage: { addListener: (f) => (listener = f) },
    },
    storage: {
      session: { set: async (value) => states.push(structuredClone(value)) },
    },
    tabs: { get: async () => ({ url }), update: async () => parents(0) },
    debugger: {
      attach: async () => {},
      detach: async () => {
        detached = true;
      },
      onEvent: { addListener: (f) => (network = f) },
      onDetach: { addListener: () => {} },
      sendCommand: async (_, method, params) => {
        if (method === "Network.getResponseBody") {
          if (params.requestId === "parents1") {
            waitingForBody = true;
            await new Promise((resolve) => prior.timeout(resolve, 60));
            waitingForBody = false;
          }
          return { body: JSON.stringify(bodies.get(params.requestId)) };
        }
        if (method !== "Runtime.evaluate") return {};
        const args = JSON.parse(
          params.expression.slice(params.expression.lastIndexOf(")(") + 2, -1),
        );
        if (args.action === "expand" && replyPages < 5) {
          assert.ok(
            scrolls >= 8,
            "all main comment pages precede reply clicks",
          );
          const page = replyPages++;
          respond(
            "replies" + page,
            `https://www.tiktok.com/api/comment/list/reply/?item_id=${root}&comment_id=1000&cursor=${page * 20}`,
            {
              has_more: page < 4 ? 1 : 0,
              comments: Array.from({ length: 20 }, (_, i) => ({
                cid: String(3000 + page * 20 + i),
                aweme_id: root,
                text: "reply",
              })),
            },
          );
          return {
            result: { value: { clicked: true, key: "reply-page-" + page } },
          };
        }
        if (args.action === "scroll") {
          assert.equal(
            waitingForBody,
            false,
            "wait for the pending response body before another scroll",
          );
          firstScrollReplies ??= replyPages;
          scrolls++;
          if (scrolls === 4) parents(1);
          if (scrolls === 8) parents(2);
        }
        return {
          result: {
            value: { ready: true, url, candidates: [], clicked: false },
          },
        };
      },
    },
  };
  globalThis.fetch = async (value, options) => {
    assert.equal(
      options.headers["X-BeeSense-Comment-Policy"],
      "source-pagination-v3",
    );
    if (new URL(value).pathname === "/api/task") {
      if (taskSent) throw new Error("Test complete");
      taskSent = true;
      return {
        ok: true,
        json: async () => ({
          operation_id: oid,
          operation: "thread",
          video_id: root,
          url,
          max_comments: null,
          collect_all_comments: true,
          max_replies: null,
          max_replies_per_thread: null,
          idle_scroll_limit: 3,
          expires_at_unix: Date.now() / 1000 + 3,
          cached_root: {
            id: root,
            link: url,
            created_at: "2026-09-13T12:50:35Z",
            description: "kampus",
          },
        }),
      };
    }
    batches.push(JSON.parse(options.body));
    return { ok: true, json: async () => ({ accepted: true }) };
  };
  try {
    await import("../../Crawler/Backend/Tiktok/chrome_extension/background.mjs?large-pagination");
    listener(
      {
        action: "start",
        origin: "http://127.0.0.1:54321/",
        code: "a".repeat(43),
        tabId: 1,
      },
      { id: "large-test" },
      () => {},
    );
    const deadline = Date.now() + 3000;
    while (!detached && Date.now() < deadline)
      await new Promise((r) => prior.timeout(r, 10));
    assert.ok(detached);
    const rows = batches.flatMap((b) => b.events).map((e) => e.payload);
    assert.equal(rows.filter((r) => r.kind === "comment").length, 1200);
    assert.equal(rows.filter((r) => r.kind === "reply").length, 100);
    assert.equal(new Set(rows.map((r) => r.id)).size, 1301);
    assert.equal(firstScrollReplies, 0);
    assert.equal(scrolls, 9);
    assert.ok(batches.every((b) => b.events.length <= 500));
    assert.equal(batches.at(-1).collection_status, "exhausted");
    assert.equal(batches.at(-1).status, "FINISHED_BEST_EFFORT");
    assert.deepEqual(states.at(-1).connectorState.counts, {
      posts: 1,
      comments: 1200,
      replies: 100,
    });
    assert.ok(
      !JSON.stringify(states).includes("a".repeat(43)),
      "pairing code stays out of session storage",
    );
  } finally {
    listener?.({ action: "stop" }, { id: "large-test" }, () => {});
    globalThis.chrome = prior.chrome;
    globalThis.fetch = prior.fetch;
    globalThis.setTimeout = prior.timeout;
  }
});

test("side panel opens on toolbar click and worker restart clears stale running state", async () => {
  const prior = globalThis.chrome;
  const writes = [],
    behavior = [];
  globalThis.chrome = {
    runtime: { id: "panel", onMessage: { addListener: () => {} } },
    sidePanel: { setPanelBehavior: async (value) => behavior.push(value) },
    storage: {
      session: {
        get: async () => ({
          connectorState: {
            running: true,
            phase: "human",
            counts: { posts: 2, comments: 4, replies: 1 },
          },
        }),
        set: async (value) => writes.push(value),
      },
    },
    debugger: {
      onEvent: { addListener: () => {} },
      onDetach: { addListener: () => {} },
    },
  };
  try {
    await import("../../Crawler/Backend/Tiktok/chrome_extension/background.mjs?panel-restart");
    await new Promise((resolve) => setImmediate(resolve));
    assert.deepEqual(behavior, [{ openPanelOnActionClick: true }]);
    assert.equal(writes.at(-1).connectorState.running, false);
    assert.equal(writes.at(-1).connectorState.phase, "stopped");
    assert.deepEqual(writes.at(-1).connectorState.counts, {
      posts: 2,
      comments: 4,
      replies: 1,
    });
  } finally {
    globalThis.chrome = prior;
  }
});
