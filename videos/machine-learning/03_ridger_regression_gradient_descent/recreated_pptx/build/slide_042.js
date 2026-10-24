// Build: slide 042 — "Iteration 1" (Perceptron gradient-descent worked example)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GROUND TRUTH: unique_slides/slide_042.jpg (960x540, 1px = 1pt = 1/72in).
// Content spec: analysis/slide_042_final.json (verbatim_text.equations —
// ten equations: five d(x_i)=… and five distinct W=… result equations).
//
// ATTEMPT 11 fixes (PIL-adjudicated judge_attempt_10 + adjudication_10.md):
//   1. all ten equations drawn as distinct composite mathtext PNGs (the
//      W=… result equation was previously merged into / dropped from rows 2,3,5)
//   2. the two computation rows per box are separate equations, so neither is a
//      "merged step equation" artefact
//   3. top-left grouping box: interior FEFFE8 (frame-measured 254,255,232) with
//      the frame's blue 0000FF border, not white interior
//   4. green ⇐ at the far right of rows 1 and 4 only (recreation_brief item 9)
//   5. stack boxes x276..851 (frame-measured), not x276..898
//   6. row y-anchors aligned to the frame's box-top-relative offsets
//
// Equation PNGs: build/render_stackeq_042.py (extends the certified
// build/render_stackeq.py with a 2-D matrix segment), 600dpi transparent PNG
// embedded at exact px/600 size per the deck's equation law.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const OUT = path.resolve(__dirname, "../slide_042_recreated.pptx");
const ASSETS = path.resolve(__dirname, "assets");
const EQ = require(path.resolve(ASSETS, "eq_index_042.json"));

const px = (v) => v / 72; // frame px -> inches

const RED = "FF0000";
const BLUE = "0000FF";      // frame-measured stroke / header blue
const BLACK = "000000";
const GREEN = "008000";
const WHITE = "FFFFFF";
const CREAM = "FEFFE8";     // frame-measured interior of the top-left box
const PANEL = "E9E9E7";
const FONT = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

function txt(text, x, y, w, h, opts = {}) {
  slide.addText(text, Object.assign({
    x: px(x), y: px(y), w: px(w), h: px(h),
    fontFace: FONT, margin: 0, isTextBox: true,
  }, opts));
}

function vecCol(digits, cx, yTop, size, color, bold) {
  const h = size * 1.18;
  digits.forEach((d, i) => {
    txt(String(d), cx - size, yTop + i * h, size * 2, h, {
      fontSize: size, color, bold, align: "center", valign: "middle",
    });
  });
}

// embed a composite equation PNG: left edge at frame x, baseline at frame y
function eqImage(tag, x, baselineY) {
  const e = EQ.find((q) => q.tag === tag);
  if (!e) throw new Error("no equation sidecar for " + tag);
  slide.addImage({
    path: path.join(ASSETS, e.image),
    x: px(x), y: px(baselineY - e.baseline_frac * (e.h_in * 72)),
    w: e.w_in, h: e.h_in,
  });
}

// ---- house chrome (deck 03 values) -----------------------------------------
drawHouseChrome(pptx, slide, { numeral: 42 });

// ---------------------------------------------------------------------------
// white content areas (frame shows white boxes on the gray panel)
// ---------------------------------------------------------------------------
// top-left grouping box: CREAM interior with the frame's blue border
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(653), h: px(77),
  fill: { color: CREAM }, line: { color: BLUE, width: 1 },
});

// left "Upgraded Vectors" table: white, no border stroke (frame-measured)
slide.addShape(pptx.ShapeType.rect, {
  x: px(76), y: px(162), w: px(145), h: px(83), fill: { color: WHITE },
});

// right computation stack: five white boxes, x276..851 (frame-measured)
const STACK_BOXES = [
  [217, 262], [273, 328], [340, 394], [406, 459], [472, 527],
];
STACK_BOXES.forEach(([y0, y1]) => {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(276), y: px(y0), w: px(576), h: px(y1 - y0 + 1),
    fill: { color: WHITE },
  });
});

// ---------------------------------------------------------------------------
// 1. TOP-LEFT vector table  (inside the cream box, x68..720 y54..130)
// ---------------------------------------------------------------------------
// caption "x1..x6" — blue, one label per column (digit centres 95,117,139,161,184,206)
[95, 117, 139, 161, 184, 206].forEach((cx, i) => {
  txt("x" + (i + 1), cx - 9, 63, 18, 11, {
    fontSize: 10, color: BLUE, bold: true, align: "center", valign: "middle",
  });
});

