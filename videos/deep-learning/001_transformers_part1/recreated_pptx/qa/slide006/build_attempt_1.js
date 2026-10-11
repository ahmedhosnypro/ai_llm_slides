// slide_006.js — main build for slide 006 "Traditional RNN  Seq2Seq model".
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//        videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_006.js
// The composition lives in components/slide_006.js (certified, shared with children 7-10);
// chrome comes from the playlist-certified shared pattern via components/house_chrome.js.

const pptxgen = require("pptxgenjs");
const path = require("path");
const { renderBase } = require(path.join(__dirname, "components", "slide_006.js"));

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

renderBase(pptx, slide, { numeral: 6 });

const OUT = path.join(__dirname, "..", "slide_006_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
