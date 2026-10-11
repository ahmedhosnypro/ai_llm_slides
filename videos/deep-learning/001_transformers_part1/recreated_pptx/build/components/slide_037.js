// components/slide_037.js — BLOCK-GRANULARITY component for slide 37,
// "Self Attention Mechanism (Adding Scaling)" (Deep Learning DSAI 308, lecture 001).
//
// DEPENDENCY LAW (founder directive 2026-10-11): slide 38 is this composition + a delta
// (green-bordered MatMul→SoftMax→Mask(opt.)→Scale→MatMul inset, drawn top-down). Children
// import THIS module and compose per block via opts.skip / opts.only — they must never
// re-derive or copy-paste this geometry. House chrome is NOT drawn here: the top-level
// build draws it ONCE via components/house_chrome.js with its own badge numeral.
//
// Geometry: PIL-measured from unique_slides/slide_037.jpg (960x540, 1px = 1pt = 1/72in),
// cross-checked with vision crop reads (qa evidence: scratch/slide037/v_*.txt).
// Measured structure (frame = ground truth):
//   - peach canvas x[53,866] y[107,522]
//   - title L1 y58-76 center x503; subtitle L2 y81-100 center x495 (red spans + subscripts)
//   - pills y[161,185]: Similarity x[271,336], Probabilities x[432,510], Weighted SUM x[598,690]
//   - 4 pipeline rows at y = 246 / 287 / 328 / 371
//   - left group: container x[58,142] y[226,394]; per row: 5-cell embedding block x[58,130]
//     (red X label over cells 2-3, rows top->bottom X4,X3,X2,X1) -> red arrow -> W_k box
//     x[152,194] (pale mint fill, GREEN border, black bold W_k^(1)) -> red row line at rowY
//     passing UNDER the K stack; K vector stack x[203,232] y[rowY-15,rowY-3] (thin vertical
//     cells) + red K label to its RIGHT x[237,250]; rows K4,K3,K2,K1 top->bottom.
//   - Dot Product box x[252,348] y[193,402], tan; maroon 2-line header; 4 navy dots on a
//     bottom-left->top-right diagonal (277,372)(295,328)(315,287)(331,246); thin red fan
//     lines from a convergence point (~300,392) up under each dot; the 4 row lines continue
//     through the box and out its right side to the Scaling box. Red "K.q" label at the
//     box's top-right corner x[346,368] y[199,211].
//   - Scaling box x[372,420] y[177,405], yellow, inner outlined rect, "Scaling by √d"
//     rotated 90 (reads top-to-bottom), orange; red stacked fraction K.q/√d (mathtext PNG,
//     bar at y206) at the box's top-RIGHT x[418,449] y[191,227].
//   - Soft max box x[459,489] y[194,402], pale purple, "Soft max" rotated 90, dark.
//   - 4 red ⊗ nodes (533,246)(561,287)(591,328)(621,369) d~16; arrows: softmax->⊗ (from
//     left), V rows->⊗ (from right, passing under the V stacks), ⊗->Σ verticals with
//     arrowheads at the Σ box bottom.
//   - Σ box x[514,656] y[195,218] pale cyan, blue Σ glyph ~26pt.
//   - Output: thick green arrow (548,164)->(578,150); short red arrow up into Y2's bottom
//     at x583; Y2 block x[548,620] y[122,146]: 7-cell segmented bar, green dashed border,
//     green bold Y2 label mid-bar.
//   - right group (mirror): container x[755,845]; per row: 5-cell embedding block x[766,838]
//     (rows top->bottom X4,X3,X2,X1 — symmetric with the K/V rows) -> W_v box x[700,745]
//     (pale cyan fill, NAVY border — measured, differs from W_k's green) <- arrows point
//     LEFT; V stack x[668,698] + red V label to its LEFT x[640,652]; rows V4,V3,V2,V1.
//   - sentence strip x[180,490] y[473,516]: 4 token blocks (X1[186,236] X2[262,338] magenta
//     highlight X3[341,391] X4[394,470], 5 pastel cells each, red label mid-block);
//     thick red block arrow below-left pointing up-right at X2; red arrow X2->W_q box
//     x[280,314] y[435,461] (white, RED border, red W_q^(1)); red arrow W_q->up past the
//     red q2 label (x[279,290]) and the 5-cell q2 vector x[305,337] y[413,425] into the
//     Dot box bottom at x298. Short dashed green stubs under both group containers.
//   - legend x[736,908] y[466,528] mint, dashed border (overhangs the canvas bottom-right
//     exactly as the original does): striped block x[750,776] y[471,483] -> "1×d" below;
//     yellow W square x[790,825] y[471,503] -> "d×d" below-right; "=" ; striped block
//     x[840,884] y[483,495] -> "1×d" below; blue "d: Embedding Length" caption at bottom.
// Colors: measured washed-JPEG values (frame is ground truth); thin red strokes C00000.
// Equations: mathtext -> 600dpi PNG -> addImage at EXACT size (Math equation format rule).

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets";

