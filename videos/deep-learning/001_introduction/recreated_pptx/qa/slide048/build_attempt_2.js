// slide_048.js — 001_introduction slide 48 "Standard Neural Network (NN) vs Convolutional
// Neural Network (ConvNet/CNN)" — Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_048.jpg (960x540, 1px = 1pt = 1/72 in).
//   Measurement passes: scratch/slide048/measure_1..15.py (banked).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 48 (slide file number; 001_introduction
//   originals carry no printed numbers — ASSUMPTION PENDING FOUNDER VETO, video AGENTS.md
//   2026-10-12; rebuild drops the badge ONLY via shared_patterns if vetoed).
//
// Measured structure (frame px):
//   content frame   white-filled red rect x58..894, y135.5..448.5 (borders ~2-3px), C00000;
//                   inner-left vertical red line x65 y136..448 (double-line left border detail)
//   title           2 lines Arial Bold ~29.5pt C00000, ink centers x481.5/482 (canonical panel
//                   center 480), cap-tops 63/98, baselines 84/119 (pitch 35) — line1 y63..89
//                   x130..833, line2 y96..123 x258..706
//   NN label box    square white rect x242..379 y155..182, blue 0000AA border (certified
//                   slide_002/049 sibling value; measured core #1D0B81 chroma-washed),
//                   text 'Neural Network' COMIC SANS MS 14pt #333333 (vision-certified crop
//                   analysis: dark charcoal comic-style, square corners) y164..174 x251..365
//   meme photo      CROP from original x247..361 y189..254 -> s048_meme.png (114x65), captions baked
//   flatten tag     yellow FFFF00 rect x387..422 y157..183; text 'Flatten'/'(1-D)' bold italic
//                   ~9pt C00000 (vision: brick/dark red on yellow), 2 lines, centers y163/176.5
//   dot column      7 dots d6 cx405.5, cys 195.5+8.33k (PIL lum profile; vision crop read 6,
//                   PIL found the 7th gray-blue blob at y245.5):
//                   black/green/red/red/blue/yellow/gray-blue (PIL cores; vision colors for hues)
//   NN arrows       black thin, y221: photo->dots x366..396, dots->block1 x440..447, gap arrows
//                   x489..496/536..544/584..590/631..638/678..685 (measured ink clusters)
//   NN blocks       6 orange 3-D blocks y186..255 (h70): fronts w24 D4821E + right side w3 9C5A12
//                   (measured (475,220)=(164,97,6)), lefts x450/497/544/591/639/686 (pitch ~47);
//                   white vert270 text 'Layer 1'..'Layer 5','Loss' ~10pt (text band y205..240)
//   NN overlines    FC/FC/FC/FC + O/P, Arial bold 13pt C00000, cap band y168..177 (baseline 177),
//                   centered over block centers 463/509.5/557/604/651.5; none over Loss
//   divider         red dash-dot line y269 x66..893 (dash ~12px, dot, pitch ~25 -> 'dashDot')
//   CNN label box   square white rect x242..480 y278..305, text 'Convolutional Neural Network'
//                   Comic Sans MS 14pt #333333, y286..296 x249..471
//   siamese photo   CROP x123..228 y313..431 -> s048_siamese.png (105x118) — skewed parallelogram baked
//   CNN slab chain  CROP x228..693 y312..440 -> s048_cnn_chain.png (465x128): the six 3-D
//                   parallelogram slabs (front D4821E + side 9C5A12 + shaded top wedges, measured
//                   wedge cores (178..203,98..131,6..47)) with their baked white vertical 2-line
//                   labels, the two red 'Conv' overlines (x232..249/x470..502, y318..328, cores
//                   ~#7A1220 = C00000 wash) and the blue 'Non Linearity' stacks (NL1 x270..319,
//                   NL2 x593..642, y416..439, cores #0A0080) — complex 3-D artwork cropped
//                   whole per the certified slide_029 precedent (meme+cards+closeup crops with
//                   baked text/arrows). Gap arrows s6->block7 at x728..732 are OUTSIDE the crop.
//   CNN blocks 7-9  upright 3-D rects x735/782/829, y333..403 (h70, w26 = front 23 + side 3),
//                   white vert270 'Layer 5','Layer 6','Loss'; FC/O/P Arial bold 13pt C00000
//                   baseline 324 over centers 747.5/795; black arrows b7->b8 (776..780),
//                   b8->b9 (823..827) y~368, s6->b7 x724..732 y368
//   bottom arrow    red C00000, shaft y462.5 x169..831 (rows 462-463), head y456..465 tip x831
//   caption         'Deep Learning (too Many Layers)' Arial bold italic 13pt C00000,
//                   x354..~596 (center ~475), cap band y468..477 (baseline ~477)
//   EXCLUDED per spec recreation_brief step 25 + judge ground rule (c): gray '+' annotation
//   mark (~x710,y~475) and the black video-player strip y519..539 x38..921.
//
// LAWS honored: playlist chrome via shared module; verbatim text (incl. double spaces
// 'Neural  Network'/'vs  Convolutional' and odd capitalization 'too Many'); margin:0 +
// explicit fontFace + explicit lineSpacing everywhere; no '#' in hex; baseline placement via
// the validated LO model baseline = top + (box_h_px - lineSpacing)/2 + 0.905*size (slide_049).

