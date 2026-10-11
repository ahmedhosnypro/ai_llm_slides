// slide_041.js — "Encoder – Decoder Transformer" (Deep Learning DSAI 308,
// Transformers — Part I). Build worker ATTEMPT 2, 2026-10-11 (resumed worker:
// attempt 1 was banked — render_1.png + selfcheck ALL PASS — but the mandatory
// dense-region crop comparisons (cropA center zoom, cropB right panel) both
// returned FAIL before the previous worker died on a provider error. Attempt 2
// rebuilds the three diagram zones from PIL pixel forensics on
// unique_slides/slide_041.jpg (960x540, 1px = 1pt): forensic1..4.py +
// connected-component color masks + ASCII color maps. Every geometry below is
// measured, not estimated; spec [?] items kept verbatim where unresolved.
//
// ROOT slide (no depends_on; `15_progress.py deps` shows root/unblocked).
//
// LAWS honored: playlist chrome via shared_patterns/house_chrome.js (numeral 41 =
// number printed on the frame); verbatim text ('SoftMax' left vs 'Softmax' right,
// lowercase 'q', 'Mask (opt.)', 'N×', '× h', 'Outputs (shifted right)',
// 'Add & Norm'); margin:0 + explicit fontFace everywhere; explicit lineSpacing on
// multi-line boxes; no '#' in hex; arrows via line shapes + endArrowType;
// single-version deliverable slide_041_recreated.pptx.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);

const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt)
const FONT = "Arial";

