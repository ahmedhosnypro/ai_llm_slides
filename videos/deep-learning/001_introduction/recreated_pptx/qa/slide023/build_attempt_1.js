// slide_023.js — 001_introduction slide 23 "Visualization of Single Layer Perceptron"
// (multi-class perceptron: m Σ-neurons, one per class) — Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_023.jpg (960x540, 1px = 1pt = 1/72 in).
//   This frame is one of the founder's SWAPPED frames (new 23 <- old 28; slide_023.jpg IS
//   ground truth, no second-guessing).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn, NEVER ml-intro values. Badge numeral = 23 (file number;
//   assumption PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).
//
// Measured constants (frame px):
//   black bar       x 38..921, y 519..539 (drawn to 537.5 so the chrome bottom stroke stays
//                   visible — certified slide_002/005/021 precedent, 2-frame-px deviation)
//   eq box          x 52..473, y 99..238, fill ~FFF8EC (modal 255,248,236), thin red border
//   eq lines        3 lines, baselines y 123.5 / 171.5 / 219.5 (pitch 48), ink left x 78;
//                   glyphs BLACK (d, W, w, x, =, +, parens), RED accents: the (X) of d_j(X)
//                   and the b_j*1 tail (measured cores (120,32,56)-family). Spec's wholesale
//                   "red equations" overridden per deck pixel law (71% of ink is neutral).
//                   W underlined (1px black line under W+sub, measured y177 on line 2).
//   tan box         x 137..326, y 360..403, fill E0E0C8 (modal 224,224,200); text
//                   "Multi-Class" / "Classification" bold-italic 8B0000, baselines 378/397
//   network panel   x 423..897, y 152..500, white, thin dark-blue border (measured line
//                   (142,140,162) = JPEG-desaturated blue family -> 333399 1pt)
//   input labels    x-left 433: x1 b290, x2 b312, x3 b334, "..." b358, "..." b380, xn b402,
//                   "1" RED b425 (bias input red — same family reading as certified-adjacent
//                   slide 022 spec: "1 (red, bias input)")
//   Sigma circles   d35 at x663.5, y 169.5 / 302.5 / 438.5 (centers 681, 187/320/455.5);
//                   fill CCFFFF, ring 339999, black Sigma glyph ~14x18px (Arial 25pt)
//   ellipsis        3 hollow circles d13.5, cx 680.5, cy 356.5/384/411.5 (between S2 and S3)
//   fan lines       21 straight lines, inputs (x450) -> circle left edge (x663), colored per
//                   bundle: red FF0000 (to S1), blue 0000FF (to S2), green 008000 (to S3)
//   weight labels   15 italic labels ~9pt at measured positions (see WEIGHTS below)
//   red arrows      S -> activation box (699,cy)->(720,cy); box -> output (768,cy+1)->(795,cy+10.5)
//   act boxes       x721 y170.5/303.5/439.5, w46 h31, fill F8E0F8, border 993366 (measured
//                   dark-rose core (141,28,72)), blue 0000CC step glyph (3 rects)
//   output texts    x804, 11pt bold black, 3 lines each: ">0 Class I" / "<0 Not Class" / "I"
//                   (the original's box wraps the trailing roman numeral — reproduced
//                   explicitly), baselines 186/200/214 (out2 316/330/344, out3 453/467/481)
//   red rule x58    OMITTED — constant VIDEO-LEVEL chrome present on every frame of this
//                   lecture (slide_021 forensics: red@x58 on slides 1/2/5/21/22/49); certified
//                   precedent (slide_002, slide_005 — judge-PASS) omits it; the house chrome
//                   panel stands in for the frame element.
//   cursor artifact black tick at (414..419, 210..219) OMITTED per judge ground rule (c).
//
// Equations: professional 2D format per founder directive 2026-10-09 — matplotlib mathtext
//   -> 600dpi transparent PNGs (scripts/render_eq.py, certified mechanism) -> addImage at
//   exact size (w = w_in from sidecar, NEVER rescaled), baseline-law vertical placement
//   (y_img = baseline - baseline_frac*h). 4 fragments per line (black d_j( / red X /
//   black ) = W_j^T X = ...+ / red b_j*1), flow-placed with 3pt gaps; fontsize 13.6pt
//   metric-solved: line flow lands at x78..438 (measured 78..439).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_023_recreated.pptx";
const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

