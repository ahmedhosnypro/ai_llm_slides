// components/slide_043.js — slide 043 "Multi Head Self Attention of Word X2 'Wide'
// Architecture" composition. ROOT of the 44←43, 45←43 dependency subtree (founder
// directive 2026-10-11): children MUST require() this module and call
// renderBase(pptx, slide, opts) / cherry-pick blocks — NEVER re-derive this geometry.
//
// Block granularity (opts.skip / opts.only):
//   chrome, title, vecbox, pipearrows, ltbox, concatbar, headarrows, cards,
//   headannots, ff_left, ff_mid, ff_right, queryrow, bottomcurve, headpanels,
//   wochips, swoosh, hlabel, legend
// Child 44: adds the Figure-2-right inset ON TOP (occludes title tail + h=5 badge).
// Child 45: drops ff_mid's linear-transformation-adjacent blocks? — NO: child 45 REMOVES
//   the ltbox+concatbar pipeline (Narrow variant) and adds input-sequence legend blocks;
//   it composes via opts.skip:['ltbox','concatbar','pipearrows',...].
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_043.jpg (960x540, 1px=1pt,
// in=px/72) — scanline runs, color medians, component bboxes (scratch/slide043/m*.py) —
// cross-read with 12 banked vision-crop transcripts (an_*.txt). The spec's fallback-model
// color/label claims were re-verified against pixels; measured values win.
//
// LAWS honored: playlist chrome via shared module (numeral = printed 43); verbatim text;
// professional-2D math (mathtext 600dpi PNGs, exact size, never rescaled); true
// sub/superscript runs for indexed labels; margin:0 + fontFace everywhere; no '#' in hex;
// explicit lineSpacing on multi-line boxes; mouse-cursor artifact omitted.

const path = require("path");
const { drawHouseChrome } = require(path.join(__dirname, "house_chrome.js"));

const ASSETS = path.join(__dirname, "..", "assets");

// ---- palette (pixel-measured cores) -----------------------------------------
const C = {
  red: "C00000",        // bright red arrows/labels
  brick: "A0400E",      // burnt orange-red (bar seg1, K labels, row lines, X/V labels)
  darkred: "8B1A10",    // swoosh / h-vector ink
  black: "1A1A1A",
  ink: "333333",
  blue: "2F55C8",       // LT-box dH, sigma, W_v borders, legend caption, oval text
  navy: "1F1F8C",       // "Wide" word
  purple: "7B2FBF",     // Soft max label
  green: "2E8B57",      // dashed borders
  brightgreen: "00AA00",// thick green arrow
  magenta: "FF69B4",    // X2 emphasis
  cardH1: "EF8C96", cardH2: "C5C1F4", cardH3: "F8FF9A", cardH4: "D4FFE5", cardH5: "F7E2CD",
  barLabel: "F9FBBD", seg1: "BB4F07", seg2: "777C5C", seg3: "F2F208", seg4: "AAFF71", seg5: "F3DEBC",
  ltFill: "F6FAD5", ltEdge: "D26900",
  pillScaling: "FBD8E8", pillSoftmax: "E4D8F4",
  tan: "D8C0A8",
  legendFill: "E6FCE6",
  vecCells: ["FCFFCB", "F1FFDB", "DFF0C8", "EAE4EE", "F6DAF3"],
  tagFill: "141405", tagText: "E8E95D",
  ovalText: "4A5AA0",
};
const SANS = "Arial";

const px = (v) => v / 72;

// ---- helpers ------------------------------------------------------------------

function text(slide, str, o) {
  slide.addText(str, Object.assign({ fontFace: SANS, margin: 0 }, o));
}

// W-chip label runs: W + subscript letter + superscript "(h)"
function wRuns(letter, h, color, size) {
  return [
    { text: "W", options: { bold: true, fontSize: size, color } },
    { text: letter, options: { bold: true, fontSize: size * 0.75, color, subscript: true } },
    { text: `(${h})`, options: { bold: true, fontSize: size * 0.7, color, superscript: true } },
  ];
}

// X/V/K/q indexed label runs
function idxRuns(base, i, color, size) {
  return [
    { text: base, options: { bold: true, fontSize: size, color } },
    { text: String(i), options: { bold: true, fontSize: size * 0.75, color, subscript: true } },
  ];
}

// ---- block functions ----------------------------------------------------------

function drawTitle(pptx, slide) {
  // line 1 — ink x 527..870, y 54..76, centered at cx~700
  text(slide, [
    { text: "Multi Head Self Attention of Word ", options: { color: C.ink } },
    { text: "X", options: { color: C.red } },
    { text: "2", options: { color: C.red, subscript: true, fontSize: 15 } },
  ], {
    x: px(500), y: px(48), w: px(400), h: px(30), align: "center", valign: "middle",
    bold: true, fontSize: 23,
  });
  // line 2 — ink x 606..797, y 78..99; "Wide" navy bold on yellow highlight (quotes outside)
  text(slide, [
    { text: "\u201C", options: { color: C.ink } },
    { text: "Wide", options: { color: C.navy, highlight: "FFFF00" } },
    { text: "\u201D Architecture", options: { color: C.ink } },
  ], {
    x: px(500), y: px(77), w: px(400), h: px(24), align: "center", valign: "middle",
    bold: true, fontSize: 20,
  });
}

function drawVecbox(pptx, slide) {
  // small output vector box x 400..470, y 50..72; blue rounded border; 5 cells; green Y2 in cell 3
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(400), y: px(50), w: px(70), h: px(22), rectRadius: 0.04,
    fill: { color: "FFFFFF" }, line: { color: "2222CC", width: 1.25 },
  });
  for (let i = 0; i < 5; i++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(402 + i * 13.4), y: px(52.5), w: px(13), h: px(17),
      fill: { color: C.vecCells[i] }, line: { color: "C9C9C9", width: 0.5 },
    });
  }
  text(slide, [
    { text: "Y", options: { bold: true, color: "007A00", fontSize: 8 } },
    { text: "2", options: { bold: true, color: "007A00", fontSize: 6, subscript: true } },
  ], { x: px(424), y: px(54), w: px(20), h: px(14), align: "center", valign: "middle" });
  text(slide, "1\u00D7d", {
    x: px(473), y: px(60), w: px(26), h: px(14), align: "left", valign: "middle",
    bold: true, fontSize: 8, color: C.red,
  });
}

