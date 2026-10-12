// Slide 040 recreation — "K -Nearest Neighbor (K -NN)" — fresh build
// Spec: videos/ml-intro/analysis/slide_040_final.json (PASS_WITH_FIXES, score 9)
//
// NOTE: an earlier pre-curation build of this file was "Feature Extraction" (old
// root-level slide_040, original numeral 32) — stale for the curated deck. That
// attempt's provenance stays banked in qa/slide040/; this script is the fresh
// build for the curated new slide 40 (old id 52), original numeral 40.
//
// HOUSE FRAME RULE (founder, 2026-10-09) — overrides spec/judge for these elements:
//   bg E8E8E8; outer frame rect x:0.15 y:0.15 w:13.03 h:7.2, line C00000 w1.5, fill E8E8E8;
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5, fill FFF9C4 line FFF9C4 w0.5, numeral "40"
//   (number printed on the original slide image; no zero-padding) bold 18pt 333333;
//   title text box starts y:0.28, x:0.6, w:12.13, align center.
//   (Spec badge #FFFF99/#333333 and spec outer-frame #AA2222 lose to the house values.)
//
// BULLET IMPLEMENTATION (pptxgenjs 4.0.1 bug workaround, prior-worker lineage):
//   no `bullet` options anywhere — bullets are manual "• " / "– " glyphs, one text
//   box per line. Runs inside a paragraph carry no paragraph-level options.
//
// VERBATIM content honored: title keeps "K -Nearest" spacing; bullet 1 keeps
// ". . ." spaced ellipsis and the spaced subscript punctuation "(x₁ , y₁ )";
// "Parameter K :" keeps the space before the colon. True subscripts rendered
// via run-level `subscript: true` per recreation_brief step 6.
// Scatter diagram (recreation_brief step 8): black axes, no labels/ticks; red
// cluster upper-left #CC0000, blue/purple upper-right #3333CC, green lower-center
// #33CC66, each inside a gray #999999 freeform-style outline; black star5 test
// point between the red and green clusters, closer to red.

const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// Palette — spec colors, hex WITHOUT leading '#'
const BG = "E8E8E8";            // house slide background
const HOUSE_RED = "C00000";     // house outer frame
const TITLE_RED = "B00020";     // spec: title text + bold red lead-ins
const BOX_RED = "AA2222";       // spec: content-box border
const TEXT = "000000";
const LINK_BLUE = "0000CC";    // spec: underlined hyperlink-style words
const BADGE = "FFF9C4";         // house badge fill/line
const INK = "333333";           // badge numeral
const WHITE = "FFFFFF";
const RED_DOT = "CC0000";
const BLUE_DOT = "3333CC";
const GREEN_DOT = "33CC66";
const GRAY = "999999";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE outer frame: red rectangle, 0.15in inset from every edge ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: HOUSE_RED, width: 1.5 },
});

// ---- Content box (spec region: ~7-93% width, ~25-95% height, thin #AA2222 border) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.933, y: 1.875, w: 11.464, h: 5.25,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 1.25 },
});

