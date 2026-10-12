// slide_051.js — "Encoder – Decoder Transformer" — FOUNDER-FLAGGED SPECIAL SLIDE
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 51; old extraction 122)
//
// CONTENT SPEC: analysis/slide_051_final.json (validated PASS_WITH_FIXES, score 9).
// Original frame: unique_slides/slide_051.jpg (960x540). Cross-video child of
// deep-learning/001_transformers_part1:18 (certified; shared_image_sources law —
// this slide splits the 001 Fig-1 SOURCE drawing into its ENCODER half and DECODER
// half, placed at THIS frame's measured positions).
//
// SPLIT-HALVES FINDING (PIL-measured 2026-10-12, scratch/slide051/m01..m11 + vision
// probes through the gate): the frame does NOT contain the paper's raster Fig 1
// (its palette is absent: tan 16 px / light-blue 8 px / black 315 px in the whole
// body vs 144k/87k/289k in the banked asset). The two halves are the INSTRUCTOR'S
// OWN REDRAWN architecture — the same certified drawing family as 001 slides
// 17->18->19 (encPanel FBECDB = this frame's peach (253,237,221); decPanel C8F8E0 =
// this frame's mint (206,255,225); steel Add&Norm 6D99B4/5C9CB7 + indigo 6E87E0;
// FF 807560/6E7E62; MHA salmon C87E57 solid-red-framed + tan-brown B28659; Masked
// MHA CE8ADC; maroon embedding B8706C; navy vkBlue 2A26A0 check circles; residual
// green 7FB421/8CC62E; the yellow V/K L-highlight SPLIT across the two panels —
// encoder keeps the bar + right stub (237..289 / 285..289), decoder keeps the
// continuation bar (724..734) + end bar (742..775); a light SEAM at frame x 724..726
// marks the cut). Encoder half sits in the peach panel's LEFT portion; decoder half
// in the mint panel's RIGHT portion; the green overlay (encoder) and orange zone
// (decoder) carry the annotations. SOURCES.md updated with the full record.
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the
// SHARED module videos/deep-learning/shared_patterns/house_chrome.js — badge numeral
// 51 (the number printed on THIS original frame; yellow-fill bbox center (875.5,
// 70.5) matches certified 002 frames exactly).
//
// FRAME->SLIDE MAPPING (certified slide_050 fit, same landmark set: left 58.5,
// right 901.5, top 43, bottom-border 516.5 <-> slide 42, 919, 45, 540):
//   slide_x = (frame_x - 18.128) / 0.961235 ;  slide_y = (frame_y + 0.045) / 0.956566
// (1px frame = 1/0.961235 pt horizontally, 1/0.956566 pt vertically; inch = pt/72.)
// All geometry below is written in FRAME PIXELS and mapped through SX/SY/SW/SH.
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c)):
//   * mouse cursor frozen over the decoder's Linear box area (frame ~785..800,
//     156..171) — capture artifact, not slide content (probe dec_top 6.1).
//   * black bottom letterbox strip, frame rows 519..539 — maps to slide y >= 542.7
//     (BELOW the 540pt slide bottom) = video player strip, not PPT design. The
//     spec's "solid black footer bar" is this letterbox misread as a footer
//     (its "y 96-100%" matches the FRAME, not the slide); omitted per the
//     certified slide_002/050 precedent.
//
// Spec [?] dispositions recorded in slide_051_source/SOURCES.md (halves redrawn;
// no raster; cut seam measured).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const PT = 1 / 72;
const SX = (fx) => ((fx - 18.128) / 0.961235) * PT; // frame px -> inches (x)
const SY = (fy) => ((fy + 0.045) / 0.956566) * PT;  // frame px -> inches (y)
const SW = (w) => (w / 0.961235) * PT;
const SH = (h) => (h / 0.956566) * PT;

const FONT = "Arial";

