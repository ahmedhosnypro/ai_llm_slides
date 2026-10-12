// bank_verify_scratch_build.js — 0-pixel-diff banking proof for components/slide_009.js.
// Requires the CERTIFIED component by absolute path (as children 16/18/19 will), draws
// renderBase with the default numeral, writes a SCRATCH pptx. The rendered PNG must be
// byte-identical (md5) to the certified deliverable's render.
const pptxgen = require("pptxgenjs");
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_009.js");
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide009_bank_verify/scratch_from_component.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide, { numeral: "9" });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
