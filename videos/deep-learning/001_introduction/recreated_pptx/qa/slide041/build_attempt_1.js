// build/slide_041.js — slide 41 "The Convolution Process" (001_introduction, Deep Learning
// DSAI 308). CHILD of certified slide 35 (dependency edge 41<-35).
//
// CHILD COMPOSITION LAW APPLICATION (founder directive 2026-10-11/12):
//   The certified parent component components/slide_035.js is IMPORTED by absolute path
//   and its renderBase draws the chrome. Measured diff of frame_041 vs frame_035 shows
//   NONE of the parent's 9 content blocks survive in slide 41's frame (different title
//   text, different panel rect 70..891 x 120..433 vs 379.5..885.5 x 168.5..431.5,
//   different grids/labels/captions), so the child calls renderBase with only:[] (chrome
//   only — the "remove parent blocks" case of the delta law) and draws its OWN delta at
//   PIL-measured geometry below. Frame slide_041.jpg is ground truth for every element.
//
// Measurement provenance (PIL, 960x540 px, 1px = 1pt = 1/72 in):
//   panel rect      red border x 70..891, y 120..433 (left 70-71, right 890-891,
//                   top 120-121, bottom 433); interior WHITE (254,255,253)
//   title ink       x 296..667, y 81..105 (cap ~25px -> TNR Bold 37.5, C00000, center 481.5)
//   'Original image'  x 99..277, y 138..157 (Comic Sans MS ~20, deck precedent slide_030)
//   photo+5x5 grid  x 99..271, y 158..289 -> BAKED crop leftgrid041.png (parent pattern:
//                   slide_035 banks leftgrid035.png the same way)
//   'Convolutional filter 1' x 80..324, y 288..309 (Comic Sans MS ~20)
//   filter 3x3      x 143..221, y 319..381 (cells 26.33x21), fill FFFF00, borders
//                   8BD33F (parent filterTable convention), digits Verdana Bold 14,
//                   row bands 324-333/346-355/367-376 -> 1 0 1 / 0 1 0 / 1 0 1
//   'a=1,' / 'b=1'  red x 239..264, y 334..359 (Arial bold ~11, lineSpacing 14)
//   notation L1     'Image:  I (x,y)' x 92..212, cap band 390..402 (Arial Bold 17;
//                   'Image:' black, 'I (x,y)' red C00000)
//   notation L2     'Filter:  h (-a:a , -b:b) (odd dimension)' x 92..404, cap 415..427
//                   ('Filter:' black, rest red; '(odd dimension)' red italic)
//   convolving grid x 385..630, y 160..350 (cells 49x38; yellow 3x3 TL, green rest,
//                   x1/x0 multipliers) + its hand-style label y 135..159 -> BAKED crop
//                   convgrid041.png (label+grid interleave rows 155..161 with the arrow:
//                   certified parent bakes this exact content family in panelcontent035)
//   result grid     tan-bordered 3x3 x 652..822, y 159..278, olive 9C9C8E '4' cell
//                   x 652..722 y 159..203 + black curved arrow x 560..652 y 136..164 +
//                   'Result' label x 707..781 y 136..150 -> BAKED crop result041.png
//   'Inner product' red hand label y 339..353 x 698..848 + hand curly brace (stem
//                   x~725 y 354..366, arms to x 698..826 y ~383) -> red-ink-only
//                   transparent overlay innerprod041.png (black equation glyphs in the
//                   same band are NOT baked — the equation is mathtext-rendered)
//   equation        ink x 459..841, y 364..418 (baseline 405.5); mathtext
//                   render_eq.py 19.5pt -> eq041.png 3186x485 @600dpi (w_in 5.31),
//                   placed at ink-left 459/72 - 8/600 pad, ink-top 364/72 - 8/600 pad
//   instruction box x 78..876, y 445..511 (border 9797B2 ~1.5pt, fill WHITE — same
//                   border color as certified parent captionBox)
//   instr line 1    'Scan the original image using the 3x3 filter' x 89..452,
//                   cap 459..471 (TNR 19: cap 12.6px measured 12-13) navy 1F3864, upright
//                   (stem/envelope test: no slant)
//   instr line 2    'Move the filter ONE pixel  (Right, Left, Up, Down) and Re-Calculate'
//                   x 89..682, cap 486..498, same style (double space after 'pixel' kept)
//   NOT drawn       bottom letterbox strip y 518..539 (video-player artifact; certified
//                   precedent slide_034/slide_017: letterbox deliberately NOT recreated);
//                   3x2px dark speck at (445..447, 80..81) on the title (cursor remnant)
//   x=58 tall red line (y 45..516): present in parent frame 35 too -> original deck's own
//                   chrome border, OVERRIDDEN by the playlist house chrome (founder
//                   directive 2026-10-11); NOT drawn.

const pptxgen = require("pptxgenjs");
const { renderBase } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_035.js"
);

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

// ---- palette (measured) ----
const RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const BOX_BORDER = "9797B2";
const NAVY = "1F3864";
const FILTER_BORDER = "8BD33F";

