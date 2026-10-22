// Build slide 009 — "Overfit vs. Generalized" (metadata-only title; NO title ink on the frame)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// ══════════════════════════════════════════════════════════════════════════════
// GROUND TRUTH: unique_slides/slide_009.jpg — 960x540, exactly 72 px/in
//                (verified: 960/13.3333 = 72.0001) => 1 frame px == 1 pt == 1/72 in.
// All geometry below is in FRAME PX == POINTS. Converted to inches by px().
// Measurement bank: recreated_pptx/qa/slide009/ (probe1..probe57 + measurements_summary.txt)
// ══════════════════════════════════════════════════════════════════════════════
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
//  2. brief/dispatch ask for vertical '50.85 mm' / '63.64 mm' arrows and labels.
//     NO 'mm' text and NO vertical double-arrow exist on the frame (probe28/29/30/44:
//     zero dark components in that region). NOT drawn.
//  3. Spec colours #F5F5F5 chart interior / #CCCCCC grid / #0000FF line / #FFA500
//     points / #E0F0FF box: measurement confirms the family; the grid renders
//     slightly lighter than #CCCCCC (cores 207..238 over a 250 interior) so D8D8D6
//     is used, and the annotation box fill measures pale CYAN (interior median
//     237,251,250 — b>g>r) not pale blue, so EDFBFA is used.
//  4. The RIGHT chart's navy border is genuinely ~12pt wider than the LEFT's
//     (independent cuts at y=300: LEFT x95..465, RIGHT x486.5..869.5) — reproduced
//     as measured rather than symmetrised.
//
// ── EQUATIONS (deck math law: professional 2D format) ─────────────────────────
//   Both are single-line with a raised superscript -> mathtext PNGs rendered by the
//   CERTIFIED scripts/render_eq.py loaded with matplotlib's STIX serif fontset
//   (the slide's typeface is serif/Times-like; STIX matches look AND measured ink
//   proportions far better than the default sans — see probe55/probe56).
//   Loader: qa/slide009/probe56_eqstix.py (certified module loaded UNCHANGED).
//   Size calibration (STIX, fs=14.5) against the frame's measured ink:
//     ink box    render 81.96x13.20pt / 82.68x13.20pt   frame 82x13 / 81x13
//     digit hgt  render 9.84..10.20pt                    frame 10pt (y157..166)
//     superscript render 6.84pt                          frame 6pt  (y155..160)
//     glyph pitch render 7.6pt                            frame ~7.4pt
//   fs=15 was rejected (ink 3.5..5.4% too wide); fs=14.5 matches within 1.7%.
//   Placement: w=w_in, h=h_in at exact px/600 size (never rescaled) + eq_*.json
//   sidecars for the orchestrator's OMML dual-representation wrap pass.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_009_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette ──────────────────────────────────────────────────────────
const NAVY = "000080";   // chart-panel border  (frame core 0,0,108)
const INTERIOR = "F5F5F5"; // chart interior     (frame ~250,252,249)
const GRID = "D8D8D6";   // grid lines          (frame cores 207..238 over 250)
const RED = "C00000";    // axes / red marks / caption keyword (house family)
const BLUE = "0000FF";   // fitted lines        (frame core 0,0,132)
const ORANGE = "FFA500"; // data points         (frame core 255,120,0)
const BIGRED = "EE3145"; // the LEFT chart's large solid disc (frame core 238,49,69)
const BOXFILL = "EDFBFA"; // annotation box fill (frame interior median 237,251,250)
const BOXLINE = "B4BAD1"; // annotation box border (frame border cores 171..195 / 176..202 / 206..221)
const INK = "333333";    // caption remainder ink (frame core 49,51,37)
const FONT = "Times New Roman"; // serif, matches the frame (Liberation Serif metrics)

// ── orange data points (d=7.5; measured blob widths 6..8, core 255,120,0) ────
const POINTS = {
  LEFT: [
    [197.5, 145.0], [188.5, 355.5], [176.5, 380.5], [242.5, 327.5], [260.5, 333.5],
    [294.0, 333.5], [324.0, 290.0], [328.5, 332.0], [381.5, 301.5], [397.5, 249.0],
    [421.5, 255.0], [233.5, 362.0],
  ],
  RIGHT: [
    [611.0, 145.0], [601.5, 355.5], [589.5, 380.5], [656.0, 327.0], [674.0, 333.5],
    [707.5, 333.5], [737.5, 290.0], [741.5, 332.0], [794.0, 302.0], [810.0, 249.0],
    [834.5, 255.0], [647.0, 362.0],
  ],
};

// ── small solid red discs (C00000; measured loose diameters 8..10.5) ──────────
const DISCS = {
  LEFT:  [[186.5, 155.0, 10.0], [247.0, 289.0, 9.0]],
  RIGHT: [[603.0, 150.0, 9.0], [679.0, 320.5, 9.5]],
};

// ── annotation boxes + equation images ───────────────────────────────────────
// Box: 1pt border centred on the rect edge, pale-cyan fill. LEFT h=26 / RIGHT
// h=27 (both top borders at y148; the bottom border measures y174 left, y175 right).
// Equation PNG ink starts 8px (0.96pt) inside the image box; placed so the ink's
// left edge lands on the measured ink x and its top on y155:
//   LEFT  ink lands at frame x226..307.96 / y155..167.12 (frame measured 226..307 / 155..167)
//   RIGHT ink lands at frame x643..725.68 / y155..167.12 (frame measured 643..723 / 155..167)
const ASSETS = path.resolve(__dirname, "assets");
const BOXES = [
  { x: 216.5, y: 148, w: 100, h: 26,
    img: path.join(ASSETS, "eq_009_left.png"),  ix: 3.125556, iy: 2.139444,
    iw: 1.163333, ih: 0.208333 },
  { x: 633.5, y: 148, w: 100, h: 27,
    img: path.join(ASSETS, "eq_009_right.png"), ix: 8.917222, iy: 2.139444,
    iw: 1.173333, ih: 0.208333 },
];

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top
// stroke on this deck), badge with numeral 9. Drawn ONCE, first (under content).
drawHouseChrome(pptx, slide, { numeral: 9 });

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

