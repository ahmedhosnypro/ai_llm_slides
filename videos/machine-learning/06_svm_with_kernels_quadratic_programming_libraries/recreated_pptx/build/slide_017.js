const pptxgen = require("pptxgenjs");
const path = require("path");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const W = 13.33, H = 7.5, FONT = "Arial";
const X = v => v * W, Y = v => v * H;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

function rect(r, fill, line, width = 1) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(r[0]), y: Y(r[1]), w: X(r[2] - r[0]), h: Y(r[3] - r[1]),
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: line, width },
  });
}
function line(x0, y0, x1, y1, color, width = 1.5, extra = {}) {
  s.addShape(pres.shapes.LINE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    line: { color, width, ...extra },
  });
}
function dots(points, color) {
  points.forEach(([x, y]) => s.addShape(pres.shapes.OVAL, {
    x: X(x) - 0.07, y: Y(y) - 0.07, w: 0.14, h: 0.14,
    fill: { color }, line: { color, width: 0.5 },
  }));
}
function callout(r, label) {
  rect(r, "FFFFFF", "1F4ED8", 1);
  s.addText(label, {
    x: X(r[0]), y: Y(r[1]), w: X(r[2] - r[0]), h: Y(r[3] - r[1]),
    align: "center", valign: "middle", fontSize: 11, bold: true, italic: true,
    color: "1F4ED8", fontFace: FONT, lineSpacing: 13, margin: 0,
  });
}

rect([0.15 / W, 0.15 / H, 13.18 / W, 7.35 / H], null, "C00000", 1.5);
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("17", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Non-Linearly ", options: { color: "C00000" } },
  { text: "Separable", options: { color: "0000FF", underline: true } },
  { text: " Data", options: { color: "C00000" } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 22, bold: true, fontFace: FONT, margin: 0,
});
rect([0.09, 0.18, 0.89, 0.89], "FFFFFF", "9E1B32", 1.25);
s.addText('Each Sample is represented by two features "x" and "y"', {
  x: X(0.10), y: Y(0.22), w: X(0.55), h: Y(0.06),
  align: "left", valign: "middle", fontSize: 13, italic: true,
  color: "8B0000", fontFace: FONT, margin: 0,
});
line(0.28, 0.565, 0.65, 0.565, "C00000", 2, { endArrowType: "triangle" });
line(0.48, 0.30, 0.48, 0.82, "C00000", 2, { beginArrowType: "triangle" });
s.addText("x", { x: X(0.64), y: Y(0.59), w: 0.3, h: 0.3, fontSize: 16, italic: true, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("y", { x: X(0.50), y: Y(0.31), w: 0.3, h: 0.3, fontSize: 16, italic: true, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.OVAL, {
  x: X(0.42), y: Y(0.45), w: X(0.13), h: Y(0.23),
  fill: { type: "none" }, line: { color: "ED7D31", width: 2 },
});
line(0.40, 0.44, 0.62, 0.77, "1F4ED8", 3, { flipV: true });

const cyan = [
  [0.51646, 0.46833], [0.45042, 0.46852],
  [0.41896, 0.51852], [0.54792, 0.51852],
  [0.40323, 0.59667], [0.56365, 0.59667],
  [0.41250, 0.66926], [0.55094, 0.66926],
  [0.51656, 0.72519], [0.45031, 0.72537],
];
const red = [
  [0.50406, 0.53519], [0.45052, 0.54667],
  [0.43771, 0.60222], [0.52594, 0.60259],
  [0.45667, 0.66389], [0.50385, 0.66926],
];
dots(cyan, "40E0D0");
dots(red, "C00000");
callout([0.66, 0.31, 0.75, 0.44], "Linear\nDecision\nBoundary");
callout([0.60, 0.71, 0.68, 0.84], "Non-Linear\nDecision\nBoundary");
line(0.60, 0.44, 0.66, 0.50, "1F4ED8", 1.25, { flipHorizontal: true });
line(0.53, 0.65, 0.60, 0.71, "808080", 1.25);
rect([0, 0.96, 1, 1], "000000", "000000", 0);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_017_recreated.pptx") })
  .then(() => console.log("wrote slide_017_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
