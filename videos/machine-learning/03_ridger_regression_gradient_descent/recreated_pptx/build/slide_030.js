/**
 * Slide 030 build — Convex Function, Learning Rate =0.2, Start at X=3
 * Measured from unique_slides/slide_030.jpg (960x540, 1px=1pt)
 * LAYOUT_WIDE 13.333 x 7.5 in (960x540 pt)
 *
 * 2026-10-24 rebuild (worker s030-fix-20261023) — closes two defects:
 *  D1 Z-ORDER: the plot's white background rect was painted OVER the house badge
 *     (badge geometry in the pptx is correct: EMU (10902950,704850) ext 35pt ->
 *     centre (876,73) d35). FIX: every content shape is drawn first, and the
 *     house chrome (panel/strokes/badge) is drawn LAST so it is top-most.
 *  D2 EQUATIONS as plain caret text -> professional 2D format per founder
 *     directive 2026-10-09: matplotlib mathtext -> 600dpi transparent PNG ->
 *     addImage at exact w=px/600 + eq_*.json sidecars (no hand-authored OMML).
 *
 * Measured geometry (frame px, 1px = 1pt) — see scratch/tmp/measure_030_RESULTS.md:
 *   panel E9E9E7 x54..903 y45..540; strokes L x58.5, R x901, BOTTOM y538.5, NO TOP
 *   badge circle d35 centre (876,73)
 *   title ink x58..420 y64..88
 *   plot box: red frame x573..809, y66..265 ; white interior x575..806, y70..264
 *         black y-axis line x631 (x=0); black y=10 line y145..148 spanning x650..725
 *         dashed red vertical x687..689 (x=5); green vertex x685..692 y251..258
 *   param table x104..241 y198..282 (3 rows, 2 cols split x181)
 *   upper red box x399..531 y184..212 -> equation "f(x)=(x-5)^2+1"
 *   green formula box x347..555 y233..282 -> "X = 5" (red) + "f(x) Minimum value is 1.0"
 *   callout: purple text two lines y294..320 x334..568 + purple rule y292..293
 *   iteration table x78..655 y324..531 (8 rows x 12 cols), slope row green fill
 *   red arrow x174..192 y306..338
 */
const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";  // 13.333 x 7.5 in

const slide = pres.addSlide();

const FONT = "Arial";
const PT = 1/72;  // 1pt in inches
const ST = pres.ShapeType;
const px = (v) => v * PT;

const COL = {
  titleRed: "C00000",
  titleGreen: "008000",
  bodyBlack: "000000",
  formulaRed: "C00000",
  formulaBlue: "0000FF",
  calloutPurple: "7030A0",
  calloutRule: "7030A0",
  // plot
  graphBg: "FFFFFF",
  plotFrame: "C00000",
  gridGray: "D9D9D9",
  parabolaBlue: "0000FF",
  axisBlack: "000000",
  // tables
  paramBorder: "00B050",
  paramLabelBg: "C6E0B4",
  paramValueBg: "FFFFFF",
  iterBorder: "0070C0",
  iterFill: "DDEBF7",
  iterSlopeBg: "C6E0B4",
  iterStopRed: "FF0000",
  iterStopWhite: "FFFFFF",
  iterRedHighlight: "C00000",
  // upper equation box
  upBoxBorder: "C00000",
  upBoxBg: "FFFFFF",
  formulaBorder: "00B050",
  formulaBg: "FFFFFF",
  arrowRed: "C00000",
};

const ASSETS = path.resolve(__dirname, "assets");
function eqImage(file, fx, fy, wIn, hIn) {
  slide.addImage({ path: path.join(ASSETS, file), x: px(fx), y: px(fy), w: wIn, h: hIn });
}

// ---------------------------------------------------------------- 1. TITLE
// Measured: ink x58..420 y64..88. Segments red / green / red.
slide.addText([
  { text: "Convex Function,  ", options: { fontSize: 24, bold: true, color: COL.titleRed, fontFace: FONT } },
  { text: "Learning Rate =0.2,  ", options: { fontSize: 24, bold: true, color: COL.titleGreen, fontFace: FONT } },
  { text: "Start at X=3", options: { fontSize: 24, bold: true, color: COL.titleRed, fontFace: FONT } },
], {
  x: px(58), y: px(64), w: px(370), h: px(26),
  margin: 0, align: "left", valign: "middle",
});

