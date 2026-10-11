// slide_033.js — "Self Attention Mechanism (Linear Transformation of Inputs)"
// Deep Learning DSAI 308, Transformers — Part I. Build worker attempt 1, 2026-10-11.
//
// ROOT build (no dependency parents; gen gate + dep gate pass). Frame-true recreation:
// ALL geometry below is PIL-measured from unique_slides/slide_033.jpg (960x540, 1px = 1pt
// = 1/72 in) — scratch/slide033/ passes w1..w6 + the prior worker's f/p passes — plus
// gated crop reads banked in scratch/slide033/crops2/ (q1..q4) and crops/ vread_A..K.
//
// FRAME-VS-SPEC corrections applied at build (frame is ground truth; recorded in
// worker_report.md):
//   * embedding widgets are FIVE-cell strips with the label in the CENTER cell (spec
//     said "white box + 3 squares"); cell palette pale yellow/green/peach/periwinkle/
//     lavender (q3 read), thin gray-olive dividers.
//   * side-container rows read X4,X3,X2,X1 top->bottom (q3 read) — pairs row-wise with
//     K4..K1 / V4..V1 exactly as SOURCES.md anticipated; spec's [?] resolved.
//   * W-matrix labels read W_k^(r) / W_v^(r) / W_q^(r): superscript "(r)" in a lighter
//     tan-olive, NOT "(1)" (two independent high-zoom reads: crops/vread_F + crops2/q1).
//   * Dot-Product corner label reads "K.q" — NO subscript (crops2/q2); spec's "K2q [?]"
//     superscript-2 was a dot misread.
//   * legend labels are "1*d" / "d*d" with LITERAL asterisks and baseline d, no
//     middle-dot separator (crops2/q4 + crops/vread_H); caption "d: Embedding Length"
//     is bold navy-blue; "=" is red-brown.
//   * pill text is indigo-blue (#3F3F8E), not dark red (crops/vread_K + cores).
//   * the peach diagram panel (F7E2CD, thin gray border) sits INSET on the chrome gray
//     panel (x51..868, y107..522 frame px) — the spec's full-panel maroon-border reading
//     was the chrome's own red strokes bleeding into the JPEG.
//   * connectors: only the RIGHT vertical dashed green (x802, y~402..472, arrowhead up
//     into the right container, lower end running behind the legend) + a small green
//     up-arrowhead stub under the LEFT container; the spec's full L-shaped left connector
//     and horizontal segment are NOT in the frame (pixel-verified empty peach).
//   * no visible softmax->circle lines; only short right stubs w/ left arrowheads at
//     circles rows 2-4 (row 1 has none — pixel-verified).
//
// LAWS honored: playlist chrome via components/house_chrome.js (badge numeral 33 = the
// number printed on the frame); verbatim text; margin:0 + explicit fontFace on every
// text element; explicit lineSpacing on both multi-line boxes (title 24pt, Dot/Product
// 13pt); no '#' in hex; single-version plain-named deliverable; banking obligation
// (002 depends on this slide) via renderBase export in build/components/slide_033.js.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js"
);

const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt)
const FONT = "Arial";

