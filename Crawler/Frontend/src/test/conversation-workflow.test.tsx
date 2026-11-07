import { describe, expect, it, vi } from 'vitest';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ConversationWorkspace from '../features/ConversationWorkspace';
import ParallelWorkspace from '../features/ParallelWorkspace';
import JobDetail from '../features/JobDetail';
import { AppContext } from '../shared/context';
import { demoApi } from '../shared/demo';
import { api } from '../shared/api';

vi.mock('../shared/api', async (original) => ({
  ...(await original<typeof import('../shared/api')>()),
  api: (await import('../shared/demo')).demoApi,
}));

async function mount(path: string) {
  sessionStorage.setItem('beesense:demo-role', 'operator');
  const cap = await demoApi.capabilities();
  const session = await demoApi.session();
  const notify = vi.fn();
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  const router = createMemoryRouter(
    [
      { path: '/crawler/conversations', element: <ConversationWorkspace /> },
      { path: '/crawler/parallel', element: <ParallelWorkspace /> },
      { path: '/crawler/parallel/jobs/:jobId', element: <JobDetail /> },
    ],
    { initialEntries: [path] },
  );
  render(
    <QueryClientProvider client={client}>
      <AppContext.Provider value={{ cap, session, notify }}>
        <RouterProvider router={router} />
      </AppContext.Provider>
    </QueryClientProvider>,
  );
  return { notify, router, user: userEvent.setup() };
}

describe('conversation-first crawling workflow', () => {
  it('keeps the conversation table and editor form in separate views', async () => {
    const { user } = await mount('/crawler/conversations');
    expect(await screen.findByRole('heading', { name: 'Tabel conversation' })).toBeInTheDocument();
    expect(screen.queryByLabelText(/^Judul conversation/)).not.toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Conversation baru' }));
    expect(screen.getByRole('heading', { name: 'Buat conversation' })).toBeInTheDocument();
    expect(screen.getByLabelText(/^Judul conversation/)).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: 'Tabel conversation' })).not.toBeInTheDocument();
  });

  it('saves a manually authored conversation with its keyword matching policy', async () => {
    const save = vi.spyOn(demoApi, 'saveConversation');
    const { user } = await mount('/crawler/conversations');
    await user.click(await screen.findByRole('button', { name: 'Conversation baru' }));
    await user.type(screen.getByLabelText(/^Judul conversation/), 'Aspirasi karier mahasiswa');
    await user.type(screen.getByLabelText(/^Tujuan riset/), 'Memahami aspirasi karier mahasiswa.');
    await user.selectOptions(screen.getByLabelText('Pencocokan include keyword'), 'all');
    await user.type(
      screen.getByLabelText(/^Ruang lingkup relevansi/),
      'Percakapan tentang pilihan dan hambatan karier mahasiswa.',
    );
    await user.type(
      screen.getByLabelText(/^Contoh relevan/),
      'Saya mempertimbangkan pekerjaan setelah lulus kuliah.',
    );
    await user.click(screen.getByRole('button', { name: 'Simpan conversation' }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect(save.mock.calls[0][0]).toMatchObject({
      title: 'Aspirasi karier mahasiswa',
      includeMode: 'all',
      origin: 'manual',
    });
  });

  it('generates a reviewable conversation draft from the title only and saves a version', async () => {
    expect(api.conversations).toBe(demoApi.conversations);
    const generate = vi.spyOn(demoApi, 'generateConversation');
    const save = vi.spyOn(demoApi, 'saveConversation');
    const { user } = await mount('/crawler/conversations');
    await user.click(await screen.findByRole('button', { name: 'Conversation baru' }));
    const title = screen.getByLabelText(/^Judul conversation/);
    await user.type(title, 'Akses beasiswa mahasiswa daerah');
    await user.click(screen.getByRole('button', { name: 'Generate draf dari judul' }));
    await waitFor(() => expect(generate).toHaveBeenCalledWith('Akses beasiswa mahasiswa daerah'));
    await waitFor(() =>
      expect((screen.getByLabelText(/^Tujuan riset/) as HTMLTextAreaElement).value).toContain(
        'Akses beasiswa mahasiswa daerah',
      ),
    );
    expect(
      (screen.getByLabelText(/^Ruang lingkup relevansi/) as HTMLTextAreaElement).value,
    ).toContain('Akses beasiswa mahasiswa daerah');
    expect(screen.getByText('Draf Gemini')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Simpan conversation' }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(1));
    expect((await screen.findAllByText('Akses beasiswa mahasiswa daerah')).length).toBeGreaterThan(
      0,
    );
    const savedRow = screen.getByRole('row', { name: /Akses beasiswa mahasiswa daerah/ });
    await user.click(within(savedRow).getByRole('button', { name: 'Buka form' }));
    expect(screen.getByRole('button', { name: 'Simpan versi baru' })).toBeInTheDocument();
  });

  it('starts multiple platforms with one frozen conversation snapshot', async () => {
    const start = vi.spyOn(demoApi, 'start');
    const { router, user } = await mount('/crawler/parallel');
    await user.selectOptions(
      await screen.findByLabelText(/^Conversation/),
      'conversation-riset-kuliah',
    );
    await user.click(screen.getByRole('checkbox', { name: /YouTube/ }));
    await user.click(screen.getByRole('checkbox', { name: /Reddit/ }));
    await user.click(screen.getByRole('button', { name: 'Tinjau & mulai parallel' }));
    const dialog = await screen.findByRole('dialog', { name: 'Mulai crawling parallel?' });
    expect(within(dialog).getByText('YouTube, Reddit')).toBeInTheDocument();
    expect(within(dialog).getByText('v3')).toBeInTheDocument();
    await user.click(within(dialog).getByRole('button', { name: 'Mulai simulasi parallel' }));
    await waitFor(() =>
      expect(router.state.location.pathname).toMatch(/^\/crawler\/parallel\/jobs\//),
    );
    expect(start).toHaveBeenCalledTimes(1);
    const [plan] = start.mock.calls[0];
    expect(plan.config.executionMode).toBe('parallel');
    expect(plan.config.conversation).toMatchObject({
      id: 'conversation-riset-kuliah',
      version: 3,
      title: 'Percakapan tentang pilihan kuliah',
    });
    expect(plan.config.platforms.youtube.enabled).toBe(true);
    expect(plan.config.platforms.reddit.enabled).toBe(true);
    expect(plan.config.platforms.instagram.enabled).toBe(false);
  });

  it('keeps a parallel platform error next to the platform list', async () => {
    const { user } = await mount('/crawler/parallel');
    await user.selectOptions(
      await screen.findByLabelText(/^Conversation/),
      'conversation-riset-kuliah',
    );
    await user.click(screen.getByRole('checkbox', { name: /YouTube/ }));
    await user.click(screen.getByRole('button', { name: 'Tinjau & mulai parallel' }));
    const error = screen.getByText('Pilih minimal 2 platform untuk mode parallel.', {
      selector: '#parallel-platforms-error',
    });
    expect(error).toBeInTheDocument();
    expect(screen.getByRole('group', { name: 'Platform crawling parallel' })).toHaveAttribute(
      'aria-describedby',
      'parallel-platforms-error',
    );
  });
});
