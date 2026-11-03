import { beforeEach, describe, expect, it, vi } from 'vitest';
import { demoApi } from '../shared/demo';
import { initialConfig } from '../shared/domain';
import { validateAuth } from '../shared/auth';
import { httpApi } from '../shared/api';
import type { Job, TransactionMigrationPlan } from '../shared/types';
beforeEach(() => sessionStorage.setItem('beesense:demo-role', 'operator'));
async function fixture(): Promise<Job> {
  const job = (await demoApi.jobs()).find((j) => j.id === 'demo-riset-001')!;
  return structuredClone(job);
}
describe('transaction-bound frontend migration', () => {
  it('scopes preparation to the selected source and rejects unrelated/unfinished data', async () => {
    const job = await fixture();
    const target = initialConfig().storage.postgresql;
    const plan = await demoApi.prepareTransactionMigration(job, 'reddit', target);
    expect(plan.total).toBe(798);
    expect(plan.platform).toBe('reddit');
    expect(plan.jobId).toBe(job.id);
    expect(plan.datasetId).toBe(job.dataset!.id);
    await expect(demoApi.prepareTransactionMigration(job, 'instagram', target)).rejects.toThrow(
      'Pilih transaksi',
    );
    job.status = 'RUNNING';
    await expect(demoApi.prepareTransactionMigration(job, 'reddit', target)).rejects.toThrow(
      'Pilih transaksi',
    );
  });
  it('binds review and idempotency key to the transaction and rejects tampering', async () => {
    const job = await fixture();
    const plan = await demoApi.prepareTransactionMigration(job, 'youtube', {
      ...initialConfig().storage.postgresql,
      host: '192.0.2.101',
    });
    await expect(
      demoApi.startTransactionMigration({ ...plan, platform: 'reddit' }, crypto.randomUUID()),
    ).rejects.toThrow('Review berubah');
    const key = crypto.randomUUID();
    const first = await demoApi.startTransactionMigration(plan, key);
    expect(await demoApi.startTransactionMigration(plan, key)).toEqual(first);
    await expect(
      demoApi.startTransactionMigration({ ...plan, jobId: 'other' }, key),
    ).rejects.toThrow('transaksi lain');
  });
  it('reports progress and skips completed dataset IDs on a repeat simulation', async () => {
    vi.useFakeTimers();
    try {
      const job = await fixture();
      const target = { ...initialConfig().storage.postgresql, host: '192.0.2.102' };
      const one = await demoApi.startTransactionMigration(
        await demoApi.prepareTransactionMigration(job, 'youtube', target),
        crypto.randomUUID(),
      );
      vi.advanceTimersByTime(5000);
      const halfway = await demoApi.transactionMigration(one.id);
      expect(halfway.processed).toBeGreaterThan(0);
      expect(halfway.inserted).toBe(0);
      vi.advanceTimersByTime(6000);
      expect(await demoApi.transactionMigration(one.id)).toMatchObject({
        status: 'COMPLETED',
        inserted: 4550,
        skipped: 0,
      });
      const two = await demoApi.startTransactionMigration(
        await demoApi.prepareTransactionMigration(job, 'youtube', target),
        crypto.randomUUID(),
      );
      vi.advanceTimersByTime(11000);
      expect(await demoApi.transactionMigration(two.id)).toMatchObject({
        status: 'COMPLETED',
        inserted: 0,
        skipped: 4550,
      });
    } finally {
      vi.useRealTimers();
    }
  });
  it('denies observer mutation', async () => {
    const job = await fixture();
    sessionStorage.setItem('beesense:demo-role', 'observer');
    await expect(
      demoApi.prepareTransactionMigration(job, 'youtube', initialConfig().storage.postgresql),
    ).rejects.toThrow('Pengamat');
  });
  it('never exposes a DSN in the review metadata', async () => {
    const job = await fixture();
    const plan = await demoApi.prepareTransactionMigration(job, 'youtube', {
      ...initialConfig().storage.postgresql,
      connectionString: 'postgresql://demo:synthetic-secret@127.0.0.1:5432/demo',
    });
    expect(JSON.stringify(plan)).not.toContain('synthetic-secret');
  });
});
describe('optional authentication inputs', () => {
  it('rejects blank saves and session IDs with control characters', () => {
    expect(validateAuth('instagram', { username: '', sessionid: '' })).toHaveLength(1);
    expect(
      validateAuth('instagram', { username: 'demo', sessionid: 'bad\nsession' })[0].field,
    ).toBe('sessionid');
    expect(validateAuth('x', { username: 'https://x.com/demo', sessionid: '' })[0].field).toBe(
      'username',
    );
  });
  it('keeps sessions isolated between sources, retaining an existing session for a blank update', async () => {
    await demoApi.saveAuth('facebook', { username: 'first_demo', sessionid: 'synthetic-secret' });
    await demoApi.saveAuth('facebook', { username: 'second_demo', sessionid: '' });
    expect(await demoApi.authStatus('facebook')).toMatchObject({
      username: 'second_demo',
      hasSession: true,
      file: 'config/auth.json',
    });
    expect(await demoApi.authStatus('tiktok')).toMatchObject({ username: '', hasSession: false });
  });
});
describe('future HTTP contract', () => {
  it('posts a dataset-bound migration request instead of file uploads', async () => {
    const job = await fixture();
    const mock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValue(new Response('{}', { headers: { 'Content-Type': 'application/json' } }));
    await httpApi.prepareTransactionMigration(job, 'reddit', initialConfig().storage.postgresql);
    expect(mock.mock.calls[0][0]).toContain(
      '/acquisition-jobs/demo-riset-001/platforms/reddit/migration-plans',
    );
    expect(JSON.parse(mock.mock.calls[0][1]!.body as string)).toMatchObject({
      dataset_id: job.dataset!.id,
      version: job.dataset!.version,
      checksum: job.dataset!.checksum,
    });
  });
  it('sends only plan ID and idempotency key when migration starts', async () => {
    const mock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValue(new Response('{}', { headers: { 'Content-Type': 'application/json' } }));
    await httpApi.startTransactionMigration(
      { id: 'plan', jobId: 'job', platform: 'x' } as TransactionMigrationPlan,
      'stable',
    );
    expect(mock.mock.calls[0][1]!.body).toBe('{"plan_id":"plan"}');
    expect(new Headers(mock.mock.calls[0][1]!.headers).get('Idempotency-Key')).toBe('stable');
  });
  it('sends credentials only to the selected source auth endpoint', async () => {
    const mock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValue(new Response('{}', { headers: { 'Content-Type': 'application/json' } }));
    await httpApi.saveAuth('x', { username: 'demo', sessionid: 'synthetic-only' });
    expect(mock.mock.calls[0][0]).toContain('/crawler/platforms/x/auth');
    expect(mock.mock.calls[0][1]!.credentials).toBe('include');
  });
});
