// slide_038.js — 001_introduction slide 38 "Filters parameters" (Deep Learning DSAI 308).
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_038.jpg (960x540, 1px = 1pt)
//   (scratch_038/measure_1..15.py). Direct 1px=1pt mapping — the certified precedent of
//   this video (slides 001/002/005/031; same chrome landmarks 58/43/899 in the frames).
// Chrome: playlist house chrome (founder directive 2026-10-11) via
//   shared_patterns/house_chrome.js — imported, NEVER re-drawn. Badge numeral 38
//   (file number; this lecture's frames carry no printed numbers — assumption
//   PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).
//
// MEASURED SPEC (frame px):
//   title ink   x 333..633 (center 483), cap top 67, baseline ~94 -> TNR Bold 38pt
//               (PIL advance 301 vs 300 measured; deck-template serif per certified
//               002/005/031 precedent; spec's "Arial-like" is the usual serif/sans
//               JPEG ambiguity — advance + cap both fit TNR Bold 38 best)
//   formula box x 90..879, y 117..234; white fill; blue border (modal (32,23,138) on a
//               3px line — spec 3333CC kept: thin-line JPEG darkening, vision-validated)
//   line1/2/3   TNR 21pt (PIL advance 669/654/177 vs measured 672/656/175), left x 102,
//               baselines 154 / 189 / 223.5 (pitch 35). Color terms: red C00000,
//               blue 000080 (PIL modal (0,0,131-144) = navy, deck pixel law beats the
//               spec's 0000CC guess; same navy as certified slide_005/031 text),
//               green 009900; bold per spec fixes.
//   diagram box x 182..810, y 250..511; white fill; red C00000 border (~2pt).
//               NOTE: the red line at x 57..59 is the PANEL's left border (spans
//               y 44..515), NOT the box — box left edge is x 182 (row-250 red runs
//               x 57..59 + 182..810 only).
//   brown slab  parallelogram: left edge x 260 (y 348..437), right edge x 344
//               (y 296..385), dark side band to x 353; face modal (175,103,18).
//   5 slabs     identical parallelograms, left edges x 393/422/451/480/508 (pitch 28.75),
//               w 42, left-edge y 358..398, rise 20 (top edge to the right), later slab
//               drawn on top (earlier tops peek above). Face colors from PIL modals.
//   dashed lines 4 (PIL count; spec flagged the count uncertain) at y 355/366/376/387,
//               x 350..386, black.
//   X sign      ~(351..374, 336..357) black.
//   = sign      two light-blue 6699FF bars (576..592, y 363..367) / (572..592, y 369..374).
//   circles     5, centers x 625.5/663.5/701.5/741.5/778.5, cy 369, fill d~20 with tan
//               D58429 ring, outer d~30.
//   annotations Comic Sans MS (installed, fc-list): "RGB" ~(294..358, 267..283);
//               "3 dims" ~(316..350, 291..302) + short arrow to (287,332);
//               "7" above stack (404..416, 331..346); "7" mid-height between slabs
//               (445..465, ~355..395); "7" right of purple slab (530..552, 338..388);
//               "3" + tiny pencil doodle (396..446, 398..448);
//               "735 weights" (378..546, 470..496) + 5 arrows fanning up from ~(461,462)
//               to the slab bottoms (399/429/460/491/521, 404).
//   black bar   y 519..539 in the ORIGINAL is the video-player progress bar — EXCLUDED
//               per spec recreation_brief step 18 + judge GROUND RULES (c) (recording
//               artifact). The chrome's half-visible bottom stroke stays visible.
//
// EQUATION LAW: the formula lines are the original's own TYPED linear color-coded text
// ("= 7*7  * 3  * 5  =735") — no stackable constructs (no fractions/sums/scripts), so
// verbatim_text law reproduces them as text; nothing to render in 2D mathtext. The 3D
// slabs are custom geometry pptxgenjs cannot approximate -> matplotlib 600dpi
// transparent PNGs (the certified mechanism), embedded at EXACT size w = px/600,
// sidecars banked in build/assets/.
//
// pptxgenjs laws: bare hex (no '#'), fontFace everywhere, margin: 0, explicit
// lineSpacing on every text box, images at EXACT sidecar size (never rescaled).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_038_recreated.pptx";

