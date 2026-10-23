// Build script for slide 037 of
// videos/machine-learning/03_ridger_regression_gradient_descent
// "Problem Formulation"
//
// Frame geometric measurements (unique_slides/slide_037.jpg, 960x540 px = slide pts,
// 1px = 1pt = 1/72in; PIL-measured 2026-10-23, all values in frame px):
//
//   Title "Problem Formulation": red (#C00000) ink rows 64..84, cols 354..628, centered
//     (center x=479.5). Badge "37" per house chrome.
//   Pale-yellow panel #FFF9C4 with red #C00000 border: cols 69..893, rows 108..205
//   Tan panel #F5E6CA with red border (middle):  cols 69..893, rows 228..373
//   Tan panel #F5E6CA with red border (bottom):  cols 69..893, rows 380..534
//
//   Inside pale-yellow panel:
//     "Define δ_i as :" (red #C00000 bold): rows 111..134, cols 68..870 (heading)
//     implication line 1 (black): rows 144..171, cols 79..845
//     implication line 2 (black): rows 172..189, cols 79..844
//       red marks: rows 146..158 cols 128..594 / 172..185 cols 360..410
//       italic blue class labels ("class I", "Class II"): rows 146..159 cols 358..415
//   Inside middle tan panel:
//     "Redefine Error function as:" (red bold): rows 229..256, cols 77..
//     error equation line: rows 264..286, cols 82..868
//       Sigma ∑ ink at cols 203..220 rows 264..286
//       red Sum-subscript "all misclassified vectors (i)" BELOW the Sum:
//         rows 292..302, cols 151..271 (red)
//     "Summation is always positive": rows 310..326, cols 76..294
//       (red italic "positive" per spec)
//   Inside bottom tan panel:
//     "Minimize the Error using Gradient Descent with step η": rows 380..399
//       black italic, "Gradient Descent" blue + bold (blue ink rows 362..377 cols 295..445)
//     first update equation: main line rows 404..440 cols 84..762
//       Sigma ∑ ink cols 652..673; red subscript "misclassified vectors" below:
//         rows 442..452, cols 611..676
//       red "η" glyph at cols 224..250, rows 422..438
//     green highlight box (#E8F5E9 fill, soft green edge ~#99CC99): rows 458..521,
//       cols 66..488 — contains the SECOND update equation:
//       main line rows 472..500, cols 85..470
//       red Sum-subscript "misclassified vectors ONLY (i)" below: rows 506..514, cols 266..419
//     NOTE: the original has NO second light-green box on the first equation and NO
//       curved green arrow — PIL scan of green ink in rows 400..458 shows none. The
//       spec's "green rounded rectangle + curved arrow" on the first line is not present
//       in the measured frame; the frame wins (frame-vs-spec law).
//
// Equations are rendered in PROFESSIONAL 2D FORMAT via matplotlib mathtext -> 600dpi
// transparent PNG (scripts/render_eq.py) + eq_*.json sidecars: each Sigma carries its
// subscript stacked below it, matching the original's stacked rendering. Text is Arial
// (deck standard); math glyphs come from the mathtext DejaVu set (house law, accepted).
//
// Spec: analysis/slide_037_final.json — VERBATIM text, per-run colors per
// recreation_brief steps 5..15.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.join(
  __dirname, "..", "..", "shared_patterns", "house_chrome.js"
));

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const slide = pptx.addSlide();

// ---- House chrome: white canvas + E9E9E7 panel + C00000 L/R/bottom strokes + badge "37" ----
drawHouseChrome(pptx, slide, { numeral: 37 });

const FONT = "Arial";
const RED = "C00000";
const BLACK = "000000";
const BLUE = "0000FF";
const PALE_YELLOW = "FFF9C4";
const TAN = "F5E6CA";
const PANEL_RED = "C00000";
const BRIGHT_RED = "FF0000";
const GREEN_FILL = "E8F5E9";

