// calib_build.js — LO baseline-model calibration for slide 043 fonts.
// One slide, single-line boxes (h 0.6in = 43.2px, lineSpacing 25), tops at known px.
// After render, PIL-measures ink bands -> derive per-font ascent A in
//   baseline = top + (43.2 - ls)/2 + A * fontSize
// and ink-center offsets for the diagram labels.
const pptxgen = require("pptxgenjs");
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide043/calib.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

const px = (v) => v / 72;
const lines = [
  { y: 60,  text: "After conv 1", font: "Comic Sans MS", size: 24, color: "000000", bold: false },
  { y: 160, text: "Image",        font: "Comic Sans MS", size: 24, color: "000000", bold: false },
  { y: 260, text: "x1",           font: "Comic Sans MS", size: 10, color: "FF0000", bold: false },
  { y: 360, text: "1",            font: "Verdana", size: 16, color: "000000", bold: true },
  { y: 460, text: "0",            font: "Verdana", size: 16, color: "000000", bold: true },
  { y: 560, text: "will be 1x1",  font: "Times New Roman", size: 21.2, color: "000080", bold: false },
  { y: 660, text: "Details are lost", font: "URW Gothic", size: 20.5, color: "3F3F3F", bold: false },
  { y: 760, text: "18",           font: "Verdana", size: 16, color: "000000", bold: true },
];
lines.forEach((L) => {
  slide.addText(L.text, {
    x: px(80), y: px(L.y), w: px(600), h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontFace: L.font, fontSize: L.size, bold: L.bold, color: L.color,
    lineSpacing: 25,
  });
});
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
