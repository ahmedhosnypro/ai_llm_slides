// slide_013.js — "Self Attention Mechanism (Linear Transformation of Inputs)" /
// "(Self Attention of word X₂ w.r.t All words in Sentence ( X₁, X₂, X₃, X₄)"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 13)
//
// STANDALONE BUILD (dispatch authorization 2026-10-12): 002:13 is a cross-video child
// of 001:33 (recap), but this build is drawn STANDALONE from THIS slide's own frame —
// every element measured from unique_slides/slide_013.jpg (960x540) by PIL
// (scratch/slide013/measure*.py). Documented deviations from the parent component:
//   * the two ellipses (translucent blue-gray input ellipse; bright mint W_k ellipse)
//     exist ONLY in this frame — parent has yellow bands + dashed containers there;
//   * W_k/W_v boxes: this frame draws the W_v boxes on a yellow band with light
//     yellow-green fills + olive borders; W_k labels sit directly ON the mint ellipse;
//   * the Dot Product box is TALLER here (frame y 187..387 vs parent 194..402) and its
//     dots/halo/labels sit at this frame's own measured staircase;
//   * palette: PIL cores match the parent-certified palette family (DP fill DBCBBB,
//     title brown 6E5133, K.q 7A231C, softmax purple 7B217B, sigma navy 000083) —
//     the analysis JSON's brighter hexes (#0070C4/#00B050/#E1C6F2/#8496B0) were the
//     vision model's approximations; frame census wins (COLOR LAW).
//
// CHROME LAW (playlist, founder 2026-10-11): shared_patterns/house_chrome.js,
// drawHouseChrome(pptx, slide, {numeral: 13}) — badge = 13 (printed on this frame).
//
// FRAME->SLIDE MAPPING (fitted from THIS frame's four chrome landmarks,
// scratch/slide013/chrome_landmarks.py: left border x=58, right x=901, top y=43,
// bottom stroke y~516.5, badge yellow-bbox center (875.5, 71.0)):
//   frame_x = 17.628 + 0.961232 * slide_x ;  frame_y = 0.955556 * slide_y
// (inverse used below; identical within ~1px to the slide_002 fit). All ink below is
// written in FRAME px and mapped through this transform at build time.
//
// OMITTED AS VIDEO ARTIFACTS (ground rule (c); spec imagery + SOURCES.md):
//   * black presenter arrow cursor at bottom (frame ~(275..300, 488..505));
//   * black/gray mouse pointer over the W_k stage (frame ~(210..220, 255..275) strokes);
//   * black letterbox strip below the slide (frame rows 518+).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const FONT = "Arial";

// ---- frame->slide transform (see header) ---------------------------------------
const AX = 17.628, SX = 0.961232, SY = 0.955556;
const XI = (fx) => (fx - AX) / SX / 72;              // frame px -> inches (x)
const YI = (fy) => fy / SY / 72;                     // frame px -> inches (y)
const WI = (w) => w / SX / 72;                       // frame px width  -> inches
const HI = (h) => h / SY / 72;                       // frame px height -> inches

// ---- palette (PIL cores; parent-certified family where measured matches) --------
const C = {
  peachPanel: "F7E2CD", panelBorder: "C9C5C0",
  inputFill: "B7C1CB",
  mintFill: "85FFA7", mintBorder: "5FBF8F", wkGreen: "3D9C4F",
  containerFill: "E7FFE9", containerBorder: "4E7D52",
  band: "F8FA68", wvBoxFill: "E4FF7D", wvBoxBorder: "A2AC3C", wvText: "7B9218",
  dpFill: "DBCBBB", dpBorder: "A69B90", dpTitle: "6E5133",
  softFill: "F8DEFB", softBorder: "CABAC7", softText: "7B217B",
  sigmaFill: "EAFEFC", sigmaBorder: "C3C7C6", sigmaText: "000083",
  pillFill: "FFFFE3", pillBorder: "A8A08C", pillText: "45406F",
  red: "C03030", redDark: "A50D1E", labelRed: "8E2222", titleRed: "900F22",
  kq: "7A231C", qRed: "800007",
  titleBlue: "00007A", black: "000000",
  dotCore: "0707A8", dotHalo: "D9E6FF", dotHaloLine: "8FA8D9",
  grayLine: "A9A5A0", greenArrow: "3D9C3D", greenArrowLine: "2E7D32",
  xLabelGray: "6E7F8C",
  cellA: "F4F8CE", cellB: "F7FADA", cellC: "FBE9DA", cellD: "E9E9F2", cellE: "EFE0F0",
  x2cellA: "F9FFC6", x2cellB: "FFFFDB",
  minivecA: "FFF3C4", minivecB: "FFD9D2", minivecC: "EADDF6",
  outCell: ["5FAF5F", "A5D3A5", "DFEDDF", "9FB3CC", "A9C9E2"],
  yLabelGreen: "1FA31F",
};

