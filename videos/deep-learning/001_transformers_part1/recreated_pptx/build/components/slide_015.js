// components/slide_015.js — slide 015 "Encoder – Decoder Transformer" composition.
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11; retro-banked 2026-10-11 under
// the PLAYLIST-SCOPED BANKING OBLIGATION — dependencies.md v2): slide 4 of
// 002_transformers_part2 builds on this composition (qualified cross-video parent ref
// `deep-learning/001_transformers_part1:15`). Cross-video children MUST require() this
// module by ABSOLUTE path and call renderBase(pptx, slide, opts) — or cherry-pick
// blocks via opts.skip / opts.only — NEVER re-derive or copy-paste this geometry.
// (Retro-bank note: slide 15 certified before 002's graph existed; this component was
// derived additively from its certified build script build/slide_015.js and verified
// 0-pixel-diff against the certified render — see
// scratch/slide015_component_verify/REPORT.md.)
//
// This composition is itself a CHILD of the certified parent component
// components/slide_014.js. The inherited blocks (title, left_panel, left_figure) are
// DELEGATED to the parent's own certified block functions via parent.BLOCKS — never
// re-drawn — and the blocks slide 15 removed (arc, right_panel, right_figure,
// red_caption, blue_takeaway) are simply ABSENT from this BLOCKS table. House chrome
// (playlist pattern, numeral 15 by default) is drawn ONCE here via
// components/house_chrome.js; children must not re-draw it on top.
//
// Block granularity (one function per visual block, in z-order):
//   title, left_panel, left_figure          (inherited — parent's certified fns)
//   green_card, fig1_recolor, block_arrow, up1, up2, encoder_header, decoder_header
//
// GEOMETRY PROVENANCE: copy-then-modify from the CERTIFIED build script
// build/slide_015.js (single source of truth — never re-derived by eye). That script's
// geometry was PIL-measured from unique_slides/slide_015.jpg (960x540, 1px=1pt,
// in = px/72) in scratch/slide015/measure1-4.py + recolor2.py + verify_asset.py:
//   - right panel card: white fill, 2pt 00B050 border, stroke centerline rect
//     (573,105) 321x419 pt (strokes cols 572-574 / 893-895, rows 104-106 / 523-525);
//   - recolored paper Figure 1 inside it (founder mandate: the downloaded arXiv
//     image, recolored per the frame — asset slide015_fig1_color.png, 600 dpi,
//     exact size 318x416 pt at (575,107); encoder column peach FDEDDD / decoder
//     column mint CEFFE1, per-box tint remaps + background fields traced from the
//     frame at class agreement 0.999, asset dark-ink IoU 0.579);
//   - red gutter block arrow (asset slide015_blockarrow.png, 600 dpi PNG at exact
//     size 68x24 pt at (458,295); polygon shaft x[458,512] y[300,313] + head base
//     x512 y[295,318] tip (525,306.5), core CC0000);
//   - two small red data-flow up-arrows (600 dpi PNGs at exact size): up1 13x27 pt
//     at (654,487) beside "Inputs", up2 11x25 pt at (740,116) beside
//     "Output Probabilities";
//   - headers "Encoder" C00000 (box (583,112) 110x20) / "Decoder" 00A651 (box
//     (769,111) 117x20), Arial bold italic 16 pt — the only italics on the slide.
//
// LAWS honored: parent component imported, never re-derived (dependencies.md);
// playlist chrome via the shared primitive (videos/deep-learning/AGENTS.md);
// founder figure-image mandate (001_transformers_part1/AGENTS.md figure family);
// verbatim labels come from the paper figure itself; margin:0 + explicit fontFace on
// text; no '#' in hex; single-version deliverable (no equations -> no OMML pass).

const path = require("path");
const { drawHouseChrome } = require(path.join(__dirname, "house_chrome.js"));
const parent = require(path.join(__dirname, "slide_014.js"));

const ASSETS = path.join(__dirname, "..", "assets");

const px = (v) => v / 72;

const C = {
  headerRed: "C00000",   // "Encoder" header (frame-measured)
  headerGreen: "00A651", // "Decoder" header (frame-measured)
  border: "00B050",     // green card border (frame-measured stroke)
  cardFill: "FFFFFF",
};
const SANS = "Arial";