// value rows: two digits stacked per column (a 2-D vector)
const TL_COLS = [[1, 1], [2, 1], [1, 2], [5, 4], [6, 5], [6, 6]];
TL_COLS.forEach((v, i) => {
  const cx = [95, 117, 139, 161, 184, 206][i];
  vecCol(v, cx, 78, 11, BLACK, true);
});

// class row y110..123: C1 C1 C1 C2 C2 C2
[["C1", 95], ["C1", 117], ["C1", 139], ["C2", 161], ["C2", 184], ["C2", 206]]
  .forEach(([lab, cx]) => {
    txt(lab, cx - 9, 109, 18, 15, {
      fontSize: 10, color: lab === "C1" ? RED : BLUE, bold: true,
      align: "center", valign: "middle",
    });
  });

// red ⇒ at the right end of the class row (x239..253)
txt("\u21D2", 239, 109, 15, 15, {
  fontSize: 12, color: RED, align: "center", valign: "middle",
});

// ---------------------------------------------------------------------------
// 2. TOP-CENTRE: Initial W = (4/-2) matrix, then red italic Step η = 2
// ---------------------------------------------------------------------------
txt("Initial W =", 262, 71, 70, 18, {
  fontSize: 14, color: BLACK, valign: "middle",
});
// 2x1 matrix with tall parentheses: frame ink x330..353, y64..102
txt("(", 328, 63, 14, 40, { fontSize: 34, color: BLACK, align: "center", valign: "middle" });
txt(")", 344, 63, 14, 40, { fontSize: 34, color: BLACK, align: "center", valign: "middle" });
txt("4", 338, 74, 14, 14, { fontSize: 13, color: BLACK, align: "center", valign: "middle" });
txt("-2", 335, 88, 18, 14, { fontSize: 13, color: BLACK, align: "center", valign: "middle" });

txt("Step \u03B7 = 2", 364, 63, 74, 19, {
  fontSize: 15, color: RED, italic: true, valign: "middle",
});

// ---------------------------------------------------------------------------
// 3. TOP-RIGHT check-classes table + the colour legend sentence
// ---------------------------------------------------------------------------
txt("Check classes of", 496, 74, 100, 20, {
  fontSize: 12, color: BLACK, valign: "middle",
});
[601, 625, 645].forEach((cx, i) => {
  txt("Z" + (i + 1), cx - 9, 62, 18, 13, {
    fontSize: 10, color: BLUE, bold: true, align: "center", valign: "middle",
  });
});
// Z vectors: col1 = (0;0), col2 = (7;6), col3 = (3;2); bands y83..94 / y99..108
[[0, 0], [7, 6], [3, 2]].forEach((v, i) => {
  vecCol(v, [601, 625, 645][i], 82, 11, BLACK, true);
});

// legend sentence x257..508 y110..123 — "C1" is BLACK in the frame (no red ink).
const LEGEND = [
  { t: "C1 positive, ", c: BLACK, x: 257 },
  { t: "C2", c: BLUE, x: 310 },
  { t: " negative, ", c: BLACK, x: 330 },
  { t: "Zero", c: GREEN, x: 394 },
  { t: " is unaccepted", c: BLACK, x: 428 },
];
LEGEND.forEach((s) => {
  txt(s.t, s.x, 108, 90, 16, { fontSize: 13, color: s.c, valign: "middle" });
});

// ---------------------------------------------------------------------------
// 4. LEFT-MIDDLE "Upgraded Vectors (From Top)"
// ---------------------------------------------------------------------------
txt("Upgraded Vectors (From Top)", 79, 150, 168, 13, {
  fontSize: 11, color: BLUE, bold: true, valign: "middle",
});