const s = pres.addSlide();

// ---- 1. playlist house chrome: badge numeral 13 ---------------------------------
drawHouseChrome(pres, s, { numeral: 13 });

// ---- helpers ----------------------------------------------------------------------
function box(shape, fx, fy, fw, fh, opts) {
  s.addShape(shape, Object.assign({ x: XI(fx), y: YI(fy), w: WI(fw), h: HI(fh) }, opts));
}
function redArrow(x1, y1, x2, y2, width, opts = {}) {
  s.addShape(pres.ShapeType.line, {
    x: XI(Math.min(x1, x2)), y: YI(Math.min(y1, y2)),
    w: WI(Math.abs(x2 - x1)), h: HI(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: {
      color: opts.color || C.red, width: width || 1,
      endArrowType: opts.head === false ? undefined : "triangle",
      dashType: opts.dash, beginArrowType: opts.begin,
    },
  });
}
function text(t, fx, fy, fw, fh, opts) {
  s.addText(t, Object.assign({
    x: XI(fx), y: YI(fy), w: WI(fw), h: HI(fh),
    margin: 0, fontFace: FONT,
  }, opts));
}
// 5-cell widget strip (parent-style pale cells), optional red X label centered
function widget(fx, fy, fw, fh, cells, label, labelOpts = {}) {
  const cw = fw / 5;
  for (let i = 0; i < 5; i++) {
    box(pres.ShapeType.rect, fx + i * cw, fy, cw, fh, {
      fill: { color: cells[i] }, line: { color: "C9C4B8", width: 0.5 },
    });
  }
  if (label) {
    text(
      [{ text: "X", options: {} }, { text: label, options: { subscript: true } }],
      fx + 1.2 * cw, fy - 2, 2.4 * cw, fh + 5,
      Object.assign({ align: "center", valign: "middle", fontSize: 10, bold: true, color: C.labelRed }, labelOpts)
    );
  }
}
// 2-cell mini vector
function miniVec(fx, fy, fw, fh, fills) {
  const cw = fw / 2;
  for (let i = 0; i < 2; i++) {
    box(pres.ShapeType.rect, fx + i * cw, fy, cw, fh, {
      fill: { color: fills[i] }, line: { color: "C9C4B8", width: 0.5 },
    });
  }
}

// ---- 2. peach diagram panel --------------------------------------------------------
box(pres.ShapeType.rect, 72, 107, 849 - 72, 500 - 107, {
  fill: { color: C.peachPanel }, line: { color: C.panelBorder, width: 1 },
});

// ---- 3. title (two lines; measured ink + colors) -----------------------------------
// L1 ink frame x 234..770 (cx 502) -> Arial Bold WIDTH-FIT 20pt (closed-loop attempt 2:
// 21.5pt rendered 1255px vs target 1161.7 -> 20pt = 1167.5px; matches the parent's
// certified 20pt title). Blue parenthetical 00007A.
text(
  [
    { text: "Self Attention Mechanism ", options: { color: C.black } },
    { text: "(Linear Transformation of Inputs)", options: { color: C.titleBlue } },
  ],
  502 - 400, 58 - 0.267 * 20, 800, 1.5 * 20,
  { align: "center", valign: "top", fontSize: 20, bold: true, wrap: false }
);
// L2 ink frame x 199..805 -> width-fit 20.0pt, box center shifted +3pt right (measured
// ink-center bias), box raised so the paren ink top lands at frame y 79 (render 172)
text(
  [
    { text: "(Self Attention of word ", options: { color: C.black } },
    { text: "X", options: { color: C.titleRed } },
    { text: "2", options: { subscript: true, color: C.titleRed } },
    { text: " w.r.t All words in Sentence ( ", options: { color: C.black } },
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
    { text: " )", options: { color: C.black } },
  ],
  505 - 400, 73.7, 800, 1.5 * 20,
  { align: "center", valign: "top", fontSize: 20, bold: true, wrap: false }
);

// ---- 4. input embedding ellipse ----------------------------------------------------
// PIL census: the frame reads a uniform cool B7C1CB (not a warm blend over the peach
// panel) -> the original ellipse is effectively opaque; drawn opaque to match.
box(pres.ShapeType.ellipse, 66, 169, 212 - 66, 423 - 169, {
  fill: { color: C.inputFill }, line: { type: "none" },
});
// 4 embedding rows inside: pale cell strips + dark gray-blue X labels below
const INROWS = [
  { cy: 231, lblY: 247, lbl: "1" },
  { cy: 274, lblY: 291, lbl: "2" },
  { cy: 319, lblY: 336, lbl: "3" },
  { cy: 364, lblY: 380, lbl: "4" },
];
INROWS.forEach((r) => {
  // 3-cell strip centered in the ellipse (x 84..138), cells 18x13
  for (let i = 0; i < 3; i++) {
    box(pres.ShapeType.rect, 84 + i * 18, r.cy - 7, 18, 14, {
      fill: { color: [C.minivecA, C.minivecB, C.minivecC][i] },
      line: { color: "9FB0BD", width: 0.5 },
    });
  }
  text(
    [{ text: "X", options: {} }, { text: r.lbl, options: { subscript: true } }],
    100, r.lblY - 2, 36, 14,
    { align: "center", valign: "middle", fontSize: 9, bold: true, color: C.xLabelGray }
  );
  // red arrow exiting the row rightward into the W_k ellipse
  redArrow(146, r.cy, 211, r.cy, 1);
});

// ---- 5. mint green W_k ellipse -------------------------------------------------------
box(pres.ShapeType.ellipse, 213, 172, 262 - 213, 421 - 172, {
  fill: { color: C.mintFill }, line: { color: C.mintBorder, width: 1 },
});
// W_k labels directly on the ellipse (4 rows, 40px pitch) + K labels at its right edge
const WKY = [231, 270, 309, 351];
WKY.forEach((cy, i) => {
  text(
    [
      { text: "W", options: {} },
      { text: "k", options: { subscript: true } },
      { text: "(r)", options: { superscript: true, fontSize: 6 } },
    ],
    219, cy - 9, 30, 18,
    { align: "center", valign: "middle", fontSize: 9, bold: true, color: C.wkGreen, wrap: false }
  );
  text(
    [{ text: "K", options: {} }, { text: String(4 - i), options: { subscript: true } }],
    247, cy - 9, 20, 18,
    { align: "center", valign: "middle", fontSize: 10, bold: true, color: C.wkGreen, wrap: false }
  );
});
// K vectors (vertical 3-cell stacks peeking left of the ellipse; measured at rows 1 & 4)
[[218, 4], [343, 1]].forEach(([ty, lbl]) => {
  for (let i = 0; i < 3; i++) {
    box(pres.ShapeType.rect, 200, ty + i * 12, 13, 12, {
      fill: { color: [C.minivecA, C.minivecB, C.minivecC][i] },
      line: { color: "B5B98A", width: 0.5 },
    });
  }
});

// ---- 6. Dot Product box ---------------------------------------------------------------
box(pres.ShapeType.rect, 264, 187, 349 - 264, 387 - 187, {
  fill: { color: C.dpFill }, line: { color: C.dpBorder, width: 1 },
});
text(
  [{ text: "Dot", options: { breakLine: true } }, { text: "Product", options: {} }],
  268, 193, 72, 26,
  { align: "center", valign: "top", fontSize: 9.5, bold: true, color: C.dpTitle, lineSpacing: 13 }
);
text("K.q", 351, 191, 26, 12, {
  align: "left", valign: "top", fontSize: 8, bold: true, color: C.kq, wrap: false,
});
// dots: pale-blue halo + navy core, staircase (measured centers)
const DOTC = [[339, 238.5], [324, 277.5], [309, 315.5], [286.5, 357.5]];
DOTC.forEach(([cx, cy]) => {
  box(pres.ShapeType.ellipse, cx - 6.5, cy - 6.5, 13, 13, {
    fill: { color: C.dotHalo }, line: { color: C.dotHaloLine, width: 0.5 },
  });
  box(pres.ShapeType.ellipse, cx - 3.5, cy - 3.5, 7, 7, {
    fill: { color: C.dotCore }, line: { type: "none" },
  });
});
// red arrows: K side -> each dot (enter left), dot -> dot staircase, dot -> softmax
const ROWY = [238.5, 277.5, 315.5, 357.5];
ROWY.forEach((y, i) => {
  redArrow(216, y, DOTC[i][0] - 8, y, 1.25);            // K vector -> dot
  redArrow(DOTC[i][0] + 8, y, 449, y, 0.75);            // dot -> Soft max
});
for (let i = 0; i < 3; i++) {
  redArrow(DOTC[i][0] - 5, DOTC[i][1] + 5, DOTC[i + 1][0] + 5, DOTC[i + 1][1] - 5, 1);
}

// ---- 7. stage pills --------------------------------------------------------------------
function pill(fx, fy, fw, fh, t, fs) {
  box(pres.ShapeType.roundRect, fx, fy, fw, fh, {
    rectRadius: 0.09, fill: { color: C.pillFill },
    line: { color: C.pillBorder, width: 1, dashType: "sysDot" },
  });
  text(t, fx, fy, fw, fh, {
    align: "center", valign: "middle", fontSize: fs, bold: true, color: C.pillText, wrap: false,
  });
}
pill(280, 159, 343 - 280, 178 - 159, "Similarity", 9.5);
pill(432, 157, 512 - 432, 177 - 157, "Probabilities", 9.5);
pill(591, 157, 680 - 591, 178 - 157, "Weighted SUM", 9.5);

// ---- 8. Soft max block ------------------------------------------------------------------
box(pres.ShapeType.roundRect, 458, 190, 489 - 458, 386 - 190, {
  rectRadius: 0.08, fill: { color: C.softFill }, line: { color: C.softBorder, width: 1 },
});
text("Soft max", 473.5 - 28, 288 - 15, 56, 30, {
  rotate: 90, align: "center", valign: "middle", fontSize: 10, bold: true,
  color: C.softText, wrap: false,
});

// ---- 9. Sigma box ------------------------------------------------------------------------
box(pres.ShapeType.rect, 515, 188, 642 - 515, 210 - 188, {
  fill: { color: C.sigmaFill }, line: { color: C.sigmaBorder, width: 1 },
});
text("\u03A3", 515, 188, 642 - 515, 210 - 188, {
  align: "center", valign: "middle", fontSize: 16, bold: true, color: C.sigmaText,
});

// ---- 10. multiply (x) nodes + stems --------------------------------------------------------
// 4 peach-filled circles w/ red ring + red x, staircase (measured); stems up into Sigma
const CIRC = [[536, 238], [564, 277], [581, 316], [608, 358]];
CIRC.forEach(([cx, cy]) => {
  box(pres.ShapeType.ellipse, cx - 6.5, cy - 6.5, 13, 13, {
    fill: { color: C.peachPanel }, line: { color: C.red, width: 1.25 },
  });
  // red x drawn as two line segments (guarantees centering inside the ring)
  redArrow(cx - 4, cy - 4, cx + 4, cy + 4, 1.25, { head: false });
  redArrow(cx - 4, cy + 4, cx + 4, cy - 4, 1.25, { head: false });
});
// stems: circles -> Sigma bottom (measured attachment x 535/564/580/607, heads at Sigma)
const STEMX = [535, 564, 580, 607];
STEMX.forEach((sx, i) => {
  redArrow(CIRC[i][0], CIRC[i][1] - 8, sx, 212, 1);
});
// softmax -> circle entry arrows (heads just left of each circle)
CIRC.forEach(([cx, cy]) => {
  redArrow(491, cy, cx - 9, cy, 0.75);
});
// V stubs: short red arrowheads poking into each circle from the right
CIRC.forEach(([cx, cy]) => {
  redArrow(cx + 12, cy, cx + 7, cy, 1);
});

// ---- 11. W_v band + boxes + V labels/vectors ------------------------------------------------
box(pres.ShapeType.rect, 689, 222, 737 - 689, 379 - 222, {
  fill: { color: C.band }, line: { type: "none" },
});
const WVY = [[225, 28], [261, 31], [302, 30], [342, 31]];
WVY.forEach(([ty, th]) => {
  box(pres.ShapeType.rect, 692, ty, 734 - 692, th, {
    fill: { color: C.wvBoxFill }, line: { color: C.wvBoxBorder, width: 1 },
  });
  text(
    [
      { text: "W", options: {} },
      { text: "v", options: { subscript: true } },
      { text: "(r)", options: { superscript: true, fontSize: 6 } },
    ],
    692, ty, 734 - 692, th,
    { align: "center", valign: "middle", fontSize: 9, bold: true, color: C.wvText }
  );
});
// V labels (top->bottom V4..V1) + 2-cell mini vectors
const VY = [227, 267, 305.5, 348];
VY.forEach((cy, i) => {
  text(
    [{ text: "V", options: {} }, { text: String(4 - i), options: { subscript: true } }],
    634, cy - 8, 18, 16,
    { align: "center", valign: "middle", fontSize: 10, bold: true, color: C.labelRed, wrap: false }
  );
  miniVec(654, cy - 5, 22, 10, [C.minivecA, C.minivecC]);
  redArrow(652, cy, CIRC[i][0] + 9, cy, 1);   // V_i -> (x) node
});

// ---- 12. right embedding container ------------------------------------------------------------
// zoom_right_cont.txt (vision, 2026-10-12): fill pale mint E8F5E7; 4 rows of 5 cells
// (~13x15 frame px) [cream FFFFCC, white, white(label), periwinkle CCCCFF, pink F49AC9];
// X labels INSIDE the 3rd (middle) cell, dark red, red subscripts; 4 red left-pointing
// arrowheads outside the left border (one per row) toward the yellow band; bottom: green
// up-arrowhead into the container + faint dashed gray leader down-left to the note.
box(pres.ShapeType.roundRect, 750, 217, 827 - 750, 381 - 217, {
  rectRadius: 0.08, fill: { color: "E8F5E7" },
  line: { color: "2E8B57", width: 1.25, dashType: "dash" },
});
const RROWY = [236, 275, 315, 356];
const RCELLS = ["FFFFCC", "FFFFFF", "FFFFFF", "CCCCFF", "F49AC9"];
RROWY.forEach((cy, i) => {
  const cw = 13, wx = 755, wy = cy - 7.5;
  for (let k = 0; k < 5; k++) {
    box(pres.ShapeType.rect, wx + k * cw, wy, cw, 15, {
      fill: { color: RCELLS[k] }, line: { color: "B9C4B9", width: 0.5 },
    });
  }
  text(
    [{ text: "X", options: {} }, { text: String(4 - i), options: { subscript: true } }],
    wx + 1.5 * cw, wy - 2, 2 * cw, 19,
    { align: "center", valign: "middle", fontSize: 10, bold: true, color: C.labelRed, wrap: false }
  );
  // red arrowhead pointing left, just outside the left border (toward the yellow band)
  redArrow(749, cy, 739, cy, 1.5);
});

// ---- 13. sentence container (bottom left) -------------------------------------------------------
// zoom_bottom_left.txt (vision, 2026-10-12): pale mint fill ~DCF2DA, dashed green border
// ~3A9A3A; 4 five-cell widgets, labels X1..X4 LEFT->RIGHT centered over the middle cell;
// widget 2 (X2) all-pink cells; highlight around widget 2 is dark MAGENTA ~8B1A8B, fine
// dotted; thick red arrow at bottom = live annotation (omitted); thin red arrow X2 top ->
// W_q box; faint dashed green curve arcs from the container's top-left up-left.
box(pres.ShapeType.roundRect, 196, 452, 472 - 196, 498 - 452, {
  rectRadius: 0.08, fill: { color: "DCF2DA" },
  line: { color: "3A9A3A", width: 1.25, dashType: "dash" },
});
// 5-cell widgets (5 x 8px), y 463..481; x centers on the measured label centers
const SW = [
  { x: 212, lbl: "1", cells: ["F5F0BD", "F2EDB0", "FBF8E0", "C9C3EE", "F3C6DC"] },
  { x: 271, lbl: "2", cells: ["F6C3D9", "EC9DC6", "F9DCE9", "D55BA4", "EA9CC5"] },
  { x: 353.5, lbl: "3", cells: ["F5F0BD", "F2EDB0", "FBF8E0", "CCC6F0", "F2C3DA"] },
  { x: 426, lbl: "4", cells: ["F5F0BD", "F2EDB0", "FBF8E0", "F0BFD8", "E3B4E0"] },
];
SW.forEach((w) => {
  const cw = 8;
  for (let i = 0; i < 5; i++) {
    box(pres.ShapeType.rect, w.x + i * cw, 463, cw, 18, {
      fill: { color: w.cells[i] }, line: { color: "B9B4A8", width: 0.5 },
    });
  }
  text(
    [{ text: "X", options: {} }, { text: w.lbl, options: { subscript: true } }],
    w.x + 2.5 * cw - 12, 465, 24, 15,
    { align: "center", valign: "middle", fontSize: 10, bold: true, color: C.labelRed, wrap: false }
  );
});
// magenta fine-dotted highlight around widget 2 (measured x 287..324, y 462..484)
box(pres.ShapeType.roundRect, 285, 460, 41, 26, {
  rectRadius: 0.05, fill: { type: "none" },
  line: { color: "8B1A8B", width: 1.5, dashType: "sysDot" },
});
// faint dashed green connector: sentence container top-left -> input ellipse (arc up-left)
s.addShape(pres.ShapeType.line, {
  x: XI(152), y: YI(425), w: WI(208 - 152), h: HI(451 - 425),
  flipV: true, line: { color: "7AA87A", width: 1, dashType: "sysDot" },
});

// ---- 14. query path (W_q, q2) --------------------------------------------------------------------
// W_q box: cream fill, dark-red border, red "W_q^(r)" (zoom_bottom_left)
box(pres.ShapeType.rect, 292, 419, 329 - 292, 442 - 419, {
  fill: { color: "FFFDF0" }, line: { color: "8B0000", width: 1.25 },
});
text(
  [
    { text: "W", options: {} },
    { text: "q", options: { subscript: true } },
    { text: "(r)", options: { superscript: true, fontSize: 6 } },
  ],
  292, 419, 329 - 292, 442 - 419,
  { align: "center", valign: "middle", fontSize: 9, bold: true, color: C.qRed }
);
// q2 label + 2-cell vector (yellow/pink cells per zoom_bottom_left)
text(
  [{ text: "q", options: {} }, { text: "2", options: { subscript: true } }],
  276, 398, 16, 14,
  { align: "center", valign: "middle", fontSize: 10, bold: true, color: C.qRed, wrap: false }
);
miniVec(296, 403, 22, 10, ["FFF3C4", "F3C6DC"]);
// W_q -> DP box arrow (vertical through q2; measured x ~307, y 390..418)
redArrow(307, 418, 307, 390, 1.25);
// X2 -> W_q (thin red arrow up from the X2 widget into the W_q box bottom, zoom_bottom_left)
redArrow(310, 470, 310, 445, 1);

// ---- 15. output Y box + green block arrow ----------------------------------------------------------
// dashed green output box (measured x 545..615, y 117..142) with 5 cells + green Y label
box(pres.ShapeType.rect, 545, 117, 615 - 545, 142 - 117, {
  fill: { color: "F2E8DC" }, line: { color: "33A02C", width: 1, dashType: "sysDot" },
});
const OCW = (615 - 549) / 5;
for (let i = 0; i < 5; i++) {
  box(pres.ShapeType.rect, 549 + i * OCW, 122, OCW, 15, {
    fill: { color: C.outCell[i] }, line: { color: "8FA89A", width: 0.5 },
  });
}
text("Y", 568, 121, 18, 18, {
  align: "center", valign: "middle", fontSize: 12, bold: true, color: C.yLabelGreen, wrap: false,
});
// green NE block arrow (Sigma -> output) + red triangle head + thin gray guide line
s.addShape(pres.ShapeType.rightArrow, {
  x: XI(549), y: YI(146), w: WI(28), h: HI(16), rotate: 315,
  fill: { color: C.greenArrow }, line: { color: C.greenArrowLine, width: 0.75 },
});
s.addShape(pres.ShapeType.triangle, {
  x: XI(576), y: YI(142), w: WI(9), h: HI(9),
  fill: { color: C.redDark }, line: { type: "none" },
});
s.addShape(pres.ShapeType.line, {
  x: XI(583), y: YI(152), w: 0, h: HI(36),
  line: { color: C.grayLine, width: 0.75 },
});

// ---- 16. dimension note (bottom right) --------------------------------------------------------------
box(pres.ShapeType.roundRect, 724, 446, 884 - 724, 511 - 446, {
  rectRadius: 0.08, fill: { type: "none" },
  line: { color: C.containerBorder, width: 1.25, dashType: "sysDot" },
});
// left cell stack (3 cells) + '1*d' label
for (let i = 0; i < 3; i++) {
  box(pres.ShapeType.rect, 746, 458 + i * 9, 13, 9, {
    fill: { color: C.minivecA }, line: { color: "C9C4B8", width: 0.5 },
  });
}
text(
  [{ text: "1*d", options: {} }],
  740, 486, 26, 12,
  { align: "center", valign: "middle", fontSize: 8.5, bold: true, color: C.labelRed, wrap: false }
);
// arrow to the W square
redArrow(762, 468, 780, 468, 1);
// W square (orange border, dark W) + 'd*d' beneath
box(pres.ShapeType.rect, 782, 456, 26, 26, {
  fill: { color: "FFFBD1" }, line: { color: "C87A2A", width: 1.5 },
});
text("W", 782, 456, 26, 26, {
  align: "center", valign: "middle", fontSize: 13, bold: true, color: "000000",
});
text("d*d", 778, 484, 34, 11, {
  align: "center", valign: "middle", fontSize: 8.5, bold: true, color: C.labelRed, wrap: false,
});
// '=' + right cell stack + '1*d'
text("=", 812, 462, 12, 16, {
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "8F4A2E", wrap: false,
});
for (let i = 0; i < 3; i++) {
  box(pres.ShapeType.rect, 838, 458 + i * 9, 13, 9, {
    fill: { color: C.minivecA }, line: { color: "C9C4B8", width: 0.5 },
  });
}
text("1*d", 832, 486, 26, 12, {
  align: "center", valign: "middle", fontSize: 8.5, bold: true, color: C.labelRed, wrap: false,
});
// caption
text("d: Embedding Length", 746, 497, 130, 12, {
  align: "center", valign: "middle", fontSize: 9.5, bold: true, color: "1A2470", wrap: false,
});
// dashed leader from the note top up-right to the container bottom + green up-arrowhead
// into the container (zoom_right_cont: gray dashed ~45deg line, green head at ~(787,391))
s.addShape(pres.ShapeType.line, {
  x: XI(752), y: YI(396), w: WI(787 - 752), h: HI(432 - 396), flipV: true,
  line: { color: C.grayLine, width: 1, dashType: "sysDot" },
});
s.addShape(pres.ShapeType.triangle, {
  x: XI(781), y: YI(383), w: WI(12), h: HI(10),
  fill: { color: C.containerBorder }, line: { type: "none" },
});

// ---- write ------------------------------------------------------------------------------------------
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_013_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
