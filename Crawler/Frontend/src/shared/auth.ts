import type { AuthInput, FieldError, Platform } from './types';

export const sessionPlatforms: Platform[] = ['instagram', 'x', 'tiktok', 'threads', 'facebook'];
export function validateAuth(platform: Platform, value: AuthInput): FieldError[] {
  const errors: FieldError[] = [];
  const username = value.username.replace(/^@/, '');
  if (!sessionPlatforms.includes(platform))
    return [{ field: 'username', message: 'Sumber ini tidak memakai username/session ID.' }];
  if (!username && !value.sessionid)
    return [{ field: 'username', message: 'Isi username atau session ID yang ingin diperbarui.' }];
  if (
    username &&
    !(platform === 'x' ? /^[A-Za-z0-9_]{1,15}$/ : /^[A-Za-z0-9_.-]{1,100}$/).test(username)
  )
    errors.push({ field: 'username', message: 'Gunakan nama akun tanpa spasi atau URL profil.' });
  if (value.sessionid && (value.sessionid.length > 4096 || /[^\x21-\x7E]/.test(value.sessionid)))
    errors.push({
      field: 'sessionid',
      message: 'Session ID maksimal 4.096 karakter tanpa spasi atau baris baru.',
    });
  return errors;
}
