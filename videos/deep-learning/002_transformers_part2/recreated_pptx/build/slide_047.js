// slide_047.js — thin build wrapper: the composition lives in the BANKED COMPONENT
// components/slide_047.js (renderBase), required by absolute path (dependency law).
// Full provenance: components/slide_047.js header + qa/slide047/worker_report.md.
const pptxgen = require("pptxgenjs");
const c47 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_047.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

c47.renderBase(pres, slide, { numeral: 47 });

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_047_recreated.pptx" })
  .then(() => console.log("WROTE slide_047_recreated.pptx (via component renderBase)"));
