import { describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import PlatformWorkspace from '../features/PlatformWorkspace';
import JobDetail from '../features/JobDetail';
import Shell from '../app/Shell';
import { demoApi } from '../shared/demo';
vi.mock('../shared/api', async (original) => ({
  ...(await original<typeof import('../shared/api')>()),
  api: (await import('../shared/demo')).demoApi,
}));
async function mount(path: string, observer = false) {
  sessionStorage.setItem('beesense:demo-role', observer ? 'observer' : 'operator');
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  const router = createMemoryRouter(
    [
      {
        element: <Shell />,
        children: [
          { path: '/crawler/:platform', element: <PlatformWorkspace /> },
          { path: '/crawler/:platform/jobs/:jobId', element: <JobDetail /> },
        ],
      },
    ],
    { initialEntries: [path] },
  );
  render(
    <QueryClientProvider client={client}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );
  await screen.findByRole('heading', { level: 1 });
  return { router, user: userEvent.setup() };
}
describe('social source dashboard', () => {
  it('only exposes seven social menus, with no manual or standalone migration page', async () => {
    await mount('/crawler/youtube');
    const nav = screen.getByRole('navigation', { name: 'Menu Crawler' });
    expect(within(nav).getAllByRole('link')).toHaveLength(7);
    expect(within(nav).queryByText('Crawler Manual')).not.toBeInTheDocument();
    expect(within(nav).queryByText('Migrasi Excel')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('Module frontend')).not.toBeInTheDocument();
  });
  it('opens complete source-scoped statistics from the crawling transaction', async () => {
    const { user, router } = await mount('/crawler/youtube?view=results');
    await user.click(
      await screen.findByRole('link', { name: 'Statistik Percakapan tentang pilihan kuliah' }),
    );
    await screen.findByRole('region', { name: 'Statistik transaksi crawling' });
    expect(router.state.location.search).toBe('?panel=statistics');
    for (const [label, total] of [
      ['Post terkumpul', '450'],
      ['Post memenuhi kriteria', '300'],
      ['Komentar', '3.200'],
      ['Balasan', '900'],
      ['Duplikat dilewati', '45'],
      ['Ditolak filter / akses', '32'],
      ['Total konten unik', '4.550'],
    ]) {
      expect(
        screen.getByText(label, { selector: '.statistics-grid dt' }).nextElementSibling,
      ).toHaveTextContent(total);
    }
    expect(
      screen.getByRole('heading', { name: 'Statistik transaksi YouTube' }),
    ).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Migrasi ke PostgreSQL' })).toHaveAttribute(
      'href',
      expect.stringContaining('transaction=demo-riset-001&action=migrate'),
    );
  });
  it('reviews migration for the selected social transaction, without uploading files', async () => {
    const prepare = vi.spyOn(demoApi, 'prepareTransactionMigration');
    const start = vi.spyOn(demoApi, 'startTransactionMigration');
    const { user, router } = await mount('/crawler/reddit?view=results');
    await user.click(
      await screen.findByRole('button', {
        name: 'Migrasi Percakapan tentang pilihan kuliah ke PostgreSQL',
      }),
    );
    const region = await screen.findByRole('region', {
      name: 'Migrasi transaksi Percakapan tentang pilihan kuliah',
    });
    expect(within(region).queryByLabelText(/Pilih.*file/)).not.toBeInTheDocument();
    await user.click(within(region).getByRole('button', { name: 'Tinjau simulasi migrasi' }));
    const review = await screen.findByRole('dialog', { name: 'Migrasikan data Reddit?' });
    expect(within(review).getByText('798 post, komentar & balasan')).toBeInTheDocument();
    expect(prepare.mock.calls[0][1]).toBe('reddit');
    await user.click(within(review).getByRole('button', { name: 'Mulai simulasi migrasi' }));
    await waitFor(() =>
      expect(new URLSearchParams(router.state.location.search).get('migration')).toMatch(
        /^demo-transaction/,
      ),
    );
    expect(start).toHaveBeenCalledTimes(1);
    expect(
      await screen.findByRole('status', { name: 'Progres migrasi transaksi' }),
    ).toBeInTheDocument();
    expect(router.state.location.pathname).toBe('/crawler/reddit');
    await user.click(within(region).getByRole('button', { name: 'Tutup pengaturan migrasi' }));
    expect(within(region).queryByLabelText(/IP address/)).not.toBeInTheDocument();
    expect(
      within(region).getByRole('status', { name: 'Progres migrasi transaksi' }),
    ).toBeInTheDocument();
  });
  it('edits optional credentials, masks the session ID and simulates auth.json without storing secrets', async () => {
    const save = vi.spyOn(demoApi, 'saveAuth');
    const { user } = await mount('/crawler/instagram');
    const account = screen.getByRole('region', { name: 'Akun Instagram' });
    await user.type(within(account).getByLabelText('Username'), 'test_account');
    await user.type(within(account).getByLabelText('Session ID'), 'synthetic-session-secret');
    expect(within(account).getByLabelText('Session ID')).toHaveAttribute('type', 'password');
    await user.click(within(account).getByRole('button', { name: 'Tampilkan sesi' }));
    expect(within(account).getByLabelText('Session ID')).toHaveAttribute('type', 'text');
    await user.click(within(account).getByRole('button', { name: 'Simulasikan simpan auth.json' }));
    await screen.findByText('Simulasi pengaturan selesai. File auth.json tidak diubah.');
    expect(save.mock.calls[0]).toEqual([
      'instagram',
      { username: 'test_account', sessionid: 'synthetic-session-secret' },
    ]);
    expect(within(account).getByLabelText('Session ID')).toHaveValue('');
    expect(JSON.stringify(localStorage)).not.toContain('synthetic-session-secret');
    expect(JSON.stringify(await demoApi.authStatus('instagram'))).not.toContain(
      'synthetic-session-secret',
    );
  });
  it('keeps credentials optional and separates them from ordinary crawling plans', async () => {
    const validate = vi.spyOn(demoApi, 'validate');
    const { user } = await mount('/crawler/instagram');
    await user.type(screen.getByLabelText('Session ID'), 'synthetic-unsaved');
    await user.click(screen.getByRole('button', { name: 'Tinjau & mulai crawling' }));
    expect(validate).not.toHaveBeenCalled();
    expect(
      await screen.findByText(/Simpan pengaturan akun ke auth.json terlebih dahulu/),
    ).toBeInTheDocument();
    await user.clear(screen.getByLabelText('Session ID'));
    await user.click(screen.getByRole('button', { name: 'Tinjau & mulai crawling' }));
    expect(
      await screen.findByRole('dialog', { name: 'Mulai crawling Instagram?' }),
    ).toBeInTheDocument();
    expect(JSON.stringify(validate.mock.calls[0])).not.toContain('sessionid');
  });
  it('observer cannot edit account settings or start a transaction migration', async () => {
    await mount('/crawler/youtube?view=results&transaction=demo-riset-001&action=migrate', true);
    expect(
      await screen.findByText('Pengamat dapat melihat progres. Migrasi dijalankan oleh operator.'),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole('button', { name: 'Tinjau simulasi migrasi' }),
    ).not.toBeInTheDocument();
    await expect(
      demoApi.saveAuth('instagram', { username: 'demo', sessionid: 'synthetic' }),
    ).rejects.toThrow('Pengamat');
  });
});
