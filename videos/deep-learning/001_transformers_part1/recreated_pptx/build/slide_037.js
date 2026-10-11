// slide_037.js — "Self Attention Mechanism (Adding Scaling)" (Deep Learning DSAI 308,
// lecture 001_transformers_part1). Top-level build for slide 37.
//
// Chrome: PLAYLIST house chrome via the per-video primitive (founder directive
// 2026-10-11) — white FFFFFF canvas, gray E9E9E7 panel x42..918 y45..bottom with the
// C00000 border, badge d36px at (893,71) FDFD96/6A5ACD ring, bold 333333 numeral 37.
// The ml-intro chrome values in 17_worker_instructions.md are superseded for this deck.
// Composition: imported from components/slide_037.js (renderBase, block granularity) —
// slide 38 (dependent) composes from that component plus its own inset delta.
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js");
const { renderBase } = require("./components/slide_037.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_037_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

drawHouseChrome(pres, slide, { numeral: 37 });
renderBase(pres, slide, {});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
