// Build slide 034 — "Non-Convex Function"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (house chrome = shared_patterns/house_chrome.js)
//
// Ground truth: unique_slides/slide_034.jpg (960x540, 1px = 1pt = 1/72 in).
// Analysis: slide_034_final.json (verbatim_text, layout, visual_elements, recreation_brief).
//
// MEASURED geometry (frame px, from unique_slides/slide_034.jpg, PIL):
//   Canvas: FFFFFF | Panel: E9E9E7 rect x54..903 y45..540 | Strokes: C00000 1pt L/R/B only (NO top)
//   Badge: circle d≈35px centered (876,73) fill FDFD96 ring 6A5ACD bold 18pt Arial #333333 numeral 34
//   Title "Non-Convex Function" 24pt bold #8B0000, ink rows 67..84 cols 195..434 (cx 314)
//   Subtitle L1 22pt #8B0000 "May reach different minimum value based on:", ink rows 94..113 cols 113..533 (cx 323)
//   Subtitle L2 22pt bold #0000FF "initial point and learning rate", ink rows 122..140 cols 192..461 (cx 326)
//   Parameter box (3 rows): border cols 75..174, rows 246..308 (dark ~1px), interior panel fill (no fill painted)
//   Red arrow: horizontal at row ~277, from the parameter box right edge (x≈182) rightwards
//   Equation box: white #FFFFFF, black 1px border, cols 465..607 rows 170..218
//   Explanatory text: two lines starting rows ~262 and ~280, cols ~270..600, 16pt (9.8 red bold #FF0000)
//   Function plot: axes box cols 607..845, rows 58..313 (y-axis spine col 721, x-axis spine row 172)
//   Main table: white, black 1px grid, rows 321..517, label col 82..136, data cols to 879
//
// Note: Equation rendered via matplotlib mathtext -> 600dpi transparent PNG -> addImage at exact px/600 size

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_034_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top),
// badge circle with numeral 34 (file number = printed number; no zero-padding).
drawHouseChrome(pptx, slide, { numeral: 34 });

// ============================================================
// TITLE BLOCK (top-left, inside the panel which starts at y=45)
// ============================================================
// MEASURED from unique_slides/slide_034.jpg (960x540, 1px = 1pt), PIL:
//   The original has ZERO content ink above y=44 (rows 0..44 are blank white canvas
//   above the panel) — so the whole title block belongs INSIDE the panel.
//   Title "Non-Convex Function": single line, ink rows 67..84, cols 195..434
//     (width 240px; Arial-Bold advance sum for the string = 9.893em -> ~24pt).
//   Subtitle L1 "May reach different minimum value based on:": ink rows 94..113,
//     cols 113..533 (width 420px; advance sum 18.4em -> ~22pt), dark red #8B0000
//     (measured ink core RGB (140,28,40); the frame wins over the analysis "black").
//   Subtitle L2 "initial point and learning rate": ink rows 122..140, cols 192..461
//     (width 269px; advance sum 12.174em bold -> ~22pt), blue #0000FF.
// LO cap-top offset ~0.278em below the box top (calibrated on the 18pt subtitle).
const TITLE_CX = (195 + 434) / 2;   // 314
const L1_CX = (113 + 533) / 2;      // 323
const L2_CX = (192 + 461) / 2;      // 326

slide.addText("Non-Convex Function", {
  x: px(TITLE_CX - 200), y: px(60), w: px(400), h: px(40),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 24, bold: true, color: "8B0000",
  lineSpacing: 30,
});

// Subtitle line 1: "May reach different minimum value based on:" (dark red #8B0000)
slide.addText("May reach different minimum value based on:", {
  x: px(L1_CX - 220), y: px(88), w: px(440), h: px(40),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 22, color: "8B0000",
  lineSpacing: 26,
});

// Subtitle line 2: "initial point and learning rate" (blue #0000FF)
slide.addText("initial point and learning rate", {
  x: px(L2_CX - 230), y: px(116), w: px(460), h: px(40),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 22, bold: true, color: "0000FF",
  lineSpacing: 26,
});

// ============================================================
// PARAMETER BOX (3-row table, left, rows 246..308, cols 75..174)
// ============================================================
// MEASURED: left border col 75 (rows 246..308), right border col 174, top row 246,
// bottom row 308. Interior reads E9E9E7 (panel) — the box carries a black border
// but NO fill of its own.
const paramX = 67;
const paramY = 246;
const paramW = 110;      // 75 .. 174
const paramRowH = px(20); // ~3 rows x 20px

