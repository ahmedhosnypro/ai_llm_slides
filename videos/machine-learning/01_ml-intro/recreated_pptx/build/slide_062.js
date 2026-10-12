// Slide 62 recreation — "IRIS Dataset" (ml-intro deck) — ATTEMPT 4 (founder-issue rework)
// Spec: videos/ml-intro/analysis/slide_062_final.json (PASS_WITH_FIXES, score 9)
// House frame rule (founder directive): house template chrome overrides spec geometry.
//
// FOUNDER ISSUE 10 (2026-10-10 final-deck review) — this attempt fixes:
//   (a) Table data incorrect/incomplete → every cell now read LIVE from the canonical
//       dataset videos/ml-intro/datasets/iris.csv (P7: one source for slides 60-64).
//       Original's displayed row set (PIL-proven from row counts 8/12/9/3 + class-color
//       composition 6red+6green / 5green+4blue + iris.csv class boundaries 1-50/51-100/101-150):
//       serials 1-8, 45-56, 96-104, 148-150, with one red "..." ellipsis row per gap.
//       (Old build wrongly showed row 44 and showed iris rows 51-57 under serials 50-56.)
//   (b) Table frame ("150 samples" data frame, left inner frame) top+bottom overflow →
//       backdrop + table re-laid out at the ORIGINAL's measured geometry with all ink
//       inside the red border with clearance (P2 inner-frame budget).
//   Hardening: info-box blank spacer paragraphs render at 10pt in every renderer
//   (old build's empty runs left endParaRPr sz=2000 → 20pt blank lines).

const fs = require("fs");
const pptxgen = require("pptxgenjs");

// ---------- canonical dataset (P7) ----------
const IRIS_CSV = "videos/ml-intro/datasets/iris.csv";
const lines = fs.readFileSync(IRIS_CSV, "utf8").trim().split(/\r?\n/);
const header = lines[0].split(","); // sepal_length,sepal_width,petal_length,petal_width,species
if (header.join(",") !== "sepal_length,sepal_width,petal_length,petal_width,species") {
  throw new Error("iris.csv header mismatch: " + header.join(","));
}
const IRIS = [null]; // 1-indexed: IRIS[n] = row n
for (const ln of lines.slice(1)) {
  const p = ln.split(",");
  if (p.length !== 5) throw new Error("bad iris.csv row: " + ln);
  IRIS.push(p);
}
if (IRIS.length !== 151) throw new Error("iris.csv must have 150 rows, got " + (IRIS.length - 1));

// number formatting as the original slide shows values: 5.0 -> "5", 5.1 -> "5.1"
function num(s) {
  const v = parseFloat(s);
  if (Number.isInteger(v)) return String(v);
  return String(v);
}
function cls(species) {
  return species.charAt(0).toUpperCase() + species.slice(1);
}

// Row set displayed by the ORIGINAL (PIL-derived; see qa/slide062 forensics):
// blocks 1-8, 45-56, 96-104, 148-150; one "..." row in each of the 3 gaps.
const BLOCKS = [
  { from: 1, to: 8 },
  { from: 45, to: 56 },
  { from: 96, to: 104 },
  { from: 148, to: 150 },
];

