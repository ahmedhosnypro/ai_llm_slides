// slide_055.js — "Encoder-Decoder Attention Mechanism (In Decoder)"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 55; P4 pattern-group #2 [54,55])
//
// CONTENT SPEC: analysis/slide_055_final.json (verbatim; validation.fixes applied).
// Original frame: unique_slides/slide_055.jpg (960x540, 1px = 1pt).
// Provenance: slide_055_source/SOURCES.md.
//
// CHROME LAW: shared module videos/deep-learning/shared_patterns/house_chrome.js —
// drawHouseChrome(pptx, slide, {numeral: 55}). Badge numeral = 55 (printed on THIS frame;
// PIL-measured frame badge yellow-bbox center (875.5, 70.5) -> slide (891.5, 73.8) vs house
// (893, 71): within the ~3px cross-check — same playlist template confirmed).
//
// FRAME->SLIDE MAPPING (P4 pattern guide §1: re-fit THIS frame's four chrome landmarks —
// measured 2026-10-12 scratch/slide055/measure_chrome2.py: left border x=58-59, right
// x=901-902, top y=42-43, bottom-border y=516-518 — identical to slide_054's certified fit
// within 1px, so the SAME constants carry over):
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// All content below is specified in FRAME px and mapped through fx2sx()/fy2sy().
//
// FRAME-MEASURED FACTS encoded here (PIL forensics scratch/slide055/measure_*.py,
// forensics*.py — frame is ground truth, overrides spec hexes where they differ):
//   * Peach panel [84,104,879,502] fill ~F7E2CD (rounded).
//   * Title L1 ink x 264..740 y 58..71 (em ~20.3 via Arial-Bold advance; red span
//     "(In Decoder)" x 632..740). L2 ink x 201..803 y 79..94 (em ~19; red Z2 at 405..420,
//     red Y1..Y4 at 690..790). Both lines centered on frame x~502 (slide ~503 — measured,
//     NOT slide-center 480; reproduced as measured).
//   * Dot Product box [289,186,409,388] tan DBCBBB; 4 navy dots (363,237.5),(348,276.5),
//     (330,316),(311.5,359) d~7 on the descending diagonal; 4 HORIZONTAL red lines run the
//     FULL box width (x 264..407) at the dot rows (mesh_bands evidence), dots sit ON them;
//     3 thin diagonals interconnect consecutive dots; "K.q" red label INSIDE box top-right
//     [378,192,398,200]; "Similarity" pill above [308,156,368,176] PALE LAVENDER EDE9FF.
//   * Scaling column [411,186,446,389] fill FDD7D6, rotated dark-red "Scaling by √d"
//     (bottom-to-top). Fraction K·q/√d (mathtext PNG, P4 pattern) at frame ink
//     [446,185,471,218] — immediately RIGHT of the column top (same relation as 054).
//   * Softmax column [487,189,515,386] fill F8DEFB; rotated purple "Soft max" ~8.5pt +
//     final-sigma glyph (P4 convention); "Probabilities" pill [459,156,539,176].
//   * Sigma box [543,189,671,209] fill EAFEFC (same as 054 within 1px); 4 up-heads under
//     it at y~211-218 x 557/587/616/645 + faint shafts to the nodes.
//   * 4 ⊗ nodes on the SAME descending diagonal as 054: (557.5,237),(587,277),(616.5,316.5),
//     (645.5,359), d~16, transparent fill + red ring + red ×.
//   * ARROW LANGUAGE (differential redness forensics): softmax->node RIGHT heads at
//     (nx-13, cy) — head-only, NO shafts (SMrow scan: ink only at the head blobs);
//     V->node LEFT heads at (nx+13.5, cy) — head-only, NO shafts from W_v (V corridor
//     x 606..727 EMPTY at all node rows — same "no connector ink" law as 054's B/K2);
//     V labels (V4..V1) float at x 662..672, ~9px ABOVE the node rows;
//     node->Sigma UP heads at y~214.5 + faint shafts; Y->W_k black arrows with heads at
//     x~192; W_k->K: NO ink (omitted, 054 pattern B); Y->W_v black LEFT arrows with heads
//     at x~761; K1's head blob is strong (redness 128 at x298-303), K4/K3/K2 fainter.
//   * W_k boxes [199,229] y-tops 227/266/304/346 fill CDE4C8 border 87C294 (light green,
//     NOT 054's pale fill); W_v boxes [727,756] y-tops 227/267/306/348 fill C1F4ED border
//     5B9BD5; K strips [240,272] y-tops 223/262/302/345 striped pale-yellow/pinkish-white,
//     red K labels at x~272..287 (K4 top -> K1 bottom, P4 embedding law).
//   * Y containers YELLOW FFFF00 w/ dashed green border: left [103,217,180,381], right
//     [781,217,859,381]; 4 strips (y-tops 228/267/307/349) each = pale cells + red Y label
//     CENTERED (measured: label x 134..149 on strip 104..180 — center 141.5≈142) + yellow
//     container showing at strip ends (bright FFFF00 measured at 104-110/170-180).
//   * Green block arrow up at [576,143,597,163] (tip ~591, short — does NOT reach Sigma);
//     O box [572,120,641,142] green w/ pale striped cells INSIDE flanking the O glyph.
//   * Decoder query: q2 red label [316,390..] + striped glyph; W_q WHITE box [~311,416,34,30]
//     (spec: white box; 054's was pink — frames differ); thin red line up x~316 (strong
//     y 367..375) angling into the bottom dot.
//   * Z-row container [215,441,525,497] fill F5C5FF (pale violet-pink); 4 strips: Z1
//     cells 219..252 + label 255..264; Z2 strip 270..366 = 2 pale cells + 4 MAGENTA cells
//     (DA70D6 family) inside a RED DASHED rect [267,438,368,489], label on the magenta;
//     Z3 cells 375..393 + label 397..408; Z4 cells 447..468 + label 471..477 + cell 486..492.
//     Thick red up-arrow below at [300,491,320,507] pointing at Z2.
//   * Caption "From Decoder / Self Attention Layer" magenta CC00CC at x 543.., y 464..488
//     (left-aligned); white 3D arrow pointing LEFT at [655,458,701,492].
//   * Legend [736,425,899,505] pale green E6FEE8 dashed green border; striped glyph cells
//     ~[752..776] y 444..456; labels DARK (red ink in legend = only the W box's brown
//     border A0522D — 17px total, not red text); navy caption 1C1F86 at y 485..492.
//   * OMITTED as video-capture artifacts (ground rule (c)): black bottom letterbox
//     (frame rows 517..539).
//
// P4 PATTERN-GROUP NOTE: conventions per recreated_pptx/qa/slide054/PATTERN_GROUP_P4.md —
// mapping constants, embedding-row primitive (bottom-up stacks), node/arrow primitives,
// fraction PNG asset reuse, unhashed-C00000 trap, equal-scale crop law.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

