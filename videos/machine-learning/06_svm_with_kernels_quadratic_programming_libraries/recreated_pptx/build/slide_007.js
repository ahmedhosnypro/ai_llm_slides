// slide_007.js — wave-3 rebuild round 2 from qa/reanalysis2/slide_007_analysis.txt ONLY.
// rb4 math assets: true stacked 2-D vectors/matrices (row PNGs + drawn brackets),
// panel-3 block sized to fit its panel, en-dash in equation 3.
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx", "build", "eq_007");
const MAN = Object.assign({}, require(path.join(EQ, "rb5_manifest.json")), require(path.join(EQ, "rb6_manifest.json")));

const W = 13.33, H = 7.5;
const X = (v) => v * W, Y = (v) => v * H;
const box = (b) => ({ x: X(b[0]), y: Y(b[1]), w: X(b[2] - b[0]), h: Y(b[3] - b[1]) });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.background = { color: "E8E8E8" };

// House chrome (mandatory, overrides spec)
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
slide.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
slide.addText("7", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
slide.addText("Equal Constraints", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: "C00000", fontFace: "Arial", margin: 0,
});

// Three red-outlined white panels
for (const p of [
  [0.094, 0.176, 0.823, 0.319],
  [0.094, 0.339, 0.823, 0.620],
  [0.094, 0.639, 0.823, 0.824],
]) {
  b = box(p);
  slide.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1 } });
}

// Math helpers
function img(name, x, y) {
  const m = MAN[name];
  slide.addImage({ path: path.join(EQ, m.image), x, y, w: m.w_in, h: m.h_in });
  return m;
}
function eqC(name, bb) {
  const m = MAN[name];
  img(name, bb.x + (bb.w - m.w_in) / 2, bb.y + (bb.h - m.h_in) / 2);
}
function plain(name, x, cy) {
  const m = MAN[name];
  img(name, x, cy - m.h_in / 2);
  return m.w_in;
}
// Stack row PNGs as a true 2-D block centered in [x, x+w] around cy; place
// mathtext-rendered bracket PNGs (rb6_br3/br4) hugging the stack edges.
function stack(names, x, w, cy, gap, br) {
  const hs = names.map((n) => MAN[n].h_in);
  const total = hs.reduce((a, c) => a + c, 0) + gap * (names.length - 1);
  const wMax = Math.max(...names.map((n) => MAN[n].w_in));
  const x0 = x + (w - wMax) / 2;
  let y = cy - total / 2;
  for (const n of names) { img(n, x0, y); y += MAN[n].h_in + gap; }
  const bm = MAN[br];
  const bw = wMax + 0.24, bh = total + 0.06;
  slide.addImage({ path: path.join(EQ, bm.image), x: x0 - 0.12, y: cy - bh / 2, w: bw, h: bh });
  return { x0, w: wMax, x1b: x0 + wMax + 0.12, y0: cy - total / 2, y1: cy + total / 2 };
}
// Section labels (blue, bold, underlined) and pink "A x = b" chips
for (const [w1, w2, bb0] of [
  ["One", "Constraint", [0.692, 0.183, 0.803, 0.209]],
  ["Three", "Constraints", [0.678, 0.387, 0.810, 0.413]],
  ["Four", "Constraints", [0.685, 0.665, 0.813, 0.691]],
]) {
  b = box(bb0);
  slide.addText([
    { text: w1 + " ", options: { fontSize: 12, bold: true, underline: true, color: "0000FF", fontFace: "Arial" } },
    { text: w2, options: { fontSize: 12, bold: true, underline: true, color: "FF0000", fontFace: "Arial" } },
  ], {
    x: b.x, y: b.y, w: b.w, h: b.h,
    align: "left", valign: "middle", margin: 0,
  });
}
for (const c of [
  [0.729, 0.222, 0.803, 0.263],
  [0.729, 0.446, 0.803, 0.487],
  [0.729, 0.709, 0.803, 0.750],
]) {
  b = box(c);
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FFC7CE" }, line: { type: "none" } });
  slide.addText("A x = b", {
    x: b.x, y: b.y, w: b.w, h: b.h,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, italic: true, color: "FF0000", fontFace: "Times New Roman", margin: 0,
  });
}

// Panel 1: summation, red arrow, [a1 a2 a3][x1;x2;x3] = (z)_{1*1}
eqC("rb5_sum1", box([0.101, 0.190, 0.368, 0.283]));
eqC("rb5_arrow", box([0.405, 0.219, 0.424, 0.248]));
b = box([0.435, 0.190, 0.625, 0.305]);
let cy = b.y + b.h / 2;
let cx = b.x + 0.03;
cx += plain("rb5_p1_rowA", cx, cy) + 0.07;
let v = stack(["rb5_x1", "rb5_x2", "rb5_x3"], cx, 0.34, cy, 0.03, "rb6_br3");
cx = v.x1b + 0.10;
plain("rb5_p1_rhs", cx, cy);

// Panel 2: three summations, arrow, 3x3 matrix * x-vector = Z-vector with 3*1
eqC("rb5_sum_a", box([0.101, 0.357, 0.172, 0.415]));
eqC("rb5_sum_b", box([0.101, 0.439, 0.172, 0.502]));
eqC("rb5_sum_c", box([0.101, 0.528, 0.172, 0.593]));
eqC("rb5_arrow", box([0.234, 0.444, 0.253, 0.474]));
b = box([0.265, 0.398, 0.560, 0.528]);
cy = b.y + b.h / 2;
cx = b.x + 0.02;
let m = stack(["rb5_r_a", "rb5_r_b", "rb5_r_c"], cx, 0.80, cy, 0.05, "rb6_br3");
cx = m.x1b + 0.10;
v = stack(["rb5_x1", "rb5_x2", "rb5_x3"], cx, 0.30, cy, 0.03, "rb6_br3");
cx = v.x1b + 0.08;
cx += plain("rb5_eq", cx, cy) + 0.08;
let r = stack(["rb5_Z1", "rb5_Z2", "rb5_Z3"], cx, 0.30, cy, 0.03, "rb6_br3");
img("rb5_ann31", r.x1b + 0.03, r.y1 - 0.27);

// Panel 3: four red equations, arrow, 4x3 matrix (4*3) * x-vector = (7;12;10;24) (4*1)
eqC("rb5_p3_left", box([0.109, 0.648, 0.210, 0.809]));
eqC("rb5_arrow", box([0.254, 0.702, 0.273, 0.732]));
b = box([0.290, 0.655, 0.600, 0.815]);
cy = b.y + b.h / 2;
cx = b.x + 0.02;
m = stack(["rb5_n1", "rb5_n2", "rb5_n3", "rb5_n4"], cx, 0.80, cy, 0.02, "rb6_br4");
img("rb5_ann43", m.x1b + 0.03, m.y1 - 0.27);
cx = m.x1b + 0.55;
v = stack(["rb5_x1", "rb5_x2", "rb5_x3"], cx, 0.30, cy, 0.03, "rb6_br3");
cx = v.x1b + 0.08;
cx += plain("rb5_eq", cx, cy) + 0.08;
r = stack(["rb5_v7", "rb5_v12", "rb5_v10", "rb5_v24"], cx, 0.30, cy, 0.03, "rb6_br4");
img("rb5_ann41", r.x1b + 0.03, r.y1 - 0.27);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_007_recreated.pptx") });
