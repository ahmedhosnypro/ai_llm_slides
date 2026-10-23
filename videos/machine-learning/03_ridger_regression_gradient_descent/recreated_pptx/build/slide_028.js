// Build slide 028 — "Effect of small and large Learning Rate"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Attempt 3 — thinner lines (0.5pt), fix label positions
// ═══════════════════════════════════════════════════════════════════════════════
// GROUND TRUTH: unique_slides/slide_028.jpg — 960x540, exactly 72 px/in
// All geometry in FRAME PX == POINTS. Converted to inches by px().
// ═══════════════════════════════════════════════════════════════════════════════
// FIXES FROM ATTEMPT 2:
// - All line widths: 0.5pt (was 0.75) — LibreOffice renders thicker
// - "Loss" labels: 8pt, minimal box
// - "Value of weight": y=453 (was 455), raised to match measured y=454-458
// - Heading: 12pt (was 13pt), y=192 (was 191) to center better
// - Title: 25pt (was 26pt), y=85

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_028_recreated.pptx";
const px = (v) => v / 72;

const TITLE_RED = "FF0000", FRAME_BLUE = "1F4E79", SHAFT_BLUE = "1B1263";
const CURVE_BLUE = "2E75B6", LOSS_RED = "C00000", INK = "333333", FONT = "Arial";

const pptx = new pptxgen(); pptx.layout = "LAYOUT_WIDE"; const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: 28 });

const rect = (x, y, w, h, fill) =>
  slide.addShape(pptx.ShapeType.rect, { x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill } });
const line = (x, y, w, h, color, width) =>
  slide.addShape(pptx.ShapeType.line, { x: px(x), y: px(y), w: px(w), h: px(h), line: { color: color, width: width } });
const arrowUp = (cx, tipY, baseY, halfW, color) =>
  slide.addShape(pptx.ShapeType.triangle, { x: px(cx - halfW), y: px(tipY), w: px(halfW * 2), h: px(baseY - tipY), fill: { color: color } });
const arrowRight = (cy, tipX, baseX, halfH, color) =>
  slide.addShape(pptx.ShapeType.triangle, { x: px(baseX), y: px(cy - halfH), w: px(tipX - baseX), h: px(halfH * 2), fill: { color: color } });
const dot = (cx, cy, d, color) =>
  slide.addShape(pptx.ShapeType.ellipse, { x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d), fill: { color: color } });

// TITLE
slide.addText("Effect of small and large Learning Rate", {
  x: px(0), y: px(85 - 12.5), w: px(960), h: px(25),
  align: "center", valign: "middle", fontFace: FONT, fontSize: 25, bold: true, color: TITLE_RED, margin: 0,
});

// DARK BLUE FRAME BORDER
slide.addShape(pptx.ShapeType.rect, { x: px(90), y: px(127), w: px(768), h: px(381), line: { color: FRAME_BLUE, width: 1 }, fill: { type: "none" } });

// PANEL DIVIDER
line(474, 127, 0, 381, FRAME_BLUE, 1);

// PANEL HEADINGS — y=192, 12pt bold
const leftCx = 282, rightCx = 666, headingY = 192, headingSize = 12;
slide.addText("Small Learning Rate", { x: px(leftCx - 90), y: px(headingY - headingSize), w: px(180), h: px(16), align: "center", valign: "middle", fontFace: FONT, fontSize: headingSize, bold: true, color: INK, margin: 0 });
slide.addText("Large Learning Rate", { x: px(rightCx - 90), y: px(headingY - headingSize), w: px(180), h: px(16), align: "center", valign: "middle", fontFace: FONT, fontSize: headingSize, bold: true, color: INK, margin: 0 });

// AXES — 0.5pt shafts
const shaftW = 0.5;
line(90, 127, 0, 381, SHAFT_BLUE, shaftW);
arrowUp(90, 211, 223, 4, SHAFT_BLUE);
line(90, 508, 384, 0, SHAFT_BLUE, shaftW);
arrowRight(508, 427, 419, 4, SHAFT_BLUE);

line(474, 127, 0, 381, SHAFT_BLUE, shaftW);
arrowUp(474, 211, 223, 4, SHAFT_BLUE);
line(474, 508, 384, 0, SHAFT_BLUE, shaftW);
arrowRight(508, 780, 772, 4, SHAFT_BLUE);