// ---- palette (measured) ----
const TITLE_RED = "C00000";
const TITLE_BLUE = "0000CC";
const BLACK = "000000";
const WHITE = "FFFFFF";
const EQ_BOX_FILL = "FFF8EC";
const TAN_FILL = "E0E0C8";
const TAN_TEXT = "8B0000";
const PANEL_BORDER = "333399";
const RED = "FF0000";
const BLUE = "0000FF";
const GREEN = "008000";
const CYAN_FILL = "CCFFFF";
const TEAL = "339999";
const ACT_FILL = "F8E0F8";
const ACT_BORDER = "993366";
const GLYPH_BLUE = "0000CC";

const px = (v) => v / 72;

// ---- equation sidecars (generated at 13.6pt; w/h in inches, baseline_frac) ----
const EQ = {
  F1_1: { w: 0.30333, h: 0.19833, bf: 0.78992 },
  F2_1: { w: 0.18833, h: 0.16333, bf: 0.91837 },
  F3_1: { w: 3.9,     h: 0.285,   bf: 0.69006 },
  F4_1: { w: 0.5,     h: 0.19833, bf: 0.78992 },
  F1_2: { w: 0.30333, h: 0.19833, bf: 0.78992 },
  F2_2: { w: 0.18833, h: 0.16333, bf: 0.91837 },
  F3_2: { w: 3.9,     h: 0.285,   bf: 0.69006 },
  F4_2: { w: 0.5,     h: 0.19833, bf: 0.78992 },
  F1_m: { w: 0.34833, h: 0.19833, bf: 0.78992 },
  F2_m: { w: 0.18833, h: 0.16333, bf: 0.91837 },
  F3_m: { w: 4.08,    h: 0.285,   bf: 0.69006 },
  F4_m: { w: 0.54333, h: 0.19833, bf: 0.78992 },
};
const EQ_BASELINES = [123.5, 171.5, 219.5]; // frame px
const EQ_LINE_TAGS = ["1", "2", "m"];
const EQ_GAP = 3; // pt between fragments (flow)

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 23)
drawHouseChrome(pres, slide, { numeral: "23" });

// Black footer bar (over the panel; chrome bottom stroke kept visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(884), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Title — two-color, Arial Bold 30.3pt (advance-solved: 578px @30.3 vs measured 579),
// ink center x441.5, baseline y81.5
slide.addText(
  [
    { text: "Visualization of Single ", options: { color: TITLE_RED } },
    { text: "Layer", options: { color: TITLE_BLUE } },
    { text: " Perceptron", options: { color: TITLE_RED } },
  ],
  {
    x: px(441.5 - 360), y: px(36.1), w: 10, h: 1.0,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 30.3, bold: true, lineSpacing: 36,
  }
);

// Tan box "Multi-Class Classification" (bold italic dark red, 2 centered lines)
slide.addShape(pres.ShapeType.rect, {
  x: px(137), y: px(360), w: px(190), h: px(44),
  fill: { color: TAN_FILL }, line: { color: TITLE_RED, width: 0.75 },
});
[["Multi-Class", 378], ["Classification", 397]].forEach(([text, b]) => {
  slide.addText(text, {
    x: px(231.5 - 60), y: px(b - 16.41), w: px(120), h: 0.35,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 12.5, bold: true, italic: true,
    color: TAN_TEXT, lineSpacing: 15,
  });
});

// Network panel (white, thin dark-blue border)
slide.addShape(pres.ShapeType.rect, {
  x: px(423), y: px(152), w: px(474), h: px(348),
  fill: { color: WHITE }, line: { color: PANEL_BORDER, width: 1 },
});

// ---- diagram (z-order: fan lines first, then nodes/labels) ----
const IN_Y = [286.5, 308, 330, 356, 378, 398.5, 420]; // input label centers
const S_CX = 681, S_CY = [187, 320, 455.5];           // Sigma circle centers
const BUNDLE_COLOR = [RED, BLUE, GREEN];

