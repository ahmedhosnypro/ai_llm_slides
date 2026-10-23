/**
 * Slide 030 build — Convex Function, Learning Rate =0.2, Start at X=3
 * Measured from unique_slides/slide_030.jpg (960x540, 1px=1pt)
 * LAYOUT_WIDE 13.333 x 7.5 in (960x540 pt)
 * House chrome per shared_patterns/house_chrome.js
 */
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";  // 13.333 x 7.5 in

const slide = pres.addSlide();

// Draw house chrome (panel, strokes, badge with numeral "30")
drawHouseChrome(pres, slide, { numeral: "30" });

// Color constants (no # prefix for pptxgenjs)
const COL = {
  // Text
  titleRed: "C00000",
  titleGreen: "008000",
  bodyBlack: "000000",
  formulaRed: "FF0000",
  formulaBlue: "0000FF",
  calloutPurple: "7030A0",
  calloutUnderline: "FF00FF",
  // Tables
  paramBorder: "00B050",
  paramLabelBg: "C6E0B4",
  paramValueBg: "FFFFFF",
  iterBorder: "0070C0",
  iterSlopeBg: "C6E0B4",
  iterStopRed: "FF0000",
  iterStopWhite: "FFFFFF",
  iterRedHighlight: "FF0000",
  // Graph
  graphBg: "FFFFFF",
  gridGray: "D9D9D9",
  parabolaBlue: "0000FF",
  axisRed: "FF0000",
  axisGreen: "00B050",
  axisBlack: "000000",
  // Formula block border (measured GREEN not magenta)
  formulaBorder: "00B050",
  formulaBg: "FFFFFF",
  // Arrow
  arrowRed: "FF0000",
};

const FONT = "Arial";
const PT = 1/72;  // 1pt in inches
const ST = pres.ShapeType;

// ============================================================
// 1. TITLE (top-left, mixed colors)
// Original: y≈55-88, x≈60-530. Text: "Convex Function,  Learning Rate =0.2, Start at X=3"
// Double space after first comma. Bold, largest text.
// Segments: "Convex Function," red | " Learning Rate =0.2," green | " Start at X=3" red
// ============================================================
slide.addText([
  { text: "Convex Function,  ", options: { fontSize: 28, bold: true, color: COL.titleRed, fontFace: FONT } },
  { text: "Learning Rate =0.2,  ", options: { fontSize: 28, bold: true, color: COL.titleGreen, fontFace: FONT } },
  { text: "Start at X=3", options: { fontSize: 28, bold: true, color: COL.titleRed, fontFace: FONT } },
], {
  x: 60 * PT, y: 55 * PT, w: 480 * PT, h: 40 * PT,
  margin: 0, align: "left", valign: "top",
});

// ============================================================
// 2. PARAMETER TABLE (left-middle)
// Original: x≈55-240, y≈150-240. 3 rows x 2 cols.
// Border: green #00B050. Left labels: bg #C6E0B4, text black. Right values: bg white, text black.
// Row1: step | 0.2  Row2: initial X | 3  Row3: delta | 0.1
// ============================================================
const paramRows = [
  [
    { text: "step", options: { fontSize: 14, bold: true, color: COL.bodyBlack, fontFace: FONT, fill: { color: COL.paramLabelBg }, margin: 5 } },
    { text: "0.2", options: { fontSize: 14, color: COL.bodyBlack, fontFace: FONT, fill: { color: COL.paramValueBg }, margin: 5, align: "center" } },
  ],
  [
    { text: "initial X", options: { fontSize: 14, bold: true, color: COL.bodyBlack, fontFace: FONT, fill: { color: COL.paramLabelBg }, margin: 5 } },
    { text: "3", options: { fontSize: 14, color: COL.bodyBlack, fontFace: FONT, fill: { color: COL.paramValueBg }, margin: 5, align: "center" } },
  ],
  [
    { text: "delta", options: { fontSize: 14, bold: true, color: COL.bodyBlack, fontFace: FONT, fill: { color: COL.paramLabelBg }, margin: 5 } },
    { text: "0.1", options: { fontSize: 14, color: COL.bodyBlack, fontFace: FONT, fill: { color: COL.paramValueBg }, margin: 5, align: "center" } },
  ],
];

