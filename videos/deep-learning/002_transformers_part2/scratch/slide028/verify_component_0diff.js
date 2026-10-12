// verify_component_0diff.js — rebuild slide 028 via the BANKED COMPONENT and diff the
// 150dpi render against the certified qa render (must be 0 differing pixels).
const path = require("path");
const pptxgen = require("pptxgenjs");
const C28 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_028.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const pptx = pres;
const slide = pres.addSlide();
C28.renderBase(pptx, slide, { numeral: 28, wordCount: 9 });
pres.writeFile({ fileName: path.join(__dirname, "component_verify.pptx") })
  .then(() => console.log("WROTE component_verify.pptx"));
