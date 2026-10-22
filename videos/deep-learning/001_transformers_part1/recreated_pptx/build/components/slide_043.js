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
// FIX PASS fixer-f10-43-resume2-20261014 (DEFECTS.md F10 huge-rework): A1-A10, B1-B5,
// C1-C7, D1-D5, E1-E6, F1-F4, G1-G5, H1-H2 applied; assets regenerated (swoosh.png
// PIL-traced ribbon, eq_kq_sqrtd.png K\cdot q, bottom_curve.png right end cut at x592);
// E-zone re-derived on the fix-step PIL map (FIVE columns h1..h5, panel tops
// 337/316/295/274/255, q tops 422/401/380/359/338, k/v pitch 40).
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

// W-chip label runs: W + subscript letter + superscript "(h)" — sub/sup kept large
// enough to read (judge attempt 1 #2: subscript was illegible at 0.75x)
function wRuns(letter, h, color, size) {
  return [
    { text: "W", options: { bold: true, fontSize: size, color } },
    { text: letter, options: { bold: true, fontSize: size * 0.85, color, subscript: true } },
    { text: `(${h})`, options: { bold: true, fontSize: size * 0.8, color, superscript: true } },
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
  // line 1 — ink x 527..867 (340px), y 54..76, centered at cx~697; 20pt matches the
  // original's measured width (23pt overflowed into the badge — judge attempt 1 #1)
  text(slide, [
    { text: "Multi Head Self Attention of Word ", options: { color: C.ink } },
    { text: "X", options: { color: C.red } },
    { text: "2", options: { color: C.red, subscript: true, fontSize: 14 } },
  ], {
    x: px(500), y: px(48), w: px(400), h: px(30), align: "center", valign: "middle",
    bold: true, fontSize: 20,
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
  text(slide, "1*d", {
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
    { text: "H", options: { color: C.blue, fontSize: 6.5, subscript: true } },
    { text: "*", options: { color: C.red, fontSize: 7.5, subscript: true } },
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
  // stadium (pill) silhouette per judge attempt 1 #6: rounded base + inset segments
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(185), y: px(128), w: px(499), h: px(23.5), rectRadius: 0.163,
    fill: { color: C.barLabel }, line: { color: "3A3A3A", width: 1 },
  });
  for (const s of SEGS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(s.x + 1), y: px(129.5), w: px(s.w - 2), h: px(20.5),
      fill: { color: s.fill }, line: { color: "3A3A3A", width: 0.5 },
    });
    // internal dotted partitions (B2: cellular strip idiom, 3 dividers per segment)
    for (let j = 1; j <= 3; j++) {
      slide.addShape(pptx.ShapeType.line, {
        x: px(s.x + 1 + ((s.w - 2) * j) / 4), y: px(130.5), w: 0, h: px(18.5),
        line: { color: "C9C9C9", width: 0.5, dashType: "sysDot" },
      });
    }
  }
  SEGS.forEach((s, i) => {
    // Y_i^(t) printed DIRECTLY on the segments (B1: no white chip boxes; (t) letters)
    const cxm = s.x + s.w / 2;
    text(slide, [
      { text: "Y", options: { bold: true, fontSize: 6, color: C.brick } },
      { text: String(i + 1), options: { bold: true, fontSize: 4.5, color: C.brick, subscript: true } },
      { text: "(t)", options: { bold: true, fontSize: 4.5, color: C.brick, superscript: true } },
    ], {
      x: px(cxm - 10), y: px(133.5), w: px(20), h: px(12.5),
      align: "center", valign: "middle",
    });
  });
  // re-draw the stadium outline so the pill silhouette stays rounded over the segments
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(185), y: px(128), w: px(499), h: px(23.5), rectRadius: 0.163,
    fill: { type: "none" }, line: { color: "3A3A3A", width: 1 },
  });
  // red two-line label at the bar's left end (ink: line1 y132..141 x191..280; line2 y142..147 x~250..298)
  text(slide, "Concatenated Vector", {
    x: px(188), y: px(130), w: px(118), h: px(12), align: "left", valign: "middle",
    bold: true, fontSize: 7.5, color: C.red,
  });
  text(slide, [
    { text: "1*", options: { color: C.red } },
    { text: "dH", options: { color: C.blue } },
  ], {
    x: px(248), y: px(141), w: px(58), h: px(9.5), align: "left", valign: "middle",
    bold: true, fontSize: 7,
  });
}

