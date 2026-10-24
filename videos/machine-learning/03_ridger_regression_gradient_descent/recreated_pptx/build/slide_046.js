// Build slide 046 — "Perceptron Algorithm: Iteration 4 — Stop Iterations"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Spec: analysis/slide_046_final.json + slide_046_raw.json
// Frame: unique_slides/slide_046.jpg (960x540, 1px = 1pt = 1/72 in) — PIL measured.
//
// MEASURED GEOMETRY (frame px, from unique_slides/slide_046.jpg):
//   Rules (black 3px bars): y 55..56 and y 128..130, both spanning x 68..719
//   Left border: NAVY/indigo stroke at x~69, y 55..130 (family 221777)
//   Top-left block, 6 columns at measured centres:
//     subscript header  y 64..73  x [94.5 116.5 138.5 160.5 183.5 206.5]  "x1 x2 x3 x4 x5 x6"
//     data row 1        y 80..89  x [96.5 118.5 140.5 163.5 186 208.5]     "1 2 1 5 6 4"
//     data row 2        y 96..105 x [97 118 140.5 163 186.5 208.5]         "1 1 2 4 5 6"
//     class labels      y 111..124 x [94 116.5 138.5 161 183.5 206.5]      "C1 C1 C1 C2 C2 C2"
//     caption           ink x 251..508 y 110..124, "Zero" green 008000 (12pt Arial)
//   Upper-mid block: "Initial" + red W-vector equation ink x 366..434 y 67..79;
//     black bracket vertical x 330.5 y 62..103; red vertical x 433.5 y 67..79;
//     "Step" BLACK x 331..353 y 89..104 (red applies only to eta = 2);
//     "eta = 2" RED ink x 402..408 y 71..79 (mathtext PNG);
//     "Check Classes of Z" x 320..508 y 110..124 (12pt)
//   Z matrix — PRESENT at x 597..657 y 60..111:
//     header "Z1 Z1 Z1" on centres [605 628 651], cap-top y 64, 12pt black;
//     two digit rows: "0 0 7" cap-top y 83, "0 6 2" cap-top y 99;
//     three tall parenthesis pairs as 1.5pt verticals at x 598/611, 621/634,
//     643/656, each spanning y 80..110.
//   NOT present: "Ugmented Vectors (From Top)" — PIL scan returns zero ink.
//   Yellow final-weight box: x 738..828, y 59..142, 1pt black border, pale-yellow fill;
//     underlined W (14pt bold italic), "=", two tall paren verticals x 786 / x 823
//     spanning y 60..139; column vector digits centre x ~805, rows 14 / -4 / 0 (13pt).
//   Augmented-vectors box — CLOSED box: left x 69..70, right x 245..246,
//     spanning y 140..249; dashed separator y 140 (x 70..246); subscript header
//     x1..x6 y 166..175; rows y 184..192 / 199..207 / 214..222;
//     class row y 232..240; solid 1px rule at y 255 spanning x 70..246.
//   "Iteration 4": SOLID RED FILL x 84..212 y 277..304, white bold 20pt text.
//   "Stop Iterations": pink box x 64..245 y 331..415 (FFC0CB), black "No change in W"
//     (W underlined) y 349..371, RED bold 17pt "Stop Iterations" y 374..396.
//   Scatter plot: plot_046_scatter.png at x=312, y=173, w=514, h=310 (native px/72)
//
// HEX never carries '#'; fontFace explicit; margin 0; single-line boxes with a
// pinned lineSpacing (LO/PowerPoint auto-pitch divergence law); images at native
// px/600 so eq glyphs are exactly fontsize pt on the slide.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");
const fs = require("fs");

const px = (v) => v / 72; // frame px -> inches
const A = "Arial";
const OUT = "recreated_pptx/slide_046_recreated.pptx";
const EQ = (n) => JSON.parse(fs.readFileSync(__dirname + "/assets/" + n + ".json", "utf8"));

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome: white canvas, gray panel, red L/R/bottom strokes, badge "46" ----
drawHouseChrome(pptx, slide, { numeral: 46 });

// ---- helpers ---------------------------------------------------------------
function AB(base, x, y, size, subSize) {          // italic base + subscript digit
  slide.addText(
    [
      { text: base, options: { fontFace: A, fontSize: size, italic: true, color: "000000" } },
      { text: "1", options: { fontFace: A, fontSize: subSize, color: "0000FF", subscript: true } },
    ],
    { x: px(x), y: px(y), w: px(18), h: px(11),
      align: "left", valign: "middle", margin: 0, lineSpacing: 11 }
  );
}
function NUM(v, x, y, size) {                      // black digit, centred on x
  slide.addText(String(v), {
    x: px(x - 6), y: px(y), w: px(12), h: px(11),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: size, color: "000000",
  });
}
function CL(sub, x, y) {                           // class label C1/C2, coloured
  const col = sub === "1" ? "0000FF" : "FF0000";
  slide.addText(
    [
      { text: "C", options: { fontFace: A, fontSize: 10, bold: true, color: col } },
      { text: sub, options: { fontFace: A, fontSize: 7.5, bold: true, color: col, subscript: true } },
    ],
    { x: px(x - 9), y: px(y), w: px(18), h: px(11),
      align: "center", valign: "middle", margin: 0, lineSpacing: 11 }
  );
}

