// base_render.js — render the imported 001:19 certified composition with numeral 37
// (FULL base, no skips) for the PIL-diff. NOT the deliverable; scratch only.
const pptxgen = require("pptxgenjs");
const comp = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_019.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
comp.renderBase(pres, s, { numeral: 37 });
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/base_019.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
