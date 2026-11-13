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
s.addText("8", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Multi-Class Classification using", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.34, align: "center", valign: "middle",
  fontSize: 24, bold: true, color: "C0392B", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "[ONE VS ALL] ", options: { color: "21618C" } },
  { text: "Binary Classifiers", options: { color: "C0392B" } },
], {
  x: 0.6, y: 0.62, w: 12.13, h: 0.34, align: "center", valign: "middle",
  fontSize: 24, bold: true, fontFace: FONT, margin: 0,
});

// Measured panel x167..798, y120..505; the PNG carries the region tints,
// hatching, boundaries, clusters, axes, ticks, and the single red panel border.
s.addImage({
  path: BUILD + "/slide_008_graph_v2.png",
  x: 167 * PX, y: 120 * PX, w: 632 * PX, h: 386 * PX,
});

function boxText(text, cx, cy, w, h, fill, lineColor, fontSize, color = "000000") {
  const opts = {
    x: (cx - w / 2) * PX, y: (cy - h / 2) * PX, w: w * PX, h: h * PX,
    align: "center", valign: "middle", fontSize, bold: true, color,
    fontFace: FONT, margin: 0,
  };
  s.addShape(pres.shapes.RECTANGLE, {
    x: opts.x, y: opts.y, w: opts.w, h: opts.h,
    fill: { color: fill }, line: { color: lineColor, width: 0.75 },
  });
  s.addText(text, opts);
}

boxText("C1", 546, 170, 38, 30, "F1C40F", "F1C40F", 16);
boxText("C2", 615, 312, 38, 30, "F1C40F", "F1C40F", 16);
boxText("C3", 281, 411, 38, 30, "F1C40F", "F1C40F", 16);
for (const [x, y] of [[280, 296], [455, 337], [645, 201], [470, 465]]) {
  boxText("?", x, y, 36, 36, "F5CBA7", "F5CBA7", 18);
}

s.addText("d1(x)", {
  x: 255 * PX, y: 198 * PX, w: 55 * PX, h: 24 * PX,
  align: "center", valign: "middle", fontSize: 12, bold: true,
  color: "C0392B", fontFace: FONT, margin: 0, rotate: 45,
});
s.addText("d3(x)", {
  x: 700 * PX, y: 213 * PX, w: 60 * PX, h: 24 * PX,
  align: "center", valign: "middle", fontSize: 12, bold: true,
  color: "008000", fontFace: FONT, margin: 0, rotate: -15,
});
for (const [x, y] of [[270, 330], [675, 137], [525, 472]]) {
  s.addText("+ve", {
    x: x * PX, y: y * PX, w: 42 * PX, h: 20 * PX,
    align: "center", valign: "middle", fontSize: 12, bold: true,
    color: "000000", fontFace: FONT, margin: 0,
  });
}

boxText("Undefined", 111, 148, 72, 20, "D5F5E3", "000000", 9);
s.addShape(pres.shapes.LINE, {
  x: 147 * PX, y: 153 * PX, w: 55 * PX, h: 45 * PX,
  line: { color: "B0B0B0", width: 0.5 },
});
s.addShape(pres.shapes.LINE, {
  x: 147 * PX, y: 153 * PX, w: 105 * PX, h: 225 * PX,
  line: { color: "B0B0B0", width: 0.5 },
});
boxText("New Class", 751, 383, 70, 20, "D7BDE2", "8E44AD", 9);

pres.writeFile({ fileName: BUILD + "/slide_008_recreated.pptx" })
  .then(() => console.log("wrote slide_008_recreated.pptx"));
