import crawlerDefaults from './crawler-defaults.json';
import type { Capabilities, Config, FieldError, Platform, StorageConfig } from './types';

export const projectId = import.meta.env.VITE_PROJECT_ID || 'university-intelligence';
export const demoMode = import.meta.env.VITE_DATA_MODE === 'demo';
export const platforms: Platform[] = [
  'youtube',
  'reddit',
  'instagram',
  'tiktok',
  'threads',
  'facebook',
  'x',
];
export const platformLabels: Record<Platform, string> = {
  youtube: 'YouTube',
  reddit: 'Reddit',
  instagram: 'Instagram',
  tiktok: 'TikTok',
  threads: 'Threads',
  facebook: 'Facebook',
  x: 'X / Twitter',
};
export const platformName = (p: Platform) => platformLabels[p];
export const platformDescription: Record<Platform, string> = {
  youtube: 'Video, komentar & reply',
  reddit: 'Post, diskusi & reply',
  instagram: 'Post, Reels & komentar',
  tiktok: 'Plugin Chrome, video, komentar & balasan',
  threads: 'Post & balasan',
  facebook: 'Post & komentar',
  x: 'Post & balasan',
};
export const platformChartColors: Record<Platform, string> = {
  youtube: '#e86400',
  reddit: '#000000',
  instagram: '#a94400',
  tiktok: '#737373',
  threads: '#ff9e43',
  facebook: '#adadad',
  x: '#663000',
};
export const number = (n: number) => new Intl.NumberFormat('id-ID').format(n);
export const dateTime = (value?: string) =>
  value
    ? new Intl.DateTimeFormat('id-ID', {
        dateStyle: 'medium',
        timeStyle: 'short',
        timeZone: 'Asia/Jakarta',
      }).format(new Date(value)) + ' WIB'
    : 'Belum dimulai';
