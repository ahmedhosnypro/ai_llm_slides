// Build slide 009 — "Overfit vs. Generalized" (metadata-only title; NO title ink on the frame)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Attempt 1 — fresh build from WIP measurements (qa/slide009/measurements_summary.txt)
//
// ═══════════════════════════════════════════════════════════════════════════════
// GROUND TRUTH: unique_slides/slide_009.jpg — 960x540, exactly 72 px/in
//                (verified: 960/13.3333 = 72.0001) => 1 frame px == 1 pt == 1/72 in.
// All geometry below is in FRAME PX == POINTS. Converted to inches by px().
// Measurement bank: recreated_pptx/qa/slide009/ (probe1..probe59 + measurements_summary.txt)
// ═══════════════════════════════════════════════════════════════════════════════
//
// CONTENT (all PIL-verified, see qa/slide009/measurements_summary.txt):
//   * NO title/subtitle text anywhere on the frame (validation.uncertain_items[0]
//     confirms slide_title 'Overfit vs. Generalized' is metadata-only) -> nothing drawn.
//   * Two side-by-side scatter charts, each: white interior inside a 1pt NAVY border,
//     16x16 light-gray grid, RED x/y axes with triangular arrowheads, a BLUE fitted
//     line, 12 ORANGE data points, one pale-red diagonal annotation stroke, and small
//     solid red discs. The LEFT chart additionally carries a large solid red disc.
//   * A pale-cyan annotation box inside each chart holding one black equation.
//   * Four caption lines BELOW the charts (2 per chart), Times-like serif, 17pt:
//     a RED bold keyword + a near-black regular remainder on line 1, all near-black
//     on line 2, each caption centred on its chart (centres 264 / 671 frame px).
//
// ── SPEC-vs-FRAME DEVIATIONS (frame wins per the judge GROUND RULES) ───────────
//  1. typography_notes claims the captions are "bold red" THROUGHOUT. Measurement
//     (probe44 per-row runs, probe45 font fits) shows ONLY the leading keyword is red;
//     the remainder of line 1 and all of line 2 are near-black #333333.
//  2. brief/dispatch describe a VERTICAL double-headed '50.85 mm' / '63.64 mm' arrow.
//     DIRECT frame re-read (2026-10-24, worker w009, attempt 4) shows the real
//     annotation: a ROTATED (-68 deg) red label '50.85 mm' / '63.64 mm' written along a
//     pale-rose dimension line that runs from the top-left outlier DOWN TO THE FITTED
//     LINE and ends in a small solid red arrowhead (LEFT tip 249,292; RIGHT tip 682,324),
//     plus a pale-rose callout leader with a red arrowhead pointing AT the outlier
//     (LEFT head 184..190,151..159; RIGHT head 600..606,145..154), plus light-periwinkle
//     dashed residual connectors from every orange point to the fitted line. The earlier
//     attempt-3 adjudication (adjudication_3_chartleft.txt) classified these as
//     hallucinations — that was WRONG: the labels are legible on the frame once the
//     region is de-rotated. All four elements are drawn here (frame wins over the spec's
//     vertical-arrow description; the spec's LABEL TEXT is verbatim and kept).
//  3. Spec colours #F5F5F5 chart interior / #CCCCCC grid / #0000FF line / #FFA500
//     points / #E0F0FF box: measurement confirms the family; the grid renders
//     slightly lighter than #CCCCCC (cores 207..238 over a 250 interior) so D8D8D6
//     is used, and the annotation box fill measures pale CYAN (interior median
//     237,251,250 — b>g>r) not pale blue, so E0F0FF is used (frame's JPEG tolerance).
//  4. The RIGHT chart's navy border is genuinely ~12pt wider than the LEFT's
//     (independent cuts at y=300: LEFT x95..465, RIGHT x486.5..869.5) — reproduced
//     as measured rather than symmetrised.
//
// ── FOUNDER DIRECTIVE 2026-10-25 (annotation correction) ──────────────────────
// The founder re-opened the annotation on the CERTIFIED render and named four
// defects. Owner feedback ranks above the frame, so the hand-drawn slant of the
// original is deliberately NOT reproduced:
//  1. the mm-labels must run ALONG the dimension arrows. They were rendered
//     ASCENDING (OOXML rot is clockwise-positive, so rot -68/-69 rises toward
//     the right); the frame's own labels DESCEND left->right (RIGHT label ink
//     PCA 66.6 deg over bbox x622..652, y209..265).
//  2. the dimension arrows must be ORTHOGONAL to the fitted line with the foot
//     exactly ON it. They carried the hand-drawn slant (LEFT 70.4 deg, RIGHT
//     68.2 deg) against the true perpendiculars 62.81 / 64.54 deg, and they
//     must be RED.
//  3. each arrow needs an UPPER arrowhead at the outlier end (double-headed).
//  4. the short leader beside the outlier must be EXACTLY PARALLEL to the
//     fitted line, RED, and must carry NO arrowhead. The old pale-rose tail
//     (2 deg off-parallel) and its red tailHead are deleted.
//
// Geometry (probe68/69): LEFT foot (269.43,285.03), u=(0.45691,0.88951),
// 62.81 deg; RIGHT foot (694.59,320.53), u=(0.42993,0.90286), 64.54 deg. The
// frame's corridors carry ONLY the periwinkle dashed residual connectors (no
// shaft ink), so the red arrow is built at the founder's construction; the
// parallel leader runs through the outlier on the fitted line's exact slope.
// The group now draws BEFORE the points so the orange outlier stays visible
// over the upper head's apex.
//
// ── EQUATIONS (deck math law: professional 2D format) ─────────────────────────
//   Both are single-line with a raised superscript -> mathtext PNGs rendered by the
//   CERTIFIED scripts/render_eq.py with matplotlib's default fontset (DejaVu Sans —
//   the frame's equation glyphs are SANS, no serifs; the attempt-1 STIX variant was
//   rejected on glyph shape).
//   ATTEMPT-4 CORRECTION (2026-10-24, worker w009): the attempt-1 PNGs (14.5pt) had
//   ink 98px wide vs the frame's measured 82px, and the placement code mistook the
//   600dpi 8px pad for frame px, so the last glyph overlapped the box border and the
//   line sat 5px high. Re-rendered at 12.1pt: PNG 717x111 / 719x111 px, INK 702px
//   (81.9pt) x 96px (11.2pt) = the frame's full ink width, dark-core height equal to
//   the frame's 10px core; ink box placed exactly on x226..307 / x643..723, y155..167.
//   Size law kept: addImage at exact px/600 size (never rescaled).
//   Placement: w=w_in, h=h_in at exact px/600 size (never rescaled) + eq_*.json
//   sidecars (eq_009_{left,right}_attempt4.json) for a future OMML wrap pass.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_009_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette ──────────────────────────────────────────────────────────
const NAVY      = "000080";   // chart-panel border  (frame core 0,0,108)
const INTERIOR  = "F5F5F5";   // chart interior      (frame ~248,248,248)
const GRID      = "D8D8D6";   // grid lines          (frame cores 207..238 over 250)
const RED       = "C00000";   // axes / red marks / caption keyword (house family)
const BLUE      = "0000FF";   // fitted lines        (frame core 0,0,132)
const ORANGE    = "FFA500";   // data points         (frame core 255,120,0)
const BIGRED    = "EE3145";   // the LEFT chart's large solid disc (frame core 238,49,69)
const BOXFILL   = "ECFDF9";   // annotation box fill (frame median 236,253,249 = pale cyan)
const BOXLINE   = "000080";   // annotation box border = navy (same as panel border)
const INK       = "333333";   // caption remainder ink (frame core 49,51,37)
const CONN      = "B4B2D2";   // light-periwinkle dashed residual connectors (frame core ~200,197,220)
const FONT      = "Times New Roman"; // serif, matches the frame (Liberation Serif metrics)

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top
// stroke on this deck), badge with numeral 9. Drawn ONCE, first (under content).
drawHouseChrome(pptx, slide, { numeral: 9 });