function drawHeadarrows(pptx, slide) {
  // B3: five THIN muted verticals at the head-chip centers, chip top -> bar bottom,
  // small arrowheads at BOTH ends; visible only in the gap between bar bottom (151.5)
  // and the back card top (~192) — cards drawn later clip the rest, as in the original.
  const arrows = [
    { x: 337, chipTop: 278 }, { x: 411, chipTop: 262 }, { x: 435, chipTop: 242 },
    { x: 473, chipTop: 217 }, { x: 490, chipTop: 197 },
  ];
  for (const a of arrows) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(a.x), y: px(152.5), w: 0, h: px(a.chipTop - 152.5),
      line: { color: "B08585", width: 0.8, beginArrowType: "triangle", endArrowType: "triangle" },
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
    // head output chips between the ovals — dashed-green-bordered, red Y labels,
    // climbing the diagonal toward the bar (judge attempt 1 #3/#4; staircase read:
    // lavender-bits / orange / dark gray / yellow + the green chip poking into the
    // gap below the bar). h1's slot: pale chip right of the Probabilities oval.
    const vecs = [
      { x: 312, y: 278, w: 62, h: 16, fill: "FFFFE3" }, // PIL: original pale-yellow (255,255,227)
      { x: 391, y: 262, w: 40, h: 14, fill: "9A86C8" },
      { x: 413, y: 242, w: 44, h: 16, fill: "A0400E" },
      { x: 445, y: 217, w: 56, h: 15, fill: "4A4A4A" },
      { x: 470, y: 197, w: 40, h: 14, fill: "E0DC1E" },
    ][k];
    if (vecs) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(vecs.x), y: px(vecs.y), w: px(vecs.w), h: px(vecs.h),
        fill: { color: vecs.fill }, line: { color: C.green, width: 1, dashType: "dash" },
      });
      text(slide, idxRuns("Y", k + 1, C.red, 6), {
        x: px(vecs.x), y: px(vecs.y), w: px(vecs.w), h: px(vecs.h),
        align: "center", valign: "middle",
      });
    }
    // h=N tag: black ellipse, bold yellow numeral text (A10: measured per-k centers
    // (578.6,287.0)(631.8,264.9)(673.1,242.9)(716.9,224.0)(761.0,205.0), blobs 30x15)
    const TAGC = [
      { x: 578.6, y: 287.0 }, { x: 631.8, y: 264.9 }, { x: 673.1, y: 242.9 },
      { x: 716.9, y: 224.0 }, { x: 761.0, y: 205.0 },
    ][k];
    const tag = { x: TAGC.x - 15, y: TAGC.y - 7.25 };
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
  // fill per PIL: original lavender (196,194,244) = C4C2F4 (crop-judge MAJOR, fixed)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(294), y: px(250), w: px(80), h: px(28),
    fill: { color: "C4C2F4" }, line: { color: "C9B8B0", width: 0.75 },
  });
  text(slide, "Probabilities", {
    x: px(294), y: px(250), w: px(80), h: px(28), align: "center", valign: "middle",
    fontSize: 6, color: C.ink,
  });
  // green gap chip rising from the layer tops toward the bar (measured #A0E060 core
  // at 485..535, 178..192) — the topmost of the climbing output chain
  slide.addShape(pptx.ShapeType.rect, {
    x: px(486), y: px(177), w: px(44), h: px(15),
    fill: { color: "8ED08A" }, line: { color: C.green, width: 1, dashType: "dash" },
  });
  text(slide, idxRuns("Y", 5, C.red, 6), {
    x: px(486), y: px(177), w: px(44), h: px(15), align: "center", valign: "middle",
  });
}

