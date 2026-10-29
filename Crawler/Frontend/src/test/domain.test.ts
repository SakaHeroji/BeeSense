import { describe, expect, it } from 'vitest';
import {
  csvCell,
  initialConfig,
  platforms,
  isoWib,
  reviewUrls,
  safeExternal,
  surveyKey,
  validateConfig,
  validateSurvey,
} from '../shared/domain';
import { demoApi } from '../shared/demo';
import type { SurveyAnswer } from '../shared/types';

const response = (id = 'r1'): SurveyAnswer[] => [
  {
    survey_id: 'minat-studi',
    survey_version: '1',
    response_id: id,
    respondent_code: 'RESP-001',
    respondent_role: 'parent',
    submitted_at: '2026-10-29T10:00:00+07:00',
    question_id: 'Q01',
    answer_text: 'Kesesuaian minat',
    answer_value: '',
    usage_permission: 'granted',
    source_reference: 'sintetis',
  },
  {
    survey_id: 'minat-studi',
    survey_version: '1',
    response_id: id,
    respondent_code: 'RESP-001',
    respondent_role: 'parent',
    submitted_at: '2026-10-29T10:00:00+07:00',
    question_id: 'Q02',
    answer_text: '',
    answer_value: '4',
    usage_permission: 'granted',
    source_reference: 'sintetis',
  },
];
describe('configuration boundary', () => {
  it('requires dates, enabled sources, and a descriptive name', async () => {
    const cap = await demoApi.capabilities();
    const c = initialConfig();
    c.platforms.youtube.enabled = false;
    c.platforms.reddit.enabled = false;
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
    ]);
  });
});
describe('URL normalization', () => {
  it('collapses canonical, short and Shorts links by native ID', () => {
    const rows = reviewUrls([
      'https://youtu.be/abcdefghijk?si=tracking',
      'https://www.youtube.com/watch?v=abcdefghijk',
      'https://www.youtube.com/shorts/abcdefghijk',
    ]);
    expect(rows.map((r) => r.status)).toEqual(['valid', 'duplicate', 'duplicate']);
    expect(new Set(rows.map((r) => r.canonical)).size).toBe(1);
  });
  it('excludes historical IDs and canonicalizes Reddit post aliases', () => {
    const rows = reviewUrls(
      [
        'https://www.reddit.com/r/indonesia/comments/abc123/title/',
        'https://old.reddit.com/comments/abc123/',
      ],
      new Set(['reddit:abc123']),
    );
    expect(rows.map((r) => r.status)).toEqual(['existing', 'duplicate']);
  });
  it.each([
    ['instagram', 'https://instagram.com/reel/ABC_123/?igsh=track'],
    ['tiktok', 'https://www.tiktok.com/@kampus/video/1234567890123456789?lang=id'],
    ['threads', 'https://www.threads.net/@kampus/post/ABC_123?xmt=track'],
    ['facebook', 'https://m.facebook.com/permalink.php?story_fbid=123456789&id=987654321'],
    ['x', 'https://twitter.com/kampus/status/1234567890123456789/photo/1'],
  ])('accepts a full %s permalink without retaining tracking parameters', (platform, input) => {
    const row = reviewUrls([input])[0];
    expect(row.status).toBe('valid');
    expect(row.platform).toBe(platform);
    expect(row.canonical).not.toContain('?');
    expect(row.locatorKey).toMatch(new RegExp(`^${platform}:`));
  });
  it('deduplicates host aliases and keeps unverified locators separate from native IDs', () => {
    const rows = reviewUrls([
      'https://www.threads.net/@kampus/post/ABC123',
      'https://threads.com/@kampus/post/ABC123',
      'https://instagram.com/p/ABC123/',
      'https://instagram.com/reel/ABC123/',
      'https://facebook.com/story.php?id=123&story_fbid=456',
      'https://www.facebook.com/123/posts/456',
      'https://twitter.com/kampus/status/123456789',
      'https://x.com/i/status/123456789',
    ]);
    expect(rows.map((r) => r.status)).toEqual([
      'valid',
      'duplicate',
      'valid',
      'duplicate',
      'valid',
      'duplicate',
      'valid',
      'duplicate',
    ]);
    expect(rows[0].nativeId).toBeUndefined();
    expect(rows[2].nativeId).toBeUndefined();
    expect(rows[4].nativeId).toBeUndefined();
    expect(rows[6].nativeId).toBe('123456789');
  });
  it.each([
    'https://youtube.com.evil.test/watch?v=abcdefghijk',
    'https://evil.test',
    'http://www.youtube.com/watch?v=abcdefghijk',
    'https://user:pass@youtube.com/watch?v=abcdefghijk',
    'javascript:alert(1)',
    'https://www.youtube.com/channel/foo',
    'https://www.youtube.com:444/watch?v=abcdefghijk',
    'https://instagram.com.evil.test/p/ABC123/',
    'https://www.instagram.com/stories/kampus/123',
    'https://vm.tiktok.com/short/',
    'https://www.threads.com/@kampus',
    'https://facebook.com/share/p/short/',
    'https://x.com/kampus',
  ])('rejects unsupported or unsafe input %s', (url) => {
    expect(reviewUrls([url])[0].status).not.toBe('valid');
  });
});
describe('atomic survey responses', () => {
  it('preserves declared roles and question context with two answers per response', () => {
    const r = validateSurvey(response());
    expect(r.validResponses).toBe(1);
    expect(r.validRows).toHaveLength(2);
    expect(r.validRows[0].respondent_role).toBe('parent');
  });
  it('holds the whole response if one required answer is missing', () => {
    const rows = response();
    rows[1].answer_value = '';
    const r = validateSurvey(rows);
    expect(r.validRows).toHaveLength(0);
    expect(r.invalidResponses).toBe(1);
  });
  it('does not turn unknown or denied permission into analytic data', () => {
    const rows = response();
    rows.forEach((r) => (r.usage_permission = 'unknown'));
    const r = validateSurvey(rows);
    expect(r.deniedResponses).toBe(1);
    expect(r.validResponses).toBe(0);
  });
  it('separates complete responses when importing valid records only', () => {
    const bad = response('bad');
    bad[0].answer_text = '';
    const r = validateSurvey([...response('good'), ...bad]);
    expect(r.totalResponses).toBe(2);
    expect(r.validRows.every((x) => x.response_id === 'good')).toBe(true);
    expect(r.invalidResponses).toBe(1);
  });
  it('skips identical records and rejects conflicts without overwrite', () => {
    const rows = response();
    const known = new Map(rows.map((r) => [surveyKey(r), JSON.stringify(r)]));
    expect(validateSurvey(rows, known).duplicateResponses).toBe(1);
    rows[0].answer_text = 'Berbeda';
    const r = validateSurvey(rows, known);
    expect(r.invalidResponses).toBe(1);
    expect(r.validRows).toHaveLength(0);
  });
  it('never guesses role and requires consistent metadata', () => {
    const rows = response();
    rows[0].respondent_role = '';
    expect(validateSurvey(rows).invalidResponses).toBe(1);
  });
  it('holds incomplete questionnaires and duplicated question IDs', () => {
    expect(validateSurvey(response().slice(0, 1)).invalidResponses).toBe(1);
    const rows = response();
    rows[1].question_id = 'Q01';
    expect(validateSurvey(rows).invalidResponses).toBe(1);
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