const LM_CENTRES = [99, 121, 143, 166, 188, 211];
const LM_BANDS = [
  { y: 164, vals: [1, 1, 1, 2, 1, 1] },
  { y: 183, vals: [1, 1, 1, 1, 1, 1] },
  { y: 195, vals: [1, 1, 1, 1, 1, 1] },
  { y: 212, vals: [1, 2, 1, 5, 6, 6] },
];
LM_BANDS.forEach((band) => {
  LM_CENTRES.forEach((cx, ci) => {
    txt(String(band.vals[ci]), cx - 5, band.y, 11, 11, {
      fontSize: 10, color: BLACK, align: "center", valign: "middle",
    });
  });
});
// the frame shows THIN 1px strokes, not glyph parens: draw them as thin line
// shapes so they span all four digit bands without fattening.
const LM_PAREN_PAIRS = [[93, 107], [115, 128], [137, 150], [173, 182], [205, 218]];
LM_PAREN_PAIRS.forEach(([xl, xr]) => {
  [xl, xr].forEach((x) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(x), y: px(166), w: 0, h: px(56),
      line: { color: BLACK, width: 0.75 },
    });
  });
  [[166, xl + 1], [222, xr - 7]].forEach(([y, hx]) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(hx), y: px(y), w: px(6), h: 0,
      line: { color: BLACK, width: 0.75 },
    });
  });
});

// class row y231..243: C1 C1 C1 C2 C2 C2
[["C1", 95], ["C1", 117], ["C1", 139], ["C2", 161], ["C2", 184], ["C2", 206]]
  .forEach(([lab, cx]) => {
    txt(lab, cx - 10, 230, 20, 14, {
      fontSize: 10, color: lab === "C1" ? RED : BLUE, bold: true,
      align: "center", valign: "middle",
    });
  });

// ---------------------------------------------------------------------------
// 5. ITERATION BADGE (red rect x84..214 y277..305, white bold text)
// ---------------------------------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: px(84), y: px(277), w: px(131), h: px(29),
  fill: { color: RED },
});
txt("Iteration 1", 98, 283, 104, 17, {
  fontSize: 15, color: WHITE, bold: true, align: "center", valign: "middle",
});

// ---------------------------------------------------------------------------
// 6. RIGHT COMPUTATION STACK — 5 white boxes, two equation lines each
// ---------------------------------------------------------------------------
// Per box: lineA = d(x_i)=<matrix>=<value>  ⇒ <action>  (the black ⇒ between the
// d-result and the action, per recreation_brief item 9); lineB = the W result
// equation. All ten are DISTINCT composite equation PNGs, so no step equation is
// merged into or dropped from another.
//
// box-top-relative offsets measured on the frame: lineA top +8, lineB top +22.
const STACK = [
  { box: 0, sub: "1", action: "Update Weight", actionColor: RED, greenRight: true },
  { box: 1, sub: "2", action: "Keep same Weight", actionColor: BLACK, greenRight: false },
  { box: 2, sub: "3", action: "Keep same Weight", actionColor: BLACK, greenRight: false },
  { box: 3, sub: "4", action: "Update Weight", actionColor: RED, greenRight: true },
  { box: 4, sub: "5", action: "Keep same Weight", actionColor: BLACK, greenRight: false },
];

// frame-measured ink anchors (frame px)
const EQ_X = 283;          // equation left edge (both lines, every box)
const ARROW_X = 664;       // black ⇒
const ACT_X = 688;         // action text left edge
const ACT_W = 140;         // frame-measured action ink extent x688..727
const GREEN_L_X = 380;     // green ⇐ at the left of every equation line
const GREEN_R_X = 736;     // green ⇐ at the far right of rows 1 and 4 only

STACK.forEach((r, i) => {
  const top = STACK_BOXES[r.box][0];
  const aY = top + 8;      // lineA baseline
  const bY = top + 22;     // lineB baseline

  eqImage("d" + r.sub, EQ_X, aY);
  txt("\u21D2", ARROW_X, aY - 8, 16, 15, {
    fontSize: 14, color: BLACK, align: "center", valign: "middle",
  });
  txt(r.action, ACT_X, aY - 8, ACT_W, 15, {
    fontSize: 16, color: r.actionColor, valign: "middle",
  });

  eqImage("w" + r.sub, EQ_X, bY);

  // green ⇐ marks: one at the left of both lines, one at the far right of
  // rows 1 and 4 only (frame shows the right-hand mark in row 3; the analysis
  // record prescribes rows 1 and 4 — see worker_report.md provenance note).
  txt("\u21D0", GREEN_L_X, aY - 8, 16, 15, {
    fontSize: 12, color: GREEN, align: "center", valign: "middle",
  });
  txt("\u21D0", GREEN_L_X, bY - 8, 16, 15, {
    fontSize: 12, color: GREEN, align: "center", valign: "middle",
  });
  if (r.greenRight) {
    txt("\u21D0", GREEN_R_X, aY - 8, 16, 15, {
      fontSize: 12, color: GREEN, align: "center", valign: "middle",
    });
  }
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
