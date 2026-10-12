// slide_054.js — "Self Attention Mechanism for Decoder  (Adding Mask)"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 54; P4 pattern-group HEAD [54,55])
//
// CONTENT SPEC: analysis/slide_054_final.json (verbatim; validation.fixes applied).
// Original frame: unique_slides/slide_054.jpg (960x540, 1px = 1pt).
// Provenance: slide_054_source/SOURCES.md (course-authored figure; Vaswani 2017 §3.2.1-3.2.3.1).
//
// CHROME LAW: shared module videos/deep-learning/shared_patterns/house_chrome.js —
// drawHouseChrome(pptx, slide, {numeral: 54}). Badge numeral = 54 (printed on THIS frame;
// PIL-measured frame badge yellow-bbox center (875.5, 71) -> slide (891.6, 74.3) vs house
// (893, 71): within the ~3px cross-check — same playlist template confirmed).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide054/measure_*.py — the four chrome
// landmarks of THIS frame: left border x=59, right x=902, top y=42, bottom-border y=516,
// identical to slide_002's fit within 1px JPEG noise):
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// All content below is specified in FRAME px and mapped through fx2sx()/fy2sy().
//
// FRAME-MEASURED FACTS encoded here (PIL + one batched zoomed vision read through the
// vision gate, transcript scratch/slide054/vision_struct_1.txt — overrides spec hexes
// per the color law, frame is ground truth):
//   * All embedding stacks read BOTTOM-UP: left/right containers and K/V strips carry
//     Z4/K4/V4 at the TOP and Z1 at the BOTTOM (consistent with mask [-inf,-inf,0,0]
//     top->bottom and query q2). Bottom container strips read left-to-right Z1..Z4.
//   * "Scaling by √d" rotated text is DARK RED, and there is NO minus before √d (frame
//     resolves the spec's "Scaling by -√d [?]" → "Scaling by √d").
//   * Softmax rotated text is PURPLE (~7030A0); Mask label is GREEN (~23844D); pill text
//     is NAVY (~333366); legend caption is NAVY (~000080); blue dots are NAVY (~1B1F95);
//     W_v boxes are LIGHT BLUE with blue border; W_k boxes light green.
//   * Pills (Similarity / Probabilities / Weighted SUM) are PALE YELLOW fill.
//   * Mask column cells are PALE YELLOW with black text; Mask box has a darker border.
//   * The 4 ⊗ nodes sit on a descending diagonal at frame (558,238),(588,275),(618,312),
//     (648,349). ARROW LANGUAGE (attempt-3 gap scans): box-to-box connectors are
//     HEAD-ONLY triangles at the box edges; full shafts exist only in the K->dot
//     corridor (x 266..328) + thin dot diagonals; Mask->Scaling heads point LEFT;
//     B (Wk->Kstrip) and K2 (Wv->V) have no connector ink at all.
//   * Fraction "K·q/√d" (mathtext PNG, professional 2D format, \cdot per frame zoom
//     reads) sits at frame [422,188,447,219], above-right of the Scaling column top.
//   * Rotated label sizes measured from the frame strips: Scaling ~21pt (strip
//     y 220..360), Mask ~14pt (y 192..227), Soft max ~8.5pt (y 256..284) + ς glyph
//     ~[514,291,522,320]. Mask cells carry a dark khaki border (~#8C8251).
//   * OMITTED as video-capture artifacts (ground rule (c)): the black bottom letterbox
//     strip (frame rows 519-539) and the small black bottom-left corner bar
//     (spec flags it "likely video-player artifact"; brief step 41 says omit).
//
// P4 PATTERN-GROUP NOTE (slide 55 mirrors this slide): the reusable conventions are
// banked in recreated_pptx/qa/slide054/PATTERN_GROUP_P4.md — mapping constants, the
// embedding-row primitive, strip primitives, node/arrow primitives, palette.

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
const RED = "C00000";          // deck red: title, arrows, red labels
const PANEL = "F5CFF6";        // big diagram panel
const CONT_FILL = "E4FBE7";    // container fill (light green)
const CONT_LINE = "92D050";    // dashed green borders
const CHIP = "FDFD96";         // yellow chips/cells
const PALE_CELL = "EEF0F5";    // pale lavender-white cells
const WK_FILL = "C9E9C6";      // W_k boxes
const WV_FILL = "BEECF1";      // W_v boxes (light blue)
const WV_LINE = "5B9BD5";
const TAN = "D8C8B9";          // Dot Product box
const SCALE_FILL = "F7D3D6";   // Scaling column
const MASK_FILL = "B9E8C6";    // Mask column
const MASK_LINE = "3E7A3E";
const MASK_LABEL = "23844D";
const MASK_CELL = "F6F6BE";
const SOFT_FILL = "F7DCF9";    // Softmax column (pale pink, ≈ panel)
const SOFT_TEXT = "7030A0";    // purple
const SIGMA_FILL = "E1F3F8";   // Σ box
const NAVY = "000080";
const DOT_NAVY = "1B1F95";     // similarity dots
const PILL_FILL = "F0F0D8";    // label pills
const PILL_LINE = "D8D88E";
const PILL_TEXT = "333366";    // navy pill text
const OUT_FILL = "A4C6A2";     // output box fill (medium light green)
const OUT_LINE = "3C8C3C";
const GREEN_ARR = "00B050";    // block arrow
const MAG = "DA70D6";          // Z2 highlight
const MAG_LINE = "8B4789";
const WQ_FILL = "F2BCD8";      // W_q box
const BLACK = "000000";
const FONT = "Arial";

