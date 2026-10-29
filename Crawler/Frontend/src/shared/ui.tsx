import { FieldErrorsContext } from './context';
import {
  cloneElement,
  isValidElement,
  useContext,
  useEffect,
  useId,
  useRef,
  type ReactNode,
} from 'react';
import { useBlocker } from 'react-router-dom';
import {
  AlertCircle,
  Check,
  ChevronRight,
  LoaderCircle,
  X,
  Play,
  MessageCircle,
  Camera,
  Music,
  AtSign,
  Users,
} from 'lucide-react';
import type { FieldError, JobStatus, Platform } from './types';

export const statusLabels: Record<JobStatus, string> = {
  QUEUED: 'Dalam antrean',
  RUNNING: 'Berjalan',
  STOP_REQUESTED: 'Menghentikan',
  FINALIZING: 'Finalisasi',
  COMPLETED: 'Selesai',
  PARTIAL: 'Hasil parsial',
  FAILED: 'Gagal',
  CANCELLED: 'Dihentikan',
};
export function Badge({ status, children }: { status: string; children?: ReactNode }) {
  return (
    <span className={`badge ${status.toLowerCase()}`}>
      <span className="status-dot" />
      {children || statusLabels[status as JobStatus] || status}
    </span>
  );
}
export function PlatformMark({ platform }: { platform: Platform }) {
  const icons = {
    youtube: Play,
    reddit: MessageCircle,
    instagram: Camera,
    tiktok: Music,
    threads: AtSign,
    facebook: Users,
    x: X,
  };
  const Icon = icons[platform];
  return (
    <span className={`platform-mark ${platform}`} aria-hidden="true">
      <Icon size={20} />
    </span>
  );
}
export function Spinner() {
  return <LoaderCircle size={17} className="spin" aria-label="Memproses" />;
}
export function Button({
  children,
  variant = 'primary',
  loading,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  loading?: boolean;
}) {
  return (
    <button
      type="button"
      {...props}
      disabled={props.disabled || loading}
      className={`button ${variant} ${props.className || ''}`}
    >
      {loading && <Spinner />}
      {children}
    </button>
  );
}
export function Field({
  label,
  hint,
  error,
  children,
  required,
  name,
}: {
  label: string;
  hint?: string;
  error?: string;
  children: (id: string) => ReactNode;
  required?: boolean;
  name?: string;
}) {
  const id = useId();
  const errors = useContext(FieldErrorsContext);
  const fieldName = name || label.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const message = error || errors.find((e) => e.field === fieldName)?.message;
  const child = children(id);
  const control = isValidElement<Record<string, unknown>>(child)
    ? cloneElement(child, {
        name: fieldName,
        autoComplete: 'off',
        'aria-required': required || undefined,
        'aria-invalid': message ? true : undefined,
        'aria-describedby':
          [hint ? `${id}-hint` : '', message ? `${id}-error` : ''].filter(Boolean).join(' ') ||
          undefined,
        ...(/kode|id respons|url|query|subreddit/i.test(label) ? { spellCheck: false } : {}),
      })
    : child;
  return (
    <div className={`field ${message ? 'has-error' : ''}`}>
      <label htmlFor={id}>
        {label}
        {required && (
          <span className="required" aria-label="wajib">
            {' '}
            *
          </span>
        )}
      </label>
      {control}
      {hint && (
        <p className="field-hint" id={`${id}-hint`}>
          {hint}
        </p>
      )}
      {message && (
        <p className="field-error" id={`${id}-error`}>
          {message}
        </p>
      )}
    </div>
  );
}
export function Notice({
  children,
  tone = 'info',
}: {
  children: ReactNode;
  tone?: 'info' | 'warning' | 'error' | 'success';
}) {
  return (
    <div className={`notice ${tone}`} role={tone === 'error' ? 'alert' : undefined}>
      <AlertCircle size={18} />
      <div>{children}</div>
    </div>
  );
}
export function Errors({ errors }: { errors: FieldError[] }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (errors.length) {
      const field = document.getElementsByName(errors[0].field)[0];
      if (field instanceof HTMLElement) field.focus();
      else ref.current?.focus();
    }
  }, [errors]);
  if (!errors.length) return null;
  return (
    <div className="error-summary" role="alert" tabIndex={-1} ref={ref}>
      <strong>Periksa kembali masukan Anda</strong>
      <ul>
        {errors.map((e, i) => (
          <li key={`${e.field}-${i}`}>
            <button
              className="error-link"
              onClick={() => document.getElementsByName(e.field)[0]?.focus()}
            >
              {e.message}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
export function Empty({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="empty">
      <span className="empty-symbol">
        <Check size={24} />
      </span>
      <h3>{title}</h3>
      <p>{children}</p>
    </div>
  );
}
export function Dialog({
  open,
  title,
  children,
  onClose,
}: {
  open: boolean;
  title: string;
  children: ReactNode;
  onClose: () => void;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const id = useId();
  useEffect(() => {
    const d = ref.current;
    if (open && !d?.open) d?.showModal();
    else if (!open && d?.open) d.close();
  }, [open]);
  return (
    <dialog ref={ref} aria-labelledby={id} onCancel={onClose} onClose={onClose}>
      <div className="dialog-top">
        <h2 id={id}>{title}</h2>
        <button className="icon-button" onClick={onClose} aria-label="Tutup dialog">
          <X size={20} />
        </button>
      </div>
      {children}
    </dialog>
  );
}
export function UnsavedGuard({ dirty }: { dirty: boolean }) {
  const blocker = useBlocker(dirty);
  useEffect(() => {
    const handler = (e: BeforeUnloadEvent) => {
      if (dirty) e.preventDefault();
    };
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [dirty]);
  return (
    <Dialog
      open={blocker.state === 'blocked'}
      title="Tinggalkan masukan yang belum disimpan?"
      onClose={() => blocker.state === 'blocked' && blocker.reset()}
    >
      <p>Masukan pada formulir ini belum dikomit. Tetap di halaman untuk melanjutkan pengisian.</p>
      <div className="dialog-actions">
        <Button variant="secondary" onClick={() => blocker.state === 'blocked' && blocker.reset()}>
          Tetap di sini
        </Button>
        <Button variant="danger" onClick={() => blocker.state === 'blocked' && blocker.proceed()}>
          Tinggalkan halaman
        </Button>
      </div>
    </Dialog>
  );
}
export function Stepper({ steps, active }: { steps: string[]; active: number }) {
  return (
    <ol className="stepper" aria-label="Tahap konfigurasi">
      {steps.map((s, i) => (
        <li
          key={s}
          aria-current={i === active ? 'step' : undefined}
          className={i === active ? 'current' : i < active ? 'done' : ''}
        >
          <span>{i < active ? <Check size={14} /> : i + 1}</span>
          <b>{s}</b>
          {i < steps.length - 1 && <ChevronRight size={14} className="step-chevron" />}
        </li>
      ))}
    </ol>
  );
}
