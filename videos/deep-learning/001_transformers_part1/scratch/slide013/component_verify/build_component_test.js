// 0-pixel-diff verification harness: render the banked component with defaults
// and compare against the certified reference render qa/slide013/render_1.png.
const path = require("path");
const pptxgen = require("pptxgenjs");
const { renderBase } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_013.js"
);
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide, {}); // defaults: chrome numeral 13 + title
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide013/component_verify/component_test.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
