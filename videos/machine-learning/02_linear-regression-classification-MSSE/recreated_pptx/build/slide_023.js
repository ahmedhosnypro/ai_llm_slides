// slide_023.js — machine-learning/02_linear-regression-classification-MSSE
// "Some Monotonically increase  Functions" (root slide; PARENT of 24 — bank this
// composition as build/components/slide_023.js after PASS).
//
// Ground truth PIL-measured from unique_slides/slide_023.jpg (960x540, 1px=1pt):
//   title ink x205..777 y70..98 (center 491,84) bold red C8102E ~30pt, double space verbatim
//   three white graph panels, violet-gray 8F8DB2 1pt borders, y132..332:
//     L x136..333.5  C x375..566.5  R x610..885
//   grids D6D6D6 0.5pt: L majors pitch 12.85(col)/13.35(row) anchored at axes;
//     C pitch 13.85/14.333 anchored at axes; R half-unit pitch 8.525/10.7
//   axes 595959 1.25pt, arrowheads both ends (L y156..307/x161..313 at origin 237,266;
//     C full-height/width at 402/232.5); R y-axis A6A6A6 x630 y152..325; R x-axis is a
//     faint D0D0D0 grid-weight full-width line y237.4 (no arrowheads, measured)
//   C y-axis numerals at every unit row (PIL-verified 2026-10-13, judge-2 BLOCKER):
//     single digits 1..6 above the axis (ink x395..398, cx~396.5) and minus+digit
//     -1..-6 below (ink x390..398, cx~394), ~7pt, same gray family as x numbers.
//     The attempt-1 build drew tick DASHES here — a misread of these digit glyphs.
//   tick numbers 333333: C x: -1,1..11 at y239; R x: 2,4,6,8,10,12,14 at y242;
//     R y: "2"@(626,196.5) "-2"@(626,281) 7pt gray 8C8C8C (4/6/-4 absent in frame)
//   C axis letters italic: "y"@(407.5,145.5) "x"@(561,231)
//   curves: log2 PNG (origin 401.6,232.5 units 13.9/14.333, CC0000 lw2) and
//     ln PNG (origin 629.7,237.3 units 17.05/20.9, 808080 lw1.7, ends x863) — matplotlib
//     600dpi transparent, canvas = panel interior, embedded at exact px/600 size
//   labels (mathtext 600dpi): y=\dfrac{1}{2}x 8B0000 ink@(256,184); y=\log_2(x) CC0000
//     ink@(511,167); f(x)=\ln(x) CC0000 ink@(696,170) — original shows a STACKED fraction
//   green 228B22 dashed direction annotations (vert + horiz shafts) with solid triangle
//     heads: L vert x244.5 y208..284 + horiz y284 x->292; C x420.5 y174..252 + y252 x->467;
//     R x657 y177..254 + y254 x->702
//   the small pen/cursor icon next to the left label is a video-capture artifact —
//     omitted per judge GROUND RULES (c) (ml-intro precedent, slide_008 build)
//
// House chrome: shared_patterns/house_chrome.js (THIS deck's geometry), numeral 23.

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const NUMERAL = "23";
const PX = (v) => v / 72; // frame px -> inches (960x540 frame, 1px = 1pt)

// measured palette
const COL = {
  title: "C8102E",
  border: "8F8DB2",
  grid: "D6D6D6",
  axis: "595959",
  axisR: "A6A6A6",
  axisFaint: "D0D0D0",
  tick: "333333",
  tickFaint: "8C8C8C",
  green: "228B22",
};
const FONT = "Arial";
// assets live in build/assets/; resolve from EITHER build/ (live build) or
// build/components/ (banked component imported by children) — same files either way
const _fs = require("fs");
const ASSETS = _fs.existsSync(path.join(__dirname, "assets"))
  ? path.join(__dirname, "assets")
  : path.resolve(__dirname, "../assets");

