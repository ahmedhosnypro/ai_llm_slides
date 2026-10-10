// Build: slide 038 recreation — "How Training Takes Place to learn the model ?"
// Spec: videos/ml-intro/analysis/slide_038_final.json (validated PASS_WITH_FIXES, score 9)
// Output: videos/ml-intro/recreated_pptx/slide_038_recreated.pptx
//
// Content (spec, kept VERBATIM): dark-red centered title; white red-bordered
// content panel (~8-92% width, ~22-95% height); five-box horizontal flowchart —
// green "Training Sample" -> dark red "Classification Model (with Model
// Parameters)" (2nd line italic) -> light blue "Predicted Class (Label)" ->
// tall beige vertical bar "Error" (rotated 90) <- pale yellow "True Label of
// the Sample" (left-pointing arrow into the Error bar); caption below the
// flowchart, left-aligned, dark red, mixed bold.
//
// HOUSE FRAME RULE (founder, 2026-10-09) — overrides spec/judge for these elements:
//   bg E8E8E8; outer frame rect x:0.15 y:0.15 w:13.03 h:7.2, line C00000 w1.5,
//   fill E8E8E8; badge oval x:12.48 y:0.30 w:0.5 h:0.5, fill FFF9C4 line FFF9C4
//   w0.5, numeral "38" bold 18pt 333333; title box starts y:0.28, x:0.6, w:12.13,
//   centered. The spec's EDEDED bg / FFF2A8 badge / own frame geometry are
//   superseded by the house values.
// Mouse-cursor artifact near the green box is a screen-capture overlay and is
// deliberately NOT recreated (recreation_brief step 16).
// No pptxgenjs bullet options anywhere (no bullets needed on this slide).

const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette (spec + house) — NO '#' prefixes (corrupts file)
const BG = "E8E8E8";        // slide background (house)
const FRAME_RED = "C00000";  // outer frame + panel border + arrows (spec)
const TITLE_RED = "B00020";  // title + caption text (spec)
const GREEN = "1E7B34";     // Training Sample box fill
const DARKRED = "8B0000";   // Classification Model box fill
const LIGHTBLUE = "D6EAF8"; // Predicted Class box fill
const BEIGE = "F5E6C8";     // Error bar fill
const PALEYELLOW = "FDF9D8";// True Label box fill
const BLUE_DARK = "1F3864"; // dark-blue borders of light boxes (spec)
const BADGE_YELLOW = "FFF9C4"; // house badge fill+line
const INK = "333333";       // badge numeral + dark text on light fills
const WHITE = "FFFFFF";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// 1. House outer red frame: 0.15 in inset from every edge, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// 2. Inner white content panel (spec: ~8-92% width, ~22-95% height), thin red border
const panelX = 1.07, panelY = 1.65, panelW = 11.20, panelH = 5.48;
s.addShape(pptx.shapes.RECTANGLE, {
  x: panelX, y: panelY, w: panelW, h: panelH,
  fill: { color: WHITE }, line: { color: FRAME_RED, width: 1.5 },
});

// 3. Title: house text-box geometry (starts y 0.28, x 0.6, w 12.13, centered),
//    verbatim text, bold dark red, largest text on the slide (~10-20% height)
s.addText("How Training Takes Place to learn the model ?", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.1, align: "center", valign: "middle",
  fontSize: 32, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// 4. House slide-number badge: yellow oval top-right, numeral = slide id "38"
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("38", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Flowchart (middle band ~25-65% height, boxes vertically centered ~3.30) ----

// Box 1: green "Training Sample" (white text)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.35, y: 2.65, w: 1.75, h: 1.30,
  fill: { color: GREEN }, line: { color: GREEN, width: 0.75 },
});
s.addText("Training Sample", {
  x: 1.35, y: 2.65, w: 1.75, h: 1.30, align: "center", valign: "middle",
  fontSize: 16, color: WHITE, fontFace: FONT, margin: 0,
});

// Arrow 1: Training Sample -> Classification Model
s.addShape(pptx.shapes.LINE, {
  x: 3.13, y: 3.30, w: 0.47, h: 0,
  line: { color: FRAME_RED, width: 2.25, endArrowType: "arrow" },
});

