const pptxgen = require("pptxgenjs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_023_recreated.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 23);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.063, 0.07, 0.946, 0.948]), { fill: { type: "none" }, line: { color: "C00000", width: 1.5 } }));
// header tag + title
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box([0.068, 0.106, 0.193, 0.167]), { fill: { type: "none" }, line: { color: "0000FF", width: 1, dashStyle: "dash" } }));
let b = box([0.068, 0.106, 0.193, 0.167]);
s.addText("Example-3", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", valign: "middle", fontSize: 12, color: "0000FF", fontFace: "Arial", margin: 0 });
b = box([0.200, 0.102, 0.625, 0.163]);
s.addText("Radial Basis Function (RBF) Kernel", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", valign: "middle", fontSize: 18, bold: true, color: "C00000", fontFace: "Arial", margin: 0 });
b = box([0.656, 0.089, 0.846, 0.139]);
s.addText("[ e^\u2212\u03b3 \u2016a \u2212 b\u2016\u00b2 ]", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", valign: "middle", fontSize: 12, color: "000000", fontFace: "Arial", margin: 0 });
function arrow(bv) {
  const b = box(bv);
  s.addShape(pres.shapes.RIGHT_ARROW, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 } });
}
function panel(bv, stroke, label) {
  s.addShape(pres.shapes.RECTANGLE, Object.assign(box(bv), { fill: { color: "FFFFFF" }, line: { color: stroke, width: 1.5 } }));
  const b = box(bv);
  s.addText(label, { x: b.x, y: b.y + 0.02, w: b.w, h: 0.3, align: "center", fontSize: 14, bold: true, color: "C00000", fontFace: "Arial", margin: 0 });
}
// top flow row
let ib = box([0.075, 0.265, 0.175, 0.361]);
s.addShape(pres.shapes.RECTANGLE, Object.assign(ib, { fill: { color: "FFFFCC" }, line: { color: "000000", width: 1 } }));
s.addText("(a1, a2)\n|\n(b1, b2)", { x: ib.x, y: ib.y, w: ib.w, h: ib.h, align: "center", valign: "middle", fontSize: 9, color: "000000", fontFace: "Arial", margin: 0 });
arrow([0.179, 0.300, 0.529, 0.340]);
panel([0.533, 0.176, 0.872, 0.472], "0000FF", "Normal Model");
let cb = box([0.565, 0.230, 0.845, 0.290]);
s.addText("Calculate a^T b", { x: cb.x, y: cb.y, w: cb.w, h: cb.h, align: "center", fontSize: 11, color: "000000", fontFace: "Arial", margin: 0 });
let mb = box([0.648, 0.311, 0.752, 0.398]);
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(mb, { fill: { color: "ADD8E6" }, line: { color: "808080", width: 1 } }));
s.addText("(a1  a2)\n(b1\nb2)", { x: mb.x, y: mb.y, w: mb.w, h: mb.h, align: "center", valign: "middle", fontSize: 10, color: "000000", fontFace: "Arial", margin: 0 });
arrow([0.875, 0.310, 0.901, 0.345]);
// mapping strip
let ms = box([0.075, 0.45, 0.526, 0.515]);
s.addShape(pres.shapes.RECTANGLE, Object.assign(ms, { fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 } }));
s.addText([{ text: "Map Input data from 2-D to ", options: { fontSize: 12, color: "0000FF", fontFace: "Arial" } }, { text: "infinite Dimension", options: { fontSize: 12, italic: true, color: "FF0000", fontFace: "Arial" } }], { x: ms.x, y: ms.y, w: ms.w, h: ms.h, align: "center", valign: "middle", margin: 0 });
// bottom flow row
ib = box([0.075, 0.657, 0.175, 0.778]);
s.addShape(pres.shapes.RECTANGLE, Object.assign(ib, { fill: { color: "FFFFCC" }, line: { color: "000000", width: 1 } }));
s.addText("(a1, a2)\n|\n(b1, b2)", { x: ib.x, y: ib.y, w: ib.w, h: ib.h, align: "center", valign: "middle", fontSize: 8, color: "000000", fontFace: "Arial", margin: 0 });
arrow([0.179, 0.700, 0.217, 0.735]);
let eb = box([0.227, 0.556, 0.367, 0.639]);
s.addShape(pres.shapes.RECTANGLE, Object.assign(eb, { fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } }));
s.addText("e^\u2212\u03b3 \u2016a \u2212 b\u2016\u00b2", { x: eb.x, y: eb.y, w: eb.w, h: eb.h, align: "center", valign: "middle", fontSize: 10, color: "000000", fontFace: "Arial", margin: 0 });
let vb = box([0.216, 0.657, 0.365, 0.778]);
s.addShape(pres.shapes.RECTANGLE, Object.assign(vb, { fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1 } }));
s.addText([{ text: "Vectors Mapping\n", options: { fontSize: 10, bold: true, color: "000000", fontFace: "Arial", breakLine: true } }, { text: "a , b \u21d2 u , v", options: { fontSize: 9, color: "000000", fontFace: "Arial" } }], { x: vb.x, y: vb.y, w: vb.w, h: vb.h, align: "center", valign: "middle", margin: 0 });
let cb2 = box([0.227, 0.781, 0.367, 0.885]);
s.addShape(pres.shapes.RECTANGLE, Object.assign(cb2, { fill: { color: "FF00FF" }, line: { color: "FF00FF" } }));
s.addText("Higher\nComputational\nComplexity !!!", { x: cb2.x, y: cb2.y, w: cb2.w, h: cb2.h, align: "center", valign: "middle", fontSize: 8, color: "000000", fontFace: "Arial", margin: 0 });
arrow([0.370, 0.700, 0.406, 0.735]);
let pb = box([0.411, 0.565, 0.505, 0.856]);
s.addShape(pres.shapes.RECTANGLE, Object.assign(pb, { fill: { color: "FFCCFF" }, line: { color: "000000", width: 1 } }));
s.addText("u1   v1\nu2   v2\nu3   v3\n...  ...\nu\u221e   v\u221e", { x: pb.x, y: pb.y, w: pb.w, h: pb.h, align: "center", valign: "middle", fontSize: 8, color: "000000", fontFace: "Arial", margin: 0 });
arrow([0.508, 0.700, 0.540, 0.735]);
panel([0.540, 0.504, 0.873, 0.917], "008000", "Kernelized Model");
cb = box([0.560, 0.555, 0.855, 0.610]);
s.addText("Calculate u^T v", { x: cb.x, y: cb.y, w: cb.w, h: cb.h, align: "center", fontSize: 11, color: "000000", fontFace: "Arial", margin: 0 });
let lb = box([0.583, 0.611, 0.844, 0.88]);
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(lb, { fill: { color: "CCFFCC" }, line: { color: "808000", width: 1 } }));
s.addText("u1 u2 u3 ... u\u221e\nv1\nv2\nv3\n...\nv\u221e", { x: lb.x, y: lb.y, w: lb.w, h: lb.h, align: "center", valign: "middle", fontSize: 8, color: "000000", fontFace: "Arial", margin: 0 });
let cb3 = box([0.750, 0.759, 0.844, 0.874]);
s.addShape(pres.shapes.RECTANGLE, Object.assign(cb3, { fill: { color: "FF00FF" }, line: { color: "FF00FF" } }));
s.addText("Higher\nComputational\nComplexity !!!", { x: cb3.x, y: cb3.y, w: cb3.w, h: cb3.h, align: "center", valign: "middle", fontSize: 8, color: "000000", fontFace: "Arial", margin: 0 });
arrow([0.875, 0.700, 0.902, 0.735]);
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
