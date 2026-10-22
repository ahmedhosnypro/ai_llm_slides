// Slide 006 — "Regression – Two Dimensional Case"
// Deck: machine-learning/02_linear-regression-classification-MSSE (39 slides)
// Worker: ml02-w006-a1, 2026-10-13. ROOT slide (no parents, no children in deps).
//
// Ground truth: unique_slides/slide_006.jpg (960x540, 1px = 1pt = 1/72 in).
// PIL measurement passes 1-7 (scratch/ml02/slide006/measure*.py), consolidated:
//   - inner white rect w/ thin dark-red border: x87..861, y96..517 (border 8B0000 ~1pt;
//     sampled (141,30,46)); area inside is WHITE, panel gray outside.
//   - title ink x291..621 y60..78, center (456,69): "Regression – " 8B0000 + "Two" 0000CD
//     + " Dimensional Case" 8B0000 (only "Two" is blue — measured col runs; the spec's
//     "'Two Dimensional Case' in blue" is a spec quirk, frame wins). Arial bold 19pt.
//   - subtitle ink x289..799 y113..130, Times New Roman bold ~19pt, blue 0000CD.
//   - 3D diagram: axes B22222 2pt w/ triangle arrowheads: Weight vertical x260
//     (y113 arrow tip -> y374), Length horizontal y357.5 (x260 -> x576), Radius
//     diagonal (261,363)->(120,491). Axes sit UNDER the translucent plane (measured
//     muted inside plane: (205,171,162) vs (176,0,23) outside).
//   - plane: perspective quad L(197,324) T(425,171) R(524,217) B(287,392), fill
//     FFFFE0 ~45% opacity (measured fill (251,254,241) over white), thin gray
//     outline (~666666, 1px). Drawn OVER the axes, UNDER dots/dashes/projections.
//   - scatter dots (18 measured): 11 strong d9 4169E1, 5 medium d6.5 B7C4D6,
//     2 faint d4.5 CBD5E2. Dashed red residual drops (B22222 1pt dash) under the
//     upper dots (measured y-extents).
//   - projection (dotted B22222 sysDot 1pt): H (257,300)->(362,300), V (363,305)->
//     (363,387), H2 (240,387)->(363,387); solid arrowhead apex-up at (362,294.5);
//     discs: "?" d23 8B0000 @(245.8,300) w/ white ?, start dot d5.5 @(264.7,300),
//     Length-axis disc d11 @(384.5,358.5), Radius-axis disc d15 @(232,386).
//   - Model box x670..837 y149..212, fill FFFFE0 (12% transp), thin gray border;
//     3 lines TNR bold 16pt lineSpacing 19: "Model" B22222 underlined /
//     "I/P:   Length, Radius" black / "O/P: Weight" black.
//   - Model (Plane) box x559..839 y227..340, same fill/border. L1 "Model " B22222 +
//     "( Plane)" 008000, TNR bold italic ~21pt underlined; L2/L3 equations as
//     mathtext PNG runs (STIX, 18.9pt fitted, per-run colors blue 0000CD /
//     red B22222, placed at measured ink-left x on shared baselines 271.1/294.7);
//     L4 "Model Parameters" 0000CD + " : a , b , c" B22222, TNR bold italic 18pt.
//   - axis labels B22222 bold Arial ~12pt: "Weight" rotated 270 center (249.5,139),
//     "Length" @(533,369 left-aligned), "Radius" rotated 318 center (168,460).
//   - cursor artifact at ~(362,347): GROUND RULES (c) — NOT drawn.
// Equations per founder directive: matplotlib mathtext -> 600dpi transparent PNG ->
// addImage at exact size (w = px/600 in), baseline-law placement, per-run colors
// (single-color runs positioned at measured x; closed-loop ink-edge check follows).
// House chrome via shared_patterns/house_chrome.js (THIS deck's values), numeral 6.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.join(__dirname, "..", "..", "shared_patterns", "house_chrome.js"));

const px = (v) => v / 72; // frame px -> inches

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "slide-recreation";
pres.title = "Regression – Two Dimensional Case";

const slide = pres.addSlide();

// --- House chrome (numeral = number printed on the original = 6) ---
drawHouseChrome(pres, slide, { numeral: 6 });

// --- Inner white rect with thin dark-red border ---
slide.addShape(pres.ShapeType.rect, {
  x: px(87), y: px(96), w: px(774), h: px(421),
  fill: { color: "FFFFFF" },
  line: { color: "8B0000", width: 1 },
});

