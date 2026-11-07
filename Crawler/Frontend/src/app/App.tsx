import { Component, lazy, type ReactNode } from 'react';
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Shell from './Shell';
const PlatformWorkspace = lazy(() => import('../features/PlatformWorkspace'));
const ConversationWorkspace = lazy(() => import('../features/ConversationWorkspace'));
const ParallelWorkspace = lazy(() => import('../features/ParallelWorkspace'));
const JobDetail = lazy(() => import('../features/JobDetail'));

const router = createBrowserRouter([
  {
    element: <Shell />,
    errorElement: (
      <div className="connection-state">
        <h1>Tampilan perlu dibuka ulang</h1>
        <p>Data pekerjaan server tetap tersedia. Muat ulang untuk membuka kembali workspace.</p>
        <a className="button primary" href="/crawler/conversations">
          Buka workspace
        </a>
      </div>
    ),
    children: [
      { path: '/', element: <Navigate to="/crawler/conversations" replace /> },
      { path: '/crawler/conversations', element: <ConversationWorkspace /> },
      { path: '/crawler/parallel', element: <ParallelWorkspace /> },
      { path: '/crawler/automatic', element: <Navigate to="/crawler/parallel" replace /> },
      { path: '/crawler/:platform', element: <PlatformWorkspace /> },
      { path: '/crawler/:platform/jobs/:jobId', element: <JobDetail /> },
      { path: '/crawler/parallel/jobs/:jobId', element: <JobDetail /> },
      { path: '/crawler/automatic/jobs/:jobId', element: <JobDetail /> },
      {
        path: '*',
        element: (
          <div className="empty">
            <h1>Halaman tidak ditemukan</h1>
            <a href="/crawler/conversations">Kembali ke Crawler</a>
          </div>
        ),
      },
    ],
  },
]);
class ErrorBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  render() {
    return this.state.failed ? (
      <div className="connection-state">
        <h1>Tampilan perlu dimuat ulang</h1>
        <p>
          Terjadi masalah pada antarmuka. Pekerjaan di server tidak dihentikan oleh masalah tampilan
          ini.
        </p>
        <button className="button primary" onClick={() => window.location.reload()}>
          Muat ulang
        </button>
      </div>
    ) : (
      this.props.children
    );
  }
}
const client = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 10000, refetchOnWindowFocus: true },
    mutations: { retry: false },
  },
});
export default function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={client}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ErrorBoundary>
  );
}
