// slide_005.js — "1-D Convolutional Neural Network" (Deep Learning DSAI 308, Transformers Part I)
// Build worker, attempt 1. PLAYLIST HOUSE CHROME drawn ONLY via the shared module
// videos/deep-learning/shared_patterns/house_chrome.js (founder directive 2026-10-11).
//
// CONTENT GEOMETRY PROVENANCE — PIL pixel forensics on slide_005.jpg (960x540, 1px = 1pt),
// banked in ../../scratch/slide005/forensics*_out.txt (2026-10-11):
//   - Title ink x261-653 (center 457, NOT slide-centered), cap top y59, cap h 18px -> 24pt bold C00000.
//   - Five cell stacks, all y178..463, 18 cells of 15.83px pitch (outlines measured every
//     ~15.8px y178.5..462.5). Stack x-ranges: WV 163-244, FM1 308-390, FM2 456-537,
//     FM3 598-679, FM4 737-818; outline gray-blue ~A7AFB9 (avg (167,175,184)).
//   - Highlighted cells (modal luma/hue classification): WV FFFFCC cells 1-3; FM1 FFCC99
//     cells 3,14,15,16 (luma ~222 = peach, chroma JPEG-crushed); FM2 cyan cells 9,10,11,15
//     (modal (207,250,243)); FM3 FFCCFF cells 3,4,5,10; FM4 CCFFCC cells 4,14. Spec's 13-cell
//     reading was an estimate flagged [?]; the frame's true grid is 18 cells (SOURCES.md
//     directed build-time verification). Spec colors kept for fills.
//   - Gray "Non Linearity" bars x412/560/702/832, w18, y178-461, fill modal (216,216,216)
//     = D8D8D8 (NOT spec BFBFBF - measured), thin gray-blue edge; blue 0000CC bold rotated
//     text y273-363 centered.
//   - Funnel triangles = vertical left edge + two hypotenuses converging to an apex at the
//     output cell: tri1 edge x252 y180-225, apex (306,218) -> FM1 cell 3; tri3 edge x545
//     y305-351, apex (596,328) -> FM3 cell 10; tri4 edge x687 y212-256, apex (737,233) ->
//     FM4 cell 4. SPEC'S TRIANGLE 2 (gap1 lower, "cells 10-13") IS ABSENT in this frame:
//     raw deviation scan y330-460 x246-306 found 5 noise px total (forensics11) - omitted,
//     frame is ground truth (founder frame swap note in SOURCES.md).
//   - Block arrow x253-305 y303.5-325.5 (body ~11px, head to tip x305) CC0000.
//   - Sequence Length: shaft x152-153 y178-449, head x147.5-158.5 y447-459 (down), red label
//     rotated 270, ink y276-385 center (141.5, 330.5).
//   - Kernel pictogram: 3 rects x60-143, y98/114/129, h13, FF9999 + C00000 outline; label
//     "Convolutional"/"Kernel" 2 lines y155-163 / y171-178 (12pt bold, pitch 16).
//   - Green callout: box x460-653 y113-139, fill modal (224,248,224) ~E0F8E0 (NOT white -
//     measured), border 00A000 1pt; leader line (458,132)->(403,151).
//   - Bottom hatched arrow: body y477-490, head (782,470)-(815,483)-(782,496), fine "\"
//     diagonal hatch (stripe drift +2.5px per +3 rows; perp pitch ~4px, stroke ~2px), red
//     on white -> pre-generated 8x PNG assets/slide005_hatch_arrow.png, embedded exact size.
//   - Warning banner: yellow band (572,509)-(918,341), angle -20.9 deg => rotate 339,
//     center (745,425), band perp width ~33px -> rect 5.4x0.44in; text 16pt bold italic
//     0000CC, literal triple asterisks both sides.
//   - Caption: ink x181-808 y506-521, 16pt 0000CC; density step ~x530 + underline runs
//     (y519-521, longest 250px) => second sentence bold + underlined, first regular.
//   - Badge: chrome module (numeral 5). Mouse-cursor artifact NOT recreated (spec step 26).
//
// pptxgenjs laws: no "#" in hex; fontFace everywhere; margin:0; explicit lineSpacing on
// multi-line boxes (headers 14pt, kernel label 16pt).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const FONT = "Arial";
const IN = 1 / 72; // px -> inch
const px = (v) => v * IN;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- PLAYLIST HOUSE CHROME (white canvas, gray panel + red border, badge d36 @ (893,71)) ----
drawHouseChrome(pres, s, { numeral: 5 });

