// slide_036.js — "Multi Head Self Attention Block" (Deep Learning DSAI 308,
// Transformers Part II — video 002, slide 36).
//
// Build entry: composes the banked component components/slide_036.js (block-
// granularity renderBase; the dependency audit recommends 38<-36, so the
// composition lives there for children to import with opts.skip/only).
// Badge numeral = 36 (the number printed on THIS original frame).
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//        videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_036.js

const pptxgen = require("pptxgenjs");
const { renderBase } = require("./components/slide_036.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();
renderBase(pres, s, { numeral: 36 });

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_036_recreated.pptx" })
  .then(() => console.log("WROTE slide_036_recreated.pptx"));