// ---- house chrome (playlist law) ----
drawHouseChrome(pres, s, { numeral: 54 });

// ================= TITLE =================
// frame ink x 97..577 y 66..84 -> slide ink x 81.5..580.7, y 69.1..87.9
// Arial Bold advance 25.67em / measured 499.2pt -> em 19.45 -> 19.6pt
// (attempt 2: em 19.5 measured 9.2px narrow at 150dpi; ink-left 80->81.5pt)
s.addText("Self Attention Mechanism for Decoder  (Adding Mask)", {
  x: IN(81.5), y: IN(61.3), w: IN(520), h: IN(30),
  fontFace: FONT, fontSize: 19.6, bold: true, color: RED,
  align: "left", valign: "middle", margin: 0,
});

// ================= TOP-RIGHT LEGEND =================
// chip1 "-inf": frame [731,64,763,84]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(731)), y: IN(sy(64)), w: IN((763 - 731) / SX), h: IN((84 - 64) / SY),
  fill: { color: "FAFAB0" }, line: { color: "A0522D", width: 1 },
});
s.addText("-\u2212\u221E", {
  x: IN(sx(731)), y: IN(sy(64)), w: IN((763 - 731) / SX), h: IN((84 - 64) / SY),
  fontFace: FONT, fontSize: 10, bold: true, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});
// red circled-asterisk: frame ink ~[780,66,801,82]
s.addShape(pres.ShapeType.ellipse, {
  x: IN(sx(781)), y: IN(sy(66)), w: IN(21 / SX), h: IN(17 / SY),
  fill: { type: "none" }, line: { color: RED, width: 1 },
});
s.addText("*", {
  x: IN(sx(781)), y: IN(sy(66)), w: IN(21 / SX), h: IN(17 / SY),
  fontFace: FONT, fontSize: 12, bold: true, color: RED,
  align: "center", valign: "middle", margin: 0,
});
// chip3 empty yellow rect (dark red/brown border per frame): frame [806,59,838,75]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(806)), y: IN(sy(59)), w: IN((838 - 806) / SX), h: IN((75 - 59) / SY),
  fill: { color: "FAFAB0" }, line: { color: "A0522D", width: 1 },
});
// badge "54" = house chrome (already drawn)

// ================= MAIN PINK PANEL =================
// frame [71,105,849,500]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(71)), y: IN(sy(105)), w: IN((849 - 71) / SX), h: IN((500 - 105) / SY),
  fill: { color: PANEL }, line: { type: "none" }, rectRadius: IN(6),
});

// ================= LEFT INPUT CONTAINER (Z4..Z1 top->bottom) =================
// frame [78,219,153,379]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(78)), y: IN(sy(219)), w: IN((153 - 78) / SX), h: IN((379 - 219) / SY),
  fill: { color: CONT_FILL }, line: { color: CONT_LINE, width: 1, dashType: "dash" },
  rectRadius: IN(5),
});
// embedding row primitive: chip + red Z label + 2 pale cells; rows frame y-tops 231,270,310,352
const LROWS = [231, 270, 310, 352];
const LNUM = ["4", "3", "2", "1"]; // top->bottom (frame reads bottom-up stacks)
LROWS.forEach((ry, i) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(87)), y: IN(sy(ry)), w: IN(9 / SX), h: IN(14 / SY),
    fill: { color: CHIP }, line: { type: "none" },
  });
  s.addText([
    { text: "Z", options: { bold: true } },
    { text: LNUM[i], options: { subscript: true, bold: true } },
  ], {
    x: IN(sx(99)), y: IN(sy(ry - 1)), w: IN(24 / SX), h: IN(16 / SY),
    fontFace: FONT, fontSize: 10, color: RED,
    align: "left", valign: "middle", margin: 0,
  });
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(122)), y: IN(sy(ry)), w: IN(15 / SX), h: IN(14 / SY),
    fill: { color: PALE_CELL }, line: { type: "none" },
  });
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(138)), y: IN(sy(ry)), w: IN(14 / SX), h: IN(14 / SY),
    fill: { color: PALE_CELL }, line: { type: "none" },
  });
});

