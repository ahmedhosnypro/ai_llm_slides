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
// House chrome: title at house position, three separate single-run boxes (LO renders
// multi-run boxes left-aligned; single-run boxes center correctly)
s.addText("KERNEL Functions", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.5, align: "center", valign: "top", margin: 0,
  fontSize: 32, bold: true, color: "CC0000", fontFace: "Arial",
});
s.addText("and", {
  x: 0.6, y: 0.78, w: 12.13, h: 0.5, align: "center", valign: "top", margin: 0,
  fontSize: 24, color: "CC0000", fontFace: "Arial",
});
s.addText("Kernel Trick", {
  x: 0.6, y: 1.28, w: 12.13, h: 0.5, align: "center", valign: "top", margin: 0,
  fontSize: 30, bold: true, color: "0000FF", fontFace: "Arial",
});
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => console.error(e));
