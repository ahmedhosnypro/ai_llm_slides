// calib2_build.js — calibration round 2 (all boxes on-slide).
const pptxgen = require("pptxgenjs");
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide043/calib2.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const px = (v) => v / 72;

function line(slide, y, text, font, size, color, bold, ls, align) {
  slide.addText(text, {
    x: px(80), y: px(y), w: px(700), h: 0.6,
    align: align || "left", valign: "middle", margin: 0,
    fontFace: font, fontSize: size, bold: !!bold, color: color,
    lineSpacing: ls,
  });
}

const s1 = pres.addSlide();
s1.background = { color: "FFFFFF" };
line(s1, 60,  "will be 1x1", "Times New Roman", 21.2, "000080", false, 25);
line(s1, 160, "Original 5x5", "Times New Roman", 20.7, "000080", true, 25);
line(s1, 260, "Details are lost", "URW Gothic", 20.5, "3F3F3F", false, 25);
line(s1, 360, "After conv 1", "Comic Sans MS", 26, "000000", false, 25);
line(s1, 460, "Image", "Comic Sans MS", 26, "000000", false, 25);

const s2 = pres.addSlide();
s2.background = { color: "FFFFFF" };
line(s2, 60, "Problem: Image will vanish  if applying more filters in cascade", "Times New Roman", 28.8, "C00000", true, 37);
line(s2, 200, "18", "Verdana", 16, "000000", true, 25);
line(s2, 300, "x0", "Comic Sans MS", 10, "FF0000", false, 25);
line(s2, 400, "After conv 2", "Comic Sans MS", 26, "000000", false, 25);

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
