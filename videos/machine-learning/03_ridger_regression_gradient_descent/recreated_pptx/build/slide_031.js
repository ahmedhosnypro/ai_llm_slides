// Build: slide 031 — "Convex Function, Learning Rate =0.3, Start at X=3"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GEOMETRY SOURCE: PIL measurement of unique_slides/slide_031.jpg (960x540, 1px=1pt=1/72in).
// Spec: analysis/slide_031_final.json. Where spec and frame disagree, THE FRAME WINS.
//
// MEASURED LAYOUT (frame px, 960x540):
//   House chrome (deck standard): white FFFFFF canvas; gray E9E9E7 panel x54..903, y45..540;
//   red C00000 1pt strokes LEFT x58.5 (rows 46..539), RIGHT x901 (rows 46..539),
//   BOTTOM y538.5 (cols 58..902); NO TOP STROKE. Badge circle d~35px centered (876,73),
//   fill FDFD96, ring 6A5ACD 2pt, bold numeral 333333 Arial 18pt -> "31".
//
//   Title (top-left, multicolor, Arial bold ~26pt):
//     "Convex Function,"   red C00000
//     "Learning Rate =0.3,"  green 008000
//     "Start at X=3"      blue 0000FF
//     measured y ~ 65-85, x ~ 40-350
//
//   Parameter table (3 rows x 2 cols, below title, x ~ 80-250, y ~ 175-215):
//     Row 1: "step" | "0.3"
//     Row 2: "initial X" | "3"
//     Row 3: "delta" | "0.1"
//     Label cells: yellow FFFFF99 fill, black text
//     Value cells: white FFFFFF fill, black text
//     Grid lines: thin black
//
//   Formula box (top-center, x ~ 330-640, y ~ 185-200):
//     Red FF0000 border, white FFFFFF fill, black text
//     Equation: f(x)=(x-5)^2+1 (rendered as eq asset, 24pt)
//
//   Graph (top-right, x ~ 600-920, y ~ 50-250):
//     Cartesian plot of f(x)=(x-5)^2+1
//     Grid: light gray CCCCCC
//     Axes: black 000000 with tick labels -5, 0, 5, 10, 15 on both x and y
//     Blue parabola 0000FF
//     Green point 008000 at (5,1) labeled "(5,1)"
//     Red point FF0000 at (3,9)
//     Black horizontal segment from (3,9) to (7,9) labeled "(7,9)"
//     Red dashed lines FF0000 at x=5 and y=1
//
//   Annotation box (center below formula, x ~ 180-800, y ~ 245-310):
//     Red FF0000 border, white FFFFFF fill
//     Line 1: "X is in between 4.8 and 5.1" (5.1 in red bold C00000)
//     Line 2: "f(x) is in between 1.04 and 1.01"
//
//   "Bouncing" label + purple arrow (center-right above table, x ~ 340-560, y ~ 310-330):
//     Purple 7030A0 text "Bouncing" with purple arrow pointing down/right
//
//   Red arrow (left side above table, x ~ 160-170, y ~ 324-348):
//     Red FF0000 arrow pointing down/right
//
//   Main table (bottom full width, 8 rows x 17 cols, x ~ 63-893, y ~ 350-530):
//     Row labels (col 0): x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x
//     16 data columns per row with exact values from analysis
//     Row background colors: FFFFF99, D9EAD3, CFE2F3, D9D9D9, FCE5CD, 000000 (text)
//     (6 colors for 8 rows - pattern: first 6 rows colored, last 2 dark text)
//
// SPEC-VS-FRAME DEVIATIONS (frame wins, per building.md):
//   1. Spec says 17 columns for main table; frame shows 16 data columns + 1 label col = 17 total.
//      Verified: 1 label col + 16 data cols.
//   2. Spec main_table row count says 8 rows; visual_elements confirms 8 rows.
//      Spec recreation_brief had 9 rows originally - fixed by validation fixes_applied[2].
//   3. "color red bold" in verbatim_text.bullets is a formatting marker, not literal text.
//      The "5.1" in annotation line 1 is rendered red bold.
//   4. Table row-to-color mapping: spec lists 6 colors for 8 rows.
//      Frame evidence: alternating row colors visible. Mapping inferred from frame scan.
//
// Laws honored: hex without '#'; fontFace explicit everywhere; margin 0;
// measured geometry over intuition; closed-loop render check before any judge call.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = __dirname + "/../slide_031_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome: white canvas, gray panel, red L/R/bottom strokes, badge "31" ----
drawHouseChrome(pptx, slide, { numeral: 31 });

