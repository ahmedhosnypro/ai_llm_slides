const pptxgen = require("pptxgenjs");
const path = require("path");

// Slide 24 v6 — "Effect of Selecting Threshold Value on Model Performance"
// Geometry PIL-measured from the original 960x540 frame (1px = 1pt = 1/72 in).
// Aircraft + gauge are verbatim crops from the original frame, embedded 1px=1pt.
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
const GREEN = "D3FBA4";
const WHITE = "FFFFFF";
const PANEL = "FFFACD";
const BLACK = "212121";
const FONT = "Arial";
const P = (px) => px / 72;
const ASSETS = path.join(__dirname, "assets");

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
  fontSize: 25, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- INNER CONTENT PANEL (measured x59-900, y82-500; white fill, thin red border) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(59), y: P(82), w: P(841), h: P(418),
  fill: { color: WHITE }, line: { color: RED, width: 1 },
});

// ---------- UPPER ANNOTATED MATRIX (measured x82-164, y90-136) ----------
const uX = 82, uY = 90, uLabelW = 26, uCellW = 28, uColH = 18, uCellH = 14;
s.addText("Predicted as", {
  x: P(uX + uLabelW), y: P(uY - 8), w: P(uCellW * 2), h: P(8),
  fontSize: 8, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
const uColL = (c) => uX + uLabelW + c * uCellW;
const uRowT = (r) => uY + uColH + r * uCellH;
s.addShape(pptx.shapes.RECTANGLE, { x: P(uColL(0)), y: P(uY), w: P(uCellW), h: P(uColH), fill: { color: WHITE }, line: { color: RED, width: 0.75 } });
s.addShape(pptx.shapes.RECTANGLE, { x: P(uColL(1)), y: P(uY), w: P(uCellW), h: P(uColH), fill: { color: WHITE }, line: { color: RED, width: 0.75 } });
s.addText("P", { x: P(uColL(0)), y: P(uY), w: P(uCellW), h: P(uColH), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: P(uColL(1)), y: P(uY), w: P(uCellW), h: P(uColH), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: P(uX), y: P(uY), w: P(uLabelW), h: P(uColH + uCellH * 2), fill: { color: WHITE }, line: { color: RED, width: 0.75 } });
s.addText("P", { x: P(uX), y: P(uRowT(0)), w: P(uLabelW), h: P(uCellH), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: P(uX), y: P(uRowT(1)), w: P(uLabelW), h: P(uCellH), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", {
  x: P(51), y: P(109), w: P(42), h: P(8), rotate: 270,
  fontSize: 9, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
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

// ---------- LOWER NUMERIC MATRIX (measured x94-229, y155-221; rows 22/22/22) ----------
const lX = 94, lY = 155, lLabelW = 37, lCellW = 49, lColH = 22, lCellH = 22;
s.addText("Predicted as", {
  x: P(lX + lLabelW), y: P(lY - 9), w: P(lCellW * 2), h: P(9),
  fontSize: 9, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
const lColL = (c) => lX + lLabelW + c * lCellW;
const lRowT = (r) => lY + lColH + r * lCellH;
s.addShape(pptx.shapes.RECTANGLE, { x: P(lColL(0)), y: P(lY), w: P(lCellW), h: P(lColH), fill: { color: WHITE }, line: { color: RED, width: 1 } });
s.addShape(pptx.shapes.RECTANGLE, { x: P(lColL(1)), y: P(lY), w: P(lCellW), h: P(lColH), fill: { color: WHITE }, line: { color: RED, width: 1 } });
s.addText("P", { x: P(lColL(0)), y: P(lY), w: P(lCellW), h: P(lColH), fontSize: 12, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: P(lColL(1)), y: P(lY), w: P(lCellW), h: P(lColH), fontSize: 12, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: P(lX), y: P(lY), w: P(lLabelW), h: P(lColH + lCellH * 2), fill: { color: WHITE }, line: { color: RED, width: 1 } });
s.addText("P", { x: P(lX), y: P(lRowT(0)), w: P(lLabelW), h: P(lCellH), fontSize: 12, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: P(lX), y: P(lRowT(1)), w: P(lLabelW), h: P(lCellH), fontSize: 12, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", {
  x: P(64), y: P(195), w: P(44), h: P(8), rotate: 270,
  fontSize: 10, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
// values: 4 blue, 1 red, 1 red, 5 blue (PIL ASCII-map of original glyphs)
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

// ---------- Boxed Threshold=0.5 callout (measured x182-309, y108-135) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(182), y: P(108), w: P(127), h: P(27),
  fill: { color: "F5D2BF" }, line: { color: RED, width: 1.5 },
});
s.addText("Threshold=0.5", {
  x: P(182), y: P(108), w: P(127), h: P(27),
  fontSize: 12, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});

// ---------- PIPELINE PANEL (measured x324-844, y93-198) ----------
const pX = 324, pY = 93, pW = 520, pH = 105;
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: P(pX), y: P(pY), w: P(pW), h: P(pH), fill: { color: PANEL }, line: { color: "C8C8A0", width: 1 }, adj: 0.08 });

function arrowRight(x0, y0, w, h) {
  s.addShape(pptx.shapes.RIGHT_ARROW, {
    x: P(x0), y: P(y0), w: P(w), h: P(h),
    fill: { color: WHITE }, line: { color: RED, width: 1.25 },
  });
}

// Test Sample: box x344-401 y133-166; plane crop inside; label drawn after Model box (z-order)
s.addShape(pptx.shapes.RECTANGLE, { x: P(344), y: P(133), w: P(57), h: P(33), fill: { color: WHITE }, line: { color: "C8B0A8", width: 0.75 } });
s.addImage({ path: path.join(ASSETS, "s24_testplane.png"), x: P(345), y: P(134), w: P(55), h: P(31) });
arrowRight(401, 142, 50, 17);

// Model box: x448-570 y120-180 dark red; gauge crop; yellow caption at bottom
const mX = 448, mY = 120, mW = 122, mH = 60;
s.addShape(pptx.shapes.RECTANGLE, { x: P(mX), y: P(mY), w: P(mW), h: P(mH), fill: { color: DARKRED }, line: { color: DARKRED, width: 1 } });
s.addText("Model", { x: P(mX + 6), y: P(mY + 8), w: P(75), h: P(24), fontSize: 14, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addImage({ path: path.join(ASSETS, "s24_gauge.png"), x: P(530), y: P(128), w: P(36), h: P(34) });
s.addText("[Any value] \u2192 (0, +1)", { x: P(mX + 6), y: P(mY + mH - 14), w: P(mW - 12), h: P(12), fontSize: 8, bold: true, color: YELLOWTXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// two-line label above the input arrow, left of the Model box; drawn after the box so it is not clipped
s.addText("Test\nSample", { x: P(403), y: P(108), w: P(48), h: P(24), fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0, lineSpacing: 11 });
arrowRight(575, 142, 35, 17);

// (0 — 1) blue-bordered box x614-675 y138-160
s.addShape(pptx.shapes.RECTANGLE, { x: P(614), y: P(138), w: P(61), h: P(22), fill: { color: WHITE }, line: { color: BLUE, width: 1.25 } });
s.addText("(0 \u2014 1)", { x: P(614), y: P(138), w: P(61), h: P(22), fontSize: 10, bold: true, color: BLUE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// "Predicted Value" two-line header x569-645 y102-125
s.addText("Predicted\nValue", { x: P(569), y: P(102), w: P(76), h: P(23), fontSize: 10, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0, lineSpacing: 11 });

// Threshold vertical rounded box x691-731 y110-188 (PIL-measured border), rotated text contained inside
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: P(691), y: P(110), w: P(40), h: P(78), fill: { color: "EDBBA4" }, line: { color: RED, width: 1.25 }, adj: 0.15 });
s.addText("Threshold\n(e.g. 0.5)", {
  x: P(672), y: P(129), w: P(78), h: P(40), rotate: 270,
  fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, lineSpacing: 11,
});

// fork arrows to Class I / Class II (red), from box right edge x731 to ovals x761
s.addShape(pptx.shapes.LINE, { x: P(733), y: P(146), w: P(26), h: P(-16), line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: P(756), y: P(128), w: P(9), h: P(10), fill: { color: RED }, line: { type: "none" }, rotate: 315 });
s.addShape(pptx.shapes.LINE, { x: P(733), y: P(168), w: P(26), h: P(6), line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: P(756), y: P(172), w: P(9), h: P(10), fill: { color: RED }, line: { type: "none" }, rotate: 45 });

// Class I oval x761-835 y120-137 / Class II oval x761-833 y166-182
s.addShape(pptx.shapes.OVAL, { x: P(761), y: P(120), w: P(74), h: P(17), fill: { color: "D7E6CF" }, line: { color: "548235", width: 1 } });
s.addText("Class I", { x: P(761), y: P(120), w: P(74), h: P(17), fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: P(761), y: P(166), w: P(72), h: P(16), fill: { color: "E9D7E3" }, line: { color: "7030A0", width: 1 } });
s.addText("Class II", { x: P(761), y: P(166), w: P(72), h: P(16), fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---------- BOTTOM PLOT ----------
// 11 aircraft as verbatim crops from the original frame, at measured bboxes
const planeCrops = [
  ["s24_plane01.png", 328, 222],
  ["s24_plane02.png", 762, 223],
  ["s24_plane03.png", 112, 234],
  ["s24_plane04.png", 196, 285],
  ["s24_plane05.png", 485, 288],
  ["s24_plane06.png", 351, 291],
  ["s24_plane07.png", 633, 295],
  ["s24_plane08.png", 93, 330],
  ["s24_plane09.png", 771, 343],
  ["s24_plane10.png", 208, 361],
  ["s24_plane11.png", 502, 368],
];
const planeSizes = {
  "s24_plane01.png": [99, 62], "s24_plane02.png": [100, 80], "s24_plane03.png": [102, 54],
  "s24_plane04.png": [102, 46], "s24_plane05.png": [102, 54], "s24_plane06.png": [100, 78],
  "s24_plane07.png": [141, 61], "s24_plane08.png": [121, 54], "s24_plane09.png": [103, 58],
  "s24_plane10.png": [83, 45], "s24_plane11.png": [103, 40],
};
for (const [img, cx, cy] of planeCrops) {
  const [cw, ch] = planeSizes[img];
  s.addImage({ path: path.join(ASSETS, img), x: P(cx), y: P(cy), w: P(cw), h: P(ch) });
}

// dashed vertical threshold line x478, y195-449 (runs through the axis to ~14px below, as in original)
for (let yy = 195; yy < 449; yy += 11) {
  s.addShape(pptx.shapes.LINE, { x: P(478), y: P(yy), w: 0, h: P(6), line: { color: "8496B0", width: 1.5 } });
}
// red threshold marker circle center (494,204) r12
s.addShape(pptx.shapes.OVAL, { x: P(482), y: P(192), w: P(24), h: P(24), fill: { color: "F52E43" }, line: { type: "none" } });

// axis: line y435 x58-901 with arrowhead; ticks every 0.1 at x=88+78k; labels 0.0/0.5/1.0
const axL = 85, axR = 889, axY = 435;
s.addShape(pptx.shapes.LINE, { x: P(axL), y: P(axY), w: P(axR - axL), h: 0, line: { color: DARKRED, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: P(879), y: P(429), w: P(11), h: P(12),
  fill: { color: DARKRED }, line: { type: "none" }, rotate: 90,
});
for (let k = 0; k <= 10; k++) {
  const tx = 88 + 78 * k;
  s.addShape(pptx.shapes.LINE, { x: P(tx), y: P(axY - 8), w: 0, h: P(16), line: { color: DARKRED, width: 2 } });
}
const ticks = [{ label: "0.0", x: 88 }, { label: "0.5", x: 478 }, { label: "1.0", x: 868 }];
for (const t of ticks) {
  s.addText(t.label, { x: P(t.x - 20), y: P(442), w: P(40), h: P(20), fontSize: 14, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
}

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_024_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