// ---- palette (measured cores) --------------------------------------------------
const C = {
  peachPanel: "F7E2CD", panelBorder: "C9C5C0",
  containerFill: "E7FFE9", containerBorder: "4E7D52",
  band: "F7F96B", boxBorder: "5E8A50",
  dpFill: "DCCBBB", dpBorder: "A69B90", dpTitle: "6E5133",
  softFill: "F8DDFC", softBorder: "C0AEC0", softText: "7B217B",
  sigmaFill: "EAFEFC", sigmaBorder: "C3C7C6", sigmaText: "000083",
  red: "C03030", redDark: "A50D1E", labelRed: "8E2222", titleRed: "990C28",
  orange: "C5700A", olive: "6B7D00", supTan: "A08A28",
  navy: "000083", capBlue: "1A2470", pillText: "3F3F8F",
  titleBlue: "000078", green: "0E9B4C", y2Border: "7FA37C",
  cell1: "EFF5C3", cell2: "F3F9D9", cell3: "FBDFD2", cell4: "DFE5F0", cell5: "ECDEF0",
  divider: "B5AFA2",
  x2c1: "F4AECB", x2c2: "F2BEDA", x2c3: "F293C2", x2c4: "E295D6", x2c5: "DC88CE",
  x2border: "BE4148",
  y2c1: "9CCB96", y2c4: "C9D6DA",
  legW: "FFFBD1", legWBorder: "C87A2A", legendRed: "A0392E", eqSign: "8F4A2E",
  kq: "7A231C", qRed: "800007",
  dotCore: "0D1B8F", dotHalo: "9FC5F0",
  grayLine: "A9A5A0", greenArrow: "4E9A4E", greenArrowLine: "2F6B2F",
  triRed: "8F2020", emph: "A00000",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pres.addSlide();

// ---- 1) playlist house chrome (badge numeral 33) -------------------------------
drawHouseChrome(pres, slide, { numeral: 33 });

// ---- 2) peach diagram panel (inset on the chrome panel) ------------------------
slide.addShape(pres.ShapeType.rect, {
  x: px(51), y: px(107), w: px(817), h: px(415),
  fill: { color: C.peachPanel }, line: { color: C.panelBorder, width: 1 },
});

// ---- helpers --------------------------------------------------------------------
// 5-cell embedding widget with a red X label in the center cell
function embedWidget(x, y, w, h, label, cells) {
  const cw = w / 5;
  const fills = cells || [C.cell1, C.cell2, C.cell3, C.cell4, C.cell5];
  for (let i = 0; i < 5; i++) {
    slide.addShape(pres.ShapeType.rect, {
      x: px(x + i * cw), y: px(y), w: px(cw), h: px(h),
      fill: { color: fills[i] }, line: { color: C.divider, width: 0.5 },
    });
  }
  if (label) {
    slide.addText(
      [
        { text: "X", options: {} },
        { text: label, options: { subscript: true } },
      ],
      {
        x: px(x + 1.5 * cw), y: px(y - 2), w: px(2 * cw), h: px(h + 4),
        align: "center", valign: "middle", margin: 0,
        fontFace: FONT, fontSize: 11, bold: true, color: C.labelRed,
      }
    );
  }
}
// 5-cell mini vector (no label)
function miniVector(x, y, w, h) {
  embedWidget(x, y, w, h, null);
}
// horizontal red arrow (pptxgenjs line; end = arrow end)
function redArrow(x1, y1, x2, y2, width, opts = {}) {
  slide.addShape(pres.ShapeType.line, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: {
      color: opts.color || C.red, width: width || 1.25,
      endArrowType: opts.head === false ? undefined : "triangle",
      dashType: opts.dash,
    },
  });
}
// small solid triangle pointing right/left (orange arrowheads on the W-box borders)
function tri(x, y, w, h, dir, color) {
  slide.addShape(pres.ShapeType.triangle, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    rotate: dir === "right" ? 90 : 270,
    fill: { color: color || C.orange }, line: { type: "none" },
  });
}

// ---- 3) sentence row (bottom) ----------------------------------------------------
slide.addShape(pres.ShapeType.roundRect, {
  x: px(177), y: px(473), w: px(315), h: px(44), rectRadius: 0.06,
  fill: { color: C.containerFill },
  line: { color: C.containerBorder, width: 1.25, dashType: "sysDot" },
});
embedWidget(189, 481, 66, 24, "1");
embedWidget(257, 481, 75, 24, "2", [C.x2c1, C.x2c2, C.x2c3, C.x2c4, C.x2c5]);
// magenta dotted highlight border over the X2 widget
slide.addShape(pres.ShapeType.roundRect, {
  x: px(255), y: px(479), w: px(79), h: px(28), rectRadius: 0.04,
  fill: { type: "none" },
  line: { color: C.x2border, width: 1.5, dashType: "sysDot" },
});
embedWidget(335, 481, 66, 24, "3");
embedWidget(403, 481, 66, 24, "4");

