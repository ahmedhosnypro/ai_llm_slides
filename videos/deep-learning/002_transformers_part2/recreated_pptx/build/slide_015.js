// slide_015.js — "Multi Head Self Attention of Word X2" (recap, badge numeral 15)
// Deep Learning DSAI 308, video 002_transformers_part2, slide 15.
//
// CROSS-VIDEO CHILD (founder directive 2026-10-11): 15 <- deep-learning/001_transformers_part1:43
// (certified in the parent's own DB: gen_status=passed, visual_check=PASS). The parent's
// certified component is REQUIRED below by absolute path and its renderBase supplies the
// playlist house chrome (drawn ONCE in the component) with THIS slide's numeral.
// renderBase(..., {numeral: 15, skip: [all 18 content blocks]}): the PIL diff of this
// frame against the imported composition's output (scratch/slide015/diff_base.py,
// 32.7% hot px) shows the recap is NOT a pixel-identical re-draw — it is the same
// multi-head architecture family re-drawn at different geometry (stack shifted right+up,
// no concat/LT row, no top title, title at BOTTOM, per-head W chip columns, orange/green
// input ellipses). Per dependencies.md ("blocks whose measured geometry deviates are
// REDRAWN at their measured geometry, copy-then-modify" — 001 slide_045 precedent) every
// content block below is drawn fresh from THIS frame's PIL measurements; nothing is
// copy-pasted from the parent's coordinate space.
//
// FRAME->SLIDE MAPPING (scratch/slide015/measure_frame.py): fitted from THIS frame's
// four chrome landmarks (panel left border 58, right 901, top 43, bottom stroke 516 <->
// slide chrome 42, 919, 45, 540):
//   frame_x = 17.628 + 0.961232 * slide_x ;  frame_y = 0.955556 * slide_y
// Badge cross-check: yellow-bbox center (874.5,70.5) -> slide (891.5,73.8) vs house
// (893,71) — the same accepted JPEG-bbox delta as the certified slide_002/018 builds.
// All geometry below is in TRUE slide coords (960x540, 1px = 1pt, in = pt/72).
//
// MEASUREMENT PROVENANCE (all banked under scratch/slide015/):
//   measure_frame.py / measure_cards*.py / measure_mega.py / measure_elements.py
//   (PIL scans on the frame resampled into slide coords) + gate vision reads
//   crops/A..E_read.txt (full-region decodes) + zooms Z1..Z5b_read.txt (labels,
//   superscripts, pill fills, title colors, swoosh path, "H" Heads verbatim).
// W_k^(0)/W_v^(0) superscripts: Z4/Z2 read ALL FOUR boxes with the SAME parenthesized
// digit, best-read (0) — reproduced verbatim as measured.
//
// LAWS honored: playlist chrome via the imported component (numeral = printed 15);
// verbatim text incl. the literal double-quoted "H" Heads (Z5b, 6x read); professional
// 2D math (stacked K·q/sqrt(d) fraction: mathtext PNGs at exact size + measured pink
// bar; rotated pill labels as pre-rotated 600dpi PNGs); margin:0 + fontFace everywhere;
// no '#' in hex; mouse cursor + letterbox bars omitted (ground rule (c)).
//
// FIX LANE fix-swoosh-015-20261014 (CASCADE_DELTA register, judge attempt 2): swoosh
// asset re-traced from the frame (fix_m1..m9, scratch/slide015/), h4/h5 outContainers
// + W-chip triads + "H" Heads seat re-measured and corrected below.

const path = require("path");
const parent = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_043.js");

const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

const slide = pres.addSlide();

// ---- imported base: house chrome only (numeral 15); every parent content block skipped
parent.renderBase(pres, slide, {
  numeral: 15,
  skip: ["title", "vecbox", "pipearrows", "ltbox", "concatbar", "headarrows", "cards",
    "headannots", "ff_left", "ff_mid", "ff_right", "queryrow", "bottomcurve",
    "headpanels", "wochips", "swoosh", "hlabel", "legend"],
});

const A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets";
const SANS = "Arial";
const px = (v) => v / 72;

