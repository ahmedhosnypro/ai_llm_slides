// slide_013.js — "Classification Models: 2-D vs d-D Input Vectors" (ML lecture 02, MSSE deck)
// CHILD of certified slide 12 (founder edge 13 > 12; chain 9 → 11 → 12 → 13).
//
// Worker ml02-s013-gen2, 2026-10-14. Ground truth: PIL-measured from
// unique_slides/slide_013.jpg (960x540, 1px = 1pt); measurements banked in
// scratch/ml02/slide013/ (m1..m95, logs b1..b32).
//
// FOUNDER SPECIAL NOTE (2026-10-14): "13 depends on 12, because it has a
// component that is on 12, but it's being resized (smaller and positioned in
// top left of the frame (the axis component)". The parent's diagram re-emitted
// at MY measured smaller scale, top-left — as THIS build's delta. The parent
// component is never edited (cascade law).
//
// COMPOSITION — this frame has NO page title (verified m93/m94: the top strip
// y44..95 holds only the two input-vector banners + badge; zones between them
// are empty). Inherit from the certified parent component ./components/slide_012.js
// for CONSTANTS and certified style recipes only; draw everything at this
// frame's measured coordinates:
//
//   house chrome          (drawn ONCE, numeral 13 = printed frame number)
//   RED banner            (152..303, 59..83) fill 9F0001, 'Input Vector: 2-D'
//                         white bold ~14pt Arial (ink x160..276 y66..79)
//   GREEN banner          (584..739, 58..84) fill 089A03, 'Input Vector: d-D'
//                         white bold ~14pt (ink x598..709 y67..75)
//   TAN PANEL             (432..894, 89..534) fill C7B6A4, dark brown border
//                         5A3010 ~1.5pt (edges measured m84/m85: top y89..92,
//                         bottom y530..533, left x432..434, right x892..893);
//                         the right-column boxes sit ON it
//   diagram box           (73..374, 91..317) white, border 2A2380 — the parent
//                         slide-12 plot resized smaller top-left (founder delta):
//                         plane_s013.png embed + resized axes + marker set
//   axes (delta)          y-axis x94 y102..302, x-axis y301.5 x94..367, heads
//                         w4.5/h5 and w5.5/h4, 'Weight' rotated 270 6.5pt,
//                         'Length' 9pt — RED 8B0000 (parent style)
//   markers (delta)       11 wood rings d5.5 C4C1B8, 12 steel rings d5 000000,
//                         ?1 ring d14 + red '?', ?2/?3 plain muted '?' 894A55,
//                         mini 'Steel'/'Wood' 5pt labels
//   LT model table        (76..258, 322..376) fill FCFCE5 border AEABC8 1pt;
//                         'Model' red bold 13 underline; I/P + O/P black bold 13
//   LT eqbox              (75..371, 379..531) fill FCFCE5 border 9090A8 0.75pt;
//                         L1 'Model ( Plane )' red/green TNR bold italic 19pt +
//                         red underline; L2/L3 mathtext runs (eq_s013 manifest);
//                         L4 'Class > 0 Steel  Class < 0 Wood' / L5 rules
//                         TNR bold italic 18pt; L6 params
//   GC box                (446..701, 121..322) white, border 2B1B73 1.5pt;
//                         banner (507..660, 109..134) fill 0200A7 'General Case'
//                         white bold 15; 'Input:' red / 'Output:' blue bold 14;
//                         '( y )' blue TNR bold italic 18; column vector =
//                         height-fitted thin parens + 6 RED mathtext entries
//   RT model table        (446..678, 335..393) fill FCFCE5 border 9090A8 0.75pt;
//                         'Model' red bold 13 underline; 'I/P:'/'O/P:' black 13;
//                         I/P value '[X1, X2, X3, . . . . Xd]' + '[y]' mathtext
//   RT eqbox              (447..880, 403..515) fill FCFCE5 border 9090A8 0.75pt;
//                         R-L1 'Model ( Hyperplane )' TNR bold italic 19pt +
//                         red underline; R2/R3/R4 mathtext runs; empty rectangle
//                         outline shape (515..531 x 456..469) before 'Class 1'
//
// Spec-vs-frame notes: the analysis JSON's slide_title does NOT appear in the
// frame (no title ink anywhere in y44..95 outside banners/badge — m93/m94);
// verbatim content follows the measured pixels throughout.

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const parent = require(path.resolve(__dirname, "components/slide_012.js"));
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const PL = 1 / 72; // frame px -> inches

