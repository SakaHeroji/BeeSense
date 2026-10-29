import { flushSync } from 'react-dom';
import { useClock } from '../shared/hooks';
import { useRef, useState } from 'react';
import { Link, useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import {
  ArrowLeft,
  ArrowRight,
  Check,
  CheckCheck,
  Clock3,
  Database,
  FileCheck2,
  Info,
  LockKeyhole,
  Plus,
  Radio,
  SlidersHorizontal,
} from 'lucide-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api, ApiError } from '../shared/api';
import {
  initialConfig,
  lines,
  number,
  platformName,
  platformDescription,
  reviewUrls,
  platforms,
  queryLines,
  validateConfig,
} from '../shared/domain';
import type { Config, FieldError, Plan, Platform, PlatformConfig } from '../shared/types';
import { Button, Errors, Field, Notice, PlatformMark, Stepper, UnsavedGuard } from '../shared/ui';
import { FieldErrorsContext, useApp } from '../shared/context';
import History from './History';

export function ConfigFields({
  config: c,
  change,
  advancedOnly = false,
}: {
  config: Config;
  change: (config: Config) => void;
  advancedOnly?: boolean;
}) {
  const field = <K extends keyof Config>(key: K, value: Config[K]) =>
    change({ ...c, [key]: value });
  const platform = (p: Platform, key: keyof PlatformConfig, value: number) =>
    change({ ...c, platforms: { ...c.platforms, [p]: { ...c.platforms[p], [key]: value } } });
  return (
    <>
      {!advancedOnly && (
        <>
          <div className="form-section-title">
            <h3>Rentang tanggal konten</h3>
            <p>Waktu pengambilan dicatat terpisah dari tanggal konten.</p>
          </div>
          <div className="form-grid">
            <Field name="dates" label="Mulai pada (WIB)" required>
              {(id) => (
                <input
                  id={id}
                  type="datetime-local"
                  value={c.since}
                  onChange={(e) => field('since', e.target.value)}
                />
              )}
            </Field>
            <Field
              name="dates"
              label="Sampai sebelum (WIB)"
              required
              hint="Batas akhir tidak termasuk dalam rentang."
            >
              {(id) => (
                <input
                  id={id}
                  type="datetime-local"
                  value={c.until}
                  onChange={(e) => field('until', e.target.value)}
                />
              )}
            </Field>
          </div>
          <div className="form-grid">
            <Field
              label="Keyword disertakan"
              hint="Satu kata/frasa per baris. Diterapkan pada judul/deskripsi post."
            >
              {(id) => (
                <textarea
                  id={id}
                  rows={3}
                  value={c.include}
                  onChange={(e) => field('include', e.target.value)}
                />
              )}
            </Field>
            <Field
              label="Keyword dikecualikan"
              hint="Exclude mengalahkan include; root yang ditolak mengeluarkan thread."
            >
              {(id) => (
                <textarea
                  id={id}
                  rows={3}
                  value={c.exclude}
                  onChange={(e) => field('exclude', e.target.value)}
                />
              )}
            </Field>
          </div>
          <Field label="Kecocokan keyword include">
            {(id) => (
              <select
                id={id}
                value={c.includeMode}
                onChange={(e) => field('includeMode', e.target.value as Config['includeMode'])}
              >
                <option value="any">Salah satu keyword</option>
                <option value="all">Semua keyword</option>
              </select>
            )}
          </Field>
          <div className="form-section-title">
            <h3>Target dan batas akuisisi</h3>
            <p>Post memenuhi kriteria setelah minimum komentar unik termasuk reply tercapai.</p>
          </div>
          <div className="target-grid">
            {platforms
              .filter((p) => c.platforms[p].enabled)
              .map((p) => (
                <div className="target-block" key={p}>
                  <h4>
                    <PlatformMark platform={p} />
                    {platformName(p)}
                  </h4>
                  <div className="form-grid">
                    <Field name={`${p}.target`} label="Target post memenuhi kriteria" required>
                      {(id) => (
                        <input
                          id={id}
                          type="number"
                          min={c.mode === 'automatic' ? 1 : 0}
                          value={c.platforms[p].target}
                          onChange={(e) => platform(p, 'target', +e.target.value)}
                        />
                      )}
                    </Field>
                    <Field name={`${p}.minComments`} label="Minimum komentar unik/post" required>
                      {(id) => (
                        <input
                          id={id}
                          type="number"
                          min={0}
                          value={c.platforms[p].minComments}
                          onChange={(e) => platform(p, 'minComments', +e.target.value)}
                        />
                      )}
                    </Field>
                  </div>
                </div>
              ))}
          </div>
        </>
      )}
      <div className="form-grid">
        <Field
          name="duration"
          label="Batas waktu akuisisi (jam)"
          required
          hint="Waktu tunggu CAPTCHA/429 ikut dihitung sejak worker mulai."
        >
          {(id) => (
            <input
              id={id}
              type="number"
              min={0.001}
              max={24}
              step="any"
              value={c.duration / 3600}
              onChange={(e) => field('duration', Math.round(+e.target.value * 3600))}
            />
          )}
        </Field>
        <div className="field side-explanation">
          <Clock3 size={19} />
          <p>
            Target adalah tujuan pengumpulan. Hasil dapat parsial karena akses, waktu, atau
            ketersediaan konten.
          </p>
        </div>
      </div>
      <details className="advanced">
        <summary>
          <SlidersHorizontal size={17} /> Pengaturan lanjut
        </summary>
        <div className="form-grid three">
          {(
            [
              ['delay', 'Jeda request (detik)'],
              ['timeout', 'Timeout request (detik)'],
              ['cooldown', 'Cooldown 429 awal (detik)'],
              ['retries', 'Maksimum retry 429'],
              ['captchaWait', 'Tunggu CAPTCHA (detik)'],
              ['captchaPoll', 'Interval periksa CAPTCHA (detik)'],
            ] as const
          ).map(([k, label]) => (
            <Field key={k} name={k} label={label}>
              {(id) => (
                <input
                  id={id}
                  type="number"
                  min={0}
                  value={c[k]}
                  onChange={(e) => field(k, +e.target.value)}
                />
              )}
            </Field>
          ))}
        </div>
        {platforms
          .filter((p) => c.platforms[p].enabled)
          .map((p) => (
            <div key={p}>
              <h4>{platformName(p)}</h4>
              <div className="form-grid three">
                {(
                  [
                    ['maxPosts', 'Batas percobaan post'],
                    ['maxCandidates', 'Batas kandidat'],
                    ['maxComments', 'Batas komentar/post'],
                    ['maxReplies', 'Batas reply'],
                    ['maxRepliesPerThread', 'Batas reply/thread'],
                  ] as const
                ).map(([k, label]) => (
                  <Field name={`${p}.${k}`} label={label} key={k}>
                    {(id) => (
                      <input
                        id={id}
                        type="number"
                        min={0}
                        value={c.platforms[p][k]}
                        onChange={(e) => platform(p, k, +e.target.value)}
                      />
                    )}
                  </Field>
                ))}
              </div>
            </div>
          ))}
        <p className="muted">
          Retry-After server yang lebih lama dari cooldown akan dihormati. Eksekusi memakai round
          robin dengan satu deadline bersama.
        </p>
      </details>
    </>
  );
}
export function Baselines({ config, change }: { config: Config; change: (c: Config) => void }) {
  const { cap } = useApp();
  return (
    <>
      <div className="form-section-title">
        <h3>Lewati data yang sudah dimiliki</h3>
        <p>Native ID dan URL kanonik dibandingkan sebelum pengambilan dan sebelum ekspor.</p>
      </div>
      {cap.baselines.map((b) => (
        <label className="baseline-option" key={b.id}>
          <input
            type="checkbox"
            checked={config.baselines.includes(b.id)}
            disabled={b.required}
            onChange={(e) =>
              change({
                ...config,
                baselines: e.target.checked
                  ? [...config.baselines, b.id]
                  : config.baselines.filter((id) => id !== b.id),
              })
            }
          />
          <Database size={23} />
          <span>
            <strong>{b.name}</strong>
            <small>
              Versi {b.version} · {number(b.roots)} ID post ·{' '}
              {b.ready ? 'Indeks tersedia' : 'Indeks belum tersedia'}
            </small>
          </span>
          <span className="required-tag">{b.required ? 'Wajib' : 'Opsional'}</span>
        </label>
      ))}
      {cap.baselines.some((b) => b.required && !b.ready) && (
        <Notice tone="error">Baseline wajib belum siap. Pekerjaan tidak dapat dimulai.</Notice>
      )}
      <div className="subtle-note">
        <LockKeyhole size={16} />
        Dataset asal tetap utuh. Hasil selalu diterbitkan sebagai versi baru.
      </div>
    </>
  );
}
export function ConfigReview({ config: c }: { config: Config }) {
  const { cap } = useApp();
  return (
    <div className="review-content">
      <div className="review-name">
        <FileCheck2 size={24} />
        <div>
          <h3>{c.name || 'Pekerjaan tanpa nama'}</h3>
          <p>
            {c.mode === 'url'
              ? `${c.urls.length} URL pilihan; tanpa pencarian tambahan`
              : 'Penemuan dan pengambilan otomatis'}
          </p>
        </div>
      </div>
      <dl className="review-dl">
        <div>
          <dt>Durasi maksimum</dt>
          <dd>{c.duration / 3600} jam, sejak worker mulai</dd>
        </div>
        <div>
          <dt>Filter tanggal</dt>
          <dd>
            {c.filtersEnabled
              ? `${c.since.replace('T', ' ')} ≤ waktu < ${c.until.replace('T', ' ')} WIB`
              : 'Tidak aktif'}
          </dd>
        </div>
        <div>
          <dt>Keyword</dt>
          <dd>
            {c.filtersEnabled
              ? `${lines(c.include).length} include / ${lines(c.exclude).length} exclude; ${c.includeMode === 'any' ? 'salah satu' : 'semua'}`
              : 'Tidak aktif'}
          </dd>
        </div>
        <div>
          <dt>Pengecualian</dt>
          <dd>{c.baselines.join(', ') || 'Tanpa baseline opsional'}</dd>
        </div>
        {platforms
          .filter((p) => c.platforms[p].enabled)
          .map((p) => (
            <div key={p}>
              <dt>{platformName(p)}</dt>
              <dd>
                {c.mode === 'automatic'
                  ? `${number(c.platforms[p].target)} post memenuhi kriteria, ${queryLines(c.platforms[p].queries).length} query`
                  : `${c.urls.filter((u) => reviewUrls([u])[0].platform === p).length} URL`}
                <small>
                  Minimum {c.platforms[p].minComments} komentar unik/post; maksimum{' '}
                  {c.platforms[p].maxComments} komentar.
                </small>
              </dd>
            </div>
          ))}
      </dl>
      {c.platforms.reddit.enabled && !cap.verificationAvailable && (
        <Notice tone="warning">
          Sesi browser worker belum tersedia pada lingkungan ini. Penanganan CAPTCHA memerlukan
          koneksi sesi worker yang sesuai.
        </Notice>
      )}
    </div>
  );
}

export default function Automatic() {
  const now = useClock();
  const [params] = useSearchParams();
  const history = params.get('view') === 'history';
  const location = useLocation();
  const navigate = useNavigate();
  const client = useQueryClient();
  const { cap, session } = useApp();
  const [config, setConfig] = useState<Config>(() =>
    location.state?.config
      ? {
          ...location.state.config,
          name: `Salinan ${location.state.config.name}`,
          mode: 'automatic',
        }
      : initialConfig(),
  );
  const [step, setStep] = useState(0),
    [errors, setErrors] = useState<FieldError[]>([]),
    [plan, setPlan] = useState<Plan | null>(null),
    [dirty, setDirty] = useState(false),
    [key, setKey] = useState(() => crypto.randomUUID());
  const revision = useRef(0);
  const change = (c: Config) => {
    revision.current++;
    setConfig(c);
    setPlan(null);
    setErrors([]);
    setDirty(true);
    setKey(crypto.randomUUID());
  };
  const validate = useMutation({
    mutationFn: (request: { config: Config; revision: number }) => api.validate(request.config),
    onSuccess: (result, request) => {
      if (request.revision === revision.current) setPlan(result);
    },
    onError: (e) =>
      setErrors(
        e instanceof ApiError && e.fields.length
          ? e.fields
          : [{ field: 'server', message: e.message }],
      ),
  });
  const start = useMutation({
    mutationFn: () => api.start(plan!, key),
    onSuccess: (job) => {
      flushSync(() => setDirty(false));
      client.setQueryData(['job', job.id], job);
      void client.invalidateQueries({ queryKey: ['jobs'] });
      navigate(`/crawler/automatic/jobs/${job.id}`);
    },
    onError: (e) => setErrors([{ field: 'server', message: e.message }]),
  });
  const next = () => {
    if (step === 3) {
      const errs = validateConfig(config, cap);
      setErrors(errs);
      if (!errs.length) validate.mutate({ config: config, revision: revision.current });
    } else {
      const all = validateConfig(config, cap);
      const sourceFields = [
        'name',
        'platforms',
        ...platforms.map((p) => `${p}.queries`),
        'subreddit',
      ];
      const current = all.filter((e) =>
        step === 0
          ? sourceFields.includes(e.field)
          : step === 2
            ? e.field === 'baselines'
            : !sourceFields.includes(e.field) && e.field !== 'baselines',
      );
      setErrors(current);
      if (!current.length) {
        setStep(step + 1);
        document.querySelector<HTMLElement>('.wizard-panel')?.scrollIntoView({ block: 'start' });
      }
    }
  };
  const totalTarget = platforms
    .filter((p) => config.platforms[p].enabled)
    .reduce((n, p) => n + config.platforms[p].target, 0);
  return (
    <>
      <UnsavedGuard dirty={dirty && !start.isSuccess && !start.isPending} />
      <div className="page-heading">
        <div>
          <span className="section-kicker">
            <Radio size={16} />
            Akuisisi berbasis pencarian
          </span>
          <h1 id="main-title" tabIndex={-1}>
            Crawler otomatis
          </h1>
          <p>Temukan percakapan yang relevan. Kumpulkan dengan konteks yang utuh.</p>
        </div>
        <div className="page-heading-note">
          <ShieldHint />
        </div>
      </div>
      <div className="page-tabs">
        <Link className={!history ? 'active' : ''} to="/crawler/automatic">
          <Plus size={16} />
          Konfigurasi baru
        </Link>
        <Link className={history ? 'active' : ''} to="/crawler/automatic?view=history">
          <Clock3 size={16} />
          Riwayat pekerjaan
        </Link>
      </div>
      {history ? (
        <History />
      ) : session.role !== 'operator' ? (
        <Notice>
          Anda berada dalam mode pengamat. Buka Riwayat pekerjaan untuk memantau akuisisi yang
          tersedia.
        </Notice>
      ) : (
        <div className="configuration-layout">
          <section className="panel wizard-panel">
            <Stepper
              steps={['Sumber', 'Filter & target', 'Pengecualian', 'Tinjau']}
              active={step}
            />
            <FieldErrorsContext.Provider value={errors}>
              <div className="wizard-content">
                <Errors errors={errors} />
                {step === 0 && (
                  <>
                    <div className="form-section-title first">
                      <h2>Mulai dari sumber yang tepat</h2>
                      <p>Pilih platform dan tentukan percakapan yang ingin ditemukan.</p>
                    </div>
                    <Field
                      name="name"
                      label="Nama pekerjaan"
                      required
                      hint="Nama yang membantu Anda mengenali riset ini nanti."
                    >
                      {(id) => (
                        <input
                          id={id}
                          maxLength={120}
                          placeholder="Contoh: Minat jurusan & beasiswa 2026"
                          value={config.name}
                          onChange={(e) => change({ ...config, name: e.target.value })}
                        />
                      )}
                    </Field>
                    <div className="source-grid">
                      {platforms.map((p) => (
                        <label
                          key={p}
                          className={`source-option ${config.platforms[p].enabled ? 'selected' : ''}`}
                        >
                          <PlatformMark platform={p} />
                          <span>
                            <b>{platformName(p)}</b>
                            <small>
                              {platformDescription[p]}
                              {!cap.platforms.includes(p) && ' · Adapter backend belum tersedia'}
                            </small>
                          </span>
                          <input
                            type="checkbox"
                            disabled={!cap.platforms.includes(p)}
                            checked={config.platforms[p].enabled}
                            onChange={(e) =>
                              change({
                                ...config,
                                platforms: {
                                  ...config.platforms,
                                  [p]: { ...config.platforms[p], enabled: e.target.checked },
                                },
                              })
                            }
                          />
                        </label>
                      ))}
                    </div>
                    <div className="form-grid">
                      {platforms
                        .filter((p) => config.platforms[p].enabled)
                        .map((p) => (
                          <Field
                            key={p}
                            name={`${p}.queries`}
                            label={`Query ${platformName(p)}`}
                            required
                            hint="Satu query per baris, maksimal 100 query."
                          >
                            {(id) => (
                              <textarea
                                id={id}
                                rows={4}
                                value={config.platforms[p].queries}
                                onChange={(e) =>
                                  change({
                                    ...config,
                                    platforms: {
                                      ...config.platforms,
                                      [p]: { ...config.platforms[p], queries: e.target.value },
                                    },
                                  })
                                }
                              />
                            )}
                          </Field>
                        ))}
                    </div>
                    {config.platforms.reddit.enabled && (
                      <Field
                        name="subreddit"
                        label="Subreddit"
                        hint="Pisahkan dengan koma, tanpa r/."
                      >
                        {(id) => (
                          <input
                            id={id}
                            value={config.subreddit}
                            onChange={(e) => change({ ...config, subreddit: e.target.value })}
                          />
                        )}
                      </Field>
                    )}
                    <Field label="Catatan riset (opsional)">
                      {(id) => (
                        <input
                          id={id}
                          maxLength={500}
                          placeholder="Tujuan atau konteks pengumpulan"
                          value={config.description}
                          onChange={(e) => change({ ...config, description: e.target.value })}
                        />
                      )}
                    </Field>
                  </>
                )}
                {step === 1 && <ConfigFields config={config} change={change} />}
                {step === 2 && <Baselines config={config} change={change} />}
                {step === 3 && <ConfigReview config={config} />}
                {plan && (
                  <Notice tone="success">
                    <strong>Rencana valid, siap dimulai.</strong>
                    {plan.warnings.map((w) => (
                      <p key={w}>{w}</p>
                    ))}
                  </Notice>
                )}
              </div>
            </FieldErrorsContext.Provider>
            <div className="wizard-footer">
              <span className="wizard-footnote">
                <LockKeyhole size={14} />
                {step === 3
                  ? 'Validasi belum menjalankan crawling'
                  : 'Konfigurasi dapat ditinjau sebelum mulai'}
              </span>
              <div>
                {step > 0 && (
                  <Button
                    variant="secondary"
                    onClick={() => {
                      setStep(step - 1);
                      setPlan(null);
                    }}
                  >
                    <ArrowLeft size={16} />
                    Kembali
                  </Button>
                )}
                {step === 3 && plan && Date.parse(plan.expiresAt) > now ? (
                  <Button
                    loading={start.isPending}
                    onClick={() => start.mutate()}
                    disabled={Date.parse(plan.expiresAt) <= now}
                  >
                    <Check size={17} />
                    Mulai akuisisi
                  </Button>
                ) : (
                  <Button loading={validate.isPending} onClick={next}>
                    {step === 3 ? 'Validasi rencana' : 'Lanjutkan'}
                    <ArrowRight size={16} />
                  </Button>
                )}
              </div>
            </div>
          </section>
          <aside className="plan-aside">
            <div className="plan-summary">
              <span className="summary-icon">
                <Database size={22} />
              </span>
              <h2>Rencana akuisisi</h2>
              <p>Satu riset, sumber yang terhubung.</p>
              <div className="plan-stat">
                <span>Target total</span>
                <b>
                  {number(totalTarget)}
                  <small> post memenuhi kriteria</small>
                </b>
              </div>
              <div className="plan-source-list">
                {platforms
                  .filter((p) => config.platforms[p].enabled)
                  .map((p) => (
                    <div key={p}>
                      <span>
                        <PlatformMark platform={p} />
                        {platformName(p)}
                      </span>
                      <b>{number(config.platforms[p].target)}</b>
                    </div>
                  ))}
              </div>
              <div className="plan-metadata">
                <span>
                  <Clock3 size={16} />
                  Batas waktu
                </span>
                <b>{config.duration / 3600} jam</b>
              </div>
              <div className="plan-metadata">
                <span>
                  <CheckCheck size={16} />
                  Deduplikasi
                </span>
                <b>{config.baselines.length} dataset</b>
              </div>
              <div className="plan-note">
                <Info size={16} />
                <p>
                  Target bukan jaminan hasil. Waktu, akses platform, dan kualitas diskusi
                  memengaruhi akuisisi.
                </p>
              </div>
            </div>
            <div className="context-note">
              <h3>Konteks ikut terkumpul</h3>
              <p>
                Post, komentar, dan reply dipisahkan agar asal setiap percakapan dapat ditelusuri.
              </p>
              <span className="context-link">
                <FileCheck2 size={16} />
                Versi baru untuk setiap hasil
              </span>
            </div>
          </aside>
        </div>
      )}
    </>
  );
}
function ShieldHint() {
  return (
    <span>
      <LockKeyhole size={15} />
      Dataset sumber tetap terjaga
    </span>
  );
}