const C = {
  red: "C00000", darkred: "8B1A10", brick: "A0400E",
  ink: "1A1A1A", gray: "8A8A8A",
  blue: "2F55C8", navy: "2226C8", dkgreen: "2E7D4A", green: "2E8B57",
  brightgreen: "00AA00", magenta: "CC44CC",
  cardH1: "EF8C96", cardH2: "C5C1F4", cardH3: "F8FF9A", cardH4: "D4FFE5", cardH5: "F7E2CD",
  pillBlue: "4A5AA0", pillGray: "9A9A9A",
  orangeBack: "E8843C", orangeFront: "EABC78", stackCell: "F0B460",
  greenEll: "3FAE5C", lime: "7DF2A2",
  dotBlue: "2B4BD0", dotHalo: "9DB4F0", arrowBlue: "6C86D8",
  dotProd: "D8C0B4", scalePill: "F6C6CC", softPill: "FAD2FA",
  wkFill: "E6B66C", wvFill: "C9EFE6",
  tagFill: "141405", tagText: "E8E95D",
  beige: "E8D8B0",
};

function text(str, o) {
  slide.addText(str, Object.assign({ fontFace: SANS, margin: 0 }, o));
}
function rrect(x, y, w, h, fill, line, radius) {
  slide.addShape(pres.ShapeType.roundRect, {
    x: px(x), y: px(y), w: px(w), h: px(h), rectRadius: radius === undefined ? 0.06 : radius,
    fill: typeof fill === "string" ? { color: fill } : fill,
    line: line || { type: "none" },
  });
}
function rect(x, y, w, h, fill, line) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: typeof fill === "string" ? { color: fill } : fill,
    line: line || { type: "none" },
  });
}
function oval(x, y, w, h, fill, line) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: typeof fill === "string" ? { color: fill } : fill,
    line: line || { type: "none" },
  });
}
function line(x, y, w, h, lo) {
  const o = { flipH: false, flipV: false };
  if (w < 0) { x += w; w = -w; o.flipH = true; }
  if (h < 0) { y += h; h = -h; o.flipV = true; }
  slide.addShape(pres.ShapeType.line, {
    x: px(x), y: px(y), w: px(w), h: px(h), flipH: o.flipH, flipV: o.flipV, line: lo,
  });
}
function varrow(x, yTop, yBot, color, lw) {
  // vertical arrow, head at yTop (renderer-proof: rect + triangle, no 0-width line)
  rect(x - lw / 2, yTop + 4, lw, yBot - yTop - 4, color);
  slide.addShape(pres.ShapeType.triangle, {
    x: px(x - 2.6), y: px(yTop - 1), w: px(5.2), h: px(5.5), fill: { color },
  });
}
function img(file, x, y, w, h) {
  slide.addImage({ path: path.join(A, file), x: px(x), y: px(y), w: px(w), h: px(h) });
}
// W + colored subscript + red "(n)" superscript (Z2/Z4-read pattern)
function wRuns(sub, n, subColor, size) {
  return [
    { text: "W", options: { bold: true, fontSize: size, color: C.ink } },
    { text: sub, options: { bold: true, fontSize: size * 0.8, color: subColor, subscript: true } },
    { text: `(${n})`, options: { bold: true, fontSize: size * 0.75, color: C.red, superscript: true } },
  ];
}
function xRuns(i, color, size) {
  return [
    { text: "X", options: { bold: true, fontSize: size, color } },
    { text: String(i), options: { bold: true, fontSize: size * 0.75, color, subscript: true } },
  ];
}

// ================= cards (back to front) =======================================
// tops/lefts/rights measured (measure_mega v/h scans + crops A/E); bottoms: h1 439
// (vbot scans), backs occluded -> measured visible strip ends.
const CARDS = [
  { x: 267, y: 104, w: 547, h: 264, fill: C.cardH5 },
  { x: 223, y: 122, w: 551, h: 263, fill: C.cardH4 },
  { x: 181, y: 143, w: 546, h: 257, fill: C.cardH3 },
  { x: 140, y: 163, w: 545, h: 257, fill: C.cardH2 },
];
for (const c of CARDS) rrect(c.x, c.y, c.w, c.h, c.fill, { type: "none" }, 0.15);

// (translucent gray plane image drawn LATE — after pills/chips/chain — because the
// original dims the h1 Similarity pill and the card tops as well; closed-loop check)

// front card last
rrect(91, 186, 548, 253, C.cardH1, { type: "none" }, 0.15);

