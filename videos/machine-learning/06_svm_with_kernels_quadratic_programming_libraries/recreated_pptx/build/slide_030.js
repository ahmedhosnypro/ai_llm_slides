const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_030_recreated.pptx";
const eq = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/eqs_023_033.json"))["30"];
const A = NS + "/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 30);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.058, 0.082, 0.948, 0.953]), { fill: { type: "none" }, line: { color: "9C1C1C", width: 1.5 } }));
let b = box([0.305, 0.095, 0.79, 0.175]);
s.addText("Radial Basis Function (RBF) Kernel", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 26, bold: true, color: "CC0000", fontFace: "Arial", margin: 0 });
// main math panel
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.105, 0.253, 0.668, 0.893]), { fill: { color: "FFFFFF" }, line: { color: "2A2AE8", width: 1 } }));
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box([0.122, 0.283, 0.232, 0.353]), { fill: { color: "FCD7B0" }, line: { color: "FCD7B0" } }));
function img(key, x, y) { const e = eq[key]; s.addImage({ path: A + `s030_${key}.png`, x, y, w: e.w_in, h: e.h_in }); }
img("deriv", 0.118 * W, 0.290 * H);
// row vector container
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box([0.12, 0.378, 0.487, 0.468]), { fill: { color: "E9F0FA" }, line: { color: "E9F0FA" } }));
img("rowvec", 0.128 * W, 0.390 * H);
function chip(bv, fill, text) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box(bv), { fill: { color: fill }, line: { color: fill } }));
  const bb = box(bv);
  s.addText(text, { x: bb.x, y: bb.y, w: bb.w, h: bb.h, align: "center", valign: "middle", fontSize: 14, bold: true, italic: true, color: "C00000", fontFace: "Arial", margin: 0 });
}
chip([0.252, 0.505, 0.332, 0.575], "E6F2CF", "");
img("phiat", 0.258 * W, 0.520 * H);
// column vector container
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box([0.5, 0.345, 0.632, 0.865]), { fill: { color: "FFFBDD" }, line: { color: "FFFBDD" } }));
s.addText("1\nb/\u221a1!\nb\u00b2/\u221a2!\nb\u00b3/\u221a3!\nb\u2074/\u221a4!\n...\n...\u221e", { x: 0.535 * W, y: 0.365 * H, w: 0.06 * W, h: 0.47 * H, align: "center", fontSize: 12, color: "000000", fontFace: "Arial", margin: 0 });
chip([0.412, 0.613, 0.487, 0.688], "FCF6D5", "\u03c6(b)");
let eb = box([0.508, 0.63, 0.563, 0.69]);
img("bfactor", eb.x, eb.y);
// right side
let rb = box([0.690, 0.362, 0.900, 0.398]);
s.addText("RBF Kernel", { x: rb.x, y: rb.y, w: rb.w, h: rb.h, fontSize: 26, bold: true, color: "CC0000", fontFace: "Arial", margin: 0 });
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.714, 0.432, 0.866, 0.532]), { fill: { color: "FFFFFF" }, line: { color: "2A2AE8", width: 1 } }));
img("rbf", 0.722 * W, 0.445 * H);
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
