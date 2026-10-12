// slide_038.js — build wrapper: renders slide 038 via the banked component
// components/slide_038.js (renderBase) and writes the single-version deliverable.
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//        videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_038.js
const pptxgen = require("pptxgenjs");
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_038.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();
renderBase(pres, s, { numeral: 38 });

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_038_recreated.pptx" })
  .then(() => console.log("WROTE slide_038_recreated.pptx"));
