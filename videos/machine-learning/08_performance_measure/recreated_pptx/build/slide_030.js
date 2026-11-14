const pptxgenpkg = require("pptxgenjs");

// Slide 30 — "ROC Curve for Same Model -different thresholds" (fresh rebuild, agent-s30-fresh, v3).
// Original frame 960x540 px; 1px = 1pt = 1/72 in. All geometry PIL-measured from
// unique_slides/slide_030.jpg (panels are WHITE-filled with colored borders —
// the pink fills in the v1/v2 builds were a misread of JPEG-washed pixels):
//   outer RED rect x[59,900] y[48,516] fill white
//   blue lines: vert x=342 (y48..516); horiz y=162, y=288, y=401 (x59..635)
//   matrix panels: red border x[60,341] y[48,162] and y[162,288]
//   tan threshold header boxes x[68,173] y[55,78] / y[174,197] (fill F7E7CD)
//   matrix grids: x[116,216], vert x=166; m1 rows y92,112,136,157; m2 rows y212,234,256,279
//   "Predicted as" above each grid: m1 y[78,92], m2 y[198,212]; "Actual" rotated in gutter
//   metrics right of grids: TPR red #C00000, FPR blue #1F497D, bold, x[230,339]
//   ROC plot panel x[641,895] y[81,387] -> asset roc_030_v6.png (254x306 px, gen_030_assets_v6.py)
//   title box x[353,622] y[426,474] white fill blue border, red bold text
//   bottom-right cell x[641,895] y[403,507] white fill blue border; formula box
//   x[649,752] y[415,500]; legend table x[784,880] y[440,500], TP/TN green #92D050,
//   FN/FP grey #F2F2F2
// Drift items (pool_run/spec_gaps.md slide_030): 2D stacked fractions
//   TPR = TP/(TP+FN), FPR = FP/(FP+TN) -> eq_030_v2_*.png (600dpi, TPR red, FPR #1F497D).
// House chrome (root AGENTS.md 2026-10-09): frame first (bg fill), badge+title LAST.

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";
const ASSETS = NS + "/recreated_pptx/build/assets";
const BG = "E8E8E8", RED = "C00000", DBLUE = "0000CC", INK = "000000";
const TAN = "F7E7CD", GREEN = "81FF00", GREY = "F2F2F2", BADGE = "FFF9C4", NUM = "333333";
const CREAM = "F9FCE3";
const FPRBLUE = "1F497D";
const FONT = "Arial";

const P = (px) => px / 72;
const rect = (x0, y0, x1, y1, fill, lineColor, lineW) => s.addShape(pptx.shapes.RECTANGLE, {
  x: P(x0), y: P(y0), w: P(x1 - x0), h: P(y1 - y0),
  fill: { color: fill }, line: { color: lineColor, width: lineW }
});
const hline = (x0, x1, y, color, w) => s.addShape(pptx.shapes.LINE, {
  x: P(x0), y: P(y), w: P(x1 - x0), h: 0, line: { color, width: w }
});
const vline = (x, y0, y1, color, w) => s.addShape(pptx.shapes.LINE, {
  x: P(x), y: P(y0), w: 0, h: P(y1 - y0), line: { color, width: w }
});
const txt = (x0, y0, x1, y1, text, size, color, bold, opts) => s.addText(text, Object.assign({
  x: P(x0), y: P(y0), w: P(x1 - x0), h: P(y1 - y0),
  align: "center", valign: "middle", fontSize: size, bold, color, fontFace: FONT, margin: 0
}, opts || {}));

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE red frame first (fill = bg gray) ---
rect(11, 11, 949, 529, BG, RED, 1.5); // 0.15in,13.03in,7.2in in frame px

// --- outer red content rect ---
rect(59, 48, 900, 516, "FFFFFF", RED, 1.5);

// --- blue structural lines ---
vline(344, 48, 516, DBLUE, 1.25);
vline(635, 48, 516, RED, 1.25);
// right-hand column sits on a light-gray field, not the white left region
rect(636, 48, 899, 516, "E7E9E6", "E7E9E6", 0);
hline(59, 635, 162, DBLUE, 1.25);
hline(59, 635, 288, DBLUE, 1.25);
hline(59, 635, 401, DBLUE, 1.25);

