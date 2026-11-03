import { useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Database } from 'lucide-react';
import { api } from '../shared/api';
import { FieldErrorsContext, useApp } from '../shared/context';
import {
  crawlDateLabel,
  demoMode,
  initialConfig,
  number,
  platformName,
  validateStorage,
} from '../shared/domain';
import { useClock } from '../shared/hooks';
import type { FieldError, Job, Platform, TransactionMigrationPlan } from '../shared/types';
import { StorageSettings } from '../shared/StorageSettings';
import { Button, Dialog, Notice, Spinner } from '../shared/ui';

export default function TransactionMigration({ job, platform }: { job: Job; platform: Platform }) {
  const { session, cap } = useApp();
  const [params, setParams] = useSearchParams();
  const open = params.get('action') === 'migrate';
  const section = useRef<HTMLElement>(null);
  const id = params.get('migration') || '';
  useEffect(() => {
    if (open) {
      section.current?.focus({ preventScroll: true });
      section.current?.scrollIntoView({ block: 'start', behavior: 'instant' });
    }
  }, [open, job.id, id]);
  const [storage, setStorage] = useState(() => ({
    ...initialConfig().storage,
    destination: 'postgresql' as const,
  }));
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [plan, setPlan] = useState<TransactionMigrationPlan | null>(null);
  const key = useRef(crypto.randomUUID());
  const revision = useRef(0);
  const now = useClock();
  const available = demoMode || cap.migrationsAvailable === true;
  const setAction = () =>
    setParams(
      (previous) => {
        const next = new URLSearchParams(previous);
        if (open) next.delete('action');
        else next.set('action', 'migrate');
        return next;
      },
      { replace: true },
    );
  const progress = useQuery({
    queryKey: ['transaction-migration', job.id, platform, id],
    queryFn: async () => {
      const result = await api.transactionMigration(id);
      if (
        result.jobId !== job.id ||
        result.platform !== platform ||
        result.datasetId !== job.dataset?.id ||
        result.version !== job.dataset?.version
      )
        throw new Error('Progres tidak sesuai dengan transaksi ini.');
      return result;
    },
    enabled: !!id,
    refetchInterval: (q) =>
      q.state.data && ['COMPLETED', 'FAILED'].includes(q.state.data.status) ? false : 1000,
    retry: false,
  });
  const validate = useMutation({
    mutationFn: ({ target }: { target: typeof storage.postgresql; revision: number }) =>
      api.prepareTransactionMigration(job, platform, target),
    onSuccess: (result, input) => {
      if (input.revision !== revision.current) return;
      setPlan(result);
      key.current = crypto.randomUUID();
      setStorage((previous) => ({
        ...previous,
        postgresql: { ...previous.postgresql, connectionString: undefined },
      }));
    },
  });
  const start = useMutation({
    mutationFn: () => api.startTransactionMigration(plan!, key.current),
    onSuccess: (result) => {
      setPlan(null);
      setParams(
        (previous) => {
          const next = new URLSearchParams(previous);
          next.set('migration', result.id);
          next.set('action', 'migrate');
          return next;
        },
        { replace: true },
      );
    },
  });
  const state = progress.data;
  const running = !!state && ['QUEUED', 'RUNNING'].includes(state.status);
  return (
    <section
      ref={section}
      tabIndex={-1}
      className="transaction-migration"
      aria-label={`Migrasi transaksi ${job.name}`}
    >
      <div className="social-section-heading">
        <div>
          <h3>
            <Database size={18} aria-hidden="true" />
            Migrasi transaksi ke PostgreSQL
          </h3>
          <p>Data {platformName(platform)} dari pengambilan ini. Excel sumber tetap tersedia.</p>
        </div>
        {session.role === 'operator' && (
          <Button variant="secondary" aria-expanded={open} onClick={setAction}>
            {open ? 'Tutup pengaturan migrasi' : 'Atur migrasi transaksi'}
          </Button>
        )}
      </div>
      {session.role !== 'operator' && (
        <p>Pengamat dapat melihat progres. Migrasi dijalankan oleh operator.</p>
      )}
      {(open || id) && (
        <>
          {demoMode && (
            <Notice>
              Pratinjau frontend: proses migrasi disimulasikan. Tidak ada pembacaan Excel atau
              penulisan database.
            </Notice>
          )}
          {!available && (
            <Notice>
              Pengaturan dapat ditinjau. Migrasi tersedia setelah layanan transaksi terhubung.
            </Notice>
          )}
          {id && progress.isPending && (
            <p role="status">
              <Spinner />
              Memuat progres migrasi transaksi…
            </p>
          )}
          {progress.error && (
            <Notice tone="error">
              {progress.error.message}
              <Button variant="ghost" onClick={() => void progress.refetch()}>
                Muat ulang progres
              </Button>
            </Notice>
          )}
          {state && (
            <div
              className="migration-inline-progress"
              role="status"
              aria-label="Progres migrasi transaksi"
            >
              <div className="social-section-heading">
                <b>{state.phase}</b>
                <span>
                  {number(state.processed)} / {number(state.total)} baris
                </span>
              </div>
              <progress
                max={state.total || 1}
                value={state.processed}
                aria-label="Baris migrasi diproses"
              />
              <dl className="migration-inline-counts">
                <div>
                  <dt>Diproses</dt>
                  <dd>{number(state.processed)}</dd>
                </div>
                <div>
                  <dt>Tersimpan</dt>
                  <dd>{number(state.inserted)}</dd>
                </div>
                <div>
                  <dt>ID dilewati</dt>
                  <dd>{number(state.skipped)}</dd>
                </div>
              </dl>
              <p>
                {state.status === 'COMPLETED'
                  ? 'Selesai. ID yang sudah ada dilewati tanpa ditimpa.'
                  : 'Hitungan tersimpan diperbarui setelah proses selesai.'}
              </p>
              {state.error && <Notice tone="error">{state.error}</Notice>}
            </div>
          )}
          {session.role === 'operator' && open && (
            <div className="migration-inline-form">
              <FieldErrorsContext.Provider value={errors}>
                <StorageSettings
                  value={storage}
                  destinationLocked
                  change={(value) => {
                    revision.current += 1;
                    setStorage({ ...value, destination: 'postgresql' });
                    setPlan(null);
                    setErrors([]);
                    validate.reset();
                  }}
                />
              </FieldErrorsContext.Provider>
              <p className="field-hint">
                Seluruh post, komentar dan balasan pada transaksi ini ikut dimigrasikan. ID unik
                dipertahankan.
              </p>
              {(validate.error || start.error) && (
                <Notice tone="error">{(validate.error || start.error)?.message}</Notice>
              )}
              <Button
                loading={validate.isPending}
                disabled={!available || running || start.isPending}
                onClick={() => {
                  const issues = validateStorage(storage);
                  setErrors(issues);
                  if (!issues.length)
                    validate.mutate({
                      target: { ...storage.postgresql },
                      revision: revision.current,
                    });
                  else
                    requestAnimationFrame(() =>
                      document
                        .querySelector<HTMLInputElement>(
                          '.transaction-migration [aria-invalid="true"]',
                        )
                        ?.focus(),
                    );
                }}
              >
                {demoMode ? 'Tinjau simulasi migrasi' : 'Tinjau migrasi transaksi'}
              </Button>
            </div>
          )}
        </>
      )}
      <Dialog
        open={!!plan}
        title={`Migrasikan data ${platformName(platform)}?`}
        onClose={() => !start.isPending && setPlan(null)}
      >
        {plan && (
          <>
            <dl className="start-summary">
              <dt>Transaksi</dt>
              <dd>{job.name}</dd>
              <dt>Sosial media</dt>
              <dd>{platformName(plan.platform)}</dd>
              <dt>Tanggal crawling WIB</dt>
              <dd>{crawlDateLabel(plan.crawlDate)}</dd>
              <dt>Data transaksi</dt>
              <dd>{number(plan.total)} post, komentar & balasan</dd>
              <dt>PostgreSQL</dt>
              <dd>
                {plan.host}:{plan.port}
              </dd>
              <dt>Jika ID sudah ada</dt>
              <dd>Lewati tanpa menimpa</dd>
            </dl>
            {demoMode && <Notice>Hanya simulasi frontend. Database tidak diubah.</Notice>}
            {Date.parse(plan.expiresAt) <= now && (
              <Notice tone="warning">Review kedaluwarsa. Tutup dan tinjau ulang.</Notice>
            )}
            {start.error && <Notice tone="error">{start.error.message}</Notice>}
            <div className="dialog-actions">
              <Button variant="secondary" disabled={start.isPending} onClick={() => setPlan(null)}>
                Kembali
              </Button>
              <Button
                loading={start.isPending}
                disabled={Date.parse(plan.expiresAt) <= now}
                onClick={() => start.mutate()}
              >
                {demoMode ? 'Mulai simulasi migrasi' : 'Migrasikan transaksi'}
              </Button>
            </div>
          </>
        )}
      </Dialog>
    </section>
  );
}
