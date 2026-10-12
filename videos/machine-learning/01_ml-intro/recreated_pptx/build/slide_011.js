const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

const BG = "E8E8E8";      // house-template background (founder rule 2026-10-09)
const RED = "C00000";     // title, section headers, borders
const TEXT = "000000";    // body text
const WHITE = "FFFFFF";   // content box fill
const BADGE_YELLOW = "FFF9C4"; // house-template badge fill (founder rule)
const INK = "333333";     // house-template badge digit color (founder rule)
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE FRAME (founder directive 2026-10-09 — overrides spec JSON):
// outer red frame = rectangle 0.15in inset from every edge, line C00000 width 1.5,
// no visible fill over background E8E8E8
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// HOUSE FRAME: title text box starts y:0.28, x:0.6, w:12.13, align center
s.addText("Supervised Learning", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.15, align: "center", valign: "middle",
  fontSize: 40, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// HOUSE FRAME: slide-number badge = oval x:12.48 y:0.30 w:0.5 h:0.5,
// fill FFF9C4 line FFF9C4, slide's own number centered, bold 18pt, color 333333
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("11", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Content box: white fill, thin red border, x 8-95% width, y 25-95% height
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.07, y: 1.88, w: 11.6, h: 5.24,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// Body text, left-aligned, black, inside the content box
const blank = { text: " ", options: { breakLine: true } };
// Build line 1 explicitly (keep the two spaces before the brace)
const line1 = [
  { text: "f", options: { italic: true } },
  { text: " : ", options: {} },
  { text: "x", options: { italic: true } },
  { text: " \u2192 ", options: {} },
  { text: "y", options: { italic: true } },
  { text: "  { ", options: {} },
  { text: "f", options: { italic: true } },
  { text: " is a function from ", options: {} },
  { text: "X", options: { italic: true } },
  { text: " to ", options: {} },
  { text: "Y", options: { italic: true } },
  { text: " }", options: { breakLine: true } },
];
const line3 = [
  { text: "y", options: { bold: true, italic: true } },
  { text: " is a discrete variable", options: { breakLine: true } },
];
const line4 = [
  { text: "Discrete variable: takes a value from a discrete set ", options: {} },
  { text: "y", options: { italic: true } },
  { text: " \u2208 {1, . . . , ", options: {} },
  { text: "K", options: { italic: true } },
  { text: " }", options: { breakLine: true } },
];
const line5 = [
  { text: "Example:", options: { bold: true } },
  { text: " Category of a web page (sports, politics, business, science, etc.)", options: { breakLine: true } },
];
const line7 = [
  { text: "y", options: { bold: true, italic: true } },
  { text: " is a real-valued variable", options: { breakLine: true } },
];
const line8 = [
  { text: "Example:", options: { bold: true } },
  { text: " Price of a stock", options: {} },
];

const body = [].concat(
  line1,
  [blank],
  [{ text: "Classification:", options: { color: RED, underline: true, breakLine: true } }],
  line3,
  line4,
  line5,
  [blank],
  [{ text: "Regression:", options: { color: RED, underline: true, breakLine: true } }],
  line7,
  line8
);

s.addText(body, {
  x: 1.45, y: 2.15, w: 10.9, h: 4.75,
  align: "left", valign: "top",
  fontSize: 22, color: TEXT, fontFace: FONT, margin: 0,
  paraSpaceAfter: 6,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_011_recreated.pptx" })
  .then(() => console.log("written: videos/ml-intro/recreated_pptx/slide_011_recreated.pptx"));