// ---- frame->slide mapping (this frame's fitted landmarks; see header) ----
const X0 = 18.63, SX = 0.96123, SY = 0.95556;
const sx = (fx) => (fx - X0) / SX;   // frame px -> slide pt
const sy = (fy) => fy / SY;
const IN = (pt) => pt / 72;          // slide pt -> inches

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 960 x 540 pt
const s = pres.addSlide();

// ---- palette (frame-measured) ----
const RED = "C00000";
const PANEL = "F7E2CD";
const TAN = "DBCBBB";
const SCALE_FILL = "FDD7D6";
const SOFT_FILL = "F8DEFB";
const SOFT_LINE = "E3BEE8";
const SOFT_TEXT = "7030A0";
const SIGMA_FILL = "EAFEFC";
const NAVY = "000080";
const DOT_NAVY = "1B1F95";
const PILL_FILL = "EDE9FF";
const PILL_LINE = "C8C8E6";
const PILL_TEXT = "333366";
const WK_FILL = "CDE4C8";
const WK_LINE = "87C294";
const WV_FILL = "C1F4ED";
const WV_LINE = "5B9BD5";
const YELL = "FFFF00";
const CONT_LINE = "00B050";
const PALE_CELL = "FDFFD4";
const PALE_CELL2 = "E5E3F1";
const STRIPE_A = "FFF7D2";
const STRIPE_B = "F2E2EC";
const STRIP_LINE = "C4BB94";
const O_FILL = "A0D696";
const O_CELL_L = "C2E4B8";
const O_CELL_R = "B9CFC0";
const GREEN_ARR = "00B050";
const ZFILL = "F5C5FF";
const MAG = "DA70D6";
const MAG_LINE = "8B4789";
const ZCELL_Y = "FFF3CE";
const ZCELL_L = "E8E4F2";
const HATCH_W = "FFFFFF";
const LEG_FILL = "E6FEE8";
const LEG_LINE = "92D050";
const WBOX_FILL = "FDFFCE";
const WBOX_LINE = "A0522D";
const CAPTION_MAG = "CC00CC";
const BLACK = "000000";
const FONT = "Arial";

// ---- house chrome (playlist law) ----
drawHouseChrome(pres, s, { numeral: 55 });