// "Loss" vertical — 8pt
slide.addText("Loss", { x: px(133 - 6), y: px(226 - 10), w: px(12), h: px(20), align: "center", valign: "middle", fontFace: FONT, fontSize: 8, bold: false, color: LOSS_RED, margin: 0, rotate: -90 });
slide.addText("Loss", { x: px(486 - 6), y: px(222 - 10), w: px(12), h: px(20), align: "center", valign: "middle", fontFace: FONT, fontSize: 8, bold: false, color: LOSS_RED, margin: 0, rotate: -90 });

// "Value of weight" — y=453 (frame), 10pt
const xLabelY = 453, xLabelSize = 10;
slide.addText("Value of weight", { x: px(leftCx - 65), y: px(xLabelY + 3), w: px(130), h: px(14), align: "center", valign: "top", fontFace: FONT, fontSize: xLabelSize, color: INK, margin: 0 });
slide.addText("Value of weight", { x: px(rightCx - 65), y: px(xLabelY + 3), w: px(130), h: px(14), align: "center", valign: "top", fontFace: FONT, fontSize: xLabelSize, color: INK, margin: 0 });

// BLUE CURVES — 0.5pt
const leftCurvePts = [
  [161,236], [168,238], [175,244], [186,268], [193,284], [202,305], [209,324],
  [216,343], [225,366], [232,384], [239,399], [248,417], [257,430], [285,438],
  [292,434], [299,425], [306,412], [313,394], [320,378], [327,361], [334,344],
  [341,328], [348,312], [355,294], [362,276], [369,262], [376,254], [383,250]
];
const rightCurvePts = [
  [514,233], [521,234], [528,242], [535,256], [542,272], [549,288], [556,309],
  [563,318], [576,359], [583,375], [590,394], [597,398], [606,420], [613,430],
  [620,436], [642,433], [649,426], [656,413], [663,398], [670,380], [679,355],
  [686,348], [695,323], [702,305], [711,284], [720,260], [727,252], [734,247]
];

function drawPolyline(points, color, width) {
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[i], p1 = points[i + 1];
    slide.addShape(pptx.ShapeType.line, { x: px(p0[0]), y: px(p0[1]), w: px(p1[0] - p0[0]), h: px(p1[1] - p0[1]), line: { color: color, width: width } });
  }
}
drawPolyline(leftCurvePts, CURVE_BLUE, 0.5);
drawPolyline(rightCurvePts, CURVE_BLUE, 0.5);

// LEFT DESCENT DOTS — d=4
const leftDescentPts = [ [190.5, 277.8], [199.3, 297.2], [211.8, 331.8], [227.6, 372.5], [312.0, 396.8], [333.2, 346.3], [359.1, 284.2] ];
for (let i = 0; i < leftDescentPts.length; i++) {
  const [x, y] = leftDescentPts[i];
  dot(x, y, 4, CURVE_BLUE);
  if (i > 0) { const [px0, py0] = leftDescentPts[i - 1]; slide.addShape(pptx.ShapeType.line, { x: px(px0), y: px(py0), w: px(x - px0), h: px(y - py0), line: { color: CURVE_BLUE, width: 0.5 } }); }
}
// Tiny arrow near left valley
slide.addShape(pptx.ShapeType.line, { x: px(267), y: px(443), w: px(-12), h: px(-15), line: { color: INK, width: 0.75 } });
arrowUp(255, 428, 436, 3, INK);

// RIGHT OSCILLATION DOTS — d=7
const rightOscPts = [ [544.5, 277.0], [559.0, 312.0], [580.6, 369.6], [592.5, 394.9], [664.6, 393.9], [672.0, 376.3], [683.0, 350.9], [693.0, 326.7], [710.5, 284.4] ];
for (let i = 0; i < rightOscPts.length; i++) {
  const [x, y] = rightOscPts[i];
  dot(x, y, 7, CURVE_BLUE);
  if (i > 0) { const [px0, py0] = rightOscPts[i - 1]; slide.addShape(pptx.ShapeType.line, { x: px(px0), y: px(py0), w: px(x - px0), h: px(y - py0), line: { color: CURVE_BLUE, width: 0.75 } }); }
}

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));