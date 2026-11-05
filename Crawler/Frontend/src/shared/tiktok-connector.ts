import defaults from './crawler-defaults.json';
import type { TikTokConnectorSession } from './types';

export const connectorVersion = defaults.tiktok_connector.version;
export const connectorStates = {
  WAITING: 'Menunggu plugin Chrome',
  CONNECTED: 'Chrome terhubung',
  VALIDATION_REQUIRED: 'Validasi manual diperlukan',
  DISCONNECTED: 'Koneksi Chrome terputus',
  EXPIRED: 'Kode pairing kedaluwarsa',
  FINISHED: 'Pengambilan berakhir',
} as const;

export function validateConnectorSession(
  value: TikTokConnectorSession,
  jobId: string,
  origin: string,
): TikTokConnectorSession {
  let url: URL;
  try {
    url = new URL(value.bridgeUrl);
  } catch {
    throw new Error('Alamat penghubung tidak valid. Periksa layanan TikTok pada server dashboard.');
  }
  if (
    value.jobId !== jobId ||
    !Object.hasOwn(connectorStates, value.state) ||
    typeof value.minimumVersion !== 'string' ||
    (value.pairingCode !== undefined &&
      (typeof value.pairingCode !== 'string' ||
        !/^[A-Za-z0-9_-]{32,128}$/.test(value.pairingCode) ||
        !value.pairingExpiresAt)) ||
    [value.pairingExpiresAt, value.lastSeenAt].some(
      (date) => date !== undefined && !Number.isFinite(Date.parse(date)),
    ) ||
    (value.thread !== undefined &&
      (!value.thread ||
        typeof value.thread.postId !== 'string' ||
        !Number.isFinite(Date.parse(value.thread.lastActivityAt)) ||
        !['comments', 'replies', 'scrolling', 'waiting'].includes(value.thread.activity) ||
        !['pending', 'exhausted', 'unverified'].includes(value.thread.pagination) ||
        [
          value.thread.comments,
          value.thread.replies,
          value.thread.sourceTotal === undefined ? 0 : value.thread.sourceTotal,
        ].some((count) => !Number.isSafeInteger(count) || count < 0))) ||
    !['http:', 'https:'].includes(url.protocol) ||
    url.origin !== origin ||
    url.pathname !== '/' ||
    url.search ||
    url.hash ||
    url.username ||
    url.password
  )
    throw new Error(
      'Koneksi plugin tidak sesuai transaksi atau server dashboard. Muat ulang status.',
    );
  return value;
}
