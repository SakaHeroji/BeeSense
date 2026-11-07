import {
  conversationOriginLabel,
  dateTime,
  isoWib,
  lines,
  number,
  platformName,
  platforms,
  storageLabels,
} from './domain';
import type { Config } from './types';
export function ConfigReview({ config }: { config: Config }) {
  return (
    <div className="review-content">
      <h2>Konfigurasi pengambilan</h2>
      <dl className="review-dl">
        <div>
          <dt>Conversation</dt>
          <dd>{config.name}</dd>
        </div>
        <div>
          <dt>Snapshot conversation</dt>
          <dd>
            {config.conversation
              ? `v${config.conversation.version} · ${conversationOriginLabel(config.conversation.origin, true)}`
              : 'Konfigurasi lama tanpa snapshot conversation'}
          </dd>
        </div>
        <div>
          <dt>Mode eksekusi</dt>
          <dd>{config.executionMode === 'parallel' ? 'Parallel' : 'Satu platform'}</dd>
        </div>
        <div>
          <dt>Publikasi mulai</dt>
          <dd>{dateTime(isoWib(config.since))}</dd>
        </div>
        <div>
          <dt>Publikasi sebelum</dt>
          <dd>{dateTime(isoWib(config.until))}</dd>
        </div>
        <div>
          <dt>Durasi maksimum</dt>
          <dd>
            {config.duration === null
              ? 'Tanpa batas waktu'
              : `${number(config.duration / 3600)} jam`}
          </dd>
        </div>
        <div>
          <dt>Kata kunci</dt>
          <dd>
            {number(lines(config.include).length)} include / {number(lines(config.exclude).length)}{' '}
            exclude
          </dd>
        </div>
        {config.conversation && (
          <div>
            <dt>Relevansi</dt>
            <dd>
              Threshold {number(config.conversation.relevance.threshold * 100)}% ·{' '}
              {config.conversation.relevance.scope}
            </dd>
          </div>
        )}
        <div>
          <dt>Penyimpanan</dt>
          <dd>{storageLabels[config.storage.destination]}</dd>
        </div>
        {platforms
          .filter((p) => config.platforms[p].enabled)
          .map((p) => (
            <div key={p}>
              <dt>{platformName(p)}</dt>
              <dd>
                {number(config.platforms[p].target)} post; seluruh komentar dan balasan yang
                tersedia
              </dd>
            </div>
          ))}
      </dl>
    </div>
  );
}
