// Slide 045 GRAPHED recreation: "Nearest Neighbors (NN) Outlier Problem"
// Second version (advanced-graph worker). The certified native build
// (build/slide_045.js) and slide_045_recreated.pptx stay UNTOUCHED.
// House chrome (frame, badge, title, captions) identical to the certified
// build. The native graph block (axes + 25 oval dots + 26 lines + 26 ticks +
// dashed ring) is replaced by ONE embedded PNG generated with matplotlib +
// sklearn.neighbors.KDTree from the banked measured scene-A constants
// (build/assets/graphs/s45_graph_v3.png, 300dpi, 1px=1pt, vision-gate PASS x2:
// graph_check_3.txt + graph_check_4.txt).
// Graph region: slide px x 94..850, y 160..484 -> addImage x=94/72=1.3056in,
// y=160/72=2.2222in, w=756/72=10.5in, h=324/72=4.5in.
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

const BG = "E8E8E8";        // house background
const FRAME = "C00000";     // house frame line color
const DARKRED = "B22222";   // title part 1, captions, borders (spec)
const BLUE = "0000CC";      // title part 2 (spec)
const INK = "333333";       // badge numeral (house)
const BADGE = "FFF9C4";     // badge fill (house)
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer chrome (identical to certified build) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.25, y: 0.25, w: 12.83, h: 7.0,
  fill: { color: "FFFFFF" }, line: { color: DARKRED, width: 1 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 11.7, h: 0.65,
  fill: { color: "FFFFFF", transparency: 100 }, line: { color: DARKRED, width: 1 },
});
s.addText(
  [
    { text: "Nearest Neighbors ", options: { color: DARKRED } },
    { text: "(NN) Outlier Problem", options: { color: BLUE } },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 0.65, align: "center", valign: "middle",
    fontSize: 30, bold: true, fontFace: FONT, margin: 0,
  }
);
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("45", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- GENERATED GRAPH (embedded PNG; replaces the native graph block) ----
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s45_graph_v3.png",
  x: 1.3056, y: 2.2222, w: 10.5, h: 4.5,
});

// ---- Captions (verbatim, unchanged from certified build) ----
s.addText("Data of Three Classes", {
  x: 1.09, y: 6.72, w: 5.34, h: 0.45, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
});
s.addText("Nearest Neighbor is the Green class", {
  x: 6.61, y: 6.72, w: 5.34, h: 0.45, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_045_recreated.pptx" })
  .then(() => console.log("done"));
