// slide_011.js — "Multi Head Self Attention of Word X2" (recap, badge numeral 11)
// Deep Learning DSAI 308, video 002_transformers_part2, slide 11.
//
// CROSS-VIDEO CHILD (founder directive 2026-10-11): 11 <- deep-learning/001_transformers_part1:43
// (certified in the parent's own DB). The parent's certified component is REQUIRED by
// absolute path; renderBase supplies the playlist house chrome (drawn ONCE) with THIS
// slide's numeral 11. Every parent content block is skipped: the PIL diff of this frame
// against the imported composition (scratch/slide011/diff_base.py, banked by the first
// worker: 30.9% hot px) and the chroma diff against certified sibling 015's frame show
// this recap is NOT a pixel re-draw — same family, own geometry (per dependencies.md
// "blocks whose measured geometry deviates are REDRAWN at their measured geometry",
// 001 slide_045 precedent; certified 002:15 is the same-parent precedent).
//
// FRAME->SLIDE MAPPING (scratch/slide011/measure_frame_out.json + probe.out, banked by
// the first worker; identical to certified slide_002/015): fitted from THIS frame's four
// chrome landmarks (panel left border 58, right 901, top 43, bottom stroke 516 <->
// slide chrome 42, 919, 45, 540):
//   frame_x = 17.628 + 0.961232 * slide_x ;  frame_y = 0.955556 * slide_y
// Badge cross-check: yellow-bbox (863..892, 56..86) center -> slide (892.1, 74.6) vs
// house (893,71) — same accepted JPEG-bbox delta as the certified builds.
// All geometry below is in TRUE slide coords (960x540, 1px = 1pt, in = pt/72).
//
// MEASUREMENT PROVENANCE (banked under scratch/slide011/):
//   m1_census_panels / m3_left / m5_regions / m6_top / m7_shared / m8_details /
//   m9_detail / m11_inherited / colmap.txt (PIL scans on the frame resampled into
//   slide coords) + gate vision reads an_A_leftinput / an_F_title / an_z9_topzone /
//   an_z13_topright / an_z1_leftW (crops + 4x-6x zooms). Shared structures verified
//   against certified sibling 015's build values (cards, pills, tags, Dot Product box,
//   pills/Sigma/nodes/V/W_v/outContainers, swoosh arc — chroma-diff clean regions).
// Deltas vs 015 re-measured from THIS frame: blue inner frame rect (spec-mandated,
// x57..880 y65..515), top-zone chain/beam (bright-yellow beam quad, cream top box,
// 4-cell dashed Y row, olive + orange chain boxes, mint strips), left zone (mint
// dashed container, pastel cell strips, mint W boxes w/ pale-red superscripts, red K
// labels), q zone (purple X2 strip at x224..278, red cell borders).
//
// LAWS honored: playlist chrome via the imported component (numeral = printed 11);
// verbatim text; professional 2D math (stacked K·q/√d fraction: certified mathtext
// PNGs at exact size + measured pink bar; rotated pill labels as pre-rotated 600dpi
// PNGs); margin:0 + fontFace everywhere; no '#' in pptx colors; explicit lineSpacing
// on multi-line boxes; mouse cursor + letterbox bars omitted (ground rule (c)).

const path = require("path");
const parent = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_043.js");

const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

const slide = pres.addSlide();

// ---- imported base: house chrome only (numeral 11); every parent content block skipped
parent.renderBase(pres, slide, {
  numeral: 11,
  skip: ["title", "vecbox", "pipearrows", "ltbox", "concatbar", "headarrows", "cards",
    "headannots", "ff_left", "ff_mid", "ff_right", "queryrow", "bottomcurve",
    "headpanels", "wochips", "swoosh", "hlabel", "legend"],
});

const A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets";
const SANS = "Arial";
const px = (v) => v / 72;

