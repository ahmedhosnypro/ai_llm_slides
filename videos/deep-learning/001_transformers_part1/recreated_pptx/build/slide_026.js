// slide_026.js — "Self Attention Mechanism (Fundamental Operation)" (Deep Learning
// DSAI 308, Transformers — Part I). Build worker attempt 1, 2026-10-11.
//
// CHROME: playlist house chrome ONLY via components/house_chrome.js (which delegates to
// videos/deep-learning/shared_patterns/house_chrome.js) — drawHouseChrome(pptx, slide,
// {numeral: 26}). The ml-intro values in 17_worker_instructions.md are superseded.
// CONTENT: every block is drawn by the shared component components/slide_026.js
// (renderBase) so dependent slides 27/28/29 can import it. Geometry provenance: PIL
// forensics on unique_slides/slide_026.jpg + 8-panel vision read — see the component
// header. pptxgenjs laws: no "#" hex, fontFace everywhere, margin:0, explicit
// lineSpacing on multi-line boxes.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js"
);
const base = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_026.js"
);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

drawHouseChrome(pres, s, { numeral: 26 });
base.renderBase(pres, s, {});

pres.writeFile({ fileName: "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_026_recreated.pptx" })
  .then(() => console.log("wrote slide_026_recreated.pptx"));
