import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const [payloadPath, outputPath, previewDir] = process.argv.slice(2);
if (!payloadPath || !outputPath || !previewDir) {
  throw new Error('Usage: build_topic_sentences.mjs payload.json output.xlsx preview-directory');
}
const payload = JSON.parse(await fs.readFile(payloadPath, 'utf8'));
const workbook = Workbook.create();
const sentences = workbook.worksheets.add('Kalimat');
const topics = workbook.worksheets.add('Topik');
const font = 'Helvetica Neue';
const literal = value => typeof value === 'string' && value.startsWith('=') ? `'${value}` : value;
const last = payload.rows.length + 5;

for (const sheet of [sentences, topics]) sheet.showGridLines = false;
sentences.getRange(`A1:B${last}`).format.font = { name: font, size: 11, color: '#17212B' };
sentences.getRange('A1').format.columnWidthPx = 330;
sentences.getRange('B1').format.columnWidthPx = 900;
sentences.getRange('A1').values = [['Topik dan kalimat']];
sentences.getRange('A1').format.font = { name: font, size: 16, bold: true };
sentences.getRange('A1:B1').format.rowHeightPx = 32;
sentences.getRange('A2:B2').values = [[`${payload.topics.length} topik`, 'Kalimat asli unik pada setiap cluster; pengulangan teks yang sama dalam topik disatukan.']];
sentences.getRange('A2:B2').format = { font: { name: font, size: 11, italic: true, color: '#56616E' }, rowHeightPx: 32, wrapText: true };
sentences.getRange('A3:B3').values = [['Coherence c_v rata-rata', payload.macro_coherence]];
sentences.getRange('B3').setNumberFormat('0.0000');
sentences.getRange(`A5:B${last}`).values = [payload.headers, ...payload.rows.map(row => row.map(literal))];
sentences.tables.add(`A5:B${last}`, true, 'KalimatTopik');
const body = sentences.getRange(`A6:B${last}`);
body.format.wrapText = true;
body.format.verticalAlignment = 'top';
body.setNumberFormat('@');
sentences.freezePanes.freezeRows(5);
sentences.freezePanes.freezeColumns(1);
console.log('Sentence values and table written');

const textLines = (text, chars) => String(text).split('\n').reduce((total, line) => {
  const units = [...line].reduce((width, char) => width + (char.codePointAt(0) >= 0x2e80 ? 2 : 1), 0);
  return total + Math.max(1, Math.ceil(units / chars));
}, 0);
let start = 6;
let height = null;
let longestIndex = 0;
for (let i = 0; i <= payload.rows.length; i++) {
  const row = payload.rows[i];
  const nextHeight = row ? Math.min(520, Math.max(36, (Math.max(textLines(row[0], 42), textLines(row[1], 90)) + 1) * 18)) : null;
  if (i < payload.rows.length && row[1].length > payload.rows[longestIndex][1].length) longestIndex = i;
  if (height !== null && nextHeight !== height) {
    sentences.getRange(`A${start}:B${i + 5}`).format.rowHeightPx = height;
    start = i + 6;
  }
  height = nextHeight;
}
console.log('Sentence row heights formatted');