// ================= W_k BOXES (4, green) =================
// frame x [175,202], y-tops 228,267,306,348
const WK_TOPS = [228, 267, 306, 348];
WK_TOPS.forEach((ty) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(175)), y: IN(sy(ty)), w: IN(27 / SX), h: IN(20 / SY),
    fill: { color: WK_FILL }, line: { type: "none" },
  });
  s.addText([
    { text: "W", options: { bold: true } },
    { text: "k", options: { subscript: true, bold: true } },
    { text: "(r)", options: { superscript: true, bold: true } },
  ], {
    x: IN(sx(176.5)), y: IN(sy(ty)), w: IN(25 / SX), h: IN(20 / SY),
    fontFace: FONT, fontSize: 8, color: BLACK,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= K STRIPS (4, labels K4..K1 top->bottom) =================
// per strip: yellow chip [218,~226,4,9] + pale cell + red label at frame x 249..258
const KSTRIP_CY = [236.5, 276.5, 315.5, 357.5]; // frame row centers
const KNUM = ["4", "3", "2", "1"];
KSTRIP_CY.forEach((cy, i) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(218)), y: IN(sy(cy - 4.5)), w: IN(4.5 / SX), h: IN(9 / SY),
    fill: { color: CHIP }, line: { type: "none" },
  });
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(224)), y: IN(sy(cy - 4.5)), w: IN(17 / SX), h: IN(9 / SY),
    fill: { color: "EFE3C8" }, line: { type: "none" },
  });
  s.addText([
    { text: "K", options: { bold: true } },
    { text: KNUM[i], options: { subscript: true, bold: true } },
  ], {
    x: IN(sx(246)), y: IN(sy(cy - 7)), w: IN(16 / SX), h: IN(14 / SY),
    fontFace: FONT, fontSize: 9, color: RED,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= DOT PRODUCT BOX (tan) =================
// frame [265,189,347,385]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(265)), y: IN(sy(189)), w: IN((347 - 265) / SX), h: IN((385 - 189) / SY),
  fill: { color: TAN }, line: { type: "none" },
});
s.addText([
  { text: "Dot", options: { breakLine: true } },
  { text: "Product", options: {} },
], {
  x: IN(sx(272)), y: IN(sy(197)), w: IN(62 / SX), h: IN(34 / SY),
  fontFace: FONT, fontSize: 10, bold: true, color: BLACK,
  align: "center", valign: "middle", lineSpacing: 13, margin: 0,
});
// 4 navy similarity dots on the descending diagonal: frame centers (337,238),(322,277),(304,316),(285,358)
const DOTS = [[337, 238], [322, 277], [304, 316], [285, 358]];
DOTS.forEach(([dx, dy]) => {
  s.addShape(pres.ShapeType.ellipse, {
    x: IN(sx(dx - 4.5)), y: IN(sy(dy - 4.5)), w: IN(9 / SX), h: IN(9 / SY),
    fill: { color: DOT_NAVY }, line: { type: "none" },
  });
});
// "K·q" red label just outside top-right (middle dot per frame zoom reads: C4 +
// crop C1 judge; spec's comma was a full-frame misread): frame [352,193,373,203]
s.addText([
  { text: "K", options: { bold: true } },
  { text: "\u00B7", options: { bold: true } },
  { text: "q", options: { bold: true } },
], {
  x: IN(sx(350)), y: IN(sy(191)), w: IN(26 / SX), h: IN(14 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: RED,
  align: "left", valign: "middle", margin: 0,
});
// "Similarity" pill: frame [282,159,343,176]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(282)), y: IN(sy(159)), w: IN((343 - 282) / SX), h: IN((176 - 159) / SY),
  fill: { color: PILL_FILL }, line: { color: PILL_LINE, width: 0.75 }, rectRadius: IN(8),
});
s.addText("Similarity", {
  x: IN(sx(282)), y: IN(sy(159)), w: IN((343 - 282) / SX), h: IN((176 - 159) / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: PILL_TEXT,
  align: "center", valign: "middle", margin: 0,
});

// ================= SCALING COLUMN =================
// frame [384,191,412,384]; rotated dark-red text (bottom-to-top)
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(384)), y: IN(sy(191)), w: IN((412 - 384) / SX), h: IN((384 - 191) / SY),
  fill: { color: SCALE_FILL }, line: { type: "none" },
});
const SC_CX = sx((384 + 412) / 2), SC_CY = sy(290);
s.addText("Scaling by \u221Ad", {
  x: IN(SC_CX - 100), y: IN(SC_CY - 13), w: IN(200), h: IN(26),
  fontFace: FONT, fontSize: 21, bold: true, color: RED, rotate: 270,
  align: "center", valign: "middle", margin: 0,
});
// fraction K·q/sqrt(d): mathtext PNG 600dpi (re-rendered with \cdot per frame zoom
// reads), embed at exact px/600; measured original ink [422,188,447,219]
const EQ_W = 215 / 600, EQ_H = 275 / 600; // inches
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq_Kcdotq_over_sqrtd.png",
  x: IN(432.65 - EQ_W * 72 / 2), y: IN(211.9 - EQ_H * 72 / 2), w: EQ_W, h: EQ_H,
});

