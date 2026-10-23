// Build slide 004 — "Concept of LOSS Function"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Fresh ROOT build (no dependencies) — attempt 1
//
// ═══════════════════════════════════════════════════════════════════════════════
// GROUND TRUTH: unique_slides/slide_004.jpg — 960x540, exactly 72 px/in
//                (verified: 960/13.3333 = 72.0001) => 1 frame px == 1 pt == 1/72 in.
// Measurement bank: recreated_pptx/qa/slide004/ (measure_frame_4.py + measure_out_4.txt)
// ════════════════════════════════════════════════════════════════════════════════
//
// CONTENT (all PIL-verified, see qa/slide004/measure_out_4.txt):
//   * Title: "Concept of LOSS Function" at y=70..91, x~280..660 — mixed red/blue
//   * Box1 (Original Labels): red border, x=80..395, y=99..222
//   * Box2 (Predicted Labels): red border, x=427..745, y=99..222
//   * Remember Box: lavender/blue border (badge ring color), x=750..900, y=94..226
//   * Objective Box: blue border, x=78..302, y=242..301
//   * Error Box: blue border, x=78..485, y=306..365
//   * Predicted/Where Block: unboxed, x=490..890, y=220..370
//   * Define Box: red border, salmon fill (FAEBD7), full width x=75..660, y=387..448
//   * Formula Box: yellow fill, full width, below Define at y~468..520
//
// EQUATIONS (deck math law: professional 2D format via matplotlib mathtext -> 600dpi PNG):
//   eq_004_Yvec.png:      Y = (y_1, y_2, ..., y_n)^T_{n x 1}
//   eq_004_Yhatvec.png:   \hat{Y} = (\hat{y}_1, \hat{y}_2, ..., \hat{y}_n)^T_{n x 1}
//   eq_004_norm.png:      ||a||_2 = a^T a
//   eq_004_formula.png:   Loss = ||Y - \hat{Y}||_2 = (Y - \hat{Y})^T (Y - \hat{Y})
//   All rendered at exact px/600 size via addImage; sidecars banked for OMML wrap.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_004_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

const NAVY    = "000080";   // blue borders (objective, error, remember)
const RED     = "C00000";   // red borders (label boxes, define) + house strokes
const REDTXT  = "FF0000";   // red text
const BLUE    = "0000FF";   // blue text
const SALMON  = "FAEBD7";   // define box fill
const YELLOW  = "FFFFE0";   // formula box fill (cream yellow)
const WHITE   = "FFFFFF";
const BLACK   = "000000";
const INK     = "333333";   // dark text
const FONT    = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top stroke), badge with numeral 4
drawHouseChrome(pptx, slide, { numeral: 4 });

// Helper: rectangle with fill
const rect = (x, y, w, h, fill, line = null) => {
  const opts = { x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill } };
  if (line) opts.line = { color: line.color, width: line.width };
  return slide.addShape(pptx.ShapeType.rect, opts);
};

// Helper: text block
const textbox = (x, y, w, h, runs, align = "left", valign = "top", lineSpacing = 1.15) => {
  slide.addText(runs, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align, valign, margin: 0, fontFace: FONT, lineSpacing,
  });
};

// ============================================================
// 1. TITLE — "Concept of LOSS Function" at y=70..91, centered
// ============================================================
// Frame: y=70..91 (21px = 0.292in), x~280..660 (380px = 5.278in)
// Use two runs: "Concept of " red, "LOSS" blue, " Function" red
textbox(280, 70, 380, 22, [
  { text: "Concept of ", options: { color: REDTXT, bold: true, fontSize: 32 } },
  { text: "LOSS", options: { color: BLUE, bold: true, fontSize: 32 } },
  { text: " Function", options: { color: REDTXT, bold: true, fontSize: 32 } },
], "center", "middle", 1.0);

// ============================================================
// 2. BOX 1 — Original Labels (red border, white fill)
//    x=80..395 (315px), y=99..222 (123px)
// ============================================================
rect(80, 99, 315, 123, WHITE, { color: RED, width: 1 });

// Vector equation (image)
const ASSETS = path.resolve(__dirname, "assets");
const Yvec = path.join(ASSETS, "eq_004_Yvec.png");
slide.addImage({ path: Yvec, x: px(90), y: px(108), w: 1.96667, h: 0.275 });

// "Original Labels" - bold red
textbox(90, 140, 300, 25, [
  { text: "Original Labels", options: { color: REDTXT, bold: true, fontSize: 16 } },
], "left", "top", 1.0);

// "from Training Samples" - black
textbox(90, 165, 300, 25, [
  { text: "from Training Samples", options: { color: BLACK, fontSize: 14 } },
], "left", "top", 1.0);

// ============================================================
// 3. BOX 2 — Predicted Labels (red border, white fill)
//    x=427..745 (318px), y=99..222 (123px)
// ============================================================
rect(427, 99, 318, 123, WHITE, { color: RED, width: 1 });

// Vector equation (image)
const Yhatvec = path.join(ASSETS, "eq_004_Yhatvec.png");
slide.addImage({ path: Yhatvec, x: px(437), y: px(108), w: 1.97333, h: 0.30333 });

// "Predicted Labels" - bold blue
textbox(437, 148, 300, 25, [
  { text: "Predicted Labels", options: { color: BLUE, bold: true, fontSize: 16 } },
], "left", "top", 1.0);

