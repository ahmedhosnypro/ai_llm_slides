// slide_040.js — "Multi-Head  Attention" section divider (Deep Learning DSAI 308,
// lecture 001 "Transformers — Part I"). Single-version deliverable:
// slide_040_recreated.pptx (SINGLE-VERSION law: no equations, no graphs — plain build).
//
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//        videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_040.js
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_040.jpg (960x540,
// 1px = 1pt = 1/72in) — scratch/slide040/measure_frame.py, measure_fine.py,
// measure_colors.py, measure_calib.py. Text-only divider: red title + two blue
// lines on the house chrome. Mouse-cursor artifact above the title is a
// screen-recording overlay — deliberately NOT recreated (spec exclusion step 8).
//
// Color provenance (JPEG-bias calibrated against KNOWN chrome colors in the frame):
// - title red: core p90 R=191 == known C00000 border stroke R=192 (chroma bleed
//   explains G/B elevation); resolves the spec's CC0000-vs-C00000 uncertainty to C00000.
// - body blue: eroded core (3,0,153), luma ~18-20 -> 0000B0 (matches the certified
//   slide_036 worker's video-chroma-corrected blue measurement for this deck).
// - chrome (panel/border/badge): NOT drawn here — shared house_chrome.js module.
//
// Font sizes from ink: title ink h=36px (ascender 0.73em) / w=483px (10.02em
// advance) -> 48pt Arial Bold; blue lines ink h=26px, cap 25px (0.716em) ->
// 35pt Arial Bold; widths 302px/337px == 8.50em/9.56em at 35pt. All single-line
// boxes (no multi-line text -> no lineSpacing mandate), positioned box-center =
// ink-center, margin:0, fontFace everywhere, no '#' hex.
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_040_recreated.pptx";
const px = (v) => v / 72; // frame px -> inches

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "slide-recreation pipeline";
pres.title = "Multi-Head  Attention";

const slide = pres.addSlide();

// ---- playlist house chrome (white canvas, gray panel, red border, badge "40") ----
drawHouseChrome(pres, slide, { numeral: 40 });

const FONT = "Arial";
const RED = "C00000";
const BLUE = "0000B0";

// ---- title: "Multi-Head  Attention" (double space preserved verbatim) ----
// ink x 224..706, y 201..236 -> center (465, 218.5); 49pt (closed-loop: 48pt
// rendered ink 473x34.1 vs orig 482x35 -> x1.019/1.026 -> 49)
slide.addText("Multi-Head  Attention", {
  x: px(165), y: px(186.5), w: px(600), h: px(60),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 49, bold: true, color: RED,
});

// ---- blue line 1: "Wide Architecture" — ink x 166..467, y 342..367 (center y 354.5) ----
// 35.5pt (closed-loop: 35pt ink w 296 vs orig 301 -> x1.016)
slide.addText("Wide Architecture", {
  x: px(165), y: px(333), w: px(560), h: px(40),
  align: "left", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 35.5, bold: true, color: BLUE,
});

// ---- blue line 2: "Narrow Architecture" — ink x 168..504, y 422..447 (center y 434.5) ----
slide.addText("Narrow Architecture", {
  x: px(165), y: px(413), w: px(560), h: px(40),
  align: "left", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 35.5, bold: true, color: BLUE,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