// ---- content constants (frame-measured) -------------------------------------
const RED = parent.RED;            // 8B0000 deck content red
const BLUE = parent.BLUE;          // 000080 eq-box blue
const GREEN = parent.GREEN;        // 008000 hyperplane green
const BLACK = "000000";
const MODEL_FILL = "FCFCE5";       // cream box fill (medians (251,253,229))
const MODEL_BORDER = "9090A8";     // eq/model box border family
const LT_TABLE_BORDER = "AEABC8";  // left model table border (m74 core)
const RED_BANNER = "9F0001";       // 'Input Vector: 2-D' banner fill (159,0,1)
const GREEN_BANNER = "089A03";     // 'Input Vector: d-D' banner fill (8,155,2)
const TAN_FILL = "C7B6A4";         // right-column panel fill (199,182,164)
const TAN_BORDER = "5A3010";       // tan panel dark brown edge (90,48,16)
const GC_BORDER = "2B1B73";        // General Case box border
const DIAGRAM_BORDER = "2A2380";   // left diagram box border
const GC_BANNER = "0200A7";        // 'General Case' banner fill (2,0,167)
const Q_MUTED = "894A55";          // ?2/?3 glyph (parent-verified ink)
const WOOD_RING = parent.WOOD_RING;// C4C1B8 light rings
const STEEL_RING = parent.STEEL_RING; // 000000 open rings
const WOOD_LABEL = "867C66";       // mini 'Wood' label

// ---- helpers ----------------------------------------------------------------
function lineSeg(pptx, slide, x1, y1, x2, y2, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: Math.min(x1, x2) * PL, y: Math.min(y1, y2) * PL,
    w: Math.abs(x2 - x1) * PL, h: Math.abs(y2 - y1) * PL,
    line: { color, width },
    flipV: (x2 - x1) * (y2 - y1) < 0,
  });
}
function ring(pptx, slide, cx, cy, d, color, width, fill) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: (cx - d / 2) * PL, y: (cy - d / 2) * PL, w: d * PL, h: d * PL,
    fill: fill ? { color: fill } : { type: "none" },
    line: { color, width },
  });
}
function labelAt(pptx, slide, cx, cy, text, opts = {}) {
  const w = (opts.wPx || 40) * PL, h = (opts.hPx || 14) * PL;
  slide.addText(text, {
    x: (cx - (opts.wPx || 40) / 2) * PL, y: (cy - (opts.hPx || 14) / 2) * PL,
    w, h, align: "center", valign: "middle", fontSize: opts.size || 10,
    bold: !!opts.bold, color: opts.color || BLACK, fontFace: opts.fontFace || "Arial",
    margin: 0, rotate: opts.rotate || 0,
  });
}

// ---- banners (title row) ----------------------------------------------------
function drawBanners(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 152 * PL, y: 59 * PL, w: 151 * PL, h: 24 * PL,
    fill: { color: RED_BANNER }, line: { type: "none" },
  });
  slide.addText("Input Vector: 2-D", {
    x: 156 * PL, y: 59 * PL, w: 124 * PL, h: 24 * PL,
    align: "center", valign: "middle", bold: true, fontSize: 14,
    color: "FFFFFF", fontFace: "Arial", margin: 0,
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 584 * PL, y: 58 * PL, w: 155 * PL, h: 26 * PL,
    fill: { color: GREEN_BANNER }, line: { type: "none" },
  });
  slide.addText("Input Vector: d-D", {
    x: 584 * PL, y: 58 * PL, w: 139 * PL, h: 26 * PL,
    align: "center", valign: "middle", bold: true, fontSize: 14,
    color: "FFFFFF", fontFace: "Arial", margin: 0,
  });
}

// ---- tan panel under the whole right column (m84/m85) -----------------------
function drawTanPanel(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 432 * PL, y: 89 * PL, w: 462 * PL, h: 445 * PL,
    fill: { color: TAN_FILL }, line: { color: TAN_BORDER, width: 1.5 },
  });
}