// ---- assets (600 dpi; PNGs carry an 8px transparent pad around the ink) ----
const EQ = {
  left:   { file: "slide023_eq_left.png",   w: 352, h: 251, inkX: 256, inkY: 184 },
  center: { file: "slide023_eq_center.png", w: 417, h: 90,  inkX: 511, inkY: 166.3 },
  right:  { file: "slide023_eq_right.png",  w: 724, h: 140, inkX: 696, inkY: 170 },
};
const CURVE = {
  log2: { file: "slide023_curve_log2.png", w: 1591, h: 1641, x: 375, y: 134 },
  ln:   { file: "slide023_curve_ln.png",   w: 2275, h: 1641, x: 611, y: 134 },
};

// ---- low-level helpers (component primitives) ------------------------------
function hline(slide, pptx, x0, x1, y, color, width, opts = {}) {
  slide.addShape(pptx.ShapeType.line, {
    x: PX(x0), y: PX(y), w: PX(x1 - x0), h: 0,
    line: { color, width, ...(opts.dash ? { dashType: opts.dash } : {}),
      ...(opts.begin ? { beginArrowType: opts.begin } : {}),
      ...(opts.end ? { endArrowType: opts.end } : {}) },
  });
}
function vline(slide, pptx, x, y0, y1, color, width, opts = {}) {
  slide.addShape(pptx.ShapeType.line, {
    x: PX(x), y: PX(y0), w: 0, h: PX(y1 - y0),
    line: { color, width, ...(opts.dash ? { dashType: opts.dash } : {}),
      ...(opts.begin ? { beginArrowType: opts.begin } : {}),
      ...(opts.end ? { endArrowType: opts.end } : {}) },
  });
}
function diag(slide, pptx, x0, y0, x1, y1, color, width, opts = {}) {
  slide.addShape(pptx.ShapeType.line, {
    x: PX(Math.min(x0, x1)), y: PX(Math.min(y0, y1)),
    w: PX(Math.abs(x1 - x0)), h: PX(Math.abs(y1 - y0)),
    // rising segment (x1>x0, y1<y0) MUST flipV=true: the default box line runs
    // top-left->bottom-right (falling); XOR of the direction bits is the fix
    // (attempt-1 bug: inverted ternary rendered y=(1/2)x FALLING — measured
    // render slope +0.506 vs original -0.5195; see qa/slide023 self-checks).
    flipV: (y1 < y0) !== (x1 < x0),
    line: { color, width, ...(opts.begin ? { beginArrowType: opts.begin } : {}),
      ...(opts.end ? { endArrowType: opts.end } : {}) },
  });
}
function numText(slide, pptx, str, cx, cy, size, color, italic = false) {
  slide.addText(str, {
    x: PX(cx - 10), y: PX(cy - 7), w: PX(20), h: PX(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: size, color, italic,
  });
}
function tri(slide, pptx, cx, cy, w, h, rotate, color) {
  slide.addShape(pptx.ShapeType.triangle, {
    x: PX(cx - w / 2), y: PX(cy - h / 2), w: PX(w), h: PX(h),
    rotate, fill: { color }, line: { type: "none" },
  });
}

// ---- per-block draws --------------------------------------------------------
function drawTitle(pptx, slide) {
  // box offset +12px right / -4px up from the panel band: the ORIGINAL's title ink
  // is centered at (491,84), not on the panel center (480.5) — measured, reproduced.
  slide.addText("Some Monotonically increase  Functions", {
    x: PX(73), y: PX(60), w: PX(839), h: PX(40),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 30, bold: true, color: COL.title,
  });
}

function panelBox(slide, pptx, x0, x1) {
  slide.addShape(pptx.ShapeType.rect, {
    x: PX(x0), y: PX(132), w: PX(x1 - x0), h: PX(200),
    fill: { color: "FFFFFF" }, line: { color: COL.border, width: 1 },
  });
}

function gridLines(slide, pptx, cols, rows, ix0, ix1) {
  for (const c of cols) vline(slide, pptx, c, 134, 331, COL.grid, 0.5);
  for (const r of rows) hline(slide, pptx, ix0, ix1, r, COL.grid, 0.5);
}

function drawPanelL(pptx, slide) {
  panelBox(slide, pptx, 136, 333.5);
  const cols = [172.75, 185.6, 198.45, 211.3, 224.15, 249.85, 262.7, 275.55, 288.4, 301.25];
  const rows = [172.55, 185.9, 199.25, 212.6, 225.95, 239.3, 252.65, 279.35, 292.7, 306.05];
  gridLines(slide, pptx, cols, rows, 137, 332);
  // axes (double arrowheads), origin (237,266)
  vline(slide, pptx, 237, 156, 307, COL.axis, 1.25, { begin: "triangle", end: "triangle" });
  hline(slide, pptx, 161, 313, 266, COL.axis, 1.25, { begin: "triangle", end: "triangle" });
  // the line y = (1/2)x through the origin, arrowheads both ends (native — straight);
  // width 1.5 (original stroke PIL-measured ~1.5px core, attempt-1's 1.75 read heavier)
  diag(slide, pptx, 177, 296, 308, 228, "6A5E8C", 1.5, { begin: "triangle", end: "triangle" });
  // two small amber data-point markers ON the line at grid (1, 1/2) and (4, 2) —
  // PIL-verified in the original (core ~rgb(150,120,75), ~4px dia; centers measured)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: PX(249.5 - 2), y: PX(259.3 - 2), w: PX(4), h: PX(4),
    fill: { color: "D89A4A" }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: PX(288.4 - 2), y: PX(239.3 - 2), w: PX(4), h: PX(4),
    fill: { color: "D89A4A" }, line: { type: "none" },
  });
  // green direction annotation (dashed shafts + solid heads)
  vline(slide, pptx, 244.5, 208, 284, COL.green, 1, { dash: "dash" });
  hline(slide, pptx, 244.5, 292, 284, COL.green, 1, { dash: "dash" });
  tri(slide, pptx, 244.5, 203, 7, 10, 0, COL.green);      // up head
  tri(slide, pptx, 296, 284, 7, 10, 90, COL.green);       // right head
  // label y = (1/2)x — mathtext PNG, ink anchored at (256,184)
  const e = EQ.left;
  slide.addImage({ path: path.join(ASSETS, e.file),
    x: PX(e.inkX) - 8 / 600, y: PX(e.inkY) - 8 / 600, w: e.w / 600, h: e.h / 600 });
}

