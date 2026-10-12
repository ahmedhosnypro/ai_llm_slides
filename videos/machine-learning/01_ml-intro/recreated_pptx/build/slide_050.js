// Slide 050 recreation — "K-Nearest Neighbors (KNN) , K=20"
// Spec: videos/ml-intro/analysis/slide_050_final.json (PASS_WITH_FIXES, score 8).
//
// HOUSE FRAME RULE (founder, 2026-10-09) — overrides spec/judge for these elements:
//   bg E8E8E8; outer frame rect x:0.15 y:0.15 w:13.03 h:7.2, line C00000 w1.5, fill E8E8E8;
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5, fill FFF9C4 line FFF9C4 w0.5, numeral "50"
//   bold 18pt 333333; title text box starts y:0.28, x:0.6, w:12.13, align center.
//
// Spec elements kept VERBATIM: title text incl. space before comma "(KNN) , K=20";
// captions "Select Nearest 20 Neighbors" / "Vote on 20 Nearest Neighbors";
// annotation "K=20, green class". Point counts approximate per spec (~8 green,
// ~9 blue, ~3 ringed orange + unringed orange, 1 bright-green outlier; 20 rings).
// Spec's white slide background is superseded by the house gray (#E8E8E8) chrome.
// No pptxgenjs bullet options anywhere; manual glyphs only (none needed here).

const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", FRAME_RED = "C00000", DIAG_RED = "CC0000",
      TEXT_RED = "B00000", BLUE = "0000CC", GREEN = "7AB648",
      CYAN = "5BC8E8", ORANGE = "E8C88A", MAGENTA = "C850C8",
      GRAY = "999999", BADGE = "FFF9C4", INK = "333333",
      BRIGHT_GREEN = "00CC44", BLACK = "000000";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE CHROME ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// Spec header band (thin red border, ~0-15% height) adapted inside the house frame
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 1.0,
  fill: { color: BG }, line: { color: DIAG_RED, width: 1 },
});

// Badge (house): yellow oval, numeral exactly "50"
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("50", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// HOUSE title box: y:0.28, x:0.6, w:12.13, centered.
// Verbatim "K-Nearest Neighbors (KNN) , K=20" — mixed colors per spec
// ("K-Nearest Neighbors" dark red, "(KNN) , K=20" blue; space before comma kept).
s.addText([
  { text: "K-Nearest Neighbors", options: { color: TEXT_RED } },
  { text: " (KNN) , K=20", options: { color: BLUE } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.74, align: "center", valign: "middle",
  fontSize: 28, bold: true, fontFace: FONT, margin: 0,
});

// ================= GRAPH EMBED (graphed variant) =================
// The native L/R panel graph block is replaced by two generated images
// (graphgen/slide_050_051_knn20.py; PIL closed-loop aligned to the original
// frame — qa/slide50/graphgen/closed_loop_v7.json PASS, 111/111 checks, max
// dev 1.11px at 960-space; 1px = 1pt). Gray #E8E8E8 background baked in so
// the images composite invisibly on the house bg. Everything else in this
// build is identical to the certified native build except the annotation and
// two caption boxes, whose positions move to the measured original ink bands
// (the certified positions would land inside the graph area and collide with
// the graph image); text content and styling are unchanged.
s.addImage({ path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s50_graph_left_v7.png",
             x: 0.8333, y: 1.3889, w: 6.2083, h: 6.0417 });
s.addImage({ path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s50_graph_right_v7.png",
             x: 7.0139, y: 1.3889, w: 5.4861, h: 6.0417 });

// Annotation at top of right panel: "K=20, green class", 'green' bold on
// bright green highlight. (Graphed variant: moved to the measured original
// ink bbox x 582..712 y 146..160 -> x:8.05 y:2.02; the certified y:1.45in
// position would cross the graph image's content-box top border.)
s.addText([
  { text: "K=20, ", options: { color: BLACK } },
  { text: "green", options: { color: BLACK, bold: true, highlight: BRIGHT_GREEN } },
  { text: " class", options: { color: BLACK } },
], {
  x: 8.05, y: 2.02, w: 3.4, h: 0.32, align: "left", valign: "top",
  fontSize: 13, fontFace: FONT, margin: 0,
});

// Left caption: bold dark red. (Graphed variant: y moved to the measured
// original ink band y 490..510 -> y:6.76; the certified y:6.45in band lands
// inside the graph area and collides with the orange cluster rings.)
s.addText("Select Nearest 20 Neighbors", {
  x: 1.11, y: 6.76, w: 5.3, h: 0.4, align: "center", valign: "top",
  fontSize: 18, bold: true, color: TEXT_RED, fontFace: FONT, margin: 0,
});

// Right caption. (Graphed variant: moved to measured ink center x=663px,
// band y 500..515 -> x:6.41 y:6.83.)
s.addText("Vote on 20 Nearest Neighbors", {
  x: 6.41, y: 6.83, w: 5.6, h: 0.4, align: "center", valign: "top",
  fontSize: 18, bold: true, color: TEXT_RED, fontFace: FONT, margin: 0,
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_050_recreated.pptx" })
  .then(() => console.log("done"));