topics.getRange('A1:C33').format.font = { name: font, size: 11, color: '#17212B' };
topics.getRange('A1').format.columnWidthPx = 620;
topics.getRange('B1').format.columnWidthPx = 130;
topics.getRange('C1').format.columnWidthPx = 180;
topics.getRange('A1').values = [['Ringkasan topik']];
topics.getRange('A1').format.font = { name: font, size: 16, bold: true };
topics.getRange('A1:C1').format.rowHeightPx = 32;
topics.getRange('A2:A4').values = [['Coherence c_v rata-rata'], ['Batas c_v rata-rata'], ['Kemunculan kalimat noise']];
topics.getRange('B2').formulas = [[`=AVERAGE(B7:B${payload.topics.length + 6})`]];
topics.getRange('B3:B4').values = [[payload.min_coherence], [payload.noise_occurrences]];
topics.getRange('B2:B3').setNumberFormat('0.0000');
topics.getRange('B4').setNumberFormat('#,##0');
topics.getRange('A6:C6').values = [['topik', 'coherence c_v', 'jumlah kalimat unik']];
topics.getRange(`A7:B${payload.topics.length + 6}`).values = payload.topics.map(row => [row.label, row.coherence_cv]);
topics.getRange(`C7:C${payload.topics.length + 6}`).formulas = payload.topics.map((_, index) => [`=COUNTIF('Kalimat'!$A$6:$A$${last},A${index + 7})`]);
topics.tables.add(`A6:C${payload.topics.length + 6}`, true, 'RingkasanTopik');
topics.getRange(`A7:C${payload.topics.length + 6}`).format = { wrapText: true, verticalAlignment: 'top', rowHeightPx: 51 };
topics.getRange(`B7:B${payload.topics.length + 6}`).setNumberFormat('0.0000');
topics.getRange(`C7:C${payload.topics.length + 6}`).setNumberFormat('#,##0');
topics.getRange(`B7:B${payload.topics.length + 6}`).conditionalFormats.add('cellIs', { operator: 'lessThan', formula: payload.min_coherence, format: { fill: '#FFF0D2', font: { color: '#713F12' } } });
topics.getRange('A29:A32').values = [
  ['Sumber dataset'],
  [payload.source_url],
  [`SHA-256: ${payload.source_sha256}`],
  ['Ambang berlaku pada rata-rata semua topik. c_v mengukur konsistensi istilah pada korpus ini, bukan akurasi berlabel. Kalimat noise tidak masuk tabel 20 topik.'],
];
topics.getRange('A29:A32').format = { wrapText: true, rowHeightPx: 51, font: { name: font, size: 11, color: '#56616E' } };

for (const [sheet, range] of [[sentences, 'A5:B5'], [topics, 'A6:C6']]) {
  sheet.getRange(range).format = {
    fill: '#334155',
    font: { name: font, size: 11, bold: true, color: '#FFFFFF' },
    rowHeightPx: 40,
    wrapText: true,
    horizontalAlignment: 'center',
    verticalAlignment: 'center',
    borders: { insideVertical: { style: 'thin', color: '#FFFFFF' } },
  };
}
console.log('Topic summary and formulas written');
const inspection = await workbook.inspect({ kind: 'table', range: 'Topik!A2:C4', include: 'values,formulas', tableMaxRows: 3, tableMaxCols: 3, maxChars: 1400 });
console.log(inspection.ndjson);
const calculated = topics.getRange('B2').values[0][0];
if (Math.abs(Number(calculated) - payload.macro_coherence) > 1e-10) throw new Error('Workbook coherence mean differs from Gensim');
for (let i = 0; i < payload.topics.length; i++) {
  if (Number(topics.getRange(`C${i + 7}`).values[0][0]) !== payload.topics[i].sentences) throw new Error('Workbook sentence count differs from cluster membership');
}
console.log((await workbook.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!', options: { useRegex: true, maxResults: 10 }, maxChars: 1200 })).ndjson);
await fs.mkdir(previewDir, { recursive: true });
for (const [sheetName, range, name] of [
  ['Kalimat', 'A1:B10', 'sentences-preview.png'],
  ['Topik', 'A1:C32', 'topics-preview.png'],
  ['Kalimat', `A${longestIndex + 6}:B${longestIndex + 6}`, 'longest-sentence-preview.png'],
]) {
  const blob = await workbook.render({ sheetName, range, scale: 1, format: 'png' });
  await fs.writeFile(path.join(previewDir, name), new Uint8Array(await blob.arrayBuffer()));
}
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await (await SpreadsheetFile.exportXlsx(workbook)).save(outputPath);
console.log(JSON.stringify({ output: outputPath, rows: payload.rows.length, topics: payload.topics.length }));
