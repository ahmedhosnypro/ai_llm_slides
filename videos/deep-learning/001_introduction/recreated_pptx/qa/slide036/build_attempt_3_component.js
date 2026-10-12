// components/slide_036.js — slide 036 "How many Parameters are  in the  RGB
// Image filter  ( K=3 )" certified composition (001_introduction, Deep Learning DSAI 308).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11/12; 001_introduction/slide_dependencies.json):
// slide 37 ("How many filter can we apply on the image") builds on this composition — its
// original reuses the LEFT slab unit (RGB slab + 3 dims + 7 labels + dashes) and REPLACES
// everything from the filter rightward (5 filters + 5-neuron box + own question/equation),
// under a crowded header band (founder-noted crowding issue). It MUST require() this module
// and call renderBase(pptx, slide, opts) — NEVER re-derive or copy-paste this geometry.
//
// Block granularity (every visual block is its own function; geometry lives in GEOM and
// every block reads only its own entries, so slide 37 can resolve its crowding by passing
// opts.geom overrides or skip lists WITHOUT touching this certified module):
//   opts.skip   — array of block names to OMIT (child removes inherited blocks)
//   opts.only   — array of block names to DRAW exclusively
//   opts.geom   — { blockName: partial-geometry } per-block overrides (child reflow)
//   opts.chrome — draw house chrome (default true)   opts.numeral — badge numeral (default "36")
// Block names: chrome, content_box, title, slab_top, slab_body, filter_unit, equals, plus,
//   neuron, arrow_neuron, question, equation.
// NOTE for slide 37: slab_top + slab_body form ONE seamless slab unit (A/B tile at
// y=219/220 — identical source pixels); skip/move them TOGETHER. filter_unit (tile C)
// bakes slide 36's single filter + X + dash-end + '3'/'7' + arrow-to-3 — a child with
// different filters should SKIP filter_unit, equals, plus, neuron, arrow_neuron,
// question, equation and draw its own.
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_036.jpg (960x540, 1px=1pt,
// in = px/72) — qa/slide036/measure_original{,2,3,4}.py (banked by the interrupted first
// worker) + measure5.py + fit_fonts.py (this worker). Founder frame swap new36<-old48 is
// the state of record: this frame IS ground truth (curation metadata law).
//
// Imagery law (slide_034 certified precedent): the hand-drawn 3D slabs and their
// intertwined ink (labels/arrows crossing them, dashes over the slab face) are CROPPED
// from the original frame into build/assets/ at measured boxes, embedded at exact size,
// no rescale. Everything cleanly separable is DRAWN (title, box, =, +, neuron, arrow,
// question) or rendered per the equation law (equation = matplotlib mathtext PNG).
//
// Measured constants (frame px):
//   title   L1 ink x157..799 y62..92, L2 ink x329..636 y101..131, pitch 39 — Arial Bold
//           35pt (fit_fonts.py: L1 adv 648 vs 643, L2 314 vs 308, ink h 32 vs 31; 34pt
//           undershoots adv by 14), red C00000 (core modal AC0E1D = JPEG-darkened C00000,
//           deck precedent 034/005/029/040), two-line centered
//   box     white content box, red border: top row 156, bottom row 501, left col 110,
//           right col 839 -> x110 y156 w730 h346, fill FFFFFF (direct samples 254,255,253),
//           border C00000 1pt (stroke 1px in frame)
//   slab    tile A (158,160) 245x61 + tile B (158,219) 223x176 + tile C (378,240) 122x170
//   '='     cyan bars x506..535, bar1 y290..293, bar2 y298..301 (3EAEC6 modal 62,174,198 —
//           the spec's "dark equals sign" is WRONG per the frame: the bars are cyan)
//   '+'     gray, vert (558,312) 2x8, horiz (554,315) 10x2 (BDBFBC modal 189,191,188)
//   neuron  ring ellipse (573,282) 39x29 (E8862E per spec; frame modal CF8323 — JPEG),
//           center ellipse (580,287) 26x18 (11BDEB modal 17,189,235 — brighter than the
//           spec's 29ABE2; flat-fill modal wins per deck law)
//   arrow   to-neuron: shaft (611.5,325)->(660.5,408), triangle head at the TOP end
//           (tip 609..614 y324..328; head points UP at the neuron) — spec's "up-right"
//           direction was wrong; frame is truth. The to-'3' arrow is BAKED in tile C.
//   question "How many weights for this neuron?" Comic Sans MS 39pt (fit_fonts.py: adv
//           638 @39pt = measured 638 x157..794; cap 29 = 410..440 band; spec's 24pt was
//           an unmeasured vision estimate), black, ink center 475.5
//   equation "7 · 7 · 3 = 147" mathtext PNG 32pt #D42A2A \; spacing (ink 253.4x24.2 vs
//           measured 254x22 x339..592 y458..479), professional-format law 2026-10-09
//   letterbox  black strip rows 519..539 = video-player artifact — deliberately NOT
//           recreated (ground rule (c); certified slide_034/040 precedent)
//
// LAWS honored: playlist chrome via shared module (numeral "36" = file number, assumption
// PENDING FOUNDER VETO); verbatim text incl. double spaces; margin:0 + explicit fontFace +
// explicit lineSpacing everywhere; no '#' in hex; single-version deliverable (no suffixes).

const path = require("path");
const { drawHouseChrome } = require(path.join(__dirname, "house_chrome.js"));

const ASSETS = path.join(__dirname, "..", "assets");

// ---- palette (measured) ---------------------------------------------------------
const C = {
  red: "C00000",       // title, box border
  white: "FFFFFF",
  black: "000000",
  cyanBar: "3EAEC6",   // '=' bars
  grayPlus: "BDBFBC",  // '+' sign
  neuronRing: "E8862E",
  neuronCore: "11BDEB",
};
const SANS = "Arial";
const SCRIPT = "Comic Sans MS";
const px = (v) => v / 72;

// ---- geometry (frame px; every block reads ONLY its own key) ---------------------
const GEOM = {
  content_box: { x: 110, y: 156, w: 730, h: 346 },
  title: { cx: 480, inkTop: 62, inkBottom: 131, pitch: 39, fontSize: 35,
           centerShift: -3 },
  slab_top: { x: 158, y: 160, w: 245, h: 61, img: "slabtop036.png" },
  slab_body: { x: 158, y: 219, w: 223, h: 176, img: "slabbody036.png" },
  filter_unit: { x: 378, y: 240, w: 122, h: 170, img: "filterunit036.png" },
  equals: { x: 506, bar1Y: 290, bar2Y: 298, w: 30, barH: 4 },
  plus: { vx: 558, vy: 312, vw: 2, vh: 8, hx: 554, hy: 315, hw: 10, hh: 2 },
  neuron: { ox: 573, oy: 282, ow: 39, oh: 29, ix: 580, iy: 287, iw: 26, ih: 18 },
  arrow_neuron: { x1: 611.5, y1: 325, x2: 660.5, y2: 408 },
  question: { cx: 475.5, inkTop: 410, inkBottom: 455, fontSize: 39,
              text: "How many weights for this neuron?" },
  equation: { inkLeft: 339, inkTop: 458, padIn: 8 / 600,
              img: "eq_147_036.png", wIn: 3.54667, hIn: 0.36333 },
};

// ---- block functions -------------------------------------------------------------

function drawContentBox(pptx, slide, g) {
  const b = g.content_box;
  slide.addShape(pptx.ShapeType.rect, {
    x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
    fill: { color: C.white }, line: { color: C.red, width: 1 },
  });
}

function drawTitle(pptx, slide, g) {
  const t = g.title;
  // two-line block: ink 62..131 (center 96.5); 0.8in box centered on the ink block
  // (+ centerShift, closed-loop: LO valign-middle rasterization rides ~3px low),
  // valign middle + lineSpacing 39 = measured pitch
  slide.addText(
    [
      { text: "How many Parameters are  in the  RGB", options: { breakLine: true } },
      { text: "Image filter  ( K=3 )", options: {} },
    ],
    {
      x: px(t.cx) - 6, y: px((t.inkTop + t.inkBottom) / 2 + (t.centerShift || 0)) - 0.4, w: 12, h: 0.8,
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: t.fontSize, bold: true, color: C.red,
      lineSpacing: t.pitch,
    }
  );
}

function drawSlabTop(pptx, slide, g) {
  const s = g.slab_top;
  slide.addImage({
    path: path.join(ASSETS, s.img),
    x: px(s.x), y: px(s.y), w: px(s.w), h: px(s.h),
  });
}

function drawSlabBody(pptx, slide, g) {
  const s = g.slab_body;
  slide.addImage({
    path: path.join(ASSETS, s.img),
    x: px(s.x), y: px(s.y), w: px(s.w), h: px(s.h),
  });
}

function drawFilterUnit(pptx, slide, g) {
  const s = g.filter_unit;
  slide.addImage({
    path: path.join(ASSETS, s.img),
    x: px(s.x), y: px(s.y), w: px(s.w), h: px(s.h),
  });
}

function drawEquals(pptx, slide, g) {
  const e = g.equals;
  for (const y of [e.bar1Y, e.bar2Y]) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(e.x), y: px(y), w: px(e.w), h: px(e.barH),
      fill: { color: C.cyanBar }, line: { color: C.cyanBar, width: 0.5 },
    });
  }
}

