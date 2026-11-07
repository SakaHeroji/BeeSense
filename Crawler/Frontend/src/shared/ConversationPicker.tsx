import { Link } from 'react-router-dom';
import { Bot, FilePenLine, FileSpreadsheet, Tags, Target } from 'lucide-react';
import { conversationOriginLabel, lines, number, queryLines } from './domain';
import type { Conversation } from './types';
import { Field, Notice } from './ui';

export function ConversationPicker({
  conversations,
  value,
  onChange,
  pending = false,
  error,
}: {
  conversations: Conversation[];
  value: string;
  onChange: (conversation: Conversation | null) => void;
  pending?: boolean;
  error?: string;
}) {
  const selected = conversations.find((conversation) => conversation.id === value) || null;
  return (
    <section className="panel conversation-picker" aria-labelledby="conversation-picker-title">
      <div className="conversation-picker-heading">
        <div>
          <span className="step-kicker">1 dari 2</span>
          <h2 id="conversation-picker-title">Pilih conversation riset</h2>
          <p>Judul, keyword, query, dan relevansi diambil dari satu snapshot.</p>
        </div>
        <Link className="button secondary" to="/crawler/conversations">
          <FilePenLine size={17} aria-hidden="true" /> Kelola conversation
        </Link>
      </div>
      {error ? (
        <Notice tone="error">{error}</Notice>
      ) : !pending && !conversations.length ? (
        <Notice>
          Belum ada conversation. Buat conversation manual atau generate draf dari judul sebelum
          crawling.
        </Notice>
      ) : (
        <Field
          name="conversation"
          label="Conversation"
          required
          hint="Mengganti conversation akan mengganti seluruh konteks riset, tetapi tidak mengubah target dan penyimpanan."
        >
          {(id) => (
            <select
              id={id}
              value={value}
              disabled={pending}
              onChange={(event) =>
                onChange(
                  conversations.find((conversation) => conversation.id === event.target.value) ||
                    null,
                )
              }
            >
              <option value="">{pending ? 'Memuat conversation…' : 'Pilih conversation…'}</option>
              {conversations.map((conversation) => (
                <option key={conversation.id} value={conversation.id}>
                  {conversation.title}, versi {conversation.version}
                </option>
              ))}
            </select>
          )}
        </Field>
      )}
      {selected && <ConversationBrief conversation={selected} />}
    </section>
  );
}

export function ConversationBrief({ conversation }: { conversation: Conversation }) {
  const include = lines(conversation.include);
  const queryCount = queryLines(conversation.queries).length;
  const hashtagCount = lines(conversation.hashtags).length;
  return (
    <article
      className="conversation-brief"
      aria-label={`Ringkasan conversation ${conversation.title}`}
    >
      <div className="conversation-brief-title">
        <div>
          <span className={`conversation-origin ${conversation.origin}`}>
            {conversation.origin === 'gemini' ? (
              <Bot size={14} aria-hidden="true" />
            ) : conversation.origin === 'excel' ? (
              <FileSpreadsheet size={14} aria-hidden="true" />
            ) : (
              <FilePenLine size={14} aria-hidden="true" />
            )}
            {conversationOriginLabel(conversation.origin)}
          </span>
          <h3>{conversation.title}</h3>
        </div>
        <span className="conversation-version">v{conversation.version}</span>
      </div>
      <p>{conversation.objective}</p>
      <dl className="conversation-brief-facts">
        <div>
          <dt>
            <Target size={15} aria-hidden="true" /> Threshold relevansi
          </dt>
          <dd>{number(conversation.relevance.threshold * 100)}%</dd>
        </div>
        <div>
          <dt>
            <Tags size={15} aria-hidden="true" /> Discovery
          </dt>
          <dd>
            {queryCount} query, {hashtagCount} hashtag, {include.length} keyword
          </dd>
        </div>
      </dl>
      <div className="conversation-scope">
        <b>Acuan relevansi</b>
        <span>{conversation.relevance.scope}</span>
      </div>
    </article>
  );
}
