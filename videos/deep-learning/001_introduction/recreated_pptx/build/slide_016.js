// slide_016.js — 001_introduction slide 16 "The Complete ML Classification Process"
// (Deep Learning DSAI 308) — DEPENDENT slide, parent = 9 (CERTIFIED).
//
// Thin runner: the composition lives in components/slide_016.js — renderBase imports
// the parent's certified component (components/slide_009.js, absolute path) and draws
// only this slide's measured delta (moved Training ellipse + Pre processing box,
// re-spanned arrow1, redrawn curve1, "Classifier Output" box replacing "Post
// processing", four hand-annotation callouts replacing the gray output labels; parent
// curve2/final_ellipse removed). This runner adds the slide and writes the deliverable.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_016.jpg (960x540, 1px = 1pt)
// — provenance in components/slide_016.js header + qa/slide016/measure_*.py.
// Badge numeral = "16" (file number; assumption PENDING FOUNDER VETO,
// 001_introduction/AGENTS.md 2026-10-12).

const pptxgen = require("pptxgenjs");
const { renderBase } = require("./components/slide_016.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_016_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

renderBase(pres, slide, { numeral: "16" });

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
