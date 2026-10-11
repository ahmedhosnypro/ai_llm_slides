// slide_036.js — "Self Attention Mechanism (Scaling based on Square Root of
// Embedding Vector Dimension)" (Deep Learning DSAI 308, Transformers — Part I).
// Build worker attempt 1, 2026-10-11.
//
// CHROME: playlist house chrome ONLY — drawHouseChrome(pptx, slide, {numeral: 36})
// from videos/deep-learning/shared_patterns/house_chrome.js. The ml-intro values in
// 17_worker_instructions.md are superseded for this playlist.
//
// GEOMETRY PROVENANCE — PIL pixel forensics on unique_slides/slide_036.jpg
// (960x540, 1px = 1pt = 1/72 in); scratch/slide036/measure*.py. All coordinates below
// are frame pixels (PX = 1/72 in). Color cores reconciled from darkest-2% pixel
// medians (video-chroma-corrected): maroon text/labels 990000, blue math 0000B0,
// arrows/borders C00000, green borders 3B7A40, indigo (bell border, output parens,
// output-chip borders) 333399, FC2 border/fill 800080/F9E3FA, subtitle 990000 with
// FFFF00 highlight on '(Scaling'.
// MEASURED FRAME FACTS that override the spec JSON (frame is ground truth):
//   - equations-box + statement-box borders are GREEN (spec said red) — border stroke
//     medians (62,133,91)/(20,121,55); eqbox fill WHITE (spec said mint); stmt1 fill
//     pale green E6FCEC (spec said white).
//   - bell-box border is INDIGO 333399 (spec said red); its axes are red C00000.
//   - statement-box math tokens (sqrt-d, 4th-root-d) are BLUE, prose MAROON
//     (spec said green token / dark prose) — token cores (0,0,99), prose (115,15,23).
//   - formula boxes 1+2 text is ALL maroon 990000 incl. w'_ij (spec said blue) —
//     no blue pixel anywhere in either box.
//   - FBOX3: 'd=100,' blue + 'sqrt-d' MAROON + '=10' blue (red segment x786..805).
//   - EQBOX L1/L2: black prose, MAROON V1/V2 token, BLUE M (blue seg x559..569 only).
//   - EQBOX L3/L4: blue bold italic with MAROON V-token (x439..451) and MAROON
//     sqrt-d token (x610..633).
//   - V2 toy columns contain FOUR glyphs each (measured bands y142/158/175/192 left,
//     y142/161/180/199 right; brackets span y131..214 — no room for a 5th), NOT five
//     as the spec transcription claims. Frame wins; recorded in worker report.
//   - FC1 fill = panel gray (no fill), FC1 border 1A1A1A, output-chip digits BLACK.
//   - 'M' label under bell x-axis: x776..789 y207..218, blue.
// Equations per the Math equation format rule: matplotlib mathtext -> 600dpi
// transparent PNG -> addImage at EXACT px/600 size, baseline-law alignment
// (y_image = target_baseline_in - baseline_frac*h_in). Tall parens/brackets via the
// certified delimiters-stretched-glyph pattern (assets d_*.png).

var fs = require("fs");
var path = require("path");
var pptxgen = require("pptxgenjs");
var drawHouseChrome = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
).drawHouseChrome;

var ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/slide036";
var PX = 1 / 72; // frame px -> inches

var C = {
  black: "1A1A1A",
  titleBlack: "000000",
  maroon: "990000",
  blue: "0000B0",
  red: "C00000",
  green: "3B7A40",
  indigo: "333399",
  purple: "800080",
  orange: "FFA500",
  vecFill: "FCFFE4",
  eqFill: "FFFFFF",
  bellFill: "FFFFFF",
  stmt1Fill: "E6FCEC",
  stmt2Fill: "FFF8D7",
  chipIn: "FFFCC0",
  chipOut: "FFFDCE",
  fc2Fill: "F9E3FA",
  highlight: "FFFF00",
};
var FONT = "Arial";