const px = (v) => v / 72; // frame px (=pt) -> inches

// palette (PIL-measured / spec; bare hex)
const RED = "C00000";        // title, diagram box border, red emphasis terms
const BLUEBOX = "3333CC";    // formula box border (spec, vision-validated)
const BLACK = "000000";      // body text, diagram ink
const NAVY = "000080";       // blue emphasis terms (PIL modal (0,0,131..144))
const GREEN = "009900";      // green emphasis terms
const EQBLUE = "6699FF";     // '=' bars in the diagram
const TANRING = "D58429";    // circle rings (PIL (213,132,41))
const WHITE = "FFFFFF";

const SERIF = "Times New Roman";
const HAND = "Comic Sans MS";

// LO single-line baseline calibration (slide_031 precedent): rendered baseline ~=
// top + (H - L)/2 + K*fs. K=0.955 initial (TNR); corrected closed-loop from render 1.
const K_SERIF = 0.955;
// closed-loop render-1 correction: LO fixed-spacing baseline sits ~0.46em lower than the
// K=0.955 model -> add per-style empirical deltas (title +12.2px, body lines +9.6px)
const DTITLE = 12.2, DLINE = 9.6;
const K_COMIC = 0.955; // corrected after render if needed
function lineTop(baselinePx, fs, Hpx, Lpt, K) {
  return baselinePx - (Hpx - Lpt) / 2 - K * fs;
}

// sidecar-driven exact-size embed
function addExactPng(slide, side) {
  slide.addImage({
    path: `${ASSETS}/${side.image}`,
    x: px(side.bbox_frame_px[0]), y: px(side.bbox_frame_px[1]),
    w: side.png_w / 600, h: side.png_h / 600,
  });
}
const brownSide = require(`${ASSETS}/slab038_brown.json`);
const stackSide = require(`${ASSETS}/slab038_stack.json`);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge "38") ----
drawHouseChrome(pres, slide, { numeral: 38 });

// ---- 2) title ----
{
  const fs = 38, H = 52, L = 38;
  slide.addText("Filters parameters", {
    x: px(83), y: px(lineTop(94, fs, H, L, K_SERIF) + DTITLE), w: px(800), h: px(H),
    align: "center", valign: "top", margin: 0,
    fontFace: SERIF, fontSize: fs, bold: true, color: RED, lineSpacing: L,
  });
}

// ---- 3) formula box ----
slide.addShape(pres.ShapeType.rect, {
  x: px(90), y: px(117), w: px(790), h: px(118),
  fill: { color: WHITE }, line: { color: BLUEBOX, width: 2 },
});

// formula lines — verbatim text, color-coded runs (single-line boxes at measured
// baselines; explicit lineSpacing pinned)
function formulaLine(baselinePx, runs) {
  const fs = 21, H = 34, L = 21;
  slide.addText(runs.map(([t, c, b]) => ({
    text: t, options: { color: c, bold: !!b },
  })), {
    x: px(102), y: px(lineTop(baselinePx, fs, H, L, K_SERIF) + DLINE), w: px(770), h: px(H),
    align: "left", valign: "top", margin: 0,
    fontFace: SERIF, fontSize: fs, lineSpacing: L,
  });
}
formulaLine(154, [
  ["Number of parameters for different filters applied to same location in the image", BLACK, false],
]);
formulaLine(189, [
  ["= ", BLACK, false],
  ["Filter size (2-D)", RED, true],
  [" * ", BLACK, false],
  ["Number of channels (K)", NAVY, true],
  ["  * ", BLACK, false],
  ["number of different filters", GREEN, true],
]);
formulaLine(223.5, [
  ["= ", BLACK, false],
  ["7*7", RED, true],
  ["  * ", BLACK, false],
  ["3", NAVY, true],
  ["  * ", BLACK, false],
  ["5", GREEN, true],
  ["  =735", BLACK, false],
]);