function drawPipearrows(pptx, slide) {
  // red connectors, flow upward: LT->vecbox and bar->LT
  slide.addShape(pptx.ShapeType.line, {
    x: px(455), y: px(74.5), w: 0, h: px(14.5),
    line: { color: C.red, width: 1.5, beginArrowType: "triangle" },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(467), y: px(115.5), w: 0, h: px(11.5),
    line: { color: C.red, width: 1.5, beginArrowType: "triangle" },
  });
}

function drawLtbox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(314), y: px(90), w: px(240), h: px(24.5),
    fill: { color: C.ltFill }, line: { color: C.ltEdge, width: 1.5 },
  });
  text(slide, [
    { text: "Linear Transformation    [ T ] ", options: { color: C.ink } },
    { text: "d", options: { color: C.red, fontSize: 7.5, subscript: true } },
    { text: "H", options: { color: C.blue, fontSize: 7.5, subscript: true } },
    { text: "\u00D7", options: { color: C.red, fontSize: 7.5, superscript: true } },
    { text: "d", options: { color: C.red, fontSize: 7.5, subscript: true } },
  ], {
    x: px(314), y: px(90), w: px(240), h: px(24.5), align: "center", valign: "middle",
    bold: true, fontSize: 10.5,
  });
}

const SEGS = [
  { x: 311, w: 74, fill: C.seg1 }, { x: 385, w: 75, fill: C.seg2 },
  { x: 460, w: 74, fill: C.seg3 }, { x: 534, w: 74, fill: C.seg4 },
  { x: 608, w: 76, fill: C.seg5 },
];