function sidecar(name) {
  return JSON.parse(fs.readFileSync(path.join(ASSETS, name + ".json"), "utf8"));
}
// place a mathtext PNG by BASELINE law: baselineY in frame px
function eqImage(slide, name, xPx, baselineYPx) {
  var s = sidecar(name);
  slide.addImage({
    path: path.join(ASSETS, name + ".png"),
    x: xPx * PX,
    y: (baselineYPx / 72) - s.baseline_frac * s.h_in,
    w: s.w_in, h: s.h_in,
  });
  return s;
}
// place a delimiter PNG by top-left frame px
function delim(slide, name, xPx, yPx) {
  var s = sidecar(name.replace(".png", ""));
  slide.addImage({
    path: path.join(ASSETS, name),
    x: xPx * PX, y: yPx * PX, w: s.w_in, h: s.h_in,
  });
}
function text(slide, runsOrStr, x, y, w, h, opts) {
  var o = {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    fontFace: FONT, margin: 0, align: (opts && opts.align) || "left",
    valign: (opts && opts.valign) || "top",
  };
  if (opts && opts.fontSize) o.fontSize = opts.fontSize;
  if (opts && opts.bold) o.bold = true;
  if (opts && opts.italic) o.italic = true;
  if (opts && opts.underline) o.underline = true;
  if (opts && opts.color) o.color = opts.color;
  if (opts && opts.rotate) o.rotate = opts.rotate;
  slide.addText(runsOrStr, o);
}

var pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
var s = pres.addSlide();

// ---- house chrome (playlist law) -------------------------------------------
drawHouseChrome(pres, s, { numeral: 36 });

// ---- title + subtitle -------------------------------------------------------
// ink y58..72 x374..616 (center 495), ~20pt bold black
text(s, "Self Attention Mechanism", 495 - 436.7, 55, 873.4, 30,
  { align: "center", fontSize: 20, bold: true, color: C.titleBlack });
// ink y80..99 x191..805 (center 498), 20pt bold maroon; FFFF00 highlight on '(Scaling'
// drawn as an EXPLICIT yellow rect (measured x196..267 y77..98) behind the text —
// LO mis-renders pptxgenjs run-level `highlight` (stray 19x4px yellow chip at x110).
s.addShape(pres.ShapeType.rect, {
  x: 196 * PX, y: 77 * PX, w: 72 * PX, h: 22 * PX,
  fill: { color: C.highlight }, line: { type: "none" },
});
text(s, "(Scaling based on Square Root of Embedding Vector Dimension)",
  498 - 436.7, 77, 873.4, 26,
  { align: "center", fontSize: 20, bold: true, color: C.maroon });

// ---- vector-transformation container (green) --------------------------------
s.addShape(pres.ShapeType.roundRect, {
  x: 46 * PX, y: 99 * PX, w: 225 * PX, h: 274 * PX, rectRadius: 0.06,
  fill: { color: C.vecFill }, line: { color: C.green, width: 1.5 },
});
// orange dashed divider at x150
s.addShape(pres.ShapeType.line, {
  x: 150 * PX, y: 115 * PX, w: 0, h: 250 * PX,
  line: { color: C.orange, width: 1.25, dashType: "dash" },
});
// white block arrow with blue outline crossing the divider
s.addShape(pres.ShapeType.rightArrow, {
  x: 115 * PX, y: 240 * PX, w: 54 * PX, h: 30 * PX,
  fill: { color: "FFFFFF" }, line: { color: C.blue, width: 1.5 },
});

// vector headers V1/V2 (blue bold italic 14pt) — x-centers 62/103/181.5/222.5
function header(cx, sub) {
  text(s, [
    { text: "V", options: {} },
    { text: sub, options: { subscript: true } },
  ], cx - 14, 106, 28, 24, { align: "center", fontSize: 14, bold: true, italic: true, color: C.blue });
}
header(63.5, "1"); header(104.5, "2"); header(183, "1"); header(224, "2");

