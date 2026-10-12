// Slide 027 component — "Sequence of 5 words / Positions are defined as angles"
// (Deep Learning DSAI 308, 002_transformers_part2) — banked per the dependency law
// (.agents/skills/slide-recreation/references/dependencies.md).
//
// CONFIRMED DEPENDENT: slide 28 (28 ← [27, 26]) = THIS composition grown from
// 5 words / 4 arcs to 9 words / 8 arcs. Block granularity is therefore MANDATORY:
// every visual block is its own function; renderBase(pptx, slide, opts) composes
// them and accepts opts.skip / opts.wordCount so the child grows the composition
// without re-deriving geometry. NEVER copy-paste this file into a child build —
// require() it (cross-video children: absolute path).
//
// All geometry PIL-measured from the ground-truth frame
// videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg
// (960x540, 1 px = 1 pt = 1/72 in) — measurement scripts banked in
// scratch/slide027/measure_frame*.py + measure_hires.py (native 1280x720
// video frame used to decode the fine dotted/spoke structure).
//
// House chrome: playlist law (videos/deep-learning/AGENTS.md) — drawn ONCE here
// via shared_patterns/house_chrome.js; children must NOT re-draw it.
//
// Z-ORDER (as measured): chrome → circle → spokes (cross the circle interior)
// → arcs → word chips (cover the spokes) → arrowheads → +ω labels → equation
// box → title.

const PATH_SHARED = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js";
const { drawHouseChrome } = require(PATH_SHARED);

const PX = 1 / 72; // frame px -> inches

// ------- measured constants (frame px unless noted) -------
const M = {
  colors: {
    circleFill: "FBFCC9", circleLine: "A0A0A5",   // pale yellow fill, muted gray-blue rim
    spoke: "BEAEB2",                              // dusty mauve (measured dot cores 190,174,178 — NOT red)
    chipFill: "CCFFCC", chipLine: "009933", chipText: "009933",
    arc: "E06010",                                // curved +ω arrows
    label: "CC0000",                              // '+ω' labels
    title: "CC0000",
    eqFill: "FFFFCC", eqLine: "9B9BAD",           // muted gray-lavender border (JPEG-muted samples)
    eqBlue: "0000CC", eqRed: "CC0000", eqGreen: "009900",
  },
  // clock-face circle
  circle: { cx: 578.5, cy: 283.5, r: 126 },
  // radial spokes: 12 dotted lines at 30 deg steps, from the circle CENTER
  // outward (they cross the interior — measured). Overshoots per angle class:
  spokeInner: 0,                                  // lines start at the center (convergence blob measured)
  spokeLenCardinalH: 314,                         // 0/180 deg — reach nearly to the panel edge
  spokeLenCardinalV: 236,                         // 90/270 deg — reach nearly to the panel top
  spokeLenDiagonal: 228,                          // 30/60/.../330 deg
  spokeWidthPt: 1,
  // word chips: centered exactly on the k*30 deg spoke at this radius
  chipR: 173.5, chipW: 0.93, chipH: 0.31,         // inches for w/h
  chipFontPt: 12,
  // arcs: circle-centered thin orange arcs sweeping spoke-to-spoke
  arcR: 216, arcStartPadDeg: 1.5, arcEndPadDeg: 1.0, arcWidthPt: 1,
  // arrowheads: UNROTATED down-pointing triangles (measured — all four point
  // screen-down regardless of spoke angle), centered at the destination spoke
  ahR: 214.5, ahW: 0.1389, ahH: 0.1806,           // inches
  // '+w' labels: bold red; first four at MEASURED positions (no clean polar
  // law — professor placed them by hand); extras (slide 28+) use the auto rule.
  labelsMeasured: [ // frame px centers, k = 0..3 (arc Word k -> Word k+1)
    [826.0, 226.0], [778.0, 99.5], [636.5, 72.0], [519.0, 72.0],
  ],
  labelAutoR: 232, labelFontPt: 17, labelBoxW: 0.5, labelBoxH: 0.3,
  // title (three red bold lines; line 3 indented — measured)
  title: {
    lines: ["Sequence of 5 words", "Positions are defined", "as angles"],
    boxes: [ // frame px [x, y(box top)] — cap tops 61/86/113 minus ascent offset
      [71.0, 56.8], [71.0, 81.8], [135.5, 104.5],
    ],
    w: [4.5, 4.5, 3.2], h: 0.42, fontPt: 22,
  },
  // equation box (pale yellow inset, left side)
  eq: { x: 81, y: 180, w: 138, h: 67, textX: 89.5, textY: 186, textW: 1.7, textH: 0.78, fontPt: 16, lineSpacingPt: 19.5 },
};

