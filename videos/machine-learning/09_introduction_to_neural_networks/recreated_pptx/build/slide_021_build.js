const pptxgen = require("pptxgenjs");

// Slide 021: four activation-function panels; no on-slide title.
// Original-frame geometry is measured at 960x540 px (1 px = 1 pt = 1/72 in).
const NUM = 21;
const FONT = "Arial";
const BG = "E8E8E8";
const RED = "C00000";
const BLACK = "000000";
const YELLOW = "FFF9C4";
const PINK = "FDE9E9";
const FORMULA_RED = "FF0000";
const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const P = (px) => px / 72;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// Source letterbox artifact, behind the mandatory house chrome.
s.addShape(pres.shapes.RECTANGLE, {
  x: P(38), y: P(518), w: P(884), h: P(22),
  fill: { color: BLACK }, line: { type: "none" },
});

const boxes = {
  relu: { x: P(113), y: P(54), w: P(301), h: P(51) },
  prelu: { x: P(550), y: P(54), w: P(301), h: P(51) },
  elu: { x: P(94), y: P(283), w: P(337), h: P(58) },
  softplus: { x: P(584), y: P(286), w: P(232), h: P(53) },
};
for (const b of Object.values(boxes)) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    ...b, fill: { color: PINK }, line: { color: FORMULA_RED, width: 1 },
  });
}

const graphs = {
  relu: [121, 109, 400, 272],
  prelu: [563, 109, 842, 275],
  elu: [121, 346, 400, 508],
  softplus: [564, 346, 842, 508],
};
for (const [name, [x0, y0, x1, y1]] of Object.entries(graphs)) {
  s.addImage({
    path: `${BUILD}/graphs_slide_021/graph_${name}.png`,
    x: P(x0), y: P(y0), w: P(x1 - x0), h: P(y1 - y0),
  });
}

for (const [name, b] of Object.entries(boxes)) {
  s.addImage({ path: `${BUILD}/eq_021_${name}.png`, ...b });
}

// House chrome: the original has no title, so the title area is intentionally empty.
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 18, bold: true,
  color: "333333", fontFace: FONT, margin: 0,
});

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_021_recreated.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote " + out));
