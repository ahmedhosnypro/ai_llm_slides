// Slide 027 component — "Sequence of 5 words / Positions are defined as angles"
// (Deep Learning DSAI 308, 002_transformers_part2) — CERTIFIED component banked per
// the dependency law (.agents/skills/slide-recreation/references/dependencies.md).
//
// CERTIFICATION: slide 027 passed the visual judge on 2026-10-12
// (qa/slide027/judge_attempt_2.txt, FINAL VERDICT: PASS; single-read, default
// route/images). This component IS the certified composition (build/slide_027.js,
// render_6.png) re-expressed as importable blocks. It SUPERSEDES the earlier
// uncertified orphan component (archived at
// qa/slide027/component_previous_worker_uncertified_v1.js), which mapped frame
// pixels 1:1 to slide points and ignored video 002's 0.958 zoom-out capture
// mapping (see build/slide_002.js header): every coordinate here is in TRUE slide
// points (frame_x = 18.63 + 0.96123*slide_x ; frame_y = 0.95556*slide_y).
//
// CONFIRMED DEPENDENTS: slide 28 (28 ← [27, 26]) = this composition grown from
// 5 words / 4 arcs to 9 words / 8 arcs; 29 ← 28; 45 ← 28. Block granularity is
// mandatory: every visual block is its own function; renderBase(pptx, slide, opts)
// composes them and accepts opts.skip / opts.wordCount so children grow the
// composition without re-deriving geometry. NEVER copy-paste this file into a
// child build — require() it by absolute path. House chrome is drawn HERE via
// shared_patterns/house_chrome.js; children must NOT re-draw it (they pass their
// own opts.numeral).
//
// CIRCLE/ARC/WORD-LANE CONVENTIONS (for slides 28/29/45 — keep identical):
//   * Center C = (581.0, 297.2) pt. Fill r = 130.75 pt (FBFCC9, ring C0C3B7 1pt).
//   * Word k sits CENTERED ON the rim at radius R_CHIP = 182.5 pt, angle k*30 deg
//     CCW from 3 o'clock. Chip 71 x 24 pt, fill CCFFCC, border 009933 0.75pt,
//     "Word k" Arial bold italic 12pt 009933. Rotation (pptxgenjs CW deg):
//     rot = -angle normalized to (-90, +90] (0°:0, 30°:-30, 60°:-60, 90°:-90
//     [reads bottom-to-top], 120°:+60 [reads top-to-bottom], 150°:+30, ...).
//   * Arc k (Word k -> Word k+1): circle-centered polyline at R_ARC = 224 pt from
//     (k*30 + 12) deg to ((k+1)*30 - 1.5) deg, 14 segments, stroke F0C9B0 0.75pt
//     SOLID (the original's stroke is below the JPEG noise floor; vision reads
//     converge on a thin pale-salmon delicate curve — do NOT thicken or dash it).
//   * Arrowhead of arc k: UNROTATED down-pointing triangle (all four original
//     heads point screen-DOWN regardless of spoke angle — PIL row profiles), 
//     10 x 11 pt, fill/line E06010, centered at polar((k+1)*30, 224.5).
//   * '+ω' labels (Arial bold 15pt CC0000, 30x16pt centered box): arcs 0..3 use
//     the four MEASURED positions below (hand-placed by the professor — no polar
//     law); extra arcs (slides 28+) use polar(midAngle, 255) as the auto rule.
//   * Spokes: 12 rays at 30 deg steps. The 0/90/180/270 cross runs through the
//     fill: horizontal y=296.7 x 246.9..905.4, vertical x=581.0 y 50.2..532.8,
//     dashType lgDash; the 8 diagonals run r 30..240, dashType sysDot; all
//     993333 @ 75% transparency, 0.75pt (faded pinkish-red appearance, PIL- and
//     judge-verified). Spokes cross the circle interior; chips/arcs/heads/labels
//     draw OVER them.

const PATH_SHARED = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js";
const { drawHouseChrome } = require(PATH_SHARED);

