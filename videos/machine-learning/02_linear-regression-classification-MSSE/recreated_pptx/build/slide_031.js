// slide_031.js — "Classification  Example" (ML lecture 02, PARENT of 32 and 35)
// Worker ml02-w031-g9, 2026-10-14. Built from PIL measurements banked in
// scratch/ml02/slide031/ (m_final/m_maps/m_boxes/m_result + z_* ASCII zooms +
// probe_colors output) against unique_slides/slide_031.jpg (960x540, 1px=1pt).
//
// Structure: house chrome (shared module, numeral 31) + two-color title
// ("Classification" blue / "Example" red) + red-bordered sketch panel holding
// the yellow parallelogram plane, 3 thin red axes with red tick digits, 4
// orange/blue data points, dashed gray projection lines, rotated -ve/+ve
// annotations; right-top box with x1=>/x2=> black vectors X1..X4 (column
// stacks, thin paren delimiters, NO superscript T — same convention as the
// certified slide_028) and colored class labels y1=C1 (red) / y2=C2 (blue);
// green box "Required to obtain W that satisfies" (blue text, red W) with the
// 4x3 design matrix (red bias column), (W) group, '=' and sign result column
// |>0 <0 >0 <0|; cream footer banner "How to deal "Mathematically" with
// "<" and ">" ???" (red "Mathematically").
//
// Equations/labels: matplotlib mathtext (STIX), 600dpi transparent PNGs
// (scripts/render_eq.py), embedded at EXACT ink px/600 size, anchored at the
// ORIGINAL's measured ink-left / baseline / ink-top (eq031_manifest.json).
// Tall delimiters: PIL-drawn parabolic paren arcs (3.4px bow) for vectors and
// (W); STRAIGHT 1pt bars for the matrix and result column (measured bars).
// Matrix column 1 digits are RED (bias 1s — measured (134,15,34) cores).

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const PX = 1 / 72; // frame px -> inches
const ASSET = (n) => path.resolve(__dirname, "assets", n + ".png");
const MAN = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq031_manifest.json"), "utf8"));

// ---- measured palette -------------------------------------------------------
const C = {
  titleBlue: "0000CC",      // title 'Classification' core (56,47,174)
  titleRed: "CC0000",       // title 'Example' / accents (cores (165,59,71))
  inkBlack: "000000",
  boxRed: "C00000",         // left sketch panel border (cores (136,0,8))
  panelBorder: "B4BAC0",    // right-top box border (204,207,212)
  planeFill: "FFFF85",      // parallelogram (253,255,133)
  axisRed: "C00000",        // thin axes + tick digits
  ptOrange: "C88313",       // data points class 1 (200,131,19)
  ptBlue: "0000CC",         // data points class 2 (2,0,179)
  dashGray: "AAAAAA",       // dashed projection lines
  predictGreen: "009900",   // 'Classify' (84,151,82)
  greenFill: "EDFDF2",      // green box (237,253,242)
  greenBorder: "B2BEBA",    // green box border (178,190,186)
  headerRule: "96A79C",     // light rule under header (150,167,156)
  footerFill: "FAFBE8",     // footer banner (250,251,232)
};

// ---- equation PNG placement (ink-anchored; PNG px = 1/600 in) ---------------
function eqBaseline(name, xPx, blPx) {
  const a = MAN[name];
  const x = (xPx - a.ink_dx * (72 / 600)) * PX;
  const y = (blPx - a.baseline_frac * a.h_px * (72 / 600)) * PX;
  return { path: ASSET(name), x, y, w: a.w_px / 600, h: a.h_px / 600 };
}
function eqCenter(name, xInkLeftPx, cyPx) {
  const a = MAN[name];
  const x = (xInkLeftPx - a.ink_dx * (72 / 600)) * PX;
  const y = (cyPx - (a.ink_dy + a.ink_h / 2) * (72 / 600)) * PX;
  return { path: ASSET(name), x, y, w: a.w_px / 600, h: a.h_px / 600 };
}
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
function hline(pptx, slide, x0Px, x1Px, yPx, color, width, dashType) {
  slide.addShape(pptx.ShapeType.line, {
    x: x0Px * PX, y: yPx * PX, w: (x1Px - x0Px) * PX, h: 0,
    line: { color, width, ...(dashType ? { dashType } : {}) },
  });
}
// diagonal segment from (x0,y0) to (x1,y1), any direction (flip-aware)
function seg(pptx, slide, x0, y0, x1, y1, color, width, extra) {
  const x = Math.min(x0, x1), y = Math.min(y0, y1);
  const w = Math.abs(x1 - x0), h = Math.abs(y1 - y0);
  const flipH = (x1 < x0) !== (y1 < y0) && w > 0 && h > 0 ? true : (x1 < x0 ? true : false);
  slide.addShape(pptx.ShapeType.line, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX, flipH,
    line: { color, width, ...(extra || {}) },
  });
}
// filled custGeom polygon (absolute inch points, close by repeating start)
function poly(pptx, slide, pts, fill, line) {
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,
    fill: { color: fill },
    line: line || { color: fill, width: 0 },
    points: pts.map((p, i) => ({
      x: p[0] * PX, y: p[1] * PX, ...(i === 0 ? { moveTo: true } : {}),
    })).concat([{ x: pts[0][0] * PX, y: pts[0][1] * PX }]),
  });
}