// ---- palette: measured hexes from the original frame (forensic passes 1-4) ----
const C = {
  titleRed: "CC0000",
  red: "CC0000",
  darkRed: "8B0000",
  black: "000000",
  gray: "595959",
  // left schematic
  schGreen: "006400",
  lavender: "C5CAE9",
  scaleYel: "FFF9C4",
  pink: "F8BBD0",
  softGreen: "C8E6C9",
  qRed: "CC2222",
  kvBlue: "2222AA",
  boxBorder: "444444",
  // center zoom
  tanFill: "DFAA75",       // container fill (measured margins)
  panelLt: "E9C084",       // inner light panel
  olive: "7C7A12",         // inner panel border + L-brackets
  stackFill: "C8815A",     // SDPA front card fill
  stackCopy: "BC895C",     // offset copies (no red border in original)
  stackCopyBd: "9A6B3E",
  stackText: "6E2A08",
  vKPurple: "7B4FA0",
  linFill: "DFAC78",       // bottom Linear boxes
  linTopFill: "C3925A",    // top Linear
  concatFill: "E5B166",    // Concat (light tan + dark text, measured)
  brownBd: "7A470A",
  xhColor: "A03000",       // × h annotation (dark red-brown, measured)
  zoomLabel: "C06030",     // zoom label is ORANGE-red (measured), not CC0000
  // right panel
  panelGreen: "00A000",
  encFill: "FDEDDD",
  decFill: "CFFFE2",
  blueAN: "6497B5",        // the 5 Add & Norm boxes are BLUE (measured)
  ffFill: "6B5C46",        // Feed Forward dark olive-gray
  ffText: "2E2414",
  encMhaFill: "CE805A",    // encoder MHA tan fill
  xMhaFill: "B4855A",      // decoder cross-MHA tan fill
  maskedPurple: "BC74C4",
  embBrown: "A97C52",      // Input Embedding
  peBrown: "7E5226",       // encoder PE band
  peBrownDec: "9A5F58",    // decoder PE band
  maroon: "9A4F4C",        // Output Embedding
  linGreen: "AEEFC4",
  smGreen: "B9EBD2",
  grnBoxBd: "2E6B3E",
  vGreen: "358A22",
  yellow: "FFFF00",
  grpBdEnc: "6B5E1E",
  grpBdDec: "8A9A3A",
  loopEnc: "98A860",
  loopDec: "7CBF2A",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pres.addSlide();

// ---- helpers ----------------------------------------------------------------
function arrow(x0, y0, x1, y1, opts = {}) {
  slide.addShape("line", {
    x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
    w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
    flipV: y1 < y0, flipH: x1 < x0,
    line: {
      color: opts.color || C.black, width: opts.width || 1,
      endArrowType: opts.noHead ? undefined : "triangle",
      beginArrowType: opts.beginHead ? "triangle" : undefined,
      dashType: opts.dash,
    },
  });
}
function block(x, y, w, h, fill, text, opts = {}) {
  slide.addShape(opts.round ? "roundRect" : "rect", {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: fill ? { color: fill } : { type: "none" },
    line: opts.border ? { color: opts.border, width: opts.borderW || 1 } : { type: "none" },
    rectRadius: opts.round ? 0.06 : undefined,
  });
  if (text !== undefined && text !== null) {
    slide.addText(text, {
      x: px(x), y: px(y), w: px(w), h: px(h),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: opts.fontSize || 8,
      color: opts.color || C.black, bold: !!opts.bold, italic: !!opts.italic,
      lineSpacing: opts.lineSpacing, wrap: true,
    });
  }
}
function tokenCircle(cx, cy, d, fill, letter, opts = {}) {
  slide.addShape("ellipse", {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill },
    line: { color: opts.ring || fill, width: opts.ringW || 0.75 },
  });
  if (letter) {
    slide.addText(letter, {
      x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: opts.fontSize || 6, bold: true,
      color: opts.letterColor || "FFFFFF",
    });
  }
}
// circle-plus (positional-encoding) glyph: outline circle + plus
function plusGlyph(cx, cy, r, color, width) {
  slide.addShape("ellipse", {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { type: "none" }, line: { color, width },
  });
  arrow(cx - r * 0.62, cy, cx + r * 0.62, cy, { color, width, noHead: true });
  arrow(cx, cy - r * 0.62, cx, cy + r * 0.62, { color, width, noHead: true });
}
// small circle with a sine squiggle beside each ⊕ (vision-confirmed twice, cropB)
function sineIcon(cx, cy, r, color) {
  slide.addShape("ellipse", {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { type: "none" }, line: { color, width: 1 },
  });
  const w = r * 1.1;
  slide.addShape("line", { x: px(cx - w), y: px(cy), w: px(w * 0.5), h: px(w * 0.55), flipV: true, line: { color, width: 0.9 } });
  slide.addShape("line", { x: px(cx - w * 0.5), y: px(cy - w * 0.55), w: px(w * 0.5), h: px(w * 0.55), line: { color, width: 0.9 } });
}

// ---- 1) playlist house chrome (badge numeral 41) -----------------------------
drawHouseChrome(pres, slide, { numeral: 41 });

// ---- 2) title ----------------------------------------------------------------
slide.addText("Encoder – Decoder Transformer", {
  x: px(108), y: px(43), w: px(744), h: px(54),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 34, bold: true, color: C.titleRed,
});