const paramTable = [
  [{ text: "step", options: { bold: true } }, { text: "0.2" }],
  [{ text: "initial X", options: { bold: true } }, { text: "7" }],
  [{ text: "delta", options: { bold: true } }, { text: "0.1" }],
];

slide.addTable(paramTable, {
  x: px(paramX), y: px(paramY), w: px(paramW),
  fontFace: "Arial", fontSize: 11,
  border: [{ type: "solid", color: "000000", width: 0.75 }],
  colW: [px(66), px(44)],
  rowH: paramRowH,
  valign: "middle",
});

// ============================================================
// RED ARROW (from the parameter box right edge, rightwards, row ~277)
// ============================================================
slide.addShape(pptx.ShapeType.line, {
  x: px(186), y: px(277), w: px(150), h: 0,
  line: { color: "FF0000", width: 3, endArrowType: "triangle" },
});

// ============================================================
// EQUATION BOX (white with black border, cols 465..607, rows 170..218)
// ============================================================
const eqBoxX = 461;
const eqBoxY = 165;
const eqBoxW = 150;   // 465 .. 607 with the 1px borders
const eqBoxH = 57;    // 170 .. 218

slide.addShape(pptx.ShapeType.rect, {
  x: px(eqBoxX), y: px(eqBoxY), w: px(eqBoxW), h: px(eqBoxH),
  fill: { color: "FFFFFF" },
  line: { color: "000000", width: 1 },
});

// Equation image centered in the box, at 3/4 of the box width so it does not
// touch the borders: 112px wide, 24px tall (f(x) = (x^2 cos(x) - x)/10).
const eqImgW = 112;
const eqImgH = 24;
slide.addImage({
  path: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/eq_034_main.png",
  x: px(eqBoxX + (eqBoxW - eqImgW) / 2), y: px(eqBoxY + (eqBoxH - eqImgH) / 2),
  w: px(eqImgW), h: px(eqImgH),
});

// ============================================================
// EXPLANATORY TEXT (two lines below the equation, cols ~270..600)
// ============================================================
// Line 1: "X is in between 9.6 and 9.8" with "9.8" in red bold #FF0000
// Line 2: "f(x) is in between -10.03 and -9.92"
slide.addText([
  { text: "X is in between 9.6 and ", options: { fontFace: "Arial", fontSize: 16, color: "000000" } },
  { text: "9.8", options: { fontFace: "Arial", fontSize: 16, bold: true, color: "FF0000" } },
], {
  x: px(279), y: px(259), w: px(400), h: px(30),
  align: "left", valign: "top", margin: 0,
  lineSpacing: 20,
});

slide.addText("f(x) is in between -10.03 and -9.92", {
  x: px(279), y: px(274), w: px(400), h: px(30),
  align: "left", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 16, color: "000000",
  lineSpacing: 20,
});

// ============================================================
// FUNCTION PLOT (top-right; axes box cols 607..845, rows 58..313)
// ============================================================
// Two layers, in order:
//   1. a WHITE backing rect covering the measured axes box — the original's plot
//      interior is white (254,255,253); the plot asset itself is transparent, so
//      without this the gray E9E9E7 panel shows through and the interior reads gray.
//   2. the graph asset scaled to FIT inside the box, preserving its native aspect
//      (2732x1832 = 1.491) and centred on the box centre (726, 186). The box is
//      239x256 (aspect 0.934), so the image letterboxes within it: 239 wide x
//      239/1.491 = 160 tall, centred vertically.
const plotBox = { x: 607, y: 58, w: 239, h: 256 };
const plotCx = plotBox.x + plotBox.w / 2;   // 726
const plotCy = plotBox.y + plotBox.h / 2;   // 186

slide.addShape(pptx.ShapeType.rect, {
  x: px(plotBox.x), y: px(plotBox.y), w: px(plotBox.w), h: px(plotBox.h),
  fill: { color: "FFFFFF" },
  line: { color: "8B0000", width: 1 },  // original axes box border is dark red, not black
});

// asset aspect 2732/1832 = 1.491; fit to box width, centre vertically
const plotImgW = plotBox.w;
const plotImgH = plotBox.w * 1832 / 2732;    // 160.2
slide.addImage({
  path: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/graph_034_main.png",
  x: px(plotCx - plotImgW / 2), y: px(plotCy - plotImgH / 2),
  w: px(plotImgW), h: px(plotImgH),
});