const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_048_recreated.pptx";

// ---- palette (measured / spec) ----
const C = {
  red: "C00000", white: "FFFFFF", black: "000000",
  blockFront: "D4821E", blockSide: "9C5A12",
  boxBorder: "0000AA", labelText: "333333",
  yellow: "FFFF00",
  dotBlack: "000000", dotGreen: "00A651", dotRed: "CC2222",
  dotBlue: "2244CC", dotYellow: "FFE000", dotGray: "96A2B8",
};
const SANS = "Arial";
const COMIC = "Comic Sans MS";

const px = (v) => v / 72;
const ASC = 0.905; // Arial ascent fraction (LO baseline model)

// single-line box: top for a target baseline (box h in px, lineSpacing in pt)
const topFor = (baseline, size, boxHpx, ls) => baseline - (boxHpx - ls) / 2 - ASC * size;

const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge numeral 48)
drawHouseChrome(pres, slide, { numeral: "48" });

// ---- 2. content frame: white-filled red rect x58..894 y135.5..448.5 (stroke-center)
slide.addShape(pres.ShapeType.rect, {
  x: px(58), y: px(135.5), w: px(836), h: px(313),
  fill: { color: C.white }, line: { color: C.red, width: 2 },
});
// inner-left vertical line x65 y136..448 (double-line left border detail)
slide.addShape(pres.ShapeType.line, {
  x: px(65), y: px(136), w: 0, h: px(312),
  line: { color: C.red, width: 1.5 },
});

// ---- 3. title (two single-line boxes, baselines 84 / 119, box h 0.55in = 39.6px, LS 35)
// closed-loop: 29.5pt rendered 3% narrow (line1 682 vs orig 703, line2 433 vs 448) -> 30.5pt
const T_H = 39.6, T_LS = 35, T_SIZE = 30.5;
slide.addText("Standard Neural  Network (NN) vs  Convolutional", {
  x: px(121), y: px(topFor(84, T_SIZE, T_H, T_LS)), w: px(720), h: 0.55,
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: T_SIZE, bold: true, color: C.red, lineSpacing: T_LS,
});
slide.addText("Neural Network (ConvNet/CNN)", {
  x: px(121), y: px(topFor(119, T_SIZE, T_H, T_LS)), w: px(720), h: 0.55,
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: T_SIZE, bold: true, color: C.red, lineSpacing: T_LS,
});

