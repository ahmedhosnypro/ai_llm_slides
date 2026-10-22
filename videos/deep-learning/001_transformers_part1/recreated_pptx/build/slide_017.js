// build/slide_017.js — builds the SINGLE-VERSION deliverable
// recreated_pptx/slide_017_recreated.pptx from the certified-bankable component.
//
// F5 POST-CERTIFICATION FIX (founder defect batch 2026-10-13, certified attempt 2):
// the four faint callout leader arrows are now drawn FULL-PATH with visible weight
// (2.25pt) and arrowheads inside components/slide_017.js (blocks leader1..4) —
// children 18/19 inherit via require(). Evidence: qa/slide017/arrow/, render_2.png,
// judge_attempt_2.txt (PASS).
//
// Run: cd /home/ahmed/Projects/ai_llm_slides && \
//      NODE_PATH=$(npm root -g) node videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_017.js

const path = require("path");
const PptxGenJS = require("pptxgenjs");
const { renderBase } = require(path.join(__dirname, "components", "slide_017.js"));

const OUT = path.join(__dirname, "..", "slide_017_recreated.pptx");

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in — house chrome expects this canvas
pptx.author = "slide-recreation worker";
pptx.title = "Encoder – Decoder Transformer (slide 17 recreation)";

const slide = pptx.addSlide();
renderBase(pptx, slide, { numeral: 17 });

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch((e) => {
  console.error("BUILD FAILED:", e);
  process.exit(1);
});