const A = "Arial";

// ============================================================
// TITLE: three colored segments, left-aligned at measured position
// Measured: y ~ 65-85, x starts ~ 54 (panel left edge + padding)
// ============================================================
const titleY = px(65);
const titleX = px(54 + 10); // 10px inside panel left
const titleSize = 26;
const lineH = 1.3;

slide.addText("Convex Function,", {
  x: titleX, y: titleY, w: px(300), h: px(titleSize * lineH),
  fontSize: titleSize, bold: true, color: "C00000", fontFace: A, margin: 0,
});
slide.addText("Learning Rate =0.3,", {
  x: titleX, y: px(65 + 30), w: px(300), h: px(titleSize * lineH),
  fontSize: titleSize, bold: true, color: "008000", fontFace: A, margin: 0,
});
slide.addText("Start at X=3", {
  x: titleX, y: px(65 + 60), w: px(300), h: px(titleSize * lineH),
  fontSize: titleSize, bold: true, color: "0000FF", fontFace: A, margin: 0,
});

// ============================================================
// PARAMETER TABLE (3 rows x 2 cols)
// Position: x ~ 80-250, y ~ 175-215
// Cell sizes: label col ~ 80px, value col ~ 80px, row height ~ 12px
// ============================================================
const pTableX = px(80);
const pTableY = px(175);
const pLabelW = px(80);
const pValueW = px(80);
const pRowH = px(13);

const pRows = [
  { label: "step", value: "0.3" },
  { label: "initial X", value: "3" },
  { label: "delta", value: "0.1" },
];

pRows.forEach((row, i) => {
  const y = pTableY + i * pRowH;
  // Label cell (yellow)
  slide.addShape(pptx.ShapeType.rect, {
    x: pTableX, y: y, w: pLabelW, h: pRowH,
    fill: { color: "FFFF99" }, line: { color: "000000", width: 0.5 },
  });
  slide.addText(row.label, {
    x: pTableX, y: y, w: pLabelW, h: pRowH,
    align: "center", valign: "middle", fontSize: 12, bold: false,
    color: "000000", fontFace: A, margin: 0,
  });
  // Value cell (white)
  slide.addShape(pptx.ShapeType.rect, {
    x: pTableX + pLabelW, y: y, w: pValueW, h: pRowH,
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.5 },
  });
  slide.addText(row.value, {
    x: pTableX + pLabelW, y: y, w: pValueW, h: pRowH,
    align: "center", valign: "middle", fontSize: 12, bold: false,
    color: "000000", fontFace: A, margin: 0,
  });
});

// ============================================================
// FORMULA BOX (red border, white fill, centered equation)
// Position: x ~ 330-640, y ~ 185-200
// Box: w ~ 310px, h ~ 50px
// ============================================================
const fBoxX = px(330);
const fBoxY = px(185);
const fBoxW = px(310);
const fBoxH = px(50);

slide.addShape(pptx.ShapeType.rect, {
  x: fBoxX, y: fBoxY, w: fBoxW, h: fBoxH,
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 },
});

// Equation rendered at 24pt, placed centered in box
// Asset: eq_031_main.png (w=1690px @600dpi = 2.81667in, h=0.38167in)
const eqInfo = require("./assets/eq_031_main.json"); // will read from generated file
// Actually we inline the JSON for now
const eqW = 2.81667;
const eqH = 0.38167;
const eqX = fBoxX + (fBoxW - eqW) / 2;
const eqY = fBoxY + (fBoxH - eqH) / 2;

slide.addImage({
  path: ASSET_DIR + "/eq_031_main.png",
  x: eqX, y: eqY, w: eqW, h: eqH,
});

// ============================================================
// GRAPH (parabola with axes, grid, points, dashed lines)
// This is complex - we'll draw it as a combination of shapes
// Position: x ~ 600-920, y ~ 50-250
// Plot area: approx x 640-900, y 70-240
// ============================================================
const gX = px(640);
const gY = px(70);
const gW = px(260); // 900-640
const gH = px(170); // 240-70

// Graph background (white)
slide.addShape(pptx.ShapeType.rect, {
  x: gX, y: gY, w: gW, h: gH,
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});

