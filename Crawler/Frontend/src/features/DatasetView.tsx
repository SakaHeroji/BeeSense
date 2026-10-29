import { useState } from 'react';
import { keepPreviousData, useMutation, useQuery } from '@tanstack/react-query';
import {
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  CheckCheck,
  Database,
  Download,
  FileCheck2,
  Search,
} from 'lucide-react';
import { api } from '../shared/api';
import { useDebouncedValue, useUrlState } from '../shared/hooks';
import {
  csvCell,
  dateTime,
  demoMode,
  download,
  number,
  platformName,
  platforms,
  safeExternal,
} from '../shared/domain';
import type { Job, PreviewRow } from '../shared/types';
import { Badge, Button, Dialog, Empty, Notice, Spinner } from '../shared/ui';
import { useApp } from '../shared/context';

export default function DatasetView({ job }: { job: Job }) {
  const { session, notify } = useApp();
  const [tab, setTab] = useUrlState('dataset', 'summary');
  const [page, setPage] = useState(1),
    [search, setSearch] = useState(''),
    [source, setSource] = useState(''),
    [selected, setSelected] = useState<PreviewRow | null>(null),
    [handoffDialog, setHandoffDialog] = useState(false),
    [accept, setAccept] = useState(false);
  const effectiveSearch = useDebouncedValue(search);
  const query = useQuery({
    queryKey: ['dataset', job.dataset!.id, job.dataset!.version, page, effectiveSearch, source],
    queryFn: () => api.dataset(job, page, effectiveSearch, source),
    placeholderData: keepPreviousData,
  });
  const handoff = useMutation({
    mutationFn: () => api.handoff(job, accept),
    onSuccess: (r) => {
      setHandoffDialog(false);
      notify(
        `${demoMode ? 'Simulasi pilihan' : 'Pilihan'} input NLP tersimpan: ${r.id}. Training belum dijalankan.`,
      );
    },
    onError: (e) => notify(e.message),
  });
  if (query.isPending)
    return (
      <div className="loading-page">
        <Spinner />
        Memuat dataset…
      </div>
    );
  if (query.error) return <Notice tone="error">{query.error.message}</Notice>;
  const { dataset: ds, rows, total, files, warning } = query.data;
  const canHandoff = session.role === 'operator' && ds.rows > 0 && ds.nlpSupported;
  const exportPreview = () => {
    const fields = ['id', 'source', 'kind', 'text', 'context', 'date', 'role', 'flag'] as const;
    download(
      'preview-sintetis.csv',
      [fields.join(','), ...rows.map((r) => fields.map((f) => csvCell(r[f] || '')).join(','))].join(
        '\n',
      ),
    );
    notify('Preview halaman ini diunduh. Ini bukan bundle crawling sebenarnya.');
  };
  return (
    <section className="panel dataset-panel">
      <div className="dataset-heading">
        <div className="dataset-symbol">
          <Database size={25} />
        </div>
        <div>
          <span className="dataset-version">
            Versi {ds.version} · {ds.schema}
          </span>
          <h2>Dataset {job.mode === 'survey' ? 'survei minat studi' : 'percakapan pendidikan'}</h2>
          <p className="break-url">{ds.id}</p>
        </div>
        <Badge status={ds.partial ? 'PARTIAL' : 'COMPLETED'} />
      </div>
      {warning && (
        <div className="padded-notice">
          <Notice tone="warning">{warning}</Notice>
        </div>
      )}
      <div className="dataset-tabs">
        {[
          ['summary', 'Ringkasan'],
          ['data', 'Data'],
          ['quality', 'Kualitas'],
          ['files', 'Berkas'],
        ].map(([id, label]) => (
          <button className={tab === id ? 'active' : ''} key={id} onClick={() => setTab(id)}>
            {label}
          </button>
        ))}
      </div>
      <div className="dataset-content">
        {tab === 'summary' && (
          <>
            <div className="dataset-stat-grid">
              <div>
                <span>{job.mode === 'survey' ? 'Jawaban tersimpan' : 'Baris konten unik'}</span>
                <b>{number(ds.rows)}</b>
              </div>
              <div>
                <span>{job.mode === 'survey' ? 'Respons valid' : 'Post memenuhi kriteria'}</span>
                <b>
                  {number(
                    job.mode === 'survey'
                      ? ds.responses || 0
                      : job.platforms.reduce((n, p) => n + p.counts.qualified, 0),
                  )}
                </b>
              </div>
              <div>
                <span>Sumber</span>
                <b className="smaller-stat">
                  {job.mode === 'survey' ? 'Survei' : job.platforms.length + ' platform'}
                </b>
              </div>
            </div>
            <div className="quality-grid">
              <div>
                <CheckCheck size={22} />
                <h3>Asal data terjaga</h3>
                <p>
                  {job.mode === 'survey'
                    ? 'Peran responden, pertanyaan, versi survei, dan izin disimpan bersama jawaban.'
                    : 'Root, komentar, dan reply tetap terpisah. Peran penulis sosial tidak ditebak.'}
                </p>
              </div>
              <div>
                <FileCheck2 size={22} />
                <h3>Hasil berversi</h3>
                <p>
                  Dataset sumber tetap utuh. Gunakan ID, versi, dan checksum saat meneruskan ke
                  tahap analisis.
                </p>
              </div>
            </div>
            <div className="table-scroll">
              <table>
                <caption>Komposisi sumber dan jenis konten pada hasil</caption>
                <thead>
                  <tr>
                    <th>Sumber</th>
                    <th>{job.mode === 'survey' ? 'Respons valid' : 'Post'}</th>
                    <th>{job.mode === 'survey' ? 'Jawaban' : 'Komentar'}</th>
                    <th>{job.mode === 'survey' ? 'Jawaban teks' : 'Reply'}</th>
                  </tr>
                </thead>
                <tbody>
                  {job.mode === 'survey' ? (
                    <tr>
                      <td>Survei</td>
                      <td>{number(ds.responses || 0)}</td>
                      <td>{number(ds.rows)}</td>
                      <td>{number(ds.textRows || 0)}</td>
                    </tr>
                  ) : (
                    job.platforms.map((p) => (
                      <tr key={p.platform}>
                        <td>{platformName(p.platform)}</td>
                        <td>{number(p.counts.roots)}</td>
                        <td>{number(p.counts.comments)}</td>
                        <td>{number(p.counts.replies)}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </>
        )}
        {tab === 'data' && (
          <>
            <div className="table-toolbar">
              <label className="search-input">
                <Search size={16} />
                <input
                  aria-label="Cari isi dataset"
                  placeholder="Cari isi atau konteks"
                  value={search}
                  onChange={(e) => {
                    setSearch(e.target.value);
                    setPage(1);
                  }}
                />
              </label>
              <select
                aria-label="Filter sumber dataset"
                value={source}
                onChange={(e) => {
                  setSource(e.target.value);
                  setPage(1);
                }}
              >
                <option value="">Semua sumber</option>
                {job.mode === 'survey' ? (
                  <option value="survey">Survei</option>
                ) : (
                  <>
                    {platforms.map((p) => (
                      <option key={p} value={p}>
                        {platformName(p)}
                      </option>
                    ))}
                  </>
                )}
              </select>
            </div>
            {rows.length ? (
              <div className="table-scroll">
                <table>
                  <caption className="sr-only">
                    Preview dataset, maksimal 50 baris per halaman
                  </caption>
                  <thead>
                    <tr>
                      <th>Sumber / jenis</th>
                      <th>Konten</th>
                      <th>Peran</th>
                      <th>Detail</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rows.map((row) => (
                      <tr key={row.id}>
                        <td>
                          {row.source}
                          <small>{row.kind}</small>
                        </td>
                        <td className="preview-text">
                          {row.text}
                          <small>{dateTime(row.date)}</small>
                        </td>
                        <td>{row.role || 'Tidak diketahui'}</td>
                        <td>
                          <button className="text-button" onClick={() => setSelected(row)}>
                            Lihat konteks
                            <ArrowUpRight size={13} />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <Empty title="Tidak ada baris untuk ditampilkan">
                Sesuaikan filter atau periksa penjelasan sumber data.
              </Empty>
            )}
            <div className="pagination">
              <span>
                {number(total)} baris preview · halaman {page}
              </span>
              <div>
                <Button variant="secondary" disabled={page === 1} onClick={() => setPage(page - 1)}>
                  <ArrowLeft size={14} />
                  Sebelumnya
                </Button>
                <Button
                  variant="secondary"
                  disabled={page * 50 >= total}
                  onClick={() => setPage(page + 1)}
                >
                  Berikutnya
                  <ArrowRight size={14} />
                </Button>
              </div>
            </div>
          </>
        )}
        {tab === 'quality' && (
          <>
            <h3>Pemeriksaan sebelum analisis</h3>
            <dl className="review-dl">
              <div>
                <dt>Status hasil</dt>
                <dd>
                  {ds.partial
                    ? 'Parsial; penerimaan eksplisit diperlukan untuk handoff.'
                    : 'Tujuan mode terpenuhi.'}
                </dd>
              </div>
              <div>
                <dt>Skema</dt>
                <dd>
                  {ds.schema} —{' '}
                  {ds.nlpSupported ? 'didukung antarmuka NLP' : 'adapter NLP belum tersedia'}
                </dd>
              </div>
              <div>
                <dt>Deduplikasi</dt>
                <dd>
                  {job.mode === 'survey'
                    ? 'Kunci respons + pertanyaan; konflik tidak ditimpa.'
                    : 'Native ID + URL kanonik; baseline dibaca tanpa diubah.'}
                </dd>
              </div>
              <div>
                <dt>Provenance</dt>
                <dd>
                  {job.mode === 'survey'
                    ? 'Peran dideklarasikan, template berversi, pertanyaan terpisah dari jawaban.'
                    : 'Sumber, root/parent, waktu, dan alasan kelayakan tetap terhubung.'}
                </dd>
              </div>
              <div>
                <dt>Checksum</dt>
                <dd className="break-url">
                  {demoMode
                    ? 'Tidak berlaku: dataset simulasi, bukan bundle terverifikasi.'
                    : ds.checksum}
                </dd>
              </div>
            </dl>
            {job.mode === 'survey' && (
              <Notice tone="warning">
                Metadata survei tidak boleh dipaksa masuk workbook sosial sepuluh kolom. Handoff
                diblokir sampai adapter skema survei tersedia.
              </Notice>
            )}
          </>
        )}
        {tab === 'files' && (
          <>
            <Notice>
              {demoMode
                ? 'Berkas berikut hanya ekspor preview sintetis dan metadata simulasi. Tidak ada workbook audit atau bundle crawling sebenarnya.'
                : 'Berkas final telah diterbitkan backend. Periksa checksum sebelum menggunakan hasil.'}
            </Notice>
            <div className="file-list">
              {files.map((f, i) => (
                <div key={f.name}>
                  <FileCheck2 size={22} />
                  <span>
                    <b>{f.name}</b>
                    <small>{f.size}</small>
                    <small className="break-url">{f.checksum}</small>
                  </span>
                  {session.canExport &&
                    (demoMode ? (
                      <Button
                        variant="secondary"
                        onClick={
                          i === 0
                            ? exportPreview
                            : () =>
                                download(
                                  f.name,
                                  JSON.stringify(
                                    { ...ds, checksum: null, synthetic: true },
                                    null,
                                    2,
                                  ),
                                  'application/json',
                                )
                        }
                      >
                        <Download size={15} />
                        Unduh
                      </Button>
                    ) : safeExternal(f.url) ? (
                      <a
                        className="button secondary"
                        href={safeExternal(f.url)}
                        download
                        rel="noreferrer"
                      >
                        Unduh
                      </a>
                    ) : (
                      <span>Belum tersedia</span>
                    ))}
                </div>
              ))}
            </div>
            {!session.canExport && <Notice>Peran Anda belum memiliki izin ekspor.</Notice>}
          </>
        )}
      </div>
      <div className="dataset-footer">
        <span>
          <FileCheck2 size={16} />
          Dataset siap diperiksa, training tetap terpisah.
        </span>
        <Button disabled={!canHandoff} onClick={() => setHandoffDialog(true)}>
          Siapkan untuk NLP
          <ArrowRight size={16} />
        </Button>
      </div>
      {!canHandoff && session.role === 'operator' && (
        <p className="blocked-handoff">
          {!ds.rows
            ? 'Dataset kosong tidak dapat disiapkan untuk NLP.'
            : 'Skema dataset ini belum didukung adapter NLP.'}
        </p>
      )}
      <Dialog open={!!selected} onClose={() => setSelected(null)} title="Konteks sumber">
        {selected && (
          <div className="source-detail">
            <Badge status="COMPLETED">{selected.kind}</Badge>
            <h3>{selected.context}</h3>
            <blockquote>{selected.text}</blockquote>
            <p>
              {selected.role} · {dateTime(selected.date)}
            </p>
            <p className="field-hint">{selected.flag}</p>
            {selected.url && safeExternal(selected.url) && (
              <a href={safeExternal(selected.url)} target="_blank" rel="noreferrer">
                Buka sumber
                <ArrowUpRight size={15} />
              </a>
            )}
          </div>
        )}
      </Dialog>
      <Dialog
        open={handoffDialog}
        onClose={() => setHandoffDialog(false)}
        title="Siapkan input NLP"
      >
        <p>
          Gunakan dataset <b>{ds.id}</b> versi {ds.version} dengan skema {ds.schema}. Tindakan ini
          menyimpan referensi; tidak memulai training atau mengganti Dashboard.
        </p>
        {demoMode && <Notice>Pilihan ini juga merupakan simulasi.</Notice>}
        {ds.partial && (
          <label className="checkbox-line acceptance">
            <input type="checkbox" checked={accept} onChange={(e) => setAccept(e.target.checked)} />
            Saya menerima penggunaan dataset parsial ini.
          </label>
        )}
        <div className="dialog-actions">
          <Button variant="secondary" onClick={() => setHandoffDialog(false)}>
            Kembali
          </Button>
          <Button
            loading={handoff.isPending}
            disabled={ds.partial && !accept}
            onClick={() => handoff.mutate()}
          >
            Simpan pilihan input
          </Button>
        </div>
      </Dialog>
    </section>
  );
}