// ================= TITLE =================
// L1: frame ink x 264..740 y 58..71; center (502, 64.5) -> slide (502.9, 67.5)
s.addText([
  { text: "Encoder-Decoder  Attention Mechanism  ", options: { color: BLACK } },
  { text: "(In Decoder)", options: { color: RED } },
], {
  x: IN(502.9 - 350), y: IN(52.4), w: IN(700), h: IN(30),
  fontFace: FONT, fontSize: 19.7, bold: true,
  align: "center", valign: "middle", margin: 0,
});
// L2: frame ink x 201..803 y 79..94; center (502, 86.5) -> slide (502.9, 90.5)
s.addText([
  { text: "(Self Attention of word ", options: { color: BLACK } },
  { text: "Z", options: { color: RED, bold: true } },
  { text: "2", options: { color: RED, bold: true, subscript: true } },
  { text: " w.r.t All words in Sentence ( ", options: { color: BLACK } },
  { text: "Y", options: { color: RED, bold: true } },
  { text: "1", options: { color: RED, bold: true, subscript: true } },
  { text: ", ", options: { color: RED, bold: true } },
  { text: "Y", options: { color: RED, bold: true } },
  { text: "2", options: { color: RED, bold: true, subscript: true } },
  { text: ", ", options: { color: RED, bold: true } },
  { text: "Y", options: { color: RED, bold: true } },
  { text: "3", options: { color: RED, bold: true, subscript: true } },
  { text: ", ", options: { color: RED, bold: true } },
  { text: "Y", options: { color: RED, bold: true } },
  { text: "4", options: { color: RED, bold: true, subscript: true } },
  { text: " )", options: { color: BLACK } },
], {
  x: IN(502.9 - 350), y: IN(76.9), w: IN(700), h: IN(26),
  fontFace: FONT, fontSize: 19.9, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// ================= MAIN PEACH PANEL =================
// frame [84,104,879,502]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(84)), y: IN(sy(104)), w: IN((879 - 84) / SX), h: IN((502 - 104) / SY),
  fill: { color: PANEL }, line: { type: "none" }, rectRadius: IN(8),
});

// ============ helper: red seg/head (FRAME px, single convention — P4 trap #2) ============
function seg(x1, y1, x2, y2, width = 0.75, color = RED) {
  const X1 = sx(x1), Y1 = sy(y1), X2 = sx(x2), Y2 = sy(y2);
  s.addShape(pres.ShapeType.line, {
    x: IN(Math.min(X1, X2)), y: IN(Math.min(Y1, Y2)),
    w: IN(Math.abs(X2 - X1)), h: IN(Math.abs(Y2 - Y1)),
    flipH: X2 < X1, flipV: Y2 < Y1,
    line: { color, width },
  });
}
function head(cx, cy, dir, color = RED) {
  const rot = dir === "right" ? 90 : dir === "left" ? 270 : 0;
  const wF = dir === "up" ? 7 : 6, hF = 9;
  s.addShape(pres.ShapeType.triangle, {
    x: IN(sx(cx - wF / 2)), y: IN(sy(cy - hF / 2)),
    w: IN(wF / SX), h: IN(hF / SY),
    fill: { color }, line: { type: "none" }, rotate: rot,
  });
}
function dseg(x1, y1, x2, y2, width = 0.75, color = BLACK) { seg(x1, y1, x2, y2, width, color); }

// ================= RED 3D BLOCK ARROWS (slide edges, outward) =================
s.addShape(pres.ShapeType.leftArrow, {
  x: IN(sx(62)), y: IN(sy(181)), w: IN(30 / SX), h: IN(26 / SY),
  fill: { color: RED }, line: { type: "none" },
});
s.addShape(pres.ShapeType.rightArrow, {
  x: IN(sx(866)), y: IN(sy(181)), w: IN(30 / SX), h: IN(26 / SY),
  fill: { color: RED }, line: { type: "none" },
});

// ================= HATCHED "From Encoder Output" BOXES =================
function hatchBox(x0, y0, x1, y1) {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(x0)), y: IN(sy(y0)), w: IN((x1 - x0) / SX), h: IN((y1 - y0) / SY),
    fill: { color: HATCH_W }, line: { color: RED, width: 1 },
  });
  // diagonal hatch on the two side bands (7 x 45-degree strokes each, 15px span)
  for (let i = 0; i < 7; i++) {
    const yy = y0 + 2 + i * 5;
    seg(x0 + 1, yy + 13, x0 + 14, yy, 0.5);
    seg(x1 - 14, yy, x1 - 1, yy + 13, 0.5);
  }
  s.addText([
    { text: "From Encoder", options: { breakLine: true } },
    { text: "Output", options: {} },
  ], {
    x: IN(sx(x0 + 6)), y: IN(sy(y0 + 5)), w: IN((x1 - x0 - 12) / SX), h: IN((y1 - y0 - 8) / SY),
    fontFace: FONT, fontSize: 9, bold: true, color: RED,
    align: "center", valign: "middle", lineSpacing: 12, margin: 0,
  });
}
hatchBox(92, 176, 197, 215);
hatchBox(763, 176, 868, 215);