// Box 2 (largest): dark red "Classification Model" + italic "(with Model Parameters)"
s.addShape(pptx.shapes.RECTANGLE, {
  x: 3.63, y: 2.40, w: 2.75, h: 1.80,
  fill: { color: DARKRED }, line: { color: DARKRED, width: 0.75 },
});
s.addText([
  { text: "Classification Model", options: { fontSize: 18, breakLine: true } },
  { text: "(with Model Parameters)", options: { fontSize: 13, italic: true } },
], {
  x: 3.63, y: 2.40, w: 2.75, h: 1.80, align: "center", valign: "middle",
  color: WHITE, fontFace: FONT, margin: 0,
});

// Arrow 2: Classification Model -> Predicted Class
s.addShape(pptx.shapes.LINE, {
  x: 6.41, y: 3.30, w: 0.47, h: 0,
  line: { color: FRAME_RED, width: 2.25, endArrowType: "arrow" },
});

// Box 3: light blue with dark-blue border, "Predicted Class" / "(Label)"
s.addShape(pptx.shapes.RECTANGLE, {
  x: 6.91, y: 2.55, w: 1.70, h: 1.50,
  fill: { color: LIGHTBLUE }, line: { color: BLUE_DARK, width: 1.5 },
});
s.addText([
  { text: "Predicted Class", options: { breakLine: true } },
  { text: "(Label)", options: {} },
], {
  x: 6.91, y: 2.55, w: 1.70, h: 1.50, align: "center", valign: "middle",
  fontSize: 15, color: INK, fontFace: FONT, margin: 0,
});

// Arrow 3: Predicted Class -> Error bar
s.addShape(pptx.shapes.LINE, {
  x: 8.64, y: 3.30, w: 0.47, h: 0,
  line: { color: FRAME_RED, width: 2.25, endArrowType: "arrow" },
});

// Box 4: tall narrow beige vertical bar, "Error" rotated 90 degrees
const errX = 9.14, errY = 2.05, errW = 0.55, errH = 2.50;
s.addShape(pptx.shapes.RECTANGLE, {
  x: errX, y: errY, w: errW, h: errH,
  fill: { color: BEIGE }, line: { color: BEIGE, width: 0.75 },
});
// Rotated text frame: pre-rotation box w=errH h=errW centered on the bar,
// rotate 90 -> renders as vertical "Error" along the bar.
s.addText("Error", {
  x: errX + errW / 2 - errH / 2, y: errY + errH / 2 - errW / 2,
  w: errH, h: errW, align: "center", valign: "middle",
  fontSize: 18, color: INK, fontFace: FONT, margin: 0, rotate: 90,
});

// Box 5: pale yellow with dark-blue border, "True Label" / "of the Sample"
s.addShape(pptx.shapes.RECTANGLE, {
  x: 10.55, y: 2.55, w: 1.70, h: 1.50,
  fill: { color: PALEYELLOW }, line: { color: BLUE_DARK, width: 1.5 },
});
s.addText([
  { text: "True Label", options: { breakLine: true } },
  { text: "of the Sample", options: {} },
], {
  x: 10.55, y: 2.55, w: 1.70, h: 1.50, align: "center", valign: "middle",
  fontSize: 15, color: INK, fontFace: FONT, margin: 0,
});

// Arrow 4: True Label of the Sample -> Error (left-pointing into the Error bar)
s.addShape(pptx.shapes.LINE, {
  x: 9.72, y: 3.30, w: 0.80, h: 0,
  line: { color: FRAME_RED, width: 2.25, beginArrowType: "arrow" },
});

// 5. Caption below the flowchart, left-aligned inside the panel (~70-78% height),
//    dark red, mixed bold per spec (bold up to "error", regular "(Loss Function)")
s.addText([
  { text: "Try to update model parameters (Iteratively) to minimize error", options: { bold: true } },
  { text: " (Loss Function)", options: { bold: false } },
], {
  x: 1.45, y: 5.35, w: 10.4, h: 0.5, align: "left", valign: "top",
  fontSize: 18, color: TITLE_RED, fontFace: FONT, margin: 0,
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_038_recreated.pptx" })
  .then(() => console.log("done"));