// ===========================================================================
// TOP-LEFT BLOCK (x 68..719, y 54..130)
// ===========================================================================
for (const ry of [54, 128]) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(68), y: px(ry), w: px(719 - 68), h: px(3),
    fill: { color: "000000" }, line: { type: "none" },
  });
}
// left border of the top table: original x=69 is a NAVY/indigo stroke (34,24,97)
slide.addShape(pptx.ShapeType.rect, {
  x: px(69), y: px(55), w: px(1.5), h: px(130 - 55),
  fill: { color: "221777" }, line: { type: "none" },
});
const TOP_H = [94.5, 116.5, 138.5, 160.5, 183.5, 206.5];
TOP_H.forEach((x) => AB("x", x - 6, 64, 8, 6));
[96.5, 118.5, 140.5, 163.5, 186, 208.5].forEach((x, i) => NUM([1, 2, 1, 5, 6, 4][i], x, 80, 13));
[97, 118, 140.5, 163, 186.5, 208.5].forEach((x, i) => NUM([1, 1, 2, 4, 5, 6][i], x, 96, 13));
[94, 116.5, 138.5, 161, 183.5, 206.5].forEach((x, i) => CL(["1", "1", "1", "2", "2", "2"][i], x, 111));

// caption: "C1 positive   C2 negative   Zero is unaccepted" (ink x 251..508, y 110..124)
const CAP = [
  { t: "C1", c: "0000FF", b: true }, { t: " positive   ", c: "000000", b: false },
  { t: "C2", c: "FF0000", b: true }, { t: " negative   ", c: "000000", b: false },
  { t: "Zero", c: "008000", b: true }, { t: " is unaccepted", c: "000000", b: false },
];
slide.addText(
  CAP.map((w) => ({ text: w.t, options: { fontFace: A, fontSize: 12, color: w.c, bold: w.b } })),
  { x: px(253), y: px(109), w: px(260), h: px(17),
    align: "left", valign: "middle", margin: 0, lineSpacing: 14 }
);

// ===========================================================================
// UPPER-MID BLOCK (x 330..545): Initial W, Step eta = 2, Check Classes of Z
// ===========================================================================
slide.addText("Initial", {
  x: px(336), y: px(62), w: px(46), h: px(12),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 10, color: "000000", lineSpacing: 12,
});
// black bracket vertical at x 330.5 spanning y 62..103
slide.addShape(pptx.ShapeType.rect, {
  x: px(330.5), y: px(62), w: px(1.5), h: px(103 - 62),
  fill: { color: "000000" }, line: { type: "none" },
});
// red vertical at x 433.5 spanning y 67..79
slide.addShape(pptx.ShapeType.rect, {
  x: px(433.5), y: px(67), w: px(1.5), h: px(79 - 67),
  fill: { color: "FF0000" }, line: { type: "none" },
});
const eInit = EQ("eq_046_initial_w");
slide.addImage({ path: __dirname + "/assets/eq_046_initial_w.png", x: px(366), y: px(67), w: eInit.w_in, h: eInit.h_in });

slide.addText("Step", {
  x: px(331), y: px(89), w: px(28), h: px(16),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 10, bold: true, color: "000000", lineSpacing: 12,
});
slide.addImage({ path: __dirname + "/assets/eq_046_step_eta.png", x: px(402), y: px(70), w: 0.352, h: 0.16 });

slide.addText("Check Classes of Z", {
  x: px(320), y: px(110), w: px(190), h: px(15),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 12, color: "000000", lineSpacing: 14,
});
// Z matrix (x 597..657, y 60..111): Z1 Z1 Z1 header, rows "0 0 7" and "0 6 2",
// with three tall parenthesis pairs as 1.5pt verticals spanning y 80..110.
const ZX = [605, 628, 651];
ZX.forEach((x, i) => {
  slide.addText(
    [
      { text: "Z", options: { fontFace: A, fontSize: 10, italic: true, color: "000000" } },
      { text: String(i + 1), options: { fontFace: A, fontSize: 7.5, color: "000000", subscript: true } },
    ],
    { x: px(x - 6), y: px(64), w: px(16), h: px(11),
      align: "left", valign: "middle", margin: 0, lineSpacing: 11 }
  );
});
["0", "0", "7"].forEach((v, i) => NUM(v, ZX[i], 83, 12));
["0", "6", "2"].forEach((v, i) => NUM(v, ZX[i], 99, 12));
for (const [lft, rgt] of [[598, 611], [621, 634], [643, 656]]) {
  for (const bx of [lft, rgt]) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(bx), y: px(80), w: px(1.5), h: px(110 - 80),
      fill: { color: "000000" }, line: { type: "none" },
    });
  }
}

