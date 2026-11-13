const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_031_recreated.pptx";
const eq = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/eqs_023_033.json"))["31"];
const A = NS + "/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 31);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.0625, 0.074, 0.944, 0.965]), { fill: { type: "none" }, line: { color: "A03030", width: 1.5 } }));
let b = box([0.283, 0.115, 0.638, 0.163]);
s.addText("Most Common Kernel Functions", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 22, bold: true, color: "C00000", fontFace: "Arial", margin: 0 });
function img(key, x, y) { const e = eq[key]; s.addImage({ path: A + `s031_${key}.png`, x, y, w: e.w_in, h: e.h_in }); }
function rule(boxv, label, labelBox, eqs) {
  s.addShape(pres.shapes.RECTANGLE, Object.assign(box(boxv), { fill: { color: "FFFFFF" }, line: { color: "3333CC", width: 1 } }));
  const lb = box(labelBox);
  s.addText(label, { x: lb.x, y: lb.y, w: lb.w, h: lb.h, fontSize: 13, bold: true, color: "000000", fontFace: "Arial", margin: 0 });
  eqs.forEach(([key, bx]) => { const bb = box(bx); img(key, bb.x, bb.y); });
}
rule([0.085, 0.226, 0.701, 0.359], "Linear Kernel", [0.115, 0.235, 0.450, 0.270], [["k1", [0.115, 0.278, 0.265, 0.330]]]);
let nb = box([0.360, 0.275, 0.585, 0.330]);
s.addText("No Mapping , \u03c6(x)=x", { x: nb.x, y: nb.y, w: nb.w, h: nb.h, fontSize: 12, color: "000000", fontFace: "Arial", margin: 0 });
rule([0.085, 0.385, 0.701, 0.519], "Quadratic Kernel", [0.115, 0.394, 0.450, 0.435], [["k2a", [0.115, 0.443, 0.300, 0.500]], ["k2b", [0.420, 0.443, 0.615, 0.500]]]);
let ob = box([0.345, 0.455, 0.375, 0.490]);
s.addText("or", { x: ob.x, y: ob.y, w: ob.w, h: ob.h, fontSize: 12, color: "000000", fontFace: "Arial", margin: 0 });
rule([0.085, 0.537, 0.701, 0.670], "Polynomial Kernel (of degree \u201cd\u201d)", [0.115, 0.546, 0.640, 0.585], [["k3a", [0.115, 0.593, 0.300, 0.645]], ["k3b", [0.420, 0.593, 0.640, 0.645]]]);
ob = box([0.345, 0.600, 0.375, 0.630]);
s.addText("or", { x: ob.x, y: ob.y, w: ob.w, h: ob.h, fontSize: 12, color: "000000", fontFace: "Arial", margin: 0 });
rule([0.085, 0.726, 0.701, 0.896], "Radial Basis Function (RBF) Kernel", [0.115, 0.735, 0.550, 0.770], [["k4", [0.115, 0.778, 0.370, 0.850]]]);
nb = box([0.420, 0.800, 0.690, 0.850]);
s.addText("\u03b3 is called RBF Kernel bandwidth", { x: nb.x, y: nb.y, w: nb.w, h: nb.h, fontSize: 12, color: "000000", fontFace: "Arial", margin: 0 });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
