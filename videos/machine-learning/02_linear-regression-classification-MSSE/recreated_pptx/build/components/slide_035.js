// COMPONENT (certified) — banked by ml02-w035-g3 after judge PASS
// (qa/slide035/judge_attempt_3.txt: "FINAL VERDICT: **PASS** for 'faithful, usable
// recreation'." — no BLOCKER/MAJOR; 3 MINORs all frame-measured non-triggers, see
// qa/slide035/worker_report.md. Dependency law: 035 is a structural SIBLING of the
// certified slide_031 — house chrome + 031's drawing conventions shared; every
// content block is 035's own measured delta at its own geometry; parent untouched.)
// slide_035.js — "y = 0 x1 − 2 x2 + 3" dot-product classification sketch
// (ML lecture 02; CHILD of certified slide 31 — dependency edge 35 > 31).
// Worker ml02-w035-g2 (gen-2, after gen-1 storm loss), 2026-10-14. Built from PIL
// measurements banked in scratch/ml02/slide035/ (m01..m16 + GEOMETRY.md) against
// unique_slides/slide_035.jpg (960x540, 1px=1pt).
//
// Composition law: 035 is a structural SIBLING of 031, not a duplicate (PIL
// compare m01: 58.5% exact-ish). Only the house chrome and the parent's
// drawing conventions (helpers below, replicated verbatim from the certified
// components/slide_031.js) are shared; EVERY content block is drawn as a delta
// at 035's own measured geometry. No parent export is called (parent's content
// geometry differs); the parent file is untouched.
//
// Structure: house chrome (shared module, numeral 35) + red-bordered white
// sketch panel holding the yellow parallelogram band W, 3 thin red axes with
// red tick digits (y:3, x1:3/7) and red x1/x2 labels, 3 orange + 2 blue data
// points, solid blue disc, navy '?' disc, dashed/dotted gray projection lines,
// rotated two-line -ve(C2, blue)/+ve(C1, red) annotations + red arrow; right
// calc box "Check Class of Test Vector" (blue/red/blue runs) with dark rule,
// banner box (pale FFFFDD) with the model equation y = 0x1 − 2x2 + 3 (0,2 blue;
// 3 red), and the dot-product: X^T (1 7 3) · W column (3;0;−2) = −3 ⇒ C2 (red ⇒).
// Row bias '1' is RED (m32 stem core (127,19,42)); 7/3(row)/3(col)/0/−2 black —
// TWO separate '3's (m32: row @642, col @683; the old "shared red corner 3" was wrong).
//
// Equations/labels: matplotlib mathtext (STIX), 600dpi transparent PNGs
// (scripts/render_eq.py), embedded at EXACT ink px/600 size, anchored at the
// ORIGINAL's measured ink-left / baseline / ink-center (eq035_manifest.json).
// Delimiters: thin gray curved parens — PIL parabolic arcs (parent 031's
// certified gen_parens031.py pattern, m19/m32/m33) — NOT straight bars.

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const PX = 1 / 72; // frame px -> inches
const ASSET = (n) => path.resolve(__dirname, "assets", n + ".png");
const MAN = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq035_manifest.json"), "utf8"));

// ---- measured palette (035 frame cores) --------------------------------------
const C = {
  inkBlack: "000000",       // dark equation glyphs / W label
  eqBlue: "0000CC",         // banner 0,2 + X^T/W labels + blue points/-ve label
  eqRed: "CC0000",          // banner 3, row bias '1', col top '3', '=>', +ve label, red arrow
  boxRed: "C00000",         // diagram panel border + axes + arrowheads (cores (140,0,13))
  panelBorder: "B4BAC0",    // calc box border (1px dilutes to (200..214) in JPEG)
  bandFill: "FFFF85",       // yellow band
  bannerFill: "FFFFDD",     // banner box (255,255,221)
  bannerBorder: "C9CABA",   // banner box top border (201,202,186)
  barGray: "969896",        // delimiter bars (149,151,148)
  dashGray: "AAAAAA",       // dashed/dotted projection lines
  ruleDark: "333333",       // heading rule (37,41,44)/(54,56,68)
  faintLine: "C9C3F2",      // X^T/W underlines ((231,220,255) on white)
  qNavy: "000080",          // '?' disc core (10,5,126)
};

