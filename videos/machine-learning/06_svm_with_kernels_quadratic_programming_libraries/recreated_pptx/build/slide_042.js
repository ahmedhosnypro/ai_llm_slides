const pptxgen = require("pptxgenjs");
const { newPres, addHouseChrome, W, H } = require("./shared.js");

const NUM = 42;
const TITLE = "Slide 042: 7 clusters with arrow";

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, NUM, TITLE);

const path = require("path");
s.addImage({ path: path.join(__dirname, "slide_042_graph.png"), x: 0.20 * W, y: 0.12 * H, w: 0.56 * W, h: 0.75 * H });

// Bottom black strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.15, w: W, h: 0.15,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_042_recreated.pptx" })
  .then(() => console.log("wrote slide_042_recreated.pptx"))
  .catch(e => console.error(e));