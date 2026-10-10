// Slide 046 GRAPHED recreation: "Nearest Neighbors (NN) Outlier Problem" (blob variant)
// Second version (advanced-graph worker). The certified native build
// (build/slide_046.js) and slide_046_recreated.pptx stay UNTOUCHED.
// House chrome (frame, badge, title, 'Outlier Sample' label box, pointer,
// captions) preserved; the native graph block (axes + ovals + blob ovals +
// fan lines + arrows) is replaced by ONE embedded PNG generated with
// matplotlib from the banked measured constants
// (build/assets/graphs/s46_graph_v2.png, 300dpi, 1px=1pt).
// Graph region: slide px x 94..850, y 160..484 -> addImage x=1.3056 y=2.2222
// w=10.5 h=4.5 (in). Captions moved y 6.55 -> 6.75 to clear the image's
// axis rows. Pointer endpoint re-targeted to the generated outlier at
// (713,213) slide px -> (9.903, 2.958) in.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// House template constants (founder directive — override spec for chrome)
const BG = "E8E8E8", RED = "C00000", BADGE_YELLOW = "FFF9C4", INK = "333333";
// Spec palette (content colors from slide_046_final.json)
const TITLE_RED = "B22222", BLUE = "0000CC",
      BOX_FILL = "E8F5E9", BOX_GREEN = "4CAF50", GRAY = "999999";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer red frame ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// ---- House slide-number badge: numeral 46 ----
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("46", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Title (split-colored per spec, house geometry) ----
s.addText([
  { text: "Nearest Neighbors", options: { color: TITLE_RED } },
  { text: " (NN) Outlier Problem", options: { color: BLUE } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.85, align: "center", valign: "top",
  fontSize: 30, bold: true, fontFace: FONT, margin: 0,
});

// plain segment (no arrowheads): bounding box + flip for the anti-diagonal
const seg = (x1, y1, x2, y2, line) => {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  const flipV = (x2 - x1) * (y2 - y1) < 0;
  s.addShape(pptx.shapes.LINE, { x, y, w, h, flipV, line });
};

// ---- GENERATED GRAPH (embedded PNG; replaces the native graph block) ----
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s46_graph_v2.png",
  x: 1.3056, y: 2.2222, w: 10.5, h: 4.5,
});

// ---- 'Outlier Sample' label box (native chrome, drawn after the image) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.55, y: 1.25, w: 0.95, h: 0.55,
  fill: { color: BOX_FILL }, line: { color: BOX_GREEN, width: 1 },
});
s.addText([
  { text: "Outlier", options: { breakLine: true } },
  { text: "Sample", options: {} },
], {
  x: 7.55, y: 1.25, w: 0.95, h: 0.55, align: "center", valign: "middle",
  fontSize: 9, color: INK, fontFace: FONT, margin: 0,
});

// thin gray pointer line from the label box to the generated red outlier
// (713,213) slide px = (9.903, 2.958) in; minus small offset like certified
seg(8.35, 1.82, 9.85, 2.88, { color: GRAY, width: 1 });

// ---- Captions (verbatim; moved to y 6.75 to clear the image) ----
s.addText("Data of Three Classes", {
  x: 1.33, y: 6.75, w: 5.07, h: 0.5, align: "center", valign: "top",
  fontSize: 18, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});
s.addText("Nearest Neighbor is the Green class", {
  x: 6.93, y: 6.75, w: 5.33, h: 0.5, align: "center", valign: "top",
  fontSize: 18, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

pptx
  .writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/ml-intro/recreated_pptx/slide_046_recreated.pptx" })
  .then(() => console.log("done"));
