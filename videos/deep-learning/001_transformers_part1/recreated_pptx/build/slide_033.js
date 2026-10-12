// slide_033.js — "Self Attention Mechanism (Linear Transformation of Inputs)"
// Deep Learning DSAI 308, Transformers — Part I. Build worker attempts 1-3, 2026-10-11/12.
//
// JUDGE-CERTIFIED (attempt 3, PASS — qa/slide033/judge_attempt_3.txt). The full
// composition is exported as the certified component components/slide_033.js
// (renderBase) per the playlist-scoped banking obligation (lecture 002 depends on
// this slide); this build script is the thin wrapper that renders the deliverable.
// Provenance of the certified build (pre-refactor, byte-for-byte): qa/slide033/
// build_attempt_3.js; the refactor was verified 0-pixel-diff against render_3.png.
//
// Frame-true build: all geometry PIL-measured from unique_slides/slide_033.jpg
// (960x540, 1px = 1pt) — scratch/slide033/ passes w1..w6 + the prior worker's
// f/p passes — plus gated crop reads banked in scratch/slide033/crops2/ (q1..q4)
// and crops/ vread_A..K. FRAME-VS-SPEC corrections are documented in
// qa/slide033/worker_report.md.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { renderBase } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_033.js"
);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pres.addSlide();

renderBase(pres, slide, { numeral: 33 });

// ---- output (SINGLE-VERSION law: one plain-named deliverable) ----------------
const OUT = path.join(__dirname, "..", "slide_033_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
