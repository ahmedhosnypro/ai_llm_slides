// Pattern: house-chrome + measured slide 001 content geometry
// Build: NODE_PATH=$(npm root -g) node slide_001_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 1;
const FONT = "Times New Roman";  // serif for lower half per judge
const TITLE_FONT = "Arial";      // title remains sans-serif
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };  // house template background

// 1. outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: TITLE_FONT, margin: 0,
});

// 3. title box - TWO LINES per original (line break after "Introduction to")
// Judge: title ~44pt, line spacing ~1.35x cap-to-cap
s.addText("Introduction to", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6,
  align: "center", valign: "top",
  fontSize: 44, bold: true, color: "C00000", fontFace: TITLE_FONT, margin: 0,
});
s.addText("Artificial Neural Networks (ANN)", {
  x: 0.6, y: 0.88, w: 12.13, h: 0.6,
  align: "center", valign: "top",
  fontSize: 44, bold: true, color: "C00000", fontFace: TITLE_FONT, margin: 0,
});

// 4. course code, measured original ink y=3.833-4.125in
s.addText("CSAI 253 - Spring 2024", {
  x: 0.6, y: 3.74, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "000080", fontFace: TITLE_FONT, margin: 0,
});

// 5. Prepared By block, measured original ink y=4.708-5.569in
s.addText("Prepared By", {
  x: 0.6, y: 4.60, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 22, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 0.6, y: 4.94, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 22, bold: true, italic: true, color: "000080", fontFace: FONT, margin: 0, charSpacing: 0.2,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 0.6, y: 5.30, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 18, italic: true, color: "000080", fontFace: FONT, margin: 0,
});

// 6. Instructors list, measured original ink y=5.625-7.083in, x=1.194-5.236in
const instLabelX = 1.19;
const instX = 1.72;
s.addText("Instructors:", {
  x: instLabelX, y: 5.52, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 22, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0, charSpacing: 0.55,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: instX, y: 5.90, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: "000080", fontFace: FONT, margin: 0, charSpacing: 0.3,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: instX, y: 6.22, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 16, italic: true, color: "000080", fontFace: FONT, margin: 0, charSpacing: 0.15,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: instX, y: 6.50, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: "000080", fontFace: FONT, margin: 0, charSpacing: 0.2,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: instX, y: 6.82, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 16, italic: true, color: "000080", fontFace: FONT, margin: 0, charSpacing: 0.15,
});

// 7. University logo, measured original x=8.25-12.54in, y=6.125-7.069in; teal tile x=8.25-9.36in
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.25, y: 6.125, w: 4.29, h: 0.944,
  fill: { color: "FFFFFF" },
  line: { color: "808080", width: 0.75 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.25, y: 6.125, w: 1.11, h: 0.944,
  fill: { color: "008080" },
  line: { type: "none" },
});
s.addImage({ path: "assets/logo_emblem_001.png", x: 8.30, y: 6.16, w: 1.01, h: 0.48 });
s.addText("ZEWAIL CITY", {
  x: 8.25, y: 6.66, w: 1.11, h: 0.22,
  align: "center", valign: "top",
  fontSize: 12, bold: true, color: "FFFFFF", fontFace: TITLE_FONT, margin: 0,
});
s.addText("SCIENCE & TECHNOLOGY", {
  x: 8.25, y: 6.90, w: 1.11, h: 0.14,
  align: "center", valign: "top",
  fontSize: 6, color: "FFFFFF", fontFace: TITLE_FONT, margin: 0,
});
s.addText("جامعة العلوم والتكنولوجيا زويل", {
  x: 9.45, y: 6.36, w: 3.0, h: 0.3,
  align: "left", valign: "top",
  fontSize: 12, bold: true, color: "8B0000", fontFace: "Arial", margin: 0,
});
s.addText("University of Science and Technology", {
  x: 9.45, y: 6.68, w: 3.0, h: 0.25,
  align: "left", valign: "top",
  fontSize: 10, color: "000000", fontFace: TITLE_FONT, margin: 0,
});

// 8. Bottom black band, measured original x=0.528-12.792in, y=7.208-7.486in
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.528, y: 7.208, w: 12.264, h: 0.278,
  fill: { color: "000000" },
  line: { type: "none" },
});

pres.writeFile({ fileName: "slide_001_recreated.pptx" }).then(() => console.log("wrote slide_001_recreated.pptx"));