const pptxgen = require("pptxgenjs");
const path = require("path");

const B = __dirname;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";
const px = v => v / 72;

s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("17", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Linear and Unit Step Activation Functions", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

for (const [file, x, y] of [
  ["slide_025_linear_w3.png", 309, 120],
  ["slide_025_unipolar_step_w3.png", 137, 289],
  ["slide_025_bipolar_step_w3.png", 487, 289],
]) {
  s.addImage({ path: path.join(B, file), x: px(x), y: px(y), w: 797 / 200, h: 411 / 200 });
}

s.addShape(pres.shapes.LINE, {
  x: px(655), y: px(119), w: px(58), h: px(47),
  line: { color: "FF0000", width: 3 },
});
s.addShape(pres.shapes.LINE, {
  x: px(655), y: px(119), w: px(58), h: px(47), flipV: true,
  line: { color: "FF0000", width: 3 },
});

for (const [x, y, w, h] of [
  [605, 176, 277, 26],
  [115, 457, 300, 51],
  [494, 457, 306, 51],
]) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: "FAE9D7" }, line: { color: "C59C98", width: 2.25 },
  });
}

for (const [file, x, y, w, h] of [
  ["eq_017_linear.png", 605, 176, 2325, 225],
  ["eq_017_unipolar.png", 117, 459, 2475, 400],
  ["eq_017_bipolar.png", 496, 459, 2525, 400],
]) {
  s.addImage({ path: path.join(B, file), x: px(x), y: px(y), w: w / 600, h: h / 600 });
}

const out = path.join(B, "slide_025_recreated.pptx");
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out));
