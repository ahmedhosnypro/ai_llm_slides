// Slide 047 GRAPHED recreation — "Nearest Neighbors (NN) Equal Distance"
// Second version (advanced-graph worker). The certified native build
// (build/slide_047.js) and slide_047_recreated.pptx stay UNTOUCHED.
// House chrome (frame, badge, title, captions) preserved; the native graph
// block (axes + dots + spokes + rings) is replaced by ONE embedded PNG
// generated with matplotlib from the banked measured constants
// (build/assets/graphs/s47_graph_v2.png, 300dpi, 1px=1pt).
// Graph region: slide px x 94..850, y 160..484 -> addImage x=1.3056 y=2.2222
// w=10.5 h=4.5 (in). Captions moved from y 5.85 to y 6.75 (original captions
// sit at y~484px = 6.72in; certified y would overlap the image's tan cluster).
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

// Palette (NO "#" prefix — corrupts the file)
const BG = "E8E8E8";       // house slide background
const RED = "C00000";      // house outer frame
const INK = "333333";      // badge numeral
const BADGE = "FFF9C4";    // badge fill (house)
const TITLE_RED = "CC0000";  // spec: 'Nearest Neighbors' red
const TITLE_BLUE = "0000CC"; // spec: '(NN) Equal Distance' blue
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer chrome (identical to certified build) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
// Slide-number badge: oval, numeral "47" (printed number on the original image)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("47", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Title (house rule: y:0.28, x:0.6, w:12.13, centered) ----
s.addText(
  [
    { text: "Nearest Neighbors", options: { bold: true, color: TITLE_RED, fontFace: FONT } },
    { text: " (NN) Equal Distance", options: { bold: true, color: TITLE_BLUE, fontFace: FONT } },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 0.75,
    align: "center", valign: "middle",
    fontSize: 28, margin: 0,
  }
);

// ---- GENERATED GRAPH (embedded PNG; replaces the native graph block) ----
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s47_graph_v2.png",
  x: 1.3056, y: 2.2222, w: 10.5, h: 4.5,
});

// ---- Captions (verbatim; moved to y 6.75 to clear the image) ----
s.addText("Data of Three Classes", {
  x: 1.7, y: 6.75, w: 4.5, h: 0.4,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});
s.addText("No Unique Nearest Neighbor", {
  x: 7.25, y: 6.75, w: 4.5, h: 0.4,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_047_recreated.pptx" })
  .then(() => console.log("done"));
