const fs = require("fs");
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
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("8", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Multi-Class Classification using", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.34, align: "center", valign: "middle",
  fontSize: 24, bold: true, color: "CC2222", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "[ONE VS ALL] ", options: { color: "0000FF", bold: true, fontSize: 24, fontFace: FONT } },
  { text: "Binary Classifiers", options: { color: "CC2222", bold: true, fontSize: 24, fontFace: FONT, breakLine: true } },
], {
  x: 0.6, y: 0.62, w: 12.13, h: 0.34, align: "center", valign: "middle",
  fontSize: 24, bold: true, fontFace: FONT, margin: 0,
});

s.addImage({
  path: BUILD + "/slide_008_graph_v2.png",
  x: 167 * PX, y: 120 * PX, w: 632 * PX, h: 386 * PX,
});

function rect(x, y, w, h, fill, lineColor, lineWidth) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    fill: { color: fill }, line: { color: lineColor, width: lineWidth },
  });
}

function text(runs, x, y, w, h, fontSize, color) {
  s.addText(runs, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    align: "center", valign: "middle", fontSize, bold: true, color,
    fontFace: FONT, margin: 0,
  });
}

function classTag(n, x, y, w, h) {
  rect(x, y, w, h, "FFFF00", "FFFF00", 0.25);
  text([
    { text: "C", options: { color: "000000", bold: true, fontSize: 16, fontFace: FONT } },
    { text: String(n), options: { color: "000000", bold: true, fontSize: 16, fontFace: FONT, subscript: true, breakLine: true } },
  ], x, y, w, h, 16, "000000");
}

function questionBox(x, y, w, h) {
  rect(x, y, w, h, "FFE0CC", "FFE0CC", 0.25);
  text([{ text: "?", options: { color: "FF3300", bold: true, fontSize: 18, fontFace: FONT, breakLine: true } }],
       x, y, w, h, 18, "FF3300");
}

classTag(1, 525, 153, 43, 35);
classTag(2, 594, 295, 43, 35);
classTag(3, 260, 395, 43, 35);
questionBox(434, 318, 44, 36);
questionBox(591, 177, 42, 33);
questionBox(243, 264, 40, 33);
questionBox(422, 418, 40, 34);

text([{ text: "?", options: { color: "FF00FF", bold: true, fontSize: 10, fontFace: FONT, breakLine: true } }],
     475, 301, 16, 20, 10, "FF00FF");

function mathLabel(name, cx, cy, rotate) {
  const side = JSON.parse(fs.readFileSync(BUILD + "/assets/eq_008_" + name + ".json", "utf8"));
  s.addImage({
    path: BUILD + "/assets/eq_008_" + name + ".png",
    x: cx * PX - side.w_in / 2,
    y: cy * PX - side.h_in / 2,
    w: side.w_in,
    h: side.h_in,
    rotate,
  });
}
mathLabel("d1", 272.5, 194.5, 35);
mathLabel("d2", 576, 154, -40);
mathLabel("d3", 725, 212, -15);

for (const [x, y, w, h] of [[638, 131, 35, 16], [251, 312, 38, 16], [494, 448, 37, 16]]) {
  text([{ text: "+ve", options: { color: "000000", bold: true, fontSize: 12, fontFace: FONT, breakLine: true } }],
       x, y, w, h, 12, "000000");
}

rect(73, 131, 75, 30, "FFFFFF", "0000FF", 0.75);
text([{ text: "Undefined", options: { color: "0000FF", bold: true, fontSize: 9, fontFace: FONT, breakLine: true } }],
     73, 131, 75, 30, 9, "0000FF");
s.addShape(pres.shapes.LINE, { x: 147 * PX, y: 140 * PX, w: 53 * PX, h: 12 * PX, line: { color: "0000FF", width: 0.5 } });
s.addShape(pres.shapes.LINE, { x: 147 * PX, y: 152 * PX, w: 96 * PX, h: 12 * PX, line: { color: "0000FF", width: 0.5 } });

rect(715, 372, 72, 24, "FFFFFF", "FF00FF", 0.75);
text([{ text: "New Class", options: { color: "FF00FF", bold: true, fontSize: 9, fontFace: FONT, breakLine: true } }],
     715, 372, 72, 24, 9, "FF00FF");

pres.writeFile({ fileName: BUILD + "/slide_008_recreated.pptx" })
  .then(() => console.log("wrote slide_008_recreated.pptx"));
