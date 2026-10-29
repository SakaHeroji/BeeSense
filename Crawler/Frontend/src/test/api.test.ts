import { describe, expect, it, vi } from 'vitest';
import { httpApi } from '../shared/api';
import { initialConfig } from '../shared/domain';
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
});