// 21 fan lines (inputs -> circle left edge x663). flipV when the input is BELOW the
// circle: pptxgenjs draws the line bbox top-left -> bottom-right, so an upward line
// must be flipped or it renders mirrored (converging at the input column instead of
// the circle) — caught by closed-loop render inspection, attempt 1.
// endArrowType: the original shows small filled arrowheads where each bundle terminates
// at its Sigma circle's left edge (crop-compare finding, remediated before judging).
for (let b = 0; b < 3; b++) {
  for (const iy of IN_Y) {
    const up = iy > S_CY[b];
    slide.addShape(pres.ShapeType.line, {
      x: px(450), y: px(Math.min(iy, S_CY[b])), w: px(213), h: px(Math.abs(S_CY[b] - iy)),
      flipV: up,
      line: { color: BUNDLE_COLOR[b], width: 1, endArrowType: "triangle" },
    });
  }
}

// 3 Sigma circles + black Sigma glyphs
for (let b = 0; b < 3; b++) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(663.5), y: px(S_CY[b] - 17.5), w: px(35), h: px(35),
    fill: { color: CYAN_FILL }, line: { color: TEAL, width: 1.25 },
  });
  slide.addText("\u03A3", {
    x: px(663.5), y: px(S_CY[b] - 17.5), w: px(35), h: px(35),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 25, color: BLACK,
  });
}

// 3 hollow ellipsis circles between S2 and S3
for (const cy of [356.5, 384, 411.5]) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(680.5 - 6.75), y: px(cy - 6.75), w: px(13.5), h: px(13.5),
    fill: { color: WHITE }, line: { color: TEAL, width: 0.75 },
  });
}

// Weight labels (15, italic ~9pt, bundle colors, measured baselines/lefts).
// Real subscript runs (same mechanism as the input labels — no Unicode subscript glyphs).
const W = (main, sub) => [
  { text: main, options: { italic: true, subscript: false } },
  { text: sub, options: { italic: true, subscript: true } },
];
const WEIGHTS = [
  // [runs, left_px, baseline_px, color]
  [W("w", "11"), 483, 261.5, TITLE_RED],
  [W("w", "12"), 481, 280.5, TITLE_RED],
  [W("w", "13"), 482, 300.5, TITLE_RED],
  [W("w", "1n"), 483, 352.5, TITLE_RED],
  [W("b", "1"),  482, 393.5, TITLE_RED],
  [W("w", "21"), 570, 302.5, TITLE_BLUE],
  [W("w", "22"), 548, 313.5, TITLE_BLUE],
  [W("w", "23"), 555, 335.5, TITLE_BLUE],
  [W("w", "2n"), 555, 354.5, TITLE_BLUE],
  [W("b", "2"),  579, 366.5, TITLE_BLUE],
  [W("w", "m1"), 579, 389.5, GREEN],
  [W("w", "m2"), 567, 404.5, GREEN],
  [W("w", "m3"), 567, 419.5, GREEN],
  [W("w", "mn"), 560, 434.5, GREEN],
  [W("b", "m"),  572, 451.5, GREEN],
];
for (const [runs, xl, b, color] of WEIGHTS) {
  slide.addText(runs, {
    x: px(xl - 1), y: px(b - 13.45), w: px(26), h: 0.3,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 9, color, lineSpacing: 11,
  });
}

// Input labels (x1..xn black italic with real subscript runs; bias "1" red 14pt)
const INPUTS = [
  { runs: [["x", "1"]], b: 290, color: BLACK, size: 12 },
  { runs: [["x", "2"]], b: 312, color: BLACK, size: 12 },
  { runs: [["x", "3"]], b: 334, color: BLACK, size: 12 },
  { runs: [["...", null]], b: 358, color: BLACK, size: 12 },
  { runs: [["...", null]], b: 380, color: BLACK, size: 12 },
  { runs: [["x", "n"]], b: 402, color: BLACK, size: 12 },
  { runs: [["1", null]], b: 425, color: TITLE_RED, size: 14 },
];
for (const item of INPUTS) {
  const [main, sub] = item.runs[0];
  const runList = sub === null
    ? [{ text: main, options: { italic: main !== "1" } }]
    : [
        { text: main, options: { italic: true, subscript: false } },
        { text: sub, options: { italic: true, subscript: true } },
      ];
  const off = (25.2 - 15) / 2 + 0.9052 * item.size; // baseline offset in the h=0.35in box
  slide.addText(runList, {
    x: px(431.5), y: px(item.b - off), w: px(20), h: 0.35,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: item.size, color: item.color, lineSpacing: 15,
  });
}