// ================= front-card left flow ========================================
// solid saturated ellipse offset down-right, then light dashed ellipse on top (Z4/census)
oval(94, 246, 70, 110, C.orangeBack);
oval(90, 226, 66, 123, C.orangeFront, { color: "C8843C", width: 1, dashType: "dash" });
// Dot Product box (two-line gray label at top)
rrect(229, 210, 59, 143, C.dotProd, { color: "7A6A54", width: 0.75 }, 0.03);
text([
  { text: "Dot", options: { breakLine: true } },
  { text: "Product", options: {} },
], { x: px(229), y: px(212), w: px(59), h: px(22), align: "center", valign: "top",
  bold: true, fontSize: 6, color: C.gray, lineSpacing: 7 });

// blue similarity arrows (drawn UNDER the translucent green ellipse, as measured)
line(228, 248, 44, 0, { color: C.arrowBlue, width: 0.9, endArrowType: "triangle" });
line(234, 275, 28, 0, { color: C.arrowBlue, width: 0.9, endArrowType: "triangle" });
line(228, 302, 21, 0, { color: C.arrowBlue, width: 0.9, endArrowType: "triangle" });
line(219, 330, 18, 0, { color: C.arrowBlue, width: 0.9, endArrowType: "triangle" });
// green ellipse (translucent) with striped key boxes + K labels
oval(183, 230, 51, 114, { color: "4FE07C", transparency: 25 }, { color: C.dkgreen, width: 0.75 });
const keyRows = [264, 292, 320, 344];
keyRows.forEach((yt, i) => {
  rect(193, yt, 18, 10.5, C.lime, { color: C.green, width: 0.75 });
  rect(199, yt, 6, 10.5, "E2FFE8", { color: C.green, width: 0.5 });
  text([
    { text: "K", options: { bold: true, fontSize: 5.5, color: C.dkgreen } },
    { text: String(i + 1), options: { bold: true, fontSize: 4.2, color: C.dkgreen, subscript: true } },
  ], { x: px(214), y: px(yt), w: px(16), h: px(10.5), align: "left", valign: "middle" });
});

// 4 token strips (5 pale-orange cells, red X_i on cell 2), arrows, tan W_k^(0) boxes
const ROWS = [248, 277, 305, 334];
ROWS.forEach((cy, i) => {
  for (let j = 0; j < 5; j++) {
    rect(94 + j * 9.2, cy - 5.5, 9.2, 11, C.stackCell, { color: "D89058", width: 0.5 });
  }
  text(xRuns(i + 1, C.red, 5), {
    x: px(101), y: px(cy - 5.5), w: px(18), h: px(11), align: "center", valign: "middle",
  });
  line(147, cy, 14, 0, { color: "C05010", width: 1, endArrowType: "triangle" });
  rect(162, cy - 6.5, 22, 13, C.wkFill, { color: C.dkgreen, width: 1 });
  text(wRuns("k", 0, C.dkgreen, 5.5), {
    x: px(162), y: px(cy - 6.5), w: px(22), h: px(13), align: "center", valign: "middle",
  });
});

// blue similarity dots (halo + core), descending down-left
const DOTS = [[280.5, 247], [269.5, 272], [254.5, 304], [244, 333]];
for (const [dx, dy] of DOTS) {
  oval(dx - 6, dy - 6, 12, 12, C.dotHalo);
  oval(dx - 3.5, dy - 3.5, 7, 7, C.dotBlue);
}
// thin converge lines from dots to the q entry at the Dot Product box bottom
DOTS.forEach(([dx, dy]) => line(dx, dy, 260 - dx, 351 - dy, { color: "B9C4E8", width: 0.5 }));
// blue arrows: green ellipse -> dots (visible parts)
// red arrows: dots -> Scaling pill
DOTS.forEach(([dx, dy]) => line(Math.max(dx + 6, 286), dy, 313 - Math.max(dx + 6, 286), 0,
  { color: C.red, width: 1, endArrowType: "triangle" }));

// "K·q" label right of the box top (red, Z1/crop-B)
text([
  { text: "K", options: {} },
  { text: "\u00B7", options: {} },
  { text: "q", options: {} },
], { x: px(292), y: px(211), w: px(28), h: px(15), align: "left", valign: "middle",
  fontSize: 10, color: C.darkred });

// stacked fraction K·q / sqrt(d): mathtext PNGs at exact size + measured pink bar
img("eq015_kq.png", 345.3, 212.5, 15.36, 8.4);
rect(345, 220.5, 18, 4, "D86472");
img("eq015_sqrtd.png", 346.5, 224.5, 13.3, 11.04);

