const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", YELLOW = "FFF2A8", INK = "333333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// Title: red, bold, centered on full slide width, two lines
s.addText("Programming Languages, Platforms,\nand Libraries", {
  x: 0.6, y: 0.35, w: W - 1.2, h: 1.5, align: "center", valign: "middle",
  fontSize: 34, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Slide number badge: yellow circle, dark outline, top-right
s.addShape(pptx.shapes.OVAL, {
  x: 12.25, y: 0.3, w: 0.65, h: 0.65,
  fill: { color: YELLOW }, line: { color: INK, width: 1.5 },
});
s.addText("7", {
  x: 12.25, y: 0.3, w: 0.65, h: 0.65, align: "center", valign: "middle",
  fontSize: 22, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Red-outlined content box, left half below title
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.65, y: 1.95, w: 5.7, h: 5.05, fill: { color: BG }, line: { color: RED, width: 2 },
});

const bu = () => ({ code: "2022", indent: 12 });
function section(y, header, items) {
  s.addText(header, {
    x: 0.95, y, w: 5.1, h: 0.3, fontSize: 19, bold: true, color: RED,
    fontFace: FONT, margin: 0,
  });
  const rows = items.map((t, i) => ({
    text: t, options: { bullet: bu(), breakLine: i < items.length - 1 },
  }));
  s.addText(rows, {
    x: 1.1, y: y + 0.3, w: 5.0, h: 0.29 * items.length, fontSize: 17,
    color: TEXT, fontFace: FONT, margin: 0, paraSpaceAfter: 4, valign: "top",
  });
}

section(2.2, "Popular Languages for ML/DL", ["Python", "R", "Matlab"]);
section(3.5, "Popular Platforms for ML/DL", ["Tensor Flow", "Pytorch"]);
section(4.5, "Popular Libraries (for python)", [
  "SciKit Learn", "SciPy", "NLTK", "Spacy", "Gensim", "OpenCV",
]);

// Handwritten '+ Keras' annotation beside 'Tensor Flow'
s.addText("+ Keras", {
  x: 2.7, y: 3.85, w: 1.6, h: 0.35, fontSize: 17, italic: true,
  color: INK, fontFace: "Comic Sans MS", margin: 0,
});

pptx.writeFile({ fileName: "analysis/slide_007_recreation.pptx" }).then(() => console.log("done"));
