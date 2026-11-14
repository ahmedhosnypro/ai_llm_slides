const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// Slide 005 — FRESH rebuild from qa/reanalysis2/slide_005_analysis.txt ONLY.
// Spec: SLIDE_TITLE none; x^T A x 3-variable quadratic form, coefficient
// definitions, bottom matrix -> coefficient-grid diagram. House chrome mandatory.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_005.js

const NUM = 5;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx", "build", "eq_005");
const MAN = JSON.parse(fs.readFileSync(path.join(EQ, "w7_manifest.json"), "utf8"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (overrides spec) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
// House title box (spec SLIDE_TITLE: none — box kept, no text added).
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Place a rendered mathtext PNG centered in its spec box, at exact size w = px/600.
function img(name) {
  const m = MAN[name];
  s.addImage({
    path: path.join(EQ, m.image),
    x: m.x + (m.w - m.w_in) / 2,
    y: m.y + (m.h - m.h_in) / 2,
    w: m.w_in,
    h: m.h_in,
  });
}

// ---- internal content panels from the original ----
for (const p of [[0.065, 0.437, 0.796, 0.735], [0.065, 0.748, 0.796, 0.975]]) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: p[0] * W, y: p[1] * H, w: (p[2] - p[0]) * W, h: (p[3] - p[1]) * H,
    fill: { type: "none" }, line: { color: "C00000", width: 1 },
  });
}
// ---- R2 top equation block (spec sections 2/8: E1, E2, E3) ----
["w7_e1", "w7_e2", "w7_e3"].forEach(img);

// ---- R3 coefficient-definition list (six implication lines) ----
["w7_d1", "w7_d2", "w7_d3", "w7_d4", "w7_d5", "w7_d6"].forEach(img);

// ---- R4 right annotation "Three Variables Example" (italic, right-aligned) ----
s.addText("Three Variables Example", {
  x: 0.803 * W, y: 0.452 * H, w: (0.928 - 0.803) * W, h: (0.532 - 0.452) * H,
  align: "right", valign: "middle",
  fontSize: 13, bold: true, underline: true, color: "C00000", fontFace: FONT, margin: 0,
});
// ---- R5 bottom diagram ----
// straight delimiter bars around both bottom matrices
for (const x of [0.075, 0.225, 0.380, 0.800]) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: x * W, y: 0.810 * H, w: 0.018, h: (0.965 - 0.810) * H,
    fill: { color: "000000" }, line: { type: "none" },
  });
}
// cell highlights behind the matrix ink: blue around a_11, red around a_12 and a_32
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.118 * W, y: 0.825 * H, w: (0.158 - 0.118) * W, h: (0.875 - 0.825) * H,
  fill: { type: "none" }, line: { color: "4472C4", width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.158 * W, y: 0.825 * H, w: (0.198 - 0.158) * W, h: (0.875 - 0.825) * H,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.158 * W, y: 0.925 * H, w: (0.198 - 0.158) * W, h: (0.970 - 0.925) * H,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
// left matrix header + rows
["w7_hdr", "w7_m1", "w7_m2", "w7_m3"].forEach(img);
// single blue implication arrow between left matrix and right coefficient grid
s.addText("⇒", {
  x: 0.315 * W, y: 0.845 * H, w: (0.420 - 0.315) * W, h: (0.915 - 0.845) * H,
  align: "center", valign: "middle", fontSize: 28, bold: true,
  color: "000000", fontFace: FONT, margin: 0,
});
// right 3x3 coefficient grid: only three highlighted cells (yellow/blue/red), then labels
const COLS = [[0.390, 0.500], [0.500, 0.630], [0.630, 0.790]];
const ROWS = [[0.815, 0.845], [0.875, 0.905], [0.935, 0.965]];
for (const [r, c, col] of [[0, 0, "FFE699"], [0, 1, "4472C4"], [2, 1, "C00000"]]) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: COLS[c][0] * W, y: ROWS[r][0] * H,
    w: (COLS[c][1] - COLS[c][0]) * W, h: (ROWS[r][1] - ROWS[r][0]) * H,
    fill: { type: "none" }, line: { color: col, width: 1.5 },
  });
}
["w7_b1", "w7_b2", "w7_b3", "w7_b4", "w7_b5", "w7_b6", "w7_b7", "w7_b8", "w7_b9"].forEach(img);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx", "slide_005_recreated.pptx") });
