const pptxgen = require("pptxgenjs");
const { newPres, addHouseChrome, addPlotShell, addDot, addCluster, W, H, FONT } = require("./shared.js");

const NUM = 42;
const TITLE = null;

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, NUM, TITLE);

// Main plot area with red border
// From analysis: scatter plot centered, x 0-40, y -10 to 40
// Measured position: plot spans ≈x215-655, y75-430 in 960x540
const PX = 0.21 * W, PY = 0.13 * H, PW = 0.55 * W, PH = 0.71 * H;
const X_MIN = 0, X_MAX = 40;
const Y_MIN = -10, Y_MAX = 40;

const mapper = addPlotShell(pres, s, PX, PY, PW, PH, X_MIN, X_MAX, Y_MIN, Y_MAX, "", "");
const path = require("path");
s.addImage({ path: path.join(__dirname, "slide_042_graph.png"), x: 0.20 * W, y: 0.12 * H, w: 0.56 * W, h: 0.75 * H });

// Seven clusters
// blue upper-left (approx x 5-15, y 15-30)
// red upper-center (approx x 18-25, y 20-25)
// cyan upper-right (approx x 30-35, y 15-30)
// yellow mid-left (approx x 5-10, y 10-13)
// magenta center (approx x 10-25, y 5-12)
// green lower-left (approx x 5-8, y 2-5)
// black lower-right (approx x 30-35, y 5-10)
const CLUSTERS = [
  {cx: 10, cy: 22, color: "0000FF", spread: 14, count: 350},
  {cx: 22, cy: 23, color: "FF0000", spread: 7, count: 300},
  {cx: 33, cy: 22, color: "00FFFF", spread: 8, count: 350},
  {cx: 7, cy: 12, color: "FFFF00", spread: 7, count: 250},
  {cx: 18, cy: 8, color: "FF00FF", spread: 16, count: 400},
  {cx: 6, cy: 3, color: "00FF00", spread: 7, count: 200},
  {cx: 33, cy: 7, color: "000000", spread: 8, count: 300},
];

CLUSTERS.forEach(c => {
  addCluster(pres, s, mapper, c.cx, c.cy, c.spread, c.count, c.color, 0.025);
});

// Bottom black strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.15, w: W, h: 0.15,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_042_recreated.pptx" })
  .then(() => console.log("wrote slide_042_recreated.pptx"))
  .catch(e => console.error(e));