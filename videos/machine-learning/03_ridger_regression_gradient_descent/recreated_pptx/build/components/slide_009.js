// components/slide_009.js — BANKED composition of slide 009
// ("Overfit vs. Generalized" — metadata-only title; NO title ink on the frame),
// ML lecture 03 (03_ridger_regression_gradient_descent). BANKED post-PASS
// (playlist-scoped component-banking obligation, 17_worker_instructions.md):
// slide 010's dispatch brief declares a dependency on build/components/slide_009.js,
// so this module MUST be banked even though 009 itself is a fresh root.
//
// CERTIFICATION (2026-10-21, worker w9-s009-20261021T0230):
//   Build: recreated_pptx/build/slide_009.js -> slide_009_recreated.pptx (single
//     plain-named version, 117,542 bytes).
//   Render: 150 dpi -> qa/slide009/render_1.png (2001x1125). House-chrome check PASS.
//   Closed-loop PIL selfcheck: qa/slide009/selfcheck_attempt_3.py -> _3.txt,
//     52/52 checks OK, VERDICT PASS (attempts 1 and 2 return 40/49 and 49/52; all
//     12 of their FIX lines were diagnosed and refuted as CHECKER bugs, never build
//     bugs — the full derivation is in each file's header docstring).
//   Geometry PIL-measured from unique_slides/slide_009.jpg (960x540, exactly
//     72 px/in => 1 frame px == 1 pt == 1/72 in). Full bank: qa/slide009/
//     (probe1..probe57 + measurements_summary.txt + selfcheck_attempt_{1,2,3}.*).
//
// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide — house chrome
// (numeral 9) + the two scatter charts (each: white interior over a navy border,
// 16x16 grid, blue fitted line, 12 orange points, pale-red diagonal stroke, red
// axes with triangular arrowheads, small solid red discs, the LEFT chart's large
// solid red disc) + the two pale-cyan annotation boxes with their equation PNGs +
// the four caption lines. opts:
//   { numeral }       — override the badge numeral (a recap variant passes its own
//                       number; the badge numeral is ALWAYS the number printed on
//                       the VARIANT's own original frame)
//   { skip: {...} }   — omit any block: chrome, panels, fittedLines, points, marks,
//                       axes, eqBoxes, captions
//   { only: {...} }   — draw ONLY the listed blocks (a child composes its delta)
//
// Draw order inside BLOCKS is the certified z-order. The chart blocks are split
// per element rather than per panel: the two panels are disjoint rectangles
// (LEFT x95..465, RIGHT x486.5..869.5) and no element of either panel crosses the
// other's border, so cross-block order is geometrically irrelevant. Faithfulness
// is proven by qa/slide009/component_fidelity.py: a pptx built from THIS module
// renders pixel-identical to the certified slide_009_recreated.pptx.
//
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette ──────────────────────────────────────────────────────────
const NAVY = "000080";    // chart-panel border  (frame core 0,0,108)
const INTERIOR = "F5F5F5";// chart interior     (frame ~250,252,249)
const GRID = "D8D8D6";    // grid lines          (frame cores 207..238 over 250)
const RED = "C00000";     // axes / red marks / caption keyword (house family)
const BLUE = "0000FF";    // fitted lines        (frame core 0,0,132)
const ORANGE = "FFA500";  // data points         (frame core 255,120,0)
const BIGRED = "EE3145";  // the LEFT chart's large solid disc (frame core 238,49,69)
const BOXFILL = "EDFBFA"; // annotation box fill (frame interior median 237,251,250)
const BOXLINE = "B4BAD1"; // annotation box border (frame border cores 171..221)
const INK = "333333";     // caption remainder ink (frame core 49,51,37)
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
// h=27 (both top borders at y148; bottom border measures y174 left, y175 right).
// Equation PNG ink starts 8px (0.96pt) inside the image box; placed so the ink's
// left edge lands on the measured ink x and its ink top on y155. ix/iy/iw/ih are
// ALREADY IN INCHES (px/600 of the 600-dpi render) — never rescaled.
// Sidecars: build/assets/eq_009_{left,right}.json (for the orchestrator's OMML
// dual-representation wrap pass; the wrap is a SEPARATE pass, not done here).
const ASSETS = path.resolve(__dirname, "..", "assets");
const BOXES = [
  { x: 216.5, y: 148, w: 100, h: 26,
    img: path.join(ASSETS, "eq_009_left.png"),  ix: 3.125556, iy: 2.139444,
    iw: 1.163333, ih: 0.208333 },
  { x: 633.5, y: 148, w: 100, h: 27,
    img: path.join(ASSETS, "eq_009_right.png"), ix: 8.917222, iy: 2.139444,
    iw: 1.173333, ih: 0.208333 },
];

// ── chart panels ─────────────────────────────────────────────────────────────
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

// ── captions: 2 lines per chart, each centred on its chart (264 / 671) ───────
// Per-line boxes (no inter-line pitch to diverge on); y = baseline - fontSize
// (LO box-top -> baseline distance calibrated at 1.0 em, slide_023/035 idiom).
// Line 1 = RED bold keyword + near-black regular remainder (two text runs);
// line 2 = all near-black. 'Successes' sic — source grammar preserved.
const CAP_BASE_OFF = 1.0;
const CAPTIONS = [
  { cx: 264, base: 500, w: 380, size: 17,
    runs: [["Overfit", { bold: true, color: RED }],
           [" (try to minimize the residuals ONLY)", { color: INK }]] },
  { cx: 264, base: 519, w: 380, size: 17,
    runs: [["Fails to detect the Pattern", { color: INK }]] },
  { cx: 671, base: 500, w: 360, size: 17,
    runs: [["Generalized", { bold: true, color: RED }],
           [" (Residuals are not minimized)", { color: INK }]] },
  { cx: 671, base: 519, w: 360, size: 17,
    runs: [["Successes to detect the Pattern", { color: INK }]] },
];