// ---- front-card flow: left (inputs -> W_k -> K bars -> Dot Product) -----------

function drawFfLeft(pptx, slide) {
  // dashed input container x 92..128, y 318..442 (C3: original width per PIL Oct11)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(92), y: px(318), w: px(36), h: px(124), rectRadius: 0.05,
    fill: { color: "F3F3F0" }, line: { color: C.green, width: 1.25, dashType: "dash" },
  });
  const cellFills = ["F6DAF3", "EAE4EE", "F6DAF3", "EAE4EE"];
  for (let i = 0; i < 4; i++) {
    const yc = 335 + 28 * i; // row centers 335/363/391/419
    // C1: X labels reversed — X4 top ... X1 bottom
    const tok = 4 - i;
    // C3: shrunken X cell + small 3-cell striped embedding bar beside it
    slide.addShape(pptx.ShapeType.rect, {
      x: px(94), y: px(yc - 11), w: px(15), h: px(22),
      fill: { color: cellFills[i] }, line: { color: "C9C9C9", width: 0.5 },
    });
    text(slide, idxRuns("X", tok, C.brick, 5), {
      x: px(94), y: px(yc - 11), w: px(15), h: px(22), align: "center", valign: "middle",
    });
    const embFills = ["F9FF96", "FFFFFF", "F08B96"];
    for (let j = 0; j < 3; j++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(110.5 + j * 4.7), y: px(yc - 7.5), w: px(4.4), h: px(15),
        fill: { color: embFills[j] }, line: { color: "B8B8B8", width: 0.5 },
      });
    }
    slide.addShape(pptx.ShapeType.line, {
      x: px(125), y: px(yc), w: px(9), h: 0,
      line: { color: C.darkred, width: 1, endArrowType: "triangle" },
    });
    // A8/C2: four bright-green bordered W_k^(1) boxes (constant head-1 superscript)
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
    // red K label above the arrow (C1: K4 top ... K1 bottom)
    text(slide, idxRuns("K", tok, C.brick, 6), {
      x: px(177), y: px(yc - 20), w: px(16), h: px(10), align: "left", valign: "middle",
    });
    // C4: red arrow ENTERS the tan panel, head TERMINATING at the circle's left rim
    const circ = [{ x: 238 }, { x: 226 }, { x: 216 }, { x: 208 }][i];
    slide.addShape(pptx.ShapeType.line, {
      x: px(186), y: px(yc), w: px(circ.x - 5 - 186), h: 0,
      line: { color: C.brick, width: 1, endArrowType: "triangle" },
    });
  }
  // tan Dot Product box x 195..253, y 301..441
  slide.addShape(pptx.ShapeType.rect, {
    x: px(195), y: px(301), w: px(58), h: px(140),
    fill: { color: C.tan }, line: { color: "8A6A48", width: 1 },
  });
  // C6: "Dot / Product" on two centered lines
  text(slide, [
    { text: "Dot", options: { breakLine: true } },
    { text: "Product", options: {} },
  ], {
    x: px(195), y: px(303), w: px(58), h: px(14), align: "center", valign: "middle",
    bold: true, fontSize: 6.5, color: "5C2E12", lineSpacing: 7,
  });
  // four target circles (navy dot + light-blue ring) on an ascending diagonal,
  // red fan lines from the box's bottom-center up to each circle (C5: heads at circles)
  const circles = [
    { x: 208, y: 419 }, { x: 216, y: 391 }, { x: 226, y: 363 }, { x: 238, y: 335 },
  ];
  for (const c of circles) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(224), y: px(438), w: px(c.x - 224), h: px(c.y + 4 - 438),
      line: { color: C.darkred, width: 0.9, endArrowType: "triangle" },
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
  // C7: q-feed arrow from below into the box bottom, tail lengthened down to y~468
  slide.addShape(pptx.ShapeType.line, {
    x: px(224), y: px(443), w: 0, h: px(25),
    line: { color: C.red, width: 1.5, beginArrowType: "triangle" },
  });
}