// ---- equation PNG placement (ink-anchored; PNG px = 1/600 in) -----------------
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

// ---- left red-bordered white sketch panel -------------------------------------
function drawPanel(pptx, slide) {
  // border strokes: top rows 108-109, right x493-495, left x79-80, bottom 528-529
  slide.addShape(pptx.ShapeType.rect, {
    x: 79.5 * PX, y: 107.5 * PX, w: 415 * PX, h: 421 * PX,
    fill: { color: "FFFFFF" }, line: { color: C.boxRed, width: 2 },
  });
}

// ---- yellow parallelogram band (no border) -------------------------------------
function drawBand(pptx, slide) {
  // extremes: top (179.5,133.5), right (398,419.5), bottom (317.5,522.5), left (89,236)
  poly(pptx, slide, [[179.5, 133.5], [398, 419.5], [317.5, 522.5], [89, 236]], C.bandFill);
}

// ---- dashed gray + dotted gray guide lines --------------------------------------
function drawDash(pptx, slide) {
  // horizontal dashed guide through the '?' disc to the x1 axis (dash (210,210,210))
  hline(pptx, slide, 131, 361, 470.5, C.dashGray, 1, "dash");
  // faint dotted diagonal from the x1 '3' tick down-left to the axis (m07)
  seg(pptx, slide, 206, 390, 146, 462, C.dashGray, 1, { dashType: "sysDot" });
  // dotted projections from the x2-axis ticks to the points (m25/m28/m30)
  seg(pptx, slide, 315.5, 334, 297, 352, C.dashGray, 1, { dashType: "sysDot" });   // tick '1' -> orange2
  hline(pptx, slide, 299, 339, 354, C.dashGray, 1, "sysDot");                      // orange2 <-> blue1
  seg(pptx, slide, 362.5, 333, 345, 350, C.dashGray, 1, { dashType: "sysDot" });   // tick '2' -> blue1
  seg(pptx, slide, 399, 333, 290, 469, C.dashGray, 1, { dashType: "sysDot" });     // tick '3' -> '?' disc
}

// ---- three thin red axes with filled arrowheads ----------------------------------
function drawAxes(pptx, slide) {
  // y-axis: vertical x271.5, origin (271.5,332) up; arrowhead tip (272,118)
  vline(pptx, slide, 271.5, 332, 124.5, C.boxRed, 1);
  poly(pptx, slide, [[272, 118], [268.3, 125], [275.7, 125]], C.boxRed);
  // x2-axis: horizontal y332 right; arrowhead tip (463.5,332)
  hline(pptx, slide, 271.5, 457, 332, C.boxRed, 1);
  poly(pptx, slide, [[463.5, 332], [456.5, 328.5], [456.5, 335.5]], C.boxRed);
  // x1-axis: diagonal down-left (slope -1); arrowhead tip (110,499)
  seg(pptx, slide, 271.5, 332, 116, 493.5, C.boxRed, 1);
  poly(pptx, slide, [[110, 499], [118.2, 495.8], [113.2, 490.8]], C.boxRed);
}

// ---- red tick digits + red axis labels --------------------------------------------
function drawTicks(pptx, slide) {
  drawImg(slide, eqTop("e35_yax", 256, 132));        // y-axis label 'y' (256..262, 132..141; m42: arms+descender, NOT a '3')
  drawImg(slide, eqBaseline("e35_tk3m", 262.5, 256)); // mid-axis '3' tick at band crossing (262..267, 246..256)
  drawImg(slide, eqBaseline("e35_tk3x", 195, 402));  // x1 '3' (196..205, 392..402)
  drawImg(slide, eqBaseline("e35_tk7", 123, 486));   // x1 '7' (124..131, 478..486)
  drawImg(slide, eqBaseline("e35_ax1", 97, 493));    // 'x1' (97..123, 486..500)
  drawImg(slide, eqBaseline("e35_ax2", 441, 346));   // 'x2' (441..452, 339..348)
  drawImg(slide, eqBaseline("e35_t1", 318.5, 329.5));   // x2 tick '1' (318..321, 321..329)
  drawImg(slide, eqBaseline("e35_t2", 358, 329.5));     // x2 tick '2' (358..364, 320..329)
  drawImg(slide, eqBaseline("e35_tk3y", 393, 328.5));   // x2 tick '3' (393..398, 318..327; reuse y-axis '3')
}

