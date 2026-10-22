// slide_012.js — build runner for slide 12 (ML lecture 02, MSSE deck).
// The composition lives in the banked component ./components/slide_012.js
// (renderBase + per-block exports; imports the certified parent component
// ./components/slide_011.js — never copy-pasted, never re-derived).
const path = require("path");
const comp = require(path.resolve(__dirname, "components/slide_012.js"));

const out =
  process.argv[2] ||
  path.resolve(__dirname, "../slide_012_recreated.pptx");

comp.build(out).catch((e) => { console.error(e); process.exit(1); });