const ASSET = __dirname + "/assets";
const px = (v) => v / 72; // frame px -> inches

// ---- panel geometry (frame px) ----
const PANELS = [
  { x: 69, y: 108, w: 893 - 69, h: 205 - 108, fill: PALE_YELLOW },
  { x: 69, y: 228, w: 893 - 69, h: 373 - 228, fill: TAN },
  { x: 69, y: 380, w: 893 - 69, h: 534 - 380, fill: TAN },
];
const PANEL_X = px(69), PANEL_W = px(893 - 69), PAD = px(12);

// ---- text metrics (frame px) ----
// cap-height advance from measured bands: heading ~20pt, body ~17pt, small subscript text ~13pt
const HEAD_SIZE = 20, BODY_SIZE = 17;

// helper: a single text line pinned to a measured ink TOP (frame px) and LEFT (frame px)
function line(text, leftPx, topPx, sizePx, color, opts = {}) {
  slide.addText(text, {
    x: px(leftPx), y: px(topPx), w: px(opts.w || 820), h: px(sizePx * 1.35),
    fontSize: sizePx, color, fontFace: FONT,
    bold: !!opts.bold, italic: !!opts.italic, underline: !!opts.underline,
    margin: 0, valign: "top", align: opts.align || "left",
  });
}
// helper: multi-run line (array of {text, options})
function runLine(runs, leftPx, topPx, sizePx, opts = {}) {
  slide.addText(runs.map((r) => ({
    text: r.text,
    options: Object.assign({ color: BLACK, fontSize: sizePx, fontFace: FONT }, r.options || {}),
  })), {
    x: px(leftPx), y: px(topPx), w: px(opts.w || 820), h: px(sizePx * 1.6),
    margin: 0, valign: "top", align: opts.align || "left",
  });
}

// ============================================================
// TITLE
// ============================================================
slide.addText("Problem Formulation", {
  x: 0, y: px(62), w: 13.333, h: px(34),
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// PANELS
// ============================================================
for (const p of PANELS) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(p.x), y: px(p.y), w: px(p.w), h: px(p.h),
    fill: { color: p.fill }, line: { color: PANEL_RED, width: 1.5 },
  });
}

// ============================================================
// PANEL 1 (pale yellow): Define δ_i as : + two implications
// ============================================================
// Heading — measured ink rows 111..134, cols 68..870
slide.addText([
  { text: "Define ", options: { color: RED, bold: true } },
  { text: "\u03b4", options: { color: RED, bold: true, italic: true } },
  { text: "_i", options: { color: RED, bold: true, italic: true, subscript: true } },
  { text: " as :", options: { color: RED, bold: true } },
], {
  x: PANEL_X, y: px(111), w: PANEL_W, h: px(HEAD_SIZE * 1.4),
  fontSize: HEAD_SIZE, fontFace: FONT, margin: 0, valign: "top",
});

// Implication 1 — measured ink rows 144..171, cols 79..845
// colors per recreation_brief step 6: class labels italic BLUE; "misclassified",
// arrows ⇒, δ_i, "-1" and "> 0" in BRIGHT RED; "d(X)" underlined.
const IMP_SIZE = BODY_SIZE;
runLine([
  { text: "If X \u2208 " },
  { text: "class I", options: { italic: true, color: BLUE } },
  { text: " and " },
  { text: "misclassified", options: { color: BRIGHT_RED } },
  { text: " as " },
  { text: "Class II", options: { italic: true, color: BLUE } },
  { text: " then " },
  { text: "d(X)", options: { underline: true } },
  { text: " will be " },
  { text: "<0", options: { color: BRIGHT_RED } },
  { text: " \u21d2 ", options: { color: BRIGHT_RED } },
  { text: "\u03b4", options: { color: BRIGHT_RED, italic: true } },
  { text: "_i", options: { color: BRIGHT_RED, italic: true, subscript: true } },
  { text: " = ", options: { color: BRIGHT_RED } },
  { text: "-1", options: { color: BRIGHT_RED } },
  { text: " \u21d2 ", options: { color: BRIGHT_RED } },
  { text: "d(X)", options: { underline: true } },
  { text: "\u03b4", options: { color: BRIGHT_RED, italic: true } },
  { text: "_i", options: { color: BRIGHT_RED, italic: true, subscript: true } },
  { text: " > 0", options: { color: BRIGHT_RED } },
], PANEL_X, px(144), IMP_SIZE);

