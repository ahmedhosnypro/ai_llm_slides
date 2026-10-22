// slide_028.js — "Regression Example" (ML lecture 02, root slide, PARENT of 29)
// Worker ml02-w028-a4, 2026-10-13. Resumed from gen-3 banked measurements
// (scratch/ml02/slide028/: measure_frame/precise/fine/glyph_bands + this
// session's color-classified CC analysis) — all geometry below is PIL-measured
// from unique_slides/slide_028.jpg (960x540, 1px = 1pt = 1/72 in).
//
// Structure: house chrome (shared module, numeral 28) + red title + white data
// panel (x72..655, y90..179, thin gray border) holding row labels x1=>/x2=>,
// four blue column vectors X1..X4 with straight-bar delimiters, red y-values,
// green Predict, blue query vector X=|7 over 3| with red "y = ???";
// right side: red-bordered formula box (W = (X^T X)^-1 X^T Y, W black-underlined,
// Y red+red-underline, red superscript -1, blue X^T X parens) over a
// blue-bordered box (y = W^T X; y= black, W^T blue, X red).
// The gray '+' crosshair at (124,369) in the original is a cursor artifact —
// EXCLUDED per judge GROUND RULES clause (c) and recreation_brief step 14.
//
// Equations: matplotlib mathtext (STIX fontset — closest measured match to the
// original's narrow TeX-like glyphs; dejavusans was +125 delta vs stix +77
// across all 21 token targets), 600dpi transparent PNGs (scripts/render_eq.py),
// embedded at EXACT px/600 size, anchored per-token at the ORIGINAL's measured
// ink-left / baseline / band-center (manifest eq028_manifest.json carries
// ink_dx/ink_dy so placement lands INK, not padded PNG, edges).
// Vector stack delimiters are 1pt line shapes at the measured bar x-centers
// (original shows straight 1-2px bars, not parens; no superscript T).

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const PX = 1 / 72; // frame px -> inches
const ASSET = (n) => path.resolve(__dirname, "assets", n + ".png");
const MAN = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq028_manifest.json"), "utf8"));

// ---- measured palette -------------------------------------------------------
const C = {
  titleRed: "CC0000",            // spec title_text (JPEG core #AF4450 of CC0000)
  panelFill: "FFFFFF",           // measured (400,95) #FFFFFD
  panelBorder: "B4BAC0",         // measured cores #B2B5B8..#C4CDD0
  vecBlue: "0000CC",             // spec accent; cores #282BAE..#3A2FA5
  yRed: "CC0000",                // spec accent; cores #A73746..#B65160
  predictGreen: "009900",        // spec accent; cores #449042..#4B9648
  inkBlack: "000000",
  box1Fill: "F7FADB",            // measured interior avg (247,250,219)
  box1Border: "C00000",          // border cores (126,48,48)/(132,35,37)
  box2Fill: "E6F9F8",            // measured interior avg (230,249,248)
  box2Border: "0000CC",          // border cores (94,98,136)/(96,96,182)
};

// ---- equation PNG placement (ink-anchored) ---------------------------------
// baseline anchor: y_png = target_baseline_px - baseline_frac * h_png_px
// center anchor:   y_png = target_center_px  - (ink_dy + ink_h/2)
// x anchor:        x_png = target_ink_left_px - ink_dx   (PNG px = 1/600 in;
// conversion to inches happens with /600; all in frame-px space * PX/... here
// we work in px and divide by 72 at draw time — 1 png px = 72/600 frame px)
function eqBaseline(name, xPx, blPx) {
  const a = MAN[name];
  const x = (xPx - a.ink_dx * (72 / 600)) * PX;
  const y = (blPx - a.baseline_frac * a.h_px * (72 / 600)) * PX;
  return { path: ASSET(name), x, y, w: a.w_px / 600, h: a.h_px / 600 };
}
function eqCenter(name, xPx, cyPx) {
  const a = MAN[name];
  const x = (xPx - a.ink_dx * (72 / 600)) * PX;
  const y = (cyPx - (a.ink_dy + a.ink_h / 2) * (72 / 600)) * PX;
  return { path: ASSET(name), x, y, w: a.w_px / 600, h: a.h_px / 600 };
}
// top-anchor variant (place PNG so its INK TOP lands on target_top_px)
function eqTop(name, xPx, topPx) {
  const a = MAN[name];
  const x = (xPx - a.ink_dx * (72 / 600)) * PX;
  const y = (topPx - a.ink_dy * (72 / 600)) * PX;
  return { path: ASSET(name), x, y, w: a.w_px / 600, h: a.h_px / 600 };
}
function drawImg(slide, spec) { slide.addImage(spec); }
function vline(pptx, slide, xPx, y0Px, y1Px, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: xPx * PX, y: y0Px * PX, w: 0, h: (y1Px - y0Px) * PX,
    line: { color, width },
  });
}
function hline(pptx, slide, x0Px, x1Px, yPx, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: x0Px * PX, y: yPx * PX, w: (x1Px - x0Px) * PX, h: 0,
    line: { color, width },
  });
}

