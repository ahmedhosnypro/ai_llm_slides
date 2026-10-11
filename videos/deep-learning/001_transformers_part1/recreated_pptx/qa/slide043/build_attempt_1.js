// build/slide_043.js — slide 043 entry point (single-version law: ONE deliverable,
// recreated_pptx/slide_043_recreated.pptx). The composition lives in
// components/slide_043.js so children 44 and 45 can import it (dependency law).
//
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//        videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_043.js

const pptxgen = require("pptxgenjs");
const { renderBase } = require("./components/slide_043.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_043_recreated.pptx";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const slide = pptx.addSlide();
renderBase(pptx, slide, { numeral: 43 });

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE", OUT);
});