slide.addTable(paramRows, {
  x: 55 * PT, y: 150 * PT, w: 185 * PT, h: 90 * PT,
  border: { pt: 1.5, color: COL.paramBorder },
});

// ============================================================
// 3. FORMULA BLOCK (center) - GREEN border, white bg
// Original: y=235-280, x=348-552. 3 lines of text.
// Line 1: f(x)=(x-5)^2+1 (black, larger ~20pt)
// Line 2: X = 5 (red, ~20pt)
// Line 3: f(x) Minimum value is 1.0 (black, 1.0 in blue)
// ============================================================
// The formula block has a green border at y=235 and y=280, x=348-552
// That's a box from (348,235) to (552,280) -> w=204pt, h=45pt
// Centered text inside
const formulaBoxX = 348 * PT;
const formulaBoxY = 235 * PT;
const formulaBoxW = 204 * PT;
const formulaBoxH = 45 * PT;

// Draw the box (green border, white fill)
slide.addShape(ST.rect, {
  x: formulaBoxX, y: formulaBoxY, w: formulaBoxW, h: formulaBoxH,
  fill: { color: COL.formulaBg },
  line: { color: COL.formulaBorder, width: 2 },
});

// Add text inside (3 lines, centered)
slide.addText([
  { text: "f(x)=(x-5)^2+1", options: { fontSize: 20, bold: true, color: COL.bodyBlack, fontFace: FONT, breakLine: true } },
  { text: "X = 5", options: { fontSize: 20, bold: true, color: COL.formulaRed, fontFace: FONT, breakLine: true } },
  { text: "f(x) Minimum value is ", options: { fontSize: 18, color: COL.bodyBlack, fontFace: FONT } },
  { text: "1.0", options: { fontSize: 18, color: COL.formulaBlue, fontFace: FONT } },
], {
  x: formulaBoxX, y: formulaBoxY, w: formulaBoxW, h: formulaBoxH,
  align: "center", valign: "middle", margin: 5,
  lineSpacing: 24,  // explicit line spacing for multi-line
});

// ============================================================
// 4. CALLOUT (center-lower) - purple text with magenta underline
// Original: y=300-310, x=346-527. Text: "Reach Minimum after 11 Steps"
// Purple #7030A0, underline magenta #FF00FF
// ============================================================
const calloutY = 302 * PT;
const calloutX = 350 * PT;
const calloutW = 180 * PT;
slide.addText("Reach Minimum after 11 Steps", {
  x: calloutX, y: calloutY, w: calloutW, h: 28 * PT,
  fontSize: 18, bold: true, color: COL.calloutPurple, fontFace: FONT,
  underline: { style: "single", color: COL.calloutUnderline },
  align: "center", valign: "middle", margin: 0,
});

// ============================================================
// 5. GRAPH (top-right) - coordinate grid with parabola, points, lines
// Original: x≈630-910, y≈46-244. Plot area roughly x=650-890, y=60-230
// Axes: x -5 to 15, y -5 to 15. Ticks at -5, 0, 5, 10, 15.
// Blue parabola f(x)=(x-5)^2+1. Red dashed vertical at x=5.
// Green point (5,1) labeled (5,1). Red point (2,10) labeled (2,10).
// Black line (2,10) to (7,1) labeled (7,1). Red point at ~(6.2, 2.44).
// ============================================================
// Plot area in slide coordinates:
// x: 650pt to 890pt (240pt wide) maps to x: -5 to 15 (20 units) -> 12pt per unit
// y: 60pt to 230pt (170pt tall) maps to y: -5 to 15 (20 units) -> 8.5pt per unit (inverted)

const plotX = 650 * PT;
const plotY = 60 * PT;
const plotW = 240 * PT;
const plotH = 170 * PT;
const xScale = 12;  // pt per x unit
const yScale = 8.5; // pt per y unit (inverted: y increases down)

