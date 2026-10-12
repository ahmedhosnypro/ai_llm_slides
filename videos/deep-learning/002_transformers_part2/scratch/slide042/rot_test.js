const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.addText("ROT270", { x: 3, y: 3, w: 1.5, h: 0.3, rotate: 270, fontSize: 12, color: "FF0000", align: "center", valign: "middle", margin: 0 });
s.addText("ROT315", { x: 6, y: 3, w: 1.5, h: 0.3, rotate: 315, fontSize: 12, color: "0000FF", align: "center", valign: "middle", margin: 0 });
s.addText("ROT0", { x: 9, y: 3, w: 1.5, h: 0.3, fontSize: 12, color: "00AA00", align: "center", valign: "middle", margin: 0 });
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide042/rot_test.pptx" }).then(() => console.log("ok"));
