import {
  COMMENT_PROTOCOL,
  CONNECTOR_BUILD,
  parsePublicJson,
  sourceVideos,
  sourceComments,
  sourceHasMore,
  commentPaginationExhausted,
  tiktokUrl,
  validateTask,
  pageOperation,
  retryAfter,
} from "./core.mjs";

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
let session = null,
  operation = null,
  resumeHuman = null;
const status = async (text) => chrome.storage.session.set({ status: text });
const cdp = async (method, params = {}) => {
  let timer;
  try {
    return await Promise.race([
      chrome.debugger.sendCommand({ tabId: session.tabId }, method, params),
      new Promise((_, reject) => {
        timer = setTimeout(() => reject(new Error("CHROME_TIMEOUT")), 10000);
      }),
    ]);
  } finally {
    clearTimeout(timer);
  }
};
const expired = () =>
  !session?.running ||
  (operation?.task.expires_at_unix != null &&
    Date.now() / 1000 >= operation.task.expires_at_unix);
async function bridge(path, body) {
  const response = await fetch(session.origin + path, {
    signal: AbortSignal.timeout(10000),
    method: body ? "POST" : "GET",
    headers: {
      Authorization: "Bearer " + session.code,
      "X-BeeSense-Comment-Policy": COMMENT_PROTOCOL,
      "X-BeeSense-Connector-Version": chrome.runtime.getManifest().version,
      "X-BeeSense-Connector-Build": CONNECTOR_BUILD,
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  if (!response.ok)
    throw new Error(
      response.status === 400
        ? "STALE_OPERATION"
        : response.status === 409
          ? "CONNECTOR_UPGRADE_REQUIRED"
          : response.status === 403
            ? "PAIRING_REJECTED"
            : "BRIDGE_UNAVAILABLE",
    );
  return response.json();
}
const page = async (action, extra = {}) => {
  const out = await cdp("Runtime.evaluate", {
    expression: `(${pageOperation.toString()})(${JSON.stringify({ action, id: operation.task.video_id, ...extra })})`,
    returnByValue: true,
  });
  if (out.exceptionDetails) throw new Error("COMMENT_CONTROL_ERROR");
  return out.result.value;
};
const requests = new Map();
chrome.debugger.onEvent.addListener((source, method, params) => {
  if (source.tabId !== session?.tabId || !operation) return;
  if (method === "Network.requestWillBeSent") {
    try {
      const u = tiktokUrl(params.request.url);
      if (!/^\/api\/(search|comment|item|challenge)\//.test(u.pathname)) return;
      requests.set(params.requestId, {
        epoch: operation.task.operation_id,
        path: u.pathname,
        root: u.searchParams.get("aweme_id") || u.searchParams.get("item_id"),
        parent: u.pathname.includes("/reply/")
          ? u.searchParams.get("comment_id")
          : null,
      });
    } catch {}
  } else if (method === "Network.responseReceived") {
    const request = requests.get(params.requestId);
    if (!request || request.epoch !== operation.task.operation_id) return;
    const code = params.response.status;
    if ([401, 403, 429].includes(code)) {
      operation.barrier =
        code === 429
          ? "RATE_LIMITED"
          : code === 401
            ? "LOGIN_REQUIRED"
            : "ACCESS_BLOCKED";
      if (code === 429) {
        const header = Object.entries(params.response.headers || {}).find(
          ([k]) => k.toLowerCase() === "retry-after",
        );
        operation.retryAfter = retryAfter(header?.[1]);
      }
    } else if (code >= 500)
      operation.interval = Math.max(5000, operation.interval * 2);
  } else if (method === "Network.loadingFinished") {
    const request = requests.get(params.requestId);
    requests.delete(params.requestId);
    const current = operation;
    if (!request || request.epoch !== current.task.operation_id) return;
    const pending = cdp("Network.getResponseBody", {
      requestId: params.requestId,
    })
      .then((body) => {
        if (operation !== current) return;
        let data;
        try {
          data = parsePublicJson(
            body.base64Encoded
              ? new TextDecoder().decode(
                  Uint8Array.from(atob(body.body), (c) => c.charCodeAt(0)),
                )
              : body.body,
          );
        } catch {
          current.warnings.add("native_json_unavailable");
          return;
        }
        if (
          data?.type === "verify" ||
          [2483, 2484].includes(data?.status_code)
        ) {
          current.barrier =
            data.type === "verify"
              ? "CAPTCHA_REQUIRED"
              : data.status_code === 2483
                ? "LOGIN_REQUIRED"
                : "RATE_LIMITED";
          return;
        }
        if (request.path.startsWith("/api/comment/")) {
          if (
            current.task.operation !== "thread" ||
            request.root !== current.task.video_id
          )
            return;
          current.commentPages.set(request.parent, sourceHasMore(data));
          for (const row of sourceComments(
            data,
            current.task.video_id,
            current.task.url,
            request.parent,
          ))
            current.comments.set(row.id, row);
        } else
          for (const video of sourceVideos(data))
            current.videos.set(video.id, video);
      })
      .catch(() => current.warnings.add("native_json_unavailable"))
      .finally(() => current.pending.delete(pending));
    current.pending.add(pending);
  }
});
chrome.debugger.onDetach.addListener((source) => {
  if (source.tabId === session?.tabId) {
    if (operation) operation.barrier = "INTERRUPTED";
    if (session) session.running = false;
    if (!session?.detaching)
      status("Chrome connection detached. No tab was closed.");
    if (resumeHuman) resumeHuman();
  }
});

async function flush(current, done = false) {
  const events = [],
    queued = new Set(current.sent);
  if (current.task.operation === "search") {
    for (const [id, item] of current.candidates) {
      if (queued.has(id)) continue;
      const root = current.videos.get(id) || item.cached_root;
      events.push({
        kind: "candidate",
        payload: { url: item.url, cached_root: root },
      });
      queued.add(id);
    }
    for (const [id, root] of current.videos) {
      if (queued.has(id)) continue;
      events.push({
        kind: "candidate",
        payload: { url: root.link, cached_root: root },
      });
      queued.add(id);
    }
  } else {
    const root =
      current.videos.get(current.task.video_id) || current.task.cached_root;
    if (root?.created_at && !queued.has(root.id)) {
      events.push({ kind: "record", payload: root });
      queued.add(root.id);
    }
    const rows = [...current.comments.values()].sort(
      (a, b) => Number(a.kind === "reply") - Number(b.kind === "reply"),
    );
    for (const row of rows) {
      if (
        queued.has(row.id) ||
        (row.kind === "reply" && !queued.has(row.parent_comment_id))
      )
        continue;
      events.push({ kind: "record", payload: row });
      queued.add(row.id);
    }
  }
  // Bound HTTP batches, acknowledge before marking IDs sent, and preserve parent
  // order across batches. Python independently validates caps and native IDs.
  for (
    let offset = 0;
    offset < events.length || (done && offset === 0);
    offset += 500
  ) {
    const batch = events.slice(offset, offset + 500),
      last = offset + 500 >= events.length;
    await bridge("/api/result", {
      operation_id: current.task.operation_id,
      events: batch,
      done: done && last,
      status: current.barrier || "FINISHED_BEST_EFFORT",
      warnings: [...current.warnings],
      collection_status: current.collectionStatus,
      ...(current.retryAfter
        ? { retry_after_seconds: current.retryAfter }
        : {}),
    });
    for (const event of batch)
      current.sent.add(
        event.payload.id ||
          event.payload.cached_root?.id ||
          new URL(event.payload.url).pathname.split("/").pop(),
      );
  }
  return events.length;
}
async function inspect(current) {
  const data = await page("read");
  if (data.captcha) {
    await status("CAPTCHA: selesaikan manual di TikTok, lalu tekan Lanjutkan.");
    await bridge("/api/progress", {
      operation_id: current.task.operation_id,
      stage: "captcha_required",
    });
    let confirmed = false;
    resumeHuman = () => {
      confirmed = true;
    };
    try {
      while (!confirmed && !expired()) await delay(250);
    } finally {
      resumeHuman = null;
    }
    if (expired()) {
      current.barrier = "CAPTCHA_REQUIRED";
      current.warnings.add("human_validation_required");
      return;
    }
    return inspect(current);
  }
  const actual = new URL(data.url),
    expected = new URL(validateTask(current.task));
  if (
    !data.ready ||
    actual.origin !== expected.origin ||
    (current.task.operation === "thread"
      ? !new RegExp(
          "^/@[^/]+/(?:video|photo)/" + current.task.video_id + "/?$",
        ).test(actual.pathname)
      : actual.pathname !== expected.pathname) ||
    actual.searchParams.get("q") !== expected.searchParams.get("q")
  )
    throw new Error("PAGE_UNAVAILABLE");
  // Search SPA hydration can retain unrelated homepage videos. Only matching
  // thread metadata is trusted; search metadata comes from captured responses.
  if (data.hydration && current.task.operation === "thread") {
    try {
      for (const row of sourceVideos(parsePublicJson(data.hydration)))
        if (row.id === current.task.video_id) current.videos.set(row.id, row);
    } catch {
      current.warnings.add("native_json_unavailable");
    }
  }
  for (const item of data.candidates || [])
    current.candidates.set(item.cached_root.id, item);
}
async function runTask(task) {
  const url = validateTask(task);
  const current = {
    task,
    videos: new Map(),
    comments: new Map(),
    commentPages: new Map(),
    candidates: new Map(),
    sent: new Set(),
    pending: new Set(),
    warnings: new Set(["comments_completeness_unverified"]),
    barrier: null,
    collectionStatus: "pending",
    interval: Math.max(
      1000,
      (task.scroll_pause_seconds || 3) * 1000,
      (task.request_interval_seconds || 3) * 1000,
    ),
  };
  operation = current;
  requests.clear();
  await status(
    "Crawling " +
      task.operation +
      " · " +
      (task.video_id || JSON.parse(task.target).query || "hashtag"),
  );
  try {
    await chrome.tabs.update(session.tabId, { url });
    let ready = false;
    for (let attempt = 0; attempt < 6 && !expired(); attempt++) {
      await delay(current.interval);
      try {
        await inspect(current);
        ready = true;
        break;
      } catch (error) {
        if (error.message !== "PAGE_UNAVAILABLE") throw error;
      }
    }
    if (!ready) throw new Error("PAGE_UNAVAILABLE");
    await flush(current);
    if (current.barrier || expired()) return;
    if (task.operation === "thread") {
      const root = current.videos.get(task.video_id) || task.cached_root;
      if (!root?.created_at) {
        current.warnings.add("post_metadata_unavailable");
        current.collectionStatus = "metadata_unavailable";
        current.barrier = "SOURCE_ERROR";
        return;
      }
      const stamp = Date.parse(root.created_at),
        policy = task.selection || {};
      if (
        (policy.since && stamp < Date.parse(policy.since)) ||
        (policy.until && stamp >= Date.parse(policy.until)) ||
        task.max_comments === 0
      ) {
        current.collectionStatus = "root_filtered";
        return;
      }
      await page("comments");
      await delay(current.interval);
    }
    let idle = 0;
    const collectAll =
      task.operation === "thread" &&
      (task.collect_all_comments === true || task.max_comments == null);
    const retryAfterRound = new Map();
    let round = 0,
      rewindNext = false,
      unproductiveClicks = 0;
    while (
      !expired() &&
      !current.barrier &&
      (collectAll || idle < (task.idle_scroll_limit || 3))
    ) {
      round++;
      if (current.pending.size) await Promise.allSettled([...current.pending]);
      await flush(current);
      if (
        task.operation === "thread" &&
        commentPaginationExhausted(
          current.commentPages,
          current.comments,
          task.max_replies !== 0 && task.max_replies_per_thread !== 0,
          (current.videos.get(task.video_id) || task.cached_root)?.stats
            ?.comment_count,
        )
      ) {
        current.collectionStatus = "exhausted";
        break;
      }
      const before = current.sent.size;
      const expanded =
        task.operation === "thread" &&
        task.max_replies !== 0 &&
        task.max_replies_per_thread !== 0 &&
        unproductiveClicks < 3
          ? await page("expand", {
              blocked: [...retryAfterRound]
                .filter(([, retry]) => retry > round)
                .map(([key]) => key),
            })
          : { clicked: false };
      let navigation = "membuka balasan";
      // Finish the visible parent's reply pages before moving its controls offscreen.
      if (!expanded.clicked) {
        unproductiveClicks = 0;
        const scroll = await page("scroll", {
          rewind: rewindNext,
        });
        navigation = scroll?.scrolled
          ? rewindNext
            ? "meninjau balasan sebelumnya"
            : "menggulir komentar"
          : "mencari panel komentar";
        // Traverse to the real bottom before revisiting earlier reply controls.
        // Rewinding every few idle rounds can trap long, already-loaded lists.
        rewindNext = collectAll && !rewindNext && scroll?.at_end === true;
        if (scroll?.comment_pane_missing) await page("comments");
      }
      await delay(Math.max(current.interval, Math.min(idle, 10) * 1000));
      await inspect(current);
      if (current.pending.size) await Promise.allSettled([...current.pending]);
      await flush(current);
      if (task.operation === "thread") {
        const parents = [...current.comments.values()].filter(
          (row) => row.kind === "comment",
        ).length;
        await status(
          `${parents} komentar · ${current.comments.size - parents} balasan · ${navigation}`,
        );
      }
      if (current.sent.size === before) {
        idle++;
        // Cool down each unproductive control independently. Clearing all
        // blocked controls every three idle rounds can cycle the same buttons
        // forever and prevent any downward scroll.
        if (expanded.clicked) {
          unproductiveClicks++;
          retryAfterRound.set(expanded.key, round + 6);
        }
      } else {
        idle = 0;
        unproductiveClicks = 0;
        if (expanded.clicked) retryAfterRound.delete(expanded.key);
      }
      if (
        task.operation === "search" &&
        task.search_results != null &&
        current.sent.size >= task.search_results
      )
        break;
    }
    if (!collectAll && idle >= (task.idle_scroll_limit || 3))
      current.warnings.add("visible_pagination_idle");
  } catch (error) {
    current.barrier = expired() ? "INTERRUPTED" : "SOURCE_ERROR";
    const reasons = {
      COMMENT_CONTROL_ERROR: "comment_control_error",
      PAGE_UNAVAILABLE: "tiktok_view_changed",
      CHROME_TIMEOUT: "chrome_command_timeout",
    };
    if (reasons[error.message]) current.warnings.add(reasons[error.message]);
    await status(
      error.message === "STALE_OPERATION"
        ? "Crawler operation expired."
        : "Operation failed; partial rows retained.",
    );
  } finally {
    if (expired() && !current.barrier) current.barrier = "INTERRUPTED";
    const expected = (current.videos.get(task.video_id) || task.cached_root)
      ?.stats?.comment_count;
    if (
      task.operation === "thread" &&
      expected != null &&
      Number(expected) > current.comments.size
    )
      current.warnings.add("comments_count_below_source_total");
    if (
      task.operation === "thread" &&
      task.max_comments == null &&
      !["exhausted", "root_filtered"].includes(current.collectionStatus)
    ) {
      current.warnings.add("comments_pagination_not_exhausted");
      if (!current.barrier) current.barrier = "COMMENTS_INCOMPLETE";
    }
    try {
      await flush(current, true);
    } catch {}
    operation = null;
    requests.clear();
  }
}
async function start(message) {
  if (session?.running) throw new Error("ALREADY_RUNNING");
  const origin = new URL(message.origin);
  if (
    origin.protocol !== "http:" ||
    origin.hostname !== "127.0.0.1" ||
    origin.pathname !== "/" ||
    origin.search ||
    origin.hash ||
    origin.username ||
    origin.password
  )
    throw new Error("INVALID_LOCAL_BRIDGE");
  const tab = await chrome.tabs.get(message.tabId);
  tiktokUrl(tab.url);
  if (!/^[a-zA-Z0-9_-]{32,128}$/.test(message.code))
    throw new Error("INVALID_PAIRING_CODE");
  session = {
    origin: origin.origin,
    code: message.code,
    tabId: message.tabId,
    running: true,
  };
  let attached = false;
  try {
    await chrome.debugger.attach({ tabId: message.tabId }, "1.3");
    attached = true;
    await cdp("Network.enable");
    let paired = false;
    while (session.running) {
      const task = await bridge("/api/task");
      if (!paired) {
        paired = true;
        await status("Terhubung ke crawler lokal.");
      }
      if (task) {
        await runTask(task);
      } else await delay(500);
    }
  } catch (error) {
    await status(
      error.message === "CONNECTOR_UPGRADE_REQUIRED"
        ? "Konektor tidak cocok. Reload BeeSense TikTok Connector 1.2.1 dari folder proyek ini."
        : error.message === "PAIRING_REJECTED"
          ? "Kode pasangan ditolak. Salin kode dari crawler yang sedang aktif."
          : attached
            ? "Local crawler disconnected; captured partial data stays in Python."
            : "Connection failed. Check the pairing code and release any other debugger on this TikTok tab.",
    );
  } finally {
    session.running = false;
    session.detaching = true;
    if (attached) {
      try {
        await chrome.debugger.detach({ tabId: session.tabId });
      } catch {}
    }
    session.code = "";
  }
}
chrome.runtime.onMessage.addListener((message, sender, reply) => {
  if (sender.id !== chrome.runtime.id) return;
  if (message.action === "start") {
    start(message).catch(() =>
      status(
        "Connection failed. Check the pairing code and release any other debugger on this TikTok tab.",
      ),
    );
    reply({ started: true });
  } else if (message.action === "continue") {
    if (resumeHuman) resumeHuman();
    reply({ continued: true });
  } else if (message.action === "stop") {
    if (session) session.running = false;
    if (resumeHuman) resumeHuman();
    reply({ stopping: true });
  }
});
