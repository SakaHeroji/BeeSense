import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { format, resolveConfig } from 'prettier';
import { URL, fileURLToPath } from 'node:url';

// This public projection contains form defaults only. Authentication material
// and PostgreSQL connection strings never enter a browser bundle.
export function publicDefaults(config) {
  const platformKeys = [
    'enabled',
    'queries',
    'hashtags',
    'urls',
    'subreddits',
    'min_posts',
    'min_comments_per_post',
    'max_posts',
    'max_candidates',
    'max_comments',
    'max_replies',
    'max_replies_per_thread',
    'search_results',
  ];
  const select = (source, keys) =>
    Object.fromEntries(keys.filter((key) => key in source).map((key) => [key, source[key]]));
  return {
    ...select(config, [
      'project_id',
      'since',
      'until',
      'include_keywords',
      'exclude_keywords',
      'comment_exclude_keywords',
      'queries',
      'total_seconds',
      'timeout_seconds',
      'delay',
      'exclude_existing_datasets',
      'output_root',
    ]),
    platform_defaults: select(config.platform_defaults || {}, platformKeys),
    platforms: Object.fromEntries(
      Object.entries(config.platforms).map(([name, platform]) => [
        name,
        select(platform, platformKeys),
      ]),
    ),
    storage: {
      destination: config.storage?.destination || 'excel',
      postgresql: {
        host: config.storage?.postgresql?.host || '127.0.0.1',
        port: config.storage?.postgresql?.port || 5432,
        connection_string_env:
          config.storage?.postgresql?.connection_string_env || 'BEESENSE_POSTGRESQL_DSN',
      },
    },
  };
}

const source = fileURLToPath(new URL('../../../config/social_crawler.json', import.meta.url));
const target = fileURLToPath(new URL('../src/shared/crawler-defaults.json', import.meta.url));
if (existsSync(source)) {
  const data = publicDefaults(JSON.parse(readFileSync(source, 'utf8')));
  writeFileSync(
    target,
    await format(JSON.stringify(data), { ...(await resolveConfig(target)), parser: 'json' }),
  );
} else if (!existsSync(target)) {
  throw new Error(
    'Generate public crawler defaults from config/social_crawler.json before building the isolated frontend context.',
  );
}
