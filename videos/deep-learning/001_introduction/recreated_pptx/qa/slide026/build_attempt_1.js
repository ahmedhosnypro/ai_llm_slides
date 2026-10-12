// slide_026.js — 001_introduction slide 26 "Update the weights by moving in the negative
// direction of the Gradient of the Loss function with respect to model weights"
// (Deep Learning DSAI 308). Fresh build (predecessor died before any artifact).
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_026.jpg (960x540, 1px = 1pt).
//   Forensics: qa/slide026/scratch/measure*.py, ascii*.py (banked).
// Chrome: playlist house chrome (founder directive 2026-10-11) via
//   shared_patterns/house_chrome.js — imported, NEVER re-drawn. Badge numeral 26
//   (file number; this lecture's frames carry no printed numbers — assumption
//   PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).
//
// MEASURED SPEC (frame px):
//   blue container  x 73..887, y 117..509 (borders: top rows 117-119, bottom 507-508,
//                   left cols 73-74, right col 886) — no fill, navy border ~2px
//   tan box 1       x 79..648, y 126..299, fill DCD4C9 (modal (220,212,201); spec guessed
//                   D6CFC5 — PIL modal wins per deck pixel law)
//   yellow box      x 82..762, y 306..369, fill FBFFD8 (modal (251,255,216); spec guessed
//                   FFFFCC — PIL modal wins)
//   tan box 2       x 79..842, y 375..501, fill DCD4C9
//   title L1 (red)   ink x 57..837 (center 447), cap top 59, baseline ~76.5
//                    -> TNR Bold 30pt (advance fit 29.9 @780px), color C00000 (deck red;
//                    JPEG-dark modals 136-160,0,0 = C00000 per certified slide_002/005)
//   title L2 (navy)  ink x 73..883 (center 478), cap top 88, baseline ~108.5
//                    -> TNR Bold 31.5pt (advance fit 31.6 @810px), color 000080 (core
//                    modal (0,0,120..135) = navy, NOT the spec's 0000CC; same navy as
//                    certified slide_005). Double space 'respect  to' preserved (spec law).
//                    NOTE: L1 center (447) != L2 center (478) in the ORIGINAL — each line
//                    is placed at its OWN measured ink center, not slide-centered.
//   note 1 '(For Sigmoid Function)'  red C00000, Arial Bold 16pt (advance fit 16.1),
//                    ink left 397, rows 209..223, baseline ~219.5
//   note 2 '(Error at Output layer ONLY)'  navy 000080, Arial Bold 16.5pt (fit 16.6),
//                    ink left 343, rows 267..282, baseline ~279.5; ONLY underlined
//                    (underline ink measured rows 280-281 under x 515..565)
//   'Let'            red C00000, TNR Bold 24pt (advance fit 24.1 @35px), ink left 462,
//                    rows 399..415, baseline 415.5 (same line as eq5)
//   'then'           red C00000, TNR Bold 25pt (advance fit 25.4 @48px), ink left 459,
//                    rows 461..477, baseline 477.5
//   red block arrow  x 320..348, y 138..148 (rows 139..147 body, tip right) C00000
//   black delta-link arrow  thin diagonal, ink (276,443)..(288,457), pointing down-left
//                    toward the delta_j of line 2; drawn (289,442)->(272,461) w1.25
//   footer bar       x 38..921, y 519..539 in the ORIGINAL (fully black to slide bottom);
//                    drawn y 519..537.5 (h 18.5) so the chrome's half-visible bottom stroke
//                    stays visible and house_chrome_check.py passes (2-frame-px deviation,
//                    documented — same as certified slide_002/005/031)
//   top red rule (spec region 1) = the chrome panel's own top red border (row 43):
//                    covered by the imported chrome; NOT drawn separately (measured).
//
// EQUATIONS (professional 2D law, certified mathtext->PNG mechanism):
//   30 chunk PNGs (eq026_cNNN.png + sidecars, banked in build/assets; manifest
//   eq_026_manifest.json). The original was authored with Equation-3.0-wide metrics:
//   at matched glyph height its tokens run 1.3-1.6x wider than any mathtext fontset
//   (measured: dejavusans/dejavuserif/stix/cm all 156-183px vs 287px on eq5). Strategy:
//   chunk each equation at the original's MEASURED token anchors (every chunk's ink left
//   edge = the original's token left edge; fraction chunks bar-anchored at the measured
//   bar row; text chunks baseline-anchored), heights fitted per chunk band. Residual:
//   chunk ink widths run ~5-25% narrow (glyph-metric residual per references/equations.md
//   — documented, not chased by breaking the height fit). Spacing commands (\; \,) inside
//   chunks reproduce the original's measured inter-token gaps; \; after \partial
//   reproduces the measured ~10px partial-derivative gaps.
//   Line baselines (frame px): eq1 151.5 (eq1b's own objects sit lower: frac bar 152.5,
//   '= O_i' baseline 158.5 — measured), sigmoid 220.5, error 275.5, chain 339.5 (bars
//   333.5), final L1 416.5 (bars 410), final L2 480.5.
//
// pptxgenjs laws: bare hex (no '#'), fontFace everywhere, margin: 0, explicit lineSpacing,
// images at EXACT sidecar size (never rescaled).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const EQMAN = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/eq_026_manifest.json");

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_026_recreated.pptx";

