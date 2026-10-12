// Slide 027 recreation — "Non-Numeric Data Representation" (ml-intro, new numbering; old deck id 35)
// Spec: videos/ml-intro/analysis/slide_027_final.json (validated) / slide_027_raw.json
// Geometry measured from the original frame videos/ml-intro/unique_slides/slide_027.jpg
// (960x540 px == 13.33x7.5in at 72 px/in):
//   title 2 lines (y73/114px), bullet box x70-878 y146-372px (white, rounded, red border),
//   bullets at y 162(+wrap 192), 228, 267, 307, 346px, markers x~104px,
//   legend (pale yellow) x107-245 y396-526px, left table x350-520 y388-522px,
//   arrow x549-572 y449-459px, right table x610-724 y388-522px.
// NOTE: this file previously held the pre-curation OLD slide-27 ("Reinforcement Learning")
// build; that build is preserved verbatim in qa/slide027/build_attempt_{1,2,3}.js.
// House frame rule (founder directive 2026-10-09) overrides spec for outer chrome:
//   bg E8E8E8, red frame 0.15in inset, badge oval 12.48/0.30/0.5/0.5 fill FFF9C4,
//   title box y:0.28 x:0.6 w:12.13 centered. Badge numeral reads exactly "27".
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// palette constants from the spec JSON (+ house chrome colors)
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE = "FFF9C4", INK = "333333";
const TITLE_RED = "AA0000", BLACK = "000000", WHITE = "FFFFFF";
const BLUE = "0000CC", REDIT = "CC0000", PINK = "FF99CC", ORANGE = "FFCC99",
      LGREEN = "99FF99", LEGEND_FILL = "FFFFCC", BOX_BORDER = "AA2222", ARROW_RED = "CC3333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---------- HOUSE CHROME ----------
// outer red frame, 0.15in inset, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});
// slide-number badge: yellow oval top-right, numeral exactly "27" (original printed number)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("27", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
// title: house geometry (y 0.28, x 0.6, w 12.13, centered); dark red bold per spec, two lines
s.addText([
  { text: "Non-Numeric", options: { breakLine: true } },
  { text: "Data Representation", options: {} },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 1.30, align: "center", valign: "top",
  fontSize: 35, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ---------- BULLET BOX (white rounded rect, thin red border; x70-878 y146-372 px) ----------
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.97, y: 2.03, w: 11.22, h: 3.14, rectRadius: 0.05,
  fill: { color: WHITE }, line: { color: BOX_BORDER, width: 1.25 },
});

// ---------- BULLETS (verbatim; manual dot glyphs, no pptxgenjs bullet options) ----------
const BUL = 23;                     // pt (calibrated: 20pt rendered 8.64in for b1L1 vs original 10.28in)
const TX = 1.75, TW = 10.40;        // text x/width (original text x126-866 px)
function marker(cy) {               // round dot, center x 1.44in (104px)
  s.addShape(pptx.shapes.OVAL, {
    x: 1.37, y: cy - 0.055, w: 0.14, h: 0.14, fill: { color: BLACK },
  });
}
function btext(yTop, runs, color) {
  s.addText(runs, {
    x: TX, y: yTop, w: TW, h: 0.40, align: "left", valign: "top",
    fontSize: BUL, color: color || BLACK, fontFace: FONT, margin: 0,
  });
}
// b1 — two lines, wrap reproduced exactly as the original ("…Tennis Playing" / "example)")
marker(2.35);
btext(2.20, "What if the data has a non-numeric representation (e.g. Tennis Playing");
btext(2.62, "example)");
// b2 — black
marker(3.24);
btext(3.12, "Features are nominal (Low/High, Yes/No, Overcast/Rainy/Sunny, etc.)");
// b3 — blue
marker(3.78);
btext(3.66, "Features with only 2 possible values can be represented as 0/1", BLUE);
// b4 — red italic
marker(4.33);
btext(4.21, "What about features having more than 2 possible values?", REDIT);
// b5 — bold black lead + blue italic underlined tail
marker(4.88);
btext(4.75, [
  { text: "Can't we just", options: { bold: true, color: BLACK } },
  { text: " ", options: { bold: true, color: BLACK } },
  { text: "map Sunny to 0, Overcast to 1, Rainy to 2?", options: { color: BLUE, italic: true, underline: true } },
]);