const RAD = Math.PI / 180;

// polar helper: point at CCW angle deg (0 = 3 o'clock) at radius r from center
function polar(deg, r) {
  return { x: M.circle.cx + r * Math.cos(deg * RAD), y: M.circle.cy - r * Math.sin(deg * RAD) };
}

// ------- blocks -------

function drawTitle(pptx, slide, opts = {}) {
  const lines = opts.titleLines || M.title.lines;
  for (let i = 0; i < lines.length && i < 3; i++) {
    const [tx, ty] = M.title.boxes[i];
    slide.addText(lines[i], {
      x: tx * PX, y: ty * PX, w: M.title.w[i], h: M.title.h,
      fontFace: "Arial", fontSize: M.title.fontPt, bold: true, color: M.colors.title,
      align: "left", valign: "top", margin: 0,
    });
  }
}

function drawEquationBox(pptx, slide, opts = {}) {
  const e = M.eq;
  slide.addShape(pptx.ShapeType.rect, {
    x: e.x * PX, y: e.y * PX, w: e.w * PX, h: e.h * PX,
    fill: { color: M.colors.eqFill }, line: { color: M.colors.eqLine, width: 1 },
  });
  // Verbatim per spec: 'Sin' bold blue + '(ω t)' red / 'Cos' blue + '(ω t)' red /
  // 't=0,1,2,3,....' green. Linear text matches the original (no stacked
  // constructs -> professional format == this text; founder math rule N/A).
  slide.addText([
    { text: "Sin", options: { color: M.colors.eqBlue, bold: true } },
    { text: "(ω t)", options: { color: M.colors.eqRed, bold: true, breakLine: true } },
    { text: "Cos", options: { color: M.colors.eqBlue, bold: true } },
    { text: "(ω t)", options: { color: M.colors.eqRed, bold: true, breakLine: true } },
    { text: "t=0,1,2,3,....", options: { color: M.colors.eqGreen, bold: true } },
  ], {
    x: e.textX * PX, y: e.textY * PX, w: e.textW, h: e.textH,
    fontFace: "Arial", fontSize: e.fontPt, align: "left", valign: "top",
    margin: 0, lineSpacing: e.lineSpacingPt,
  });
}

function drawCircle(pptx, slide) {
  const c = M.circle;
  slide.addShape(pptx.ShapeType.ellipse, {
    x: (c.cx - c.r) * PX, y: (c.cy - c.r) * PX, w: 2 * c.r * PX, h: 2 * c.r * PX,
    fill: { color: M.colors.circleFill }, line: { color: M.colors.circleLine, width: 1 },
  });
}

function drawSpokes(pptx, slide) {
  for (let k = 0; k < 12; k++) {
    const phi = k * 30;
    const len = (phi % 180 === 0) ? M.spokeLenCardinalH
      : (phi % 90 === 0) ? M.spokeLenCardinalV
      : M.spokeLenDiagonal;
    const tip = polar(phi, len);
    const mid = polar(phi, len / 2);
    slide.addShape(pptx.ShapeType.line, {
      x: mid.x * PX, y: mid.y * PX, w: len * PX, h: 0,
      rotate: (360 - phi) % 360,
      line: { color: M.colors.spoke, width: M.spokeWidthPt, dashType: "sysDot" },
    });
  }
}

// One word chip centered on the phi-degree spoke. opts: {label, angleDeg}
function drawWordChip(pptx, slide, o) {
  const c = polar(o.angleDeg, M.chipR);
  slide.addText(o.label, {
    shape: pptx.ShapeType.rect,
    x: (c.x - (M.chipW * 72) / 2) * PX, y: (c.y - (M.chipH * 72) / 2) * PX,
    w: M.chipW, h: M.chipH, rotate: (360 - (o.angleDeg % 360)) % 360,
    fill: { color: M.colors.chipFill }, line: { color: M.colors.chipLine, width: 1 },
    fontFace: "Arial", fontSize: M.chipFontPt, bold: true, italic: true,
    color: M.colors.chipText, align: "center", valign: "middle", margin: 0,
  });
}

