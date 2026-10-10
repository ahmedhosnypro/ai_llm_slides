const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const WHITE = "FFFFFF", GRAY = "E8E8E8", RED = "C00000", BLACK = "000000",
      BLUE = "2222C0", YELLOW = "FFFF66", PURPLE = "9933CC", INK = "333333",
      MAROON = "660000", BADGE_YELLOW = "FFF9C4";
const FONT = "Arial";
const DOT = "\u2022  "; // round bullet glyph (spec: six round black dots)

let s = pptx.addSlide();
s.background = { color: GRAY };

// HOUSE FRAME (founder directive 2026-10-09): outer red frame, 0.15in inset
// from every edge, line C00000 width 1.5, no visible fill (gray E8E8E8).
// Replaces the old per-slide gray panel (0.77,0.62,11.78,6.86 maroon outline).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: GRAY }, line: { color: RED, width: 1.5 },
});

// 1. Title: HOUSE FRAME text box starts y:0.28, x:0.6, w:12.13, align center
s.addText("Major Machine Learning Paradigms", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.7, align: "center", valign: "middle",
  fontSize: 35, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. HOUSE FRAME slide-number badge: oval x:12.48 y:0.30 w:0.5 h:0.5,
//    fill FFF9C4, line FFF9C4 width 0.5; digit = slide id "8", bold 18pt, 333333.
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("8", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// 3. Content frame: red rectangle with WHITE interior, widened per judge attempt 5
//    (original: white box nearly spans the slide width, small gray side gutters)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.99, w: 12.33, h: 5.26,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// 5. Nomenclature line (mixed-color runs, double space kept verbatim), ~25pt
s.addText([
  { text: "Nomenclature: ", options: { bold: true, color: BLACK } },
  { text: "x", options: { bold: true, color: RED } },
  { text: " denotes an ", options: { color: BLACK } },
  { text: "input,", options: { color: RED } },
  { text: " y", options: { bold: true, color: BLUE } },
  { text: " denotes  output/label/prediction", options: { color: BLUE } },
], {
  x: 1.2, y: 2.22, w: 11.4, h: 0.5, align: "left", valign: "middle",
  fontSize: 25, fontFace: FONT, margin: 0,
});

// 6. Section [1] header, ~25pt bold
s.addText([
  { text: "[1]  ", options: { color: BLACK } },
  { text: "Supervised Learning:", options: { color: RED } },
  { text: " learning with a teacher", options: { color: BLACK } },
], {
  x: 1.2, y: 2.815, w: 11.4, h: 0.45, align: "left", valign: "middle",
  fontSize: 25, bold: true, fontFace: FONT, margin: 0,
});

// Bullets: 20pt, text starts ~2.36in, round dot prefix
const bulletBox = { x: 2.15, w: 10.1, h: 0.42, align: "left", valign: "middle",
  fontSize: 20, color: BLACK, fontFace: FONT, margin: 0 };

// 7. Bullet 1a — subscripts via subscript runs
s.addText([
  { text: DOT + "Given: N labeled training examples {(x" },
  { text: "1", options: { subscript: true } },
  { text: " , y" },
  { text: "1", options: { subscript: true } },
  { text: " ), . . . , (x" },
  { text: "N", options: { subscript: true } },
  { text: " , y" },
  { text: "N", options: { subscript: true } },
  { text: " )}" },
], Object.assign({ y: 3.3 }, bulletBox));

// 8. Bullet 1b — 'f' as larger bold-italic glyph
s.addText([
  { text: DOT + "Goal: learn mapping " },
  { text: "f", options: { bold: true, italic: true, fontSize: 22 } },
  { text: " that predicts label y for a test example x" },
], Object.assign({ y: 3.83 }, bulletBox));

// 9. Bullet 1c
s.addText(DOT + "Example: Spam classification, webpage categorization",
  Object.assign({ y: 4.3 }, bulletBox));

// 10. Section [2] header
s.addText([
  { text: "[2]  ", options: { color: BLACK } },
  { text: "Unsupervised Learning:", options: { color: RED } },
  { text: " learning without a teacher", options: { color: BLACK } },
], {
  x: 1.2, y: 4.825, w: 11.4, h: 0.45, align: "left", valign: "middle",
  fontSize: 25, bold: true, fontFace: FONT, margin: 0,
});

// 11. Bullet 2a — subscripts
s.addText([
  { text: DOT + "Given: a set of N unlabeled inputs {x" },
  { text: "1", options: { subscript: true } },
  { text: " , . . . , x" },
  { text: "N", options: { subscript: true } },
  { text: " }" },
], Object.assign({ y: 5.29 }, bulletBox));

// 12. Bullet 2b
s.addText(DOT + "Goal: learn some intrinsic structure in the inputs (e.g., groups/clusters)",
  Object.assign({ y: 5.76 }, bulletBox));

// 13. Bullet 2c
s.addText(DOT + "Example: Automatically grouping news stories (Google News)",
  Object.assign({ y: 6.165 }, bulletBox));

// Multi-video layout: write into the ml-intro namespace (run from project root).
pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_008_recreated.pptx" })
  .then(() => console.log("done"));