// "from Model Ŷ=XW" - black
textbox(437, 173, 300, 25, [
  { text: "from Model ", options: { color: BLACK, fontSize: 14 } },
  { text: "Ŷ=XW", options: { color: BLACK, fontSize: 14 } },
], "left", "top", 1.0);

// ============================================================
// 4. REMEMBER BOX — lavender/blue border (badge ring color 6A5ACD)
//    x=750..900 (150px), y=94..226 (132px) — smaller, to far right
// ============================================================
const REMEMBER_RING = "6A5ACD";
rect(750, 94, 150, 132, WHITE, { color: REMEMBER_RING, width: 1 });

// "Remember" - bold black
textbox(758, 102, 134, 20, [
  { text: "Remember", options: { color: BLACK, bold: true, fontSize: 13 } },
], "left", "top", 1.0);

// Norm equation (image)
const normEq = path.join(ASSETS, "eq_004_norm.png");
slide.addImage({ path: normEq, x: px(758), y: px(126), w: 0.97167, h: 0.25333 });

// ============================================================
// 5. OBJECTIVE BOX — blue border (NAVY), white fill
//    x=78..302 (224px), y=242..301 (59px)
// ============================================================
rect(78, 242, 224, 59, WHITE, { color: NAVY, width: 1 });

// "Objective is Ŷ=Y" - black, Ŷ and Y italic
textbox(85, 248, 210, 35, [
  { text: "Objective is ", options: { color: INK, fontSize: 14 } },
  { text: "Ŷ=Y", options: { color: INK, fontSize: 14, italic: true } },
], "left", "middle", 1.0);

// ============================================================
// 6. ERROR BOX — blue border (NAVY), white fill
//    x=78..485 (407px), y=306..365 (59px)
// ============================================================
rect(78, 306, 407, 59, WHITE, { color: NAVY, width: 1 });

// "If Ŷ≠Y ⇒ There is an Error (Loss)" - "Error (Loss)" in red
textbox(85, 312, 395, 35, [
  { text: "If ", options: { color: INK, fontSize: 14 } },
  { text: "Ŷ≠Y", options: { color: INK, fontSize: 14, italic: true } },
  { text: " ⇒ There is an ", options: { color: INK, fontSize: 14 } },
  { text: "Error (Loss)", options: { color: REDTXT, bold: true, fontSize: 14 } },
], "left", "middle", 1.0);

// ============================================================
// 7. PREDICTED/WHERE BLOCK — unboxed, right middle
//    x=490..890 (400px), y=220..370 (150px)
// ============================================================
// Line 1: "Ŷ = XW" + "Predicted" in red
textbox(490, 225, 400, 30, [
  { text: "Ŷ = XW", options: { color: INK, fontSize: 16, italic: true } },
  { text: "  Predicted", options: { color: REDTXT, bold: true, fontSize: 14 } },
], "left", "top", 1.0);

// Line 2: "Where:" + three lines
textbox(490, 255, 400, 100, [
  { text: "Where:", options: { color: INK, bold: true, fontSize: 14 }, breakLine: true },
  { text: "X_{N×(d+1)} is a matrix → Given", options: { color: INK, fontSize: 14 }, breakLine: true },
  { text: "Y_{N×1} is labels vector → Given", options: { color: INK, fontSize: 14 }, breakLine: true },
  { text: "W is Model Parameter → Required", options: { color: INK, fontSize: 14 } },
], "left", "top", 1.2);

// ============================================================
// 8. DEFINE BOX — red border (C00000), salmon fill (FAEBD7)
//    Full width: x=75..660 (585px), y=387..448 (61px)
// ============================================================
rect(75, 387, 585, 61, SALMON, { color: RED, width: 1 });

// "Define Loss function as squared distance between Ŷ and Y"
// "Loss" red, "squared distance" blue, rest black
textbox(85, 393, 565, 35, [
  { text: "Define ", options: { color: INK, fontSize: 15 } },
  { text: "Loss", options: { color: REDTXT, bold: true, fontSize: 15 } },
  { text: " function as ", options: { color: INK, fontSize: 15 } },
  { text: "squared distance", options: { color: BLUE, bold: true, fontSize: 15 } },
  { text: " between ", options: { color: INK, fontSize: 15 } },
  { text: "Ŷ", options: { color: INK, fontSize: 15, italic: true } },
  { text: " and ", options: { color: INK, fontSize: 15 } },
  { text: "Y", options: { color: INK, fontSize: 15, italic: true } },
], "left", "middle", 1.0);

// ============================================================
// 9. FORMULA BOX — yellow fill (cream), full width below Define
//    x=75..660 (585px), y=455..515 (60px) — adjusted to sit just below Define bottom (448) with gap
// ============================================================
rect(75, 455, 585, 60, YELLOW); // no border per measurement (only yellow fill)

// Formula equation (image) - centered
const formulaEq = path.join(ASSETS, "eq_004_formula.png");
slide.addImage({ path: formulaEq, x: px(75 + (585 - 2070/600*72)/2), y: px(462), w: 3.45, h: 0.32167 });
// Actually let's center it: (585px - 3.45in*72)/2 = (585 - 248.4)/2 = 168.3px from left
// So x = 75 + 168.3 = 243.3

slide.addImage({ path: formulaEq, x: px(243.3), y: px(462), w: 3.45, h: 0.32167 });

// Write output
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));