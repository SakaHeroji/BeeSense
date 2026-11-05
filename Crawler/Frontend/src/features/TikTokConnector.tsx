import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Check, Copy, Eye, EyeOff, Monitor, Plug, RefreshCw, ShieldCheck } from 'lucide-react';
import { api } from '../shared/api';
import { useApp } from '../shared/context';
import { dateTime, demoMode, number } from '../shared/domain';
import { useClock } from '../shared/hooks';
import { connectorStates, connectorVersion } from '../shared/tiktok-connector';
import type { Job } from '../shared/types';
import { Button, Field, Notice, Spinner } from '../shared/ui';

export function TikTokWorkflow({ step = 1 }: { step?: number }) {
  return (
    <ol className="tiktok-workflow" aria-label="Alur crawling TikTok">
      {['Atur pengambilan', 'Hubungkan Chrome', 'Pantau hasil'].map((label, index) => (
        <li
          key={label}
          className={index + 1 < step ? 'done' : index + 1 === step ? 'current' : ''}
          aria-current={index + 1 === step ? 'step' : undefined}
        >
          <span aria-hidden="true">{index + 1 < step ? <Check size={16} /> : index + 1}</span>
          {label}
        </li>
      ))}
    </ol>
  );
}

export function TikTokChromePreparation() {
  return (
    <section className="panel tiktok-preparation" aria-labelledby="chrome-preparation-title">
      <div className="tiktok-connection-heading">
        <Monitor size={22} aria-hidden="true" />
        <h2 id="chrome-preparation-title">Gunakan Chrome Anda</h2>
      </div>
      <p>TikTok diambil melalui tab Chrome yang sudah login.</p>
      <ul>
        <li>Aktifkan BeeSense TikTok Connector {connectorVersion} atau lebih baru.</li>
        <li>Alamat server dan kode pairing muncul di sini setelah konfigurasi ditinjau.</li>
        <li>Biarkan tab TikTok aktif dan jendela Chrome terbuka. Popup plugin boleh ditutup.</li>
        <li>
          Biarkan plugin menggulir dan membuka balasan. Hindari pindah post atau refresh manual.
        </li>
        <li>Jika diminta, selesaikan CAPTCHA langsung pada tab TikTok.</li>
      </ul>
      <div className="tiktok-timer-note">
        <ShieldCheck size={18} aria-hidden="true" />
        <span>Waktu crawling mulai dihitung setelah plugin terhubung.</span>
      </div>
    </section>
  );
}

