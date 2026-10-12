// slide_022.js — 001_introduction slide 22 "Visualization of Single Perceptron"
// (Deep Learning DSAI 308). REWORKED build (attempt 2): resumes the crashed
// predecessor's build (banked as qa/slide022/build_pre_rework.js + render_1.png),
// keeping its measured structure and closing its empirical gaps found by
// closed-loop measurement of render_1 vs the ground-truth frame.
//
// RESUME PROVENANCE: predecessor measured the frame (scratch/slide022/forensics1..20
// + MEASUREMENTS.md), built eq022_* tokens + render_1, died before judging. This
// rework re-measured independently (scratch_022/forensics1..f26) and renders the
// equations from the eq_022_* asset set (STIX mathtext, fs-solved per token against
// measured ink, sidecars in eq_022_manifest.json). Empirical fixes vs render_1:
//   - title: TNR Bold 34 (render_1 @33 was 476px wide vs gt 490; 34 -> ~490.6,
//     cap 22.5 = gt 60..82.5 exactly), baseline 82.5
//   - box labels: TNR Italic 16 navy 000080 (render_1 @19 was 121/112 wide vs gt
//     104/91); blue = 000080 (darkest-px read (20,12,89)..(24,11,127); certified
//     slide_005 navy), not 0000CC; underline y172.5 (gt rows 172-173)
//   - case lines: full-line navy STIX renders (case1/2/3, w 116/116/184 = gt), the
//     case arrows are NAVY (PIL) — predecessor agreed; '>0/</=0' included
//   - EQ3 decision equation: per-token pinning (17 tokens at measured cluster x),
//     composed-segment interior drifted up to 14px around the '.....' in probe
//   - Sigma circle: d38 at (430.5,420.5) (render_1 oval h26 vs gt y402..439)
//   - step block: CIRCLE d36 center (489,421), purple 6F449D ring, NO fill, red
//     shaft crossing under (render_1 rect h16 vs gt ring arcs y403..439); second
//     arrowhead into the block added (gt blob x455..473)
//   - fan lines: start x272 (gt traces pass x306 at ys 377..471; render_1 started
//     x312 -> no ink at x306), rows [360.5,383,405,430.5,453,473.5,494.5]
//   - O/P: TNR Bold 20 ink-left 575 (render_1 @19 x583 w30 vs gt x575 w33)
//   - callout: TNR Bold-Italic 17.8 (render_1 @19 163/82 wide vs gt 149/79)
//   - step glyph NAVY 000080 (measured (38,19,126)/(43,23,134)), not #333
//   - reds = C00000 (measured modals 982030/A00020/B02038 = title-red family)
// PIL overrides of spec guesses (deck pixel law — modal beats vision guess):
//   - decision box fill #FAFEED, callout fill #E3E5C9 + dark-tan border #A79E88,
//     callout text dark brown #604820, case-grouping bar = thin lavender hairline
//     x544 y264..323 (spine washed (175,172,201) — NOT red; the spec's "red brace"
//     hooks were the '>' glyphs of case lines 1/3), W red, d(X) X red, no red brace.
//   - "wn" sits HIGH in the diagram, beside the second dots row (measured, reproduced)
// Excluded as recording artifacts: mouse cursor. Black bottom bar DRAWN per certified
// deck precedent (002/005/031): x38..921 y518..537.5, chrome stroke stays visible.
//
// pptxgenjs laws: bare hex (no '#'), fontFace everywhere, margin: 0, explicit
// lineSpacing, images at EXACT sidecar size (never rescaled).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const EQ = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/eq_022_manifest.json");

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_022_recreated.pptx";

const px = (v) => v / 72; // frame px (=pt) -> inches
const PAD_IN = 8 / 600;   // transparent pad around each equation PNG's ink

// palette (PIL-measured; bare hex)
const RED = "C00000";
const BLACK = "000000";
const NAVY = "000080";
const WHITE = "FFFFFF";
const DEC_FILL = "FAFEED";
const CALL_FILL = "E3E5C9";
const CALL_BORDER = "A79E88";
const CALL_TEXT = "604820";
const PINK = "FF66CC";
const BLOCK_BORDER = "6F449D";
const STEPG = "000080";
const CYAN = "CCFFFF";
const BAR = "5550A0";

