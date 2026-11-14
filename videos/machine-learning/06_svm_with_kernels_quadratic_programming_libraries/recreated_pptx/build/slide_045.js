// slide_045.js — SVM decision regions (fix2: green annulus around cyan core, blue nonconvex two-lobe blob)
// House frame + embedded matplotlib PNG; geometry matches gen_slides_045_055.js slide 45.
// Run: NODE_PATH=$(npm root -g) node slide_045.js

const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const ASSETS = path.join(NS, "recreated_pptx/build/assets/045_055");
const OUT = path.join(NS, "recreated_pptx");
const FONT = "Arial";
const W = 13.33, H = 7.5;

const NUM = 45;
const chart = [0.234, 0.148, 0.764, 0.841];

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const s = pres.addSlide();
  s.background = { color: "E8E8E8" };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
    fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
  });
  s.addShape(pres.shapes.OVAL, {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
  });
  s.addText(String(NUM), {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
  });
  s.addText("Figure 45", {
    x: 0.6, y: 0.28, w: 12.13, h: 0.5,
    align: "center", valign: "top",
    fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
  });
  const [cx, cy, cx2, cy2] = chart;
  s.addImage({
    path: path.join(ASSETS, "slide_045_plot_fix3.png"),
    x: cx * W, y: cy * H, w: (cx2 - cx) * W, h: (cy2 - cy) * H,
  });
  const file = path.join(OUT, `slide_${String(NUM).padStart(3, "0")}_recreated.pptx`);
  await pres.writeFile({ fileName: file });
  console.log("wrote", file);
})().catch((e) => { console.error(e); process.exit(1); });
