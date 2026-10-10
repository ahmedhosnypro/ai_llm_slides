// Slide 60 recreation build — "IRIS Dataset" (ml-intro deck)
// Spec: videos/ml-intro/analysis/slide_060_final.json
// All content coordinates measured from the original 960x540 frame (72 px/in
// on a 13.33x7.5in slide), so px/72 gives inches directly.
// House chrome (founder directive, overrides spec): bg E8E8E8, red frame
// x:0.15 y:0.15 w:13.03 h:7.2 line C00000 1.5pt, badge oval x:12.48 y:0.30
// w:0.5 h:0.5 fill FFF9C4 numeral bold 18pt 333333, title box y:0.28 x:0.6
// w:12.13 centered.
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette (from spec JSON; NEVER prefix hex with '#')
const BG = "E8E8E8";        // house slide background
const FRAME = "C00000";    // house outer frame
const BADGE = "FFF9C4";    // house badge fill/line
const INK = "333333";      // house badge numeral
const TITLE = "0000CD";    // title + footer text blue
const PANEL_LINE = "8B0000"; // panel maroon borders
const BLACK = "000000";
const WHITE = "FFFFFF";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House chrome ----
// Outer red frame (no visible fill: same as background)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});
// Slide-number badge: yellow oval, numeral "60" (number printed on the
// original slide image)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("60", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
// Title (house box; content per spec: blue bold "IRIS Dataset")
s.addText("IRIS Dataset", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 30, bold: true, color: TITLE, fontFace: FONT, margin: 0,
});

// ---- Three species panels ----
// Panel rects measured from the original frame:
// p1 x 69..321px, p2 x 339..590px, p3 x 623..873px; y 139..482px
const PANEL_Y = 1.931, PANEL_H = 4.78;
const panels = [
  { x: 0.958, w: 3.50, header: "iris setosa",
    img: "videos/ml-intro/recreated_pptx/build/assets/slide060_photo1.png",
    imgX: 1.000, imgW: 3.431,
    petal: 2.236, sepal: 3.389 },
  { x: 4.708, w: 3.50, header: "iris versicolor",
    img: "videos/ml-intro/recreated_pptx/build/assets/slide060_photo2.png",
    imgX: 4.750, imgW: 3.417,
    petal: 6.097, sepal: 7.597 },
  { x: 8.653, w: 3.472, header: "iris virginica",
    img: "videos/ml-intro/recreated_pptx/build/assets/slide060_photo3.png",
    imgX: 8.681, imgW: 3.417,
    petal: 10.042, sepal: 11.222 },
];

for (const p of panels) {
  // Red/maroon-bordered panel box
  s.addShape(pptx.shapes.RECTANGLE, {
    x: p.x, y: PANEL_Y, w: p.w, h: PANEL_H,
    fill: { color: WHITE }, line: { color: PANEL_LINE, width: 1 },
  });
  // Bold black class-name header, centered at the top of the panel
  s.addText(p.header, {
    x: p.x, y: 2.03, w: p.w, h: 0.35, align: "center", valign: "middle",
    fontSize: 20, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
  // Flower photograph (crop of the original panel interior, incl. the
  // original 'petal'/'sepal' leader lines), placed at its measured position
  s.addImage({
    path: p.img, x: p.imgX, y: 2.542, w: p.imgW, h: 3.611,
  });
  // 'petal' / 'sepal' labels beneath the photo, at their measured centers
  // (leader lines come down from the photo crop to just above these)
  s.addText("petal", {
    x: p.petal - 0.4, y: 6.17, w: 0.8, h: 0.28, align: "center", valign: "top",
    fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
  });
  s.addText("sepal", {
    x: p.sepal - 0.4, y: 6.17, w: 0.8, h: 0.28, align: "center", valign: "top",
    fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ---- Footer banner ----
// Blue-bordered strip with the blue bold summary sentence (spec step 20-21;
// geometry measured: text x 153..819px, rows 501..515px)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.92, y: 6.81, w: 9.67, h: 0.49,
  fill: { color: WHITE }, line: { color: TITLE, width: 1 },
});
s.addText("150 Samples, 3 Classes, features of petal and sepal parts of each flower", {
  x: 1.92, y: 6.81, w: 9.67, h: 0.49, align: "center", valign: "middle",
  fontSize: 16, bold: true, color: TITLE, fontFace: FONT, margin: 0,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_060_recreated.pptx" })
  .then((f) => console.log("written:", f));
