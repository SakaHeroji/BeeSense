import { Suspense, useEffect, useRef, useState } from 'react';
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import {
  ArrowUpRight,
  FlaskConical,
  FolderKanban,
  Layers3,
  LifeBuoy,
  Menu,
  ShieldCheck,
  X,
} from 'lucide-react';
import { api } from '../shared/api';
import { useMediaQuery } from '../shared/hooks';
import { demoMode, platformName, platforms } from '../shared/domain';
import { Button, Dialog, Notice, PlatformMark, Spinner } from '../shared/ui';
import { AppContext } from '../shared/context';

export default function Shell() {
  const location = useLocation();
  const client = useQueryClient();
  const [mobile, setMobile] = useState(false);
  const [help, setHelp] = useState(false);
  const [toast, setToast] = useState('');
  const narrow = useMediaQuery('(max-width: 760px)');
  const sidebar = useRef<HTMLElement>(null);
  const menuTrigger = useRef<HTMLButtonElement>(null);
  const session = useQuery({ queryKey: ['session'], queryFn: api.session, retry: false });
  const capabilities = useQuery({
    queryKey: ['capabilities'],
    queryFn: api.capabilities,
    retry: false,
  });
  useEffect(() => {
    document.getElementById('main-title')?.focus();
  }, [location.pathname]);
  useEffect(() => {
    if (!mobile) return;
    const elements = () =>
      Array.from(sidebar.current?.querySelectorAll<HTMLElement>('a, button, select') || []);
    elements()[0]?.focus();
    const handler = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setMobile(false);
        requestAnimationFrame(() => menuTrigger.current?.focus());
      }
      if (event.key === 'Tab') {
        const items = elements(),
          first = items[0],
          last = items.at(-1);
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last?.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first?.focus();
        }
      }
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [mobile]);
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => setToast(''), 7000);
    return () => clearTimeout(timer);
  }, [toast]);
  return (
    <div className="workspace">
      <a className="skip-link" href="#main">
        Lewati navigasi
      </a>
      {mobile && (
        <button
          className="nav-scrim"
          aria-label="Tutup navigasi"
          onClick={() => setMobile(false)}
        />
      )}
      <aside
        id="crawler-nav"
        inert={narrow && !mobile}
        ref={sidebar}
        className={`sidebar ${mobile ? 'is-open' : ''}`}
        aria-label="Navigasi workspace"
      >
        <Link to="/crawler/conversations" className="brand" onClick={() => setMobile(false)}>
          <img src="/beesense.svg" alt="" width="39" height="39" />
          <span>
            BeeSense<span className="brand-sub">Research workspace</span>
          </span>
        </Link>
        <p className="nav-caption">Persiapan</p>
        <nav aria-label="Menu Crawler">
          <NavLink to="/crawler/conversations" onClick={() => setMobile(false)}>
            <span className="nav-feature-icon" aria-hidden="true">
              <FolderKanban size={18} />
            </span>
            <span>Conversation</span>
          </NavLink>
        </nav>
        <p className="nav-caption nav-caption-secondary">Crawling</p>
        <nav aria-label="Mode dan platform crawling">
          <NavLink to="/crawler/parallel" onClick={() => setMobile(false)}>
            <span className="nav-feature-icon" aria-hidden="true">
              <Layers3 size={18} />
            </span>
            <span>Parallel</span>
          </NavLink>
          {platforms.map((platform) => (
            <NavLink
              key={platform}
              to={`/crawler/${platform}`}
              onClick={() => {
                setMobile(false);
              }}
            >
              <PlatformMark platform={platform} />
              <span>{platformName(platform)}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <button className="help-button" onClick={() => setHelp(true)}>
            <LifeBuoy size={18} /> Panduan workspace <ArrowUpRight size={14} />
          </button>
          <span className="sidebar-version">
            BeeSense Crawler <span>v1.3</span>
          </span>
        </div>
      </aside>
      <div className="workspace-body" inert={narrow && mobile}>
        <header className="topbar">
          <div className="breadcrumb">
            <button
              ref={menuTrigger}
              className="icon-button mobile-menu"
              onClick={() => setMobile(true)}
              aria-label="Buka navigasi"
              aria-expanded={mobile}
            >
              <Menu size={20} />
            </button>
            <span>Workspace</span>
            <span className="slash">/</span>
            <b>{location.pathname.includes('/conversations') ? 'Conversation' : 'Crawling'}</b>
          </div>
          <div className="header-right">
            <span className="project-label">
              <span className="project-dot" />
              Riset pendidikan
            </span>
            {demoMode && <span className="demo-pill">Simulasi</span>}
            <span className="avatar" aria-hidden="true">
              {session.data?.role === 'observer' ? 'PA' : 'OR'}
            </span>
            {demoMode ? (
              <select
                className="role-select"
                aria-label="Peran simulasi"
                value={session.data?.role || 'operator'}
                onChange={(e) => {
                  sessionStorage.setItem('beesense:demo-role', e.target.value);
                  client.clear();
                  setToast('Peran simulasi diubah. Data formulir dikosongkan.');
                }}
              >
                <option value="operator">Operator demo</option>
                <option value="observer">Pengamat demo</option>
              </select>
            ) : (
              <span>{session.data?.name || 'Menghubungkan'}</span>
            )}
          </div>
        </header>
        <main id="main" className="main-content">
          {demoMode && (
            <div className="demo-banner">
              <FlaskConical size={16} />
              <span>
                <b>Ruang simulasi.</b> Seluruh angka dan hasil adalah data contoh. Tidak ada
                crawling atau training yang dijalankan.
              </span>
            </div>
          )}
          {session.isPending || capabilities.isPending ? (
            <div className="loading-page">
              <Spinner />
              <p>Menyiapkan workspace…</p>
            </div>
          ) : session.error || capabilities.error ? (
            <div className="connection-state">
              <h1 id="main-title" tabIndex={-1}>
                Hubungkan backend Crawler
              </h1>
              <Notice tone="error">{(session.error || capabilities.error)?.message}</Notice>
              <p>
                Mode API memerlukan layanan backend sesuai kontrak frontend. Untuk mencoba antarmuka
                dengan data sintetis, jalankan mode demo yang dijelaskan di README.
              </p>
              <Button
                onClick={() => {
                  void session.refetch();
                  void capabilities.refetch();
                }}
              >
                Coba hubungkan kembali
              </Button>
            </div>
          ) : (
            <AppContext.Provider
              value={{ cap: capabilities.data!, session: session.data!, notify: setToast }}
            >
              <Suspense
                fallback={
                  <div className="loading-page" role="status">
                    <Spinner />
                    Memuat halaman…
                  </div>
                }
              >
                <Outlet key={session.data!.role} />
              </Suspense>
            </AppContext.Provider>
          )}
        </main>
        <footer className="workspace-footer">
          <span>
            BeeSense <span className="footer-dot" /> Akuisisi untuk memahami pilihan pendidikan
          </span>
          <span>Waktu ditampilkan dalam WIB</span>
        </footer>
      </div>
      {toast && (
        <div className="toast" role="status">
          <ShieldCheck size={19} />
          <span>{toast}</span>
          <button aria-label="Tutup pemberitahuan" onClick={() => setToast('')}>
            <X size={16} />
          </button>
        </div>
      )}
      <Dialog open={help} onClose={() => setHelp(false)} title="Panduan workspace">
        <p>
          Susun judul, keyword, discovery, dan relevansi di menu Conversation. Saat akan crawling,
          pilih conversation yang sudah siap lalu tentukan satu platform atau mode parallel. Gunakan
          Hasil per tanggal untuk statistik, data lengkap, dan migrasi transaksi ke PostgreSQL.
        </p>
        <div className="help-list">
          <p>
            <b>Conversation adalah sumber konteks</b>
            <br />
            Perubahan conversation tidak mengubah pekerjaan yang sudah dimulai; setiap pekerjaan
            menyimpan snapshot versinya.
          </p>
          <p>
            <b>Post memenuhi kriteria</b>
            <br />
            Post unik yang memenuhi jumlah minimum komentar, berbeda dari total post terkumpul.
          </p>
          <p>
            <b>Hasil parsial tetap bernilai</b>
            <br />
            Periksa alasan dan kualitas sebelum menyiapkannya untuk NLP.
          </p>
          <p>
            <b>CAPTCHA pada sesi worker</b>
            <br />
            Pada mode API, verifikasi harus dilakukan pada sesi browser worker yang ditautkan, bukan
            tab Reddit biasa.
          </p>
          {demoMode && (
            <p>
              <b>Simulasi aman</b>
              <br />
              Gunakan data sintetis. Pengaturan akun dan migrasi hanya disimulasikan, tanpa menulis
              file atau database. Hanya metadata pekerjaan simulasi disimpan di browser.
            </p>
          )}
        </div>
        <Button onClick={() => setHelp(false)}>Mengerti</Button>
      </Dialog>
    </div>
  );
}
