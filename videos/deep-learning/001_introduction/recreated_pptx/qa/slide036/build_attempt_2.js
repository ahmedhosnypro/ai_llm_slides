// slide_036.js — 001_introduction slide 36 "How many Parameters are  in the  RGB
// Image filter  ( K=3 )" (Deep Learning DSAI 308) — ROOT slide with dependent 37.
//
// Thin runner: the composition lives in components/slide_036.js (renderBase, per-block
// functions, GEOM parameters — slide 37 imports it and resolves its crowding via
// opts.skip/opts.geom). This runner adds the slide and writes the deliverable.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_036.jpg (960x540, 1px = 1pt)
// — provenance in components/slide_036.js header + qa/slide036/measure_*.py (banked
// passes from the interrupted first worker + this worker's measure5/fit_fonts).
// Badge numeral = "36" (file number; assumption PENDING FOUNDER VETO,
// 001_introduction/AGENTS.md 2026-10-12).

const pptxgen = require("pptxgenjs");
const { renderBase } = require("./components/slide_036.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_036_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

renderBase(pres, slide, { numeral: "36" });

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