// left V1 column: 12 maroon X's (x58..75), cy 150.5 + i*16.6
var i, cy;
for (i = 0; i < 12; i++) {
  cy = 150.5 + i * 16.6;
  text(s, [
    { text: "X", options: {} },
    { text: String(i + 1), options: { subscript: true } },
  ], 56, cy - 9, 22, 18, { align: "center", fontSize: 12, bold: true, color: C.maroon });
}
// left V2 column: 4 maroon X's (x104..116), cy 147.5 + i*17.2
for (i = 0; i < 4; i++) {
  cy = 147.5 + i * 17.2;
  text(s, [
    { text: "X", options: {} },
    { text: String(i + 1), options: { subscript: true } },
  ], 101, cy - 9, 19, 18, { align: "center", fontSize: 12, bold: true, color: C.maroon });
}
// right V1 column: 12 blue M's (x178..192), cy 151 + i*16.14
for (i = 0; i < 12; i++) {
  cy = 151 + i * 16.14;
  text(s, "M", 175, cy - 9, 21, 18, { align: "center", fontSize: 14, bold: true, color: C.blue });
}
// right V2 column: 4 blue M's (x224..238), cy 147.5 + i*18.67
for (i = 0; i < 4; i++) {
  cy = 147.5 + i * 18.67;
  text(s, "M", 221, cy - 9, 21, 18, { align: "center", fontSize: 14, bold: true, color: C.blue });
}
// tall maroon parens (stretched-glyph PNGs, exact px/600 size)
delim(s, "d_v1L_l.png", 51, 132); delim(s, "d_v1L_r.png", 72, 132);
delim(s, "d_v2L_l.png", 94, 131); delim(s, "d_v2L_r.png", 117, 131);
delim(s, "d_v1R_l.png", 170, 132); delim(s, "d_v1R_r.png", 196, 132);
delim(s, "d_v2R_l.png", 214, 131); delim(s, "d_v2R_r.png", 238, 131);
// 1xd labels (maroon italic 11pt)
function xd(x, y, sub) {
  text(s, [
    { text: "1xd", options: {} },
    { text: sub, options: { subscript: true } },
  ], x, y, 32, 22, { align: "center", fontSize: 15, italic: true, color: C.maroon });
}
xd(78, 346, "1");   // under left V1 (measured x84..109 y347..365)
xd(117, 211, "2");  // bottom-right of left V2 (x123..148 y212..229)
xd(198, 346, "1");  // under right 12-M column (x204..228 y347..364)
xd(237, 211, "2");  // bottom-right of right V2 (x243..268 y212..229)

// ---- equations box (white fill, green border) --------------------------------
s.addShape(pres.ShapeType.rect, {
  x: 308 * PX, y: 106 * PX, w: 352 * PX, h: 121 * PX,
  fill: { color: C.eqFill }, line: { color: C.green, width: 1.25 },
});
// L1: y121..133 — black prose, maroon V1, blue M
text(s, [
  { text: "Let Average Values of elements of ", options: { color: C.black } },
  { text: "V", options: { color: C.maroon, bold: true } },
  { text: "1", options: { color: C.maroon, bold: true, subscript: true } },
  { text: " = ", options: { color: C.black } },
  { text: "M", options: { color: C.blue, bold: true } },
], 321, 118, 262, 19, { fontSize: 13.5 });
// L2
text(s, [
  { text: "Let Average Values of elements of ", options: { color: C.black } },
  { text: "V", options: { color: C.maroon, bold: true } },
  { text: "2", options: { color: C.maroon, bold: true, subscript: true } },
  { text: " = ", options: { color: C.black } },
  { text: "M", options: { color: C.blue, bold: true } },
], 321, 140, 262, 19, { fontSize: 13.5 });
// L3: blue bold italic; maroon first V1 + maroon sqrt(d1) PNG at x610 (baseline 184)
text(s, [
  { text: "Vector Length of ", options: {} },
  { text: "V", options: { color: C.maroon } },
  { text: "1", options: { color: C.maroon, subscript: true } },
  { text: " (all Ms) = ", options: {} },
  { text: "V", options: {} },
  { text: "1", options: { subscript: true } },
  { text: "T", options: { superscript: true } },
  { text: " V", options: {} },
  { text: "1", options: { subscript: true } },
  { text: " = M ", options: {} },
], 323, 165, 284, 26, { fontSize: 15, bold: true, italic: true, color: C.blue });
eqImage(s, "eq_sqrt_d1", 610, 184);
// L4
text(s, [
  { text: "Vector Length of ", options: {} },
  { text: "V", options: { color: C.maroon } },
  { text: "2", options: { color: C.maroon, subscript: true } },
  { text: " (all Ms) = ", options: {} },
  { text: "V", options: {} },
  { text: "2", options: { subscript: true } },
  { text: "T", options: { superscript: true } },
  { text: " V", options: {} },
  { text: "2", options: { subscript: true } },
  { text: " = M ", options: {} },
], 323, 194, 284, 26, { fontSize: 15, bold: true, italic: true, color: C.blue });
eqImage(s, "eq_sqrt_d2", 610, 213);