// --- Axes (B22222, 2pt, triangle arrowheads) — drawn BEFORE the translucent plane ---
const AXIS = { color: "B22222", width: 2 };
// Weight (vertical): arrow at TOP (flipV so path end = top)
slide.addShape(pres.ShapeType.line, {
  x: px(260), y: px(113), w: 0, h: px(261), flipV: true,
  line: { color: AXIS.color, width: AXIS.width, endArrowType: "triangle" },
});
// Length (horizontal): arrow at RIGHT
slide.addShape(pres.ShapeType.line, {
  x: px(260), y: px(357.5), w: px(316), h: 0,
  line: { color: AXIS.color, width: AXIS.width, endArrowType: "triangle" },
});
// Radius (diagonal down-left): arrow at END (120,491) (flipH: start (261,363))
slide.addShape(pres.ShapeType.line, {
  x: px(120), y: px(363), w: px(141), h: px(128), flipH: true,
  line: { color: AXIS.color, width: AXIS.width, endArrowType: "triangle" },
});

// --- Regression plane: perspective quad (custGeom, translucent pale yellow) ---
slide.addShape(pres.ShapeType.custGeom, {
  x: 0, y: 0, w: 13.333, h: 7.5, // full-slide bbox; absolute inch points
  fill: { color: "FFFFE0", transparency: 50 },
  line: { color: "666666", width: 0.75 },
  points: [
    { x: px(197), y: px(324), moveTo: true }, // left corner
    { x: px(425), y: px(171) },               // top corner
    { x: px(524), y: px(217) },               // right corner
    { x: px(287), y: px(392) },               // bottom corner
    { x: px(197), y: px(324), close: true },
  ],
});

// --- Residual dashed drops (B22222 1pt dash) under the upper dots ---
const RES = { color: "B22222", width: 1, dashType: "dash" };
const resids = [
  [418, 194, 236], [399, 207, 236], [462, 223, 247], [498, 220, 247],
  [359, 261, 282], [314, 276, 300], [351, 245, 270], [339, 289, 308],
];
for (const [x, y0, y1] of resids) {
  slide.addShape(pres.ShapeType.line, {
    x: px(x), y: px(y0), w: 0, h: px(y1 - y0), line: { ...RES },
  });
}
// fainter drops under the pale dots
const RESF = { color: "B22222", width: 1, dashType: "dash", transparency: 50 };
for (const [x, y0, y1] of [[372, 225, 240], [450, 249, 262], [378, 299, 314], [308, 318, 332]]) {
  slide.addShape(pres.ShapeType.line, {
    x: px(x), y: px(y0), w: 0, h: px(y1 - y0), line: { ...RESF },
  });
}

// --- Scatter dots ---
function dot(cx, cy, d, color, transparency) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color, transparency: transparency || 0 }, line: { type: "none" },
  });
}
// strong (4169E1, d9)
for (const [cx, cy] of [[420, 190], [399, 203], [498, 216], [420, 219], [462, 219],
  [351, 241], [359, 257], [314, 272], [339, 285], [275, 317], [308, 336]]) {
  dot(cx, cy, 9, "4169E1");
}
// medium (B7C4D6, d6.5)
for (const [cx, cy] of [[372, 221], [450, 245], [378, 295], [308, 314], [274, 338]]) {
  dot(cx, cy, 6.5, "B7C4D6");
}
// faint (CBD5E2, d4.5)
for (const [cx, cy] of [[433, 273], [405, 289]]) {
  dot(cx, cy, 4.5, "CBD5E2");
}

// --- Projection dotted lines + markers (over the plane) ---
const PROJ = { color: "B22222", width: 1, dashType: "sysDot" };
slide.addShape(pres.ShapeType.line, { x: px(257), y: px(300), w: px(105), h: 0, line: { ...PROJ } });
slide.addShape(pres.ShapeType.line, { x: px(363), y: px(305), w: 0, h: px(82), line: { ...PROJ } });
slide.addShape(pres.ShapeType.line, { x: px(240), y: px(387), w: px(123), h: 0, line: { ...PROJ } });
// solid arrowhead apex-up at top of the vertical dotted line
slide.addShape(pres.ShapeType.triangle, {
  x: px(357), y: px(294.5), w: px(10), h: px(10.5),
  fill: { color: "B22222" }, line: { color: "B22222", width: 0 },
});
// start dot right of the "?" disc
dot(264.7, 300, 5.5, "8B0000");
// disc on the Length axis
dot(384.5, 358.5, 11, "B22222");
// disc on the Radius axis
dot(232, 386, 15, "B22222");
// "?" disc with white question mark
dot(245.8, 300, 23, "8B0000");
slide.addText("?", {
  x: px(245.8 - 11.5), y: px(300 - 11.5), w: px(23), h: px(23),
  align: "center", valign: "middle", fontFace: "Times New Roman",
  fontSize: 13, bold: true, color: "FFFFFF", margin: 0,
});

