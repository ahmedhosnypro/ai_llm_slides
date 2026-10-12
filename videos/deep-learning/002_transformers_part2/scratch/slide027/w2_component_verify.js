// Worker-2 verification: render the banked certified component standalone and
// pixel-diff against the certified render_6.png. Touches nothing certified.
const pptxgen = require("pptxgenjs");
const comp = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_027.js");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
comp.renderBase(pres, slide, { numeral: 27, wordCount: 5 });
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide027/w2_component_verify.pptx" })
  .then(() => console.log("component-verify pptx written"));
