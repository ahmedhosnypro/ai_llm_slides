// build/slide_057.js — slide 057 full encoder-decoder stack (002_transformers_part2,
// Deep Learning DSAI 308). Builder: zcoordinator-agent resume 2026-10-13 02:07 (RESUME.md).
//
// DEPENDENCY CONTRACT + FORK HEADER (banked verdicts; RESUME.md is authoritative):
//  * COMPOSITION PROVENANCE: slide 049's certified stacked-encoder composition RESTYLED
//    tan/red at 057's measured geometry (v_comp_vs049 YES-identity; v_comp_vs047 NOT-47 —
//    supersedes the original brief's "encoder from 047"; the 57<-49 re-anchor is pending
//    founder ratification, DB edge stays 47). Fork mechanisms at 057 geometry per the
//    certified 47<-46 restyle precedent (m18_ffdiff): 049's DELTA blocks are NOT called
//    (they are full-width; 057 compresses the encoder to the left half and adds decoder,
//    central striped column, K/V/Q feeds and the color legend).
//  * FOUNDER DEPENDENCY EDGE 57<-47 honored: the certified components/slide_047.js is
//    required below BY ABSOLUTE PATH and its 0-BASED SUBS label law is reused verbatim
//    for the token chips (never edited; cascade law).
//  * FRAME->SLIDE MAPPING: certified fit SX=.962329 OX=17.582 SY=.955556 (== 047/049/026);
//    px/x/y/w/h helpers imported from components/slide_026.js (the same helpers 049 uses).
//  * GRID: 8 cols [114.5,150,185.5,221,256.5,292,384.5,419.5] (word boxes x102..434, stack
//    dots x114..420, Y/X chip censuses). Chip labels 0-BASED [0..5,N-2,N-1] = P047.SUBS
//    (049-identity law + v_M6/M7 storm reads); word labels Word0..5,N-2,N-1 (v_M7).
//  * BADGE: numeral 57 = the number printed on slide_057.jpg (v_badge crop-read).
//  * OMITTED per GROUND RULES(c) + builder3 banked decisions: cursor artifact on the
//    central column (v_J_blue), bottom player strip, spec's "Tokens" brace label (brace
//    unlabeled per v_A_dec_top/v_A2/v_blk4), purple-bar end labels (p3 census solid ends;
//    v_blk4/v_K2 not-resolvable). Sketched (unresolvable <5px, documented): right-margin
//    dark marks x822..837 y263..298.
//  * ALL coordinates below are FRAME px on the 960x540 frame; helpers convert.

const P049 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_049.js"); // composition provenance (banked)
const P047 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_047.js"); // founder edge 57<-47; SUBS 0-based
const P026 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_026.js"); // certified mapping helpers
const chrome = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const { x, y, w, h } = P026; // frame px -> slide in
const SUBS = P047.SUBS; // ["0".."5","N-2","N-1"] — 0-based label law

const F = "Arial";
const FS = "Times New Roman";

// ---- palette (PIL census cores / storm vision reads; frame wins over spec) ----
const C = {
  encFill: "CCC1B3", encLine: "7A2318",            // encoder container tan + dark maroon border
  purpleBar: "584592",                              // Encoder Block bars
  navy: "00008B", dot: "04048C",
  pinkArrow: "F2C9D6", redLine: "C00000",
  greenArrow: "D8EFC8", greenArrowLine: "2E8B57",
  chipCream: "FDF3DC", chipPink: "F2C4CC", chipPink2: "F6D8E0", chipLine: "6A1A1A",
  lemon: "FFF3C8", warm2: "FFE0A8", warm3: "FFAD7A", warm4: "FF8D6A", warm5: "F8B8B0", warm6: "F8D0D0",
  labelRed: "8E1A1A",
  embTan: "F4CEA4", embOrange: "E07018", peGreen: "DFF5D0", peNavy: "2838A0",
  wordFill: "FBE0CC", wordLine: "C04030", grayDot: "8A8A8A",
  colFill: "B4AEE6", colStripe: "E0E0FA", colLine: "1A1160", fan: "8D8AB5",
  badgeFill: "FFF8E0", badgeLine: "B02020", badgeInk: "8E2E31",
  hatchFill: "C8C4F0", hatchLine: "333399",
  decFill: "C0EBD0", decLine: "2E8E38",
  maroon: "7A1F1F", ffnGreen: "1E9028",
  teal: "3AA8A8", magenta: "B400C8", fanTeal: "2E8E8E", gbox: "A5EFC0", gboxLine: "1E8E3E",
  gcircle: "9FE8AC",
  bFill: "D6EEDC", bLine: "8A9070",
  attnFill: "001878", attnLine: "3078C0", attnShadow: "58A8C8",
  sage: "A8C0A8", sageLine: "789878",
  seg1: "FFFCE8", seg2: "F0F0D8", seg3: "E8E8C8", segLine: "888878",
  stripFill: "FFF8E0", stripLine: "8A8A60", tan4: "D2C088", tan4Line: "8A7A40",
  lavFill: "CFC1E2", lavLine: "C893C4",
  purpleBarDec: "5C186E",
  tokFill: "C8E8C8", tokLine: "5A9A6A", tokInk: "A03020", tokStrip: "E0F4DC",
  hollowFill: "E8E0F8", hollowLine: "5A2E98",
  green3: "1E8E3E", blue3: "2038C8",
  decGreen: "1E8E3E", encRed: "C00000",
};