const C = {
  ink: "1A1A1A", gray: "8A8A8A",
  blue: "2F55C8", navy: "2226C8", dkgreen: "2E7D4A", green: "2E8B57",
  brightgreen: "00AA00", magenta: "CC44CC", red: "C00000", darkred: "8B1A10",
  brick: "A0400E",
  cardH1: "EF8C96", cardH2: "C5C1F4", cardH3: "F8FF9A", cardH4: "D4FFE5", cardH5: "F7E2CD",
  dotProd: "D8C0B4", scalePill: "F6C6CC", softPill: "FAD2FA",
  beam: "F2F13E", cream: "F6DEBE", chainOlive: "B8BE45", chainOrange: "F5CF50",
  mint: "D1FFE5", wvFill: "C9EFE6", wkFill: "DFF2D8",
  tagFill: "141405", tagText: "E8E95D",
  beige: "E8D8B0", stackCell: "F0B460",
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
function img(file, x, y, w, h) {
  slide.addImage({ path: path.join(A, file), x: px(x), y: px(y), w: px(w), h: px(h) });
}
function wRuns(sub, n, subColor, size, supColor) {
  return [
    { text: "W", options: { bold: true, italic: true, fontSize: size, color: C.ink } },
    { text: sub, options: { bold: true, fontSize: size * 0.8, color: subColor, subscript: true } },
    { text: `(${n})`, options: { bold: true, fontSize: size * 0.75, color: supColor || "C87A7A", superscript: true } },
  ];
}
function xRuns(i, color, size) {
  return [
    { text: "X", options: { bold: true, fontSize: size, color } },
    { text: String(i), options: { bold: true, fontSize: size * 0.75, color, subscript: true } },
  ];
}

// ================= blue inner frame (spec-mandated; measured x57..880 y65..515) ===
rect(57, 65, 823, 450, { type: "none" }, { color: "2244CC", width: 1.25 });

// ================= beam (drawn LATE — after pills/containers — the original's
// translucent yellow ribbon overlays the card tops; closed-loop checked) ==========

// ================= cards (verified vs certified 015 — chroma-clean) ==============
const CARDS = [
  { x: 267, y: 104, w: 547, h: 264, fill: C.cardH5 },
  { x: 223, y: 122, w: 551, h: 263, fill: C.cardH4 },
  { x: 181, y: 143, w: 546, h: 257, fill: C.cardH3 },
  { x: 140, y: 163, w: 545, h: 257, fill: C.cardH2 },
];
for (const c of CARDS) rrect(c.x, c.y, c.w, c.h, c.fill, { type: "none" }, 0.15);
// front card last
rrect(91, 186, 548, 253, C.cardH1, { type: "none" }, 0.15);


// ================= front-card left flow ========================================
// mint dashed container (measured x88..152 y235..347) with pastel cell strips
rrect(88, 231, 64, 120, { color: "E0F0E0", transparency: 12 },
  { color: C.dkgreen, width: 1, dashType: "dash" }, 0.08);
const ROWS = [243, 271, 299, 330];
const cellFills = ["F9FF96", "F9FF96", "FFFFFF", "D6E4F8", "EAE4F0"];
ROWS.forEach((cy, i) => {
  for (let j = 0; j < 5; j++) {
    rect(96 + j * 9.2, cy - 5.5, 9.2, 11, cellFills[j], { color: "D89058", width: 0.5 });
  }
  // red X label inside the THIRD (white) cell (z7 read)
  text(xRuns(i + 1, C.red, 5), {
    x: px(96 + 2 * 9.2), y: px(cy - 5.5), w: px(9.2), h: px(11), align: "center", valign: "middle",
  });
  line(144, cy, 17, 0, { color: "C05010", width: 1, endArrowType: "triangle" });
  // mint-green W box (z1/z7: green fill, dark-green border, black italic W + pale-red superscript)
  rect(163, cy - 9.5, 24, 19, "D5EBC5", { color: C.dkgreen, width: 1.25 });
  text(wRuns("v", 0, C.ink, 5.5, "C87A7A"), {
    x: px(163), y: px(cy - 9.5), w: px(24), h: px(19), align: "center", valign: "middle",
  });
  // tiny K bar strip floats ABOVE the connector line + red K label to its right (z7)
  for (let j = 0; j < 4; j++) {
    rect(190 + j * 5.6, cy - 11, 5.6, 9, ["F9FF96", "FFFFFF", "FFFFFF", "D6E4F8"][j], { color: "B8B8B8", width: 0.5 });
  }
  text([
    { text: "K", options: { bold: true, fontSize: 5.5, color: C.darkred } },
    { text: String(i + 1), options: { bold: true, fontSize: 4.2, color: C.darkred, subscript: true } },
  ], { x: px(214), y: px(cy - 12), w: px(14), h: px(11), align: "left", valign: "middle" });
  line(226, cy, 4, 0, { color: C.brick, width: 1, endArrowType: "triangle" });
});

// ================= Dot Product box + pills + Sigma (015-verified) ===============
rrect(229, 210, 59, 143, C.dotProd, { color: "7A6A54", width: 0.75 }, 0.03);
text([
  { text: "Dot", options: { breakLine: true } },
  { text: "Product", options: {} },
], { x: px(229), y: px(212), w: px(59), h: px(22), align: "center", valign: "top",
  bold: true, fontSize: 6, color: "6B4423", lineSpacing: 7 });

// blue similarity arrows + blue dots + converge lines (015-verified positions)
line(228, 248, 44, 0, { color: "6C86D8", width: 0.9, endArrowType: "triangle" });
line(234, 275, 28, 0, { color: "6C86D8", width: 0.9, endArrowType: "triangle" });
line(228, 302, 21, 0, { color: "6C86D8", width: 0.9, endArrowType: "triangle" });
line(219, 330, 18, 0, { color: "6C86D8", width: 0.9, endArrowType: "triangle" });
const DOTS = [[280.5, 247], [269.5, 272], [254.5, 304], [244, 333]];
for (const [dx, dy] of DOTS) {
  oval(dx - 6, dy - 6, 12, 12, "9DB4F0");
  oval(dx - 3.5, dy - 3.5, 7, 7, "2B4BD0");
}
DOTS.forEach(([dx, dy]) => line(dx, dy, 260 - dx, 351 - dy, { color: "B9C4E8", width: 0.5 }));
DOTS.forEach(([dx, dy]) => line(Math.max(dx + 6, 286), dy, 313 - Math.max(dx + 6, 286), 0,
  { color: C.red, width: 1, endArrowType: "triangle" }));

// "K·q" label right of the box top (measured ink x288..308 y211..227)
text([
  { text: "K", options: {} },
  { text: "\u00B7", options: {} },
  { text: "q", options: {} },
], { x: px(290), y: px(211), w: px(26), h: px(15), align: "left", valign: "middle",
  fontSize: 10, color: C.darkred });

// stacked fraction K·q / sqrt(d): certified mathtext PNGs at exact size + pink bar
img("eq015_kq.png", 345.3, 210.5, 15.36, 8.4);
rect(345, 219.5, 18, 4, "D86472");
img("eq015_sqrtd.png", 346.5, 223.5, 13.3, 11.04);

// Scaling / Soft max pills with rotated 600dpi labels (015-verified geometry)
rrect(314, 213, 20, 140, C.scalePill, { color: "E8A8C8", width: 0.75 }, 0.09);
img("eq015_scaling_rot.png", 316.06, 240.68, 14.88, 83.64);
rrect(368, 212, 19, 141, C.softPill, { color: "C8B8E8", width: 0.75 }, 0.09);
img("eq015_softmax_rot.png", 372.68, 254.7, 8.64, 54.6);

// red arrows Scaling -> Soft max and Soft max -> Sigma
for (const cy of ROWS) line(336, cy, 29, 0, { color: C.red, width: 1, endArrowType: "triangle" });
line(388, 220, 18, 0, { color: C.red, width: 0.9, endArrowType: "triangle" });
line(388, 248, 19, 0, { color: C.red, width: 0.9, endArrowType: "triangle" });

// Sigma box
rect(408, 211, 91, 17, "DCF3F3", { color: C.blue, width: 1.25 });
text("\u03A3", { x: px(408), y: px(211), w: px(91), h: px(17), align: "center", valign: "middle",
  bold: true, fontSize: 13, color: C.blue });

// four red drop lines into Sigma
for (const lx of [418.7, 440.5, 462.1, 483.9]) {
  const yTop = 231, yBot = 272;
  rect(lx - 0.45, yTop + 4, 0.9, yBot - yTop - 4, C.red);
  slide.addShape(pres.ShapeType.triangle, {
    x: px(lx - 2.6), y: px(yTop - 1), w: px(5.2), h: px(5.5), fill: { color: C.red },
  });
}

// multiply nodes + V labels + beige strips + W_v boxes (015-verified)
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
[238, 266, 294, 325].forEach((yt) => {
  rect(536, yt, 24, 18, C.wvFill, { color: "1F3A8C", width: 1.25 });
  text(wRuns("v", 0, C.ink, 5.5, "CC2222"), {
    x: px(536), y: px(yt), w: px(24), h: px(18), align: "center", valign: "middle",
  });
  // dark-red LEFT-pointing arrowhead touching the box's right border (z2: flow right->left)
  line(572, yt + 9, 12, 0, { color: "8B2020", width: 0.9, beginArrowType: "triangle" });
});

// ================= output containers (h1..h5, 015-verified) =====================
function outContainer(x, y, w, h, strips, cellW, xCell, borderColor) {
  rrect(x, y, w, h, "DFEAD2", { color: borderColor || "2E8B57", width: 0.75, dashType: "dash" }, 0.05);
  const palette = ["F2DCD4", "E6E4F6", "D8DEC8", "F0E2EE"];
  strips.forEach((sy, k) => {
    for (let j = 0; j < 4; j++) {
      const cw = (w - 10) / 4;
      rect(x + 5 + j * cw, sy, cw, 12, palette[j], { color: "D8B8B8", width: 0.5 });
      if (j === 1) xCell.push([x + 5 + j * cw, sy, cw, k + 1]);
    }
  });
  const yTop = y + h - 8, yBot = y + h - 1;
  rect(x + w / 2 - 0.6, yTop + 4, 1.25, yBot - yTop - 4, C.brightgreen);
  slide.addShape(pres.ShapeType.triangle, {
    x: px(x + w / 2 - 3.2), y: px(yTop - 1), w: px(6.4), h: px(5.5), fill: { color: C.brightgreen }, flipV: true,
  });
}
const xCells = [];
outContainer(575, 233, 58, 122, [242, 268, 294, 322], null, xCells, "A0A385");
outContainer(639, 213, 35, 131, [219, 247, 275, 302], null, xCells);
outContainer(691, 208, 33, 119, [213, 240, 268, 296], null, xCells);
outContainer(735, 182, 39, 117, [187, 215, 243, 271], null, xCells);
outContainer(763, 144, 42, 122, [153, 181, 209, 236], null, xCells);
for (const [cx, cy, cw, idx] of xCells) {
  text(xRuns(idx, C.red, 5), { x: px(cx), y: px(cy), w: px(cw), h: px(12),
    align: "center", valign: "middle" });
}

// ================= per-head tag row: pills + h ovals (015-verified) =============
function pill(x, y, w, h, label, txtColor) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: "FFFFFF" },
    line: { color: "9A9A9A", width: 0.5 },
    shadow: { type: "outer", color: "999999", blur: 3, offset: 1, angle: 90 },
  });
  text(label, { x: px(x), y: px(y), w: px(w), h: px(h), align: "center", valign: "middle",
    bold: true, fontSize: 5.5, color: txtColor });
}
const SIMS = [[236, 186, 46, 18], [282, 165, 44, 16], [330, 148, 42, 14], [373, 128, 41, 14], [417, 109, 41, 14]];
SIMS.forEach(([x, y, w, h]) => pill(x, y, w, h, "Similarity", "9A9A9A"));
pill(349, 186, 53, 18, "Probabilities", "4A5AA0");
pill(396, 167, 53, 18, "Probabilities", "4A5AA0");
const WSS = [[440, 186, 76, 18], [505, 168, 67, 16], [547, 148, 69, 15], [592, 128, 69, 15], [638, 108, 62, 15]];
WSS.forEach(([x, y, w, h]) => pill(x, y, w, h, "Weighted SUM", "4A5AA0"));
// ================= top zone: chain cascade (z14/z9 reads + measured boxes) ======
// drawn AFTER the pills (the ribbon overlays them); h-ovals drawn later still.
// The beam ribbon is injected post-build as custGeom vectors (fix_beam.py) replacing
// the anchor image below — LO mis-renders solid semi-transparent PNGs (measured).
img("beam011.png", 392, 58, 310, 125);
// full-width cream + mint strips BEHIND the ribbon, OVER the cards (measured)
rect(356, 104, 414, 18, { color: C.cream, transparency: 25 });
rect(356, 122, 414, 20, { color: C.mint, transparency: 30 });
// dashed chain boxes along the beam (top->bottom), orange UP-arrows between (z14)
function chainBox(x, y, w, h, fill, glyphColor, label) {
  rrect(x, y, w, h, fill, { color: glyphColor, width: 1, dashType: "dash" }, 0.05);
  if (label) {
    text(label.runs, { x: px(x), y: px(y), w: px(w), h: px(h), align: "center", valign: "middle" });
  }
}
function upArrowOrange(x, yBot, yTop) {
  rect(x - 0.9, yBot, 1.8, yTop - yBot - 4, "E87830");
  slide.addShape(pres.ShapeType.triangle, {
    x: px(x - 3), y: px(yTop - 5), w: px(6), h: px(5.5), fill: { color: "E87830" },
  });
}
chainBox(590, 72, 75, 13, { color: "FFE98C", transparency: 30 }, "C8901C",
  { runs: [{ text: "Y", options: { bold: true, italic: true, fontSize: 6, color: "C8901C" } }] });
