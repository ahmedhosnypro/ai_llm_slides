const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_032_recreated.pptx";
const eq = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/eqs_023_033.json"))["32"];
const A = NS + "/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 32);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.059, 0.078, 0.941, 0.948]), { fill: { color: "FFFFFF" }, line: { color: "A00000", width: 1.5 } }));
let b = box([0.23, 0.115, 0.77, 0.225]);
s.addText("New Kernel Functions can be derived From other Kernels", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 22, bold: true, color: "CC0000", fontFace: "Arial", margin: 0 });
function rule(boxv, label, lb, eqKey, eb) {
  s.addShape(pres.shapes.RECTANGLE, Object.assign(box(boxv), { fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 } }));
  const l = box(lb);
  s.addText(label, { x: l.x, y: l.y, w: l.w, h: l.h, fontSize: 13, bold: true, color: "000000", fontFace: "Arial", margin: 0 });
  const e = box(eb), im = eq[eqKey];
  s.addImage({ path: A + `s032_${eqKey}.png`, x: e.x, y: e.y, w: im.w_in, h: im.h_in });
}
rule([0.078, 0.293, 0.708, 0.441], "Sum of Kernels is a Kernel", [0.099, 0.315, 0.325, 0.350], "r1", [0.135, 0.370, 0.420, 0.415]);
rule([0.078, 0.463, 0.708, 0.602], "Scalar Product of Kernel is a kernel", [0.099, 0.481, 0.435, 0.518], "r2", [0.135, 0.540, 0.330, 0.582]);
rule([0.078, 0.620, 0.708, 0.756], "Product of Kernels is a Kernel", [0.099, 0.640, 0.335, 0.676], "r3", [0.135, 0.695, 0.418, 0.738]);
rule([0.078, 0.774, 0.708, 0.907], "Combination of the above rules is a Kernel", [0.099, 0.796, 0.450, 0.833], "r4", [0.130, 0.852, 0.488, 0.895]);
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