// Grid lines (light gray CCCCCC) - both horizontal and vertical
// Grid spans x: -5 to 15 (20 units), y: -5 to 15 (20 units)
// Plot: x in [-5,15] mapped to [0, gW], y in [-5,15] mapped to [gH, 0]
const xMin = -5, xMax = 15;
const yMin = -5, yMax = 15;
const tickVals = [-5, 0, 5, 10, 15];

function mapX(x) { return gX + ((x - xMin) / (xMax - xMin)) * gW; }
function mapY(y) { return gY + gH - ((y - yMin) / (yMax - yMin)) * gH; }

// Vertical grid lines
tickVals.forEach(xv => {
  const xPx = mapX(xv);
  slide.addShape(pptx.ShapeType.line, {
    x: xPx, y: gY, w: 0, h: gH,
    line: { color: "CCCCCC", width: 0.5 },
  });
});

// Horizontal grid lines
tickVals.forEach(yv => {
  const yPx = mapY(yv);
  slide.addShape(pptx.ShapeType.line, {
    x: gX, y: yPx, w: gW, h: 0,
    line: { color: "CCCCCC", width: 0.5 },
  });
});

// Axes (black, slightly thicker)
slide.addShape(pptx.ShapeType.line, { // x-axis (y=0)
  x: gX, y: mapY(0), w: gW, h: 0,
  line: { color: "000000", width: 1.5 },
});
slide.addShape(pptx.ShapeType.line, { // y-axis (x=0)
  x: mapX(0), y: gY, w: 0, h: gH,
  line: { color: "000000", width: 1.5 },
});

// Tick labels (Arial 9pt)
tickVals.forEach(xv => {
  slide.addText(String(xv), {
    x: mapX(xv) - px(12), y: mapY(0) + px(4), w: px(24), h: px(14),
    align: "center", valign: "top", fontSize: 9, color: "000000", fontFace: A, margin: 0,
  });
});
tickVals.forEach(yv => {
  if (yv === 0) return; // skip 0 on y-axis (already at origin)
  slide.addText(String(yv), {
    x: mapX(0) - px(30), y: mapY(yv) - px(7), w: px(28), h: px(14),
    align: "right", valign: "middle", fontSize: 9, color: "000000", fontFace: A, margin: 0,
  });
});

// Axis labels "x" and "y"
slide.addText("x", { x: gX + gW - px(15), y: mapY(0) + px(4), w: px(15), h: px(14), fontSize: 10, bold: true, color: "000000", fontFace: A, margin: 0 });
slide.addText("y", { x: mapX(0) - px(15), y: gY - px(12), w: px(15), h: px(14), fontSize: 10, bold: true, color: "000000", fontFace: A, margin: 0 });

// Parabola f(x) = (x-5)^2 + 1 - draw as smooth polyline (many points)
// Color: 0000FF (blue), width: 2pt
const N = 200;
let prevX = null, prevY = null;
for (let i = 0; i <= N; i++) {
  const x = xMin + (xMax - xMin) * i / N;
  const y = Math.pow(x - 5, 2) + 1;
  const px1 = mapX(x);
  const py1 = mapY(y);
  if (prevX !== null) {
    slide.addShape(pptx.ShapeType.line, {
      x: prevX, y: prevY, w: px1 - prevX, h: py1 - prevY,
      line: { color: "0000FF", width: 2 },
    });
  }
  prevX = px1; prevY = py1;
}

// Green point at (5,1) - minimum
const gx5 = mapX(5);
const gy1 = mapY(1);
slide.addShape(pptx.ShapeType.ellipse, {
  x: gx5 - px(4), y: gy1 - px(4), w: px(8), h: px(8),
  fill: { color: "008000" }, line: { color: "008000", width: 1 },
});
slide.addText("(5,1)", {
  x: gx5 - px(18), y: gy1 - px(22), w: px(36), h: px(14),
  align: "center", valign: "bottom", fontSize: 9, color: "008000", fontFace: A, margin: 0,
});

// Red point at (3,9)
const gx3 = mapX(3);
const gy9 = mapY(9);
slide.addShape(pptx.ShapeType.ellipse, {
  x: gx3 - px(4), y: gy9 - px(4), w: px(8), h: px(8),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 1 },
});

