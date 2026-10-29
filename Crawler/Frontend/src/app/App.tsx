import { Component, type ReactNode } from 'react';
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Shell from './Shell';
import Automatic from '../features/Automatic';
import Manual from '../features/Manual';
import JobDetail from '../features/JobDetail';

const router = createBrowserRouter([
  {
    element: <Shell />,
    errorElement: (
      <div className="connection-state">
        <h1>Tampilan perlu dibuka ulang</h1>
        <p>Data pekerjaan server tetap tersedia. Muat ulang untuk membuka kembali workspace.</p>
        <a className="button primary" href="/crawler/automatic">
          Buka workspace
        </a>
      </div>
    ),
    children: [
      { path: '/', element: <Navigate to="/crawler/automatic" replace /> },
      { path: '/crawler/automatic', element: <Automatic /> },
      { path: '/crawler/manual', element: <Manual /> },
      { path: '/crawler/automatic/jobs/:jobId', element: <JobDetail /> },
      { path: '/crawler/manual/jobs/:jobId', element: <JobDetail /> },
      {
        path: '*',
        element: (
          <div className="empty">
            <h1>Halaman tidak ditemukan</h1>
            <a href="/crawler/automatic">Kembali ke Crawler</a>
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