// ══════════════════════════════════════════════════════════════════════════════
// CHART PANELS
// ══════════════════════════════════════════════════════════════════════════════
// border lines are centred on the rect edge (1pt == 1 frame px)
const PANELS = [
  { name: "LEFT",  bx: 95,    by: 110, bw: 370, bh: 362,   // navy border rect
    fx: 96,    fy: 111, fw: 369, fh: 361,                   // white interior
    col0: 103.5, colPitch: 23, nCol: 16,                    // vertical grid lines
    row0: 120.5, rowPitch: 22.4, nRow: 16,                  // horizontal grid lines
    axisX: 126.5, axisX0: 152, axisX1: 434,                 // y-axis (vertical)
    axisY: 434, axisY0: 127, axisY1: 434,                   // x-axis (horizontal)
    headUp:   { cx: 126.5, tipY: 142, baseY: 151, halfW: 4.0 },
    headRight:{ cy: 434,  tipX: 436, baseX: 430, halfH: 3.5 },
    line: { x0: 141, y0: 352, x1: 433, y1: 199 },           // blue fitted line
    diag: { x0: 199, y0: 198, x1: 232, y1: 241 },           // pale-red annotation stroke
    bigDisc: { cx: 232.5, cy: 241, d: 24.5 },
    gOff: 0 },
  { name: "RIGHT", bx: 486.5, by: 110, bw: 383, bh: 362,
    fx: 487.5, fy: 111, fw: 382, fh: 361,
    col0: 517.5, colPitch: 23, nCol: 16,
    row0: 120.5, rowPitch: 22.4, nRow: 16,
    axisX: 540, axisX0: 152, axisX1: 434,
    axisY: 434, axisY0: 540, axisY1: 847,
    headUp:   { cx: 540, tipY: 142, baseY: 151, halfW: 3.5 },
    headRight:{ cy: 434,  tipX: 849, baseX: 843, halfH: 3.5 },
    line: { x0: 555, y0: 389, x1: 849, y1: 247 },
    diag: { x0: 626, y0: 208, x1: 646, y1: 264 },
    bigDisc: null,
    gOff: 413.5 },
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

  // 3. blue fitted line (2pt; frame per-column core span 2-3px)
  slide.addShape(pptx.ShapeType.line, {
    x: px(p.line.x0), y: px(p.line.y1), w: px(p.line.x1 - p.line.x0),
    h: px(p.line.y0 - p.line.y1), flipV: true,
    line: { color: BLUE, width: 2 },
  });

  // 4. 12 orange data points, d=7.5 (measured blob widths 6..8)
  for (const [cx, cy] of POINTS[p.name]) ellipse(cx, cy, 7.5, ORANGE);

  // 5. pale-red diagonal annotation stroke (2pt; measured core 2-3px, pale halo)
  slide.addShape(pptx.ShapeType.line, {
    x: px(p.diag.x0), y: px(p.diag.y0), w: px(p.diag.x1 - p.diag.x0),
    h: px(p.diag.y1 - p.diag.y0), line: { color: RED, width: 2 },
  });

  // 6. red axes (1pt shafts, centred on the measured axis)
  rect(p.axisX - 0.5, p.axisX0, 1, p.axisX1 - p.axisX0, RED); // vertical
  rect(p.axisY0, p.axisY - 0.5, p.axisY1 - p.axisY0, 1, RED); // horizontal

  // 7. triangular arrowheads (measured ~8x8 for the up-head, ~6x7 for the right-head)
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

  // 8. red marks: small solid discs (+ the LEFT chart's large solid disc)
  for (const [cx, cy, d] of DISCS[p.name]) ellipse(cx, cy, d, RED);
  if (p.bigDisc) ellipse(p.bigDisc.cx, p.bigDisc.cy, p.bigDisc.d, BIGRED);

  // 9. navy border on top
  stroked(p.bx, p.by, p.bw, p.bh, NAVY, 1);
}

// ══════════════════════════════════════════════════════════════════════════════
// ANNOTATION BOXES + EQUATION IMAGES
// ══════════════════════════════════════════════════════════════════════════════
// Box border 1pt centred on the box edge; fill pale cyan. Equation ink placed so
// its tight-ink left edge lands on the measured ink x, and its ink top on y155.
// ix/iy/iw/ih are ALREADY IN INCHES (px/600 of the 600-dpi render).
for (const b of BOXES) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
    fill: { color: BOXFILL }, line: { color: BOXLINE, width: 1 },
  });
  slide.addImage({ path: b.img, x: b.ix, y: b.iy, w: b.iw, h: b.ih });
}

// ══════════════════════════════════════════════════════════════════════════════
// CAPTIONS — 2 lines per chart, each line centred on its chart (264 / 671)
// ══════════════════════════════════════════════════════════════════════════════
// Per-line boxes (no inter-line pitch to diverge on); y = baseline - fontSize
// (LO box-top -> baseline distance calibrated at 1.0 em, slide_023/035 idiom).
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