// ================= LEFT Y CONTAINER (yellow, dashed green) =================
function yContainer(cx0, cy0, cx1, cy1, rows, labelCx, cellXs) {
  s.addShape(pres.ShapeType.roundRect, {
    x: IN(sx(cx0)), y: IN(sy(cy0)), w: IN((cx1 - cx0) / SX), h: IN((cy1 - cy0) / SY),
    fill: { color: YELL }, line: { color: CONT_LINE, width: 1, dashType: "dash" },
    rectRadius: IN(5),
  });
  const NUMS = ["4", "3", "2", "1"]; // top->bottom (stack reads bottom-up, P4 §5)
  rows.forEach((ty, i) => {
    cellXs.forEach((cxx) => {
      s.addShape(pres.ShapeType.rect, {
        x: IN(sx(cxx)), y: IN(sy(ty + 3)), w: IN(10 / SX), h: IN(14 / SY),
        fill: { color: PALE_CELL }, line: { color: "E0D8A0", width: 0.5 },
      });
    });
    s.addText([
      { text: "Y", options: { bold: true } },
      { text: NUMS[i], options: { subscript: true, bold: true } },
    ], {
      x: IN(sx(labelCx - 12)), y: IN(sy(ty)), w: IN(24 / SX), h: IN(16 / SY),
      fontFace: FONT, fontSize: 10, bold: true, color: RED,
      align: "center", valign: "middle", margin: 0,
    });
  });
}
const LROWS = [228, 267, 307, 349];
yContainer(103, 217, 180, 381, LROWS, 141.5, [112, 124, 150, 162]);