upArrowOrange(629, 85, 90);
chainBox(546, 91, 76, 17, { color: "D2FFE0", transparency: 30 }, "2E7D4A",
  { runs: [{ text: "Y", options: { bold: true, italic: true, fontSize: 6, color: "2E7D4A" } }] });
upArrowOrange(585, 108, 122);
chainBox(546, 109, 73, 21, { color: "FFE98C", transparency: 30 }, "C8901C",
  { runs: [{ text: "Y", options: { bold: true, italic: true, fontSize: 6, color: "C8901C" } }] });
// olive chain box (measured x458..544 y132..157)
chainBox(458, 132, 86, 26, C.chainOlive, "6B8E23", null);
upArrowOrange(520, 158, 180);
// dark-orange chain box over the h1 card top (measured x378..570 y184..205)
chainBox(378, 184, 192, 21, C.chainOrange, "6B8E23", null);

const OVALS = [[596, 191, 31, 15, 1], [650, 169, 30, 15, 2], [690, 146, 31, 15, 3],
  [734, 128, 31, 14, 4], [778, 109, 30, 15, 5]];
for (const [x, y, w, h, n] of OVALS) {
  oval(x, y, w, h, C.tagFill);
  text(`h=${n}`, { x: px(x), y: px(y), w: px(w), h: px(h), align: "center", valign: "middle",
    bold: true, italic: true, fontSize: 6.5, color: C.tagText });
}

