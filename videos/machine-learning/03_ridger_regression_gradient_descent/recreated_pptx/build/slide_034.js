// Build slide 034 — "Non-Convex Function"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (house chrome = shared_patterns/house_chrome.js)
//
// Ground truth: unique_slides/slide_034.jpg (960x540, 1px = 1pt = 1/72 in).
// Analysis: slide_034_final.json (verbatim_text, layout, visual_elements, recreation_brief).
//
// MEASURED geometry (frame px, JPEG smear ±2px):
//   Canvas: FFFFFF | Panel: E9E9E7 rect x54..903 y45..540 | Strokes: C00000 1pt L/R/B only (NO top)
//   Badge: circle d≈35px centered (876,73) fill FDFD96 ring 6A5ACD bold 18pt Arial #333333 numeral 34
//
// Content regions (measured from frame):
//   Title "Non-Convex Function": red #C00000 (JPEG-darkened #8B0000), ink x 56..399, rows 35..43
//     baseline ~row 39 (x-height top 36, baseline 39, descender to 43), cap height ~8px
//     Ink center x ~227 (should center at frame center 480 -> box center 481 for LO)
//     Font size: ~44pt (from ink width ~340px / 7.7 chars * 1pt per char ~44pt)
//   Subtitle L1 "May reach different minimum value based on:": dark gray/black
//     Row ~46, ink x ~56..399, center ~227 -> box center 481
//   Subtitle L2 "initial point and learning rate": blue #0000FF
//     Rows 48..79 (multi-line wrapped), ink x 53..399, center ~226 -> box center 481
//   Parameter box (3-row table): top-left below subtitle, pale yellow fill #FFFACD
//     Rows ~85..160, cols ~55..220 (approx)
//     Row labels: step, initial X, delta | Values: 0.2, 7, 0.1
//   Red arrow: thick #FF0000 from param box right edge toward main table
//   Equation box: white #FFFFFF with black border, centered-left
//     Rows ~200..275, cols ~200..550
//     Equation: f(x) = (x^2 cos(x) - x)/10 rendered as stacked fraction
//   Explanatory text: below equation, rows ~260..295, cols ~100..490
//     "X is in between 9.6 and 9.8" (9.8 red bold #FF0000)
//     "f(x) is in between -10.03 and -9.92"
//   Function plot: top-right, rows ~43..270, cols ~576..911
//     Blue curve #0000FF, red markers #FF0000, orange arrow #FFA500, pink annotation #FF69B4
//   Main table: bottom, rows ~300..495, cols ~95..859 (1 label + 18 data cols = 19 cols)
//     Row colors:
//       Row 0 (x): cyan #AFEEEE
//       Row 1 (f(x)): white #FFFFFF with green #90EE90 highlights on data cols 14-18
//       Rows 2-5 (x-delta, f(x-delta), x+delta, f(x+delta)): yellow #FFFACD
//       Row 6 (slope): pink #FFB6C1
//       Row 7 (next x): light green #98FB98
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
// TITLE BLOCK (top-left, above panel which starts at y=45)
// ============================================================
// Title "Non-Convex Function": red #C00000
// Measured baseline at row ~39. For 44pt: ascent 40.73, halfLead 1.87, LO offset +1.6
// => baseline = top + 44.2 => top = 39 - 44.2 = -5.2
// Ink center x ~227 (frame center 480), LO centers ~1px left -> box center 481
// Box width: ink spans ~343px, add 20% -> ~412px
slide.addText("Non-Convex Function", {
  x: px(275), y: px(-5.2), w: px(412), h: px(70),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 44, bold: true, color: "C00000",
  lineSpacing: 54,
});

// Subtitle line 1: "May reach different minimum value based on:"
// Measured at row ~46 (dark gray). For 18pt: ascent 16.6, halfLead 0.75, LO offset ~0.7
// => baseline = top + 18 => top = 46 - 18 = 28
slide.addText("May reach different minimum value based on:", {
  x: px(275), y: px(28), w: px(412), h: px(40),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 18, color: "333333",
  lineSpacing: 22,
});

// Subtitle line 2: "initial point and learning rate" (blue #0000FF)
// First baseline at row ~52. top = 52 - 18 = 34
slide.addText("initial point and learning rate", {
  x: px(275), y: px(34), w: px(412), h: px(70),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 18, bold: true, color: "0000FF",
  lineSpacing: 22,
});

// ============================================================
// PARAMETER BOX (3-row table, top-left below subtitle, inside panel)
// ============================================================
// Panel starts at x=54, y=45. Parameter box at ~x=60, y=100
const paramX = px(60);
const paramY = px(100);
const paramW = px(180);
const paramRowH = px(22);

const paramTable = [
  [{ text: "step", options: { bold: true } }, { text: "0.2" }],
  [{ text: "initial X", options: { bold: true } }, { text: "7" }],
  [{ text: "delta", options: { bold: true } }, { text: "0.1" }],
];

slide.addTable(paramTable, {
  x: paramX, y: paramY, w: paramW,
  fontFace: "Arial", fontSize: 14,
  fill: "FFFACD",
  border: [{ type: "solid", color: "000000", width: 0.75 }],
  colW: [px(90), px(90)],
  rowH: paramRowH,
  valign: "middle",
});