// Helpers
const rect = (x, y, w, h, fill) =>
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill },
  });
const stroked = (x, y, w, h, color, width) =>
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    line: { color: color, width: width },
  });
const ellipse = (cx, cy, d, fill) =>
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill },
  });
// Plain segment (no heads): always drawn left-to-right, flipV when the left end is
// the LOWER one (pptxgenjs phantom-segment pitfall: positive w/h + flipV only).
const seg = (xa, ya, xb, yb, color, width, dashType) => {
  const xl = Math.min(xa, xb), xr = Math.max(xa, xb);
  const yl = xa <= xb ? ya : yb, yr = xa <= xb ? yb : ya;
  const line = { color: color, width: width };
  if (dashType) line.dashType = dashType;
  slide.addShape(pptx.ShapeType.line, {
    x: px(xl), y: px(Math.min(yl, yr)), w: px(xr - xl), h: px(Math.abs(yr - yl)),
    flipV: yl > yr, line: line,
  });
};
// Solid triangular arrowhead with its TIP at (tipX,tipY) pointing along (ux,uy),
// base width bw, height h (measured bbox from the frame).
const head = (tipX, tipY, ux, uy, bw, h) => {
  const cx = tipX - ux * h / 2, cy = tipY - uy * h / 2;
  const rot = Math.atan2(ux, -uy) * 180 / Math.PI;
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(cx - bw / 2), y: px(cy - h / 2), w: px(bw), h: px(h),
    rotate: rot, fill: { color: RED },
  });
};

