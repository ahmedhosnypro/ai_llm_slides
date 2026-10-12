// Throwaway chain-load verification: require the certified 16->9 component chain,
// render slide_016's composition (with numeral 17, its callouts skipped to preview
// the 17 base), write a pptx. Success = chain loads + pptx written.
const pptxgen = require("pptxgenjs");
const P16 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_016.js");
const P9 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_009.js");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
P16.renderBase(pres, slide, {
  numeral: "17",
  skip: ["callout_inspection_016","callout_handcrafted_016","callout_decision_016","callout_apply_016"],
});
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide017/chainverify/chain_verify.pptx" })
  .then(() => console.log("CHAIN VERIFY OK: pptx written"))
  .catch((e) => { console.error("CHAIN FAIL:", e); process.exit(1); });