// ---- helpers ----
function line(x1, y1, x2, y2, color, width) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  const opts = { x: px(x), y: px(y), w: px(w), h: px(h), line: { color, width } };
  // pptxgenjs draws TL->BR by default; flip to match the actual direction
  if ((x2 - x1) * (y2 - y1) < 0) opts.flipV = true;
  s.addShape(pres.ShapeType.line, opts);
}

// ---- 1. five cell stacks (18 cells each) ----
const TOP = 178, CELLH = 285 / 18, NCELL = 18;
const OUTLINE = "A7AFB9";
const STACKS = [
  { name: "WV", x: 163, w: 82, fill: "FFFFCC", cells: [1, 2, 3] },
  { name: "FM1", x: 308, w: 83, fill: "FFCC99", cells: [3, 14, 15, 16] },
  { name: "FM2", x: 456, w: 82, fill: "99FFFF", cells: [9, 10, 11, 15] },
  { name: "FM3", x: 598, w: 82, fill: "FFCCFF", cells: [3, 4, 5, 10] },
  { name: "FM4", x: 737, w: 82, fill: "CCFFCC", cells: [4, 14] },
];
for (const st of STACKS) {
  for (let ci = 1; ci <= NCELL; ci++) {
    const on = st.cells.includes(ci);
    s.addShape(pres.ShapeType.rect, {
      x: px(st.x), y: px(TOP + (ci - 1) * CELLH), w: px(st.w), h: px(CELLH),
      fill: { color: on ? st.fill : "E9E9E7" },
      line: { color: OUTLINE, width: 0.75 },
    });
  }
}

// ---- 2. funnel triangles (3 lines each; drawn BEFORE the gray bars so tri3's mid is
//      covered by bar 2 exactly as in the frame) ----
const RED = "C00000";
function funnel(xEdge, yTop, yBot, xApex, yApex) {
  line(xEdge, yTop, xEdge, yBot, RED, 1);
  line(xEdge, yTop, xApex, yApex, RED, 1);
  line(xEdge, yBot, xApex, yApex, RED, 1);
}
funnel(252, 180, 225, 306, 218);   // tri1: WV cells 1-3 -> FM1 cell 3
funnel(545, 305, 351, 596, 328);   // tri3: FM2 cyan cells 9-11 -> FM3 cell 10
funnel(687, 212, 256, 737, 233);   // tri4: FM3 pink cells 3-5 -> FM4 cell 4
// (spec's tri2 absent from this frame - measured, see header comment)