// ---- 3) LEFT SCHEMATIC — Scaled Dot-Product Attention ------------------------
// label (red bold italic, two lines; measured ink x38..200 y210..272)
slide.addText([
  { text: "Scaled Dot-Product", options: { breakLine: true } },
  { text: "Attention", options: {} },
], {
  x: px(34), y: px(210), w: px(168), h: px(62),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 13.5, bold: true, italic: true, color: C.red,
  lineSpacing: 17,
});
// schematic box (measured x58..190 y268..488)
block(58, 268, 132, 220, "FFFFFF", null, { border: C.schGreen, borderW: 1.5 });
// small green corner-square handles at the right corners (cropC-verified zoom anchors;
// measured: original green ink never extends past the border, so squares sit inside)
slide.addShape("rect", { x: px(182), y: px(269), w: px(8), h: px(8), fill: { color: C.schGreen }, line: { type: "none" } });
slide.addShape("rect", { x: px(182), y: px(480), w: px(8), h: px(8), fill: { color: C.schGreen }, line: { type: "none" } });
// inner boxes (measured: MatMul2 x105..173 y296..312; SoftMax x78..144 y328..348;
// Mask x72..148 y360..380; Scale x84..136 y393..413; MatMul1 x78..144 y428..446)
block(105, 296, 68, 16, C.lavender, "MatMul", { fontSize: 7.5, border: C.boxBorder, borderW: 0.75 });
block(78, 328, 66, 20, C.softGreen, "SoftMax", { fontSize: 7.5, border: C.boxBorder, borderW: 0.75 });
block(72, 360, 76, 20, C.pink, "Mask (opt.)", { fontSize: 7, border: C.boxBorder, borderW: 0.75 });
block(84, 393, 52, 20, C.scaleYel, "Scale", { fontSize: 7.5, border: C.boxBorder, borderW: 0.75 });
block(78, 428, 66, 18, C.lavender, "MatMul", { fontSize: 7.5, border: C.boxBorder, borderW: 0.75 });
// circles Q K V — SOLID fills with white letters (measured cy~472.5, d~19)
tokenCircle(91.5, 472.5, 19, C.qRed, "Q", { fontSize: 8 });
tokenCircle(129, 473, 20, C.kvBlue, "K", { fontSize: 8 });
tokenCircle(166.5, 473, 20, C.kvBlue, "V", { fontSize: 8 });
// arrows: Q,K -> bottom MatMul -> Scale -> Mask -> SoftMax -> top MatMul
arrow(91.5, 462, 91.5, 448);
arrow(129, 462, 122, 448);
arrow(111, 427, 111, 415);
arrow(110, 392, 110, 382);
arrow(110, 359, 110, 350);
arrow(111, 327, 122, 314);
// V feeds the top MatMul via the riser (measured x~166.5, y318..461)
arrow(166.5, 462, 166.5, 314);
// output arrow exits the top MatMul upward
arrow(139, 295, 139, 270);

// ---- 4) RIGHT PANEL — full Encoder–Decoder architecture ----------------------
// half fills (measured split x~736) + panel border
block(577, 106, 158, 417, C.encFill, null, {});
block(736, 106, 158, 417, C.decFill, null, {});
block(575, 104, 320, 421, null, null, { border: C.panelGreen, borderW: 2 });
// yellow translucent band behind the encoder group's right portion
// (measured x678..745 y252..322) — drawn before the boxes it sits behind
slide.addShape("rect", {
  x: px(678), y: px(252), w: px(67), h: px(70),
  fill: { color: C.yellow, transparency: 55 }, line: { type: "none" },
});
// panel labels (measured: Encoder x585..650 y116..127; Decoder ~y128..146)
slide.addText("Encoder", {
  x: px(583), y: px(110), w: px(72), h: px(20), margin: 0,
  fontFace: FONT, fontSize: 12, bold: true, italic: true, color: C.red, align: "left",
});
slide.addText("Decoder", {
  x: px(752), y: px(126), w: px(74), h: px(20), margin: 0,
  fontFace: FONT, fontSize: 11, bold: true, italic: true, color: C.red, align: "center",
});
// thick red up-arrow into Output Probabilities (measured x742..750 y117..139)
arrow(746, 140, 746, 117, { color: C.red, width: 3 });

