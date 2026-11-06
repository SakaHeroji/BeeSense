import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Eye, EyeOff, KeyRound } from 'lucide-react';
import { api } from './api';
import { sessionCookies, sessionPlatforms, validateAuth } from './auth';
import { SessionGuide } from './SessionGuide';
import { demoMode, platformName } from './domain';
import { FieldErrorsContext, useApp } from './context';
import type { AuthInput, FieldError, Platform } from './types';
import { Button, Field, Notice } from './ui';

export function AuthSettings({
  platform,
  value,
  change,
}: {
  platform: Platform;
  value: AuthInput;
  change: (v: AuthInput) => void;
}) {
  const { cap } = useApp();
  const client = useQueryClient();
  const [show, setShow] = useState(false);
  const [errors, setErrors] = useState<FieldError[]>([]);
  const supported = sessionPlatforms.includes(platform);
  const cookie = sessionCookies[platform];
  const available = demoMode || cap.authAvailable === true;
  const query = useQuery({
    queryKey: ['platform-auth', platform],
    queryFn: () => api.authStatus(platform),
    enabled: supported && available,
  });
  const save = useMutation({
    mutationFn: (input: AuthInput) => api.saveAuth(platform, input),
    onSuccess: (result) => {
      client.setQueryData(['platform-auth', platform], result);
      change({ username: '', sessionid: '' });
      setShow(false);
    },
  });
  if (!supported) return null;
  return (
    <section className="panel account-settings" aria-label={`Akun ${platformName(platform)}`}>
      <div className="social-section-heading">
        <div>
          <h2>Akun & sesi</h2>
          <p>Opsional, jika pengambilan memerlukan akun {platformName(platform)}.</p>
        </div>
        <KeyRound size={20} aria-hidden="true" />
      </div>
      <p className="account-file">
        Tujuan penyimpanan <code translate="no">config/auth.json</code>
      </p>
      {query.isPending && available && <p role="status">Memeriksa pengaturan akun…</p>}
      {query.error && (
        <Notice tone="error">
          Pengaturan akun belum dimuat.{' '}
          <Button variant="ghost" onClick={() => void query.refetch()}>
            Coba lagi
          </Button>
        </Notice>
      )}
      {query.data && (
        <p className="field-hint">
          {query.data.username
            ? `Username tersimpan: ${query.data.username}. `
            : 'Belum ada username tersimpan. '}
          {query.data.hasSession
            ? 'Session ID tersedia; nilainya disembunyikan.'
            : 'Belum ada session ID.'}
        </p>
      )}
      <SessionGuide platform={platform} />
      <FieldErrorsContext.Provider value={errors}>
        <Field
          name="username"
          label="Username"
          hint="Kosongkan untuk mempertahankan username yang tersimpan."
        >
          {(id) => (
            <input
              id={id}
              name="socialUsername"
              value={value.username}
              onChange={(e) => {
                change({ ...value, username: e.target.value });
                setErrors([]);
                save.reset();
              }}
              autoComplete="off"
              spellCheck={false}
              autoCapitalize="none"
              disabled={save.isPending}
              placeholder="nama_akun…"
            />
          )}
        </Field>
        <Field
          name="sessionid"
          label="Session ID"
          hint={
            cookie
              ? `Isi nilai cookie ${cookie.name}. Kosongkan untuk memakai sesi yang tersimpan.`
              : 'Opsional; format sesi menunggu integrasi backend. Isian boleh dikosongkan.'
          }
        >
          {(id) => (
            <input
              id={id}
              name="socialSessionId"
              type={show ? 'text' : 'password'}
              value={value.sessionid}
              onChange={(e) => {
                change({ ...value, sessionid: e.target.value });
                setErrors([]);
                save.reset();
              }}
              autoComplete="off"
              spellCheck={false}
              autoCapitalize="none"
              disabled={save.isPending}
              placeholder="Session ID akun…"
            />
          )}
        </Field>
      </FieldErrorsContext.Provider>
      <div className="account-actions">
        <Button variant="ghost" aria-pressed={show} onClick={() => setShow(!show)}>
          {show ? <EyeOff size={16} aria-hidden="true" /> : <Eye size={16} aria-hidden="true" />}
          {show ? 'Sembunyikan sesi' : 'Tampilkan sesi'}
        </Button>
        <Button
          variant="secondary"
          loading={save.isPending}
          disabled={!available}
          onClick={() => {
            const issues = validateAuth(platform, value);
            setErrors(issues);
            if (!issues.length) save.mutate({ ...value });
            else
              requestAnimationFrame(() =>
                document
                  .querySelector<HTMLInputElement>('.account-settings [aria-invalid="true"]')
                  ?.focus(),
              );
          }}
        >
          {demoMode ? 'Simulasikan simpan auth.json' : 'Simpan ke auth.json'}
        </Button>
      </div>
      {save.error && (
        <Notice tone="error">Pengaturan belum tersimpan. Periksa isian lalu coba lagi.</Notice>
      )}
      <div aria-live="polite">
        {save.isSuccess && (
          <Notice>
            {demoMode
              ? 'Simulasi pengaturan selesai. File auth.json tidak diubah.'
              : 'Pengaturan akun disimpan ke auth.json.'}
          </Notice>
        )}
      </div>
      <p className="connection-note">
        {demoMode
          ? 'Frontend simulasi: sesi tidak disimpan atau dikirim ke server.'
          : available
            ? 'Session ID dikirim hanya saat menyimpan; nilainya tidak ditampilkan kembali.'
            : 'Penyimpanan auth.json tersedia setelah layanan akun terhubung.'}
      </p>
    </section>
  );
}
