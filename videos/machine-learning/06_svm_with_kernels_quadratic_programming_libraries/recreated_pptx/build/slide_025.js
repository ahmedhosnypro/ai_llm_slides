const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, title, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_025_recreated.pptx";
const A = NS + "/recreated_pptx/build/assets/resume_math/";
const eq = JSON.parse(fs.readFileSync(A + "manifest.json"))["25"];
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 25);
title(s, "Quadratic Kernel Mapping and Kernel Trick", 0.28, "C00000", 24);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.057, 0.078, 0.943, 0.961]), { fill: { type: "none" }, line: { color: "C00000", width: 1.5 } }));
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.069, 0.167, 0.931, 0.657]), { fill: { color: "FFFFCC" }, line: { color: "0000FF", width: 1 } }));
function img(key, bv, mode) {
  const e = eq[key], b = box(bv);
  const x = mode === "left" ? b.x : b.x + (b.w - e.w_in) / 2;
  const y = mode === "top" ? b.y : b.y + (b.h - e.h_in) / 2;
  s.addImage({ path: A + `s025_${key}.png`, x, y, w: e.w_in, h: e.h_in });
}
img("vecpair", [0.080, 0.205, 0.235, 0.275], "left");
img("eq1", [0.072, 0.300, 0.846, 0.345], "left");
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(box([0.075, 0.287, 0.146, 0.344]), { fill: { type: "none" }, line: { color: "FF0000", width: 1.5 } }));
img("eq2", [0.072, 0.430, 0.565, 0.567], "left");
img("where", [0.575, 0.455, 0.930, 0.565], "left");
let n = box([0.694, 0.565, 0.780, 0.608]);
s.addText("2D ⇒ 3D", { x: n.x, y: n.y, w: n.w, h: n.h, fontSize: 16, bold: true, color: "FF0000", fontFace: "Arial", margin: 0 });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => { console.error(e); process.exit(1); });