export const duration = (seconds: number) => {
  const s = Math.max(0, Math.ceil(seconds));
  return `${String(Math.floor(s / 3600)).padStart(2, '0')}:${String(Math.floor(s / 60) % 60).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
};
export const lines = (s: string) => [
  ...new Set(
    s
      .split(/[\n,]/)
      .map((x) => x.trim())
      .filter(Boolean),
  ),
];
export const queryLines = (s: string) => [
  ...new Set(
    s
      .split('\n')
      .map((x) => x.trim())
      .filter(Boolean),
  ),
];
export const isoWib = (s: string) => {
  const d = new Date(`${s.length === 16 ? s + ':00' : s}+07:00`);
  return Number.isFinite(d.getTime()) ? d.toISOString() : '';
};
export function wibInput(value: string | null | undefined): string {
  if (!value || !Number.isFinite(Date.parse(value))) return '';
  const parts = Object.fromEntries(
    new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Asia/Jakarta',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hourCycle: 'h23',
    })
      .formatToParts(new Date(value))
      .map((p) => [p.type, p.value]),
  );
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}`;
}
export function crawlDate(job: { startedAt?: string; createdAt: string }): string {
  if (!job.startedAt || !Number.isFinite(Date.parse(job.startedAt))) return '';
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Jakarta',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(new Date(job.startedAt));
  const p = Object.fromEntries(parts.map((v) => [v.type, v.value]));
  return `${p.year}-${p.month}-${p.day}`;
}
export function crawlDateLabel(value: string): string {
  if (!value || !Number.isFinite(Date.parse(value))) return 'Belum dieksekusi';
  return new Intl.DateTimeFormat('id-ID', {
    timeZone: 'Asia/Jakarta',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date(value + 'T00:00:00+07:00'));
}
export const storageLabels = {
  excel: 'Excel lokal',
  postgresql: 'PostgreSQL',
  both: 'Excel & PostgreSQL',
};
export function redactConfig(config: Config): Config {
  const copy = structuredClone(config);
  if (copy.storage?.postgresql) delete copy.storage.postgresql.connectionString;
  return copy;
}
export function initialConfig(mode: 'automatic' | 'url' = 'automatic', only?: Platform): Config {
  type RawPlatform = {
    enabled?: boolean;
    queries?: string[];
    hashtags?: string[];
    min_posts?: number;
    min_comments_per_post?: number;
    max_posts?: number | null;
    max_candidates?: number | null;
    max_comments?: number | null;
    max_replies?: number | null;
    max_replies_per_thread?: number | null;
  };
  const rawPlatforms = crawlerDefaults.platforms as Record<string, RawPlatform>;
  const configPlatforms = Object.fromEntries(
    platforms.map((name) => {
      const raw = {
        ...crawlerDefaults.platform_defaults,
        ...rawPlatforms[name === 'x' ? 'twitter' : name],
      } as RawPlatform;
      return [
        name,
        {
          enabled: only ? name === only : Boolean(raw.enabled),
          queries: mode === 'automatic' ? (raw.queries || crawlerDefaults.queries).join('\n') : '',
          hashtags: (raw.hashtags || []).join('\n'),
          target: raw.min_posts ?? 1000,
          minComments: mode === 'url' ? 0 : (raw.min_comments_per_post ?? 0),
          maxPosts: raw.max_posts ?? null,
          maxCandidates: raw.max_candidates ?? null,
          maxComments: raw.max_comments ?? null,
          maxReplies: raw.max_replies ?? null,
          maxRepliesPerThread: raw.max_replies_per_thread ?? null,
        },
      ];
    }),
  ) as Config['platforms'];
  return {
    name: '',
    description: '',
    mode,
    since: wibInput(crawlerDefaults.since),
    until: wibInput(crawlerDefaults.until),
    include: crawlerDefaults.include_keywords.join('\n'),
    exclude: crawlerDefaults.exclude_keywords.join('\n'),
    includeMode: 'any',
    subreddit: crawlerDefaults.platforms.reddit.subreddits.join(', '),
    duration: crawlerDefaults.total_seconds as number | null,
    delay: crawlerDefaults.delay.seconds,
    timeout: crawlerDefaults.timeout_seconds,
    cooldown: 360,
    retries: 3,
    captchaWait: 600,
    captchaPoll: 5,
    baselines: crawlerDefaults.exclude_existing_datasets.map((path) =>
      path.split('/').filter(Boolean).at(-1)!,
    ),
    urls: [],
    filtersEnabled: mode === 'automatic',
    platforms: configPlatforms,
    storage: {
      destination: crawlerDefaults.storage.destination as Config['storage']['destination'],
      postgresql: {
        host: crawlerDefaults.storage.postgresql.host,
        port: crawlerDefaults.storage.postgresql.port,
        connectionEnv: crawlerDefaults.storage.postgresql.connection_string_env,
      },
    },
  };
}
export function validateConfig(c: Config, cap: Capabilities): FieldError[] {
  const errors: FieldError[] = [];
  const add = (field: string, message: string) => errors.push({ field, message });
  const range = (field: string, value: number, min: number, max: number) => {
    if (!Number.isInteger(value) || value < min || value > max)
      add(field, `Isi bilangan bulat antara ${number(min)} dan ${number(max)}.`);
  };
  if (!c.name.trim() || c.name.length > 120)
    add('name', 'Isi nama pekerjaan, maksimum 120 karakter.');
  if (c.filtersEnabled) {
    if (!c.since || !c.until) add('dates', 'Pilih tanggal mulai dan akhir dalam WIB.');
    else if (!Number.isFinite(Date.parse(isoWib(c.since))) || isoWib(c.since) >= isoWib(c.until))
      add('dates', 'Waktu akhir harus sesudah waktu mulai.');
  }
  const active = platforms.filter((p) => c.platforms[p].enabled);
  if (!active.length) add('platforms', 'Pilih minimal satu platform.');
  for (const p of active) {
    if (!cap.platforms.includes(p)) add('platforms', `${platformName(p)} belum tersedia.`);
    const v = c.platforms[p];
    const q = queryLines(v.queries);
    if (
      c.mode === 'automatic' &&
      p !== 'instagram' &&
      ((!q.length && !(p === 'tiktok' && lines(v.hashtags).length)) ||
        q.length > cap.limits.maxQueries ||
        q.some(
          (x) =>
            x.length > cap.limits.maxQueryLength || [...x].some((char) => char.charCodeAt(0) < 32),
        ))
    )
      add(
        `${p}.queries`,
        `Isi 1–${cap.limits.maxQueries} query, maksimum ${cap.limits.maxQueryLength} karakter per baris.`,
      );
    if (
      p === 'tiktok' &&
      (lines(v.hashtags).length > cap.limits.maxQueries ||
        lines(v.hashtags).some((tag) => !/^[A-Za-z0-9_]{1,100}$/.test(tag.replace(/^#/, ''))))
    )
      add('tiktok.hashtags', 'Isi hashtag TikTok tanpa spasi, maksimum 100 karakter per hashtag.');
    if (
      c.mode === 'automatic' &&
      p === 'instagram' &&
      (!lines(v.hashtags).length ||
        lines(v.hashtags).some((tag) => !/^[A-Za-z0-9_]{1,64}$/.test(tag.replace(/^#/, ''))))
    )
      add(`${p}.hashtags`, 'Isi hashtag Instagram tanpa spasi, satu per baris.');
    range(`${p}.target`, v.target, c.mode === 'automatic' ? 1 : 0, cap.limits.maxPosts);
    if (v.maxPosts !== null) range(`${p}.maxPosts`, v.maxPosts, 1, cap.limits.maxPosts);
    if (v.maxCandidates !== null)
      range(`${p}.maxCandidates`, v.maxCandidates, 1, cap.limits.maxCandidates);
    if (v.maxComments !== null) range(`${p}.maxComments`, v.maxComments, 1, cap.limits.maxComments);
    range(`${p}.minComments`, v.minComments, 0, cap.limits.maxComments);
    if (v.maxReplies !== null) range(`${p}.maxReplies`, v.maxReplies, 0, cap.limits.maxReplies);
    if (v.maxRepliesPerThread !== null)
      range(`${p}.maxRepliesPerThread`, v.maxRepliesPerThread, 0, 100);
    if (
      (v.maxPosts !== null && v.target > v.maxPosts) ||
      (v.maxCandidates !== null && v.target > v.maxCandidates)
    )
      add(`${p}.target`, 'Target melebihi batas percobaan atau kandidat.');
    if (v.maxComments !== null && v.minComments > v.maxComments)
      add(`${p}.minComments`, 'Minimum komentar melebihi batas komentar.');
  }
  if (
    c.platforms.reddit.enabled &&
    (lines(c.subreddit).length < 1 ||
      lines(c.subreddit).length > cap.limits.maxSubreddits ||
      lines(c.subreddit).some((x) => !/^[A-Za-z0-9_]{2,21}$/.test(x)))
  )
    add('subreddit', `Isi 1–${cap.limits.maxSubreddits} nama subreddit tanpa r/.`);
  if (c.duration !== null) range('duration', c.duration, 1, cap.limits.maxDuration);
  range('delay', c.delay, 0, 300);
  range('timeout', c.timeout, 5, 600);
  range('cooldown', c.cooldown, 1, 10800);
  range('retries', c.retries, 0, 10);
  range('captchaWait', c.captchaWait, 0, 10800);
  range('captchaPoll', c.captchaPoll, 1, 60);
  if (c.mode === 'url' && (!c.urls.length || c.urls.length > cap.limits.maxUrls))
    add('urls', `Pilih 1–${cap.limits.maxUrls} URL valid unik.`);
  for (const b of cap.baselines)
    if (b.required && (!c.baselines.includes(b.id) || !b.ready))
      add('baselines', `Baseline wajib ${b.name} harus tersedia dan dipilih.`);
  for (const id of c.baselines)
    if (!cap.baselines.find((b) => b.id === id && b.ready))
      add('baselines', 'Dataset pengecualian tidak tersedia. Pilih versi yang valid.');
  errors.push(...validateStorage(c.storage));
  return errors;
}
export function validateStorage(storage: StorageConfig): FieldError[] {
  const errors: FieldError[] = [];
  const add = (field: string, message: string) => errors.push({ field, message });
  const range = (field: string, value: number, min: number, max: number) => {
    if (!Number.isInteger(value) || value < min || value > max)
      add(field, `Isi bilangan bulat antara ${number(min)} dan ${number(max)}.`);
  };
  if (!storage || !['excel', 'postgresql', 'both'].includes(storage.destination))
    add('storage.destination', 'Pilih tempat penyimpanan hasil crawling.');
  else if (storage.destination !== 'excel') {
    const pg = storage.postgresql;
    if (!/^[A-Za-z0-9_.:[\]-]{1,253}$/.test(pg.host))
      add('storage.host', 'Isi IP address atau hostname PostgreSQL tanpa protokol.');
    range('storage.port', pg.port, 1, 65535);
    if (pg.connectionString?.trim()) {
      try {
        const uri = new URL(pg.connectionString);
        if (
          !['postgresql:', 'postgres:'].includes(uri.protocol) ||
          !uri.hostname ||
          uri.pathname.length < 2
        )
          throw new Error('uri');
        if (
          uri.hostname.replace(/^\[|\]$/g, '').toLowerCase() !==
            pg.host.replace(/^\[|\]$/g, '').toLowerCase() ||
          +(uri.port || '5432') !== pg.port
        )
          add(
            'storage.connectionString',
            'Host dan port harus sama dengan yang tercantum pada string koneksi.',
          );
      } catch {
        add(
          'storage.connectionString',
          'Gunakan URI postgresql://pengguna:sandi@host:5432/database yang valid.',
        );
      }
    } else if (!/^[A-Z_][A-Z0-9_]*$/.test(pg.connectionEnv))
      add(
        'storage.connectionString',
        'Isi string koneksi PostgreSQL atau pilih koneksi dari konfigurasi server.',
      );
  }
  return errors;
}
export const csvCell = (value: string) =>
  `"${(/^(?:\s*[=+\-@]|[\t\r])/.test(value) ? "'" : '') + value.replaceAll('"', '""')}"`;
export function download(name: string, text: string, type = 'text/csv;charset=utf-8') {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 500);
}
export function safeExternal(value: string | undefined): string | undefined {
  if (!value) return undefined;
  try {
    const u = new URL(value, window.location.origin);
    if (
      !u.username &&
      !u.password &&
      (u.origin === window.location.origin || u.protocol === 'https:')
    )
      return u.href;
  } catch {
    /* Invalid URLs are not actionable. */
  }
  return undefined;
}