// ---- 4) connectors (dashed green) -----------------------------------------------
// right vertical: from behind the legend up into the right container bottom
slide.addShape(pres.ShapeType.line, {
  x: px(802), y: px(402), w: 0, h: px(70),
  line: { color: C.containerBorder, width: 1.25, dashType: "sysDot" },
});
slide.addShape(pres.ShapeType.triangle, {
  x: px(795), y: px(392), w: px(14), h: px(14),
  fill: { color: C.containerBorder }, line: { type: "none" },
});
// left stub: small green up-arrowhead under the left container bottom border
slide.addShape(pres.ShapeType.triangle, {
  x: px(92), y: px(392), w: px(14), h: px(14),
  fill: { color: C.containerBorder }, line: { type: "none" },
});

// ---- 5) side input containers (rows read X4..X1 top->bottom) ----------------------
slide.addShape(pres.ShapeType.roundRect, {
  x: px(58), y: px(226), w: px(82), h: px(170), rectRadius: 0.08,
  fill: { color: C.containerFill },
  line: { color: C.containerBorder, width: 1.25, dashType: "sysDot" },
});
slide.addShape(pres.ShapeType.roundRect, {
  x: px(763), y: px(226), w: px(83), h: px(170), rectRadius: 0.08,
  fill: { color: C.containerFill },
  line: { color: C.containerBorder, width: 1.25, dashType: "sysDot" },
});
const ROWY = [237, 278, 319, 363];
const ROWLBL = ["4", "3", "2", "1"];
ROWY.forEach((y, i) => {
  embedWidget(66, y, 65, 17, ROWLBL[i]);
  embedWidget(771, y, 67, 17, ROWLBL[i]);
});

// ---- 6) Dot Product box (drawn BEFORE the flow lines so they stay visible) ----------
slide.addShape(pres.ShapeType.rect, {
  x: px(255), y: px(194), w: px(87), h: px(208),
  fill: { color: C.dpFill }, line: { color: C.dpBorder, width: 1 },
});
slide.addText(
  [
    { text: "Dot", options: { breakLine: true } },
    { text: "Product", options: {} },
  ],
  {
    x: px(262), y: px(196), w: px(72), h: px(34),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 11, bold: true, color: C.dpTitle, lineSpacing: 13,
  }
);
slide.addText(
  [
    { text: "K", options: {} },
    { text: ".", options: {} },
    { text: "q", options: {} },
  ],
  {
    x: px(332), y: px(196), w: px(26), h: px(17),
    align: "left", valign: "top", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 9, bold: true, color: C.kq,
  }
);
// dots: pale-blue halo + navy core, diagonal staircase (on top of the flow lines)
const DOTC = [
  [330, 246], [314, 287], [296, 328], [277, 372],
];
DOTC.forEach(([cx, cy]) => {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 6.5), y: px(cy - 6.5), w: px(13), h: px(13),
    fill: { color: C.dotHalo }, line: { color: "6F8FC0", width: 0.5 },
  });
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 3.5), y: px(cy - 3.5), w: px(7), h: px(7),
    fill: { color: C.dotCore }, line: { type: "none" },
  });
});

// ---- 7) K/V flow lines UNDER the W bands (long reds, occluded by boxes) ------------
const LINEY = [247.5, 288, 329, 372.5];
const DOTX = [330, 314, 296, 277];
// container -> W_k box (short, red) — orange heads added later, on top
LINEY.forEach((y) => redArrow(139, y, 149, y, 1.5, { head: false }));
// W_k box -> DP dot (long, red, arrowhead at the dot; crosses the DP border)
LINEY.forEach((y, i) => redArrow(200, y, DOTX[i] - 8, y, 1.25));
// right container -> W_v box (short, red)
LINEY.forEach((y) => redArrow(763, y, 753, y, 1.5, { head: false }));
// converging red lines from the bottom convergence point up to each dot
DOTC.forEach(([cx, cy]) => {
  slide.addShape(pres.ShapeType.line, {
    x: px(Math.min(cx, 300)), y: px(cy), w: px(Math.abs(cx - 300)), h: px(399 - cy),
    flipV: cx > 300,
    line: { color: C.red, width: 1 },
  });
});