// ================= W chip columns (015-verified) ================================
const COLS = [
  { x: 608, tops: [377, 402, 422], n: 1 },
  { x: 656, tops: [355, 376, 396], n: 2 },
  { x: 699, tops: [333, 356, 378], n: 3 },
  { x: 744, tops: [320, 344, 367], n: 4 },
  { x: 785, tops: [297, 321, 344], n: 5 },
];
const chipBorder = { q: "CC2222", k: "2E8B57", v: "2F55C8" };
const chipFill = { q: "FDE4E4", k: "E0F5E0", v: "E0E8F8" };
for (const c of COLS) {
  ["q", "k", "v"].forEach((ltr, i) => {
    slide.addShape(pres.ShapeType.rect, {
      x: px(c.x), y: px(c.tops[i]), w: px(24), h: px(15),
      fill: { color: chipFill[ltr], transparency: 20 },
      line: { color: chipBorder[ltr], width: 1.25 },
    });
    text(wRuns(ltr, c.n, chipBorder[ltr], 5.5, chipBorder[ltr]), {
      x: px(c.x), y: px(c.tops[i]), w: px(24), h: px(15), align: "center", valign: "middle",
    });
  });
}

// ================= swoosh + label (chroma-clean vs 015; asset reused) ===========
img("swoosh015.png", 550, 235, 295, 165);
text('"H" Heads', { x: px(778), y: px(262), w: px(72), h: px(30), align: "center",
  valign: "middle", bold: true, italic: true, fontSize: 10, color: C.navy, rotate: 338 });

