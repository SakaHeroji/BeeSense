import { afterEach, describe, expect, it, vi } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import PlatformWorkspace from '../features/PlatformWorkspace';
import JobDetail from '../features/JobDetail';
import { AppContext } from '../shared/context';
import { demoApi } from '../shared/demo';
import { httpApi } from '../shared/api';
import { applyConversation, initialConfig } from '../shared/domain';
import { validateConnectorSession } from '../shared/tiktok-connector';
import type { TikTokConnectorSession } from '../shared/types';

vi.mock('../shared/api', async (original) => ({
  ...(await original<typeof import('../shared/api')>()),
  api: (await import('../shared/demo')).demoApi,
}));
afterEach(() => vi.useRealTimers());

async function newTikTokJob() {
  sessionStorage.setItem('beesense:demo-role', 'operator');
  const config = applyConversation(
    initialConfig('automatic', 'tiktok'),
    (await demoApi.conversations())[0],
  );
  config.duration = 10800;
  return demoApi.start(await demoApi.validate(config), crypto.randomUUID());
}
async function mount(path = '/crawler/tiktok', observer = false) {
  sessionStorage.setItem('beesense:demo-role', observer ? 'observer' : 'operator');
  const cap = await demoApi.capabilities(),
    session = await demoApi.session();
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

describe('TikTok plugin workspace', () => {
  it('keeps configuration, pairing and progress in one source-scoped transaction', async () => {
    const { user, router } = await mount();
    expect(screen.getByRole('list', { name: 'Alur crawling TikTok' })).toBeInTheDocument();
    expect(screen.getByText('Gunakan Chrome Anda')).toBeInTheDocument();
    expect(screen.queryByLabelText('Session ID')).not.toBeInTheDocument();
    await user.selectOptions(
      await screen.findByLabelText(/^Conversation/),
      'conversation-riset-kuliah',
    );
    expect(screen.getByText('Query & hashtag conversation')).toBeInTheDocument();
    expect(screen.queryByLabelText('Hashtag TikTok')).not.toBeInTheDocument();
    expect(screen.getByRole('radio', { name: /^Excel lokal/ })).toBeChecked();
    await user.click(screen.getByRole('button', { name: 'Tinjau & siapkan koneksi Chrome' }));
    const dialog = await screen.findByRole('dialog', {
      name: 'Siapkan crawling TikTok melalui Chrome?',
    });
    await user.click(within(dialog).getByRole('button', { name: 'Siapkan koneksi simulasi' }));
    const code = await screen.findByLabelText('Kode pairing sementara');
    expect(code).toHaveAttribute('type', 'password');
    expect(screen.getByLabelText('Alamat server dashboard')).toHaveValue(
      window.location.origin + '/',
    );
    expect(router.state.location.pathname).toMatch(/^\/crawler\/tiktok\/jobs\//);
    expect(router.state.location.search).not.toContain((code as HTMLInputElement).value);
    expect(JSON.stringify(localStorage)).not.toContain((code as HTMLInputElement).value);
    expect(screen.getByText(/Pengambilan dan hitungan durasi belum dimulai/)).toBeInTheDocument();
    await user.click(screen.getByText('Uji alur plugin dalam simulasi'));
    await user.click(screen.getByRole('button', { name: 'Simulasikan plugin terhubung' }));
    expect(await screen.findByText('Chrome terhubung')).toBeInTheDocument();
    expect(await screen.findByText('Post yang sedang dibaca')).toBeInTheDocument();
    expect(screen.getByText('Komentar terbaca').nextElementSibling).toHaveTextContent('12');
    expect(
      screen.getByText('Komentar', { selector: '.platform-numbers span' }).nextElementSibling,
    ).toHaveTextContent('0');
  });
  it('does not expose pairing data to an observer', async () => {
    const job = await newTikTokJob();
    const privateRead = vi.spyOn(demoApi, 'tiktokConnector');
    await mount(`/crawler/tiktok/jobs/${job.id}`, true);
    await screen.findByText(/Pairing dikelola operator/);
    expect(privateRead).not.toHaveBeenCalled();
    expect(screen.queryByLabelText('Kode pairing sementara')).not.toBeInTheDocument();
    await expect(demoApi.tiktokConnector(job.id)).rejects.toThrow('Pengamat');
  });
  it('uses validated discovery from the selected conversation without duplicate inputs', async () => {
    const { user } = await mount();
    await user.selectOptions(
      await screen.findByLabelText(/^Conversation/),
      'conversation-riset-kuliah',
    );
    expect(screen.queryByLabelText(/Queries pencarian/)).not.toBeInTheDocument();
    expect(screen.queryByLabelText('Hashtag TikTok')).not.toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Tinjau & siapkan koneksi Chrome' }));
    expect(
      await screen.findByRole('dialog', { name: 'Siapkan crawling TikTok melalui Chrome?' }),
    ).toBeInTheDocument();
  });
});

describe('plugin connection lifecycle', () => {
  it('waits for a verified connection before starting time and preserves the deadline on reconnect', async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-11-05T05:00:00Z'));
    const job = await newTikTokJob();
    const initialPairing = await demoApi.tiktokConnector(job.id);
    vi.advanceTimersByTime(20 * 60000);
    const waiting = await demoApi.job(job.id);
    expect(waiting.status).toBe('WAITING_CONNECTOR');
    expect(waiting.startedAt).toBeUndefined();
    expect(waiting.deadlineAt).toBeUndefined();
    expect(waiting.platforms[0].counts.qualified).toBe(0);
    expect((await demoApi.tiktokConnector(job.id)).state).toBe('EXPIRED');
    const replacement = await demoApi.renewTikTokConnector(job.id);
    expect(replacement.pairingCode).not.toBe(initialPairing.pairingCode);
    expect((await demoApi.job(job.id)).startedAt).toBeUndefined();
    const connected = await demoApi.demoScenario!(job.id, 'connector-ready');
    expect(connected.startedAt).toBe('2026-11-05T05:20:00.000Z');
    expect(connected.deadlineAt).toBe('2026-11-05T08:20:00.000Z');
    vi.advanceTimersByTime(3000);
    await demoApi.demoScenario!(job.id, 'connector-disconnected');
    const pairing = await demoApi.renewTikTokConnector(job.id);
    expect(pairing.state).toBe('WAITING');
    const resumed = await demoApi.demoScenario!(job.id, 'connector-ready');
    expect(resumed.deadlineAt).toBe(connected.deadlineAt);
    expect(resumed.startedAt).toBe(connected.startedAt);
    expect(JSON.stringify(resumed)).not.toContain(pairing.pairingCode!);
    expect(JSON.stringify(localStorage)).not.toContain(pairing.pairingCode!);
  });
});

describe('same-server plugin transport', () => {
  const response = (): TikTokConnectorSession => ({
    jobId: 'job-a',
    state: 'WAITING',
    bridgeUrl: window.location.origin + '/',
    minimumVersion: '1.2.3',
    pairingCode: 'demo-private-code-12345678901234567890',
    pairingExpiresAt: '2099-01-01T00:00:00Z',
  });
  it('uses the existing project API and binds the private response to the job and dashboard origin', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(
      async () =>
        new Response(JSON.stringify(response()), {
          headers: { 'Content-Type': 'application/json' },
        }),
    );
    await httpApi.tiktokConnector('job-a');
    await httpApi.renewTikTokConnector('job-a');
    expect(fetchMock.mock.calls[0][0]).toContain(
      '/api/v1/projects/university-intelligence/acquisition-jobs/job-a/tiktok-connector',
    );
    expect(fetchMock.mock.calls[0][1]?.credentials).toBe('include');
    expect(fetchMock.mock.calls[1][0]).toContain('/tiktok-connector/pairing');
    expect(fetchMock.mock.calls[1][1]?.method).toBe('POST');
    expect(String(fetchMock.mock.calls[0][0])).not.toContain('demo-private-code');
    expect(String(fetchMock.mock.calls[1][1]?.body)).not.toContain('demo-private-code');
  });
  it('rejects another job, external origins and credential-bearing bridge addresses', () => {
    for (const value of [
      { ...response(), jobId: 'another-job' },
      { ...response(), bridgeUrl: 'https://unrelated.example/' },
      { ...response(), bridgeUrl: window.location.origin + '/?code=private' },
      { ...response(), pairingExpiresAt: undefined },
      { ...response(), state: 'toString' } as unknown as TikTokConnectorSession,
    ])
      expect(() => validateConnectorSession(value, 'job-a', window.location.origin)).toThrow();
  });
  it('keeps CAPTCHA pending when the server has not verified recovery', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ ...response(), state: 'VALIDATION_REQUIRED' }), {
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    expect((await httpApi.resumeTikTokConnector('job-a')).state).toBe('VALIDATION_REQUIRED');
  });
});
