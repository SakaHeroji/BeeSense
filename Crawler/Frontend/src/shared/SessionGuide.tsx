import { BookOpen, ChevronDown, ExternalLink } from 'lucide-react';
import { sessionCookies, sessionPlatforms } from './auth';
import { platformName } from './domain';
import type { Platform } from './types';

export function SessionGuide({ platform }: { platform: Platform }) {
  if (!sessionPlatforms.includes(platform)) return null;
  const cookie = sessionCookies[platform];
  const name = platformName(platform);
  const chrome = platform === 'tiktok';
  const title = cookie
    ? `Cara mengambil Session ID ${name}`
    : chrome
      ? 'Cara menggunakan sesi Chrome TikTok'
      : `Informasi sesi ${name}`;
  return (
    <details className="session-guide">
      <summary>
        <BookOpen size={18} aria-hidden="true" />
        <span>
          <strong>{title}</strong>
          <small>
            {cookie
              ? `Salin nilai cookie ${cookie.name} dari Chrome.`
              : chrome
                ? 'Gunakan tab yang sudah login, tanpa menyalin cookie.'
                : 'Metode autentikasi menunggu integrasi backend.'}
          </small>
        </span>
        <ChevronDown className="session-guide-chevron" size={18} aria-hidden="true" />
      </summary>
      <div className="session-guide-content">
        {cookie ? (
          <>
            <dl className="session-guide-source">
              <div>
                <dt>Domain di Chrome</dt>
                <dd>
                  <code translate="no">{cookie.origin}</code>
                </dd>
              </div>
              <div>
                <dt>Nama cookie</dt>
                <dd>
                  <code translate="no">{cookie.name}</code>
                </dd>
              </div>
            </dl>
            <ol className="session-guide-steps">
              <li>
                <p>
                  Buka{' '}
                  <a href={cookie.origin} target="_blank" rel="noopener noreferrer">
                    {name} <ExternalLink size={13} aria-hidden="true" />
                    <span className="sr-only"> (tab baru)</span>
                  </a>{' '}
                  di Chrome, lalu masuk ke akun Anda seperti biasa.
                </p>
              </li>
              <li>
                <p>
                  Buka DevTools dengan <kbd>⌘</kbd> + <kbd>⌥</kbd> + <kbd>I</kbd> di macOS, atau{' '}
                  <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>I</kbd> di Windows/Linux.
                </p>
              </li>
              <li>
                <p>
                  Pilih <b>Application → Storage → Cookies</b>, lalu pilih domain{' '}
                  <code translate="no">{cookie.origin}</code>. Jika Application belum terlihat, buka
                  menu tab tambahan <b>»</b> di DevTools.
                </p>
              </li>
              <li>
                <p>
                  Cari baris dengan <b>Name</b> <code translate="no">{cookie.name}</code>. Pilih
                  barisnya dan salin isi kolom <b>Value</b> saja, tanpa nama cookie, tanda kutip
                  atau cookie lain. Pertahankan nilai utuh seperti yang tampil.
                </p>
              </li>
              <li>
                <p>
                  Tempel Value ke kolom <b>Session ID</b> di bawah panduan ini. Isi <b>Username</b>{' '}
                  dengan nama akun yang sama, bukan URL profil.
                </p>
              </li>
            </ol>
            <p className="session-guide-tip">
              Cookie belum terlihat? Pastikan akun sudah login dan domain yang dipilih benar.
              Tulisan “Session” pada kolom Expires bukan nilai yang perlu disalin.
            </p>
            <p className="session-guide-footnote">
              Nilai sesi memberi akses akun. Gunakan akun Anda sendiri dan simpan nilainya secara
              privat.{' '}
              <a
                href="https://developer.chrome.com/docs/devtools/application/cookies/"
                target="_blank"
                rel="noopener noreferrer"
              >
                Panduan cookie Chrome <ExternalLink size={13} aria-hidden="true" />
                <span className="sr-only"> (tab baru)</span>
              </a>
            </p>
          </>
        ) : chrome ? (
          <>
            <p>
              TikTok memakai sesi pada tab Chrome pilihan Anda. Session ID tidak perlu ditempel ke
              frontend.
            </p>
            <ol className="session-guide-steps">
              <li>
                <p>
                  Buka{' '}
                  <a href="https://www.tiktok.com/" target="_blank" rel="noopener noreferrer">
                    TikTok <ExternalLink size={13} aria-hidden="true" />
                    <span className="sr-only"> (tab baru)</span>
                  </a>{' '}
                  di Chrome, lalu masuk ke akun Anda.
                </p>
              </li>
              <li>
                <p>
                  Aktifkan BeeSense TikTok Connector. Tinjau konfigurasi crawling agar alamat dan
                  kode pairing tersedia.
                </p>
              </li>
              <li>
                <p>
                  Klik ikon BeeSense untuk membuka sidebar. Pilih tab TikTok, isi alamat dan kode
                  pairing, lalu tekan <b>Hubungkan & mulai</b>.
                </p>
              </li>
              <li>
                <p>
                  Biarkan tab terbuka. Jika diminta CAPTCHA atau login ulang, selesaikan langsung di
                  tab TikTok lalu lanjutkan dari sidebar.
                </p>
              </li>
            </ol>
            <p className="session-guide-tip">
              Kode pairing berasal dari crawler BeeSense dan dipakai untuk menghubungkan plugin.
              Kode ini berbeda dari sesi login TikTok.
            </p>
          </>
        ) : (
          <>
            <p>
              Backend crawler {name} belum tersedia. Form akun saat ini disiapkan untuk integrasi
              berikutnya.
            </p>
            <p>
              Nama cookie dan format kredensial untuk {name} belum ditetapkan. Belum ada Session ID
              yang dapat diverifikasi atau dipakai untuk crawling {name} dari frontend ini.
            </p>
            <p className="session-guide-tip">
              Anda dapat membiarkan isian sesi kosong. Panduan pengambilan sesi akan mengikuti
              metode autentikasi backend saat tersedia.
            </p>
          </>
        )}
      </div>
    </details>
  );
}