// ================= query row ====================================================
// dashed dark-green pill container (z11: dashed dark-green rounded border)
rrect(173, 404, 219, 38, "EEFDDC", { color: "2E7D4A", width: 1.25, dashType: "dash" }, 0.05);
// five translucent attention ellipses fanning right over the row (spec item 30, [?]-placed)
oval(226, 352, 60, 96, { color: "7B9FE8", transparency: 52 });
oval(244, 360, 50, 80, { color: "9B7FE0", transparency: 52 });
oval(260, 368, 44, 68, { color: "B08FE8", transparency: 52 });
oval(274, 376, 38, 56, { color: "E8D87B", transparency: 52 });
oval(286, 384, 32, 44, { color: "8FD98F", transparency: 52 });
// four strips of ~7 cells, alternating pale-yellow/pale-lavender; red-bordered X cluster
// in the middle of each; strip 2 dashed dark-purple w/ lavender-blue cells (z11)
const QGROUPS = [
  { x: 184, w: 40, y: 408, h: 19, i: 1, fillA: "F7F3D8", fillB: "EAE4F0", border: "B03030", dash: false },
  { x: 228, w: 54, y: 406, h: 22, i: 2, fillA: "D8CCEC", fillB: "C8C4E8", border: "7B2FBF", dash: true },
  { x: 287, w: 44, y: 408, h: 19, i: 3, fillA: "F7F3D8", fillB: "EAE4F0", border: "B03030", dash: false },
  { x: 336, w: 48, y: 408, h: 19, i: 4, fillA: "F7F3D8", fillB: "EAE4F0", border: "B03030", dash: false },
];
for (const g of QGROUPS) {
  const n = 7, cw = g.w / n;
  if (g.dash) {
    rrect(g.x - 1, g.y - 1, g.w + 2, g.h + 2, { type: "none" },
      { color: "7B2FBF", width: 1, dashType: "dash" }, 0.04);
  }
  for (let j = 0; j < n; j++) {
    rect(g.x + j * cw, g.y, cw, g.h, j % 2 ? g.fillB : g.fillA, { color: "C9A06A", width: 0.4 });
  }
  // red-bordered cluster around the middle cell(s) + red X label
  const mx = g.x + 3 * cw - 1;
  rect(mx, g.y - 0.5, cw * 2 + 2, g.h + 1, { type: "none" }, { color: "B03030", width: 1 });
  text(xRuns(g.i, C.red, 5), {
    x: px(mx), y: px(g.y), w: px(cw * 2 + 2), h: px(g.h), align: "center", valign: "middle",
  });
}
// thick red pointer DOWN into X2 (z11: maroon arrowhead at bottom ~x250)
(function darr(x, yTop, yBot) {
  rect(x - 2, yTop, 4, yBot - yTop - 5, C.red);
  slide.addShape(pres.ShapeType.triangle, {
    x: px(x - 4), y: px(yBot - 6), w: px(8), h: px(6), fill: { color: C.red }, flipV: true,
  });
})(250, 426, 442);
// q chain: white box w/ FIVE yellow vector cells + red right edge (z6) above the query row
for (let j = 0; j < 5; j++) {
  rect(262 + j * 5.4, 363, 5.4, 10, j % 2 ? "F0E0B0" : "F9E48C", { color: "C9A06A", width: 0.5 });
}
rect(259, 361, 30, 14, { type: "none" }, { color: "B8A888", width: 0.5 });
line(291, 361, 0, 14, { color: C.red, width: 0.75 });
text([
  { text: "q", options: { bold: true, fontSize: 5.5, color: C.red } },
  { text: "1", options: { bold: true, fontSize: 4.2, color: C.red, subscript: true } },
], { x: px(246), y: px(362), w: px(12), h: px(11), align: "left", valign: "middle" });
// W box (white, thin dark border, NAVY W; red shaft passes behind w/ heads both ends)
rect(244, 375, 21, 25, "FFFFFF", { color: "444444", width: 1 });
text(wRuns("q", 0, "2F4488", 5.5, "CC2222"), { x: px(244), y: px(375), w: px(21), h: px(25),
  align: "center", valign: "middle" });
