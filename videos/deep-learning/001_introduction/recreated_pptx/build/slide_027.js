// slide_027.js — 001_introduction slide 27 "[4] Introduction to Deep Learning and CNN"
// (section [4] divider) — Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_027.jpg (960x540, 1px = 1pt).
//   Measurement evidence: scratch_027/measure_027.py, measure2_027.py, measure3_027.py.
// Chrome: playlist house chrome (founder directive 2026-10-11) via
//   shared_patterns/house_chrome.js — imported, NEVER re-drawn. Badge numeral 27
//   (file number; 001_introduction originals carry no printed numbers —
//   001_introduction/AGENTS.md, assumption pending founder veto).
//
// Measured constants (frame px):
//   L1 "[4] Introduction to"  ink cols 264..682 (w 419), band rows 133..179;
//                             cap 'I' 135..169 (cap h 35), baseline 169.5 ('[' 133..179)
//   L2 "Deep Learning"        ink cols 240..719 (w 480), band rows 229..295;
//                             cap 'D' 231..280 (cap h 50), baseline 280 ('g' desc to 295)
//   L3 "and"                  ink cols 439..518 (w 80), band rows 312..347;
//                             ascender 'd' 312..347, baseline 346.5 (x-h top 321)
//   L4 "CNN"                  ink cols 406..551 (w 146), band rows 372..423;
//                             cap 'N' 373..422 (cap h 50), baseline 422.5 ('C' overshoot 423)
//   Ink centers: L1 473, L2 479.5, L3 478.5, L4 478.5 (panel center 480 — L1 sits ~7px
//   left, reproduced by centering each line's box on ITS measured ink center).
//   Black strip rows 519..539 full width + mouse cursor (rows 443..457, cols 276..288)
//   = video artifacts (spec recreation_brief step 8/9: OMIT; judge ground rule (c)) —
//   deliberately NOT recreated.
// Fonts (metric-verified, scratch_027/measure2_027.py + measure3_027.py):
//   ALL FOUR lines Liberation Sans Bold (sans) — width-fit + IoU win over serif:
//   L1 @50 (w err 4, IoU 0.829 vs serif 0.312), L2 @70 (err 3, IoU 0.903 vs 0.555),
//   L3 @48 (err 0, IoU 0.864), L4 @71 (err 1, IoU 0.877 vs 0.603).
//   Build uses fontFace "Arial" — LO substitutes metric-compatible Liberation Sans
//   (certified slide_015 precedent: "Times New Roman" -> Liberation Serif).
// Colors: PIL 5x5-core modal of title ink = #B4000B (top-5 #B3000C..#B6000B, mean
//   #B0000B, n=10628) — measured value overrides the spec's #C11B22 estimate (deck
//   AGENTS.md law: pixel column-profiles settle color claims). Chrome per shared module.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_027_recreated.pptx";

// ---- palette (measured) ----
const TITLE_RED = "B4000B";

// ---- geometry (frame px / 72 = inches) ----
const px = (v) => v / 72;

// Title lines: single-line boxes, valign middle, lineSpacing = box height so the
// LO baseline model (validated on slide_002/slide_040/slide_015) reduces to
//   baseline = box_top + ascent * fontSize,  ascent(Arial->Liberation Sans) = 0.9053 em
//   (hhea 1854/2048; boxH kept == (ascent+descent)*size so the valign-middle centering
//   term is zero — closed-loop self-check verifies/corrects the constant).
const ASCENT = 0.9053;
const DESCENT = 0.2119; // hhea -434/2048
const LINES = [
  { text: "[4] Introduction to", size: 50, baseline: 169.5, cx: 473 },
  { text: "Deep Learning", size: 70, baseline: 280, cx: 479.5 },
  { text: "and", size: 48, baseline: 346.5, cx: 478.5 },
  { text: "CNN", size: 71, baseline: 422.5, cx: 478.5 },
];
const BOX_W = 800; // wide enough that no line wraps (max ink width 480)

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 27)
drawHouseChrome(pres, slide, { numeral: "27" });

// Four-line section title — Arial Bold (Liberation Sans), BA-measured red, centered
LINES.forEach((L) => {
  const boxH = (ASCENT + DESCENT) * L.size;
  const topPx = L.baseline - ASCENT * L.size; // box_h == lineSpacing model
  slide.addText(L.text, {
    x: px(L.cx - BOX_W / 2), y: px(topPx), w: px(BOX_W), h: px(boxH),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: L.size, bold: true, color: TITLE_RED,
    lineSpacing: boxH,
  });
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
