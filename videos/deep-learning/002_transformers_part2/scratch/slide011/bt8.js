const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/yellowtest.png", x: 1, y: 1, w: 1, h: 1 });
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/yellowtest_opaque.png", x: 3, y: 1, w: 1, h: 1 });
pres.writeFile({ fileName: __dirname + "/bt8.pptx" }).then(() => console.log("ok"));
