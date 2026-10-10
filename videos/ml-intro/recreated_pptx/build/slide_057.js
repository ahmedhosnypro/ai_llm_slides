// Slide 057 — "Choice of K - Neighborhood Size" (KNN decision-boundary trio)
// Source spec: analysis/slide_057_final.json  (house frame per 17_worker_instructions.md)
// Build attempt 3: interleaved diagonal red/green swath per judge findings
// (comparisons a1/a2 of render_1.png), ring at spec (1.3, 1.6) clear of all points.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// House template (founder directive — overrides spec)
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE = "FFF9C4", INK = "333333";
// Content colors (verbatim from spec)
const BAND = "E6E6E6", TITLE_RED = "B00020", TEXT = "000000";
const PINK = "F4A6A6", LGREEN = "B7F0B1", PERI = "C9C9F2";
const PT_RED = "FF0000", PT_GREEN = "00CC00", PT_BLUE = "0000CC", GRAY = "808080";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- Header band (spec region: light gray E6E6E6, top ~0-18%) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 1.15, fill: { color: BAND }, line: { type: "none" },
});

// ---- House outer red frame (transparent fill, C00000 1.5pt) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG, transparency: 100 }, line: { color: FRAME_RED, width: 1.5 },
});

// ---- Title (house: y 0.28, x 0.6, w 12.13, centered) ----
s.addText("Choice of K - Neighborhood Size", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "middle",
  fontSize: 30, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ---- House slide-number badge: oval 12.48/0.30/0.5/0.5, numeral "57" ----
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("57", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Graphed version: native mosaic/ticks/labels/points approximation REPLACED by
// addImage of the sklearn+matplotlib generated panels (graphgen/slide_057_knn.py,
// attempt v3; PIL-aligned to the original's measured placement within 4px; graph
// vision leg PASS, transcript qa/slide057/graphgen/graph_check_1.txt).
// Panel image rects measured from the original frame (1px = 1pt = 1/72in):
//   P1 x94..346, P2 x348..606, P3 x611..869, all y230..429.
// Captions ("K = N") stay native text, repositioned to the measured spots
// (ink centered ~(232,224), (493.5,224), (755,224) px).
const PANELS = [
  { k: 1,  img: "videos/ml-intro/recreated_pptx/build/assets/graphs/s057_graph_v3_P1.png",
    x: 94 / 72,  y: 230 / 72, w: 252 / 72, h: 199 / 72, cap: 232 / 72 },
  { k: 3,  img: "videos/ml-intro/recreated_pptx/build/assets/graphs/s057_graph_v3_P2.png",
    x: 348 / 72, y: 230 / 72, w: 258 / 72, h: 199 / 72, cap: 493.5 / 72 },
  { k: 31, img: "videos/ml-intro/recreated_pptx/build/assets/graphs/s057_graph_v3_P3.png",
    x: 611 / 72, y: 230 / 72, w: 258 / 72, h: 199 / 72, cap: 755 / 72 },
];

PANELS.forEach((p) => {
  s.addImage({ path: p.img, x: p.x, y: p.y, w: p.w, h: p.h });
  s.addText([
    { text: "K", options: { italic: true } },
    { text: " = " + p.k, options: {} },
  ], {
    x: p.cap - 0.7, y: 224 / 72 - 0.14, w: 1.4, h: 0.28, align: "center", valign: "middle",
    fontSize: 14, italic: true, color: TEXT, fontFace: FONT, margin: 0,
  });
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_057_recreated.pptx" })
  .then((f) => console.log("written:", f));
