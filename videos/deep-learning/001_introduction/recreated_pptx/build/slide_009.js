// slide_009.js — 001_introduction slide 9 "The Complete ML Classification Process".
//
// Thin runner: the composition lives in components/slide_009.js (renderBase, per-block
// functions) so children 16/18/19 can import it (dependency law). This runner adds the
// slide and writes the deliverable pptx.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_009.jpg (960x540, 1px = 1pt).
// Chrome: playlist house chrome via components/house_chrome.js (delegates to
//   shared_patterns/house_chrome.js) — imported, NEVER re-drawn. Badge numeral = "9"
//   (file number; assumption PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).

const pptxgen = require("pptxgenjs");
const { renderBase } = require("./components/slide_009.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_009_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

renderBase(pres, slide, { numeral: "9" });

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
