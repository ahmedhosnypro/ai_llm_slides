const { buildSourcePanel } = require("./source_panel");
buildSourcePanel(48).catch((e) => { console.error(e); process.exit(1); });