// ---- bell-curve box (white fill, indigo border) ------------------------------
s.addShape(pres.ShapeType.rect, {
  x: 683 * PX, y: 110 * PX, w: 211 * PX, h: 110 * PX,
  fill: { color: C.bellFill }, line: { color: C.indigo, width: 1.5 },
});
// plot interior (grid + red L axes + gaussian + dashed peak) as one 600dpi PNG
s.addImage({
  path: path.join(ASSETS, "bell_plot.png"),
  x: 704 * PX, y: 112 * PX, w: 160 / 72, h: 90 / 72,
});
// blue bold-italic M under the x-axis (measured x776..789 y207..218)
text(s, "M", 771, 203, 23, 19, { align: "center", fontSize: 13, bold: true, italic: true, color: C.blue });

// ---- statement boxes ---------------------------------------------------------
// STMT1: white->pale-green fill, thick green border; blue sqrt(d) PNG + maroon prose
s.addShape(pres.ShapeType.rect, {
  x: 296 * PX, y: 238 * PX, w: 306 * PX, h: 42 * PX,
  fill: { color: C.stmt1Fill }, line: { color: C.green, width: 2 },
});
eqImage(s, "eq_sqrtd_b", 305, 267);
text(s, " is a good choice for scaling", 347, 242, 250, 28,
  { fontSize: 18.5, bold: true, italic: true, color: C.maroon, valign: "middle" });
// STMT2: pale-yellow fill, green border; blue 4th-root(d) PNG + maroon prose
s.addShape(pres.ShapeType.rect, {
  x: 617 * PX, y: 238 * PX, w: 280 * PX, h: 43 * PX,
  fill: { color: C.stmt2Fill }, line: { color: C.green, width: 1.5 },
});
eqImage(s, "eq_4sqrtd_b", 655, 267);
text(s, " Some times is used", 698, 242, 186, 28,
  { fontSize: 18.5, bold: true, italic: true, color: C.maroon, valign: "middle" });

// ---- formula boxes -----------------------------------------------------------
// FBOX1 x291..443 y306..363: SoftMax + tall [ ] + w'_ij (all maroon)
s.addShape(pres.ShapeType.rect, {
  x: 291 * PX, y: 306 * PX, w: 153 * PX, h: 58 * PX,
  fill: { color: "FFFFFF" }, line: { color: C.red, width: 1.5 },
});
text(s, "SoftMax", 296, 325, 64, 20,
  { align: "center", fontSize: 15, bold: true, color: C.maroon, valign: "middle" });
delim(s, "d_fb1_l.png", 378, 314);
delim(s, "d_fb1_r.png", 409, 314);
eqImage(s, "eq_wij_inner", 390.5, 339);
// FBOX2 x503..655 y296..373: SoftMax + big parens + stacked fraction (all maroon)
s.addShape(pres.ShapeType.rect, {
  x: 503 * PX, y: 296 * PX, w: 153 * PX, h: 78 * PX,
  fill: { color: "FFFFFF" }, line: { color: C.red, width: 1.5 },
});
text(s, "SoftMax", 507, 327, 70, 22,
  { align: "center", fontSize: 15, bold: true, color: C.maroon, valign: "middle" });
delim(s, "d_fb2_l.png", 590, 305);
delim(s, "d_fb2_r.png", 634, 305);
(function () {
  var f = sidecar("eq_frac");
  s.addImage({
    path: path.join(ASSETS, "eq_frac.png"),
    x: 600 * PX,
    y: (337.5 / 72) - f.h_in / 2, // display fraction: center on measured band mid
    w: f.w_in, h: f.h_in,
  });
})();
// FBOX3 x705..857 y308..359: 'd=100,' blue + maroon sqrt(d) PNG + '=10' blue
s.addShape(pres.ShapeType.rect, {
  x: 705 * PX, y: 308 * PX, w: 153 * PX, h: 52 * PX,
  fill: { color: "FFFFFF" }, line: { color: C.red, width: 1.5 },
});
text(s, "d=100,", 719, 321, 66, 20, { fontSize: 14.5, bold: true, color: C.blue });
eqImage(s, "eq_sqrtd_m", 786, 337);
text(s, " =10", 808, 321, 36, 20, { fontSize: 14.5, bold: true, color: C.blue });

// ---- Remember box -------------------------------------------------------------
s.addShape(pres.ShapeType.rect, {
  x: 44 * PX, y: 386 * PX, w: 180 * PX, h: 122 * PX,
  fill: { color: "FFFFFF" }, line: { color: C.red, width: 1.25 },
});
text(s, "Remember:", 49, 397, 92, 18,
  { fontSize: 14, bold: true, italic: true, color: C.blue });
text(s, "\"d\" is", 104, 413, 62, 18,
  { align: "center", fontSize: 14, bold: true, color: C.black });
