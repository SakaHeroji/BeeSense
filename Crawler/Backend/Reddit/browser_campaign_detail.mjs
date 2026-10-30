import fs from 'node:fs/promises';
import path from 'node:path';
import {setTimeout as delay} from 'node:timers/promises';
import {inWindow} from './browser_campaign.mjs';

export function classifyCaptureFailure(snapshot) {
  if (/ERR_BLOCKED_BY_CLIENT|This page has been blocked by Chrome/i.test(snapshot)) return 'CLIENT_BROWSER_BLOCK';
  if (/blocked by network|verify (?:that )?you.re human|complete.*captcha|you.ve been blocked/i.test(snapshot)) return 'ACCESS_BARRIER';
  return 'BROWSER_CAPTURE_ERROR_UNVERIFIED';
}

export function rateLimitSeconds(text) {
  const match = text.match(/request has been rate limited[\s\S]*?break for\s+(\d+)\s+seconds/i);
  return match ? Number(match[1]) : null;
}

export async function enrichBatch(tab, directory, window, {batchSize = 6, target = 1000, requestDelayMs = 2000, keepPublicWebExcerpts = true} = {}) {
  const rawDirectory = path.join(directory, 'raw');
  await fs.mkdir(rawDirectory, {recursive: true});
  const allowedSubreddits = new Set(window.subreddits || ['indonesia', 'karir', 'indotech']);
  const candidates = JSON.parse(await fs.readFile(path.join(directory, 'candidates.json'), 'utf8'))
    .filter(row => allowedSubreddits.has(row.subreddit?.toLowerCase()) && inWindow(row.published_at, window.since, window.until));
  const allowedIds = new Set(candidates.map(row => row.native_id));
  const rawFiles = (await fs.readdir(rawDirectory)).filter(name => name.endsWith('.json'));
  const existing = await Promise.all(rawFiles.map(async name => ({
    id: name.slice(0, -5), value: JSON.parse(await fs.readFile(path.join(rawDirectory, name), 'utf8')),
  })));
  const acceptedVersions = new Set(['browser-dom:2', ...(keepPublicWebExcerpts ? ['public-web-excerpt:1'] : [])]);
  const completed = new Set(existing.filter(row => acceptedVersions.has(row.value.extractor_version) && allowedIds.has(row.id)).map(row => row.id));
  const obsolete = new Set(existing.filter(row => !acceptedVersions.has(row.value.extractor_version)).map(row => row.id));
  const receiptsFile = path.join(directory, 'thread_receipts.jsonl');
  let attempted = new Set();
  let lastRequestAt = 0;
  try {
    const prior = (await fs.readFile(receiptsFile, 'utf8')).trim().split('\n').filter(Boolean).map(line => JSON.parse(line));
    attempted = new Set(prior.map(row => row.native_id).filter(id => !obsolete.has(id)));
    lastRequestAt = Date.parse(prior.at(-1)?.started_at) || 0;
  }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  const queue = candidates.filter(row => !completed.has(row.native_id) && !attempted.has(row.native_id));
  const results = [];
  let consecutiveCaptureErrors = 0;
  for (const candidate of queue.slice(0, batchSize)) {
    if (completed.size >= target) break;
    const remainingDelay = requestDelayMs - (Date.now() - lastRequestAt);
    if (remainingDelay > 0) await delay(remainingDelay);
    lastRequestAt = Date.now();
    let receipt = {native_id: candidate.native_id, target: candidate.canonical_url, started_at: new Date().toISOString()};
    try {
      await tab.goto(candidate.canonical_url);
      await tab.playwright.locator('shreddit-post').first().waitFor({state: 'visible', timeoutMs: 10000});
      const captured = await tab.playwright.evaluate(nativeId => {
        const element = Array.from(document.querySelectorAll('shreddit-post')).find(post => post.id === 't3_' + nativeId);
        const banner = Array.from(document.querySelectorAll('[role="banner"], header')).map(item => item.innerText).join('\n');
        if (!element) return {post: null, comments: [], banner};
        const post = {
          native_id: nativeId, title: element.getAttribute('post-title'),
          text: element.querySelector('[id="' + element.id + '-post-rtjson-content"]')?.innerText ||
            Array.from(element.querySelectorAll('p')).map(p => p.innerText).join('\n\n'),
          published_at: element.getAttribute('created-timestamp'), permalink: element.getAttribute('permalink'),
          subreddit: element.getAttribute('subreddit-name'), post_type: element.getAttribute('post-type'),
          score_display: element.getAttribute('score'), comment_count_display: element.getAttribute('comment-count'),
          source_show_full_content: element.hasAttribute('show-full-content'),
        };
        const comments = Array.from(document.querySelectorAll('[role="article"]')).map(element => {
          const own = selector => Array.from(element.querySelectorAll(selector)).filter(child => child.closest('[role="article"]') === element);
          const link = own('a[href*="/comment/"]')[0];
          const commentId = link?.href.match(/\/comment\/([a-z0-9]+)\//)?.[1];
          const body = commentId ? element.querySelector('[id="t1_' + commentId + '-post-rtjson-content"]') : null;
          const parent = element.parentElement?.closest('[role="article"]');
          const parentLink = parent ? Array.from(parent.querySelectorAll('a[href*="/comment/"]')).find(child => child.closest('[role="article"]') === parent) : null;
          return {url: link?.href || null, parent_url: parentLink?.href || null,
            text: body?.innerText || own('p').map(p => p.innerText).join('\n\n'),
            published_at: own('time')[0]?.getAttribute('datetime') || null,
            published_display: own('time')[0]?.innerText || null};
        }).filter(row => row.url && row.text);
        return {post, comments, banner};
      }, candidate.native_id);
      const retryAfter = rateLimitSeconds(captured.banner);
      if (retryAfter !== null) throw Object.assign(new Error('Visible Reddit rate limit'), {name: 'RateLimitError', retryAfter});
      const {post, comments} = captured;
      if (!post || !post.title || !inWindow(post.published_at, window.since, window.until)) {
        receipt = {...receipt, status: post ? 'REJECTED_SOURCE_DATE_OR_TITLE' : 'POST_ID_MISMATCH'};
      } else {
        const capturedAt = new Date().toISOString();
        const value = {candidate, post, comments, captured_at: capturedAt,
          method: 'connected_chrome_rendered_dom', extractor_version: 'browser-dom:2', rss_used: false,
          coverage: 'PARTIAL_RENDERED_DOM', more_replies_expanded: false};
        const filename = path.join(rawDirectory, candidate.native_id + '.json');
        await fs.writeFile(filename + '.tmp', JSON.stringify(value));
        await fs.rename(filename + '.tmp', filename);
        completed.add(candidate.native_id);
        receipt = {...receipt, status: 'CAPTURED', comment_entries: comments.length, published_at: post.published_at};
      }
    } catch (error) {
      const snapshot = await tab.playwright.domSnapshot().catch(() => '');
      receipt = {...receipt, status: error.name === 'RateLimitError' ? 'RATE_LIMITED' : classifyCaptureFailure(snapshot),
        reason: 'browser_capture_failed_not_proof_post_missing', error_type: error.name};
      const retryAfter = error.retryAfter ?? rateLimitSeconds(snapshot);
      if (retryAfter !== null) {receipt.status = 'RATE_LIMITED'; receipt.retry_after_seconds = retryAfter;}
    }
    receipt.finished_at = new Date().toISOString();
    await fs.appendFile(receiptsFile, JSON.stringify(receipt) + '\n');
    results.push(receipt);
    consecutiveCaptureErrors = receipt.status === 'BROWSER_CAPTURE_ERROR_UNVERIFIED' ? consecutiveCaptureErrors + 1 : 0;
    if (['ACCESS_BARRIER', 'CLIENT_BROWSER_BLOCK', 'RATE_LIMITED'].includes(receipt.status)) break;
    if (consecutiveCaptureErrors >= 3) break;
  }
  const progress = {captured_posts: completed.size, target_posts: target,
    candidates: candidates.length, batch: results, updated_at: new Date().toISOString(),
    status: completed.size >= target ? 'TARGET_REACHED' : 'IN_PROGRESS_ACTIVE_BATCHES'};
  await fs.writeFile(path.join(directory, 'progress.json.tmp'), JSON.stringify(progress, null, 2));
  await fs.rename(path.join(directory, 'progress.json.tmp'), path.join(directory, 'progress.json'));
  return progress;
}
