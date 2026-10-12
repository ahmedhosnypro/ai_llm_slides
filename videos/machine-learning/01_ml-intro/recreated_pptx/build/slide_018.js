// Slide 018 recreation — "Data Overfit and Underfit" (attempt 2)
// Spec: videos/ml-intro/analysis/slide_018_final.json (validation PASS_WITH_FIXES applied)
//
// NOTE: this file previously held the OLD-numbered (pre-curation, old id 18 =
// new id 15) build; that evidence is preserved verbatim at
// videos/ml-intro/recreated_pptx/build/archive_old104/slide_018_old18.js
// (matching pptx at recreated_pptx/archive_old104_pptx/slide_018_old18_recreated.pptx).
//
// House-frame rule (founder directive 2026-10-09, OVERRIDES spec + judge for these):
//   LAYOUT_WIDE 13.33x7.5, bg E8E8E8, outer red frame 0.15/0.15/13.03/7.2 line C00000 1.5,
//   badge oval 12.48/0.30/0.5/0.5 fill+line FFF9C4 with numeral "18" bold 18pt 333333,
//   title box y:0.28 x:0.6 w:12.13 centered.
//
// Attempt-2 fixes (judge attempt 1, judge_attempt_1.txt):
//   1. MAJOR: M=9 curve was a tame Catmull-Rom thread — now a TRUE degree-9
//      interpolating polynomial through all 10 data points (Vandermonde solve),
//      sampled densely and clamped at the axes frame: strong between-point
//      oscillation + boundary overshoot, the canonical Bishop overfit figure.
//   2. MINOR red hue: bullet-1 text, 'Simple models', 'General guideline:' are
//      dark maroon #8B0000 in the original (resolves the spec uncertain_item
//      "exact shade of the red bullet text").
//   3. MINOR underlines: 'can prevent overfitting' and 'not-too-simple, yet
//      not-too-complex' are hyperlink-blue underlined in the original.
//   4. MINOR: removed the bullet glyph on the third question line
//      (original has no visible marker there).
//   5. MINOR wrapping: the four Lesson/guideline lines are single-line in the
//      original — moved to a full-width band below the plots grid.
//   6. MINOR: plot titles INSIDE the top of each axes area (not above), and
//      lighter/smaller axes + ticks (original's are finer).
//
// Layout bands from spec layout.regions (amended per judge):
//   title ~5-15% h | content box ~20-90% h | questions top-left | plots grid
//   top-right ~55-90% w, ~20-60% h | lesson lines full-width band below plots

const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";     // slide background — HOUSE FRAME rule (overrides spec FFFFFF)
const FRAMERED = "C00000";  // house outer frame line
const DARKRED = "8B0000";   // title + content-box border + maroon text (judge attempt 1)
const BLK = "000000";      // body text / axes
const BLU = "0000CC";      // bullet-2 text + hyperlink-blue underlines + data dots
const GREEN = "009900";    // green question text (spec)
const CHGRN = "00CC00";    // chart 'true' curve green (spec, distinct from text green)
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// Straight line-segment helper (flip-safe, as in the proven slide-007/old-018 pattern).
function seg(x1, y1, x2, y2, lineOpts) {
  const w = Math.max(Math.abs(x2 - x1), 0.001);
  const h = Math.max(Math.abs(y2 - y1), 0.001);
  s.addShape(pptx.shapes.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w, h,
    flipH: x2 < x1, flipV: y2 < y1,
    line: lineOpts,
  });
}

// ---------- HOUSE FRAME ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: FRAMERED, width: 1.5 },
});

// ---------- Badge (HOUSE values, numeral = slide id 18) ----------
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("18", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ---------- Title (HOUSE box y:0.28 x:0.6 w:12.13, centered) ----------
s.addText("Data Overfit and Underfit", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.05, align: "center", valign: "middle",
  fontSize: 30, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
});

// ---------- Content box (spec: ~10-90% w, ~20-90% h, thin #8B0000 border) ----------
const CB = { x: 1.35, y: 1.55, w: 10.63, h: 5.4 };
s.addShape(pptx.shapes.RECTANGLE, {
  x: CB.x, y: CB.y, w: CB.w, h: CB.h,
  fill: { color: "FFFFFF" }, line: { color: DARKRED, width: 1.5 },
});

// ---------- Questions block (top-left of content box) ----------
const TX = 1.78, TW = 5.4;   // text column x/width (to ~7.18)
const FS = 17;              // body font size

