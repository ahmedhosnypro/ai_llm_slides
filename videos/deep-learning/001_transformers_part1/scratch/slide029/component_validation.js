// Component validation: rebuild slide 29 PURELY from components/slide_029.js + chrome
// and compare the render against the certified deliverable's render_2.png.
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js"
);
const comp = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_029.js"
);
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
drawHouseChrome(pres, s, { numeral: 29 });
comp.renderBase(pres, s, {});
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide029/component_validation.pptx" })
  .then(() => console.log("WROTE component_validation.pptx"));
