import { Link } from 'react-router-dom';
import { Database } from 'lucide-react';
import {
  crawlDate,
  crawlDateLabel,
  dateTime,
  duration,
  number,
  platformName,
  storageLabels,
} from '../shared/domain';
import type { Job, Platform } from '../shared/types';

export default function JobStatistics({ job, platform }: { job: Job; platform?: Platform }) {
  const selected = job.platforms.filter((p) => !platform || p.platform === platform);
  const counts = selected.reduce(
    (sum, p) => ({
      roots: sum.roots + p.counts.roots,
      qualified: sum.qualified + p.counts.qualified,
      comments: sum.comments + p.counts.comments,
      replies: sum.replies + p.counts.replies,
      candidates: sum.candidates + p.counts.candidates,
      duplicates: sum.duplicates + p.counts.duplicates,
      rejected: sum.rejected + p.counts.rejected,
      target: sum.target + p.target,
    }),
    {
      roots: 0,
      qualified: 0,
      comments: 0,
      replies: 0,
      candidates: 0,
      duplicates: 0,
      rejected: 0,
      target: 0,
    },
  );
  const rows = counts.roots + counts.comments + counts.replies;
  const percent = counts.target ? Math.min(100, (counts.qualified / counts.target) * 100) : 0;
  const seconds = job.startedAt
    ? Math.max(0, (Date.parse(job.updatedAt) - Date.parse(job.startedAt)) / 1000)
    : 0;
  return (
    <section className="panel transaction-statistics" aria-label="Statistik transaksi crawling">
      <div className="social-section-heading">
        <div>
          <h2>Statistik transaksi {platform ? platformName(platform) : 'crawling'}</h2>
          <p>Ringkasan seluruh konten dan hasil pemeriksaan transaksi ini.</p>
        </div>
        {platform && job.dataset && (
          <Link
            className="button primary transaction-action"
            to={`/crawler/${platform}?view=results&transaction=${encodeURIComponent(job.id)}&action=migrate`}
          >
            <Database size={18} aria-hidden="true" />
            Migrasi ke PostgreSQL
          </Link>
        )}
      </div>
      <dl className="statistics-grid">
        {(
          [
            ['Post terkumpul', counts.roots],
            ['Post memenuhi kriteria', counts.qualified],
            ['Komentar', counts.comments],
            ['Balasan', counts.replies],
            ['Total konten unik', rows],
            ['Kandidat diperiksa', counts.candidates],
            ['Duplikat dilewati', counts.duplicates],
            ['Ditolak filter / akses', counts.rejected],
          ] as const
        ).map(([label, value]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>{number(value)}</dd>
          </div>
        ))}
      </dl>
      <div className="statistics-target">
        <div>
          <h3>Pencapaian target</h3>
          <p>
            {number(counts.qualified)} dari {number(counts.target)} post memenuhi kriteria
          </p>
        </div>
        <b>{number(Math.round(percent * 10) / 10)}%</b>
        <progress
          max={counts.target || 1}
          value={Math.min(counts.qualified, counts.target)}
          aria-label="Pencapaian target transaksi"
        />
        <p>
          Kekurangan target: {number(Math.max(0, counts.target - counts.qualified))} post. Komentar
          dan balasan tidak dihitung sebagai target post.
        </p>
      </div>
      <dl className="review-dl statistics-metadata">
        <div>
          <dt>Tanggal crawling WIB</dt>
          <dd>{crawlDateLabel(crawlDate(job))}</dd>
        </div>
        <div>
          <dt>Mulai</dt>
          <dd>{dateTime(job.startedAt)}</dd>
        </div>
        <div>
          <dt>Pembaruan terakhir</dt>
          <dd>{dateTime(job.updatedAt)}</dd>
        </div>
        <div>
          <dt>Durasi tercatat</dt>
          <dd>{job.startedAt ? duration(seconds) : 'Belum dimulai'}</dd>
        </div>
        <div>
          <dt>Penyimpanan</dt>
          <dd>{storageLabels[job.config?.storage?.destination || 'excel']}</dd>
        </div>
        <div>
          <dt>Versi dataset</dt>
          <dd>{job.dataset ? number(job.dataset.version) : 'Belum tersedia'}</dd>
        </div>
      </dl>
      {job.reason && <p className="statistics-reason">Alasan hasil: {job.reason}</p>}
    </section>
  );
}
