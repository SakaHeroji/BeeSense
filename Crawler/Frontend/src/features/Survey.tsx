import { flushSync } from 'react-dom';
import { useClock } from '../shared/hooks';
import { useRef, useState, type ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import Papa from 'papaparse';
import { ArrowRight, Download, FileSpreadsheet, UploadCloud } from 'lucide-react';
import { api } from '../shared/api';
import { demoMode, download, isoWib, number } from '../shared/domain';
import {
  surveyFields,
  type SurveyAnswer,
  type SurveyField,
  type SurveyReview,
} from '../shared/types';
import { Button, Field, Notice, Stepper, UnsavedGuard } from '../shared/ui';
import { useApp } from '../shared/context';

const labels: Record<SurveyField, string> = {
  survey_id: 'ID survei',
  survey_version: 'Versi survei',
  response_id: 'ID respons',
  respondent_code: 'Kode responden',
  respondent_role: 'Peran responden',
  submitted_at: 'Waktu pengisian',
  question_id: 'ID pertanyaan',
  answer_text: 'Jawaban teks',
  answer_value: 'Nilai/skala',
  usage_permission: 'Izin pemanfaatan',
  source_reference: 'Referensi sumber',
};
const sample = [
  surveyFields.join(','),
  'minat-studi,1,DEMO-001,RESP-001,prospective_student,2026-10-29T10:00:00+07:00,Q01,Saya memilih jurusan sesuai minat,,granted,pengumpulan-sintetis',
  'minat-studi,1,DEMO-001,RESP-001,prospective_student,2026-10-29T10:00:00+07:00,Q02,,4,granted,pengumpulan-sintetis',
].join('\n');
type WorkbookData = { names: string[]; readSheet: (name: string) => string[][] };
export default function Survey() {
  const now = useClock();
  const { cap, notify } = useApp();
  const navigate = useNavigate();
  const client = useQueryClient();
  const [method, setMethod] = useState<'form' | 'file'>('form'),
    [dirty, setDirty] = useState(false),
    [error, setError] = useState(''),
    [review, setReview] = useState<SurveyReview | null>(null),
    [accept, setAccept] = useState(false),
    [key, setKey] = useState(() => crypto.randomUUID());
  const [form, setForm] = useState({
    response_id: crypto.randomUUID(),
    respondent_code: '',
    respondent_role: '',
    submitted_at: '',
    source_reference: '',
    usage_permission: '',
    text: '',
    scale: '',
  });
  const [headers, setHeaders] = useState<string[]>([]),
    [data, setData] = useState<string[][]>([]),
    [mapping, setMapping] = useState<Record<string, string>>({}),
    [book, setBook] = useState<WorkbookData | null>(null),
    [sheet, setSheet] = useState(''),
    [fileName, setFileName] = useState(''),
    [reading, setReading] = useState(false);
  const revision = useRef(0);
  const resetReview = () => {
    revision.current++;
    setReview(null);
    setAccept(false);
    setError('');
    setKey(crypto.randomUUID());
    setDirty(true);
  };
  const change = (k: keyof typeof form, value: string) => {
    setForm({ ...form, [k]: value });
    resetReview();
  };
  const applyRows = (rows: string[][]) => {
    if (!rows.length || rows.length < 2)
      throw new Error('File perlu header dan minimal satu baris jawaban.');
    if (rows.length - 1 > cap.limits.maxRows)
      throw new Error(`Maksimum ${number(cap.limits.maxRows)} baris jawaban.`);
    const hs = rows[0].map((v) => String(v).trim());
    if (hs.some((h) => !h) || new Set(hs).size !== hs.length)
      throw new Error('Header tidak boleh kosong atau berulang.');
    setHeaders(hs);
    setData(rows.slice(1));
    setMapping(Object.fromEntries(surveyFields.map((f) => [f, hs.includes(f) ? f : ''])));
  };
  async function readFile(event: ChangeEvent<HTMLInputElement>) {
    const f = event.target.files?.[0];
    if (!f) return;
    resetReview();
    setHeaders([]);
    setData([]);
    setBook(null);
    setSheet('');
    setFileName(f.name);
    if (f.size > cap.limits.maxFileBytes) {
      setError('Ukuran maksimum file 10 MB.');
      return;
    }
    if (!/\.(csv|xlsx)$/i.test(f.name)) {
      setError('Gunakan CSV UTF-8 atau XLSX tanpa macro.');
      return;
    }
    setReading(true);
    try {
      if (/\.csv$/i.test(f.name)) {
        const parsed = Papa.parse<string[]>(await f.text(), {
          skipEmptyLines: 'greedy',
          preview: cap.limits.maxRows + 2,
        });
        if (parsed.errors.length)
          throw new Error(
            'CSV tidak dapat dibaca. Periksa delimiter, tanda kutip, dan encoding UTF-8.',
          );
        applyRows(parsed.data);
      } else {
        const xlsx = await import('xlsx');
        const array = await f.arrayBuffer();
        const wb = xlsx.read(array, {
          type: 'array',
          sheetRows: cap.limits.maxRows + 2,
          cellFormula: false,
          cellHTML: false,
          cellDates: false,
          bookVBA: false,
        });
        const workbook = {
          names: wb.SheetNames,
          readSheet: (name: string) =>
            xlsx.utils.sheet_to_json<string[]>(wb.Sheets[name], {
              header: 1,
              raw: false,
              defval: '',
              blankrows: false,
            }),
        };
        setBook(workbook);
        if (wb.SheetNames.length === 1) {
          setSheet(wb.SheetNames[0]);
          applyRows(workbook.readSheet(wb.SheetNames[0]));
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Berkas tidak dapat dibaca.');
    } finally {
      setReading(false);
      event.target.value = '';
    }
  }
  const buildRows = (): SurveyAnswer[] => {
    if (method === 'form') {
      const common = {
        survey_id: 'minat-studi',
        survey_version: '1',
        response_id: form.response_id,
        respondent_code: form.respondent_code.trim(),
        respondent_role: form.respondent_role,
        submitted_at: form.submitted_at ? isoWib(form.submitted_at) : '',
        usage_permission: form.usage_permission,
        source_reference: form.source_reference.trim(),
      };
      return [
        { ...common, question_id: 'Q01', answer_text: form.text, answer_value: '' },
        { ...common, question_id: 'Q02', answer_text: '', answer_value: form.scale },
      ];
    }
    if (
      !data.length ||
      surveyFields
        .filter((f) => !['answer_text', 'answer_value'].includes(f))
        .some((f) => !mapping[f])
    )
      throw new Error('Petakan seluruh field wajib sebelum validasi.');
    return data.map(
      (row) =>
        Object.fromEntries(
          surveyFields.map((field) => [
            field,
            mapping[field] ? String(row[headers.indexOf(mapping[field])] || '').trim() : '',
          ]),
        ) as SurveyAnswer,
    );
  };
  const validate = useMutation({
    mutationFn: (request: { rows: SurveyAnswer[]; revision: number }) =>
      api.validateSurvey(request.rows),
    onSuccess: (result, request) => {
      if (request.revision !== revision.current) return;
      setReview(result);
      setAccept(false);
    },
    onError: (e) => setError(e.message),
  });
  const commit = useMutation({
    mutationFn: () => api.commitSurvey(review!, key),
    onSuccess: (j) => {
      flushSync(() => setDirty(false));
      client.setQueryData(['job', j.id], j);
      void client.invalidateQueries({ queryKey: ['jobs'] });
      notify('Respons valid tersimpan sebagai batch baru.');
      navigate(`/crawler/manual/jobs/${j.id}`);
    },
    onError: (e) => {
      setError(e.message);
      setReview(null);
    },
  });
  const excluded = review ? review.totalResponses - review.validResponses : 0;
  return (
    <>
      <UnsavedGuard dirty={dirty && !commit.isSuccess && !commit.isPending} />
      <div className="configuration-layout">
        <section className="panel padded">
          <div className="form-section-title first">
            <h2>Suara calon mahasiswa dan orang tua</h2>
            <p>
              Masukkan respons yang telah dikumpulkan. Pertanyaan dan peran responden ikut terjaga.
            </p>
          </div>
          <div className="segmented" aria-label="Cara input survei">
            <button
              className={method === 'form' ? 'active' : ''}
              onClick={() => {
                if (
                  !dirty ||
                  window.confirm(
                    'Ganti cara input? Review dibatalkan; masukan tetap berada pada formulir ini.',
                  )
                ) {
                  setMethod('form');
                  resetReview();
                }
              }}
            >
              Input formulir
            </button>
            <button
              className={method === 'file' ? 'active' : ''}
              onClick={() => {
                if (
                  !dirty ||
                  window.confirm(
                    'Ganti cara input? Review dibatalkan; masukan tetap berada pada formulir ini.',
                  )
                ) {
                  setMethod('file');
                  resetReview();
                }
              }}
            >
              <FileSpreadsheet size={16} />
              Impor file
            </button>
          </div>
          {demoMode && (
            <Notice>
              Gunakan respons sintetis. Jawaban pada simulasi hanya berada di memori dan hilang
              setelah refresh.
            </Notice>
          )}
          {error && <Notice tone="error">{error}</Notice>}
          {method === 'form' ? (
            <>
              <div className="template-label">
                <ClipboardTemplate />
                <span>
                  Minat studi <small>Template minat-studi · versi 1 · Q01 & Q02 wajib</small>
                </span>
              </div>
              <p className="field-hint">
                Field bertanda * wajib diisi. Kode responden menggunakan pseudonim, bukan identitas
                pribadi.
              </p>
              <div className="form-grid">
                <Field label="Peran responden" required>
                  {(id) => (
                    <select
                      id={id}
                      value={form.respondent_role}
                      onChange={(e) => change('respondent_role', e.target.value)}
                    >
                      <option value="">Pilih sesuai sumber</option>
                      <option value="prospective_student">Calon mahasiswa</option>
                      <option value="parent">Orang tua</option>
                    </select>
                  )}
                </Field>
                <Field
                  label="Kode responden"
                  required
                  hint="Contoh: RESP-001, bukan nama/nomor telepon."
                >
                  {(id) => (
                    <input
                      id={id}
                      value={form.respondent_code}
                      onChange={(e) => change('respondent_code', e.target.value)}
                      maxLength={100}
                    />
                  )}
                </Field>
                <Field label="ID respons" required hint="ID stabil untuk satu pengisian survei.">
                  {(id) => (
                    <input
                      id={id}
                      value={form.response_id}
                      onChange={(e) => change('response_id', e.target.value)}
                      maxLength={100}
                    />
                  )}
                </Field>
                <Field label="Waktu pengisian (WIB)" required>
                  {(id) => (
                    <input
                      id={id}
                      type="datetime-local"
                      value={form.submitted_at}
                      onChange={(e) => change('submitted_at', e.target.value)}
                    />
                  )}
                </Field>
                <Field label="Referensi sumber" required>
                  {(id) => (
                    <input
                      id={id}
                      value={form.source_reference}
                      onChange={(e) => change('source_reference', e.target.value)}
                      placeholder="Kode pengumpulan internal"
                      maxLength={200}
                    />
                  )}
                </Field>
                <Field label="Izin pemanfaatan" required>
                  {(id) => (
                    <select
                      id={id}
                      value={form.usage_permission}
                      onChange={(e) => change('usage_permission', e.target.value)}
                    >
                      <option value="">Pilih status dari sumber</option>
                      <option value="granted">Diberikan</option>
                      <option value="not_granted">Tidak diberikan</option>
                      <option value="unknown">Belum diketahui</option>
                    </select>
                  )}
                </Field>
              </div>
              <div className="question-block">
                <span>Q01 · Jawaban teks</span>
                <Field label="Apa pertimbangan utama memilih jurusan?" required>
                  {(id) => (
                    <textarea
                      id={id}
                      rows={4}
                      maxLength={10000}
                      value={form.text}
                      onChange={(e) => change('text', e.target.value)}
                    />
                  )}
                </Field>
              </div>
              <div className="question-block">
                <span>Q02 · Skala 1–5</span>
                <Field
                  label="Seberapa penting biaya kuliah?"
                  required
                  hint="1 = tidak penting, 5 = sangat penting."
                >
                  {(id) => (
                    <select
                      id={id}
                      value={form.scale}
                      onChange={(e) => change('scale', e.target.value)}
                    >
                      <option value="">Pilih nilai</option>
                      {[1, 2, 3, 4, 5].map((n) => (
                        <option value={n} key={n}>
                          {n}
                        </option>
                      ))}
                    </select>
                  )}
                </Field>
              </div>
            </>
          ) : (
            <>
              <Stepper
                steps={['File', 'Mapping', 'Review']}
                active={review ? 2 : headers.length ? 1 : 0}
              />
              <div className="upload-zone">
                <UploadCloud size={31} />
                <h3>Pilih file respons survei</h3>
                <p>CSV UTF-8 / XLSX · maks. 10 MB · 10.000 baris jawaban</p>
                <label className="button secondary" htmlFor="survey-file">
                  {reading ? 'Membaca file…' : 'Pilih berkas'}
                </label>
                <input
                  id="survey-file"
                  type="file"
                  accept=".csv,.xlsx"
                  disabled={reading}
                  onChange={(e) => void readFile(e)}
                  className="sr-only"
                />
                <span>{fileName || 'Satu baris = satu jawaban untuk satu pertanyaan'}</span>
              </div>
              <Button
                variant="ghost"
                onClick={() => download('template-survei-sintetis.csv', sample)}
              >
                <Download size={16} />
                Unduh template sintetis
              </Button>
              {book && (
                <Field label="Pilih sheet" required>
                  {(id) => (
                    <select
                      id={id}
                      value={sheet}
                      onChange={(e) => {
                        setSheet(e.target.value);
                        setHeaders([]);
                        setData([]);
                        resetReview();
                        try {
                          if (e.target.value) applyRows(book.readSheet(e.target.value));
                        } catch (e) {
                          setError((e as Error).message);
                        }
                      }}
                    >
                      <option value="">Pilih satu sheet</option>
                      {book.names.map((n) => (
                        <option key={n}>{n}</option>
                      ))}
                    </select>
                  )}
                </Field>
              )}
              {!!headers.length && (
                <>
                  <div className="form-section-title">
                    <h3>Petakan kolom sumber</h3>
                    <p>
                      {number(data.length)} baris jawaban terbaca. Kolom wajib harus terpetakan
                      sebelum validasi.
                    </p>
                  </div>
                  <div className="table-scroll">
                    <table>
                      <thead>
                        <tr>
                          <th>Field tujuan</th>
                          <th>Kolom sumber</th>
                          <th>Contoh nilai</th>
                        </tr>
                      </thead>
                      <tbody>
                        {surveyFields.map((f) => (
                          <tr key={f}>
                            <td>
                              {labels[f]}{' '}
                              {!['answer_text', 'answer_value'].includes(f) && (
                                <span className="required">*</span>
                              )}
                            </td>
                            <td>
                              <select
                                aria-label={`Mapping ${f}`}
                                value={mapping[f] || ''}
                                onChange={(e) => {
                                  setMapping({ ...mapping, [f]: e.target.value });
                                  resetReview();
                                }}
                              >
                                <option value="">Tidak dipetakan</option>
                                {headers.map((h) => (
                                  <option key={h}>{h}</option>
                                ))}
                              </select>
                            </td>
                            <td className="mapping-example">
                              {mapping[f]
                                ? data[0]?.[headers.indexOf(mapping[f])] || 'Kosong'
                                : '—'}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </>
              )}
            </>
          )}
          <div className="form-actions">
            <Button
              variant={review ? 'secondary' : 'primary'}
              loading={validate.isPending}
              disabled={reading || (method === 'file' && !data.length)}
              onClick={() => {
                setError('');
                try {
                  validate.mutate({ rows: buildRows(), revision: revision.current });
                } catch (e) {
                  setError((e as Error).message);
                }
              }}
            >
              Validasi {method === 'form' ? 'respons' : 'data survei'}
              <ArrowRight size={16} />
            </Button>
          </div>
          {review && (
            <div className="survey-review">
              <h3>Hasil pemeriksaan respons</h3>
              <div className="review-counts">
                <span>
                  <b>{review.totalResponses}</b> total respons
                </span>
                <span>
                  <b>{review.validResponses}</b> valid
                </span>
                <span>
                  <b>{review.duplicateResponses}</b> duplikat
                </span>
                <span>
                  <b>{review.invalidResponses}</b> invalid
                </span>
                <span>
                  <b>{review.deniedResponses}</b> tanpa izin
                </span>
              </div>
              <p className="field-hint">
                {number(review.answerRows)} baris jawaban. Respons dengan pertanyaan wajib invalid
                ditahan seluruhnya.
              </p>
              {!!review.issues.length && (
                <div className="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>Baris/Respons</th>
                        <th>Field</th>
                        <th>Perbaikan</th>
                      </tr>
                    </thead>
                    <tbody>
                      {review.issues.slice(0, 100).map((issue, i) => (
                        <tr key={i}>
                          <td>
                            {issue.row}
                            <small>{issue.responseId}</small>
                          </td>
                          <td>{labels[issue.field as SurveyField] || issue.field}</td>
                          <td>{issue.message}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {review.issues.length > 100 && (
                    <p>
                      Menampilkan 100 error pertama dari {number(review.issues.length)} error.
                      Perbaiki file lalu validasi ulang.
                    </p>
                  )}
                </div>
              )}
              {excluded > 0 && (
                <label className="checkbox-line acceptance">
                  <input
                    type="checkbox"
                    checked={accept}
                    onChange={(e) => setAccept(e.target.checked)}
                  />
                  Saya memahami {excluded} respons tidak dimasukkan.
                </label>
              )}
              <div className="form-actions">
                <Button
                  loading={commit.isPending}
                  disabled={
                    !review.validResponses ||
                    (excluded > 0 && !accept) ||
                    Date.parse(review.expiresAt) <= now
                  }
                  onClick={() => commit.mutate()}
                >
                  {method === 'form'
                    ? 'Simpan respons'
                    : `Impor ${review.validResponses} respons valid`}
                  <ArrowRight size={16} />
                </Button>
              </div>
            </div>
          )}
        </section>
        <aside className="plan-aside">
          <div className="plan-summary">
            <span className="summary-icon">
              <FileSpreadsheet size={23} />
            </span>
            <h2>Setiap suara punya konteks</h2>
            <p>Bedakan responden, respons, dan jawaban.</p>
            <div className="survey-guide">
              <b>Responden</b>
              <p>Calon mahasiswa atau orang tua, sesuai deklarasi pada sumber.</p>
              <b>Respons</b>
              <p>Satu pengisian survei dengan ID yang tetap.</p>
              <b>Jawaban</b>
              <p>Isi satu pertanyaan dalam sebuah respons.</p>
            </div>
          </div>
          <div className="context-note">
            <h3>Siap diperiksa, sebelum dianalisis</h3>
            <p>
              Hanya respons valid dengan izin pemanfaatan yang masuk dataset analisis. Training
              dijalankan terpisah di modul NLP.
            </p>
          </div>
        </aside>
      </div>
    </>
  );
}
function ClipboardTemplate() {
  return <FileSpreadsheet size={22} />;
}
