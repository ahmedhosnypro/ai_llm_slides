// Slide 58 recreation — "K-Nearest Neighbor: Properties" — attempt 1
// Spec: videos/ml-intro/analysis/slide_058_final.json (validated PASS_WITH_FIXES,
// score 8; staged from old deck slide_091_final.json — byte-identical, same image).
// House chrome (founder directive 2026-10-09 — overrides spec AND judge):
//   bg E8E8E8; red frame x:0.15 y:0.15 w:13.03 h:7.2 line C00000 w1.5;
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill/line FFF9C4, numeral "58"
//   (the number printed on the original slide image) bold 18pt 333333;
//   title box y:0.28 x:0.6 w:12.13 centered.
// pptxgenjs bullet-bug workaround: manual "• " / "– " glyphs, one text box
// per line, NO bullet options anywhere.
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", RED = "C00000", BADGE = "FFF9C4", INK = "333333";
const BODY = "000000", GRAY = "808080", BLUE = "1F3864";
const FONT = "Arial", HAND = "Comic Sans MS";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE outer red frame ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});

// ---- HOUSE slide-number badge: numeral is the number printed on the
// original slide image ("58") ----
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("58", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- HOUSE title box (y:0.28, x:0.6, w:12.13, centered) ----
// Original title: red bold, top ~5-15% height.
s.addText("K -Nearest Neighbor: Properties", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.85,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- Content box (measured from original pixels): thin red border INSET
// from the slide edges — left 0.97, right 12.29, top 1.94, bottom 7.24 —
// with visible bg margins outside the box. No fill (bg shows through).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.97, y: 1.94, w: 11.32, h: 5.30,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});

// ---- Left ~65% column: two bulleted sections (verbatim text) ----
const LX = 1.25, LW = 8.0;

// Section header 1
s.addText("What\u2019s nice", {
  x: LX, y: 2.25, w: LW, h: 0.35,
  fontSize: 18, bold: true, color: BODY, fontFace: FONT, margin: 0,
});
// Bullet: black with "easily implementable" bold red (multi-run, no bullet opts)
s.addText([
  { text: "\u2022 Simple and intuitive; ", options: { color: BODY } },
  { text: "easily implementable", options: { color: RED, bold: true } },
], {
  x: LX, y: 2.66, w: LW, h: 0.32,
  fontSize: 16, color: BODY, fontFace: FONT, margin: 0,
});
s.addText("\u2022 K -NN approaches the best possible classifier (Bayes optimal)", {
  x: LX, y: 3.04, w: LW, h: 0.32,
  fontSize: 16, color: BODY, fontFace: FONT, margin: 0,
});

// Section header 2
s.addText("What\u2019s not so nice..", {
  x: LX, y: 3.54, w: LW, h: 0.35,
  fontSize: 18, bold: true, color: BODY, fontFace: FONT, margin: 0,
});
// Main bullet — bold red (whole bullet, per recreation_brief step 9)
s.addText("\u2022 Store all the training data in memory even at test time", {
  x: LX, y: 3.95, w: LW, h: 0.32,
  fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// Three dash sub-bullets — smaller gray (808080)
s.addText("\u2013 Can be memory intensive for large training datasets", {
  x: LX + 0.3, y: 4.37, w: LW - 0.3, h: 0.27,
  fontSize: 13, color: GRAY, fontFace: FONT, margin: 0,
});
s.addText("\u2013 An example of non-parametric, or memory/instance-based methods", {
  x: LX + 0.3, y: 4.65, w: LW - 0.3, h: 0.27,
  fontSize: 13, color: GRAY, fontFace: FONT, margin: 0,
});
s.addText("\u2013 Different from parametric, model-based learning models", {
  x: LX + 0.3, y: 4.93, w: LW - 0.3, h: 0.27,
  fontSize: 13, color: GRAY, fontFace: FONT, margin: 0,
});
// Main bullet — bold red
s.addText("\u2022 Expensive at test time: O(ND) computations for each test point", {
  x: LX, y: 5.35, w: LW, h: 0.32,
  fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// Two dash sub-bullets
s.addText("\u2013 Have to search through all training data to find nearest neighbors", {
  x: LX + 0.3, y: 5.77, w: LW - 0.3, h: 0.27,
  fontSize: 13, color: GRAY, fontFace: FONT, margin: 0,
});
s.addText("\u2013 Distance computations with N training points (D features each)", {
  x: LX + 0.3, y: 6.05, w: LW - 0.3, h: 0.27,
  fontSize: 13, color: GRAY, fontFace: FONT, margin: 0,
});
// Two final main bullets — bold red
s.addText("\u2022 Sensitive to noisy features", {
  x: LX, y: 6.47, w: LW, h: 0.32,
  fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("\u2022 May perform badly in high dimensions (curse of dimensionality)", {
  x: LX, y: 6.85, w: LW, h: 0.32,
  fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- Right ~35% column of the content box: intentionally EMPTY.
// The current ground-truth frame has NO sketch there (the dark-blue ink
// annotation appears only in later frames of this slide group); the only
// thing in that region of the original is a video mouse-capture artifact,
// which must NOT be recreated.

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_058_recreated.pptx" })
  .then(() => console.log("done"));
