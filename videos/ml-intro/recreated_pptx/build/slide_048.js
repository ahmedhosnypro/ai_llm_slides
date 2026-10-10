// Slide 048 GRAPHED recreation build — "K-Nearest Neighbors (KNN) , K=3"
// Copy of the certified native build (build/slide_048.js — FROZEN, never modified)
// with ONLY the two graph panels swapped for the vision-validated generated graph
// image (graphgen/slide_048_049_knn.py v2; build/assets/graphs/s48_graph_v2_white.png,
// white composite used per pilot finding that opaque white composites cleanly
// through soffice). House frame, badge, title, header rule, captions and the
// "K=3, cyan class" annotation are UNCHANGED certified text/chrome.
// v2 region measured from the original frame (960x540, 1px = 1pt = 1/72in):
//   content box + both panels span x 60..895, y 100..527 px
//   -> x=0.8333in y=1.3889in w=11.5972in h=5.9306in
//   (v2 image also carries the outer content box, the panel divider, the
//   dark-red ticks beside green points and the solid faint left baseline that
//   the v1 image omitted; the native divider shape was therefore removed.
//   The box bottom edge is intentionally absent from the image — the house
//   frame line at 7.35in closes the box at the same y as the original.)
//   Captions moved to the measured original glyph bands: left band y 491-503px,
//   right band y 498-509px (below the axis line at y~481px, matching the
//   original; the certified 6.62in position collided with the axis).
// The generated image contains: left KNN scatter (26 measured neighbor points +
// red query + connectors + solid magenta rings on the 3 nearest, sklearn KNN
// verified: 1 green + 2 cyan -> cyan class), right 26-dot sorted-distance ranking
// ladder (measured heights/colors, dotted verticals, red baseline dots, blue
// cutoff after the 3rd dot), measured axes/baselines, content box + divider.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette (from spec JSON)
const BG = "E8E8E8";        // house slide background
const WHITE = "FFFFFF";     // spec: slide interior background
const MAROON = "8B0000";    // axes, dividers, captions, title red part
const BLUE = "0000CC";      // title blue part + vertical separator line
const INK = "333333";       // badge numeral / dark ticks
const BADGE_YELLOW = "FFF9C4";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---------- HOUSE FRAME (founder directive — overrides spec frame) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: "C00000", width: 1.5 },
});

// White interior (spec: background #FFFFFF, original slide is white inside the frame)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.18, y: 0.18, w: 12.97, h: 7.14,
  fill: { color: WHITE }, line: { color: WHITE, width: 0.25 },
});

// ---------- HOUSE badge: yellow oval, numeral 48 (printed on the original) ----------
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("48", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---------- HOUSE title: y 0.28, x 0.6, w 12.13, centered; bicolor per spec ----------
s.addText([
  { text: "K-Nearest Neighbors", options: { color: MAROON } },
  { text: " (KNN) , K=3", options: { color: BLUE } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.75, align: "center", valign: "middle",
  fontSize: 30, bold: true, fontFace: FONT, margin: 0,
});

// ---------- Frame structure (spec region 'frame') ----------
// Horizontal maroon rule closing the header band at ~15% height
s.addShape(pptx.shapes.LINE, {
  x: 0.18, y: 1.15, w: 12.97, h: 0,
  line: { color: MAROON, width: 1.5 },
});

// ---------- GENERATED GRAPH IMAGE (graphed variant, v2) ----------
// Replaces the native-shapes scatter approximation (both panels) from the
// certified build. PIL closed-loop ink-edge alignment PASSED at the v2 region
// (max offset 1.12px at 1x ~ 2.3px at 150dpi, binding bound ~4px).
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/ml-intro/recreated_pptx/build/assets/graphs/s48_graph_v2_white.png",
  x: 0.8333, y: 1.3889, w: 11.5972, h: 5.9306,
});

// (Panel divider now drawn BY the image at x~499.5px -> 6.94in; the native
// divider shape from the v1 build was removed.)

// Left caption, centered beneath the panel at the measured original glyph
// band (y 491-503px -> box y 6.71in, glyph center ~6.90in), bold maroon
s.addText("Select Nearest 3 Neighbors", {
  x: 0.67, y: 6.71, w: 5.75, h: 0.4, align: "center", valign: "middle",
  fontSize: 16, bold: true, color: MAROON, fontFace: FONT, margin: 0,
});

// 'K=3, cyan class' annotation, top-left of panel, 'cyan' on a cyan highlight
s.addText([
  { text: "K=3, ", options: { color: "000000" } },
  { text: "cyan", options: { color: "000000", highlight: "00E5E5" } },
  { text: " class", options: { color: "000000" } },
], {
  x: 7.0, y: 1.55, w: 2.6, h: 0.32, align: "left", valign: "middle",
  fontSize: 14, bold: false, fontFace: FONT, margin: 0,
});

// Right caption, centered beneath the panel at the measured original glyph
// band (y 498-509px -> box y 6.79in, glyph center ~6.99in), bold maroon
s.addText("Vote on 3 Nearest Neighbors", {
  x: 6.93, y: 6.79, w: 5.73, h: 0.4, align: "center", valign: "middle",
  fontSize: 16, bold: true, color: MAROON, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "/home/ahmed/Projects/ai_llm_slides/videos/ml-intro/recreated_pptx/slide_048_recreated.pptx",
}).then(() => console.log("done: slide_048_recreated.pptx"));
