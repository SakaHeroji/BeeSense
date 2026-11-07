import { flushSync } from 'react-dom';
import { useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { Clock3, Database, Layers3, Play, ShieldCheck } from 'lucide-react';
import { api, ApiError } from '../shared/api';
import { ConversationPicker } from '../shared/ConversationPicker';
import { FieldErrorsContext, useApp } from '../shared/context';
import {
  applyConversation,
  dateTime,
  demoMode,
  initialConfig,
  isoWib,
  number,
  platformDescription,
  platformName,
  platforms,
  storageLabels,
  validateConfig,
} from '../shared/domain';
import { useClock } from '../shared/hooks';
import type { Config, FieldError, Plan, Platform } from '../shared/types';
import { Button, Dialog, Errors, Field, Notice, PlatformMark, UnsavedGuard } from '../shared/ui';
import { StorageSettings } from '../shared/StorageSettings';

function emptyParallelConfig(): Config {
  const config = initialConfig();
  config.executionMode = 'parallel';
  for (const platform of platforms) config.platforms[platform].enabled = false;
  return config;
}

export default function ParallelWorkspace() {
  const { cap, session, notify } = useApp();
  const [config, setConfig] = useState(emptyParallelConfig);
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [dirty, setDirty] = useState(false);
  const [key, setKey] = useState(() => crypto.randomUUID());
  const revision = useRef(0);
  const conversations = useQuery({ queryKey: ['conversations'], queryFn: api.conversations });
  const client = useQueryClient();
  const navigate = useNavigate();
  const now = useClock();
  const active = platforms.filter((platform) => config.platforms[platform].enabled);
  const platformError = errors.find((error) => error.field === 'platforms');
  const change = (next: Config) => {
    revision.current += 1;
    setConfig(next);
    setDirty(true);
    setPlan(null);
    setErrors([]);
    setKey(crypto.randomUUID());
  };
  const field = <K extends keyof Config>(name: K, value: Config[K]) =>
    change({ ...config, [name]: value });
  const platformChange = (platform: Platform, values: Partial<Config['platforms'][Platform]>) =>
    change({
      ...config,
      platforms: {
        ...config.platforms,
        [platform]: { ...config.platforms[platform], ...values },
      },
    });
  const validate = useMutation({
    mutationFn: ({ snapshot }: { snapshot: Config; revision: number }) => api.validate(snapshot),
    onSuccess: (result, submitted) => {
      if (revision.current === submitted.revision) setPlan(result);
    },
    onError: (error, submitted) => {
      if (revision.current !== submitted.revision) return;
      if (error instanceof ApiError && error.fields.length) setErrors(error.fields);
      else notify(error.message);
    },
  });
  const start = useMutation({
    mutationFn: () => api.start(plan!, key),
    onSuccess: (job) => {
      client.setQueryData(['job', job.id], job);
      void client.invalidateQueries({ queryKey: ['jobs'] });
      flushSync(() => {
        setDirty(false);
        setPlan(null);
      });
      notify(
        demoMode
          ? 'Conversation parallel dibuat sebagai simulasi. Tidak ada crawling nyata.'
          : 'Conversation parallel diterima. Setiap platform dipantau secara terpisah.',
      );
      navigate(`/crawler/parallel/jobs/${encodeURIComponent(job.id)}`);
    },
    onError: (error) => notify(error.message),
  });
  const submit = (event: React.FormEvent) => {
    event.preventDefault();
    const issues: FieldError[] = [];
    if (!config.conversation)
      issues.push({ field: 'conversation', message: 'Pilih conversation sebelum mulai crawling.' });
    if (active.length < 2)
      issues.push({ field: 'platforms', message: 'Pilih minimal 2 platform untuk mode parallel.' });
    issues.push(...validateConfig(config, cap).filter((error) => error.field !== 'platforms'));
    setErrors(issues);
    if (!issues.length)
      validate.mutate({ snapshot: structuredClone(config), revision: revision.current });
  };
  return (
    <>
      <UnsavedGuard dirty={dirty} pathOnly />
      <header className="conversation-page-heading parallel-heading">
        <div className="parallel-title">
          <span className="parallel-title-icon">
            <Layers3 size={24} aria-hidden="true" />
          </span>
          <div>
            <span className="page-kicker">Satu conversation, beberapa sumber</span>
            <h1 id="main-title" tabIndex={-1}>
              Crawling parallel
            </h1>
            <p>
              Jalankan snapshot conversation yang sama pada beberapa platform. Kegagalan satu sumber
              tidak membatalkan sumber lain.
            </p>
          </div>
        </div>
        <span className="source-readiness available">
          <span /> {active.length} platform dipilih
        </span>
      </header>
      {session.role !== 'operator' ? (
        <Notice>
          Pengamat dapat melihat hasil. Crawling baru hanya dapat dimulai oleh operator.
        </Notice>
      ) : (
        <FieldErrorsContext.Provider value={errors}>
          <ConversationPicker
            conversations={conversations.data || []}
            value={config.conversation?.id || ''}
            pending={conversations.isPending}
            error={conversations.error?.message}
            onChange={(conversation) => {
              if (conversation) change(applyConversation(config, conversation));
              else change({ ...config, conversation: null, name: '', description: '' });
            }}
          />
          <form className="parallel-config-layout" onSubmit={submit} noValidate>
            <section className="panel parallel-platform-panel">
              <div className="social-section-heading">
                <div>
                  <span className="step-kicker">2 dari 2</span>
                  <h2>Pilih platform & target</h2>
                  <p>Setiap platform memakai worker, progres, dan hasilnya sendiri.</p>
                </div>
                <Layers3 size={21} aria-hidden="true" />
              </div>
              <Errors errors={errors} />
              <fieldset className="transaction-date-range">
                <legend>Rentang publikasi transaksi</legend>
                <div>
                  <Field
                    name="dates"
                    label="Mulai publikasi"
                    required
                    hint="Waktu Indonesia Barat (WIB)."
                  >
                    {(id) => (
                      <input
                        id={id}
                        type="datetime-local"
                        value={config.since}
                        onChange={(event) => field('since', event.target.value)}
                      />
                    )}
                  </Field>
                  <Field name="until" label="Sebelum tanggal" required>
                    {(id) => (
                      <input
                        id={id}
                        type="datetime-local"
                        value={config.until}
                        onChange={(event) => field('until', event.target.value)}
                      />
                    )}
                  </Field>
                </div>
              </fieldset>
              <fieldset
                className="parallel-platforms"
                aria-describedby={platformError ? 'parallel-platforms-error' : undefined}
              >
                <legend className="sr-only">Platform crawling parallel</legend>
                {platforms.map((platform) => {
                  const available = cap.platforms.includes(platform);
                  const selected = config.platforms[platform].enabled;
                  return (
                    <div
                      key={platform}
                      className={`parallel-platform ${selected ? 'selected' : ''} ${available ? '' : 'unavailable'}`}
                    >
                      <label>
                        <input
                          type="checkbox"
                          name="platforms"
                          checked={selected}
                          disabled={!available}
                          onChange={(event) =>
                            platformChange(platform, { enabled: event.target.checked })
                          }
                        />
                        <PlatformMark platform={platform} />
                        <span>
                          <b>{platformName(platform)}</b>
                          <small>
                            {available ? platformDescription[platform] : 'Belum tersedia'}
                          </small>
                        </span>
                      </label>
                      {selected && (
                        <Field
                          name={`${platform}.target`}
                          label={`Target ${platformName(platform)}`}
                        >
                          {(id) => (
                            <input
                              id={id}
                              type="number"
                              inputMode="numeric"
                              min={1}
                              max={cap.limits.maxPosts}
                              value={config.platforms[platform].target}
                              onChange={(event) =>
                                platformChange(platform, {
                                  target:
                                    event.target.value === '' ? Number.NaN : +event.target.value,
                                })
                              }
                            />
                          )}
                        </Field>
                      )}
                    </div>
                  );
                })}
              </fieldset>
              {platformError && (
                <p className="field-error" id="parallel-platforms-error">
                  {platformError.message}
                </p>
              )}
              <div className="parallel-safety-note">
                <ShieldCheck size={18} aria-hidden="true" />
                <p>
                  Akun dan sesi dibaca dari pengaturan tiap platform. Nilai kredensial tidak masuk
                  ke snapshot conversation atau formulir ini.
                </p>
              </div>
            </section>
            <aside className="social-controls">
              <section className="panel run-settings">
                <div className="social-section-heading">
                  <div>
                    <h2>Waktu eksekusi</h2>
                    <p>Satu deadline untuk seluruh transaksi parallel.</p>
                  </div>
                  <Clock3 size={20} aria-hidden="true" />
                </div>
                <label className="optional-time">
                  <input
                    type="checkbox"
                    checked={config.duration !== null}
                    onChange={(event) => field('duration', event.target.checked ? 3600 : null)}
                  />
                  <span>
                    <b>Batasi waktu crawling</b>
                    <small>Termasuk menunggu koneksi dan cooldown.</small>
                  </span>
                </label>
                {config.duration !== null && (
                  <Field name="duration" label="Limit waktu (jam)" required>
                    {(id) => (
                      <input
                        id={id}
                        type="number"
                        min={0.01}
                        step="any"
                        max={cap.limits.maxDuration / 3600}
                        value={
                          Number.isFinite(config.duration) ? (config.duration || 0) / 3600 : ''
                        }
                        onChange={(event) =>
                          field(
                            'duration',
                            event.target.value === ''
                              ? Number.NaN
                              : Math.round(+event.target.value * 3600),
                          )
                        }
                      />
                    )}
                  </Field>
                )}
              </section>
              <section className="panel storage-panel">
                <div className="social-section-heading">
                  <div>
                    <h2>Simpan hasil ke</h2>
                    <p>Berlaku untuk seluruh hasil conversation.</p>
                  </div>
                  <Database size={20} aria-hidden="true" />
                </div>
                <StorageSettings
                  value={config.storage}
                  change={(storage) => field('storage', storage)}
                />
              </section>
              <div className="run-action parallel-run-action">
                <div>
                  <span>{active.length} platform</span>
                  <span>
                    <Clock3 size={15} aria-hidden="true" />
                    {config.duration === null
                      ? 'Tanpa batas waktu'
                      : `${number(config.duration / 3600 || 0)} jam`}
                  </span>
                </div>
                <Button type="submit" loading={validate.isPending}>
                  <Play size={17} aria-hidden="true" /> Tinjau & mulai parallel
                </Button>
                <p>Conversation dan target platform ditinjau sekali lagi sebelum dimulai.</p>
              </div>
            </aside>
          </form>
          <Dialog
            open={!!plan}
            title="Mulai crawling parallel?"
            onClose={() => !start.isPending && setPlan(null)}
          >
            <dl className="start-summary">
              <dt>Conversation</dt>
              <dd>{config.name}</dd>
              <dt>Snapshot</dt>
              <dd>v{config.conversation?.version || '—'}</dd>
              <dt>Platform</dt>
              <dd>{active.map(platformName).join(', ')}</dd>
              <dt>Rentang publikasi</dt>
              <dd>
                {dateTime(isoWib(config.since))} – {dateTime(isoWib(config.until))}
              </dd>
              <dt>Durasi</dt>
              <dd>
                {config.duration === null
                  ? 'Tanpa batas waktu'
                  : `${number(config.duration / 3600)} jam`}
              </dd>
              <dt>Penyimpanan</dt>
              <dd>{storageLabels[config.storage.destination]}</dd>
            </dl>
            {plan?.warnings.map((warning) => (
              <Notice key={warning}>{warning}</Notice>
            ))}
            {plan && Date.parse(plan.expiresAt) <= now && (
              <Notice tone="error">Rencana kedaluwarsa. Tinjau ulang konfigurasi.</Notice>
            )}
            <div className="dialog-actions">
              <Button variant="secondary" onClick={() => setPlan(null)} disabled={start.isPending}>
                Kembali
              </Button>
              <Button
                onClick={() => start.mutate()}
                loading={start.isPending}
                disabled={!plan || Date.parse(plan.expiresAt) <= now}
              >
                <Play size={16} aria-hidden="true" />
                {demoMode ? 'Mulai simulasi parallel' : 'Mulai crawling parallel'}
              </Button>
            </div>
          </Dialog>
        </FieldErrorsContext.Provider>
      )}
    </>
  );
}
