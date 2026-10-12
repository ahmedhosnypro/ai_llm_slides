// bank_verify_scratch_build_016.js — 0-pixel-diff banking proof for slide 016.
// Builds a THROWAWAY pptx in the scratch dir by requiring the BANKED component
// (build/components/slide_016.js) by absolute path — the exact module a child
// (slide 17) will import — and rendering it must be byte-identical to the certified
// render (qa/slide016/render_K.png) md5. The certified deliverable pptx is never touched.
const pptxgen = require("pptxgenjs");
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_016.js");

const OUT = process.argv[2];
if (!OUT) { console.error("usage: node bank_verify_scratch_build_016.js <out.pptx>"); process.exit(2); }

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide, { numeral: "16" });
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