// Scaling / Soft max pills with rotated 600dpi labels
rrect(314, 213, 20, 140, C.scalePill, { color: "E8A8C8", width: 0.75 }, 0.09);
img("eq015_scaling_rot.png", 316.06, 240.68, 14.88, 83.64);
rrect(368, 212, 19, 141, C.softPill, { color: "C8B8E8", width: 0.75 }, 0.09);
img("eq015_softmax_rot.png", 372.68, 254.7, 8.64, 54.6);

// red arrows Scaling -> Soft max (4 rows) and Soft max -> Sigma/nodes (2, measured)
for (const cy of ROWS) line(336, cy, 29, 0, { color: C.red, width: 1, endArrowType: "triangle" });
line(388, 220, 18, 0, { color: C.red, width: 0.9, endArrowType: "triangle" });
line(388, 248, 19, 0, { color: C.red, width: 0.9, endArrowType: "triangle" });

// Sigma box
rect(408, 211, 91, 17, "DCF3F3", { color: C.blue, width: 1.25 });
text("\u03A3", { x: px(408), y: px(211), w: px(91), h: px(17), align: "center", valign: "middle",
  bold: true, fontSize: 13, color: C.blue });

// four red drop lines into Sigma (measured span y231..272, heads at top)
for (const lx of [418.7, 440.5, 462.1, 483.9]) {
  varrow(lx, 231, 272, C.red, 0.9);
}

// multiply nodes (white fill, red ring, red x) + V labels + beige strips
const NODES = [[417.6, 248], [438.4, 275.2], [458.3, 302.9], [479.7, 333.8]];
NODES.forEach(([nx, ny], i) => {
  oval(nx - 4.5, ny - 4.5, 9, 9, "FFFFFF", { color: "CC2222", width: 1.25 });
  text("\u00D7", { x: px(nx - 4.5), y: px(ny - 4.5), w: px(9), h: px(9), align: "center",
    valign: "middle", bold: true, fontSize: 7, color: "CC2222" });
  text([
    { text: "V", options: { bold: true, italic: true, fontSize: 6, color: C.red } },
    { text: String(i + 1), options: { bold: true, fontSize: 4.5, color: C.red, subscript: true } },
  ], { x: px(497), y: px(ny - 11), w: px(13), h: px(11), align: "left", valign: "middle" });
  for (let j = 0; j < 4; j++) {
    rect(513 + j * 4.5, ny - 7, 4.5, 8.5, j % 2 ? "FFFFFF" : "F0E0B0",
      { color: "C9A06A", width: 0.5 });
  }
});

// W_v^(0) boxes (pale mint fill, blue border; Z2: all four read (0))
[241, 268, 295, 325].forEach((yt) => {
  rect(538, yt, 20, 15, C.wvFill, { color: C.blue, width: 1 });
  text(wRuns("v", 0, C.blue, 5.5), {
    x: px(538), y: px(yt), w: px(20), h: px(15), align: "center", valign: "middle",
  });
  line(559, yt + 7, 12, 1, { color: C.red, width: 0.9, endArrowType: "triangle" });
});

// ================= output containers (h1..h5) ==================================
function outContainer(x, y, w, h, strips, cellW, xCell, borderColor) {
  rrect(x, y, w, h, "DFEAD2", { color: borderColor || "2E8B57", width: 0.75, dashType: "dash" }, 0.05);
  const palette = strips === 5
    ? ["F9FF96", "FFFFFF", "F9FF96", "FFFFFF", "F6DAF3"]
    : ["CDD8B0", "E0E0D8", "CDD8B0", "E0E0D8"];
  strips.forEach((sy, k) => {
    const n = strips === 5 ? 5 : 4;
    for (let j = 0; j < n; j++) {
      const cw = (w - 10) / n;
      rect(x + 5 + j * cw, sy, cw, 12, palette[j], { color: "D8B8B8", width: 0.5 });
      if (j === (strips === 5 ? 3 : 1)) xCell.push([x + 5 + j * cw, sy, cw, k + 1]);
    }
  });
  varrow(x + w / 2, y + h - 8, y + h - 1, C.brightgreen, 1.25);
}
const xCells = [];
outContainer(575, 233, 58, 122, [242, 268, 294, 322], null, xCells, "A0A385");
outContainer(639, 213, 35, 131, [219, 247, 275, 302], null, xCells);
outContainer(691, 208, 33, 119, [213, 240, 268, 296], null, xCells);
// h4/h5 re-measured 2026-10-14 (fix_m7..m9 column/row dash runs): h4 right edge solid
// frame x750-751 -> slide ~762, top dashes y163-165 -> ~172, bottom dashes y273-275 ->
// ~287, left ~729.5; h5 left dashed frame x759-760 -> ~771.8, right solid x790-791 ->
// ~803.5, top y146-147 -> ~152.8, bottom y254-255 -> ~266.9. Cell rows pitch 27.
outContainer(729.5, 172, 32.5, 115, [177, 204, 231, 258], null, xCells);
outContainer(771.8, 153, 32, 114, [160, 187, 214, 241], null, xCells);
for (const [cx, cy, cw, idx] of xCells) {
  text(xRuns(idx, C.red, 5), { x: px(cx), y: px(cy), w: px(cw), h: px(12),
    align: "center", valign: "middle" });
}