// ---------- LEGEND TABLE (bottom-left, pale yellow, no visible border; x107-245 y396-526 px) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.49, y: 5.50, w: 1.91, h: 1.81,
  fill: { color: LEGEND_FILL }, line: { color: LEGEND_FILL, width: 0.5 },
});
const LEG = 11, LX1 = 1.56, LX2 = 2.18;
function leg(yCtr, label, value) {
  s.addText(label, { x: LX1, y: yCtr - 0.11, w: 0.45, h: 0.24, align: "left", valign: "middle",
    fontSize: LEG, color: BLACK, fontFace: FONT, margin: 0 });
  s.addText(value, { x: LX2, y: yCtr - 0.11, w: 1.15, h: 0.24, align: "left", valign: "middle",
    fontSize: LEG, color: BLACK, fontFace: FONT, margin: 0 });
}
// row centers measured from the original: 403.5, 426, 465, 487.5, 510 px
leg(5.60, "P", "Play");
leg(5.92, "N", "No Play");
leg(6.46, "Out", "Outlook");
leg(6.77, "T", "Temperature");
leg(7.08, "R", "Humidity");

// ---------- DATA TABLES (bottom; colored full-height columns + black text rows) ----------
const TBL_Y = 5.39, TBL_H = 1.86;   // y388-522 px
const CELL = 11;
function col(x, w, color) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x, y: TBL_Y, w, h: TBL_H,
    fill: { color }, line: { color, width: 0.25 },
  });
}
function tcell(x, w, yCtr, text) {
  s.addText(text, { x, y: yCtr - 0.10, w, h: 0.22, align: "center", valign: "middle",
    fontSize: CELL, color: BLACK, fontFace: FONT, margin: 0 });
}
// row centers: header 397px, then 15px pitch (412..517px)
const ROWS = [5.51, 5.72, 5.93, 6.14, 6.35, 6.56, 6.76, 6.97, 7.18];

// ----- left (categorical) table: x350-520 px -----
const L = { Y: [4.86, 0.45], Out: [5.31, 0.81], T: [6.29, 0.46], R: [6.86, 0.36] };
col(L.Y[0], L.Y[1], WHITE);
col(L.Out[0], L.Out[1], PINK);
col(L.T[0], L.T[1], ORANGE);
col(L.R[0], L.R[1], LGREEN);
// header
tcell(L.Y[0], L.Y[1], ROWS[0], "Y");
tcell(L.Out[0], L.Out[1], ROWS[0], "Out");
tcell(L.T[0], L.T[1], ROWS[0], "T");
tcell(L.R[0], L.R[1], ROWS[0], "R");
// 8 data rows (verbatim from the spec)
const leftRows = [
  ["P", "Sunny",    "Low",  "Yes"],
  ["N", "Sunny",    "High", "Yes"],
  ["N", "Sunny",    "High", "No"],
  ["P", "Overcast", "Low",  "Yes"],
  ["P", "Overcast", "High", "No"],
  ["P", "Overcast", "Low",  "No"],
  ["P", "Rainy",    "Low",  "Yes"],
  ["N", "Rainy",    "Low",  "No"],
];
leftRows.forEach((r, i) => {
  const y = ROWS[i + 1];
  tcell(L.Y[0], L.Y[1], y, r[0]);
  tcell(L.Out[0], L.Out[1], y, r[1]);
  tcell(L.T[0], L.T[1], y, r[2]);
  tcell(L.R[0], L.R[1], y, r[3]);
});

// ----- arrow between the tables (hollow red right arrow; x549-572 y449-459 px) -----
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 7.58, y: 6.20, w: 0.40, h: 0.24,
  fill: { color: BG }, line: { color: ARROW_RED, width: 1.25 },
});

// ----- right (numeric result) table: x610-724 px -----
const R2 = { Y: [8.47, 0.47], Out: [8.94, 0.38], T: [9.43, 0.21], R: [9.64, 0.35] };
col(R2.Y[0], R2.Y[1], WHITE);
col(R2.Out[0], R2.Out[1], PINK);
col(R2.T[0], R2.T[1], ORANGE);
col(R2.R[0], R2.R[1], LGREEN);
// header
tcell(R2.Y[0], R2.Y[1], ROWS[0], "Y");
tcell(R2.Out[0], R2.Out[1], ROWS[0], "Out");
tcell(R2.T[0], R2.T[1], ROWS[0], "T");
tcell(R2.R[0], R2.R[1], ROWS[0], "R");
// 8 data rows (verbatim from the spec; Out column is eight '?' — intentional content)
const rightRows = [
  ["1", "?", "1", "1"],
  ["0", "?", "0", "1"],
  ["0", "?", "0", "0"],
  ["1", "?", "0", "0"],
  ["1", "?", "0", "0"],
  ["1", "?", "0", "1"],
  ["0", "?", "0", "0"],
  ["1", "?", "0", "1"],
];
rightRows.forEach((r, i) => {
  const y = ROWS[i + 1];
  tcell(R2.Y[0], R2.Y[1], y, r[0]);
  tcell(R2.Out[0], R2.Out[1], y, r[1]);
  tcell(R2.T[0], R2.T[1], y, r[2]);
  tcell(R2.R[0], R2.R[1], y, r[3]);
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_027_recreated.pptx" })
  .then(() => console.log("done"));