// ================= MASK COLUMN =================
// frame [456,191,484,385]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(456)), y: IN(sy(191)), w: IN((484 - 456) / SX), h: IN((385 - 191) / SY),
  fill: { color: MASK_FILL }, line: { color: MASK_LINE, width: 1 },
});
// "Mask" rotated (frame strip y 192..227 = 35px -> em ~14pt)
const MK_CX = sx(470), MK_CY = sy(209.5);
s.addText("Mask", {
  x: IN(MK_CX - 40), y: IN(MK_CY - 10), w: IN(80), h: IN(20),
  fontFace: FONT, fontSize: 14, bold: true, color: MASK_LABEL, rotate: 270,
  align: "center", valign: "middle", margin: 0,
});
// 4 pale-yellow cells with dark khaki border (measured #8C8251 ring): frame
// [459, y, 478, y+12], y-tops 233,272,309,351; text -inf,-inf,0,0 (U+2212 minus)
const MCELLS = [[233, "-\u2212\u221E"], [272, "-\u2212\u221E"], [309, "0"], [351, "0"]];
MCELLS.forEach(([ty, txt]) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(459)), y: IN(sy(ty)), w: IN(19 / SX), h: IN(12 / SY),
    fill: { color: MASK_CELL }, line: { color: "8C8250", width: 0.75 },
  });
  s.addText(txt, {
    x: IN(sx(459)), y: IN(sy(ty)), w: IN(19 / SX), h: IN(12 / SY),
    fontFace: FONT, fontSize: 8, bold: true, color: BLACK,
    align: "center", valign: "middle", margin: 0,
  });
});
// Look Ahead Mask ellipse: frame [432,390,506,434]
s.addShape(pres.ShapeType.ellipse, {
  x: IN(sx(432)), y: IN(sy(390)), w: IN((506 - 432) / SX), h: IN((434 - 390) / SY),
  fill: { color: BLACK }, line: { type: "none" },
});
s.addText([
  { text: "Look Ahead", options: { breakLine: true } },
  { text: "Mask", options: {} },
], {
  x: IN(sx(436)), y: IN(sy(398)), w: IN(66 / SX), h: IN(28 / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: "FFFF00",
  align: "center", valign: "middle", lineSpacing: 11, margin: 0,
});

// ================= SOFTMAX COLUMN =================
// frame [512,190,534,386] (panel-pink pale fill, edges visible)
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(512)), y: IN(sy(190)), w: IN((534 - 512) / SX), h: IN((386 - 190) / SY),
  fill: { color: SOFT_FILL }, line: { color: "E3BEE8", width: 0.75 },
});
// rotated "Soft max" purple, SMALL (frame strip y 256..284 -> em ~8.5pt), center (521,270)
const SM_CX = sx(521), SM_CY = sy(270);
s.addText("Soft max", {
  x: IN(SM_CX - 70), y: IN(SM_CY - 11), w: IN(140), h: IN(22),
  fontFace: FONT, fontSize: 8.5, bold: true, color: SOFT_TEXT, rotate: 270,
  align: "center", valign: "middle", margin: 0,
});
// large final-sigma glyph below the rotated text: frame ~[514,291,522,320], center (518,305)
s.addText("\u03C2", {
  x: IN(sx(510)), y: IN(sy(288)), w: IN(16 / SX), h: IN(34 / SY),
  fontFace: FONT, fontSize: 20, bold: true, color: SOFT_TEXT,
  align: "center", valign: "middle", margin: 0,
});
// "Probabilities" pill: frame [472,157,552,177]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(472)), y: IN(sy(157)), w: IN((552 - 472) / SX), h: IN((177 - 157) / SY),
  fill: { color: PILL_FILL }, line: { color: PILL_LINE, width: 0.75 }, rectRadius: IN(9),
});
s.addText("Probabilities", {
  x: IN(sx(472)), y: IN(sy(157)), w: IN((552 - 472) / SX), h: IN((177 - 157) / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: PILL_TEXT,
  align: "center", valign: "middle", margin: 0,
});
// red "0" near the softmax top-right (on the top fan arrow): frame ~[534,226,542,236]
s.addText("0", {
  x: IN(sx(531)), y: IN(sy(224)), w: IN(14 / SX), h: IN(14 / SY),
  fontFace: FONT, fontSize: 10, bold: true, color: RED,
  align: "center", valign: "middle", margin: 0,
});

// ================= SIGMA BOX + Weighted SUM pill + green block arrow + OUTPUT BOX =================
// Sigma box: frame [542,189,670,210]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(542)), y: IN(sy(189)), w: IN((670 - 542) / SX), h: IN((210 - 189) / SY),
  fill: { color: SIGMA_FILL }, line: { type: "none" },
});
s.addText("\u03A3", {
  x: IN(sx(542)), y: IN(sy(189)), w: IN((670 - 542) / SX), h: IN((210 - 189) / SY),
  fontFace: FONT, fontSize: 18, bold: true, color: NAVY,
  align: "center", valign: "middle", margin: 0,
});
// Weighted SUM pill: frame [619,157,708,177]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(619)), y: IN(sy(157)), w: IN((708 - 619) / SX), h: IN((177 - 157) / SY),
  fill: { color: PILL_FILL }, line: { color: PILL_LINE, width: 0.75 }, rectRadius: IN(9),
});
s.addText("Weighted SUM", {
  x: IN(sx(619)), y: IN(sy(157)), w: IN((708 - 619) / SX), h: IN((177 - 157) / SY),
  fontFace: FONT, fontSize: 9.5, bold: true, color: PILL_TEXT,
  align: "center", valign: "middle", margin: 0,
});
// green block arrow: rises from ~frame (588,180) up-right into the output box
// (~frame 606,145): lean atan(18/52) ~ 19deg clockwise from vertical; the original
// arrow STOPS ~10pt above the Sigma box (frame rows ~138..180, no overlap with Sigma)
s.addShape(pres.ShapeType.upArrow, {
  x: IN(sx(589)), y: IN(sy(146)), w: IN(16 / SX), h: IN(42 / SY),
  fill: { color: GREEN_ARR }, line: { type: "none" }, rotate: 19,
});
// output box: frame [570,114,628,139] — dashed green border, green fill, Z strip inside
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(570)), y: IN(sy(114)), w: IN((628 - 570) / SX), h: IN((139 - 114) / SY),
  fill: { color: OUT_FILL }, line: { color: OUT_LINE, width: 1, dashType: "dash" },
  rectRadius: IN(4),
});
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(583)), y: IN(sy(126)), w: IN(6.5 / SX), h: IN(12 / SY),
  fill: { color: CHIP }, line: { type: "none" },
});
s.addText("Z", {
  x: IN(sx(590.5)), y: IN(sy(124.5)), w: IN(10 / SX), h: IN(15 / SY),
  fontFace: FONT, fontSize: 9, bold: true, color: RED,
  align: "center", valign: "middle", margin: 0,
});
[601.5, 608, 614.5].forEach((cxx) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(cxx)), y: IN(sy(126)), w: IN(5.5 / SX), h: IN(12 / SY),
    fill: { color: "92D050" }, line: { type: "none" },
  });
});