// ---- 7) W_k / W_v yellow bands + four bordered boxes each --------------------------
slide.addShape(pres.ShapeType.rect, {
  x: px(150), y: px(226), w: px(50), h: px(166),
  fill: { color: C.band }, line: { type: "none" },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(698), y: px(229), w: px(50), h: px(166),
  fill: { color: C.band }, line: { type: "none" },
});
const BOXY = [234, 276, 316, 360];
function wBox(x, y, w, h, sub) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: C.band }, line: { color: C.boxBorder, width: 1 },
  });
  slide.addText(
    [
      { text: "W", options: {} },
      { text: sub, options: { subscript: true } },
      { text: "(r)", options: { superscript: true, color: C.supTan, fontSize: 6.5 } },
    ],
    {
      x: px(x), y: px(y), w: px(w), h: px(h),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 11, bold: true, color: C.olive,
    }
  );
}
BOXY.forEach((y) => wBox(150, y, 50, 24, "k"));
BOXY.forEach((y) => wBox(698, y, 50, 24, "v"));

// ---- 8) K/V vectors + labels (above the flow lines) --------------------------------
const KVEC = [231, 272, 313, 357];
KVEC.forEach((y) => miniVector(204, y, 33, 12));
KVEC.forEach((y) => miniVector(667, y, 31, 12));
const KLBL = ["4", "3", "2", "1"];
KLBL.forEach((s, i) => {
  slide.addText(
    [
      { text: "K", options: {} },
      { text: s, options: { subscript: true } },
    ],
    {
      x: px(236), y: px(KVEC[i] - 2), w: px(20), h: px(17),
      align: "left", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 11, bold: true, color: C.labelRed,
    }
  );
  slide.addText(
    [
      { text: "V", options: {} },
      { text: s, options: { subscript: true } },
    ],
    {
      x: px(638), y: px([227, 269, 316, 360][i]), w: px(20), h: px(16),
      align: "left", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 11, bold: true, color: C.labelRed,
    }
  );
});

// ---- 10) Softmax bar ------------------------------------------------------------------
slide.addShape(pres.ShapeType.roundRect, {
  x: px(458), y: px(194), w: px(33), h: px(209), rectRadius: 0.08,
  fill: { color: C.softFill }, line: { color: C.softBorder, width: 1 },
});
slide.addText("Soft max", {
  x: px(447), y: px(283), w: px(55), h: px(30), rotate: 90,
  align: "center", valign: "middle", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 11, bold: true, color: C.softText,
});

// ---- 11) dot -> softmax faint arrows ----------------------------------------------------
DOTC.forEach(([cx, cy], i) => {
  redArrow(cx + 7, LINEY[i], 455, LINEY[i], 0.75);
});

// ---- 12) Sigma box + circles + stems -----------------------------------------------------
slide.addShape(pres.ShapeType.rect, {
  x: px(516), y: px(194), w: px(135), h: px(25),
  fill: { color: C.sigmaFill }, line: { color: C.sigmaBorder, width: 1 },
});
slide.addText("\u03A3", {
  x: px(516), y: px(194), w: px(135), h: px(25),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 16, bold: true, color: C.sigmaText,
});
const CIRC = [
  [532, 246], [563, 288], [592, 328], [622, 372],
];
CIRC.forEach(([cx, cy]) => {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 9.5), y: px(cy - 9.5), w: px(19), h: px(19),
    fill: { color: "FFFFFF" }, line: { color: C.red, width: 1.5 },
  });
  slide.addText("*", {
    x: px(cx - 9.5), y: px(cy - 9.5), w: px(19), h: px(19),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 14, bold: true, color: C.red,
  });
});
// stems: circles -> Sigma (arrowheads land under the Sigma box)
redArrow(531, 241, 531, 225, 1);
redArrow(563, 283, 563, 225, 1);
redArrow(592, 323, 592, 225, 1);
redArrow(623, 367, 623, 225, 1);
// short right stubs with left-pointing arrowheads (rows 2-4 only, as measured)
redArrow(584, LINEY[1], 574, LINEY[1], 1.25);
redArrow(612, LINEY[2], 594, LINEY[2], 1.25);
redArrow(643, LINEY[3], 624, LINEY[3], 1.25);