const PX = 1 / 72; // slide pt -> inches

const M = {
  colors: {
    circleFill: "FBFCC9", circleRing: "C0C3B7",
    axis: "993333", axisTransparency: 75,
    chipFill: "CCFFCC", chipLine: "009933", chipText: "009933",
    arcStroke: "F0C9B0", arrowhead: "E06010",
    label: "CC0000", title: "C00000",
    eqFill: "FFFFCC", eqBorder: "BEC3C3",
    eqBlue: "0000CC", eqRed: "CC0000", eqGreen: "009900",
  },
  circle: { cx: 581.0, cy: 297.2, r: 130.75 },
  axis: { hx0: 246.9, hx1: 905.4, hy: 296.7, vy0: 50.2, vy1: 532.8, vx: 581.0 },
  spokeR: { inner: 30, outer: 240 },
  chipR: 182.5, chipW: 71, chipH: 24, chipFontPt: 12,
  // CERTIFIED chip centers (PIL-measured, build/slide_027.js): k = 0..4 use these
  // EXACT values (pixel-diff verified vs render_6.png); k >= 5 (slide 28) uses the
  // polar rule chipR @ k*30 deg.
  chipsMeasured: [
    [762.6, 297.2], [738.4, 204.6], [672.3, 138.6], [581.1, 113.3], [490.4, 139.9],
  ],
  arcR: 224, arcStartPadDeg: 12, arcEndPadDeg: 1.5, arcSegs: 14,
  ahR: 224.5, ahW: 10, ahH: 11,
  // CERTIFIED arrowhead centers (PIL-measured, build/slide_027.js): k = 0..3 use
  // these EXACT values (pixel-diff verified); k >= 4 (slide 28) uses the polar
  // rule polar((k+1)*30, ahR).
  headsMeasured: [[776.4, 188.4], [692.6, 100.5], [585.6, 71.2], [473.3, 101.5]],
  // '+ω' label centers (slide pt), k = arc index (Word k -> Word k+1)
  labelsMeasured: [[840.2, 236.5], [788.8, 104.1], [642.8, 75.4], [520.6, 75.4]],
  labelAutoR: 255, labelFontPt: 15, labelBoxW: 30, labelBoxH: 16,
  title: {
    lines: ["Sequence of 5 words", "Positions are defined", "as angles"],
    // [x, y(box top)] slide pt — closed-loop-fitted (render ink == measured ink)
    boxes: [[55.0, 56.40], [53.9, 82.70], [120.5, 110.76]],
    w: [320, 320, 160], h: 36, fontPt: 24.3,
  },
  eq: { x: 65.9, y: 190.5, w: 139.5, h: 66.9, textX: 70, textY: 194, textW: 132, textH: 60,
        fontPt: 20, lineSpacingPt: 21 },
};

const RAD = Math.PI / 180;
function polar(deg, r) {
  return { x: M.circle.cx + r * Math.cos(deg * RAD), y: M.circle.cy - r * Math.sin(deg * RAD) };
}

// ------- blocks -------

function drawTitle(pptx, slide, opts = {}) {
  const lines = opts.titleLines || M.title.lines;
  for (let i = 0; i < lines.length && i < 3; i++) {
    const [tx, ty] = M.title.boxes[i];
    slide.addText(lines[i], {
      x: tx * PX, y: ty * PX, w: M.title.w[i] * PX, h: M.title.h * PX,
      fontFace: "Arial", fontSize: M.title.fontPt, bold: true, color: M.colors.title,
      align: "left", valign: "top", margin: 0,
    });
  }
}