// ================= FOUR (x) MULTIPLY NODES (descending diagonal) =================
// frame centers (558,238),(588,275),(618,312),(648,349), d~16
const NODES = [[558, 238], [588, 275], [618, 312], [648, 349]];
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

// ================= V STRIPS (labels V4..V1 top->bottom, fixed column) =================
// red label at frame x ~661..671 + yellow cell [676..684] + lavender cell [686..698]
const VROWS = [[236.5, "4"], [276.5, "3"], [315.5, "2"], [357.5, "1"]];
VROWS.forEach(([cy, num]) => {
  s.addText([
    { text: "V", options: { bold: true } },
    { text: num, options: { subscript: true, bold: true } },
  ], {
    x: IN(sx(656)), y: IN(sy(cy - 7)), w: IN(17 / SX), h: IN(14 / SY),
    fontFace: FONT, fontSize: 9, color: RED,
    align: "left", valign: "middle", margin: 0,
  });
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(676)), y: IN(sy(cy - 5)), w: IN(8 / SX), h: IN(10 / SY),
    fill: { color: CHIP }, line: { type: "none" },
  });
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(686)), y: IN(sy(cy - 5)), w: IN(12 / SX), h: IN(10 / SY),
    fill: { color: PALE_CELL }, line: { type: "none" },
  });
});