// ===== ENCODER column =====
// residual loop rail (pale green, left of the stack; measured x~628..631)
arrow(630, 392, 630, 270, { color: C.loopEnc, width: 1.25, noHead: true });
arrow(630, 392, 655, 392, { color: C.loopEnc, width: 1.25, noHead: true });
arrow(630, 270, 655, 270, { color: C.loopEnc, width: 1.25, noHead: true });
// "Inputs" text + thick red up-arrow (measured arrow x655..665 y489..511)
slide.addText("Inputs", {
  x: px(664), y: px(496), w: px(48), h: px(14), margin: 0,
  fontFace: FONT, fontSize: 8, color: C.black, align: "left", valign: "middle",
});
arrow(660, 511, 660, 486, { color: C.red, width: 3 });
// Input Embedding (measured x652..724 y445..483)
block(652, 445, 72, 38, C.embBrown, "Input Embedding", { fontSize: 7.5, color: "3A2410" });
// Positional-Encoding band + circle-plus (measured band x652..724 y417..445)
block(652, 417, 72, 28, C.peBrown, null, {});
plusGlyph(684, 431, 9, C.black, 1.25);
sineIcon(663, 431, 7, C.black);
slide.addText([
  { text: "Positional", options: { breakLine: true } },
  { text: "Encoding", options: {} },
], {
  x: px(594), y: px(410), w: px(58), h: px(34), margin: 0,
  fontFace: FONT, fontSize: 6.5, color: C.gray, align: "right", valign: "middle",
  lineSpacing: 8,
});
// token circles (measured: V green ~cx662, K blue ~cx695, Q red ~cx716, cy~402)
tokenCircle(662, 402, 15, C.vGreen, "V", { fontSize: 6 });
tokenCircle(695, 401, 15, C.kvBlue, "K", { fontSize: 6 });
tokenCircle(716, 403, 15, C.qRed, "Q", { fontSize: 6 });
// layer group (measured x636..722 y267..407, olive border, rounded)
block(636, 267, 86, 140, null, null, { border: C.grpBdEnc, borderW: 1.75, round: true });
// Multi-Head Attention (measured x648..723 y354..390, tan fill + red border)
block(648, 354, 75, 37, C.encMhaFill, "Multi-Head\nAttention", {
  fontSize: 6.5, border: C.red, borderW: 1.5, color: "3A2008", lineSpacing: 7.5,
});
// Add & Norm #1 (blue, measured x655..718 y343..352)
block(655, 343, 63, 10, C.blueAN, "Add & Norm", { fontSize: 5.5, color: "102030" });
// Feed Forward (measured x654..720 y288..341, dark olive-gray; 2-line wrap in original)
block(654, 288, 66, 53, C.ffFill, "Feed\nForward", { fontSize: 6.5, color: C.ffText, lineSpacing: 8 });
// Add & Norm #2 (blue, measured x655..718 y276..285)
block(655, 276, 63, 10, C.blueAN, "Add & Norm", { fontSize: 5.5, color: "102030" });
// N× at mid-height left of the stack (measured ~x600..626 y288..331)
slide.addText("N×", {
  x: px(600), y: px(298), w: px(30), h: px(22), margin: 0,
  fontFace: FONT, fontSize: 10, color: C.gray, align: "left",
});
// encoder internal arrows (thin black)
arrow(687, 415, 687, 410);
arrow(687, 394, 687, 392);
arrow(687, 343, 687, 342, { noHead: true });
arrow(687, 288, 687, 287, { noHead: true });
arrow(687, 266, 687, 240); // group output arrow up

