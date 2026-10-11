// build/slide_018.js — builds the SINGLE-VERSION deliverable
// recreated_pptx/slide_018_recreated.pptx from the bankable child component.
//
// Run: cd /home/ahmed/Projects/ai_llm_slides && \
//      NODE_PATH=$(npm root -g) node videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_018.js

const path = require("path");
const PptxGenJS = require("pptxgenjs");
const { renderBase } = require(path.join(__dirname, "components", "slide_018.js"));

const OUT = path.join(__dirname, "..", "slide_018_recreated.pptx");

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in — house chrome expects this canvas
pptx.author = "slide-recreation worker";
pptx.title = "Encoder – Decoder Transformer (slide 18 recreation)";

const slide = pptx.addSlide();
renderBase(pptx, slide, { numeral: 18 });

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch((e) => {
  console.error("BUILD FAILED:", e);
  process.exit(1);
});
