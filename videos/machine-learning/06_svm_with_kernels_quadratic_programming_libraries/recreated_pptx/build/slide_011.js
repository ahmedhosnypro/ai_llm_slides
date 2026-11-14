// slide_011.js — REBUILD WAVE 3, built only from qa/reanalysis2 + judge findings + doc-parse
// of unique_slides/slide_011.jpg. Run: NODE_PATH=$(npm root -g) node slide_011.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_011") + "/";
const NUM = 11;
const TITLE = "Training Vectors: SVM QP Formulation";
const FONT = "Arial";
const W = 13.33, H = 7.5;
const MAN = require(EQ + "manifest.json");
function img(name, x, y, maxw, maxh) {
  const m = MAN[name];
  const scale = Math.min(1, maxw / m.w_in, maxh / m.h_in);
  s.addImage({ path: EQ + name, x, y, w: m.w_in * scale, h: m.h_in * scale });
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome
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
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Top-left: Training Vectors box with all four vectors + labels
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.35, y: 0.95, w: 4.35, h: 1.9,
  fill: { color: "FBF7C8" }, line: { color: "BFBFBF", width: 1 },
});
s.addText("Training Vectors", {
  x: 0.5, y: 1.02, w: 4.0, h: 0.28,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
img("eq_vecs.png", 0.5, 1.32, 4.0, 1.45);

// Top-middle: Test Vectors box
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.85, y: 0.95, w: 2.7, h: 1.9,
  fill: { color: "FBF7C8" }, line: { color: "BFBFBF", width: 1 },
});
s.addText("Test Vectors", {
  x: 5.0, y: 1.02, w: 2.4, h: 0.28,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
img("eq_test.png", 5.15, 1.38, 2.2, 1.35);
// Top-right: "Use C=1" inside a red rectangular callout box
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.7, y: 0.95, w: 2.3, h: 0.5,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 2 },
});
s.addText("Use C=1", {
  x: 7.7, y: 0.95, w: 2.3, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Top-right: constraint box — equality + four separate 0<=alpha_i<=C rows
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.7, y: 1.55, w: 5.28, h: 1.3,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});
img("eq_cons.png", 7.85, 1.68, 4.9, 1.0);

// Middle band: Maximize => Minimize dual (blue outline)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.35, y: 3.0, w: 12.63, h: 0.72,
  fill: { color: "FFFFFF" }, line: { color: "1F4E79", width: 1.5 },
});
img("eq_dual.png", 0.55, 3.06, 12.1, 0.60);

// Diagonal watermark (large grey, as in original)
s.addText("From Previous Lecture", {
  x: 3.2, y: 3.72, w: 6.6, h: 0.5, rotate: -18,
  fontSize: 20, bold: true, italic: true, color: "808080", fontFace: FONT, margin: 0,
});
// Pale-yellow matrix panel (as in original) behind the matrices row
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.35, y: 3.95, w: 12.63, h: 1.67,
  fill: { color: "FFFDE7" }, line: { color: "C00000", width: 1.5 },
});
// Matrices row: X, G = X^T X, y-vector (1,1,-1,-1), |1 1 -1 -1| = YG matrix
img("eq_X.png", 0.45, 4.05, 2.3, 1.45);
img("eq_G.png", 2.85, 4.05, 3.3, 1.45);
img("eq_Y.png", 6.25, 4.05, 1.7, 1.45);
img("eq_YG.png", 8.05, 4.05, 4.85, 1.45);

// Lower red panel: quadratic objective + constraints
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.35, y: 5.6, w: 12.63, h: 1.75,
  fill: { color: "FBEEDD" }, line: { color: "C00000", width: 1.5 },
});
s.addText("Minimize:", {
  x: 0.5, y: 5.68, w: 1.3, h: 0.3,
  fontSize: 13, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
// objective across three aligned lines, leading "[ +1a1^2+2a1a2-5.5a1a3-6a1a4..."
img("eq_obj.png", 1.85, 5.64, 8.6, 1.02);
img("eq_bounds.png", 9.25, 6.68, 3.6, 0.42);

// "Subject to:" on its own line
s.addText("Subject to:", {
  x: 0.5, y: 6.78, w: 1.3, h: 0.3,
  fontSize: 12, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
img("eq_subj.png", 1.85, 6.72, 7.2, 0.565);

// "Quadratic Equation in α with constraints" bottom-RIGHT of the panel
s.addText("Quadratic Equation in \u03b1 with constraints", {
  x: 8.3, y: 7.12, w: 4.6, h: 0.25,
  align: "right", valign: "middle",
  fontSize: 12, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_011_recreated.pptx") })
  .then(() => console.log("wrote slide_011_recreated.pptx"))
  .catch(e => console.error(e));