// Implication 2 — measured ink rows 172..189, cols 79..844
runLine([
  { text: "If X \u2208 " },
  { text: "class II", options: { italic: true, color: BLUE } },
  { text: " and " },
  { text: "misclassified", options: { color: BRIGHT_RED } },
  { text: " as " },
  { text: "Class I", options: { italic: true, color: BLUE } },
  { text: " then " },
  { text: "d(X)", options: { underline: true } },
  { text: " will be " },
  { text: ">0", options: { color: BRIGHT_RED } },
  { text: " \u21d2 ", options: { color: BRIGHT_RED } },
  { text: "\u03b4", options: { color: BRIGHT_RED, italic: true } },
  { text: "_i", options: { color: BRIGHT_RED, italic: true, subscript: true } },
  { text: " = ", options: { color: BRIGHT_RED } },
  { text: "+1", options: { color: BRIGHT_RED } },
  { text: " \u21d2 ", options: { color: BRIGHT_RED } },
  { text: "d(X)", options: { underline: true } },
  { text: "\u03b4", options: { color: BRIGHT_RED, italic: true } },
  { text: "_i", options: { color: BRIGHT_RED, italic: true, subscript: true } },
  { text: " > 0", options: { color: BRIGHT_RED } },
], PANEL_X, px(172), IMP_SIZE);

// ============================================================
// PANEL 2 (middle tan): Redefine Error function
// ============================================================
// Heading — measured ink rows 229..256, cols 77..
line("Redefine Error function as:", px(77), px(229), HEAD_SIZE, RED, { bold: true });

// Error equation — main line rows 264..286, cols 82..868.
// Sigma ∑ ink cols 203..220; red stacked subscript "all misclassified vectors (i)"
// below it (rows 292..302, cols 151..271).
// The line composes: "Error = " + [Sigma+subscript image] + " δ_i W^T X_i ⇒ (W^T X_i) takes
// positive and negative values and δ_i has the same sign"
const EQ1_SIZE = 17;
runLine([{ text: "Error = " }], PANEL_X, px(264), EQ1_SIZE, { w: 120 });

// Sigma-with-subscript image (professional 2D format), bottom-aligned so the folded
// subscript sits under the Sum, matching the original's stacked rendering.
slide.addImage({
  path: ASSET + "/eq_037_sum_error.png",
  x: px(203 - 8), y: px(286 - 0.46333 * 600 + 135), // baseline pass; re-pinned in closed loop
  w: 1.94667, h: 0.46333,
});

runLine([
  { text: " \u03b4", options: { italic: true } },
  { text: "_i", options: { italic: true, subscript: true } },
  { text: " W" },
  { text: "T", options: { superscript: true } },
  { text: " X" },
  { text: "_i", options: { subscript: true } },
  { text: " " },
  { text: "\u21d2", options: { color: BRIGHT_RED, fontSize: EQ1_SIZE + 3 } },
  { text: " (W" },
  { text: "T", options: { superscript: true } },
  { text: " X" },
  { text: "_i", options: { subscript: true } },
  { text: ") takes " },
  { text: "positive", options: { color: BRIGHT_RED, italic: true } },
  { text: " and negative values and " },
  { text: "\u03b4", options: { italic: true, color: BRIGHT_RED } },
  { text: "_i", options: { italic: true, color: BRIGHT_RED, subscript: true } },
  { text: " has the same sign" },
], px(320), px(264), EQ1_SIZE, { w: 560 });