// Grid background
slide.addShape(ST.rect, {
  x: plotX, y: plotY, w: plotW, h: plotH,
  fill: { color: COL.graphBg },
  line: { color: COL.gridGray, width: 0.5 },
});

// Grid lines (light gray)
for (let xi = -5; xi <= 15; xi += 5) {
  const px = plotX + (xi + 5) * xScale * PT;
  slide.addShape(ST.line, {
    x: px, y: plotY, w: 0, h: plotH,
    line: { color: COL.gridGray, width: 0.5, dashType: "sysDash" },
  });
  // Tick label
  slide.addText(String(xi), {
    x: px - 15 * PT, y: plotY + plotH + 3 * PT, w: 30 * PT, h: 14 * PT,
    fontSize: 10, color: COL.bodyBlack, fontFace: FONT, align: "center", margin: 0,
  });
}
for (let yi = -5; yi <= 15; yi += 5) {
  const py = plotY + plotH - (yi + 5) * yScale * PT;
  slide.addShape(ST.line, {
    x: plotX, y: py, w: plotW, h: 0,
    line: { color: COL.gridGray, width: 0.5, dashType: "sysDash" },
  });
  // Tick label
  slide.addText(String(yi), {
    x: plotX - 30 * PT, y: py - 7 * PT, w: 28 * PT, h: 14 * PT,
    fontSize: 10, color: COL.bodyBlack, fontFace: FONT, align: "right", valign: "middle", margin: 0,
  });
}

// Axis labels
slide.addText("x", {
  x: plotX + plotW/2 - 10 * PT, y: plotY + plotH + 18 * PT, w: 20 * PT, h: 14 * PT,
  fontSize: 12, bold: true, color: COL.bodyBlack, fontFace: FONT, align: "center", margin: 0,
});
slide.addText("f(x)", {
  x: plotX - 35 * PT, y: plotY + plotH/2 - 10 * PT, w: 30 * PT, h: 20 * PT,
  fontSize: 12, bold: true, color: COL.bodyBlack, fontFace: FONT, align: "center", margin: 0,
});

// Parabola: f(x) = (x-5)^2 + 1
// Sample points and draw as polyline (smooth curve approximation)
const parabolaPts = [];
for (let xi = -5; xi <= 15; xi += 0.2) {
  const yi = Math.pow(xi - 5, 2) + 1;
  const px = plotX + (xi + 5) * xScale * PT;
  const py = plotY + plotH - (yi + 5) * yScale * PT;
  if (py >= plotY && py <= plotY + plotH) {
    parabolaPts.push({ x: px, y: py });
  }
}
// Draw as series of small line segments (pptxgenjs doesn't have polyline)
for (let i = 0; i < parabolaPts.length - 1; i++) {
  const p1 = parabolaPts[i];
  const p2 = parabolaPts[i+1];
  slide.addShape(ST.line, {
    x: p1.x, y: p1.y, w: p2.x - p1.x, h: p2.y - p1.y,
    line: { color: COL.parabolaBlue, width: 2 },
  });
}

// Red dashed vertical line at x=5
const vx5 = plotX + (5 + 5) * xScale * PT;
slide.addShape(ST.line, {
  x: vx5, y: plotY, w: 0, h: plotH,
  line: { color: COL.axisRed, width: 1.5, dashType: "sysDash" },
});

// Points and labels
// (5,1) - green point
const px_5_1 = plotX + (5 + 5) * xScale * PT;
const py_5_1 = plotY + plotH - (1 + 5) * yScale * PT;
slide.addShape(ST.ellipse, {
  x: px_5_1 - 4 * PT, y: py_5_1 - 4 * PT, w: 8 * PT, h: 8 * PT,
  fill: { color: COL.axisGreen }, line: { color: COL.axisGreen, width: 1 },
});
slide.addText("(5,1)", {
  x: px_5_1 + 6 * PT, y: py_5_1 - 12 * PT, w: 40 * PT, h: 14 * PT,
  fontSize: 11, color: COL.axisGreen, fontFace: FONT, bold: true, margin: 0,
});

