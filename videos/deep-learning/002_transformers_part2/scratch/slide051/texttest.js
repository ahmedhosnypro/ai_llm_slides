const pptxgen = require("pptxgenjs");
const p = new pptxgen(); p.layout = "LAYOUT_WIDE";
const s = p.addSlide(); s.background = { color: "FFFFFF" };
const variants = [
  [0.5, 5.5, "Add & Norm", "6D99B4", "1B3A5C"],
  [2.5, 6.5, "Add & Norm", "6D99B4", "1B3A5C"],
  [4.5, 7.0, "Add & Norm", "6D99B4", "1B3A5C"],
  [0.5, 5.5, "Add \u0026 Norm", "5C9CB7", "1B3A5C"],
  [2.5, 5.5, "Add & Norm", "5C9CB7", "1B3A5C"],
  [4.5, 5.5, "Add & Norm", "6E87E0", "2E3E8C"],
];
for (const [x, fs, t, fill, col] of variants) {
  s.addShape("rect", { x, y: 0.5, w: 0.91, h: 0.145, fill: { color: fill }, line: { color: fill, width: 0.5 } });
  s.addText(t, { x, y: 0.5, w: 0.91, h: 0.145, align: "center", valign: "middle", margin: 0, fontFace: "Arial", fontSize: fs, bold: true, color: col });
}
p.writeFile({ fileName: "texttest.pptx" }).then(() => console.log("ok"));
