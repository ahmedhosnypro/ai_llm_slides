// component_proof.js — scratch build requiring components/slide_035.js ONLY.
// The render of this build must be md5-identical to the certified render_2.png
// (0-pixel-diff banking proof for child slide 41).
const pptxgen = require("pptxgenjs");
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_035.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/scratch/slide035/component_proof.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide, { numeral: "35" });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