// ================= LEFT W_k BOXES (4, light green) =================
const WKTOPS = [227, 266, 304, 346];
WKTOPS.forEach((ty) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(199)), y: IN(sy(ty)), w: IN(30 / SX), h: IN(21 / SY),
    fill: { color: WK_FILL }, line: { color: WK_LINE, width: 1 },
  });
  s.addText([
    { text: "W", options: { bold: true } },
    { text: "k", options: { subscript: true, bold: true } },
    { text: "(r)", options: { superscript: true, bold: true } },
  ], {
    x: IN(sx(200.5)), y: IN(sy(ty)), w: IN(28 / SX), h: IN(21 / SY),
    fontFace: FONT, fontSize: 8, color: BLACK,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= K STRIPS (4, striped; labels K4..K1 top->bottom) =================
const KSTRIP_TOPS = [223, 262, 302, 345];
const KSTRIP_CY = [230.5, 269.5, 309.5, 352];
KSTRIP_TOPS.forEach((ty, i) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(240)), y: IN(sy(ty)), w: IN(32 / SX), h: IN(15 / SY),
    fill: { color: STRIPE_A }, line: { color: STRIP_LINE, width: 0.5 },
  });
  for (let k = 1; k < 5; k++) {
    seg(240 + k * 6.4, ty + 1, 240 + k * 6.4, ty + 14, 0.5, "D8C8A8");
  }
  s.addText([
    { text: "K", options: { bold: true } },
    { text: ["4", "3", "2", "1"][i], options: { subscript: true, bold: true } },
  ], {
    x: IN(sx(272)), y: IN(sy(KSTRIP_CY[i] - 8)), w: IN(17 / SX), h: IN(16 / SY),
    fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= DOT PRODUCT BOX (tan) =================
// frame [289,186,409,388]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(289)), y: IN(sy(186)), w: IN((409 - 289) / SX), h: IN((388 - 186) / SY),
  fill: { color: TAN }, line: { type: "none" },
});
s.addText([
  { text: "Dot", options: { breakLine: true } },
  { text: "Product", options: {} },
], {
  x: IN(sx(296)), y: IN(sy(191)), w: IN(64 / SX), h: IN(30 / SY),
  fontFace: FONT, fontSize: 10, bold: true, color: BLACK,
  align: "center", valign: "middle", lineSpacing: 13, margin: 0,
});
// "K.q" red label inside top-right: frame [378,192,398,200]
s.addText([
  { text: "K", options: { bold: true } },
  { text: ".", options: { bold: true } },
  { text: "q", options: { bold: true } },
], {
  x: IN(sx(376)), y: IN(sy(190)), w: IN(26 / SX), h: IN(14 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
  align: "left", valign: "middle", margin: 0,
});
// 4 navy dots on the descending diagonal (measured centers)
const DOTS = [[363, 237.5], [348, 276.5], [330, 316], [311.5, 359]];
DOTS.forEach(([dx, dy]) => {
  s.addShape(pres.ShapeType.ellipse, {
    x: IN(sx(dx - 3.5)), y: IN(sy(dy - 3.5)), w: IN(7 / SX), h: IN(7 / SY),
    fill: { color: DOT_NAVY }, line: { type: "none" },
  });
});
// 4 horizontal red lines the FULL width (frame evidence: x 264..407 at dot rows)
const DOTROWS = [237.5, 276.5, 316, 359];
DOTROWS.forEach((dy, i) => {
  seg(264, dy, 407, dy, 0.75);
  head(DOTS[i][0] - 11, dy, "right");
});
// 3 thin diagonals interconnecting consecutive dots
seg(360, 243, 351, 272, 0.5);
seg(346, 282, 333, 311, 0.5);
seg(328, 321, 315, 354, 0.5);
// "Similarity" pill: frame [308,156,368,176]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(308)), y: IN(sy(156)), w: IN((368 - 308) / SX), h: IN((176 - 156) / SY),
  fill: { color: PILL_FILL }, line: { color: PILL_LINE, width: 0.75 }, rectRadius: IN(8),
});
s.addText("Similarity", {
  x: IN(sx(308)), y: IN(sy(156)), w: IN((368 - 308) / SX), h: IN((176 - 156) / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: PILL_TEXT,
  align: "center", valign: "middle", margin: 0,
});

// ================= SCALING COLUMN =================
// frame [411,186,446,389]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(411)), y: IN(sy(186)), w: IN((446 - 411) / SX), h: IN((389 - 186) / SY),
  fill: { color: SCALE_FILL }, line: { type: "none" },
});
const SC_CX = sx((411 + 446) / 2), SC_CY = sy(288);
s.addText("Scaling by \u221Ad", {
  x: IN(SC_CX - 100), y: IN(SC_CY - 13), w: IN(200), h: IN(26),
  fontFace: FONT, fontSize: 20, bold: true, color: RED, rotate: 90,
  align: "center", valign: "middle", margin: 0,
});
// fraction K·q/sqrt(d): mathtext PNG 600dpi (P4 §7; reused certified asset), embed at
// exact px/600 centered on the measured ink [446,185,471,218] (center 458.5, 201.5)
const EQ_W = 215 / 600, EQ_H = 275 / 600; // inches
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq_Kcdotq_over_sqrtd.png",
  x: IN(sx(458.5) - EQ_W * 72 / 2), y: IN(sy(201.5) - EQ_H * 72 / 2), w: EQ_W, h: EQ_H,
});