function drawConcatbar(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(185), y: px(128), w: px(499), h: px(23.5),
    fill: { color: C.barLabel }, line: { color: "3A3A3A", width: 1 },
  });
  for (const s of SEGS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(s.x), y: px(128), w: px(s.w), h: px(23.5),
      fill: { color: s.fill }, line: { color: "3A3A3A", width: 0.5 },
    });
    // tiny white Y chip w/ subscript numeral (spec item 6, [?]-marked in spec)
    const cxm = s.x + s.w / 2;
    slide.addShape(pptx.ShapeType.rect, {
      x: px(cxm - 8), y: px(133.5), w: px(16), h: px(12.5),
      fill: { color: "FFFFFF" }, line: { color: "B0B0B0", width: 0.5 },
    });
  }
  SEGS.forEach((s, i) => {
    const cxm = s.x + s.w / 2;
    text(slide, idxRuns("Y", i + 1, C.brick, 5.5), {
      x: px(cxm - 8), y: px(133.5), w: px(16), h: px(12.5),
      align: "center", valign: "middle",
    });
  });
  // red two-line label at the bar's left end (ink: line1 y132..141 x191..280; line2 y142..147 x~250..298)
  text(slide, "Concatenated Vector", {
    x: px(188), y: px(130), w: px(118), h: px(12), align: "left", valign: "middle",
    bold: true, fontSize: 7.5, color: C.red,
  });
  text(slide, [
    { text: "1\u00D7", options: { color: C.red } },
    { text: "dH", options: { color: C.blue } },
  ], {
    x: px(248), y: px(141), w: px(58), h: px(9.5), align: "left", valign: "middle",
    bold: true, fontSize: 7,
  });
}

function drawHeadarrows(pptx, slide) {
  // five thin red arrows rise from the head-vector stack into the bar's five segments;
  // visible only in the gap between bar bottom (151.5) and the back card top (~192) —
  // the cards drawn later clip the rest, exactly as in the original.
  const xs = [411, 431, 451, 471, 491];
  for (const x of xs) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(x), y: px(152.5), w: 0, h: px(38),
      line: { color: C.red, width: 1.1, beginArrowType: "triangle" },
    });
  }
}

const CARDS = [
  { x: 234, y: 192, h: 240, fill: C.cardH5 },
  { x: 189, y: 208, h: 247, fill: C.cardH4 },
  { x: 152, y: 232, h: 250, fill: C.cardH3 },
  { x: 104, y: 252, h: 256, fill: C.cardH2 },
  { x: 56, y: 274, h: 252, fill: C.cardH1 },
];

function drawCards(pptx, slide) {
  for (const c of CARDS) {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(c.x), y: px(c.y), w: px(548), h: px(c.h), rectRadius: 0.06,
      fill: { color: c.fill }, line: { type: "none" },
    });
  }
}

function drawHeadannots(pptx, slide) {
  // per-card white ovals + head output vector + h=N tag (staircase pitch +44 x, -20.5 y)
  for (let k = 0; k < 5; k++) {
    const yc = 285.5 - 20.5 * k;       // oval center y
    const simX = 206 + 44 * k;
    const wsX = 428 + 44 * k;
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(simX), y: px(yc - 7), w: px(44), h: px(14),
      fill: { color: "FFFFFF" }, line: { color: "9A9A9A", width: 0.75 },
    });
    text(slide, "Similarity", {
      x: px(simX), y: px(yc - 7), w: px(44), h: px(14), align: "center", valign: "middle",
      fontSize: 5.5, color: C.ovalText,
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(wsX), y: px(yc - 7), w: px(63), h: px(14),
      fill: { color: "FFFFFF" }, line: { color: "9A9A9A", width: 0.75 },
    });
    text(slide, "Weighted SUM", {
      x: px(wsX), y: px(yc - 7), w: px(63), h: px(14), align: "center", valign: "middle",
      fontSize: 5.5, color: C.ovalText,
    });
    // head output vector between the ovals (measured fills; h1's slot carries the
    // Probabilities oval — its vector is occluded in the original)
    const vecs = [
      null,
      { x: 390, y: 256, w: 50, h: 15, fill: "9A86C8" },
      { x: 408, y: 242, w: 50, h: 16, fill: "A0400E" },
      { x: 433, y: 216, w: 66, h: 15, fill: "4A4A4A" },
      { x: 468, y: 196, w: 44, h: 14, fill: "E0DC1E" },
    ][k];
    if (vecs) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(vecs.x), y: px(vecs.y), w: px(vecs.w), h: px(vecs.h),
        fill: { color: vecs.fill }, line: { color: "3A3A3A", width: 0.5 },
      });
    }
    // h=N tag: black ellipse, bold yellow numeral text
    const tag = { x: 563 + 46 * k, y: 280 - 20.5 * k };
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(tag.x), y: px(tag.y), w: px(30), h: px(14.5),
      fill: { color: C.tagFill }, line: { type: "none" },
    });
    text(slide, `h=${k + 1}`, {
      x: px(tag.x), y: px(tag.y), w: px(30), h: px(14.5), align: "center", valign: "middle",
      bold: true, fontSize: 7, color: C.tagText,
    });
  }
  // Probabilities oval straddling the h2/h1 top edges (ink x 312..374 y 276..295 + top half)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(298), y: px(264), w: px(78), h: px(29),
    fill: { color: "FDF3EE" }, line: { color: "C9B8B0", width: 0.75 },
  });
  text(slide, "Probabilities", {
    x: px(298), y: px(264), w: px(78), h: px(29), align: "center", valign: "middle",
    fontSize: 6, color: C.ink,
  });
}