// ---- black W label over the band + black underline (m22/m23: bar x179..201, y190..191) ----
function drawWLabel(pptx, slide) {
  drawImg(slide, eqTop("e35_w", 179, 171));  // ink 179..201, 171..191
  hline(pptx, slide, 179, 201, 190.5, C.inkBlack, 1);
}

// ---- data points (3 orange, 2 blue; d~7-8px) ---------------------------------------
const PTS = [
  { x: 265, y: 251, c: "C88313" },
  { x: 295, y: 354, c: "C88313" },
  { x: 280, y: 373, c: "C88313" },
  { x: 343, y: 354, c: C.eqBlue },
  { x: 324, y: 373, c: C.eqBlue },
];
function drawPoints(pptx, slide) {
  PTS.forEach((p) => slide.addShape(pptx.ShapeType.ellipse, {
    x: (p.x - 4) * PX, y: (p.y - 4) * PX, w: 8 * PX, h: 8 * PX,
    fill: { color: p.c }, line: { color: p.c, width: 0 },
  }));
}

// ---- solid blue disc + navy '?' disc with white ? -----------------------------------
function drawDiscs(pptx, slide) {
  // solid blue disc (170,310) d17 (core (2,0,206))
  slide.addShape(pptx.ShapeType.ellipse, {
    x: 161.5 * PX, y: 301.5 * PX, w: 17 * PX, h: 17 * PX,
    fill: { color: C.eqBlue }, line: { color: C.eqBlue, width: 0 },
  });
  // navy '?' disc (289.5,469.5) d17 (core (10,5,126)) + white '?' (light interior)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: 281 * PX, y: 461 * PX, w: 17 * PX, h: 17 * PX,
    fill: { color: C.qNavy }, line: { color: C.qNavy, width: 0 },
  });
  slide.addText("?", {
    x: (289.5 - 30) * PX, y: (469.5 / 72) - 0.3, w: 60 * PX, h: 0.6,
    align: "center", valign: "middle", margin: 0,
    fontSize: 13, bold: true, color: "FFFFFF", fontFace: "Arial",
  });
}

// ---- rotated two-line -ve/+ve annotations + red arrow --------------------------------
function drawAnnotations(pptx, slide) {
  // blue annotation: frame line order is 'Class C2' FIRST (up-right, m41 corridor
  // fragments (174..189,272..291) on a path parallel to '-ve ( < 0 )'), '-ve ( < 0 )'
  // second (down-left chain (133,252)->(158,281)); per-line perp distance 17 (m41),
  // NOT 30. Block center (162,273) — RENDER-VERIFIED (gen-3 re-read of m27 pixel art:
  // the '-ve ( < 0 )' line runs (133,252)->(174,301) — '0' glyph (157..168,283..293),
  // ')' (168..174,295..301) ending at the blue disc edge — true line2 center (153.5,276.5);
  // (162,273) renders line2 at (155.5,278.5), ~3px off. The gen-2 (152,261) anchor used the
  // truncated chain (133,252)->(158,281) and overshoots ~10px up-left; reverted to the last
  // closed-loop-verified value (check_035_4 residual box delta is font-metric, not position).
  slide.addText("Class C2\n-ve ( < 0 )", {
    x: (162 - 65) * PX, y: (273 / 72) - 0.45, w: 130 * PX, h: 0.9,
    align: "center", valign: "middle", margin: 0,
    fontSize: 11, color: C.eqBlue, fontFace: "Arial", rotate: 50, lineSpacing: 17,
  });
  // red '+ve ( > 0 ) / Class C1': line centers (124,318)/(108,327.3) (m27/m41),
  // perp distance 17.1; block center (116,323).
  slide.addText("+ve ( > 0 )\nClass C1", {
    x: (116 - 65) * PX, y: (323 / 72) - 0.45, w: 130 * PX, h: 0.9,
    align: "center", valign: "middle", margin: 0,
    fontSize: 11, color: C.eqRed, fontFace: "Arial", rotate: 50, lineSpacing: 17,
  });
  // red arrow (m23/m27: frame red ink max ~(151,350); head blob (144..153,344..352)).
  // NO blue arrow: the frame's blue corridor (150..205, 272..322) holds ONLY the
  // 'Class C2' glyphs + the disc (m41/m43); the judge-2 "blue arrow" was that text line.
  seg(pptx, slide, 135, 313, 152, 349, C.eqRed, 1.25, { endArrowType: "triangle" });
}

