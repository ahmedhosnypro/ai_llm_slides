const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

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
s.addText("31", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Example", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("Better Weights", {
  x: px(73), y: px(65), w: px(104), h: px(15),
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

const diagram = JSON.parse(fs.readFileSync(path.join(B, "slide_031_nn_diagram.json")));
s.addImage({
  path: path.join(B, diagram.image),
  x: diagram.position.x, y: diagram.position.y,
  w: diagram.width_in, h: diagram.height_in,
});

s.addText("Forward", {
  x: px(70), y: px(245), w: px(110), h: px(22),
  align: "left", valign: "middle",
  fontSize: 16, bold: true, italic: true, color: "0000FF", fontFace: FONT, margin: 0,
});

function box(x, y, w, h, fill, line) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill }, line: { color: line, width: 1.5 },
  });
}

function eq(name, x, y) {
  const side = JSON.parse(fs.readFileSync(path.join(B, name.replace(".png", ".json"))));
  s.addImage({ path: path.join(B, name), x: px(x), y: px(y), w: side.w_in, h: side.h_in });
}

box(72, 267, 360, 137, "FBFDE8", "000080");
eq("eq_net3.png", 82, 281);
eq("eq_net4.png", 81, 328);
eq("eq_net5.png", 82, 375);
box(72, 418, 557, 89, "FBFDE8", "000080");
eq("eq_net6.png", 78, 430);
eq("eq_net7.png", 78, 472);
box(638, 265, 241, 141, "EFFFE2", "008000");
eq("eq_O3.png", 657, 273);
eq("eq_O4.png", 657, 318);
eq("eq_O5.png", 657, 363);
box(638, 416, 241, 93, "EFFFF2", "008000");
eq("eq_O6.png", 663, 424);
eq("eq_O7.png", 660, 468);

const outPath = path.join(B, "slide_031_recreated.pptx");
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));
