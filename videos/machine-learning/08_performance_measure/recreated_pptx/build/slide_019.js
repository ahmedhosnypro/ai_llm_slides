// Slide 019 rebuild v9 — v8 + attempt-4 FAIL fix: Evaluation "Test Sample" text moved
// above its input arrow (was clipped by the arrow's white fill); step glyphs shrunk
// slightly (judge MINOR: larger/thicker than original). Attempt-3 fixes adjudicated by PIL scans + zoomed crops
// of the original (960x540, 1px=1pt):
// activation panel really is x574..882 y90..165 (h75; blue border x575/x881, bottom y164);
// training panel x608..902 y206..322 (cream from y208, bottom border y320..322), ROUNDED
// corners, "Training" heading x699..790 y177..192 ABOVE it; model box x612..736 y245..305
// with pink circle x694..732 y253..291 and thick purple step glyph; LOSS circle center
// (812,273) d60, hollow left arrow x845..885 y265..283 OUTSIDE the circle, blue (+1,-1)
// x835..881 y286..299; eval panel x608..902 y380..497 rounded. Planes = v4 skull side-view
// (crop-verified); step glyphs = v5 thick #732575.
// right-column panels really span x574..902 (activation) / x612..902 (training, evaluation);
// Training/Evaluation flows use plain-text sample labels + HOLLOW (white fill, red outline) arrows;
// Model = dark-red box (measured ~156,0,0) with white "Model", pink step-icon circle INSIDE the box
// on its right, yellow caption "[Any value] -> (-1 , +1)" at box bottom; LOSS = peach circle (252,200,189)
// with red text, fed by a hollow LEFT arrow from "Label of Input Sample" / "(+1, -1)" blue text.
// Panels: activation x574 y90 w308 h75; training x608 y206 w294 h116 (rounded); evaluation x608 y380 w294 h117 (rounded).
// Samples panel x57..556 y90..509 fill #E7E9E6; pos box x81..237 y136..504; pos strip x247..289 y161..491;
// neg box x331..482 y136..504; neg strip x498..540 y161..497. Planes = v4 assets (side-view, skull-marked enemies).
const pptxgen = require("pptxgenjs");
const path = require("path");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const TXT_RED = "C02828";
const TXT_GREEN = "1E8A3C";
const BOX_RED = "9C0000";    // model box / plane-box border (measured ~156,0,0 / 159,0,0)
const PINK = "F9DDFC";       // step circles (measured 253,220,252)
const PINK_STRIP = "F8DBDD"; // measured 248,219,221
const GREEN_STRIP = "E4FFEE";// measured 228,255,238
const MAROON = "A01818";
const TEAL = "12694E";
const PEACH = "FCC8BD";      // LOSS circle (measured 252,200,189)
const CREAM = "FBFEE3";      // measured 251,254,227
const ORANGE = "E8A33D";
const BLUE = "20409B";
const ACT_FILL = "F0FFFC";   // measured 240,255,252
const PURPLE = "6A3FB5";
const NAVY = "2E2A6E";
const BLUE_TXT = "0000CC";
const CAP_YELLOW = "FFD652"; // caption yellow (measured 253,166,70-ish gold)
const WHITE = "FFFFFF";
const GRAY_LINE = "C8C8C8";
const PANEL_GRAY = "E7E9E6"; // measured 231,233,230
const FONT = "Arial";

const ASSETS = path.join(__dirname, "assets");
const PLANES_ENEMY = ["p019_enemy_1.png", "p019_enemy_2.png", "p019_enemy_3.png", "p019_enemy_4.png", "p019_enemy_5.png"];
const PLANES_SAFE = ["p019_safe_1.png", "p019_safe_2.png", "p019_safe_3.png", "p019_safe_4.png", "p019_safe_5.png", "p019_safe_6.png"];
const STEP_PLOT_S = path.join(ASSETS, "eq_019_step_plot_small.png");
const PLANE_W = 1.30, PLANE_H = 1.30 * 732 / 1092;
const STEP_S_W = 592 / 600, STEP_S_H = 450 / 600;

const P = 1 / 72; // frame px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome (root AGENTS.md, overrides everything) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 11.8, h: 0.62,
  fill: { color: WHITE }, line: { color: BLUE, width: 1.5 },
});
s.addText("Training Samples with Labels  (Two Classes)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 22, bold: true, color: NAVY, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("19", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// ---- samples panel x57..556 y90..509 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 57 * P, y: 90 * P, w: 499 * P, h: 419 * P,
  fill: { color: PANEL_GRAY }, line: { color: GRAY_LINE, width: 1 },
});