// ---- title: "Classification  Example" (blue + red) ---------------------------
function drawTitle(pptx, slide) {
  // ink x365..623 y60..81 (center 494, 70.5); bold Arial ~24pt. LO valign
  // middle compensation per certified slide_028 (box center pre-shifted 67.6).
  slide.addText([
    { text: "Classification  ", options: { color: C.titleBlue } },
    { text: "Example", options: { color: C.titleRed } },
  ], {
    x: (494 - 300) * PX, y: (67.6 / 72) - 0.5, w: 600 * PX, h: 1.0,
    align: "center", valign: "middle", margin: 0,
    fontSize: 24, bold: true, fontFace: "Arial", charSpacing: -0.5,
  });
}

// ---- left red-bordered sketch panel ------------------------------------------
function drawLeftBox(pptx, slide) {
  // border strokes: left x74-76, right 404-406, top 108-109, bottom 523-524
  slide.addShape(pptx.ShapeType.rect, {
    x: 74.5 * PX, y: 108.5 * PX, w: 331 * PX, h: 415.5 * PX,
    fill: { color: "FFFFFF" }, line: { color: C.boxRed, width: 2 },
  });
}

// ---- yellow parallelogram plane (no border) -----------------------------------
function drawPlane(pptx, slide) {
  // vertices: top (146,222), right (311,443), bottom (251,514), left (84,300)
  poly(pptx, slide, [[146, 222], [311, 443], [251, 514], [84, 300]], C.planeFill);
}

// ---- W label over the plane (black bold + underline) --------------------------
function drawWLabel(pptx, slide) {
  drawImg(slide, eqTop("wlab", 134.5, 246));
  hline(pptx, slide, 134, 159.5, 263.5, C.inkBlack, 1);
}

// ---- three thin red axes with arrowheads + red tick digits --------------------
function drawAxes(pptx, slide) {
  // y-axis: vertical x223, origin (223,412) up to arrowhead
  vline(pptx, slide, 223, 412, 119, C.axisRed, 1);
  poly(pptx, slide, [[223, 106], [218, 119.5], [228, 119.5]], C.axisRed);
  drawImg(slide, eqBaseline("axy", 208, 159.5));          // red italic 'y'
  // x2-axis: horizontal y412 from origin to x~370 (no separate arrowhead)
  hline(pptx, slide, 223, 370, 412, C.axisRed, 1);
  drawImg(slide, eqBaseline("axx2", 373, 421.5));          // 'x2'
  drawImg(slide, eqBaseline("tk1", 269, 407.5));           // red '1'
  drawImg(slide, eqBaseline("tk2", 310, 407.5));           // red '2'
  // x1-axis: diagonal from origin down-left, arrowhead at ~(145,480)
  seg(pptx, slide, 223, 412, 155, 471.5, C.axisRed, 1);
  poly(pptx, slide, [[145, 480], [157.8, 474.9], [151.8, 468.1]], C.axisRed);
  drawImg(slide, eqBaseline("tk1", 193, 433));             // red '1'
  drawImg(slide, eqBaseline("tk2", 171, 454));             // red '2'
  drawImg(slide, eqBaseline("axx1", 113, 512.5));          // 'x1'
}

// ---- data points (orange class 1, blue class 2; d~10px) -----------------------
const PTS = [
  { x: 246.5, y: 433, c: C.ptOrange },
  { x: 230.8, y: 451.5, c: C.ptOrange },
  { x: 295.6, y: 433.1, c: C.ptBlue },
  { x: 277.5, y: 452, c: C.ptBlue },
];
function drawPoints(pptx, slide) {
  PTS.forEach((p) => slide.addShape(pptx.ShapeType.ellipse, {
    x: (p.x - 5) * PX, y: (p.y - 5) * PX, w: 10 * PX, h: 10 * PX,
    fill: { color: p.c }, line: { color: p.c, width: 0 },
  }));
}

