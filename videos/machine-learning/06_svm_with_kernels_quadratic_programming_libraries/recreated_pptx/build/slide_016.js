// slide_016.js — REBUILD from qa/reanalysis2/slide_016_analysis.txt (fix round 2).
// Spec coords normalized [x0,y0,x1,y1] -> inches: x*13.33, y*7.5.
// Build from project root: node <NS>/recreated_pptx/build/slide_016.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_016");
const man = JSON.parse(fs.readFileSync(path.join(EQ, "manifest.json"), "utf8"));
const W = 13.33, H = 7.5, FONT = "Arial", SERIF = "Times New Roman";
const box = r => ({ x: r[0] * W, y: r[1] * H, w: (r[2] - r[0]) * W, h: (r[3] - r[1]) * H });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (mandatory, overrides spec): red frame, badge, title
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("16", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Non-Linearly ", options: { fontSize: 26, bold: true, color: "C00000", fontFace: FONT } },
  { text: "Separable", options: { fontSize: 26, bold: true, color: "0000FF", underline: true, fontFace: FONT } },
  { text: " Data", options: { fontSize: 26, bold: true, color: "C00000", fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top", margin: 0,
});

// Inner red plot frame around the whole diagram region
const pf = box([0.090, 0.161, 0.902, 0.883]);
s.addShape(pres.shapes.RECTANGLE, {
  x: pf.x, y: pf.y, w: pf.w, h: pf.h,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
});

// Beige "Mapping" box, peach fill, blue italic serif header
const mb = box([0.103, 0.254, 0.288, 0.409]);
s.addShape(pres.shapes.RECTANGLE, {
  x: mb.x, y: mb.y, w: mb.w, h: mb.h,
  fill: { color: "F6D9A8" }, line: { color: "C8A96A", width: 1.25 },
});
s.addText([
  { text: "Mapping  x  ", options: { fontSize: 15, italic: true, color: "3333CC", fontFace: SERIF } },
  { text: "\u21d2", options: { fontSize: 15, color: "000000", fontFace: SERIF } },
  { text: "  \u03c6(x)", options: { fontSize: 15, color: "C00000", fontFace: SERIF } },
], {
  x: mb.x + 0.01, y: mb.y + 0.01, w: mb.w - 0.02, h: 0.22,
  align: "left", valign: "middle", margin: 0,
});
// Equation image x => [ x ; x^2 ] (true 2-D column, black serif), inside the box
const eb = box([0.110, 0.290, 0.280, 0.350]);
const em = man.eq_map;
s.addImage({
  path: path.join(EQ, em.file), w: em.w_in,
  x: eb.x + (eb.w - em.w_in) / 2, y: eb.y + (eb.h - em.h_in) / 2,
});

// Right-upper note in a red-bordered box, both lines red, first line bold italic
const nb = box([0.689, 0.296, 0.888, 0.383]);
s.addShape(pres.shapes.RECTANGLE, {
  x: nb.x, y: nb.y, w: nb.w, h: nb.h,
  fill: { type: "none" }, line: { color: "C00000", width: 1 },
});
const t1 = box([0.693, 0.302, 0.884, 0.338]);
s.addText("Data is linearly separable", {
  x: t1.x, y: t1.y, w: t1.w, h: t1.h,
  align: "left", valign: "middle",
  fontSize: 15, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0,
});
const t2 = box([0.693, 0.340, 0.884, 0.378]);
s.addText("In the new representation", {
  x: t2.x, y: t2.y, w: t2.w, h: t2.h,
  align: "left", valign: "middle",
  fontSize: 15, italic: true, color: "C00000", fontFace: FONT, margin: 0,
});

// "Linear Decision Boundary" callout: three-line bold-italic blue label inside a
// bordered box beside the right end of the boundary, thin leader to the line end
const bl = box([0.704, 0.444, 0.805, 0.552]);
s.addShape(pres.shapes.RECTANGLE, {
  x: bl.x, y: bl.y, w: bl.w, h: bl.h,
  fill: { color: "FFFFFF" }, line: { color: "1F49C7", width: 1 },
});
s.addText("Linear\nDecision\nBoundary", {
  x: bl.x, y: bl.y, w: bl.w, h: bl.h,
  align: "left", valign: "middle",
  fontSize: 13, bold: true, italic: true, color: "1F49C7", fontFace: SERIF, margin: 0,
});
s.addShape(pres.shapes.LINE, {
  x: 0.754 * W, y: 0.552 * H, w: (0.754 - 0.714) * W, h: (0.580 - 0.552) * H,
  line: { color: "7F7F7F", width: 1 },
});

// Red axes with arrowheads. Vertical x^2 axis at PANEL CENTRE (points straddle it);
// horizontal x axis along the zero line. Axis labels as crisp text runs.
const AX = 0.478;
s.addShape(pres.shapes.LINE, {
  x: AX * W, y: 0.237 * H, w: 0, h: (0.815 - 0.237) * H,
  line: { color: "C00000", width: 2, beginArrowType: "triangle" },
});
s.addShape(pres.shapes.LINE, {
  x: 0.111 * W, y: 0.815 * H, w: (0.860 - 0.111) * W, h: 0,
  line: { color: "C00000", width: 2, endArrowType: "triangle" },
});
s.addText([
  { text: "x", options: { fontSize: 18, italic: true, color: "C00000", fontFace: SERIF } },
  { text: "2", options: { fontSize: 12, italic: true, color: "C00000", fontFace: SERIF, superscript: true } },
], { x: AX * W + 0.09, y: 0.235 * H, w: 0.5, h: 0.3, margin: 0 });
s.addText("x", {
  x: 0.862 * W, y: 0.822 * H, w: 0.3, h: 0.3, margin: 0,
  fontSize: 15, italic: true, color: "C00000", fontFace: SERIF,
});

// Blue horizontal linear decision boundary, stopping short of the callout
s.addShape(pres.shapes.LINE, {
  x: 0.208 * W, y: 0.576 * H, w: (0.754 - 0.208) * W, h: 0,
  line: { color: "0000FF", width: 2.25 },
});

// Cyan class: symmetric parabola arms about the axis (V/U opening upward).
// Red class: V converging toward the vertical axis as it approaches the x-axis.
const cyan = [[0.327, 0.237], [0.656, 0.237], [0.356, 0.394],
              [0.589, 0.394], [0.385, 0.526], [0.560, 0.526]];
const red = [[0.3863, 0.6468], [0.4158, 0.7363], [0.4471, 0.7867],
             [0.4914, 0.7865], [0.5232, 0.7363], [0.5543, 0.6467]];
function dots(list, color) {
  list.forEach(p => {
    const cx = p[0] * W, cy = p[1] * H, r = 0.085;
    s.addShape(pres.shapes.OVAL, {
      x: cx - r, y: cy - r, w: 2 * r, h: 2 * r,
      fill: { color }, line: { color, width: 0 },
    });
  });
}
dots(cyan, "17BECF");
dots(red, "DD2C2C");

// Original 1-D data: 12 open circles on the x-axis, grouped 3 blue / 6 red / 3 blue
const seq = ["5050FF", "5050FF", "5050FF", "FF0000", "FF0000", "FF0000", "FF0000",
             "FF0000", "FF0000", "FF0000", "5050FF", "5050FF", "5050FF"];
const xs = [0.298, 0.327, 0.356, 0.385, 0.415, 0.444, 0.473, 0.502, 0.531, 0.560, 0.590, 0.619, 0.648];
for (let i = 0; i < 13; i++) {
  const cx = xs[i] * W, cy = 0.815 * H, r = 0.07;
  s.addShape(pres.shapes.OVAL, {
    x: cx - r, y: cy - r, w: 2 * r, h: 2 * r,
    fill: { type: "none" },
    line: { color: seq[i], width: 1.5 },
  });
}

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_016_recreated.pptx") })
  .then(() => console.log("wrote slide_016_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