// ---- 13) query path -----------------------------------------------------------------------
// W_q box
slide.addShape(pres.ShapeType.rect, {
  x: px(271), y: px(428), w: px(51), h: px(40),
  fill: { color: C.band }, line: { color: C.boxBorder, width: 1 },
});
slide.addText(
  [
    { text: "W", options: {} },
    { text: "q", options: { subscript: true } },
    { text: "(r)", options: { superscript: true, color: C.supTan, fontSize: 6.5 } },
  ],
  {
    x: px(271), y: px(428), w: px(51), h: px(40),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 12, bold: true, color: C.olive,
  }
);
// q2 label + vector
slide.addText(
  [
    { text: "q", options: {} },
    { text: "2", options: { subscript: true } },
  ],
  {
    x: px(277), y: px(407), w: px(26), h: px(22),
    align: "left", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 12, bold: true, color: C.qRed,
  }
);
miniVector(304, 414, 34, 12);
// W_q -> DP box arrow (up, through q2)
redArrow(299, 433, 299, 407, 1.5);
// X2 -> W_q (short up arrow into the yellow box bottom; pixel-verified head tip ~y462)
redArrow(299, 475, 299, 464, 1.25);

// ---- 14) Y2 output widget + arrows -----------------------------------------------------------
const y2cells = [C.y2c1, C.y2c1, C.y2c1, C.y2c4, C.y2c4];
for (let i = 0; i < 5; i++) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(549 + i * 14), y: px(121), w: px(14), h: px(25),
    fill: { color: y2cells[i] }, line: { color: C.y2Border, width: 0.5 },
  });
}
slide.addShape(pres.ShapeType.rect, {
  x: px(549), y: px(121), w: px(70), h: px(25),
  fill: { type: "none" }, line: { color: C.y2Border, width: 1, dashType: "sysDot" },
});
slide.addText("Y", {
  x: px(575), y: px(123), w: px(17), h: px(21),
  align: "center", valign: "middle", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 13, bold: true, color: C.green,
});
slide.addText("2", {
  x: px(584), y: px(134), w: px(8), h: px(12),
  align: "left", valign: "bottom", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 7.5, bold: true, color: C.green,
});
// green block arrow (Sigma -> Y2), red triangle head + thin gray guide line
slide.addShape(pres.ShapeType.rightArrow, {
  x: px(548), y: px(149), w: px(30), h: px(16), rotate: 315,
  fill: { color: C.greenArrow }, line: { color: C.greenArrowLine, width: 0.75 },
});
slide.addShape(pres.ShapeType.triangle, {
  x: px(579), y: px(146), w: px(8), h: px(8),
  fill: { color: C.triRed }, line: { type: "none" },
});
slide.addShape(pres.ShapeType.line, {
  x: px(583), y: px(156), w: 0, h: px(38),
  line: { color: C.grayLine, width: 0.75 },
});

// ---- 15) stage pills --------------------------------------------------------------------------
function pill(x, y, w, h, text) {
  slide.addShape(pres.ShapeType.roundRect, {
    x: px(x), y: px(y), w: px(w), h: px(h), rectRadius: 0.12,
    fill: { color: "FFFFE3" },
    line: { color: "8AA88A", width: 1, dashType: "sysDot" },
  });
  slide.addText(text, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 11, bold: true, color: C.pillText,
  });
}
pill(271, 163, 67, 22, "Similarity");
pill(429, 161, 86, 22, "Probabilities");
pill(596, 161, 95, 23, "Weighted SUM");

