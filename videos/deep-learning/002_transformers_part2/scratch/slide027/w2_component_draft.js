// ============================================================================
// SLIDE 027 COMPONENT — DRAFT v2 (worker 2) — mirrors the certified build
// recreated_pptx/build/slide_027.js (worker A, attempt 2, 2026-10-12 01:55)
// shape-for-shape so a render of this component is pixel-identical to the
// certified render. DEPLOY to build/components/slide_027.js ONLY after the
// build certifies, with a 0-pixel-diff verification against the certified
// render (dependencies.md retro-bank discipline).
//
// Block granularity for the CONFIRMED DEPENDENT slide 28 (28 <- [27,26]):
// 28 = this composition grown from 5 words / 4 arcs to 9 words / 8 arcs.
// opts: {numeral, wordCount (default 5), skip: [...], titleLines: [...]}
// Blocks: circle, axis, chips, arcs (arc polyline + arrowhead + label),
// eqbox, title. Chrome drawn ONCE here (playlist law).
//
// Geometry: worker A's measured frame->slide mapping (002 capture zoom 0.958):
//   slide_x = (frame_x - 18.63) / 0.96123 ; slide_y = frame_y / 0.95556
// All values below are in SLIDE POINTS (1 pt = 1/72 in), from
// scratch/slide027/measure2.json + probe3/4/5 (worker A) and my
// measure_frame*.py cross-checks.
// ============================================================================

const PATH_SHARED = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js";
const { drawHouseChrome } = require(PATH_SHARED);

const M = {
  colors: {
    title: "C00000",
    eqBlue: "0000CC", eqRed: "CC0000", eqGreen: "009900",
    circleFill: "FBFCC9", circleRing: "C0C3B7",
    boxFill: "FFFFCC", boxBorder: "BEC3C3",
    chipFill: "CCFFCC", chipGreen: "009933",
    arc: "E06010", label: "CC0000", axis: "6E6E6E",
  },
  fonts: { title: "Arial", eq: "Arial", chip: "Arial" },
  // circle: center slide-pt (581.0, 297.2), r 130.75
  circle: { cx: 581.0, cy: 297.2, r: 130.75 },
  // faint axis cross (solid gray 60% transparency, 0.75pt)
  axis: { hx: [246.9, 905.4], hy: 296.7, vx: 581.0, vy: [50.2, 532.8] },
  // word chips: 71x24 pt, centered ON rim R=182.5 at k*30 deg; first five
  // EXACTLY as measured/certified; extras follow the polar rule.
  chipR: 182.5, chipW: 71 / 72, chipH: 24 / 72, chipFontPt: 12,
  chipCentersMeasured: [ // slide-pt centers, k = 0..4
    [762.6, 297.2], [738.4, 204.6], [672.3, 138.6], [581.1, 113.3], [490.4, 139.9],
  ],
  // arcs: 14-segment polylines at R=224 around the circle center, sweeping
  // (k*30 + 12) deg -> (k*30 + 28.5) deg (CCW); certified for k = 0..3.
  arcR: 224, arcSegs: 14, arcFromPad: 12, arcToPadDeg: 1.5, arcWidthPt: 1.25,
  // arrowheads: ~9.5pt triangles aimed into the destination chip; first four
  // EXACTLY as certified; extras follow the polar rule (r 224 on dest spoke).
  headR: 224, headSizePt: 9.5,
  headsMeasured: [ // [head center, chip center] slide-pt, k = 0..3
    [[776.4, 188.4], [738.4, 204.6]],
    [[692.6, 100.5], [672.3, 138.6]],
    [[585.6, 71.2], [581.1, 113.3]],
    [[473.3, 101.5], [490.4, 139.9]],
  ],
  // '+w' labels: Arial Bold 15pt CC0000, 30x16pt box centered at:
  labelsMeasured: [ // slide-pt centers, k = 0..3
    [840.2, 236.5], [788.8, 104.1], [642.8, 75.4], [520.6, 75.4],
  ],
  labelBoxW: 30 / 72, labelBoxH: 16 / 72, labelFontPt: 15,
  labelAutoR: 236, // slide-pt radius for labels k >= 4 (arc mid, outside arc)
  // equation box + text (per-glyph certified runs)
  eq: { x: 65.9, y: 190.5, w: 139.5, h: 66.9, textX: 70, textY: 194, textW: 132, textH: 60, fontPt: 20, lineSpacingPt: 21 },
  // title: three single-line boxes, Arial Bold 24.3pt, y = ink_top - lead
  title: {
    lines: ["Sequence of 5 words", "Positions are defined", "as angles"],
    boxes: [ // [x, y, w] slide-pt (h = 36)
      [55.0, 56.40, 320], [53.9, 82.70, 320], [120.5, 110.76, 160],
    ],
    fontPt: 24.3, h: 36 / 72,
  },
};

