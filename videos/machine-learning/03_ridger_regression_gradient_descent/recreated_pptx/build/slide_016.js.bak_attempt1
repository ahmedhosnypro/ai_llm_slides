const pptxgen = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require(
  "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/house_chrome.js"
);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.333, H = 7.5;

let slide = pres.addSlide();
slide.background = { color: CHROME.canvas };

// Draw house chrome (gray panel, red strokes, badge with numeral "16")
drawHouseChrome(pres, slide, { numeral: "16" });

/*
 * ============================================================
 * SLIDE-SPECIFIC CONTENT
 * ============================================================
 * All coordinates from PIL measurement of slide_016.jpg (960x540, 1px=1pt=1/72in)
 */

const FONT = "Arial";

// White content box inside the gray panel
// Box outer: x=85..830 (745px), y=94..530 (436px) in frame px
// In inches: x=1.1806, y=1.3056, w=10.3472, h=6.0556
// Border: ~1-2px dark blue ~#2B237A (RGB ~43,35,122)
const boxX = 85 / 72;      // 1.1806 in
const boxY = 94 / 72;      // 1.3056 in
const boxW = 745 / 72;     // 10.3472 in
const boxH = 436 / 72;     // 6.0556 in
const borderColor = "2B237A";  // dark blue border
const boxFill = "FFFFFF";

// Text area inside box with margins
const textX = boxX + 0.20;        // 1.3806 in
const textW = boxW - 0.40;        // 9.9472 in

// ============================================================
// BACKGROUND SHAPES (added first, so they sit BEHIND text)
// ============================================================

// 1. White box with dark blue border
slide.addShape("rect", {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { color: boxFill },
  line: { color: borderColor, width: 1.5 },
});

// 2. Yellow highlight behind "better generalization" on line 3
// Frame: x=286..457 (3.97..6.35in), y=175..198 (2.43..2.75in)
// Our line 3 y position: ~2.2in. Highlight rect:
const hl_x = 4.0;      // ~288px
const hl_y = 2.25;     // ~162px
const hl_w = 2.4;      // ~173px
const hl_h = 0.30;     // ~22px
slide.addShape("rect", {
  x: hl_x, y: hl_y, w: hl_w, h: hl_h,
  fill: { color: "FFFF00" },
  line: { width: 0 },
});

// 3. Red underline for "customized weigh factor" on line 4
// Frame: y~180..181 (2.5in), x~286..457 (3.97..6.35in) -> same x as highlight roughly
const ul4_x = hl_x;
const ul4_y = 2.75;   // line 4 baseline
const ul4_w = hl_w;
slide.addShape("line", {
  x: ul4_x, y: ul4_y, w: ul4_w, h: 0,
  line: { color: "C00000", width: 1 },
});

// 4. Black underlines for "Small number of samples (N)" and "Large vector Length (d)" on line 7
// Frame: y=497..526 (6.90..7.31in), two separate underlines
// First underline: "Small number of samples (N)" at left area
// Second: "Large vector Length (d)" at right area
const ul7_y = 6.95;   // baseline for last line

// First underline position - estimated from text layout
const ul7a_x = textX + 5.5;  // after "Regularization is particularly important for "
const ul7a_w = 3.0;          // width of "Small number of samples (N)"
slide.addShape("line", {
  x: ul7a_x, y: ul7_y, w: ul7a_w, h: 0,
  line: { color: "000000", width: 1 },
});

// Second underline
const ul7b_x = textX + 8.0;  // further right
const ul7b_w = 2.8;          // width of "Large vector Length (d)"
slide.addShape("line", {
  x: ul7b_x, y: ul7_y, w: ul7b_w, h: 0,
  line: { color: "000000", width: 1 },
});

// ============================================================
// TEXT CONTENT (added after shapes, so on top)
// ============================================================

// Title: "L₁ and L₂ Regularization" - dark red #8B0000, bold ~32pt, centered
slide.addText("L\u2081 and L\u2082 Regularization", {
  x: 0.6, y: 0.75, w: W - 1.2, h: 0.7,
  align: "center", valign: "middle",
  fontSize: 32, bold: true, color: "8B0000",
  fontFace: FONT, margin: 0,
});

