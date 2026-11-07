import { describe, expect, it, vi } from 'vitest';
import { httpApi } from '../shared/api';
import { emptyConversationDraft, initialConfig } from '../shared/domain';
import type { Plan } from '../shared/types';

describe('API transport contract', () => {
  it('sends credentials and stable idempotency key without submitting a second plan body', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 'j1' }), {
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    const plan: Plan = { id: 'p1', config: initialConfig(), expiresAt: '2099-01-01', warnings: [] };
    await httpApi.start(plan, 'stable-key');
    const [url, options] = fetchMock.mock.calls[0];
    expect(url).toContain('/acquisition-jobs');
    expect(options?.credentials).toBe('include');
    expect(options?.body).toBe('{"plan_id":"p1"}');
    expect(new Headers(options?.headers).get('Idempotency-Key')).toBe('stable-key');
  });
  it('fails clearly when a static host serves HTML instead of an API', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response('<html>SPA</html>', { headers: { 'Content-Type': 'text/html' } }),
    );
    await expect(httpApi.capabilities()).rejects.toThrow('Backend Crawler belum tersedia');
  });
  it('handles authorization denial without leaking server response details', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response('{"message":"sensitive internal detail"}', {
        status: 403,
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    await expect(httpApi.stop('private-job')).rejects.toThrow('Anda tidak memiliki izin');
  });
  it('sends only the conversation title to the Gemini draft endpoint', async () => {
    const generated = {
      ...emptyConversationDraft('Akses beasiswa mahasiswa daerah'),
      objective: 'Memahami akses beasiswa.',
    };
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify(generated), {
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    await httpApi.generateConversation('Akses beasiswa mahasiswa daerah');
    const [url, options] = fetchMock.mock.calls[0];
    expect(url).toContain('/crawler/conversations/generate');
    expect(options?.method).toBe('POST');
    expect(JSON.parse(options?.body as string)).toEqual({
      title: 'Akses beasiswa mahasiswa daerah',
    });
  });
});

describe('storage transport', () => {
  it('sends per-platform storage once to plan validation and redacts echoed credentials', async () => {
    const config = initialConfig('automatic', 'reddit');
    config.storage.destination = 'postgresql';
    config.storage.postgresql.connectionString = 'postgresql://demo:synthetic@127.0.0.1:5432/demo';
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 'p1', config, expiresAt: '2099-01-01', warnings: [] }), {
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    const plan = await httpApi.validate(config);
    expect(
      JSON.parse(fetchMock.mock.calls[0][1]!.body as string).config.storage.postgresql
        .connectionString,
    ).toContain('synthetic');
    expect(plan.config.storage.destination).toBe('postgresql');
    expect(plan.config.storage.postgresql.connectionString).toBeUndefined();
    expect(config.storage.postgresql.connectionString).toContain('synthetic');
  });
});
