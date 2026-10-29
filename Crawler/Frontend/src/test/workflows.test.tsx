import { describe, expect, it, vi } from 'vitest';
import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Automatic from '../features/Automatic';
import Manual from '../features/Manual';
import JobDetail from '../features/JobDetail';
import Shell from '../app/Shell';
import type { UrlReview } from '../shared/types';
import { AppContext } from '../shared/context';
import { demoApi } from '../shared/demo';

vi.mock('../shared/api', async (importOriginal) => ({
  ...(await importOriginal<typeof import('../shared/api')>()),
  api: (await import('../shared/demo')).demoApi,
}));
async function mount(path: string, observer = false) {
  sessionStorage.setItem('beesense:demo-role', observer ? 'observer' : 'operator');
  const cap = await demoApi.capabilities();
  const session = await demoApi.session();
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  const router = createMemoryRouter(
    [
      { path: '/crawler/automatic', element: <Automatic /> },
      { path: '/crawler/manual', element: <Manual /> },
      { path: '/crawler/automatic/jobs/:jobId', element: <JobDetail /> },
      { path: '/crawler/manual/jobs/:jobId', element: <JobDetail /> },
    ],
    { initialEntries: [path] },
  );
  render(
    <QueryClientProvider client={client}>
      <AppContext.Provider value={{ cap, session, notify: vi.fn() }}>
        <RouterProvider router={router} />
      </AppContext.Provider>
    </QueryClientProvider>,
  );
  return { user: userEvent.setup(), router };
}
describe('operator workflows against synthetic adapter', () => {
  it('adds all five new sources to queries, targets and the job monitor', async () => {
    const { user, router } = await mount('/crawler/automatic');
    await user.type(screen.getByLabelText(/Nama pekerjaan/), 'Tujuh sumber sintetis');
    for (const name of ['Instagram', 'TikTok', 'Threads', 'Facebook', 'X / Twitter']) {
      await user.click(screen.getByRole('checkbox', { name: new RegExp(name) }));
      expect(screen.getByLabelText(`Query ${name}`, { exact: false })).toBeInTheDocument();
    }
    await user.click(screen.getByRole('button', { name: /Lanjutkan/ }));
    expect(screen.getAllByLabelText(/Target post memenuhi kriteria/)).toHaveLength(7);
    await user.type(screen.getByLabelText(/Mulai pada/), '2026-10-01T00:00');
    await user.type(screen.getByLabelText(/Sampai sebelum/), '2026-10-29T00:00');
    await user.click(screen.getByRole('button', { name: /Lanjutkan/ }));
    await user.click(screen.getByRole('button', { name: /Lanjutkan/ }));
    await user.click(screen.getByRole('button', { name: 'Validasi rencana' }));
    await user.click(await screen.findByRole('button', { name: 'Mulai akuisisi' }));
    await waitFor(() => expect(router.state.location.pathname).toMatch(/\/jobs\/demo-/));
    expect(
      await screen.findAllByText('post memenuhi kriteria', { selector: '.qualified-caption' }),
    ).toHaveLength(7);
  });
  it('ignores an old URL validation response when the operator edits the input', async () => {
    let resolveReview!: (rows: UrlReview[]) => void;
    const pending = new Promise<UrlReview[]>((resolve) => {
      resolveReview = resolve;
    });
    vi.spyOn(demoApi, 'reviewUrls').mockReturnValueOnce(pending);
    const { user } = await mount('/crawler/manual?tab=url');
    const field = screen.getByLabelText(/URL post atau video/);
    await user.type(field, 'https://youtu.be/abcdefghijk');
    await user.click(screen.getByRole('button', { name: 'Validasi URL' }));
    await user.clear(field);
    await user.type(field, 'https://youtu.be/12345678901');
    await act(async () => {
      resolveReview([
        {
          input: 'https://youtu.be/abcdefghijk',
          canonical: 'https://www.youtube.com/watch?v=abcdefghijk',
          nativeId: 'abcdefghijk',
          platform: 'youtube',
          status: 'valid',
          reason: 'Valid lama',
        },
      ]);
    });
    expect(screen.queryByText('Valid lama')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Tinjau & validasi/ })).toBeDisabled();
  });
  it('keeps hidden mobile navigation inert and restores it with keyboard controls', async () => {
    Object.defineProperty(window, 'matchMedia', {
      configurable: true,
      value: vi.fn(() => ({
        matches: true,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      })),
    });
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const router = createMemoryRouter(
      [{ element: <Shell />, children: [{ path: '/crawler/automatic', element: <Automatic /> }] }],
      { initialEntries: ['/crawler/automatic'] },
    );
    render(
      <QueryClientProvider client={client}>
        <RouterProvider router={router} />
      </QueryClientProvider>,
    );
    await screen.findByRole('heading', { name: 'Crawler otomatis' });
    const aside = document.getElementById('crawler-nav')!;
    expect(aside).toHaveAttribute('inert');
    const user = userEvent.setup();
    await user.click(screen.getByRole('button', { name: 'Buka navigasi' }));
    expect(aside).not.toHaveAttribute('inert');
    expect(
      within(aside).getByRole('navigation', { name: 'Menu Crawler' }).querySelectorAll('a'),
    ).toHaveLength(2);
    await user.keyboard('{Escape}');
    expect(aside).toHaveAttribute('inert');
  });
  it('requires an explicit XLSX sheet and maps its survey answers', async () => {
    const { user } = await mount('/crawler/manual?tab=survey');
    await user.click(screen.getByRole('button', { name: /Impor file/ }));
    const xlsx = await import('xlsx');
    const wb = xlsx.utils.book_new();
    xlsx.utils.book_append_sheet(
      wb,
      xlsx.utils.aoa_to_sheet([['catatan'], ['bukan respons']]),
      'Petunjuk',
    );
    xlsx.utils.book_append_sheet(
      wb,
      xlsx.utils.aoa_to_sheet([
        [
          'survey_id',
          'survey_version',
          'response_id',
          'respondent_code',
          'respondent_role',
          'submitted_at',
          'question_id',
          'answer_text',
          'answer_value',
          'usage_permission',
          'source_reference',
        ],
        [
          'minat-studi',
          '1',
          'XLSX-001',
          'R-XLSX',
          'parent',
          '2026-10-29T10:00:00+07:00',
          'Q01',
          'Minat',
          '',
          'granted',
          'sintetis',
        ],
        [
          'minat-studi',
          '1',
          'XLSX-001',
          'R-XLSX',
          'parent',
          '2026-10-29T10:00:00+07:00',
          'Q02',
          '',
          '3',
          'granted',
          'sintetis',
        ],
      ]),
      'Respons',
    );
    const bytes = xlsx.write(wb, { type: 'array', bookType: 'xlsx' });
    const file = new File([bytes], 'sintetis.xlsx', {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });
    Object.defineProperty(file, 'arrayBuffer', { value: async () => bytes });
    await user.upload(screen.getByLabelText('Pilih berkas'), file);
    const sheet = await screen.findByLabelText(/Pilih sheet/);
    expect(screen.queryByLabelText('Mapping response_id')).not.toBeInTheDocument();
    await user.selectOptions(sheet, 'Respons');
    await user.click(screen.getByRole('button', { name: 'Validasi data survei' }));
    expect(await screen.findByRole('button', { name: 'Impor 1 respons valid' })).toBeEnabled();
  });
  it('keeps invalid source configuration on its step and links the error to the field', async () => {
    const { user } = await mount('/crawler/automatic');
    await user.click(screen.getByRole('button', { name: /Lanjutkan/ }));
    const name = screen.getByLabelText(/Nama pekerjaan/);
    expect(name).toHaveAttribute('aria-invalid', 'true');
    expect(name).toHaveFocus();
    expect(screen.queryByLabelText(/Mulai pada/)).not.toBeInTheDocument();
  });
  it('commits a complete synthetic survey and preserves context in its result', async () => {
    const { user, router } = await mount('/crawler/manual?tab=survey');
    await user.selectOptions(screen.getByLabelText(/Peran responden/), 'prospective_student');
    await user.type(screen.getByLabelText(/Kode responden/), 'SYNTH-VALID');
    await user.type(screen.getByLabelText(/Waktu pengisian/), '2026-10-29T10:00');
    await user.type(screen.getByLabelText(/Referensi sumber/), 'sintetis-lengkap');
    await user.selectOptions(screen.getByLabelText(/Izin pemanfaatan/), 'granted');
    await user.type(screen.getByLabelText(/Apa pertimbangan/), 'Kesesuaian dengan minat');
    await user.selectOptions(screen.getByLabelText(/Seberapa penting/), '4');
    await user.click(screen.getByRole('button', { name: /Validasi respons/ }));
    await user.click(await screen.findByRole('button', { name: 'Simpan respons' }));
    await waitFor(() =>
      expect(router.state.location.pathname).toMatch(/manual\/jobs\/demo-survey-/),
    );
    expect(await screen.findByText('Respons tersimpan')).toBeInTheDocument();
    await user.click(screen.getByRole('link', { name: /Hasil dataset/ }));
    expect(await screen.findByText(/adapter NLP/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Siapkan untuk NLP' })).toBeDisabled();
  });
  it('imports a CSV with automatic mapping and validates complete responses', async () => {
    const { user } = await mount('/crawler/manual?tab=survey');
    await user.click(screen.getByRole('button', { name: /Impor file/ }));
    const csv =
      'survey_id,survey_version,response_id,respondent_code,respondent_role,submitted_at,question_id,answer_text,answer_value,usage_permission,source_reference\nminat-studi,1,CSV-001,R-CSV,parent,2026-10-29T10:00:00+07:00,Q01,Biaya,,granted,sintetis\nminat-studi,1,CSV-001,R-CSV,parent,2026-10-29T10:00:00+07:00,Q02,,5,granted,sintetis';
    const file = new File([csv], 'sintetis.csv', { type: 'text/csv' });
    Object.defineProperty(file, 'text', { value: async () => csv });
    await user.upload(screen.getByLabelText('Pilih berkas'), file);
    expect(await screen.findByLabelText('Mapping response_id')).toHaveValue('response_id');
    await user.click(screen.getByRole('button', { name: 'Validasi data survei' }));
    expect(await screen.findByRole('button', { name: 'Impor 1 respons valid' })).toBeEnabled();
  });
  it('validates an automatic job and starts exactly one job, then restores its monitor route', async () => {
    const spy = vi.spyOn(demoApi, 'start');
    const { user, router } = await mount('/crawler/automatic');
    await user.type(screen.getByLabelText(/Nama pekerjaan/), 'Riset integrasi');
    await user.click(screen.getByRole('button', { name: /Lanjutkan/ }));
    await user.type(screen.getByLabelText(/Mulai pada/), '2026-10-01T00:00');
    await user.type(screen.getByLabelText(/Sampai sebelum/), '2026-10-29T00:00');
    await user.click(screen.getByRole('button', { name: /Lanjutkan/ }));
    await user.click(screen.getByRole('button', { name: /Lanjutkan/ }));
    await user.click(screen.getByRole('button', { name: 'Validasi rencana' }));
    await user.click(await screen.findByRole('button', { name: 'Mulai akuisisi' }));
    await waitFor(() => expect(router.state.location.pathname).toMatch(/\/jobs\/demo-/));
    expect(spy).toHaveBeenCalledTimes(1);
    expect(
      (await screen.findAllByText('post memenuhi kriteria', { selector: '.qualified-caption' }))
        .length,
    ).toBe(2);
  });
  it('reviews valid, duplicate and unsafe URLs and requires acknowledgement of skipped inputs', async () => {
    const { user } = await mount('/crawler/manual?tab=url');
    await user.type(screen.getByLabelText(/Nama pekerjaan/), 'URL riset');
    await user.type(
      screen.getByLabelText(/URL post atau video/),
      'https://youtu.be/abcdefghijk\nhttps://www.youtube.com/watch?v=abcdefghijk\nhttps://evil.test',
    );
    await user.click(screen.getByRole('button', { name: 'Validasi URL' }));
    expect(await screen.findByText('Duplikat input')).toBeInTheDocument();
    const reviewButton = screen.getByRole('button', { name: /Tinjau & validasi/ });
    expect(reviewButton).toBeDisabled();
    await user.click(screen.getByRole('checkbox', { name: /Saya memahami 2 input/ }));
    expect(reviewButton).toBeEnabled();
  });
  it('rejects a survey without permission before commit', async () => {
    const { user } = await mount('/crawler/manual?tab=survey');
    await user.selectOptions(screen.getByLabelText(/Peran responden/), 'parent');
    await user.type(screen.getByLabelText(/Kode responden/), 'SYNTH-001');
    await user.type(screen.getByLabelText(/Waktu pengisian/), '2026-10-29T10:00');
    await user.type(screen.getByLabelText(/Referensi sumber/), 'sintetis');
    await user.selectOptions(screen.getByLabelText(/Izin pemanfaatan/), 'unknown');
    await user.type(screen.getByLabelText(/Apa pertimbangan/), 'Minat dan biaya');
    await user.selectOptions(screen.getByLabelText(/Seberapa penting/), '4');
    await user.click(screen.getByRole('button', { name: /Validasi respons/ }));
    expect(await screen.findByText(/Seluruh respons dikecualikan/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Simpan respons/ })).toBeDisabled();
  });
  it('prevents observer input and backend simulator mutations', async () => {
    await mount('/crawler/manual?tab=survey', true);
    expect(screen.getByText(/Pengamat dapat melihat hasil/)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Simpan respons/ })).not.toBeInTheDocument();
    await expect(demoApi.stop('demo-riset-001')).rejects.toThrow('Pengamat');
    sessionStorage.removeItem('beesense:demo-role');
  });
  it('shows a final dataset and requires partial acceptance for NLP handoff', async () => {
    const { user } = await mount('/crawler/automatic/jobs/demo-riset-001');
    await user.click(await screen.findByRole('link', { name: /Hasil dataset/ }));
    await user.click(await screen.findByRole('button', { name: 'Siapkan untuk NLP' }));
    const dialog = screen.getByRole('dialog', { name: 'Siapkan input NLP' });
    const save = within(dialog).getByRole('button', { name: 'Simpan pilihan input' });
    expect(save).toBeDisabled();
    await user.click(within(dialog).getByRole('checkbox'));
    expect(save).toBeEnabled();
  });
});
