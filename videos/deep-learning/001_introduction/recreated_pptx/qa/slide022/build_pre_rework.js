// slide_022.js — 001_introduction slide 22 "Visualization of Single Perceptron"
// (Deep Learning DSAI 308). Fresh build, sole owner, 2026-10-12.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_022.jpg (960x540, 1px = 1pt)
//   (scratch/slide022/forensics1..20.py + MEASUREMENTS.md — full table banked there).
//   Direct 1px=1pt mapping — the certified precedent of this video (001/002/005/031).
// Chrome: playlist house chrome (founder directive 2026-10-11) via
//   shared_patterns/house_chrome.js — imported, NEVER re-drawn. Badge numeral 22
//   (file number; this lecture's frames carry no printed numbers — assumption
//   PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).
//
// EQUATIONS (professional 2D law): mathtext has NO matrix/array environment, so the
// CERTIFIED slide_031/002 mechanism applies: per-entry STIX-serif mathtext renders at
// 600dpi (scripts/render_eq.py via gen_assets_022.py), embedded at EXACT sidecar size
// (w = px/600 in, NEVER rescaled), anchored at MEASURED ink-left + per-entry baseline
// (baseline_frac law). Column-vector parens + red case brace: stretched-glyph pattern
// (huge glyph, tight crop, anisotropic resize, recolor) -> eq022_pv*/brace PNGs.
// Five-dot "....." in the decision equation: PIL-drawn dots (mathtext '.....' measured
// 42pt vs the original's 22pt).
//
// PIL overrides of spec guesses (deck pixel law — modal beats vision guess):
//   - decision box fill #FAFEED (modal 250,254,237), not #FFFFE1
//   - callout fill #E3E5C9, border DARK TAN #A79E88 (not red), text dark brown #663300
//   - step-block border purple #6F449D (measured (111,68,157)), not #FF66CC
//   - case arrows BLUE like the case text (PIL), spec's "red arrows" overridden
//   - eq2 "W" RED, eq3 "d(X)" X RED (measured); NO underlines under X/W (0-7 noise px)
//   - "wn" sits HIGH in the diagram, beside the second dots row (measured, reproduced)
// Excluded as recording artifacts (GROUND RULES (c) + spec brief step 15): mouse cursor.
// Black bottom bar DRAWN per certified deck precedent (slides 002/005/031): x38..921,
// y518..537.5 so the chrome's half-visible bottom stroke stays visible.
//
// pptxgenjs laws: bare hex (no '#'), fontFace everywhere, margin: 0, explicit
// lineSpacing on multi-line text, images at EXACT sidecar size.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const EQ = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/eq022_manifest.json");

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_022_recreated.pptx";

const px = (v) => v / 72; // frame px (=pt) -> inches

// palette (PIL-measured; bare hex for pptxgenjs)
const RED = "C00000";        // title + box borders (deck precedent, washed-red modals)
const BLACK = "000000";      // math glyphs, O/P, step glyph, black bar
const INKRED = "FF0000";     // in-equation red: =>, b, 1, b*1, brace, junction, arrows
const BLUE = "0000CC";       // labels, weight labels, case lines
const WHITE = "FFFFFF";
const DEC_FILL = "FAFEED";   // decision box (modal 250,254,237)
const CALL_FILL = "E3E5C9";  // callout fill (modal 226,229,202)
const CALL_BORDER = "A79E88";// callout border (dark tan, measured)
const CALL_TEXT = "663300";  // callout text (dark brown, measured core)
const PINK = "FF66CC";       // fan lines
const BLOCK_BORDER = "6F449D"; // step block border (measured purple)
const STEPG = "333333";      // step glyph bars/stem
const CYAN = "CCFFFF";       // sigma circle fill

const FONT = "Times New Roman";

// LO single-line baseline calibration (slide_031 precedent): for box height H pt and
// lineSpacing L pt, top = baseline - (H - L)/2 - K*fs; K pinned from attempt-1 render.
function lineTop(baselinePx, fs, Hpt, Lpt, K) {
  const k = K === undefined ? 0.955 : K;
  return baselinePx - (Hpt - Lpt) / 2 - k * fs;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge "22") ----
drawHouseChrome(pres, slide, { numeral: "22" });