// (2,10) - red point
const px_2_10 = plotX + (2 + 5) * xScale * PT;
const py_2_10 = plotY + plotH - (10 + 5) * yScale * PT;
slide.addShape(ST.ellipse, {
  x: px_2_10 - 4 * PT, y: py_2_10 - 4 * PT, w: 8 * PT, h: 8 * PT,
  fill: { color: COL.axisRed }, line: { color: COL.axisRed, width: 1 },
});
slide.addText("(2,10)", {
  x: px_2_10 - 45 * PT, y: py_2_10 - 12 * PT, w: 45 * PT, h: 14 * PT,
  fontSize: 11, color: COL.axisRed, fontFace: FONT, bold: true, align: "right", margin: 0,
});

// (7,1) - black line endpoint with label
const px_7_1 = plotX + (7 + 5) * xScale * PT;
const py_7_1 = plotY + plotH - (1 + 5) * yScale * PT;
slide.addText("(7,1)", {
  x: px_7_1 + 6 * PT, y: py_7_1 - 12 * PT, w: 40 * PT, h: 14 * PT,
  fontSize: 11, color: COL.axisBlack, fontFace: FONT, bold: true, margin: 0,
});

// Black line segment from (2,10) to (7,1)
slide.addShape(ST.line, {
  x: px_2_10, y: py_2_10, w: px_7_1 - px_2_10, h: py_7_1 - py_2_10,
  line: { color: COL.axisBlack, width: 2 },
});

// Unlabeled red point at intersection (~6.2, 2.44)
const ix = 6.2;
const iy = Math.pow(ix - 5, 2) + 1; // 2.44
const px_int = plotX + (ix + 5) * xScale * PT;
const py_int = plotY + plotH - (iy + 5) * yScale * PT;
slide.addShape(ST.ellipse, {
  x: px_int - 4 * PT, y: py_int - 4 * PT, w: 8 * PT, h: 8 * PT,
  fill: { color: COL.axisRed }, line: { color: COL.axisRed, width: 1 },
});

// ============================================================
// 6. RED DOWN ARROW (between param table and iter table)
// Original: x≈140-200, y≈235-300. Solid red block arrow pointing down.
// ============================================================
// Draw as triangle (arrowhead) + rectangle (shaft)
const arrowX = 170 * PT;  // center x
const arrowY = 250 * PT;  // top y
const arrowW = 30 * PT;
const arrowH = 70 * PT;
// Shaft
slide.addShape(ST.rect, {
  x: arrowX - arrowW/2, y: arrowY, w: arrowW, h: arrowH * 0.7,
  fill: { color: COL.arrowRed }, line: { color: COL.arrowRed, width: 0 },
});
// Arrowhead (triangle pointing down)
slide.addShape(ST.triangle, {
  x: arrowX - arrowW, y: arrowY + arrowH * 0.7, w: arrowW * 2, h: arrowH * 0.3,
  fill: { color: COL.arrowRed }, line: { color: COL.arrowRed, width: 0 },
});

