import { CONNECTOR_BUILD, tiktokUrl } from "./core.mjs";

const $ = (id) => document.getElementById(id);
const numbers = new Intl.NumberFormat("id-ID");
const clock = new Intl.DateTimeFormat("id-ID", {
  hour: "2-digit",
  minute: "2-digit",
});
let state = {},
  pending = false;

$("version").textContent = `v${chrome.runtime.getManifest().version}`;
$("build").textContent =
  `Connector ${chrome.runtime.getManifest().version} · ${CONNECTOR_BUILD}`;

function fieldError(id, message = "") {
  $(id).setAttribute("aria-invalid", String(Boolean(message)));
  $(`${id}-error`).textContent = message;
  $(`${id}-error`).hidden = !message;
}

function render() {
  const running = state.running === true;
  const connecting = state.phase === "connecting";
  const human = state.phase === "human" && running;
  const stopping = state.phase === "stopping" && running;
  $("connection").dataset.state = human
    ? "human"
    : connecting
      ? "connecting"
      : running
        ? "running"
        : state.phase || "idle";
  $("connection-label").textContent = human
    ? "Perlu validasi Anda"
    : connecting
      ? "Menyambungkan…"
      : running
        ? "Terhubung ke crawler"
        : state.phase === "error"
          ? "Periksa koneksi"
          : state.phase === "stopped"
            ? "Pengambilan berhenti"
            : "Belum terhubung";
  $("setup").hidden = running;
  $("monitor").hidden = !running;
  $("monitor-title").textContent = human
    ? "Selesaikan validasi"
    : connecting
      ? "Menyambungkan…"
      : stopping
        ? "Menghentikan…"
        : "Pengambilan berjalan";
  $("monitor-hint").textContent = human
    ? "Selesaikan CAPTCHA di tab TikTok, lalu lanjutkan dari sidebar ini."
    : "Tab terpilih dikendalikan crawler. Sidebar dapat tetap terbuka.";
  $("selected-tab").textContent = state.tabTitle || "TikTok";
  $("run-controls").hidden = !running;
  $("continue").hidden = !human;
  $("stop").disabled = stopping;
  $("progress").hidden = !state.counts;
  for (const key of ["posts", "comments", "replies"])
    $(key).textContent = numbers.format(state.counts?.[key] || 0);
  if (state.message && $("status").textContent !== state.message)
    $("status").textContent = state.message;
  $("activity-context").hidden = !state.target;
  $("activity-context").textContent = state.target
    ? `Sedang diproses: ${state.target}`
    : "";
  $("updated").textContent = state.updatedAt
    ? clock.format(new Date(state.updatedAt))
    : "";
  if (state.updatedAt)
    $("updated").dateTime = new Date(state.updatedAt).toISOString();
  $("start").disabled = pending || connecting;
  $("start-label").textContent =
    pending || connecting ? "Menyambungkan…" : "Hubungkan & mulai";
  $("pairing").setAttribute("aria-busy", String(pending || connecting));
}

async function refresh() {
  const saved = await chrome.storage.session.get(["connectorState", "status"]);
  state = saved.connectorState || {};
  if (!state.message && saved.status) state.message = saved.status;
  render();
}

async function tabs() {
  const selected = $("tab").value;
  const all = await chrome.tabs.query({
    currentWindow: true,
    url: "https://www.tiktok.com/*",
  });
  $("tab").replaceChildren();
  for (const tab of all) {
    const option = document.createElement("option");
    option.value = String(tab.id);
    option.textContent = tab.title || "TikTok";
    option.selected = selected
      ? selected === option.value
      : Boolean(tab.active);
    $("tab").append(option);
  }
  if (!all.length) {
    const empty = document.createElement("option");
    empty.value = "";
    empty.textContent = "Belum ada tab TikTok";
    $("tab").append(empty);
  }
  $("open-tiktok").hidden = all.length > 0;
}

$("pairing").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (pending || state.running || state.phase === "connecting") return;
  for (const id of ["tab", "origin", "code"]) fieldError(id);
  let firstError;
  const reject = (id, message) => {
    fieldError(id, message);
    firstError ||= id;
  };
  const tabId = Number($("tab").value);
  if (!$("tab").value)
    reject("tab", "Buka tab TikTok yang sudah login, lalu tekan Perbarui.");
  let origin;
  try {
    origin = new URL($("origin").value.trim());
    if (
      origin.protocol !== "http:" ||
      origin.hostname !== "127.0.0.1" ||
      origin.pathname !== "/" ||
      origin.search ||
      origin.hash ||
      origin.username ||
      origin.password
    )
      throw new Error();
  } catch {
    reject(
      "origin",
      "Gunakan alamat http://127.0.0.1:PORT/ dari crawler aktif.",
    );
  }
  const code = $("code").value.trim();
  if (!/^[a-zA-Z0-9_-]{32,128}$/.test(code))
    reject(
      "code",
      "Salin kode pasangan lengkap dari crawler yang sedang aktif.",
    );
  if (firstError) {
    $(firstError).focus();
    return;
  }
  pending = true;
  render();
  try {
    const tab = await chrome.tabs.get(tabId);
    tiktokUrl(tab.url);
    const reply = await chrome.runtime.sendMessage({
      action: "start",
      tabId,
      origin: origin.origin + "/",
      code,
    });
    if (!reply?.started) throw new Error();
    $("code").value = "";
    $("code").type = "password";
    $("show-code").textContent = "Tampilkan";
    $("show-code").setAttribute("aria-pressed", "false");
    await refresh();
  } catch {
    state = {
      ...state,
      message:
        "Tidak dapat menghubungkan tab. Periksa crawler lokal, lalu pilih ulang tab TikTok.",
    };
  } finally {
    pending = false;
    render();
  }
});

$("show-code").addEventListener("click", () => {
  const show = $("code").type === "password";
  $("code").type = show ? "text" : "password";
  $("show-code").textContent = show ? "Sembunyikan" : "Tampilkan";
  $("show-code").setAttribute("aria-pressed", String(show));
});
$("refresh-tabs").addEventListener("click", () => tabs().catch(showTabError));
function showTabError() {
  fieldError(
    "tab",
    "Daftar tab belum terbaca. Tekan Perbarui untuk mencoba lagi.",
  );
}
$("open-tiktok").addEventListener("click", async () => {
  try {
    await chrome.tabs.create({ url: "https://www.tiktok.com/" });
    await tabs();
  } catch {
    showTabError();
  }
});
for (const action of ["continue", "stop"])
  $(action).addEventListener("click", async () => {
    $(action).disabled = true;
    try {
      await chrome.runtime.sendMessage({ action });
      await refresh();
    } catch {
      state = {
        ...state,
        message: "Perintah belum diterima. Coba lagi dari sidebar ini.",
      };
    } finally {
      $(action).disabled = false;
      render();
    }
  });
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === "session" && (changes.connectorState || changes.status))
    refresh().catch(() => {});
});
chrome.tabs.onActivated.addListener(() => {
  if (!state.running) tabs().catch(showTabError);
});
chrome.tabs.onUpdated.addListener(() => {
  if (!state.running) tabs().catch(showTabError);
});
chrome.tabs.onRemoved.addListener(() => {
  if (!state.running) tabs().catch(showTabError);
});
refresh().catch(() => {
  $("status").textContent =
    "Status belum terbaca. Tutup dan buka kembali sidebar BeeSense.";
});
tabs().catch(showTabError);
if (chrome.sidePanel?.getLayout)
  chrome.sidePanel
    .getLayout()
    .then(({ side }) => {
      $("layout-hint").hidden = side !== "left";
    })
    .catch(() => {});
