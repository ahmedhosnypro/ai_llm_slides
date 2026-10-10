// Slide 034 recreation — "Classification"
// Spec: videos/ml-intro/analysis/slide_034_final.json (validated). House chrome per
// founder directive 2026-10-09 overrides spec frame/badge/title geometry.
// Started from build/slide_043.js (old pre-curation id 43); badge numeral 34.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", FRAME_RED = "C00000", RED = "C00000",
      ARROW_RED = "CC0000", SUB_RED = "C00000", TEXT = "000000",
      WHITE = "FFFFFF", BADGE_YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE CHROME (overrides spec) ----
// Outer red frame, 0.15in inset from every edge
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// Slide-number badge: yellow oval top-right, numeral exactly "34"
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("34", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Title: centered text box, y 0.28 (house geometry; house style red bold)
s.addText("Classification", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- CONTENT (per spec) ----
// White content area with thin red border (~5-95% width, below title zone)
const boxX = 0.9, boxY = 1.7, boxW = 11.53, boxH = 5.4;
s.addShape(pptx.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { color: WHITE }, line: { color: ARROW_RED, width: 1.5 },
});

// Subtitle: red, italic
s.addText("Classification Techniques are based on Data separability nature", {
  x: 1.4, y: 2.05, w: 10.0, h: 0.45, align: "left", valign: "top",
  fontSize: 20, italic: true, color: SUB_RED, fontFace: FONT, margin: 0,
});

// Intro sentence, black with "data can be classified into" bolded.
// Multi-run paragraph, NO bullet options (pptxgenjs bullet bug workaround).
s.addText([
  { text: "From the separability point of view ", options: { color: TEXT } },
  { text: "data can be classified into", options: { color: TEXT, bold: true } },
  { text: " :", options: { color: TEXT } },
], {
  x: 1.4, y: 2.7, w: 10.0, h: 0.45, align: "left", valign: "top",
  fontSize: 20, fontFace: FONT, margin: 0,
});

// Three bullet rows: manual "•" glyph, one text box per line, red block
// arrow, parenthesized note. Row band ~40-70% of slide height.
const BODY = 20, LINE_H = 0.45;
const rows = [
  { bullet: "Linearly Separable",       note: "(Use Linear classifier)" },
  { bullet: "Non-Linearly Separable",   note: "(Use Non-Linear classifier)" },
  { bullet: "Non-Separable",            note: "(Use Kernels with Classifiers)" },
];
const rowY = [3.6, 4.6, 5.6];
rows.forEach((r, i) => {
  const y = rowY[i];
  // manual bullet glyph
  s.addText("\u2022", {
    x: 1.4, y, w: 0.35, h: LINE_H, align: "left", valign: "top",
    fontSize: BODY, color: TEXT, fontFace: FONT, margin: 0,
  });
  // bullet label
  s.addText(r.bullet, {
    x: 1.75, y, w: 3.6, h: LINE_H, align: "left", valign: "top",
    fontSize: BODY, color: TEXT, fontFace: FONT, margin: 0,
  });
  // thick red right-pointing block arrow
  s.addShape(pptx.shapes.RIGHT_ARROW, {
    x: 5.55, y: y + 0.02, w: 1.7, h: 0.38,
    fill: { color: ARROW_RED }, line: { color: ARROW_RED, width: 0.75 },
  });
  // parenthesized note
  s.addText(r.note, {
    x: 7.55, y, w: 4.6, h: LINE_H, align: "left", valign: "top",
    fontSize: BODY, color: TEXT, fontFace: FONT, margin: 0,
  });
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_034_recreated.pptx" })
  .then(() => console.log("done"));
