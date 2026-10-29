import { useEffect, useRef, useState } from 'react';
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import {
  ArrowUpRight,
  BookOpen,
  ChevronDown,
  Database,
  FlaskConical,
  Layers3,
  LifeBuoy,
  Menu,
  Radio,
  ShieldCheck,
  X,
} from 'lucide-react';
import { api } from '../shared/api';
import { useMediaQuery } from '../shared/hooks';
import { demoMode, safeExternal } from '../shared/domain';
import { Button, Dialog, Notice, Spinner } from '../shared/ui';
import { AppContext } from '../shared/context';

export default function Shell() {
  const location = useLocation();
  const client = useQueryClient();
  const [mobile, setMobile] = useState(false);
  const [modules, setModules] = useState(false);
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
  const manual = location.pathname.includes('/manual');
  const externalModules = [
    { name: 'NLP Machine Learning', icon: FlaskConical, url: import.meta.env.VITE_NLP_URL },
    { name: 'Dashboard', icon: Layers3, url: import.meta.env.VITE_DASHBOARD_URL },
  ];
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
        <Link to="/crawler/automatic" className="brand" onClick={() => setMobile(false)}>
          <img src="/beesense.svg" alt="" width="39" height="39" />
          <span>
            BeeSense<span className="brand-sub">Research workspace</span>
          </span>
        </Link>
        <div className="module-switch">
          <button onClick={() => setModules(!modules)} aria-expanded={modules}>
            <span>
              <Database size={17} /> Crawler
            </span>
            <ChevronDown size={15} />
          </button>
          {modules && (
            <div className="module-menu">
              <strong>Frontend BeeSense</strong>
              {externalModules.map((m) => {
                const href = m.url ? safeExternal(m.url) : undefined;
                return href ? (
                  <a key={m.name} href={href} target="_blank" rel="noreferrer">
                    <m.icon size={17} />
                    {m.name}
                    <ArrowUpRight size={14} />
                  </a>
                ) : (
                  <span key={m.name}>
                    <m.icon size={17} />
                    <span>
                      {m.name}
                      <small>Belum tersedia</small>
                    </span>
                  </span>
                );
              })}
            </div>
          )}
        </div>
        <p className="nav-caption">Akuisisi data</p>
        <nav aria-label="Menu Crawler">
          <NavLink
            to="/crawler/automatic"
            className={!manual ? 'active' : ''}
            onClick={() => {
              setMobile(false);
              setModules(false);
            }}
          >
            <Radio size={19} />
            <span>Crawler Otomatis</span>
          </NavLink>
          <NavLink
            to="/crawler/manual?tab=url"
            className={manual ? 'active' : ''}
            onClick={() => {
              setMobile(false);
              setModules(false);
            }}
          >
            <BookOpen size={19} />
            <span>Crawler Manual</span>
          </NavLink>
        </nav>
        <div className="sidebar-bottom">
          <div className="research-note">
            <span className="leaf-icon">
              <ShieldCheck size={19} />
            </span>
            <strong>Data yang dapat ditelusuri</strong>
            <p>Setiap akuisisi membawa sumber, versi, dan jejak kualitasnya.</p>
          </div>
          <button className="help-button" onClick={() => setHelp(true)}>
            <LifeBuoy size={18} /> Panduan workspace <ArrowUpRight size={14} />
          </button>
          <span className="sidebar-version">
            BeeSense Crawler <span>v1.0</span>
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
            <b>Crawler</b>
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
              <Outlet key={session.data!.role} />
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
          Gunakan Crawler Otomatis untuk menemukan post melalui query. Gunakan Crawler Manual untuk
          URL pilihan atau respons survei yang telah dikumpulkan.
        </p>
        <div className="help-list">
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
              Gunakan data sintetis. Jawaban survei demo berada di memori dan hilang saat refresh.
              Hanya metadata pekerjaan simulasi disimpan di browser.
            </p>
          )}
        </div>
        <Button onClick={() => setHelp(false)}>Mengerti</Button>
      </Dialog>
    </div>
  );
}