// ================= W_v BOXES (4, light blue) =================
// frame x [706,736], y-tops 226,266,305,347
const WV_TOPS = [226, 266, 305, 347];
WV_TOPS.forEach((ty) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(706)), y: IN(sy(ty)), w: IN(30 / SX), h: IN(24 / SY),
    fill: { color: WV_FILL }, line: { color: WV_LINE, width: 1 },
  });
  s.addText([
    { text: "W", options: { bold: true } },
    { text: "v", options: { subscript: true, bold: true } },
    { text: "(r)", options: { superscript: true, bold: true } },
  ], {
    x: IN(sx(708.5)), y: IN(sy(ty)), w: IN(27 / SX), h: IN(24 / SY),
    fontFace: FONT, fontSize: 8, color: BLACK,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= RIGHT INPUT CONTAINER (Z4..Z1 top->bottom) =================
// frame [752,220,827,379]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(752)), y: IN(sy(220)), w: IN((827 - 752) / SX), h: IN((379 - 220) / SY),
  fill: { color: CONT_FILL }, line: { color: CONT_LINE, width: 1, dashType: "dash" },
  rectRadius: IN(5),
});
const RROWS = [231, 270, 310, 352];
const RNUM = ["4", "3", "2", "1"];
RROWS.forEach((ry, i) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(759)), y: IN(sy(ry)), w: IN(9.5 / SX), h: IN(14 / SY),
    fill: { color: CHIP }, line: { type: "none" },
  });
  s.addText([
    { text: "Z", options: { bold: true } },
    { text: RNUM[i], options: { subscript: true, bold: true } },
  ], {
    x: IN(sx(771)), y: IN(sy(ry - 1)), w: IN(24 / SX), h: IN(16 / SY),
    fontFace: FONT, fontSize: 10, color: RED,
    align: "left", valign: "middle", margin: 0,
  });
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(795)), y: IN(sy(ry)), w: IN(15 / SX), h: IN(14 / SY),
    fill: { color: PALE_CELL }, line: { type: "none" },
  });
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(811)), y: IN(sy(ry)), w: IN(14 / SX), h: IN(14 / SY),
    fill: { color: PALE_CELL }, line: { type: "none" },
  });
});

// ================= BOTTOM CONTAINER (strips Z1..Z4 left->right, Z2 magenta) =================
// frame [193,457,490,495]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(193)), y: IN(sy(457)), w: IN((490 - 193) / SX), h: IN((495 - 457) / SY),
  fill: { color: CONT_FILL }, line: { color: CONT_LINE, width: 1, dashType: "dash" },
  rectRadius: IN(5),
});
// strip primitive: chip + 2 pale cells + red Z label (measured chip/label x per strip)
const BSTrips = [
  { chip: 205, label: 226, num: "1" },
  { magenta: true, x0: 277, label: 288, num: "2" },
  { chip: 347, label: 368, num: "3" },
  { chip: 420, label: 441, num: "4" },
];
BSTrips.forEach((t) => {
  if (t.magenta) {
    // 4 magenta cells spanning frame 277..335 with dashed magenta border + red Z2 label on top
    [277, 291.5, 306, 320.5].forEach((cxx) => {
      s.addShape(pres.ShapeType.rect, {
        x: IN(sx(cxx)), y: IN(sy(466.5)), w: IN(13 / SX), h: IN(16.5 / SY),
        fill: { color: MAG }, line: { color: MAG_LINE, width: 0.75, dashType: "dash" },
      });
    });
    s.addText([
      { text: "Z", options: { bold: true } },
      { text: "2", options: { subscript: true, bold: true } },
    ], {
      x: IN(sx(288)), y: IN(sy(466)), w: IN(24 / SX), h: IN(17.5 / SY),
      fontFace: FONT, fontSize: 9.5, color: RED,
      align: "center", valign: "middle", margin: 0,
    });
  } else {
    s.addShape(pres.ShapeType.rect, {
      x: IN(sx(t.chip)), y: IN(sy(467.5)), w: IN(9.5 / SX), h: IN(14 / SY),
      fill: { color: CHIP }, line: { type: "none" },
    });
    s.addShape(pres.ShapeType.rect, {
      x: IN(sx(t.chip + 10.5)), y: IN(sy(467.5)), w: IN(9 / SX), h: IN(14 / SY),
      fill: { color: PALE_CELL }, line: { type: "none" },
    });
    s.addShape(pres.ShapeType.rect, {
      x: IN(sx(t.chip + 20.5)), y: IN(sy(467.5)), w: IN(9 / SX), h: IN(14 / SY),
      fill: { color: PALE_CELL }, line: { type: "none" },
    });
    s.addText([
      { text: "Z", options: { bold: true } },
      { text: t.num, options: { subscript: true, bold: true } },
    ], {
      x: IN(sx(t.label)), y: IN(sy(466.5)), w: IN(16 / SX), h: IN(16 / SY),
      fontFace: FONT, fontSize: 9.5, color: RED,
      align: "left", valign: "middle", margin: 0,
    });
  }
});
// thick red block arrow below the container pointing up at Z2: frame [277,491,296,506]
s.addShape(pres.ShapeType.upArrow, {
  x: IN(sx(279)), y: IN(sy(491.5)), w: IN(15 / SX), h: IN(14.5 / SY),
  fill: { color: RED }, line: { type: "none" },
});