// ---- front-card flow: left (inputs -> W_k -> K bars -> Dot Product) -----------

function drawFfLeft(pptx, slide) {
  // dashed input container x 92..128, y 318..442 with 4 pink/lavender cells
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(92), y: px(318), w: px(36), h: px(124), rectRadius: 0.05,
    fill: { color: "F3F3F0" }, line: { color: C.green, width: 1.25, dashType: "dash" },
  });
  const cellFills = ["F6DAF3", "EAE4EE", "F6DAF3", "EAE4EE"];
  for (let i = 0; i < 4; i++) {
    const yc = 335 + 28 * i; // row centers 335/363/391/419
    slide.addShape(pptx.ShapeType.rect, {
      x: px(96), y: px(yc - 11), w: px(28), h: px(22),
      fill: { color: cellFills[i] }, line: { color: "C9C9C9", width: 0.5 },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: px(125), y: px(yc), w: px(9), h: 0,
      line: { color: C.darkred, width: 1, endArrowType: "triangle" },
    });
    // four bright-green bordered W_k^(1) boxes x 128..152
    slide.addShape(pptx.ShapeType.rect, {
      x: px(128), y: px(yc - 9.5), w: px(24), h: px(19),
      fill: { color: "F0FFF0" }, line: { color: C.green, width: 1.25 },
    });
    text(slide, wRuns("k", 1, C.ink, 5.5), {
      x: px(128), y: px(yc - 9.5), w: px(24), h: px(19), align: "center", valign: "middle",
    });
    // striped K bar x 156..184 (yellow/white/red-pink segments)
    const barFills = ["F9FF96", "FFFFFF", "F08B96"];
    for (let j = 0; j < 3; j++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(156 + j * 9.5), y: px(yc - 7.5), w: px(9.5), h: px(15),
        fill: { color: barFills[j] }, line: { color: "B8B8B8", width: 0.5 },
      });
    }
    // red K label above the arrow into the Dot Product box (K1..K4 top->bottom)
    text(slide, idxRuns("K", i + 1, C.brick, 6), {
      x: px(177), y: px(yc - 20), w: px(16), h: px(10), align: "left", valign: "middle",
    });
    slide.addShape(pptx.ShapeType.line, {
      x: px(186), y: px(yc), w: px(9), h: 0,
      line: { color: C.brick, width: 1, endArrowType: "triangle" },
    });
  }
  // tan Dot Product box x 195..253, y 301..441
  slide.addShape(pptx.ShapeType.rect, {
    x: px(195), y: px(301), w: px(58), h: px(140),
    fill: { color: C.tan }, line: { color: "8A6A48", width: 1 },
  });
  text(slide, "Dot Product", {
    x: px(195), y: px(303), w: px(58), h: px(14), align: "center", valign: "middle",
    bold: true, fontSize: 6.5, color: "5C2E12",
  });
  // four target circles (navy dot + light-blue ring) on an ascending diagonal,
  // red fan lines from the box's bottom-center up to each circle
  const circles = [
    { x: 208, y: 419 }, { x: 216, y: 391 }, { x: 226, y: 363 }, { x: 238, y: 335 },
  ];
  for (const c of circles) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(224), y: px(438), w: px(c.x - 224), h: px(c.y + 4 - 438),
      line: { color: C.darkred, width: 0.9 },
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(c.x - 5), y: px(c.y - 5), w: px(10), h: px(10),
      fill: { color: "BFE0F0" }, line: { color: "5A8AC8", width: 1 },
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(c.x - 2), y: px(c.y - 2), w: px(4), h: px(4),
      fill: { color: "1F2A5C" }, line: { type: "none" },
    });
  }
  // q1 entry arrow from below into the box bottom
  slide.addShape(pptx.ShapeType.line, {
    x: px(224), y: px(443), w: 0, h: px(20),
    line: { color: C.red, width: 1.5, beginArrowType: "triangle" },
  });
}