// ---- dashed gray projection lines + blue connectors ---------------------------
function drawProjections(pptx, slide) {
  hline(pptx, slide, 196, 297, 431.5, C.dashGray, 1, "dash");
  hline(pptx, slide, 176, 277, 453.5, C.dashGray, 1, "dash");
  // blue pointer from x2 tick region to blue point (312,408)->(294,434)
  seg(pptx, slide, 312, 408, 294, 434, C.ptBlue, 1);
  // short blue segment near b2 point (276-280, 449-454)
  seg(pptx, slide, 277, 449.5, 280.5, 454.5, C.ptBlue, 1);
}

// ---- rotated +/-ve annotations with arrows -------------------------------------
function drawAnnotations(pptx, slide) {
  // red '-ve ( < 0 )' along the plane's upper-right edge (run (145,313)->(195,366))
  slide.addText("-ve ( < 0 )", {
    x: (170 - 65) * PX, y: (339.5 / 72) - 0.15, w: 130 * PX, h: 0.3,
    align: "center", valign: "middle", margin: 0,
    fontSize: 12, color: C.titleRed, fontFace: "Arial", rotate: 47,
  });
  seg(pptx, slide, 188, 352, 173, 373, C.titleRed, 1.25, { endArrowType: "triangle" });
  // blue '+ve ( > 0 )' along the plane's lower-left edge (run (98,354)->(135,401))
  slide.addText("+ve ( > 0 )", {
    x: (116.5 - 65) * PX, y: (377.5 / 72) - 0.15, w: 130 * PX, h: 0.3,
    align: "center", valign: "middle", margin: 0,
    fontSize: 12, color: C.ptBlue, fontFace: "Arial", rotate: 52,
  });
  seg(pptx, slide, 120, 388, 146, 404, C.ptBlue, 1.25, { endArrowType: "triangle" });
}

// ---- right-top white box -------------------------------------------------------
function drawRtopBox(pptx, slide) {
  // border strokes: x432..855, y104..305 (gray 1px)
  slide.addShape(pptx.ShapeType.rect, {
    x: 432.5 * PX, y: 104.5 * PX, w: 422 * PX, h: 200 * PX,
    fill: { color: "FFFFFF" }, line: { color: C.panelBorder, width: 1 },
  });
}

// ---- four black column vectors X1..X4 with class labels ------------------------
const VEC_X = [510, 601, 689, 776];                 // 'Xi' ink lefts, baseline 146.5
const VEC_EQ = [533.8, 624.8, 712.8, 799.8];        // '=' ink lefts, cy 137.5
const VEC_LP = [550, 641, 729, 816];                // left paren ink left, top y117
const VEC_RP = [569.5, 660.5, 748.5, 835.5];        // right paren ink left, top y119
const VEC_DIGITS = [                                // [topName, bottomName], left x
  ["nb1", "nb1"], ["nb2", "nb2"], ["nb2", "nb1"], ["nb1", "nb2"],
];
const VEC_DLW = { w: MAN.dlv_l.frame_w, h: MAN.dlv_l.frame_h };  // 3.36 x 47.04
function drawVectors(pptx, slide) {
  drawImg(slide, eqBaseline("x1m", 442, 139.5));
  drawImg(slide, eqBaseline("x2m", 442, 169.5));
  drawImg(slide, eqCenter("arr", 479.6, 128.5));
  drawImg(slide, eqCenter("arr", 479.6, 157));
  VEC_X.forEach((x, i) => drawImg(slide, eqBaseline("Xv" + (i + 1), x, 146.5)));
  VEC_EQ.forEach((x) => drawImg(slide, eqCenter("veq", x, 137.5)));
  VEC_LP.forEach((x) => slide.addImage({ path: ASSET("dlv_l"), x: x * PX, y: 117 * PX, w: VEC_DLW.w, h: VEC_DLW.h }));
  VEC_RP.forEach((x) => slide.addImage({ path: ASSET("dlv_r"), x: x * PX, y: 119 * PX, w: MAN.dlv_r.frame_w, h: MAN.dlv_r.frame_h }));
  VEC_DIGITS.forEach((d, i) => {
    const x = VEC_LP[i] + 8;
    drawImg(slide, eqBaseline(d[0], x, 135.5));
    drawImg(slide, eqBaseline(d[1], x, 160.5));
  });
  // class labels: whole label colored (measured: y1 row ALL red, y2 ALL blue)
  drawImg(slide, eqTop("y1c1", 510, 174));
  drawImg(slide, eqTop("y2c2", 600, 174));
  drawImg(slide, eqTop("y3c1", 688, 174));
  drawImg(slide, eqTop("y4c2", 776, 174));
}

