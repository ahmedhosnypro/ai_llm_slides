// slide_011.js — "Transformer / Attention is All You Need" (Deep Learning DSAI 308, lecture 001)
// Built from PIL-measured geometry of unique_slides/slide_011.jpg (960x540, 1px = 1pt = 1/72in).
// Chrome: PLAYLIST house chrome (videos/deep-learning/shared_patterns/house_chrome.js,
// founder directive 2026-10-11) — badge numeral 11.
//
// Frame-is-ground-truth decisions (all PIL-measured; see scratch/slide011/ + qa/slide011/worker_report.md):
// - The original carries a WHITE content rectangle over the gray panel (x 40..920, y 114..499)
//   that covers the panel's side borders at those rows — reproduced verbatim (fidelity law).
//   Consequence: house_chrome_check.py's exposed-panel assumption cannot pass even on the
//   ORIGINAL frame; chrome is instead verified by the module + the adapted self-check.
// - No #BFBFBF footer strip exists: the bottom band is the exposed panel itself.
// - Sub-block fills measured from large uniform interiors (JPEG-stable): EFF1FD / F3F1FC.
// - Cross-attention dashes measured pale mauve B790A5 (not the spec's FF9E9E guess; the
//   frame's dash cores are (183,144,165)); four dash chains T1..T4 per pixel evidence.
// - Math tokens x1..x3 / o1..o3 = matplotlib mathtext PNGs at 600dpi, exact size, baseline law.
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/";
const px = (v) => v / 72; // frame px -> inches

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- playlist house chrome (white canvas, gray panel, red border, badge "11") ----
drawHouseChrome(pres, slide, { numeral: 11 });

const FONT = "Arial";
const RED = "E00000";
const BLUE = "2222CC";
const INK = "1A1A1A";

// ---- white content rectangle over the panel (measured x 40..920, y 114..499) ----
slide.addShape(pres.shapes.RECTANGLE, {
  x: px(40), y: px(114), w: px(880), h: px(385),
  fill: { color: "FFFFFF" }, line: { type: "none" },
});

// ---- title / subtitle (ink centers (462.5,71) / (462.5,103)) ----
slide.addText("Transformer", {
  x: px(340), y: px(52), w: px(245), h: px(38),
  align: "center", valign: "middle",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});
slide.addText("Attention is All You Need", {
  x: px(330), y: px(93), w: px(265), h: px(20),
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 'Decoder' label (red bold italic, ink center (727.5,97.5)) ----
slide.addText("Decoder", {
  x: px(687), y: px(87), w: px(81), h: px(21),
  align: "center", valign: "middle",
  fontSize: 19, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- yellow decoder block (x 479..904, y 162..283) ----
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: px(479), y: px(162), w: px(426), h: px(122),
  fill: { color: "FFFF00" }, line: { type: "none" }, rectRadius: 0.1,
});
slide.addText("Multi Head Self Attention Blocks", {
  x: px(489), y: px(204), w: px(406), h: px(38),
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- orange encoder block (x 46..487, y 306..451) ----
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: px(46), y: px(306), w: px(442), h: px(146),
  fill: { color: "F5AB62" }, line: { type: "none" }, rectRadius: 0.1,
});
slide.addText("Multi Head Self Attention Blocks", {
  x: px(56), y: px(359), w: px(422), h: px(39),
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- encoder lavender sub-block (x 110..470, y 226..299) ----
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: px(110), y: px(226), w: px(361), h: px(74),
  fill: { color: "EFF1FD" }, line: { color: "C3CCD5", width: 1 }, rectRadius: 0.07,
});
// 'attention' box (white, x 246..329, y 252..274)
slide.addShape(pres.shapes.RECTANGLE, {
  x: px(246), y: px(252), w: px(84), h: px(23),
  fill: { color: "FFFFFF" }, line: { color: "BABEBF", width: 1 },
});
slide.addText("attention", {
  x: px(246), y: px(252), w: px(84), h: px(23),
  align: "center", valign: "middle",
  fontSize: 15, italic: true, color: "72747C", fontFace: "Times New Roman", margin: 0,
});

// ---- decoder lavender sub-block (x 494..856, y 289..339) ----
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: px(494), y: px(289), w: px(363), h: px(51),
  fill: { color: "F3F1FC" }, line: { color: "ABAEBD", width: 1 }, rectRadius: 0.07,
});

// ---- 'Encoder-Decoder Attention' labels (blue bold italic 16pt) ----
slide.addText("Encoder-Decoder Attention", {
  x: px(168), y: px(196), w: px(230), h: px(20),
  align: "center", valign: "middle",
  fontSize: 16, bold: true, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});