// ---- 2) content boxes (PIL fill bboxes; rect path = fill edge - ~1.5px) ----
slide.addShape(pres.ShapeType.rect, { // left box  x82.5..418.5 y88.5..246.5
  x: px(82.5), y: px(88.5), w: px(336), h: px(158),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
slide.addShape(pres.ShapeType.rect, { // right box x528.5..792.5 y88.5..245.5
  x: px(528.5), y: px(88.5), w: px(264), h: px(157),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
slide.addShape(pres.ShapeType.rect, { // decision box x81.5..766.5 y255.5..342.5
  x: px(81.5), y: px(255.5), w: px(685), h: px(87),
  fill: { color: DEC_FILL }, line: { color: RED, width: 1.5 },
});
slide.addShape(pres.ShapeType.rect, { // diagram box x228.5..612.5 y350.5..508
  x: px(228.5), y: px(350.5), w: px(384), h: px(157.5),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// ---- 3) title — TNR Bold 34 C00000, ink center 473.5, baseline 82.5 ----
// attempt-1 closed loop: fs 33 rendered 476.6pt wide vs orig 492 -> fs 34; LO put the
// cap-top +1.5 low -> baseline target 81.7. box h 0.8in (57.6pt), lineSpacing 40.
slide.addText("Visualization of Single Perceptron", {
  x: px(473.5) - 4, y: px(lineTop(81.7, 34, 57.6, 40)), w: 8, h: 0.8,
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 34, bold: true, color: RED,
  lineSpacing: 40,
});

// ---- 4) equation tokens (manifest-driven; baseline law) ----
for (const e of EQ.assets) {
  if (e.kind === "token") {
    slide.addImage({
      path: `${ASSETS}/${e.image}`,
      x: e.x_pt / 72 - (e.pad === false ? 0 : 0.0133), // tight-crop pad compensation
      y: e.baseline_pt / 72 - e.baseline_frac * e.h_in, // ALIGNMENT LAW
      w: e.w_in, h: e.h_in,
    });
  } else { // stretched delimiters anchored by top-left, exact size
    slide.addImage({
      path: `${ASSETS}/${e.image}`,
      x: e.x_pt / 72, y: e.y_pt / 72, w: e.w_in, h: e.h_in,
    });
  }
}

// ---- 5) blue labels (TNR italic, underlined via rect) ----
// "Ugmented Vector": ink x297..407 baseline 172, fs 19; underline y~175 x297..407
// "Model Weights": ink x668..762 baseline 172
slide.addText("Ugmented Vector", {
  x: px(297), y: px(lineTop(172, 19, 36, 24)), w: 1.85, h: 0.5,
  align: "left", valign: "middle", margin: 0, italic: true,
  fontFace: FONT, fontSize: 18, color: BLUE, lineSpacing: 24,
});
slide.addShape(pres.ShapeType.rect, {
  x: px(297.5), y: px(173.5), w: px(110), h: px(1.2),
  fill: { color: BLUE }, line: { color: BLUE, width: 0 },
});
slide.addText("Model Weights", {
  x: px(669.5), y: px(lineTop(172, 19, 36, 24)), w: 1.6, h: 0.5,
  align: "left", valign: "middle", margin: 0, italic: true,
  fontFace: FONT, fontSize: 17.5, color: BLUE, lineSpacing: 24,
});
slide.addShape(pres.ShapeType.rect, {
  x: px(669.5), y: px(173.5), w: px(93), h: px(1.2),
  fill: { color: BLUE }, line: { color: BLUE, width: 0 },
});

// ---- 6) case words (upright serif text; tokens carry >0/<0/=0 and blue arrows) ----
// attempt-1 loop: fs 21 rendered +4..8 wide -> fs 19.5; LO rendered +1 low -> baselines -1
slide.addText("Class I", {
  x: px(613.5), y: px(lineTop(278.5, 19.5, 36, 26)), w: 1.2, h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 19.5, color: BLUE, lineSpacing: 26,
});
slide.addText("Class II", {
  x: px(613.5), y: px(lineTop(300.5, 19.5, 36, 26)), w: 1.2, h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 19.5, color: BLUE, lineSpacing: 26,
});
slide.addText("Undefined Class", {
  x: px(613.5), y: px(lineTop(322.5, 19.5, 36, 26)), w: 2.0, h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 19.5, color: BLUE, lineSpacing: 26,
});

// ---- 7) perceptron diagram ----
// 7.a fan lines: pink FF66CC from (312,row_y) to junction (397,420.5)
const ROWS = [360.5, 383, 405, 430.5, 453, 473.5, 494.5];
for (const ry of ROWS) {
  const y0 = ry, y1 = 420.5;
  slide.addShape(pres.ShapeType.line, {
    x: px(312), y: px(Math.min(y0, y1)), w: px(85), h: px(Math.abs(y1 - y0)),
    flipV: y1 < y0,
    line: { color: PINK, width: 1 },
  });
}
// 7.b junction: red triangle pointing right (398,415)-(398,427)-(409,421)
slide.addShape(pres.ShapeType.triangle, {
  x: px(398), y: px(415), w: px(11), h: px(12), rotate: 90,
  fill: { color: INKRED }, line: { color: INKRED, width: 0 },
});
// 7.c sigma circle: oval x411..444 y406..432, cyan fill, black outline
slide.addShape(pres.ShapeType.ellipse, {
  x: px(411), y: px(406), w: px(33), h: px(26),
  fill: { color: CYAN }, line: { color: BLACK, width: 1 },
});
// 7.d step block: x470.5..512 path y413..429, purple border, NO fill (red shaft crosses)
slide.addShape(pres.ShapeType.rect, {
  x: px(470.5), y: px(413), w: px(41.5), h: px(16),
  fill: { color: WHITE, transparency: 100 }, line: { color: BLOCK_BORDER, width: 1.75 },
});
// 7.e thick red shaft y419..423.5 x447..563 (UNDER block borders + stem)
slide.addShape(pres.ShapeType.rect, {
  x: px(447), y: px(419), w: px(116), h: px(4.5),
  fill: { color: INKRED }, line: { color: INKRED, width: 0 },
});
// 7.f step glyph: bottom bar, stem (breaks the red), top bar — dark
slide.addShape(pres.ShapeType.rect, { // bottom bar x476..490.5 y428..430.5
  x: px(476), y: px(428), w: px(14.5), h: px(2.5),
  fill: { color: STEPG }, line: { color: STEPG, width: 0 },
});
slide.addShape(pres.ShapeType.rect, { // stem x488.5..491.5 y414..428
  x: px(488.5), y: px(414), w: px(3), h: px(14),
  fill: { color: STEPG }, line: { color: STEPG, width: 0 },
});
slide.addShape(pres.ShapeType.rect, { // top bar x492..505.5 y412..414.5
  x: px(492), y: px(412), w: px(13.5), h: px(2.5),
  fill: { color: STEPG }, line: { color: STEPG, width: 0 },
});
// 7.g red head: triangle (563,415.5)-(563,427.5)-(574.5,421.5)
slide.addShape(pres.ShapeType.triangle, {
  x: px(563), y: px(415.5), w: px(11.5), h: px(12), rotate: 90,
  fill: { color: INKRED }, line: { color: INKRED, width: 0 },
});
// 7.h O/P — bold black TNR ~19pt, ink x583 baseline 428
slide.addText("O/P", {
  x: px(582), y: px(lineTop(428, 19, 28.8, 22)), w: 0.8, h: 0.4,
  align: "left", valign: "middle", margin: 0, bold: true,
  fontFace: FONT, fontSize: 19, color: BLACK, lineSpacing: 22,
});

// ---- 8) classification callout (tan, dark-tan border, brown bold-italic text) ----
slide.addShape(pres.ShapeType.rect, { // x626.5..818.5 y395.5..444.5
  x: px(626.5), y: px(395.5), w: px(192), h: px(49),
  fill: { color: CALL_FILL }, line: { color: CALL_BORDER, width: 1.5 },
});
// line1 "Binary Classification" ink x648..799 baseline 420; centered on 723.5
// attempt-1 loop: fs 19 rendered ~168 wide vs orig 151 -> fs 18 + charSpacing -0.4; LO +2 low
slide.addText("Binary Classification", {
  x: px(626.5), y: px(lineTop(416, 18, 36, 24)), w: px(192), h: 0.5,
  align: "center", valign: "middle", margin: 0, bold: true, italic: true, charSpacing: -0.4,
  fontFace: FONT, fontSize: 18, color: CALL_TEXT, lineSpacing: 24,
});
// line2 "(2 Classes)" ink x683..764 baseline 437
slide.addText("(2 Classes)", {
  x: px(626.5), y: px(lineTop(433, 18, 36, 24)), w: px(192), h: 0.5,
  align: "center", valign: "middle", margin: 0, bold: true, italic: true, charSpacing: -0.4,
  fontFace: FONT, fontSize: 18, color: CALL_TEXT, lineSpacing: 24,
});

// ---- 9) black bottom bar (certified deck precedent; chrome stroke stays visible) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(518), w: px(884), h: px(19.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
