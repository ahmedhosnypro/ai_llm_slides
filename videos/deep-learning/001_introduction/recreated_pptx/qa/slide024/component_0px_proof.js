// component_0px_proof.js — scratch build proving components/slide_024.js renders
// md5-identically to the certified render_4.png (0-pixel-diff proof for slide 25).
const pptxgen = require("pptxgenjs");
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_024.js");

const OUT = "/tmp/s24scratch/component_024_proof.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide, { numeral: "24" });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