// ---- left diagram box: parent slide-12 plot, resized top-left (founder delta)
function drawDiagramBox(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 73 * PL, y: 91 * PL, w: 301 * PL, h: 226 * PL,
    fill: { color: "FFFFFF" }, line: { color: DIAGRAM_BORDER, width: 1.75 },
  });
  // tilted perspective plane — generated image, exact-size embed
  const info = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/plane_s013.json"), "utf8"));
  slide.addImage({
    path: path.resolve(__dirname, "assets/plane_s013.png"),
    x: info.x_in, y: info.y_in, w: info.w_in, h: info.h_in,
  });
  // resized axes (founder delta, parent style RED): y-axis x94 y102..302
  slide.addShape(pptx.ShapeType.line, {
    x: 94 * PL, y: 102 * PL, w: 0, h: (302 - 102) * PL,
    line: { color: RED, width: 1 },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: (94 - 2.25) * PL, y: 99.5 * PL, w: 4.5 * PL, h: 5 * PL,
    fill: { color: RED }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 94 * PL, y: 301.5 * PL, w: (367 - 94) * PL, h: 0,
    line: { color: RED, width: 1 },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: 362 * PL, y: (301.5 - 2) * PL, w: 5.5 * PL, h: 4 * PL,
    fill: { color: RED }, line: { type: "none" },
    rotate: 90, // apex pointing RIGHT
  });
  // 'Weight' rotated 270, ink center (83.5,109.5); 'Length' center (357.5,313)
  slide.addText("Weight", {
    x: (83.5 - 15) * PL, y: (109.5 - 15) * PL, w: 30 * PL, h: 30 * PL,
    rotate: 270, align: "center", valign: "middle",
    fontSize: 6.5, color: RED, fontFace: "Arial", margin: 0,
  });
  slide.addText("Length", {
    x: (357.5 - 17) * PL, y: (313 - 6) * PL, w: 34 * PL, h: 12 * PL,
    align: "center", valign: "middle",
    fontSize: 9, color: RED, fontFace: "Arial", margin: 0,
  });
}

// ---- marker set (parent slide-12 families, this frame's measured centers) ---
const WOOD_CENTERS = [
  [333.7, 161.0], [319.1, 162.1], [288.4, 173.0], [319.1, 174.1], [258.2, 203.9],
  [271.6, 207.2], [235.2, 209.1], [234.5, 229.4], [206.0, 246.8], [211.9, 246.8],
  [195.2, 253.3],
];
const STEEL_CENTERS = [
  [303.5, 189.5], [263.5, 102.5], [234.5, 109.5], [220.5, 138.5], [155.5, 189.5],
  [277.5, 97.5], [132.5, 201.5], [122.5, 203.0], [111.5, 213.5], [173.0, 169.5],
  [143.5, 187.5], [157.0, 172.5],
];
function drawMarkers(pptx, slide, opts = {}) {
  for (const [cx, cy] of WOOD_CENTERS) ring(pptx, slide, cx, cy, 5.5, WOOD_RING, 1);
  for (const [cx, cy] of STEEL_CENTERS) ring(pptx, slide, cx, cy, 5, STEEL_RING, 1);
  // ?1: open black ring d14 + red '?'
  ring(pptx, slide, 254, 132.5, 14, STEEL_RING, 1);
  slide.addText("?", {
    x: (254 - 6) * PL, y: (132.5 - 7) * PL, w: 12 * PL, h: 14 * PL,
    align: "center", valign: "middle", bold: true, fontSize: 10,
    color: RED, fontFace: "Arial", margin: 0,
  });
  // ?2 / ?3: plain muted '?' (no ring measured)
  for (const [cx, cy] of [[303, 166.5], [187.5, 225.5]]) {
    slide.addText("?", {
      x: (cx - 6) * PL, y: (cy - 7) * PL, w: 12 * PL, h: 14 * PL,
      align: "center", valign: "middle", bold: true, fontSize: 10,
      color: Q_MUTED, fontFace: "Arial", margin: 0,
    });
  }
  // mini class labels beside the clusters
  labelAt(pptx, slide, 234, 109.5, "Steel", { size: 5, color: BLACK, wPx: 18, hPx: 7, bold: true });
  labelAt(pptx, slide, 303.5, 189.5, "Wood", { size: 5, color: WOOD_LABEL, wPx: 20, hPx: 7, bold: true });
}

// ---- left model table -------------------------------------------------------
function drawLTTable(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 76 * PL, y: 322 * PL, w: 182 * PL, h: 54 * PL,
    fill: { color: MODEL_FILL }, line: { color: LT_TABLE_BORDER, width: 1 },
  });
  slide.addText("Model", {
    x: 82 * PL, y: 324 * PL, w: 62 * PL, h: 21 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 13,
    color: RED, fontFace: "Arial", margin: 0, underline: { style: "sng" },
  });
  slide.addText("I/P: Length, Weight", {
    x: 82 * PL, y: 342 * PL, w: 170 * PL, h: 16 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 13,
    color: BLACK, fontFace: "Arial", margin: 0,
  });
  slide.addText("O/P: Class Type", {
    x: 82 * PL, y: 356 * PL, w: 170 * PL, h: 16 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 13,
    color: BLACK, fontFace: "Arial", margin: 0,
  });
}

