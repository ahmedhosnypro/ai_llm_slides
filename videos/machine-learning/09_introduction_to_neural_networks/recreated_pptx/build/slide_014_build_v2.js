const pptxgen = require("pptxgenjs");

const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const PX = 1 / 72;
const FONT = "Arial";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 518 * PX, w: 13.33, h: 22 * PX,
  fill: { color: "000000" }, line: { type: "none" },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("14", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Using Two Perceptron Layers", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "middle",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

function panel(x, y, w, h, fill, image) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    fill: { color: fill }, line: { color: "BFBFBF", width: 1 },
  });
  s.addImage({ path: BUILD + "/" + image, x: x * PX, y: y * PX, w: w * PX, h: h * PX });
}
panel(83, 100, 470, 205, "FFFFFF", "slide_014_main_diagram.png");
s.addShape(pres.shapes.RECTANGLE, {
  x: 83 * PX, y: 315 * PX, w: 515 * PX, h: 167 * PX,
  fill: { color: "FFFFFF" }, line: { color: "BFBFBF", width: 1 },
});
panel(607, 337, 284, 125, "FFFFE0", "slide_014_small_diagram.png");

function eq(name, x, y, w, h) {
  s.addImage({ path: BUILD + "/" + name + ".png", x: x * PX, y: y * PX, w, h });
}
function sumLabel(text, x, y) {
  s.addText(text, {
    x: x * PX, y: y * PX, w: 0.95, h: 0.28,
    align: "left", valign: "middle", fontSize: 16, bold: true,
    color: "C00000", fontFace: FONT, margin: 0,
  });
}
sumLabel("Sum 1", 85, 323);
sumLabel("Sum 2", 380, 323);
sumLabel("Sum 3", 85, 375);
eq("eq14_sum1", 155, 326, 1.94167, 0.22);
eq("eq14_sum2", 450, 326, 1.94167, 0.22);
eq("eq14_sum3", 155, 378, 5.295, 0.25667);
eq("eq14_expand", 140, 409, 5.63, 0.25667);
eq("eq14_linear", 140, 441, 1.855, 0.265);
s.addText("⇒", {
  x: 350 * PX, y: 438 * PX, w: 0.35, h: 0.28,
  align: "center", valign: "middle", fontSize: 16, bold: true,
  color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("Still Linear Equation", {
  x: 405 * PX, y: 438 * PX, w: 2.2, h: 0.28,
  align: "left", valign: "middle", fontSize: 12, italic: true, underline: true,
  color: "0000FF", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: BUILD + "/slide_014_recreated.pptx" })
  .then(() => console.log("wrote slide_014_recreated.pptx"));