// ================= per-head tag row: pills + h ovals ===========================
function pill(x, y, w, h, label, txtColor) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: "FFFFFF" },
    line: { color: C.pillGray, width: 0.5 },
    shadow: { type: "outer", color: "999999", blur: 3, offset: 1, angle: 90 },
  });
  text(label, { x: px(x), y: px(y), w: px(w), h: px(h), align: "center", valign: "middle",
    bold: true, fontSize: 5.5, color: txtColor });
}
const SIMS = [[236, 186, 46, 18], [282, 165, 44, 16], [330, 148, 42, 14], [373, 128, 41, 14], [417, 109, 41, 14]];
SIMS.forEach(([x, y, w, h]) => pill(x, y, w, h, "Similarity", C.pillGray));
pill(349, 186, 53, 18, "Probabilities", C.pillBlue);
pill(396, 167, 53, 18, "Probabilities", C.pillBlue);
const WSS = [[440, 186, 76, 18], [505, 168, 67, 16], [547, 148, 69, 15], [592, 128, 69, 15], [638, 108, 62, 15]];
WSS.forEach(([x, y, w, h]) => pill(x, y, w, h, "Weighted SUM", C.pillBlue));
const OVALS = [[596, 191, 31, 15, 1], [650, 169, 30, 15, 2], [690, 146, 31, 15, 3],
  [734, 128, 31, 14, 4], [778, 109, 30, 15, 5]];
for (const [x, y, w, h, n] of OVALS) {
  oval(x, y, w, h, C.tagFill);
  text(`h=${n}`, { x: px(x), y: px(y), w: px(w), h: px(h), align: "center", valign: "middle",
    bold: true, italic: true, fontSize: 6.5, color: C.tagText });
}

// ================= W chip columns W_q/k/v^(1..5) (white @38% over the panels) ===
const COLS = [
  { x: 608, tops: [377, 402, 422], n: 1 },
  { x: 656, tops: [355, 376, 396], n: 2 },
  { x: 699, tops: [333, 356, 378], n: 3 },
  { x: 742, tops: [314, 334, 355], n: 4 },
  { x: 784, tops: [296, 317, 337], n: 5 },
];
const chipBorder = { q: "CC2222", k: "2E8B57", v: "2F55C8" };
for (const c of COLS) {
  ["q", "k", "v"].forEach((ltr, i) => {
    slide.addShape(pres.ShapeType.rect, {
      x: px(c.x), y: px(c.tops[i]), w: px(24), h: px(15),
      fill: { color: "FFFFFF", transparency: 38 },
      line: { color: chipBorder[ltr], width: 1.25 },
    });
    text(wRuns(ltr, c.n, chipBorder[ltr], 5.5), {
      x: px(c.x), y: px(c.tops[i]), w: px(24), h: px(15), align: "center", valign: "middle",
    });
  });
}

// ================= climbing output chain (5 boxes + red up-arrows) =============
const CHAIN = [
  { x: 419, y: 153, w: 80, h: 16, fill: "BC4E05", line: { color: C.red, width: 1 } },
  { x: 464, y: 135, w: 72, h: 15, fill: "6B7052", line: { color: "B0B0B0", width: 0.75, dashType: "dash" } },
  { x: 510, y: 115, w: 70, h: 13, fill: "FAFF0C", line: { color: "B8B860", width: 0.75, dashType: "dash" } },
  { x: 548, y: 92, w: 76, h: 18, fill: "A0FF78", line: { color: C.green, width: 0.75, dashType: "dash" } },
  { x: 594, y: 75, w: 73, h: 16, fill: "F6DEBE", line: { color: C.green, width: 0.75, dashType: "dash" } },
];
for (const b of CHAIN) rrect(b.x, b.y, b.w, b.h, b.fill, b.line, 0.03);
[[501, 160, 150], [543, 140, 130], [586, 120, 110], [630, 100, 90]].forEach(([x, y1, y2]) => {
  varrow(x, y2, y1, C.red, 1);
});
// thick green arrow: Probabilities zone -> rust box
line(427, 175, 21, 11, { color: C.brightgreen, width: 2.5, flipH: true, beginArrowType: "triangle" });