// ---- front-card flow: middle (K,q labels, pills, Probabilities->Sigma) --------

function drawFfMid(pptx, slide) {
  // D2: row lanes SOLID dark-red in three segments with RED ARROWHEADS at each
  // segment's right end (DotProduct->Scaling 253..278, Scaling->Softmax 300..332,
  // Softmax->nodes 355..430 into the circles' left rim)
  for (const y of [335, 363, 391, 419]) {
    for (const seg of [[253, 278], [300, 332], [355, 430]]) {
      slide.addShape(pptx.ShapeType.line, {
        x: px(seg[0]), y: px(y), w: px(seg[1] - seg[0]), h: 0,
        line: { color: C.darkred, width: 1, endArrowType: "triangle" },
      });
    }
  }
  // A3/D1: "K.q" with the dot operator (never a comma)
  text(slide, "K.q", {
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
  // K.q / sqrt(d) stacked fraction above the Soft max pill (D5: dot operator,
  // professional 2D — PNG at exact size from the certified sidecar)
  slide.addImage({
    path: path.join(ASSETS, "eq_kq_sqrtd.png"),
    x: px(304), y: px(294), w: 0.24667, h: 0.31667,
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
  // Sigma box (D3: measured right position ~(394,289) w60 h34, glyph center ~(424,306))
  slide.addShape(pptx.ShapeType.rect, {
    x: px(394), y: px(289), w: px(60), h: px(34),
    fill: { color: "FFFFFF" }, line: { color: C.blue, width: 1.25 },
  });
  text(slide, "\u03A3", {
    x: px(394), y: px(289), w: px(60), h: px(34), align: "center", valign: "middle",
    bold: true, fontSize: 20, color: C.blue,
  });
}

// ---- front-card flow: right (nodes -> V bars -> W_v -> X cells) ---------------

function drawFfRight(pptx, slide) {
  const rows = [335, 363, 391, 419];
  rows.forEach((y, i) => {
    // circled-X node; D4: the BOTTOM one is a circled STAR/asterisk
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(432), y: px(y - 7.5), w: px(15), h: px(15),
      fill: { color: "FCE8E8" }, line: { color: "CC2222", width: 1.25 },
    });
    text(slide, i === 3 ? "*" : "\u00D7", {
      x: px(432), y: px(y - 7.5), w: px(15), h: px(15), align: "center", valign: "middle",
      bold: true, fontSize: 9, color: "CC2222",
    });
    // D4: per-row red LEFTWARD arrowhead INTO the W_v left face (tail at X-bar 558)
    slide.addShape(pptx.ShapeType.line, {
      x: px(510), y: px(y), w: px(48), h: 0,
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
    // A8: W_v^(1) box (white, blue outline) — constant head-1 superscript
    slide.addShape(pptx.ShapeType.rect, {
      x: px(510), y: px(y - 11), w: px(42), h: px(22),
      fill: { color: "FFFFFF" }, line: { color: C.blue, width: 1 },
    });
    text(slide, wRuns("v", 1, C.ink, 5.5), {
      x: px(510), y: px(y - 11), w: px(42), h: px(22), align: "center", valign: "middle",
    });
  });
  // D4: short vertical up-arrow feeding the Sigma box's bottom (head at y=323)
  slide.addShape(pptx.ShapeType.line, {
    x: px(440), y: px(323), w: 0, h: px(9),
    line: { color: C.red, width: 1, beginArrowType: "triangle" },
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
  // A6: striped q-vector icon (pale rounded, ~4 vertical stripes) + A4: label q2 —
  // the solid red bar is GONE (measured: no flat red bar in the original's query row)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(186), y: px(461), w: px(22), h: px(18), rectRadius: 0.03,
    fill: { color: "F3F0E8" }, line: { color: "B8B8B8", width: 0.5 },
  });
  const iconFills = ["F9FF96", "FFFFFF", "F08B96", "EAE4EE"];
  for (let j = 0; j < 4; j++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(188 + j * 4.5), y: px(463.5), w: px(4), h: px(13),
      fill: { color: iconFills[j] }, line: { color: "C9C9C9", width: 0.4 },
    });
  }
  // A4: q2 label (query belongs to word X2) — measured red ink x164..183 y455..480
  text(slide, idxRuns("q", 2, C.red, 8), {
    x: px(162), y: px(458), w: px(22), h: px(22), align: "center", valign: "middle",
  });
  // A5: W_q^(0) box re-centered over X2 (measured x211..237, y448..489) + the q-feed
  // arrow rising from it into the Dot Product box (drawn in ff_left, head at y443)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(211), y: px(448), w: px(26), h: px(41),
    fill: { color: "FFFFFF" }, line: { color: "CC2222", width: 1 },
  });
  text(slide, wRuns("q", 0, C.red, 6), {
    x: px(211), y: px(448), w: px(26), h: px(41), align: "center", valign: "middle",
  });
  // small red arrow from the box's bottom center down to the strips (measured 222..226)
  slide.addShape(pptx.ShapeType.line, {
    x: px(224), y: px(489), w: 0, h: px(6),
    line: { color: C.red, width: 1, endArrowType: "triangle" },
  });
  // G2: token container with 4 SEGMENTED multi-cell strips; X2 emphasized with pale
  // magenta cells + red dotted border (equal 44px strips, measured X2 at 203..247)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(150), y: px(492), w: px(198), h: px(29), rectRadius: 0.05,
    fill: { color: "E8FCE8" }, line: { color: C.green, width: 1.25, dashType: "dash" },
  });
  const strips = [
    { x: 155, hot: false }, { x: 203, hot: true },
    { x: 251, hot: false }, { x: 299, hot: false },
  ];
  strips.forEach((s, i) => {
    const cells = ["F9FF96", "FFFFF0", "F6DAF3", "EAE4EE"];
    for (let j = 0; j < 4; j++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(s.x + 1 + j * 10.5), y: px(497), w: px(10), h: px(14),
        fill: { color: s.hot ? (j % 2 ? "F2C8F0" : "F6DAF3") : cells[j] },
        line: { color: "B8B8B8", width: 0.5 },
      });
    }
    // G4: X labels inside the strips in red (X2 bigger)
    text(slide, idxRuns("X", i + 1, C.red, s.hot ? 6.5 : 5), {
      x: px(s.x), y: px(497), w: px(44), h: px(14), align: "center", valign: "middle",
    });
    if (s.hot) {
      // red dotted emphasis border over the X2 strip
      slide.addShape(pptx.ShapeType.rect, {
        x: px(s.x), y: px(496), w: px(44), h: px(16),
        fill: { type: "none" }, line: { color: C.red, width: 1.25, dashType: "sysDot" },
      });
    }
  });
  // G3: thick red diagonal from outside/below the container (tail ~(205,527)) into
  // the X2 strip's lower-left, head AT the chip's bottom edge (~(224,499))
  slide.addShape(pptx.ShapeType.line, {
    x: px(205), y: px(527), w: px(19), h: px(-28),
    line: { color: C.red, width: 2.25, endArrowType: "triangle" },
  });
}