// ===========================================================================
// YELLOW FINAL-WEIGHT BOX (x 738..828, y 59..142)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(738), y: px(59), w: px(828 - 738), h: px(142 - 59),
  fill: { color: "FDFD96" }, line: { color: "000000", width: 1 },
});
slide.addText("W", {
  x: px(742), y: px(89), w: px(38), h: px(19),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 14, bold: true, italic: true, color: "000000",
  underline: true, lineSpacing: 16,
});
slide.addText("=", {
  x: px(766), y: px(94), w: px(10), h: px(9),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 12, color: "000000", lineSpacing: 12,
});
// two tall parenthesis verticals spanning y 60..139
for (const bx of [786, 823]) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(bx), y: px(60), w: px(1.5), h: px(139 - 60),
    fill: { color: "000000" }, line: { type: "none" },
  });
}
["14", "−4", "0"].forEach((v, i) => {
  slide.addText(v, {
    x: px(792), y: px([74, 99, 126][i]), w: px(26), h: px(17),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 13, color: "000000", lineSpacing: 16,
  });
});

// ===========================================================================
// AUGMENTED-VECTORS BOX (CLOSED): left x 69..70, right x 245..246, y 140..249
// ===========================================================================
for (const bx of [69, 245]) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(bx), y: px(140), w: px(1.5), h: px(249 - 140),
    fill: { color: "000000" }, line: { type: "none" },
  });
}
slide.addShape(pptx.ShapeType.line, {
  x: px(70), y: px(140), w: px(176), h: 0,
  line: { color: "000000", width: 0.75, dashType: "dash" },
});
// subscript header y 166..175
const LO_H = [97.5, 119.5, 142.5, 164.5, 187.5, 210.5];
LO_H.forEach((x) => AB("x", x - 6, 166, 8, 6));
// three data rows
const LO_R = [100, 121.5, 144, 166.5, 189.5, 212];
const LO_V = [[1, 2, 1, 5, 6, 4], [1, 1, 2, 4, 5, 6], [1, 1, 1, 4, 5, 6]];
LO_V.forEach((vals, r) => {
  vals.forEach((v, i) => NUM(v, LO_R[i], 184 + r * 15, 11));
});
// class labels y 232..240
[97.5, 120, 142, 165, 187.5, 210].forEach((x, i) =>
  CL(["1", "1", "1", "2", "2", "2"][i], x, 232)
);
// solid 1px rule at y 255 spanning x 70..246
slide.addShape(pptx.ShapeType.line, {
  x: px(70), y: px(255), w: px(176), h: 0,
  line: { color: "000000", width: 0.75 },
});

// ===========================================================================
// "ITERATION 4" solid red fill, white bold text (PIL census: interior C00000-family)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(84), y: px(277), w: px(212 - 84), h: px(304 - 277),
  fill: { color: "C00000" }, line: { type: "none" },
});
slide.addText("Iteration 4", {
  x: px(84), y: px(277), w: px(212 - 84), h: px(304 - 277),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 20, bold: true, color: "FFFFFF", lineSpacing: 22,
});

// ===========================================================================
// "STOP ITERATIONS" pink box (x 64..245, y 331..415)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(64), y: px(331), w: px(245 - 64), h: px(415 - 331),
  fill: { color: "FFC0CB" }, line: { color: "000000", width: 1 },
});
slide.addText(
  [
    { text: "No change in ", options: { fontFace: A, fontSize: 15, color: "000000" } },
    { text: "W", options: { fontFace: A, fontSize: 15, color: "000000", underline: true } },
  ],
  { x: px(64), y: px(349), w: px(245 - 64), h: px(22),
    align: "center", valign: "middle", margin: 0, lineSpacing: 18 }
);
slide.addText("Stop Iterations", {
  x: px(64), y: px(374), w: px(245 - 64), h: px(22),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 17, bold: true, color: "FF0000", lineSpacing: 20,
});

// ===========================================================================
// SCATTER PLOT — plot_046_scatter.png at native px/72 (NO rescale)
// ===========================================================================
slide.addImage({
  path: __dirname + "/assets/plot_046_scatter.png",
  x: px(312), y: px(173), w: px(514), h: px(310),
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));

