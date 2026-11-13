const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { W, H, house, box } = require("./house023.js");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_026_recreated.pptx";
const eq = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/eqs_023_033.json"))["26"];
const A = NS + "/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 26);
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.047, 0.061, 0.953, 0.941]), { fill: { type: "none" }, line: { color: "C00000", width: 1.5 } }));
let b = box([0.205, 0.08, 0.795, 0.14]);
s.addText("Quadratic Kernel Mapping and Kernel Trick", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 22, bold: true, color: "000000", fontFace: "Arial", margin: 0 });
// upper math box
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.048, 0.15, 0.952, 0.507]), { fill: { type: "none" }, line: { color: "2E5AAC", width: 1 } }));
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.063, 0.275, 0.145, 0.325]), { fill: { color: "FCE4D6" }, line: { color: "FCE4D6" } }));
function img(key, x, y) { const e = eq[key]; s.addImage({ path: A + `s026_${key}.png`, x, y, w: e.w_in, h: e.h_in }); }
const x0 = 0.070 * W;
img("ab", x0, 0.225 * H);
img("eq1", x0, 0.285 * H);
img("eq2", x0, 0.345 * H);

// vertical divider
s.addShape(pres.shapes.RECTANGLE, { x: 0.615 * W, y: 0.15 * H, w: 0.002 * W, h: 0.355 * H, fill: { color: "BFBFBF" }, line: { color: "BFBFBF" } });
let wb = box([0.625, 0.26, 0.905, 0.48]);
s.addText("Where:", { x: wb.x, y: wb.y, w: wb.w, h: 0.3, fontSize: 13, color: "000000", fontFace: "Arial", margin: 0 });
img("phi", 0.625 * W, 0.305 * H);
let db = box([0.795, 0.462, 0.905, 0.5]);
s.addText("2D \u21d2 3D", { x: db.x, y: db.y, w: db.w, h: db.h, fontSize: 13, bold: true, color: "C00000", fontFace: "Arial", margin: 0 });
// lower exercise box
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.048, 0.515, 0.952, 0.905]), { fill: { type: "none" }, line: { color: "C00000", width: 1.5 } }));
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.062, 0.54, 0.902, 0.875]), { fill: { type: "none" }, line: { color: "2E5AAC", width: 1 } }));
img("abnum", 0.052 * W, 0.555 * H);
img("num", 0.220 * W, 0.560 * H);
s.addText("\u2190", { x: 0.9 * W, y: 0.555 * H, w: 0.045 * W, h: 0.06 * H, fontSize: 16, color: "C00000", fontFace: "Arial", margin: 0 });
img("alt", 0.56 * W, 0.800 * H);
s.addText("\u2190", { x: 0.898 * W, y: 0.815 * H, w: 0.045 * W, h: 0.06 * H, fontSize: 16, color: "C00000", fontFace: "Arial", margin: 0 });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
