// slide_034.js — build the single-version deliverable slide_034_recreated.pptx
// (SINGLE-VERSION law: one plain-named pptx; equation slides get the OMML wrap
// applied to THIS file post-certification).
//
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//        videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_034.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { renderBase } = require(path.join(__dirname, "components", "slide_034.js"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "slide-recreation pipeline";
pres.title = "Self Attention Mechanism (Embedding Vector Dimension and Softmax Sensitivity)";

const slide = pres.addSlide();
renderBase(pres, slide, { numeral: 34 });

const OUT = path.join(__dirname, "..", "slide_034_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
