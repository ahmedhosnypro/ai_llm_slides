// slide_041.js — "Encoder – Decoder Transformer" (Deep Learning DSAI 308,
// Transformers — Part I). Build worker attempt 1, 2026-10-11 (fresh start; prior
// worker died on a provider error with nothing banked — resumed from zero, DB row
// was fully pending).
//
// ROOT slide (no depends_on; `15_progress.py deps` shows root/unblocked).
//
// CONTENT: three-level zoom composition — left "Scaled Dot-Product Attention"
// schematic (paper Fig 2 left), center tan "Multi-Head Attention" zoom (Fig 2
// right) with red WE ARE HERE pin, right full Encoder–Decoder architecture panel
// (Fig 1), tied by red dotted zoom lines. All strings verbatim per
// analysis/slide_041_final.json (gate-passed PASS_WITH_FIXES, score 9; validation
// fixes already applied in that file). Original capitalization preserved:
// 'SoftMax' (left schematic) vs 'Softmax' (right panel), lowercase 'q',
// 'Mask (opt.)', 'N×', '× h', 'Outputs (shifted right)', 'Add & Norm'.
//
// GEOMETRY PROVENANCE: PIL pixel forensics on unique_slides/slide_041.jpg
// (960x540, 1px = 1pt = 1/72 in) — scratch/slide041/measure{1..6}.py scanline
// passes (containers, block bands, circles, highlight bands, red ink). Gated
// vision region reads were attempted 3x for the two dense zones but the shared
// gateway returned EmptyStreamError on every attempt (congested by parallel
// workers); attempt 1 therefore builds on forensics + the validated spec, with
// the mandatory dense-region crop comparisons to follow pre-judge.
//
// LAWS honored: playlist chrome via shared_patterns/house_chrome.js (numeral 41 =
// number printed on the frame); verbatim text; margin:0 + explicit fontFace
// everywhere; explicit lineSpacing on multi-line boxes; no '#' in hex; arrows via
// line shapes with flipV/flipH + endArrowType; single-version deliverable.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);

const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt)
const FONT = "Arial";