// ---- 16) dimension legend (bottom right) --------------------------------------------------------
slide.addShape(pres.ShapeType.roundRect, {
  x: px(736), y: px(467), w: px(165), h: px(63), rectRadius: 0.08,
  fill: { color: C.containerFill },
  line: { color: C.containerBorder, width: 1.25, dashType: "sysDot" },
});
const legCells = ["F2F4C6", "F6F8D6", "FAEDD2", "EFE2EC", "F5E1EE"];
function legendStrip(x, y, w, h) {
  const cw = w / 5;
  for (let i = 0; i < 5; i++) {
    slide.addShape(pres.ShapeType.rect, {
      x: px(x + i * cw), y: px(y), w: px(cw), h: px(h),
      fill: { color: legCells[i] }, line: { color: C.divider, width: 0.5 },
    });
  }
}
legendStrip(753, 470, 32, 15);
legendStrip(842, 478, 40, 15);
slide.addText(
  [
    { text: "1", options: {} },
    { text: "*", options: {} },
    { text: "d", options: {} },
  ],
  {
    x: px(773), y: px(484), w: px(21), h: px(16),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 8.5, bold: true, color: C.legendRed,
  }
);
slide.addShape(pres.ShapeType.rect, {
  x: px(798), y: px(472), w: px(29), h: px(29),
  fill: { color: C.legW }, line: { color: C.legWBorder, width: 1.5 },
});
slide.addText("W", {
  x: px(798), y: px(472), w: px(29), h: px(29),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 14, bold: true, color: "000000",
});
slide.addText(
  [
    { text: "d", options: {} },
    { text: "*", options: {} },
    { text: "d", options: {} },
  ],
  {
    x: px(794), y: px(500), w: px(36), h: px(15),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 9, bold: true, color: C.legendRed,
  }
);
slide.addText("=", {
  x: px(827), y: px(477), w: px(13), h: px(21),
  align: "center", valign: "middle", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 11, bold: true, color: C.eqSign,
});
slide.addText(
  [
    { text: "1", options: {} },
    { text: "*", options: {} },
    { text: "d", options: {} },
  ],
  {
    x: px(869), y: px(496), w: px(21), h: px(16),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 8.5, bold: true, color: C.legendRed,
  }
);
slide.addText("d: Embedding Length", {
  x: px(746), y: px(509), w: px(148), h: px(18),
  align: "center", valign: "middle", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 10, bold: true, color: C.capBlue,
});

// ---- 17) orange arrowheads on the W-box borders (on top) ------------------------------------------
LINEY.forEach((y) => tri(142, y - 4.5, 8, 9, "right"));
LINEY.forEach((y) => tri(741, y - 4.5, 8, 9, "left"));

// ---- 18) emphasis overlays -------------------------------------------------------------------------
// translucent dark-red circle over the K2 row
slide.addShape(pres.ShapeType.ellipse, {
  x: px(215), y: px(301), w: px(36), h: px(36),
  fill: { color: C.emph, transparency: 35 }, line: { type: "none" },
});
// chunky red block arrow pointing up-right at X2
slide.addShape(pres.ShapeType.rightArrow, {
  x: px(263), y: px(511), w: px(26), h: px(14), rotate: 332,
  fill: { color: C.redDark }, line: { type: "none" },
});

// ---- 19) title (two lines as separate pinned boxes; frame pitch 24px) ----------------
// L1 ink: caps y58..72; L2 ink: y82..96 (measured). Separate boxes pin the pitch in
// BOTH renderers (LO tightened the 24pt spcPts on the merged paragraph).
slide.addText(
  [
    { text: "Self Attention Mechanism ", options: { color: "000000" } },
    { text: "(Linear Transformation of Inputs)", options: { color: C.titleBlue } },
  ],
  {
    x: px(183), y: px(53), w: px(650), h: px(24),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 20, bold: true,
  }
);
slide.addText(
  [
    { text: "(Self Attention of word ", options: { color: "000000" } },
    { text: "X", options: { color: C.titleRed } },
    { text: "2", options: { subscript: true, color: C.titleRed } },
    { text: " w.r.t All words in Sentence ( ", options: { color: "000000" } },
    { text: "X", options: { color: C.titleRed } },
    { text: "1", options: { subscript: true, color: C.titleRed } },
    { text: ", ", options: { color: C.titleRed } },
    { text: "X", options: { color: C.titleRed } },
    { text: "2", options: { subscript: true, color: C.titleRed } },
    { text: ", ", options: { color: C.titleRed } },
    { text: "X", options: { color: C.titleRed } },
    { text: "3", options: { subscript: true, color: C.titleRed } },
    { text: ", ", options: { color: C.titleRed } },
    { text: "X", options: { color: C.titleRed } },
    { text: "4", options: { subscript: true, color: C.titleRed } },
    { text: " )", options: { color: "000000" } },
  ],
  {
    x: px(183), y: px(81), w: px(650), h: px(24),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 20, bold: true,
  }
);

// ---- output (SINGLE-VERSION law: one plain-named deliverable) ---------------------------------------
const OUT = path.join(__dirname, "..", "slide_033_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