const px = (v) => v / 72; // frame px -> inches

// ---- palette (measured) ----
const C = {
  peach: "F7E2CD",
  containerFill: "E7FDE8",
  containerLine: "00B050",
  dotBox: "D8CBBC",
  dotBoxLine: "8B7B6C",
  dotHeaderText: "5C3A1E",
  scalingFill: "FAF36E",
  scalingInner: "DDBA3C",
  scalingText: "E8890C",
  softmaxFill: "F7DFF9",
  softmaxLine: "E0C7E8",
  softmaxText: "464646",
  sigmaFill: "EBFDFC",
  sigmaLine: "C9BEB2",
  sigmaGlyph: "333399",
  pillFill: "FCFEDD",
  pillText: "0033CC",
  wkFill: "DCFEE6",
  wkLine: "5FAF72",
  wvFill: "D4FBF7",
  wvLine: "26268F",
  red: "C00000",
  blockArrowRed: "E00000",
  navy: "3A3AA8",
  navyRing: "A9C0F5",
  greenArrow: "00B050",
  y2Line: "00B050",
  y2Text: "00B050",
  cellYellow: "FCFED0",
  cellGreen: "EDFEE0",
  cellWhite: "F2F2F4",
  cellLavender: "E4E6F5",
  cellPink: "F8DDEF",
  cellStripe: "C9C2B8",
  magenta: "DF92E4",
  magentaLine: "EE6FD5",
  legendFill: "E7FDE8",
  legendLine: "2E8B57",
  legendWsqu: "FAFBCE",
  legendBlue: "0070C0",
  black: "000000",
};

// 4 pipeline row center-y values (frame px)
const ROWS = [246, 287, 328, 371];

// ---------------------------------------------------------------- helpers
function stripedBlock(slide, pptx, x0, y0, x1, y1, cells, lineColor) {
  // cells: array of fill colors, drawn left-to-right inside [x0,x1]x[y0,y1]
  const n = cells.length;
  const w = (x1 - x0) / n;
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: "FFFFFF" }, line: { color: lineColor, width: 0.75 },
  });
  for (let i = 0; i < n; i++) {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: px(x0 + i * w), y: px(y0), w: px(w), h: px(y1 - y0),
      fill: { color: cells[i] }, line: { color: lineColor, width: 0.5 },
    });
  }
}

function arrow(slide, pptx, x1, y1, x2, y2, width, opts = {}) {
  if (width === 1.25) width = 1.1;
  slide.addShape(pptx.shapes.LINE, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: {
      color: opts.color || C.red, width: width,
      dashType: opts.dash || "solid",
      ...(opts.headAtStart
        ? { beginArrowType: "triangle" }
        : { endArrowType: "triangle" }),
    },
  });
}

function subLabel(slide, base, sub, opts) {
  // red bold label with true subscript, e.g. K4 -> "K" + "4"
  slide.addText(
    [
      { text: base, options: {} },
      { text: sub, options: { subscript: true, fontSize: Math.round(opts.fontSize * 0.62) } },
    ],
    Object.assign({ fontFace: "Arial", bold: true, color: C.red, margin: 0 }, opts)
  );
}

function matLabel(slide, mathtextPng, wIn, hIn, cxPx, cyPx) {
  slide.addImage({
    path: `${ASSETS}/${mathtextPng}`,
    x: px(cxPx) - wIn / 2, y: px(cyPx) - hIn / 2, w: wIn, h: hIn,
  });
}