function drawPanelC(pptx, slide) {
  panelBox(slide, pptx, 375, 566.5);
  const cols = [], rows = [];
  for (let k = -1; k <= 11; k++) if (k !== 0) cols.push(401.6 + 13.85 * k);
  for (let k = -6; k <= 6; k++) if (k !== 0) rows.push(232.5 + 14.333 * k);
  gridLines(slide, pptx, cols, rows, 376, 566);
  // axes full interior, double arrowheads
  vline(slide, pptx, 402, 134.5, 330.5, COL.axis, 1.25, { begin: "triangle", end: "triangle" });
  hline(slide, pptx, 375.5, 566, 232.5, COL.axis, 1.25, { begin: "triangle", end: "triangle" });
  // y-axis numerals at every unit row (PIL-measured glyph centers; 7pt, 333333 —
  // core color matches the x numbers; single digits above, minus+digits below)
  const yt = [["6", 146.5], ["5", 160.8], ["4", 175.2], ["3", 189.5], ["2", 203.8], ["1", 218.2]];
  for (const [s, cy] of yt) numText(slide, pptx, s, 396.5, cy, 7, COL.tick);
  const ytn = [["-1", 246.8], ["-2", 261.2], ["-3", 275.5], ["-4", 289.8], ["-5", 304.2], ["-6", 318.5]];
  for (const [s, cy] of ytn) numText(slide, pptx, s, 394, cy, 7, COL.tick);
  // x tick numbers (verbatim, measured centers; "1" at 416 — the original's glyph
  // sits right of the curve, ink x415..417, NOT at the 414 the attempt-2 build
  // used, where the fat curve stroke swallowed it)
  const xt = [["-1", 385], ["1", 416], ["2", 429.5], ["3", 443], ["4", 457], ["5", 470.5],
              ["6", 484], ["7", 498], ["8", 511.5], ["9", 525], ["10", 539.5], ["11", 552.5]];
  for (const [s, cx] of xt) numText(slide, pptx, s, cx, 239, 8, COL.tick);
  // axis letters
  numText(slide, pptx, "y", 407.5, 145.5, 9, COL.tick, true);
  numText(slide, pptx, "x", 561, 231, 9, COL.tick, true);
  // log2 curve (matplotlib PNG, exact size)
  const c = CURVE.log2;
  slide.addImage({ path: path.join(ASSETS, c.file),
    x: PX(c.x), y: PX(c.y), w: c.w / 600, h: c.h / 600 });
  // green direction annotation
  vline(slide, pptx, 420.5, 174, 252, COL.green, 1, { dash: "dash" });
  hline(slide, pptx, 420.5, 467, 252, COL.green, 1, { dash: "dash" });
  tri(slide, pptx, 420.5, 169.5, 8, 9, 0, COL.green);
  tri(slide, pptx, 471.5, 251.5, 7, 10, 90, COL.green);
  // label y = log_2(x) — mathtext PNG, ink anchored at (511,167)
  const e = EQ.center;
  slide.addImage({ path: path.join(ASSETS, e.file),
    x: PX(e.inkX) - 8 / 600, y: PX(e.inkY) - 8 / 600, w: e.w / 600, h: e.h / 600 });
}