// ---- front-card flow: middle (K,q labels, pills, Probabilities->Sigma) --------

function drawFfMid(pptx, slide) {
  // four dashed row lines from the Dot Product cells rightward (under the pills)
  for (const y of [335, 363, 391, 419]) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(256), y: px(y), w: px(158), h: 0,
      line: { color: C.brick, width: 1, dashType: "dash" },
    });
  }
  // "K,q" label right of the Dot Product box
  text(slide, "K,q", {
    x: px(255), y: px(302), w: px(24), h: px(12), align: "left", valign: "middle",
    bold: true, fontSize: 6.5, color: C.brick,
  });
  // Scaling pill (pale pink) with rotated mathtext label
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(278), y: px(301), w: px(22), h: px(140), rectRadius: 0.09,
    fill: { color: C.pillScaling }, line: { color: "E8A8C8", width: 0.75 },
  });
  slide.addImage({
    path: path.join(ASSETS, "eq_scaling_pill_rot.png"),
    x: px(279.5), y: px(318), w: 0.25833, h: 1.23167,
  });
  // K,q / sqrt(d) stacked fraction above the Soft max pill (professional 2D — PNG at exact size)
  slide.addImage({
    path: path.join(ASSETS, "eq_kq_sqrtd.png"),
    x: px(305), y: px(294), w: 0.225, h: 0.31667,
  });
  // Soft max pill (light lavender) with rotated label
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(332), y: px(301), w: px(23), h: px(140), rectRadius: 0.09,
    fill: { color: C.pillSoftmax }, line: { color: "C8B8E8", width: 0.75 },
  });
  slide.addImage({
    path: path.join(ASSETS, "eq_softmax_pill_rot.png"),
    x: px(339), y: px(352), w: 0.12167, h: 0.57333,
  });
  // thick green arrow from Probabilities toward the Sigma stage
  slide.addShape(pptx.ShapeType.line, {
    x: px(378), y: px(277), w: px(32), h: px(-6),
    line: { color: C.brightgreen, width: 2.5, endArrowType: "triangle" },
  });
  // Sigma box (white, blue outline, large blue sigma)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(354), y: px(296), w: px(60), h: px(34),
    fill: { color: "FFFFFF" }, line: { color: C.blue, width: 1.25 },
  });
  text(slide, "\u03A3", {
    x: px(354), y: px(296), w: px(60), h: px(34), align: "center", valign: "middle",
    bold: true, fontSize: 20, color: C.blue,
  });
}

// ---- front-card flow: right (nodes -> V bars -> W_v -> X cells) ---------------