const FONT = "Times New Roman";

// LO single-line baseline calibration (slide_031 precedent)
function lineTop(baselinePx, fs, Hpt, Lpt, K) {
  const k = K === undefined ? 0.955 : K;
  return baselinePx - (Hpt - Lpt) / 2 - k * fs;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge "22") ----
drawHouseChrome(pres, slide, { numeral: "22" });

// ---- 2) content boxes ----
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
// 2.b) Sigma circle drawn HERE (z-order fix): the cyan disc must sit UNDER the
// Sigma glyph image, which the equation-images loop adds in section 4. In the
// previous render the opaque disc was drawn after it and erased the glyph
// (crop_diag BLOCKER: 'Sigma missing').
slide.addShape(pres.ShapeType.ellipse, {
  x: px(411.5), y: px(402), w: px(38), h: px(38),
  fill: { color: CYAN }, line: { color: BLACK, width: 1 },
});

// ---- 3) title — TNR Bold 34 C00000, ink center 473.5, baseline 82.5 ----
slide.addText("Visualization of Single Perceptron", {
  x: px(473.5) - 4, y: px(lineTop(82.5, 34, 40, 40)), w: 8, h: 0.55,
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 34, bold: true, color: RED,
  lineSpacing: 40,
});

// ---- 4) equation tokens (eq_022 manifest; baseline law) ----
for (const e of EQ.equations) {
  const wIn = e.w_px / 600, hIn = e.h_px / 600;
  const xIn = e.anchor.mode === "left"
    ? e.anchor.x / 72 - PAD_IN
    : (e.anchor.x - (e.w_px * 72 / 600) / 2) / 72;
  const yIn = (e.baseline_px - e.baseline_frac * (e.h_px * 72 / 600)) / 72;
  slide.addImage({ path: `${ASSETS}/${e.path}`, x: xIn, y: yIn, w: wIn, h: hIn });
}
// stretched-glyph parens (top-left anchored, exact size)
for (const p of EQ.parens) {
  slide.addImage({
    path: `${ASSETS}/${p.image}`,
    x: p.x_px / 72, y: p.y0_px / 72, w: p.w_px / 600, h: p.h_px / 600,
  });
}

// ---- 5) blue labels (TNR italic 16, navy 000080) + measured underlines ----
slide.addText("Ugmented Vector", {
  x: px(299.3), y: px(lineTop(172, 16, 36, 24) - 4.5), w: 1.85, h: 0.5,
  align: "left", valign: "middle", margin: 0, italic: true,
  fontFace: FONT, fontSize: 15.4, color: NAVY, lineSpacing: 24,
});
slide.addShape(pres.ShapeType.rect, {
  x: px(300), y: px(172.5), w: px(105), h: px(1.2),
  fill: { color: NAVY }, line: { color: NAVY, width: 0 },
});
slide.addText("Model Weights", {
  x: px(669.3), y: px(lineTop(172, 16, 36, 24) - 4.5), w: 1.6, h: 0.5,
  align: "left", valign: "middle", margin: 0, italic: true,
  fontFace: FONT, fontSize: 16, color: NAVY, lineSpacing: 24,
});
slide.addShape(pres.ShapeType.rect, {
  x: px(670), y: px(172.5), w: px(92), h: px(1.2),
  fill: { color: NAVY }, line: { color: NAVY, width: 0 },
});

// ---- 6) case-group delimiters: hairline curved paren pair from the manifest
// (replaces the earlier straight bar; the original encloses the 3 cases on BOTH
// sides — judge dec-crop MAJOR find) ----