// ---- HOUSE title text box (y:0.28, x:0.6, w:12.13, centered); color per spec ----
s.addText("K -Nearest Neighbor (K -NN)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "middle",
  fontSize: 30, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ---- HOUSE slide-number badge — numeral "40" ----
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("40", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Bullet 1 (verbatim incl. ". . ." and spaced subscript punctuation) ----
// "• Given: training data D = {(x₁ , y₁ ), . . . , (x_N , y_N )} and a test point"
s.addText(
  [
    { text: "• ", options: { color: TEXT } },
    { text: "Given:", options: { bold: true, color: TITLE_RED } },
    { text: " training data D = {(x", options: { color: TEXT } },
    { text: "1", options: { color: TEXT, subscript: true } },
    { text: " , y", options: { color: TEXT } },
    { text: "1", options: { color: TEXT, subscript: true } },
    { text: " ), . . . , (x", options: { color: TEXT } },
    { text: "N", options: { color: TEXT, subscript: true } },
    { text: " , y", options: { color: TEXT } },
    { text: "N", options: { color: TEXT, subscript: true } },
    { text: " )} and a test point", options: { color: TEXT } },
  ],
  {
    x: 1.45, y: 2.10, w: 10.4, h: 0.42, align: "left", valign: "middle",
    fontSize: 18, fontFace: FONT, margin: 0,
  }
);

// ---- Bullet 2 ----
// "• Prediction Rule: Look at the K most similar training examples"
s.addText(
  [
    { text: "• ", options: { color: TEXT } },
    { text: "Prediction Rule:", options: { bold: true, color: TITLE_RED } },
    { text: " Look at the K most similar training examples", options: { color: TEXT } },
  ],
  {
    x: 1.45, y: 2.62, w: 10.4, h: 0.42, align: "left", valign: "middle",
    fontSize: 18, fontFace: FONT, margin: 0,
  }
);

// ---- Scatter diagram (recreation_brief step 8), centered in the content box ----
// Plot band: x 5.15..8.15, y 3.25..4.90. Axes: black, no labels/ticks.
const AX = 5.20, AX_END = 8.05, AY_TOP = 3.35, AY = 4.80; // axis lines
s.addShape(pptx.shapes.LINE, {
  x: AX, y: AY_TOP, w: 0, h: AY - AY_TOP,
  line: { color: TEXT, width: 1.5 },
});
s.addShape(pptx.shapes.LINE, {
  x: AX, y: AY, w: AX_END - AX, h: 0,
  line: { color: TEXT, width: 1.5 },
});

// Dot helper: small filled circle centered at (cx, cy)
const D = 0.09;
function dot(cx, cy, color) {
  s.addShape(pptx.shapes.OVAL, {
    x: cx - D / 2, y: cy - D / 2, w: D, h: D,
    fill: { color }, line: { color, width: 0.25 },
  });
}

// Gray hand-drawn-style cluster outlines (no fill)
function outline(x, y, w, h) {
  s.addShape(pptx.shapes.OVAL, {
    x, y, w, h, fill: { type: "none" }, line: { color: GRAY, width: 1.25 },
  });
}

// Red cluster, upper-left (enclosed by gray outline)
outline(5.48, 3.50, 0.68, 0.80);
[[5.72, 3.72], [5.98, 3.68], [5.62, 3.95], [5.88, 3.92], [6.02, 3.85], [5.70, 4.12], [5.92, 4.06]]
  .forEach(([cx, cy]) => dot(cx, cy, RED_DOT));

// Blue/purple cluster, upper-right
outline(7.10, 3.48, 0.68, 0.80);
[[7.36, 3.70], [7.62, 3.66], [7.28, 3.93], [7.54, 3.90], [7.66, 3.82], [7.34, 4.10], [7.58, 4.04]]
  .forEach(([cx, cy]) => dot(cx, cy, BLUE_DOT));

// Green cluster, lower-center
outline(6.30, 4.22, 0.68, 0.66);
[[6.52, 4.36], [6.78, 4.32], [6.44, 4.55], [6.70, 4.52], [6.84, 4.44], [6.56, 4.68], [6.76, 4.62]]
  .forEach(([cx, cy]) => dot(cx, cy, GREEN_DOT));

// Black star test point: between red and green clusters, closer to red
s.addShape(pptx.shapes.STAR_5_POINT, {
  x: 6.14, y: 4.18, w: 0.22, h: 0.22,
  fill: { color: TEXT }, line: { color: TEXT, width: 0.5 },
});

// ---- Sub-bullet: classification (blue underlined hyperlink-style words) ----
s.addText(
  [
    { text: "– For ", options: { color: TEXT } },
    { text: "classification", options: { color: LINK_BLUE, underline: true } },
    { text: ": assign the majority class label (", options: { color: TEXT } },
    { text: "majority voting", options: { color: LINK_BLUE, underline: true } },
    { text: ")", options: { color: TEXT } },
  ],
  {
    x: 1.75, y: 5.10, w: 10.1, h: 0.42, align: "left", valign: "middle",
    fontSize: 18, fontFace: FONT, margin: 0,
  }
);

// ---- Sub-bullet: regression ----
s.addText(
  [
    { text: "– For ", options: { color: TEXT } },
    { text: "regression", options: { color: LINK_BLUE, underline: true } },
    { text: ": assign the average response", options: { color: TEXT } },
  ],
  {
    x: 1.75, y: 5.55, w: 10.1, h: 0.42, align: "left", valign: "middle",
    fontSize: 18, fontFace: FONT, margin: 0,
  }
);

// ---- Bullet 3 ----
s.addText("• The algorithm requires:", {
  x: 1.45, y: 6.02, w: 10.4, h: 0.42, align: "left", valign: "middle",
  fontSize: 18, color: TEXT, fontFace: FONT, margin: 0,
});

// ---- Bottom sub-bullet: "– Parameter K : number of nearest neighbors to look for" ----
s.addText(
  [
    { text: "– ", options: { color: TEXT } },
    { text: "Parameter K", options: { bold: true, color: TITLE_RED } },
    { text: " : number of nearest neighbors to look for", options: { color: TEXT } },
  ],
  {
    x: 1.75, y: 6.47, w: 10.1, h: 0.42, align: "left", valign: "middle",
    fontSize: 18, fontFace: FONT, margin: 0,
  }
);

pptx.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/ml-intro/recreated_pptx/slide_040_recreated.pptx" })
  .then(() => console.log("done"));
