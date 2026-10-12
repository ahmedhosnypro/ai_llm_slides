// Banking verification: rebuild slide 038 from the CERTIFIED component into scratch
// (never touching the certified deliverable) for the 0-pixel-diff check.
const pptxgen = require("pptxgenjs");
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_038.js");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
renderBase(pres, s, { numeral: 38 });
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide038/bankverify/verify_038.pptx" })
  .then(() => console.log("WROTE verify_038.pptx"));
