import type { Job, TikTokConnectorSession, TikTokConnectorState } from './types';
import { connectorVersion } from './tiktok-connector';

// Pairing data stays in memory, outside the persisted demo job snapshots.
const connections = new Map<string, TikTokConnectorSession>();
export const isTikTokJob = (job: Job) => job.platforms.some((p) => p.platform === 'tiktok');
export function demoConnection(job: Job): TikTokConnectorSession {
  let value = connections.get(job.id);
  if (!value) {
    value = {
      jobId: job.id,
      state: job.startedAt ? 'DISCONNECTED' : 'WAITING',
      bridgeUrl: window.location.origin + '/',
      minimumVersion: connectorVersion,
      pairingCode: `demo-${crypto.randomUUID().replaceAll('-', '')}`,
      pairingExpiresAt: new Date(Date.now() + 600000).toISOString(),
      demo: true,
    };
    connections.set(job.id, value);
  }
  if (['COMPLETED', 'PARTIAL', 'FAILED', 'CANCELLED'].includes(job.status)) {
    value.state = 'FINISHED';
    delete value.pairingCode;
  } else if (value.state === 'WAITING' && Date.parse(value.pairingExpiresAt!) <= Date.now()) {
    value.state = 'EXPIRED';
  }
  job.connector = { state: value.state, version: value.version, lastSeenAt: value.lastSeenAt };
  const copy = structuredClone(value);
  if (value.state === 'CONNECTED') {
    copy.thread = {
      postId: 'post-contoh-sintetis',
      comments: 12,
      replies: 4,
      sourceTotal: 60,
      activity: 'scrolling',
      pagination: 'pending',
      lastActivityAt: new Date().toISOString(),
    };
  }
  return copy;
}
export function changeDemoConnection(job: Job, state: TikTokConnectorState) {
  demoConnection(job);
  const value = connections.get(job.id)!;
  value.state = state;
  if (state === 'WAITING') {
    value.pairingCode = `demo-${crypto.randomUUID().replaceAll('-', '')}`;
    value.pairingExpiresAt = new Date(Date.now() + 600000).toISOString();
  }
  if (state === 'CONNECTED') {
    value.version = connectorVersion;
    value.build = 'simulasi-frontend';
    value.lastSeenAt = new Date().toISOString();
    delete value.pairingCode;
  }
  return demoConnection(job);
}
