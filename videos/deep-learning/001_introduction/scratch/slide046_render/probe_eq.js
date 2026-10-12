const pptxgen = require("pptxgenjs");
const px = (v) => v / 72;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };
function topFor(baseline, ls, size, ascent = 0.9053) {
  return baseline - (43.2 - ls) / 2 - ascent * size;
}
[[365,60],[375,180],[385,300]].forEach(([bl, x]) => {
  slide.addText("=", { x: px(x), y: px(topFor(bl, 24, 24)), w: px(40), h: 0.6,
    align: "left", valign: "middle", margin: 0, fontFace: "Arial", fontSize: 24,
    color: "000000", lineSpacing: 24 });
});
[[365,380],[375,460]].forEach(([bl, x]) => {
  slide.addText("(", { x: px(x), y: px(topFor(bl, 24, 20, 0.891)), w: px(20), h: 0.6,
    align: "left", valign: "middle", margin: 0, fontFace: "Times New Roman", fontSize: 20,
    italic: true, color: "000000", lineSpacing: 24 });
});
pres.writeFile({ fileName: process.argv[2] }).then(() => console.log("ok"));