// ================= SOFTMAX COLUMN =================
// frame [487,189,515,386]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(487)), y: IN(sy(189)), w: IN((515 - 487) / SX), h: IN((386 - 189) / SY),
  fill: { color: SOFT_FILL }, line: { color: SOFT_LINE, width: 0.75 },
});
const SM_CX = sx(501), SM_CY = sy(270);
s.addText("Soft max", {
  x: IN(SM_CX - 70), y: IN(SM_CY - 11), w: IN(140), h: IN(22),
  fontFace: FONT, fontSize: 8.5, bold: true, color: SOFT_TEXT, rotate: 270,
  align: "center", valign: "middle", margin: 0,
});
s.addText("\u03C2", {
  x: IN(sx(493)), y: IN(sy(285)), w: IN(16 / SX), h: IN(34 / SY),
  fontFace: FONT, fontSize: 30, bold: true, color: SOFT_TEXT,
  align: "center", valign: "middle", margin: 0,
});
// "Probabilities" pill: frame [459,156,539,176]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(459)), y: IN(sy(156)), w: IN((539 - 459) / SX), h: IN((176 - 156) / SY),
  fill: { color: PILL_FILL }, line: { color: PILL_LINE, width: 0.75 }, rectRadius: IN(9),
});
s.addText("Probabilities", {
  x: IN(sx(459)), y: IN(sy(156)), w: IN((539 - 459) / SX), h: IN((176 - 156) / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: PILL_TEXT,
  align: "center", valign: "middle", margin: 0,
});

// ================= SIGMA BOX + Weighted SUM pill =================
// Sigma box: frame [543,189,671,209]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(543)), y: IN(sy(189)), w: IN((671 - 543) / SX), h: IN((209 - 189) / SY),
  fill: { color: SIGMA_FILL }, line: { type: "none" },
});
s.addText("\u03A3", {
  x: IN(sx(543)), y: IN(sy(189)), w: IN((671 - 543) / SX), h: IN((209 - 189) / SY),
  fontFace: FONT, fontSize: 18, bold: true, color: NAVY,
  align: "center", valign: "middle", margin: 0,
});
// Weighted SUM pill: frame [620,156,708,177]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(620)), y: IN(sy(156)), w: IN((708 - 620) / SX), h: IN((177 - 156) / SY),
  fill: { color: PILL_FILL }, line: { color: PILL_LINE, width: 0.75 }, rectRadius: IN(9),
});
s.addText("Weighted SUM", {
  x: IN(sx(620)), y: IN(sy(156)), w: IN((708 - 620) / SX), h: IN((177 - 156) / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: PILL_TEXT,
  align: "center", valign: "middle", margin: 0,
});

// ================= GREEN BLOCK ARROW + O OUTPUT BOX =================
// green up arrow: frame [576,143,597,163], slight lean (tip ~591)
s.addShape(pres.ShapeType.upArrow, {
  x: IN(sx(576)), y: IN(sy(143)), w: IN(22 / SX), h: IN(21 / SY),
  fill: { color: GREEN_ARR }, line: { type: "none" }, rotate: 13,
});
// O box: frame [572,120,641,142] with pale striped cells inside flanking the O glyph
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(572)), y: IN(sy(120)), w: IN((641 - 572) / SX), h: IN((142 - 120) / SY),
  fill: { color: O_FILL }, line: { type: "none" },
});
[578, 585, 592].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(123)), w: IN(6 / SX), h: IN(16 / SY),
    fill: { color: O_CELL_L }, line: { color: "89B27A", width: 0.5 },
  });
});
s.addText("O", {
  x: IN(sx(598)), y: IN(sy(120)), w: IN(18 / SX), h: IN(22 / SY),
  fontFace: FONT, fontSize: 12, bold: true, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});
[618, 624, 630, 636].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(123)), w: IN(5 / SX), h: IN(16 / SY),
    fill: { color: O_CELL_R }, line: { color: "89B27A", width: 0.5 },
  });
});

// ================= FOUR (x) MULTIPLY NODES (descending diagonal, same as 054) =================
const NODES = [[557.5, 237], [587, 277], [616.5, 316.5], [645.5, 359]];
NODES.forEach(([nx, ny]) => {
  s.addShape(pres.ShapeType.ellipse, {
    x: IN(sx(nx - 8)), y: IN(sy(ny - 8)), w: IN(16 / SX), h: IN(16 / SY),
    fill: { type: "none" }, line: { color: RED, width: 1.25 },
  });
  s.addText("\u00D7", {
    x: IN(sx(nx - 8)), y: IN(sy(ny - 8)), w: IN(16 / SX), h: IN(16 / SY),
    fontFace: FONT, fontSize: 11, bold: true, color: RED,
    align: "center", valign: "middle", margin: 0,
  });
});

