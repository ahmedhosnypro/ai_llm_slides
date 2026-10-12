const pptxgen = require("pptxgenjs");
const comp = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_045.js");
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
comp.renderBase(pptx, slide, { numeral: 45 });
pptx.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide045/bankverify/verify_045.pptx" }).then(() => console.log("WROTE verify_045.pptx"));