// ═══════════════════════════════════════════════════════════════════════════════
// CHART PANELS
// ═══════════════════════════════════════════════════════════════════════════════
// border lines are centred on the rect edge (1pt == 1 frame px)
// Panel measurements from probe40/probe41:
const PANELS = [
  {
    name: "LEFT",
    // Navy border rect (outer)
    bx: 95,   by: 107, bw: 371, bh: 367,
    // White interior
    fx: 98,   fy: 111, fw: 365, fh: 359,
    // Grid box
    col0: 103.5, colPitch: 23, nCol: 16,
    row0: 120.5, rowPitch: 22.4, nRow: 16,
    // Axes (red)
    axisX: 126.5, axisX0: 152, axisX1: 437,
    axisY: 434,   axisY0: 124, axisY1: 428,
    // Arrowheads
    headUp:   { cx: 126.5, tipY: 143, baseY: 151, halfW: 4.0 },
    headRight:{ cy: 434,   tipX: 435, baseX: 428, halfH: 3.5 },
    // Blue fitted line (measured from probe41)
    line: { x0: 141, y0: 351, x1: 433, y1: 201 },
    // Annotation group — founder directive 2026-10-25 (header block): RED
    // double-headed arrow ORTHOGONAL to the fitted line (foot exactly on it)
    // + a plain RED leader exactly parallel to the fitted line through the
    // outlier, carrying NO arrowhead + the label rotated to run along the arrow.
    dim: { x0: 197.5, y0: 145.0, x1: 269.43, y1: 285.03 },
    dimHeadLow: { tipX: 269.43, tipY: 285.03, ux: 0.45691, uy: 0.88951, bw: 7, h: 7.5 },
    dimHeadUp:  { tipX: 197.5,  tipY: 145.0,  ux: -0.45691, uy: -0.88951, bw: 8, h: 9 },
    tail: { x0: 176.5, y0: 155.79, x1: 197.5, y1: 145.0 },
    label: { text: "50.85 mm", cx: 210, cy: 212, rot: 62.8 },
    // Large red disc (left chart only) — sits ON the dimension line
    bigDisc: { cx: 232.5, cy: 241, d: 24.5 },
    // Data points (12 orange, measured from probe41)
    points: [
      [197.5, 145.0], [188.5, 355.5], [176.5, 380.5], [242.5, 327.5], [260.5, 333.5],
      [294.0, 333.5], [324.0, 290.0], [328.5, 332.0], [381.5, 301.5], [397.5, 249.0],
      [421.5, 255.0], [233.5, 362.0],
    ],
    gOff: 0,
  },
  {
    name: "RIGHT",
    bx: 486.5, by: 107, bw: 385, bh: 367,
    fx: 489.5, fy: 111, fw: 378, fh: 359,
    col0: 517.5, colPitch: 23, nCol: 16,
    row0: 120.5, rowPitch: 22.4, nRow: 16,
    axisX: 540,   axisX0: 152, axisX1: 437,
    axisY: 434,   axisY0: 538, axisY1: 841,
    headUp:   { cx: 540,   tipY: 143, baseY: 151, halfW: 3.5 },
    headRight:{ cy: 434,   tipX: 848, baseX: 841, halfH: 3.5 },
    line: { x0: 555, y0: 387, x1: 849, y1: 247 },
    // Same construction as LEFT (founder directive 2026-10-25): RED
    // double-headed arrow orthogonal to the fitted line + plain parallel leader.
    dim: { x0: 611.0, y0: 145.0, x1: 694.59, y1: 320.53 },
    dimHeadLow: { tipX: 694.59, tipY: 320.53, ux: 0.42993, uy: 0.90286, bw: 7, h: 8 },
    dimHeadUp:  { tipX: 611.0,  tipY: 145.0,  ux: -0.42993, uy: -0.90286, bw: 8, h: 9 },
    tail: { x0: 591.0, y0: 154.52, x1: 611.0, y1: 145.0 },
    label: { text: "63.64 mm", cx: 637, cy: 237, rot: 64.5 },
    bigDisc: null,
    points: [
      [611.0, 145.0], [601.5, 355.5], [589.5, 380.5], [656.0, 327.0], [674.0, 333.5],
      [707.5, 333.5], [737.5, 290.0], [741.5, 332.0], [794.0, 302.0], [810.0, 249.0],
      [834.5, 255.0], [647.0, 362.0],
    ],
    gOff: 413.5,
  },
];