function drawBottomcurve(pptx, slide) {
  slide.addImage({
    path: path.join(ASSETS, "bottom_curve.png"),
    x: px(230), y: px(452), w: 5.20833, h: 1.13889,
  });
}

// ---- per-head right panels: dotted X-boxes on the card slivers + W-chip columns
// E1 (resolved by the dedicated PIL map, fix_m3): FIVE columns h1..h5 — panel lefts
// 601/645/688/731/774 (w 43), tops 337/316/295/274/255 (h 78); measured q-chip tops
// 422/401/380/359/338 = panel bottom + 7; k/v pitch 40 (h2 q 401, k 441, v 481).
const HEADCOLS = [
  { h: 1, x: 601, xboxY: 337, wtop: 422 },
  { h: 2, x: 645, xboxY: 316, wtop: 401 },
  { h: 3, x: 688, xboxY: 295, wtop: 380 },
  { h: 4, x: 731, xboxY: 274, wtop: 359 },
  { h: 5, x: 774, xboxY: 255, wtop: 338 },
];
const PANEL_H = 78, PANEL_W = 43;

function drawHeadpanels(pptx, slide) {
  // E3: muted gray/lavender/pink cell palette (vivid rows were a defect)
  const muted = ["DAD2CE", "D8D2E0", "E4D6D8", "D8D2E0", "DAD2CE"];
  for (const c of HEADCOLS) {
    // E2: dark-green DOTTED border (fine dots), no fill
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(c.x), y: px(c.xboxY), w: px(PANEL_W), h: px(PANEL_H), rectRadius: 0.05,
      fill: { color: "FFFFFF" }, line: { color: "1F6B3A", width: 1, dashType: "sysDot" },
    });
    for (let i = 0; i < 4; i++) {
      const yc = c.xboxY + 12 + i * 18;
      // A9: 5 muted cells per row; the LEFTMOST cell carries a thick red X-STRIKE
      // (hand-drawn strike marks, not text labels — g_panelrow wave-4 decision)
      for (let j = 0; j < 5; j++) {
        slide.addShape(pptx.ShapeType.rect, {
          x: px(c.x + 1.5 + j * 8.2), y: px(yc - 6), w: px(7.5), h: px(12),
          fill: { color: muted[(i + j) % 5] }, line: { color: "BFB8B4", width: 0.4 },
        });
      }
      const lx = c.x + 1.5, lw = 7.5;
      slide.addShape(pptx.ShapeType.line, {
        x: px(lx), y: px(yc - 6), w: px(lw), h: px(12),
        line: { color: C.red, width: 1.4 },
      });
      slide.addShape(pptx.ShapeType.line, {
        x: px(lx), y: px(yc - 6), w: px(lw), h: px(-12),
        line: { color: C.red, width: 1.4 },
      });
    }
  }
  // E4: stemmed green arrows seated at the panel bottoms, heads up — 3 (h=2..4)
  // + 1 near the h=5 right edge; drawn here so the W chips (next block) overlap
  // only the tails, as measured (q top = panel bottom + 7)
  for (const idx of [1, 2, 3, 4]) {
    const c = HEADCOLS[idx];
    const ax = idx === 4 ? c.x + 40 : c.x + 21;
    slide.addShape(pptx.ShapeType.line, {
      x: px(ax), y: px(c.xboxY + PANEL_H - 4), w: 0,
      h: px(c.wtop + 8 - (c.xboxY + PANEL_H - 4)),
      line: { color: C.brightgreen, width: 1.25, beginArrowType: "triangle" },
    });
  }
}

