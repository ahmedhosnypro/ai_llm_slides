// components/slide_009.js — BANKED composition of slide 009
// ("Overfit vs. Generalized" — metadata-only title; NO title ink on the frame),
// ML lecture 03 (03_ridger_regression_gradient_descent).
//
// REFRESHED 2026-10-24 (worker w009-judge-20261024): re-sourced from the
// CERTIFIED build/slide_009.js after the attempt-2 adjudication pass, so this
// module and slide_009_recreated.pptx are one artifact again (cascade law:
// the previous banking, 2026-10-21, described the pre-attempt-2 build).
//
// CERTIFICATION (2026-10-24, w009-judge-20261024):
//   Build: recreated_pptx/build/slide_009.js -> slide_009_recreated.pptx (single
//     plain-named version).
//   Render: 150 dpi -> qa/slide009/render_3.png (2001x1125). House-chrome check
//     PASS (shared_patterns/house_chrome_check.py).
//   Visual gate: BOTH legs from render_3 — full-slide judge judge_attempt_3.txt
//     + six zoomed crop certificates crop_3_<name>_judge.txt (Procedure B,
//     matched effective scale, cut_crops_3.py VERDICT PASS).
//   PIL adjudication of every raised finding: qa/slide009/adjudication_attempt_2.txt
//     (attempt 1) and adjudication_attempt_2b.txt / adjudication_attempt_3.txt
//     (attempts 2-3); full record in qa/slide009/worker_report.md.
//
// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide — house chrome
// (numeral 9) + the two scatter charts (each: white interior over a navy border,
// 16x16 grid, blue fitted line, 12 orange points, pale-red diagonal stroke, red
// axes with triangular arrowheads, the red residual marks — diamond + arrow —
// and the LEFT chart's large solid red disc) + the two pale-cyan annotation
// boxes with their equation PNGs + the two caption-band boxes (cream fill,
// rose open-top outline) + the four caption lines. opts:
//   { numeral }       — override the badge numeral (a recap variant passes its own
//                       number; the badge numeral is ALWAYS the number printed on
//                       the VARIANT's own original frame)
//   { skip: {...} }   — omit any block: chrome, panels, fittedLines, points,
//                       marks, axes, eqBoxes, capBoxes, captions
//   { only: {...} }   — draw ONLY the listed blocks (a child composes its delta)
//
// Draw order inside BLOCKS is the certified z-order. The chart blocks are split
// per element rather than per panel: the two panels are disjoint rectangles
// (LEFT x95..465, RIGHT x486.5..869.5) and no element of either panel crosses
// the other's border, so cross-block z-order is geometrically irrelevant.
// bandMarks sits LAST: the rose underlines overlay the caption text exactly as
// the hand annotation does on the frame.
//
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette ──────────────────────────────────────────────────────────
const NAVY     = "000080";   // chart-panel border  (frame core 0,0,108)
const INTERIOR = "F5F5F5";   // chart interior      (frame ~248,248,248)
const GRID     = "D8D8D6";   // grid lines          (frame cores 207..238 over 250)
const RED      = "C00000";   // axes / red marks / caption keyword (house family)
const BLUE     = "0000FF";   // fitted lines        (frame core 0,0,132)
const ORANGE   = "FFA500";   // data points         (frame core 255,120,0)
const BIGRED   = "EE3145";   // the LEFT chart's large solid disc (frame core 238,49,69)
const BOXFILL  = "ECFDF9";   // annotation box fill (frame median 236,253,249)
const BOXLINE  = "000080";   // annotation box border = navy (same as panel border)
const INK      = "333333";   // caption remainder ink (frame core 49,51,37)
const FONT     = "Times New Roman"; // serif, matches the frame (Liberation Serif metrics)

// caption-band box palette (PIL-measured 2026-10-24, frame cores)
const CAPFILL = "FBFCEC"; // caption-box fill (frame median 251,252,236)
const BAND_STROKES = [
  { x: 95.5,  y: 479, w: 2, h: 49, c: "E2C6C3" },   // LEFT left vertical  (226,198,195)
  { x: 432.5, y: 479, w: 2, h: 49, c: "F0E6E7" },   // LEFT right vertical (240,230,231)
  { x: 96,    y: 527.5, w: 337, h: 2, c: "DCBBBB" }, // LEFT bottom rule  (220,187,187)
  { x: 502,   y: 479, w: 2, h: 49, c: "D3BCB9" },   // RIGHT left vertical (211,188,185)
  { x: 839.5, y: 479, w: 2, h: 49, c: "CAA5A6" },   // RIGHT right vertical (202,165,166)
  { x: 503,   y: 527.5, w: 337, h: 2, c: "D9BBBA" }, // RIGHT bottom rule  (217,187,186)
];
const BAND_FILLS = [
  { x: 97,  y: 480, w: 335, h: 47 },
  { x: 504, y: 480, w: 335, h: 47 },
];