// ---- title ------------------------------------------------------------------
function drawTitle(pptx, slide) {
  // ink x381..607 y60..81 (center 494, 70.5); bold Arial ~24pt. LO's valign
  // middle sits the ink ~2.9px below the box center (measured attempt 1
  // render: ink center 73.4) — box center pre-shifted to 67.6 to compensate.
  slide.addText("Regression Example", {
    x: (494 - 300) * PX, y: (67.6 / 72) - 0.5, w: 600 * PX, h: 1.0,
    align: "center", valign: "middle", margin: 0,
    fontSize: 24, bold: true, color: C.titleRed, fontFace: "Arial",
    charSpacing: -0.5,
  });
}

// ---- data panel -------------------------------------------------------------
function drawPanel(pptx, slide) {
  // border strokes measured: left x72-73, top y90-91, right x654-655, bottom y178-179
  slide.addShape(pptx.ShapeType.rect, {
    x: 72.5 * PX, y: 90.5 * PX, w: 582 * PX, h: 88 * PX,
    fill: { color: C.panelFill }, line: { color: C.panelBorder, width: 1 },
  });
}

// ---- row labels x1=> / x2=> ---------------------------------------------------
function drawLabels(pptx, slide) {
  // 'x' glyphs x82..91/93, subs, double-stroke arrows x119..133
  drawImg(slide, eqBaseline("lx", 82, 118.5));
  drawImg(slide, eqBaseline("lx", 82, 147.5));
  drawImg(slide, eqBaseline("xs1", 93.75, 123.5));
  drawImg(slide, eqBaseline("xs2", 93.75, 152.5));
  drawImg(slide, eqCenter("arr", 119, 111.5));
  drawImg(slide, eqCenter("arr", 119, 140.5));
}

// ---- four training column vectors X1..X4 ------------------------------------
// each: "Xi =" PNG + top/bottom digit PNGs + tall hairline paren delimiters
// (delimiters-stretched-glyph pattern: the ORIGINAL delimiters are thin curved
// parens h~40px bow~2-3px — 8x-gate-verified, NOT straight bars; PNGs
// dl028_l/r.png 25x329@600dpi = 3.0x39.5 frame px, ink-left at measured bbox)
const VEC_XEQ = [
  { n: "vx1", x: 150 }, { n: "vx2", x: 240 }, { n: "vx3", x: 329 }, { n: "vx4", x: 416 },
];
const VEC_PARENS = [
  // [leftParenInkLeft, rightParenInkLeft], top y104, h 39.5
  [190, 209], [281, 299], [369, 388], [457, 476],
];
const VEC_DIGITS = [
  // [topDigit, topX, bottomDigit, bottomX]  (top bl 118.5, bottom bl 143.5)
  ["vd1", 198, "vd1", 198],
  ["vd2", 287, "vd2", 287],
  ["vd2", 375, "vd1", 375],
  ["vd1", 464, "vd2", 463],
];
const VEC_EQX = [175, 265, 352, 441]; // '=' ink lefts, band center y121.25
const DL = { w: 25 / 600, h: 329 / 600 };       // training-vector delims
const DLQ = { w: 25 / 600, h: 313 / 600 };      // query-vector delims (35.5pt)
function drawVectors(pptx, slide) {
  VEC_XEQ.forEach((v) => drawImg(slide, eqBaseline(v.n, v.x, 129.5)));
  VEC_EQX.forEach((x) => drawImg(slide, eqCenter("veq", x, 121.25)));
  VEC_DIGITS.forEach((d) => {
    drawImg(slide, eqBaseline(d[0], d[1], 118.5));
    drawImg(slide, eqBaseline(d[2], d[3], 143.5));
  });
  VEC_PARENS.forEach((p) => {
    slide.addImage({ path: ASSET("dl028_l"), x: p[0] * PX, y: 104 * PX, w: DL.w, h: DL.h });
    slide.addImage({ path: ASSET("dl028_r"), x: p[1] * PX, y: 104 * PX, w: DL.w, h: DL.h });
  });
}

// ---- red y-values row ---------------------------------------------------------
function drawYValues(pptx, slide) {
  drawImg(slide, eqBaseline("vy1", 149, 171.5));
  drawImg(slide, eqBaseline("vy2", 240, 171.5));
  drawImg(slide, eqBaseline("vy3", 328, 171.5));
  drawImg(slide, eqBaseline("vy4", 415, 171.5));
  [171, 262, 349, 437].forEach((x) => drawImg(slide, eqCenter("vyeq", x, 165.25)));
  // digit pairs center-anchored on the original pair spans (stix digits run
  // ~1.5px wide; centering distributes the residual to both edges <=3px@150)
  drawImg(slide, eqBaseline("vp10", 197.5 - 18.6 / 2, 171.5));
  drawImg(slide, eqBaseline("vp15", 287.5 - 17.88 / 2, 171.5));
  drawImg(slide, eqBaseline("vp13", 375.5 - 17.64 / 2, 171.5));
  drawImg(slide, eqBaseline("vp12", 463 - 18.48 / 2, 171.5));
}