// ============================================================
// MAIN TABLE (bottom; white, black grid, rows 321..517, cols 82..879)
// ============================================================
// 8 rows x 19 columns (1 label + 18 data)
// Row labels: x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x
// Data (18 columns each from analysis):
const tableData = {
  labels: ["x", "f(x)", "x-delta", "f(x-delta)", "x+delta", "f(x+delta)", "slope", "next x"],
  rows: [
    // x row (18 values) — the tail ALTERNATES 9.8/9.6 (analysis transcript collapsed it
    // to four 9.8s; the dataset's own next-x / x-delta / f(x) rows force the alternation)
    [7, 7.2, 7.4, 7.6, 7.8, 8, 8.2, 8.4, 8.6, 8.8, 9, 9.2, 9.4, 9.6, 9.8, 9.6, 9.8, 9.6],
    // f(x) row
    [2.99, 2.43, 1.66, 0.69, -0.45, -1.73, -3.1, -4.5, -5.88, -7.16, -8.28, -9.17, -9.77, -10.03, -9.92, -10.03, -9.92, -10.03],
    // x-delta row
    [6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5, 8.7, 8.9, 9.1, 9.3, 9.5, 9.7, 9.5, 9.7, 9.5],
    // f(x-delta) row
    [3.19, 2.74, 2.07, 1.2, 0.14, -1.08, -2.41, -3.8, -5.2, -6.54, -7.75, -8.76, -9.51, -9.95, -10.02, -9.95, -10.02, -9.95],
    // x+delta row
    [7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5, 8.7, 8.9, 9.1, 9.3, 9.5, 9.7, 9.9, 9.7, 9.9, 9.7],
    // f(x+delta) row
    [2.74, 2.07, 1.2, 0.14, -1.08, -2.41, -3.8, -5.2, -6.54, -7.75, -8.76, -9.51, -9.95, -10.02, -9.7, -10.02, -9.7, -10.02],
    // slope row
    [-4.5, -6.7, -8.7, -10.6, -12.2, -13.3, -13.9, -14, -13.4, -12.1, -10.1, -7.5, -4.4, -0.7, 3.2, -0.7, 3.2, -0.7],
    // next x row
    [7.2, 7.4, 7.6, 7.8, 8, 8.2, 8.4, 8.6, 8.8, 9, 9.2, 9.4, 9.6, 9.8, 9.6, 9.8, 9.6, 9.8],
  ],
  // Row fills (index = row index in the 8 data rows)
  rowFills: [
    "AFEEEE",  // x - cyan
    "FFFFFF",  // f(x) - white (with green highlights on cols 14-18)
    "FFFACD",  // x-delta - yellow
    "FFFACD",  // f(x-delta) - yellow
    "FFFACD",  // x+delta - yellow
    "FFFACD",  // f(x+delta) - yellow
    "FFB6C1",  // slope - pink
    "98FB98",  // next x - light green
  ],
};

// Build table rows for pptxgenjs
const tableRows = [];
for (let i = 0; i < 8; i++) {
  const row = [];
  // Label cell
  row.push({
    text: tableData.labels[i],
    options: { bold: true, fill: tableData.rowFills[i], fontSize: 9, fontFace: "Arial" },
  });
  // Data cells (18 columns)
  for (let j = 0; j < 18; j++) {
    let cellFill = tableData.rowFills[i];
    // Green highlight on f(x) row (index 1) for data columns 14-18 (0-indexed: 13-17)
    if (i === 1 && j >= 13 && j <= 17) {
      cellFill = "90EE90";
    }
    row.push({
      text: String(tableData.rows[i][j]),
      options: { fill: cellFill, fontSize: 9, fontFace: "Arial", align: "center" },
    });
  }
  tableRows.push(row);
}

// Table position: rows 321..517, cols 82..879 — 8 rows x 24.5px (196px total)
// 19 columns: label 58px + 18 data cols x 41.11px = 798px total
const tableX = 78;
const tableY = 321;
const tableW = 798;   // 82 .. 879
const labelColW = px(58);
const dataColW = px(41.11);
const tableRowH = px(24.5);

slide.addTable(tableRows, {
  x: px(tableX), y: px(tableY), w: px(tableW),
  fontFace: "Arial", fontSize: 9,
  border: [{ type: "solid", color: "000000", width: 0.5 }],
  colW: [labelColW, ...Array(18).fill(dataColW)],
  rowH: tableRowH,
  valign: "middle",
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