// ---- 3. Sequence Length arrow (vertical, head DOWN) + rotated label ----
line(153, 178, 153, 449, RED, 1.5);
s.addShape(pres.ShapeType.triangle, {
  x: px(147.5), y: px(447), w: px(11), h: px(12),
  fill: { color: RED }, line: { type: "none" }, rotate: 180,
});
s.addText("Sequence Length", {
  x: px(141.5 - 68.4), y: px(330.5 - 9.4), w: px(136.8), h: px(18.7),
  align: "center", valign: "middle", rotate: 270,
  fontSize: 13, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- 4. block arrow (convolution step) ----
s.addShape(pres.ShapeType.rightArrow, {
  x: px(253), y: px(303.5), w: px(52), h: px(22),
  fill: { color: "CC0000" }, line: { type: "none" },
});

// ---- 5. gray Non Linearity bars + rotated blue text ----
const BAR = "D8D8D8";
const BLUE = "0000CC";
const barXs = [412, 560, 702, 832];
for (const bx of barXs) {
  s.addShape(pres.ShapeType.rect, {
    x: px(bx), y: px(178), w: px(18), h: px(283),
    fill: { color: BAR }, line: { color: OUTLINE, width: 0.75 },
  });
  s.addText("Non Linearity", {
    x: px(bx + 9 - 55.8), y: px(319.5 - 9.7), w: px(111.6), h: px(19.4),
    align: "center", valign: "middle", rotate: 270,
    fontSize: 14, bold: true, color: BLUE, fontFace: FONT, margin: 0,
  });
}

// ---- 6. kernel pictogram + label ----
for (const ky of [98, 114, 129]) {
  s.addShape(pres.ShapeType.rect, {
    x: px(60), y: px(ky), w: px(83), h: px(13),
    fill: { color: "FF9999" }, line: { color: RED, width: 1 },
  });
}
s.addText(
  [
    { text: "Convolutional", options: { breakLine: true } },
    { text: "Kernel", options: {} },
  ],
  {
    x: px(100.5 - 57.6), y: px(150.5), w: px(115.2), h: px(34),
    align: "center", valign: "top", fontSize: 12, bold: true, color: RED,
    fontFace: FONT, lineSpacing: 16, margin: 0,
  }
);

// ---- 7. green callout + leader ----
s.addShape(pres.ShapeType.rect, {
  x: px(460), y: px(113), w: px(193), h: px(26),
  fill: { color: "E0F8E0" }, line: { color: "00A000", width: 1 },
});
s.addText("Can be Computed In Parallel", {
  x: px(462), y: px(114), w: px(189), h: px(24),
  align: "center", valign: "middle",
  fontSize: 12.5, bold: true, italic: true, color: "00A000", fontFace: FONT, margin: 0,
});
line(458, 132, 403, 151, "00A000", 1);

// ---- 8. column headers (two lines, ordinal superscripts) ----
const headers = [
  { cx: 203.5, runs: [{ text: "Words", options: { breakLine: true } }, { text: "Vectors", options: {} }] },
  { cx: 349, runs: [{ text: "1", options: {} }, { text: "st", options: { superscript: true } }, { text: " Feature", options: { breakLine: true } }, { text: "Map", options: {} }] },
  { cx: 496.5, runs: [{ text: "2", options: {} }, { text: "nd", options: { superscript: true } }, { text: " Feature", options: { breakLine: true } }, { text: "Map", options: {} }] },
  { cx: 638.5, runs: [{ text: "3", options: {} }, { text: "rd", options: { superscript: true } }, { text: " Feature", options: { breakLine: true } }, { text: "Map", options: {} }] },
  { cx: 777.5, runs: [{ text: "4", options: {} }, { text: "th", options: { superscript: true } }, { text: " Feature", options: { breakLine: true } }, { text: "Map", options: {} }] },
];
for (const h of headers) {
  s.addText(h.runs, {
    x: px(h.cx - 61.2), y: px(146.5), w: px(122.4), h: px(30),
    align: "center", valign: "top", fontSize: 12, bold: true, color: RED,
    fontFace: FONT, lineSpacing: 14, margin: 0,
  });
}

// ---- 9. title ----
s.addText("1-D Convolutional Neural Network", {
  x: px(457 - 432), y: px(52.5), w: px(864), h: px(30),
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- 10. bottom hatched arrow (pre-generated 8x PNG, exact-size embed) ----
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/slide005_hatch_arrow.png",
  x: px(176), y: px(470), w: px(639), h: px(27),
});

// ---- 11. diagonal warning banner (yellow rect + rotated text; measured -21.7deg, band
//      length ~362px, perp ~31.6px, midline center (745,428) => rotate 338) ----
s.addShape(pres.ShapeType.rect, {
  x: px(745 - 181), y: px(428 - 15.85), w: px(362), h: px(31.7),
  fill: { color: "FFFF00" }, line: { type: "none" }, rotate: 338,
});
s.addText("*** Not Practical for Very Long Sequences***", {
  x: px(745 - 192.6), y: px(428 - 12.6), w: px(385.2), h: px(25.2),
  align: "center", valign: "middle", rotate: 338,
  fontSize: 16, bold: true, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 12. caption ----
s.addText(
  [
    { text: "As Word Sequence Length Increases, ", options: {} },
    { text: "we need to stack many convolution Layers.", options: { bold: true, underline: { style: "sng" } } },
  ],
  {
    x: px(494.5 - 396), y: px(502), w: px(792), h: px(22),
    align: "center", valign: "top", fontSize: 16.5, color: BLUE, fontFace: FONT, margin: 0,
  }
);

pres.writeFile({ fileName: "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_005_recreated.pptx" })
  .then(() => console.log("wrote slide_005_recreated.pptx"));
