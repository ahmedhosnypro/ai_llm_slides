// probe: the inherited base ONLY (numeral 44, no delta) — for the inheritance diff
const path = require("path");
const pptxgen = require("pptxgenjs");
const { renderBase } = require(path.join("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build", "components", "slide_043.js"));
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide, { numeral: 44, skip: ["title"] });
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide044/probe_base.pptx" }).then(() => console.log("OK"));