function drawPanelR(pptx, slide) {
  panelBox(slide, pptx, 610, 885);
  const cols = [], rows = [];
  for (let k = 1; k <= 29; k++) cols.push(629.7 + 8.525 * k);
  for (let k = -9; k <= 8; k++) if (k !== 0) rows.push(237.3 + 10.7 * k);
  gridLines(slide, pptx, cols, rows, 611, 884);
  // faint grid-weight x-axis line, full width, no arrowheads (measured)
  hline(slide, pptx, 612, 883, 237.4, COL.axisFaint, 0.75);
  // y-axis (light gray) with double arrowheads
  vline(slide, pptx, 630, 152, 325, COL.axisR, 1.25, { begin: "triangle", end: "triangle" });
  // tick numbers
  const xt = [["2", 663.5], ["4", 697.5], ["6", 731.5], ["8", 765.5], ["10", 800],
              ["12", 834], ["14", 868]];
  for (const [s, cx] of xt) numText(slide, pptx, s, cx, 242, 8, COL.tick);
  numText(slide, pptx, "2", 626, 196.5, 7, COL.tickFaint);
  numText(slide, pptx, "-2", 626, 281, 7, COL.tickFaint);
  // ln curve (matplotlib PNG, exact size; measured end x863)
  const c = CURVE.ln;
  slide.addImage({ path: path.join(ASSETS, c.file),
    x: PX(c.x), y: PX(c.y), w: c.w / 600, h: c.h / 600 });
  // green direction annotation
  vline(slide, pptx, 657, 177, 254, COL.green, 1, { dash: "dash" });
  hline(slide, pptx, 657, 702, 254, COL.green, 1, { dash: "dash" });
  tri(slide, pptx, 657, 172.5, 6.5, 9, 0, COL.green);
  tri(slide, pptx, 708, 254.5, 7, 10, 90, COL.green);
  // label f(x) = ln(x) — mathtext PNG, ink anchored at (696,170)
  const e = EQ.right;
  slide.addImage({ path: path.join(ASSETS, e.file),
    x: PX(e.inkX) - 8 / 600, y: PX(e.inkY) - 8 / 600, w: e.w / 600, h: e.h / 600 });
}

// renderBase: full composition (chrome once + title + 3 panels).
// Children (slide 24) import this; opts.skip = ['title'|'panelL'|'panelC'|'panelR'].
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? NUMERAL : opts.numeral });
  const skip = new Set(opts.skip || []);
  if (!skip.has("title")) drawTitle(pptx, slide);
  if (!skip.has("panelL")) drawPanelL(pptx, slide);
  if (!skip.has("panelC")) drawPanelC(pptx, slide);
  if (!skip.has("panelR")) drawPanelR(pptx, slide);
}

// ---- direct run ----
if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const slide = pres.addSlide();
  renderBase(pres, slide);
  const out = process.argv[2] || path.resolve(__dirname, "../slide_023_recreated.pptx");
  pres.writeFile({ fileName: out })
    .then(() => console.log("WROTE", out))
    .catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawTitle, drawPanelL, drawPanelC, drawPanelR, COL, EQ, CURVE, NUMERAL };