slide.addText("Encoder-Decoder Attention", {
  x: px(623), y: px(348), w: px(231), h: px(20),
  align: "center", valign: "middle",
  fontSize: 16, bold: true, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- fan of 3 solid dark lines from the attention-box bottom (285.5,277) to the orange top ----
function line(x1, y1, x2, y2, color, width, opts = {}) {
  slide.addShape(pres.shapes.LINE, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: Object.assign({ color: color, width: width }, opts),
  });
}
line(285.5, 277, 190, 306, "40444E", 1.25);
line(285.5, 277, 288, 306, "40444E", 1.25);
line(285.5, 277, 385, 306, "40444E", 1.25);

// ---- encoder input lines (gray) + x1..x3 mathtext labels ----
line(152.5, 452, 152.5, 477, "999999", 1.25);
line(286, 452, 286, 477, "999999", 1.25);
line(421, 452, 421, 477, "999999", 1.25);

// math PNGs: exact size (px/600 in), baseline law: y_img = baseline_pt/72 - baseline_frac*h_in
function eq(name, json, cxPt, baselinePt) {
  const s = require(json);
  const w = s.w_px / 600, h = s.h_px / 600;
  const p = s.path.startsWith("/") ? s.path : EQ + s.path;
  slide.addImage({
    path: p,
    x: cxPt / 72 - w / 2, y: baselinePt / 72 - s.baseline_frac * h, w: w, h: h,
  });
}
const EQ = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/eq011/";
eq("x1", EQ + "eq011_x1.json", 151, 489.5);
eq("x2", EQ + "eq011_x2.json", 286, 489.5);
eq("x3", EQ + "eq011_x3.json", 420.5, 489.5);

// ---- decoder output up-arrows + o1..o3 labels ----
function arrowUp(x, y1, y2) {
  slide.addShape(pres.shapes.LINE, {
    x: px(x), y: px(y2), w: 0, h: px(y1 - y2),
    flipV: true,
    line: { color: "444444", width: 1.5, endArrowType: "triangle" },
  });
}
arrowUp(558, 161, 143.5);
arrowUp(692, 161, 143.5);
arrowUp(826, 161, 143.5);
eq("o1", EQ + "eq011_o1.json", 554.5, 131.5);
eq("o2", EQ + "eq011_o2.json", 689, 131.5);
eq("o3", EQ + "eq011_o3.json", 823.5, 131.5);

// ---- small black side-exit arrow at the yellow block's right edge (~y 262) ----
line(903, 262.5, 913, 262.5, "333333", 1.5, { endArrowType: "triangle" });

// ---- dashed cross-attention curves (4 chains, pale mauve; over both sub-blocks) ----
slide.addImage({ path: A + "dashes011.png", x: px(326), y: px(220), w: 4.58333, h: 1.55556 });

// ---- red cross-attention arc (dot -> curve -> head+dot; over the orange block) ----
// F3 FIX (founder defect batch 2026-10-13): arc asset regenerated by
// scratch/slide011/gen_arc011_f3fix.py — same canvas/path to the crest, then a
// terminal hook lands the arrowhead tip at (512.2, 290.8) ON the
// 'Encoder-Decoder Attention' panel's top edge (y=289), closing the gap the
// founder green-looped (same arrow class as slide 010's certified contact).
// Pre-fix asset banked: qa/slide011/arrowfix/arc011_red_prefix.png.
slide.addImage({ path: A + "arc011_red.png", x: px(448), y: px(248), w: 1.08333, h: 1.30556 });

// ---- self-loop arrows on the decoder sub-block ----
slide.addImage({ path: A + "loop011_1.png", x: px(661.2), y: px(278.3), w: 0.47222, h: 166 / 600 });
slide.addImage({ path: A + "loop011_2.png", x: px(795.0), y: px(278.3), w: 0.47222, h: 166 / 600 });

// ---- note box (beige, gray border; x 458..890, y 409..524; over the orange corner) ----
slide.addShape(pres.shapes.RECTANGLE, {
  x: px(458), y: px(409), w: px(433), h: px(116),
  fill: { color: "EAE6DD" }, line: { color: "B9BCBF", width: 1 },
});
slide.addText("Attention Mechanism supports:", {
  x: px(464), y: px(419), w: px(420), h: px(22),
  align: "left", valign: "middle",
  fontSize: 17, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
const bulletRuns = (pre, link, post) => ([
  { text: pre, options: { color: INK } },
  { text: link, options: { color: "0000FF", underline: { style: "sng" } } },
  { text: post, options: { color: INK } },
]);
slide.addText(bulletRuns("\u2022 ", "Parallelization", " of Encoder ,"), {
  x: px(463), y: px(444), w: px(420), h: px(19),
  align: "left", valign: "middle", fontSize: 17, fontFace: FONT, margin: 0,
});
slide.addText(bulletRuns("\u2022 ", "Parallelization", " of Decoder ( Training Mode Only)"), {
  x: px(463), y: px(470), w: px(420), h: px(21),
  align: "left", valign: "middle", fontSize: 17, fontFace: FONT, margin: 0,
});
slide.addText(bulletRuns("\u2022 Very Long  ", "Sequence length", ""), {
  x: px(463), y: px(496), w: px(420), h: px(20),
  align: "left", valign: "middle", fontSize: 17, fontFace: FONT, margin: 0,
});

// ---- 'Encoder' label on the exposed panel below the white box (center (263,516)) ----
slide.addText("Encoder", {
  x: px(224), y: px(506), w: px(78), h: px(20),
  align: "center", valign: "middle",
  fontSize: 19, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_011_recreated.pptx" })
  .then(() => console.log("wrote slide_011_recreated.pptx"));
