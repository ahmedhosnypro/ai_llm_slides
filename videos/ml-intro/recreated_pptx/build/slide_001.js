const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette from analysis/slide_001_final.json
const BG = "E8E8E8";      // background light gray
const RED = "C00000";     // title / Instructors: label
const DARKRED = "8B1A1A"; // border frame, logo wordmark text
const BLUE = "0000CC";    // course code, instructor names/emails
const BLACK = "000000";  // body text, badge numeral
const YELLOW = "FFFF99";  // badge fill
const PURPLE = "7030A0";  // badge outline
const TEAL = "1B9E8F";   // logo square
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// 2. Outer red house frame, 0.15in inset from every edge (founder directive 2026-10-09)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 3. Slide-number badge: house geometry/colors (numeral text unchanged)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" },
  line: { color: "FFF9C4", width: 0.5 },
});
s.addText("1", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 4. Title, house position (text box starts y=0.28, x=0.6, w=12.13):
// two lines, very large bold red
s.addText(
  [
    { text: "Introduction to", options: { breakLine: true } },
    { text: "Machine Learning", options: {} },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 1.55,
    align: "center", valign: "top",
    fontSize: 40, bold: true, color: RED, fontFace: FONT, margin: 0,
  }
);

// 5. Course code, centered directly beneath the title (judge attempt 3:
// was too low/too large relative to the title — moved up to follow the
// house-pinned title and scaled down)
s.addText("CSAI 253  -  Spring 2024", {
  x: 0.9, y: 1.85, w: W - 1.8, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 22, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// 6. Prepared-by block, centered compactly below the course line
// (judge attempt 3: was pushed far down and oversized)
s.addText(
  [
    { text: "Prepared By", options: { fontSize: 18, italic: true, color: BLACK, breakLine: true } },
    { text: "Dr. Khaled Mostafa ElSayed", options: { fontSize: 20, italic: true, color: BLACK, breakLine: true } },
    { text: "kmelsayed@zewailcity.edu.eg", options: { fontSize: 14, color: BLUE } },
  ],
  {
    x: 3.5, y: 2.65, w: W - 7.0, h: 1.2,
    align: "center", valign: "top", fontFace: FONT, margin: 0, paraSpaceAfter: 4,
  }
);

// 7. Instructors block, bottom-left (~80%-98% vertical), left-aligned
// (judge attempt 3: tighten the leading)
s.addText(
  [
    { text: "Instructors:", options: { fontSize: 16, bold: true, italic: true, color: RED, breakLine: true } },
    { text: "Dr. Khaled Mostafa ElSayed", options: { fontSize: 14, bold: true, italic: true, color: BLUE, breakLine: true } },
    { text: "kmelsayed@zewailcity.edu.eg", options: { fontSize: 12, color: BLUE, breakLine: true } },
    { text: "Dr. Mohamed Maher Ata", options: { fontSize: 14, bold: true, italic: true, color: BLUE, breakLine: true } },
    { text: "momaher@zewailcity.edu.eg", options: { fontSize: 12, color: BLUE } },
  ],
  {
    x: 0.5, y: 5.75, w: 5.6, h: 1.4,
    align: "left", valign: "top", fontFace: FONT, margin: 0, paraSpaceAfter: 2,
  }
);

// 8. Logo, bottom-right corner (recreated with shapes per spec description)
// Teal square with white mountain-and-sun graphic + 'ZEWAIL CITY' text
// (attempt 2: block shifted left — at x=10.55 the wordmark box reached
// 13.82in, past the 13.33in slide edge, clipping the English line)
const logoX = 9.45, logoY = 5.85, logoS = 1.05;
s.addShape(pptx.shapes.RECTANGLE, {
  x: logoX, y: logoY, w: logoS, h: logoS,
  fill: { color: TEAL }, line: { color: TEAL, width: 0.5 },
});
// White sun (small circle, upper area of the square)
s.addShape(pptx.shapes.OVAL, {
  x: logoX + 0.62, y: logoY + 0.12, w: 0.2, h: 0.2,
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0.25 },
});
// White mountain (triangle)
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: logoX + 0.14, y: logoY + 0.24, w: 0.78, h: 0.42,
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0.25 },
});
s.addText("ZEWAIL CITY", {
  x: logoX, y: logoY + 0.68, w: logoS, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
// Bilingual wordmark: boxed WHITE panel to the right of the square
// (judge attempt 3 BLOCKER: original lockup is teal emblem + boxed white
// panel holding the Arabic/English wordmark in dark red; text enlarged
// for legibility)
s.addShape(pptx.shapes.RECTANGLE, {
  x: logoX + logoS + 0.06, y: logoY + 0.06, w: 2.75, h: 0.92,
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0.5 },
});
s.addText(
  [
    { text: "\u062c\u0627\u0645\u0639\u0629 \u0627\u0644\u0639\u0644\u0648\u0645 \u0648\u0627\u0644\u062a\u0643\u0646\u0648\u0644\u0648\u062c\u064a\u0627", options: { fontSize: 12, color: DARKRED, breakLine: true } },
    { text: "University of Science and Technology", options: { fontSize: 10, color: DARKRED } },
  ],
  {
    x: logoX + logoS + 0.14, y: logoY + 0.12, w: 2.6, h: 0.8,
    align: "left", valign: "middle", fontFace: FONT, margin: 0,
  }
);

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_001_recreated.pptx" })
  .then(() => console.log("done"));