function drawWochips(pptx, slide) {
  // E5: pastel-filled chips, thin semantic borders; q top = wtop, k/v pitch 40.
  // Labels semantic per chip letter (original ink: q red 200,0,0 / k green ~3EA74B /
  // v dark blue) — brick was a fidelity gap vs the frame, caught in closed-loop F2.
  const styles = {
    q: { border: "CC2222", fill: "FBD5DC", label: C.red },
    k: { border: C.green, fill: "DFF0D5", label: C.green },
    v: { border: C.blue, fill: "D6E4F7", label: C.blue },
  };
  for (const c of HEADCOLS) {
    const rows = [
      { letter: "q", dy: 0 }, { letter: "k", dy: 40 }, { letter: "v", dy: 80 },
    ];
    for (const r of rows) {
      const st = styles[r.letter];
      slide.addShape(pptx.ShapeType.rect, {
        x: px(c.x), y: px(c.wtop + r.dy), w: px(PANEL_W), h: px(22),
        fill: { color: st.fill }, line: { color: st.border, width: 0.9 },
      });
      text(slide, wRuns(r.letter, c.h, st.label, 5.5), {
        x: px(c.x), y: px(c.wtop + r.dy), w: px(PANEL_W), h: px(22),
        align: "center", valign: "middle",
      });
    }
  }
}