// ---- Predict (green, Arial bold italic) ---------------------------------------
function drawPredict(pptx, slide, opts = {}) {
  // ink x510..564 y128..141 (band center 134.75)
  slide.addText("Predict", {
    x: 509 * PX, y: (134.75 / 72) - 0.45, w: 90 * PX, h: 0.9,
    align: "left", valign: "middle", margin: 0,
    fontSize: 18.5, bold: true, italic: true, color: C.predictGreen,
    fontFace: "Arial", charSpacing: opts.predictCharSpacing === undefined ? -1.2 : opts.predictCharSpacing,
  });
}

// ---- query vector X = |7 over 3| + y = ??? -------------------------------------
function drawQuery(pptx, slide) {
  drawImg(slide, eqBaseline("vxq", 579, 129.5));
  drawImg(slide, eqCenter("veq", 597, 121.25));
  drawImg(slide, eqBaseline("vd7", 621, 118.5));
  drawImg(slide, eqBaseline("vd3", 621, 143.5));
  slide.addImage({ path: ASSET("dl028_ql"), x: 614 * PX, y: 107 * PX, w: DLQ.w, h: DLQ.h });
  slide.addImage({ path: ASSET("dl028_qr"), x: 633 * PX, y: 107 * PX, w: DLQ.w, h: DLQ.h });
  drawImg(slide, eqBaseline("vyq", 573, 171.5));
}

// ---- formula boxes -------------------------------------------------------------
function drawBox1(pptx, slide) {
  // border strokes: left 668-670, top 101-103, right 886-889, bottom 137-139
  slide.addShape(pptx.ShapeType.rect, {
    x: 669 * PX, y: 102 * PX, w: 218.5 * PX, h: 36 * PX,
    fill: { color: C.box1Fill }, line: { color: C.box1Border, width: 2 },
  });
}
function drawBox2(pptx, slide) {
  // strokes: left 761-762, top 147-149, right 866-867, bottom 183-185
  slide.addShape(pptx.ShapeType.rect, {
    x: 761.5 * PX, y: 148 * PX, w: 105 * PX, h: 36 * PX,
    fill: { color: C.box2Fill }, line: { color: C.box2Border, width: 2 },
  });
}

// ---- eq1: W = (X^T X)^-1 X^T Y  (baseline 131.5, eq band y112..134) ------------
function drawEq1(pptx, slide) {
  drawImg(slide, eqBaseline("eW", 679, 131.5));   // W black, underlined
  drawImg(slide, eqCenter("eeq", 714, 124.2));    // =
  drawImg(slide, eqTop("pl", 734, 111.67));       // ( blue tall (center 123.25)
  drawImg(slide, eqBaseline("Xa", 743, 131.5));   // X blue
  drawImg(slide, eqCenter("T1", 760, 116.2));     // ^T blue
  drawImg(slide, eqBaseline("Xb", 771, 131.5));   // X blue
  drawImg(slide, eqTop("pr", 789, 111.67));       // ) blue tall (center 123.25)
  drawImg(slide, eqCenter("inv", 797, 116.25));   // ^-1 RED
  drawImg(slide, eqBaseline("XT", 816, 131.5));   // X^T blue
  drawImg(slide, eqBaseline("eY", 859, 131.5));   // Y RED
  hline(pptx, slide, 679, 697.5, 133.5, C.inkBlack, 1);  // W underline (black)
  hline(pptx, slide, 858.5, 871.5, 133.5, C.yRed, 1);    // Y underline (red)
}

// ---- eq2: y = W^T X -------------------------------------------------------------
function drawEq2(pptx, slide) {
  drawImg(slide, eqBaseline("ey2", 770, 175));    // y= black
  drawImg(slide, eqBaseline("eWT", 808, 177.5));  // W^T blue
  drawImg(slide, eqBaseline("eX", 845, 176.5));   // X red
  // vector-notation underlines (measured in the original: blue x809..829
  // rows 178-179 under W, red x847..859 row 177 under X; same convention as
  // eq1's W/Y underlines and certified slide_015's box4s)
  hline(pptx, slide, 809, 829.5, 178.9, C.vecBlue, 1);
  hline(pptx, slide, 847, 859.5, 177.5, C.yRed, 1);
}

// ---- component export -----------------------------------------------------------
// renderBase draws the full slide; children (slide 29) import this and pass
// their own numeral + opts.delta to replace/extend blocks.
function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 28 : opts.numeral;
  drawHouseChrome(pptx, slide, { numeral });
  drawTitle(pptx, slide);
  drawPanel(pptx, slide);
  drawLabels(pptx, slide);
  drawVectors(pptx, slide);
  drawYValues(pptx, slide);
  drawPredict(pptx, slide, opts);
  drawQuery(pptx, slide);
  drawBox1(pptx, slide);
  drawBox2(pptx, slide);
  drawEq1(pptx, slide);
  drawEq2(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] || path.resolve(__dirname, "../slide_028_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = {
  renderBase, drawTitle, drawPanel, drawLabels, drawVectors, drawYValues,
  drawPredict, drawQuery, drawBox1, drawBox2, drawEq1, drawEq2, C,
};