// ── equation PNG assets (600-dpi matplotlib mathtext, deck math law) ──────────
const ASSETS = path.resolve(__dirname, "..", "assets");

// ── chart panels ─────────────────────────────────────────────────────────────
// border lines are centred on the rect edge (1pt == 1 frame px)
// Panel measurements from probe40/probe41 (banked with build/slide_009.js):
const PANELS = [
  { name: "LEFT",
    bx: 95,   by: 107, bw: 371, bh: 367,   // navy border rect
    fx: 98,   fy: 111, fw: 365, fh: 359,   // white interior
    col0: 103.5, colPitch: 23, nCol: 16,   // vertical grid lines
    row0: 120.5, rowPitch: 22.4, nRow: 16, // horizontal grid lines
    axisX: 126.5, axisX0: 152, axisX1: 437, // y-axis (vertical)
    axisY: 434,   axisY0: 124, axisY1: 428, // x-axis (horizontal)
    headUp:   { cx: 126.5, tipY: 143, baseY: 151, halfW: 4.0 },
    headRight:{ cy: 434,   tipX: 435, baseX: 428, halfH: 3.5 },
    line: { x0: 141, y0: 351, x1: 433, y1: 201 }, // blue fitted line
    diag: { x0: 199, y0: 198, x1: 232, y1: 241 }, // pale-red annotation stroke
    bigDisc: { cx: 232.5, cy: 241, d: 24.5 },     // LEFT chart only
    // genuine red residual marks (diamond + diagonal arrow)
    redMarks: [
      { type: "diamond", cx: 187,   cy: 155,   d: 9 },
      { type: "arrow",   x0: 204, y0: 199, x1: 218, y1: 233, headW: 34 },
    ],
    points: [
      [197.5, 145.0], [188.5, 355.5], [176.5, 380.5], [242.5, 327.5], [260.5, 333.5],
      [294.0, 333.5], [324.0, 290.0], [328.5, 332.0], [381.5, 301.5], [397.5, 249.0],
      [421.5, 255.0], [233.5, 362.0],
    ] },
  { name: "RIGHT",
    bx: 486.5, by: 107, bw: 385, bh: 367,
    fx: 489.5, fy: 111, fw: 378, fh: 359,
    col0: 517.5, colPitch: 23, nCol: 16,
    row0: 120.5, rowPitch: 22.4, nRow: 16,
    axisX: 540,   axisX0: 152, axisX1: 437,
    axisY: 434,   axisY0: 538, axisY1: 841,
    headUp:   { cx: 540,   tipY: 143, baseY: 151, halfW: 3.5 },
    headRight:{ cy: 434,   tipX: 848, baseX: 841, halfH: 3.5 },
    line: { x0: 555, y0: 387, x1: 849, y1: 247 },
    diag: { x0: 626, y0: 208, x1: 646, y1: 264 },
    bigDisc: null,
    redMarks: [
      { type: "diamond", cx: 602.5, cy: 149.5, d: 8 },
      { type: "arrow",   x0: 627, y0: 212, x1: 636, y1: 232, headW: 19 },
    ],
    points: [
      [611.0, 145.0], [601.5, 355.5], [589.5, 380.5], [656.0, 327.0], [674.0, 333.5],
      [707.5, 333.5], [737.5, 290.0], [741.5, 332.0], [794.0, 302.0], [810.0, 249.0],
      [834.5, 255.0], [647.0, 362.0],
    ] },
];

// ── annotation boxes + equation images ───────────────────────────────────────
// Box: navy 1pt border centred on the rect edge, pale-cyan fill.
// LEFT  box x216..317 y148..175 (w102 h27)
// RIGHT box x631..734 y148..175 (w104 h27)
// Equation PNG placed at EXACTLY the 600-dpi px/600 size (never rescaled — deck
// math law); ix/iy/iw/ih are ALREADY IN INCHES, solved so the PNG's ~8px ink
// inset lands its left edge on the frame's measured ink x and its top on y155.
// Sidecars: build/assets/eq_009_{left,right}.json (for the orchestrator's OMML
// dual-representation wrap pass; the wrap is a SEPARATE pass, not done here).
const BOXES = [
  { x: 216, y: 148, w: 102, h: 27,
    img: path.join(ASSETS, "eq_009_left.png"),
    ix: 3.027778, iy: 2.041667, iw: 1.426667, ih: 0.218333 },
  { x: 631, y: 148, w: 104, h: 27,
    img: path.join(ASSETS, "eq_009_right.png"),
    ix: 8.819444, iy: 2.041667, iw: 1.433333, ih: 0.218333 },
];

