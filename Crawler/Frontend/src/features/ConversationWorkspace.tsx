import { useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  ArrowLeft,
  Bot,
  CalendarDays,
  CheckCircle2,
  Download,
  FilePenLine,
  FileSpreadsheet,
  Library,
  Plus,
  Save,
  Search,
  Sparkles,
  Target,
  Upload,
} from 'lucide-react';
import { api } from '../shared/api';
import { FieldErrorsContext, useApp } from '../shared/context';
import {
  dateTime,
  emptyConversationDraft,
  isoWib,
  number,
  queryLines,
  validateConversation,
} from '../shared/domain';
import type { Conversation, ConversationDraft, FieldError } from '../shared/types';
import {
  conversationPrompt,
  parseConversationWorkbook,
  promptFilename,
} from '../shared/conversation-workbook';
import { Button, Errors, Field, Notice, Spinner, UnsavedGuard } from '../shared/ui';

const cloneDraft = (conversation: Conversation): ConversationDraft => structuredClone(conversation);

export default function ConversationWorkspace() {
  const { cap, session, notify } = useApp();
  const client = useQueryClient();
  const conversations = useQuery({ queryKey: ['conversations'], queryFn: api.conversations });
  const [view, setView] = useState<'library' | 'editor'>('library');
  const [selectedId, setSelectedId] = useState('');
  const [draft, setDraft] = useState<ConversationDraft>(() => emptyConversationDraft());
  const [dirty, setDirty] = useState(false);
  const [errors, setErrors] = useState<FieldError[]>([]);
  const uploadRef = useRef<HTMLInputElement>(null);
  const selected = conversations.data?.find((conversation) => conversation.id === selectedId);
  const change = (next: ConversationDraft) => {
    setDraft(next);
    setDirty(true);
    setErrors([]);
  };
  const field = <K extends keyof ConversationDraft>(name: K, value: ConversationDraft[K]) =>
    change({ ...draft, [name]: value });
  const relevance = <K extends keyof ConversationDraft['relevance']>(
    name: K,
    value: ConversationDraft['relevance'][K],
  ) => change({ ...draft, relevance: { ...draft.relevance, [name]: value } });
  const generate = useMutation({
    mutationFn: () => api.generateConversation(draft.title),
    onSuccess: (generated) => {
      setDraft(generated);
      setSelectedId('');
      setDirty(true);
      setErrors([]);
      notify('Draf conversation dibuat dari judul. Tinjau seluruh isi sebelum menyimpan.');
    },
    onError: (error) => notify(error.message),
  });
  const save = useMutation({
    mutationFn: (value: ConversationDraft) => api.saveConversation(value),
    onSuccess: (saved) => {
      client.setQueryData<Conversation[]>(['conversations'], (current = []) => [
        saved,
        ...current.filter((conversation) => conversation.id !== saved.id),
      ]);
      setSelectedId(saved.id);
      setDraft(cloneDraft(saved));
      setDirty(false);
      setErrors([]);
      setView('library');
      notify(`Conversation “${saved.title}” disimpan sebagai versi ${saved.version}.`);
    },
    onError: (error) => notify(error.message),
  });
  const submit = (event: React.FormEvent) => {
    event.preventDefault();
    const issues = validateConversation(draft, cap);
    setErrors(issues);
    if (!issues.length) save.mutate(draft);
  };
  const edit = (conversation: Conversation) => {
    setSelectedId(conversation.id);
    setDraft(cloneDraft(conversation));
    setDirty(false);
    setErrors([]);
    setView('editor');
  };
  const create = () => {
    setSelectedId('');
    setDraft(emptyConversationDraft());
    setDirty(false);
    setErrors([]);
    setView('editor');
  };
  const returnToLibrary = () => {
    if (dirty && !window.confirm('Perubahan conversation belum disimpan. Kembali ke tabel?'))
      return;
    setDirty(false);
    setErrors([]);
    setView('library');
  };
  const downloadPrompt = () => {
    const blob = new Blob([conversationPrompt(draft.title)], {
      type: 'text/markdown;charset=utf-8',
    });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = promptFilename(draft.title);
    anchor.click();
    URL.revokeObjectURL(url);
    notify('Prompt Markdown diunduh. Gunakan untuk membuat workbook Excel sesuai kontrak.');
  };
  const importWorkbook = useMutation({
    mutationFn: async (file: File) => {
      if (!/\.xlsx$/i.test(file.name)) throw new Error('Pilih file Excel dengan ekstensi .xlsx.');
      if (file.size > cap.limits.maxFileBytes)
        throw new Error(`Ukuran file melebihi ${number(cap.limits.maxFileBytes / 1048576)} MB.`);
      const imported = await parseConversationWorkbook(await file.arrayBuffer(), draft);
      const issues = validateConversation(imported, cap);
      if (issues.length) {
        setDraft(imported);
        setDirty(true);
        setErrors(issues);
        throw new Error('Workbook dibaca, tetapi beberapa field belum valid. Periksa form.');
      }
      return api.saveConversation(imported);
    },
    onSuccess: (saved) => {
      client.setQueryData<Conversation[]>(['conversations'], (current = []) => [
        saved,
        ...current.filter((conversation) => conversation.id !== saved.id),
      ]);
      setSelectedId(saved.id);
      setDraft(cloneDraft(saved));
      setDirty(false);
      setErrors([]);
      setView('library');
      notify(
        `Workbook dibaca dan Conversation “${saved.title}” disimpan sebagai versi ${saved.version}.`,
      );
    },
    onError: (error) => notify(error.message),
  });
  return (
    <>
      <UnsavedGuard dirty={dirty} />
      <header className="conversation-page-heading">
        <div>
          <span className="page-kicker">Pusat konteks riset</span>
          <h1 id="main-title" tabIndex={-1}>
            Conversation
          </h1>
          <p>
            Susun konteks sekali, lalu gunakan snapshot yang sama saat crawling satu platform atau
            beberapa platform sekaligus.
          </p>
        </div>
        {view === 'library' && session.role === 'operator' && (
          <Button variant="secondary" onClick={create}>
            <Plus size={17} aria-hidden="true" /> Conversation baru
          </Button>
        )}
        {view === 'editor' && (
          <Button variant="secondary" onClick={returnToLibrary}>
            <ArrowLeft size={17} aria-hidden="true" /> Kembali ke tabel
          </Button>
        )}
      </header>
      {session.role !== 'operator' && (
        <Notice>
          Anda dapat melihat conversation. Pembuatan dan perubahan hanya untuk operator.
        </Notice>
      )}
      {view === 'library' ? (
        <section
          className="panel conversation-library"
          aria-labelledby="conversation-library-title"
        >
          <div className="conversation-library-heading">
            <Library size={19} aria-hidden="true" />
            <div>
              <h2 id="conversation-library-title">Tabel conversation</h2>
              <p>
                {number(conversations.data?.length || 0)} conversation tersedia. Buka satu baris
                untuk melihat atau membuat versi baru.
              </p>
            </div>
          </div>
          {conversations.isPending ? (
            <div className="conversation-library-state" role="status">
              <Spinner /> Memuat conversation…
            </div>
          ) : conversations.error ? (
            <Notice tone="error">{conversations.error.message}</Notice>
          ) : !conversations.data?.length ? (
            <div className="conversation-library-state">
              <p>Belum ada conversation.</p>
              {session.role === 'operator' && (
                <Button variant="secondary" onClick={create}>
                  Buat conversation pertama
                </Button>
              )}
            </div>
          ) : (
            <>
              <p className="conversation-table-hint">Geser tabel untuk melihat kolom lain.</p>
              <div
                className="conversation-table-scroll"
                tabIndex={0}
                aria-label="Tabel conversation"
              >
                <table className="conversation-table">
                  <caption className="sr-only">Conversation riset yang tersedia</caption>
                  <thead>
                    <tr>
                      <th scope="col">Judul</th>
                      <th scope="col">Sumber</th>
                      <th scope="col">Discovery</th>
                      <th scope="col">Versi</th>
                      <th scope="col">Diperbarui</th>
                      <th scope="col">Tindakan</th>
                    </tr>
                  </thead>
                  <tbody>
                    {conversations.data.map((conversation) => (
                      <tr key={conversation.id}>
                        <th scope="row">
                          <span className={`conversation-card-icon ${conversation.origin}`}>
                            {conversation.origin === 'gemini' ? (
                              <Bot size={18} aria-hidden="true" />
                            ) : conversation.origin === 'excel' ? (
                              <FileSpreadsheet size={18} aria-hidden="true" />
                            ) : (
                              <FilePenLine size={18} aria-hidden="true" />
                            )}
                          </span>
                          <span>{conversation.title}</span>
                        </th>
                        <td>
                          {conversation.origin === 'gemini'
                            ? 'Gemini'
                            : conversation.origin === 'excel'
                              ? 'Excel'
                              : 'Manual'}
                        </td>
                        <td>{number(queryLines(conversation.queries).length)} query</td>
                        <td>v{conversation.version}</td>
                        <td>{dateTime(conversation.updatedAt)}</td>
                        <td>
                          <Button variant="secondary" onClick={() => edit(conversation)}>
                            {session.role === 'operator' ? 'Buka form' : 'Lihat'}
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </section>
      ) : (
        <section className="panel conversation-editor" aria-labelledby="conversation-editor-title">
          <div className="conversation-editor-heading">
            <div>
              <span className={`conversation-origin ${draft.origin}`}>
                {draft.origin === 'gemini' ? (
                  <Bot size={14} aria-hidden="true" />
                ) : draft.origin === 'excel' ? (
                  <FileSpreadsheet size={14} aria-hidden="true" />
                ) : (
                  <FilePenLine size={14} aria-hidden="true" />
                )}
                {draft.origin === 'gemini'
                  ? 'Draf Gemini'
                  : draft.origin === 'excel'
                    ? 'Import Excel'
                    : 'Manual'}
              </span>
              <h2 id="conversation-editor-title">
                {selected ? 'Edit conversation' : 'Buat conversation'}
              </h2>
              <p>
                Generator hanya menerima judul. Isi hasilnya tetap harus ditinjau sebelum disimpan.
              </p>
            </div>
            {selected && <span className="conversation-version">v{selected.version}</span>}
          </div>
          {session.role === 'operator' ? (
            <FieldErrorsContext.Provider value={errors}>
              <form onSubmit={submit} noValidate>
                <Errors errors={errors} />
                <section
                  className="conversation-form-section"
                  aria-labelledby="conversation-basics-title"
                >
                  <div className="conversation-form-heading">
                    <Sparkles size={18} aria-hidden="true" />
                    <div>
                      <h3 id="conversation-basics-title">Judul & tujuan</h3>
                      <p>Mulai manual atau biarkan Gemini menyiapkan draf dari judul saja.</p>
                    </div>
                  </div>
                  <Field name="conversation.title" label="Judul conversation" required>
                    {(id) => (
                      <input
                        id={id}
                        maxLength={120}
                        value={draft.title}
                        onChange={(event) => field('title', event.target.value)}
                        placeholder="Contoh: Persepsi calon mahasiswa tentang biaya kuliah…"
                      />
                    )}
                  </Field>
                  <div className="conversation-generate-action">
                    <Button
                      variant="secondary"
                      loading={generate.isPending}
                      disabled={!draft.title.trim()}
                      onClick={() => generate.mutate()}
                    >
                      <Bot size={17} aria-hidden="true" /> Generate draf dari judul
                    </Button>
                    <span>Hanya judul yang dikirim ke endpoint generator.</span>
                  </div>
                  <section className="conversation-excel-flow" aria-labelledby="excel-flow-title">
                    <div>
                      <FileSpreadsheet size={20} aria-hidden="true" />
                      <div>
                        <h4 id="excel-flow-title">Siapkan lewat prompt & Excel</h4>
                        <p>
                          Unduh prompt dari judul, minta AI membuat workbook sesuai kontrak, lalu
                          upload untuk divalidasi dan langsung disimpan.
                        </p>
                      </div>
                    </div>
                    <ol>
                      <li>
                        <span>1</span>
                        <div>
                          <b>Unduh prompt Markdown</b>
                          <small>Berisi nama sheet, header, tipe data, dan aturan relevansi.</small>
                        </div>
                        <Button
                          variant="secondary"
                          disabled={!draft.title.trim()}
                          onClick={downloadPrompt}
                        >
                          <Download size={17} aria-hidden="true" /> Unduh prompt .md
                        </Button>
                      </li>
                      <li>
                        <span>2</span>
                        <div>
                          <b>Upload workbook hasil AI</b>
                          <small>
                            Hanya .xlsx, maksimal {number(cap.limits.maxFileBytes / 1048576)} MB.
                          </small>
                        </div>
                        <input
                          ref={uploadRef}
                          hidden
                          type="file"
                          aria-label="Upload workbook Conversation"
                          accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                          onChange={(event) => {
                            const file = event.target.files?.[0];
                            if (file) importWorkbook.mutate(file);
                            event.target.value = '';
                          }}
                        />
                        <Button
                          variant="secondary"
                          loading={importWorkbook.isPending}
                          onClick={() => uploadRef.current?.click()}
                        >
                          <Upload size={17} aria-hidden="true" /> Upload & simpan
                        </Button>
                      </li>
                    </ol>
                    <p className="conversation-excel-note">
                      Rentang publikasi tetap memakai nilai pada form. Workbook mengisi tujuan,
                      keyword, query, hashtag, subreddit, scope, threshold, dan contoh relevansi.
                    </p>
                  </section>
                  <Field name="conversation.objective" label="Tujuan riset" required>
                    {(id) => (
                      <textarea
                        id={id}
                        rows={3}
                        maxLength={600}
                        value={draft.objective}
                        onChange={(event) => field('objective', event.target.value)}
                        placeholder="Jelaskan keputusan atau pertanyaan yang ingin dipahami…"
                      />
                    )}
                  </Field>
                </section>
                <section
                  className="conversation-form-section"
                  aria-labelledby="conversation-discovery-title"
                >
                  <div className="conversation-form-heading">
                    <Search size={18} aria-hidden="true" />
                    <div>
                      <h3 id="conversation-discovery-title">Discovery & keyword</h3>
                      <p>Sumber yang berbeda menerjemahkan input ini sesuai kemampuannya.</p>
                    </div>
                  </div>
                  <fieldset className="social-fieldset">
                    <legend>
                      <CalendarDays size={17} aria-hidden="true" /> Rentang publikasi
                    </legend>
                    <div className="form-grid">
                      <Field name="conversation.dates" label="Dari tanggal" required>
                        {(id) => (
                          <input
                            id={id}
                            type="datetime-local"
                            value={draft.since}
                            onChange={(event) => field('since', event.target.value)}
                          />
                        )}
                      </Field>
                      <Field name="conversation.dates" label="Sampai sebelum tanggal" required>
                        {(id) => (
                          <input
                            id={id}
                            type="datetime-local"
                            value={draft.until}
                            onChange={(event) => field('until', event.target.value)}
                          />
                        )}
                      </Field>
                    </div>
                  </fieldset>
                  <div className="form-grid">
                    <Field
                      name="conversation.include"
                      label="Include keywords"
                      hint="Satu kata atau frasa per baris."
                    >
                      {(id) => (
                        <textarea
                          id={id}
                          rows={5}
                          value={draft.include}
                          onChange={(event) => field('include', event.target.value)}
                          placeholder="Satu keyword per baris…"
                        />
                      )}
                    </Field>
                    <Field
                      name="conversation.exclude"
                      label="Exclude keywords"
                      hint="Konten yang cocok akan dilewati."
                    >
                      {(id) => (
                        <textarea
                          id={id}
                          rows={5}
                          value={draft.exclude}
                          onChange={(event) => field('exclude', event.target.value)}
                          placeholder="Satu keyword pengecualian per baris…"
                        />
                      )}
                    </Field>
                  </div>
                  <Field
                    name="conversation.includeMode"
                    label="Pencocokan include keyword"
                    hint="Pilih apakah satu keyword cukup atau seluruh keyword harus cocok."
                  >
                    {(id) => (
                      <select
                        id={id}
                        value={draft.includeMode}
                        onChange={(event) =>
                          field(
                            'includeMode',
                            event.target.value as ConversationDraft['includeMode'],
                          )
                        }
                      >
                        <option value="any">Salah satu keyword</option>
                        <option value="all">Semua keyword</option>
                      </select>
                    )}
                  </Field>
                  <Field name="conversation.queries" label="Query discovery" required>
                    {(id) => (
                      <textarea
                        id={id}
                        rows={5}
                        value={draft.queries}
                        onChange={(event) => field('queries', event.target.value)}
                        placeholder="Satu query pencarian per baris…"
                        spellCheck={false}
                      />
                    )}
                  </Field>
                  <div className="form-grid">
                    <Field name="conversation.hashtags" label="Hashtag">
                      {(id) => (
                        <textarea
                          id={id}
                          rows={4}
                          value={draft.hashtags}
                          onChange={(event) => field('hashtags', event.target.value)}
                          placeholder="Satu hashtag per baris…"
                          spellCheck={false}
                        />
                      )}
                    </Field>
                    <Field name="conversation.subreddits" label="Subreddit">
                      {(id) => (
                        <textarea
                          id={id}
                          rows={4}
                          value={draft.subreddits}
                          onChange={(event) => field('subreddits', event.target.value)}
                          placeholder="Satu subreddit per baris…"
                          spellCheck={false}
                        />
                      )}
                    </Field>
                  </div>
                </section>
                <section
                  className="conversation-form-section"
                  aria-labelledby="conversation-relevance-title"
                >
                  <div className="conversation-form-heading">
                    <Target size={18} aria-hidden="true" />
                    <div>
                      <h3 id="conversation-relevance-title">Acuan relevansi</h3>
                      <p>Contoh adalah pedoman klasifikasi, bukan teks yang akan dicari persis.</p>
                    </div>
                  </div>
                  <Field
                    name="conversation.relevance.scope"
                    label="Ruang lingkup relevansi"
                    required
                  >
                    {(id) => (
                      <textarea
                        id={id}
                        rows={3}
                        value={draft.relevance.scope}
                        onChange={(event) => relevance('scope', event.target.value)}
                        placeholder="Konten dianggap relevan ketika…"
                      />
                    )}
                  </Field>
                  <div className="form-grid">
                    <Field
                      name="conversation.relevance.relevant"
                      label="Contoh relevan"
                      required
                      hint="Satu contoh per baris."
                    >
                      {(id) => (
                        <textarea
                          id={id}
                          rows={5}
                          value={draft.relevance.relevantExamples}
                          onChange={(event) => relevance('relevantExamples', event.target.value)}
                          placeholder="Kalimat yang jelas berada dalam ruang lingkup…"
                        />
                      )}
                    </Field>
                    <Field name="conversation.relevance.irrelevant" label="Contoh tidak relevan">
                      {(id) => (
                        <textarea
                          id={id}
                          rows={5}
                          value={draft.relevance.irrelevantExamples}
                          onChange={(event) => relevance('irrelevantExamples', event.target.value)}
                          placeholder="Kalimat di luar ruang lingkup…"
                        />
                      )}
                    </Field>
                  </div>
                  <div className="form-grid conversation-relevance-row">
                    <Field name="conversation.relevance.generic" label="Contoh generik">
                      {(id) => (
                        <textarea
                          id={id}
                          rows={3}
                          value={draft.relevance.genericExamples}
                          onChange={(event) => relevance('genericExamples', event.target.value)}
                          placeholder="Kalimat netral tanpa konteks cukup…"
                        />
                      )}
                    </Field>
                    <Field
                      name="conversation.relevance.threshold"
                      label="Threshold relevansi"
                      hint="0 berarti longgar, 1 paling ketat."
                    >
                      {(id) => (
                        <input
                          id={id}
                          type="number"
                          inputMode="decimal"
                          min={0}
                          max={1}
                          step={0.01}
                          value={draft.relevance.threshold}
                          onChange={(event) =>
                            relevance(
                              'threshold',
                              event.target.value === '' ? Number.NaN : Number(event.target.value),
                            )
                          }
                        />
                      )}
                    </Field>
                  </div>
                </section>
                <div className="conversation-save-bar">
                  <div>
                    <CheckCircle2 size={18} aria-hidden="true" />
                    <span>
                      {draft.origin === 'gemini'
                        ? 'Konten hasil generator harus diverifikasi operator.'
                        : draft.origin === 'excel'
                          ? 'Isi workbook sudah dipetakan ke kontrak Conversation.'
                          : 'Conversation manual akan menjadi sumber konteks crawling.'}
                    </span>
                  </div>
                  <Button type="submit" loading={save.isPending}>
                    <Save size={17} aria-hidden="true" />
                    {selected ? 'Simpan versi baru' : 'Simpan conversation'}
                  </Button>
                </div>
              </form>
            </FieldErrorsContext.Provider>
          ) : selected ? (
            <div className="conversation-readonly">
              <h3>{selected.title}</h3>
              <p>{selected.objective}</p>
              <dl>
                <dt>Rentang publikasi</dt>
                <dd>
                  {dateTime(isoWib(selected.since))} – {dateTime(isoWib(selected.until))}
                </dd>
                <dt>Ruang lingkup</dt>
                <dd>{selected.relevance.scope}</dd>
                <dt>Query</dt>
                <dd>{queryLines(selected.queries).join(', ')}</dd>
              </dl>
            </div>
          ) : (
            <Notice>Pilih conversation pada library untuk melihat detailnya.</Notice>
          )}
        </section>
      )}
    </>
  );
}