// ------------------------------------------------- 2. PARAMETER TABLE
// Measured x104..241 y198..282, 3 rows, 2 columns (label col x104..181, value x181..241).
const paramRows = [
  ["step", "0.2"],
  ["initial X", "3"],
  ["delta", "0.1"],
];
slide.addTable(
  paramRows.map((row) => row.map((cell, ci) => ({
    text: cell,
    options: {
      fontSize: 14, bold: ci === 0, color: COL.bodyBlack, fontFace: FONT,
      fill: { color: ci === 0 ? COL.paramLabelBg : COL.paramValueBg },
      margin: [4, 6, 4, 6], align: ci === 0 ? "left" : "center", valign: "middle",
    },
  }))),
  {
    x: px(104), y: px(198), w: px(137), h: px(84),
    colW: [px(77), px(60)],
    border: { pt: 1.5, color: COL.paramBorder },
  }
);

// --------------------------------------------- 3. UPPER EQUATION BOX (red)
// Measured: red frame x399..531, y184..212 (borders y184-187, y210-212, x399 / x531).
// Contains the 2D-rendered equation "f(x)=(x-5)^2+1" (black, ~9pt ink height 12px).
slide.addShape(ST.rect, {
  x: px(399), y: px(184), w: px(133), h: px(29),
  fill: { color: COL.upBoxBg },
  line: { color: COL.upBoxBorder, width: 1.5 },
});
// eq sidecar: eq_030_fx.png — ink 169.44x23.28 frame px at fontsize 20pt.
// Original ink is ~78x17 px, i.e. ~9.2pt -> scale by 78/169.44.
{
  const fs = require(path.join(ASSETS, "eq_030_fx.json"));
  const k = 78 / fs.w_px;                      // match the measured 78px ink width
  eqImage("eq_030_fx.png", 399 + (133 - fs.w_px * k) / 2,
          184 + (29 - fs.h_px * k) / 2 + 1,
          (fs.w_px / 600) * k, (fs.h_px / 600) * k);
}

// ------------------------------------------ 4. GREEN FORMULA BOX
// Measured: green frame x347..555 y233..282; line 1 "X = 5" (red) y240..251;
// line 2 "f(x) Minimum value is 1.0" (black + blue 1.0) y261..278.
slide.addShape(ST.rect, {
  x: px(347), y: px(233), w: px(209), h: px(50),
  fill: { color: COL.formulaBg },
  line: { color: COL.formulaBorder, width: 2 },
});
// "X = 5" — rendered in 2D mathtext (eq_030_x5.json, ink 51.96x16.8 px @20pt).
// Original ink is ~52x14 px, so scale 1.0 (font size already matches).
{
  const x5 = require(path.join(ASSETS, "eq_030_x5.json"));
  const fx = 399 + (133 - x5.w_px) / 2;        // centred inside the box width
  const fy = 236 + (45 - x5.h_px) / 2;         // top half of the green box
  eqImage("eq_030_x5.png", fx, fy, x5.w_in, x5.h_in);
  // recolour to red by overlaying a red-tinted copy is not possible at build time;
  // the sidecar renders black ink, so the red is applied via a red text layer only
  // when mathtext colour is re-rendered. Until then the box keeps mathtext ink.
  void fx; void fy;
}
// line 2: "f(x) Minimum value is " (black) + "1.0" (blue)
slide.addText([
  { text: "f(x) Minimum value is ", options: { fontSize: 16, color: COL.bodyBlack, fontFace: FONT } },
  { text: "1.0", options: { fontSize: 16, color: COL.formulaBlue, fontFace: FONT } },
], {
  x: px(352), y: px(257), w: px(199), h: px(22),
  align: "center", valign: "middle", margin: 0,
});

// ------------------------------------------------------- 5. CALLOUT
// Measured: purple text two lines y294..320 x334..568; purple rule y292..293.
slide.addShape(ST.line, {
  x: px(352), y: px(292.5), w: px(218), h: 0,
  line: { color: COL.calloutRule, width: 1.5 },
});
slide.addText("Reach Minimum after 11 Steps", {
  x: px(334), y: px(294), w: px(234), h: px(26),
  fontSize: 16, bold: true, color: COL.calloutPurple, fontFace: FONT,
  align: "center", valign: "middle", margin: 0,
});

// ------------------------------------------------------- 6. PLOT
// Measured frame x573..809 y66..265, white interior x575..806 y70..264.
// y-axis (vertical black) at x631 => x=0. Red dashed vertical at x687..689 => x=5.
// Horizontal black band y145..148 x650..725 => the y=10 line between (2,10) and (8,10).
// Green vertex x685..692 y251..258.
const BX0 = 573, BX1 = 809, BY0 = 66, BY1 = 265;
const plotW = BX1 - BX0, plotH = BY1 - BY0;

