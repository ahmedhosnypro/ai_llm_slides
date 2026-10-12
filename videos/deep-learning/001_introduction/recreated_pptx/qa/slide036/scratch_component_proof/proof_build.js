// 0-pixel-diff banking proof: scratch build that requires the CERTIFIED component
// by absolute path and renders the identical composition (same renderBase call as
// the thin runner). Its render must be md5-identical to the certified render_3.png.
const pptxgen = require("pptxgenjs");
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_036.js");
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide036/scratch_component_proof/proof_036.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide, { numeral: "36" });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
