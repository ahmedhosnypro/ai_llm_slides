const pptxgen = require("pptxgenjs");

// Slide 006: Visualization of Single Layer Perceptron (Multi-Class)
const NUM = 6;
const TITLE = "Visualization of Single Layer Perceptron";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const GREEN = "008000";
const BORDER_RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const PEACH = "FDEBD0";
const TAN = "E6D5B8";
const TAN_TEXT = "5C4A2A";
const LIGHT_BLUE = "C0C0FF";
const PURPLE = "D0B0FF";
const GRAY = "808080";
const INPUT_FILL = "E6F3FF";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Slide-number badge - HOUSE CHROME LAW (yellow oval at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 3. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
// Title: "Visualization of" (red), "Single Layer" (blue), "Perceptron" (red)
s.addText([
  { text: "Visualization of ", options: { color: RED, bold: true, fontSize: 30, fontFace: FONT } },
  { text: "Single Layer ", options: { color: BLUE, bold: true, fontSize: 30, fontFace: FONT } },
  { text: "Perceptron", options: { color: RED, bold: true, fontSize: 30, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Original frame x=60..899, y=60..516 maps onto the mandated house frame.
const X = (px) => 0.15 + (px - 60) * (13.03 / 839);
const Y = (py) => 0.15 + (py - 60) * (7.2 / 456);
const WX = (wpx) => wpx * (13.03 / 839);
const HY = (hpx) => hpx * (7.2 / 456);

// 4. Right side first: generated perceptron diagram (the equation panel occludes its top-left).
const diag_meta = require("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_006_perceptron_multiclass.json");
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_006_perceptron_multiclass.png",
  x: diag_meta.position.x, y: diag_meta.position.y, w: diag_meta.position.w, h: diag_meta.position.h,
});

// 5. Measured white equation panel: original x=72..471, y=100..236.
const eq_x = X(72), eq_y = Y(100), eq_w = WX(471 - 72), eq_h = HY(236 - 100);
s.addShape(pres.shapes.RECTANGLE, {
  x: eq_x, y: eq_y, w: eq_w, h: eq_h,
  fill: { color: "FFFFFC" }, line: { color: "D64B7E", width: 0.75 },
});

// Equations at their measured ink tops; exact 600-dpi asset sizes from the sidecars.
const eq_manifest = require("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_006_equations.json");
const eq_by_name = Object.fromEntries(eq_manifest.equations.map((e) => [e.name, e]));
for (const [name, py] of [["eq_s006_d1", 108], ["eq_s006_d2", 157], ["eq_s006_dm", 205]]) {
  const meta = eq_by_name[name].sidecar;
  s.addImage({
    path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/" + name + ".png",
    x: X(79), y: Y(py), w: meta.w_in, h: meta.h_in,
  });
}

// 6. Measured pale-yellow callout: original x=137..327, y=360..399, two centered italic lines.
const class_x = X(137), class_y = Y(360), class_w = WX(327 - 137), class_h = HY(399 - 360);
s.addShape(pres.shapes.RECTANGLE, {
  x: class_x, y: class_y, w: class_w, h: class_h,
  fill: { color: "FFFFCC" }, line: { color: "B8B400", width: 0.75 },
});
s.addText([
  { text: "Multi-Class", options: { breakLine: true, italic: true, bold: true, fontSize: 12, color: TAN_TEXT, fontFace: FONT } },
  { text: "Classification", options: { italic: true, bold: true, fontSize: 12, color: TAN_TEXT, fontFace: FONT } },
], {
  x: class_x, y: class_y, w: class_w, h: class_h,
  align: "center", valign: "middle", lineSpacing: 14, margin: 0,
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_006_recreated.pptx" 
}).then(() => console.log("wrote slide_006_recreated.pptx"));