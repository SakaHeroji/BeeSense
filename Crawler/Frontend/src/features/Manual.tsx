import { flushSync } from 'react-dom';
import { useClock } from '../shared/hooks';
import { useRef, useState } from 'react';
import { Link, useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ArrowRight, BookOpen, Check, Clock3, ClipboardList, Link2 } from 'lucide-react';
import type { Config, FieldError, Plan, UrlReview } from '../shared/types';
import { initialConfig, platformName, platforms, validateConfig } from '../shared/domain';
import { api } from '../shared/api';
import { Badge, Button, Errors, Field, Notice, UnsavedGuard } from '../shared/ui';
import { useApp } from '../shared/context';
import { Baselines, ConfigFields, ConfigReview } from './Automatic';
import History from './History';
import Survey from './Survey';

export default function Manual() {
  const [params] = useSearchParams();
  const tab = params.get('tab') || 'url';
  const { session } = useApp();
  return (
    <>
      <div className="page-heading">
        <div>
          <span className="section-kicker">
            <BookOpen size={16} />
            Akuisisi dengan masukan manusia
          </span>
          <h1 id="main-title" tabIndex={-1}>
            Crawler manual
          </h1>
          <p>Dari sumber pilihan Anda, menjadi data riset yang terstruktur.</p>
        </div>
      </div>
      <div className="page-tabs">
        {[
          { id: 'url', label: 'Input URL', icon: Link2 },
          { id: 'survey', label: 'Data Survei', icon: ClipboardList },
          { id: 'history', label: 'Riwayat', icon: Clock3 },
        ].map((t) => (
          <Link
            key={t.id}
            className={tab === t.id ? 'active' : ''}
            to={`/crawler/manual?tab=${t.id}`}
          >
            <t.icon size={17} />
            {t.label}
          </Link>
        ))}
      </div>
      {tab === 'history' ? (
        <History manual />
      ) : session.role !== 'operator' ? (
        <Notice>
          Pengamat dapat melihat hasil melalui tab Riwayat. Input data memerlukan izin operator.
        </Notice>
      ) : tab === 'survey' ? (
        <Survey />
      ) : (
        <ManualUrl />
      )}
    </>
  );
}
function ManualUrl() {
  const now = useClock();
  const location = useLocation();
  const { cap } = useApp();
  const navigate = useNavigate();
  const client = useQueryClient();
  const [config, setConfig] = useState<Config>(() =>
    location.state?.config
      ? { ...location.state.config, name: `Salinan ${location.state.config.name}`, mode: 'url' }
      : initialConfig('url'),
  );
  const [text, setText] = useState(() => config.urls.join('\n')),
    [review, setReview] = useState<UrlReview[]>([]),
    [selected, setSelected] = useState<string[]>([]),
    [accept, setAccept] = useState(false),
    [dirty, setDirty] = useState(false),
    [plan, setPlan] = useState<Plan | null>(null),
    [errors, setErrors] = useState<FieldError[]>([]),
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
  const urlRevision = useRef(0);
  const clearReview = () => {
    urlRevision.current++;
    revision.current++;
    setReview([]);
    setSelected([]);
    setAccept(false);
    setPlan(null);
  };
  const inputUrls = text
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean);
  const urls = useMutation({
    mutationFn: (request: { inputs: string[]; baselines: string[]; revision: number }) =>
      api.reviewUrls(request.inputs, request.baselines),
    onSuccess: (data, request) => {
      if (request.revision !== urlRevision.current) return;
      setReview(data);
      setSelected(data.filter((r) => r.status === 'valid').map((r) => r.canonical!));
      setAccept(false);
    },
    onError: (e) => setErrors([{ field: 'urls', message: e.message }]),
  });
  const omitted = review.length - selected.length;
  const effective: Config = {
    ...config,
    urls: selected,
    platforms: Object.fromEntries(
      platforms.map((p) => [
        p,
        {
          ...config.platforms[p],
          enabled: selected.some((u) => review.find((r) => r.canonical === u)?.platform === p),
          queries: '',
          target: selected.filter((u) => review.find((r) => r.canonical === u)?.platform === p)
            .length,
        },
      ]),
    ) as Config['platforms'],
  };
  const validate = useMutation({
    mutationFn: (request: { config: Config; revision: number }) => api.validate(request.config),
    onSuccess: (result, request) => {
      if (request.revision === revision.current) setPlan(result);
    },
    onError: (e) => setErrors([{ field: 'server', message: e.message }]),
  });
  const start = useMutation({
    mutationFn: () => api.start(plan!, key),
    onSuccess: (j) => {
      flushSync(() => setDirty(false));
      client.setQueryData(['job', j.id], j);
      void client.invalidateQueries({ queryKey: ['jobs'] });
      navigate(`/crawler/manual/jobs/${j.id}`);
    },
    onError: (e) => setErrors([{ field: 'server', message: e.message }]),
  });
  return (
    <>
      <UnsavedGuard dirty={dirty && !start.isSuccess && !start.isPending} />
      <div className="configuration-layout">
        <section className="panel padded">
          <div className="form-section-title first">
            <h2>Percakapan yang sudah Anda temukan</h2>
            <p>Tempel tautan post atau video. Sistem hanya memproses URL yang dipilih.</p>
          </div>
          <Errors errors={errors} />
          <Field label="Nama pekerjaan" required>
            {(id) => (
              <input
                id={id}
                value={config.name}
                maxLength={120}
                onChange={(e) => change({ ...config, name: e.target.value })}
                placeholder="Contoh: Video referensi beasiswa"
              />
            )}
          </Field>
          <Field
            label="URL post atau video"
            required
            hint={`Satu URL per baris. Maksimum ${cap.limits.maxUrls} URL dari 7 platform.`}
          >
            {(id) => (
              <textarea
                id={id}
                rows={6}
                value={text}
                placeholder={
                  'https://www.youtube.com/watch?v=…\nhttps://www.reddit.com/r/…/comments/…/'
                }
                onChange={(e) => {
                  setText(e.target.value);
                  clearReview();
                  setDirty(true);
                  setErrors([]);
                }}
              />
            )}
          </Field>
          <Button
            variant="secondary"
            loading={urls.isPending}
            disabled={!inputUrls.length || inputUrls.length > cap.limits.maxUrls}
            onClick={() =>
              urls.mutate({
                inputs: inputUrls,
                baselines: config.baselines,
                revision: urlRevision.current,
              })
            }
          >
            <Check size={17} />
            Validasi URL
          </Button>
          {inputUrls.length > cap.limits.maxUrls && (
            <Notice tone="error">
              Terlalu banyak URL; maksimum {cap.limits.maxUrls} URL per pekerjaan.
            </Notice>
          )}
          {!!review.length && (
            <>
              <div className="review-counts">
                <span>
                  <b>{review.length}</b> input
                </span>
                <span>
                  <b>{review.filter((r) => r.status === 'valid').length}</b> valid unik
                </span>
                <span>
                  <b>{review.filter((r) => ['duplicate', 'existing'].includes(r.status)).length}</b>{' '}
                  duplikat
                </span>
                <span>
                  <b>
                    {review.filter((r) => ['invalid', 'unsupported'].includes(r.status)).length}
                  </b>{' '}
                  invalid
                </span>
              </div>
              <div className="table-scroll">
                <table>
                  <caption className="sr-only">Hasil validasi URL</caption>
                  <thead>
                    <tr>
                      <th>Pilih</th>
                      <th>Sumber dan URL</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {review.map((r, i) => (
                      <tr key={i}>
                        <td>
                          <input
                            aria-label={`Pilih URL ${i + 1}`}
                            type="checkbox"
                            disabled={r.status !== 'valid'}
                            checked={r.status === 'valid' && selected.includes(r.canonical!)}
                            onChange={(e) => {
                              revision.current++;
                              setSelected(
                                e.target.checked
                                  ? [...selected, r.canonical!]
                                  : selected.filter((u) => u !== r.canonical),
                              );
                              setPlan(null);
                              setAccept(false);
                              setKey(crypto.randomUUID());
                            }}
                          />
                        </td>
                        <td>
                          <strong>
                            {r.platform ? platformName(r.platform) : 'Tidak didukung'}
                          </strong>
                          <small className="break-url">{r.canonical || r.input}</small>
                        </td>
                        <td>
                          <Badge status={r.status === 'valid' ? 'COMPLETED' : 'PARTIAL'}>
                            {
                              {
                                valid: 'Valid',
                                duplicate: 'Duplikat input',
                                existing: 'Sudah ada',
                                unsupported: 'Tidak didukung',
                                invalid: 'Tidak valid',
                              }[r.status]
                            }
                          </Badge>
                          <small>{r.reason}</small>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="field-hint">
                Format valid belum menjamin post tersedia. Akses konten diperiksa worker saat
                pengambilan.
              </p>
            </>
          )}
          <details className="advanced">
            <summary>Pengaturan pengambilan</summary>
            <ConfigFields config={config} change={change} advancedOnly />
            <div className="form-grid">
              {platforms.map((p) => (
                <Field key={p} label={`Minimum komentar ${platformName(p)}`}>
                  {(id) => (
                    <input
                      id={id}
                      type="number"
                      min={0}
                      value={config.platforms[p].minComments}
                      onChange={(e) =>
                        change({
                          ...config,
                          platforms: {
                            ...config.platforms,
                            [p]: { ...config.platforms[p], minComments: +e.target.value },
                          },
                        })
                      }
                    />
                  )}
                </Field>
              ))}
            </div>
            <label className="checkbox-line">
              <input
                type="checkbox"
                checked={config.filtersEnabled}
                onChange={(e) => change({ ...config, filtersEnabled: e.target.checked })}
              />
              Aktifkan filter tanggal dan keyword
            </label>
            {config.filtersEnabled && <ManualFilters config={config} change={change} />}
          </details>
          <Baselines
            config={config}
            change={(c) => {
              change(c);
              clearReview();
            }}
          />
          {!!review.length && omitted > 0 && (
            <label className="checkbox-line acceptance">
              <input
                type="checkbox"
                checked={accept}
                onChange={(e) => setAccept(e.target.checked)}
              />
              Saya memahami {omitted} input tidak akan diproses.
            </label>
          )}
          {plan && (
            <>
              <div className="divider" />
              <ConfigReview config={plan.config} />
              <Notice tone="success">Rencana URL valid. Tidak ada discovery query tambahan.</Notice>
            </>
          )}
          <div className="form-actions">
            {plan && Date.parse(plan.expiresAt) > now ? (
              <Button
                loading={start.isPending}
                disabled={Date.parse(plan.expiresAt) <= now || (omitted > 0 && !accept)}
                onClick={() => start.mutate()}
              >
                Mulai ambil {selected.length} URL
                <ArrowRight size={16} />
              </Button>
            ) : (
              <Button
                loading={validate.isPending}
                disabled={!selected.length || (omitted > 0 && !accept)}
                onClick={() => {
                  const e = validateConfig(effective, cap);
                  setErrors(e);
                  if (!e.length) validate.mutate({ config: effective, revision: revision.current });
                }}
              >
                Tinjau & validasi pengambilan
                <ArrowRight size={16} />
              </Button>
            )}
          </div>
        </section>
        <aside className="plan-aside">
          <div className="plan-summary">
            <span className="summary-icon">
              <Link2 size={23} />
            </span>
            <h2>Daftar pilihan Anda</h2>
            <p>Fokus pada sumber yang telah Anda tentukan.</p>
            <div className="plan-stat">
              <span>URL terpilih</span>
              <b>
                {selected.length}
                <small> post/video unik</small>
              </b>
            </div>
            <div className="plan-note">
              <p>
                Varian tautan yang menuju post sama dihitung satu kali. URL yang ada pada baseline
                dilewati.
              </p>
            </div>
          </div>
          <div className="context-note">
            <h3>Konten tetap berkonteks</h3>
            <p>
              Minimum komentar bawaan 0. Thread yang pendek tetap bisa dikumpulkan tanpa
              menyembunyikan jumlah komentarnya.
            </p>
          </div>
        </aside>
      </div>
    </>
  );
}

function ManualFilters({ config, change }: { config: Config; change: (c: Config) => void }) {
  return (
    <div className="manual-filters">
      <div className="form-grid">
        <Field label="Mulai pada (WIB)" required>
          {(id) => (
            <input
              id={id}
              type="datetime-local"
              value={config.since}
              onChange={(e) => change({ ...config, since: e.target.value })}
            />
          )}
        </Field>
        <Field label="Sampai sebelum (WIB)" required hint="Batas akhir eksklusif.">
          {(id) => (
            <input
              id={id}
              type="datetime-local"
              value={config.until}
              onChange={(e) => change({ ...config, until: e.target.value })}
            />
          )}
        </Field>
        <Field label="Keyword disertakan">
          {(id) => (
            <textarea
              id={id}
              rows={3}
              value={config.include}
              onChange={(e) => change({ ...config, include: e.target.value })}
            />
          )}
        </Field>
        <Field label="Keyword dikecualikan">
          {(id) => (
            <textarea
              id={id}
              rows={3}
              value={config.exclude}
              onChange={(e) => change({ ...config, exclude: e.target.value })}
            />
          )}
        </Field>
      </div>
      <Field label="Kecocokan include">
        {(id) => (
          <select
            id={id}
            value={config.includeMode}
            onChange={(e) =>
              change({ ...config, includeMode: e.target.value as Config['includeMode'] })
            }
          >
            <option value="any">Salah satu keyword</option>
            <option value="all">Semua keyword</option>
          </select>
        )}
      </Field>
    </div>
  );
}
