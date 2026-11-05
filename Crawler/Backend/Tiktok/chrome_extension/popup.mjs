import { CONNECTOR_BUILD } from "./core.mjs";
const status = document.querySelector("#status");
document.querySelector("#build").textContent =
  `Connector ${chrome.runtime.getManifest().version} · ${CONNECTOR_BUILD}`;
const refresh = async () => {
  status.textContent =
    (await chrome.storage.session.get("status")).status || "Belum terhubung.";
};
document.querySelector("#start").addEventListener("click", async () => {
  try {
    status.textContent = "Menyambungkan…";
    await chrome.storage.session.set({ status: "Menyambungkan…" });
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    await chrome.runtime.sendMessage({
      action: "start",
      tabId: tab.id,
      origin: document.querySelector("#origin").value.trim(),
      code: document.querySelector("#code").value.trim(),
    });
    document.querySelector("#code").value = "";
    await refresh();
  } catch {
    status.textContent = "Pilih tab TikTok dan periksa alamat penghubung.";
  }
});
for (const action of ["continue", "stop"])
  document
    .querySelector("#" + action)
    .addEventListener("click", () => chrome.runtime.sendMessage({ action }));
chrome.storage.onChanged.addListener(refresh);
refresh();