// Black horizontal segment from (3,9) to (7,9)
const gx7 = mapX(7);
slide.addShape(pptx.ShapeType.line, {
  x: gx3, y: gy9, w: gx7 - gx3, h: 0,
  line: { color: "000000", width: 1.5 },
});
slide.addText("(7,9)", {
  x: gx7 - px(18), y: gy9 - px(22), w: px(36), h: px(14),
  align: "center", valign: "bottom", fontSize: 9, color: "000000", fontFace: A, margin: 0,
});

// Red dashed lines at x=5 (vertical) and y=1 (horizontal)
// pptxgenjs doesn't support dashed lines well, use short segments
// Vertical dashed at x=5
for (let yv = yMin; yv <= yMax; yv += 0.5) {
  const y1 = mapY(yv);
  const y2 = mapY(yv + 0.25);
  slide.addShape(pptx.ShapeType.line, {
    x: gx5, y: y1, w: 0, h: y2 - y1,
    line: { color: "FF0000", width: 1 },
  });
}
// Horizontal dashed at y=1
for (let xv = xMin; xv <= xMax; xv += 0.5) {
  const x1 = mapX(xv);
  const x2 = mapX(xv + 0.25);
  slide.addShape(pptx.ShapeType.line, {
    x: x1, y: gy1, w: x2 - x1, h: 0,
    line: { color: "FF0000", width: 1 },
  });
}

// ============================================================
// ANNOTATION BOX (red border, white fill, 2 lines)
// Position: x ~ 180-800, y ~ 245-310
// Box: w ~ 620px, h ~ 65px
// ============================================================
const aBoxX = px(180);
const aBoxY = px(245);
const aBoxW = px(620);
const aBoxH = px(65);

slide.addShape(pptx.ShapeType.rect, {
  x: aBoxX, y: aBoxY, w: aBoxW, h: aBoxH,
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 },
});

// Line 1: "X is in between 4.8 and 5.1" (5.1 in red bold)
// Use rich text runs
slide.addText([
  { text: "X is in between 4.8 and ", options: { fontSize: 13, color: "000000", fontFace: A, bold: false } },
  { text: "5.1", options: { fontSize: 13, color: "C00000", fontFace: A, bold: true } },
], {
  x: aBoxX + px(10), y: aBoxY + px(8), w: aBoxW - px(20), h: px(25),
  align: "left", valign: "top", lineSpacing: 1.3, margin: 0,
});

// Line 2: "f(x) is in between 1.04 and 1.01"
slide.addText("f(x) is in between 1.04 and 1.01", {
  x: aBoxX + px(10), y: aBoxY + px(35), w: aBoxW - px(20), h: px(25),
  align: "left", valign: "top", fontSize: 13, color: "000000", fontFace: A, margin: 0,
});

// ============================================================
// BOUNCING LABEL + PURPLE ARROW
// "Bouncing" in purple 7030A0 at x ~ 340-560, y ~ 310-330
// Arrow pointing down/right toward oscillating columns
// ============================================================
const bounceX = px(380);
const bounceY = px(310);
slide.addText("Bouncing", {
  x: bounceX, y: bounceY, w: px(120), h: px(20),
  fontSize: 14, bold: true, color: "7030A0", fontFace: A, margin: 0,
});

// Purple arrow: from near "Bouncing" pointing down/right
// Draw as triangle (arrowhead) + line
const arrowStartX = px(460);
const arrowStartY = px(320);
const arrowEndX = px(520);
const arrowEndY = px(350);
slide.addShape(pptx.ShapeType.line, {
  x: arrowStartX, y: arrowStartY, w: arrowEndX - arrowStartX, h: arrowEndY - arrowStartY,
  line: { color: "7030A0", width: 2 },
});
// Arrowhead (triangle)
slide.addShape(pptx.ShapeType.triangle, {
  x: arrowEndX - px(5), y: arrowEndY - px(5), w: px(10), h: px(10),
  fill: { color: "7030A0" }, line: { color: "7030A0", width: 0 },
  flipV: true, // point down/right
});