// One curved +w arrow from angle a to angle b (CCW deg): thin orange arc
// (circle-centered, radius M.arcR) + unrotated down-triangle arrowhead at the
// destination spoke + optional '+w' label (k<4 measured positions, else auto).
function drawArc(pptx, slide, o) {
  const startCCW = o.fromDeg + M.arcStartPadDeg;
  const endCCW = o.toDeg - M.arcEndPadDeg;
  // pptxgenjs/PowerPoint arc angles: 0 = 3 o'clock, CLOCKWISE positive
  // (probe-verified: angleRange [a,b] sweeps clockwise a->b).
  const pptStart = (360 - endCCW) % 360;
  const pptEnd = (360 - startCCW) % 360;
  const R = M.arcR;
  slide.addShape(pptx.ShapeType.arc, {
    x: (M.circle.cx - R) * PX, y: (M.circle.cy - R) * PX, w: 2 * R * PX, h: 2 * R * PX,
    angleRange: [pptStart, pptEnd],
    line: { color: M.colors.arc, width: M.arcWidthPt }, fill: { type: "none" },
  });
  // arrowhead: down-pointing triangle centered on the destination spoke
  const ah = polar(o.toDeg, M.ahR);
  slide.addShape(pptx.ShapeType.triangle, {
    x: (ah.x - (M.ahW * 72) / 2) * PX, y: (ah.y - (M.ahH * 72) / 2) * PX,
    w: M.ahW, h: M.ahH, flipV: true,
    fill: { color: M.colors.arc }, line: { type: "none" },
  });
  // '+w' label
  const k = Math.round(o.fromDeg / 30);
  let lp;
  if (k < M.labelsMeasured.length) {
    lp = { x: M.labelsMeasured[k][0], y: M.labelsMeasured[k][1] };
  } else {
    lp = polar(o.fromDeg / 2 + o.toDeg / 2, M.labelAutoR);
  }
  slide.addText("+ω", {
    x: (lp.x - (M.labelBoxW * 72) / 2) * PX, y: (lp.y - (M.labelBoxH * 72) / 2) * PX,
    w: M.labelBoxW, h: M.labelBoxH,
    fontFace: "Arial", fontSize: M.labelFontPt, bold: true, color: M.colors.label,
    align: "center", valign: "middle", margin: 0,
  });
}

// Full certified composition. opts:
//   numeral   — badge numeral (printed number on the ORIGINAL frame; child MUST
//               pass its own)
//   wordCount — number of word chips at 30 deg steps from 0 deg (default 5;
//               slide 28 passes 9)
//   skip      — array of block names to omit: 'title','eqbox','circle',
//               'spokes','chips','arcs'
function renderBase(pptx, slide, opts = {}) {
  const wordCount = opts.wordCount === undefined ? 5 : opts.wordCount;
  const skip = new Set(opts.skip || []);
  drawHouseChrome(pptx, slide, { numeral: opts.numeral });
  if (!skip.has("circle")) drawCircle(pptx, slide);
  if (!skip.has("spokes")) drawSpokes(pptx, slide);
  if (!skip.has("arcs")) {
    for (let k = 0; k + 1 < wordCount; k++) {
      drawArc(pptx, slide, { fromDeg: k * 30, toDeg: (k + 1) * 30 });
    }
  }
  if (!skip.has("chips")) {
    for (let k = 0; k < wordCount; k++) {
      drawWordChip(pptx, slide, { label: "Word " + k, angleDeg: k * 30 });
    }
  }
  if (!skip.has("eqbox")) drawEquationBox(pptx, slide);
  if (!skip.has("title")) drawTitle(pptx, slide);
}

module.exports = { M, drawHouseChrome, drawTitle, drawEquationBox, drawCircle, drawSpokes, drawWordChip, drawArc, renderBase };
