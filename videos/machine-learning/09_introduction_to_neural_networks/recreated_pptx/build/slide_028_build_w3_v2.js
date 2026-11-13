// Wave-3 build for slide 028: Neural Network Model.
// House chrome is native pptxgenjs; the measured architecture diagram is a
// generated matplotlib image from graphgen/slide_028_nn_model.py.
const pptxgen = require("pptxgenjs");
const path = require("path");

const B = __dirname;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";

s.addImage({
  path: path.join(B, "slide_028_nn_model.png"),
  x: 0, y: 0, w: W, h: H,
});

// Original video-capture strip: x38..921, y518..540 in the 960x540 frame.
s.addShape(pres.shapes.RECTANGLE, {
  x: 38 / 72, y: 518 / 72, w: 883 / 72, h: 22 / 72,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

// House frame.
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// House badge; numeral follows the approved slides_index.json / NNN instruction.
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("28", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

s.addText("Neural Network Model", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

const out = path.join(B, "slide_028_recreated.pptx");
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out));