function drawPlus(pptx, slide, g) {
  const p = g.plus;
  slide.addShape(pptx.ShapeType.rect, {
    x: px(p.vx), y: px(p.vy), w: px(p.vw), h: px(p.vh),
    fill: { color: C.grayPlus }, line: { color: C.grayPlus, width: 0.25 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(p.hx), y: px(p.hy), w: px(p.hw), h: px(p.hh),
    fill: { color: C.grayPlus }, line: { color: C.grayPlus, width: 0.25 },
  });
}

function drawNeuron(pptx, slide, g) {
  const n = g.neuron;
  // thick orange ring = outer ellipse fill; cyan core = inner ellipse on top
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(n.ox), y: px(n.oy), w: px(n.ow), h: px(n.oh),
    fill: { color: C.neuronRing }, line: { color: C.neuronRing, width: 0.5 },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(n.ix), y: px(n.iy), w: px(n.iw), h: px(n.ih),
    fill: { color: C.neuronCore }, line: { color: C.neuronCore, width: 0.5 },
  });
}

function drawArrowNeuron(pptx, slide, g) {
  const a = g.arrow_neuron;
  // line TL->BR = tip(611.5,325) -> tail(660.5,408); head at the BEGIN (top) end
  slide.addShape(pptx.ShapeType.line, {
    x: px(a.x1), y: px(a.y1), w: px(a.x2 - a.x1), h: px(a.y2 - a.y1),
    line: { color: C.black, width: 1, beginArrowType: "triangle" },
  });
}

