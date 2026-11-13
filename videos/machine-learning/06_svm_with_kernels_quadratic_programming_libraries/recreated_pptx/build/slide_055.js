const { buildSourcePanel } = require("./source_panel");
buildSourcePanel(55).catch((e) => { console.error(e); process.exit(1); });
