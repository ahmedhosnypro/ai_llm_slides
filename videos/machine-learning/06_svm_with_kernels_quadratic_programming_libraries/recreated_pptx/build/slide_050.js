const { buildSourcePanel } = require("./source_panel");
buildSourcePanel(50).catch((e) => { console.error(e); process.exit(1); });
