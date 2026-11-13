const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const W = 13.33, H = 7.5;

async function buildSourcePanel(num) {
  const ss = String(num).padStart(3, "0");
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const s = pres.addSlide();
  s.background = { color: "E8E8E8" };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.15, y: 0.15, w: 13.03, h: 7.2,
    fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
  });
  s.addShape(pres.shapes.OVAL, {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
  });
  s.addText(String(num), {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    align: "center", valign: "middle", fontSize: 18, bold: true,
    color: "333333", fontFace: "Arial", margin: 0,
  });
  s.addText("", {
    x: 0.6, y: 0.28, w: 12.13, h: 0.55,
    align: "center", valign: "top", fontSize: 24, bold: true,
    color: "C00000", fontFace: "Arial", margin: 0,
  });
  s.addImage({
    path: path.join(NS, `recreated_pptx/build/slide_${ss}_source_panel.png`),
    x: 58 / 960 * W, y: 42 / 540 * H,
    w: 844 / 960 * W, h: 476 / 540 * H,
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 519 / 540 * H, w: W, h: 21 / 540 * H,
    fill: { color: "000000" }, line: { type: "none" },
  });
  const out = path.join(NS, `recreated_pptx/slide_${ss}_recreated.pptx`);
  await pres.writeFile({ fileName: out });
  console.log(`wrote ${out}`);
}

module.exports = { buildSourcePanel };
