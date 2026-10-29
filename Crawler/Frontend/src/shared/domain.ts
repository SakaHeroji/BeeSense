import type {
  Capabilities,
  Config,
  FieldError,
  Platform,
  SurveyAnswer,
  SurveyIssue,
  SurveyReview,
  UrlReview,
} from './types';

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
  tiktok: 'Video & komentar',
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
export function initialConfig(mode: 'automatic' | 'url' = 'automatic'): Config {
  const common = {
    enabled: true,
    queries: '',
    target: 1000,
    minComments: mode === 'url' ? 0 : 10,
    maxPosts: 4000,
    maxCandidates: 6000,
    maxComments: 100,
    maxReplies: 30,
    maxRepliesPerThread: 10,
  };
  return {
    name: '',
    description: '',
    mode,
    since: '',
    until: '',
    include: 'kuliah\nkampus\nuniversitas\nbeasiswa\njurusan',
    exclude: 'judi\nslot gacor\npolitik',
    includeMode: 'any',
    subreddit: 'indonesia, karir, indotech',
    duration: 10800,
    delay: 2,
    timeout: 90,
    cooldown: 360,
    retries: 3,
    captchaWait: 600,
    captchaPoll: 5,
    baselines: ['social_20261028_01'],
    urls: [],
    filtersEnabled: mode === 'automatic',
    platforms: {
      youtube: {
        ...common,
        queries: mode === 'automatic' ? 'beasiswa kuliah\njurusan kampus' : '',
      },
      reddit: { ...common, queries: mode === 'automatic' ? 'biaya kuliah\npilihan jurusan' : '' },
      ...Object.fromEntries(
        (['instagram', 'tiktok', 'threads', 'facebook', 'x'] as const).map((p) => [
          p,
          {
            ...common,
            enabled: false,
            queries: mode === 'automatic' ? 'beasiswa kuliah\npilihan kampus' : '',
          },
        ]),
      ),
    } as Record<Platform, Config['platforms'][Platform]>,
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
      (!q.length ||
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
    range(`${p}.target`, v.target, c.mode === 'automatic' ? 1 : 0, cap.limits.maxPosts);
    range(`${p}.maxPosts`, v.maxPosts, 1, cap.limits.maxPosts);
    range(`${p}.maxCandidates`, v.maxCandidates, 1, cap.limits.maxCandidates);
    range(`${p}.maxComments`, v.maxComments, 1, cap.limits.maxComments);
    range(`${p}.minComments`, v.minComments, 0, cap.limits.maxComments);
    range(`${p}.maxReplies`, v.maxReplies, 0, cap.limits.maxReplies);
    range(`${p}.maxRepliesPerThread`, v.maxRepliesPerThread, 0, 100);
    if (v.target > v.maxPosts || v.target > v.maxCandidates)
      add(`${p}.target`, 'Target melebihi batas percobaan atau kandidat.');
    if (v.minComments > v.maxComments)
      add(`${p}.minComments`, 'Minimum komentar melebihi batas komentar.');
  }
  if (
    c.platforms.reddit.enabled &&
    (lines(c.subreddit).length < 1 ||
      lines(c.subreddit).length > cap.limits.maxSubreddits ||
      lines(c.subreddit).some((x) => !/^[A-Za-z0-9_]{2,21}$/.test(x)))
  )
    add('subreddit', `Isi 1–${cap.limits.maxSubreddits} nama subreddit tanpa r/.`);
  range('duration', c.duration, 1, cap.limits.maxDuration);
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
  return errors;
}
export function reviewUrls(inputs: string[], existing = new Set<string>()): UrlReview[] {
  const seen = new Set<string>();
  return inputs.map((input) => {
    const invalid: UrlReview = {
      input,
      status: 'invalid',
      reason: 'Gunakan URL HTTPS post/video lengkap dari salah satu dari 7 platform.',
    };
    let u: URL;
    try {
      u = new URL(input);
    } catch {
      return invalid;
    }
    if (u.protocol !== 'https:' || u.username || u.password || u.port) return invalid;
    const host = u.hostname.toLowerCase();
    let p: Platform | undefined, id: string | undefined, canonical: string | undefined;
    const unsupported = (reason: string): UrlReview => ({
      ...invalid,
      status: 'unsupported',
      reason,
    });
    if (['youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be'].includes(host)) {
      p = 'youtube';
      id =
        host === 'youtu.be'
          ? u.pathname.slice(1)
          : u.pathname === '/watch'
            ? u.searchParams.get('v') || undefined
            : u.pathname.match(/^\/shorts\/([\w-]{11})\/?$/)?.[1];
      if (!id || !/^[\w-]{11}$/.test(id))
        return unsupported('Gunakan tautan video/Shorts, bukan kanal atau playlist.');
      canonical = `https://www.youtube.com/watch?v=${id}`;
    } else if (['reddit.com', 'www.reddit.com', 'old.reddit.com'].includes(host)) {
      p = 'reddit';
      id = u.pathname
        .match(/^\/(?:r\/[A-Za-z0-9_]+\/)?comments\/([a-z0-9]+)(?:\/|$)/i)?.[1]
        ?.toLowerCase();
      if (!id) return unsupported('Gunakan tautan post Reddit, bukan profil/komunitas.');
      canonical = `https://www.reddit.com/comments/${id}/`;
    } else if (['instagram.com', 'www.instagram.com'].includes(host)) {
      p = 'instagram';
      const match = u.pathname.match(/^\/(p|reel|tv)\/([A-Za-z0-9_-]+)\/?$/);
      if (!match)
        return unsupported('Gunakan tautan post/Reel Instagram lengkap, bukan profil atau Story.');
      id = match[2];
      canonical = `https://www.instagram.com/${match[1]}/${id}/`;
    } else if (['tiktok.com', 'www.tiktok.com', 'm.tiktok.com'].includes(host)) {
      p = 'tiktok';
      const match = u.pathname.match(/^\/@([A-Za-z0-9_.]+)\/(video|photo)\/(\d+)\/?$/);
      if (!match)
        return unsupported('Gunakan tautan TikTok lengkap: /@akun/video/ID atau /@akun/photo/ID.');
      id = match[3];
      canonical = `https://www.tiktok.com/@${match[1]}/${match[2]}/${id}`;
    } else if (
      ['threads.com', 'www.threads.com', 'threads.net', 'www.threads.net'].includes(host)
    ) {
      p = 'threads';
      const match = u.pathname.match(/^\/@([A-Za-z0-9_.]+)\/post\/([A-Za-z0-9_-]+)\/?$/);
      if (!match) return unsupported('Gunakan tautan post Threads lengkap: /@akun/post/ID.');
      id = match[2];
      canonical = `https://www.threads.com/@${match[1]}/post/${id}`;
    } else if (['facebook.com', 'www.facebook.com', 'm.facebook.com'].includes(host)) {
      p = 'facebook';
      const match = u.pathname.match(/^\/([A-Za-z0-9_.]+)\/posts\/(\d+|pfbid[A-Za-z0-9]+)\/?$/);
      const owner = u.searchParams.get('id'),
        story = u.searchParams.get('story_fbid');
      const reel = u.pathname.match(/^\/reel\/(\d+)\/?$/);
      if (match) {
        id = `${match[1].toLowerCase()}:${match[2]}`;
        canonical = `https://www.facebook.com/${match[1]}/posts/${match[2]}`;
      } else if (
        ['/story.php', '/permalink.php'].includes(u.pathname) &&
        owner &&
        story &&
        /^\d+$/.test(owner) &&
        /^(?:\d+|pfbid[A-Za-z0-9]+)$/.test(story)
      ) {
        id = `${owner}:${story}`;
        canonical = `https://www.facebook.com/${owner}/posts/${story}`;
      } else if (reel) {
        id = `reel:${reel[1]}`;
        canonical = `https://www.facebook.com/reel/${reel[1]}`;
      } else
        return unsupported(
          'Gunakan permalink post atau Reel Facebook lengkap. Tautan profil/share belum didukung.',
        );
    } else if (
      ['x.com', 'www.x.com', 'twitter.com', 'www.twitter.com', 'mobile.twitter.com'].includes(host)
    ) {
      p = 'x';
      id = u.pathname.match(
        /^\/(?:[A-Za-z0-9_]+\/status|i\/web\/status)\/(\d+)(?:\/(?:photo|video)\/\d+)?\/?$/,
      )?.[1];
      if (!id) return unsupported('Gunakan tautan post X/Twitter lengkap yang memuat /status/ID.');
      canonical = `https://x.com/i/status/${id}`;
    } else
      return unsupported(
        'Host belum didukung. Gunakan permalink lengkap dari 7 platform yang tersedia.',
      );
    const key = `${p}:${id}`;
    const status = seen.has(key) ? 'duplicate' : existing.has(key) ? 'existing' : 'valid';
    seen.add(key);
    return {
      input,
      platform: p,
      nativeId: ['youtube', 'reddit', 'tiktok', 'x'].includes(p) ? id : undefined,
      locatorKey: key,
      canonical,
      status,
      reason:
        status === 'duplicate'
          ? 'Post sama dalam daftar ini.'
          : status === 'existing'
            ? 'Sudah ada dalam baseline terpilih.'
            : 'Format valid; akses konten dan ID asli diverifikasi adapter saat pengambilan.',
    };
  });
}
export const surveyKey = (r: SurveyAnswer) =>
  [projectId, r.survey_id, r.survey_version, r.response_id, r.question_id].join(':');
export const responseKey = (r: SurveyAnswer) =>
  [projectId, r.survey_id, r.survey_version, r.response_id].join(':');
export function validateSurvey(
  rows: SurveyAnswer[],
  known = new Map<string, string>(),
): SurveyReview {
  const issues: SurveyIssue[] = [];
  const groups = new Map<string, { row: SurveyAnswer; index: number }[]>();
  rows.forEach((row, index) => {
    const key = responseKey(row);
    groups.set(key, [...(groups.get(key) || []), { row, index: index + 2 }]);
  });
  let invalid = 0,
    denied = 0,
    duplicate = 0,
    valid = 0;
  const validRows: SurveyAnswer[] = [];
  for (const group of groups.values()) {
    let bad = false,
      noPermission = false;
    const keys = new Set<string>();
    const questionIds = new Set<string>();
    const issue = (index: number, field: string, message: string) => {
      bad = true;
      issues.push({
        row: index,
        responseId: group[0].row.response_id || '(kosong)',
        field,
        message,
      });
    };
    for (const { row: r, index } of group) {
      for (const field of [
        'survey_id',
        'survey_version',
        'response_id',
        'respondent_code',
        'respondent_role',
        'submitted_at',
        'question_id',
        'usage_permission',
        'source_reference',
      ] as const)
        if (!r[field]?.trim()) issue(index, field, 'Field wajib belum diisi.');
      if (r.survey_id !== 'minat-studi' || r.survey_version !== '1')
        issue(index, 'survey_id', 'Pilih template minat-studi versi 1.');
      if (!['prospective_student', 'parent'].includes(r.respondent_role))
        issue(
          index,
          'respondent_role',
          'Peran harus calon mahasiswa atau orang tua sesuai sumber.',
        );
      if (
        !/(Z|[+-]\d{2}:\d{2})$/.test(r.submitted_at) ||
        !Number.isFinite(Date.parse(r.submitted_at))
      )
        issue(
          index,
          'submitted_at',
          'Isi waktu ISO dengan zona, contoh 2026-10-29T10:00:00+07:00.',
        );
      if (!['granted', 'not_granted', 'unknown'].includes(r.usage_permission))
        issue(index, 'usage_permission', 'Nilai izin tidak dikenal.');
      if (r.usage_permission !== 'granted') noPermission = true;
      if (!['Q01', 'Q02'].includes(r.question_id))
        issue(index, 'question_id', 'Pertanyaan hanya Q01 dan Q02 pada template ini.');
      if (r.question_id === 'Q01' && !r.answer_text.trim())
        issue(index, 'answer_text', 'Jawaban teks Q01 wajib diisi.');
      if (r.question_id === 'Q02' && !/^[1-5]$/.test(r.answer_value))
        issue(index, 'answer_value', 'Skala Q02 harus bilangan bulat 1–5.');
      const key = surveyKey(r);
      if (keys.has(key)) issue(index, 'question_id', 'Pertanyaan berulang pada satu respons.');
      keys.add(key);
      questionIds.add(r.question_id);
      const original = known.get(key);
      if (original && original !== JSON.stringify(r))
        issue(index, 'response_id', 'Konflik: kunci sama dengan isi berbeda. Tidak ditimpa.');
      for (const field of [
        'respondent_code',
        'respondent_role',
        'submitted_at',
        'usage_permission',
        'source_reference',
      ] as const)
        if (r[field] !== group[0].row[field])
          issue(index, field, 'Metadata harus konsisten dalam satu respons.');
    }
    if (!questionIds.has('Q01') || !questionIds.has('Q02'))
      issue(group[0].index, 'question_id', 'Respons harus lengkap: Q01 dan Q02.');
    if (bad) invalid++;
    else if (noPermission) {
      denied++;
      issues.push({
        row: group[0].index,
        responseId: group[0].row.response_id,
        field: 'usage_permission',
        message: 'Seluruh respons dikecualikan karena izin pemanfaatan bukan granted.',
      });
    } else if (group.every(({ row }) => known.has(surveyKey(row)))) duplicate++;
    else if (group.some(({ row }) => known.has(surveyKey(row)))) {
      invalid++;
      issues.push({
        row: group[0].index,
        responseId: group[0].row.response_id,
        field: 'response_id',
        message: 'Respons lama tidak lengkap; perlu review, tidak digabung diam-diam.',
      });
    } else {
      valid++;
      validRows.push(...group.map((x) => x.row));
    }
  }
  return {
    id: crypto.randomUUID(),
    fingerprint: JSON.stringify(rows),
    expiresAt: new Date(Date.now() + 300000).toISOString(),
    totalResponses: groups.size,
    answerRows: rows.length,
    validResponses: valid,
    duplicateResponses: duplicate,
    invalidResponses: invalid,
    deniedResponses: denied,
    issues,
    validRows,
  };
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