// --- confusion matrix panels ---
function matrixPanel(py, pend, hY, header, ty, rows, cells, coY0, coY1) {
  // py..pend panel (red border, white fill); header tan box at hY; grid at ty with 3 bands
  rect(60, py, 340, pend, "FFFFFF", RED, 1.25);
  rect(68, hY, 173, hY + 23, TAN, RED, 1);
  txt(68, hY, 173, hY + 23, header, 13, RED, true);
  // "Predicted as" above the grid (red in the original)
  txt(116, ty - 14, 216, ty, "Predicted as", 8, RED, true);
  // grid; red row lines run across the gutter (x80..216); red vline separates gutter
  rect(116, ty, 216, rows[2], "FFFFFF", RED, 1);
  vline(166, ty, rows[2], RED, 1);
  vline(80, rows[0], rows[2], RED, 1);
  hline(80, 216, rows[0], RED, 1);
  hline(80, 216, rows[1], RED, 1);
  // column headers P N
  txt(116, ty, 166, rows[0], "P", 10, INK, true);
  txt(166, ty, 216, rows[0], "N", 10, INK, true);
  // gutter: rotated red "Actual" at x[63,75] + P/N row labels at x[82,114]
  txt(44, ty + 37, 94, ty + 49, "Actual", 8, RED, true, { rotate: 270 });
  txt(82, rows[0], 114, rows[1], "P", 10, INK, true);
  txt(82, rows[1], 114, rows[2], "N", 10, INK, true);
  // cell values: [PP, PN, NP, NN] colors [cPP, cPN, cNP, cNN]
  const c = (cx0, cx1, cy0, cy1, t, col) => txt(cx0, cy0, cx1, cy1, t, 13, col, true);
  c(116, 166, rows[0], rows[1], cells[0][0], cells[0][1]);
  c(166, 216, rows[0], rows[1], cells[1][0], cells[1][1]);
  c(116, 166, rows[1], rows[2], cells[2][0], cells[2][1]);
  c(166, 216, rows[1], rows[2], cells[3][0], cells[3][1]);
  // worked metrics on a red-bordered cream callout box: TPR red, FPR blue, 20px pitch
  rect(228, coY0, 338, coY1, CREAM, RED, 1);
  s.addText([
    { text: cells[4], options: { fontSize: 10.5, color: RED, bold: true, fontFace: FONT, breakLine: true } },
    { text: cells[5], options: { fontSize: 10.5, color: FPRBLUE, bold: true, fontFace: FONT, breakLine: true } },
  ], { x: P(232), y: P(coY0 + 5), w: P(334 - 232), h: P(38), margin: 0, lineSpacing: 20 });
}

matrixPanel(48, 162, 55, "Threshold=0.0", 92, [112, 136, 157],
  [["5", RED], ["0", INK], ["6", RED], ["0", INK], "TPR=5/(5+0)=1", "FPR=6/(6+0)=1"], 99, 147);
matrixPanel(162, 288, 174, "Threshold=0.1", 212, [234, 256, 279],
  [["5", RED], ["0", INK], ["4", RED], ["2", INK], "TPR=5/(5+0)=1", "FPR=4/(4+2)=0.66"], 218, 273);

// --- ROC plot panel (generated image, whole panel baked) ---
s.addImage({ path: ASSETS + "/roc_030_v6.png", x: P(641), y: P(81), w: P(254), h: P(306) });

// --- title box (light-gray fill, blue border) ---
rect(353, 426, 622, 474, "E7E9E6", DBLUE, 1.25);
s.addText([
  { text: "ROC Curve for", options: { fontSize: 13, color: RED, bold: true, fontFace: FONT, breakLine: true } },
  { text: "Same Model -different thresholds", options: { fontSize: 13, color: RED, bold: true, fontFace: FONT } },
], { x: P(358), y: P(428), w: P(612 - 358), h: P(42), margin: 0, align: "center", valign: "middle", lineSpacing: 19 });

// --- bottom-right: two separate red-bordered formula boxes (no outer cell rect) ---
rect(651, 416, 749, 456, "FFFFFF", RED, 1);
rect(651, 465, 749, 504, "FFFFFF", RED, 1);
// drift equations as professional 2D fractions (600dpi PNG, exact size)
s.addImage({ path: ASSETS + "/eq_030_v2_tpr.png", x: P(656), y: P(421), w: 728 / 600, h: 230 / 600 });
s.addImage({ path: ASSETS + "/eq_030_v2_fpr.png", x: P(656), y: P(470), w: 725 / 600, h: 230 / 600 });

// --- legend 2x2 key: red lines, x[778,885] y[438,500]; cols 778-803-845-885; rows 438-460-480-500 ---
rect(778, 438, 885, 500, "FFFFFF", RED, 1);
rect(805, 460, 845, 480, "E2F0D9", RED, 0.75);   // TP pale green
rect(845, 480, 885, 500, "66FF33", RED, 0.75);   // TN bright green
vline(803, 438, 500, RED, 0.75);
vline(845, 438, 500, RED, 0.75);
hline(778, 885, 460, RED, 0.75);
hline(778, 885, 480, RED, 0.75);
txt(778, 425, 885, 438, "Predicted as", 7, RED, true);
txt(812, 440, 836, 460, "P", 8, INK, true);
txt(854, 440, 876, 460, "N", 8, INK, true);
txt(779, 460, 795, 480, "P", 8, INK, true);
txt(779, 480, 795, 500, "N", 8, INK, true);
txt(805, 460, 845, 480, "TP", 8, INK, true);
txt(845, 460, 885, 480, "FN", 8, INK, true);
txt(805, 480, 845, 500, "FP", 8, INK, true);
txt(845, 480, 885, 500, "TN", 8, INK, true);
// rotated red "Actual" left of the legend, clear of the P/N row labels
txt(735, 471, 785, 483, "Actual", 8, RED, true, { rotate: 270 });

// --- HOUSE badge + title LAST ---
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("30", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.28, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: RED, fontFace: FONT, margin: 0
});

const outPath = NS + "/recreated_pptx/slide_030_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