function drawFfRight(pptx, slide) {
  const rows = [335, 363, 391, 419];
  rows.forEach((y, i) => {
    // circled-X node
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(432), y: px(y - 7.5), w: px(15), h: px(15),
      fill: { color: "FCE8E8" }, line: { color: "CC2222", width: 1.25 },
    });
    text(slide, "\u00D7", {
      x: px(432), y: px(y - 7.5), w: px(15), h: px(15), align: "center", valign: "middle",
      bold: true, fontSize: 8, color: "CC2222",
    });
    // thin red arrow node -> Sigma box right edge
    slide.addShape(pptx.ShapeType.line, {
      x: px(418), y: px(316 + i * 4), w: px(10), h: px(y - 7.5 - (316 + i * 4)),
      line: { color: C.red, width: 0.9, beginArrowType: "triangle" },
    });
    // V label + tiny multi-colored bar
    text(slide, idxRuns("V", i + 1, C.brick, 5.5), {
      x: px(452), y: px(y - 9), w: px(15), h: px(10), align: "left", valign: "middle",
    });
    const barFills = ["F9FF96", "FFFFFF", "F08B96", "EAE4EE"];
    for (let j = 0; j < 4; j++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(468 + j * 9), y: px(y - 7), w: px(9), h: px(14),
        fill: { color: barFills[j] }, line: { color: "B8B8B8", width: 0.5 },
      });
    }
    // W_v^(1) box (white, blue outline)
    slide.addShape(pptx.ShapeType.rect, {
      x: px(510), y: px(y - 11), w: px(42), h: px(22),
      fill: { color: "FFFFFF" }, line: { color: C.blue, width: 1 },
    });
    text(slide, wRuns("v", 1, C.ink, 5.5), {
      x: px(510), y: px(y - 11), w: px(42), h: px(22), align: "center", valign: "middle",
    });
  });
  // dashed X-cells box x 558..602, y 320..432
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(558), y: px(320), w: px(46), h: px(112), rectRadius: 0.05,
    fill: { color: "FFFFFF" }, line: { color: C.green, width: 1, dashType: "dash" },
  });
  const rowFills = [
    ["F9FF96", "FFFFF0", "F6DAF3"],
    ["EAE4EE", "F9FF96", "FFFFF0"],
    ["F6DAF3", "EAE4EE", "F9FF96"],
    ["FFFFF0", "F6DAF3", "EAE4EE"],
  ];
  for (let i = 0; i < 4; i++) {
    const yc = 334 + 27 * i;
    text(slide, idxRuns("X", i + 1, C.brick, 5), {
      x: px(561), y: px(yc - 8), w: px(12), h: px(16), align: "left", valign: "middle",
    });
    for (let j = 0; j < 3; j++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(574 + j * 9.5), y: px(yc - 8), w: px(9.5), h: px(16),
        fill: { color: rowFills[i][j] }, line: { color: "C9C9C9", width: 0.5 },
      });
    }
  }
}

// ---- query row (bottom) --------------------------------------------------------

function drawQueryrow(pptx, slide) {
  // q1 red vector bar + label, red arrow up into the Dot Product box
  slide.addShape(pptx.ShapeType.rect, {
    x: px(205), y: px(467), w: px(46), h: px(12),
    fill: { color: C.red }, line: { type: "none" },
  });
  text(slide, idxRuns("q", 1, C.red, 7), {
    x: px(189), y: px(466), w: px(15), h: px(13), align: "left", valign: "middle",
  });
  // W_q^(1) box (white, red outline) + small red arrow down toward the container
  slide.addShape(pptx.ShapeType.rect, {
    x: px(258), y: px(448), w: px(44), h: px(24),
    fill: { color: "FFFFFF" }, line: { color: "CC2222", width: 1.25 },
  });
  text(slide, wRuns("q", 1, C.ink, 6), {
    x: px(258), y: px(448), w: px(44), h: px(24), align: "center", valign: "middle",
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(280), y: px(474), w: 0, h: px(12),
    line: { color: C.red, width: 1, endArrowType: "triangle" },
  });
  // token container: dashed green, pale green fill, 4 word strips, X2 magenta
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(152), y: px(492), w: px(190), h: px(29), rectRadius: 0.05,
    fill: { color: "E8FCE8" }, line: { color: C.green, width: 1.25, dashType: "dash" },
  });
  const strips = [
    { x: 158, w: 56, fill: "F7F3D8", hot: false },
    { x: 222, w: 36, fill: "F2C8F0", hot: true },
    { x: 260, w: 46, fill: "F7F3D8", hot: false },
    { x: 310, w: 32, fill: "F7F3D8", hot: false },
  ];
  strips.forEach((s, i) => {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(s.x), y: px(496), w: px(s.w), h: px(15),
      fill: { color: s.fill },
      line: s.hot ? { color: C.magenta, width: 1.5 } : { color: "B8B8B8", width: 0.5 },
    });
    text(slide, idxRuns("X", i + 1, C.brick, 5), {
      x: px(s.x), y: px(496), w: px(s.w), h: px(15), align: "center", valign: "middle",
    });
  });
  // thick red arrow pointing up-right into the X2 strip from lower-left
  slide.addShape(pptx.ShapeType.line, {
    x: px(243), y: px(513), w: px(10), h: px(-13),
    line: { color: C.red, width: 2.25, endArrowType: "triangle" },
  });
}

