import {test} from 'node:test';
import assert from 'node:assert/strict';
import {inWindow, mergeCandidates} from './browser_campaign.mjs';

const window = {since: '2025-10-27T00:00:00+07:00', until: '2026-10-28T00:00:00+07:00'};
const source = {subreddit: 'indonesia', query: 'kuliah', url: 'https://www.reddit.com/r/indonesia/search/?q=kuliah&t=year'};
const row = {native_id: 'abc123', subreddit: 'indonesia', title: 'Biaya kuliah', canonical_url: 'https://www.reddit.com/r/indonesia/comments/abc123/biaya_kuliah/', published_at: '2026-01-01T00:00:00Z'};

test('year boundaries honor Jakarta timezone and exclusive end', () => {
  assert.equal(inWindow('2025-10-26T16:59:59Z', window.since, window.until), false);
  assert.equal(inWindow('2025-10-26T17:00:00Z', window.since, window.until), true);
  assert.equal(inWindow('2026-10-27T17:00:00Z', window.since, window.until), false);
  assert.equal(inWindow('unknown', window.since, window.until), false);
});
test('same native post discovered by two searches remains one post with both origins', () => {
  const first = mergeCandidates([], [row], source, window);
  const second = mergeCandidates(first, [row], {...source, query: 'universitas', url: source.url + '&sort=top'}, window);
  assert.equal(second.length, 1);
  assert.deepEqual(second[0].queries, ['kuliah', 'universitas']);
  assert.equal(second[0].searches.length, 2);
  assert.equal(second[0].discovered_from, source.url);
});
test('reject out-of-period, unknown dates, unrelated hosts, mismatched IDs and empty titles', () => {
  const invalid = [{...row, published_at: '2024-01-01Z'}, {...row, published_at: null},
    {...row, canonical_url: 'https://example.com/r/indonesia/comments/abc123/title/'},
    {...row, native_id: 'wrong'}, {...row, title: ''},
    {...row, canonical_url: 'https://www.reddit.com/r/elsewhere/comments/abc123/title/'}];
  assert.deepEqual(mergeCandidates([], invalid, source, window), []);
});
