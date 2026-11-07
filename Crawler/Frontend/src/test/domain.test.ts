import { describe, expect, it } from 'vitest';
import {
  applyConversation,
  csvCell,
  crawlDate,
  crawlDateLabel,
  redactConfig,
  initialConfig,
  platforms,
  isoWib,
  safeExternal,
  validateConfig,
} from '../shared/domain';
import { demoApi } from '../shared/demo';
describe('configuration boundary', () => {
  it('requires dates, enabled sources, and a descriptive name', async () => {
    const cap = await demoApi.capabilities();
    const c = initialConfig();
    for (const p of platforms) c.platforms[p].enabled = false;
    c.since = '';
    c.until = '';
    const fields = validateConfig(c, cap).map((e) => e.field);
    expect(fields).toEqual(expect.arrayContaining(['name', 'dates', 'platforms']));
  });
  it('rejects impossible targets, minimum comments and unavailable mandatory baseline', async () => {
    const cap = await demoApi.capabilities();
    cap.baselines[0].ready = false;
    const c = initialConfig();
    c.name = 'Riset';
    c.since = '2026-10-01T00:00';
    c.until = '2026-10-02T00:00';
    c.platforms.youtube.maxCandidates = 50;
    c.platforms.youtube.minComments = 101;
    c.platforms.youtube.maxComments = 100;
    expect(validateConfig(c, cap).map((e) => e.field)).toEqual(
      expect.arrayContaining(['youtube.target', 'youtube.minComments', 'baselines']),
    );
  });
  it('uses an inclusive start, exclusive end and a WIB offset', () => {
    expect(isoWib('2026-10-29T10:00')).toBe('2026-10-29T03:00:00.000Z');
    expect(isoWib('bad')).toBe('');
  });
  it('manual URLs contain no discovery queries', () => {
    const c = initialConfig('url');
    expect(c.platforms.youtube.queries).toBe('');
    expect(c.platforms.youtube.minComments).toBe(0);
    expect(c.filtersEnabled).toBe(false);
  });
  it('rejects new sources until the server advertises their adapter', async () => {
    const cap = await demoApi.capabilities();
    const c = initialConfig();
    cap.platforms = ['youtube', 'reddit'];
    c.platforms.instagram.enabled = true;
    expect(validateConfig(c, cap)).toContainEqual({
      field: 'platforms',
      message: 'Instagram belum tersedia.',
    });
    expect(platforms).toHaveLength(7);
    expect(platforms.filter((p) => initialConfig().platforms[p].enabled)).toEqual([
      'youtube',
      'reddit',
      'instagram',
      'tiktok',
      'x',
    ]);
  });
});
describe('safe rendering and export boundaries', () => {
  it('escapes spreadsheet formulas including leading whitespace and CSV quotes', () => {
    expect(csvCell(' =SUM(1,2)')).toBe('"\' =SUM(1,2)"');
    expect(csvCell('a"b')).toBe('"a""b"');
  });
  it('allows authorized link formats, never javascript or credentials', () => {
    expect(safeExternal('javascript:alert(1)')).toBeUndefined();
    expect(safeExternal(undefined)).toBeUndefined();
    expect(safeExternal('https://user:pass@example.test')).toBeUndefined();
    expect(safeExternal('https://example.test')).toBe('https://example.test/');
  });
});

describe('shared defaults, nullable limits and storage', () => {
  it('uses 1000 posts, unrestricted comments and no duration cap from the main JSON', async () => {
    const config = initialConfig('automatic', 'youtube');
    config.name = 'Uji';
    expect(config.duration).toBeNull();
    expect(config.storage.destination).toBe('excel');
    expect(config.platforms.youtube.target).toBe(1000);
    expect(config.platforms.youtube.maxComments).toBeNull();
    expect(config.platforms.youtube.maxReplies).toBeNull();
    expect(validateConfig(config, await demoApi.capabilities())).toEqual([]);
  });
  it('checks the PostgreSQL destination, host, port and URI agreement', async () => {
    const config = initialConfig('automatic', 'youtube');
    config.name = 'Uji';
    config.storage.destination = 'both';
    config.storage.postgresql.connectionString =
      'postgresql://demo:synthetic@192.0.2.4:5433/example';
    const cap = await demoApi.capabilities();
    expect(validateConfig(config, cap).map((e) => e.field)).toContain('storage.connectionString');
    config.storage.postgresql.host = '192.0.2.4';
    config.storage.postgresql.port = 5433;
    expect(validateConfig(config, cap)).toEqual([]);
    config.storage.postgresql.host = 'https://example.test';
    expect(validateConfig(config, cap).map((e) => e.field)).toContain('storage.host');
    config.storage.postgresql.port = 65536;
    expect(validateConfig(config, cap).map((e) => e.field)).toContain('storage.port');
  });
});

describe('transaction dates and redaction', () => {
  it('keeps publication dates on the transaction when applying a conversation', async () => {
    const conversation = structuredClone((await demoApi.conversations())[0]) as Awaited<
      ReturnType<typeof demoApi.conversations>
    >[number] & { since?: string; until?: string };
    conversation.since = '2024-01-01T00:00';
    conversation.until = '2024-02-01T00:00';
    const config = initialConfig('automatic', 'youtube');
    config.since = '2026-09-01T08:00';
    config.until = '2026-10-01T08:00';
    const applied = applyConversation(config, conversation);
    expect(applied.since).toBe('2026-09-01T08:00');
    expect(applied.until).toBe('2026-10-01T08:00');
    expect(applied.conversation).not.toHaveProperty('since');
    expect(applied.conversation).not.toHaveProperty('until');
  });
  it('uses execution time across WIB midnight, never the queued creation date', () => {
    expect(
      crawlDate({ startedAt: '2026-11-02T17:00:00Z', createdAt: '2026-10-01T00:00:00Z' }),
    ).toBe('2026-11-03');
    expect(
      crawlDate({ startedAt: '2026-11-02T16:59:59Z', createdAt: '2026-10-01T00:00:00Z' }),
    ).toBe('2026-11-02');
    expect(crawlDate({ createdAt: '2026-10-01T00:00:00Z' })).toBe('');
    expect(crawlDateLabel('')).toBe('Belum dieksekusi');
  });
  it('removes a connection secret without mutating the form', () => {
    const config = initialConfig();
    config.storage.postgresql.connectionString = 'secret-sentinel';
    expect(JSON.stringify(redactConfig(config))).not.toContain('secret-sentinel');
    expect(config.storage.postgresql.connectionString).toBe('secret-sentinel');
  });
});
