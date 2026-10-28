import fs from 'node:fs/promises';
import path from 'node:path';

export function inWindow(value, since, until) {
  const time = Date.parse(value);
  return Number.isFinite(time) && time >= Date.parse(since) && time < Date.parse(until);
}

export function mergeCandidates(existing, incoming, source, window) {
  const map = new Map(existing.map(row => [row.native_id, row]));
  for (const row of incoming) {
    const match = row.canonical_url?.match(/^https:\/\/www\.reddit\.com\/r\/([A-Za-z0-9_]+)\/comments\/([a-z0-9]+)\//);
    if (!match || match[1].toLowerCase() !== source.subreddit.toLowerCase() ||
        match[2] !== row.native_id || !row.title?.trim() ||
        !inWindow(row.published_at, window.since, window.until)) continue;
    const previous = map.get(row.native_id);
    map.set(row.native_id, {
      ...row,
      discovered_from: previous?.discovered_from || source.url,
      queries: [...new Set([...(previous?.queries || []), source.query])],
      searches: [...new Set([...(previous?.searches || []), source.url])],
      observed_at: new Date().toISOString(),
    });
  }
  return [...map.values()];
}

export async function createCollector(tab, directory, source, window) {
  await fs.mkdir(directory, {recursive: true});
  const filename = path.join(directory, 'candidates.json');
  let rows;
  try { rows = JSON.parse(await fs.readFile(filename, 'utf8')); }
  catch (error) { if (error.code !== 'ENOENT') throw error; rows = []; }

  async function capture() {
    const cards = await tab.playwright.getByRole('heading', {level: 2}).evaluateAll(headings =>
      headings.map(heading => {
        const card = heading.parentElement?.parentElement;
        const url = heading.querySelector('a')?.href;
        const match = url?.match(/\/r\/([^/]+)\/comments\/([a-z0-9]+)\//);
        return match ? {
          native_id: match[2], subreddit: match[1], canonical_url: url,
          title: heading.innerText,
          published_at: card?.querySelector('time')?.getAttribute('datetime') || null,
          published_display: card?.querySelector('time')?.innerText || null,
          metrics_display: card?.innerText.split('\n').at(-1) || null,
        } : null;
      }).filter(Boolean));
    const before = rows.length;
    rows = mergeCandidates(rows, cards, source, window);
    await fs.writeFile(filename + '.tmp', JSON.stringify(rows, null, 2));
    await fs.rename(filename + '.tmp', filename);
    const receipt = {at: new Date().toISOString(), source, dom_cards: cards.length,
      unique_candidates: rows.length, added: rows.length - before,
      oldest_in_dom: cards.at(-1)?.published_at || null};
    await fs.appendFile(path.join(directory, 'search_receipts.jsonl'), JSON.stringify(receipt) + '\n');
    return receipt;
  }

  async function step() {
    await tab.scroll([700, 650], 'down', 5);
    await tab.getAXState({emit: false});
    return capture();
  }

  return {capture, step, get rows() {return rows;}};
}
