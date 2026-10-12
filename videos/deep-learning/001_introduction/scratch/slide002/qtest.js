const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };
s.addText("Quick revision of Neural Network", {
  x: 1.9, y: 1.0, w: 10.9, h: 0.6, align: "left", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 30.6, bold: true, color: "0000AA", lineSpacing: 34,
});
s.addText("Quick revision of Neural Network", {
  x: 1.9, y: 2.0, w: 10.9, h: 0.6, align: "left", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 30.6, bold: true, color: "0000AA",
});
pres.writeFile({ fileName: process.env.QTEST });