// Per-row: red arrow S->box, activation box + blue step glyph, exit arrow, output text
for (let b = 0; b < 3; b++) {
  const cy = S_CY[b];
  // red arrow Sigma -> activation box
  slide.addShape(pres.ShapeType.line, {
    x: px(699), y: px(cy), w: px(21), h: 0,
    line: { color: RED, width: 1.5, endArrowType: "triangle" },
  });
  // activation box (pink fill, dark-rose border)
  const bt = cy - 15.5; // box top (cy 187 -> 171.5 ≈ measured 170.5)
  slide.addShape(pres.ShapeType.rect, {
    x: px(721), y: px(bt), w: px(46), h: px(31),
    fill: { color: ACT_FILL }, line: { color: ACT_BORDER, width: 1 },
  });
  // blue step-function glyph: vertical bar + top arm (right) + bottom arm (left)
  slide.addShape(pres.ShapeType.rect, { x: px(744), y: px(bt + 11.5), w: px(2.5), h: px(11), fill: { color: GLYPH_BLUE }, line: { color: GLYPH_BLUE, width: 0 } });
  slide.addShape(pres.ShapeType.rect, { x: px(744), y: px(bt + 7), w: px(16), h: px(3), fill: { color: GLYPH_BLUE }, line: { color: GLYPH_BLUE, width: 0 } });
  slide.addShape(pres.ShapeType.rect, { x: px(732), y: px(bt + 23), w: px(15), h: px(3), fill: { color: GLYPH_BLUE }, line: { color: GLYPH_BLUE, width: 0 } });
  // red exit arrow -> output text
  slide.addShape(pres.ShapeType.line, {
    x: px(768), y: px(cy + 1), w: px(27), h: px(9.5),
    line: { color: RED, width: 1.5, endArrowType: "triangle" },
  });
  // output text (3 explicit lines — the trailing roman numeral wraps in the original)
  const outs = [
    [">0 Class I", "<0 Not Class", "I", 186],
    [">0 Class II", "<0 Not Class", "II", 316],
    [">0 Class m", "<0 Not Class", "m", 453],
  ];
  const [l1, l2, l3, b1] = outs[b];
  slide.addText(
    [
      { text: l1, options: { breakLine: true } },
      { text: l2, options: { breakLine: true } },
      { text: l3, options: {} },
    ],
    {
      x: px(804), y: px(b1 - 10.36), w: 1.2, h: 0.65,
      align: "left", valign: "top", margin: 0,
      fontFace: "Arial", fontSize: 11, bold: true, color: BLACK, lineSpacing: 14,
    }
  );
}

// Equation box (cream, thin red border)
slide.addShape(pres.ShapeType.rect, {
  x: px(52), y: px(99), w: px(421), h: px(139),
  fill: { color: EQ_BOX_FILL }, line: { color: TITLE_RED, width: 1 },
});

// Equation fragments — 4 per line, flow placement, baseline law
for (let i = 0; i < 3; i++) {
  const tag = EQ_LINE_TAGS[i];
  const baseline = EQ_BASELINES[i];
  let xpt = 78;
  for (const f of ["F1", "F2", "F3", "F4"]) {
    const s = EQ[`${f}_${tag}`];
    const ypt = baseline - s.bf * (s.h * 72);
    slide.addImage({
      path: `${ASSETS}/eq_${f}_${tag}.png`,
      x: px(xpt), y: px(ypt), w: s.w, h: s.h,
    });
    xpt += s.w * 72 + EQ_GAP;
  }
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