// 8-column grid (frame px centers)
const COLS = [114.5, 150, 185.5, 221, 256.5, 292, 384.5, 419.5];
// 5 decoder column centers (attn boxes etc.)
const DCOLS = [603, 645.5, 690.5, 739, 781];
const DBOX = [586, 629, 674, 722, 765]; // attn/masked/token box left edges (w 34)

// ---- helpers (frame px in) ----
function rect(s, p, fx, fy, fw, fh, o = {}) {
  s.addShape(p.ShapeType.rect, {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh),
    fill: o.fill ? { color: o.fill } : { type: "none" },
    line: o.line === null ? { type: "none" }
      : { color: (o.line && o.line.color) || C.navy, width: (o.line && o.line.width) || 1,
          dashType: (o.line && o.line.dashType) || "solid" },
  });
}
function rrect(s, p, fx, fy, fw, fh, r, o = {}) {
  s.addShape(p.ShapeType.roundRect, {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh), rectRadius: r,
    fill: o.fill ? { color: o.fill } : { type: "none" },
    line: o.line === null ? { type: "none" }
      : { color: (o.line && o.line.color) || C.navy, width: (o.line && o.line.width) || 1 },
  });
}
function txt(s, p, t, fx, fy, fw, fh, o = {}) {
  s.addText(t, {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh),
    align: o.align || "center", valign: o.valign || "middle", margin: 0,
    fontFace: o.font || F, fontSize: o.size || 8, bold: !!o.bold, italic: !!o.italic,
    color: o.color || "FFFFFF", lineSpacing: o.ls || undefined, charSpacing: o.cs || undefined,
    vert: o.vert || undefined, wrap: o.wrap === false ? false : true,
  });
}
function dot(s, p, fx, fy, fd, color, outline) {
  s.addShape(p.ShapeType.ellipse, {
    x: x(fx - fd / 2), y: y(fy - fd / 2), w: w(fd), h: h(fd),
    fill: color ? { color } : { type: "none" },
    line: outline ? { color: outline.color, width: outline.width || 0.75 } : { type: "none" },
  });
}
function seg(s, p, fx0, fy0, fx1, fy1, color, width) {
  s.addShape(p.ShapeType.line, {
    x: x(Math.min(fx0, fx1)), y: y(Math.min(fy0, fy1)),
    w: w(Math.abs(fx1 - fx0)), h: h(Math.abs(fy1 - fy0)),
    flipH: fx1 < fx0, flipV: fy1 < fy0,
    line: { color, width },
  });
}
function upArrow(s, p, fx, fy, fw, fh, fill, lineColor, lineW) {
  s.addShape(p.ShapeType.upArrow, {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh),
    fill: { color: fill }, line: lineColor ? { color: lineColor, width: lineW || 0.75 } : { type: "none" },
  });
}
function downArrow(s, p, fx, fy, fw, fh, fill) {
  s.addShape(p.ShapeType.downArrow, {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh),
    fill: { color: fill }, line: { type: "none" },
  });
}
function rightArrow(s, p, fx, fy, fw, fh, fill, lineColor, lineW) {
  s.addShape(p.ShapeType.rightArrow, {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh),
    fill: { color: fill }, line: lineColor ? { color: lineColor, width: lineW || 1 } : { type: "none" },
  });
}
function hatch(s, p, fx, fy, fw, fh, n) { // filled arrow + diagonal hatch lines
  rightArrow(s, p, fx, fy, fw, fh, C.hatchFill, C.hatchLine, 1.25);
  for (let k = 1; k <= n; k++) {
    const sx = fx + (fw * k) / (n + 1);
    seg(s, p, sx, fy + fh - 1, Math.min(sx + fh * 0.8, fx + fw - 1), fy + 1, C.hatchLine, 0.5);
  }
}
function chipLabel(s, p, letter, sub, fx, fy, fw, fh, size) {
  s.addText([
    { text: letter, options: { italic: true } },
    { text: sub, options: { italic: true, subscript: true } },
  ], {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh),
    align: "center", valign: "middle", margin: 0,
    fontFace: FS, fontSize: size, bold: true, color: C.labelRed,
  });
}
function attnBox(s, p, fx, fy, fw, fh, lines, ls, sz) {
  rect(s, p, fx + 2.5, fy + 2.5, fw, fh, { fill: C.attnShadow, line: null }); // 3-D shadow lower-right
  rect(s, p, fx, fy, fw, fh, { fill: C.attnFill, line: { color: C.attnLine, width: 0.75 } });
  s.addText(lines.map((t, i) => ({ text: t, options: { breakLine: i < lines.length - 1 } })), {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: sz || 5, bold: true, color: "FFFFFF", lineSpacing: ls || 5.5, wrap: false,
  });
}
function redBar(s, p, fy) {
  rect(s, p, 588, fy, 793 - 588, 7, { fill: C.maroon, line: null });
  txt(s, p, "Residual Connection and Layer Normalization", 588, fy, 793 - 588, 7, { size: 5.5, bold: true });
}
function ffnBar(s, p, fy) {
  rect(s, p, 587, fy, 794 - 587, 9, { fill: C.ffnGreen, line: null });
  txt(s, p, "Feed Forward Networks - One Hidden with RELU Activation", 587, fy, 794 - 587, 9,
    { size: 5, bold: true, italic: true });
}
function decoderBlock(s, p, fyTop, fyBot, sqY, sqN) { // pale-green container + square groups
  rrect(s, p, 581, fyTop, 801 - 581, fyBot - fyTop, 0.08, { fill: C.bFill, line: { color: C.bLine, width: 1.25 } });
  for (const cx of DCOLS) {
    for (let k = 0; k < sqN; k++) {
      rect(s, p, cx - (sqN * 4.5) / 2 + k * 4.5, sqY, 4, 5,
        { fill: k % 2 ? C.seg2 : C.seg1, line: { color: C.segLine, width: 0.5 } });
    }
  }
}

