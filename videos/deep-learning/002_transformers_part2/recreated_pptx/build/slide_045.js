// slide_045.js — build the "Feed Forward Neural Network" recreation (002_transformers_part2).
// Thin wrapper: the composition lives in components/slide_045.js (banked for slide 46).
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_045.js
const pptxgen = require("pptxgenjs");
const comp = require(__dirname + "/components/slide_045.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_045_recreated.pptx";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
comp.renderBase(pptx, slide, { numeral: 45 });

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE", OUT);
}).catch((e) => { console.error("WRITE FAILED", e); process.exit(1); });