// ---- left equation box ------------------------------------------------------
function drawLTEqBox(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 75 * PL, y: 379 * PL, w: 296 * PL, h: 152 * PL,
    fill: { color: MODEL_FILL }, line: { color: MODEL_BORDER, width: 0.75 },
  });
  // L1 'Model ( Plane )' red/green TNR bold italic 19pt (ink y384..400)
  slide.addText([
    { text: "Model ", options: { color: RED } },
    { text: "( Plane )", options: { color: GREEN } },
  ], {
    x: 78 * PL, y: (392 / 72) - 0.3, w: 140 * PL, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    bold: true, italic: true, fontFace: "Times New Roman", fontSize: 19,
  });
  lineSeg(pptx, slide, 78, 399.5, 200, 399.5, RED, 1.25);
  // L2/L3 certified mathtext runs (baselines 421.5 / 444 in the manifest)
  const EQ = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq_s013_manifest.json"), "utf8"));
  for (const ln of ["L2", "L3"]) {
    for (const run of EQ.groups.L.runs.filter((r) => r.tag.startsWith(ln + "_"))) {
      slide.addImage({
        path: path.resolve(__dirname, "assets", run.image),
        x: run.x_in, y: run.y_in, w: run.w_in, h: run.h_in,
      });
    }
  }
  // L4/L5 decision rules (TNR bold italic 18pt, parent-certified recipe).
  // L4 packs TWO conditions (b39 audit: 'Class' x231..272, rule x281..302,
  // 'Wood' x313..358 — judge attempt-1 DISCREPANCY 1, pixel-verified).
  const rules = [
    [471.5, "  > 0", "   Steel", "       ", "Class", "  < 0", "  Wood"],
    [493.5, "  = 0", "   Undefined"],
  ];
  for (const [cy, cond, cls, sp2, cls2a, cond2, cls2b] of rules) {
    const runs = [
      { text: "Class", options: { color: BLUE } },
      { text: cond, options: { color: RED } },
      { text: cls, options: { color: BLUE } },
    ];
    if (cls2a) {
      runs.push({ text: sp2, options: { color: BLUE } });
      runs.push({ text: cls2a, options: { color: BLUE } });
      runs.push({ text: cond2, options: { color: RED } });
      runs.push({ text: cls2b, options: { color: BLUE } });
    }
    slide.addText(runs, {
      x: 77 * PL, y: (cy / 72) - 0.3, w: 300 * PL, h: 0.6,
      align: "left", valign: "middle", margin: 0,
      bold: true, italic: true, fontFace: "Times New Roman", fontSize: 18,
    });
  }
  // L6 'Model Parameters : a , b , c' (baseline ~524)
  slide.addText([
    { text: "Model Parameters", options: { color: BLUE } },
    { text: " : ", options: { color: BLUE } },
    { text: "a", options: { color: RED } },
    { text: " , ", options: { color: BLUE } },
    { text: "b", options: { color: RED } },
    { text: " , ", options: { color: BLUE } },
    { text: "c", options: { color: RED } },
  ], {
    x: 79 * PL, y: (518 / 72) - 0.3, w: 240 * PL, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    bold: true, italic: true, fontFace: "Times New Roman", fontSize: 18,
  });
}

// ---- General Case box + column vector --------------------------------------
function drawGCBox(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 446 * PL, y: 121 * PL, w: 255 * PL, h: 201 * PL,
    fill: { color: "FFFFFF" }, line: { color: GC_BORDER, width: 1.5 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 507 * PL, y: 109 * PL, w: 153 * PL, h: 25 * PL,
    fill: { color: GC_BANNER }, line: { type: "none" },
  });
  slide.addText("General Case", {
    x: 507 * PL, y: 109 * PL, w: 153 * PL, h: 25 * PL,
    align: "center", valign: "middle", bold: true, fontSize: 15,
    color: "FFFFFF", fontFace: "Arial", margin: 0,
  });
  slide.addText("Input:", {
    x: 468 * PL, y: 213 * PL, w: 60 * PL, h: 20 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 14,
    color: RED, fontFace: "Arial", margin: 0,
  });
  slide.addText("Output:", {
    x: 586 * PL, y: 213 * PL, w: 72 * PL, h: 20 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 14,
    color: BLUE, fontFace: "Arial", margin: 0,
  });
  slide.addText("( y )", {
    x: 650 * PL, y: 211 * PL, w: 32 * PL, h: 21 * PL,
    align: "left", valign: "middle", margin: 0,
    bold: true, italic: true, fontFace: "Times New Roman", fontSize: 18,
    color: BLUE,
  });
  const EQ = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq_s013_manifest.json"), "utf8"));
  for (const run of EQ.groups.PAREN.runs) {
    slide.addImage({
      path: path.resolve(__dirname, "assets", run.image),
      x: run.x_in, y: run.y_in, w: run.w_in, h: run.h_in,
    });
  }
  for (const run of EQ.groups.GC.runs) {
    slide.addImage({
      path: path.resolve(__dirname, "assets", run.image),
      x: run.x_in, y: run.y_in, w: run.w_in, h: run.h_in,
    });
  }
}