// ---- palette (JPEG-core measured; 001-certified names where identical) ---------
const P = {
  encPanel: "FBECDB", decPanel: "C8F8E0", maskGreen: "11FF74",
  panelBorder: "00A000", orange: "F2A557", seam: "EADFB8",
  titleRed: "C00000", encLabel: "C00000", decLabel: "0E7D10",
  steel: "6D99B4", steelDec: "5C9CB7", steelBorder: "2F6476", steelText: "1B3A5C",
  indigo: "6E87E0", indigoBorder: "3A5697", indigoText: "2E3E8C",
  ffEnc: "807560", ffDec: "6E7E62", ffBorder: "3E3A28", ffTextEnc: "55482E", ffTextDec: "3A4A2C",
  mhaSalmon: "C87E57", mhaTan: "B28659", mhaText: "703817", mhaBorder: "7B4B2A",
  purple: "CE8ADC", purpleBorder: "562366",
  maroon: "B8706C", maroonBorder: "753029", maroonText: "4A1512",
  brown: "B08058", brownBorder: "6E4423", brownText: "5A3315",
  tanFill: "C8A888", tanBorder: "7B4B2A",
  vkBlue: "2A26A0", qRed: "C00000", vGreen: "55A044", checkGreen: "3C8A32",
  resGreen: "7FB421", resGreenBright: "8CC62E",
  yellow: "FFFF00", dashRed: "8B1010",
  softmaxFill: "A8ECBC", linearFill: "B0E4CE", softBorder: "23655C", softText: "1D5A52",
  ink: "1A1A1A", connLine: "333333", calloutRed: "C00000",
  outputText: "8B0000", probText: "3B3B3B", shiftGreen: "3C8C3C",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- helpers --------------------------------------------------------------------
function rect(x, y, w, h, fill, line, lw, opts = {}) {
  const o = { x: SX(x), y: SY(y), w: SW(w), h: SH(h), fill: { color: fill } };
  if (line) o.line = { color: line, width: lw || 0.75 };
  else o.line = { type: "none" };
  if (opts.dash) o.line.dashType = opts.dash;
  if (opts.round) o.rectRadius = opts.round;
  s.addShape(opts.round ? "roundRect" : "rect", o);
}
function frameOval(x, y, w, h, line, lw, dash) {
  s.addShape("ellipse", {
    x: SX(x), y: SY(y), w: SW(w), h: SH(h),
    fill: { type: "none" }, line: { color: line, width: lw, dashType: dash || "dash" },
  });
}
function lines(color, width, pts, opts = {}) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
    const ln = { color, width };
    if (opts.dash) ln.dashType = opts.dash;
    s.addShape("line", {
      x: SX(Math.min(x0, x1)), y: SY(Math.min(y0, y1)),
      w: SW(Math.abs(x1 - x0)), h: SH(Math.abs(y1 - y0)),
      flipV: y1 < y0, flipH: x1 < x0, line: ln,
    });
  }
}
function check(color, width, x, y, size) {
  // checkmark as two strokes: short down-right, long up-right (x,y = top-left of bbox)
  const x1 = x + size * 0.38, y1 = y + size * 0.55, x2 = x + size, y2 = y;
  lines(color, width, [[x + size * 0.05, y + size * 0.3], [x1, y1], [x2, y2]]);
}
function txt(t, x, y, w, h, size, color, opts = {}) {
  s.addText(t, {
    x: SX(x), y: SY(y), w: SW(w), h: SH(h),
    align: opts.align || "center", valign: opts.valign || "middle", margin: 0,
    fontFace: FONT, fontSize: size, bold: opts.bold !== false,
    italic: !!opts.italic, color, lineSpacing: opts.ls,
  });
}
function multiText(arr, x, y, w, h, size, color, opts = {}) {
  const items = arr.map((t, i) => ({ text: t, options: { breakLine: i < arr.length - 1 } }));
  s.addText(items, {
    x: SX(x), y: SY(y), w: SW(w), h: SH(h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: size, bold: true, color, lineSpacing: opts.ls,
  });
}
function badge(cx, cy, d, fill, glyph, gsize, gcolor) {
  s.addShape("ellipse", {
    x: SX(cx - d / 2), y: SY(cy - d / 2), w: SW(d), h: SH(d),
    fill: { color: fill }, line: { color: fill, width: 0.5 },
  });
  if (glyph === "check") check(gcolor || "FFFFFF", 1.5, cx - d * 0.28, cy - d * 0.22, d * 0.56);
  else if (glyph) txt(glyph, cx - d / 2, cy - d / 2, d, d, gsize || 6, gcolor || "FFFFFF");
}
function upArrow(cx, headY, headW, headH, shaftW, shaftH, color) {
  s.addShape("triangle", {
    x: SX(cx - headW / 2), y: SY(headY), w: SW(headW), h: SH(headH),
    fill: { color }, line: { color, width: 0.5 },
  });
  s.addShape("rect", {
    x: SX(cx - shaftW / 2), y: SY(headY + headH - 1), w: SW(shaftW), h: SH(shaftH),
    fill: { color }, line: { color, width: 0.5 },
  });
}

// ---- 1. house chrome (badge numeral 51) ----------------------------------------
drawHouseChrome(pres, s, { numeral: 51 });

// ---- 2. title --------------------------------------------------------------------
// ink x 224..737 y 58..81 (frame) -> cx 481.0pt, capTop 60.68pt, capH 24.04pt
// width fit 533.7pt/15.282em = 34.9 -> 35.3 (closed-loop re-fit: rendered 1103px vs
// 1111.6 target at 35pt); box y = capTop - 0.274em lead (closed-loop confirmed lead
// 0.274em on attempt 2, matching certified slide_050's 0.273em) -> frame 48.8.
txt("Encoder \u2013 Decoder Transformer", 180, 48.8, 600, 40, 35.3, P.titleRed, {
  align: "center", valign: "top",
});

// ================= ENCODER HALF (left panel) ======================================
// panel + green mask overlay + label
rect(136, 102, 308.5, 401, P.encPanel, P.panelBorder, 1);
rect(292, 103, 152, 398, P.maskGreen, null);
txt("Encoder", 146, 109, 70, 16, 13, P.encLabel, { align: "left", italic: true });

// yellow V/K L-highlight (split; encoder keeps bar + right stub)
rect(237, 243, 52, 15, P.yellow, null);
rect(285, 258, 5, 52, P.yellow, null);

// encoder stack (Add&Norm / Feed Forward / Add&Norm / Multi-Head Attention)
rect(213, 266, 63, 10, P.steel, P.steelBorder, 0.5);
txt("Add & Norm", 213, 266, 63, 10, 5.5, P.steelText);
rect(215, 281, 60, 23, P.ffEnc, P.ffBorder, 0.5);
multiText(["Feed", "Forward"], 215, 281, 60, 23, 6.5, P.ffTextEnc, { ls: 7.5 });
rect(214, 330, 62, 10, P.steel, P.steelBorder, 0.5);
txt("Add & Norm", 214, 330, 62, 10, 5.5, P.steelText);
rect(215, 345, 61, 24, P.mhaSalmon, P.titleRed, 1.25);
multiText(["Multi-Head", "Attention"], 215, 345, 61, 24, 6.5, P.mhaText, { ls: 7.5 });

// green residual bus + stubs (7FB421; bright connectors where measured)
rect(195, 267, 4, 124, P.resGreen, null);
rect(199, 268, 45, 7, P.resGreenBright, null);
rect(199, 314, 45, 7, P.resGreen, null);
rect(199, 333, 45, 7, P.resGreenBright, null);
rect(199, 386.5, 17, 3, P.resGreen, null);
rect(229, 386.5, 17, 3, P.resGreen, null);
// tan residual curve hugging the stack's left (measured x191, y271..384)
lines(P.tanFill, 1.5, [[191.5, 271], [191.5, 384]]);

// checkmarks (measured positions; colors per the frame census)
check("1A1A1A", 1.5, 204, 284, 13);        // black check left of Feed Forward
check(P.titleRed, 1.5, 279, 350, 12);      // red check right of MHA
// light-gray patch under the black check (measured (202,201,197) core)
rect(201, 282, 13, 22, "CBC9C3", null);
check("1A1A1A", 1.5, 203.5, 284.5, 13);

// navy check badges (vkBlue circles with white checks)
badge(214.5, 258, 20, P.vkBlue, "check");
badge(282.5, 329.5, 20, P.vkBlue, "check");

// Q/K/V circles under the MHA box
badge(252, 385.5, 11, P.vkBlue, "K", 5.5);
badge(270, 385.5, 11, P.qRed, "Q", 5.5);
badge(261, 371, 11, P.vGreen, "V", 5.5);

// N x circle + green check badge overlapping it
s.addShape("ellipse", {
  x: SX(160.5), y: SY(319.5), w: SW(21), h: SH(21),
  fill: { color: P.tanFill }, line: { color: P.tanBorder, width: 0.75 },
});
txt("N x", 160.5, 319.5, 21, 21, 7, "333333");
badge(163, 315, 19, P.checkGreen, "check");

// Positional Encoding label (2 lines, measured (160..204, 401..424)); the tan PE
// bar + yellow line sit BETWEEN stack and embedding box (measured y 391..396)
multiText(["Positional", "Encoding"], 157, 400, 50, 26, 6.5, "404040", { ls: 8 });
rect(196, 390.5, 51, 1.5, P.yellow, null);
rect(192, 392, 59, 5, P.tanFill, P.tanBorder, 0.5);

// Output Embedding block (brown) — dark text measured on the fill
rect(211, 400, 71, 63, P.brown, P.brownBorder, 1);
multiText(["Output", "Embedding"], 211, 400, 71, 63, 7, P.brownText, { ls: 9 });

// Inputs red up-arrow + label (measured: head 11x7 at y470, shaft 8x14 to y491)
s.addShape("triangle", {
  x: SX(214), y: SY(470), w: SW(11), h: SH(7),
  fill: { color: P.qRed }, line: { color: P.qRed, width: 0.5 },
});
s.addShape("rect", {
  x: SX(215.5), y: SY(477), w: SW(8), h: SH(14),
  fill: { color: P.qRed }, line: { color: P.qRed, width: 0.5 },
});
txt("Inputs", 227, 477, 34, 12, 7, P.ink);

// ================= DECODER HALF (right panel) =====================================
// orange callout zone + mint stack zone + seam + union border
rect(571, 103, 153, 399, P.orange, null);
rect(727, 103, 149, 399, P.decPanel, null);
rect(724, 103, 3, 399, P.seam, null);
s.addShape("rect", {
  x: SX(568.5), y: SY(102), w: SW(308.5), h: SH(401),
  fill: { type: "none" }, line: { color: P.panelBorder, width: 1 },
});
txt("Decoder", 798, 110, 70, 16, 13, P.decLabel, { align: "right", italic: true });

// Output cluster: red up-arrow + yellow Output box + Probabilities
upArrow(733.5, 106, 18, 10, 8, 27, P.qRed);
rect(752, 110, 44, 13, P.yellow, null);
txt("Output", 752, 110, 44, 13, 7, P.outputText);
txt("Probabilities", 742, 125, 60, 11, 7, P.probText);

// dashed grouping ellipses (behind boxes) + Softmax / Linear + connectors
frameOval(708, 136, 121, 24, P.dashRed, 1);
s.addShape("roundRect", {
  x: SX(738), y: SY(143), w: SW(62), h: SH(12), rectRadius: 0.04,
  fill: { color: P.softmaxFill }, line: { color: P.softBorder, width: 0.75 },
});
txt("Softmax", 738, 143, 62, 12, 6.5, P.softText);
frameOval(700, 159, 134, 25, P.dashRed, 1);
s.addShape("roundRect", {
  x: SX(742), y: SY(166), w: SW(66), h: SH(13), rectRadius: 0.04,
  fill: { color: P.linearFill }, line: { color: P.softBorder, width: 0.75 },
});
txt("Linear", 742, 166, 66, 13, 6.5, P.softText);
lines(P.connLine, 0.75, [[769.5, 136], [769.5, 143]]);
lines(P.connLine, 0.75, [[769.5, 155], [769.5, 166]]);
lines(P.connLine, 0.75, [[769.5, 179], [769.5, 201]]);

// navy check badge at the stack's top-left
badge(738, 197.5, 19, P.vkBlue, "check");

// decoder stack: A&N / FF / A&N / MHA(tan, dashed red ring) / A&N(indigo) / Masked MHA
rect(741, 201, 61, 10, P.steelDec, P.steelBorder, 0.5);
txt("Add & Norm", 741, 201, 61, 10, 5.5, P.steelText);
rect(742, 213, 60, 27, P.ffDec, P.ffBorder, 0.5);
multiText(["Feed", "Forward"], 742, 213, 60, 27, 6.5, P.ffTextDec, { ls: 8 });
rect(741, 255, 61, 10, P.steelDec, P.steelBorder, 0.5);
txt("Add & Norm", 741, 255, 61, 10, 5.5, P.steelText);
frameOval(735, 265, 84, 43, P.titleRed, 1);
rect(742, 271, 60, 24, P.mhaTan, P.mhaBorder, 0.75);
multiText(["Multi-Head", "Attention"], 742, 271, 60, 24, 6.5, P.mhaText, { ls: 7.5 });
rect(742, 318, 58, 11, P.indigo, P.indigoBorder, 0.5);
txt("Add & Norm", 742, 318, 58, 11, 5.5, P.indigoText);
rect(737, 331, 77, 60, P.purple, P.purpleBorder, 1);
multiText(["Masked", "Multi-Head", "Attention"], 737, 331, 77, 60, 6.5, P.purpleBorder, { ls: 8 });

// red ~ (Encoder-Decoder Attention marker) at the Masked MHA's left
txt("\u2248", 727, 341, 22, 20, 11, P.titleRed);

// small navy circles at the attention inputs (measured; letters pending probes)
badge(736.5, 304.5, 10, P.vkBlue, null);
badge(761.5, 304.5, 8, P.vkBlue, null);
badge(738.5, 376, 11, P.vkBlue, null);
badge(782, 376, 12, P.vkBlue, null);

// navy check badges right of the stack
badge(806.5, 255, 20, P.vkBlue, "check");
badge(809.5, 321, 19, P.vkBlue, "check");

// green residual trunk + connectors (right side)
rect(814, 199, 5, 82, P.resGreenBright, null);
rect(815, 329, 5, 61, P.resGreenBright, null);
rect(776, 245, 38, 6, P.resGreen, null);
rect(774, 308, 40, 6, P.resGreen, null);

// four white callouts with red block arrows (c3's ellipse drawn with the stack)
function callout(x, y, w, h, linesArr, fs, ls) {
  rect(x, y, w, h, "FFFFFF", "D8C8B8", 0.5);
  multiText(linesArr, x, y, w, h, fs, P.calloutRed, { ls });
}
callout(575, 145, 81, 17, ["Decoder Only"], 6.5);
s.addShape("rightArrow", { x: SX(663), y: SY(147.5), w: SW(37), h: SH(13), fill: { color: "FFFFFF" }, line: { color: P.calloutRed, width: 1 } });
callout(575, 169, 81, 16, ["Decoder Only"], 6.5);
s.addShape("rightArrow", { x: SX(663), y: SY(171.5), w: SW(37), h: SH(13), fill: { color: "FFFFFF" }, line: { color: P.calloutRed, width: 1 } });
callout(575, 286, 81, 42, ["Encoder \u2013", "Decoder", "Attention"], 6.5, 8);
s.addShape("rightArrow", { x: SX(665), y: SY(297), w: SW(34), h: SH(15), fill: { color: "FFFFFF" }, line: { color: P.calloutRed, width: 1 } });
callout(575, 343, 81, 16, ["Adding Mask"], 6.5);
s.addShape("rightArrow", { x: SX(665), y: SY(346), w: SW(33), h: SH(10), fill: { color: "FFFFFF" }, line: { color: P.calloutRed, width: 1 } });

// Output Embedding block (maroon)
rect(737, 400, 70, 63, P.maroon, P.maroonBorder, 1);
multiText(["Output", "Embedding"], 737, 400, 70, 63, 7, P.maroonText, { ls: 9 });

// bottom: Outputs label (yellow box + green '(shifted right)' below, measured)
rect(751, 474, 45, 15, P.yellow, null);
txt("Outputs", 751, 474, 45, 15, 6.5, P.ink);
txt("(shifted right)", 742, 489, 72, 11, 6.5, P.shiftGreen);

// ---- write -----------------------------------------------------------------------
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_051_recreated.pptx" })
  .then(() => console.log("WROTE slide_051_recreated.pptx"));