// ---- 4. NN label box (square white rect, blue border) + comic text
slide.addShape(pres.ShapeType.rect, {
  x: px(242), y: px(155), w: px(137), h: px(27),
  fill: { color: C.white }, line: { color: C.boxBorder, width: 1.75 },
});
slide.addText("Neural Network", {
  x: px(242), y: px(155), w: px(137), h: px(27),
  align: "center", valign: "middle", margin: 0,
  fontFace: COMIC, fontSize: 16, color: C.labelText, lineSpacing: 18,
});

// ---- 5. meme photo (verbatim crop, captions baked)
slide.addImage({ path: `${ASSETS}/s048_meme.png`, x: px(247), y: px(189), w: 114 / 72, h: 65 / 72 });

// ---- 6. flatten tag (yellow rect + 2 lines bold italic red)
slide.addShape(pres.ShapeType.rect, {
  x: px(387), y: px(157), w: px(36), h: px(27),
  fill: { color: C.yellow }, line: { color: C.yellow, width: 0.5 },
});
slide.addText(
  [
    { text: "Flatten", options: { breakLine: true } },
    { text: "(1-D)", options: {} },
  ],
  {
    x: px(387), y: px(158), w: px(36), h: px(25),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 9, bold: true, italic: true, color: C.red, lineSpacing: 13.5,
  }
);

// ---- 7. dot column (7 dots, d6, cx 405.5)
const DOTS = [
  { cy: 195.5, c: C.dotBlack }, { cy: 204.5, c: C.dotGreen }, { cy: 212.5, c: C.dotRed },
  { cy: 220.5, c: C.dotRed }, { cy: 229.5, c: C.dotBlue }, { cy: 237.5, c: C.dotYellow },
  { cy: 245.5, c: C.dotGray },
];
for (const d of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(405.5 - 3), y: px(d.cy - 3), w: px(6), h: px(6),
    fill: { color: d.c }, line: { color: d.c, width: 0 },
  });
}

// ---- 8. black arrows (thin, triangle heads)
function arrow(x0, x1, y, wpt) {
  slide.addShape(pres.ShapeType.line, {
    x: px(x0), y: px(y), w: px(x1 - x0), h: 0,
    line: { color: C.black, width: wpt, endArrowType: "triangle" },
  });
}
arrow(366, 397, 221, 1.25);   // meme photo -> dots
arrow(440, 449, 221, 1);      // dots -> NN block 1
arrow(489, 496, 221, 1);      // NN gap arrows
arrow(536, 544, 221, 1);
arrow(584, 590, 221, 1);
arrow(631, 638, 221, 1);
arrow(678, 685, 221, 1);
arrow(724, 732, 368, 1);      // slab 6 -> CNN block 7
arrow(769, 780, 368, 1);      // CNN block 7 -> 8
arrow(816, 827, 368, 1);      // CNN block 8 -> 9

// ---- 9. NN blocks (6 orange 3-D blocks, white vertical text)
const NN_X = [450, 497, 544, 591, 639, 686];
const NN_TEXT = ["Layer 1", "Layer 2", "Layer 3", "Layer 4", "Layer 5", "Loss"];
for (let i = 0; i < 6; i++) {
  const x0 = NN_X[i];
  slide.addShape(pres.ShapeType.rect, { // right 3-D side
    x: px(x0 + 23.5), y: px(186), w: px(3), h: px(70),
    fill: { color: C.blockSide }, line: { color: C.blockSide, width: 0 },
  });
  slide.addShape(pres.ShapeType.rect, { // front face
    x: px(x0), y: px(186), w: px(23.5), h: px(70),
    fill: { color: C.blockFront }, line: { color: C.blockFront, width: 0 },
  });
  slide.addText(NN_TEXT[i], {
    x: px(x0), y: px(186), w: px(23.5), h: px(70),
    align: "center", valign: "middle", margin: 0, vert: "vert270",
    fontFace: SANS, fontSize: 10, color: C.white, lineSpacing: 12,
  });
}

