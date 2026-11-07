import type { ConversationDraft } from './types';

type WorkbookRow = Record<string, unknown>;

const text = (value: unknown) => String(value ?? '').trim();
const unique = (values: string[]) => [
  ...new Set(values.map((value) => value.trim()).filter(Boolean)),
];

export function conversationPrompt(title: string): string {
  const cleanTitle = title.trim();
  return `# Prompt generator workbook Conversation BeeSense

## Judul conversation

${cleanTitle}

## Tugas

Buat satu file Excel berformat **.xlsx** untuk menyiapkan discovery keyword dan acuan relevansi Conversation BeeSense berdasarkan judul di atas. Kembalikan file Excel saja, tanpa uraian tambahan. Gunakan Bahasa Indonesia, hindari duplikasi, jangan gunakan formula, macro, hyperlink, atau data tersembunyi.

Workbook wajib memiliki tepat tiga sheet berikut.

### 1. \`conversation\`

Satu baris data dengan header persis:

| title | objective | include_mode | relevance_scope | relevance_threshold |
| --- | --- | --- | --- | --- |

- \`title\`: pertahankan judul di atas.
- \`objective\`: tujuan riset yang operasional dan ringkas.
- \`include_mode\`: hanya \`any\` atau \`all\`.
- \`relevance_scope\`: definisi jelas tentang konten yang dianggap relevan.
- \`relevance_threshold\`: angka desimal 0–1; gunakan nilai yang masuk akal untuk pemetaan percakapan publik.

### 2. \`discovery\`

Header persis \`type\` dan \`value\`. Setiap nilai berada pada baris terpisah. \`type\` hanya boleh berisi:

- \`include_keyword\`: kata/frasa yang wajib dipertimbangkan;
- \`exclude_keyword\`: spam, promosi, atau konteks yang harus dibuang;
- \`query\`: variasi query pencarian natural;
- \`hashtag\`: tanpa awalan tanda pagar;
- \`subreddit\`: tanpa awalan \`r/\`.

Buat cakupan yang cukup beragam untuk berbagai cara pengguna membicarakan topik, termasuk sinonim, kebutuhan, hambatan, keputusan, pengalaman, dan pertanyaan. Jangan menambahkan istilah yang tidak relevan hanya untuk memperbanyak baris.

### 3. \`relevance_examples\`

Header persis \`classification\` dan \`text\`. \`classification\` hanya boleh berisi \`relevant\`, \`generic\`, atau \`irrelevant\`. Buat beberapa contoh kalimat natural untuk setiap kelas. Contoh harus cukup berbeda agar dapat menjadi acuan klasifikasi, bukan sekadar mengganti satu kata.

## Pemeriksaan sebelum menyerahkan file

1. Nama sheet dan header sama persis dengan kontrak di atas.
2. Tidak ada sel gabungan, formula, macro, kolom tambahan, atau baris kosong di tengah data.
3. Semua nilai berupa teks biasa, kecuali \`relevance_threshold\` berupa angka.
4. Workbook dapat dibuka sebagai file .xlsx standar.
`;
}

export function promptFilename(title: string): string {
  const slug = title
    .trim()
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 64);
  return `prompt-conversation-${slug || 'baru'}.md`;
}