for (const p of PANELS) {
  // 1. white interior (drawn first so the grid/axes sit on it)
  rect(p.fx, p.fy, p.fw, p.fh, INTERIOR);

  // 2. grid — 16 vertical + 16 horizontal 1pt lines inside the measured grid box.
  //    Grid box: x col0 .. col0+colPitch*(nCol-1); y row0 .. row0+rowPitch*(nRow-1)
  const gx0 = p.col0, gx1 = p.col0 + p.colPitch * (p.nCol - 1);
  const gy0 = p.row0, gy1 = p.row0 + p.rowPitch * (p.nRow - 1);
  for (let k = 0; k < p.nCol; k++) {
    const cx = p.col0 + p.colPitch * k;
    rect(cx - 0.5, gy0, 1, gy1 - gy0, GRID);
  }
  for (let k = 0; k < p.nRow; k++) {
    const cy = p.row0 + p.rowPitch * k;
    rect(gx0, cy - 0.5, gx1 - gx0, 1, GRID);
  }

  // 3. light-periwinkle DASHED residual connectors: one per point, from the point
  //    centre to its perpendicular foot on the fitted line (frame shows them under
  //    the points and under the line; distances < 9px have no visible connector).
  const { x0: lx0, y0: ly0, x1: lx1, y1: ly1 } = p.line;
  const ldx = lx1 - lx0, ldy = ly1 - ly0, l2 = ldx * ldx + ldy * ldy;
  for (const [cx, cy] of p.points) {
    const t = ((cx - lx0) * ldx + (cy - ly0) * ldy) / l2;
    const fx = lx0 + t * ldx, fy = ly0 + t * ldy;
    if (Math.hypot(fx - cx, fy - cy) < 9) continue;
    seg(cx, cy, fx, fy, CONN, 0.75, "dash");
  }

  // 4. blue fitted line (2pt; frame per-column core span 2-3px)
  //    pptxgenjs line: x/y is top-left of bbox; w/h is bbox; use flipV for upward lines
  slide.addShape(pptx.ShapeType.line, {
    x: px(p.line.x0), y: px(p.line.y1), w: px(p.line.x1 - p.line.x0),
    h: px(p.line.y0 - p.line.y1), flipV: true,
    line: { color: BLUE, width: 2 },
  });

  // 5. annotation group (founder directive 2026-10-25): RED double-headed arrow
  //    orthogonal to the fitted line (foot exactly on it), a plain RED leader
  //    exactly parallel to the fitted line through the outlier (NO arrowhead),
  //    then the large red disc (LEFT only, drawn AFTER the arrow so it covers
  //    it — as on the frame). Drawn BEFORE the points so the orange outlier
  //    stays visible over the upper head's apex.
  seg(p.dim.x0, p.dim.y0, p.dim.x1, p.dim.y1, RED, 1.0);
  seg(p.tail.x0, p.tail.y0, p.tail.x1, p.tail.y1, RED, 1.0);
  head(p.dimHeadLow.tipX, p.dimHeadLow.tipY, p.dimHeadLow.ux, p.dimHeadLow.uy, p.dimHeadLow.bw, p.dimHeadLow.h);
  head(p.dimHeadUp.tipX, p.dimHeadUp.tipY, p.dimHeadUp.ux, p.dimHeadUp.uy, p.dimHeadUp.bw, p.dimHeadUp.h);
  if (p.bigDisc) ellipse(p.bigDisc.cx, p.bigDisc.cy, p.bigDisc.d, BIGRED);

  // 6. 12 orange data points, d=7.5 (measured blob widths 6..8)
  for (const [cx, cy] of p.points) ellipse(cx, cy, 7.5, ORANGE);

  // 7. rotated measurement label ('50.85 mm' / '63.64 mm'), red bold, running
  //    ALONG the dimension arrow (rot = the arrow's own angle, 62.8 / 64.5 deg
  //    clockwise, so the text DESCENDS left->right as on the frame).
  slide.addText(p.label.text, {
    x: px(p.label.cx - 45), y: px(p.label.cy - 7), w: px(90), h: px(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 11, bold: true, color: RED,
    rotate: p.label.rot,
  });

  // 8. red axes (1pt shafts, centred on the measured axis)
  rect(p.axisX - 0.5, p.axisX0, 1, p.axisX1 - p.axisX0, RED); // vertical
  rect(p.axisY0, p.axisY - 0.5, p.axisY1 - p.axisY0, 1, RED); // horizontal

  // 9. triangular arrowheads (measured ~8x8 for the up-head, ~6x7 for the right-head)
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(p.headUp.cx - p.headUp.halfW), y: px(p.headUp.tipY),
    w: px(p.headUp.halfW * 2), h: px(p.headUp.baseY - p.headUp.tipY),
    fill: { color: RED },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(p.headRight.baseX), y: px(p.headRight.cy - p.headRight.halfH),
    w: px(p.headRight.halfH * 2), h: px(p.headRight.tipX - p.headRight.baseX),
    rotate: 90, fill: { color: RED },
  });

  // 10. navy border on top
  stroked(p.bx, p.by, p.bw, p.bh, NAVY, 1);
}

