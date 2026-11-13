const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_028_recreated.pptx";
const eq = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/eqs_023_033.json"))["28"];
const A = NS + "/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 28);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.059, 0.091, 0.940, 0.948]), { fill: { color: "FDF6F6" }, line: { color: "C00000", width: 1.5 } }));
// upper panel
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.063, 0.139, 0.871, 0.500]), { fill: { color: "F8F8E8" }, line: { color: "2F2FD3", width: 1 } }));
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box([0.073, 0.176, 0.154, 0.224]), { fill: { color: "F2D7A0" }, line: { color: "8A5A2B", width: 1 } }));
function img(key, x, y) { const e = eq[key]; s.addImage({ path: A + `s028_${key}.png`, x, y, w: e.w_in, h: e.h_in }); }
img("head", 0.076 * W, 0.180 * H);
img("eq", 0.168 * W, 0.150 * H);
let eb = box([0.520, 0.170, 0.871, 0.230]);
s.addText("= \u03c6(a)^T \u03c6(b)", { x: eb.x, y: eb.y, w: eb.w, h: eb.h, fontSize: 14, color: "000000", fontFace: "Arial", margin: 0 });
let wb = box([0.590, 0.235, 0.866, 0.300]);
s.addText("Where:", { x: wb.x, y: wb.y, w: wb.w, h: 0.3, fontSize: 14, color: "000000", fontFace: "Arial", margin: 0 });
img("phi", 0.590 * W, 0.270 * H);
// lower panel
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.063, 0.519, 0.924, 0.930]), { fill: { color: "F8F8E8" }, line: { color: "2F2FD3", width: 1 } }));
img("ab", 0.073 * W, 0.540 * H);
img("num", 0.073 * W, 0.610 * H);
img("sum", 0.535 * W, 0.850 * H);
s.addText("\u21d0", { x: 0.725 * W, y: 0.845 * H, w: 0.035 * W, h: 0.04 * H, fontSize: 14, color: "FF0000", fontFace: "Arial", margin: 0 });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box([0.073, 0.865, 0.160, 0.910]), { fill: { color: "F2D7A0" }, line: { color: "8A5A2B", width: 1 } }));
img("head", 0.076 * W, 0.868 * H);
img("alt", 0.165 * W, 0.868 * H);
s.addText("\u21d0", { x: 0.395 * W, y: 0.868 * H, w: 0.035 * W, h: 0.04 * H, fontSize: 14, color: "FF0000", fontFace: "Arial", margin: 0 });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
