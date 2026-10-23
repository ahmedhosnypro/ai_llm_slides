// Slide 049 — machine-learning lecture 03 (03_ridger_regression_gradient_descent)
// "Iteration 2" — built from measured frame unique_slides/slide_049.jpg (960x540, 1px=1pt).
//
// MEASURED GEOMETRY (frame px), banked from PIL measurement 2026-10-23:
//   chrome            : panel x54..903 y45..540, C00000 strokes L58.5 R901 B538.5, badge (876,73) d35
//   top blue box      : x68..719 y54..130, thin blue-violet border, white interior
//   top data table    : 6 numeric cols x89..215 (pitch 22), "Initial" col x239..253,
//                       4 rows y62..78 / 78..95 / 95..112 / 112..128
//   "Initial W =..."  : x258..424 (row-band y78..128)
//   REPEAT (red)      : x426..500 y58..76
//   "Check classes of": x542..612 y86..98 ; 3x3 grid x636..706 y66..118 (pitch 23/17)
//   legend            : x86..207 y144..160
//   "Ugmented Vectors": x82..214 y148..159  -> merged with the legend band (see note)
//   aug table         : x79..211 y162..230, 6 cols pitch 22, 5 rows
//   class labels      : C1 x88..134 / C2 x152..202, y230..244
//   RED BOX           : x84..214 y278..306, red fill + one white text line
//   "No change in W"  : x77..156 y350..370   (plain text on the panel)
//   red "=>"          : x84..122 y375..394
//   "Stop Iterations" : x76..205 y375..394
//   calc rows         : table x273..856, 6 rows of 66px: y142, 204, 268, 332, 396, 460
//                       (borders y202/268/332/396/460/524, light E3E9EA)
//                       per row: matrix x283..426, action x498..612, W-vector x696..746
// NOTE: the frame shows only ONE legend/title line in the left-middle band (y144..160);
// slide 048 (the sibling build) renders "Ugmented Vectors (from Top)" in that same band,
// so this build uses the frame's line verbatim and the legend text is carried by the
// Calc-row annotations.

const pptxgenpkg = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";  // 13.333 x 7.5 in
const s = pptx.addSlide();

drawHouseChrome(pptx, s, { numeral: "49" });

const FONT = "Arial";
const BLACK = "000000";
const RED = "FF0000";
const BLUE = "0000FF";
const TITLE_BLUE = "706AB4";   // measured blue-violet of the left-middle heading line
const BOX_BLUE = "9A94D4";     // measured blue-violet border of the top blue box
const CALC_LINE = "E3E9EA";    // measured light blue-grey rule between calc rows
const WHITE = "FFFFFF";

// frame px -> inches (absolute frame coordinates: 960x540 == 13.333x7.5 in)
function fx(px) { return px / 72; }
function fy(px) { return px / 72; }
function fw(px) { return px / 72; }
function fh(px) { return px / 72; }

function cell(text, o) {
  return { text: text, options: Object.assign({
    fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle", margin: 0,
  }, o || {}) };
}

// ---------------- 1. TOP BLUE BOX ----------------
s.addShape(pptx.ShapeType.rect, {
  x: fx(68), y: fy(54), w: fw(719 - 68), h: fh(130 - 54),
  fill: { color: WHITE }, line: { color: BOX_BLUE, width: 1 },
});

// ---------------- 2. TOP DATA TABLE (x1..x6 + Initial) ----------------
const tbl_x = fx(86), tbl_y = fy(62), tbl_w = fw(253 - 86);
const tbl_rowH = fh(16.5);
const tbl_rows = [
  [cell("x1", { fontSize: 12 }), cell("x2", { fontSize: 12 }), cell("x3", { fontSize: 12 }),
   cell("x4", { fontSize: 12 }), cell("x5", { fontSize: 12 }), cell("x6", { fontSize: 12 }),
   cell("Initial", { fontSize: 11 })],
  [cell("1"), cell("2"), cell("1"), cell("5"), cell("6"), cell("6"), cell(" ")],
  [cell("1"), cell("1"), cell("2"), cell("4"), cell("5"), cell("6"), cell(" ")],
  [cell("1"), cell("1"), cell("2"), cell("4"), cell("5"), cell("6"), cell(" ")],
];
s.addTable(tbl_rows, {
  x: tbl_x, y: tbl_y, w: tbl_w,
  colW: [fw(21.2), fw(21.2), fw(21.2), fw(21.2), fw(21.2), fw(21.2), fw(40)],
  rowH: tbl_rowH, fontFace: FONT, margin: 0, border: { type: "none" },
});