// per-block geometry (pt) — exported for children's closed-loop self-checks
const GEO = {
  green_card: { x: 573, y: 105, w: 321, h: 419 },
  fig1_recolor: { x: 575, y: 107, w: 318, h: 416 },
  block_arrow: { x: 458, y: 295, w: 68, h: 24 },
  up1: { x: 654, y: 487, w: 13, h: 27 },
  up2: { x: 740, y: 116, w: 11, h: 25 },
  encoder_header: { x: 583, y: 112, w: 110, h: 20 },
  decoder_header: { x: 769, y: 111, w: 117, h: 20 },
};

// ---- delta block functions (copy-then-modify from build/slide_015.js) -----------

function drawGreenCard(pptx, slide) {
  // right panel card: white fill, 2pt green border
  slide.addShape(pptx.ShapeType.rect, {
    x: px(573), y: px(105), w: px(321), h: px(419),
    fill: { color: "FFFFFF" },
    line: { color: "00B050", width: 2 },
  });
}

function drawFig1Recolor(pptx, slide) {
  // recolored Figure 1 (600dpi canvas: shading fields baked in, paper figure on top)
  slide.addImage({
    path: path.join(ASSETS, "slide015_fig1_color.png"),
    x: px(575), y: px(107), w: px(318), h: px(416),
  });
}

function drawBlockArrow(pptx, slide) {
  // red transition block arrow in the gutter (600dpi PNG at exact size)
  slide.addImage({
    path: path.join(ASSETS, "slide015_blockarrow.png"),
    x: px(458), y: px(295), w: px(68), h: px(24),
  });
}

function drawUp1(pptx, slide) {
  // small red data-flow up-arrow beside "Inputs" (600dpi PNG at exact size)
  slide.addImage({
    path: path.join(ASSETS, "slide015_up1.png"),
    x: px(654), y: px(487), w: px(13), h: px(27),
  });
}

function drawUp2(pptx, slide) {
  // small red data-flow up-arrow beside "Output Probabilities" (600dpi PNG)
  slide.addImage({
    path: path.join(ASSETS, "slide015_up2.png"),
    x: px(740), y: px(116), w: px(11), h: px(25),
  });
}

function drawEncoderHeader(pptx, slide) {
  // Encoder header (the only italics on the slide)
  slide.addText("Encoder", {
    x: px(583), y: px(112), w: px(110), h: px(20),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 16, bold: true, italic: true, color: "C00000",
  });
}

function drawDecoderHeader(pptx, slide) {
  // Decoder header
  slide.addText("Decoder", {
    x: px(769), y: px(111), w: px(117), h: px(20),
    align: "right", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 16, bold: true, italic: true, color: "00A651",
  });
}

// ---- composition ----------------------------------------------------------------
// Inherited blocks are the parent component's own certified block functions — the
// same functions parent.renderBase would call for slide 15's certified skip list
// ["arc","right_panel","right_figure","red_caption","blue_takeaway"] — referenced,
// never re-drawn. BLOCKS order = the certified z-order (chrome, then inherited
// blocks, then the delta in build order).

const BLOCKS = {
  title: parent.BLOCKS.title,
  left_panel: parent.BLOCKS.left_panel,
  left_figure: parent.BLOCKS.left_figure,
  green_card: drawGreenCard,
  fig1_recolor: drawFig1Recolor,
  block_arrow: drawBlockArrow,
  up1: drawUp1,
  up2: drawUp2,
  encoder_header: drawEncoderHeader,
  decoder_header: drawDecoderHeader,
};

/**
 * Draw the full slide-015 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool, numeral:string|number }
 *   — skip/only name blocks from the table above; unknown names THROW (a typo in a
 *     child's selector must never silently drop a block).
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  const known = new Set(Object.keys(BLOCKS));
  for (const name of skip) {
    if (!known.has(name)) throw new Error(`slide_015: unknown block name in opts.skip: '${name}'`);
  }
  if (only) {
    for (const name of only) {
      if (!known.has(name)) throw new Error(`slide_015: unknown block name in opts.only: '${name}'`);
    }
  }
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 15 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, C, px, GEO };
