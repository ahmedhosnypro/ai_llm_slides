// slide_042.js — 001_introduction slide 42 "Output dimensions of Convolution?"
// Deep Learning DSAI 308 playlist. RESUME BUILD (2026-10-12): previous workers banked
// 4 PIL measurement rounds (qa/slide042/measure_original*_out.txt) + generate_diagrams.py
// (traced 3D-volume PNGs + label pastes); this worker verified the measurements against
// the frame, decomposed the 4 box equations into measured ink-anchored token renders
// (the banked whole-equation \dfrac PNGs are 1.6-1.8x too tall — width-only calibration;
// kept banked, unused), and wrote this build.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_042.jpg (960x540, 1px = 1pt).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 42 (001_introduction originals carry no printed
//   numbers — ASSUMPTION PENDING FOUNDER VETO, see video AGENTS.md).
//
// Measured constants (frame px):
//   title   Verdana Bold 30pt C00000 (Verdana Bold 30 ink w 592 vs measured 593 — best fit;
//           cap 22 vs ~24.5 measured, documented MINOR), ink x186..778 center 482,
//           cap top 80, baseline ~104.5
//   panel   inner white panel stroke-center rect x77..891 y135..507, fill FFFFFF,
//           border C00000 1pt (strokes 2 frame-px thick = 1pt@150dpi; modal #7D1B28 = washed C00000)
//   slab    traced 600dpi PNG x112..268 y192..366 (input slab + w_in/h_in/d_in labels + stride
//           arrow + 's' — all baked by generate_diagrams.py from the original pixels)
//   slices  traced 600dpi PNG x262..470 y210..325 (5 filter slices + w_f/n_f/h_f/d_f labels)
//   output  traced 600dpi PNG x545..880 y366.. (x545..880 y158..366; tan box + w_out/h_out/d_out)
//   equals  large '=' between slices and output: ink x500..522 y266..273 — TWO bars (3px/2.5px),
//           drawn as 2 native rects (text '=' cannot match the 23x8 aspect at any size)
//   eqbox   white rect stroke-center x317..521 y334..462, border 000000 1pt (modal #232323)
//   eqs     4 equations DECOMPOSED into 30 token PNGs (Liberation Serif = TNR-metric; italic
//           variables, upright '='/'+'/'1'/'out'/'in' — upright fits the measured subscript
//           w/xh aspect 3.8) + 4 native rects (2 fraction bars, 2 minus signs), each placed at
//           its measured ink box (ALIGNMENT LAW). Manifest: build/assets/eq42tok/.
//   legend  6 lines, ALL-NAVY 000060 per frame forensics (darkest-core #040454..#06065C; the
//           spec's '#0000CC symbols + black words' is a spec approximation — frame wins),
//           Verdana 16 (word widths best fit: 'Filters Count' 102 vs 101 measured),
//           symbols bold-italic @x106, words regular @x136, baselines 386.5/407.5/428.5/449.5/
//           470.5/491.5 (pitch 21). VERBATIM incl. the 'hight' misspelling.
//   NOT recreated (video artifacts, spec brief step 10 + judge ground rule (c)): bottom black
//   letterbox strip.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const EQ = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/eq42tok/eq42tok_manifest.json");

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_042_recreated.pptx";

const px = (v) => v / 72; // frame px (=pt) -> inches

// ---- palette (PIL-measured; bare hex for pptxgenjs) ----
const RED = "C00000";    // title + inner panel border (deck standard; measured modal wash #7D1B28)
const WHITE = "FFFFFF";
const BLACK = "000000";
const NAVY = "000060";   // legend (measured darkest core)

// LO single-line baseline law (empirical, closed-loop-verified on slides 005/031/043):
// baseline = top + (H - L)/2 + L - descent_em*fs  ->  top = baseline - (H-L)/2 - L + d*fs
// Verdana d = 0.206 (reproduces slide_043's calibrated Verdana Bold 16 offset 30.8 at ls25).
function lineTopVerdana(baselinePx, fs, Lpt) {
  const H = 43.2; // 0.6in box
  return baselinePx - (H - Lpt) / 2 - Lpt + 0.206 * fs;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge 42) ----
drawHouseChrome(pres, slide, { numeral: "42" });

// ---- 2) inner white panel with red border (stroke-center x77..891 y135..507) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(77), y: px(135), w: px(891 - 77), h: px(507 - 135),
  fill: { color: WHITE }, line: { color: RED, width: 1 },
});