// Line positions - matched to original frame measurements
// Line 1 (Header): "Regularizers are based on:" -- red #C00000, bold, ~18pt
// Frame y~102..147 (1.42..2.04in) -> use y=1.5in
let y1 = 1.50;
slide.addText("Regularizers are based on:", {
  x: textX, y: y1, w: textW, h: 0.35,
  fontSize: 18, bold: true, color: "C00000",
  fontFace: FONT, margin: 0,
});

// Line 2 (Sub-header): "Penalize large values of W (model parameters)" -- blue #0000FF, bold, ~16pt
// Frame y~102..147 (same band) -> y=1.85in
let y2 = 1.85;
slide.addText("Penalize large values of W (model parameters)", {
  x: textX, y: y2, w: textW, h: 0.35,
  fontSize: 16, bold: true, color: "0000FF",
  fontFace: FONT, margin: 0,
});

// Line 3 (Bullet 1): "This has the effect of better generalization of the model"
// black, ~16pt, with yellow highlight on "better generalization" (handled by shape above)
// Frame y~175..199 (2.43..2.76in) -> y=2.25in
let y3 = 2.25;
const bullet = "\u2022 ";
const l3a = "This has the effect of ";
const l3b = "better generalization";
const l3c = " of the model";
slide.addText([
  { text: bullet + l3a, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l3b, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l3c, options: { fontSize: 16, color: "000000", fontFace: FONT } },
], {
  x: textX, y: y3, w: textW, h: 0.35,
  margin: 0,
});

// Line 4 (Bullet 2): Long line with red underline on "customized weigh factor" (shape above)
// Frame y~175..199 (same band as line 3, wraps) -> y=2.65in
let y4 = 2.65;
const l4a = "Since there is a contradiction between model training (using training dataset) and model generalization, the generalization term is added to the objective loss function with a ";
const l4b = "customized weigh factor";
const l4c = " (do regularization to what extent)";
slide.addText([
  { text: bullet + l4a, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l4b, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l4c, options: { fontSize: 16, color: "000000", fontFace: FONT } },
], {
  x: textX, y: y4, w: textW, h: 0.70,
  margin: 0,
});

// Line 5 (Bullet 3): "Penalization may be applied on the Squared Norm... L₂ regularization..."
// black, with "L₂ regularization" in blue
// Frame y~229..248 (3.18..3.44in) -> y=3.25in
let y5 = 3.25;
const l5a = "Penalization may be applied on the Squared Norm of the Weight Vector This is called ";
const l5b = "L\u2082 regularization";
const l5c = " (also known as Ridge Regularization)";
slide.addText([
  { text: bullet + l5a, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l5b, options: { fontSize: 16, color: "0000FF", fontFace: FONT } },
  { text: l5c, options: { fontSize: 16, color: "000000", fontFace: FONT } },
], {
  x: textX, y: y5, w: textW, h: 0.50,
  margin: 0,
});

// Line 6 (Bullet 4): "Penalization may also be applied on the sum of Absolute values... L₁ regularization"
// black, with "L₁ regularization" in blue
// Frame y~255..306 (3.54..4.25in) -> y=3.75in (wraps to 2 lines)
let y6 = 3.75;
const l6a = "Penalization may also be applied on the sum of Absolute values of the Weight Vector This is called ";
const l6b = "L\u2081 regularization";
slide.addText([
  { text: bullet + l6a, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l6b, options: { fontSize: 16, color: "0000FF", fontFace: FONT } },
], {
  x: textX, y: y6, w: textW, h: 0.70,
  margin: 0,
});

// Line 7 (Bullet 5): "Regularization is particularly important for Small number of samples (N) and Large vector Length (d)"
// black, with black underlines (shapes above) on the two phrases
// Frame y~483..528 (6.71..7.33in) -> y=6.75in
let y7 = 6.75;
const l7a = "Regularization is particularly important for ";
const l7b = "Small number of samples (N)";
const l7c = " and ";
const l7d = "Large vector Length (d)";
slide.addText([
  { text: bullet + l7a, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l7b, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l7c, options: { fontSize: 16, color: "000000", fontFace: FONT } },
  { text: l7d, options: { fontSize: 16, color: "000000", fontFace: FONT } },
], {
  x: textX, y: y7, w: textW, h: 0.40,
  margin: 0,
});

// Output
const outPath = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_016_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("done"));