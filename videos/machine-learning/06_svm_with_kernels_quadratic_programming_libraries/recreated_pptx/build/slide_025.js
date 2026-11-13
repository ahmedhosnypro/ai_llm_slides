const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_025_recreated.pptx";
const eq = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/eqs_023_033.json"))["25"];
const A = NS + "/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 25);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.057, 0.078, 0.943, 0.961]), { fill: { type: "none" }, line: { color: "C00000", width: 1.5 } }));
let b = box([0.263, 0.100, 0.807, 0.148]);
s.addText("Quadratic Kernel Mapping and Kernel Trick", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 24, bold: true, color: "C00000", fontFace: "Arial", margin: 0 });
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.069, 0.167, 0.931, 0.657]), { fill: { color: "FFFFCC" }, line: { color: "0000FF", width: 1 } }));
function img(key, b) {
  const e = eq[key];
  s.addImage({ path: A + `s025_${key}.png`, x: b.x, y: b.y, w: e.w_in, h: e.h_in });
}
img("vecpair", box([0.080, 0.205, 0.235, 0.275]));
img("eq1", box([0.072, 0.300, 0.846, 0.345]));
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box([0.075, 0.287, 0.125, 0.344]), { fill: { type: "none" }, line: { color: "FF0000", width: 1.5 } }));
img("eq2", box([0.072, 0.430, 0.565, 0.567]));
let w = box([0.575, 0.455, 0.930, 0.565]);
img("where", { x: w.x, y: w.y, w: eq.where.w_in, h: eq.where.h_in });
let n = box([0.694, 0.583, 0.780, 0.626]);
s.addText("2D \u21d2 3D", { x: n.x, y: n.y, w: n.w, h: n.h, fontSize: 16, bold: true, color: "FF0000", fontFace: "Arial", margin: 0 });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
