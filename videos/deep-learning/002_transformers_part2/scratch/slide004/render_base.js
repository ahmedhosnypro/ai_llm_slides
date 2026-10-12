// render_base.js — render the IMPORTED 001:15 certified composition with THIS
// slide's badge numeral (4) for the PIL frame-vs-composition diff. The composition
// is imported, never re-drawn (BUILD LAW). This is a scratch harness, not the build.
const PARENT = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_015.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();
// full base, chrome ON, MY numeral (badge = number printed on MY frame)
PARENT.renderBase(pres, s, { numeral: 4 });

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004/base_num4.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
