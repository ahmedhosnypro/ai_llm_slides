const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/beam2.png",
  x: 5.444, y: 0.8056, w: 4.3056, h: 1.7361 });
pres.writeFile({ fileName: __dirname + "/beamtest.pptx" }).then(() => console.log("ok"));