// ── captions: 2 lines per chart, each centred on its chart (264 / 671) ───────
// Per-line boxes; y = baseline - fontSize (LO box-top -> baseline ~1.0 em).
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

// ── caption-band annotation boxes (frame px, 1px=1pt) ────────────────────────
// PIL-measured on the frame 2026-10-24: each caption sits inside a CREAM-FILLED,
// rose-outlined box that is OPEN AT THE TOP — left + right verticals plus a
// bottom rule, no top stroke:
//   LEFT  box x95..434 y479..529 ; RIGHT box x501..842 y479..529
// Fill medians 251,252,236 (cream) both sides; stroke cores per side (the
// frame's JPEG halos widen each stroke ~1-2px around the cores above).

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
  // 2pt (frame per-column core span 2-3px); flipV for the upward lines
  for (const p of PANELS) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(p.line.x0), y: px(p.line.y1), w: px(p.line.x1 - p.line.x0),
      h: px(p.line.y0 - p.line.y1), flipV: true,
      line: { color: BLUE, width: 2 },
    });
  }
}

function drawPoints(pptx, slide) {
  // 12 orange data points per chart, d=7.5 (measured blob widths 6..8)
  for (const p of PANELS) {
    for (const [cx, cy] of p.points) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(cx - 7.5 / 2), y: px(cy - 7.5 / 2), w: px(7.5), h: px(7.5),
        fill: { color: ORANGE },
      });
    }
  }
}

function drawMarks(pptx, slide) {
  // pale-red diagonal annotation strokes (2pt core, pale halo) + the genuine red
  // residual marks (diamond + diagonal arrow) + the LEFT chart's large solid
  // disc (drawn AFTER the diagonal, so the disc covers the diagonal's end — as
  // on the frame).
  for (const p of PANELS) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(p.diag.x0), y: px(p.diag.y0), w: px(p.diag.x1 - p.diag.x0),
      h: px(p.diag.y1 - p.diag.y0), line: { color: RED, width: 2 },
    });
  }
  for (const p of PANELS) {
    for (const m of p.redMarks) {
      if (m.type === "diamond") {
        // Diamond = rotated square
        slide.addShape(pptx.ShapeType.rect, {
          x: px(m.cx - m.d / 2), y: px(m.cy - m.d / 2),
          w: px(m.d), h: px(m.d), rotate: 45, fill: { color: RED },
        });
      } else if (m.type === "arrow") {
        // Arrow shaft
        slide.addShape(pptx.ShapeType.line, {
          x: px(m.x0), y: px(m.y0), w: px(m.x1 - m.x0), h: px(m.y1 - m.y0),
          line: { color: RED, width: 3 },
        });
        // Arrowhead — triangle at the tip (pointing towards the data point)
        const dx = m.x1 - m.x0, dy = m.y1 - m.y0;
        const len = Math.hypot(dx, dy);
        const ux = dx / len, uy = dy / len;
        const hx = m.x1 - ux * 8, hy = m.y1 - uy * 8; // 8pt back from tip
        const perpX = -uy, perpY = ux;
        const hw = m.headW / 2;
        slide.addShape(pptx.ShapeType.triangle, {
          x: px(hx + perpX * hw), y: px(hy + perpY * hw),
          w: px(hw * 2), h: px(8), // approximate
          rotate: Math.atan2(dy, dx) * 180 / Math.PI - 90,
          fill: { color: RED },
        });
      }
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
  // pale-cyan box (navy 1pt border) + equation PNG at exact px/600 size
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

function drawBandMarks(pptx, slide) { // block name: capBoxes
  // cream fill first, then the rose outline (fills under the caption ink)
  for (const f of BAND_FILLS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(f.x), y: px(f.y), w: px(f.w), h: px(f.h), fill: { color: CAPFILL },
    });
  }
  for (const m of BAND_STROKES) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(m.x), y: px(m.y), w: px(m.w), h: px(m.h), fill: { color: m.c },
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
  capBoxes: drawBandMarks,
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
  PANELS, BOXES, CAPTIONS, BAND_FILLS, BAND_STROKES,
  NAVY, INTERIOR, GRID, RED, BLUE, ORANGE, BIGRED, BOXFILL, BOXLINE, INK, FONT,
  CAPFILL, ASSETS, CAP_BASE_OFF,
};