rect(258.6, 354, 0.9, 50, C.red);
slide.addShape(pres.ShapeType.triangle, {
  x: px(256), y: px(349), w: px(5.2), h: px(5.5), fill: { color: C.red },
});
slide.addShape(pres.ShapeType.triangle, {
  x: px(256), y: px(402), w: px(5.2), h: px(5.5), fill: { color: C.red }, flipV: true,
});
// green up-triangle below the left container + faint dashed green curve (crop A)
rect(129, 351, 1.25, 10, C.brightgreen);
slide.addShape(pres.ShapeType.triangle, {
  x: px(125.5), y: px(345), w: px(8), h: px(6.5), fill: { color: C.brightgreen },
});
line(133, 358, 10, 46, { color: "3FAE5C", width: 0.75, dashType: "dash" });

// ================= title (bottom-center, measured = 015-verified) ===============
text([
  { text: "Multi Head ", options: { color: C.red } },
  { text: "Self Attention of Word ", options: { color: C.ink } },
  { text: "X", options: { color: C.red } },
  { text: "2", options: { color: C.red, subscript: true, fontSize: 10 } },
], { x: px(297), y: px(477), w: px(382), h: px(26), align: "center", valign: "middle",
  bold: true, fontSize: 19.5 });

pres.writeFile({ fileName: __dirname + "/../slide_011_recreated.pptx" })
  .then(() => console.log("WROTE slide_011_recreated.pptx"));
