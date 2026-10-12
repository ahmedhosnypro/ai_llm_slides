// Render ONLY the imported 001 slide_043 component (numeral 15) — the "parent base"
// whose output my frame must be PIL-diffed against (build law: import, never re-draw).
const pptxgen = require("pptxgenjs");
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_043.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide, { numeral: 15 });
pres.writeFile({ fileName: __dirname + "/parent_base_015.pptx" }).then(() => console.log("OK"));
