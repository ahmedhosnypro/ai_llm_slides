// components/slide_013.js — slide 013 "Transformer Building Blocks" (section
// divider) composition, Deep Learning DSAI 308, Transformers — Part I (lecture 001).
//
// CERTIFIED COMPONENT (single source of truth): derived byte-faithfully from the
// CERTIFIED build script build/slide_013.js (attempt 1, DB gen_status=passed,
// visual_check=PASS 2026-10-12; comparison transcript
// recreated_pptx/qa/slide013/judge_attempt_1.txt). Do NOT edit after certification
// (cascade law) — copy-then-modify into a NEW module instead.
//
// BANKING SCOPE (founder directive 2026-10-11, playlist-scoped): slide 013 has no
// same-video children, but lecture 002's recap slide 13 recapitulates THIS slide —
// 002's child build MUST require() this module by ABSOLUTE path and call
// renderBase(pptx, slide, opts) with ITS OWN badge numeral
// (opts.numeral = the number printed on the CHILD's original frame) plus its own
// measured delta. NEVER re-derive or copy-paste this geometry.
//
// Block granularity (opts.skip / opts.only), in certified z-order:
//   title
// The house chrome is drawn ONCE here (opts.chrome !== false) via the per-video
// chrome primitive (components/house_chrome.js — delegates to the playlist-shared
// shared_patterns/house_chrome.js); children must NOT re-draw it. Default numeral
// is 13 (the number printed on THIS video's frame); children pass opts.numeral.
//
// GEOMETRY PROVENANCE (PIL-measured from unique_slides/slide_013.jpg, 960x540,
// 1px = 1pt = 1/72 in; scratch/slide013/measure_frame.py):
//   - TITLE "Transformer Building Blocks": ink bbox x[157,822] (w=666), cap top
//     y=250, baseline ~285, descender bottom 295; ink center (489.5, 272.5).
//     Arial Bold em = 666/13.725/0.97 ~ 48.9px AND cap height 35px/0.716 = 48.9px
//     -> fontSize 49 (frame is ground truth; the spec's 54-60pt/56pt pin was a
//     vision estimate, superseded by measurement). Color CC0000, single line.
//     Closed-loop verified on the 150dpi render: ink edges within 5.7 render px
//     (~2.7 frame px) of the original on all four sides (tolerance 8.3).
//   - Text box w=800px (16% wrap headroom over the 672px advance), h=60px,
//     align center + valign middle, box center at the line-box center (489.5, 268).
//   - The gray panel + thin red border + yellow/purple badge ARE the playlist
//     house chrome (this frame's measured border rows/cols are within ~3 frame px
//     of the ratified canonical chrome — the same chrome, video-softened).
//   - The original's cursor artifact at x[638,649] y[286,296] is a screen-capture
//     artifact — deliberately NOT part of this composition (judge ground rule (c)).
//
// VERIFIED: 0-pixel-diff render of a renderBase(default) pptx vs the certified
// reference render qa/slide013/render_1.png (scratch/slide013/component_verify/,
// 2026-10-12).
//
// LAWS honored: playlist chrome drawn once via components/house_chrome.js; badge
// numeral = printed frame number (13 default, overridable); verbatim text;
// margin:0 + fontFace on the text element; single-line box (explicit lineSpacing
// n/a); no '#' in hex; single-version plain-named deliverable.

const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js"
);

const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt)
const FONT = "Arial";

// ---- palette (measured cores) --------------------------------------------------
const C = {
  title: "CC0000", // title ink modal ~(192,15,33) on the video frame; spec CC0000
};

// ---- geometry (frame px) --------------------------------------------------------
const GEO = {
  titleBox: { x: 89.5, y: 238, w: 800, h: 60 }, // ink center (489.5, 272.5)
  titleSize: 49,
};

// ---- blocks (certified z-order) -------------------------------------------------
function drawTitle(pptx, slide) {
  slide.addText("Transformer Building Blocks", {
    x: px(GEO.titleBox.x), y: px(GEO.titleBox.y),
    w: px(GEO.titleBox.w), h: px(GEO.titleBox.h),
    align: "center", valign: "middle",
    fontSize: GEO.titleSize, bold: true, color: C.title,
    fontFace: FONT, margin: 0,
  });
}

const BLOCKS = {
  title: drawTitle,
};

/**
 * Draw the full slide-013 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool,
 *                         numeral:string|number }
 *   — skip/only name blocks from the table above; unknown names THROW (a typo in
 *     a child's selector must never silently drop a block). Default numeral is 13;
 *     cross-video children MUST pass their own printed badge numeral.
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  const known = new Set(Object.keys(BLOCKS));
  for (const name of skip) {
    if (!known.has(name)) throw new Error(`slide_013: unknown block name in opts.skip: '${name}'`);
  }
  if (only) {
    for (const name of only) {
      if (!known.has(name)) throw new Error(`slide_013: unknown block name in opts.only: '${name}'`);
    }
  }
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 13 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, C, px, GEO };
