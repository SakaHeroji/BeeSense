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
  platforms: Platform[];
  limits: Limits;
  baselines: Baseline[];
  verificationAvailable: boolean;
  surveySchemaSupported: boolean;
}
export interface PlatformConfig {
  enabled: boolean;
  queries: string;
  target: number;
  minComments: number;
  maxPosts: number;
  maxCandidates: number;
  maxComments: number;
  maxReplies: number;
  maxRepliesPerThread: number;
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
  duration: number;
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
export type UrlStatus = 'valid' | 'duplicate' | 'existing' | 'unsupported' | 'invalid';
export interface UrlReview {
  input: string;
  canonical?: string;
  nativeId?: string;
  locatorKey?: string;
  platform?: Platform;
  status: UrlStatus;
  reason: string;
}
export const surveyFields = [
  'survey_id',
  'survey_version',
  'response_id',
  'respondent_code',
  'respondent_role',
  'submitted_at',
  'question_id',
  'answer_text',
  'answer_value',
  'usage_permission',
  'source_reference',
] as const;
export type SurveyField = (typeof surveyFields)[number];
export type SurveyAnswer = Record<SurveyField, string>;
export interface SurveyIssue {
  row: number;
  responseId: string;
  field: string;
  message: string;
}
export interface SurveyReview {
  id: string;
  fingerprint: string;
  expiresAt: string;
  totalResponses: number;
  answerRows: number;
  validResponses: number;
  duplicateResponses: number;
  invalidResponses: number;
  deniedResponses: number;
  issues: SurveyIssue[];
  validRows: SurveyAnswer[];
}
export interface Api {
  session(): Promise<Session>;
  capabilities(): Promise<Capabilities>;
  jobs(): Promise<Job[]>;
  job(id: string): Promise<Job>;
  validate(config: Config): Promise<Plan>;
  start(plan: Plan, key: string): Promise<Job>;
  stop(id: string): Promise<Job>;
  verification(id: string): Promise<{ url?: string; message: string }>;
  reviewUrls(urls: string[], baselines: string[]): Promise<UrlReview[]>;
  validateSurvey(rows: SurveyAnswer[]): Promise<SurveyReview>;
  commitSurvey(review: SurveyReview, key: string): Promise<Job>;
  dataset(job: Job, page: number, search: string, source: string): Promise<DatasetDetail>;
  handoff(job: Job, acceptPartial: boolean): Promise<{ id: string }>;
  demoScenario?(id: string, scenario: string): Promise<Job>;
}
