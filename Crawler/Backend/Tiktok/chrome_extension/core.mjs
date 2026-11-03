export function tiktokUrl(value) {
  const u = new URL(value);
  if (
    u.protocol !== "https:" ||
    u.hostname !== "www.tiktok.com" ||
    u.port ||
    u.username ||
    u.password
  )
    throw new Error("INVALID_TIKTOK_URL");
  return u;
}

export function parsePublicJson(text) {
  // Preserve numeric native IDs before JSON.parse can round integers above 2^53.
  let result = "",
    quoted = false,
    escaped = false;
  for (let i = 0; i < text.length;) {
    const c = text[i];
    if (quoted) {
      result += c;
      i++;
      if (escaped) escaped = false;
      else if (c === "\\") escaped = true;
      else if (c === '"') quoted = false;
      continue;
    }
    if (c === '"') {
      quoted = true;
      result += c;
      i++;
      continue;
    }
    if (/[0-9-]/.test(c)) {
      const match = text.slice(i).match(/^-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/);
      if (match) {
        const token = match[0];
        result += /^\d{16,}$/.test(token) ? JSON.stringify(token) : token;
        i += token.length;
        continue;
      }
    }
    result += c;
    i++;
  }
  return JSON.parse(result);
}

const nativeId = (value) => {
  if (typeof value === "number" && !Number.isSafeInteger(value))
    throw new Error("UNSAFE_NATIVE_ID");
  const id = String(value);
  if (!/^[1-9][0-9]{0,24}$/.test(id)) throw new Error("INVALID_NATIVE_ID");
  return id;
};
const metric = (value) =>
  typeof value === "number" && Number.isSafeInteger(value) && value >= 0
    ? value
    : typeof value === "string" && /^\d+$/.test(value)
      ? value
      : null;

export function sourceVideo(value) {
  const id = nativeId(value.id);
  const author =
    typeof value.author === "string"
      ? value.author
      : value.author?.uniqueId || value.author?.unique_id;
  if (!/^[a-zA-Z0-9_.]{1,40}$/.test(author || ""))
    throw new Error("MISSING_SOURCE_AUTHOR");
  const stamp = value.createTime ?? value.create_time;
  const stats = value.statsV2 || value.stats || {};
  return {
    id,
    link: `https://www.tiktok.com/@${author}/video/${id}`,
    description: value.desc || "",
    created_at: stamp ? new Date(Number(stamp) * 1000).toISOString() : null,
    stats: Object.fromEntries(
      Object.entries({
        play_count: "playCount",
        like_count: "diggCount",
        comment_count: "commentCount",
        share_count: "shareCount",
        save_count: "collectCount",
        repost_count: "repostCount",
      }).map(([name, key]) => [name, metric(stats[key])]),
    ),
  };
}

export function sourceVideos(body) {
  const out = new Map();
  function walk(v) {
    if (!v || typeof v !== "object") return;
    if (v.id && typeof v.desc === "string" && v.author) {
      try {
        const item = sourceVideo(v);
        out.set(item.id, item);
      } catch {}
    }
    for (const value of Object.values(v)) walk(value);
  }
  walk(body);
  return [...out.values()];
}

export function sourceComments(body, root, url, parent = null) {
  const result = [];
  for (const row of body.comments || body.data?.comments || []) {
    try {
      if (row.aweme_id && nativeId(row.aweme_id) !== root) continue;
      const id = nativeId(row.cid);
      result.push({
        id,
        video_id: root,
        kind: parent ? "reply" : "comment",
        parent_comment_id: parent,
        link: url + "?comment_id=" + id,
        text: row.text || "",
        created_at: row.create_time
          ? new Date(Number(row.create_time) * 1000).toISOString()
          : null,
        like_count: metric(row.digg_count),
        reply_count: metric(row.reply_comment_total),
      });
      result.push(
        ...sourceComments({ comments: row.reply_comment || [] }, root, url, id),
      );
    } catch {}
  }
  return result;
}

export function sourceHasMore(body) {
  const data = body.data && typeof body.data === "object" ? body.data : body;
  if (!Array.isArray(data.comments)) return null;
  if ([false, 0, "0"].includes(data.has_more)) return false;
  if ([true, 1, "1"].includes(data.has_more)) return true;
  return null;
}

export function commentPaginationExhausted(
  pages,
  comments,
  includeReplies = true,
) {
  if (pages.get(null) !== false) return false;
  if (!includeReplies) return true;
  const counts = new Map();
  for (const row of comments.values())
    if (row.kind === "reply")
      counts.set(
        row.parent_comment_id,
        (counts.get(row.parent_comment_id) || 0) + 1,
      );
  for (const row of comments.values()) {
    if (row.kind !== "comment" || pages.get(row.id) === false) continue;
    if (
      row.reply_count == null ||
      (counts.get(row.id) || 0) < Number(row.reply_count)
    )
      return false;
  }
  return true;
}