// ================= translucent gray plane (over stack's upper-left) ============
img("plane015.png", 110, 65, 335, 163);

// ================= swoosh + "H" Heads label ====================================
// swoosh015.png regenerated 2026-10-14 from the fix_m1/m4/m7 frame trace (tapered
// 7.0->5.6 crimson ribbon, J-hook head tip (810.3,251.2) pointing down, U-curl tail
// w/ small UP arrowhead tip (588.7,351.6)); same 295x165 canvas at (550,235) — the
// img() line is unchanged and sibling 002:11 re-uses the fixed pixels as-is.
img("swoosh015.png", 550, 235, 295, 165);
// label re-seated so the ink center matches the measured (820.7,274.7): box center
// (785+36, 260+15) = (821, 275); sits just clear of the thin shaft under the hook arch.
text('"H" Heads', { x: px(785), y: px(260), w: px(72), h: px(30), align: "center",
  valign: "middle", bold: true, italic: true, fontSize: 10, color: C.navy, rotate: 338 });

// ================= query row ===================================================
rrect(173, 401, 219, 32, "EEFDDC", { color: "999999", width: 1.5, dashType: "dash" }, 0.05);
const GROUPS = [
  { x: 180, y: 408, w: 37, h: 19, i: 1, fill: "F7F3D8", hot: false },
  { x: 234, y: 406, w: 48, h: 22, i: 2, fill: "D296C8", hot: true },
  { x: 288, y: 408, w: 45, h: 19, i: 3, fill: "F7F3D8", hot: false },
  { x: 337, y: 408, w: 46, h: 19, i: 4, fill: "F7F3D8", hot: false },
];
for (const g of GROUPS) {
  const n = 4, cw = g.w / n;
  for (let j = 0; j < n; j++) {
    rect(g.x + j * cw, g.y, cw, g.h, g.fill,
      g.hot ? { color: C.magenta, width: 1.25 } : { color: "C9A06A", width: 0.5 });
  }
  text(xRuns(g.i, g.hot ? "8B0000" : C.red, 5.5), {
    x: px(g.x), y: px(g.y), w: px(g.w), h: px(g.h), align: "center", valign: "middle",
  });
}
// thick red pointer into X2 from lower-left
line(237, 426, 5, 16, { color: C.red, width: 4, beginArrowType: "triangle" });
// q chain: beige striped q-vector box + red W_q^(0) box + short up-arrows
for (let j = 0; j < 4; j++) {
  rect(260 + j * 6, 363, 6, 10, j % 2 ? "FFFFFF" : C.beige, { color: "B8A888", width: 0.5 });
}
text([
  { text: "q", options: { bold: true, fontSize: 5.5, color: C.red } },
  { text: "1", options: { bold: true, fontSize: 4.2, color: C.red, subscript: true } },
], { x: px(246), y: px(362), w: px(12), h: px(11), align: "left", valign: "middle" });
rect(244, 375, 21, 25, "FFFFFF", { color: "CC2222", width: 1.25 });
text(wRuns("q", 0, "CC2222", 5.5), { x: px(244), y: px(375), w: px(21), h: px(25),
  align: "center", valign: "middle" });
varrow(260, 354, 362, C.red, 0.9);
varrow(257, 397, 404, C.red, 0.9);
// faint dashed red connector: orange ellipse bottom -> query container
line(130, 348, 13, 57, { color: C.red, width: 0.75, dashType: "dash" });

// ================= title (bottom-center, measured 20pt bold) ===================
text([
  { text: "Multi Head ", options: { color: C.red } },
  { text: "Self Attention of Word ", options: { color: C.ink } },
  { text: "X", options: { color: C.red } },
  { text: "2", options: { color: C.red, subscript: true, fontSize: 10 } },
], { x: px(297), y: px(477), w: px(382), h: px(26), align: "center", valign: "middle",
  bold: true, fontSize: 19.5 });

pres.writeFile({ fileName: __dirname + "/../slide_015_recreated.pptx" })
  .then(() => console.log("WROTE slide_015_recreated.pptx"));