// ================= W_q BOX + q2 STRIP (query path) =================
// W_q box: frame [278,416,317,448]
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(278)), y: IN(sy(416)), w: IN((317 - 278) / SX), h: IN((448 - 416) / SY),
  fill: { color: WQ_FILL }, line: { type: "none" },
});
s.addText([
  { text: "W", options: { bold: true } },
  { text: "q", options: { subscript: true, bold: true } },
  { text: "(r)", options: { superscript: true, bold: true } },
], {
  x: IN(sx(278)), y: IN(sy(416)), w: IN(39 / SX), h: IN(32 / SY),
  fontFace: FONT, fontSize: 8.5, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});
// q2 strip: red label frame [289,399,302,410] + cells to the right
s.addText([
  { text: "q", options: { bold: true } },
  { text: "2", options: { subscript: true, bold: true } },
], {
  x: IN(sx(286)), y: IN(sy(397)), w: IN(16 / SX), h: IN(15 / SY),
  fontFace: FONT, fontSize: 9.5, color: RED,
  align: "left", valign: "middle", margin: 0,
});
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(303)), y: IN(sy(399)), w: IN(8 / SX), h: IN(12 / SY),
  fill: { color: CHIP }, line: { type: "none" },
});
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(312)), y: IN(sy(399)), w: IN(16 / SX), h: IN(12 / SY),
  fill: { color: PALE_CELL }, line: { type: "none" },
});

// ================= LEGEND (bottom-right, dashed green box) =================
// frame [725,448,887,512]
s.addShape(pres.ShapeType.roundRect, {
  x: IN(sx(725)), y: IN(sy(448)), w: IN((887 - 725) / SX), h: IN((512 - 448) / SY),
  fill: { color: CONT_FILL }, line: { color: CONT_LINE, width: 1, dashType: "dash" },
  rectRadius: IN(5),
});
// strip1: "1 x d" above + 4 yellow cells
s.addText("1\u00D7d", {
  x: IN(sx(742)), y: IN(sy(452)), w: IN(38 / SX), h: IN(11 / SY),
  fontFace: FONT, fontSize: 8, bold: true, color: RED,
  align: "center", valign: "middle", margin: 0,
});
[0, 1, 2, 3].forEach((i) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(744 + i * 8.5)), y: IN(sy(466)), w: IN(7.5 / SX), h: IN(11 / SY),
    fill: { color: CHIP }, line: { type: "none" },
  });
});
// W box + "d x d" below
s.addShape(pres.ShapeType.rect, {
  x: IN(sx(784)), y: IN(sy(455)), w: IN(28 / SX), h: IN(28 / SY),
  fill: { color: "F6F0BE" }, line: { color: "A0522D", width: 1 },
});
s.addText("W", {
  x: IN(sx(784)), y: IN(sy(455)), w: IN(28 / SX), h: IN(28 / SY),
  fontFace: FONT, fontSize: 11, bold: true, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});
s.addText("d\u00D7d", {
  x: IN(sx(784)), y: IN(sy(484.5)), w: IN(30 / SX), h: IN(11 / SY),
  fontFace: FONT, fontSize: 8, bold: true, color: RED,
  align: "center", valign: "middle", margin: 0,
});
// "="
s.addText("=", {
  x: IN(sx(820)), y: IN(sy(462)), w: IN(16 / SX), h: IN(20 / SY),
  fontFace: FONT, fontSize: 14, bold: true, color: RED,
  align: "center", valign: "middle", margin: 0,
});
// strip2: 4 cells (yellow + lavender) + "1 x d" below
[0, 1, 2, 3].forEach((i) => {
  s.addShape(pres.ShapeType.rect, {
    x: IN(sx(843 + i * 9)), y: IN(sy(466)), w: IN(8 / SX), h: IN(11 / SY),
    fill: { color: i % 2 === 0 ? CHIP : PALE_CELL }, line: { type: "none" },
  });
});
s.addText("1\u00D7d", {
  x: IN(sx(840)), y: IN(sy(479)), w: IN(38 / SX), h: IN(11 / SY),
  fontFace: FONT, fontSize: 8, bold: true, color: RED,
  align: "center", valign: "middle", margin: 0,
});
// caption "d: Embedding Length" NAVY: frame [775,498,853,508]
s.addText("d: Embedding Length", {
  x: IN(sx(772)), y: IN(sy(496.5)), w: IN(86 / SX), h: IN(12 / SY),
  fontFace: FONT, fontSize: 8, bold: true, color: NAVY,
  align: "center", valign: "middle", margin: 0,
});