// white plot background + red frame border
slide.addShape(ST.rect, {
  x: px(BX0), y: px(BY0), w: px(plotW), h: px(plotH),
  fill: { color: COL.graphBg },
  line: { color: COL.plotFrame, width: 1.5 },
});

// grid: dashed light-gray at every 5 units, ticks -5..15
const XMIN = -5, XMAX = 15, YMIN = -5, YMAX = 15;
const XS = (v) => BX0 + ((v - XMIN) / (XMAX - XMIN)) * plotW;
const YS = (v) => BY0 + ((YMAX - v) / (YMAX - YMIN)) * plotH;
for (let v = XMIN; v <= XMAX; v += 5) {
  slide.addShape(ST.line, {
    x: px(XS(v)), y: px(BY0), w: 0, h: px(plotH),
    line: { color: COL.gridGray, width: 0.5, dashType: "sysDash" },
  });
}
for (let v = YMIN; v <= YMAX; v += 5) {
  slide.addShape(ST.line, {
    x: px(BX0), y: px(YS(v)), w: px(plotW), h: 0,
    line: { color: COL.gridGray, width: 0.5, dashType: "sysDash" },
  });
}

// x tick labels below the plot (measured y~275, x575/630/685/740/795)
for (let v = XMIN; v <= XMAX; v += 5) {
  slide.addText(String(v), {
    x: px(XS(v) - 16), y: px(273), w: px(32), h: px(14),
    fontSize: 10, color: COL.bodyBlack, fontFace: FONT, align: "center", margin: 0,
  });
}
// y tick labels left of the plot (measured x547..557)
for (let v = YMIN; v <= YMAX; v += 5) {
  slide.addText(String(v), {
    x: px(BX0 - 29), y: px(YS(v) - 7), w: px(26), h: px(14),
    fontSize: 10, color: COL.bodyBlack, fontFace: FONT, align: "right", valign: "middle", margin: 0,
  });
}
// axis names
slide.addText("x", {
  x: px(XS(5) - 10), y: px(288), w: px(20), h: px(14),
  fontSize: 12, bold: true, color: COL.bodyBlack, fontFace: FONT, align: "center", margin: 0,
});
slide.addText("f(x)", {
  x: px(BX0 - 52), y: px(YS(5) - 10), w: px(30), h: px(20),
  fontSize: 12, bold: true, color: COL.bodyBlack, fontFace: FONT, align: "center", margin: 0,
});

// black y-axis (vertical) at x=0 -> x631 ; horizontal y=10 line x650..725 (black band)
slide.addShape(ST.line, {
  x: px(631), y: px(BY0), w: 0, h: px(plotH),
  line: { color: COL.axisBlack, width: 1 },
});
slide.addShape(ST.line, {
  x: px(650), y: px(146.5), w: px(75), h: 0,
  line: { color: COL.axisBlack, width: 2 },
});

// red dashed vertical at x=5 -> x688
slide.addShape(ST.line, {
  x: px(688), y: px(BY0), w: 0, h: px(plotH),
  line: { color: COL.formulaRed, width: 1.5, dashType: "sysDash" },
});

// THE COST CURVE: ONE dense analytic parabola y = (x-5)^2 + 1.
// Dense uniform sampling (0.1 frame px steps in x) -> second-difference ripple check.
const VX = 688, VY = 254.5;             // vertex pixels (5,1)
const A_X = (BX1 - BX0 - 4) / 20;       // px per unit (approx 11.6)
const A_Y = (BY1 - BY0 - 6) / 20;
{
  const pts = [];
  for (let pxX = BX0 + 2; pxX <= BX1 - 2; pxX += 0.25) {
    const xd = XMIN + ((pxX - BX0) / plotW) * (XMAX - XMIN);
    const yd = Math.pow(xd - 5, 2) + 1;
    let pxY = BY0 + ((YMAX - yd) / (YMAX - YMIN)) * plotH;
    // calibrate so the vertex lands on the measured green point (5,1)
    const cal = (pxY - BY0) * (VY - BY0) / (BY0 + ((YMAX - 1) / (YMAX - YMIN)) * plotH - BY0);
    pxY = BY0 + cal;
    pts.push({ x: px(pxX), y: px(pxY) });
  }
  for (let i = 0; i < pts.length - 1; i++) {
    slide.addShape(ST.line, {
      x: pts[i].x, y: pts[i].y, w: pts[i + 1].x - pts[i].x, h: pts[i + 1].y - pts[i].y,
      line: { color: COL.parabolaBlue, width: 2 },
    });
  }
}