// ================= V LABELS (V4..V1 top->bottom, floating above the head line) =================
NODES.forEach(([nx, ny], i) => {
  s.addText([
    { text: "V", options: { bold: true } },
    { text: ["4", "3", "2", "1"][i], options: { subscript: true, bold: true } },
  ], {
    x: IN(sx(660)), y: IN(sy(ny - 16)), w: IN(16 / SX), h: IN(14 / SY),
    fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= W_v BOXES (4, light blue) =================
const WVTOPS = [227, 267, 306, 348];
WVTOPS.forEach((ty) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(727)), y: IN(sy(ty)), w: IN(29 / SX), h: IN(21 / SY),
    fill: { color: WV_FILL }, line: { color: WV_LINE, width: 1 },
  });
  s.addText([
    { text: "W", options: { bold: true } },
    { text: "v", options: { subscript: true, bold: true } },
    { text: "(r)", options: { superscript: true, bold: true } },
  ], {
    x: IN(sx(728.5)), y: IN(sy(ty)), w: IN(27 / SX), h: IN(21 / SY),
    fontFace: FONT, fontSize: 8, color: BLACK,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= RIGHT Y CONTAINER (yellow, dashed green) =================
const RROWS = [228, 267, 307, 349];
yContainer(781, 217, 859, 381, RROWS, 817, [789, 801, 825, 837]);

// ================= BLACK ARROWS =================
// A. left Y rows -> W_k (rightward; heads at ~x192, shafts 181..189)
[237, 276.5, 316, 358.5].forEach((cy) => {
  dseg(181, cy, 189, cy, 0.75);
  head(192.5, cy, "right", BLACK);
});
// B. W_k -> K strips: NO ink in the original — omitted (054 pattern B).
// K. right Y rows -> W_v (leftward; heads at ~x761.5, shafts 781..768)
[237, 277, 316.5, 359].forEach((cy) => {
  dseg(781, cy, 768, cy, 0.75);
  head(761.5, cy, "left", BLACK);
});
// K2. W_v -> V labels: NO connector ink in the original — omitted (054 pattern K2).
// H. Soft max -> nodes: RIGHT heads at node left edges, head-only (no shafts measured)
NODES.forEach(([nx, ny]) => head(nx - 13, ny, "right"));
// J. V -> nodes: LEFT heads just right of node edges, head-only (no shafts measured)
NODES.forEach(([nx, ny]) => head(nx + 13.5, ny, "left"));
// I. nodes -> Sigma: UP heads under Sigma (y~214.5) + faint shafts to node tops
[557, 587, 616, 645].forEach((xx, i) => {
  head(xx, 214.5, "up");
  seg(xx, 219, xx, NODES[i][1] - 9, 0.5);
});
// L. query path: q2 up into the bottom dot (strong segment y 367..375 at x~316)
seg(316, 396, 316, 366, 0.75);
seg(316, 366, 306, 359.5, 0.5);

// ================= DECODER QUERY (q2 + glyph + W_q box) =================
// q2 red label: frame [316,390..] + striped glyph cells to the right
s.addText([
  { text: "q", options: { bold: true } },
  { text: "2", options: { subscript: true, bold: true } },
], {
  x: IN(sx(313)), y: IN(sy(390)), w: IN(17 / SX), h: IN(14 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
  align: "left", valign: "middle", margin: 0,
});
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(331)), y: IN(sy(394)), w: IN(8 / SX), h: IN(11 / SY),
  fill: { color: "FDFD96" }, line: { type: "none" },
});
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(340)), y: IN(sy(394)), w: IN(8 / SX), h: IN(11 / SY),
  fill: { color: "EEF0F5" }, line: { type: "none" },
});
// W_q box (WHITE per this frame; spec uncertain-item): frame [311,416,345,446]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(311)), y: IN(sy(416)), w: IN(34 / SX), h: IN(30 / SY),
  fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
});
s.addText([
  { text: "W", options: { bold: true } },
  { text: "q", options: { subscript: true, bold: true } },
  { text: "(r)", options: { superscript: true, bold: true } },
], {
  x: IN(sx(311)), y: IN(sy(416)), w: IN(34 / SX), h: IN(30 / SY),
  fontFace: FONT, fontSize: 8.5, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});

// ================= Z-ROW CONTAINER =================
// frame [215,441,525,497] fill F5C5FF
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(215)), y: IN(sy(441)), w: IN((525 - 215) / SX), h: IN((497 - 441) / SY),
  fill: { color: ZFILL }, line: { color: "E0A8D8", width: 0.75 }, rectRadius: IN(5),
});
// Z1 strip: cells 219..252 + label 255..264
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(219)), y: IN(sy(459)), w: IN(11 / SX), h: IN(24 / SY),
  fill: { color: ZCELL_L }, line: { type: "none" },
});
[231, 242].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(459)), w: IN(10 / SX), h: IN(24 / SY),
    fill: { color: ZCELL_Y }, line: { type: "none" },
  });
});
s.addText([
  { text: "Z", options: { bold: true } },
  { text: "1", options: { subscript: true, bold: true } },
], {
  x: IN(sx(252)), y: IN(sy(462)), w: IN(16 / SX), h: IN(17 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
  align: "left", valign: "middle", margin: 0,
});
// Z2 strip: red dashed highlight rect [267,438,368,489]; 2 pale cells + 4 magenta cells
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(267)), y: IN(sy(438)), w: IN((368 - 267) / SX), h: IN((489 - 438) / SY),
  fill: { type: "none" }, line: { color: RED, width: 1, dashType: "dash" },
});
[271, 284].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(459)), w: IN(12 / SX), h: IN(24 / SY),
    fill: { color: PALE_CELL2 }, line: { type: "none" },
  });
});
[300, 316.5, 333, 349.5].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(458)), w: IN(15 / SX), h: IN(26 / SY),
    fill: { color: MAG }, line: { color: MAG_LINE, width: 0.75, dashType: "dash" },
  });
});
s.addText([
  { text: "Z", options: { bold: true } },
  { text: "2", options: { subscript: true, bold: true } },
], {
  x: IN(sx(301)), y: IN(sy(462)), w: IN(22 / SX), h: IN(17 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
  align: "left", valign: "middle", margin: 0,
});
// Z3 strip: cells 375..393 + label 397..408
[375, 385].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(459)), w: IN(9 / SX), h: IN(24 / SY),
    fill: { color: ZCELL_Y }, line: { type: "none" },
  });
});
s.addText([
  { text: "Z", options: { bold: true } },
  { text: "3", options: { subscript: true, bold: true } },
], {
  x: IN(sx(395)), y: IN(sy(462)), w: IN(16 / SX), h: IN(17 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
  align: "left", valign: "middle", margin: 0,
});
// Z4 strip: cells 447..468 + label 471..477 + cell 486..492
[447, 458].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(459)), w: IN(10 / SX), h: IN(24 / SY),
    fill: { color: ZCELL_Y }, line: { type: "none" },
  });
});
s.addText([
  { text: "Z", options: { bold: true } },
  { text: "4", options: { subscript: true, bold: true } },
], {
  x: IN(sx(469)), y: IN(sy(462)), w: IN(14 / SX), h: IN(17 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
  align: "left", valign: "middle", margin: 0,
});
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(486)), y: IN(sy(459)), w: IN(8 / SX), h: IN(24 / SY),
  fill: { color: ZCELL_L }, line: { type: "none" },
});
// thick red up-arrow below the container pointing at Z2: frame [300,491,320,507]
s.addShape(pres.ShapeType.upArrow, {
  x: IN(sx(300)), y: IN(sy(491)), w: IN(21 / SX), h: IN(17 / SY),
  fill: { color: RED }, line: { type: "none" },
});

