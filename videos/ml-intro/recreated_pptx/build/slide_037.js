const pptxgenpkg = require("pptxgenjs");

// Build: slide 037 recreation — "Main Classification Learning Approaches"
// Spec: videos/ml-intro/analysis/slide_037_final.json (validated PASS_WITH_FIXES, score 8/10)
// Output: videos/ml-intro/recreated_pptx/slide_037_recreated.pptx
//
// Geometry measured from unique_slides/slide_037.jpg (960x540 px == 13.33x7.5 in,
// 1 px == 1 pt). Verbatim text verified against the original pixels by OCR:
//   "Main Classification" / "Learning Approaches" (title box, white on dark red)
//   "Supervised Learning" (blue box), "Unsuepervised Learning" (green box, typo preserved)
//   "Data Labels are required for training" (exactly one caption line, left)
//   "No Need for Data Labels" / "(A.K.A Clustering)" (exactly two caption lines, right)
// Badge numeral "37" confirmed printed on the original image.
//
// House frame (founder directive 2026-10-09) overrides the outer chrome:
//   bg E8E8E8, red frame 0.15 in inset (line C00000 1.5pt), badge oval
//   12.48/0.30/0.5/0.5 FFF9C4 with numeral "37" (bold 18pt, 333333), title text
//   box starts y 0.28, x 0.6, w 12.13, centered. The original's gray header
//   strip, bottom gray band and inner double perimeter frame are outer chrome
//   superseded by the house values (same treatment as sibling slide_009).

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;
const PT = 1 / 72; // measured JPG: 1 px == 1 pt

// Palette (spec + house) — NO '#' prefixes (corrupts file)
const BG = "E8E8E8";        // slide background (house)
const RED = "C00000";       // house frame line
const TITLE_BOX = "8B0000"; // dark-red title box fill (spec)
const BLUE = "0000CC";      // supervised box fill (spec)
const GREEN = "1E8C3A";     // unsupervised box fill (spec)
const ARROW = "CC0000";     // thin red arrows (spec)
const WHITE = "FFFFFF";
const BLACK = "000000";
const BADGE_YELLOW = "FFF9C4"; // house badge fill+line
const BADGE_INK = "333333";    // badge numeral
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE FRAME: outer red frame, 0.15in inset from every edge, line C00000 1.5pt,
// no visible fill (gray E8E8E8).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// HOUSE slide-number badge: numeral "37" = the number printed on the original.
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("37", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_INK, fontFace: FONT, margin: 0,
});

// Dark-red title box (measured x 276-658pt, y 125-204pt).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 276 * PT, y: 125 * PT, w: (658 - 276) * PT, h: (204 - 125) * PT,
  fill: { color: TITLE_BOX }, line: { color: TITLE_BOX, width: 0.5 },
});

// Slide title — HOUSE text-box geometry (starts y:0.28, x:0.6, w:12.13, centered);
// tall box + valign middle places the two glyph lines at the original's measured
// position (line centers ~147.5pt / ~180pt) inside the dark-red box.
s.addText([
  { text: "Main Classification", options: { breakLine: true } },
  { text: "Learning Approaches", options: {} },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 3.94, // 0.28 .. 4.22in; block center 2.25in
  align: "center", valign: "middle",
  fontSize: 27, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  lineSpacing: 32,
});

// Left branch: blue box (measured x 107-430pt, y 284-364pt) with white bold label.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 107 * PT, y: 284 * PT, w: (430 - 107) * PT, h: (364 - 284) * PT,
  fill: { color: BLUE }, line: { color: BLUE, width: 0.5 },
});
s.addText("Supervised Learning", {
  x: 107 * PT, y: 284 * PT, w: (430 - 107) * PT, h: (364 - 284) * PT,
  align: "center", valign: "middle",
  fontSize: 23, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// Right branch: green box (measured x 524-839pt, y 284-364pt); source typo
// "Unsuepervised" preserved verbatim.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 524 * PT, y: 284 * PT, w: (839 - 524) * PT, h: (364 - 284) * PT,
  fill: { color: GREEN }, line: { color: GREEN, width: 0.5 },
});
s.addText("Unsuepervised Learning", {
  x: 524 * PT, y: 284 * PT, w: (839 - 524) * PT, h: (364 - 284) * PT,
  align: "center", valign: "middle",
  fontSize: 23, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// Two thin red curved arrows with downward arrowheads: from the bottom center of
// the title box (467pt, 204pt) to the top centers of the blue box (268pt, 284pt)
// and green box (681pt, 284pt). The left connector uses flipH so it runs
// top-right -> bottom-left; endArrowType puts the arrowhead at the child-box end.
s.addShape("curvedConnector4", {
  x: 268 * PT, y: 204 * PT, w: (467 - 268) * PT, h: (284 - 204) * PT,
  flipH: true,
  line: { color: ARROW, width: 2.5, endArrowType: "stealth" },
});
s.addShape("curvedConnector4", {
  x: 467 * PT, y: 204 * PT, w: (681 - 467) * PT, h: (284 - 204) * PT,
  line: { color: ARROW, width: 2.5, endArrowType: "stealth" },
});

// Left caption (exactly one line; measured glyph band y 392-409pt, centered on
// the blue box column): black bold 16pt.
s.addText("Data Labels are required for training", {
  x: 1.13, y: 5.38, w: 5.20, h: 0.32,
  align: "center", valign: "top",
  fontSize: 19, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Right caption (exactly two lines; measured glyph bands y 392-405 / 414-431pt,
// centered on the green box column): black bold 16pt, line pitch 22pt.
s.addText([
  { text: "No Need for Data Labels", options: { breakLine: true } },
  { text: "(A.K.A Clustering)", options: {} },
], {
  x: 524 * PT, y: 5.38, w: (839 - 524) * PT, h: 0.62,
  align: "center", valign: "top",
  fontSize: 19, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  lineSpacing: 22,
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_037_recreated.pptx" })
  .then(() => console.log("done"));
