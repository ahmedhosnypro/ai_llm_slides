const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_029_recreated.pptx";
const eq = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/eqs_023_033.json"))["29"];
const A = NS + "/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 29);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.058, 0.033, 0.944, 0.959]), { fill: { type: "none" }, line: { color: "B00020", width: 2 } }));
let b = box([0.22, 0.12, 0.78, 0.21]);
s.addText("Radial Basis Function (RBF) Kernel", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 26, bold: true, color: "990000", fontFace: "Arial", margin: 0 });
// left panel
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.075, 0.23, 0.70, 0.95]), { fill: { color: "FFFFFF" }, line: { color: "B00020", width: 1 } }));
function img(key, x, y, scale = 1) { const e = eq[key]; s.addImage({ path: A + `s029_${key}.png`, x, y, w: e.w_in * scale, h: e.h_in * scale }); }
img("eq1", 0.09 * W, 0.26 * H);
img("eq2", 0.09 * W, 0.38 * H);
// vector product row
let rv = box([0.09, 0.49, 0.69, 0.80]);
s.addText("e^(ab) =  (1  a/\u221a1!  a\u00b2/\u221a2!  a\u00b3/\u221a3!  a\u2074/\u221a4!  ....  ....  \u221e)", { x: rv.x, y: rv.y, w: rv.w, h: 0.3, fontSize: 12, color: "000000", fontFace: "Arial", margin: 0 });
let cv = box([0.40, 0.54, 0.66, 0.80]);
s.addText("( 1\nb/\u221a1!\nb\u00b2/\u221a2!\nb\u00b3/\u221a3!\nb\u2074/\u221a4!\n....\n....\u221e )", { x: cv.x, y: cv.y, w: cv.w, h: cv.h, fontSize: 11, color: "000000", fontFace: "Arial", margin: 0 });
function chip(bv, text) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box(bv), { fill: { color: "FFF9C4" }, line: { color: "003399", width: 1 } }));
  const bb = box(bv);
  s.addText(text, { x: bb.x, y: bb.y, w: bb.w, h: bb.h, align: "center", valign: "middle", fontSize: 14, bold: true, color: "003399", fontFace: "Arial", margin: 0 });
}
chip([0.16, 0.54, 0.30, 0.59], "\u03c6(a)^T");
chip([0.53, 0.80, 0.66, 0.85], "\u03c6(b)");
// right panel
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.71, 0.23, 0.94, 0.85]), { fill: { color: "FFF9C4" }, line: { color: "B00020", width: 1 } }));
let hb = box([0.72, 0.25, 0.93, 0.30]);
s.addText("Taylor series expansion of (x)", { x: hb.x, y: hb.y, w: hb.w, h: hb.h, align: "center", fontSize: 12, bold: true, color: "990000", fontFace: "Arial", margin: 0 });
img("ex", 0.715 * W, 0.32 * H, 0.85);
img("e3", 0.715 * W, 0.44 * H, 0.85);
const ladder = ["Approx. to 4 terms => 13", "Approx. to 5 terms => 16.375", "Approx. to 6 terms => 18.4", "Approx. to 7 terms => 19.413", "Approx. to 8 terms => 19.84", "Approx. to 9 terms => 19.8420.01", "Actual Value => 20.086"];
let lb = box([0.72, 0.52, 0.94, 0.84]);
s.addText(ladder.map(l => ({ text: l, options: { fontSize: 13, color: "000000", fontFace: "Arial", breakLine: true, lineSpacing: 17 } })), { x: lb.x, y: lb.y, w: lb.w, h: lb.h, margin: 0 });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
