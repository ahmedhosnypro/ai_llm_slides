// Slide 039 recreation — "Nearest Neighbor (NN) and K -Nearest Neighbor (K -NN)"
// Spec: videos/ml-intro/analysis/slide_039_final.json (validated PASS_WITH_FIXES, score 8)
// Output: videos/ml-intro/recreated_pptx/slide_039_recreated.pptx
//
// HOUSE FRAME RULE (founder, 2026-10-09) — overrides spec/judge for these elements:
//   bg E8E8E8; outer frame rect x:0.15 y:0.15 w:13.03 h:7.2, line C00000 w1.5, fill E8E8E8;
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5, fill FFF9C4 line FFF9C4 w0.5, numeral "39"
//   (slide id, no zero-padding — fresh spec labels confirm the original prints "39")
//   bold 18pt 333333; title text box starts y:0.28, x:0.6, w:12.13, align center.
//
// Title-box handling (slide_029 precedent, same structural case: title-only slide
// whose 3-line title sits centered inside the spec's white inner box): the house
// title text box is given the house geometry and made tall with valign:middle, so
// the three rendered lines land centered inside the white content box as in the
// original. The spec's outer gray panel is replaced by the house chrome.
//
// VERBATIM content rules honored: 'K -Nearest' / 'K -NN' keep the extracted space
// after 'K' (likely OCR artifact, kept per spec uncertain_items).

const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette (spec + house) — NO '#' prefixes (corrupts the file)
const BG = "E8E8E8";      // house background / spec colors.background
const FRAME = "C00000";    // house frame line
const BOXLINE = "B03030"; // spec: thin red/maroon border of the inner white box
const WHITE = "FFFFFF";   // spec: inner box fill
const BLUE = "0000CC";    // spec: title line 1
const BLACK = "000000";   // spec: 'and'
const TITLE_RED = "CC0000"; // spec: title line 3
const BADGE = "FFF9C4";   // house badge fill/line
const INK = "333333";      // badge numeral
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE outer chrome ----
// Outer red frame: rectangle, 0.15in inset from every edge, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});

// Slide-number badge: yellow oval top-right, numeral = slide id "39"
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("39", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Spec content: inner white title box, thin red/maroon border ----
// Spec geometry: x 7%-92% of width, y 28%-85% of height.
const boxX = 0.07 * W;          // 0.93 in
const boxY = 0.28 * H;          // 2.10 in
const boxW = (0.92 - 0.07) * W; // 11.33 in
const boxH = (0.85 - 0.28) * H; // 4.28 in
s.addShape(pptx.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { color: WHITE }, line: { color: BOXLINE, width: 1.5 },
});

// ---- Title: house text-box geometry (starts y:0.28, x:0.6, w:12.13, centered) ----
// Tall box + valign middle so the three lines sit centered inside the white box
// exactly as in the original (slide_029 precedent).
// Judge attempt 3 (MAJOR): lines under-scaled — measured 44.1% (blue) / 55% (red)
// of frame width vs the original's ~60% / ~70%. Calibrated: blue 52pt, red 51pt
// => predicted ~60% / ~70%. 'and' kept at the approved 0.65 ratio (34pt), line
// pitch scaled to 78pt.
// Judge attempt 3 (MINOR): original shows a conspicuously enlarged gap between
// 'Neighbor' and '(NN)' — widened to 3 spaces (~3x a normal interword gap).
s.addText(
  [
    { text: "Nearest Neighbor   (NN)", options: { fontSize: 52, bold: true, color: BLUE, breakLine: true } },
    { text: "and", options: { fontSize: 34, bold: false, color: BLACK, breakLine: true } },
    { text: "K -Nearest Neighbor (K -NN)", options: { fontSize: 51, bold: true, color: TITLE_RED } },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 7.5,
    align: "center", valign: "middle",
    fontFace: FONT, margin: 0, lineSpacing: 78,
  }
);

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_039_recreated.pptx" })
  .then(() => console.log("done"));