// --- Axis labels ---
slide.addText("Weight", {
  x: px(249.5) - 0.5, y: px(139) - 0.15, w: 1.0, h: 0.3,
  align: "center", valign: "middle", rotate: 270,
  fontFace: "Arial", fontSize: 12, bold: true, color: "B22222", margin: 0,
});
slide.addText("Length", {
  x: px(531), y: px(369) - 0.15, w: 1.0, h: 0.3,
  align: "left", valign: "middle",
  fontFace: "Arial", fontSize: 12, bold: true, color: "B22222", margin: 0,
});
slide.addText("Radius", {
  x: px(168) - 0.5, y: px(460) - 0.15, w: 1.0, h: 0.3,
  align: "center", valign: "middle", rotate: 318,
  fontFace: "Arial", fontSize: 12, bold: true, color: "B22222", margin: 0,
});

// --- Title (measured ink center (456,69); box centered on ink center) ---
slide.addText([
  { text: "Regression – ", options: { color: "8B0000" } },
  { text: "Two", options: { color: "0000CD" } },
  { text: " Dimensional Case", options: { color: "8B0000" } },
], {
  x: px(456) - 4.5, y: px(69) - 0.25, w: 9.0, h: 0.5,
  align: "center", valign: "middle", bold: true, fontFace: "Arial",
  fontSize: 19, margin: 0,
});

// --- Subtitle (measured ink x289..799 y113..130; TNR bold 19pt 0000CD;
// double gaps after "Radius," and "of" reproduce the original's measured gaps) ---
slide.addText("Length, Radius,  and Weight of  different samples of Steel Bars", {
  x: px(287), y: px(121.5) - 0.2, w: 7.6, h: 0.4,
  align: "left", valign: "middle", bold: true, fontFace: "Times New Roman",
  fontSize: 19, color: "0000CD", margin: 0,
});

// --- Model box (x670..837 y149..212) ---
slide.addShape(pres.ShapeType.rect, {
  x: px(670), y: px(149), w: px(167), h: px(63),
  fill: { color: "FFFFE0", transparency: 12 },
  line: { color: "8C8C8C", width: 0.75 },
});
slide.addText([
  { text: "Model", options: { color: "B22222", underline: true, breakLine: true } },
  { text: "I/P:   Length, Radius", options: { color: "000000", breakLine: true } },
  { text: "O/P: Weight", options: { color: "000000" } },
], {
  x: px(675), y: px(151), w: px(160), h: px(59),
  align: "left", valign: "top", bold: true, fontFace: "Times New Roman",
  fontSize: 16, lineSpacing: 19, margin: 0,
});

// --- Model (Plane) box (x559..839 y227..340) ---
slide.addShape(pres.ShapeType.rect, {
  x: px(559), y: px(227), w: px(280), h: px(113),
  fill: { color: "FFFFE0", transparency: 12 },
  line: { color: "8C8C8C", width: 0.75 },
});
// L1 heading
slide.addText([
  { text: "Model ", options: { color: "B22222" } },
  { text: "( Plane)", options: { color: "008000" } },
], {
  x: px(562), y: px(225.75), w: px(250), h: px(30),
  align: "left", valign: "top", bold: true, italic: true, underline: true,
  fontFace: "Times New Roman", fontSize: 21, margin: 0,
});
// L2/L3 equation PNGs (mathtext, exact size, baseline-law placement)
const EQ = JSON.parse(fs.readFileSync(path.join(__dirname, "assets", "eq_s006_manifest.json"), "utf8"));
for (const line of ["L2", "L3"]) {
  for (const run of EQ.lines[line].runs) {
    slide.addImage({
      path: path.join(__dirname, "assets", run.image),
      x: run.x_in, y: run.y_in, w: run.w_in, h: run.h_in,
    });
  }
}
// L4
slide.addText([
  { text: "Model Parameters", options: { color: "0000CD" } },
  { text: " : a , b , c", options: { color: "B22222" } },
], {
  x: px(562), y: px(316.1), w: px(250), h: px(26),
  align: "left", valign: "top", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 18, margin: 0,
});

const OUT = path.join(__dirname, "..", "slide_006_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE", OUT);
});