text(s, "Dimension of Embedding", 44, 430, 183, 20,
  { align: "center", fontSize: 14, bold: true, color: C.red, underline: true });
text(s, "Not", 104, 463, 62, 18,
  { align: "center", fontSize: 14, bold: true, color: C.blue });
text(s, "length of input Sequence", 44, 479, 183, 18,
  { align: "center", fontSize: 14, italic: true, color: C.blue });

// ---- flowchart chips helper ---------------------------------------------------
function chip(x, y, w, h, fill, border, label, fs) {
  s.addShape(pres.ShapeType.rect, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    fill: { color: fill }, line: { color: border, width: 1 },
  });
  text(s, label, x, y - 1, w, h + 2,
    { align: "center", fontSize: fs, bold: true, color: C.black, valign: "middle" });
}
function thickArrow(x1, x2, y) {
  s.addShape(pres.ShapeType.line, {
    x: x1 * PX, y: y * PX, w: (x2 - x1) * PX, h: 0,
    line: { color: C.red, width: 3.5, endArrowType: "triangle" },
  });
}

// ---- FC1: unscaled SoftMax flowchart (black border, panel-gray interior) ------
s.addShape(pres.ShapeType.rect, {
  x: 286 * PX, y: 379 * PX, w: 217 * PX, h: 145 * PX,
  fill: { type: "none" }, line: { color: "1A1A1A", width: 1.75 },
});
delim(s, "d_fc1L_l.png", 301, 408); delim(s, "d_fc1L_r.png", 335, 408);
var inVals = ["10", "20", "30", "40"];
for (i = 0; i < 4; i++) chip(306, 395.5 + i * 30.6, 30, 21, C.chipIn, C.red, inVals[i], 11);
text(s, "SoftMax", 347, 427, 65, 18,
  { align: "center", fontSize: 13, bold: true, color: C.maroon, valign: "middle" });
thickArrow(350, 419, 457);
delim(s, "d_fc1R_l.png", 422, 383); delim(s, "d_fc1R_r.png", 478, 383);
var outVals = ["0.0000", "0.0000", "0.0000", "1.0000"];
for (i = 0; i < 4; i++) chip(427, 395.5 + i * 30.6, 51, 21, C.chipOut, C.indigo, outVals[i], 11);

// ---- FC2: scaled SoftMax flowchart (purple border, orchid fill) ----------------
s.addShape(pres.ShapeType.rect, {
  x: 512 * PX, y: 378 * PX, w: 388 * PX, h: 146 * PX,
  fill: { color: C.fc2Fill }, line: { color: C.purple, width: 1.75 },
});
delim(s, "d_fc2a_l.png", 520, 382); delim(s, "d_fc2a_r.png", 558, 382);
for (i = 0; i < 4; i++) chip(526, 395.5 + i * 30.6, 26, 21, C.chipIn, C.red, inVals[i], 11);
text(s, "/", 562, 429, 18, 28,
  { align: "center", fontSize: 22, bold: true, color: C.maroon, valign: "middle" });
delim(s, "d_fc2b_l.png", 586, 382); delim(s, "d_fc2b_r.png", 624, 382);
eqImage(s, "eq_sqrtd_fc2", 593, 448);
text(s, "Scaled", 632, 430, 56, 20,
  { align: "center", fontSize: 15, bold: true, color: C.maroon, valign: "middle" });
thickArrow(640, 705, 458);
delim(s, "d_fc2c_l.png", 712, 390); delim(s, "d_fc2c_r.png", 750, 390);
var midVals = ["1", "2", "3", "4"];
for (i = 0; i < 4; i++) chip(717, 395.5 + i * 30.6, 25, 21, C.chipIn, C.red, midVals[i], 11);
text(s, "SoftMax", 754, 432, 72, 20,
  { align: "center", fontSize: 15, bold: true, color: C.maroon, valign: "middle" });
thickArrow(764, 826, 458);
delim(s, "d_fc2d_l.png", 832, 383); delim(s, "d_fc2d_r.png", 891, 383);
var out2Vals = ["0.0321", "0.0871", "0.2369", "0.6439"];
for (i = 0; i < 4; i++) chip(837, 395.5 + i * 30.6, 51, 21, C.chipOut, C.indigo, out2Vals[i], 11);

pres.writeFile({ fileName: "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_036_recreated.pptx" })
  .then(function () { console.log("wrote slide_036_recreated.pptx"); });