// ---- right calc box -------------------------------------------------------------------
function drawCalcBox(pptx, slide) {
  // border strokes: x533-534 / 840-841, y214-215 / 364-365
  slide.addShape(pptx.ShapeType.rect, {
    x: 533.5 * PX, y: 214.5 * PX, w: 307 * PX, h: 150 * PX,
    fill: { color: "FFFFFF" }, line: { color: C.panelBorder, width: 1 },
  });
}

// ---- heading "Check Class of Test Vector" + DARK rule ----------------------------------
function drawHeading(pptx, slide) {
  // ink x545..780, cap band y225..239; 'Check'+'of Test Vector' blue, 'Class' red
  slide.addText([
    { text: "Check  ", options: { color: C.eqBlue } },
    { text: "Class", options: { color: C.eqRed } },
    { text: " of Test Vector", options: { color: C.eqBlue } },
  ], {
    x: 544 * PX, y: (232 / 72) - 0.3, w: 240 * PX, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontSize: 19, bold: true, fontFace: "Arial", charSpacing: -0.5,
  });
  // dark rule under the heading (cores (37,41,44); NOT the parent's light rule)
  hline(pptx, slide, 546, 780, 240.8, C.ruleDark, 1);
}

// ---- blue X^T / W labels above the operands + faint underlines -------------------------
function drawXTW(pptx, slide) {
  drawImg(slide, eqBaseline("e35_xt", 608, 267));  // X^T: X 608..618 (253..267), T sup
  drawImg(slide, eqBaseline("e35_wl", 680, 266));  // W 680..696 (251..266)
  hline(pptx, slide, 605, 627, 269.5, C.faintLine, 0.75);
  hline(pptx, slide, 678, 698, 268, C.faintLine, 0.75);
}

// ---- gray curved paren delimiters (m19/m32: thin parabolic arcs, NOT straight bars) ------
// PIL parens are tight-cropped (ink_dx=ink_dy=0): x,y = ink top-left, size = frame_w/frame_h.
function drawBars(pptx, slide) {
  // row vector: '(' apex 576 (tips ~577.5) y278..296; ')' tips 655 (apex ~656.8) y278..296
  slide.addImage({ path: ASSET("e35_pl_s"), x: 576 * PX, y: 278 * PX, w: MAN.e35_pl_s.frame_w, h: MAN.e35_pl_s.frame_h });
  slide.addImage({ path: ASSET("e35_pr_s"), x: 655 * PX, y: 278 * PX, w: MAN.e35_pr_s.frame_w, h: MAN.e35_pr_s.frame_h });
  // W column: '(' apex 668.5 (tips ~670.5) y276..353; ')' tips 703 (apex ~704.8) y275..353
  slide.addImage({ path: ASSET("e35_pl_t"), x: 668.5 * PX, y: 276 * PX, w: MAN.e35_pl_t.frame_w, h: MAN.e35_pl_t.frame_h });
  slide.addImage({ path: ASSET("e35_pr_t"), x: 703 * PX, y: 275 * PX, w: MAN.e35_pr_t.frame_w, h: MAN.e35_pr_t.frame_h });
}

