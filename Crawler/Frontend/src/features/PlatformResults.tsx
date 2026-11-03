import { useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { keepPreviousData, useQuery } from '@tanstack/react-query';
import {
  ArrowLeft,
  ArrowRight,
  BarChart3,
  CalendarDays,
  Database,
  Download,
  Eye,
  FileSpreadsheet,
  Search,
  X,
} from 'lucide-react';
import { api } from '../shared/api';
import { useApp } from '../shared/context';
import {
  crawlDate,
  crawlDateLabel,
  dateTime,
  demoMode,
  number,
  platformName,
} from '../shared/domain';
import { useDebouncedValue, useUrlState } from '../shared/hooks';
import type { Job, Platform } from '../shared/types';
import { Badge, Button, Empty, Notice, Spinner } from '../shared/ui';
import TransactionMigration from './TransactionMigration';

export default function PlatformResults({ platform }: { platform: Platform }) {
  const [params, setParams] = useSearchParams();
  const date = params.get('date') || '';
  const selectDate = (value: string) =>
    setParams(
      (previous) => {
        const next = new URLSearchParams(previous);
        if (value) next.set('date', value);
        else next.delete('date');
        next.delete('page');
        next.delete('transaction');
        next.delete('action');
        next.delete('migration');
        return next;
      },
      { replace: true },
    );
  const transaction = params.get('transaction') || '';
  const selectTransaction = (id: string, migrate = false) =>
    setParams(
      (previous) => {
        const next = new URLSearchParams(previous);
        if (id) next.set('transaction', id);
        else next.delete('transaction');
        if (migrate) next.set('action', 'migrate');
        else next.delete('action');
        next.delete('migration');
        return next;
      },
      { replace: true },
    );
  const [pageValue, setPage] = useUrlState('page', '1');
  const jobs = useQuery({
    queryKey: ['jobs'],
    queryFn: api.jobs,
    refetchInterval: demoMode ? 2000 : 5000,
  });
  if (jobs.isPending)
    return (
      <div className="loading-page" role="status">
        <Spinner />
        Memuat hasil crawling…
      </div>
    );
  if (jobs.error)
    return (
      <Notice tone="error">
        {jobs.error.message}
        <Button variant="secondary" onClick={() => void jobs.refetch()}>
          Muat ulang hasil
        </Button>
      </Notice>
    );
  const scoped = [
    ...new Map(
      jobs.data
        .filter(
          (job) => job.mode === 'automatic' && job.platforms.some((p) => p.platform === platform),
        )
        .map((job) => [job.id, job]),
    ).values(),
  ].sort((a, b) => Date.parse(b.startedAt || b.createdAt) - Date.parse(a.startedAt || a.createdAt));
  const dates = [...new Set(scoped.map(crawlDate).filter(Boolean))];
  const filtered = scoped.filter((job) => !date || crawlDate(job) === date);
  const pages = Math.max(1, Math.ceil(filtered.length / 10));
  const page = Math.min(pages, Math.max(1, Number.parseInt(pageValue) || 1));
  const shown = filtered.slice((page - 1) * 10, page * 10);
  const selected = filtered.find(
    (job) => job.id === transaction && job.dataset && job.dataset.rows > 0,
  );
  const contents = filtered.reduce((sum, job) => {
    const c = job.platforms.find((p) => p.platform === platform)!.counts;
    return sum + c.roots + c.comments + c.replies;
  }, 0);
  return (
    <div className="social-results">
      <section className="panel transaction-panel">
        <div className="social-section-heading">
          <div>
            <h2>Hasil crawling {platformName(platform)}</h2>
            <p>
              Dikelompokkan menurut tanggal proses dijalankan dalam WIB, terpisah dari tanggal
              publikasi post.
            </p>
          </div>
        </div>
        <div className="transaction-toolbar">
          <label className="transaction-date">
            <CalendarDays size={18} aria-hidden="true" />
            <span>Tanggal crawling</span>
            <input
              type="date"
              aria-label="Filter tanggal crawling WIB"
              name="crawlDate"
              autoComplete="off"
              value={date}
              onChange={(e) => {
                selectDate(e.target.value);
              }}
            />
          </label>
          {date && (
            <Button
              variant="ghost"
              onClick={() => {
                selectDate('');
              }}
            >
              <X size={16} aria-hidden="true" />
              Semua tanggal
            </Button>
          )}
          <span className="transaction-count">
            {number(filtered.length)} pengambilan · {number(contents)} baris konten
          </span>
        </div>
        {dates.length > 0 && (
          <div className="date-shortcuts" aria-label="Tanggal tersedia">
            <button
              className={!date ? 'selected' : ''}
              aria-pressed={!date}
              onClick={() => {
                selectDate('');
              }}
            >
              Semua tanggal
            </button>
            {dates.slice(0, 6).map((day) => (
              <button
                key={day}
                className={date === day ? 'selected' : ''}
                aria-pressed={date === day}
                onClick={() => {
                  selectDate(day);
                }}
              >
                {crawlDateLabel(day)}
              </button>
            ))}
          </div>
        )}
        {!filtered.length ? (
          <Empty
            title={
              date
                ? 'Belum ada pengambilan pada tanggal ini'
                : `Belum ada hasil ${platformName(platform)}`
            }
          >
            <span>
              {date
                ? 'Pilih tanggal lain atau lihat semua tanggal.'
                : 'Atur pencarian dan jalankan pengambilan pertama.'}
            </span>
            <br />
            <Link className="inline-link" to={`/crawler/${platform}`}>
              Buka konfigurasi crawling
            </Link>
          </Empty>
        ) : (
          <>
            <p className="transaction-scroll-hint">Geser tabel untuk melihat semua kolom.</p>
            <div
              className="table-scroll transaction-scroll"
              role="region"
              aria-label={`Daftar transaksi ${platformName(platform)}`}
              tabIndex={0}
            >
              <table className="transaction-table">
                <caption>
                  Transaksi crawling {platformName(platform)} menurut tanggal eksekusi WIB
                </caption>
                <colgroup>
                  <col className="transaction-column-name" />
                  <col className="transaction-column-status" />
                  <col className="transaction-column-posts" />
                  <col className="transaction-column-comments" />
                  <col className="transaction-column-replies" />
                  <col className="transaction-column-storage" />
                  <col className="transaction-column-actions" />
                </colgroup>
                <thead>
                  <tr>
                    <th scope="col">Transaksi / waktu crawling</th>
                    <th scope="col">Status</th>
                    <th scope="col" className="numeric">
                      Post
                    </th>
                    <th scope="col" className="numeric">
                      Komentar
                    </th>
                    <th scope="col" className="numeric">
                      Balasan
                    </th>
                    <th scope="col">Penyimpanan</th>
                    <th scope="col">Tindakan</th>
                  </tr>
                </thead>
                <tbody>
                  {shown.map((job) => {
                    const p = job.platforms.find((item) => item.platform === platform)!;
                    const destination = job.config?.storage?.destination || 'excel';
                    return (
                      <tr
                        key={job.id}
                        className={selected?.id === job.id ? 'selected-transaction' : ''}
                      >
                        <td>
                          <b className="transaction-title">{job.name}</b>
                          <time className="transaction-time" dateTime={job.startedAt}>
                            {job.startedAt ? dateTime(job.startedAt) : 'Crawling belum dimulai'}
                          </time>
                        </td>
                        <td>
                          <Badge status={job.status} />
                        </td>
                        <td className="numeric">{number(p.counts.roots)}</td>
                        <td className="numeric">{number(p.counts.comments)}</td>
                        <td className="numeric">{number(p.counts.replies)}</td>
                        <td>
                          <div className="transaction-storage">
                            {destination !== 'postgresql' && (
                              <span>
                                <FileSpreadsheet size={15} aria-hidden="true" />
                                Excel lokal
                              </span>
                            )}
                            {destination !== 'excel' && (
                              <span>
                                <Database size={15} aria-hidden="true" />
                                PostgreSQL
                              </span>
                            )}
                          </div>
                        </td>
                        <td>
                          <div className="transaction-actions">
                            <Link
                              className="button secondary transaction-action"
                              aria-label={`Statistik ${job.name}`}
                              to={`/crawler/${platform}/jobs/${encodeURIComponent(job.id)}?panel=statistics`}
                            >
                              <BarChart3 size={18} aria-hidden="true" />
                              Statistik
                            </Link>
                            {job.dataset?.rows ? (
                              <Button
                                variant="secondary"
                                onClick={() =>
                                  selectTransaction(selected?.id === job.id ? '' : job.id)
                                }
                              >
                                <Eye size={18} aria-hidden="true" />
                                {selected?.id === job.id ? 'Tutup data' : 'Lihat data'}
                              </Button>
                            ) : (
                              <Link
                                className="button secondary"
                                to={`/crawler/${platform}/jobs/${encodeURIComponent(job.id)}`}
                              >
                                Lihat proses
                              </Link>
                            )}
                            {!!job.dataset?.rows &&
                              ['COMPLETED', 'PARTIAL', 'CANCELLED'].includes(job.status) && (
                                <Button
                                  variant="primary"
                                  className="transaction-action"
                                  aria-label={`Migrasi ${job.name} ke PostgreSQL`}
                                  onClick={() => selectTransaction(job.id, true)}
                                >
                                  <Database size={18} aria-hidden="true" />
                                  Migrasi ke PostgreSQL
                                </Button>
                              )}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            <div className="pagination">
              <span>
                {number(filtered.length)} pengambilan · Halaman {number(page)} dari {number(pages)}
              </span>
              <div>
                <Button
                  variant="secondary"
                  aria-label="Halaman pengambilan sebelumnya"
                  disabled={page <= 1}
                  onClick={() => setPage(String(page - 1))}
                >
                  <ArrowLeft size={16} aria-hidden="true" />
                </Button>
                <Button
                  variant="secondary"
                  aria-label="Halaman pengambilan berikutnya"
                  disabled={page >= pages}
                  onClick={() => setPage(String(page + 1))}
                >
                  <ArrowRight size={16} aria-hidden="true" />
                </Button>
              </div>
            </div>
          </>
        )}
      </section>
      {selected && <TransactionPreview key={selected.id} job={selected} platform={platform} />}
    </div>
  );
}

function TransactionPreview({ job, platform }: { job: Job; platform: Platform }) {
  const { session, notify } = useApp();
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [exporting, setExporting] = useState(false);
  const effectiveSearch = useDebouncedValue(search);
  const query = useQuery({
    queryKey: [
      'transaction-preview',
      job.dataset!.id,
      job.dataset!.version,
      page,
      effectiveSearch,
      platform,
    ],
    queryFn: () => api.dataset(job, page, effectiveSearch, platform),
    placeholderData: keepPreviousData,
  });
  const exportExcel = async () => {
    setExporting(true);
    try {
      const xlsx = await import('xlsx');
      const sheet = xlsx.utils.json_to_sheet(
        (query.data?.rows || []).map((row) => ({
          ID: row.id,
          Sumber: row.source,
          Jenis: row.kind,
          Teks: row.text,
          Konteks: row.context,
          'Tanggal publikasi konten': row.date,
          'Tanggal crawling WIB': crawlDate(job),
        })),
      );
      const book = xlsx.utils.book_new();
      xlsx.utils.book_append_sheet(book, sheet, 'Preview');
      const bytes = xlsx.write(book, { bookType: 'xlsx', type: 'array' });
      const url = URL.createObjectURL(
        new Blob([bytes], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        }),
      );
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = `${demoMode ? 'preview-simulasi' : 'preview'}-${platform}-${crawlDate(job)}.xlsx`;
      anchor.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      notify(
        'Preview Excel halaman ini diunduh. Berkas lengkap tersedia melalui detail pekerjaan.',
      );
    } catch {
      notify('Preview Excel belum dapat dibuat. Coba kembali setelah data selesai dimuat.');
    } finally {
      setExporting(false);
    }
  };
  return (
    <section className="panel transaction-preview" aria-label={`Data ${job.name}`}>
      <div className="social-section-heading">
        <div>
          <h2>Data pengambilan</h2>
          <p>
            {job.name} · {dateTime(job.startedAt || job.createdAt)}
          </p>
        </div>
        <Link
          className="button secondary"
          to={`/crawler/${platform}/jobs/${encodeURIComponent(job.id)}?panel=result`}
        >
          Detail pekerjaan
          <ArrowRight size={16} aria-hidden="true" />
        </Link>
      </div>
      <TransactionMigration job={job} platform={platform} />
      <div className="preview-toolbar">
        <label className="search-input">
          <Search size={18} aria-hidden="true" />
          <input
            name="transactionSearch"
            autoComplete="off"
            aria-label="Cari teks pada hasil crawling"
            placeholder="Cari teks atau konteks…"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </label>
        {session.canExport && (
          <Button
            variant="secondary"
            onClick={() => void exportExcel()}
            loading={exporting}
            disabled={!query.data?.rows.length || query.isFetching}
          >
            <Download size={16} aria-hidden="true" />
            Excel halaman ini
          </Button>
        )}
      </div>
      {query.isPending ? (
        <div className="loading-page" role="status">
          <Spinner />
          Memuat data…
        </div>
      ) : query.error ? (
        <Notice tone="error">{query.error.message}</Notice>
      ) : (
        <>
          {query.data.warning && (
            <div className="preview-notice">
              <Notice>{query.data.warning}</Notice>
            </div>
          )}
          <div className="table-scroll">
            <table className="preview-table">
              <caption>
                Preview konten {platformName(platform)}; tanggal publikasi konten berbeda dari
                tanggal crawling
              </caption>
              <thead>
                <tr>
                  <th>Jenis</th>
                  <th>Teks / konteks post</th>
                  <th>Tanggal publikasi konten</th>
                </tr>
              </thead>
              <tbody>
                {query.data.rows.map((row) => (
                  <tr key={row.id}>
                    <td>
                      <b>{row.kind}</b>
                      <small className="native-id">{row.id}</small>
                    </td>
                    <td>
                      <p>{row.text}</p>
                      <small>{row.context}</small>
                    </td>
                    <td>{dateTime(row.date)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {!query.data.rows.length && (
            <Empty title="Teks belum ditemukan">
              Coba kata pencarian lain atau kosongkan pencarian.
            </Empty>
          )}
          <div className="pagination">
            <span>
              {number(query.data.total)} baris · Halaman {number(page)}
            </span>
            <div>
              <Button
                variant="secondary"
                disabled={page <= 1 || query.isFetching}
                onClick={() => setPage(page - 1)}
                aria-label="Halaman data sebelumnya"
              >
                <ArrowLeft size={16} aria-hidden="true" />
              </Button>
              <Button
                variant="secondary"
                disabled={page * 50 >= query.data.total || query.isFetching}
                onClick={() => setPage(page + 1)}
                aria-label="Halaman data berikutnya"
              >
                <ArrowRight size={16} aria-hidden="true" />
              </Button>
            </div>
          </div>
        </>
      )}
    </section>
  );
}