export async function parseConversationWorkbook(
  bytes: ArrayBuffer,
  base: ConversationDraft,
): Promise<ConversationDraft> {
  const xlsx = await import('xlsx');
  const workbook = xlsx.read(bytes, { type: 'array' });
  const requiredSheets = new Set(['conversation', 'discovery', 'relevance_examples']);
  const normalizedSheets = workbook.SheetNames.map((name) => name.trim().toLowerCase());
  const extraSheets = normalizedSheets.filter((name) => !requiredSheets.has(name));
  if (extraSheets.length)
    throw new Error(`Workbook memiliki sheet di luar kontrak: ${extraSheets.join(', ')}.`);
  for (const sheet of Object.values(workbook.Sheets)) {
    const formula = Object.values(sheet).find(
      (cell) => typeof cell === 'object' && cell !== null && 'f' in cell,
    );
    if (formula) throw new Error('Workbook tidak boleh memuat formula.');
  }
  const findSheet = (name: string) =>
    workbook.SheetNames.find((candidate) => candidate.trim().toLowerCase() === name);
  const rows = (name: string): WorkbookRow[] => {
    const actual = findSheet(name);
    if (!actual) throw new Error(`Sheet “${name}” tidak ditemukan.`);
    return xlsx.utils.sheet_to_json<WorkbookRow>(workbook.Sheets[actual], {
      defval: '',
      raw: true,
    });
  };

  const metadataRows = rows('conversation');
  if (metadataRows.length !== 1)
    throw new Error('Sheet “conversation” harus berisi tepat satu baris data.');
  const metadata = metadataRows[0];
  const requiredMetadata = [
    'title',
    'objective',
    'include_mode',
    'relevance_scope',
    'relevance_threshold',
  ];
  const missing = requiredMetadata.filter((column) => !(column in metadata));
  if (missing.length) throw new Error(`Kolom conversation belum lengkap: ${missing.join(', ')}.`);

  const includeMode = text(metadata.include_mode).toLowerCase();
  if (includeMode !== 'any' && includeMode !== 'all')
    throw new Error('include_mode harus bernilai “any” atau “all”.');
  const threshold = Number(metadata.relevance_threshold);
  if (!Number.isFinite(threshold) || threshold < 0 || threshold > 1)
    throw new Error('relevance_threshold harus berupa angka antara 0 dan 1.');

  const discovery = rows('discovery');
  const allowedDiscovery = new Set([
    'include_keyword',
    'exclude_keyword',
    'query',
    'hashtag',
    'subreddit',
  ]);
  const discoveryValues = new Map<string, string[]>(
    [...allowedDiscovery].map((kind) => [kind, []]),
  );
  discovery.forEach((row, index) => {
    if (!('type' in row) || !('value' in row))
      throw new Error('Sheet “discovery” wajib memakai kolom type dan value.');
    const kind = text(row.type).toLowerCase();
    const value = text(row.value);
    if (!allowedDiscovery.has(kind))
      throw new Error(`Tipe discovery tidak dikenal pada baris ${index + 2}: ${kind || 'kosong'}.`);
    if (value) discoveryValues.get(kind)!.push(value.replace(/^#/, '').replace(/^r\//i, ''));
  });

  const exampleRows = rows('relevance_examples');
  const allowedClasses = new Set(['relevant', 'generic', 'irrelevant']);
  const examples = new Map<string, string[]>([...allowedClasses].map((kind) => [kind, []]));
  exampleRows.forEach((row, index) => {
    if (!('classification' in row) || !('text' in row))
      throw new Error('Sheet “relevance_examples” wajib memakai kolom classification dan text.');
    const classification = text(row.classification).toLowerCase();
    const value = text(row.text);
    if (!allowedClasses.has(classification))
      throw new Error(
        `Klasifikasi relevansi tidak dikenal pada baris ${index + 2}: ${classification || 'kosong'}.`,
      );
    if (value) examples.get(classification)!.push(value);
  });

  return {
    ...base,
    title: text(metadata.title),
    objective: text(metadata.objective),
    includeMode,
    include: unique(discoveryValues.get('include_keyword')!).join('\n'),
    exclude: unique(discoveryValues.get('exclude_keyword')!).join('\n'),
    queries: unique(discoveryValues.get('query')!).join('\n'),
    hashtags: unique(discoveryValues.get('hashtag')!).join('\n'),
    subreddits: unique(discoveryValues.get('subreddit')!).join('\n'),
    relevance: {
      scope: text(metadata.relevance_scope),
      threshold,
      relevantExamples: unique(examples.get('relevant')!).join('\n'),
      genericExamples: unique(examples.get('generic')!).join('\n'),
      irrelevantExamples: unique(examples.get('irrelevant')!).join('\n'),
    },
    origin: 'excel',
  };
}
