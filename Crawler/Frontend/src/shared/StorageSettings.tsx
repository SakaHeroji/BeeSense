import { useState } from 'react';
import { Eye, EyeOff, FileSpreadsheet, Database, FolderOpen } from 'lucide-react';
import { demoMode } from './domain';
import type { StorageConfig } from './types';
import { Button, Field } from './ui';

export function StorageSettings({
  value,
  change,
  destinationLocked = false,
}: {
  value: StorageConfig;
  change: (value: StorageConfig) => void;
  destinationLocked?: boolean;
}) {
  const [show, setShow] = useState(false);
  const pg = value.postgresql;
  const pgField = (key: keyof StorageConfig['postgresql'], val: string | number) =>
    change({ ...value, postgresql: { ...pg, [key]: val } });
  const connection = (text: string) => {
    let next = { ...pg, connectionString: text };
    try {
      const uri = new URL(text);
      if (['postgresql:', 'postgres:'].includes(uri.protocol) && uri.hostname)
        next = { ...next, host: uri.hostname.replace(/^\[|\]$/g, ''), port: +(uri.port || '5432') };
    } catch {
      /* Inline validation explains incomplete input on submit. */
    }
    change({ ...value, postgresql: next });
  };
  return (
    <>
      {!destinationLocked && (
        <fieldset className="storage-options">
          <legend className="sr-only">Tempat penyimpanan</legend>
          {(
            [
              ['excel', FileSpreadsheet, 'Excel lokal', 'Berkas per sosmed dan tanggal crawling'],
              ['postgresql', Database, 'PostgreSQL', 'Simpan ke database yang Anda tentukan'],
              ['both', FolderOpen, 'Keduanya', 'Excel lokal dan database PostgreSQL'],
            ] as const
          ).map(([id, Icon, title, description]) => (
            <label
              key={id}
              className={`storage-option ${value.destination === id ? 'selected' : ''}`}
            >
              <input
                type="radio"
                name="storage.destination"
                value={id}
                checked={value.destination === id}
                onChange={() => change({ ...value, destination: id })}
              />
              <Icon size={20} aria-hidden="true" />
              <span>
                <b>{title}</b>
                <small>{description}</small>
              </span>
              {id === 'excel' && <span className="default-label">Default</span>}
            </label>
          ))}
        </fieldset>
      )}
      {value.destination !== 'excel' && (
        <div className="postgres-settings">
          <div className="postgres-address">
            <Field name="storage.host" label="IP address / host PostgreSQL" required>
              {(id) => (
                <input
                  id={id}
                  value={pg.host}
                  onChange={(e) => pgField('host', e.target.value)}
                  placeholder="127.0.0.1…"
                  spellCheck={false}
                />
              )}
            </Field>
            <Field name="storage.port" label="Port" required>
              {(id) => (
                <input
                  id={id}
                  type="number"
                  inputMode="numeric"
                  min={1}
                  max={65535}
                  value={pg.port || ''}
                  onChange={(e) => pgField('port', +e.target.value)}
                />
              )}
            </Field>
          </div>
          <Field
            name="storage.connectionString"
            label="String koneksi PostgreSQL"
            hint={`Kosongkan untuk memakai koneksi server (${pg.connectionEnv}).`}
          >
            {(id) => (
              <input
                id={id}
                type={show ? 'text' : 'password'}
                value={pg.connectionString || ''}
                onChange={(e) => connection(e.target.value)}
                placeholder="postgresql://user:password@host:5432/database…"
                spellCheck={false}
                autoCapitalize="none"
              />
            )}
          </Field>
          <Button
            variant="ghost"
            className="reveal-connection"
            aria-pressed={show}
            onClick={() => setShow(!show)}
          >
            {show ? <EyeOff size={16} aria-hidden="true" /> : <Eye size={16} aria-hidden="true" />}
            {show ? 'Sembunyikan string koneksi' : 'Tampilkan string koneksi'}
          </Button>
          <p className="connection-note">
            String koneksi dari formulir hanya dipakai untuk permintaan ini dan tidak disimpan di
            browser.{' '}
            {demoMode
              ? 'Simulasi tidak terhubung ke PostgreSQL.'
              : 'Server akan memvalidasi koneksi sebelum menjalankan pekerjaan.'}
          </p>
        </div>
      )}
    </>
  );
}
