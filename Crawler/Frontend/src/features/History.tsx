import { useState } from 'react';
import { useUrlState } from '../shared/hooks';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowUpRight, Search } from 'lucide-react';
import { api } from '../shared/api';
import { dateTime, demoMode, number, platformName, platforms } from '../shared/domain';
import { Badge, Empty, Notice, Spinner, statusLabels } from '../shared/ui';

export default function History({ manual = false }: { manual?: boolean }) {
  const [search, setSearch] = useUrlState('q');
  const [status, setStatus] = useUrlState('status');
  const [source, setSource] = useUrlState('source');
  const [date, setDate] = useUrlState('date');
  const [page, setPage] = useState(1);
  const jobs = useQuery({
    queryKey: ['jobs'],
    queryFn: api.jobs,
    refetchInterval: demoMode ? 2000 : 5000,
  });
  if (jobs.isPending)
    return (
      <div className="loading-page">
        <Spinner /> Memuat riwayat…
      </div>
    );
  if (jobs.error) return <Notice tone="error">{jobs.error.message}</Notice>;
  const filtered = jobs.data.filter(
    (j) =>
      (manual ? j.mode !== 'automatic' : j.mode === 'automatic') &&
      (!status || j.status === status) &&
      (!source ||
        (source === 'survey'
          ? j.mode === 'survey'
          : j.platforms.some((p) => p.platform === source))) &&
      `${j.name} ${j.id}`.toLowerCase().includes(search.toLowerCase()) &&
      (!date ||
        new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Jakarta' }).format(
          new Date(j.createdAt),
        ) === date),
  );
  return (
    <section className="panel history-panel">
      <div className="panel-heading">
        <div>
          <h2>Riwayat akuisisi</h2>
          <p>Konfigurasi, perjalanan, dan hasil dalam satu jejak.</p>
        </div>
        <span className="count-label">{number(filtered.length)} pekerjaan</span>
      </div>
      <div className="table-toolbar">
        <label className="search-input">
          <Search size={17} />
          <input
            aria-label="Cari nama atau ID pekerjaan"
            placeholder="Cari nama atau ID pekerjaan"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </label>
        <select
          aria-label="Filter status pekerjaan"
          value={status}
          onChange={(e) => {
            setStatus(e.target.value);
            setPage(1);
          }}
        >
          <option value="">Semua status</option>
          {Object.entries(statusLabels).map(([k, v]) => (
            <option key={k} value={k}>
              {v}
            </option>
          ))}
        </select>
        <select
          aria-label="Filter sumber pekerjaan"
          value={source}
          onChange={(e) => {
            setSource(e.target.value);
            setPage(1);
          }}
        >
          <option value="">Semua sumber</option>
          {platforms.map((p) => (
            <option key={p} value={p}>
              {platformName(p)}
            </option>
          ))}
          {manual && <option value="survey">Survei</option>}
        </select>
        <input
          type="date"
          aria-label="Tanggal pekerjaan WIB"
          value={date}
          onChange={(e) => {
            setDate(e.target.value);
            setPage(1);
          }}
        />
      </div>
      {!filtered.length ? (
        <Empty title="Belum ada pekerjaan yang cocok">
          Buat akuisisi baru atau sesuaikan filter riwayat.
        </Empty>
      ) : (
        <div className="job-list">
          {filtered.slice((page - 1) * 20, page * 20).map((j) => (
            <Link
              className="job-row"
              key={j.id}
              to={`/crawler/${manual ? 'manual' : 'automatic'}/jobs/${j.id}`}
            >
              <div className={`job-icon ${j.mode === 'survey' ? 'survey' : ''}`}>
                {j.mode === 'survey' ? 'S' : '↗'}
              </div>
              <div className="job-name">
                <strong>{j.name}</strong>
                <span>
                  {j.mode === 'survey'
                    ? 'Survei'
                    : j.mode === 'url'
                      ? 'URL pilihan'
                      : 'Pencarian otomatis'}{' '}
                  <span className="separator">/</span> {dateTime(j.createdAt)}
                </span>
              </div>
              <div className="job-count">
                <b>
                  {number(
                    j.mode === 'survey'
                      ? j.dataset?.responses || 0
                      : j.platforms.reduce((n, p) => n + p.counts.qualified, 0),
                  )}
                </b>
                <span>{j.mode === 'survey' ? 'respons valid' : 'post memenuhi kriteria'}</span>
              </div>
              <div className="job-sources">
                {j.platforms.map((p) => (
                  <span key={p.platform}>{platformName(p.platform)}</span>
                ))}
              </div>
              <Badge status={j.status} />
              <ArrowUpRight size={18} />
            </Link>
          ))}
        </div>
      )}
      {filtered.length > 20 && (
        <div className="pagination">
          <span>
            Halaman {page} dari {Math.ceil(filtered.length / 20)}
          </span>
          <div>
            <button
              className="button secondary"
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
            >
              Sebelumnya
            </button>
            <button
              className="button secondary"
              disabled={page * 20 >= filtered.length}
              onClick={() => setPage(page + 1)}
            >
              Berikutnya
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