// ---- palette: spec hexes for small blocks; scanline-measured hexes for the
// ---- large fills (big flat areas survive JPEG faithfully; small blocks don't).
const C = {
  titleRed: "CC0000",
  red: "CC0000",
  darkRed: "8B0000",
  black: "000000",
  gray: "595959",          // N× / Positional Encoding gray text
  // left schematic
  schGreen: "006400",
  lavender: "C5CAE9",
  scaleYel: "FFF9C4",
  pink: "F8BBD0",
  softGreen: "C8E6C9",
  qRed: "CC2222",
  kvBlue: "2222AA",
  // center zoom
  tanFill: "E8B57E",       // measured (232,181,126)
  tanBorder: "C08040",
  sdpaFill: "C88258",      // measured ~(200,130,88)
  vkPurple: "7B4FA0",
  concatDark: "7A470A",    // measured dark blob (122,71,10)
  linearTop: "DEAB73",     // measured (222,171,116)
  boxBorderBrown: "7A470A",
  // right panel
  panelGreen: "00A000",
  encFill: "F6EBDA",       // measured (246,235,218)
  decFill: "CCFADC",       // measured (204,250,221)
  encBrown: "C89A6A",      // Input Embedding
  maroon: "8B4A4A",        // Output Embedding
  blockGray: "A8A8A8",     // MHA / Add & Norm / Feed Forward
  maskedPurple: "B39DDB",  // Masked Multi-Head Attention
  ltGreen: "A8E8A8",
  vGreen: "2AA82A",
  yellow: "FFFF00",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pres.addSlide();

// ---- helpers ----------------------------------------------------------------
// line from (x0,y0) to (x1,y1) in FRAME PX; arrowhead at the (x1,y1) end.
function arrow(x0, y0, x1, y1, opts = {}) {
  slide.addShape("line", {
    x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
    w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
    flipV: y1 < y0, flipH: x1 < x0,
    line: {
      color: opts.color || C.black, width: opts.width || 1,
      endArrowType: opts.noHead ? undefined : "triangle",
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
function circleToken(cx, cy, d, ring, letter, opts = {}) {
  slide.addShape("ellipse", {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: opts.fill ? { color: opts.fill } : { color: "FFFFFF" },
    line: { color: ring, width: opts.ringW || 1.25 },
  });
  if (letter) {
    slide.addText(letter, {
      x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: opts.fontSize || 8, bold: true,
      color: opts.letterColor || C.black,
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

// ---- 1) playlist house chrome (badge numeral 41) -----------------------------
drawHouseChrome(pres, slide, { numeral: 41 });

// ---- 2) title ----------------------------------------------------------------
slide.addText("Encoder – Decoder Transformer", {
  x: px(108), y: px(43), w: px(744), h: px(54),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 34, bold: true, color: C.titleRed,
});

// ---- 3) LEFT SCHEMATIC — Scaled Dot-Product Attention ------------------------
// label (red bold italic, wraps to two lines)
slide.addText("Scaled Dot-Product Attention", {
  x: px(36), y: px(226), w: px(158), h: px(40),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 12, bold: true, italic: true, color: C.red,
  lineSpacing: 14,
});
// schematic box (white fill, dark-green border) — measured x60..190 y271..490
block(60, 271, 130, 219, "FFFFFF", null, { border: C.schGreen, borderW: 1.5 });
// internal boxes (bottom-to-top; measured y-bands)
block(80, 428, 62, 17, C.lavender, "MatMul", { fontSize: 8 });          // bottom MatMul
block(90, 394, 42, 18, C.scaleYel, "Scale", { fontSize: 8 });           // Scale
block(88, 361, 47, 18, C.pink, "Mask (opt.)", { fontSize: 7.5 });       // Mask (opt.)
block(80, 328, 62, 18, C.softGreen, "SoftMax", { fontSize: 8 });        // SoftMax
block(105, 295, 68, 18, C.lavender, "MatMul", { fontSize: 8 });         // top MatMul
// circles Q K V (measured cy~466)
circleToken(106, 466, 29, C.qRed, "Q", { fontSize: 9 });
circleToken(143, 466, 29, C.kvBlue, "K", { fontSize: 9 });
circleToken(176, 466, 29, C.kvBlue, "V", { fontSize: 9 });
// arrows: Q,K -> bottom MatMul -> Scale -> Mask -> SoftMax -> top MatMul
arrow(106, 451, 106, 447);
arrow(143, 451, 138, 447);
arrow(111, 426, 111, 414);   // MatMul1 -> Scale
arrow(111, 392, 111, 381);   // Scale -> Mask
arrow(111, 359, 111, 348);   // Mask -> SoftMax
arrow(111, 326, 120, 315);   // SoftMax -> top MatMul
// V feeds the top MatMul via the right side (measured vertical at x~188)
arrow(190, 448, 190, 306, { noHead: true });  // long riser
arrow(190, 306, 175, 306);                    // into MatMul2 right edge
// output arrow exits the top MatMul upward
arrow(139, 293, 139, 275);

// ---- 4) RIGHT PANEL — full Encoder–Decoder architecture ----------------------
// half fills (measured split at x~736) + panel border
block(577, 106, 158, 417, C.encFill, null, {});
block(736, 106, 158, 417, C.decFill, null, {});
block(575, 104, 320, 421, null, null, { border: C.panelGreen, borderW: 2 });
// yellow highlight band across the Multi-Head Attention level (measured
// x678..742 y252..322) — drawn behind the blocks it covers
slide.addShape("rect", {
  x: px(678), y: px(252), w: px(64), h: px(70),
  fill: { color: C.yellow, transparency: 55 }, line: { type: "none" },
});
// panel labels
slide.addText("Encoder", {
  x: px(590), y: px(108), w: px(95), h: px(22), margin: 0,
  fontFace: FONT, fontSize: 12, bold: true, italic: true, color: C.red, align: "left",
});
slide.addText("Decoder", {
  x: px(758), y: px(129), w: px(95), h: px(20), margin: 0,
  fontFace: FONT, fontSize: 11, bold: true, italic: true, color: C.red, align: "left",
});

// ===== ENCODER column (blocks x648..726; col center ~687) =====
slide.addText("Inputs", {
  x: px(640), y: px(507), w: px(60), h: px(16), margin: 0,
  fontFace: FONT, fontSize: 8, color: C.black, align: "center",
});
arrow(660, 505, 660, 494, { color: C.red, width: 3 });            // thick red up-arrow
block(648, 448, 78, 44, C.encBrown, "Input Embedding", { fontSize: 7.5 });
plusGlyph(687, 429, 8, C.black, 1);                                // ⊕
slide.addText("Positional\nEncoding", {
  x: px(588), y: px(416), w: px(90), h: px(26), margin: 0,
  fontFace: FONT, fontSize: 7, color: C.gray, align: "right", lineSpacing: 8,
});
circleToken(651, 402, 14, C.vGreen, null, { ringW: 1 });
circleToken(688, 402, 14, C.kvBlue, null, { ringW: 1 });
circleToken(715, 402, 14, C.qRed, null, { ringW: 1 });
block(652, 348, 70, 44, C.blockGray, "Multi-Head\nAttention", {
  fontSize: 6.5, border: C.red, borderW: 1.5, lineSpacing: 7.5,
});
block(658, 322, 58, 20, C.blockGray, "Add & Norm", { fontSize: 6.5 });
// green-outlined group: Add & Norm (top) + Feed Forward
block(640, 252, 90, 66, null, null, { border: C.panelGreen, borderW: 1.25, round: true });
slide.addText("Add & Norm", {
  x: px(646), y: px(255), w: px(78), h: px(14), margin: 0,
  fontFace: FONT, fontSize: 6.5, color: C.black, align: "center",
});
block(648, 274, 74, 38, C.blockGray, "Feed Forward", { fontSize: 6.5 });
// N× at mid-height left of the stack
slide.addText("N×", {
  x: px(606), y: px(300), w: px(34), h: px(20), margin: 0,
  fontFace: FONT, fontSize: 9, color: C.gray, align: "left",
});
// encoder internal arrows (thin black)
arrow(660, 492, 660, 494, { noHead: true }); // (short; thick red arrow covers the span)
arrow(687, 446, 687, 439);
arrow(687, 419, 687, 411);
arrow(687, 393, 687, 395, { noHead: true });
arrow(687, 346, 687, 344);
arrow(687, 320, 687, 320, { noHead: true });
arrow(687, 250, 687, 236);                   // output arrow up
// encoder output feeds right toward the decoder cross-attention (paper Fig 1)
arrow(687, 240, 745, 240, { noHead: true });

// ===== DECODER column (blocks x748..818; col center ~787) =====
// yellow-highlighted "Outputs (shifted right)" (measured band x764..810 y494..508)
slide.addShape("rect", {
  x: px(760), y: px(492), w: px(54), h: px(18),
  fill: { color: C.yellow, transparency: 45 }, line: { type: "none" },
});
slide.addText("Outputs (shifted right)", {
  x: px(748), y: px(492), w: px(78), h: px(18), margin: 0,
  fontFace: FONT, fontSize: 6.5, color: C.black, align: "center", valign: "middle",
});
block(752, 442, 64, 40, C.maroon, "Output\nEmbedding", { fontSize: 6.5, color: "FFFFFF", lineSpacing: 7.5 });
plusGlyph(787, 416, 8, C.black, 1);                                // ⊕
slide.addText("Positional\nEncoding", {
  x: px(799), y: px(403), w: px(88), h: px(26), margin: 0,
  fontFace: FONT, fontSize: 7, color: C.gray, align: "left", lineSpacing: 8,
});
block(750, 342, 66, 65, C.maskedPurple, "Masked\nMulti-Head\nAttention", {
  fontSize: 6.5, border: C.red, borderW: 1.5, lineSpacing: 7.5,
});
circleToken(757, 336, 13, C.vGreen, null, { ringW: 1 });
circleToken(784, 336, 13, C.kvBlue, null, { ringW: 1 });
circleToken(810, 336, 13, C.qRed, null, { ringW: 1 });
block(750, 282, 66, 24, C.blockGray, "Add & Norm", { fontSize: 6.5 });
circleToken(757, 269, 13, C.vGreen, null, { ringW: 1 });
circleToken(784, 269, 13, C.kvBlue, null, { ringW: 1 });
circleToken(810, 269, 13, C.qRed, null, { ringW: 1 });
block(750, 225, 66, 24, C.blockGray, "Multi-Head\nAttention", {
  fontSize: 6, border: C.red, borderW: 1.5, lineSpacing: 6.5,
});
// green-outlined group: Add & Norm (top) + Feed Forward (squeezed — measured)
block(748, 200, 70, 24, null, null, { border: C.panelGreen, borderW: 1, round: true });
slide.addText("Add & Norm", {
  x: px(750), y: px(200), w: px(66), h: px(11), margin: 0,
  fontFace: FONT, fontSize: 5.5, color: C.black, align: "center", valign: "middle",
});
block(752, 212, 62, 11, C.blockGray, "Feed Forward", { fontSize: 5 });
// Linear / Softmax: text on the pale-green half (measured: no distinct fill)
slide.addText("Linear", {
  x: px(758), y: px(176), w: px(52), h: px(14), margin: 0,
  fontFace: FONT, fontSize: 7, color: C.black, align: "center",
});
slide.addText("Softmax", {
  x: px(758), y: px(152), w: px(52), h: px(14), margin: 0,
  fontFace: FONT, fontSize: 7, color: C.black, align: "center",
});
// yellow-highlighted "Output Probabilities" (measured band x764..810 y112..127)
slide.addShape("rect", {
  x: px(760), y: px(110), w: px(54), h: px(19),
  fill: { color: C.yellow, transparency: 45 }, line: { type: "none" },
});
slide.addText("Output Probabilities", {
  x: px(748), y: px(110), w: px(78), h: px(19), margin: 0,
  fontFace: FONT, fontSize: 6.5, color: C.black, align: "center", valign: "middle",
});
arrow(787, 130, 787, 129, { color: C.red, width: 2.5, noHead: true }); // stub under highlight
// N× at mid-height right of the stack (measured ~(850, 301..320))
slide.addText("N×", {
  x: px(844), y: px(300), w: px(34), h: px(20), margin: 0,
  fontFace: FONT, fontSize: 9, color: C.gray, align: "left",
});
// decoder internal arrows (thin black)
arrow(787, 490, 787, 484);
arrow(787, 440, 787, 426);
arrow(787, 405, 787, 409, { noHead: true });
arrow(787, 341, 787, 344, { noHead: true });
arrow(787, 329, 787, 308);
arrow(787, 280, 787, 277, { noHead: true });
arrow(787, 262, 787, 251);
arrow(787, 223, 787, 226, { noHead: true });
arrow(787, 198, 787, 192);
arrow(787, 174, 787, 168, { noHead: true });
arrow(787, 150, 787, 131);

// autoregressive dashed loop: from beside "Outputs (shifted right)" up along the
// decoder's right edge to "Output Probabilities" (measured crossing ~(880,218)).
// OOXML arcs sweep CLOCKWISE: [270,90] = top -> right -> bottom (right semicircle);
// path START is the top point, so the arrowhead rides on beginArrowType.
slide.addShape("arc", {
  x: px(800), y: px(106), w: px(88), h: px(400),
  angleRange: [270, 90],
  line: { color: C.darkRed, width: 1.5, dashType: "dash", beginArrowType: "triangle" },
});

// ---- 5) CENTER ZOOM — Multi-Head Attention -----------------------------------
// container (measured x~286..521 y~208..525)
slide.addShape("roundRect", {
  x: px(286), y: px(208), w: px(235), h: px(318),
  fill: { color: C.tanFill }, line: { color: C.tanBorder, width: 2 },
  rectRadius: 0.08,
});
// dark-green L corner brackets (inset ~5px, leg ~18px, thickness ~2.5px)
function bracket(cx, cy, dx, dy) {
  // horizontal leg + vertical leg of an L pointing into the container
  arrow(cx, cy, cx + dx, cy, { color: C.schGreen, width: 2, noHead: true });
  arrow(cx + dx, cy, cx + dx, cy + dy, { color: C.schGreen, width: 2, noHead: true });
}
bracket(291, 213, 18, 18);    // top-left: right then down
bracket(516, 213, -18, 18);   // top-right: left then down
bracket(291, 521, 18, -18);   // bottom-left: right then up
bracket(516, 521, -18, -18);  // bottom-right: left then up
// red label
slide.addText("Multi-Head Attention", {
  x: px(296), y: px(212), w: px(215), h: px(26), margin: 0,
  fontFace: FONT, fontSize: 15, bold: true, italic: true, color: C.red,
  align: "center", valign: "middle",
});
// SDPA stack: 4 offset copies cascading down-right, front (text) card top-left
block(328, 390, 164, 51, C.sdpaFill, null, { border: C.red, borderW: 2 });   // copy 4
block(320, 378, 164, 51, C.sdpaFill, null, { border: C.red, borderW: 2 });   // copy 3
block(312, 366, 164, 51, C.sdpaFill, null, { border: C.red, borderW: 2 });   // copy 2
block(304, 354, 164, 51, C.sdpaFill, "Scaled Dot-Product\nAttention", {
  fontSize: 9, border: C.red, borderW: 2, lineSpacing: 10.5,
});
// × h annotation with leader line (measured leader x478 y368..389, text ~(500,378))
arrow(470, 380, 480, 377, { color: C.red, width: 1, noHead: true });
slide.addText("× h", {
  x: px(482), y: px(366), w: px(34), h: px(22), margin: 0,
  fontFace: FONT, fontSize: 10, color: C.black, align: "left", valign: "middle",
});
// Concat (measured dark blob x364..412 y300..345) + Linear above it
block(364, 300, 48, 45, C.concatDark, "Concat", { fontSize: 8, color: "FFF8DC" });
block(366, 258, 44, 38, C.linearTop, "Linear", { fontSize: 8, border: C.boxBorderBrown, borderW: 1 });
// three Linear boxes at the bottom (measured borders x329/387/445, y~448..487)
block(331, 448, 56, 39, null, "Linear", { fontSize: 8, border: C.boxBorderBrown, borderW: 1.25 });
block(389, 448, 56, 39, null, "Linear", { fontSize: 8, border: C.boxBorderBrown, borderW: 1.25 });
block(447, 448, 56, 39, null, "Linear", { fontSize: 8, border: C.boxBorderBrown, borderW: 1.25 });
// bottom circles V K q (measured cx 331/387/444, cy ~496) — filled tokens, white letters
slide.addShape("ellipse", {
  x: px(331 - 9.5), y: px(496 - 9.5), w: px(19), h: px(19),
  fill: { color: C.vkPurple }, line: { color: C.vkPurple, width: 0.75 },
});
slide.addText("V", { x: px(331 - 9.5), y: px(496 - 9.5), w: px(19), h: px(19), align: "center", valign: "middle", margin: 0, fontFace: FONT, fontSize: 8, bold: true, color: "FFFFFF" });
slide.addShape("ellipse", {
  x: px(387 - 9.5), y: px(496 - 9.5), w: px(19), h: px(19),
  fill: { color: C.vkPurple }, line: { color: C.vkPurple, width: 0.75 },
});
slide.addText("K", { x: px(387 - 9.5), y: px(496 - 9.5), w: px(19), h: px(19), align: "center", valign: "middle", margin: 0, fontFace: FONT, fontSize: 8, bold: true, color: "FFFFFF" });
slide.addShape("ellipse", {
  x: px(444 - 10.5), y: px(497 - 10.5), w: px(21), h: px(21),
  fill: { color: C.qRed }, line: { color: C.qRed, width: 0.75 },
});
slide.addText("q", { x: px(444 - 10.5), y: px(497 - 10.5), w: px(21), h: px(21), align: "center", valign: "middle", margin: 0, fontFace: FONT, fontSize: 9, bold: true, color: "FFFFFF" });
// center arrows
arrow(359, 446, 359, 443, { noHead: true });   // Linear1 -> stack (short)
arrow(417, 446, 417, 443, { noHead: true });   // Linear2 -> stack
arrow(475, 446, 475, 443, { noHead: true });   // Linear3 -> stack
arrow(388, 352, 388, 347);                     // stack -> Concat
arrow(388, 298, 388, 297, { noHead: true });   // Concat -> Linear(top)
arrow(388, 256, 388, 242);                     // Linear(top) -> output (exits top)

// ---- 6) red dotted zoom connectors -------------------------------------------
// two from the left schematic's right edge converging on the zoomed SDPA block
arrow(192, 300, 300, 362, { color: C.red, width: 1, dash: "sysDot", noHead: true });
arrow(192, 425, 300, 390, { color: C.red, width: 1, dash: "sysDot", noHead: true });
// two from the zoom's right edge to the encoder Multi-Head Attention block
arrow(524, 355, 648, 352, { color: C.red, width: 1, dash: "sysDot", noHead: true });
arrow(524, 400, 648, 380, { color: C.red, width: 1, dash: "sysDot", noHead: true });

// ---- 7) WE ARE HERE pin (over the container's top-left corner) ----------------
// tail first (under the circle)
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