const px = (v) => v / 72;

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// ---- chrome via the certified parent component (numeral = this frame's own number) ----
renderBase(pptx, slide, { numeral: "41", only: [] });

// ---- main framed panel (content ground truth) ----
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(120), w: px(822), h: px(314),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// ---- title ----
slide.addText("The Convolution Process", {
  x: px(481.5) - 4, y: px(93) - 0.35, w: 8, h: 0.7,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Times New Roman", fontSize: 35, bold: true, color: RED,
});

// ---- left column ----
slide.addText("Original image", {
  x: px(98), y: px(145) - 0.2, w: px(220), h: 0.4,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Comic Sans MS", fontSize: 20, color: BLACK,
});
slide.addImage({
  path: `${ASSETS}/leftgrid041.png`,
  x: px(99), y: px(158), w: 173 / 72, h: 132 / 72,
});
slide.addText("Convolutional filter 1", {
  x: px(79), y: px(298.5) - 0.2, w: px(260), h: 0.4,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Comic Sans MS", fontSize: 20, color: BLACK,
});
slide.addTable(
  [
    [{ text: "1" }, { text: "0" }, { text: "1" }],
    [{ text: "0" }, { text: "1" }, { text: "0" }],
    [{ text: "1" }, { text: "0" }, { text: "1" }],
  ],
  {
    x: px(143), y: px(319), w: px(79), h: px(63),
    colW: [px(26.33), px(26.33), px(26.34)],
    rowH: [px(21), px(21), px(21)],
    fill: { color: "FFFF00" },
    border: { type: "solid", pt: 1.5, color: FILTER_BORDER },
    align: "center", valign: "middle", margin: 0,
    fontFace: "Verdana", fontSize: 14, bold: true, color: BLACK,
  }
);
slide.addText(
  [
    { text: "a=1,", options: { breakLine: true } },
    { text: "b=1" },
  ],
  {
    x: px(239), y: px(346) - 0.25, w: px(44), h: 0.5,
    align: "left", valign: "middle", margin: 0, lineSpacing: 14,
    fontFace: "Arial", fontSize: 14, bold: true, color: RED,
  }
);

// ---- notation lines ----
// Red math spans are Times New Roman Bold (probe-calibrated: Arial Bold punctuation is
// ~34% wider than the original's red math; TNR Bold 20 fits both spans within tol).
slide.addText(
  [
    { text: "Image:  ", options: { color: BLACK, fontFace: "Arial", fontSize: 19.5 } },
    { text: "I (x,y)", options: { color: RED, fontFace: "Times New Roman", fontSize: 18.5 } },
  ],
  {
     x: px(91), y: px(393) - 0.2, w: px(330), h: 0.4,
    align: "left", valign: "middle", margin: 0,
    fontSize: 19.5, bold: true,
  }
);
slide.addText(
  [
    { text: "Filter:  ", options: { color: BLACK, fontFace: "Arial", fontSize: 19.5 } },
    { text: "h (-a:a , -b:b)", options: { color: RED, fontFace: "Times New Roman", fontSize: 20.5 } },
    { text: " (odd dimension)", options: { color: RED, fontFace: "Times New Roman", fontSize: 19.5, italic: true } },
  ],
  {
    x: px(91), y: px(416) - 0.2, w: px(390), h: 0.4,
    align: "left", valign: "middle", margin: 0,
    fontSize: 19.5, bold: true,
  }
);

// ---- center + right baked content (label+grid, label+arrow+result grid) ----
slide.addImage({
  path: `${ASSETS}/result041.png`,
  x: px(548), y: px(131), w: 315 / 72, h: 155 / 72,
});
slide.addImage({
  path: `${ASSETS}/convgrid041.png`,
  x: px(381), y: px(131), w: 256 / 72, h: 226 / 72,
});

// ---- 'Inner product' hand label + brace (red ink overlay, transparent) ----
slide.addImage({
  path: `${ASSETS}/innerprod041.png`,
  x: px(694), y: px(334), w: 193 / 72, h: 50 / 72,
});

// ---- equation (professional 2D mathtext, exact-size embed) ----
slide.addImage({
  path: `${ASSETS}/eq041.png`,
  x: 459 / 72 - 8 / 600, y: 364 / 72 - 8 / 600, w: 5.31, h: 0.80833,
});

// ---- instruction box + lines ----
slide.addShape(pptx.ShapeType.rect, {
  x: px(78), y: px(445), w: px(799), h: px(66),
  fill: { color: WHITE }, line: { color: BOX_BORDER, width: 1.5 },
});
slide.addText("Scan the original image using the 3x3 filter", {
  x: px(88), y: px(465) - 0.2, w: px(420), h: 0.4,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Times New Roman", fontSize: 21, color: NAVY,
});
slide.addText("Move the filter ONE pixel  (Right, Left, Up, Down) and Re-Calculate", {
  x: px(88), y: px(492) - 0.2, w: px(640), h: 0.4,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Times New Roman", fontSize: 21.35, color: NAVY,
});

pptx.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_041_recreated.pptx" })
  .then(() => console.log("WROTE slide_041_recreated.pptx"));