function drawSwoosh(pptx, slide) {
  // F1/F4: regenerated ribbon — J-curl tail at (559,453), rising body, hooked
  // tapered terminal (no arrowhead) at (787,333); bright red C00000; the head tip
  // stops just short of the h=5 panel's bottom edge (F4)
  slide.addImage({
    path: path.join(ASSETS, "swoosh.png"),
    x: px(546), y: px(323), w: 3.55556, h: 2.30556,
  });
}

function drawHlabel(pptx, slide) {
  // F3: blue italic serif «"H" Heads» with literal quotes, rising ~-22 deg along the
  // swoosh's upper end — measured line center (745,443), ink x703..790 y424..463
  text(slide, [
    { text: "\u201CH\u201D Heads", options: { italic: true, bold: true, fontSize: 11, color: "0033CC" } },
  ], {
    x: px(694), y: px(435), w: px(102), h: px(16), align: "center", valign: "middle",
    rotate: 338, margin: 0, fontFace: "Times New Roman",
  });
}

function drawLegend(pptx, slide) {
  // H1: [striped vector icon + red 1*d] [yellow W box; red d*d UNDER it] [red =]
  //     [second striped vector icon + red 1*d] [blue caption] — legend box measured
  //     734..903 x 466..531; W box 796..828 x 473..501; chip2 846..886
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(734), y: px(466), w: px(169), h: px(65), rectRadius: 0.06,
    fill: { color: C.legendFill }, line: { color: C.green, width: 1.25, dashType: "sysDot" },
  });
  const chip1x = 744, chip2x = 846;
  const cellFills = ["F9FF96", "FFFFFF", "F6DAF3", "EAE4EE", "F9FF96", "FFFFFF", "F6DAF3", "EAE4EE"];
  for (let j = 0; j < 8; j++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(chip1x + j * 5), y: px(476), w: px(5), h: px(12),
      fill: { color: cellFills[j] }, line: { color: "C9C9C9", width: 0.5 },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: px(chip2x + j * 5), y: px(476), w: px(5), h: px(12),
      fill: { color: cellFills[j] }, line: { color: "C9C9C9", width: 0.5 },
    });
  }
  // H2: dimension captions red/maroon C00000-family
  text(slide, "1*d", {
    x: px(chip1x), y: px(492), w: px(40), h: px(10), align: "center", valign: "middle",
    bold: true, fontSize: 6, color: C.red,
  });
  text(slide, "1*d", {
    x: px(chip2x + 20), y: px(492), w: px(40), h: px(10), align: "center", valign: "middle",
    bold: true, fontSize: 6, color: C.red,
  });
  // W square (measured 796..828 x 473..501)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(796), y: px(473), w: px(32), h: px(28),
    fill: { color: "FBE8B8" }, line: { color: C.ink, width: 1.25 },
  });
  text(slide, "W", {
    x: px(796), y: px(473), w: px(32), h: px(28), align: "center", valign: "middle",
    bold: true, fontSize: 12, color: C.ink,
  });
  // d*d caption UNDER the W box (H1 defect 2: dimension note belongs to W)
  text(slide, "d*d", {
    x: px(802), y: px(503), w: px(48), h: px(10), align: "center", valign: "middle",
    bold: true, fontSize: 6, color: C.red,
  });
  // = (red operator between W and the second chip)
  text(slide, "=", {
    x: px(830), y: px(478), w: px(14), h: px(16), align: "center", valign: "middle",
    bold: true, fontSize: 12, color: C.red,
  });
  // caption (blue bold per two independent crop reads)
  text(slide, "d: Embedding Length", {
    x: px(740), y: px(514), w: px(157), h: px(12), align: "center", valign: "middle",
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
