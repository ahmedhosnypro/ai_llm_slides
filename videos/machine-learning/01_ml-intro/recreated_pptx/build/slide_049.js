// Slide 049 GRAPHED recreation build — "K-Nearest Neighbors (KNN) , K=5"
// Copy of the certified native build (build/slide_049.js — FROZEN, never modified)
// with ONLY the two graph panels swapped for the vision-validated generated graph
// image (graphgen/slide_048_049_knn.py v2; build/assets/graphs/s49_graph_v2.png).
// House frame, badge, title, header rule, captions and the "K=5, cyan class"
// annotation are UNCHANGED certified text/chrome.
// v2 region measured from the original frame (960x540, 1px = 1pt = 1/72in):
//   content box + both panels span x 60..895, y 100..527 px
//   -> x=0.8333in y=1.3889in w=11.5972in h=5.9306in
//   (v2 image also carries the outer content box, the panel divider, the
//   dark-red ticks beside green points and the solid faint left baseline that
//   the v1 image omitted. The box bottom edge is intentionally absent from the
//   image — the house frame line at 7.35in closes the box at the same y as the
//   original.)
//   Captions moved to the measured original glyph bands: left band y 497-509px,
//   right band y 505-515px (below the axis line at y~481px, matching the
//   original; the certified 6.5in position collided with the axis).
// The generated image contains: left KNN scatter (26 measured neighbor points +
// red query + connectors + solid magenta rings on the 5 nearest, sklearn KNN
// verified: 1 green + 4 cyan -> cyan class), right 26-dot sorted-distance ranking
// ladder (measured heights/colors, dotted verticals, red baseline dots, blue
// cutoff after the 5th dot), measured axes/baselines, content box + divider.
const pptxgen = require("pptxgenjs");
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";           // house background
const FRAME = "C00000";        // house frame line
const DARKRED = "B22222";      // axes, captions, title part 1 (spec)
const BLUE = "0000CC";         // title part 2, divider (spec)
const INK = "333333";
const BADGE = "FFF9C4";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer chrome ----
// Red frame rectangle (0.15in inset, no visible fill)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});
// Slide-number badge: yellow oval, numeral "49" (printed number on the original image)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("49", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
// Title: two-tone ("K-Nearest Neighbors" dark red + "(KNN) , K=5" blue), centered
s.addText(
  [
    { text: "K-Nearest Neighbors ", options: { color: DARKRED } },
    { text: "(KNN) , K=5", options: { color: BLUE } },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "middle",
    fontSize: 30, bold: true, fontFace: FONT, margin: 0,
  }
);
// Header band divider: thin dark-red rule at ~15% height, full width (spec step 2)
s.addShape(pptx.shapes.LINE, {
  x: 0.15, y: 1.05, w: 13.03, h: 0,
  line: { color: DARKRED, width: 1.5 },
});

// ---- GENERATED GRAPH IMAGE (graphed variant, v2) ----
// Replaces the native-shapes scatter approximation (both panels) from the
// certified build. PIL closed-loop ink-edge alignment PASSED at the v2 region
// (max offset 1.17px at 1x ~ 2.4px at 150dpi, binding bound ~4px). TRANSPARENT
// PNG: the certified 049 build has no white interior rect (house interior is
// E8E8E8, as judge-certified), so the graph ink composites on the slide
// background exactly like the certified native shapes did.
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/ml-intro/recreated_pptx/build/assets/graphs/s49_graph_v2.png",
  x: 0.8333, y: 1.3889, w: 11.5972, h: 5.9306,
});

// Left caption: bold red, centered under the panel at the measured original
// glyph band (y 497-509px -> box y 6.76in, glyph center ~6.99in)
s.addText("Select Nearest 5 Neighbors", {
  x: 1.33, y: 6.76, w: 5.34, h: 0.45, align: "center", valign: "middle",
  fontSize: 20, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
});

// Annotation top-left of right panel: "K=5, cyan class" with 'cyan' highlighted cyan
s.addText(
  [
    { text: "K=5, ", options: { color: "000000" } },
    { text: "cyan", options: { color: "000000", highlight: "00FFFF" } },
    { text: " class", options: { color: "000000" } },
  ],
  {
    x: 7.35, y: 1.45, w: 3.0, h: 0.35, align: "left", valign: "middle",
    fontSize: 14, fontFace: FONT, margin: 0,
  }
);

// Right caption: bold red, centered under the panel at the measured original
// glyph band (y 505-515px -> box y 6.86in, glyph center ~7.08in)
s.addText("Vote on 5 Nearest Neighbors", {
  x: 6.94, y: 6.86, w: 5.72, h: 0.45, align: "center", valign: "middle",
  fontSize: 20, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
});

pptx.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/ml-intro/recreated_pptx/slide_049_recreated.pptx" })
  .then(() => console.log("done: slide_049_recreated.pptx"));
