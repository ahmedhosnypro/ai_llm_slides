const pptxgen = require("pptxgenjs");

// Slide 24 v2 — "Effect of Selecting Threshold Value on Model Performance"
// Rebuilt against PIL-measured original geometry (960x540 frame, 1px = 1pt = 1/72 in).
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const DARKRED = "8B0000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE = "0000FF";
const GREEN = "90EE90";
const PINK = "FFB6C1";
const WHITE = "FFFFFF";
const PANEL = "FFFACD";
const BLACK = "212121";
const FONT = "Arial";

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

// ---------- DETAILED CONFUSION MATRIX (top-left) ----------
// original: header 'Predicted as' y~52-76; col heads P/N y~88-100; cells y~104-140;
// row labels P/N x~75-90; 'Actual' left. Convert px->in (/72).
const dX = 60 / 72, dY = 50 / 72;
const dLabelW = 24 / 72, dCellW = 55 / 72, dHeadH = 22 / 72, dColH = 16 / 72, dCellH = 34 / 72;
const dCellTop = (r) => dY + dHeadH + dColH + r * dCellH;
const dColLeft = (c) => dX + dLabelW + c * dCellW;

s.addText("Predicted as", {
  x: dX + dLabelW, y: dY, w: dCellW * 2, h: dHeadH,
  fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addText("P", { x: dColLeft(0), y: dY + dHeadH, w: dCellW, h: dColH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: dColLeft(1), y: dY + dHeadH, w: dCellW, h: dColH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: dX, y: dY + dHeadH + dColH, w: dLabelW, h: dCellH * 2, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("P", { x: dX, y: dCellTop(0), w: dLabelW, h: dCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: dX, y: dCellTop(1), w: dLabelW, h: dCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// cells: TP=4 green, FN=1 pink (row 0); FP=1 pink, TN=5 green (row 1)
const dCells = [
  { lbl: "TP", val: "4", fill: GREEN, row: 0, col: 0 },
  { lbl: "FN", val: "1", fill: PINK, row: 0, col: 1 },
  { lbl: "FP", val: "1", fill: PINK, row: 1, col: 0 },
  { lbl: "TN", val: "5", fill: GREEN, row: 1, col: 1 },
];
for (const c of dCells) {
  const cx = dColLeft(c.col), cy = dCellTop(c.row);
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: dCellW, h: dCellH, fill: { color: c.fill }, line: { color: BLACK, width: 0.75 } });
  s.addText(c.lbl + "\n" + c.val, {
    x: cx, y: cy, w: dCellW, h: dCellH,
    fontSize: 9, bold: true, color: BLACK, fontFace: FONT,
    align: "center", valign: "middle", margin: 0, lineSpacing: 12,
  });
}

// ---------- NUMERIC CONFUSION MATRIX directly beneath ----------
// original: 'Predicted as' y~176-190, col heads y~196-208, cells y~214-246
const nX = 66 / 72, nY = 172 / 72;
const nLabelW = 22 / 72, nCellW = 60 / 72, nHeadH = 16 / 72, nColH = 14 / 72, nCellH = 18 / 72;
const nTop = (r) => nY + nHeadH + nColH + r * nCellH;
s.addText("Predicted as", {
  x: nX + nLabelW, y: nY, w: nCellW * 2, h: nHeadH,
  fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addText("P", { x: nX + nLabelW, y: nY + nHeadH, w: nCellW, h: nColH, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nX + nLabelW + nCellW, y: nY + nHeadH, w: nCellW, h: nColH, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: nX, y: nY + nHeadH + nColH, w: nLabelW, h: nCellH * 2, fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("P", { x: nX, y: nTop(0), w: nLabelW, h: nCellH, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nX, y: nTop(1), w: nLabelW, h: nCellH, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
const nVals = [["4", "1"], ["1", "5"]];
for (let r = 0; r < 2; r++) {
  for (let c = 0; c < 2; c++) {
    const cx = nX + nLabelW + c * nCellW, cy = nTop(r);
    s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: nCellW, h: nCellH, fill: { color: WHITE }, line: { color: RED, width: 1 } });
    s.addText(nVals[r][c], { x: cx, y: cy, w: nCellW, h: nCellH, fontSize: 11, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  }
}

// ---------- Boxed Threshold=0.5 callout (original red outline x178-312 y105-138) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 178 / 72, y: 105 / 72, w: 134 / 72, h: 33 / 72,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
s.addText("Threshold=0.5", {
  x: 178 / 72, y: 105 / 72, w: 134 / 72, h: 33 / 72,
  fontSize: 12, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});

// ---------- PIPELINE PANEL (cream) ----------
// original cream panel approx x113-893, y56-198 -> in
const pX = 328 / 72, pY = 56 / 72, pW = 576 / 72, pH = 142 / 72;
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: pX, y: pY, w: pW, h: pH, fill: { color: PANEL }, line: { color: "C8C8A0", width: 1 }, adj: 0.08 });

const fy = 128 / 72; // flow center line y~128px
const bh = 40 / 72;
const aw = 22 / 72;

function arrowRight(x0, y) {
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: y - 0.02, w: aw, h: 0.04, fill: { color: BLACK }, line: { type: "none" } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x0 + aw - 0.02, y: y - 0.06, w: 0.10, h: 0.12, fill: { color: BLACK }, line: { type: "none" }, rotate: 90 });
}

function drawPlane(cx, cy, sc, dotColor) {
  s.addShape(pptx.shapes.OVAL, {
    x: cx - 0.34 * sc, y: cy - 0.035 * sc, w: 0.68 * sc, h: 0.07 * sc,
    fill: { color: "BDBDBD" }, line: { color: "616161", width: 0.75 },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 0.37 * sc, y: cy - 0.16 * sc, w: 0.12 * sc, h: 0.13 * sc,
    fill: { color: "CFCFCF" }, line: { color: "616161", width: 0.5 },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 0.06 * sc, y: cy + 0.02 * sc, w: 0.24 * sc, h: 0.13 * sc,
    fill: { color: "CFCFCF" }, line: { color: "616161", width: 0.5 }, rotate: 180,
  });
  s.addShape(pptx.shapes.OVAL, {
    x: cx + 0.10 * sc, y: cy - 0.045 * sc, w: 0.09 * sc, h: 0.09 * sc,
    fill: { color: "E8E8E8" }, line: { color: "616161", width: 0.5 },
  });
  s.addShape(pptx.shapes.OVAL, {
    x: cx - 0.035 * sc, y: cy - 0.035 * sc, w: 0.07 * sc, h: 0.07 * sc,
    fill: { color: dotColor }, line: { type: "none" },
  });
}

// Test Sample: label above box (y~66), airplane inside box (x~330-435, y~104-168)
const tsX = 330 / 72, tsW = 105 / 72;
s.addText("Test Sample", { x: tsX, y: 64 / 72, w: tsW, h: 16 / 72, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: tsX, y: fy - bh / 2, w: tsW, h: bh, fill: { color: WHITE }, line: { color: RED, width: 1 } });
drawPlane(tsX + tsW / 2, fy, 0.85, BLUE);
arrowRight(tsX + tsW, fy);

// Model box: dark red fill x408-610 y120-180, white bold "Model", purple pie icon right side
const mX = 408 / 72, mY = 120 / 72, mW = 202 / 72, mH = 60 / 72;
s.addShape(pptx.shapes.RECTANGLE, { x: mX, y: mY, w: mW, h: mH, fill: { color: DARKRED }, line: { color: DARKRED, width: 1 } });
s.addText("Model", { x: mX, y: mY, w: 120 / 72, h: mH, fontSize: 14, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// purple pie-chart icon at x531-565 y131-156
s.addShape(pptx.shapes.PIE, {
  x: 531 / 72, y: 131 / 72, w: 34 / 72, h: 25 / 72,
  fill: { color: "B4A7D6" }, line: { color: "7030A0", width: 1 },
  startAngle: 0, endAngle: 270,
});
s.addText("[Any value] \u2014 (0, +1)", { x: mX, y: mY + mH + 0.04, w: mW, h: 16 / 72, fontSize: 8, color: BLACK, fontFace: FONT, align: "center", margin: 0 });

arrowRight(mX + mW, fy);
// '(0 \u2014 1)' label on the arrow, above it (original y~107-123 x~555-620)
s.addText("(0 \u2014 1)", { x: 548 / 72, y: 100 / 72, w: 80 / 72, h: 18 / 72, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });

// 'Predicted Value' header above the threshold/value stage (original ~x575-655 y~70-86, dark red)
s.addText("Predicted Value", { x: 560 / 72, y: 68 / 72, w: 110 / 72, h: 18 / 72, fontSize: 10, bold: true, color: DARKRED, fontFace: FONT, align: "center", margin: 0 });

// Threshold (e.g. 0.5) box: two lines inside (x~655-770)
const thX = 655 / 72, thW = 115 / 72;
s.addShape(pptx.shapes.RECTANGLE, { x: thX, y: fy - bh / 2, w: thW, h: bh, fill: { color: WHITE }, line: { color: RED, width: 1.25 } });
s.addText("Threshold\n(e.g. 0.5)", { x: thX, y: fy - bh / 2, w: thW, h: bh, fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, lineSpacing: 12 });

// branch arrows to Class I / Class II (fork at x~770)
const forkX = thX + thW;
const ciX = 795 / 72, ciW = 85 / 72;
s.addShape(pptx.shapes.LINE, { x: forkX + 0.03, y: fy - 0.08, w: ciX - forkX - 0.12, h: -(fy - 0.08 - (pY + 0.45)), line: { color: BLACK, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: ciX - 0.11, y: pY + 0.39, w: 0.10, h: 0.12, fill: { color: BLACK }, line: { type: "none" }, rotate: 90 });
s.addShape(pptx.shapes.LINE, { x: forkX + 0.03, y: fy + 0.08, w: ciX - forkX - 0.12, h: (pY + 1.48) - (fy + 0.08), line: { color: BLACK, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: ciX - 0.11, y: pY + 1.42, w: 0.10, h: 0.12, fill: { color: BLACK }, line: { type: "none" }, rotate: 90 });

// Class I (light green oval, upper ~y107-135) / Class II (pink oval, lower ~y163-191)
s.addShape(pptx.shapes.OVAL, { x: ciX, y: 104 / 72, w: ciW, h: 32 / 72, fill: { color: "98FB98" }, line: { color: "548235", width: 1 } });
s.addText("Class I", { x: ciX, y: 104 / 72, w: ciW, h: 32 / 72, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: ciX, y: 160 / 72, w: ciW, h: 32 / 72, fill: { color: PINK }, line: { color: "C55A11", width: 1 } });
s.addText("Class II", { x: ciX, y: 160 / 72, w: ciW, h: 32 / 72, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---------- BOTTOM PLOT ----------
// original: axis row y=435, x58-901; ticks every ~0.1 (x58 + k*84.3); labels 0.0/0.5/1.0 at x~60/482/900 y~448-462;
// dashed blue line x~487 y195-430; red circle cx494 cy204 r~12; planes measured.
const axL = 58 / 72, axR = 901 / 72, axY = 435 / 72;
const thrX = 487 / 72;

s.addText("Predicted", { x: axL, y: axY - 24 / 72, w: 70 / 72, h: 16 / 72, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "left", margin: 0 });

// airplanes at measured centers (cx, cy in px); blue decal only on right-of-threshold planes
const planesPlain = [
  [377, 252], [163, 260], [246, 307], [153, 356], [249, 383], [126, 443],
];
const planesBlue = [[553, 387], [822, 372]];
for (const [px, py] of planesPlain) drawPlane(px / 72, py / 72, 1.15, "9E9E9E");
for (const [px, py] of planesBlue) drawPlane(px / 72, py / 72, 1.15, BLUE);

// dashed vertical line at x=475 from y206 down to the axis
const thrLineX = 475 / 72;
for (let yy = 206 / 72; yy < axY - 0.05; yy += 11 / 72) {
  s.addShape(pptx.shapes.LINE, { x: thrLineX, y: yy, w: 0, h: 6 / 72, line: { color: "8496B0", width: 1.5 } });
}
// red threshold circle cx494 cy215 r~12px
s.addShape(pptx.shapes.OVAL, { x: (494 - 12) / 72, y: (215 - 12) / 72, w: 24 / 72, h: 24 / 72, fill: { color: "FF0000" }, line: { type: "none" } });

// dark-red horizontal axis with arrowhead at right end, ticks every 0.1, labels 0.0/0.5/1.0
s.addShape(pptx.shapes.LINE, { x: axL, y: axY, w: axR - axL, h: 0, line: { color: DARKRED, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: (901 - 8) / 72, y: (435 - 5) / 72, w: 16 / 72, h: 10 / 72,
  fill: { color: DARKRED }, line: { type: "none" }, rotate: 90,
});
for (let k = 0; k <= 10; k++) {
  const tx = axL + (axR - axL) * k / 10;
  s.addShape(pptx.shapes.LINE, { x: tx, y: axY - 0.08, w: 0, h: 0.16, line: { color: DARKRED, width: 2 } });
}
const ticks = [{ label: "0.0", x: axL }, { label: "0.5", x: 475 / 72 }, { label: "1.0", x: axR }];
for (const t of ticks) {
  s.addText(t.label, { x: t.x - 0.25, y: axY + 0.12, w: 0.50, h: 0.26, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
}

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_024_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