// ---------- palette ----------
const BG = "E8E8E8";        // slide background
const RED = "CC0000";       // title, table border, Setosa, ellipsis, "No Direct Visualization"
const GREEN = "009900";     // Versicolor
const BLUE = "0000CC";      // Virginica, bold summary lines
const ORANGE = "FF6600";    // table header row text
const WHITE = "FFFFFF";     // table / info-box fill
const GRID = "CCCCCC";      // table gridlines
const INFO_BORDER = "6666CC";
const INK = "333333";       // badge numeral
const TEXT = "000000";      // table numeric text
const FONT = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House chrome (founder directive, overrides spec) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("62", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText("IRIS Dataset", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.7, align: "center", valign: "middle",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- Data table (left; frame at ORIGINAL-measured geometry, P2 budget) ----
// Original (960x540 frame): border x=[80,461]px y=[114,526]px -> x=1.111..6.403in,
// y=1.583..7.306in (h=5.72). LibreOffice's row-height floor for 8pt text is
// 0.153in/row (measured render_4: 22.97px) -> 36 rows = 5.51in, taller than the
// original's rows; per the P2/slide-5 founder directive the frame is ENLARGED and
// moved up (not the ink squeezed) so all table ink sits inside with clearance:
// y=1.51..7.24 (h=5.73), keeping >=16px clearance to the house frame bottom (7.35in).
// Measured clearances (render_5): top 21px, bottom 12px, left 8px, right 6px.
const FRAME = { x: 1.11, y: 1.51, w: 5.29, h: 5.73 }; // backdrop rect (border box)
// Column proportions measured from the original's gridlines (50,69,69,69,69,52)/378.
const COLW = [0.69, 0.95, 0.95, 0.95, 0.95, 0.71]; // sum 5.20
const TABLE_W = COLW.reduce((a, b) => a + b, 0);
const ROW_H = 0.15;
const N_ROWS = 1 + 32 + 3; // header + 32 data rows + 3 ellipsis rows = 36
// Vertical: 0.14in (21px) below the frame's top border; bottom clearance follows
// from the measured LO row pitch (36 x 22.97px = 827px -> bottom edge at 7.16in).
const TABLE_Y = FRAME.y + 0.14;

s.addShape(pptx.shapes.RECTANGLE, {
  x: FRAME.x, y: FRAME.y, w: FRAME.w, h: FRAME.h,
  fill: { color: WHITE }, line: { color: RED, width: 1.25 },
});

const CLASS_COLOR = { Setosa: RED, Versicolor: GREEN, Virginica: BLUE };
const GRIDB = { color: GRID, pt: 0.5 };
const HEADERS = ["Serial", "sepal.length", "sepal.width", "petal.length", "petal.width", "Class"];

const cellOpts = (color) => ({
  color, fill: { color: WHITE }, border: GRIDB,
  align: "center", valign: "middle", fontSize: 8, fontFace: FONT,
});

const tableRows = [];
tableRows.push(HEADERS.map((h) => ({ text: h, options: cellOpts(ORANGE) })));

for (let b = 0; b < BLOCKS.length; b++) {
  if (b > 0) {
    // one ellipsis row per gap, red "..." in all 6 cells (as the original's first gap shows)
    tableRows.push(["...", "...", "...", "...", "...", "..."].map(() => ({
      text: "...", options: cellOpts(RED),
    })));
  }
  for (let n = BLOCKS[b].from; n <= BLOCKS[b].to; n++) {
    const r = IRIS[n]; // [sepal_length, sepal_width, petal_length, petal_width, species]
    if (!r) throw new Error("iris.csv missing row " + n);
    const className = cls(r[4]);
    if (!(className in CLASS_COLOR)) throw new Error("unknown species at row " + n + ": " + r[4]);
    tableRows.push([
      { text: String(n), options: cellOpts(TEXT) },
      { text: num(r[0]), options: cellOpts(TEXT) },
      { text: num(r[1]), options: cellOpts(TEXT) },
      { text: num(r[2]), options: cellOpts(TEXT) },
      { text: num(r[3]), options: cellOpts(TEXT) },
      { text: className, options: cellOpts(CLASS_COLOR[className]) },
    ]);
  }
}

s.addTable(tableRows, {
  x: FRAME.x + 0.05, y: TABLE_Y, w: TABLE_W, colW: COLW,
  rowH: ROW_H, margin: 0.01,
});

// ---- Info box (right-center; geometry kept from certified attempt 2/3) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.75, y: 2.15, w: 3.15, h: 3.4,
  fill: { color: WHITE }, line: { color: INFO_BORDER, width: 1 },
});
// NEW LAW (17_worker_instructions.md pre-judge item 8 / patterns.md P2 amendment,
// founder slide-5 evidence): PowerPoint's auto line pitch is ~15% taller than LO's,
// which made the old build's centered text block overflow this box top AND bottom in
// PowerPoint (founder report) while the LO render fit. Every paragraph therefore pins
// EXACT lineSpacing (spcPts) so both renderers use the same pitch:
//   20pt lines -> 24, 16pt class lines -> 19, 14pt last line -> 17, 10pt spacers -> 10.
// Pinned block height = 166pt lines + 6pt paraSpaceAfter = 172pt = 2.39in, centered in
// the 3.4in box -> ~0.5in LO top/bottom clearance (>= 0.4in law bar).
// Blank spacers are single-space runs at 10pt (empty runs made pptxgenjs emit
// endParaRPr sz=2000 -> 20pt blank lines).
s.addText(
  [
    { text: "150 Samples", options: { fontSize: 20, bold: true, color: BLUE, breakLine: true, lineSpacing: 24, paraSpaceAfter: 2 } },
    { text: " ", options: { fontSize: 10, breakLine: true, lineSpacing: 10, paraSpaceAfter: 0 } },
    { text: "3 Classes", options: { fontSize: 20, bold: true, color: BLUE, breakLine: true, lineSpacing: 24, paraSpaceAfter: 0 } },
    { text: "Setosa", options: { fontSize: 16, color: RED, breakLine: true, lineSpacing: 19, paraSpaceAfter: 0 } },
    { text: "Versicolor", options: { fontSize: 16, color: GREEN, breakLine: true, lineSpacing: 19, paraSpaceAfter: 0 } },
    { text: "Virginica", options: { fontSize: 16, color: BLUE, breakLine: true, lineSpacing: 19, paraSpaceAfter: 2 } },
    { text: " ", options: { fontSize: 10, breakLine: true, lineSpacing: 10, paraSpaceAfter: 0 } },
    { text: "4 Features", options: { fontSize: 20, bold: true, color: BLUE, breakLine: true, lineSpacing: 24, paraSpaceAfter: 2 } },
    { text: "No Direct Visualization", options: { fontSize: 14, italic: true, underline: true, color: RED, lineSpacing: 17 } },
  ],
  {
    x: 7.75, y: 2.15, w: 3.15, h: 3.4, align: "center", valign: "middle",
    fontFace: FONT, margin: 0.05,
  }
);

// NOTE (per founder ground rules): the mouse cursor seen in the original video frame
// is a screen-capture artifact and is intentionally NOT recreated.

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_062_recreated.pptx" })
  .then(() => console.log("done: table rows=" + (tableRows.length - 1) + " (incl. header), data from " + IRIS_CSV));
