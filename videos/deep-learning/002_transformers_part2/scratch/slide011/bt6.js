const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq015_kq.png",
  x: 5.444, y: 0.8056, w: 1.5, h: 0.82 });
pres.writeFile({ fileName: __dirname + "/bt6.pptx" }).then(() => console.log("ok"));