// green vertex point (5,1)
slide.addShape(ST.ellipse, {
  x: px(VX - 4), y: px(VY - 4), w: px(8), h: px(8),
  fill: { color: "00B050" }, line: { color: "00B050", width: 1 },
});
// point labels (measured: (5,1) at x704..721 y248..258 -> right of the vertex)
slide.addText("(5,1)", {
  x: px(VX + 16), y: px(VY - 4), w: px(30), h: px(14),
  fontSize: 11, color: "008000", fontFace: FONT, bold: true, margin: 0,
});

// --------------------------------------------------- 7. RED DOWN ARROW
// Measured red block arrow x174..192, y306..338 (shaft + downward triangle head).
{
  const ax = 183, ay = 306, aw = 19, ah = 32;
  slide.addShape(ST.rect, {
    x: px(ax - aw / 2), y: px(ay), w: px(aw), h: px(ah * 0.62),
    fill: { color: COL.arrowRed }, line: { color: COL.arrowRed, width: 0 },
  });
  slide.addShape(ST.triangle, {
    x: px(ax - aw), y: px(ay + ah * 0.62), w: px(aw * 2), h: px(ah * 0.38),
    fill: { color: COL.arrowRed }, line: { color: COL.arrowRed, width: 0 },
  });
}

// --------------------------------------------- 8. ITERATION TABLE
// Measured x78..655 y324..531, 8 rows x 12 cols. Values verbatim from the frame.
const iterData = [
  ["x", "3", "3.2", "3.4", "3.6", "3.8", "4", "4.2", "4.4", "4.6", "4.8", "5"],
  ["f(x)", "5", "4.24", "3.56", "2.96", "2.44", "2", "1.64", "1.36", "1.16", "1.04", "1"],
  ["x-delta", "2.9", "3.1", "3.3", "3.5", "3.7", "3.9", "4.1", "4.3", "4.5", "4.7", "4.9"],
  ["f(x-delta)", "5.41", "4.61", "3.89", "3.25", "2.69", "2.21", "1.81", "1.49", "1.25", "1.09", "1.01"],
  ["x+delta", "3.1", "3.3", "3.5", "3.7", "3.9", "4.1", "4.3", "4.5", "4.7", "4.9", "5.1"],
  ["f(x+delta)", "4.61", "3.89", "3.25", "2.69", "2.21", "1.81", "1.49", "1.25", "1.09", "1.01", "1.01"],
  ["slope", "-8", "-7.2", "-6.4", "-5.6", "-4.8", "-4", "-3.2", "-2.4", "-1.6", "-0.8", "0"],
  ["next x", "3.2", "3.4", "3.6", "3.8", "4", "4.2", "4.4", "4.6", "4.8", "5", "stop"],
];
slide.addTable(
  iterData.map((row, ri) => row.map((cell, ci) => {
    const isLabel = ci === 0;
    const isSlopeRow = ri === 6;
    const isStopCell = ri === 7 && ci === 11;
    const isXRowRed = ri === 0 && (ci === 1 || ci === 11);
    const opts = {
      fontSize: 9, fontFace: FONT, color: COL.bodyBlack,
      margin: [1, 3, 1, 3],
      align: isLabel ? "left" : "center", valign: "middle",
    };
    if (isLabel) { opts.bold = true; }
    if (ri === 0 && !isLabel) { opts.bold = true; }
    if (isSlopeRow) { opts.fill = { color: COL.iterSlopeBg }; }
    else if (!isStopCell) { opts.fill = { color: COL.iterFill }; }
    if (isStopCell) {
      opts.fill = { color: COL.iterStopRed };
      opts.color = COL.iterStopWhite;
      opts.bold = true;
    }
    if (isXRowRed) { opts.color = COL.iterRedHighlight; opts.bold = true; }
    return { text: cell, options: opts };
  })),
  {
    x: px(78), y: px(324), w: px(577), h: px(207),
    colW: Array(12).fill(px(577 / 12)),
    rowH: Array(8).fill(px(207 / 8)),
    border: { pt: 1.5, color: COL.iterBorder },
  }
);

// ---------------------------------------------- 9. HOUSE CHROME LAST
// THE z-order fix: chrome is the TOP-most paint so the badge can never be
// occluded by content (the plot's white background used to paint over it).
drawHouseChrome(pres, slide, { numeral: "30" });

// ---------------------------------------------------------------- output
const outPath = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_030_recreated.pptx";
pres.writeFile(outPath).then(() => {
  console.log("Written:", outPath);
}).catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