// ---------------------------------------------------------------- blocks
function drawTitle(pptx, slide, opts) {
  slide.addText(
    [
      { text: "Self Attention Mechanism ", options: { color: C.black } },
      { text: "(Adding Scaling)", options: { color: C.red } },
    ],
    {
      x: px(203), y: px(53), w: px(600), h: px(28),
      align: "center", valign: "middle", fontSize: 20, bold: true,
      fontFace: "Arial", margin: 0,
    }
  );
  slide.addText(
    [
      { text: "(Self Attention of word ", options: { color: C.black } },
      { text: "X", options: { color: C.red } },
      { text: "2", options: { color: C.red, subscript: true, fontSize: 11 } },
      { text: " w.r.t All words in Sentence ( ", options: { color: C.black } },
      { text: "X", options: { color: C.red } },
      { text: "1", options: { color: C.red, subscript: true, fontSize: 11 } },
      { text: ", ", options: { color: C.red } },
      { text: "X", options: { color: C.red } },
      { text: "2", options: { color: C.red, subscript: true, fontSize: 11 } },
      { text: ", ", options: { color: C.red } },
      { text: "X", options: { color: C.red } },
      { text: "3", options: { color: C.red, subscript: true, fontSize: 11 } },
      { text: ", ", options: { color: C.red } },
      { text: "X", options: { color: C.red } },
      { text: "4", options: { color: C.red, subscript: true, fontSize: 11 } },
      { text: " )", options: { color: C.red } },
    ],
    {
      x: px(143), y: px(76), w: px(720), h: px(28),
      align: "center", valign: "middle", fontSize: 20.3, bold: true,
      fontFace: "Arial", margin: 0,
    }
  );
}

function drawCanvas(pptx, slide, opts) {
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: px(53), y: px(107), w: px(813), h: px(415),
    fill: { color: C.peach }, line: { type: "none" }, rectRadius: 0.08,
  });
}

const EMBED_CELLS = [C.cellYellow, C.cellGreen, C.cellWhite, C.cellLavender, C.cellPink];

function embeddingRow(pptx, slide, x0, x1, rowY, baseLabel, sub) {
  // 5-cell embedding block with red label over cells 2-3 (measured x93-105 / x796-808 band)
  stripedBlock(slide, pptx, x0, rowY - 9, x1, rowY + 9, EMBED_CELLS, "6B6B6B");
  const cx = x0 + (x1 - x0) * 0.49;
  slide.addText(
    [
      { text: baseLabel, options: {} },
      { text: sub, options: { subscript: true, fontSize: 6 } },
    ],
    {
      x: px(cx - 9), y: px(rowY - 8), w: px(20), h: px(16),
      align: "center", valign: "middle", fontSize: 10, bold: true,
      color: C.red, fontFace: "Arial", margin: 0,
    }
  );
}

function drawLeftGroup(pptx, slide, opts) {
  // container
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: px(58), y: px(226), w: px(84), h: px(168),
    fill: { color: C.containerFill },
    line: { color: C.containerLine, width: 1, dashType: "dash" },
    rectRadius: 0.06,
  });
  const subs = ["4", "3", "2", "1"];
  const kx0 = 203, kx1 = 232;
  for (let i = 0; i < 4; i++) {
    const y = ROWS[i];
    embeddingRow(pptx, slide, 58, 130, y, "X", subs[i]);
    arrow(slide, pptx, 131, y, 150, y, 1.25);
    // W_k box (green border, pale mint fill)
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: px(152), y: px(y - 13), w: px(42), h: px(26),
      fill: { color: C.wkFill }, line: { color: C.wkLine, width: 1.25 },
    });
    slide.addText(
      [
        { text: "W", options: {} },
        { text: "k", options: { subscript: true, fontSize: 6 } },
        { text: "(1)", options: { superscript: true, fontSize: 6 } },
      ],
      {
        x: px(152), y: px(y - 13), w: px(42), h: px(26),
        align: "center", valign: "middle", fontSize: 10, bold: true,
        color: C.black, fontFace: "Arial", margin: 0,
      }
    );
    // K vector stack (thin vertical cells) + red K label to its RIGHT, above the row line
    stripedBlock(slide, pptx, kx0, y - 15, kx1, y - 3,
      [C.cellYellow, C.cellYellow, C.cellLavender, C.cellLavender], "555555");
    subLabel(slide, "K", subs[i], {
      x: px(236), y: px(y - 16), w: px(15), h: px(15),
      align: "center", valign: "middle", fontSize: 11,
    });
  }
  // dashed green stub below the container (measured x~98, y394-406)
  arrow(slide, pptx, 98, 394, 98, 406, 1, { color: C.containerLine, dash: "dash" });
}