// Positive Class (red) — 5 enemy planes, 5x "+1"
s.addText("Positive Class", {
  x: 113 * P, y: 97 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("\u201CShoot the Enemy\u201D", {
  x: 113 * P, y: 117 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 247 * P, y: 118 * P, w: 42 * P, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 81 * P, y: 136 * P, w: 156 * P, h: 368 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2.5 },
});
for (let i = 0; i < 5; i++) {
  const cy = 136 + 368 * (i + 0.5) / 5;
  s.addImage({
    path: path.join(ASSETS, PLANES_ENEMY[i]),
    x: 81 * P + (156 * P - PLANE_W) / 2, y: cy * P - PLANE_H / 2,
    w: PLANE_W, h: PLANE_H,
  });
}
s.addShape(pptx.shapes.RECTANGLE, {
  x: 247 * P, y: 161 * P, w: 42 * P, h: 330 * P,
  fill: { color: PINK_STRIP }, line: { color: TXT_RED, width: 1 },
});
const POS_CY = [195, 257, 319, 380, 441];
for (const cy of POS_CY) {
  s.addText("+1", {
    x: 247 * P, y: (cy - 9) * P, w: 42 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
}

// Negative Class (green) — 6 safe planes, 6x "-1"
s.addText("Negative Class", {
  x: 353 * P, y: 97 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("\u201CSafe\u201D", {
  x: 353 * P, y: 117 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 498 * P, y: 118 * P, w: 42 * P, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 331 * P, y: 136 * P, w: 151 * P, h: 368 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2.5 },
});
for (let i = 0; i < 6; i++) {
  const cy = 136 + 368 * (i + 0.5) / 6;
  s.addImage({
    path: path.join(ASSETS, PLANES_SAFE[i]),
    x: 331 * P + (151 * P - PLANE_W) / 2, y: cy * P - PLANE_H / 2,
    w: PLANE_W, h: PLANE_H,
  });
}
s.addShape(pptx.shapes.RECTANGLE, {
  x: 498 * P, y: 161 * P, w: 42 * P, h: 336 * P,
  fill: { color: GREEN_STRIP }, line: { color: TXT_GREEN, width: 1 },
});
const NEG_CY = [176, 238, 283, 336, 398, 460];
for (const cy of NEG_CY) {
  s.addText("-1", {
    x: 498 * P, y: (cy - 9) * P, w: 42 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: TEAL, fontFace: FONT, margin: 0,
  });
}

// ---- Activation Function panel x574..882 y90..165 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 574 * P, y: 90 * P, w: 308 * P, h: 75 * P,
  fill: { color: ACT_FILL }, line: { color: BLUE, width: 1.5 },
});
s.addText("Activation Function", {
  x: 596 * P, y: 96 * P, w: 204 * P, h: 20 * P,
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Bi-polar step ", options: { fontSize: 12, bold: true, color: BLUE, fontFace: FONT } },
  { text: "(-1 , +1)", options: { fontSize: 12, bold: true, color: DARK, fontFace: FONT } },
], {
  x: 583 * P, y: 118 * P, w: 170 * P, h: 18 * P,
  align: "left", valign: "middle", margin: 0,
});
s.addText("Threshold at \u201Czero\u201D", {
  x: 587 * P, y: 140 * P, w: 160 * P, h: 16 * P,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
// pink circle with bipolar step glyph at panel right (orig x811..868 y99..158, panel center y127.5)
s.addShape(pptx.shapes.OVAL, {
  x: 811 * P, y: 99 * P, w: 59 * P, h: 59 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({
  path: STEP_PLOT_S,
  x: 820 * P, y: 110 * P, w: STEP_S_W * 0.6, h: STEP_S_H * 0.6,
});

// ---- Training: heading x699..790 y177..192 + rounded panel x608..902 y206..322 ----
s.addText("Training", {
  x: 699 * P, y: 177 * P, w: 92 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 608 * P, y: 206 * P, w: 294 * P, h: 116 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
// "Input Sample" text left of the panel + hollow arrow into the Model box
s.addText("Input\nSample", {
  x: 571 * P, y: 233 * P, w: 40 * P, h: 24 * P,
  align: "left", valign: "middle",
  fontSize: 10, color: DARK, fontFace: FONT, margin: 0, lineSpacing: 11,
});
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 575 * P, y: 266 * P, w: 36 * P, h: 17 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 1.75 },
});
// Model: dark-red box x612..736 y245..305, step circle inside right, yellow caption at bottom
const MTY = 245 * P;
s.addShape(pptx.shapes.RECTANGLE, {
  x: 612 * P, y: MTY, w: 124 * P, h: 60 * P,
  fill: { color: BOX_RED },
});
s.addText("Model", {
  x: 624 * P, y: MTY + 13 * P, w: 56 * P, h: 20 * P,
  align: "left", valign: "middle",
  fontSize: 13, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 694 * P, y: MTY + 8 * P, w: 38 * P, h: 38 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({
  path: STEP_PLOT_S,
  x: 700 * P, y: MTY + 14 * P, w: STEP_S_W * 0.35, h: STEP_S_H * 0.35,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 616 * P, y: MTY + 42 * P, w: 118 * P, h: 14 * P,
  align: "left", valign: "middle", wrap: false,
  fontSize: 8, bold: true, color: CAP_YELLOW, fontFace: FONT, margin: 0,
});
// "Predicted Class" label above the Model->LOSS arrow (orig x725..787 y231..252)
s.addText("Predicted\nClass", {
  x: 725 * P, y: 231 * P, w: 62 * P, h: 24 * P,
  align: "center", valign: "middle",
  fontSize: 9, color: DARK, fontFace: FONT, margin: 0, lineSpacing: 10,
});
// hollow arrow Model -> LOSS (orig x736..794 y264..281)
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 736 * P, y: 266 * P, w: 58 * P, h: 16 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 1.75 },
});
// LOSS peach circle center (812,273) d60
s.addShape(pptx.shapes.OVAL, {
  x: 782 * P, y: 243 * P, w: 60 * P, h: 60 * P,
  fill: { color: PEACH }, line: { color: BOX_RED, width: 1.25 },
});
s.addText("LOSS", {
  x: 782 * P, y: 243 * P, w: 60 * P, h: 60 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BOX_RED, fontFace: FONT, margin: 0,
});
// "Label of Input Sample" above the hollow left arrow (orig x831..901 y216..252)
s.addText("Label of\nInput Sample", {
  x: 831 * P, y: 218 * P, w: 70 * P, h: 34 * P,
  align: "center", valign: "middle",
  fontSize: 9, color: DARK, fontFace: FONT, margin: 0, lineSpacing: 11,
});
// hollow LEFT arrow OUTSIDE the circle, head at its right edge (orig x845..885 y265..283)
s.addShape(pptx.shapes.LEFT_ARROW, {
  x: 845 * P, y: 265 * P, w: 40 * P, h: 18 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 1.75 },
});
// blue "(+1, -1)" below the left arrow (orig x835..881 y286..299)
s.addText("(+1, -1)", {
  x: 835 * P, y: 286 * P, w: 48 * P, h: 14 * P,
  align: "center", valign: "middle", wrap: false,
  fontSize: 10, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

// ---- Evaluation: heading x697..790 y352..364 + rounded panel x608..902 y380..497 ----
s.addText("Evaluation", {
  x: 697 * P, y: 352 * P, w: 93 * P, h: 14 * P,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 608 * P, y: 380 * P, w: 294 * P, h: 117 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const MEY = 420 * P;
s.addText("Test\nSample", {
  x: 561 * P, y: MEY - 5 * P, w: 52 * P, h: 24 * P,
  align: "left", valign: "middle",
  fontSize: 10, color: DARK, fontFace: FONT, margin: 0, lineSpacing: 11,
});
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 575 * P, y: MEY + 28 * P, w: 36 * P, h: 17 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 1.75 },
});
// Model box x612..736 y420..480
s.addShape(pptx.shapes.RECTANGLE, {
  x: 612 * P, y: MEY, w: 124 * P, h: 60 * P,
  fill: { color: BOX_RED },
});
s.addText("Model", {
  x: 624 * P, y: MEY + 13 * P, w: 56 * P, h: 20 * P,
  align: "left", valign: "middle",
  fontSize: 13, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 694 * P, y: MEY + 8 * P, w: 38 * P, h: 38 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({
  path: STEP_PLOT_S,
  x: 700 * P, y: MEY + 14 * P, w: STEP_S_W * 0.35, h: STEP_S_H * 0.35,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 616 * P, y: MEY + 42 * P, w: 118 * P, h: 14 * P,
  align: "left", valign: "middle", wrap: false,
  fontSize: 8, bold: true, color: CAP_YELLOW, fontFace: FONT, margin: 0,
});
s.addText("Predicted\nClass", {
  x: 735 * P, y: 407 * P, w: 52 * P, h: 22 * P,
  align: "center", valign: "middle",
  fontSize: 9, color: DARK, fontFace: FONT, margin: 0, lineSpacing: 10,
});
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 741 * P, y: MEY + 20 * P, w: 38 * P, h: 15 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 1.75 },
});
// blue "(+1, -1)" at the right end (no LOSS in evaluation; orig x788..834 y444..456)
s.addText("(+1, -1)", {
  x: 788 * P, y: MEY + 24 * P, w: 48 * P, h: 14 * P,
  align: "center", valign: "middle", wrap: false,
  fontSize: 10, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_019_recreated.pptx"
}).then(() => console.log("done"));