// ============================================================
// RED ARROW (left side above main table)
// x ~ 160-170, y ~ 324-348, pointing down/right
// ============================================================
const rArrowStartX = px(165);
const rArrowStartY = px(330);
const rArrowEndX = px(220);
const rArrowEndY = px(370);
slide.addShape(pptx.ShapeType.line, {
  x: rArrowStartX, y: rArrowStartY, w: rArrowEndX - rArrowStartX, h: rArrowEndY - rArrowStartY,
  line: { color: "FF0000", width: 2 },
});
// Arrowhead
slide.addShape(pptx.ShapeType.triangle, {
  x: rArrowEndX - px(5), y: rArrowEndY - px(5), w: px(10), h: px(10),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
  flipV: true,
});

// ============================================================
// MAIN TABLE (8 rows x 17 cols = 1 label + 16 data)
// Position: x ~ 63-893, y ~ 350-530
// Row labels: x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x
// ============================================================
const mTableX = px(63);
const mTableY = px(350);
const mLabelW = px(80);
const mColW = px(50); // 830px / 16 = ~52px per col
const mRowH = px(22); // ~180px / 8 = 22.5px

const rowLabels = [
  "x", "f(x)", "x-delta", "f(x-delta)", "x+delta", "f(x+delta)", "slope", "next x"
];

const rowData = [
  // row 0: x
  [3, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1],
  // row 1: f(x)
  [9, 3.89, 2.96, 2.21, 1.64, 1.25, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01],
  // row 2: x-delta
  [2.9, 3.2, 3.5, 3.8, 4.1, 4.4, 4.7, 5, 4.7, 5, 4.7, 5, 4.7, 5, 4.7, 5],
  // row 3: f(x-delta)
  [5.41, 4.24, 3.25, 2.44, 1.81, 1.36, 1.09, 1, 1.09, 1, 1.09, 1, 1.09, 1, 1.09, 1],
  // row 4: x+delta
  [3.1, 3.4, 3.7, 4, 4.3, 4.6, 4.9, 5.2, 4.9, 5.2, 4.9, 5.2, 4.9, 5.2, 4.9, 5.2],
  // row 5: f(x+delta)
  [4.61, 3.56, 2.69, 2, 1.49, 1.16, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04],
  // row 6: slope
  [-8, -6.8, -5.6, -4.4, -3.2, -2, -0.8, 0.4, -0.8, 0.4, -0.8, 0.4, -0.8, 0.4, -0.8, 0.4],
  // row 7: next x
  [3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8],
];

// Row background colors (from visual_elements colors list)
// #FFFF99, #D9EAD3, #CFE2F3, #D9D9D9, #FCE5CD, #000000 (text color)
// 6 colors for 8 rows - pattern from frame: first 6 rows have colored backgrounds,
// last 2 rows appear to have dark text on white/light bg
const rowBgColors = [
  "FFFF99",  // row 0: x
  "D9EAD3",  // row 1: f(x)
  "CFE2F3",  // row 2: x-delta
  "D9D9D9",  // row 3: f(x-delta)
  "FCE5CD",  // row 4: x+delta
  "FFFFFF",  // row 5: f(x+delta) - frame shows light
  "FFFFFF",  // row 6: slope
  "FFFFFF",  // row 7: next x
];
const rowTextColors = [
  "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000"
];

// Draw table
for (let r = 0; r < 8; r++) {
  const y = mTableY + r * mRowH;
  const bgColor = rowBgColors[r];
  const textColor = rowTextColors[r];
  
  // Label cell
  slide.addShape(pptx.ShapeType.rect, {
    x: mTableX, y: y, w: mLabelW, h: mRowH,
    fill: { color: bgColor }, line: { color: "000000", width: 0.5 },
  });
  slide.addText(rowLabels[r], {
    x: mTableX, y: y, w: mLabelW, h: mRowH,
    align: "center", valign: "middle", fontSize: 10, bold: true,
    color: textColor, fontFace: A, margin: 0,
  });
  
  // Data cells (16 columns)
  for (let c = 0; c < 16; c++) {
    const x = mTableX + mLabelW + c * mColW;
    const val = rowData[r][c];
    const valStr = (val === Math.floor(val)) ? String(val) : val.toFixed(2).replace(/\.00$/, "");
    
    slide.addShape(pptx.ShapeType.rect, {
      x: x, y: y, w: mColW, h: mRowH,
      fill: { color: bgColor }, line: { color: "000000", width: 0.5 },
    });
    slide.addText(valStr, {
      x: x, y: y, w: mColW, h: mRowH,
      align: "center", valign: "middle", fontSize: 9,
      color: textColor, fontFace: A, margin: 0,
    });
  }
}

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));