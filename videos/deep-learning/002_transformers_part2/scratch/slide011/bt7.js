const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/beam011.png",
  x: 1, y: 1, w: 2, h: 0.9 });
pres.writeFile({ fileName: __dirname + "/bt7.pptx" }).then(() => console.log("ok"));
