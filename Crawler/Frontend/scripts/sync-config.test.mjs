import { test } from 'node:test';
import assert from 'node:assert/strict';
import { publicDefaults } from './sync-config.mjs';
test('public projection excludes authentication and connection secrets at every level', () => {
  const defaults = publicDefaults({
    since: '2026-11-01T00:00:00+07:00',
    total_seconds: null,
    queries: ['kuliah'],
    auth: { password: 'private-sentinel' },
    platform_defaults: { min_posts: 1000, max_comments: null, password: 'private-sentinel' },
    platforms: { instagram: { enabled: true, hashtags: ['kuliah'], cookies: 'private-sentinel' } },
    storage: {
      destination: 'excel',
      postgresql: { host: '192.0.2.4', port: 5432, connection_string: 'private-sentinel' },
    },
  });
  assert.equal(JSON.stringify(defaults).includes('private-sentinel'), false);
  assert.equal(defaults.platform_defaults.min_posts, 1000);
  assert.equal(defaults.platform_defaults.max_comments, null);
  assert.equal(defaults.total_seconds, null);
  assert.equal(defaults.storage.postgresql.connection_string_env, 'BEESENSE_POSTGRESQL_DSN');
});