function drawEquationBox(pptx, slide) {
  const e = M.eq;
  slide.addShape(pptx.ShapeType.rect, {
    x: e.x * PX, y: e.y * PX, w: e.w * PX, h: e.h * PX,
    fill: { color: M.colors.eqFill }, line: { color: M.colors.eqBorder, width: 0.75 },
  });
  // Per-glyph color runs PIL-verified from the frame: "Sin(" blue, "ω" red,
  // " t" GREEN, ")" blue; line 3 all green. Linear text matches the original
  // (no stacked constructs -> professional format == this text).
  slide.addText([
    { text: "Sin(", options: { color: M.colors.eqBlue } },
    { text: "ω", options: { color: M.colors.eqRed } },
    { text: " t", options: { color: M.colors.eqGreen } },
    { text: ")", options: { color: M.colors.eqBlue, breakLine: true } },
    { text: "Cos(", options: { color: M.colors.eqBlue } },
    { text: "ω", options: { color: M.colors.eqRed } },
    { text: " t", options: { color: M.colors.eqGreen } },
    { text: ")", options: { color: M.colors.eqBlue, breakLine: true } },
    { text: "t=0,1,2,3,....", options: { color: M.colors.eqGreen } },
  ], {
    x: e.textX * PX, y: e.textY * PX, w: e.textW * PX, h: e.textH * PX,
    fontFace: "Arial", fontSize: e.fontPt, bold: true, align: "left", valign: "top",
    margin: 0, lineSpacing: e.lineSpacingPt,
  });
}

function drawCircle(pptx, slide) {
  const c = M.circle;
  slide.addShape(pptx.ShapeType.ellipse, {
    x: (c.cx - c.r) * PX, y: (c.cy - c.r) * PX, w: 2 * c.r * PX, h: 2 * c.r * PX,
    fill: { color: M.colors.circleFill }, line: { color: M.colors.circleRing, width: 1 },
  });
}

function drawSpokes(pptx, slide) {
  // dashed axis cross through the fill
  slide.addShape(pptx.ShapeType.line, {
    x: M.axis.hx0 * PX, y: M.axis.hy * PX, w: (M.axis.hx1 - M.axis.hx0) * PX, h: 0,
    line: { color: M.colors.axis, width: 0.75, transparency: M.colors.axisTransparency, dashType: "lgDash" },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: M.axis.vx * PX, y: M.axis.vy0 * PX, w: 0, h: (M.axis.vy1 - M.axis.vy0) * PX,
    line: { color: M.colors.axis, width: 0.75, transparency: M.colors.axisTransparency, dashType: "lgDash" },
  });
  // 8 diagonal dotted spokes (0/90/180/270 are the cross above)
  for (const deg of [30, 60, 120, 150, 210, 240, 300, 330]) {
    const p1 = polar(deg, M.spokeR.inner), p2 = polar(deg, M.spokeR.outer);
    slide.addShape(pptx.ShapeType.line, {
      x: Math.min(p1.x, p2.x) * PX, y: Math.min(p1.y, p2.y) * PX,
      w: Math.abs(p2.x - p1.x) * PX, h: Math.abs(p2.y - p1.y) * PX,
      flipH: p2.x < p1.x, flipV: p2.y < p1.y,
      line: { color: M.colors.axis, width: 0.75, transparency: M.colors.axisTransparency, dashType: "sysDot" },
    });
  }
}

// One word chip centered on the deg-degree spoke. k = deg/30: certified k ranges
// use the MEASURED centers; extras (slide 28) use the polar rule at M.chipR.
function drawWordChip(pptx, slide, o) {
  const k = Math.round(o.angleDeg / 30);
  const c = k < M.chipsMeasured.length
    ? { x: M.chipsMeasured[k][0], y: M.chipsMeasured[k][1] }
    : polar(o.angleDeg, M.chipR);
  let rot = -o.angleDeg;
  while (rot < -90) rot += 180; // 90 keeps -90 (reads bottom-to-top); 120 -> +60
  slide.addText(o.label, {
    shape: pptx.ShapeType.rect,
    x: (c.x - M.chipW / 2) * PX, y: (c.y - M.chipH / 2) * PX,
    w: M.chipW * PX, h: M.chipH * PX, rotate: rot,
    fill: { color: M.colors.chipFill }, line: { color: M.colors.chipLine, width: 0.75 },
    fontFace: "Arial", fontSize: M.chipFontPt, bold: true, italic: true,
    color: M.colors.chipText, align: "center", valign: "middle", margin: 0,
  });
}