// ---- 7) perceptron diagram ----
// 7.a fan lines: pink FF66CC from (272,row_y) to junction (398,421)
const ROWS = [360.5, 383, 405, 430.5, 453, 473.5, 494.5];
for (const ry of ROWS) {
  const y0 = ry, y1 = 421;
  slide.addShape(pres.ShapeType.line, {
    x: px(272), y: px(Math.min(y0, y1)), w: px(126), h: px(Math.abs(y1 - y0)),
    flipV: y1 < y0,
    line: { color: PINK, width: 1 },
  });
}
// 7.b junction: red triangle pointing right (396,415)-(407,427)
slide.addShape(pres.ShapeType.triangle, {
  x: px(396), y: px(415), w: px(11), h: px(12), rotate: 90,
  fill: { color: RED }, line: { color: RED, width: 0 },
});
// 7.c2 activation block FIRST: PINK-FILLED RECTANGLE w/ magenta border (judge crop
// read: IMG2 = pink-filled rect x468.5..510.5 y404.5..438). Drawn BEFORE the shaft so
// the red line crosses visibly OVER the fill, exactly as in the original.
slide.addShape(pres.ShapeType.rect, {
  x: px(468.5), y: px(404.5), w: px(42), h: px(33.5),
  fill: { color: "E9B7D4" }, line: { color: "CC66CC", width: 1.5 },
});
// 7.d thick red shaft y419..423.5 x447..563 (OVER the block fill, UNDER the stem)
slide.addShape(pres.ShapeType.rect, {
  x: px(447), y: px(419), w: px(116), h: px(4.5),
  fill: { color: RED }, line: { color: RED, width: 0 },
});
// 7.e second arrowhead into the block (gt blob x455..473)
slide.addShape(pres.ShapeType.triangle, {
  x: px(461.5), y: px(415.5), w: px(11), h: px(12), rotate: 90,
  fill: { color: RED }, line: { color: RED, width: 0 },
});
// 7.f block border re-stroke over the shaft edges is unnecessary — border drawn with
// the fill above; the shaft crossing it at y419..423 matches the original's
// continuous red read.
// 7.g step glyph: bottom bar, stem, top bar — NAVY (measured), stem breaks the red
slide.addShape(pres.ShapeType.rect, { // bottom bar x481..495 y428.5..431
  x: px(481), y: px(428.5), w: px(14), h: px(2.5),
  fill: { color: STEPG }, line: { color: STEPG, width: 0 },
});
slide.addShape(pres.ShapeType.rect, { // stem x492..494 y412..431
  x: px(492), y: px(412), w: px(2), h: px(19),
  fill: { color: STEPG }, line: { color: STEPG, width: 0 },
});
slide.addShape(pres.ShapeType.rect, { // top bar x494..508 y412..414.5
  x: px(494), y: px(412), w: px(14), h: px(2.5),
  fill: { color: STEPG }, line: { color: STEPG, width: 0 },
});
// 7.h red head: triangle (563,415.5)-(574.5,427.5)
slide.addShape(pres.ShapeType.triangle, {
  x: px(563), y: px(415.5), w: px(11.5), h: px(12), rotate: 90,
  fill: { color: RED }, line: { color: RED, width: 0 },
});
// 7.i O/P — bold black TNR 20, ink x575 baseline 428
slide.addText("O/P", {
  x: px(574.3), y: px(lineTop(428, 20, 28.8, 22)), w: 0.8, h: 0.4,
  align: "left", valign: "middle", margin: 0, bold: true,
  fontFace: FONT, fontSize: 20, color: BLACK, lineSpacing: 22,
});

// ---- 8) classification callout (tan, dark-tan border, brown bold-italic TNR 17.8) ----
slide.addShape(pres.ShapeType.rect, { // x626.5..818.5 y395.5..444.5
  x: px(626.5), y: px(395.5), w: px(192), h: px(49),
  fill: { color: CALL_FILL }, line: { color: CALL_BORDER, width: 1.5 },
});
slide.addText("Binary Classification", {
  x: px(626.5), y: px(lineTop(420, 17.8, 36, 24)), w: px(192), h: 0.5,
  align: "center", valign: "middle", margin: 0, bold: true, italic: true,
  fontFace: FONT, fontSize: 17.8, color: CALL_TEXT, lineSpacing: 24,
});
slide.addText("(2 Classes)", {
  x: px(626.5), y: px(lineTop(436.5, 17.8, 36, 24)), w: px(192), h: 0.5,
  align: "center", valign: "middle", margin: 0, bold: true, italic: true,
  fontFace: FONT, fontSize: 17.8, color: CALL_TEXT, lineSpacing: 24,
});

// ---- 9) black bottom bar (certified deck precedent; chrome stroke stays visible) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(518), w: px(884), h: px(19.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
