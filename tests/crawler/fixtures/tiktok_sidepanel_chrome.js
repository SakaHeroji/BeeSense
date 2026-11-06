// Offline Chrome API fixture. Never connects to TikTok or the local crawler.
(() => {
  const changed = [];
  let saved = JSON.parse(sessionStorage.getItem("fixtureState") || "{}");
  let tabs = [
    {
      id: 6,
      active: false,
      title: "TikTok lain",
      url: "https://www.tiktok.com/",
    },
    {
      id: 7,
      active: true,
      title: "TikTok · Pendidikan",
      url: "https://www.tiktok.com/@example/video/100",
    },
  ];
  const update = (value) => {
    saved = value;
    sessionStorage.setItem("fixtureState", JSON.stringify(value));
    for (const listener of changed)
      listener({ connectorState: { newValue: value } }, "session");
  };
  const fixture = (window.uiFixture = {
    messages: [],
    update,
    setTabs: (value) => {
      tabs = value;
    },
  });
  window.chrome = {
    runtime: {
      getManifest: () => ({ version: "1.4.0" }),
      sendMessage: async (message) => {
        if (fixture.fail) throw new Error("Offline fixture failure");
        fixture.messages.push(message);
        if (message.action === "start")
          update({
            phase: "running",
            running: true,
            counts: { posts: 0, comments: 0, replies: 0 },
            tabTitle: "TikTok · Pendidikan",
            message: "Terhubung ke crawler lokal.",
            updatedAt: Date.now(),
          });
        if (message.action === "stop")
          update({
            ...saved,
            phase: "stopped",
            running: false,
            message: "Pengambilan dihentikan.",
          });
        if (message.action === "continue")
          update({
            ...saved,
            phase: "running",
            message: "Pengambilan dilanjutkan.",
          });
        return { started: true, continued: true, stopping: true };
      },
    },
    storage: {
      session: { get: async () => ({ connectorState: saved }) },
      onChanged: { addListener: (f) => changed.push(f) },
    },
    tabs: {
      query: async () => tabs,
      get: async (id) => tabs.find((tab) => tab.id === id),
      create: async ({ url }) => {
        tabs = [{ id: 8, active: true, title: "TikTok", url }];
      },
      onActivated: { addListener: () => {} },
      onUpdated: { addListener: () => {} },
      onRemoved: { addListener: () => {} },
    },
    sidePanel: { getLayout: async () => ({ side: "right" }) },
  };
})();
