// slide_015.js — 001_introduction slide 15 "[2] Machine Learning vs Deep Learning"
// (section divider) — Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_015.jpg (960x540, 1px = 1pt).
//   Measurement evidence: scratch_015/measure_original2.py, font_solve2_015.py,
//   vs_solve.py (also summarized in qa/slide015/selfcheck outputs).
// Chrome: playlist house chrome (founder directive 2026-10-11) via
//   shared_patterns/house_chrome.js — imported, NEVER re-drawn. Badge numeral 15
//   (file number; 001_introduction originals carry no printed numbers —
//   001_introduction/AGENTS.md, assumption pending founder veto).
//
// Measured constants (frame px):
//   title L1 "[2] Machine Learning"  ink cols 219..761 (w 543), band rows 189..242;
//                                    cap-top 192, baseline 230 ('[' top 189, 'g' to 242)
//   title L2 "vs" (lowercase)        ink cols 471..507 (w 37), band rows 270..289;
//                                    x-height top 270, baseline 290
//   title L3 "Deep Learning"         ink cols 304..674 (w 371), band rows 320..372;
//                                    cap-top 321, baseline 360 ('g' to 372)
//   ink center x of all three lines  ~489.5 (panel center 480 — original text block sits
//                                    ~9.5 px right of panel center; reproduced by centering
//                                    boxes on x 489.5)
//   black strip y 518..539 full width + white pen/cursor icon at ~(595,297) = video
//                                    artifacts (spec: non-content; judge ground rule (c);
//                                    certified slide_040 convention) — deliberately NOT
//                                    recreated.
// Fonts (metric-verified, qa evidence font_solve2_015.py / vs_solve.py):
//   titles Liberation Serif Bold @59 (mask IoU 0.845/0.840 vs sans 0.468/0.517 — SERIF
//   wins on THIS frame, unlike slide_003's sans), ink widths fit err<=3px, cap 38-39px.
//   "vs" lowercase Liberation Serif Bold @43.5-44 (native-scale IoU 0.833 vs 'VS' 0.743).
// Colors: PIL 5x5-core modal of title ink = B3000C (top-5 #B3000C..#B7000B, mean
//   #B3000C, n=4124) — measured value overrides the spec's B22222 estimate (deck
//   AGENTS.md law: pixel profiles settle color claims). Chrome per shared module.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_015_recreated.pptx";

// ---- palette (measured) ----
const TITLE_RED = "B3000C";

// ---- geometry (frame px / 72 = inches) ----
const px = (v) => v / 72;

// Title lines: single-line boxes, valign middle, lineSpacing = box height so the
// LO baseline model (validated on slide_002/slide_040) reduces to
//   baseline = box_top + ascent * fontSize,  ascent(Times/Liberation Serif) = 0.891em.
const ASCENT = 0.891;
const LINES = [
  { text: "[2] Machine Learning", size: 59, baseline: 230, boxH: 66 },
  { text: "vs", size: 43.5, baseline: 290, boxH: 49 },
  { text: "Deep Learning", size: 59, baseline: 360, boxH: 66 },
];
// Boxes centered on measured ink center x=489.5: x = 489.5 - 876/2 = 51.5, w = 876.
const BOX_X = 51.5;
const BOX_W = 876;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 15)
drawHouseChrome(pres, slide, { numeral: "15" });

// Three-line section title — Times New Roman Bold, BA-measured red, centered
LINES.forEach((L) => {
  const topPx = L.baseline - ASCENT * L.size; // box_h == lineSpacing model
  slide.addText(L.text, {
    x: px(BOX_X), y: px(topPx), w: px(BOX_W), h: px(L.boxH),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Times New Roman", fontSize: L.size, bold: true, color: TITLE_RED,
    lineSpacing: L.boxH,
  });
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
