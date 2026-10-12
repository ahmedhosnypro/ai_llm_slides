// slide_046.js — thin build wrapper: the composition lives in the BANKED COMPONENT
// components/slide_046.js (renderBase), required by absolute path (dependency law).
// Full provenance: components/slide_046.js header + qa/slide046/worker_report.md.
const pptxgen = require("pptxgenjs");
const c46 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_046.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

c46.renderBase(pres, slide, { numeral: 46 });

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_046_recreated.pptx" })
  .then(() => console.log("WROTE slide_046_recreated.pptx (via component renderBase)"));