// ===== DECODER column =====
// residual loop rail (bright green, right of the stack; measured x~828..838)
arrow(836, 408, 836, 210, { color: C.loopDec, width: 1.25, noHead: true });
arrow(836, 408, 800, 408, { color: C.loopDec, width: 1.25, noHead: true });
arrow(836, 210, 800, 210, { color: C.loopDec, width: 1.25, noHead: true });
// lower rounded group border around decoder A&N + Masked MHA + circles (cropB-verified)
block(742, 326, 98, 84, null, null, { border: C.grpBdDec, borderW: 1, round: true });
// yellow-highlighted "Outputs (shifted right)" — two lines, overflows hl (measured)
slide.addShape("rect", {
  x: px(760), y: px(486), w: px(54), h: px(25),
  fill: { color: C.yellow, transparency: 45 }, line: { type: "none" },
});
slide.addText([
  { text: "Outputs", options: { breakLine: true } },
  { text: "(shifted right)", options: {} },
], {
  x: px(750), y: px(486), w: px(80), h: px(25), margin: 0,
  fontFace: FONT, fontSize: 6, color: C.black, align: "center", valign: "middle",
  lineSpacing: 7.5,
});
// Output Embedding (maroon, measured x751..822 y444..482)
block(751, 444, 71, 38, C.maroon, "Output\nEmbedding", { fontSize: 6.5, color: "FFFFFF", lineSpacing: 7.5 });
// Positional-Encoding band + circle-plus (measured x752..822 y416..442)
block(752, 416, 70, 26, C.peBrownDec, null, {});
plusGlyph(787, 429, 9, C.black, 1.25);
sineIcon(808, 429, 7, C.black);
slide.addText([
  { text: "Positional", options: { breakLine: true } },
  { text: "Encoding", options: {} },
], {
  x: px(824), y: px(406), w: px(68), h: px(36), margin: 0,
  fontFace: FONT, fontSize: 6.5, color: C.gray, align: "left", valign: "middle",
  lineSpacing: 8,
});
// token circles BELOW Masked MHA (measured cy~391: blue V ~751, blue K ~782, red Q ~802)
tokenCircle(751, 391, 13, C.kvBlue, "V", { fontSize: 5.5 });
tokenCircle(782, 391, 13, C.kvBlue, "K", { fontSize: 5.5 });
tokenCircle(802, 391, 13, C.qRed, "Q", { fontSize: 5.5 });
// Masked Multi-Head Attention (purple, measured x748..826 y344..406)
block(748, 344, 78, 62, C.maskedPurple, "Masked\nMulti-Head\nAttention", {
  fontSize: 6, border: C.red, borderW: 1.25, lineSpacing: 7,
});
// Add & Norm #3 (blue, measured x753..817 y330..342)
block(753, 330, 64, 12, C.blueAN, "Add & Norm", { fontSize: 5.5, color: "102030" });
// decoder layer group (measured x744..840 y198..325, olive border, rounded)
block(744, 198, 96, 127, null, null, { border: C.grpBdDec, borderW: 1.75, round: true });
// cross-attention Multi-Head Attention (measured x747..823 y276..311, tan + red border)
block(747, 276, 76, 35, C.xMhaFill, "Multi-Head\nAttention", {
  fontSize: 6, border: C.red, borderW: 1.5, color: "3A2008", lineSpacing: 6.5,
});
// Add & Norm #4 (blue, measured x753..816 y265..274)
block(753, 265, 64, 10, C.blueAN, "Add & Norm", { fontSize: 5.5, color: "102030" });
// Feed Forward (measured x751..818 y222..252; 2-line wrap in original)
block(751, 222, 67, 30, C.ffFill, "Feed\nForward", { fontSize: 6, color: C.ffText, lineSpacing: 7 });
// Add & Norm #5 (blue, measured x753..816 y208..218)
block(753, 208, 64, 11, C.blueAN, "Add & Norm", { fontSize: 5.5, color: "102030" });
// N× right of the stack (measured x840..861 y295..325)
slide.addText("N×", {
  x: px(838), y: px(300), w: px(28), h: px(20), margin: 0,
  fontFace: FONT, fontSize: 10, color: C.gray, align: "left",
});
// decoder box chain: Linear (measured y177..191) and Softmax (y151..166)
block(754, 177, 62, 15, C.linGreen, "Linear", { fontSize: 6.5, border: C.grnBoxBd, borderW: 1 });
block(754, 151, 62, 15, C.smGreen, "Softmax", { fontSize: 6.5, border: C.grnBoxBd, borderW: 1 });
// yellow-highlighted "Output Probabilities" (measured hl x762..810 y112..127;
// original wraps to two lines, second line overflowing the highlight)
slide.addShape("rect", {
  x: px(760), y: px(110), w: px(54), h: px(19),
  fill: { color: C.yellow, transparency: 45 }, line: { type: "none" },
});
slide.addText([
  { text: "Output", options: { breakLine: true } },
  { text: "Probabilities", options: {} },
], {
  x: px(750), y: px(106), w: px(78), h: px(26), margin: 0,
  fontFace: FONT, fontSize: 6.5, color: C.black, align: "center", valign: "middle",
  lineSpacing: 8,
});
// decoder internal arrows (thin black)
arrow(787, 484, 787, 483, { noHead: true });
arrow(787, 415, 787, 400);
arrow(787, 343, 787, 344, { noHead: true });
arrow(787, 329, 787, 326);
arrow(787, 197, 787, 193);
arrow(787, 176, 787, 167);
arrow(787, 150, 787, 131);