function drawRightGroup(pptx, slide, opts) {
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: px(755), y: px(226), w: px(90), h: px(168),
    fill: { color: C.containerFill },
    line: { color: C.containerLine, width: 1, dashType: "dash" },
    rectRadius: 0.06,
  });
  const subs = ["4", "3", "2", "1"];
  const vx0 = 668, vx1 = 698;
  for (let i = 0; i < 4; i++) {
    const y = ROWS[i];
    embeddingRow(pptx, slide, 766, 838, y, "X", subs[i]);
    // arrows point LEFT: from embedding block's left edge to the W_v box's right edge
    arrow(slide, pptx, 764, y, 747, y, 1.25);
    // W_v box (NAVY border, pale cyan fill — measured)
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: px(700), y: px(y - 13), w: px(45), h: px(26),
      fill: { color: C.wvFill }, line: { color: C.wvLine, width: 1.25 },
    });
    slide.addText(
      [
        { text: "W", options: {} },
        { text: "v", options: { subscript: true, fontSize: 6 } },
        { text: "(1)", options: { superscript: true, fontSize: 6 } },
      ],
      {
        x: px(700), y: px(y - 13), w: px(45), h: px(26),
        align: "center", valign: "middle", fontSize: 10, bold: true,
        color: C.black, fontFace: "Arial", margin: 0,
      }
    );
    // V vector stack + red V label to its LEFT, above the row line
    stripedBlock(slide, pptx, vx0, y - 15, vx1, y - 3,
      [C.cellYellow, C.cellYellow, C.cellWhite, C.cellPink], "555555");
    subLabel(slide, "V", subs[i], {
      x: px(639), y: px(y - 16), w: px(15), h: px(15),
      align: "center", valign: "middle", fontSize: 11,
    });
  }
  arrow(slide, pptx, 800, 396, 800, 408, 1, { color: C.containerLine, dash: "dash" });
}

const DOT_XY = [
  [331, 246], [315, 287], [295, 328], [277, 372],
];

function drawRowLines(pptx, slide, opts) {
  // the 4 long horizontal red pipeline lines at the row centers (drawn OVER the stage
  // boxes' fills, matching the frame): W_k boxes -> through the Dot box -> its dots;
  // Dot box -> Scaling box; Scaling -> Soft max; Soft max -> ⊗ nodes; V rows -> ⊗ nodes
  // (the V-side segments live in drawMultiplyNodes so the ⊗ heads stay above the circles).
  for (let i = 0; i < 4; i++) {
    const y = ROWS[i];
    const [dx] = DOT_XY[i];
    arrow(slide, pptx, 194, y, dx - 9, y, 1.25);        // W_k -> dot (head before the dot)
    arrow(slide, pptx, 348, y, 362, y, 1.25);           // Dot box -> Scaling box
    arrow(slide, pptx, 421, y, 447, y, 1.25);           // Scaling -> Soft max
    arrow(slide, pptx, 489, y, MULT_XY[i][0] - 13, y, 1.25); // Soft max -> ⊗
  }
}

function drawDotProduct(pptx, slide, opts) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(252), y: px(193), w: px(96), h: px(209),
    fill: { color: C.dotBox }, line: { color: C.dotBoxLine, width: 0.75 },
  });
  slide.addText(
    [
      { text: "Dot", options: { breakLine: true } },
      { text: "Product", options: {} },
    ],
    {
      x: px(252), y: px(196), w: px(96), h: px(34),
      align: "center", valign: "middle", fontSize: 12.5, bold: true,
      color: C.dotHeaderText, fontFace: "Arial", margin: 0, lineSpacing: 16,
    }
  );
  // fan lines from convergence point up under each dot (under the dots)
  for (const [dx, dy] of DOT_XY) {
    arrow(slide, pptx, 300, 392, dx - 1, dy + 6, 0.9);
  }
  // the four navy dots (pale blue ring)
  for (const [dx, dy] of DOT_XY) {
    slide.addShape(pptx.shapes.OVAL, {
      x: px(dx - 4.5), y: px(dy - 4.5), w: px(9), h: px(9),
      fill: { color: C.navy }, line: { color: C.navyRing, width: 1.5 },
    });
  }
  // red "K.q" mathtext label at the box's top-right corner
  matLabel(slide, "eq_Kq_037.png", 0.365, 0.20833, 357, 205);
}

