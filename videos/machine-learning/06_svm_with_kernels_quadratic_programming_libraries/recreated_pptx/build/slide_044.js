const pptxgen = require("pptxgenjs");
const { newPres, addHouseChrome, addPlotShell, addDot, addCluster, addRing, W, H, FONT } = require("./shared.js");

const NUM = 44;
const TITLE = null;

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, NUM, TITLE);

// Main plot area with red border
// From analysis: x 0-50, y 0-30
const PX = 0.156 * W, PY = 0.089 * H, PW = 0.740 * W, PH = 0.785 * H;
const X_MIN = 0, X_MAX = 50;
const Y_MIN = 0, Y_MAX = 30;

const mapper = addPlotShell(pres, s, PX, PY, PW, PH, X_MIN, X_MAX, Y_MIN, Y_MAX, "", "");

addCluster(pres, s, mapper, 10, 20, 5, 300, "000000", 0.025);
addCluster(pres, s, mapper, 20, 19, 4, 250, "FF00FF", 0.025);
for (let i = 0; i < 500; i++) {
  const a = i * 2.399963, r = 2.4 + (i % 17) / 17 * 1.8;
  addDot(pres, s, mapper, 13 + r * Math.cos(a), 9 + r * Math.sin(a), "00FF00", 0.025);
}
addCluster(pres, s, mapper, 13, 9, 1.5, 100, "00FFFF", 0.025);
for (let i = 0; i < 350; i++) {
  const a = -1.2 + (i % 70) / 70 * 2.4, r = 2.5 + Math.floor(i / 70) * 0.35;
  addDot(pres, s, mapper, 32 + r * Math.cos(a), 16 + r * Math.sin(a), "0000FF", 0.025);
}
for (let x = 30; x <= 44; x += 1.4) {
  for (let y = 8; y <= 23; y += 1.4) addDot(pres, s, mapper, x, y, "FF0000", 0.025);
}
s.addShape(pres.shapes.LINE, { x: mapper.toX(29), y: mapper.toY(22), w: 0.25, h: 0.20,
  line: { color: "000000", width: 1.5, endArrowType: "triangle" } });

// Bottom black strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.15, w: W, h: 0.15,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_044_recreated.pptx" })
  .then(() => console.log("wrote slide_044_recreated.pptx"))
  .catch(e => console.error(e));