// autoregressive dashed loop: from beside "Outputs (shifted right)" up along the
// decoder's right edge to "Output Probabilities" (measured crossing ~(880,218)).
slide.addShape("arc", {
  x: px(800), y: px(106), w: px(88), h: px(400),
  angleRange: [270, 90],
  line: { color: C.darkRed, width: 1.5, dashType: "dash", beginArrowType: "triangle" },
});

// ---- 5) CENTER ZOOM — Multi-Head Attention -----------------------------------
// container (measured tan fill x286..523 y207..526, no strong border)
slide.addShape("roundRect", {
  x: px(286), y: px(207), w: px(237), h: px(319),
  fill: { color: C.tanFill }, line: { type: "none" },
  rectRadius: 0.08,
});
// inner light panel with olive border (measured x296..511 y246..516)
block(296, 246, 215, 270, C.panelLt, null, { border: C.olive, borderW: 1.25 });
// olive L corner brackets on the inner panel (measured legs ~13px, thickness ~3px)
function bracket(cx, cy, dx, dy) {
  arrow(cx, cy, cx + dx, cy, { color: C.olive, width: 2.5, noHead: true });
  arrow(cx + dx, cy, cx + dx, cy + dy, { color: C.olive, width: 2.5, noHead: true });
}
bracket(299, 249, 14, 0);  bracket(313, 249, 0, 12);   // top-left
bracket(508, 249, -14, 0); bracket(494, 249, 0, 12);   // top-right
bracket(299, 513, 14, 0);  bracket(313, 513, 0, -12);  // bottom-left
bracket(508, 513, -14, 0); bracket(494, 513, 0, -12);  // bottom-right
// red-orange label (measured ink x300..475 y210..229, ONE line)
slide.addText("Multi-Head Attention", {
  x: px(296), y: px(206), w: px(215), h: px(26), margin: 0,
  fontFace: FONT, fontSize: 13, bold: true, italic: true, color: C.zoomLabel,
  align: "center", valign: "middle",
});
// SDPA stack: 3 plain tan copies offset UP-RIGHT behind the front card
// (measured: copies peek y328..352 above the front box, right edge to x~487)
block(318, 329, 173, 43, C.stackCopy, null, { border: C.stackCopyBd, borderW: 0.75 });
block(313, 337, 173, 43, C.stackCopy, null, { border: C.stackCopyBd, borderW: 0.75 });
block(308, 345, 173, 43, C.stackCopy, null, { border: C.stackCopyBd, borderW: 0.75 });
// front card (measured x302..481 y353..396, RED border, 2 lines dark-maroon text)
block(302, 353, 179, 43, C.stackFill, "Scaled Dot-Product\nAttention", {
  fontSize: 8.5, border: C.red, borderW: 2, color: C.stackText, lineSpacing: 10.5,
});
// × h annotation (measured ink x484..500 y364..377, dark red-brown)
slide.addText("× h", {
  x: px(478), y: px(358), w: px(26), h: px(24), margin: 0,
  fontFace: FONT, fontSize: 9, bold: true, color: C.xhColor,
  align: "center", valign: "middle",
});
// Concat (measured x361..413 y307..330, LIGHT tan fill + dark text)
block(361, 307, 52, 23, C.concatFill, "Concat", { fontSize: 8, color: "4A2A08", border: C.brownBd, borderW: 1 });
// top Linear (measured x361..414 y266..289)
block(361, 266, 53, 23, C.linTopFill, "Linear", { fontSize: 8, border: C.brownBd, borderW: 1 });
// three bottom Linear boxes with one up-right shadow copy each
// (measured: fronts y409..443 at L≈326/382/438, copies y403..)
[[326], [382], [438]].forEach(([L]) => {
  block(L + 6, 403, 40, 34, C.linFill, null, { border: C.brownBd, borderW: 0.75 });
  block(L, 409, 40, 34, C.linFill, "Linear", { fontSize: 7.5, color: "5A3208", border: C.brownBd, borderW: 1 });
});
// bottom circles V K q (measured cx 330.5/387/443.5, cy~497; q RED, lowercase)
tokenCircle(330.5, 497, 21, C.vKPurple, "V", { fontSize: 8 });
tokenCircle(387, 497, 21, C.vKPurple, "K", { fontSize: 8 });
tokenCircle(443.5, 497, 22, C.qRed, "q", { fontSize: 9 });
// stems from circles up to the Linear boxes
arrow(331, 486, 331, 445, { noHead: true, width: 1 });
arrow(387, 486, 387, 445, { noHead: true, width: 1 });
// thick red up-arrow from q into the rightmost Linear (measured head x426..449 y422..447)
arrow(443, 486, 443, 452, { color: C.red, width: 4, noHead: true });
slide.addShape("triangle", {
  x: px(426), y: px(421), w: px(24), h: px(28),
  fill: { color: C.red }, line: { type: "none" },
});
// center arrows: three dark multi-head arrows stack -> Concat; Concat -> Linear; out
arrow(370, 352, 370, 338, { color: "4A2A08", width: 1 });
arrow(388, 352, 388, 334, { color: "4A2A08", width: 1 });
arrow(406, 352, 406, 338, { color: "4A2A08", width: 1 });
arrow(388, 305, 388, 291);
arrow(388, 265, 388, 248); // output arrow ends at the inner panel's top edge