// ---- ENCODER (049 mechanism, tan/red restyle, left half) ----
function drawEncoder(s, p) {
  // container
  rect(s, p, 65, 131, 448 - 65, 510 - 131, { fill: C.encFill, line: { color: C.encLine, width: 2 } });
  // top-border nubs (one per chip pitch; v_yrow)
  for (const cx of COLS) rect(s, p, cx - 1.5, 129.5, 3, 3, { fill: C.encLine, line: null });
  // green up-arrows container-top -> Y row (v_M8; 049 drawGreenArrows mechanism)
  for (const cx of COLS) upArrow(s, p, cx - 6.5, 106, 13, 24, C.greenArrow, C.greenArrowLine, 0.75);
  // 4 purple bars
  const bars = [
    { t: "Encoder Block M", y0: 152, y1: 176 },
    { t: "Encoder Block 2", y0: 250, y1: 273 },
    { t: "Encoder Block 1", y0: 291, y1: 315 },
    { t: "Encoder Block 0", y0: 333, y1: 356 },
  ];
  for (const b of bars) {
    rect(s, p, 100, b.y0, 435 - 100, b.y1 - b.y0, { fill: C.purpleBar, line: null });
    txt(s, p, b.t, 100, b.y0, 435 - 100, b.y1 - b.y0, { size: 11, bold: true });
  }
  // navy dot columns between Block M and Block 2 (8 cols x 5 dots)
  for (const cx of COLS) for (const dy of [186, 196.5, 207, 217.5, 228]) dot(s, p, cx, dy, 6, C.dot);
  // pink/red up-arrows in the two gaps (probe a: pink fill + red ink; 049 mechanism)
  for (const cx of COLS) {
    upArrow(s, p, cx - 5, 276, 10, 13, C.pinkArrow, C.redLine, 0.75);
    upArrow(s, p, cx - 5, 318, 10, 13, C.pinkArrow, C.redLine, 0.75);
  }
  // purple hollow up-arrows: Block0 -> X row (tall), X row <- bars-top band, word -> bars
  for (const cx of COLS) {
    upArrow(s, p, cx - 6.5, 358, 13, 25, C.hollowFill, C.hollowLine, 1.25);
    upArrow(s, p, cx - 6, 401, 12, 14, C.hollowFill, C.hollowLine, 1.25);
    upArrow(s, p, cx - 6, 461, 12, 15, C.hollowFill, C.hollowLine, 1.25);
  }
  // Y chips (5 stripes: pale yellow / white-pink alternating; v_M5) + labels
  for (let i = 0; i < 8; i++) {
    const cx = COLS[i], bx = cx - 15;
    const stripes = [C.chipPink, C.chipCream, C.chipPink2, C.chipCream, C.chipPink];
    for (let k = 0; k < 5; k++) rect(s, p, bx + k * 6, 110.5, 6, 16, { fill: stripes[k], line: null });
    rect(s, p, bx, 110.5, 30, 16, { line: { color: C.chipLine, width: 0.75 } });
    chipLabel(s, p, "Y", SUBS[i], bx - 1, 108.5, 32, 20, 8.5);
  }
  for (let k = 0; k < 5; k++) dot(s, p, 314 + k * 13, 118, 4.5, C.navy); // Y ellipsis
  // X chips (warm gradient stripes; v_M6) + labels
  for (let i = 0; i < 8; i++) {
    const cx = COLS[i], bx = cx - 15;
    const stripes = [C.lemon, C.warm2, C.warm3, C.warm4, C.warm5, C.warm6];
    for (let k = 0; k < 6; k++) rect(s, p, bx + k * 5, 384.5, 5, 16, { fill: stripes[k], line: null });
    rect(s, p, bx, 384.5, 30, 16, { line: { color: C.wordLine, width: 0.75 } });
    chipLabel(s, p, "X", SUBS[i], bx - 1, 382.5, 32, 20, 8.5);
  }
  for (let k = 0; k < 5; k++) dot(s, p, 314 + k * 13, 392, 4.5, "00B050"); // X ellipsis (bright green, v_M6)
  // embedding box (black border; tan Word Embedding + pale green PE bar; v_M7)
  rect(s, p, 100, 416, 436 - 100, 460 - 416, { fill: "FFFFFF", line: { color: "111111", width: 2 } });
  rect(s, p, 102, 418, 434 - 102, 438 - 418, { fill: C.embTan, line: null });
  txt(s, p, "Word Embedding", 102, 418, 434 - 102, 20, { size: 9, bold: true, color: C.embOrange });
  seg(s, p, 102, 438.5, 434, 438.5, "2E8BC0", 1);
  rect(s, p, 102, 439, 434 - 102, 458 - 439, { fill: C.peGreen, line: null });
  txt(s, p, "Positional  Encoding / Embedding", 102, 439, 434 - 102, 19, { size: 8.5, bold: true, color: C.peNavy });
  // word row (peach boxes, red serif italic; v_M7/v_wordsbars)
  for (let i = 0; i < 8; i++) {
    const cx = COLS[i];
    rect(s, p, cx - 13, 477, 26, 16, { fill: C.wordFill, line: { color: C.wordLine, width: 0.75 } });
    txt(s, p, "Word " + SUBS[i], cx - 14, 475, 28, 20, { font: FS, size: 6.5, italic: true, color: C.labelRed, wrap: false });
  }
  for (let k = 0; k < 6; k++) dot(s, p, 302 + k * 14, 485, 4, null, { color: C.grayDot, width: 0.75 });
  // vertical red "Encoder" label (v_M11: bold, NOT italic, bottom-to-top)
  txt(s, p, "Encoder", 73, 256, 16, 104, { vert: "vert270", size: 15, bold: true, color: C.encRed, cs: 2 });
  // color legend (v_L_caption + judge attempt 2 + PIL row scan of the original: sits in the
  // CENTER column below the striped stack; ink x463..535, rows red y426-443 / green y444-462 /
  // blue y463-482 → ~15.5pt bold italic, left-aligned, ~18.5px pitch)
  txt(s, p, "Encoder", 466, 426, 76, 17, { size: 15.5, bold: true, italic: true, color: C.encRed, align: "left" });
  txt(s, p, "Decoder", 466, 444.5, 76, 17, { size: 15.5, bold: true, italic: true, color: C.green3, align: "left" });
  txt(s, p, "Attention", 466, 463, 76, 17, { size: 15.5, bold: true, italic: true, color: C.blue3, align: "left" });
}