// ================= ARROWS (red C00000) =================
// FRAME-MEASURED ARROW LANGUAGE (2026-10-12 gap scans, scratch/slide054/*measure*.txt):
// box-to-box connectors are HEAD-ONLY triangles poking out of the box edges; full
// shafts exist ONLY in the open K-strip->dot corridor (shaft x 266..~328, 2px thick)
// and as the thin dot diagonals. B (Wk->Kstrip) and K2 (Wv->V) have NO connector ink
// at all in the original. F heads point LEFT (Mask -> Scaling; crop-C1 judge read).
function seg(x1, y1, x2, y2, width = 0.5) {
  s.addShape(pres.ShapeType.line, {
    x: IN(Math.min(x1, x2)), y: IN(Math.min(y1, y2)),
    w: IN(Math.abs(x2 - x1)), h: IN(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: RED, width },
  });
}
// head triangle: horizontal dirs footprint 9x6 frame px, up footprint 7x9
function head(cx, cy, dir) {
  const rot = dir === "right" ? 90 : dir === "left" ? 270 : 0;
  const wF = dir === "up" ? 7 : 6, hF = 9;
  s.addShape(pres.ShapeType.triangle, {
    x: IN(sx(cx - wF / 2)), y: IN(sy(cy - hF / 2)),
    w: IN(wF / SX), h: IN(hF / SY),
    fill: { color: RED }, line: { type: "none" }, rotate: rot,
  });
}

// A. left container -> W_k: head-only (measured x 162..172, rows y 237.5/277/316/358)
[237.5, 277, 316, 358].forEach((cy) => head(167, cy, "right"));
// B. W_k -> K strip: NO ink in the original — omitted.
// C. K strips -> dots: the ONE full-shaft corridor (measured shaft y238.5 x 266..328)
const DOTXY = [[337, 238], [322, 277], [304, 316], [285, 358]];
DOTXY.forEach(([dx, dy]) => {
  seg(266, dy, dx - 13, dy, 1.75);
  head(dx - 9, dy, "right");
});
// D. thin diagonals interconnecting consecutive dots (faint stubs measured near dots)
seg(sx(331), sy(242), sx(316), sy(273));
seg(sx(316), sy(281), sx(298), sy(312));
seg(sx(298), sy(320), sx(279), sy(354));
// E. DotProduct -> Scaling: head-only (measured blob x 374..380, y ~240)
head(377, 240, "right");
// F. Mask -> Scaling: LEFT-pointing heads (measured x 446..452, tip ~446) + tie to Mask edge
[237.5, 277, 316.5, 357].forEach((cy) => {
  seg(455.5, cy, 452, cy, 0.75);
  head(449, cy, "left");
});
// G. Mask -> Soft max: head-only (measured x 499..508)
[237.5, 277.5, 316.5, 358.5].forEach((cy) => head(503.5, cy, "right"));
// H. Soft max -> nodes: head-only at node left edges (measured node1 x 540..549)
NODES.forEach(([nx, ny]) => head(nx - 13.5, ny, "right"));
// I. nodes -> Sigma: UP heads under Sigma (measured y 212..220 at x 556/586/616/646)
[556, 586, 616, 646].forEach((xx) => head(xx, 216, "up"));
// J. V strips -> nodes: LEFT heads just right of each node (measured node1 x 568..575)
NODES.forEach(([nx, ny]) => head(nx + 14, ny, "left"));
// K. right container -> W_v: LEFT heads (measured x 740..748)
[238, 277, 316.5, 358.5].forEach((cy) => head(744.5, cy, "left"));
// K2. W_v -> V strips: NO ink in the original — omitted.
// L. query path: three UP heads at x~306 (measured y 444..453 / 403..412 / 389..397)
head(306.5, 448.5, "up");
head(306.5, 407.5, "up");
head(306.5, 393, "up");
// M. dashed green curved connectors: bottom container ends up to the side containers
// (bezier-PNG pattern — pptxgenjs has no curvedConnector preset; 600dpi transparent
// PNGs embedded at exact px/600; generation script build/assets/gen_connectors.py)
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/conn_left.png",
  x: IN(110.66), y: IN(398.72), w: 594 / 600, h: 849 / 600,
});
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/conn_right.png",
  x: IN(490.38), y: IN(398.72), w: 2429 / 600, h: 853 / 600,
});

// ================= WRITE =================
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_054_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
