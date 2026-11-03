export type Platform = 'youtube' | 'reddit' | 'instagram' | 'tiktok' | 'threads' | 'facebook' | 'x';
export type Mode = 'automatic' | 'url' | 'survey';
export type JobStatus =
  | 'QUEUED'
  | 'RUNNING'
  | 'STOP_REQUESTED'
  | 'FINALIZING'
  | 'COMPLETED'
  | 'PARTIAL'
  | 'FAILED'
  | 'CANCELLED';
export type PlatformStatus =
  | 'PENDING'
  | 'FETCHING'
  | 'WAITING_CAPTCHA'
  | 'RATE_LIMITED'
  | 'TARGET_REACHED'
  | 'EXHAUSTED'
  | 'BLOCKED'
  | 'STOPPED'
  | 'ERROR';
export type Session = { name: string; role: 'operator' | 'observer'; canExport: boolean };
export interface Limits {
  maxUrls: number;
  maxRows: number;
  maxFileBytes: number;
  maxQueries: number;
  maxQueryLength: number;
  maxSubreddits: number;
  maxDuration: number;
  maxPosts: number;
  maxCandidates: number;
  maxComments: number;
  maxReplies: number;
}
export interface Baseline {
  id: string;
  version: number;
  name: string;
  roots: number;
  ready: boolean;
  required: boolean;
}
export interface Capabilities {
  migrationsAvailable?: boolean;
  authAvailable?: boolean;
  platforms: Platform[];
  limits: Limits;
  baselines: Baseline[];
  verificationAvailable: boolean;
}
export type StorageDestination = 'excel' | 'postgresql' | 'both';
export interface StorageConfig {
  destination: StorageDestination;
  postgresql: {
    host: string;
    port: number;
    connectionEnv: string;
    connectionString?: string;
  };
}
export interface PlatformConfig {
  enabled: boolean;
  queries: string;
  hashtags: string;
  target: number;
  minComments: number;
  maxPosts: number | null;
  maxCandidates: number | null;
  maxComments: number | null;
  maxReplies: number | null;
  maxRepliesPerThread: number | null;
}
export interface Config {
  name: string;
  description: string;
  mode: 'automatic' | 'url';
  since: string;
  until: string;
  include: string;
  exclude: string;
  includeMode: 'any' | 'all';
  subreddit: string;
  duration: number | null;
  storage: StorageConfig;
  delay: number;
  timeout: number;
  cooldown: number;
  retries: number;
  captchaWait: number;
  captchaPoll: number;
  baselines: string[];
  urls: string[];
  filtersEnabled: boolean;
  platforms: Record<Platform, PlatformConfig>;
}
export interface FieldError {
  field: string;
  message: string;
}
export interface Plan {
  id: string;
  config: Config;
  expiresAt: string;
  warnings: string[];
}
export interface Counts {
  roots: number;
  qualified: number;
  comments: number;
  replies: number;
  duplicates: number;
  rejected: number;
  candidates: number;
}
export interface PlatformProgress {
  platform: Platform;
  status: PlatformStatus;
  target: number;
  counts: Counts;
  waitUntil?: string;
  retry?: number;
  reason?: string;
}
export interface JobEvent {
  id: string;
  at: string;
  message: string;
  platform?: Platform;
}
export type SeriesPoint = { at: string } & Partial<Record<Platform, number>>;
export interface Dataset {
  id: string;
  version: number;
  schema: string;
  checksum: string;
  partial: boolean;
  rows: number;
  responses?: number;
  textRows?: number;
  nlpSupported: boolean;
}
export interface Job {
  id: string;
  name: string;
  mode: Mode;
  status: JobStatus;
  createdAt: string;
  startedAt?: string;
  deadlineAt?: string;
  updatedAt: string;
  snapshotVersion: number;
  platforms: PlatformProgress[];
  events: JobEvent[];
  series: SeriesPoint[];
  dataset?: Dataset;
  config?: Config;
  reason?: string;
  canStop: boolean;
  demo?: boolean;
  scenario?: string;
}
export interface PreviewRow {
  id: string;
  source: string;
  kind: string;
  text: string;
  context: string;
  date: string;
  role?: string;
  url?: string;
  flag?: string;
}
export interface DatasetFile {
  name: string;
  size: string;
  checksum: string;
  url?: string;
}
export interface DatasetDetail {
  dataset: Dataset;
  rows: PreviewRow[];
  total: number;
  files: DatasetFile[];
  warning?: string;
}
export interface Api {
  prepareTransactionMigration(
    job: Job,
    platform: Platform,
    target: StorageConfig['postgresql'],
  ): Promise<TransactionMigrationPlan>;
  startTransactionMigration(
    plan: TransactionMigrationPlan,
    key: string,
  ): Promise<TransactionMigration>;
  transactionMigration(id: string): Promise<TransactionMigration>;
  authStatus(platform: Platform): Promise<AuthStatus>;
  saveAuth(platform: Platform, value: AuthInput): Promise<AuthStatus>;
  session(): Promise<Session>;
  capabilities(): Promise<Capabilities>;
  jobs(): Promise<Job[]>;
  job(id: string): Promise<Job>;
  validate(config: Config): Promise<Plan>;
  start(plan: Plan, key: string): Promise<Job>;
  stop(id: string): Promise<Job>;
  verification(id: string): Promise<{ url?: string; message: string }>;
  dataset(job: Job, page: number, search: string, source: string): Promise<DatasetDetail>;
  handoff(job: Job, acceptPartial: boolean): Promise<{ id: string }>;
  demoScenario?(id: string, scenario: string): Promise<Job>;
}

export interface AuthInput {
  username: string;
  sessionid: string;
}
export interface AuthStatus {
  platform: Platform;
  username: string;
  hasSession: boolean;
  file: 'config/auth.json';
  demo?: boolean;
}
export interface TransactionMigrationPlan {
  id: string;
  expiresAt: string;
  jobId: string;
  platform: Platform;
  datasetId: string;
  version: number;
  checksum: string;
  crawlDate: string;
  total: number;
  host: string;
  port: number;
}
export interface TransactionMigration extends TransactionMigrationPlan {
  status: 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  phase: string;
  createdAt: string;
  updatedAt: string;
  processed: number;
  inserted: number;
  skipped: number;
  error?: string;
  demo?: boolean;
}