// ---- CENTRAL striped column + K/V/Q feeds ----
function drawCentral(s, p) {
  // striped column x470..503 y100..418
  rect(s, p, 470.5, 100, 502.5 - 470.5, 418 - 100, { fill: C.colFill, line: null });
  for (let k = 0; k < 8; k++) rect(s, p, 474 + k * 3.5, 100, 1.4, 318, { fill: C.colStripe, line: null });
  seg(s, p, 470.5, 100, 470.5, 418, C.colLine, 1.5);
  seg(s, p, 501.5, 100, 501.5, 418, C.colLine, 1.5);
  // bus + descender + fan to Y chips
  seg(s, p, 150, 60, 494, 60, C.fan, 1.5);
  seg(s, p, 469, 58, 469, 102, C.fan, 1.5);
  for (const cx of COLS) seg(s, p, 468, 60, cx, 106, C.fan, 1);
  // K feed
  dot(s, p, 518, 168, 20, C.badgeFill, { color: C.badgeLine, width: 1.25 });
  txt(s, p, "K", 508, 158, 20, 20, { font: FS, size: 11, bold: true, color: C.badgeInk });
  rightArrow(s, p, 528, 163, 26, 12, "FFFFFF", C.redLine, 1);
  // V feed
  dot(s, p, 519, 265, 20, C.badgeFill, { color: C.badgeLine, width: 1.25 });
  txt(s, p, "V", 509, 255, 20, 20, { font: FS, size: 11, bold: true, color: C.badgeInk });
  rightArrow(s, p, 528, 262, 26, 12, "FFFFFF", C.redLine, 1);
  // big hatched arrow -> attn1; 3 thin hatched -> squares band; hatched -> attn2/attn3
  hatch(s, p, 505, 181, 50, 15, 3);
  hatch(s, p, 505, 215, 43, 8, 2);
  hatch(s, p, 505, 227, 43, 8, 2);
  hatch(s, p, 505, 240, 43, 8, 2);
  hatch(s, p, 505, 305, 50, 12, 3);
  hatch(s, p, 505, 384, 50, 15, 3);
  // tiny Q badges at attn2/attn3 left + pale-green feed lines
  dot(s, p, 578, 302, 9, C.badgeFill, { color: C.badgeLine, width: 0.75 });
  txt(s, p, "Q", 573, 297, 10, 10, { font: FS, size: 5, bold: true, color: C.badgeInk });
  dot(s, p, 577, 383, 9, C.badgeFill, { color: C.badgeLine, width: 0.75 });
  txt(s, p, "Q", 572, 378, 10, 10, { font: FS, size: 5, bold: true, color: C.badgeInk });
  seg(s, p, 556, 315.5, 577, 315.5, "7ED07E", 1);
  seg(s, p, 556, 396.5, 576, 396.5, "7ED07E", 1);
  // bottom-right Q badge + thick up arrow (v_H/v_K2: white fill, red/maroon outline, serif Q)
  upArrow(s, p, 827, 399, 10, 30, "FFFFFF", C.maroon, 1.5);
  dot(s, p, 833, 437, 16, "F5F0D0", { color: C.badgeLine, width: 1.25 });
  txt(s, p, "Q", 825, 429, 16, 16, { font: FS, size: 9, bold: true, color: C.badgeInk });
}