function CopyField({
  label,
  value,
  secret = false,
}: {
  label: string;
  value: string;
  secret?: boolean;
}) {
  const [shown, setShown] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');
  const copy = async () => {
    setError('');
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
    } catch {
      setError('Clipboard tidak tersedia. Tampilkan dan salin isian ini secara manual.');
    }
  };
  return (
    <div className="tiktok-copy-field">
      <Field label={label}>
        {(id) => (
          <input
            id={id}
            type={secret && !shown ? 'password' : 'text'}
            readOnly
            value={value}
            spellCheck={false}
            onFocus={(e) => e.target.select()}
          />
        )}
      </Field>
      <div className="button-row">
        <Button
          variant="secondary"
          onClick={() => void copy()}
          aria-label={`Salin ${label.toLowerCase()}`}
        >
          {copied ? <Check size={16} aria-hidden="true" /> : <Copy size={16} aria-hidden="true" />}
          {copied ? 'Tersalin' : 'Salin'}
        </Button>
        {secret && (
          <Button
            variant="ghost"
            onClick={() => setShown(!shown)}
            aria-pressed={shown}
            aria-label={shown ? 'Sembunyikan kode pairing' : 'Tampilkan kode pairing'}
          >
            {shown ? <EyeOff size={16} aria-hidden="true" /> : <Eye size={16} aria-hidden="true" />}
            {shown ? 'Sembunyikan' : 'Tampilkan'}
          </Button>
        )}
      </div>
      <span className="sr-only" role="status">
        {copied ? `${label} tersalin.` : ''}
      </span>
      {error && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

export default function TikTokConnector({ job }: { job: Job }) {
  const { cap, session, notify } = useApp();
  const client = useQueryClient();
  const now = useClock();
  const live = ['QUEUED', 'WAITING_CONNECTOR', 'RUNNING', 'STOP_REQUESTED', 'FINALIZING'].includes(
    job.status,
  );
  const queryKey = ['tiktok-connector', job.id];
  const query = useQuery({
    queryKey,
    queryFn: () => api.tiktokConnector(job.id),
    enabled: cap.tiktokConnectorAvailable === true && session.role === 'operator' && live,
    refetchInterval: live ? 2000 : false,
    gcTime: 0,
    staleTime: 0,
    retry: false,
  });
  const action = useMutation({
    mutationFn: (kind: 'renew' | 'resume') =>
      kind === 'renew' ? api.renewTikTokConnector(job.id) : api.resumeTikTokConnector(job.id),
    onSuccess: (connection) => {
      client.setQueryData(queryKey, connection);
      void client.invalidateQueries({ queryKey: ['job', job.id] });
    },
    onError: (error) => notify(error.message),
  });
  const simulate = useMutation({
    mutationFn: (scenario: string) => api.demoScenario!(job.id, scenario),
    onSuccess: (snapshot) => {
      client.setQueryData(['job', job.id], snapshot);
      void query.refetch();
    },
    onError: (error) => notify(error.message),
  });
  const connection = query.data;
  const state = !live ? 'FINISHED' : connection?.state || job.connector?.state || 'WAITING';
  const expired = connection?.pairingExpiresAt
    ? Date.parse(connection.pairingExpiresAt) <= now
    : false;
  const thread = connection?.thread;
  const staleThread = thread && now - Date.parse(thread.lastActivityAt) > 60000;
  return (
    <section
      className={`panel tiktok-connector state-${state.toLowerCase()}`}
      aria-labelledby="tiktok-connector-title"
    >
      <div className="tiktok-connection-heading">
        <Plug size={23} aria-hidden="true" />
        <div>
          <h2 id="tiktok-connector-title">Koneksi Chrome & plugin</h2>
          <p>Satu koneksi untuk transaksi ini.</p>
        </div>
        <span className="tiktok-connection-state" role="status">
          {query.error ? 'Status belum diperbarui' : connectorStates[state]}
        </span>
      </div>
      {demoMode && (
        <p className="field-hint">
          Mode simulasi: kode pairing di bawah hanya contoh. Gunakan tombol uji simulasi untuk
          meninjau alur; halaman ini tidak mengendalikan Chrome atau crawler nyata.
        </p>
      )}
      {!cap.tiktokConnectorAvailable ? (
        <Notice>
          Server dashboard belum menyediakan penghubung TikTok. Status koneksi akan muncul di
          transaksi ini setelah layanan tersedia.
        </Notice>
      ) : session.role !== 'operator' ? (
        <p>Pairing dikelola operator. Anda tetap dapat memantau hasil pengambilan.</p>
      ) : query.isPending && live ? (
        <p>
          <Spinner /> Memeriksa koneksi plugin…
        </p>
      ) : (
        <>
          {query.error && (
            <Notice tone="warning">
              Status koneksi belum dapat diperbarui. {query.error.message}{' '}
              <Button variant="secondary" onClick={() => void query.refetch()}>
                Coba lagi
              </Button>
            </Notice>
          )}
          {live && connection && ['WAITING', 'DISCONNECTED', 'EXPIRED'].includes(state) && (
            <>
              <p className="tiktok-connection-intro">
                Buka tab TikTok di Chrome yang sudah login, lalu buka popup{' '}
                <b>BeeSense TikTok Connector</b>. Gunakan alamat dan kode dari transaksi ini.
              </p>
              <div className="tiktok-pairing-grid">
                <CopyField label="Alamat server dashboard" value={connection.bridgeUrl} />
                {!expired && connection.pairingCode && (
                  <CopyField
                    key={connection.pairingExpiresAt}
                    label="Kode pairing sementara"
                    value={connection.pairingCode}
                    secret
                  />
                )}
              </div>
              <div className="tiktok-pairing-footer">
                <p>
                  Klik <b>Mulai pada tab TikTok ini</b> di popup. Halaman ini akan memperbarui
                  status otomatis.
                </p>
                <span>Plugin minimum {connection.minimumVersion}</span>
              </div>
              {expired || !connection.pairingCode || state === 'EXPIRED' ? (
                <Button
                  variant="secondary"
                  loading={action.isPending}
                  onClick={() => action.mutate('renew')}
                >
                  <RefreshCw size={16} aria-hidden="true" />
                  Buat kode pairing baru
                </Button>
              ) : (
                <p className="field-hint">
                  Kode berlaku sampai {dateTime(connection.pairingExpiresAt)}. Tidak perlu membuka
                  server atau terminal lain.
                </p>
              )}
              <div className="tiktok-timer-note">
                <ShieldCheck size={18} aria-hidden="true" />
                <span>
                  {job.startedAt
                    ? 'Hasil yang sudah diterima dipertahankan. Deadline tetap berjalan saat koneksi terputus.'
                    : 'Pengambilan dan hitungan durasi belum dimulai. Menunggu verifikasi koneksi plugin.'}
                </span>
              </div>
            </>
          )}
          {state === 'CONNECTED' && (
            <p>
              Biarkan tab TikTok aktif dan jendela Chrome terbuka tanpa diminimalkan. Popup plugin
              boleh ditutup. Biarkan plugin menggulir, membuka balasan dan berpindah post; hindari
              refresh atau navigasi manual. Selesaikan CAPTCHA jika diminta.
            </p>
          )}
          {state === 'VALIDATION_REQUIRED' && (
            <div className="tiktok-validation">
              <Notice tone="warning">
                Selesaikan CAPTCHA atau login langsung di tab TikTok yang sedang dipakai. Setelah
                selesai, minta crawler memeriksa kembali halaman tersebut.
              </Notice>
              <Button loading={action.isPending} onClick={() => action.mutate('resume')}>
                {demoMode
                  ? 'Simulasikan lanjut setelah validasi'
                  : 'Lanjut setelah validasi manual'}
              </Button>
            </div>
          )}
          {!!connection?.version && (
            <p className="tiktok-client-version">
              Connector {connection.version}
              {connection.lastSeenAt
                ? ` · Terhubung terakhir ${dateTime(connection.lastSeenAt)}`
                : ''}
            </p>
          )}
          {live && thread && (
            <div className="tiktok-current-thread">
              <div>
                <h3>Post yang sedang dibaca</h3>
                <span translate="no">{thread.postId}</span>
              </div>
              <dl>
                <div>
                  <dt>Komentar terbaca</dt>
                  <dd>{number(thread.comments)}</dd>
                </div>
                <div>
                  <dt>Balasan terbaca</dt>
                  <dd>{number(thread.replies)}</dd>
                </div>
                <div>
                  <dt>Penelusuran komentar</dt>
                  <dd>
                    {thread.pagination === 'exhausted'
                      ? 'Akhir terverifikasi'
                      : thread.pagination === 'unverified'
                        ? 'Belum terverifikasi'
                        : 'Masih ditelusuri'}
                  </dd>
                </div>
              </dl>
              <p className="field-hint">
                {thread.activity === 'comments'
                  ? 'Membaca komentar pada post ini.'
                  : thread.activity === 'replies'
                    ? 'Membuka dan membaca balasan.'
                    : thread.activity === 'scrolling'
                      ? 'Menggulir daftar komentar.'
                      : 'Menunggu data komentar berikutnya.'}
              </p>
              <p>
                Data thread berjalan belum termasuk hitungan operasi selesai di bawah. Statistik
                jumlah komentar TikTok:{' '}
                {thread.sourceTotal === undefined ? 'belum tersedia' : number(thread.sourceTotal)}.
              </p>
              <p className={staleThread ? 'tiktok-no-new-data' : 'field-hint'}>
                {staleThread
                  ? 'Belum ada ID baru lebih dari 1 menit. Hitungan terakhir dipertahankan; ini tidak otomatis berarti Chrome terputus.'
                  : `ID baru terakhir ${dateTime(thread.lastActivityAt)}.`}
              </p>
            </div>
          )}
          {!live && (
            <p>
              Pairing ditutup untuk transaksi ini. Hasil, statistik, dan status kelengkapan tetap
              tersedia pada tab di bawah.
            </p>
          )}
          {demoMode && live && (
            <details className="tiktok-demo-controls">
              <summary>Uji alur plugin dalam simulasi</summary>
              <p>
                Tombol berikut hanya mengubah ilustrasi frontend. Tidak menghubungkan Chrome atau
                mengendalikan crawler yang sedang berjalan.
              </p>
              <div className="button-row">
                <Button
                  variant="secondary"
                  loading={simulate.isPending}
                  onClick={() => simulate.mutate('connector-ready')}
                >
                  Simulasikan plugin terhubung
                </Button>
                {!!job.startedAt && (
                  <>
                    <Button
                      variant="secondary"
                      onClick={() => simulate.mutate('connector-captcha')}
                      disabled={simulate.isPending}
                    >
                      Simulasikan CAPTCHA TikTok
                    </Button>
                    <Button
                      variant="secondary"
                      onClick={() => simulate.mutate('connector-disconnected')}
                      disabled={simulate.isPending}
                    >
                      Simulasikan koneksi terputus
                    </Button>
                  </>
                )}
              </div>
            </details>
          )}
        </>
      )}
    </section>
  );
}
