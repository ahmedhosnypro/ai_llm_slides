// Slide 002 — "Linear Regression" (section divider)
// Deck: machine-learning/02_linear-regression-classification-MSSE
//
// Ground truth: unique_slides/slide_002.jpg (960x540, 1px = 1pt = 1/72 in).
// PIL measurements 2026-10-13 (worker ml02-w002-a1):
//   - Title "Linear Regression" red ink bbox x 304..668, y 248..288
//     (ink center x=486 ~ panel center 480; cap+descender height 41px -> ~44pt Arial Bold;
//      core color ~ (170,24,41) JPEG-soft of C00000)
//   - Badge yellow disc x 860..893, y 59..89 (center ~(876,74), d~34) = canonical chrome
//   - Cursor artifact at ~(813,394): screen-recording overlay, GROUND RULES (c) — NOT drawn
// House chrome via the deck's shared module (panel x61..899 y46->bottom, C00000 border,
// red bottom stroke rows 538-539, badge FDFD96 center (876,73) d35 ring 6A5ACD, numeral 2).
// Title placement is closed-loop (worker ml02-w002-a3, resumed from ml02-w002-a1):
//   attempt 1: ink center (479.8, 273.8) vs original (486, 268) — 44pt, box on panel center
//   attempt 2: ink center (486.0, 268.1) EXACT; vertical extent 248.2..288.0 matches
//              original 248..288 within 0.2px; but font-metric width 377 px vs original
//              365 px put both horizontal edges ±6.4px off (symmetric about true center)
//   attempt 3: fontSize 43 (still in the 40-44pt spec band) — advance width scales to
//              ~368 px, collapsing the edge residual to ~±2px; boxCenterY re-corrected
//              (ink-below-box-center offset scales with font size: 5.8*43/44 ≈ 5.7)
// Verified post-render by PIL ink-band comparison (selfcheck_attempt_3.py).

const path = require("path");
const pptxgen = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require(path.join(
  __dirname, "..", "..", "shared_patterns", "house_chrome.js"
));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "slide-recreation";
pres.title = "Linear Regression";

const slide = pres.addSlide();

// --- House chrome (shared module; numeral = number printed on the original = 2) ---
drawHouseChrome(pres, slide, { numeral: 2 });

// --- Title ---
// Original ink: x 304..668 (center 486 px), y 248..288 (center 268 px) — re-measured
// from slide_002.jpg by ml02-w002-a3 2026-10-13 (matches worker a1's numbers).
// Box spans the panel width but is OFFSET so its center lands on the measured ink
// center x=486 (panel center is 480; the original title sits 6px right of it).
// Vertical: attempt-1 closed loop showed LO renders the ink 5.8px BELOW the box
// center, so boxCenterY = 268 - 5.8 ≈ 262 px.
const TITLE = {
  text: "Linear Regression",
  color: "C00000",        // unhashed for pptxgenjs
  fontSize: 43,           // 40-44pt spec band; 43 collapses font-width edge residual to ~2px
  boxW: CHROME.panel.w,
  boxX: CHROME.panel.x + 6 / 72,          // ink center x 486, not panel center 480
  boxCenterY: (268 - 5.7) / 72,           // closed-loop corrected ink center y 268 (43pt)
  boxH: 1.2,
};
slide.addText(TITLE.text, {
  x: TITLE.boxX,
  y: TITLE.boxCenterY - TITLE.boxH / 2,
  w: TITLE.boxW,
  h: TITLE.boxH,
  align: "center",
  valign: "middle",
  bold: true,
  fontSize: TITLE.fontSize,
  color: TITLE.color,
  fontFace: "Arial",
  margin: 0,
});

// --- Exclusions (per spec recreation_brief step 5 + 6): no bullets, no subtitle,
// no images, no footer, no cursor artifact. Nothing else on the slide. ---

const OUT = path.join(__dirname, "..", "slide_002_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE", OUT);
});
