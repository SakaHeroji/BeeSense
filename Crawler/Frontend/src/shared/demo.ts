import type {
  Api,
  Capabilities,
  Config,
  Counts,
  Dataset,
  Job,
  SeriesPoint,
  PreviewRow,
  SurveyAnswer,
  SurveyReview,
} from './types';
import {
  initialConfig,
  platforms,
  queryLines,
  reviewUrls,
  surveyKey,
  validateConfig,
  validateSurvey,
} from './domain';

// This adapter NEVER contacts social networks. Only job metadata (never survey answers) persists.
const storageKey = 'beesense:crawler:demo-jobs:v2';
const plans = new Map<string, { config: Config; expiresAt: string }>();
const reviews = new Map<string, SurveyReview>();
const surveyKnown = new Map<string, string>();
const surveyDatasets = new Map<string, SurveyAnswer[]>();
const committed = new Map<string, Job>();
let jobCache: Job[] | undefined;
const cap: Capabilities = {
  platforms,
  verificationAvailable: false,
  surveySchemaSupported: false,
  limits: {
    maxUrls: 100,
    maxRows: 10000,
    maxFileBytes: 10485760,
    maxQueries: 100,
    maxQueryLength: 300,
    maxSubreddits: 10,
    maxDuration: 86400,
    maxPosts: 10000,
    maxCandidates: 20000,
    maxComments: 2000,
    maxReplies: 1000,
  },
  baselines: [
    {
      id: 'social_20261028_01',
      name: 'social_20261028_01',
      version: 1,
      roots: 231,
      ready: true,
      required: true,
    },
  ],
};
const stamp = () => new Date().toISOString();
const emptyCounts = (): Counts => ({
  roots: 0,
  qualified: 0,
  comments: 0,
  replies: 0,
  duplicates: 0,
  rejected: 0,
  candidates: 0,
});
const zeros = '0'.repeat(64);
function dataset(job: Job, partial: boolean): Dataset {
  const rows = job.platforms.reduce(
    (n, p) => n + p.counts.roots + p.counts.comments + p.counts.replies,
    0,
  );
  return {
    id: `demo-${job.id}`,
    version: 1,
    schema: 'social.v1',
    checksum: zeros,
    partial,
    rows,
    nlpSupported: job.platforms.every((p) => ['youtube', 'reddit'].includes(p.platform)),
  };
}
function seed(): Job[] {
  const config = initialConfig();
  config.name = 'Percakapan tentang pilihan kuliah';
  config.since = '2026-10-01T00:00';
  config.until = '2026-10-29T00:00';
  const at = new Date(Date.now() - 4 * 3600000).toISOString();
  const job: Job = {
    id: 'demo-riset-001',
    name: config.name,
    mode: 'automatic',
    status: 'PARTIAL',
    createdAt: at,
    startedAt: at,
    deadlineAt: new Date(Date.parse(at) + 10800000).toISOString(),
    updatedAt: new Date(Date.parse(at) + 10800000).toISOString(),
    snapshotVersion: 1,
    config,
    canStop: false,
    demo: true,
    reason: 'Contoh sintetis: batas waktu tercapai; sebagian post belum memenuhi minimum komentar.',
    platforms: [
      {
        platform: 'youtube',
        status: 'STOPPED',
        target: 1000,
        counts: {
          roots: 450,
          qualified: 300,
          comments: 3200,
          replies: 900,
          duplicates: 45,
          rejected: 32,
          candidates: 527,
        },
      },
      {
        platform: 'reddit',
        status: 'STOPPED',
        target: 1000,
        counts: {
          roots: 98,
          qualified: 58,
          comments: 500,
          replies: 200,
          duplicates: 12,
          rejected: 20,
          candidates: 130,
        },
      },
    ],
    events: [
      { id: 'e1', at, message: 'Contoh pekerjaan sintetis, bukan hasil crawling sebenarnya.' },
    ],
    series: [0, 1, 2, 3].map((i) => ({
      at: new Date(Date.parse(at) + i * 3600000).toISOString(),
      youtube: i * 100,
      reddit: Math.round((i * 58) / 3),
    })),
  };
  job.dataset = dataset(job, true);
  return [job];
}
function load(): Job[] {
  if (jobCache) return jobCache;
  try {
    const saved: unknown = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (
      Array.isArray(saved) &&
      saved.every((x) => typeof x?.id === 'string' && x.demo === true && Array.isArray(x.platforms))
    )
      return (jobCache = saved as Job[]);
  } catch {
    /* A corrupt browser cache must not break the app. */
  }
  return (jobCache = seed());
}
function save(jobs: Job[]) {
  jobCache = jobs;
  try {
    localStorage.setItem(storageKey, JSON.stringify(jobs));
  } catch {
    /* UI still works in memory when storage is unavailable. */
  }
}
function get(id: string) {
  const j = load().find((x) => x.id === id);
  if (!j) throw new Error('Pekerjaan simulasi tidak ditemukan. Kembali ke riwayat.');
  return j;
}
function requireOperator() {
  if (sessionStorage.getItem('beesense:demo-role') === 'observer')
    throw new Error('Pengamat tidak memiliki izin melakukan tindakan ini.');
}
function update(job: Job): Job {
  save(load().map((j) => (j.id === job.id ? job : j)));
  return structuredClone(job);
}
function advance(job: Job): Job {
  if (!['QUEUED', 'RUNNING', 'STOP_REQUESTED', 'FINALIZING'].includes(job.status)) return job;
  const elapsed = Math.max(0, (Date.now() - Date.parse(job.createdAt)) / 1000);
  if (
    job.status === 'STOP_REQUESTED' ||
    (job.status === 'FINALIZING' && job.reason === 'Dihentikan operator.')
  ) {
    const next = {
      ...job,
      status: 'CANCELLED' as const,
      canStop: false,
      updatedAt: stamp(),
      dataset: dataset(job, true),
    };
    return update(next);
  }
  const deadlineReached = job.deadlineAt ? Date.now() >= Date.parse(job.deadlineAt) : false;
  const scenario = job.scenario;
  const blocked = ['captcha', '429'].includes(scenario || '');
  const finish = (elapsed >= 40 && !blocked) || deadlineReached;
  job.status =
    elapsed < 2
      ? 'QUEUED'
      : finish
        ? elapsed < 44 && !deadlineReached
          ? 'FINALIZING'
          : scenario === 'export-error'
            ? 'FAILED'
            : deadlineReached
              ? 'PARTIAL'
              : 'COMPLETED'
        : 'RUNNING';
  if (job.status === 'RUNNING' && !job.startedAt) {
    job.startedAt = stamp();
    job.deadlineAt = new Date(Date.now() + (job.config?.duration || 10800) * 1000).toISOString();
  }
  const ratio = Math.min(1, Math.max(0, (elapsed - 2) / 38));
  job.platforms = job.platforms.map((p) => {
    const waiting = p.platform === 'reddit' && blocked;
    const previous = p.counts;
    const target =
      job.config?.mode === 'url'
        ? job.config.urls.filter((u) => reviewUrls([u])[0].platform === p.platform).length
        : p.target;
    const qualified = waiting ? previous.qualified : Math.round(target * ratio);
    const extra = job.mode === 'url' ? 0 : Math.round(qualified * 0.12);
    const roots = Math.min(target + extra, qualified + extra);
    return {
      ...p,
      target,
      counts: waiting
        ? previous
        : {
            roots,
            qualified,
            comments: roots * 12,
            replies: roots * 2,
            duplicates: Math.round(roots * 0.08),
            rejected: Math.round(roots * 0.03),
            candidates: Math.round(roots * 1.2),
          },
      status: waiting
        ? scenario === 'captcha'
          ? 'WAITING_CAPTCHA'
          : 'RATE_LIMITED'
        : ratio === 1
          ? 'TARGET_REACHED'
          : 'FETCHING',
      reason: waiting ? 'Hambatan simulasi; tidak ada request ke Reddit.' : undefined,
    };
  });
  job.canStop = ['QUEUED', 'RUNNING'].includes(job.status);
  job.updatedAt = stamp();
  job.snapshotVersion++;
  const point: SeriesPoint = {
    at: stamp(),
    ...Object.fromEntries(job.platforms.map((p) => [p.platform, p.counts.qualified])),
  };
  job.series = [...job.series.slice(-29), point];
  if (['COMPLETED', 'PARTIAL'].includes(job.status))
    job.dataset = dataset(job, job.status === 'PARTIAL');
  if (job.status === 'FAILED')
    job.reason = 'Simulasi kegagalan ekspor. Tidak ada berkas final yang diterbitkan.';
  if (job.status === 'PARTIAL')
    job.reason = 'Deadline simulasi tercapai. Target belum seluruhnya terpenuhi.';
  return update(job);
}
export const demoApi: Api = {
  async session() {
    const observer = sessionStorage.getItem('beesense:demo-role') === 'observer';
    return {
      name: observer ? 'Pengamat demo' : 'Operator demo',
      role: observer ? 'observer' : 'operator',
      canExport: !observer,
    };
  },
  async capabilities() {
    return structuredClone(cap);
  },
  async jobs() {
    return load().map((j) => structuredClone(advance(j)));
  },
  async job(id) {
    return structuredClone(advance(get(id)));
  },
  async validate(config) {
    requireOperator();
    const errors = validateConfig(config, cap);
    if (errors.length) throw new Error(errors.map((e) => e.message).join(' '));
    if (
      config.mode === 'url' &&
      reviewUrls(config.urls, new Set(['youtube:dQw4w9WgXcQ'])).some((r) => r.status !== 'valid')
    )
      throw new Error('Daftar URL harus valid dan unik; ulangi validasi URL.');
    const id = crypto.randomUUID(),
      expiresAt = new Date(Date.now() + 300000).toISOString();
    plans.set(id, { config: structuredClone(config), expiresAt });
    return {
      id,
      config: structuredClone(config),
      expiresAt,
      warnings: [
        'Mode simulasi: proses dipercepat menjadi sekitar 45 detik, tanpa mengakuisisi data sebenarnya.',
        ...(config.platforms.reddit.enabled
          ? ['Sesi CAPTCHA worker tidak tersedia dalam simulasi.']
          : []),
      ],
    };
  },
  async start(plan, key) {
    requireOperator();
    const existing = load().find((j) => j.id === `demo-${key}`);
    if (existing) return structuredClone(existing);
    const entry = plans.get(plan.id);
    if (
      !entry ||
      Date.parse(entry.expiresAt) <= Date.now() ||
      JSON.stringify(entry.config) !== JSON.stringify(plan.config)
    )
      throw new Error('Validasi rencana kedaluwarsa. Validasi ulang sebelum mulai.');
    const config = entry.config;
    const job: Job = {
      id: `demo-${key}`,
      name: config.name,
      mode: config.mode,
      createdAt: stamp(),
      updatedAt: stamp(),
      status: 'QUEUED',
      canStop: true,
      snapshotVersion: 1,
      config: structuredClone(config),
      demo: true,
      platforms: platforms
        .filter((p) => config.platforms[p].enabled)
        .map((p) => ({
          platform: p,
          target:
            config.mode === 'url'
              ? config.urls.filter((u) => reviewUrls([u])[0].platform === p).length
              : config.platforms[p].target,
          status: 'PENDING',
          counts: emptyCounts(),
        })),
      events: [
        {
          id: crypto.randomUUID(),
          at: stamp(),
          message: `Rencana simulasi diterima: ${platforms.filter((p) => config.platforms[p].enabled).reduce((sum, p) => sum + queryLines(config.platforms[p].queries).length, 0)} query; tidak ada crawling nyata.`,
        },
      ],
      series: [],
    };
    save([job, ...load()].slice(0, 60));
    return structuredClone(job);
  },
  async stop(id) {
    requireOperator();
    const job = get(id);
    if (!job.canStop) return job;
    return update({
      ...job,
      status: 'STOP_REQUESTED',
      canStop: false,
      reason: 'Dihentikan operator.',
      events: [
        ...job.events,
        {
          id: crypto.randomUUID(),
          at: stamp(),
          message: 'Permintaan berhenti diterima. Hasil parsial akan difinalisasi.',
        },
      ],
    });
  },
  async verification(id) {
    requireOperator();
    get(id);
    return {
      message:
        'Simulasi tidak mempunyai browser worker. Pada mode API, tindakan ini harus membuka sesi worker yang terotorisasi; akses tidak ditandai pulih dari browser ini.',
    };
  },
  async reviewUrls(urls, baselineIds) {
    return reviewUrls(urls, new Set(baselineIds.length ? ['youtube:dQw4w9WgXcQ'] : []));
  },
  async validateSurvey(rows) {
    requireOperator();
    if (rows.length > cap.limits.maxRows) throw new Error('Batas 10.000 baris jawaban terlampaui.');
    const result = validateSurvey(rows, surveyKnown);
    reviews.set(result.id, structuredClone(result));
    return result;
  },
  async commitSurvey(review, key) {
    requireOperator();
    if (committed.has(key)) return structuredClone(committed.get(key)!);
    const current = reviews.get(review.id);
    if (
      !current ||
      current.fingerprint !== review.fingerprint ||
      Date.parse(current.expiresAt) <= Date.now()
    )
      throw new Error('Review survei kedaluwarsa; validasi ulang.');
    const recheck = validateSurvey(current.validRows, surveyKnown);
    if (recheck.validResponses !== current.validResponses || !current.validResponses)
      throw new Error('Data berubah/duplikat sejak review. Validasi ulang.');
    current.validRows.forEach((r) => surveyKnown.set(surveyKey(r), JSON.stringify(r)));
    const id = `demo-survey-${key}`;
    const datasetId = `demo-data-${key}`;
    surveyDatasets.set(datasetId, structuredClone(current.validRows));
    const job: Job = {
      id,
      name: 'Survei minat studi · batch manual',
      mode: 'survey',
      status: 'COMPLETED',
      createdAt: stamp(),
      startedAt: stamp(),
      updatedAt: stamp(),
      snapshotVersion: 1,
      platforms: [],
      series: [],
      canStop: false,
      demo: true,
      events: [
        {
          id: crypto.randomUUID(),
          at: stamp(),
          message: 'Respons valid dikomit dalam memori demo, bukan ke server.',
        },
      ],
      dataset: {
        id: datasetId,
        version: 1,
        schema: 'survey.v1',
        checksum: zeros,
        partial: false,
        rows: current.validRows.length,
        responses: current.validResponses,
        textRows: current.validRows.filter((r) => r.answer_text.trim()).length,
        nlpSupported: false,
      },
    };
    committed.set(key, job);
    save([job, ...load()]);
    return structuredClone(job);
  },
  async dataset(job, page, search, source) {
    const ds = job.dataset!;
    const survey = surveyDatasets.get(ds.id);
    let rows: PreviewRow[];
    if (job.mode === 'survey')
      rows = (survey || []).map((r, i) => ({
        id: `${r.response_id}/${r.question_id}/${i}`,
        source: 'survey',
        kind: 'Jawaban survei',
        text: r.answer_text || r.answer_value,
        context:
          r.question_id === 'Q01'
            ? 'Apa pertimbangan utama memilih jurusan?'
            : 'Seberapa penting biaya kuliah? (1–5)',
        role: r.respondent_role === 'parent' ? 'Orang tua' : 'Calon mahasiswa',
        date: r.submitted_at,
        flag: `Template ${r.survey_id} v${r.survey_version}; izin ${r.usage_permission}; asal ${r.source_reference}`,
      }));
    else
      rows = Array.from({ length: Math.min(ds.rows, 125) }, (_, i) => {
        const platform = job.platforms[i % job.platforms.length]?.platform || 'youtube';
        return {
          id: `sintetis-${i + 1}`,
          source: platform,
          kind: ['Post', 'Komentar', 'Reply'][i % 3],
          text: [
            'Saya ingin memilih jurusan sesuai minat dan peluang kerja.',
            'Informasi biaya kuliah dan beasiswa sangat membantu.',
            'Lokasi kampus dan dukungan keluarga menjadi pertimbangan.',
          ][i % 3],
          context: 'Contoh sintetis percakapan pilihan kuliah',
          date: job.createdAt,
          role: 'Tidak diketahui',
          flag: 'Data ilustrasi; bukan konten pengguna sebenarnya.',
        };
      });
    rows = rows.filter(
      (r) =>
        (!source || r.source === source) &&
        (!search ||
          `${r.text} ${r.context} ${r.role}`.toLowerCase().includes(search.toLowerCase())),
    );
    return {
      dataset: ds,
      total: rows.length,
      rows: rows.slice((page - 1) * 50, page * 50),
      files: [
        {
          name: 'preview-sintetis.csv',
          size: 'Dibuat saat unduh',
          checksum: 'Tidak berlaku untuk simulasi',
        },
        {
          name: 'manifest-simulasi.json',
          size: 'Metadata simulasi',
          checksum: 'Tidak berlaku untuk simulasi',
        },
      ],
      warning:
        job.mode === 'survey' && !survey
          ? 'Jawaban survei demo hanya disimpan dalam memori. Setelah refresh, impor ulang untuk melihat preview; jawaban tidak disimpan di browser storage.'
          : job.mode !== 'survey'
            ? 'Preview berisi maksimum 125 baris sintetis. Angka progres bukan jumlah data nyata.'
            : undefined,
    };
  },
  async handoff(job, acceptPartial) {
    requireOperator();
    if (!job.dataset?.rows || !job.dataset.nlpSupported || (job.dataset.partial && !acceptPartial))
      throw new Error('Dataset kosong, parsial belum diterima, atau skema NLP belum didukung.');
    return { id: `demo-selection-${job.dataset.id}-v${job.dataset.version}` };
  },
  async demoScenario(id, scenario) {
    requireOperator();
    const job = get(id);
    const next = {
      ...job,
      scenario,
      events: [
        ...job.events,
        {
          id: crypto.randomUUID(),
          at: stamp(),
          message: `Skenario simulasi diubah: ${scenario || 'normal'}.`,
        },
      ],
    };
    next.platforms = next.platforms.map((p) => ({
      ...p,
      waitUntil: new Date(
        Date.now() + (scenario === '429' ? Math.max(job.config?.cooldown || 360, 600) : 600) * 1000,
      ).toISOString(),
      retry: 1,
    }));
    return update(next);
  },
};
