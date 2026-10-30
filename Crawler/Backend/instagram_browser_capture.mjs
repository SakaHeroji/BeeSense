// Only public post fields embedded in the rendered document are returned.
// No cookies, auth headers, tracking fields, or full hydration payloads leave Chrome.
export function instagramDocumentPayload(payload, shortcode, renderedCommentIds = []) {
  const mediaKey = "xdt_api__v1__media__shortcode__web_info";
  const commentKey = "xdt_api__v1__media__media_id__comments__connection";
  const result = {media: null, comments: []};
  const rendered = new Set(renderedCommentIds);
  const pending = [];
  const id = value => typeof value === "string" && /^[1-9]\d{0,29}$/.test(value)
    ? value : Number.isSafeInteger(value) && value > 0 ? String(value) : null;
  const user = value => ({pk: id(value?.pk ?? value?.id)});
  const stamp = value => Number.isSafeInteger(value) && value > 0
    && value < 253402300800 ? new Date(value * 1000).toISOString() : null;
  const seen = new Set();
  const add = (value, parent = null, depth = 0) => {
    const pk = id(value?.pk ?? value?.id);
    if (!pk || seen.has(pk) || typeof value.text !== "string" || depth > 5) return;
    seen.add(pk);
    const explicit = id(value.parent_comment_id ?? value.replied_to_comment_id) || parent;
    result.comments.push({pk, text: value.text, created_at_utc: stamp(value.created_at),
      user: user(value.user ?? value.owner), like_count: value.comment_like_count ?? value.like_count,
      replied_to_comment_id: explicit});
    for (const edge of value.edge_threaded_comments?.edges || []) add(edge.node, pk, depth + 1);
    for (const child of value.child_comments || []) add(child, pk, depth + 1);
  };
  const walk = (value, depth = 0) => {
    if (!value || typeof value !== "object" || depth > 26) return;
    const media = value[mediaKey]?.items?.find(item => item.code === shortcode);
    if (media && id(media.pk) && Number.isSafeInteger(media.taken_at)) {
      result.media = {pk: id(media.pk), code: media.code,
        caption_text: typeof media.caption?.text === "string" ? media.caption.text : "",
        taken_at: stamp(media.taken_at), user: user(media.user),
        like_count: media.like_count, comment_count: media.comment_count};
      for (const comment of media.preview_comments || []) add(comment);
    }
    // Streamed comment chunks often live in a separate script. Their native IDs
    // must also appear in a DOM permalink for this exact post before acceptance.
    for (const edge of value[commentKey]?.edges || [])
      pending.push({node: edge.node, besideSource: !!media});
    for (const child of Object.values(value)) walk(child, depth + 1);
  };
  walk(payload);
  if (result.media) for (const item of pending)
    if(item.besideSource || rendered.has(id(item.node?.pk ?? item.node?.id))) add(item.node);
  if (!result.media) result.comments = [];
  return result;
}

export function instagramBarrier(path, passwordFields, challengeFrame, httpStatus) {
  if (httpStatus === 429) return "RATE_LIMITED";
  if (challengeFrame || /^\/(challenge|checkpoint)\//.test(path)) return "CHALLENGE_REQUIRED";
  if (passwordFields || /^\/(accounts\/(login|password)|auth_platform)\//.test(path)) return "LOGIN_REQUIRED";
  if (httpStatus === 401 || httpStatus === 403) return "ACCESS_BLOCKED";
  return null;
}

export function instagramRetryAfter(value, now = Date.now()) {
  if (typeof value !== 'string' || !value.trim()) return null;
  const seconds = /^\d+(?:\.\d+)?$/.test(value.trim())
    ? Number(value) : (Date.parse(value) - now) / 1000;
  return Number.isFinite(seconds) ? Math.max(0, Math.ceil(seconds)) : null;
}

export function instagramSourceRateLimit(response) {
  try {
    const host = new URL(response.url()).hostname.toLowerCase();
    if (response.status() !== 429 || !(host === 'instagram.com' || host.endsWith('.instagram.com'))) return null;
    const headers = response.headers();
    const header = Object.entries(headers).find(([key]) => key.toLowerCase() === 'retry-after');
    return {status: 'RATE_LIMITED', retry_after_seconds: instagramRetryAfter(header ? String(header[1]) : '')};
  } catch { return null; }
}

export async function instagramNavigate(page, url, timeout) {
  // Chrome can reject goto with ERR_HTTP_RESPONSE_CODE_FAILURE before returning
  // its Response. Observe only main-document status and Retry-After, including
  // CDP extra-info headers; never serialize cookies or authentication headers.
  let status = null, retryAfter = null, session = null;
  const observe = (code, headers = {}) => {
    if (status === 429 && code !== 429) return;
    status = code;
    const header = Object.entries(headers).find(([name]) => name.toLowerCase() === 'retry-after');
    if (header) retryAfter = instagramRetryAfter(String(header[1]));
  };
  const listener = response => {
    if (response.request().isNavigationRequest() && response.frame() === page.mainFrame())
      observe(response.status(), response.headers());
  };
  page.on('response', listener);
  try {
    try {
      session = await page.context().newCDPSession(page);
      const {frameTree} = await session.send('Page.getFrameTree');
      const documents = new Set();
      session.on('Network.requestWillBeSent', event => {
        if (event.type === 'Document' && event.frameId === frameTree.frame.id) documents.add(event.requestId);
      });
      session.on('Network.responseReceivedExtraInfo', event => {
        if (documents.has(event.requestId)) observe(event.statusCode, event.headers);
      });
      await session.send('Network.enable');
    } catch { /* Standard Playwright response observation remains available. */ }
    let response = null;
    try {
      response = await page.goto(url, {waitUntil: 'domcontentloaded', timeout});
      if (response) observe(response.status(), response.headers());
    } catch (error) {
      // A generic navigation failure alone must never be called HTTP 429.
      if (![429, 401, 403].includes(status)) throw error;
    }
    return {response, http_status: status, retry_after_seconds: retryAfter};
  } finally {
    page.off('response', listener);
    if (session) await session.detach().catch(() => {});
  }
}