function drawChrome(pptx, slide, opts) {
  const n = opts && opts.numeral !== undefined ? opts.numeral : 9;
  drawHouseChrome(pptx, slide, { numeral: n });
}

function drawPanels(pptx, slide) {
  const rect = (x, y, w, h, fill) =>
    slide.addShape(pptx.ShapeType.rect, {
      x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill },
    });
  const stroked = (x, y, w, h, color, width) =>
    slide.addShape(pptx.ShapeType.rect, {
      x: px(x), y: px(y), w: px(w), h: px(h), line: { color: color, width: width },
    });
  for (const p of PANELS) {
    // white interior (first, so the grid/axes sit on it)
    rect(p.fx, p.fy, p.fw, p.fh, INTERIOR);
    // 16 vertical + 16 horizontal 1pt grid lines inside the measured grid box
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
    // navy border on top
    stroked(p.bx, p.by, p.bw, p.bh, NAVY, 1);
  }
}

function drawFittedLines(pptx, slide) {
  // 2pt (frame per-column core span 2-3px)
  for (const p of PANELS) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(p.line.x0), y: px(p.line.y1), w: px(p.line.x1 - p.line.x0),
      h: px(p.line.y0 - p.line.y1), flipV: true,
      line: { color: BLUE, width: 2 },
    });
  }
}

function drawPoints(pptx, slide) {
  for (const p of PANELS) {
    for (const [cx, cy] of POINTS[p.name]) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(cx - 7.5 / 2), y: px(cy - 7.5 / 2), w: px(7.5), h: px(7.5),
        fill: { color: ORANGE },
      });
    }
  }
}

function drawMarks(pptx, slide) {
  // pale-red diagonal annotation strokes (2pt core, pale halo) + small solid
  // discs + the LEFT chart's large solid disc (drawn AFTER the diagonal, so the
  // disc covers the diagonal's end — as on the frame).
  for (const p of PANELS) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(p.diag.x0), y: px(p.diag.y0), w: px(p.diag.x1 - p.diag.x0),
      h: px(p.diag.y1 - p.diag.y0), line: { color: RED, width: 2 },
    });
  }
  for (const p of PANELS) {
    for (const [cx, cy, d] of DISCS[p.name]) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
        fill: { color: RED },
      });
    }
    if (p.bigDisc) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(p.bigDisc.cx - p.bigDisc.d / 2), y: px(p.bigDisc.cy - p.bigDisc.d / 2),
        w: px(p.bigDisc.d), h: px(p.bigDisc.d), fill: { color: BIGRED },
      });
    }
  }
}

function drawAxes(pptx, slide) {
  // red 1pt shafts centred on the measured axis + triangular arrowheads
  for (const p of PANELS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(p.axisX - 0.5), y: px(p.axisX0), w: px(1), h: px(p.axisX1 - p.axisX0),
      fill: { color: RED },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: px(p.axisY0), y: px(p.axisY - 0.5), w: px(p.axisY1 - p.axisY0), h: px(1),
      fill: { color: RED },
    });
    // up-head (~8x8) and right-head (~6x7, rotated 90)
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
  }
}

function drawEqBoxes(pptx, slide) {
  // pale-cyan box; equation PNG placed at exact px/600 size (never rescaled)
  for (const b of BOXES) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      fill: { color: BOXFILL }, line: { color: BOXLINE, width: 1 },
    });
    slide.addImage({ path: b.img, x: b.ix, y: b.iy, w: b.iw, h: b.ih });
  }
}

function drawCaptions(pptx, slide) {
  const R = (text, o) => Object.assign({ text: text, options: o || {} });
  for (const c of CAPTIONS) {
    const runs = c.runs.map(([t, o]) => R(t, o));
    slide.addText(runs, {
      x: px(c.cx - c.w / 2), y: px(c.base - c.size * CAP_BASE_OFF), w: px(c.w), h: px(34),
      align: "center", valign: "top", margin: 0,
      fontFace: FONT, fontSize: c.size, lineSpacing: c.size * 1.2,
    });
  }
}

const BLOCKS = {
  chrome: drawChrome,
  panels: drawPanels,
  fittedLines: drawFittedLines,
  points: drawPoints,
  marks: drawMarks,
  axes: drawAxes,
  eqBoxes: drawEqBoxes,
  captions: drawCaptions,
};

function renderBase(pptx, slide, opts = {}) {
  const skip = opts.skip || {};
  const only = opts.only || null;
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (only && !only[name]) continue;
    if (!only && skip[name]) continue;
    fn(pptx, slide, opts);
  }
}

module.exports = {
  renderBase, BLOCKS,
  PANELS, POINTS, DISCS, BOXES, CAPTIONS,
  NAVY, INTERIOR, GRID, RED, BLUE, ORANGE, BIGRED, BOXFILL, BOXLINE, INK, FONT,
  ASSETS, CAP_BASE_OFF,
};
