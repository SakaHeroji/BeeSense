import { flushSync } from 'react-dom';
import { useRef, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Clock3, Database, FolderOpen, Play, Settings2, SlidersHorizontal } from 'lucide-react';
import { api, ApiError } from '../shared/api';
import { FieldErrorsContext, useApp } from '../shared/context';
import {
  dateTime,
  demoMode,
  applyConversation,
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
import { TikTokChromePreparation, TikTokWorkflow } from './TikTokConnector';
import { ConversationPicker } from '../shared/ConversationPicker';

export default function PlatformWorkspace() {
  const { platform = 'youtube' } = useParams();
  if (!platforms.includes(platform as Platform)) return <Navigate to="/crawler/youtube" replace />;
  return <PlatformPage key={platform} platform={platform as Platform} />;
}

function PlatformPage({ platform }: { platform: Platform }) {
  const { cap, session, notify } = useApp();
  const [view] = useUrlState('view', 'config');
  const [config, setConfig] = useState(() => initialConfig('automatic', platform));
  const [dirty, setDirty] = useState(false);
  const [credentials, setCredentials] = useState<AuthInput>({ username: '', sessionid: '' });
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [key, setKey] = useState(() => crypto.randomUUID());
  const revision = useRef(0);
  const now = useClock();
  const client = useQueryClient();
  const navigate = useNavigate();
  const conversations = useQuery({ queryKey: ['conversations'], queryFn: api.conversations });
  const selectedConversation = conversations.data?.find(
    (conversation) => conversation.id === config.conversation?.id,
  );
  const conversationSnapshot = selectedConversation || config.conversation;
  const isTikTok = platform === 'tiktok';
  const supported =
    cap.platforms.includes(platform) && (!isTikTok || cap.tiktokConnectorAvailable === true);
  const backendAvailable = ['youtube', 'reddit', 'instagram', 'x', 'tiktok'].includes(platform);
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
    if (!config.conversation) {
      setErrors([{ field: 'conversation', message: 'Pilih conversation sebelum mulai crawling.' }]);
      requestAnimationFrame(() => document.getElementsByName('conversation')[0]?.focus());
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
            <p>
              {isTikTok
                ? 'Crawling melalui plugin Chrome. Pengaturan, koneksi, dan hasil dalam satu transaksi.'
                : `${platformDescription[platform]}. Konfigurasi dan hasil dalam satu tempat.`}
            </p>
          </div>
        </div>
        <span className={`source-readiness ${backendAvailable ? 'available' : ''}`}>
          <span />
          {isTikTok ? 'Plugin Chrome' : backendAvailable ? 'Siap dikonfigurasi' : 'Segera tersedia'}
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
          {isTikTok && <TikTokWorkflow />}
          {isTikTok && !cap.tiktokConnectorAvailable && (
            <Notice>
              Server dashboard belum mengaktifkan penghubung plugin TikTok. Konfigurasi tetap dapat
              dilihat; pembuatan koneksi tersedia setelah layanan di server yang sama diaktifkan.
            </Notice>
          )}
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
              <form
                className={`social-config-layout ${isTikTok ? 'tiktok-config' : ''}`}
                onSubmit={submit}
                noValidate
              >
                <section className="panel social-form">
                  <div className="social-section-heading">
                    <div>
                      <span className="step-kicker">2 dari 2</span>
                      <h2>Atur eksekusi {platformName(platform)}</h2>
                      <p>
                        Konteks riset berasal dari conversation. Di sini Anda hanya mengatur cara
                        platform ini dijalankan.
                      </p>
                    </div>
                    <SlidersHorizontal size={21} aria-hidden="true" />
                  </div>
                  <Errors errors={errors} />
                  {conversationSnapshot ? (
                    <div className="platform-conversation-plan">
                      <dl>
                        <div>
                          <dt>Conversation</dt>
                          <dd>{conversationSnapshot.title}</dd>
                        </div>
                        <div>
                          <dt>Metode discovery</dt>
                          <dd>
                            {platform === 'instagram'
                              ? 'Hashtag conversation'
                              : isTikTok
                                ? 'Query & hashtag conversation'
                                : platform === 'reddit'
                                  ? 'Query conversation & subreddit'
                                  : 'Query conversation'}
                          </dd>
                        </div>
                        <div>
                          <dt>Relevansi</dt>
                          <dd>
                            Threshold {number(conversationSnapshot.relevance.threshold * 100)}%
                          </dd>
                        </div>
                        <div>
                          <dt>Versi snapshot</dt>
                          <dd>v{conversationSnapshot.version}</dd>
                        </div>
                      </dl>
                      <Notice>
                        Perubahan pada conversation setelah pekerjaan dimulai tidak mengubah
                        snapshot pekerjaan ini. Buat pekerjaan baru untuk memakai versi terbaru.
                      </Notice>
                    </div>
                  ) : (
                    <div className="conversation-required-state">
                      <h3>Pilih conversation untuk melanjutkan</h3>
                      <p>
                        Semua keyword, query, dan aturan relevansi dikelola dari menu Conversation.
                        Rentang publikasi dipilih pada transaksi crawling ini.
                      </p>
                    </div>
                  )}
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
                </section>
                <aside className="social-controls">
                  {isTikTok && <TikTokChromePreparation />}
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
                        hint={
                          isTikTok
                            ? 'Dimulai setelah plugin terhubung; termasuk jeda dan validasi selama crawling.'
                            : 'Termasuk waktu tunggu selama pengambilan.'
                        }
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
                  {!isTikTok && (
                    <AuthSettings
                      platform={platform}
                      value={credentials}
                      change={(value) => {
                        setCredentials(value);
                      }}
                    />
                  )}
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
                      {isTikTok ? 'Tinjau & siapkan koneksi Chrome' : 'Tinjau & mulai crawling'}
                    </Button>
                    <p>
                      {isTikTok
                        ? 'Setelah ditinjau, pairing dan progres tampil dalam transaksi yang sama.'
                        : 'Konfigurasi ditinjau sekali lagi sebelum proses dimulai.'}
                    </p>
                  </div>
                </aside>
              </form>
            </FieldErrorsContext.Provider>
          )}
          <Dialog
            open={!!plan}
            title={
              isTikTok
                ? 'Siapkan crawling TikTok melalui Chrome?'
                : `Mulai crawling ${platformName(platform)}?`
            }
            onClose={() => !start.isPending && setPlan(null)}
          >
            <dl className="start-summary">
              <dt>Conversation</dt>
              <dd>{config.name}</dd>
              <dt>Snapshot</dt>
              <dd>v{config.conversation?.version || '—'} · eksekusi satu platform</dd>
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
            {isTikTok && (
              <Notice>
                Transaksi akan menunggu koneksi plugin. Waktu crawling baru dihitung setelah server
                memverifikasi konektor; tidak perlu menjalankan server penghubung lain.
              </Notice>
            )}
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
                {isTikTok
                  ? demoMode
                    ? 'Siapkan koneksi simulasi'
                    : 'Siapkan koneksi Chrome'
                  : demoMode
                    ? 'Mulai simulasi'
                    : 'Mulai crawling'}
              </Button>
            </div>
          </Dialog>
        </>
      )}
    </>
  );
}