// ---- 3) diagram regions — DIRECT CROPS of the original frame (slide_040 certified
//         precedent for regions pptxgenjs cannot draw). The previous worker's color-cluster
//         vector trace lost the stride marker (drawn outside the traced axes — BLOCKER in
//         the attempt-3 slab crop comparison) and merged the filter-slice colors (MAJOR);
//         the traced PNGs stay banked, the crops replace them. Region borders verified in
//         white space; labels + stride marker are the original's own verbatim pixels. ----
slide.addImage({
  path: `${ASSETS}/slide042_slab_crop.png`,
  x: px(112), y: px(192), w: px(268 - 112), h: px(366 - 192),
});
slide.addImage({
  path: `${ASSETS}/slide042_slices_crop.png`,
  x: px(262), y: px(210), w: px(470 - 262), h: px(325 - 210),
});
slide.addImage({
  path: `${ASSETS}/slide042_output_crop.png`,
  x: px(545), y: px(158), w: px(880 - 545), h: px(366 - 158),
});

// ---- 4) large '=' between slices and output (two native bars, ink x500..522 y266..273) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(500), y: px(265.9), w: px(23), h: px(2.8), fill: { color: BLACK }, line: { type: "none" },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(500), y: px(272.0), w: px(23), h: px(2.6), fill: { color: BLACK }, line: { type: "none" },
});

// ---- 5) equation box (white, black 1pt border; stroke-center x317..521 y334..462) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(317), y: px(334), w: px(521 - 317), h: px(462 - 334),
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});

// ---- 6) equation tokens (ink-anchored; manifest carries per-token fs + measured box) ----
for (const T of EQ.tokens) {
  slide.addImage({
    path: T.png,
    x: px(T.ink_left), y: px(T.ink_top), w: T.w_in, h: T.h_in,
  });
}
// fraction bars + minus signs (pure geometry -> native rects, exact measured boxes)
for (const R of EQ.rects.bars) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(R.x), y: px(R.y), w: px(R.w), h: px(R.h), fill: { color: BLACK }, line: { type: "none" },
  });
}
for (const R of EQ.rects.minus) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(R.x), y: px(R.y), w: px(R.w), h: px(R.h), fill: { color: BLACK }, line: { type: "none" },
  });
}

// ---- 7) title — Verdana Bold 30.2 C00000, ink center 482, baseline 104.5 ----
// (attempt-1 closed loop: 30pt ink w 588 vs 592 target -> fs 30.2; center 480.9 -> x 51)
slide.addText("Output dimensions of Convolution?", {
  x: px(51), y: px(lineTopVerdana(104.5, 30.2, 36)), w: px(864), h: 0.6,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Verdana", fontSize: 30.2, bold: true, color: RED,
  lineSpacing: 36,
});

// ---- 8) variable legend — 6 lines, Times New Roman ITALIC 19 (SERIF — the attempt-3
//         legend crop comparison found the original's legend is serif italic with a light
//         (non-bold) symbol column; the earlier Verdana choice failed on face+style),
//         all-navy 000060 per frame forensics, symbols regular-italic @x106, words
//         regular-italic @ measured per-line ink start, baselines pitch 21,
//         VERBATIM incl. the 'hight' misspelling ----
const LEGEND = [
  { sym: "h", word: "hight", wx: 139.5, baseline: 386.5 },
  { sym: "w", word: "Width", wx: 138.5, baseline: 407.5 },
  { sym: "d", word: "Depth", wx: 138.5, baseline: 428.5 },
  { sym: "f", word: "Filter", wx: 140.5, baseline: 449.5 },
  { sym: "n", word: "Filters Count", wx: 135.5, baseline: 470.5 },
  { sym: "S", word: "Stride", wx: 135.5, baseline: 491.5 },
];
// LO single-line baseline law, Times New Roman (slide_031/043 double-calibrated K=0.924):
// top = baseline - (H - L)/2 - K*fs
function lineTopTimes(baselinePx, fs, Lpt) {
  const H = 43.2; // 0.6in box
  return baselinePx - (H - Lpt) / 2 - 0.924 * fs;
}
LEGEND.forEach((L) => {
  slide.addText(L.sym, {
    x: px(106), y: px(lineTopTimes(L.baseline, 19, 21)), w: px(26), h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Times New Roman", fontSize: 19, italic: true, color: NAVY,
    lineSpacing: 21,
  });
  slide.addText(L.word, {
    x: px(L.wx), y: px(lineTopTimes(L.baseline, 19, 21)), w: px(320 - L.wx), h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Times New Roman", fontSize: 19, italic: true, color: NAVY,
    lineSpacing: 21,
  });
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