// ================= DECODER CAPTION + WHITE ARROW =================
s.addText([
  { text: "From Decoder", options: { breakLine: true } },
  { text: "Self Attention Layer", options: {} },
], {
  x: IN(sx(541)), y: IN(sy(461)), w: IN(122 / SX), h: IN(28 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: CAPTION_MAG,
  align: "left", valign: "middle", lineSpacing: 14, margin: 0,
});
s.addShape(pres.ShapeType.leftArrow, {
  x: IN(sx(656)), y: IN(sy(459)), w: IN(44 / SX), h: IN(32 / SY),
  fill: { color: "FFFFFF" }, line: { color: "C0C0C0", width: 0.75 },
});

// ================= LEGEND (bottom-right, dashed green box) =================
// frame [736,425,899,505]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(736)), y: IN(sy(425)), w: IN((899 - 736) / SX), h: IN((505 - 425) / SY),
  fill: { color: LEG_FILL }, line: { color: LEG_LINE, width: 1, dashType: "dash" },
  rectRadius: IN(5),
});
// striped glyph cells ~[752..776] y 444..456 (3 cells)
[752, 760, 768].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(444)), w: IN(7 / SX), h: IN(12 / SY),
    fill: { color: "FDFD96" }, line: { color: "C8C890", width: 0.5 },
  });
});
// "1 x d" beneath the glyph (DARK text per frame — red ink in legend is only the W border)
s.addText("1\u00D7d", {
  x: IN(sx(748)), y: IN(sy(458)), w: IN(34 / SX), h: IN(11 / SY),
  fontFace: FONT, fontSize: 8, bold: true, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});
// W box: frame ~[788,458,818,488] pale-yellow fill + brown border
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(788)), y: IN(sy(458)), w: IN(30 / SX), h: IN(30 / SY),
  fill: { color: WBOX_FILL }, line: { color: WBOX_LINE, width: 1 },
});
s.addText("W", {
  x: IN(sx(788)), y: IN(sy(458)), w: IN(30 / SX), h: IN(30 / SY),
  fontFace: FONT, fontSize: 11, bold: true, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});
// "= d x d" right of the W box
s.addText("= d\u00D7d", {
  x: IN(sx(822)), y: IN(sy(466)), w: IN(42 / SX), h: IN(12 / SY),
  fontFace: FONT, fontSize: 8, bold: true, color: BLACK,
  align: "left", valign: "middle", margin: 0,
});
// rotated "1 x d" at far right
s.addText("1\u00D7d", {
  x: IN(sx(880) - 30), y: IN(sy(466) - 8), w: IN(60), h: IN(16),
  fontFace: FONT, fontSize: 8, bold: true, color: BLACK, rotate: 270,
  align: "center", valign: "middle", margin: 0,
});
// navy caption: frame [768,485,864,492]
s.addText("d: Embedding Length", {
  x: IN(sx(766)), y: IN(sy(483)), w: IN(100 / SX), h: IN(11 / SY),
  fontFace: FONT, fontSize: 8, bold: true, color: "1C1F86",
  align: "center", valign: "middle", margin: 0,
});

// ================= WRITE =================
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_055_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