// ---- 10. NN overlines FC/FC/FC/FC + O/P (Arial bold 13pt, baseline 177, box h 21.6px LS 16)
const OL_H = 21.6, OL_LS = 16;
const NN_OL = [
  { t: "FC", cx: 463 }, { t: "FC", cx: 509.5 }, { t: "FC", cx: 557 },
  { t: "FC", cx: 604 }, { t: "O/P", cx: 651.5 },
];
for (const o of NN_OL) {
  slide.addText(o.t, {
    x: px(o.cx - 30), y: px(topFor(177, 13.5, OL_H, OL_LS)), w: px(60), h: 0.3,
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 13.5, bold: true, color: C.red, lineSpacing: OL_LS,
  });
}

// ---- 11. divider (red dash-dot, y269, x66..893)
slide.addShape(pres.ShapeType.line, {
  x: px(66), y: px(269), w: px(827), h: 0,
  line: { color: C.red, width: 1.5, dashType: "dashDot" },
});

// ---- 12. CNN label box + comic text
slide.addShape(pres.ShapeType.rect, {
  x: px(242), y: px(278), w: px(238), h: px(27),
  fill: { color: C.white }, line: { color: C.boxBorder, width: 1.75 },
});
slide.addText("Convolutional Neural Network", {
  x: px(242), y: px(278), w: px(238), h: px(27),
  align: "center", valign: "middle", margin: 0,
  fontFace: COMIC, fontSize: 16, color: C.labelText, lineSpacing: 18,
});

// ---- 13. siamese photo (verbatim crop; parallelogram skew baked)
slide.addImage({ path: `${ASSETS}/s048_siamese.png`, x: px(123), y: px(313), w: 105 / 72, h: 118 / 72 });

// ---- 14. CNN slab chain (verbatim crop: 6 slabs + baked labels + Conv overlines + Non Linearity + gap arrows)
slide.addImage({ path: `${ASSETS}/s048_cnn_chain.png`, x: px(228), y: px(312), w: 465 / 72, h: 128 / 72 });

// ---- 15. CNN blocks 7-9 (upright 3-D rects, white vertical text)
const CNN_X = [735, 782, 829];
const CNN_TEXT = ["Layer 5", "Layer 6", "Loss"];
for (let i = 0; i < 3; i++) {
  const x0 = CNN_X[i];
  slide.addShape(pres.ShapeType.rect, {
    x: px(x0 + 23), y: px(333), w: px(3), h: px(70),
    fill: { color: C.blockSide }, line: { color: C.blockSide, width: 0 },
  });
  slide.addShape(pres.ShapeType.rect, {
    x: px(x0), y: px(333), w: px(23), h: px(70),
    fill: { color: C.blockFront }, line: { color: C.blockFront, width: 0 },
  });
  slide.addText(CNN_TEXT[i], {
    x: px(x0), y: px(333), w: px(23), h: px(70),
    align: "center", valign: "middle", margin: 0, vert: "vert270",
    fontFace: SANS, fontSize: 10, color: C.white, lineSpacing: 12,
  });
}

// ---- 16. CNN FC / O/P overlines (baseline 324)
const CNN_OL = [{ t: "FC", cx: 747.5 }, { t: "O/P", cx: 795 }];
for (const o of CNN_OL) {
  slide.addText(o.t, {
    x: px(o.cx - 30), y: px(topFor(324, 13.5, OL_H, OL_LS)), w: px(60), h: 0.3,
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 13.5, bold: true, color: C.red, lineSpacing: OL_LS,
  });
}

// ---- 17. long red arrow below the frame (shaft y462.5, x169..831, head tip x831)
slide.addShape(pres.ShapeType.line, {
  x: px(169), y: px(462.5), w: px(662), h: 0,
  line: { color: C.red, width: 1.5, endArrowType: "triangle" },
});

// ---- 18. caption (bold italic red, baseline ~477, center 475)
slide.addText("Deep Learning (too Many Layers)", {
  x: px(325), y: px(462), w: px(300), h: 0.3,
  align: "center", valign: "middle", margin: 0,
  fontFace: COMIC, fontSize: 13.5, bold: true, italic: true, color: C.red, lineSpacing: OL_LS,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