const px = (v) => v / 72; // frame px (=pt) -> inches

// palette (PIL-measured; bare hex)
const RED = "C00000";
const NAVY = "000080";
const BLACK = "000000";
const TAN = "DCD4C9";
const YELLOW = "FBFFD8";

const SERIF = "Times New Roman";
const SANS = "Arial";

// LO single-line baseline calibration (certified slide_031 constants):
// rendered baseline ~= top + (H - L)/2 + K*fs ; TNR K=0.924, Arial K=0.905.
function lineTop(baselinePx, fs, Hpx, Lpt, K) {
  const k = K === undefined ? 0.924 : K;
  return baselinePx - (Hpx - Lpt) / 2 - k * fs;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge "26") ----
drawHouseChrome(pres, slide, { numeral: "26" });

// ---- 2) blue container x73..887 y117..509 (no fill, navy ~2px border) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(73), y: px(117), w: px(814), h: px(392),
  fill: { color: "FFFFFF", transparency: 100 }, line: { color: NAVY, width: 2 },
});

// ---- 3) shaded boxes ----
slide.addShape(pres.ShapeType.rect, { // tan definitions box
  x: px(79), y: px(126), w: px(570), h: px(174),
  fill: { color: TAN }, line: { color: TAN, width: 0 },
});
slide.addShape(pres.ShapeType.rect, { // yellow chain-rule box
  x: px(82), y: px(306), w: px(681), h: px(64),
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0 },
});
slide.addShape(pres.ShapeType.rect, { // tan final-derivation box
  x: px(79), y: px(375), w: px(764), h: px(127),
  fill: { color: TAN }, line: { color: TAN, width: 0 },
});

// ---- 4) title, two lines at their own measured ink centers ----
// L1 red TNR Bold 30, center 447, baseline 76.5 (box h 43.2px, ls 36)
slide.addText("Update the weights by moving in the negative direction of the", {
  x: px(447) - 6, y: px(lineTop(76.5, 30, 43.2, 36)), w: 12, h: 0.6,
  align: "center", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: 30, bold: true, color: RED,
  lineSpacing: 36,
});
// L2 navy TNR Bold 31.5, center 478, baseline 108.5 (box h 43.2px, ls 38)
slide.addText("Gradient of the Loss function with respect  to model weights", {
  x: px(478) - 6, y: px(lineTop(108.5, 31.5, 43.2, 38)), w: 12, h: 0.6,
  align: "center", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: 31.5, bold: true, color: NAVY,
  lineSpacing: 38,
});

// ---- 5) red block arrow (tan1 line 1) x320..348 y138..148 ----
slide.addShape(pres.ShapeType.rightArrow, {
  x: px(320), y: px(138), w: px(28), h: px(10.5),
  fill: { color: RED }, line: { color: RED, width: 0 },
});

// ---- 6) black delta-link diagonal arrow (tan2), down-left, tip at (272,461) ----
slide.addShape(pres.ShapeType.line, {
  x: px(272), y: px(442), w: px(17), h: px(19), flipH: true,
  line: { color: BLACK, width: 1.25, endArrowType: "triangle" },
});

// ---- 7) parenthetical notes ----
// '(For Sigmoid Function)' red Arial Bold 16, ink left 397, baseline 219.5
slide.addText("(For Sigmoid Function)", {
  x: px(397), y: px(lineTop(219.5, 16, 28.8, 20, 0.905)), w: px(220), h: 0.4,
  align: "left", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 16, bold: true, color: RED,
  lineSpacing: 20,
});
// '(Error at Output layer ONLY)' navy Arial Bold 16.5, ink left 343, baseline 279.5,
// ONLY underlined (runs; underline on the ONLY run only)
slide.addText([
  { text: "(Error at Output layer ", options: {} },
  { text: "ONLY", options: { underline: true } },
  { text: ")", options: {} },
], {
  x: px(343), y: px(lineTop(279.5, 16.5, 28.8, 21, 0.905)), w: px(240), h: 0.4,
  align: "left", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 16.5, bold: true, color: NAVY,
  lineSpacing: 21,
});

// ---- 8) 'Let' / 'then' — red TNR Bold accents on the final-box lines ----
slide.addText("Let", {
  x: px(462), y: px(lineTop(415.5, 24, 28.8, 29)), w: px(60), h: 0.4,
  align: "left", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: 24, bold: true, color: RED,
  lineSpacing: 29,
});
slide.addText("then", {
  x: px(459), y: px(lineTop(477.5, 25, 28.8, 30)), w: px(70), h: 0.4,
  align: "left", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: 25, bold: true, color: RED,
  lineSpacing: 30,
});

// ---- 9) equations — chunk PNGs at EXACT sidecar size, anchor-placed ----
for (const e of EQMAN.slides[0].equations) {
  slide.addImage({
    path: `${ASSETS}/${e.image}`,
    x: e.x_in, y: e.y_in, w: e.w_in, h: e.h_in,
  });
}

// ---- 10) black footer bar (over the panel; chrome bottom stroke kept visible) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(884), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