// One curved +ω arrow from angle a to angle b (CCW deg): pale thin arc polyline +
// unrotated down-triangle arrowhead on the destination spoke + '+ω' label
// (arcs 0..3 measured label positions; extras auto at polar(mid, 255)).
function drawArc(pptx, slide, o) {
  const k = Math.round(o.fromDeg / 30);
  const a0 = o.fromDeg + M.arcStartPadDeg, a1 = o.toDeg - M.arcEndPadDeg;
  const N = M.arcSegs;
  for (let i = 0; i < N; i++) {
    const t0 = a0 + ((a1 - a0) * i) / N, t1 = a0 + ((a1 - a0) * (i + 1)) / N;
    const p1 = polar(t0, M.arcR), p2 = polar(t1, M.arcR);
    slide.addShape(pptx.ShapeType.line, {
      x: Math.min(p1.x, p2.x) * PX, y: Math.min(p1.y, p2.y) * PX,
      w: Math.abs(p2.x - p1.x) * PX, h: Math.abs(p2.y - p1.y) * PX,
      flipH: p2.x < p1.x, flipV: p2.y < p1.y,
      line: { color: M.colors.arcStroke, width: 0.75 },
    });
  }
  const ah = k < M.headsMeasured.length
    ? { x: M.headsMeasured[k][0], y: M.headsMeasured[k][1] }
    : polar(o.toDeg, M.ahR);
  slide.addShape(pptx.ShapeType.triangle, {
    x: (ah.x - M.ahW / 2) * PX, y: (ah.y - M.ahH / 2) * PX,
    w: M.ahW * PX, h: M.ahH * PX, flipV: true,
    fill: { color: M.colors.arrowhead }, line: { color: M.colors.arrowhead, width: 0.5 },
  });
  const lp = k < M.labelsMeasured.length
    ? { x: M.labelsMeasured[k][0], y: M.labelsMeasured[k][1] }
    : polar((o.fromDeg + o.toDeg) / 2, M.labelAutoR);
  slide.addText("+ω", {
    x: (lp.x - M.labelBoxW / 2) * PX, y: (lp.y - M.labelBoxH / 2) * PX,
    w: M.labelBoxW * PX, h: M.labelBoxH * PX,
    fontFace: "Arial", fontSize: M.labelFontPt, bold: true, color: M.colors.label,
    align: "center", valign: "middle", margin: 0,
  });
}

// Full certified composition. opts:
//   numeral   — badge numeral (printed number on the ORIGINAL frame; child MUST
//               pass its own; default 27)
//   wordCount — number of word chips at 30 deg steps from 0 deg (default 5;
//               slide 28 passes 9)
//   skip      — array of block names to omit: 'title','eqbox','circle',
//               'spokes','chips','arcs'
function renderBase(pptx, slide, opts = {}) {
  const wordCount = opts.wordCount === undefined ? 5 : opts.wordCount;
  const skip = new Set(opts.skip || []);
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 27 : opts.numeral });
  if (!skip.has("circle")) drawCircle(pptx, slide);
  if (!skip.has("spokes")) drawSpokes(pptx, slide);
  if (!skip.has("chips")) {
    for (let k = 0; k < wordCount; k++) {
      drawWordChip(pptx, slide, { label: "Word " + k, angleDeg: k * 30 });
    }
  }
  if (!skip.has("arcs")) {
    for (let k = 0; k + 1 < wordCount; k++) {
      drawArc(pptx, slide, { fromDeg: k * 30, toDeg: (k + 1) * 30 });
    }
  }
  if (!skip.has("eqbox")) drawEquationBox(pptx, slide);
  if (!skip.has("title")) drawTitle(pptx, slide);
}

module.exports = { M, drawHouseChrome, drawTitle, drawEquationBox, drawCircle, drawSpokes, drawWordChip, drawArc, renderBase };