// "Initial W = [4, -2]" (row band y78..128, measured ink x258..424)
s.addText([
  { text: "Initial ", options: { color: BLACK } },
  { text: "W", options: { color: BLACK, italic: true } },
  { text: " = [4, -2]", options: { color: BLACK } },
], {
  x: fx(257), y: fy(79), w: fw(168), h: fh(18),
  fontFace: FONT, fontSize: 10, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// ---------------- 3. REPEAT instruction (red) ----------------
s.addText("REPEAT using Step \u03b7 = 1", {
  x: fx(426), y: fy(58), w: fw(80), h: fh(18),
  fontFace: FONT, fontSize: 10, color: RED, bold: true,
  align: "left", valign: "middle", margin: 0,
});

// ---------------- 4. "Check classes of" + 3x3 grid ----------------
s.addText("Check classes of", {
  x: fx(538), y: fy(86), w: fw(76), h: fh(13),
  fontFace: FONT, fontSize: 10, color: BLACK, align: "left", valign: "middle", margin: 0,
});

const grid_x = fx(636), grid_y = fy(66);
const grid_rows = [
  [cell("Z1", { fontSize: 11 }), cell("Z1", { fontSize: 11 }), cell("Z1", { fontSize: 11 })],
  [cell("(0)"), cell("(7)"), cell("(3)")],
  [cell("(0)"), cell("(6)"), cell("(2)")],
];
s.addTable(grid_rows, {
  x: grid_x, y: grid_y, w: fw(70), colW: [fw(23.3), fw(23.3), fw(23.4)],
  rowH: fh(17), fontFace: FONT, margin: 0, border: { type: "none" },
});

// ---------------- 5. legend line (measured x86..207, y144..160) ----------------
s.addText("C1 positive C2 negative Zero is unaccepted", {
  x: fx(86), y: fy(144), w: fw(125), h: fh(16),
  fontFace: FONT, fontSize: 9, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// ---------------- 6. Ugmented Vectors title + table ----------------
s.addText("Ugmented Vectors (from Top)", {
  x: fx(80), y: fy(146), w: fw(140), h: fh(15),
  fontFace: FONT, fontSize: 10, color: TITLE_BLUE, align: "left", valign: "middle", margin: 0,
});

const aug_x = fx(79), aug_y = fy(162);
const aug_rows = [
  [cell("x1", { fontSize: 11 }), cell("x2", { fontSize: 11 }), cell("x3", { fontSize: 11 }),
   cell("x4", { fontSize: 11 }), cell("x5", { fontSize: 11 }), cell("x6", { fontSize: 11 })],
  [cell("1", { fontSize: 11 }), cell("1", { fontSize: 11 }), cell("1", { fontSize: 11 }),
   cell("1", { fontSize: 11 }), cell("1", { fontSize: 11 }), cell("1", { fontSize: 11 })],
  [cell("1", { fontSize: 11 }), cell("2", { fontSize: 11 }), cell("1", { fontSize: 11 }),
   cell("5", { fontSize: 11 }), cell("6", { fontSize: 11 }), cell("6", { fontSize: 11 })],
  [cell("1", { fontSize: 11 }), cell("1", { fontSize: 11 }), cell("2", { fontSize: 11 }),
   cell("4", { fontSize: 11 }), cell("5", { fontSize: 11 }), cell("6", { fontSize: 11 })],
  [cell("1", { fontSize: 11 }), cell("1", { fontSize: 11 }), cell("2", { fontSize: 11 }),
   cell("4", { fontSize: 11 }), cell("5", { fontSize: 11 }), cell("6", { fontSize: 11 })],
];
s.addTable(aug_rows, {
  x: aug_x, y: aug_y, w: fw(132), colW: [fw(22), fw(22), fw(22), fw(22), fw(22), fw(22)],
  rowH: fh(13.6), fontFace: FONT, margin: 0, border: { type: "none" },
});

// class labels beneath the table (measured x88..134 red / x152..202 blue)
const cls_y = fy(230), cls_h = fh(14);
[["C1", fx(87), RED], ["C1", fx(109), RED], ["C1", fx(131), RED],
 ["C2", fx(152), BLUE], ["C2", fx(174), BLUE], ["C2", fx(196), BLUE]].forEach(function (c) {
  s.addText(c[0], {
    x: c[1], y: cls_y, w: fw(20), h: cls_h,
    fontFace: FONT, fontSize: 11, color: c[2], bold: true, align: "center", valign: "middle", margin: 0,
  });
});

// ---------------- 7. RED BOX "Iteration 2" (x84..214, y278..306) ----------------
s.addShape(pptx.ShapeType.rect, {
  x: fx(84), y: fy(278), w: fw(130), h: fh(28),
  fill: { color: RED }, line: { color: RED, width: 1 },
});
s.addText("Iteration 2", {
  x: fx(84), y: fy(278), w: fw(130), h: fh(28),
  fontFace: FONT, fontSize: 13, color: WHITE, bold: true, align: "center", valign: "middle", margin: 0,
});

// ---------------- 8. "No change in W" / "Stop Iterations" ----------------
s.addText([
  { text: "No change in ", options: { color: BLACK } },
  { text: "W", options: { color: BLACK, italic: true } },
], {
  x: fx(77), y: fy(350), w: fw(130), h: fh(20),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "left", valign: "middle", margin: 0,
});
s.addText("\u21d2", {
  x: fx(82), y: fy(375), w: fw(42), h: fh(19),
  fontFace: FONT, fontSize: 13, color: RED, bold: true, align: "center", valign: "middle", margin: 0,
});
s.addText("Stop Iterations", {
  x: fx(74), y: fy(375), w: fw(134), h: fh(19),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle", margin: 0,
});

// ---------------- 9. SIX CALCULATION ROWS (table x273..856) ----------------
const CALC = [
  { y: 142, m: "[1, 1, 1, 5]", res: "[-1, 3]" },
  { y: 204, m: "[1, 2, 1, 5]", res: "[-1, 2]" },
  { y: 268, m: "[1, 1, 2, 5]", res: "[-1, 2]" },
  { y: 332, m: "[1, 5, 4, 5]", res: "[-1, -4]" },
  { y: 396, m: "[1, 6, 5, 5]", res: "[-1, -6]" },
  { y: 460, m: "[1, 6, 6, 5]", res: "[-1, -7]" },
];
CALC.forEach(function (r, i) {
  // horizontal rule above each row (measured y202/268/332/396/460/524)
  s.addShape(pptx.ShapeType.line, {
    x: fx(273), y: fy(r.y - 1.5), w: fw(856 - 273), h: 0,
    line: { color: CALC_LINE, width: 1 },
  });
  const boxY = fy(r.y), boxH = fh(66);

  // d(x_i) matrix: 2x2 bracketed block, centred in x283..426
  s.addText([
    { text: "[", options: { fontFace: FONT, fontSize: 16, color: BLACK } },
    { text: " " + r.m + " ", options: { fontFace: FONT, fontSize: 13, color: BLACK } },
    { text: "]", options: { fontFace: FONT, fontSize: 16, color: BLACK } },
  ], {
    x: fx(283), y: fy(r.y + 8), w: fw(143), h: fh(16),
    align: "center", valign: "middle", margin: 0,
  });
  s.addText([
    { text: "[", options: { fontFace: FONT, fontSize: 16, color: BLACK } },
    { text: " " + r.res, options: { fontFace: FONT, fontSize: 13, color: BLACK } },
    { text: "]", options: { fontFace: FONT, fontSize: 16, color: BLACK } },
  ], {
    x: fx(283), y: fy(r.y + 42), w: fw(143), h: fh(16),
    align: "center", valign: "middle", margin: 0,
  });

  // "=> Keep same Weight"
  s.addText("\u21d2 Keep same Weight", {
    x: fx(498), y: boxY, w: fw(122), h: boxH,
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });

  // W column vector 5 / -1 / -1  (measured x696..746)
  s.addText([
    { text: "5", options: { breakLine: true } },
    { text: "-1", options: { breakLine: true } },
    { text: "-1", options: {} },
  ], {
    x: fx(696), y: fy(r.y + 6), w: fw(50), h: fh(54),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle",
    lineSpacing: 16, margin: 0,
  });
});
// bottom rule of the last row
s.addShape(pptx.ShapeType.line, {
  x: fx(273), y: fy(524), w: fw(856 - 273), h: 0,
  line: { color: CALC_LINE, width: 1 },
});

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_049_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