// ============================================================
// RED ARROW (from param box right edge toward main table)
// ============================================================
// Param box right edge at frame x = 60 + 180 = 240
// Arrow from x=240 to ~400 (toward table starting at x~95)
// Y centered on param box: 100 + 3*22/2 = 133
slide.addShape(pptx.ShapeType.line, {
  x: px(240), y: px(133), w: px(160), h: 0,
  line: { color: "FF0000", width: 3, endArrowType: "triangle" },
});

// ============================================================
// EQUATION BOX (center-left)
// ============================================================
// White box with black border at rows ~200..275, cols ~200..550
// Equation asset: eq_034_main.png (1206x260 px at 600dpi = 2.01 x 0.433 in)
const eqBoxX = px(200);
const eqBoxY = px(200);
const eqBoxW = px(350);
const eqBoxH = px(80);

slide.addShape(pptx.ShapeType.rect, {
  x: eqBoxX, y: eqBoxY, w: eqBoxW, h: eqBoxH,
  fill: { color: "FFFFFF" },
  line: { color: "000000", width: 1 },
});

// Equation image - centered in box
// Image: 2.01 x 0.433 in. Box: 4.86 x 1.11 in.
// Center x: 200 + (350 - 1206/600*72)/2 = 200 + (350 - 241.2)/2 = 254.4
// Center y: 200 + (80 - 260/600*72)/2 = 200 + (80 - 31.2)/2 = 224.4
const eqImgX = px(254);
const eqImgY = px(224);
const eqImgW = 1206 / 600;
const eqImgH = 260 / 600;

slide.addImage({
  path: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/eq_034_main.png",
  x: eqImgX, y: eqImgY, w: eqImgW, h: eqImgH,
});

// ============================================================
// EXPLANATORY TEXT (below equation)
// ============================================================
// Two lines, rows ~260..295, cols ~100..490
// Line 1: "X is in between 9.6 and 9.8" with "9.8" in red bold #FF0000
// Line 2: "f(x) is in between -10.03 and -9.92"
// Line 1 baseline at row ~275. For 16pt: ascent 14.8, halfLead 0.67, LO offset ~0.6 -> 16px to baseline
// top = 275 - 16 = 259
slide.addText([
  { text: "X is in between 9.6 and ", options: { fontFace: "Arial", fontSize: 16, color: "000000" } },
  { text: "9.8", options: { fontFace: "Arial", fontSize: 16, bold: true, color: "FF0000" } },
], {
  x: px(100), y: px(259), w: px(400), h: px(30),
  align: "left", valign: "top", margin: 0,
  lineSpacing: 20,
});

// Line 2 baseline at row ~290 -> top = 290 - 16 = 274
slide.addText("f(x) is in between -10.03 and -9.92", {
  x: px(100), y: px(274), w: px(400), h: px(30),
  align: "left", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 16, color: "000000",
  lineSpacing: 20,
});

// ============================================================
// FUNCTION PLOT (top-right)
// ============================================================
// Plot asset: graph_034_main.png (2732x1832 px at 600dpi = 4.553 x 3.053 in)
// Plot area in frame: rows 43..270, cols 576..911
// In inches: x = 576/72 = 8.0, y = 43/72 = 0.597
// w = (911-576)/72 = 4.65, h = (270-43)/72 = 3.15
const graphX = px(576);
const graphY = px(43);
const graphW = 2732 / 600;
const graphH = 1832 / 600;

slide.addImage({
  path: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/graph_034_main.png",
  x: graphX, y: graphY, w: graphW, h: graphH,
});

// ============================================================
// MAIN TABLE (bottom)
// ============================================================
// 8 rows x 19 columns (1 label + 18 data)
// Row labels: x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x
// Data (18 columns each from analysis):
const tableData = {
  labels: ["x", "f(x)", "x-delta", "f(x-delta)", "x+delta", "f(x+delta)", "slope", "next x"],
  rows: [
    // x row (18 values)
    [7, 7.2, 7.4, 7.6, 7.8, 8, 8.2, 8.4, 8.6, 8.8, 9, 9.2, 9.4, 9.6, 9.8, 9.8, 9.8, 9.8],
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

// Table position: rows ~300..495, cols ~95..859
// In inches: x = 95/72 = 1.319, y = 300/72 = 4.167
// w = (859-95)/72 = 10.61, h = (495-300)/72 = 2.71
// 19 columns: 1 label + 18 data. Label col wider, data cols equal.
const tableX = px(95);
const tableY = px(300);
const tableW = px(764); // 859 - 95
// Column widths: label ~80px, 18 data cols ~38px each = 684, total ~764
const labelColW = px(80);
const dataColW = px(38);

slide.addTable(tableRows, {
  x: tableX, y: tableY, w: tableW,
  fontFace: "Arial", fontSize: 9,
  border: [{ type: "solid", color: "000000", width: 0.5 }],
  colW: [labelColW, ...Array(18).fill(dataColW)],
  rowH: px(22),
  valign: "middle",
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));