function drawScaling(pptx, slide, opts) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(372), y: px(177), w: px(48), h: px(228),
    fill: { color: C.scalingFill }, line: { color: C.scalingInner, width: 0.75 },
  });
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(377), y: px(183), w: px(38), h: px(217),
    fill: { color: "FFF069" }, line: { color: C.scalingInner, width: 1 },
  });
  slide.addText("Scaling by √d", {
    x: px(372), y: px(177), w: px(48), h: px(228),
    rotate: 90, align: "center", valign: "middle",
    fontSize: 11, bold: true, color: C.scalingText, fontFace: "Arial", margin: 0,
  });
  // red stacked fraction K.q / √d — composed from mathtext parts + a drawn bar so each
  // part lands on the ORIGINAL's measured ink (closed-loop: num x[418,444] y[191,205],
  // bar x[418,449] y206, den x[424,448] y[208,226]; single-PNG dfrac was 9px off at top)
  slide.addImage({
    path: `${ASSETS}/eq_Kq_num_037.png`,
    x: px(431) - 0.33833 / 2, y: px(198) - 0.19333 / 2, w: 0.33833, h: 0.19333,
  });
  slide.addShape(pptx.shapes.LINE, {
    x: px(418), y: px(206), w: px(31), h: 0,
    line: { color: C.red, width: 1.5 },
  });
  slide.addImage({
    path: `${ASSETS}/eq_Sqrtd_037.png`,
    x: px(436) - 0.285 / 2, y: px(217) - 0.23333 / 2, w: 0.285, h: 0.23333,
  });
}

function drawSoftmax(pptx, slide, opts) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(459), y: px(194), w: px(30), h: px(208),
    fill: { color: C.softmaxFill }, line: { color: C.softmaxLine, width: 0.75 },
  });
  slide.addText("Soft max", {
    x: px(459), y: px(194), w: px(30), h: px(208),
    rotate: 90, align: "center", valign: "middle",
    fontSize: 11, bold: true, color: C.softmaxText, fontFace: "Arial", margin: 0,
  });
}

const MULT_XY = [
  [533, 246], [561, 287], [591, 328], [621, 369],
];

function drawMultiplyNodes(pptx, slide, opts) {
  // (softmax->⊗ segments are drawn in drawRowLines; here: V-side arrows, nodes, Σ arrows)
  for (let i = 0; i < 4; i++) {
    const y = ROWS[i];
    const [mx, my] = MULT_XY[i];
    // V row -> multiply node (from the right; line passes under the V stack)
    arrow(slide, pptx, 701, y, mx + 12, y, 1.25);
    // multiply node -> sigma (vertical, arrowhead at the sigma box bottom)
    arrow(slide, pptx, mx, my - 8, mx, 229, 1.25);
    // circled-X node
    slide.addShape(pptx.shapes.OVAL, {
      x: px(mx - 8), y: px(my - 8), w: px(16), h: px(16),
      fill: { type: "none" }, line: { color: C.red, width: 1.5 },
    });
    slide.addShape(pptx.shapes.LINE, {
      x: px(mx - 4.5), y: px(my - 4.5), w: px(9), h: px(9),
      line: { color: C.red, width: 1.5 },
    });
    slide.addShape(pptx.shapes.LINE, {
      x: px(mx - 4.5), y: px(my - 4.5), w: px(9), h: px(9),
      flipV: true, line: { color: C.red, width: 1.5 },
    });
  }
}

