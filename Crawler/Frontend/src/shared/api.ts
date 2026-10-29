import type { Api, Config, Job, Plan, SurveyAnswer, SurveyReview } from './types';
import { demoMode, projectId } from './domain';
import { demoApi } from './demo';

export class ApiError extends Error {
  constructor(
    message: string,
    public status = 0,
    public fields: { field: string; message: string }[] = [],
  ) {
    super(message);
  }
}
const base = (import.meta.env.VITE_API_BASE_URL || '/api/v1').replace(/\/$/, '');
async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${base}/projects/${encodeURIComponent(projectId)}${path}`, {
      credentials: 'include',
      signal: AbortSignal.timeout(20000),
      ...options,
      headers: {
        Accept: 'application/json',
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
    });
  } catch {
    throw new ApiError(
      'Server belum dapat dihubungi. Periksa koneksi lalu coba lagi; permintaan sebelumnya mungkin sudah diterima.',
    );
  }
  if (!response.headers.get('content-type')?.includes('application/json'))
    throw new ApiError('Backend Crawler belum tersedia pada alamat API ini.', response.status);
  const data = await response.json();
  if (!response.ok)
    throw new ApiError(
      response.status === 401
        ? 'Sesi berakhir. Masuk kembali melalui penyedia autentikasi organisasi.'
        : response.status === 403
          ? 'Anda tidak memiliki izin untuk tindakan ini.'
          : data.message || 'Permintaan belum berhasil. Coba lagi setelah memeriksa status.',
      response.status,
      data.fields || [],
    );
  return data as T;
}
const post = <T>(path: string, data: unknown, key?: string) =>
  request<T>(path, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: key ? { 'Idempotency-Key': key } : {},
  });
const jobPath = (id: string) => `/acquisition-jobs/${encodeURIComponent(id)}`;
export const httpApi: Api = {
  session: () => request('/session'),
  capabilities: () => request('/crawler/capabilities'),
  jobs: () => request('/acquisition-jobs'),
  job: (id) => request(jobPath(id)),
  validate: (config: Config) => post('/acquisition-plans/validate', { config }),
  start: (plan: Plan, key: string) => post('/acquisition-jobs', { plan_id: plan.id }, key),
  stop: (id) => post(`${jobPath(id)}/stop`, {}),
  verification: (id) => post(`${jobPath(id)}/verification-session`, {}),
  reviewUrls: (urls, baselines) => post('/crawler/urls/validate', { urls, baselines }),
  validateSurvey: (rows: SurveyAnswer[]) => post('/survey-imports/validate', { rows }),
  commitSurvey: (review: SurveyReview, key: string) =>
    post(
      `/survey-imports/${encodeURIComponent(review.id)}/commit`,
      { validation_id: review.id, fingerprint: review.fingerprint, accept_valid_only: true },
      key,
    ),
  dataset: (job: Job, page: number, search: string, source: string) =>
    request(
      `/datasets/${encodeURIComponent(job.dataset!.id)}/versions/${job.dataset!.version}?${new URLSearchParams({ page: String(page), search, source })}`,
    ),
  handoff: (job, acceptPartial) =>
    post('/nlp-input-selections', {
      dataset_id: job.dataset!.id,
      version: job.dataset!.version,
      checksum: job.dataset!.checksum,
      accept_partial: acceptPartial,
    }),
};
export const api: Api = demoMode ? demoApi : httpApi;
