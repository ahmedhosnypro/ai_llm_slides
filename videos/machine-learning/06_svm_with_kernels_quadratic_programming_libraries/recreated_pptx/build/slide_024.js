const pptxgen = require("pptxgenjs");
const { W, H, house, box } = require("./house023.js");
const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_024_recreated.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
house(pres, s, 24);
// light-gray slide field + dark-red frame per spec (house frame drawn on top)
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.042, 0.058, 0.961, 0.942]), { fill: { color: "F2F2F2" }, line: { color: "F2F2F2" } }));
s.addShape(pres.shapes.RECTANGLE, Object.assign(box([0.040, 0.056, 0.963, 0.944]), { fill: { type: "none" }, line: { color: "8B0000", width: 1.5 } }));
// faint hairline
s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.075 * H, w: W, h: 0.002 * H, fill: { color: "D8D8D8" }, line: { color: "D8D8D8" } });
// bottom black letterbox bar
s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.956 * H, w: W, h: 0.044 * H, fill: { color: "000000" }, line: { color: "000000" } });
// title lines
let b = box([0.371, 0.337, 0.630, 0.383]);
s.addText("KERNEL Functions", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 32, bold: true, color: "CC0000", fontFace: "Arial", margin: 0 });
b = box([0.466, 0.474, 0.534, 0.510]);
s.addText("and", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 24, color: "CC0000", fontFace: "Arial", margin: 0 });
b = box([0.417, 0.552, 0.583, 0.598]);
s.addText("Kernel Trick", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", fontSize: 30, bold: true, color: "0000FF", fontFace: "Arial", margin: 0 });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