const RAD = Math.PI / 180;

function chipCenter(k) {
  if (k < M.chipCentersMeasured.length) {
    return { x: M.chipCentersMeasured[k][0], y: M.chipCentersMeasured[k][1] };
  }
  const a = (k * 30) * RAD;
  return { x: M.circle.cx + M.chipR * Math.cos(a), y: M.circle.cy - M.chipR * Math.sin(a) };
}

// ---- blocks ----

function drawCircle(pptx, slide) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: (M.circle.cx - M.circle.r) / 72, y: (M.circle.cy - M.circle.r) / 72,
    w: (2 * M.circle.r) / 72, h: (2 * M.circle.r) / 72,
    fill: { color: M.colors.circleFill }, line: { color: M.colors.circleRing, width: 1 },
  });
}

function drawAxis(pptx, slide) {
  slide.addShape(pptx.ShapeType.line, {
    x: M.axis.hx[0] / 72, y: M.axis.hy / 72, w: (M.axis.hx[1] - M.axis.hx[0]) / 72, h: 0,
    line: { color: M.colors.axis, width: 0.75, transparency: 60 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: M.axis.vx / 72, y: M.axis.vy[0] / 72, w: 0, h: (M.axis.vy[1] - M.axis.vy[0]) / 72,
    line: { color: M.colors.axis, width: 0.75, transparency: 60 },
  });
}

function drawWordChip(pptx, slide, k, label) {
  const c = chipCenter(k);
  const rotDeg = (k * 30) % 360;
  const rot = rotDeg === 0 ? 0 : -rotDeg; // pptxgenjs cw-positive; chips read CCW-tilted
  slide.addText(label, {
    shape: pptx.ShapeType.rect,
    x: (c.x - 35.5) / 72, y: (c.y - 12) / 72, w: M.chipW, h: M.chipH,
    rotate: rot, fill: { color: M.colors.chipFill }, line: { color: M.colors.chipGreen, width: 0.75 },
    align: "center", valign: "middle", fontFace: M.fonts.chip, fontSize: M.chipFontPt,
    bold: true, italic: true, color: M.colors.chipGreen, margin: 0,
  });
}

function drawArcUnit(pptx, slide, k) {
  // 14-segment arc polyline (certified method)
  const a0 = k * 30 + M.arcFromPad, a1 = (k + 1) * 30 - M.arcToPadDeg;
  const pt = (deg) => {
    const a = deg * RAD;
    return [M.circle.cx + M.arcR * Math.cos(a), M.circle.cy - M.arcR * Math.sin(a)];
  };
  for (let i = 0; i < M.arcSegs; i++) {
    const p1 = pt(a0 + ((a1 - a0) * i) / M.arcSegs);
    const p2 = pt(a0 + ((a1 - a0) * (i + 1)) / M.arcSegs);
    slide.addShape(pptx.ShapeType.line, {
      x: Math.min(p1[0], p2[0]) / 72, y: Math.min(p1[1], p2[1]) / 72,
      w: Math.abs(p2[0] - p1[0]) / 72, h: Math.abs(p2[1] - p1[1]) / 72,
      flipH: p2[0] < p1[0], flipV: p2[1] < p1[1],
      line: { color: M.colors.arc, width: M.arcWidthPt },
    });
  }
  // arrowhead aimed into the destination chip
  let head, chipC;
  if (k < M.headsMeasured.length) {
    head = { x: M.headsMeasured[k][0][0], y: M.headsMeasured[k][0][1] };
    chipC = { x: M.headsMeasured[k][1][0], y: M.headsMeasured[k][1][1] };
  } else {
    const a = ((k + 1) * 30) * RAD;
    head = { x: M.circle.cx + M.headR * Math.cos(a), y: M.circle.cy - M.headR * Math.sin(a) };
    chipC = chipCenter(k + 1);
  }
  const vx = chipC.x - head.x, vy = chipC.y - head.y;
  const rot = (Math.atan2(vx, -vy) * 180) / Math.PI;
  slide.addShape(pptx.ShapeType.triangle, {
    x: (head.x - M.headSizePt / 2) / 72, y: (head.y - M.headSizePt / 2) / 72,
    w: M.headSizePt / 72, h: M.headSizePt / 72,
    rotate: rot, fill: { color: M.colors.arc }, line: { color: M.colors.arc, width: 0.5 },
  });
  // '+w' label
  let lp;
  if (k < M.labelsMeasured.length) {
    lp = { x: M.labelsMeasured[k][0], y: M.labelsMeasured[k][1] };
  } else {
    const mid = ((k * 30 + 12) + ((k + 1) * 30 - M.arcToPadDeg)) / 2 * RAD;
    lp = { x: M.circle.cx + M.labelAutoR * Math.cos(mid), y: M.circle.cy - M.labelAutoR * Math.sin(mid) };
  }
  slide.addText("+\u03C9", {
    x: (lp.x - 15) / 72, y: (lp.y - 8) / 72, w: M.labelBoxW, h: M.labelBoxH,
    align: "center", valign: "middle", fontFace: "Arial", fontSize: M.labelFontPt,
    bold: true, color: M.colors.label, margin: 0,
  });
}

function drawEquationBox(pptx, slide) {
  const e = M.eq;
  slide.addShape(pptx.ShapeType.rect, {
    x: e.x / 72, y: e.y / 72, w: e.w / 72, h: e.h / 72,
    fill: { color: M.colors.boxFill }, line: { color: M.colors.boxBorder, width: 0.75 },
  });
  slide.addText([
    { text: "Sin(", options: { color: M.colors.eqBlue } },
    { text: "\u03C9", options: { color: M.colors.eqRed } },
    { text: " t", options: { color: M.colors.eqGreen } },
    { text: ")", options: { color: M.colors.eqBlue, breakLine: true } },
    { text: "Cos(", options: { color: M.colors.eqBlue } },
    { text: "\u03C9", options: { color: M.colors.eqRed } },
    { text: " t", options: { color: M.colors.eqGreen } },
    { text: ")", options: { color: M.colors.eqBlue, breakLine: true } },
    { text: "t=0,1,2,3,....", options: { color: M.colors.eqGreen } },
  ], {
    x: e.textX / 72, y: e.textY / 72, w: e.textW / 72, h: e.textH / 72,
    align: "left", valign: "top", fontFace: M.fonts.eq, fontSize: e.fontPt, bold: true,
    lineSpacing: e.lineSpacingPt, margin: 0,
  });
}

function drawTitle(pptx, slide, lines) {
  for (let i = 0; i < lines.length && i < 3; i++) {
    const b = M.title.boxes[i];
    slide.addText(lines[i], {
      x: b[0] / 72, y: b[1] / 72, w: b[2] / 72, h: M.title.h,
      align: "left", valign: "top", fontFace: M.fonts.title, fontSize: M.title.fontPt,
      bold: true, color: M.colors.title, margin: 0,
    });
  }
}

// Full composition. opts.skip: ['circle','axis','chips','arcs','eqbox','title'].
// opts.wordCount: 5 (this slide) / 9 (slide 28). opts.titleLines overrides text.
function renderBase(pptx, slide, opts = {}) {
  const wc = opts.wordCount === undefined ? 5 : opts.wordCount;
  const skip = new Set(opts.skip || []);
  drawHouseChrome(pptx, slide, { numeral: opts.numeral });
  if (!skip.has("circle")) drawCircle(pptx, slide);
  if (!skip.has("axis")) drawAxis(pptx, slide);
  if (!skip.has("arcs")) for (let k = 0; k + 1 < wc; k++) drawArcUnit(pptx, slide, k);
  if (!skip.has("chips")) for (let k = 0; k < wc; k++) drawWordChip(pptx, slide, k, "Word " + k);
  if (!skip.has("eqbox")) drawEquationBox(pptx, slide);
  if (!skip.has("title")) drawTitle(pptx, slide, opts.titleLines || M.title.lines);
}

module.exports = { M, drawCircle, drawAxis, drawWordChip, drawArcUnit, drawEquationBox, drawTitle, renderBase };