// ---- DECODER (measured band inventory; flow bottom-up) ----
function drawDecoder(s, p) {
  // panel
  rrect(s, p, 555, 49, 854 - 555, 516 - 49, 0.06, { fill: C.decFill, line: { color: C.decLine, width: 2 } });
  // red brace over the white-circle row (unlabeled per banked GROUND RULES(c)).
  // attempt-1 lesson: preset leftBrace + rotate renders as a displaced vertical bar in LO
  // (judge MAJOR: line crossing the house frame). Deterministic arch instead: top half of
  // a wide flat ellipse, ends at the circle-row top, peak above it (v_A2 "arching over").
  s.addShape(p.ShapeType.arc, {
    x: x(592), y: y(46), w: w(793 - 592), h: h(68 - 46),
    angleRange: [180, 360], fill: { type: "none" }, line: { color: C.maroon, width: 1.5 },
  });
  // white circles + navy stems
  for (let k = 0; k < 17; k++) {
    const cx = 597.5 + k * 11.97;
    seg(s, p, cx, 67, cx, 71, "001878", 1);
    dot(s, p, cx, 64, 7, "FFFFFF", { color: C.teal, width: 0.75 });
  }
  // Softmax bar
  rect(s, p, 594, 70.5, 791 - 594, 6, { fill: C.maroon, line: null });
  txt(s, p, "Softmax", 594, 70.5, 791 - 594, 6, { size: 5.5, bold: true });
  // green box: magenta circles + fan + green circles
  rrect(s, p, 592, 81, 793 - 592, 121 - 81, 0.1, { fill: C.gbox, line: { color: C.gboxLine, width: 1.5 } });
  const mxs = [];
  for (let k = 0; k < 16; k++) mxs.push(604 + k * 11.85);
  for (const cx of DCOLS) {
    for (const mx of mxs) seg(s, p, mx, 95, cx, 107, C.fanTeal, 0.5);
  }
  for (const mx of mxs) dot(s, p, mx, 91.5, 7.5, C.magenta);
  for (const cx of DCOLS) dot(s, p, cx, 114, 15, C.gcircle, { color: C.gboxLine, width: 1.25 });
  // pale-green block containers (drawn before their contents)
  decoderBlock(s, p, 123, 202, 0, 0); // B1 shell (squares drawn below)
  for (const cx of DCOLS) for (let k = 0; k < 5; k++)
    rect(s, p, cx - 11 + k * 4.5, 127, 4, 5, { fill: k % 2 ? C.seg2 : C.seg1, line: { color: C.segLine, width: 0.5 } });
  decoderBlock(s, p, 249, 326, 0, 0); // B2 shell
  for (const cx of DCOLS) for (let k = 0; k < 5; k++)
    rect(s, p, cx - 15 + k * 6, 253, 5.5, 8, { fill: [C.seg1, C.seg2, C.seg3][k % 3], line: { color: C.segLine, width: 0.5 } });
  decoderBlock(s, p, 331, 405, 335, 4); // B3 shell + its square groups
  // B1 contents
  for (const cx of DCOLS) downArrow(s, p, cx - 2.5, 137, 5, 6, C.attnFill);
  redBar(s, p, 143.5);
  ffnBar(s, p, 152.5);
  redBar(s, p, 164);
  for (const cx of DCOLS) upArrow(s, p, cx - 3, 171, 6, 5, C.attnFill);
  for (const bx of DBOX) attnBox(s, p, bx, 176, 34, 21, ["Encoder", "Decoder", "Attention"]);
  // open band: sage rects 5x3 + seg-bar row + down arrows (B2 contents)
  for (const cx of DCOLS) for (let r = 0; r < 3; r++)
    rect(s, p, cx - 6.5, [217, 228.5, 240][r], 13, 8.5, { fill: C.sage, line: { color: C.sageLine, width: 0.75 } });
  for (const cx of DCOLS) downArrow(s, p, cx - 2.5, 261, 5, 6, C.attnFill);
  redBar(s, p, 268);
  ffnBar(s, p, 277);
  redBar(s, p, 288);
  for (const cx of DCOLS) upArrow(s, p, cx - 3, 294, 6, 5, C.attnFill);
  for (const bx of DBOX) attnBox(s, p, bx, 299, 34, 21, ["Encoder", "Decoder", "Attention"]);
  // B3 contents
  redBar(s, p, 348);
  ffnBar(s, p, 359);
  redBar(s, p, 368);
  for (const cx of DCOLS) upArrow(s, p, cx - 3, 377, 6, 5, C.attnFill);
  for (const bx of DBOX) attnBox(s, p, bx, 382, 34, 20, ["Encoder", "Decoder", "Attention"]);
  for (const bx of DBOX) { // tiny red+blue square pairs at top-right corners (v_K2)
    rect(s, p, bx + 35.5, 383.5, 3, 3, { fill: "C04040", line: null });
    rect(s, p, bx + 39.5, 383.5, 3, 3, { fill: "3050C0", line: null });
  }
  // strips: gray-outlined units holding 4 tan squares + down arrows (v_K1 Row A / v_K2)
  for (const cx of DCOLS) {
    rect(s, p, cx - 15, 403, 30, 9, { fill: C.stripFill, line: { color: C.stripLine, width: 0.75 } });
    for (let k = 0; k < 4; k++) rect(s, p, cx - 10 + k * 5.5, 405, 4, 5, { fill: C.tan4, line: { color: C.tan4Line, width: 0.5 } });
  }
  for (const cx of DCOLS) downArrow(s, p, cx - 2.5, 423, 5, 6, C.attnFill);
  // lavender panel
  rrect(s, p, 569, 427, 817 - 569, 511 - 427, 0.08, { fill: C.lavFill, line: { color: C.lavLine, width: 1.25 } });
  redBar(s, p, 432);
  for (const cx of DCOLS) seg(s, p, cx, 441, cx, 444, C.attnFill, 1);
  for (const bx of DBOX) attnBox(s, p, bx, 444, 34, 19, ["Multi-Head", "Self-Attention"], 6, 4.5);
  // red attention arcs between masked boxes
  for (let k = 0; k < 4; k++) {
    s.addShape(p.ShapeType.arc, {
      x: x(DBOX[k] + 33), y: y(448), w: w(DBOX[k + 1] - DBOX[k] - 32), h: h(13),
      angleRange: [180, 360], fill: { type: "none" }, line: { color: "C03030", width: 0.75 },
    });
  }
  // band-6 boxes: 2 staggered rows of multicolored squares (v_K2)
  const mc = ["C04040", "3050C0", "E0C040", "E08030", "40A060"];
  for (const bx of DBOX) {
    rect(s, p, bx, 463, 34, 14, { fill: "DFF5C8", line: { color: "8A9A70", width: 0.75 } });
    for (let k = 0; k < 5; k++) rect(s, p, bx + 7 + k * 4.2, 465, 3.5, 3.5, { fill: mc[k % 5], line: null });
    for (let k = 0; k < 4; k++) rect(s, p, bx + 9 + k * 4.2, 470, 3.5, 3.5, { fill: mc[(k + 2) % 5], line: null });
  }
  for (const cx of DCOLS) seg(s, p, cx, 477, cx, 487, C.attnFill, 1);
  // purple bar (v_blk4 + v_K2: "Word and Position Encoding")
  rect(s, p, 593, 487.5, 792 - 593, 8.5, { fill: C.purpleBarDec, line: null });
  txt(s, p, "Word and Position Encoding", 593, 487.5, 792 - 593, 8.5, { size: 6, bold: true });
  // bottom token boxes (v_K1/v_token5: tan squares, red text, divider, lighter strip)
  const toks = ["SOS", "Je", "ne", "suis", "faisait"];
  for (let i = 0; i < 5; i++) {
    const bx = DBOX[i];
    rrect(s, p, bx, 497, 34, 18, 0.12, { fill: C.tokFill, line: { color: C.tokLine, width: 0.75 } });
    for (let k = 0; k < 4; k++) rect(s, p, bx + 8 + k * 5, 498.5, 4, 4, { fill: C.tan4, line: { color: C.tan4Line, width: 0.5 } });
    txt(s, p, toks[i], bx, 503.5, 34, 8, { size: 5, bold: true, color: C.tokInk });
    seg(s, p, bx + 3, 511.5, bx + 31, 511.5, C.tokLine, 0.5);
    rect(s, p, bx + 1.5, 512, 31, 2.5, { fill: C.tokStrip, line: null });
  }
  // vertical green "Decoder" label (v_M12: bold sans-serif, bottom-to-top)
  txt(s, p, "Decoder", 838, 232, 19, 100, { vert: "vert270", size: 20, bold: true, color: C.decGreen, cs: 2 });
}

// ---- composition ----
function compose(pres) {
  const s = pres.addSlide();
  chrome.drawHouseChrome(pres, s, { numeral: 57 });
  drawDecoder(s, pres);
  drawCentral(s, pres);
  drawEncoder(s, pres);
  return s;
}

module.exports = { compose, DELTA: { drawEncoder, drawCentral, drawDecoder } };

if (require.main === module) {
  const pptxgen = require("pptxgenjs");
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  compose(pres);
  pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_057_recreated.pptx" })
    .then(() => console.log("WROTE slide_057_recreated.pptx"))
    .catch((e) => { console.error(e); process.exit(1); });
}