export function retryAfter(value, now = Date.now()) {
  if (/^\d+$/.test(String(value))) return Math.max(1, Number(value));
  const stamp = Date.parse(value);
  return Number.isFinite(stamp)
    ? Math.max(1, Math.ceil((stamp - now) / 1000))
    : 60;
}

export function validateTask(task) {
  if (
    !task ||
    !/^[a-f0-9]{32}$/.test(task.operation_id) ||
    !["search", "thread"].includes(task.operation)
  )
    throw new Error("INVALID_TASK");
  if (task.operation === "thread") {
    const u = tiktokUrl(task.url),
      match = u.pathname.match(
        /^\/@[a-zA-Z0-9_.]+\/(video|photo)\/([1-9][0-9]{0,24})\/?$/,
      );
    if (!match || match[2] !== nativeId(task.video_id) || u.search || u.hash)
      throw new Error("TASK_ID_MISMATCH");
    return u.href;
  }
  const spec = JSON.parse(task.target);
  if (
    typeof spec.query === "string" &&
    spec.query.trim() &&
    spec.query.length <= 300
  )
    return (
      "https://www.tiktok.com/search?" + new URLSearchParams({ q: spec.query })
    );
  if (typeof spec.hashtag === "string" && /^\w{1,100}$/.test(spec.hashtag))
    return "https://www.tiktok.com/tag/" + spec.hashtag;
  throw new Error("INVALID_SEARCH");
}

// Executed in the selected TikTok document. No cookies, storage, credentials or
// synthetic API requests are read or created. Only public DOM/UI is accessed.
export function pageOperation({ action, id, blocked = [] }) {
  const visible = (e) => !!e && !!e.getClientRects().length;
  const challenge = [
    ...document.querySelectorAll(
      'iframe[src*="captcha"],[id*="captcha"],[class*="captcha_verify"]',
    ),
  ].some(visible);
  if (challenge) return { captcha: true };
  if (action === "read") {
    const candidates = [
      ...new Map(
        [
          ...document.querySelectorAll(
            '[data-e2e="search_top-item-list"] a[href],a[data-e2e="search-video-link"]',
          ),
        ]
          .filter((a) => /\/@[^/]+\/(video|photo)\/[1-9][0-9]+/.test(a.href))
          .map((a) => {
            const u = new URL(a.href);
            u.search = "";
            u.hash = "";
            const ident = u.pathname.split("/").pop();
            return [
              ident,
              {
                url: u.href,
                cached_root: {
                  id: ident,
                  link: u.href,
                  description: a.querySelector("img")?.alt || "",
                  created_at: null,
                  stats: {},
                },
              },
            ];
          }),
      ).values(),
    ];
    const script = document.querySelector(
      "script#__UNIVERSAL_DATA_FOR_REHYDRATION__",
    );
    return {
      candidates,
      hydration: script?.textContent || null,
      url: location.href,
      ready: document.readyState !== "loading",
    };
  }
  if (action === "comments") {
    const button = [
      ...document.querySelectorAll('button,[role="button"]'),
    ].find(
      (e) =>
        visible(e) &&
        /^(Read or add comments|Comments$)/i.test(
          e.getAttribute("aria-label") || e.textContent?.trim() || "",
        ),
    );
    if (button) {
      button.click();
      return { clicked: true };
    }
    return { clicked: false };
  }
  if (action === "expand") {
    for (const button of document.querySelectorAll(
      'button,[role="button"],[data-e2e^="view-more"],p,span',
    )) {
      const text = (button.textContent || "").trim();
      if (
        !visible(button) ||
        !/^(?:View\s+(?:\d+\s+)?(?:repl|more)|Lihat\s+(?:\d+\s+)?balasan)/i.test(
          text,
        )
      )
        continue;
      let wrapper = button.parentElement;
      while (wrapper && !wrapper.querySelector('[data-e2e="comment-level-1"]'))
        wrapper = wrapper.parentElement;
      const key =
        (
          wrapper?.querySelector('[data-e2e="comment-level-1"]')?.textContent ||
          ""
        ).slice(0, 160) +
        "|" +
        text;
      if (blocked.includes(key)) continue;
      button.click();
      return { clicked: true, key };
    }
    return { clicked: false };
  }
  if (action === "scroll") {
    const comment = document.querySelector('[data-e2e="comment-level-1"]');
    let el =
      comment ||
      document.querySelector(
        '[data-e2e="comment-list"],[class*="CommentListContainer"],[data-e2e="search_top-item-list"]',
      );
    while (
      el &&
      !(
        el.scrollHeight > el.clientHeight + 20 &&
        /(auto|scroll)/.test(getComputedStyle(el).overflowY)
      )
    )
      el = el.parentElement;
    el = el || document.scrollingElement;
    el?.scrollBy(0, Math.max(500, (el.clientHeight || 700) * 0.8));
    return { scrolled: !!el };
  }
  return { invalid: true };
}
