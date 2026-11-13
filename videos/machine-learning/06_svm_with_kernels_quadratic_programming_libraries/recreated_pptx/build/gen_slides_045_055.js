// gen_slides_045_055.js — house-frame builds for figure-only slides 045-055.
// Each slide: gray bg, red house frame, yellow badge, plot PNG at spec chart bbox.
// Run: NODE_PATH=$(npm root -g) node gen_slides_045_055.js
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const ASSETS = path.join(NS, "recreated_pptx/build/assets/045_055");
const OUT = path.join(NS, "recreated_pptx");
const FONT = "Arial";
const W = 13.33, H = 7.5;

// chart bboxes from analysis/slide_NNN_final.json layout regions (normalized)
const SLIDES = {
  45: { img: "slide_045_plot.png", chart: [0.234, 0.148, 0.764, 0.841] },
  46: { img: "slide_046_plot.png", chart: [0.216, 0.154, 0.756, 0.852] },
  47: { img: "slide_047_plot.png", chart: [0.231, 0.124, 0.777, 0.874] },
  48: { img: "slide_048_plot.png", chart: [0.231, 0.107, 0.769, 0.902] },
  49: { img: "slide_049_plot.png", chart: [0.250, 0.163, 0.758, 0.807] },
  50: { img: "slide_050_plot.png", chart: [0.21, 0.11, 0.78, 0.91] },
  51: { img: "slide_051_plot.png", chart: [0.24, 0.15, 0.76, 0.80] },
  52: { img: "slide_052_plot.png", chart: [0.260, 0.157, 0.756, 0.881] },
  53: { img: "slide_053_plot.png", chart: [0.2625, 0.1593, 0.7656, 0.8519] },
  54: { img: "slide_054_plot.png", chart: [0.236, 0.116, 0.917, 0.865] },
  55: { img: "slide_055_plot.png", chart: [0.241, 0.075, 0.868, 0.877] },
};

async function build(num) {
  const cfg = SLIDES[num];
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
  s.addText(String(num), {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
  });
  const [cx, cy, cx2, cy2] = cfg.chart;
  s.addImage({
    path: path.join(ASSETS, cfg.img),
    x: cx * W, y: cy * H, w: (cx2 - cx) * W, h: (cy2 - cy) * H,
  });
  const file = path.join(OUT, `slide_${String(num).padStart(3, "0")}_recreated.pptx`);
  await pres.writeFile({ fileName: file });
  console.log("wrote", file);
}

(async () => {
  const only = process.argv[2] ? [Number(process.argv[2])] : Object.keys(SLIDES).map(Number);
  for (const n of only) await build(n);
})().catch((e) => { console.error(e); process.exit(1); });