// "Summation is always positive" — measured ink rows 310..326, cols 76..294
runLine([
  { text: "Summation is always " },
  { text: "positive", options: { color: BRIGHT_RED, italic: true } },
], PANEL_X, px(310), EQ1_SIZE);

// ============================================================
// PANEL 3 (bottom tan): Minimize the Error using Gradient Descent
// ============================================================
// Heading — measured ink rows 380..399; black italic + blue bold "Gradient Descent"
runLine([
  { text: "Minimize the Error using ", options: { italic: true } },
  { text: "Gradient Descent", options: { italic: true, bold: true, color: BLUE } },
  { text: " with step ", options: { italic: true } },
  { text: "\u03b7", options: { italic: true } },
], PANEL_X, px(380), HEAD_SIZE);

// ---- first update equation: main line rows 404..440, cols 84..762 ----
// "W^(updated) = W^(old) - η ∂Error/∂W where ∂Error/∂W = " + [Sigma+sub image] + " δ_i X_i"
// measured: "W^(updated) = W^(old) - η ∂Error/∂W where ∂Error/∂W =" ends at col ~600;
// Sigma ink cols 652..673; red stacked subscript "misclassified vectors" rows 442..452
// cols 611..676; then "δ_i X_i" cols ~700..762.
const EQ2_SIZE = 17;
runLine([
  { text: "W" },
  { text: "(updated)", options: { superscript: true } },
  { text: " = W" },
  { text: "(old)", options: { superscript: true } },
  { text: " - " },
  { text: "\u03b7", options: { color: BRIGHT_RED } },
  { text: " " },
  { text: "\u2202Error/\u2202W" },
  { text: " " },
  { text: "where", options: { italic: true } },
  { text: " " },
  { text: "\u2202Error/\u2202W" },
  { text: " = " },
], PANEL_X, px(404), EQ2_SIZE, { w: 600 });

slide.addImage({
  path: ASSET + "/eq_037_sum_misclass.png",
  x: px(652 - 8), y: px(452 - 0.46333 * 600 + 135),
  w: 1.6, h: 0.38,
});

runLine([
  { text: " \u03b4", options: { italic: true } },
  { text: "_i", options: { italic: true, subscript: true } },
  { text: " X" },
  { text: "_i", options: { subscript: true } },
], px(700), px(404), EQ2_SIZE, { w: 80 });

// ---- green highlight box (measured rows 458..521, cols 66..488) ----
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(66), y: px(458), w: px(488 - 66), h: px(521 - 458),
  fill: { color: GREEN_FILL },
  line: { color: "99CC99", width: 1 },
});

// ---- second update equation inside the green box ----
// main line rows 472..500, cols 85..470:
// "W^(updated) = W^(old) - η " + [Sigma + red stacked subscript "misclassified vectors
// ONLY (i)"] + " δ_i X_i"
// red Sum-subscript measured rows 506..514, cols 266..419 (below the Sum).
runLine([
  { text: "W" },
  { text: "(updated)", options: { superscript: true } },
  { text: " = W" },
  { text: "(old)", options: { superscript: true } },
  { text: " - " },
  { text: "\u03b7", options: { color: BRIGHT_RED } },
  { text: " " },
], px(85), px(472), EQ2_SIZE, { w: 240 });

slide.addImage({
  path: ASSET + "/eq_037_sum_only.png",
  x: px(300 - 8), y: px(514 - 0.46333 * 600 + 135),
  w: 2.4, h: 0.57,
});

runLine([
  { text: " \u03b4", options: { italic: true } },
  { text: "_i", options: { italic: true, subscript: true } },
  { text: " X" },
  { text: "_i", options: { subscript: true } },
], px(420), px(472), EQ2_SIZE, { w: 80 });

// ============================================================
// OUTPUT
// ============================================================
const OUT = path.resolve(
  __dirname, "..", "..", "recreated_pptx", "slide_037_recreated.pptx"
);
pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));