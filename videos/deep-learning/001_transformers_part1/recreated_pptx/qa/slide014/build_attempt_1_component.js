// components/slide_014.js — slide 014 "Encoder – Decoder Transformer" composition.
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slide 15 builds on this
// composition and REPLACES the right half. It MUST require() this module and call
// renderBase(pptx, slide, opts) (or cherry-pick blocks via opts.skip/opts.only) —
// NEVER re-derive or copy-paste this geometry.
//
// Block granularity: every visual block is its own function; renderBase accepts
//   opts.skip   — array of block names to OMIT (child removes inherited blocks)
//   opts.only   — array of block names to DRAW exclusively (child replaces composition)
//   opts.chrome — draw house chrome (default true; chrome via components/house_chrome.js,
//                 which delegates to the playlist shared pattern)
//   opts.numeral— badge numeral (default 14)
// Block names: title, left_panel, left_figure, arc, right_panel, right_figure,
//   red_caption, blue_takeaway.
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_014.jpg (960x540, 1px=1pt,
// in = px/72; scratch/slide014/measure1-5.py + arc_opt.py + fontcal.py):
//   - White panels are course-drawn white rects with thin black borders:
//     left x[93.5,411.5] y[106,522.5]; right x[476.5,892.5] y[152,470.5] (exact transposes).
//   - Both panels contain the founder-downloaded paper Figure 1 (arXiv 1706.03762v7,
//     banked at ../001_transformers_part1/slide_18_source/, founder directive: slides 14/15
//     MUST use the downloaded images) pasted at natural aspect, scale 0.182:
//     left rect x[117,394] y[115,522] (IoU 0.761); right = the SAME image rotated 90 deg
//     CW (PIL ROTATE_270), rect x[478,885] y[176,453] (IoU 0.781) — margins are exact
//     90-deg-CW transposes (L22 T7 R17 B0 -> L0 T22 R7 B17).
//   - Red rotation arrow: freestanding thick circular arrow in the gutter, circle center
//     (450.4,307.6), annulus r 12.75..30.75, sweep from 90 deg to 285 deg (y-up), triangular
//     head (base r 6.5..40 at 90 deg, tip r 27.5 at 52 deg) pointing CW into the east gap;
//     IoU-optimized against the frame red mask (0.851), rendered as a 600dpi transparent
//     PNG (750x750 px -> exactly 1.25 in), core color CC0000 (measured #CC0404).
//   - Texts (Arial Bold, calibrated with real Arial metrics against frame ink):
//     title 36pt A0000E ink y57..83; red caption 20pt A0000E ink y117..131 x464..719;
//     blue takeaway 25pt 00008B ink y487..509 x456..879 (verbatim double spaces kept).
//
// LAWS honored: playlist chrome via shared module (videos/deep-learning/AGENTS.md);
// founder figure-image mandate (001_transformers_part1/AGENTS.md figure family);
// verbatim text incl. en dash and double spaces; margin:0 + explicit fontFace everywhere;
// no '#' in hex; no multi-line boxes (explicit lineSpacing not applicable).

const path = require("path");
const { drawHouseChrome } = require(path.join(__dirname, "house_chrome.js"));

const ASSETS = path.join(__dirname, "..", "assets");

const px = (v) => v / 72;

const C = {
  red: "A0000E",      // title + red caption (measured cores #9F101F..#AD1A29; certified slide-006 red)
  arcRed: "CC0000",   // rotation arrow fill core (measured #CC0404)
  blue: "00008B",     // takeaway (measured cores #04047C..#040484)
  panelLine: "000000",
  panelFill: "FFFFFF",
};
const SANS = "Arial";

// ---- block functions ---------------------------------------------------------

function drawTitle(pptx, slide) {
  slide.addText("Encoder \u2013 Decoder Transformer", {
    x: px(130), y: px(48.5), w: px(700), h: px(44),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 35.5, bold: true, color: C.red,
  });
}

function drawLeftPanel(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(93.5), y: px(106), w: px(318), h: px(416.5),
    fill: { color: C.panelFill }, line: { color: C.panelLine, width: 1 },
  });
}

function drawLeftFigure(pptx, slide) {
  slide.addImage({
    path: path.join(ASSETS, "slide014_fig1.png"),
    x: px(117), y: px(115), w: px(277), h: px(407),
  });
}

function drawArc(pptx, slide) {
  // 600dpi transparent PNG (750x750 px -> 1.25 in at exact size, never rescaled)
  slide.addImage({
    path: path.join(ASSETS, "slide014_arc_cw.png"),
    x: px(406), y: px(264), w: px(90), h: px(90),
  });
}

function drawRightPanel(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(476.5), y: px(152), w: px(416), h: px(318.5),
    fill: { color: C.panelFill }, line: { color: C.panelLine, width: 1 },
  });
}

function drawRightFigure(pptx, slide) {
  // the same Figure 1 pre-rotated 90 deg clockwise (PIL ROTATE_270), embedded at
  // the frame's measured rect — the frame shows a rigidly rotated copy of the left
  slide.addImage({
    path: path.join(ASSETS, "slide014_fig1_cw.png"),
    x: px(478), y: px(176), w: px(407), h: px(277),
  });
}

function drawRedCaption(pptx, slide) {
  slide.addText("Orientation is not the Issue", {
    x: px(463), y: px(103), w: px(330), h: px(44),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 20, bold: true, color: C.red,
  });
}

function drawBlueTakeaway(pptx, slide) {
  slide.addText("Let us focus on the  Building  blocks", {
    x: px(454), y: px(474.5), w: px(540), h: px(44),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 24.5, bold: true, color: C.blue,
  });
}

// ---- composition -------------------------------------------------------------

const BLOCKS = {
  title: drawTitle,
  left_panel: drawLeftPanel,
  left_figure: drawLeftFigure,
  arc: drawArc,
  right_panel: drawRightPanel,
  right_figure: drawRightFigure,
  red_caption: drawRedCaption,
  blue_takeaway: drawBlueTakeaway,
};

/**
 * Draw the full slide-014 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool, numeral:string|number }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 14 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, C, px };
