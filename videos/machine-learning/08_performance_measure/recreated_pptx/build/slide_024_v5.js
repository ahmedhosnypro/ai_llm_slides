const pptxgen = require("pptxgenjs");

// Slide 24 v4 — "Effect of Selecting Threshold Value on Model Performance"
// Rebuilt against PIL-measured original geometry (960x540 frame, 1px = 1pt = 1/72 in).
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const DARKRED = "8B0000";
const YELLOW = "FFF9C4";
const YELLOWTXT = "FFFF00";
const DARK = "333333";
const BLUE = "0000FF";
const GREEN = "9CF52B";
const PINK = "FFB6C1";
const WHITE = "FFFFFF";
const PANEL = "FFFACD";
const BLACK = "212121";
const GRAYHEAD = "F2F2F2";
const FONT = "Arial";
const P = (px) => px / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// ---------- HOUSE CHROME ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("24", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- UPPER ANNOTATED MATRIX (measured x86-166, y96-144; header text above) ----------
const uX = 86, uY = 96, uLabelW = 23, uCellW = 28, uColH = 15, uCellH = 15, uHeadH = 12;
s.addText("Predicted as", {
  x: P(uX + uLabelW), y: P(uY - uHeadH), w: P(uCellW * 2), h: P(uHeadH),
  fontSize: 9, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
const uColL = (c) => uX + uLabelW + c * uCellW;
const uRowT = (r) => uY + uColH + r * uCellH;
// col heads
s.addShape(pptx.shapes.RECTANGLE, { x: P(uColL(0)), y: P(uY), w: P(uCellW), h: P(uColH), fill: { color: WHITE }, line: { color: RED, width: 0.75 } });
s.addShape(pptx.shapes.RECTANGLE, { x: P(uColL(1)), y: P(uY), w: P(uCellW), h: P(uColH), fill: { color: WHITE }, line: { color: RED, width: 0.75 } });
s.addText("P", { x: P(uColL(0)), y: P(uY), w: P(uCellW), h: P(uColH), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: P(uColL(1)), y: P(uY), w: P(uCellW), h: P(uColH), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// label col
s.addShape(pptx.shapes.RECTANGLE, { x: P(uX), y: P(uY), w: P(uLabelW), h: P(uColH + uCellH * 2), fill: { color: WHITE }, line: { color: RED, width: 0.75 } });
s.addText("P", { x: P(uX), y: P(uRowT(0)), w: P(uLabelW), h: P(uCellH), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: P(uX), y: P(uRowT(1)), w: P(uLabelW), h: P(uCellH), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", {
  x: P(67.5), y: P(122), w: P(30), h: P(8), rotate: 270,
  fontSize: 9, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
// cells: TP green, FN white, FP white, TN green (labels only, no numbers)
const uCells = [
  { lbl: "TP", fill: GREEN, row: 0, col: 0 },
  { lbl: "FN", fill: WHITE, row: 0, col: 1 },
  { lbl: "FP", fill: WHITE, row: 1, col: 0 },
  { lbl: "TN", fill: GREEN, row: 1, col: 1 },
];
for (const c of uCells) {
  const cx = uColL(c.col), cy = uRowT(c.row);
  s.addShape(pptx.shapes.RECTANGLE, { x: P(cx), y: P(cy), w: P(uCellW), h: P(uCellH), fill: { color: c.fill }, line: { color: RED, width: 0.75 } });
  s.addText(c.lbl, { x: P(cx), y: P(cy), w: P(uCellW), h: P(uCellH), fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
}

// ---------- LOWER NUMERIC MATRIX (measured x92-230, y163-243; header above) ----------
const lX = 92, lY = 163, lLabelW = 37, lCellW = 50, lColH = 36, lCellH = 22, lHeadH = 12;
s.addText("Predicted as", {
  x: P(lX + lLabelW), y: P(lY - lHeadH), w: P(lCellW * 2), h: P(lHeadH),
  fontSize: 9, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
const lColL = (c) => lX + lLabelW + c * lCellW;
const lRowT = (r) => lY + lColH + r * lCellH;
s.addShape(pptx.shapes.RECTANGLE, { x: P(lColL(0)), y: P(lY), w: P(lCellW), h: P(lColH), fill: { color: GRAYHEAD }, line: { color: RED, width: 1 } });
s.addShape(pptx.shapes.RECTANGLE, { x: P(lColL(1)), y: P(lY), w: P(lCellW), h: P(lColH), fill: { color: GRAYHEAD }, line: { color: RED, width: 1 } });
s.addText("P", { x: P(lColL(0)), y: P(lY), w: P(lCellW), h: P(lColH), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: P(lColL(1)), y: P(lY), w: P(lCellW), h: P(lColH), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: P(lX), y: P(lY), w: P(lLabelW), h: P(lColH + lCellH * 2), fill: { color: GRAYHEAD }, line: { color: RED, width: 1 } });
s.addText("P", { x: P(lX), y: P(lRowT(0)), w: P(lLabelW), h: P(lCellH), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: P(lX), y: P(lRowT(1)), w: P(lLabelW), h: P(lCellH), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", {
  x: P(61), y: P(217), w: P(44), h: P(8), rotate: 270,
  fontSize: 10, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
// values: 4 blue, 1 red, 1 red, 5 blue
const lVals = [
  { v: "4", color: BLUE, row: 0, col: 0 },
  { v: "1", color: RED, row: 0, col: 1 },
  { v: "1", color: RED, row: 1, col: 0 },
  { v: "5", color: BLUE, row: 1, col: 1 },
];
for (const c of lVals) {
  const cx = lColL(c.col), cy = lRowT(c.row);
  s.addShape(pptx.shapes.RECTANGLE, { x: P(cx), y: P(cy), w: P(lCellW), h: P(lCellH), fill: { color: WHITE }, line: { color: RED, width: 1 } });
  s.addText(c.v, { x: P(cx), y: P(cy), w: P(lCellW), h: P(lCellH), fontSize: 14, bold: true, color: c.color, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
}

// ---------- Boxed Threshold=0.5 callout (measured x181-309, y108-136) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(181), y: P(108), w: P(128), h: P(28),
  fill: { color: "FFF2CC" }, line: { color: RED, width: 1.5 },
});
s.addText("Threshold=0.5", {
  x: P(181), y: P(108), w: P(128), h: P(28),
  fontSize: 12, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});

// ---------- PIPELINE PANEL (measured x324-894, y93-198) ----------
const pX = 324, pY = 93, pW = 570, pH = 105;
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: P(pX), y: P(pY), w: P(pW), h: P(pH), fill: { color: PANEL }, line: { color: "C8C8A0", width: 1 }, adj: 0.08 });

function arrowRight(x0, y0, w, h) {
  s.addShape(pptx.shapes.RIGHT_ARROW, {
    x: P(x0), y: P(y0), w: P(w), h: P(h),
    fill: { color: WHITE }, line: { color: RED, width: 1.25 },
  });
}

// cx, cy, sc in original-frame pixels (960x540); plane body ~0.68*sc px wide
function drawPlane(cx, cy, sc, dotColor) {
  s.addShape(pptx.shapes.OVAL, {
    x: P(cx - 0.34 * sc), y: P(cy - 0.035 * sc), w: P(0.68 * sc), h: P(0.07 * sc),
    fill: { color: "BDBDBD" }, line: { color: "616161", width: 0.75 },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: P(cx - 0.37 * sc), y: P(cy - 0.16 * sc), w: P(0.12 * sc), h: P(0.13 * sc),
    fill: { color: "CFCFCF" }, line: { color: "616161", width: 0.5 },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: P(cx - 0.06 * sc), y: P(cy + 0.02 * sc), w: P(0.24 * sc), h: P(0.13 * sc),
    fill: { color: "CFCFCF" }, line: { color: "616161", width: 0.5 }, rotate: 180,
  });
  s.addShape(pptx.shapes.OVAL, {
    x: P(cx + 0.10 * sc), y: P(cy - 0.045 * sc), w: P(0.09 * sc), h: P(0.09 * sc),
    fill: { color: "E8E8E8" }, line: { color: "616161", width: 0.5 },
  });
  s.addShape(pptx.shapes.OVAL, {
    x: P(cx - 0.035 * sc), y: P(cy - 0.035 * sc), w: P(0.07 * sc), h: P(0.07 * sc),
    fill: { color: dotColor }, line: { type: "none" },
  });
}

// Test Sample: label above box, box x343-395 y137-172 with plane sketch inside
s.addText("Test\nSample", { x: P(330), y: P(103), w: P(78), h: P(26), fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0, lineSpacing: 11 });
s.addShape(pptx.shapes.RECTANGLE, { x: P(343), y: P(137), w: P(52), h: P(35), fill: { color: WHITE }, line: { color: RED, width: 1 } });
drawPlane(369, 154, 30, "9E9E9E");
arrowRight(401, 146, 26, 14);

// Model box: x439-572 y123-181 dark red; white "Model"; purple pie icon; yellow caption inside
const mX = 439, mY = 123, mW = 133, mH = 58;
s.addShape(pptx.shapes.RECTANGLE, { x: P(mX), y: P(mY), w: P(mW), h: P(mH), fill: { color: DARKRED }, line: { color: DARKRED, width: 1 } });
s.addText("Model", { x: P(mX + 6), y: P(mY + 12), w: P(75), h: P(24), fontSize: 14, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// pie icon circle x526-567 y125-175
s.addShape(pptx.shapes.OVAL, { x: P(526), y: P(125), w: P(41), h: P(50), fill: { color: "B4A7D6" }, line: { color: "7030A0", width: 1 } });
s.addShape(pptx.shapes.LINE, { x: P(546), y: P(128), w: P(0), h: P(44), line: { color: "7030A0", width: 1 } });
s.addText("[Any value] \u2192 (0, +1)", { x: P(mX + 6), y: P(mY + mH - 12), w: P(mW - 12), h: P(12), fontSize: 8, bold: true, color: YELLOWTXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
arrowRight(578, 146, 26, 14);

// (0 — 1) blue-bordered box x614-671 y136-155
s.addShape(pptx.shapes.RECTANGLE, { x: P(614), y: P(136), w: P(57), h: P(19), fill: { color: WHITE }, line: { color: BLUE, width: 1.25 } });
s.addText("(0 \u2013 1)", { x: P(614), y: P(136), w: P(57), h: P(19), fontSize: 10, bold: true, color: BLUE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// "Predicted Value" two-line header above the value/threshold stage x569-645 y102-125
s.addText("Predicted\nValue", { x: P(569), y: P(102), w: P(76), h: P(23), fontSize: 10, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0, lineSpacing: 11 });

// Threshold vertical rounded box x691-731 y110-188, rotated text contained inside
const thX = 691, thY = 110, thW = 40, thH = 78;
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: P(thX), y: P(thY), w: P(thW), h: P(thH), fill: { color: "EDD5B3" }, line: { color: RED, width: 1.25 }, adj: 0.15 });
s.addText("Threshold (e.g. 0.5)", {
  x: P(672), y: P(129), w: P(78), h: P(40), rotate: 270,
  fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});

// fork arrows to Class I / Class II (red)
s.addShape(pptx.shapes.LINE, { x: P(733), y: P(146), w: P(42), h: P(-13), line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: P(772), y: P(130), w: P(9), h: P(10), fill: { color: RED }, line: { type: "none" }, rotate: 315 });
s.addShape(pptx.shapes.LINE, { x: P(733), y: P(168), w: P(42), h: P(9), line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: P(772), y: P(174), w: P(9), h: P(10), fill: { color: RED }, line: { type: "none" }, rotate: 45 });

// Class I (green oval x778-854 y123-146) / Class II (pink oval x778-854 y163-186)
s.addShape(pptx.shapes.OVAL, { x: P(778), y: P(123), w: P(76), h: P(23), fill: { color: "D0FFE6" }, line: { color: "548235", width: 1 } });
s.addText("Class I", { x: P(778), y: P(123), w: P(76), h: P(23), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: P(778), y: P(163), w: P(76), h: P(23), fill: { color: "F6CCFA" }, line: { color: "7030A0", width: 1 } });
s.addText("Class II", { x: P(778), y: P(163), w: P(76), h: P(23), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---------- BOTTOM PLOT ----------
// 11 planes at measured centers; 6 red dots, 5 blue dots; skull marks on 3 right-side planes
const planesRed = [[128, 266], [282, 296], [572, 299], [376, 302], [110, 342], [222, 371]];
const planesBlue = [[347, 229], [776, 266], [652, 311], [855, 356], [518, 376]];
const skulls = [[377, 255], [682, 337], [885, 382]];
for (const [px, py] of planesRed) drawPlane(px, py, 110, RED);
for (const [px, py] of planesBlue) drawPlane(px, py, 110, BLUE);
for (const [sx, sy] of skulls) {
  s.addShape(pptx.shapes.OVAL, { x: P(sx - 5), y: P(sy - 5), w: P(10), h: P(10), fill: { color: WHITE }, line: { color: BLACK, width: 1 } });
  s.addShape(pptx.shapes.LINE, { x: P(sx - 4), y: P(sy - 4), w: P(8), h: P(8), line: { color: BLACK, width: 1 } });
  s.addShape(pptx.shapes.LINE, { x: P(sx - 4), y: P(sy + 4), w: P(8), h: P(-8), line: { color: BLACK, width: 1 } });
}

// dashed vertical threshold line at x478, y206-430
const thrLineX = 478;
for (let yy = 206; yy < 430; yy += 11) {
  s.addShape(pptx.shapes.LINE, { x: P(thrLineX), y: P(yy), w: 0, h: P(6), line: { color: "8496B0", width: 1.5 } });
}
// red threshold marker circle cx494 cy207 r12
s.addShape(pptx.shapes.OVAL, { x: P(494 - 12), y: P(207 - 12), w: P(24), h: P(24), fill: { color: "F52E43" }, line: { type: "none" } });

// axis: line y435 x58-901 with arrowhead; ticks every 0.1 at x=86+78.2k; labels 0.0/0.5/1.0
const axL = 58, axR = 901, axY = 435;
s.addShape(pptx.shapes.LINE, { x: P(axL), y: P(axY), w: P(axR - axL), h: 0, line: { color: DARKRED, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: P(893), y: P(430), w: P(10), h: P(10),
  fill: { color: DARKRED }, line: { type: "none" }, rotate: 90,
});
for (let k = 0; k <= 10; k++) {
  const tx = 86 + 78.2 * k;
  s.addShape(pptx.shapes.LINE, { x: P(tx), y: P(axY - 8), w: 0, h: P(16), line: { color: DARKRED, width: 2 } });
}
const ticks = [{ label: "0.0", x: 86 }, { label: "0.5", x: 479 }, { label: "1.0", x: 868 }];
for (const t of ticks) {
  s.addText(t.label, { x: P(t.x - 18), y: P(448), w: P(36), h: P(14), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
}

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_024_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
