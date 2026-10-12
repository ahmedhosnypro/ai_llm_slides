// Slide 059 — "KNN Assignment" (six numbered assignment steps in a red-bordered box)
// Source spec: analysis/slide_059_final.json (verified against original pixels, 2026-10-09)
// House frame per 17_worker_instructions.md (founder directive — overrides spec).
// Spec fidelity notes:
//   - step 6 wraps after "Compare" (verified on original); second line hanging-indented
//     under "Normalize" (i.e. past the "6) " prefix)
//   - "[Optional]" (step 2) and "each K" (step 5) underlined; "6)" and "Normalize" bold
//   - text VERBATIM incl. "[120 , 30 samples]" and "accuracy ?" spacing
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// House template (founder directive — overrides spec)
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE = "FFF9C4", INK = "333333";
// Content colors (verbatim from spec)
const TITLE_RED = "C00000", BODY_BLUE = "1F2E9E", BOX_RED = "B22222", WHITE = "FFFFFF";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer red frame (transparent fill, C00000 1.5pt) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG, transparency: 100 }, line: { color: FRAME_RED, width: 1.5 },
});

// ---- Title (house: y 0.28, x 0.6, w 12.13, centered) — red bold per spec ----
s.addText("KNN Assignment", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.95, align: "center", valign: "middle",
  fontSize: 36, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ---- House slide-number badge: oval 12.48/0.30/0.5/0.5, numeral "59" ----
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("59", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Content box (spec: thin red/maroon outline, white fill, ~x 8-92%, y 25-95%) ----
const BOX = { x: 1.07, y: 1.9, w: 11.19, h: 5.15 };
s.addShape(pptx.shapes.RECTANGLE, {
  x: BOX.x, y: BOX.y, w: BOX.w, h: BOX.h,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 1.75 },
});

// ---- Six numbered steps: dark blue, left-aligned, medium size ----
const STEP_X = 1.5, STEP_W = BOX.w - 0.9, STEP_H = 0.55, BODY_SIZE = 20;
const baseOpts = {
  x: STEP_X, w: STEP_W, h: STEP_H, align: "left", valign: "middle",
  fontSize: BODY_SIZE, color: BODY_BLUE, fontFace: FONT, margin: 0,
};

// step 2: "[Optional]" underlined
s.addText([
  { text: "2) Use PCA to visualize the Dataset (as 2-D) ", options: {} },
  { text: "[Optional]", options: { underline: { style: "sng" } } },
], Object.assign({ y: 3.05 }, baseOpts));

// step 5: "each K" underlined
s.addText([
  { text: "5) Calculate the classification accuracy for ", options: {} },
  { text: "each K", options: { underline: { style: "sng" } } },
  { text: ", Which is the best?", options: {} },
], Object.assign({ y: 5.15 }, baseOpts));

// steps 1, 3, 4 (plain)
[
  ["1) Download \u201cIRIS\u201d Data set (three flowers) [150 Samples]", 2.35],
  ["3) Divide the data into 80% Training, 20% test [120 , 30 samples]", 3.75],
  ["4) Apply KNN with K=3, 5, and 7 on Test Samples.", 4.45],
].forEach(([t, y]) => {
  s.addText(t, Object.assign({ y }, baseOpts));
});

// step 6: two physical lines (verified wrap point on the original).
// Line 1: "6)" + bold "Normalize" ... up to "Compare"
// Line 2: hanging indent aligned under "Normalize" (past the "6) " prefix)
const HANG = 0.42; // width of "6) " at 20pt Arial
s.addText([
  { text: "6) ", options: { bold: true } },
  { text: "Normalize", options: { bold: true } },
  { text: " the IRIS dataset and repeat steps 4 and 5. Compare", options: {} },
], Object.assign({ y: 5.85 }, baseOpts));
s.addText("with previous results, does normalization affect the accuracy ?", Object.assign({
  x: STEP_X + HANG, y: 6.45, w: STEP_W - HANG,
}, baseOpts));

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_059_recreated.pptx" })
  .then((f) => console.log("written:", f));