// ---- right model table ------------------------------------------------------
function drawRTTable(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 446 * PL, y: 335 * PL, w: 232 * PL, h: 58 * PL,
    fill: { color: MODEL_FILL }, line: { color: MODEL_BORDER, width: 0.75 },
  });
  slide.addText("Model", {
    x: 452 * PL, y: 338 * PL, w: 50 * PL, h: 18 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 13,
    color: RED, fontFace: "Arial", margin: 0, underline: { style: "sng" },
  });
  slide.addText("I/P:", {
    x: 452 * PL, y: 355 * PL, w: 34 * PL, h: 16 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 13,
    color: BLACK, fontFace: "Arial", margin: 0,
  });
  slide.addText("O/P:", {
    x: 451 * PL, y: 371 * PL, w: 40 * PL, h: 16 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 13,
    color: BLACK, fontFace: "Arial", margin: 0,
  });
  const EQ = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq_s013_manifest.json"), "utf8"));
  for (const run of EQ.groups.RT.runs) {
    slide.addImage({
      path: path.resolve(__dirname, "assets", run.image),
      x: run.x_in, y: run.y_in, w: run.w_in, h: run.h_in,
    });
  }
}

// ---- right equation box -----------------------------------------------------
function drawRTEqBox(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 447 * PL, y: 403 * PL, w: 433 * PL, h: 112 * PL,
    fill: { color: MODEL_FILL }, line: { color: MODEL_BORDER, width: 0.75 },
  });
  // R-L1 'Model ( Hyperplane )' red/green TNR bold italic 19pt (ink y407..425)
  slide.addText([
    { text: "Model ", options: { color: RED } },
    { text: "( Hyperplane )", options: { color: GREEN } },
  ], {
    x: 450 * PL, y: (416 / 72) - 0.3, w: 200 * PL, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    bold: true, italic: true, fontFace: "Times New Roman", fontSize: 19,
  });
  lineSeg(pptx, slide, 451, 422.5, 633, 422.5, RED, 1.25);
  const EQ = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq_s013_manifest.json"), "utf8"));
  for (const ln of ["R2", "R3", "R4"]) {
    for (const run of EQ.groups.R.runs.filter((r) => r.tag.startsWith(ln + "_"))) {
      slide.addImage({
        path: path.resolve(__dirname, "assets", run.image),
        x: run.x_in, y: run.y_in, w: run.w_in, h: run.h_in,
      });
    }
  }
  // R-L3 empty rectangle outline before 'Class 1' (measured 515..531 x 456..469)
  slide.addShape(pptx.ShapeType.rect, {
    x: 515 * PL, y: 456 * PL, w: 16 * PL, h: 13 * PL,
    fill: { type: "none" }, line: { color: BLUE, width: 1 },
  });
  // R-L4 'Model Parameters :' text head (mathtext w-runs follow at baseline 507.5)
  slide.addText([
    { text: "Model Parameters", options: { color: BLUE } },
    { text: " :", options: { color: BLUE } },
  ], {
    x: 450 * PL, y: (501.5 / 72) - 0.3, w: 160 * PL, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    bold: true, italic: true, fontFace: "Times New Roman", fontSize: 18,
  });
}

// ---- composition ------------------------------------------------------------
// opts.numeral overrides the badge numeral (default 13 = printed frame number).
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 13 : opts.numeral });
  drawTanPanel(pptx, slide, opts);   // under everything in the right column
  drawBanners(pptx, slide, opts);    // title row (no page title in this frame)
  drawDiagramBox(pptx, slide, opts); // parent-12 plot resized top-left (founder delta)
  drawMarkers(pptx, slide, opts);
  drawLTTable(pptx, slide, opts);
  drawLTEqBox(pptx, slide, opts);
  drawGCBox(pptx, slide, opts);
  drawRTTable(pptx, slide, opts);
  drawRTEqBox(pptx, slide, opts);
}

// ---- build ----------------------------------------------------------------
function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out =
    process.argv[2] ||
    path.resolve(__dirname, "..", "slide_013_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, build, drawBanners, drawTanPanel, drawDiagramBox, drawMarkers, drawLTTable, drawLTEqBox, drawGCBox, drawRTTable, drawRTEqBox };
