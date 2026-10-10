// Slide 004 recreation: "What is Machine Learning?" — attempt 3 (v2, size-calibrated)
// Spec: analysis/slide_004_final.json + pixel measurements of unique_slides/slide_004.jpg
// (960x540 = 72px/in). Font sizes solved from measured line extents with Liberation
// (Arial-metric) fonts: main text 25pt, dash sub-bullets 22pt, title 35pt bold.
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in = 16:9 (original frame is 960x540, same aspect)
const FONT = "Arial";

// Colors: spec hex, cross-checked against pixel averages of the original
const BG = "E8E8E8";       // slide background (measured 231,233,230 outside the box)
const MAROON = "B03040";    // border red-maroon (spec/visual_elements)
const DARKRED = "A00000";   // title / Generalization / red-italic (judges read dark red)
const TEXT = "000000";      // body text
const BLUE = "2020A0";      // blue emphasis (recert judge: IMG2 ~#2020A0-#3333CC, not vivid)
const YELLOW = "FFFF00";   // highlighter
const BADGE_FILL = "FCFE9B"; // measured badge interior avg (252,254,155)
const INK = "333333";       // badge outline / number

let s = pptx.addSlide();
s.background = { color: BG };

// Outer frame: HOUSE template (founder directive 2026-10-09) — 0.15in inset
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// Slide-number badge: HOUSE geometry/colors, numeral '4' = slide id
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("4", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Title: HOUSE position (text box starts y=0.28, x=0.6, w=12.13)
s.addText("What is Machine Learning?", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.65, align: "center", valign: "middle",
  fontSize: 35, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
});

// Content box: measured x 89->875, y 144->525 px — WHITE interior (measured 254,255,255)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.24, y: 2.00, w: 10.92, h: 5.28,
  fill: { color: "FFFFFF" }, line: { color: MAROON, width: 1 },
});

// Body lines: each line is its own text box at the measured position
// (wrap:false + measured widths reproduce the original's exact wrap points).
// Main text 25pt, dash sub-bullets 22pt (both solved from measured extents).
function line(runs, x, y, w, opts = {}) {
  s.addText(runs, Object.assign({
    x, y, w, h: 0.50, fontSize: 25, color: TEXT, fontFace: FONT,
    margin: 0, valign: "top", wrap: false,
  }, opts));
}

// L1 (ink band y 2.31): underline on "uses the statistically motivated" ONLY
// (measured underline run x 412-756 px; nothing under "approach")
line([
  { text: "Machine Learning primarily ", options: {} },
  { text: "uses the statistically motivated", options: { underline: { style: "sng" } } },
], 1.40, 2.22, 9.60);

// L2 (ink band y 2.78): "approach" wrapped onto its own line, as in the original
line([
  { text: "approach", options: { underline: { style: "sng" } } },
], 1.40, 2.69, 2.0);

// Dash sub-bullet 1, line 1 (ink band y 3.25) — dash at x 2.04, text at x 2.42 (22pt)
line("- ", 2.04, 3.17, 0.40, { fontSize: 22, h: 0.45 });
line([
  { text: "No hand-crafted rules", options: { bold: true, color: BLUE } },
  { text: " - subtle pattern nuances are often be difficult to", options: {} },
], 2.42, 3.17, 9.75, { fontSize: 22, h: 0.45 });

// Dash sub-bullet 1, line 2 (ink band y 3.67): hanging indent at x 2.42
line("specify", 2.42, 3.59, 2.0, { fontSize: 22, h: 0.45 });

// Dash sub-bullet 2, line 1 (ink band y 4.15) — NO underline on "on its own"
// (0 dark pixels under this line in the original); "building" red italic ends line 1
line("- ", 2.04, 4.07, 0.40, { fontSize: 22, h: 0.45 });
line([
  { text: "Instead, ", options: {} },
  { text: "let the machine figure out the rules", options: { bold: true, color: BLUE } },
  { text: " ", options: {} },
  { text: "on its own", options: { bold: true, color: BLUE, underline: { style: "sng" } } },
  { text: " by ", options: {} },
  { text: "building", options: { italic: true, color: DARKRED } },
], 2.42, 4.07, 9.75, { fontSize: 22, h: 0.45 });

// Dash sub-bullet 2, line 2 (ink band y ~4.45): red italic tail, hanging indent
line([
  { text: "statistical models of the data", options: { italic: true, color: DARKRED } },
], 2.42, 4.37, 4.20, { fontSize: 22, h: 0.45 });

// Heading (ink band y 5.00): "Desirable Property: Generalization" — 25pt bold (solved 25.3)
line([
  { text: "Desirable Property: ", options: { bold: true } },
  { text: "Generalization", options: { bold: true, color: DARKRED } },
], 1.40, 4.91, 6.20);

// Round bullet 1 (ink band y 5.57): yellow highlight behind "shouldn't overfit";
// "on the training data" BLUE underlined (measured blue x 450-667 px)
line("\u2022", 1.49, 5.48, 0.35);
line([
  { text: "The model ", options: {} },
  { text: "shouldn't overfit", options: { highlight: YELLOW, underline: { style: "sng" } } },
  { text: " ", options: {} },
  { text: "on the training data", options: { color: BLUE, underline: { style: "sng" } } },
], 1.85, 5.48, 8.0);

// Round bullet 2 (ink band y 6.14)
line("\u2022", 1.49, 6.05, 0.35);
line([
  { text: "It should generalize", options: { bold: true, color: BLUE } },
  { text: " well on unseen (future) test data", options: {} },
], 1.85, 6.05, 9.0);

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_004_recreated.pptx" })
  .then(() => console.log("wrote recreated_pptx/slide_004_recreated.pptx"));
