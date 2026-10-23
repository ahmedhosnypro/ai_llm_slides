// Build slide 046 — "Perceptron Algorithm: Iteration 4 — Stop Iterations"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Spec: analysis/slide_046_final.json + slide_046_raw.json
// Frame: unique_slides/slide_046.jpg (960x540, 1px = 1pt = 1/72 in) — PIL measured.
//
// MEASURED GEOMETRY (frame px):
//   Top data matrix (gray E9E9E7 panel, no border):
//     header rule y 54..56 (x 68..539); caption band y 110..125 (x 68..~510)
//     subscript header row y 166..175 (x 89..236)
//     class-label row  y 232..243 (x 94..219): C1 C1 C1 C2 C2 C2
//     data rows y 184..199 (1 2 1 5 6 4), y 199..213 (1 1 2 4 5 6), y 214..224 (1 1 1 4 5 6)
//     top rule of matrix area: dashed line y 140 (x 70..246)
//   Upper-mid (top-right of matrix):
//     "Initial W = (4, -2, -2)^T"     x 336..468, y 66..80     (black, ~16pt)
//     "Step η = 2"                    x 336..435, y 90..101     (red bold 13pt)
//     "Check Classes of"             x 336..~480, y 113..124   (black 12pt)
//     Z-matrix (Z1 Z1 Z1 / 0 0 7 / 0 6 2)  x 336..500, y 143..176, header red italic
//   Final-weight yellow box: x 744..828, y 58..107 (fill FFFF99, 1pt black border),
//     holds eq_046_final_w.png = W = (14,-4,0)^T
//   Title rule: y 128..130 (x 68..539)
//   Middle-left "Ugmented Vectors (From Top)" header: x 68..~234, y 255..~268
//     augmented matrix: subscripts x 89..236 y 284..292, rows y 298..312, labels y 313..~322
//   "Iteration 4" red-outlined box: x 83..217, y 278..305
//   "Stop Iterations" pink box: x 63..244, y 330..416
//   Scatter plot: plot_046_scatter.png at x=312, y=173, w=514, h=310 (native px/72)
//
// LAWS: hex without '#', fontFace explicit, margin 0, single-line text boxes with
// pinned lineSpacing, native px/72 image placement, closed-loop render check first.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const px = (v) => v / 72; // frame px -> inches
const A = "Arial";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_046_recreated.pptx";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome: white canvas, gray panel, red L/R/bottom strokes, badge "46" ----
drawHouseChrome(pptx, slide, { numeral: 46 });

// ===========================================================================
// TOP DATA MATRIX  (x1..x6 header + three data rows + C1/C2 labels)
// ===========================================================================
// Top rule (thin black bar) at y 54..56 spanning x 68..539
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(539 - 68), h: px(3),
  fill: { color: "000000" }, line: { type: "none" },
});
// Dashed separator line at y 140 (x 70..246) — table header underline
slide.addShape(pptx.ShapeType.line, {
  x: px(70), y: px(140), w: px(246 - 70), h: 0,
  line: { color: "000000", width: 0.75, dashType: "dash" },
});
// Second rule at y 128..130 (x 68..539) — under the upper-mid block
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(128), w: px(539 - 68), h: px(3),
  fill: { color: "000000" }, line: { type: "none" },
});

// Header: x1 x2 x3 x4 x5 x6 (subscript row), y 166..175
const headerX = [89, 111, 133, 156, 178, 201];
const headerBase = ["x", "x", "x", "x", "x", "x"];
const headerSub = ["1", "2", "3", "4", "5", "6"];
for (let i = 0; i < 6; i++) {
  slide.addText(
    [
      { text: headerBase[i], options: { fontFace: A, fontSize: 12, italic: true, color: "000000" } },
      { text: headerSub[i], options: { fontFace: A, fontSize: 8, color: "000000", subscript: true } },
    ],
    {
      x: px(headerX[i] - 12), y: px(165), w: px(26), h: px(12),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, lineSpacing: 12,
    }
  );
}

// Three data rows: row1 y 184..199, row2 y 199..213, row3 y 214..224
const dataRows = [
  { y: 182, vals: ["1", "2", "1", "5", "6", "4"] },
  { y: 197, vals: ["1", "1", "2", "4", "5", "6"] },
  { y: 212, vals: ["1", "1", "1", "4", "5", "6"] },
];
for (const row of dataRows) {
  for (let i = 0; i < 6; i++) {
    slide.addText(row.vals[i], {
      x: px(headerX[i] - 12), y: px(row.y), w: px(26), h: px(16),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 11, color: "000000", lineSpacing: 14,
    });
  }
}

// Class-label row y 232..243: C1 C1 C1 C2 C2 C2 (C1 blue, C2 red)
const classLabels = ["C1", "C1", "C1", "C2", "C2", "C2"];
for (let i = 0; i < 6; i++) {
  slide.addText(classLabels[i], {
    x: px(headerX[i] - 12), y: px(231), w: px(26), h: px(13),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 10, bold: true,
    color: classLabels[i] === "C1" ? "0000FF" : "FF0000", lineSpacing: 12,
  });
}