// ---- 6) red dotted zoom connectors -------------------------------------------
arrow(192, 300, 300, 362, { color: C.red, width: 1, dash: "sysDot", noHead: true });
arrow(192, 425, 300, 390, { color: C.red, width: 1, dash: "sysDot", noHead: true });
arrow(524, 355, 648, 352, { color: C.red, width: 1, dash: "sysDot", noHead: true });
arrow(524, 400, 648, 380, { color: C.red, width: 1, dash: "sysDot", noHead: true });

// ---- 7) WE ARE HERE pin (over the container's top-left corner) ----------------
slide.addShape("triangle", {
  x: px(292), y: px(196), w: px(26), h: px(40), flipV: true, rotate: 325,
  fill: { color: C.red }, line: { type: "none" },
});
slide.addShape("ellipse", {
  x: px(247), y: px(131), w: px(62), h: px(62), rotate: 352,
  fill: { color: C.red }, line: { type: "none" },
});
slide.addText([
  { text: "WE ARE", options: { breakLine: true } },
  { text: "HERE", options: {} },
], {
  x: px(247), y: px(131), w: px(62), h: px(62), rotate: 352,
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 8.5, bold: true, color: "FFFFFF", lineSpacing: 10,
});

// ---- write -------------------------------------------------------------------
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_041_recreated.pptx" })
  .then(() => console.log("WROTE slide_041_recreated.pptx"))
  .catch((e) => { console.error("WRITE FAILED", e); process.exit(1); });