// ============================================================
// 7. ITERATION TABLE (bottom) - 8 rows x 12 cols
// Original: x≈57-902, y≈375-528. Blue border #0070C0.
// Row 1 (x): 3 | 3.2 | 3.4 | 3.6 | 3.8 | 4 | 4.2 | 4.4 | 4.6 | 4.8 | 5  (3 and 5 red)
// Row 2 (f(x)): 5 | 4.24 | 3.56 | 2.96 | 2.44 | 2 | 1.64 | 1.36 | 1.16 | 1.04 | 1
// Row 3 (x-delta): 2.9 | 3.1 | 3.3 | 3.5 | 3.7 | 3.9 | 4.1 | 4.3 | 4.5 | 4.7 | 4.9
// Row 4 (f(x-delta)): 5.41 | 4.61 | 3.89 | 3.25 | 2.69 | 2.21 | 1.81 | 1.49 | 1.25 | 1.09 | 1.01
// Row 5 (x+delta): 3.1 | 3.3 | 3.5 | 3.7 | 3.9 | 4.1 | 4.3 | 4.5 | 4.7 | 4.9 | 5.1
// Row 6 (f(x+delta)): 4.61 | 3.89 | 3.25 | 2.69 | 2.21 | 1.81 | 1.49 | 1.25 | 1.09 | 1.01 | 1.01
// Row 7 (slope): -8 | -7.2 | -6.4 | -5.6 | -4.8 | -4 | -3.2 | -2.4 | -1.6 | -0.8 | 0 (green tint)
// Row 8 (next x): 3.2 | 3.4 | 3.6 | 3.8 | 4 | 4.2 | 4.4 | 4.6 | 4.8 | 5 | stop (stop: red bg, white text)
// ============================================================
const iterData = [
  // Header row (labels)
  ["x", "3", "3.2", "3.4", "3.6", "3.8", "4", "4.2", "4.4", "4.6", "4.8", "5"],
  ["f(x)", "5", "4.24", "3.56", "2.96", "2.44", "2", "1.64", "1.36", "1.16", "1.04", "1"],
  ["x-delta", "2.9", "3.1", "3.3", "3.5", "3.7", "3.9", "4.1", "4.3", "4.5", "4.7", "4.9"],
  ["f(x-delta)", "5.41", "4.61", "3.89", "3.25", "2.69", "2.21", "1.81", "1.49", "1.25", "1.09", "1.01"],
  ["x+delta", "3.1", "3.3", "3.5", "3.7", "3.9", "4.1", "4.3", "4.5", "4.7", "4.9", "5.1"],
  ["f(x+delta)", "4.61", "3.89", "3.25", "2.69", "2.21", "1.81", "1.49", "1.25", "1.09", "1.01", "1.01"],
  ["slope", "-8", "-7.2", "-6.4", "-5.6", "-4.8", "-4", "-3.2", "-2.4", "-1.6", "-0.8", "0"],
  ["next x", "3.2", "3.4", "3.6", "3.8", "4", "4.2", "4.4", "4.6", "4.8", "5", "stop"],
];

const iterRows = iterData.map((row, ri) => {
  return row.map((cell, ci) => {
    const isHeader = (ri === 0);
    const isLabelCol = (ci === 0);
    const isSlopeRow = (ri === 6);
    const isStopCell = (ri === 7 && ci === 11);
    const isRedHighlight = (ri === 0 && (ci === 1 || ci === 11));  // 3 and 5 in x row
    
    let opts = {
      fontSize: 9,
      fontFace: FONT,
      color: COL.bodyBlack,
      margin: 2,
      align: isLabelCol ? "left" : "center",
      valign: "middle",
    };
    
    if (isHeader) {
      opts.bold = true;
      opts.fontSize = 9;
    }
    if (isLabelCol) {
      opts.bold = true;
    }
    if (isSlopeRow && !isLabelCol) {
      opts.fill = { color: COL.iterSlopeBg };
    }
    if (isStopCell) {
      opts.fill = { color: COL.iterStopRed };
      opts.color = COL.iterStopWhite;
      opts.bold = true;
    }
    if (isRedHighlight) {
      opts.color = COL.iterRedHighlight;
      opts.bold = true;
    }
    
    return { text: cell, options: opts };
  });
});

const iterTableX = 57 * PT;
const iterTableY = 375 * PT;
const iterTableW = 845 * PT;
const iterTableH = 153 * PT;

slide.addTable(iterRows, {
  x: iterTableX, y: iterTableY, w: iterTableW, h: iterTableH,
  border: { pt: 1.5, color: COL.iterBorder },
  // rowHeights handled by content
});

// ============================================================
// Write output
// ============================================================
const outPath = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_030_recreated.pptx";
pres.writeFile(outPath).then(() => {
  console.log("Written:", outPath);
}).catch(err => {
  console.error("Error:", err);
  process.exit(1);
});