// ---- upper-mid text block (x 336..~500, y 60..135) ----
// "Initial W = (4, -2, -2)^T" y 66..80 — the W-vector is the certified eq PNG
const eqInit = JSON.parse(
  require("fs").readFileSync(__dirname + "/assets/eq_046_initial_w.json", "utf8")
);
slide.addText("Initial", {
  x: px(336), y: px(64), w: px(100), h: px(17),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 13, color: "000000", lineSpacing: 16,
});
slide.addImage({
  path: __dirname + "/assets/eq_046_initial_w.png",
  x: px(336), y: px(64), w: eqInit.w_in, h: eqInit.h_in,
});
// "Step η = 2" red bold, y 90..101
slide.addText("Step", {
  x: px(336), y: px(89), w: px(30), h: px(13),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 12, bold: true, color: "FF0000", lineSpacing: 13,
});
slide.addImage({
  path: __dirname + "/assets/eq_046_step_eta.png",
  x: px(365), y: px(88), w: 0.352, h: 0.16,
});
// "Check Classes of" y 113..124
slide.addText("Check Classes of", {
  x: px(336), y: px(113), w: px(165), h: px(13),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 12, color: "000000", lineSpacing: 13,
});

// ===========================================================================
// Z MATRIX  (x 336..500, y 143..176): Z1 Z1 Z1 / 0 0 7 / 0 6 2
// ===========================================================================
const zHeadX = [342, 372, 402];
const zHeadY = 143;
for (let i = 0; i < 3; i++) {
  slide.addText(
    [
      { text: "Z", options: { fontFace: A, fontSize: 11, italic: true, color: "FF0000" } },
      { text: "1", options: { fontFace: A, fontSize: 8, color: "FF0000", subscript: true } },
    ],
    {
      x: px(zHeadX[i]), y: px(zHeadY), w: px(20), h: px(13),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, lineSpacing: 12,
    }
  );
}
const zRows = [
  { y: 157, vals: ["0", "0", "7"] },
  { y: 168, vals: ["0", "6", "2"] },
];
for (const row of zRows) {
  for (let i = 0; i < 3; i++) {
    slide.addText(row.vals[i], {
      x: px(zHeadX[i]), y: px(row.y), w: px(20), h: px(14),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 11, color: "000000", lineSpacing: 13,
    });
  }
}

// ===========================================================================
// FINAL-WEIGHT YELLOW BOX (x 744..828, y 58..107)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(744), y: px(58), w: px(828 - 744), h: px(107 - 58),
  fill: { color: "FFFF99" }, line: { color: "000000", width: 1 },
});
const eqFinal = JSON.parse(
  require("fs").readFileSync(__dirname + "/assets/eq_046_final_w.json", "utf8")
);
slide.addImage({
  path: __dirname + "/assets/eq_046_final_w.png",
  x: px(744 + (828 - 744) / 2) - eqFinal.w_in / 2,
  y: px(58 + (107 - 58) / 2) - eqFinal.h_in / 2,
  w: eqFinal.w_in, h: eqFinal.h_in,
});

// ===========================================================================
// AUGMENTED VECTORS BLOCK (middle-left, x 68..~240, y 255..325)
// ===========================================================================
slide.addText("Ugmented Vectors (From Top)", {
  x: px(68), y: px(255), w: px(172), h: px(15),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 12, bold: true, color: "000000", lineSpacing: 14,
});
// Header subscripts y 284..292
for (let i = 0; i < 6; i++) {
  slide.addText(
    [
      { text: "x", options: { fontFace: A, fontSize: 11, italic: true, color: "000000" } },
      { text: String(i + 1), options: { fontFace: A, fontSize: 8, color: "000000", subscript: true } },
    ],
    {
      x: px(headerX[i] - 12), y: px(283), w: px(26), h: px(11),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, lineSpacing: 11,
    }
  );
}
// Augmented rows: all-1s, then 1 2 1 5 6 4, then 1 1 2 4 5 6
const augRows = [
  { y: 296, vals: ["1", "1", "1", "1", "1", "1"] },
  { y: 307, vals: ["1", "2", "1", "5", "6", "4"] },
  { y: 318, vals: ["1", "1", "2", "4", "5", "6"] },
];
for (const row of augRows) {
  for (let i = 0; i < 6; i++) {
    slide.addText(row.vals[i], {
      x: px(headerX[i] - 12), y: px(row.y), w: px(26), h: px(12),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 10, color: "000000", lineSpacing: 11,
    });
  }
}

// ===========================================================================
// "ITERATION 4" red-outlined box (x 83..217, y 278..305)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(83), y: px(278), w: px(217 - 83), h: px(305 - 278),
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1 },
});
slide.addText("Iteration 4", {
  x: px(83), y: px(278), w: px(217 - 83), h: px(305 - 278),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 16, bold: true, color: "FF0000", lineSpacing: 18,
});

// ===========================================================================
// "STOP ITERATIONS" pink box (x 63..244, y 330..416)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(63), y: px(330), w: px(244 - 63), h: px(416 - 330),
  fill: { color: "FFC0CB" }, line: { color: "000000", width: 1 },
});
// black "No change in W" with W underlined, y ~350..367
slide.addText(
  [
    { text: "No change in ", options: { fontFace: A, fontSize: 15, color: "000000" } },
    { text: "W", options: { fontFace: A, fontSize: 15, color: "000000", underline: true } },
  ],
  {
    x: px(63), y: px(350), w: px(244 - 63), h: px(20),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, lineSpacing: 18,
  }
);
// red bold "Stop Iterations" y ~375..395
slide.addText("Stop Iterations", {
  x: px(63), y: px(375), w: px(244 - 63), h: px(20),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 18, bold: true, color: "FF0000", lineSpacing: 20,
});

// ===========================================================================
// SCATTER PLOT — plot_046_scatter.png at native px/72 (NO rescale)
// ===========================================================================
slide.addImage({
  path: __dirname + "/assets/plot_046_scatter.png",
  x: px(312), y: px(173), w: px(514), h: px(310),
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