function drawSigma(pptx, slide, opts) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(514), y: px(195), w: px(138), h: px(25),
    fill: { color: C.sigmaFill }, line: { color: C.sigmaLine, width: 0.75 },
  });
  slide.addText("Σ", {
    x: px(514), y: px(195), w: px(138), h: px(25),
    align: "center", valign: "middle", fontSize: 26, bold: true,
    color: C.sigmaGlyph, fontFace: "Arial", margin: 0,
  });
}

function drawOutput(pptx, slide, opts) {
  // thick green block arrow toward Y2
  arrow(slide, pptx, 548, 164, 578, 150, 4.5, { color: C.greenArrow });
  // short red arrow up into Y2's bottom edge
  arrow(slide, pptx, 583, 158, 583, 148, 1.25);
  // Y2 segmented bar with green dashed border
  stripedBlock(slide, pptx, 548, 122, 620, 146,
    ["CFE8C8", "C9D6C4", "CFE8C8", "C9D6C4", "CFE8C8", "C9D6C4", "CFE8C8"], "777777");
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(548), y: px(122), w: px(72), h: px(24),
    fill: { type: "none" },
    line: { color: C.y2Line, width: 1, dashType: "dash" },
  });
  slide.addText(
    [
      { text: "Y", options: {} },
      { text: "2", options: { subscript: true, fontSize: 8 } },
    ],
    {
      x: px(566), y: px(124), w: px(36), h: px(20),
      align: "center", valign: "middle", fontSize: 13, bold: true,
      color: C.y2Text, fontFace: "Arial", margin: 0,
    }
  );
}

function drawPills(pptx, slide, opts) {
  const pills = [
    ["Similarity", 271, 336],
    ["Probabilities", 428, 514],
    ["Weighted SUM", 596, 691],
  ];
  for (const [label, x0, x1] of pills) {
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: px(x0), y: px(161), w: px(x1 - x0), h: px(24),
      fill: { color: C.pillFill }, line: { color: "CFC7AE", width: 1 }, rectRadius: 0.1,
    });
    slide.addText(label, {
      x: px(x0), y: px(161), w: px(x1 - x0), h: px(24),
      align: "center", valign: "middle", fontSize: 11, bold: true,
      color: C.pillText, fontFace: "Arial", margin: 0,
    });
  }
}

function drawSentenceStrip(pptx, slide, opts) {
  // container
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: px(180), y: px(473), w: px(310), h: px(43),
    fill: { color: C.containerFill },
    line: { color: C.containerLine, width: 1, dashType: "dash" },
    rectRadius: 0.06,
  });
  // token blocks: [x0, x1, magenta?]
  const toks = [
    [186, 236, false, "1"],
    [262, 338, true, "2"],
    [341, 391, false, "3"],
    [394, 470, false, "4"],
  ];
  for (const [x0, x1, mag, sub] of toks) {
    stripedBlock(slide, pptx, x0, 483, x1, 503,
      mag
        ? [C.magenta, C.magenta, C.magenta, C.magenta, C.magenta]
        : [C.cellYellow, C.cellGreen, C.cellWhite, C.cellLavender, C.cellPink],
      mag ? C.magentaLine : "6B6B6B");
    slide.addText(
      [
        { text: "X", options: {} },
        { text: sub, options: { subscript: true, fontSize: 6 } },
      ],
      {
        x: px((x0 + x1) / 2 - 10), y: px(485), w: px(20), h: px(16),
        align: "center", valign: "middle", fontSize: 10, bold: true,
        color: C.red, fontFace: "Arial", margin: 0,
      }
    );
  }
  // thick red block arrow below-left, pointing up-right at X2
  arrow(slide, pptx, 270, 527, 295, 509, 5, { color: C.blockArrowRed });
  // X2 -> W_q (up)
  arrow(slide, pptx, 298, 473, 298, 463, 1.25);
  // W_q box (white, RED border, red W_q^(1))
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(280), y: px(435), w: px(34), h: px(26),
    fill: { color: "FFFFFF" }, line: { color: C.red, width: 1.25 },
  });
  slide.addText(
    [
      { text: "W", options: {} },
      { text: "q", options: { subscript: true, fontSize: 6 } },
      { text: "(1)", options: { superscript: true, fontSize: 6 } },
    ],
    {
      x: px(280), y: px(435), w: px(34), h: px(26),
      align: "center", valign: "middle", fontSize: 9.5, bold: true,
      color: C.red, fontFace: "Arial", margin: 0,
    }
  );
  // W_q -> Dot Product bottom (up), with q2 label + q2 vector beside it
  arrow(slide, pptx, 298, 434, 298, 406, 1.25);
  subLabel(slide, "q", "2", {
    x: px(277), y: px(412), w: px(16), h: px(15),
    align: "center", valign: "middle", fontSize: 11,
  });
  stripedBlock(slide, pptx, 305, 413, 337, 425,
    [C.cellYellow, C.cellYellow, C.cellGreen, C.cellLavender, C.cellPink], "555555");
}

