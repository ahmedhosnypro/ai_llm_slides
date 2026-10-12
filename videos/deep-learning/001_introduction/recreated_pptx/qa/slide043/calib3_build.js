const pptxgen = require("pptxgenjs");
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide043/calib3.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const px = (v) => v / 72;
const s1 = pres.addSlide();
s1.background = { color: "FFFFFF" };
function line(y, text, font, size, color, bold, ls, x, w, align) {
  s1.addText(text, { x: px(x), y: px(y), w: px(w), h: 0.6, align: align || "left", valign: "middle",
    margin: 0, fontFace: font, fontSize: size, bold: !!bold, color: color, lineSpacing: ls });
}
line(60,  "Problem: Image will vanish  if applying more filters in cascade", "Times New Roman", 28.8, "C00000", true, 37, 48, 864, "center");
line(160, "After apply one filter  of size 3x3, output will be3x3", "Times New Roman", 21.2, "000080", false, 25, 80, 700);
line(260, "After applying second filter on the output (cascaded filters)", "Times New Roman", 21.0, "000080", false, 25, 80, 700);
line(360, "Output will be 1x1", "Times New Roman", 20.5, "000080", false, 25, 80, 700);
line(460, "Our images get smaller and smaller", "URW Gothic", 20.5, "3F3F3F", false, 25, 80, 700);
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
