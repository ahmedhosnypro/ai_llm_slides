// 0-pixel-diff verify driver: build via the BANKED COMPONENT exactly as slide 10
// will consume it (require by absolute path + renderBase), then render-compare.
const pptxgen = require("pptxgenjs");
const C9 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_009.js");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
C9.renderBase(pres, s, { numeral: 9 });
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide009/component_verify.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