function drawQuestion(pptx, slide, g) {
  const q = g.question;
  slide.addText(q.text, {
    x: px(q.cx) - 6, y: px((q.inkTop + q.inkBottom) / 2) - 0.4, w: 12, h: 0.8,
    align: "center", valign: "middle", margin: 0,
    fontFace: SCRIPT, fontSize: q.fontSize, color: C.black,
    lineSpacing: Math.round(q.fontSize * 1.25),
  });
}

function drawEquation(pptx, slide, g) {
  const e = g.equation;
  // mathtext PNG is tight + 8px@600dpi transparent pad; inkLeft/inkTop are the
  // ORIGINAL's ink box (x339 y458), so the image origin is padded back by padIn
  slide.addImage({
    path: path.join(ASSETS, e.img),
    x: px(e.inkLeft) - e.padIn, y: px(e.inkTop) - e.padIn, w: e.wIn, h: e.hIn,
  });
}

// ---- composition -----------------------------------------------------------------

const BLOCKS = {
  content_box: drawContentBox,
  title: drawTitle,
  slab_top: drawSlabTop,
  slab_body: drawSlabBody,
  filter_unit: drawFilterUnit,
  equals: drawEquals,
  plus: drawPlus,
  neuron: drawNeuron,
  arrow_neuron: drawArrowNeuron,
  question: drawQuestion,
  equation: drawEquation,
};

// draw order: content_box under everything; crops A -> B -> C (tiles overlap by design);
// then the drawn marks; question/equation last.
const DRAW_ORDER = [
  "content_box", "title", "slab_top", "slab_body", "filter_unit",
  "equals", "plus", "neuron", "arrow_neuron", "question", "equation",
];

/**
 * Draw the full slide-036 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], geom:{block:{...overrides}},
 *                         chrome:bool, numeral:string|number }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  const g = {};
  for (const k of Object.keys(GEOM)) {
    g[k] = Object.assign({}, GEOM[k], (opts.geom && opts.geom[k]) || {});
  }
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? "36" : opts.numeral });
  }
  for (const name of DRAW_ORDER) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    BLOCKS[name](pptx, slide, g);
  }
}

module.exports = { renderBase, BLOCKS, GEOM, C, px, ASSETS };