// ═══════════════════════════════════════════════════════════════════════════════
// ANNOTATION BOXES + EQUATION IMAGES
// ═══════════════════════════════════════════════════════════════════════════════
// Box: navy 1pt border centred on the rect edge, pale-cyan fill.
// LEFT  box x216..317 y147..175 (w102 h29);  top y148 (probe26/27)
// RIGHT box x631..734 y147..175 (w104 h29);  top y148
// Equation PNG ink starts ~8px (0.96pt) inside the image box; placed so the ink's
// left edge lands on the measured ink x and its top on y155.
const ASSETS = path.resolve(__dirname, "assets");
const BOXES = [
  // LEFT: x216..317 (w102), y148..175 (h27)
  // Attempt 4 (2026-10-24): the attempt-1 PNG (14.5pt DejaVu) rendered ink 98px wide —
  // 16px wider than the frame's measured 82px — and was placed with PNG-px padding
  // mistaken for frame px, so its last glyph overlapped the box border and it sat 5px
  // high. Re-rendered at 12.1pt (ink 702px = 81.9pt wide, 96px tall; certified
  // render_eq.py, DejaVu Sans = the frame's sans family) and placed so the INK box
  // lands exactly on the frame's measured ink bbox x226..307, y155..167.
  // PNG pad = 8px @600dpi = 0.8pt -> image x = (226-0.8)/72, y = (155-0.8)/72.
  { x: 216, y: 148, w: 102, h: 27,
    img: path.join(ASSETS, "eq_009_left_attempt4.png"),
    ix: 3.127778, iy: 2.141667, iw: 1.195, ih: 0.185 },
  // RIGHT: x631..734 (w104), y148..175 (h27); ink target x643..723, y155..167
  { x: 631, y: 148, w: 104, h: 27,
    img: path.join(ASSETS, "eq_009_right_attempt4.png"),
    ix: 8.919444, iy: 2.141667, iw: 1.198333, ih: 0.185 },
];