// ---- 'Classify' (green bold) ----------------------------------------------------
function drawClassify(pptx, slide) {
  // ink x456..516 y241..257 (cy 249)
  slide.addText("Classify", {
    x: 455 * PX, y: (249 / 72) - 0.45, w: 90 * PX, h: 0.9,
    align: "left", valign: "middle", margin: 0,
    fontSize: 17, bold: true, color: C.predictGreen, fontFace: "Arial",
    charSpacing: -0.3,
  });
}

// ---- blue query vector X=(7/3) + 'y = C1 or C2 ???' -----------------------------
function drawQuery(pptx, slide) {
  drawImg(slide, eqBaseline("Xq", 586, 251));
  drawImg(slide, eqCenter("qeq", 604.8, 242.5));
  slide.addImage({ path: ASSET("dlv_l"), x: 620.5 * PX, y: 221.5 * PX, w: VEC_DLW.w, h: VEC_DLW.h });
  slide.addImage({ path: ASSET("dlv_r"), x: 639.5 * PX, y: 221.5 * PX, w: MAN.dlv_r.frame_w, h: MAN.dlv_r.frame_h });
  drawImg(slide, eqTop("q7", 626.5, 226));
  drawImg(slide, eqTop("q3", 624.5, 251));
  // 'y = C1 or C2  ???' row (baseline 295): black 'y=', red C1, black or,
  // blue C2, black '???' (fs21 — measured 30px wide vs C's 17px)
  drawImg(slide, eqBaseline("yeq", 530, 295));
  drawImg(slide, eqBaseline("cy1", 563, 295));
  drawImg(slide, eqBaseline("orw", 585, 295));
  drawImg(slide, eqBaseline("cy2", 620, 295));
  drawImg(slide, eqTop("qqq", 664, 279));
}

// ---- green formula box -----------------------------------------------------------
function drawGreenBox(pptx, slide) {
  // border strokes: x460..815, y318..471
  slide.addShape(pptx.ShapeType.rect, {
    x: 460.5 * PX, y: 318.5 * PX, w: 354 * PX, h: 152 * PX,
    fill: { color: C.greenFill }, line: { color: C.greenBorder, width: 1 },
  });
}

// ---- header 'Required to obtain W that satisfies' + light rule ------------------
function drawHeader(pptx, slide) {
  // ink x474..781 y328..348 (cap band 333..344); W red lands x646..660 at fs18
  slide.addText([
    { text: "Required to obtain  ", options: { color: C.titleBlue } },
    { text: "W", options: { color: C.titleRed } },
    { text: "  that satisfies", options: { color: C.titleBlue } },
  ], {
    x: 473.5 * PX, y: (336 / 72) - 0.45, w: 330 * PX, h: 0.9,
    align: "left", valign: "middle", margin: 0,
    fontSize: 18, bold: true, fontFace: "Arial",
  });
  hline(pptx, slide, 642, 666, 344.5, C.titleRed, 1);       // red underline under W
  hline(pptx, slide, 461, 814, 348.5, C.headerRule, 0.75);  // light rule
}

// ---- design matrix block ----------------------------------------------------------
// rows (bias 1s RED, coordinates black): (1,1,1) (1,2,2) (1,2,1) (1,1,2)
const MROWS = [
  { bl: 374.5, acy: 364.5, al: 537.5, cols: [["c1r", 565], ["nb1", 595], ["nb1", 626]] },
  { bl: 399.5, acy: 392, al: 536, cols: [["c1r", 565], ["nb2", 593], ["nb2", 624]] },
  { bl: 425, acy: 420.5, al: 537, cols: [["c1r", 565], ["nb2", 593], ["nb1", 625]] },
  { bl: 450.5, acy: 449.5, al: 536, cols: [["c1r", 565], ["nb1", 595], ["nb2", 622]] },
];
function drawMatrix(pptx, slide) {
  const BL = ["x1m", "x2m", "x3m", "x4m"];
  MROWS.forEach((r, i) => {
    drawImg(slide, eqBaseline(BL[i], 500, r.bl + 1));
    drawImg(slide, eqCenter("arrm", r.al, r.acy));
    r.cols.forEach((cl) => drawImg(slide, eqBaseline(cl[0], cl[1], r.bl)));
  });
  // straight bar delimiters (measured 1-2px vertical bars y347..456)
  vline(pptx, slide, 558.5, 347.5, 456.5, C.inkBlack, 1);
  vline(pptx, slide, 635.5, 347.5, 456.5, C.inkBlack, 1);
}

