// Slide 016 recreation — "Data Overfit and Underfit"
// Spec: videos/ml-intro/analysis/slide_016_final.json (staged from old-deck slide 19; content verified identical) (Bishop PRML Fig 1.4-style 2x2 poly-fit demo)
// Geometry measured from unique_slides/slide_016.jpg via PIL (72 px/in at 960x540) — re-verified against the current frame 2026-10-09 (container 2.681..9.986in measured vs 2.673..9.979 built).
// House frame (founder directive 2026-10-09): slide-3 outer template; badge numeral
// = SLIDE ID ("16"), which also matches the original frame's printed badge "16".
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Spec colors (no '#' prefix!)
const BG = "E8E8E8";        // slide background (house frame template)
const TITLE_RED = "CC0000"; // title + container border
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFFF99";    // M-label boxes
const BAND = "EEEEEE";     // header/footer bands (spec accent, measured ~#E7E9E6)
const GREEN = "00FF00";     // true sine curve
const BLUE = "0000FF";      // data point circles
const FITRED = "FF0000";    // fit curves + annotation dot
const AXES = "B3B3B3";      // subplot box/ticks (light gray, measured ~#B5B7B4)
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---------------- house frame (founder directive 2026-10-09, slide-3 template) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: "C00000", width: 1.5 },
});

// title (house rule: box y 0.28, x 0.6, w 12.13, centered)
s.addText("Data Overfit and Underfit", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "top",
  fontSize: 36, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// slide-number badge (house frame; numeral = slide id per founder clarification)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("16", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// gray header band + white content region + gray footer band (judge attempt 1:
// original's nested region structure; measured bands ~9-23% and ~95-100% height,
// white interior between them). Drawn inside the house frame line.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.17, y: 0.95, w: 12.99, h: 0.76,
  fill: { color: BAND },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.17, y: 1.71, w: 12.99, h: 5.37,
  fill: { color: WHITE },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.17, y: 7.08, w: 12.99, h: 0.26,
  fill: { color: BAND },
});

// instruction line (verbatim, single sentence; measured at ~29% height, left side)
s.addText("The X axis is the input. The Y axis is the response.", {
  x: 2.1, y: 2.16, w: 9.5, h: 0.4, align: "left", valign: "top",
  fontSize: 20, color: BLACK, fontFace: FONT, margin: 0,
});

// ---------------- graphed: native plot approximation replaced by the
// generated graph image (build/assets/graphs/s016_graph_v1.png; 300dpi, baked
// container border + axes + fits; placed at the original frame's measured
// region, 1px = 1pt). Everything else is byte-identical to the certified build.
s.addImage({ path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s016_graph_v1.png",
               x: 2.62500, y: 2.55556, w: 7.40278, h: 4.38889 });

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_016_recreated.pptx" })
  .then(() => console.log("done: videos/ml-intro/recreated_pptx/slide_016_recreated.pptx"));
