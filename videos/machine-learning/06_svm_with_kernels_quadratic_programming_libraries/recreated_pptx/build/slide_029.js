const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_029_recreated.pptx";
const legacy = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/eqs_023_033.json"))["29"];
const man = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/resume028_029/manifest.json"));
const A = NS + "/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 29);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.058, 0.033, 0.944, 0.959]), { fill: { type: "none" }, line: { color: "B00020", width: 2 } }));
s.addText("Radial Basis Function (RBF) Kernel", { x: 0.6, y: 0.28, w: 12.13, h: 0.5, align: "center", valign: "top", fontSize: 26, bold: true, color: "990000", fontFace: "Arial", margin: 0 });
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.075, 0.23, 0.70, 0.95]), { fill: { color: "FFFFFF" }, line: { color: "2F2FD3", width: 1 } }));
function img(key, x, y, scale = 1) { const e = legacy[key]; s.addImage({ path: A + `s029_${key}.png`, x, y, w: e.w_in * scale, h: e.h_in * scale }); }
function math(key, x, y) { const e = man["s029_" + key]; s.addImage({ path: e.path, x, y, w: e.w_in, h: e.h_in }); }
img("eq1", 0.09 * W, 0.26 * H);
img("eq2", 0.09 * W, 0.38 * H);
math("rowlabel", 0.09 * W, 0.50 * H);
math("row", 0.14 * W, 0.49 * H);
math("col", 0.40 * W, 0.51 * H);
function chip(bv) { s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box(bv), { fill: { color: "FFF9C4" }, line: { color: "003399", width: 1 } })); }
chip([0.16, 0.82, 0.30, 0.87]);
math("phia", 0.182 * W, 0.827 * H);
chip([0.53, 0.88, 0.66, 0.94]);
math("phib", 0.55 * W, 0.895 * H);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.71, 0.23, 0.94, 0.85]), { fill: { color: "FFF9C4" }, line: { color: "B00020", width: 1 } }));
let hb = box([0.72, 0.25, 0.93, 0.30]);
s.addText("Taylor series expansion of (x)", { x: hb.x, y: hb.y, w: hb.w, h: hb.h, align: "center", fontSize: 12, bold: true, color: "990000", fontFace: "Arial", margin: 0 });
img("ex", 0.715 * W, 0.32 * H, 0.85);
img("e3", 0.715 * W, 0.44 * H, 0.85);
const ladder = ["Approx. to 4 terms => 13", "Approx. to 5 terms => 16.375", "Approx. to 6 terms => 18.4", "Approx. to 7 terms => 19.413", "Approx. to 8 terms => 19.84", "Approx. to 9 terms => 19.8420.01", "Actual Value => 20.086"];
ladder.forEach((line, i) => {
  const [label, value] = line.split(" => ");
  const y = (0.52 + i * 0.04) * H;
  s.addText([
    { text: label + " => ", options: { fontSize: 13, color: "000000", fontFace: "Arial" } },
    { text: value, options: { fontSize: 13, bold: true, color: "B00000", fontFace: "Arial" } },
  ], { x: 0.72 * W, y, w: 0.22 * W, h: 0.28, margin: 0 });
});
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
