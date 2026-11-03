import { flushSync } from 'react-dom';
import { useRef, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  CalendarDays,
  Check,
  Clock3,
  Database,
  FolderOpen,
  Play,
  Search,
  Settings2,
} from 'lucide-react';
import { api, ApiError } from '../shared/api';
import { FieldErrorsContext, useApp } from '../shared/context';
import {
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
import { useClock, useUrlState } from '../shared/hooks';
import type { Config, FieldError, Plan, Platform } from '../shared/types';
import { Button, Dialog, Errors, Field, Notice, PlatformMark, UnsavedGuard } from '../shared/ui';
import PlatformResults from './PlatformResults';
import { StorageSettings } from '../shared/StorageSettings';
import { AuthSettings } from '../shared/AuthSettings';
import type { AuthInput } from '../shared/types';

export default function PlatformWorkspace() {
  const { platform = 'youtube' } = useParams();
  if (!platforms.includes(platform as Platform)) return <Navigate to="/crawler/youtube" replace />;
  return <PlatformPage key={platform} platform={platform as Platform} />;
}

function PlatformPage({ platform }: { platform: Platform }) {
  const { cap, session, notify } = useApp();
  const [view] = useUrlState('view', 'config');
  const [config, setConfig] = useState(() => ({
    ...initialConfig('automatic', platform),
    name: `Riset pendidikan di ${platformName(platform)}`,
  }));
  const [dirty, setDirty] = useState(false);
  const [credentials, setCredentials] = useState<AuthInput>({ username: '', sessionid: '' });
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [key, setKey] = useState(() => crypto.randomUUID());
  const revision = useRef(0);
  const now = useClock();
  const client = useQueryClient();
  const navigate = useNavigate();
  const supported = cap.platforms.includes(platform);
  const backendAvailable = ['youtube', 'reddit', 'instagram', 'x'].includes(platform);
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
  const settings = config.platforms[platform];
  const platformField = (name: 'queries' | 'hashtags' | 'target', value: string | number) =>
    change({
      ...config,
      platforms: { ...config.platforms, [platform]: { ...settings, [name]: value } },
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
          ? 'Pekerjaan simulasi dibuat. Tidak ada koneksi database atau crawling nyata.'
          : 'Pekerjaan crawling diterima. Progres dapat dipantau di halaman ini.',
      );
      navigate(`/crawler/${platform}/jobs/${encodeURIComponent(job.id)}`);
    },
    onError: (error) => notify(error.message),
  });
  const submit = (event: React.FormEvent) => {
    event.preventDefault();
    if (credentials.username || credentials.sessionid) {
      notify('Simpan pengaturan akun ke auth.json terlebih dahulu, atau kosongkan isian akun.');
      document.querySelector<HTMLButtonElement>('.account-actions button:last-child')?.focus();
      return;
    }
    const issues = validateConfig(config, cap);
    setErrors(issues);
    if (!issues.length)
      validate.mutate({ snapshot: structuredClone(config), revision: revision.current });
  };
  return (
    <>
      <UnsavedGuard dirty={dirty || !!credentials.username || !!credentials.sessionid} pathOnly />
      <header className="social-heading">
        <div className="social-identity">
          <PlatformMark platform={platform} />
          <div>
            <h1 id="main-title" tabIndex={-1}>
              {platformName(platform)}
            </h1>
            <p>{platformDescription[platform]}. Konfigurasi dan hasil dalam satu tempat.</p>
          </div>
        </div>
        <span className={`source-readiness ${backendAvailable ? 'available' : ''}`}>
          <span />
          {backendAvailable ? 'Siap dikonfigurasi' : 'Segera tersedia'}
        </span>
      </header>
      <nav className="page-tabs social-tabs" aria-label={`Halaman ${platformName(platform)}`}>
        <Link
          aria-current={view !== 'results' ? 'page' : undefined}
          className={view !== 'results' ? 'active' : ''}
          to={`/crawler/${platform}`}
        >
          <Settings2 size={17} aria-hidden="true" />
          Konfigurasi crawling
        </Link>
        <Link
          aria-current={view === 'results' ? 'page' : undefined}
          className={view === 'results' ? 'active' : ''}
          to={`/crawler/${platform}?view=results`}
        >
          <FolderOpen size={17} aria-hidden="true" />
          Hasil per tanggal
        </Link>
      </nav>
      {view === 'results' ? (
        <PlatformResults platform={platform} />
      ) : (
        <>
          {!backendAvailable && (
            <Notice>
              Pengaturan {platformName(platform)} dapat ditinjau di sini.{' '}
              {demoMode
                ? 'Mulai hanya menjalankan simulasi; pengambilan data nyata belum tersedia.'
                : 'Crawling baru dapat dimulai setelah pengambilan data platform ini tersedia.'}
            </Notice>
          )}
          {session.role !== 'operator' ? (
            <Notice>
              Anda dapat melihat hasil per tanggal. Pengaturan crawling hanya dapat diubah oleh
              operator.
            </Notice>
          ) : (
            <FieldErrorsContext.Provider value={errors}>
              <form className="social-config-layout" onSubmit={submit} noValidate>
                <section className="panel social-form">
                  <div className="social-section-heading">
                    <div>
                      <h2>Apa yang ingin dikumpulkan?</h2>
                      <p>
                        Nilai awal mengikuti konfigurasi proyek. Sesuaikan untuk pengambilan ini.
                      </p>
                    </div>
                    <Search size={21} aria-hidden="true" />
                  </div>
                  <Errors errors={errors} />
                  <Field name="name" label="Nama pengambilan" required>
                    {(id) => (
                      <input
                        id={id}
                        maxLength={120}
                        value={config.name}
                        onChange={(e) => field('name', e.target.value)}
                        placeholder="Contoh: Pilihan jurusan November…"
                      />
                    )}
                  </Field>
                  <fieldset className="social-fieldset">
                    <legend>
                      <CalendarDays size={18} aria-hidden="true" />
                      Tanggal publikasi post
                    </legend>
                    <p className="section-description">
                      Waktu dalam WIB. Tanggal crawling akan dicatat terpisah pada hasil.
                    </p>
                    <div className="form-grid">
                      <Field name="dates" label="Dari tanggal" required>
                        {(id) => (
                          <input
                            id={id}
                            type="datetime-local"
                            value={config.since}
                            onChange={(e) => field('since', e.target.value)}
                          />
                        )}
                      </Field>
                      <Field
                        name="dates"
                        label="Sampai sebelum tanggal"
                        required
                        hint="Batas akhir tidak termasuk."
                      >
                        {(id) => (
                          <input
                            id={id}
                            type="datetime-local"
                            value={config.until}
                            onChange={(e) => field('until', e.target.value)}
                          />
                        )}
                      </Field>
                    </div>
                  </fieldset>
                  <fieldset className="social-fieldset">
                    <legend>Kata kunci pada post</legend>
                    <div className="form-grid">
                      <Field
                        name="include"
                        label="Include keywords"
                        hint="Satu kata atau frasa per baris."
                      >
                        {(id) => (
                          <textarea
                            id={id}
                            rows={4}
                            value={config.include}
                            onChange={(e) => field('include', e.target.value)}
                            placeholder="beasiswa kuliah…"
                          />
                        )}
                      </Field>
                      <Field
                        name="exclude"
                        label="Exclude keywords"
                        hint="Post yang cocok akan dilewati."
                      >
                        {(id) => (
                          <textarea
                            id={id}
                            rows={4}
                            value={config.exclude}
                            onChange={(e) => field('exclude', e.target.value)}
                            placeholder="Kata atau topik yang dikecualikan…"
                          />
                        )}
                      </Field>
                    </div>
                  </fieldset>
                  <fieldset className="social-fieldset">
                    <legend>Pencarian {platformName(platform)}</legend>
                    {platform === 'instagram' ? (
                      <Field
                        name={`${platform}.hashtags`}
                        label="Hashtag"
                        required
                        hint="Instagram menggunakan hashtag. Tulis satu per baris; tanda # boleh disertakan."
                      >
                        {(id) => (
                          <textarea
                            id={id}
                            rows={5}
                            value={settings.hashtags}
                            onChange={(e) => platformField('hashtags', e.target.value)}
                            placeholder="kuliah\nbeasiswa…"
                            spellCheck={false}
                          />
                        )}
                      </Field>
                    ) : (
                      <Field
                        name={`${platform}.queries`}
                        label="Queries pencarian"
                        required
                        hint="Satu query per baris. Hashtag dapat ditulis langsung dalam query jika platform mendukungnya."
                      >
                        {(id) => (
                          <textarea
                            id={id}
                            rows={5}
                            value={settings.queries}
                            onChange={(e) => platformField('queries', e.target.value)}
                            placeholder="biaya kuliah beasiswa…"
                            spellCheck={false}
                          />
                        )}
                      </Field>
                    )}
                    {platform === 'reddit' && (
                      <Field
                        name="subreddit"
                        label="Subreddit"
                        hint="Pisahkan dengan koma, tanpa r/."
                      >
                        {(id) => (
                          <input
                            id={id}
                            value={config.subreddit}
                            onChange={(e) => field('subreddit', e.target.value)}
                            spellCheck={false}
                          />
                        )}
                      </Field>
                    )}
                    <div className="context-preserved">
                      <Check size={17} aria-hidden="true" />
                      <span>
                        Seluruh komentar dan balasan yang tersedia ikut diambil, tanpa batas jumlah.
                      </span>
                    </div>
                  </fieldset>
                </section>
                <aside className="social-controls">
                  <section className="panel run-settings">
                    <div className="social-section-heading">
                      <div>
                        <h2>Target pengambilan</h2>
                        <p>Post unik yang lolos filter.</p>
                      </div>
                      <Play size={20} aria-hidden="true" />
                    </div>
                    <Field
                      name={`${platform}.target`}
                      label="Jumlah post"
                      required
                      hint="Komentar dan balasan tidak mengurangi target post."
                    >
                      {(id) => (
                        <input
                          id={id}
                          type="number"
                          inputMode="numeric"
                          min={1}
                          max={cap.limits.maxPosts}
                          value={Number.isFinite(settings.target) ? settings.target : ''}
                          onChange={(e) =>
                            platformField('target', e.target.value === '' ? NaN : +e.target.value)
                          }
                        />
                      )}
                    </Field>
                    <label className="optional-time">
                      <input
                        type="checkbox"
                        checked={config.duration !== null}
                        onChange={(e) => field('duration', e.target.checked ? 3600 : null)}
                      />
                      <span>
                        <b>Batasi waktu crawling</b>
                        <small>Opsional. Default tanpa batas waktu.</small>
                      </span>
                    </label>
                    {config.duration !== null && (
                      <Field
                        name="duration"
                        label="Limit waktu (jam)"
                        required
                        hint="Termasuk waktu tunggu selama pengambilan."
                      >
                        {(id) => (
                          <input
                            id={id}
                            type="number"
                            min={0.01}
                            step="any"
                            max={cap.limits.maxDuration / 3600}
                            value={
                              Number.isFinite(config.duration) ? (config.duration ?? 0) / 3600 : ''
                            }
                            onChange={(e) =>
                              field(
                                'duration',
                                e.target.value === '' ? NaN : Math.round(+e.target.value * 3600),
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
                        <p>Excel lokal dipilih secara default.</p>
                      </div>
                      <Database size={20} aria-hidden="true" />
                    </div>
                    <StorageSettings
                      value={config.storage}
                      change={(storage) => field('storage', storage)}
                    />
                  </section>
                  <AuthSettings
                    platform={platform}
                    value={credentials}
                    change={(value) => {
                      setCredentials(value);
                    }}
                  />
                  <div className="run-action">
                    <div>
                      <span>{number(settings.target || 0)} post</span>
                      <span>
                        <Clock3 size={15} aria-hidden="true" />
                        {config.duration === null
                          ? 'Tanpa batas waktu'
                          : `${number(config.duration / 3600 || 0)} jam`}
                      </span>
                    </div>
                    <Button type="submit" loading={validate.isPending} disabled={!supported}>
                      <Play size={17} aria-hidden="true" />
                      Tinjau & mulai crawling
                    </Button>
                    <p>Konfigurasi ditinjau sekali lagi sebelum proses dimulai.</p>
                  </div>
                </aside>
              </form>
            </FieldErrorsContext.Provider>
          )}
          <Dialog
            open={!!plan}
            title={`Mulai crawling ${platformName(platform)}?`}
            onClose={() => !start.isPending && setPlan(null)}
          >
            <dl className="start-summary">
              <dt>Nama pengambilan</dt>
              <dd>{config.name}</dd>
              <dt>Target</dt>
              <dd>{number(settings.target)} post unik, seluruh komentar & balasan</dd>
              <dt>Publikasi mulai</dt>
              <dd>{dateTime(isoWib(config.since))}</dd>
              <dt>Publikasi sebelum</dt>
              <dd>{dateTime(isoWib(config.until))}</dd>
              <dt>Durasi</dt>
              <dd>
                {config.duration === null
                  ? 'Tanpa batas waktu'
                  : `${number(config.duration / 3600)} jam`}
              </dd>
              <dt>Penyimpanan</dt>
              <dd>{storageLabels[config.storage.destination]}</dd>
              {config.storage.destination !== 'excel' && (
                <>
                  <dt>Host PostgreSQL</dt>
                  <dd>
                    {config.storage.postgresql.host}:{config.storage.postgresql.port}
                  </dd>
                </>
              )}
            </dl>
            {plan?.warnings.map((warning) => (
              <Notice key={warning}>{warning}</Notice>
            ))}
            {plan && Date.parse(plan.expiresAt) <= now && (
              <Notice tone="error">
                Rencana kedaluwarsa. Tutup dialog dan tinjau ulang konfigurasi.
              </Notice>
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
                {demoMode ? 'Mulai simulasi' : 'Mulai crawling'}
              </Button>
            </div>
          </Dialog>
        </>
      )}
    </>
  );
}