function drawLegend(pptx, slide, opts) {
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: px(736), y: px(466), w: px(172), h: px(62),
    fill: { color: C.legendFill },
    line: { color: C.legendLine, width: 1, dashType: "dash" },
    rectRadius: 0.06,
  });
  // left striped block (1×d input vector)
  stripedBlock(slide, pptx, 750, 471, 776, 483,
    [C.cellYellow, C.cellYellow, C.cellWhite, C.cellLavender], "555555");
  matLabel(slide, "eq_1xd_037.png", 0.27667, 0.12167, 786, 489);
  // W square
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(790), y: px(471), w: px(35), h: px(32),
    fill: { color: C.legendWsqu }, line: { color: C.dotBoxLine, width: 1 },
  });
  slide.addText("W", {
    x: px(790), y: px(471), w: px(35), h: px(32),
    align: "center", valign: "middle", fontSize: 15, bold: true,
    color: C.black, fontFace: "Arial", margin: 0,
  });
  // =
  slide.addText("=", {
    x: px(825), y: px(478), w: px(14), h: px(18),
    align: "center", valign: "middle", fontSize: 12, bold: true,
    color: C.red, fontFace: "Arial", margin: 0,
  });
  // right striped block (output vector)
  stripedBlock(slide, pptx, 846, 483, 882, 495,
    [C.cellYellow, C.cellYellow, C.cellWhite, C.cellLavender, C.cellPink], "555555");
  matLabel(slide, "eq_1xd_037.png", 0.27667, 0.12167, 877, 501);
  matLabel(slide, "eq_dxd_037.png", 0.285, 0.12167, 840, 511);
  // blue caption
  slide.addText("d: Embedding Length", {
    x: px(744), y: px(515), w: px(156), h: px(14),
    align: "center", valign: "middle", fontSize: 9.5, bold: true,
    color: C.legendBlue, fontFace: "Arial", margin: 0,
  });
}

// ---------------------------------------------------------------- registry
const BLOCKS = [
  "canvas", "title", "pills", "leftGroup", "rightGroup", "dotProduct",
  "scaling", "softmax", "rowLines", "sigma", "multiply", "output", "strip", "legend",
];

/**
 * Draw slide 37's full composition at block granularity.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide to draw on (house chrome already drawn by the caller)
 * @param {object} opts  { skip: string[] , only: string[] } — block selectors per the
 *                       dependency law (children compose per block, never erase)
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  const want = (n) => !skip.has(n) && (!only || only.has(n));
  // z-order: canvas -> containers/groups -> stage boxes -> arrows/nodes -> overlays
  if (want("canvas")) drawCanvas(pptx, slide, opts);
  if (want("leftGroup")) drawLeftGroup(pptx, slide, opts);
  if (want("rightGroup")) drawRightGroup(pptx, slide, opts);
  if (want("dotProduct")) drawDotProduct(pptx, slide, opts);
  if (want("scaling")) drawScaling(pptx, slide, opts);
  if (want("softmax")) drawSoftmax(pptx, slide, opts);
  if (want("rowLines")) drawRowLines(pptx, slide, opts);
  if (want("sigma")) drawSigma(pptx, slide, opts);
  if (want("multiply")) drawMultiplyNodes(pptx, slide, opts);
  if (want("output")) drawOutput(pptx, slide, opts);
  if (want("pills")) drawPills(pptx, slide, opts);
  if (want("strip")) drawSentenceStrip(pptx, slide, opts);
  if (want("legend")) drawLegend(pptx, slide, opts);
  if (want("title")) drawTitle(pptx, slide, opts);
}

module.exports = { renderBase, BLOCKS, ROWS, C };