// ---- (W) group, '=', sign result column -------------------------------------------
function drawResult(pptx, slide) {
  // ( W ): tall curved parens h60 (y376..435), W red baseline 412.5
  slide.addImage({ path: ASSET("dlw_l"), x: 649.5 * PX, y: 375.5 * PX, w: MAN.dlw_l.frame_w, h: MAN.dlw_l.frame_h });
  slide.addImage({ path: ASSET("dlw_r"), x: 678.5 * PX, y: 376 * PX, w: MAN.dlw_r.frame_w, h: MAN.dlw_r.frame_h });
  drawImg(slide, eqBaseline("wr", 658, 412.5));
  drawImg(slide, eqCenter("veq", 688.8, 404));   // '=' bars y397-400/408-411
  // result column: straight bar delimiters, entries alternate red/blue
  // (measured per-glyph: '>'/'<' ~10px wide, '0' ~10px, 15-16px tall = fs21;
  // r1 ink 724..749, r2-4 720..745; baselines 375/400.5/426.5/452.5)
  vline(pptx, slide, 710.5, 347.5, 456.5, C.inkBlack, 1);
  vline(pptx, slide, 753, 347.5, 456.5, C.inkBlack, 1);
  drawImg(slide, eqBaseline("gt", 724, 375));
  drawImg(slide, eqBaseline("zr", 739, 375));
  drawImg(slide, eqBaseline("lt", 720, 400.5));
  drawImg(slide, eqBaseline("zb", 736, 400.5));
  drawImg(slide, eqBaseline("gt", 720, 426.5));
  drawImg(slide, eqBaseline("zr", 736, 426.5));
  drawImg(slide, eqBaseline("lt", 720, 452.5));
  drawImg(slide, eqBaseline("zb", 736, 452.5));
}

// ---- cream footer banner -----------------------------------------------------------
function drawFooter(pptx, slide) {
  // box x425..902, y491..525; fill (250,251,232); border dark maroon -> C00000 1pt
  slide.addShape(pptx.ShapeType.rect, {
    x: 425.5 * PX, y: 491.5 * PX, w: 476 * PX, h: 33.5 * PX,
    fill: { color: C.footerFill }, line: { color: C.titleRed, width: 1 },
  });
  // ink x445..873 y499..516 (center 659); 'Mathematically' (with its curly
  // quotes) red x549..693; fs18 (closed-loop: fs16 rendered 384px vs 428 orig)
  slide.addText([
    { text: "How to deal ", options: { color: C.inkBlack } },
    { text: "\u201CMathematically\u201D", options: { color: C.titleRed } },
    { text: " with \u201C<\u201D and \u201C>\u201D ???", options: { color: C.inkBlack } },
  ], {
    x: (659 - 238) * PX, y: (506 / 72) - 0.45, w: 476 * PX, h: 0.9,
    align: "center", valign: "middle", margin: 0,
    fontSize: 18, bold: true, fontFace: "Arial",
  });
}

// ---- component export ---------------------------------------------------------------
// renderBase draws the full slide (house chrome included). Children: slide 32
// is an INTENTIONAL exact duplicate of 31 (founder directive) — it may call
// renderBase with numeral 32; slide 35 depends on 31.
function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 31 : opts.numeral;
  drawHouseChrome(pptx, slide, { numeral });
  drawTitle(pptx, slide);
  drawLeftBox(pptx, slide);
  drawPlane(pptx, slide);
  drawWLabel(pptx, slide);
  drawAxes(pptx, slide);
  drawPoints(pptx, slide);
  drawProjections(pptx, slide);
  drawAnnotations(pptx, slide);
  drawRtopBox(pptx, slide);
  drawVectors(pptx, slide);
  drawClassify(pptx, slide);
  drawQuery(pptx, slide);
  drawGreenBox(pptx, slide);
  drawHeader(pptx, slide);
  drawMatrix(pptx, slide);
  drawResult(pptx, slide);
  drawFooter(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] || path.resolve(__dirname, "../slide_031_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = {
  renderBase, drawTitle, drawLeftBox, drawPlane, drawWLabel, drawAxes,
  drawPoints, drawProjections, drawAnnotations, drawRtopBox, drawVectors,
  drawClassify, drawQuery, drawGreenBox, drawHeader, drawMatrix, drawResult,
  drawFooter, C, PTS, MROWS, VEC_X, VEC_DLW,
};
