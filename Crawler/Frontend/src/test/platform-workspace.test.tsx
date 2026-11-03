import { describe, expect, it, vi } from 'vitest';
import { act, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import PlatformWorkspace from '../features/PlatformWorkspace';
import JobDetail from '../features/JobDetail';
import { AppContext } from '../shared/context';
import { demoApi } from '../shared/demo';
import { initialConfig, platforms } from '../shared/domain';
import type { Job, Plan } from '../shared/types';
vi.mock('../shared/api', async (original) => ({
  ...(await original<typeof import('../shared/api')>()),
  api: (await import('../shared/demo')).demoApi,
}));
async function mount(path = '/crawler/youtube', observer = false) {
  sessionStorage.setItem('beesense:demo-role', observer ? 'observer' : 'operator');
  const cap = await demoApi.capabilities();
  const session = await demoApi.session();
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  const router = createMemoryRouter(
    [
      { path: '/crawler/:platform', element: <PlatformWorkspace /> },
      { path: '/crawler/:platform/jobs/:jobId', element: <JobDetail /> },
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
  return { router, user: userEvent.setup() };
}
describe('platform collection workspace', () => {
  it('loads source JSON defaults and only enables the current source', async () => {
    await mount('/crawler/instagram');
    expect(screen.getByRole('heading', { name: 'Instagram', level: 1 })).toBeInTheDocument();
    expect(screen.getByLabelText(/Hashtag/)).toHaveValue(
      initialConfig('automatic', 'instagram').platforms.instagram.hashtags,
    );
    expect(screen.queryByLabelText(/Queries pencarian/)).not.toBeInTheDocument();
    expect(screen.getByLabelText(/Jumlah post/)).toHaveValue(1000);
    expect(screen.getByRole('radio', { name: /^Excel lokal/ })).toBeChecked();
    expect(screen.getByRole('checkbox', { name: /Batasi waktu/ })).not.toBeChecked();
    expect(screen.queryByLabelText(/Limit waktu/)).not.toBeInTheDocument();
    expect(
      platforms.filter((p) => initialConfig('automatic', 'instagram').platforms[p].enabled),
    ).toEqual(['instagram']);
  });
  it('supports optional hours and an ephemeral PostgreSQL URI with matching host', async () => {
    const { user, router } = await mount();
    const start = vi.spyOn(demoApi, 'start');
    await user.type(screen.getByLabelText(/Nama pengambilan/), 'Uji penyimpanan sintetis');
    await user.click(screen.getByRole('checkbox', { name: /Batasi waktu/ }));
    const hours = screen.getByLabelText(/Limit waktu/);
    await user.clear(hours);
    await user.type(hours, '1.5');
    await user.click(screen.getByRole('radio', { name: /Keduanya/ }));
    await user.type(
      screen.getByLabelText(/String koneksi PostgreSQL/),
      'postgresql://demo:synthetic-secret@192.0.2.9:5433/demo',
    );
    expect(screen.getByLabelText(/IP address/)).toHaveValue('192.0.2.9');
    expect(screen.getByLabelText(/^Port/)).toHaveValue(5433);
    expect(screen.getByLabelText(/String koneksi PostgreSQL/)).toHaveAttribute('type', 'password');
    await user.click(screen.getByRole('button', { name: /Tinjau & mulai/ }));
    const dialog = await screen.findByRole('dialog', { name: 'Mulai crawling YouTube?' });
    expect(within(dialog).getByText('1,5 jam')).toBeInTheDocument();
    expect(within(dialog).queryByText(/synthetic-secret/)).not.toBeInTheDocument();
    await user.click(within(dialog).getByRole('button', { name: 'Mulai simulasi' }));
    await waitFor(() =>
      expect(router.state.location.pathname).toMatch(/^\/crawler\/youtube\/jobs\//),
    );
    expect(start).toHaveBeenCalledTimes(1);
    const [plan] = start.mock.calls[0];
    expect(plan.config.duration).toBe(5400);
    expect(plan.config.storage.destination).toBe('both');
    expect(plan.config.storage.postgresql.connectionString).toBeUndefined();
    expect(JSON.stringify(localStorage)).not.toContain('synthetic-secret');
  });
  it('focuses an invalid field and never submits an invalid target', async () => {
    const { user } = await mount();
    const validate = vi.spyOn(demoApi, 'validate');
    await user.type(screen.getByLabelText(/Nama pengambilan/), 'Target invalid');
    const target = screen.getByLabelText(/Jumlah post/);
    await user.clear(target);
    await user.type(target, '0');
    await user.click(screen.getByRole('button', { name: /Tinjau & mulai/ }));
    expect(target).toHaveAttribute('aria-invalid', 'true');
    expect(target).toHaveFocus();
    expect(validate).not.toHaveBeenCalled();
  });
  it('ignores a validation response for a configuration that has changed', async () => {
    let resolve!: (plan: Plan) => void;
    vi.spyOn(demoApi, 'validate').mockReturnValueOnce(
      new Promise((done) => {
        resolve = done;
      }),
    );
    const { user } = await mount();
    await user.type(screen.getByLabelText(/Nama pengambilan/), 'Awal');
    await user.click(screen.getByRole('button', { name: /Tinjau & mulai/ }));
    await user.type(screen.getByLabelText(/Nama pengambilan/), ' berubah');
    await act(async () =>
      resolve({
        id: 'stale',
        config: initialConfig('automatic', 'youtube'),
        warnings: [],
        expiresAt: new Date(Date.now() + 60000).toISOString(),
      }),
    );
    expect(
      screen.queryByRole('dialog', { name: 'Mulai crawling YouTube?' }),
    ).not.toBeInTheDocument();
  });
  it('preserves draft across results tabs and confirms when changing platforms', async () => {
    const { user, router } = await mount();
    await user.clear(screen.getByLabelText(/Nama pengambilan/));
    await user.type(screen.getByLabelText(/Nama pengambilan/), 'Draft utuh');
    await user.click(screen.getByRole('link', { name: 'Hasil per tanggal' }));
    await user.click(screen.getByRole('link', { name: 'Konfigurasi crawling' }));
    expect(screen.getByLabelText(/Nama pengambilan/)).toHaveValue('Draft utuh');
    await act(async () => {
      await router.navigate('/crawler/reddit');
    });
    expect(screen.getByRole('dialog', { name: /Tinggalkan masukan/ })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Tinggalkan halaman' }));
    expect(await screen.findByRole('heading', { name: 'Reddit', level: 1 })).toBeInTheDocument();
  });
  it('blocks mutations for an observer', async () => {
    await mount('/crawler/youtube', true);
    expect(screen.getByText(/hanya dapat diubah oleh operator/)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Tinjau & mulai/ })).not.toBeInTheDocument();
  });
  it('groups and filters by execution day in WIB, clearing page and preview atomically', async () => {
    const base = (await demoApi.jobs()).find((job) => job.id === 'demo-riset-001')!;
    const job = (id: string, at: string): Job => ({
      ...structuredClone(base),
      id,
      name: id,
      createdAt: '2026-10-01T00:00:00Z',
      startedAt: at,
    });
    vi.spyOn(demoApi, 'jobs').mockResolvedValue([
      job('Lewat tengah malam WIB', '2026-11-02T18:00:00Z'),
      job('Hari sebelumnya WIB', '2026-11-02T16:59:00Z'),
      job('Lewat tengah malam WIB', '2026-11-02T18:00:00Z'),
    ]);
    const { user, router } = await mount('/crawler/youtube?view=results&page=2&transaction=old');
    await screen.findByText('Lewat tengah malam WIB');
    expect(screen.getAllByText('Lewat tengah malam WIB')).toHaveLength(1);
    await user.click(screen.getByRole('button', { name: '3 November 2026' }));
    await waitFor(() => expect(screen.queryByText('Hari sebelumnya WIB')).not.toBeInTheDocument());
    const params = new URLSearchParams(router.state.location.search);
    expect(params.get('date')).toBe('2026-11-03');
    expect(params.has('page')).toBe(false);
    expect(params.has('transaction')).toBe(false);
    expect(params.get('view')).toBe('results');
    await user.click(screen.getByRole('button', { name: 'Lihat data' }));
    expect(
      await screen.findByRole('region', { name: 'Data Lewat tengah malam WIB' }),
    ).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Detail pekerjaan' })).toHaveAttribute(
      'href',
      '/crawler/youtube/jobs/Lewat%20tengah%20malam%20WIB?panel=result',
    );
  });
});
