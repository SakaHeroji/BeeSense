import { describe, expect, it } from 'vitest';
import * as xlsx from 'xlsx';
import {
  conversationPrompt,
  parseConversationWorkbook,
  promptFilename,
} from '../shared/conversation-workbook';
import { emptyConversationDraft } from '../shared/domain';

function workbookBytes() {
  const book = xlsx.utils.book_new();
  xlsx.utils.book_append_sheet(
    book,
    xlsx.utils.json_to_sheet([
      {
        title: 'Akses beasiswa daerah',
        objective: 'Memahami hambatan dan kebutuhan calon penerima beasiswa.',
        include_mode: 'any',
        relevance_scope: 'Percakapan tentang pencarian dan akses beasiswa pendidikan.',
        relevance_threshold: 0.66,
      },
    ]),
    'conversation',
  );
  xlsx.utils.book_append_sheet(
    book,
    xlsx.utils.json_to_sheet([
      { type: 'include_keyword', value: 'beasiswa daerah' },
      { type: 'include_keyword', value: 'beasiswa daerah' },
      { type: 'exclude_keyword', value: 'pinjaman ilegal' },
      { type: 'query', value: 'cara mendapat beasiswa daerah' },
      { type: 'hashtag', value: '#beasiswa' },
      { type: 'subreddit', value: 'r/indonesia' },
    ]),
    'discovery',
  );
  xlsx.utils.book_append_sheet(
    book,
    xlsx.utils.json_to_sheet([
      { classification: 'relevant', text: 'Saya kesulitan memenuhi syarat beasiswa daerah.' },
      { classification: 'generic', text: 'Terima kasih atas informasinya.' },
      { classification: 'irrelevant', text: 'Saya sedang mencari suku cadang kendaraan.' },
    ]),
    'relevance_examples',
  );
  return xlsx.write(book, { type: 'array', bookType: 'xlsx' }) as ArrayBuffer;
}

describe('Conversation workbook exchange', () => {
  it('downloads a title-bound prompt with the exact workbook contract', () => {
    const prompt = conversationPrompt('Akses beasiswa daerah');
    expect(prompt).toContain('Akses beasiswa daerah');
    expect(prompt).toContain('`conversation`');
    expect(prompt).toContain('`discovery`');
    expect(prompt).toContain('`relevance_examples`');
    expect(promptFilename('Akses Beasiswa Daerah')).toBe(
      'prompt-conversation-akses-beasiswa-daerah.md',
    );
  });

  it('maps a valid workbook into a deduplicated Excel-origin conversation', async () => {
    const draft = await parseConversationWorkbook(workbookBytes(), emptyConversationDraft());
    expect(draft).toMatchObject({
      title: 'Akses beasiswa daerah',
      includeMode: 'any',
      include: 'beasiswa daerah',
      exclude: 'pinjaman ilegal',
      queries: 'cara mendapat beasiswa daerah',
      hashtags: 'beasiswa',
      subreddits: 'indonesia',
      origin: 'excel',
      relevance: { threshold: 0.66 },
    });
  });

  it('rejects a workbook whose discovery type is outside the contract', async () => {
    const book = xlsx.read(workbookBytes(), { type: 'array' });
    book.Sheets.discovery = xlsx.utils.json_to_sheet([{ type: 'unknown', value: 'x' }]);
    const bytes = xlsx.write(book, { type: 'array', bookType: 'xlsx' }) as ArrayBuffer;
    await expect(parseConversationWorkbook(bytes, emptyConversationDraft())).rejects.toThrow(
      'Tipe discovery tidak dikenal',
    );
  });
});