// ---- 4) diagram box ----
slide.addShape(pres.ShapeType.rect, {
  x: px(182), y: px(250), w: px(629), h: px(262),
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

// ---- 5) slabs (600dpi PNGs, exact size) ----
addExactPng(slide, brownSide);
addExactPng(slide, stackSide);

// ---- 6) four dashed projection lines (measured count = 4) ----
for (const y of [355, 366, 376, 387]) {
  slide.addShape(pres.ShapeType.line, {
    x: px(350), y: px(y), w: px(36), h: 0,
    line: { color: BLACK, width: 1, dashType: "dash" },
  });
}

// ---- 7) X multiplication sign ----
slide.addText("X", {
  x: px(350), y: px(332), w: px(24), h: px(28),
  align: "center", valign: "middle", margin: 0,
  fontFace: HAND, fontSize: 26, bold: true, color: BLACK,
});

// ---- 8) light-blue '=' bars ----
slide.addShape(pres.ShapeType.rect, {
  x: px(575), y: px(362.5), w: px(17), h: px(4),
  fill: { color: EQBLUE }, line: { color: EQBLUE, width: 0 },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(572), y: px(369), w: px(20), h: px(5),
  fill: { color: EQBLUE }, line: { color: EQBLUE, width: 0 },
});

// ---- 9) five output circles (colored fill + tan ring) ----
const CIRC_COLORS = ["0BBFE9", "0ABF50", "E90000", "FDFF0B", "6A239D"];
const CIRC_CX = [625.5, 663.5, 701.5, 741.5, 778.5];
for (let i = 0; i < 5; i++) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(CIRC_CX[i] - 14), y: px(369 - 14), w: px(28), h: px(28),
    fill: { color: CIRC_COLORS[i] }, line: { color: TANRING, width: 2 },
  });
}

// ---- 10) handwritten annotations (Comic Sans MS) ----
function handText(t, box, fs, opts = {}) {
  slide.addText(t, {
    x: px(box[0]), y: px(box[1]), w: px(box[2]), h: px(box[3]),
    align: opts.align || "center", valign: opts.valign || "middle", margin: 0,
    fontFace: HAND, fontSize: fs, bold: true, color: BLACK,
    charSpacing: opts.charSpacing,
  });
}
handText("RGB", [292, 262, 68, 26], 21, { charSpacing: 7 }); // above the brown slab (original letters widely spaced: ink w 64 vs Comic 21pt 47)
handText("3 dims", [314, 288, 40, 18], 12);              // label, arrow below
handText("7", [400, 328, 20, 22], 19);                   // above the filter stack
handText("7", [440, 352, 30, 44], 34);                   // mid-height, between slabs
handText("7", [522, 334, 34, 56], 42);                   // right side of purple slab
handText("3", [392, 399, 22, 26], 17);                   // beside the pencil doodle
handText("735 weights", [372, 466, 180, 34], 25, { charSpacing: 2.5 });

// ---- 11) arrows ----
function arrow(x1, y1, x2, y2, width = 1) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  slide.addShape(pres.ShapeType.line, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: BLACK, width, endArrowType: "triangle" },
  });
}
arrow(318, 306, 290, 328, 1.25);          // "3 dims" -> slab depth edge (render-2: head ran 8px long)
// five arrows fanning up from "735 weights" to the five slabs
for (const tx of [399, 429, 460, 491, 521]) arrow(461, 462, tx, 404, 1);

// ---- 12) tiny pencil doodle beside the "3" ----
slide.addShape(pres.ShapeType.line, {
  x: px(406), y: px(420), w: px(34), h: px(23),
  flipV: true, line: { color: BLACK, width: 2.5 },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(426), y: px(396), w: px(13), h: px(9), rotate: 12,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
slide.addShape(pres.ShapeType.triangle, {
  x: px(436), y: px(440), w: px(10), h: px(8), rotate: 115,
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
