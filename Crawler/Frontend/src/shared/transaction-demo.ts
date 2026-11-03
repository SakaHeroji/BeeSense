import { crawlDate, validateStorage } from './domain';
import { validateAuth } from './auth';
import type { Api, AuthStatus, TransactionMigration, TransactionMigrationPlan } from './types';

// Frontend-only fixtures. Never opens Excel, auth.json, a database, or a network connection.
const plans = new Map<string, TransactionMigrationPlan>();
const migrations = new Map<string, TransactionMigration>();
const accounts = new Map<string, AuthStatus>();
const completed = new Set<string>();
function operator() {
  if (sessionStorage.getItem('beesense:demo-role') === 'observer')
    throw new Error('Pengamat hanya dapat melihat hasil.');
}
const destinationKey = (p: TransactionMigrationPlan) =>
  `${p.platform}:${p.datasetId}:${p.version}:${p.host}:${p.port}`;
export const transactionDemoApi: Pick<
  Api,
  | 'prepareTransactionMigration'
  | 'startTransactionMigration'
  | 'transactionMigration'
  | 'authStatus'
  | 'saveAuth'
> = {
  async authStatus(platform) {
    return structuredClone(
      accounts.get(platform) || {
        platform,
        username: '',
        hasSession: false,
        file: 'config/auth.json',
        demo: true,
      },
    );
  },
  async saveAuth(platform, value) {
    operator();
    const errors = validateAuth(platform, value);
    if (errors.length) throw new Error(errors[0].message);
    const old = accounts.get(platform);
    const next: AuthStatus = {
      platform,
      username: value.username.replace(/^@/, '') || old?.username || '',
      hasSession: !!value.sessionid || !!old?.hasSession,
      file: 'config/auth.json',
      demo: true,
    };
    accounts.set(platform, next); // Only metadata; never retain the session ID.
    return structuredClone(next);
  },
  async prepareTransactionMigration(job, platform, target) {
    operator();
    const errors = validateStorage({ destination: 'postgresql', postgresql: target });
    if (errors.length) throw new Error(errors[0].message);
    const progress = job.platforms.find((p) => p.platform === platform);
    if (
      !progress ||
      !job.dataset?.rows ||
      !['COMPLETED', 'PARTIAL', 'CANCELLED'].includes(job.status) ||
      !crawlDate(job)
    )
      throw new Error('Pilih transaksi selesai dengan dataset dan tanggal crawling yang tersedia.');
    const total = progress.counts.roots + progress.counts.comments + progress.counts.replies;
    if (!total) throw new Error('Transaksi ini belum memiliki data untuk dimigrasikan.');
    const plan: TransactionMigrationPlan = {
      id: crypto.randomUUID(),
      expiresAt: new Date(Date.now() + 300000).toISOString(),
      jobId: job.id,
      platform,
      datasetId: job.dataset.id,
      version: job.dataset.version,
      checksum: job.dataset.checksum,
      crawlDate: crawlDate(job),
      total,
      host: target.host,
      port: target.port,
    };
    plans.set(plan.id, structuredClone(plan));
    return plan;
  },
  async startTransactionMigration(plan, key) {
    operator();
    const id = `demo-transaction-migration-${key}`;
    const existing = migrations.get(id);
    if (existing) {
      if (
        existing.jobId !== plan.jobId ||
        existing.platform !== plan.platform ||
        existing.datasetId !== plan.datasetId ||
        existing.version !== plan.version
      )
        throw new Error('Kunci permintaan sudah digunakan untuk transaksi lain.');
      return structuredClone(existing);
    }
    const stored = plans.get(plan.id);
    if (
      !stored ||
      stored.expiresAt <= new Date().toISOString() ||
      JSON.stringify(stored) !== JSON.stringify(plan)
    )
      throw new Error('Review berubah atau kedaluwarsa. Tinjau ulang transaksi.');
    if (
      [...migrations.values()].some(
        (m) =>
          destinationKey(m) === destinationKey(plan) && ['QUEUED', 'RUNNING'].includes(m.status),
      )
    )
      throw new Error('Migrasi transaksi ini sedang berlangsung.');
    const at = new Date().toISOString();
    const result: TransactionMigration = {
      ...stored,
      id,
      status: 'QUEUED',
      phase: 'Menyiapkan transaksi simulasi',
      createdAt: at,
      updatedAt: at,
      processed: 0,
      inserted: 0,
      skipped: 0,
      demo: true,
    };
    migrations.set(id, result);
    return structuredClone(result);
  },
  async transactionMigration(id) {
    const job = migrations.get(id);
    if (!job)
      throw new Error('Progres simulasi tidak tersedia. Tinjau kembali transaksi crawling.');
    if (job.status !== 'COMPLETED') {
      const ratio = Math.min(1, Math.max(0, (Date.now() - Date.parse(job.createdAt)) / 10000));
      job.status = ratio === 1 ? 'COMPLETED' : 'RUNNING';
      job.phase =
        ratio === 1
          ? 'Simulasi migrasi selesai'
          : ratio < 0.25
            ? 'Memeriksa ID transaksi'
            : 'Menyalin data simulasi';
      job.updatedAt = new Date().toISOString();
      job.processed = Math.floor(job.total * ratio);
      if (ratio === 1) {
        const duplicate = completed.has(destinationKey(job));
        job.inserted = duplicate ? 0 : job.total;
        job.skipped = duplicate ? job.total : 0;
        completed.add(destinationKey(job));
      }
    }
    return structuredClone(job);
  },
};
