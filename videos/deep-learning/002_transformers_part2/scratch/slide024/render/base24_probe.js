// base probe: render ONLY the certified slide_023 component at numeral 24 (scratch use)
const path = require("path");
const pptxgen = require("pptxgenjs");
const parent = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_023.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
parent.renderBase(pres, slide, { numeral: 24 });
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide024/render/base24_probe.pptx" })
  .then(() => console.log("WROTE base24_probe.pptx"));