s.addText("Questions:-", {
  x: TX, y: 1.92, w: TW, h: 0.4, fontSize: 20, bold: true, color: BLK,
  fontFace: FONT, margin: 0, align: "left", valign: "top",
});

// Bullet 1 — dark maroon (judge attempt 1: original is #8B0000), manual bullet glyph
s.addText(
  [{ text: "• Which of the four red curves fits the data (blue dots) best?",
     options: { color: DARKRED, fontFace: FONT } }],
  { x: TX, y: 2.44, w: TW, h: 0.62, fontSize: FS, align: "left", valign: "top",
    margin: 0, paraSpaceAfter: 0 }
);

// Bullet 2 — blue, 'generalize' underlined
s.addText(
  [
    { text: "• Which curve is expected to ", options: { color: BLU, fontFace: FONT } },
    { text: "generalize", options: { color: BLU, fontFace: FONT, underline: true } },
    { text: " the best?", options: { color: BLU, fontFace: FONT } },
  ],
  { x: TX, y: 3.14, w: TW, h: 0.62, fontSize: FS, align: "left", valign: "top", margin: 0 }
);

// Bullet 3 — green bold question + black remainder; NO bullet glyph (judge attempt 1)
s.addText(
  [
    { text: "Are they both the same?", options: { color: GREEN, fontFace: FONT, bold: true } },
    { text: " If yes, why? If no, why not?", options: { color: BLK, fontFace: FONT } },
  ],
  { x: TX, y: 3.80, w: TW, h: 0.62, fontSize: FS, align: "left", valign: "top", margin: 0 }
);

// ---------------- graphed: native plot approximation replaced by the
// generated graph image (build/assets/graphs/s018_graph_v1.png; 300dpi, baked
// container border + axes + fits; placed at the original frame's measured
// region, 1px = 1pt). Everything else is byte-identical to the certified build.
s.addImage({ path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s018_graph_v1.png",
               x: 7.66667, y: 1.81944, w: 4.44444, h: 2.59722 });

// ---------- Lesson/guideline band (full content-box width, BELOW the plots) ----------
const LX = 1.78, LW = 9.95;   // band x/width (to ~11.73)

// Lesson line 1 — single line; 'Lesson:' bold black, 'Simple models' maroon,
// 'preferred' bold underlined black
s.addText(
  [
    { text: "Lesson: ", options: { color: BLK, fontFace: FONT, bold: true } },
    { text: "Simple models", options: { color: DARKRED, fontFace: FONT } },
    { text: " should be ", options: { color: BLK, fontFace: FONT } },
    { text: "preferred", options: { color: BLK, fontFace: FONT, bold: true, underline: true } },
    { text: " over complicated models", options: { color: BLK, fontFace: FONT } },
  ],
  { x: LX, y: 4.62, w: LW, h: 0.4, fontSize: FS, align: "left", valign: "top", margin: 0 }
);

// Lesson line 2 — 'can prevent overfitting' hyperlink-blue underlined (judge fix)
s.addText(
  [
    { text: "Simple models ", options: { color: BLK, fontFace: FONT } },
    { text: "can prevent overfitting", options: { color: BLU, fontFace: FONT, underline: true } },
  ],
  { x: LX, y: 5.16, w: LW, h: 0.4, fontSize: FS, align: "left", valign: "top", margin: 0 }
);

// Lesson line 3 — 'Too simple a model' + 'underfit' underlined (black, matched)
s.addText(
  [
    { text: "Too simple a model", options: { color: BLK, fontFace: FONT, underline: true } },
    { text: " can ", options: { color: BLK, fontFace: FONT } },
    { text: "underfit", options: { color: BLK, fontFace: FONT, underline: true } },
    { text: " (e.g., M = 0 above)", options: { color: BLK, fontFace: FONT } },
  ],
  { x: LX, y: 5.70, w: LW, h: 0.4, fontSize: FS, align: "left", valign: "top", margin: 0 }
);

// Lesson line 4 — 'General guideline:' bold dark red; 'not-too-simple...' blue underlined
s.addText(
  [
    { text: "General guideline: ", options: { color: DARKRED, fontFace: FONT, bold: true } },
    { text: "Choose a model ", options: { color: BLK, fontFace: FONT } },
    { text: "not-too-simple, yet not-too-complex",
      options: { color: BLU, fontFace: FONT, underline: true } },
  ],
  { x: LX, y: 6.24, w: LW, h: 0.45, fontSize: FS, align: "left", valign: "top", margin: 0 }
);

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_018_recreated.pptx" })
  .then(() => console.log("done"));