function drawBottomcurve(pptx, slide) {
  slide.addImage({
    path: path.join(ASSETS, "bottom_curve.png"),
    x: px(230), y: px(452), w: 5.20833, h: 1.13889,
  });
}

// ---- per-head right panels: dashed X-boxes on the card slivers + W-chip columns

const HEADCOLS = [
  { h: 2, x: 616, xboxY: 322, wtop: 446 },
  { h: 3, x: 660, xboxY: 296, wtop: 420 },
  { h: 4, x: 704, xboxY: 270, wtop: 394 },
  { h: 5, x: 748, xboxY: 244, wtop: 368 },
];

function drawHeadpanels(pptx, slide) {
  const rowFills = [
    ["F9FF96", "FFFFF0", "F6DAF3"],
    ["EAE4EE", "F9FF96", "FFFFF0"],
    ["F6DAF3", "EAE4EE", "F9FF96"],
    ["FFFFF0", "F6DAF3", "EAE4EE"],
  ];
  for (const c of HEADCOLS) {
    // dashed X-box on the card sliver
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(c.x), y: px(c.xboxY), w: px(42), h: px(122), rectRadius: 0.05,
      fill: { color: "FFFFFF" }, line: { color: C.green, width: 1, dashType: "dash" },
    });
    for (let i = 0; i < 4; i++) {
      const yc = c.xboxY + 16 + i * 30;
      text(slide, idxRuns("X", i + 1, C.brick, 5), {
        x: px(c.x + 3), y: px(yc - 8), w: px(12), h: px(16), align: "left", valign: "middle",
      });
      for (let j = 0; j < 3; j++) {
        slide.addShape(pptx.ShapeType.rect, {
          x: px(c.x + 15 + j * 8.5), y: px(yc - 8), w: px(8.5), h: px(16),
          fill: { color: rowFills[i][j] }, line: { color: "C9C9C9", width: 0.5 },
        });
      }
    }
    // small green arrowhead beneath the dashed group
    slide.addShape(pptx.ShapeType.line, {
      x: px(c.x + 21), y: px(c.xboxY + 116), w: 0, h: px(9),
      line: { color: C.brightgreen, width: 1.25, beginArrowType: "triangle" },
    });
  }
}

function drawWochips(pptx, slide) {
  const borders = { q: "CC2222", k: C.green, v: C.blue };
  for (const c of HEADCOLS) {
    const rows = [
      { letter: "q", dy: 0 }, { letter: "k", dy: 24 }, { letter: "v", dy: 48 },
    ];
    for (const r of rows) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(c.x), y: px(c.wtop + r.dy), w: px(42), h: px(22),
        fill: { color: "FFFFFF" }, line: { color: borders[r.letter], width: 1.25 },
      });
      text(slide, wRuns(r.letter, c.h, C.brick, 5.5), {
        x: px(c.x), y: px(c.wtop + r.dy), w: px(42), h: px(22),
        align: "center", valign: "middle",
      });
    }
  }
}

function drawSwoosh(pptx, slide) {
  slide.addImage({
    path: path.join(ASSETS, "swoosh.png"),
    x: px(585), y: px(325), w: 2.43056, h: 2.08333,
  });
}

