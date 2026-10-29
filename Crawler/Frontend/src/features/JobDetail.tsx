import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeft,
  ArrowUpRight,
  Clock3,
  Copy,
  Hourglass,
  PauseCircle,
  Radio,
  ShieldAlert,
} from 'lucide-react';
import { api } from '../shared/api';
import { useUrlState } from '../shared/hooks';
import {
  dateTime,
  demoMode,
  duration,
  number,
  platformName,
  platformChartColors,
  safeExternal,
} from '../shared/domain';
import type { Job, Platform, PlatformProgress } from '../shared/types';
import { Badge, Button, Dialog, Empty, Notice, PlatformMark, Spinner } from '../shared/ui';
import { useApp } from '../shared/context';
import { ConfigReview } from './Automatic';
import DatasetView from './DatasetView';

const liveStates = ['QUEUED', 'RUNNING', 'STOP_REQUESTED', 'FINALIZING'];
export default function JobDetail() {
  const { jobId = '' } = useParams();
  const client = useQueryClient();
  const { session, notify } = useApp();
  const navigate = useNavigate();
  const [tab, setTab] = useUrlState('panel', 'progress');
  const [verificationResult, setVerificationResult] = useState<{
    url?: string;
    message: string;
  } | null>(null);
  const [stopDialog, setStopDialog] = useState(false),
    [now, setNow] = useState(() => Date.now()),
    [online, setOnline] = useState(navigator.onLine),
    [eventFilter, setEventFilter] = useState('');
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 1000);
    const update = () => setOnline(navigator.onLine);
    window.addEventListener('online', update);
    window.addEventListener('offline', update);
    return () => {
      clearInterval(timer);
      window.removeEventListener('online', update);
      window.removeEventListener('offline', update);
    };
  }, []);
  const query = useQuery({
    queryKey: ['job', jobId],
    queryFn: async () => {
      const snapshot = await api.job(jobId);
      const previous = client.getQueryData<Job>(['job', jobId]);
      return previous && previous.snapshotVersion > snapshot.snapshotVersion ? previous : snapshot;
    },
    refetchInterval: (q) =>
      !q.state.data || liveStates.includes(q.state.data.status) ? (demoMode ? 1000 : 5000) : false,
    staleTime: 0,
  });
  const stop = useMutation({
    mutationFn: () => api.stop(jobId),
    onSuccess: (j) => {
      client.setQueryData(['job', jobId], j);
      setStopDialog(false);
      notify('Permintaan berhenti diterima. Hasil yang tersedia akan difinalisasi.');
    },
    onError: (e) => notify(e.message),
  });
  const scenario = useMutation({
    mutationFn: (s: string) => api.demoScenario!(jobId, s),
    onSuccess: (j) => {
      client.setQueryData(['job', jobId], j);
      void query.refetch();
    },
    onError: (e) => notify(e.message),
  });
  const verification = useMutation({
    mutationFn: () => api.verification(jobId),
    onSuccess: (result) => {
      setVerificationResult({ ...result, url: result.url ? safeExternal(result.url) : undefined });
    },
    onError: (e) => notify(e.message),
  });
  if (query.isPending)
    return (
      <div className="loading-page">
        <Spinner />
        Memuat pekerjaan…
      </div>
    );
  if (!query.data)
    return (
      <>
        <h1 id="main-title">Pekerjaan belum dapat dibuka</h1>
        <Notice tone="error">{query.error?.message}</Notice>
        <Button onClick={() => void query.refetch()}>Coba lagi</Button>
      </>
    );
  const job = query.data;
  const live = liveStates.includes(job.status);
  const manual = job.mode !== 'automatic';
  const stale = live && (!online || !!query.error || now - Date.parse(job.updatedAt) > 20000);
  const counts = job.platforms.reduce(
    (acc, p) => ({
      roots: acc.roots + p.counts.roots,
      comments: acc.comments + p.counts.comments,
      replies: acc.replies + p.counts.replies,
      duplicates: acc.duplicates + p.counts.duplicates,
      rejected: acc.rejected + p.counts.rejected,
    }),
    { roots: 0, comments: 0, replies: 0, duplicates: 0, rejected: 0 },
  );
  return (
    <>
      <Link
        className="back-link"
        to={`/crawler/${manual ? 'manual?tab=history' : 'automatic?view=history'}`}
      >
        <ArrowLeft size={15} />
        Riwayat {manual ? 'manual' : 'otomatis'}
      </Link>
      <div className="page-heading job-heading">
        <div>
          <span className="section-kicker">
            <Radio size={16} />
            {job.mode === 'survey'
              ? 'Data survei'
              : job.mode === 'url'
                ? 'Akuisisi URL pilihan'
                : 'Akuisisi otomatis'}
          </span>
          <h1 id="main-title" tabIndex={-1}>
            {job.name}
          </h1>
          <p className="job-id">{job.id}</p>
        </div>
        <div className="job-heading-actions">
          <Badge status={job.status} />
          {session.role === 'operator' && job.canStop && (
            <Button variant="secondary" onClick={() => setStopDialog(true)}>
              <PauseCircle size={16} />
              Hentikan akuisisi
            </Button>
          )}
        </div>
      </div>
      <div className="job-timeline">
        <span>
          <Clock3 size={16} />
          <b>Mulai</b> {dateTime(job.startedAt)}
        </span>
        <span>
          <Hourglass size={16} />
          <b>Deadline</b> {job.deadlineAt ? dateTime(job.deadlineAt) : 'Menunggu worker'}
        </span>
        {live && job.deadlineAt && (
          <span className="time-remaining">
            <b>Sisa waktu</b> {duration((Date.parse(job.deadlineAt) - now) / 1000)}
          </span>
        )}
        <span className="last-update">Pembaruan {dateTime(job.updatedAt)}</span>
      </div>
      <div aria-live="polite" aria-atomic="true" className="job-status-notices">
        {stale && (
          <Notice tone="warning">
            <b>Status belum diperbarui.</b> Data terakhir dipertahankan; worker mungkin masih
            berjalan.{' '}
            <button className="text-button" onClick={() => void query.refetch()}>
              Sambungkan kembali
            </button>
          </Notice>
        )}
        {job.status === 'FINALIZING' && (
          <Notice>
            Akuisisi berakhir. Berkas sedang disusun dan divalidasi; unduhan tersedia setelah
            diterbitkan.
          </Notice>
        )}
        {job.reason && (
          <Notice tone={job.status === 'FAILED' ? 'error' : 'warning'}>{job.reason}</Notice>
        )}
      </div>
      {!!job.platforms.length && (
        <div className="platform-progress-grid">
          {job.platforms.map((p) => (
            <PlatformCard
              key={p.platform}
              p={p}
              job={job}
              now={now}
              onVerification={() => verification.mutate()}
              loading={verification.isPending}
            />
          ))}
        </div>
      )}
      {demoMode && live && session.role === 'operator' && (
        <details className="simulation-tools">
          <summary>Uji skenario simulasi</summary>
          <p>
            Tidak memengaruhi platform sesungguhnya. Hambatan disimulasikan sampai dipilih Normal
            atau pekerjaan dihentikan.
          </p>
          <div className="button-row">
            {[
              ['', 'Normal'],
              ['captcha', 'CAPTCHA Reddit'],
              ['429', 'HTTP 429 Reddit'],
              ['export-error', 'Gagal ekspor'],
            ].map(([value, label]) => (
              <Button
                key={label}
                variant="secondary"
                disabled={scenario.isPending}
                onClick={() => scenario.mutate(value)}
              >
                {label}
              </Button>
            ))}
          </div>
        </details>
      )}
      <div className="page-tabs">
        {[
          ['progress', 'Progres'],
          ['activity', 'Aktivitas'],
          ['configuration', 'Konfigurasi'],
          ['result', 'Hasil dataset'],
        ].map(([id, label]) => (
          <Link key={id} className={tab === id ? 'active' : ''} to={{ search: `?panel=${id}` }}>
            {label}
            {id === 'result' && job.dataset && <span className="tab-dot" />}
          </Link>
        ))}
      </div>
      {tab === 'progress' &&
        (job.mode === 'survey' ? (
          <section className="panel padded">
            <h2>Respons tersimpan</h2>
            <div className="review-counts">
              <span>
                <b>{job.dataset?.responses || 0}</b> respons valid
              </span>
              <span>
                <b>{job.dataset?.rows || 0}</b> jawaban
              </span>
              <span>
                <b>{job.dataset?.textRows || 0}</b> jawaban teks
              </span>
            </div>
            <p>Pertanyaan dan peran responden tetap terpisah dari teks jawaban.</p>
            <Button onClick={() => setTab('result')}>
              Periksa dataset
              <ArrowUpRight size={16} />
            </Button>
          </section>
        ) : (
          <>
            <ProgressChart job={job} />
            <div className="chart-grid">
              <Composition
                title="Komposisi konten terkumpul"
                values={[
                  ['Post', counts.roots],
                  ['Komentar', counts.comments],
                  ['Reply', counts.replies],
                ]}
              />
              <Composition
                title="Data yang dilewati"
                values={[
                  ['Duplikat', counts.duplicates],
                  ['Ditolak filter/akses', counts.rejected],
                ]}
              />
            </div>
          </>
        ))}
      {tab === 'activity' && (
        <section className="panel padded">
          <div className="panel-heading">
            <div>
              <h2>Jejak aktivitas</h2>
              <p>Perubahan penting dan alasan pada setiap langkah.</p>
            </div>
            <select
              aria-label="Filter platform aktivitas"
              value={eventFilter}
              onChange={(e) => setEventFilter(e.target.value)}
            >
              <option value="">Semua platform</option>
              {job.platforms.map((p) => (
                <option value={p.platform} key={p.platform}>
                  {platformName(p.platform)}
                </option>
              ))}
            </select>
          </div>
          <ol className="event-list">
            {job.events
              .filter((e) => !eventFilter || e.platform === eventFilter)
              .map((e) => (
                <li key={e.id}>
                  <span className="event-dot" />
                  <time>{dateTime(e.at)}</time>
                  <p>
                    {e.platform && <b>{platformName(e.platform)}: </b>}
                    {e.message}
                  </p>
                </li>
              ))}
          </ol>
          {!job.events.filter((e) => !eventFilter || e.platform === eventFilter).length && (
            <Empty title="Belum ada event untuk filter ini" />
          )}
        </section>
      )}
      {tab === 'configuration' && (
        <section className="panel padded">
          {job.config ? (
            <>
              <ConfigReview config={job.config} />
              {session.role === 'operator' && (
                <div className="form-actions">
                  <Button
                    variant="secondary"
                    onClick={() =>
                      navigate(`/crawler/${manual ? 'manual?tab=url' : 'automatic'}`, {
                        state: { config: job.config },
                      })
                    }
                  >
                    <Copy size={16} />
                    Buat pekerjaan baru dari konfigurasi
                  </Button>
                </div>
              )}
            </>
          ) : (
            <>
              <h2>Batch survei</h2>
              <p>
                Template minat-studi versi 1. Jawaban tidak dimasukkan ke konfigurasi pekerjaan atau
                browser storage.
              </p>
            </>
          )}
        </section>
      )}
      {tab === 'result' &&
        (job.dataset ? (
          <DatasetView job={job} />
        ) : (
          <section className="panel">
            <Empty
              title={
                job.status === 'FAILED'
                  ? 'Dataset belum dapat diterbitkan'
                  : 'Hasil final belum tersedia'
              }
            >
              Unduhan muncul sesudah ekspor dan pemeriksaan manifest berhasil.
            </Empty>
          </section>
        ))}
      <Dialog
        open={!!verificationResult}
        onClose={() => setVerificationResult(null)}
        title="Sesi browser worker"
      >
        <p>{verificationResult?.message}</p>
        {verificationResult?.url && (
          <a
            className="button primary"
            href={verificationResult.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            Buka sesi verifikasi
            <ArrowUpRight size={16} />
          </a>
        )}
        <p className="field-hint">
          Status akses diperbarui worker setelah verifikasi berhasil. Membuka atau menutup sesi ini
          tidak menandai CAPTCHA selesai.
        </p>
      </Dialog>
      <Dialog open={stopDialog} onClose={() => setStopDialog(false)} title="Hentikan akuisisi?">
        <p>
          Worker akan berhenti dengan aman. Data yang sudah diperoleh akan difinalisasi sebagai
          hasil parsial bila valid.
        </p>
        <div className="dialog-actions">
          <Button variant="secondary" onClick={() => setStopDialog(false)}>
            Tetap berjalan
          </Button>
          <Button variant="danger" loading={stop.isPending} onClick={() => stop.mutate()}>
            Hentikan dan simpan hasil
          </Button>
        </div>
      </Dialog>
    </>
  );
}
function PlatformCard({
  p,
  job,
  now,
  onVerification,
  loading,
}: {
  p: PlatformProgress;
  job: Job;
  now: number;
  onVerification: () => void;
  loading: boolean;
}) {
  const { cap, session } = useApp();
  const labels = {
    PENDING: 'Menunggu',
    FETCHING: 'Mengambil data',
    WAITING_CAPTCHA: 'Perlu verifikasi',
    RATE_LIMITED: 'Menunggu HTTP 429',
    TARGET_REACHED: 'Target tercapai',
    EXHAUSTED: 'Kandidat habis',
    BLOCKED: 'Akses dibatasi',
    STOPPED: 'Berhenti',
    ERROR: 'Gangguan akses',
  };
  return (
    <section
      className={`platform-card ${p.status === 'RATE_LIMITED' || p.status === 'WAITING_CAPTCHA' ? 'waiting' : ''}`}
    >
      <div className="platform-card-title">
        <span>
          <PlatformMark platform={p.platform} />
          <h2>{platformName(p.platform)}</h2>
        </span>
        <span className="platform-state">
          <span className="status-dot" />
          {labels[p.status]}
        </span>
      </div>
      <div className="qualified-count">
        <b>{number(p.counts.qualified)}</b>
        <span>/ {number(p.target)}</span>
      </div>
      <span className="qualified-caption">post memenuhi kriteria</span>
      <progress
        aria-label={`Target ${platformName(p.platform)}`}
        max={p.target || 1}
        value={Math.min(p.target || 1, p.counts.qualified)}
      />
      <div className="platform-numbers">
        <div>
          <span>Post terkumpul</span>
          <b>{number(p.counts.roots)}</b>
        </div>
        <div>
          <span>Komentar</span>
          <b>{number(p.counts.comments)}</b>
        </div>
        <div>
          <span>Reply</span>
          <b>{number(p.counts.replies)}</b>
        </div>
        <div>
          <span>Duplikat dilewati</span>
          <b>{number(p.counts.duplicates)}</b>
        </div>
      </div>
      <details className="counts-details">
        <summary>Lihat kandidat dan gap target</summary>
        <p>
          {number(p.counts.candidates)} kandidat diperiksa; {number(p.counts.rejected)} ditolak.
          Kekurangan target: {number(Math.max(0, p.target - p.counts.qualified))} post.
        </p>
      </details>
      {p.status === 'RATE_LIMITED' && (
        <div className="platform-alert">
          <Clock3 size={18} />
          <div>
            <b>Reddit membatasi permintaan</b>
            <p>
              Retry {p.retry || 0}/{job.config?.retries || 3}. Tunggu{' '}
              {p.waitUntil
                ? duration((Date.parse(p.waitUntil) - now) / 1000)
                : 'sesuai status worker'}
              .
            </p>
            <small>Cooldown menghormati Retry-After server. Deadline tetap berjalan.</small>
          </div>
        </div>
      )}
      {p.status === 'WAITING_CAPTCHA' && (
        <div className="platform-alert">
          <ShieldAlert size={19} />
          <div>
            <b>Verifikasi manusia diperlukan</b>
            <p>
              Sisa jendela:{' '}
              {p.waitUntil ? duration((Date.parse(p.waitUntil) - now) / 1000) : 'menunggu worker'}.
            </p>
            {session.role === 'operator' && (
              <Button variant="secondary" loading={loading} onClick={onVerification}>
                {cap.verificationAvailable ? 'Buka sesi verifikasi' : 'Periksa sesi worker'}
              </Button>
            )}
            {!cap.verificationAvailable && (
              <small>Sesi worker belum tersedia pada lingkungan ini.</small>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
function ProgressChart({ job }: { job: Job }) {
  const values = job.series;
  const active = job.platforms.map((p) => p.platform);
  const max = Math.max(1, ...values.flatMap((point) => active.map((p) => point[p] || 0)));
  const line = (platform: Platform) =>
    values
      .map(
        (point, i) =>
          `${i === 0 ? 'M' : 'L'}${55 + (i * 620) / Math.max(1, values.length - 1)},${204 - ((point[platform] || 0) * 164) / max}`,
      )
      .join(' ');
  return (
    <section className="panel chart-panel">
      <div className="panel-heading">
        <div>
          <h2>Perjalanan akuisisi</h2>
          <p>Post yang memenuhi kriteria, bertambah seiring waktu.</p>
        </div>
        <div className="chart-legend">
          {active.map((p) => (
            <span key={p}>
              <i style={{ background: platformChartColors[p] }} />
              {platformName(p)}
            </span>
          ))}
        </div>
      </div>
      {!values.length ? (
        <Empty title="Menunggu titik progres pertama" />
      ) : (
        <>
          <div className="chart-scale">
            <span>Skala: 0–{number(max)} post memenuhi kriteria</span>
            <span>Waktu akuisisi dalam WIB</span>
          </div>
          <svg
            className="line-chart progress-chart-plot"
            viewBox="0 0 720 230"
            role="img"
            aria-label="Grafik kumulatif post memenuhi kriteria per platform. Nilai lengkap tersedia pada tabel progres."
          >
            {[0, 1, 2, 3, 4].map((i) => (
              <line key={i} x1="55" x2="680" y1={204 - i * 41} y2={204 - i * 41} stroke="#dddddd" />
            ))}
            {active.map((p, i) => (
              <path
                key={p}
                d={line(p)}
                stroke={platformChartColors[p]}
                strokeWidth="3"
                strokeDasharray={i % 2 ? '8 4' : undefined}
                fill="none"
              />
            ))}
          </svg>
          <div className="chart-scale">
            <span>{dateTime(values[0].at)}</span>
            <span>{dateTime(values.at(-1)!.at)}</span>
          </div>
          <details className="chart-table">
            <summary>Lihat tabel progres</summary>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Waktu</th>
                    {active.map((p) => (
                      <th key={p}>{platformName(p)}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {values.map((point, i) => (
                    <tr key={i}>
                      <td>{dateTime(point.at)}</td>
                      {active.map((p) => (
                        <td key={p}>{number(point[p] || 0)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
        </>
      )}
    </section>
  );
}
export function Composition({ title, values }: { title: string; values: [string, number][] }) {
  const max = Math.max(1, ...values.map((v) => v[1]));
  return (
    <section className="panel composition-panel">
      <h2>{title}</h2>
      <div className="composition-bars">
        {values.map(([label, value], i) => (
          <div key={label}>
            <span>{label}</span>
            <b>{number(value)}</b>
            <div className="bar-track">
              <span style={{ width: `${(value * 100) / max}%` }} className={`bar-color-${i}`} />
            </div>
          </div>
        ))}
      </div>
      <p className="field-hint">Jumlah unik menurut jenis, bukan persentase target.</p>
    </section>
  );
}