// ---- banner box (pale yellow) ------------------------------------------------------------
function drawBannerBox(pptx, slide) {
  // box x564.5..739, y108..142; fill (255,255,221), top border (201,202,186)
  slide.addShape(pptx.ShapeType.rect, {
    x: 564.5 * PX, y: 108 * PX, w: 174.5 * PX, h: 34 * PX,
    fill: { color: C.bannerFill }, line: { color: C.bannerBorder, width: 0.75 },
  });
}

// ---- banner equation: y = 0 x1 − 2 x2 + 3 (baseline 131; 0,2 blue; 3 red) ----------------
function drawBannerEq(pptx, slide) {
  drawImg(slide, eqBaseline("e35_yb", 568, 131));
  drawImg(slide, eqCenter("e35_eqb", 585, 124));
  drawImg(slide, eqBaseline("e35_b0", 606, 131));
  drawImg(slide, eqBaseline("e35_bx1", 623, 131));
  drawImg(slide, eqCenter("e35_bmi", 647, 124));
  drawImg(slide, eqBaseline("e35_b2", 668, 131));
  drawImg(slide, eqBaseline("e35_bx2", 683, 131));
  drawImg(slide, eqCenter("e35_bpl", 707, 123.5));
  drawImg(slide, eqBaseline("e35_b3", 726, 131));
}

// ---- calc dot-product equation -------------------------------------------------------------
function drawCalcEq(pptx, slide) {
  // 'y =' split pieces (mathtext space too wide vs measured 4-5px gaps)
  drawImg(slide, eqBaseline("e35_yc", 546, 301));
  drawImg(slide, eqCenter("e35_eqc", 561, 296));
  // row vector (1 7 3): bias '1' RED (m32 stem core (127,19,42)), 7 @612, 3 @642
  drawImg(slide, eqBaseline("e35_r1", 584, 295));
  drawImg(slide, eqBaseline("e35_r7", 612, 295.5));
  drawImg(slide, eqBaseline("e35_r3", 642, 295.5));
  // W column entries 3 / 0 / −2: top '3' RED (m43 core (156,52,75) = same red family
  // as row '1' (127,19,42) and banner 3 (172,7,17); 0/−2 black cores (33-68))
  drawImg(slide, eqBaseline("e35_c3r", 683, 294.5));
  drawImg(slide, eqCenter("e35_c0", 682, 313.5));
  drawImg(slide, eqBaseline("e35_cm2", 675, 346));
  // tail '= −3 ⇒ C2'
  drawImg(slide, eqCenter("e35_teq", 716, 295.5));
  drawImg(slide, eqBaseline("e35_tm3", 736, 302));
  drawImg(slide, eqCenter("e35_timp", 779, 296.5));   // RED ⇒
  drawImg(slide, eqBaseline("e35_tc2", 808, 302));
}

// ---- slide assembly (chrome FIRST, once) ----------------------------------------------------
function renderSlide(pptx, slide) {
  drawHouseChrome(pptx, slide, { numeral: 35 });
  drawPanel(pptx, slide);
  drawBand(pptx, slide);
  drawDash(pptx, slide);
  drawAxes(pptx, slide);
  drawTicks(pptx, slide);
  drawWLabel(pptx, slide);
  drawPoints(pptx, slide);
  drawDiscs(pptx, slide);
  drawAnnotations(pptx, slide);
  drawCalcBox(pptx, slide);
  drawHeading(pptx, slide);
  drawXTW(pptx, slide);
  drawBars(pptx, slide);
  drawBannerBox(pptx, slide);
  drawBannerEq(pptx, slide);
  drawCalcEq(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderSlide(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] || path.resolve(__dirname, "../slide_035_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderSlide, drawPanel, drawBand, drawAxes, drawTicks, drawWLabel,
  drawPoints, drawDiscs, drawAnnotations, drawCalcBox, drawHeading, drawXTW,
  drawBars, drawBannerBox, drawBannerEq, drawCalcEq, C, PTS };