function drawHlabel(pptx, slide) {
  // blue italic "H^th Heads" along the swoosh's upper end (angled parallel to it)
  text(slide, [
    { text: "H", options: { italic: true, bold: true, fontSize: 10, color: "0033CC" } },
    { text: "th", options: { italic: true, bold: true, fontSize: 7, color: "0033CC", superscript: true } },
    { text: " Heads", options: { italic: true, bold: true, fontSize: 10, color: "0033CC" } },
  ], {
    x: px(612), y: px(392), w: px(96), h: px(16), align: "center", valign: "middle",
    rotate: 322, margin: 0, fontFace: SANS,
  });
}

function drawLegend(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(736), y: px(468), w: px(170), h: px(64), rectRadius: 0.06,
    fill: { color: C.legendFill }, line: { color: C.green, width: 1.25, dashType: "dash" },
  });
  // vector icon: 8 tiny cells + red 1×d caption
  const cellFills = ["F9FF96", "FFFFFF", "F6DAF3", "EAE4EE", "F9FF96", "FFFFFF", "F6DAF3", "EAE4EE"];
  for (let j = 0; j < 8; j++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(744 + j * 5.6), y: px(472), w: px(5.6), h: px(11),
      fill: { color: cellFills[j] }, line: { color: "C9C9C9", width: 0.5 },
    });
  }
  text(slide, "1\u00D7d", {
    x: px(744), y: px(486), w: px(44), h: px(10), align: "center", valign: "middle",
    bold: true, fontSize: 6, color: C.brick,
  });
  // W square
  slide.addShape(pptx.ShapeType.rect, {
    x: px(798), y: px(472), w: px(26), h: px(26),
    fill: { color: "FBE8B8" }, line: { color: C.ink, width: 1.25 },
  });
  text(slide, "W", {
    x: px(798), y: px(472), w: px(26), h: px(26), align: "center", valign: "middle",
    bold: true, fontSize: 12, color: C.ink,
  });
  // =
  text(slide, "=", {
    x: px(828), y: px(478), w: px(14), h: px(16), align: "center", valign: "middle",
    bold: true, fontSize: 12, color: C.red,
  });
  // d×d grid icon + caption
  slide.addShape(pptx.ShapeType.rect, {
    x: px(846), y: px(472), w: px(26), h: px(26),
    fill: { color: "FFFFFF" }, line: { color: C.ink, width: 1 },
  });
  for (let j = 1; j < 4; j++) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(846 + j * 6.5), y: px(472), w: 0, h: px(26),
      line: { color: "8A8A8A", width: 0.5 },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: px(846), y: px(472 + j * 6.5), w: px(26), h: 0,
      line: { color: "8A8A8A", width: 0.5 },
    });
  }
  text(slide, "d\u00D7d", {
    x: px(840), y: px(500), w: px(38), h: px(10), align: "center", valign: "middle",
    bold: true, fontSize: 6, color: C.brick,
  });
  // caption (blue bold per two independent crop reads)
  text(slide, "d: Embedding Length", {
    x: px(740), y: px(514), w: px(162), h: px(12), align: "center", valign: "middle",
    bold: true, fontSize: 7, color: C.blue,
  });
}

// ---- composition ----------------------------------------------------------------

const BLOCKS = {
  title: drawTitle,
  vecbox: drawVecbox,
  pipearrows: drawPipearrows,
  ltbox: drawLtbox,
  concatbar: drawConcatbar,
  headarrows: drawHeadarrows,
  cards: drawCards,
  headannots: drawHeadannots,
  ff_left: drawFfLeft,
  ff_mid: drawFfMid,
  ff_right: drawFfRight,
  queryrow: drawQueryrow,
  bottomcurve: drawBottomcurve,
  headpanels: drawHeadpanels,
  wochips: drawWochips,
  swoosh: drawSwoosh,
  hlabel: drawHlabel,
  legend: drawLegend,
};

/**
 * Draw the full slide-043 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool, numeral:string|number }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 43 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, C, px, GEO: { CARDS, SEGS, HEADCOLS } };