for (const b of BOXES) {
  // Box background + border
  slide.addShape(pptx.ShapeType.rect, {
    x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
    fill: { color: BOXFILL }, line: { color: BOXLINE, width: 1 },
  });
  // Equation image at exact px/600 size
  slide.addImage({ path: b.img, x: b.ix, y: b.iy, w: b.iw, h: b.ih });
}

// ═══════════════════════════════════════════════════════════════════════════════
// CAPTION-BAND ROSE ANNOTATION BOXES — PIL-measured on the frame 2026-10-24.
// Each caption sits inside a CREAM-FILLED, rose-outlined box that is open at the
// top: left + right verticals plus a bottom rule, no top stroke. Drawn BEFORE
// the captions so the ink sits on the fill, exactly as the hand annotation does.
//   LEFT  box x95..434 y479..529 ; RIGHT box x501..842 y479..529 (frame px)
// Fill medians 251,252,236 (cream) on both sides; stroke cores measured per side
// (the frame's JPEG halos widen each stroke ~1-2px around the cores below).
// ═══════════════════════════════════════════════════════════════════════════════
const CAPFILL = "FBFCEC"; // caption-box fill (frame median 251,252,236)
const BANDS = [
  { fill: { x: 97,    y: 480,  w: 335, h: 47, c: CAPFILL },
    strokes: [
      { x: 95.5,  y: 479,   w: 2, h: 49, c: "E2C6C3" }, // left vertical  (226,198,195)
      { x: 432.5, y: 479,   w: 2, h: 49, c: "F0E6E7" }, // right vertical (240,230,231)
      { x: 96,    y: 527.5, w: 337, h: 2, c: "DCBBBB" }, // bottom rule   (220,187,187)
    ] },
  { fill: { x: 504,   y: 480,  w: 335, h: 47, c: CAPFILL },
    strokes: [
      { x: 502,   y: 479,   w: 2, h: 49, c: "D3BCB9" }, // left vertical  (211,188,185)
      { x: 839.5, y: 479,   w: 2, h: 49, c: "CAA5A6" }, // right vertical (202,165,166)
      { x: 503,   y: 527.5, w: 337, h: 2, c: "D9BBBA" }, // bottom rule   (217,187,186)
    ] },
];
for (const band of BANDS) {
  rect(band.fill.x, band.fill.y, band.fill.w, band.fill.h, band.fill.c);
  for (const s of band.strokes) rect(s.x, s.y, s.w, s.h, s.c);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CAPTIONS — 2 lines per chart, each line centred on its chart (264 / 671)
// ═══════════════════════════════════════════════════════════════════════════════
// Per-line boxes; y = baseline - fontSize (LO box-top -> baseline ~1.0 em)
const BASE_OFF = 1.0;
function captionLine(cx, baseline, w, runs, size) {
  slide.addText(runs, {
    x: px(cx - w / 2), y: px(baseline - size * BASE_OFF), w: px(w), h: px(34),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: size, lineSpacing: size * 1.2,
  });
}
const R = (text, o) => Object.assign({ text: text, options: o || {} });

// LEFT — line 1: red bold 'Overfit' + near-black regular remainder
captionLine(264, 500, 380, [
  R("Overfit", { bold: true, color: RED }),
  R(" (try to minimize the residuals ONLY)", { color: INK }),
], 17);
// LEFT — line 2: all near-black
captionLine(264, 519, 380, [
  R("Fails to detect the Pattern", { color: INK }),
], 17);
// RIGHT — line 1
captionLine(671, 500, 360, [
  R("Generalized", { bold: true, color: RED }),
  R(" (Residuals are not minimized)", { color: INK }),
], 17);
// RIGHT — line 2 ('Successes' sic — source grammar preserved)
captionLine(671, 519, 360, [
  R("Successes to detect the Pattern", { color: INK }),
], 17);

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
