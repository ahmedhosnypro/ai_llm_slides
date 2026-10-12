// Build: slide 030 recreation — "The Complete ML Classification Process" flowchart slide.
// Spec: videos/ml-intro/analysis/slide_030_final.json (validated PASS_WITH_FIXES, score 9/10)
// Output: videos/ml-intro/recreated_pptx/slide_030_recreated.pptx
//
// NOTE (2026-10-09 re-curation): this file replaces the previous live build script, which
// belonged to the superseded numbering round (the old "Data Sets" divider slide). Its
// per-attempt provenance copies remain banked in qa/slide030/build_attempt_*.js.
//
// HOUSE FRAME RULE (founder, 2026-10-09; recorded in AGENTS.md and
// scripts/17_worker_instructions.md): every slide uses slide 3's shared outer template,
// OVERRIDING the spec JSON and any judge finding for these elements — background E8E8E8,
// outer red frame (rect x:0.15 y:0.15 w:13.03 h:7.2, line C00000 width 1.5, no visible
// fill over BG), slide-number badge (oval x:12.48 y:0.30 w:0.5 h:0.5, fill/line FFF9C4,
// numeral = number printed on the original image = "30", bold 18pt 333333), slide-title
// text box (y:0.28, x:0.6, w:12.13, align center; slide-3 style: red bold 30pt Arial).
// Judge discrepancies about frame/badge/title-y are OVERRIDDEN — not fix triggers.
//
// Content layer per spec (geometry pinned by direct PIL measurement of
// videos/ml-intro/unique_slides/slide_030.jpg, 960x540 px -> 13.33x7.5 in, 1px = 1pt):
// white card (px x 69-896, y 102-485) with thin C00000 border holding the flowchart;
// beige "Training Data" oval upper-left -> five pastel process boxes in a middle band
// (Pre processing FFFDE7/blue outline, Feature Extraction D6E4F0/blue, Feature Selection
// D9EAD3/green, Classification B30000 white text, Post processing E6CCFF/purple) joined
// by red CC0000 arrows; four gray E8E8E8 rounded caption boxes under the arrow gaps
// (Cleaned Data, Feature Vectors, Final Features, Predicted Class); yellow FFFF66
// "Final Result" oval lower-right fed by a red arrow from Post processing.
// The mouse cursor in the original (imagery/animation_state lecture-capture artifact)
// is deliberately NOT recreated. Box outline colors are PIL-sampled approx hexes of the
// colored outlines captured on the original frame (archived analysis_old104/slide_038_raw.json).

const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette — NO '#' prefixes (corrupts the file), never 8-char hex
const BG = "E8E8E8";          // slide background light gray (house)
const HOUSE_RED = "C00000";  // house frame line, house title, card border
const BADGE_YELLOW = "FFF9C4"; // house badge fill/line
const INK = "333333";         // badge numeral
const CARD_WHITE = "FFFFFF";  // white content card fill
const ARROW_RED = "CC0000";   // flow arrows
const TEXT_BLACK = "000000";
const CAPTION_GRAY = "E8E8E8"; // caption box fill
const CAPTION_TEXT = "595959"; // caption text (spec: standard medium gray)
// Flow node fills (spec)
const OVAL_BEIGE = "F5E0C8";  // Training Data oval
const BOX_YELLOW = "FFFDE7";  // Pre processing
const BOX_BLUE = "D6E4F0";    // Feature Extraction
const BOX_GREEN = "D9EAD3";   // Feature Selection
const BOX_DARKRED = "B30000"; // Classification
const BOX_LAVENDER = "E6CCFF";// Post processing
const OVAL_RESULT = "FFFF66"; // Final Result oval
// PIL-sampled outline approx hexes of the original colored box outlines
const LINE_BLUE1 = "5F568B";  // Pre processing outline
const LINE_BLUE2 = "555C92";  // Feature Extraction outline
const LINE_GREEN = "74A588";  // Feature Selection outline
const LINE_DARKRED = "7A0004"; // Classification outline
const LINE_PURPLE = "8D4295"; // Post processing outline
const LINE_TAN = "B4B4A8";    // Training Data oval outline (washed gray-tan)

const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---------------- HOUSE FRAME 1: outer thin red frame inset 0.15in ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: HOUSE_RED, width: 1.5 },
});

// ---------------- HOUSE FRAME 2: slide-title text box (slide-3 template style) ----------------
s.addText(
  [
    { text: "The Complete ML ", options: {} },
    { text: "Classification", options: { underline: true } },
    { text: " Process", options: {} },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "middle",
    fontSize: 30, bold: true, color: HOUSE_RED, fontFace: FONT, margin: 0,
  }
);

// ---------------- HOUSE FRAME 3: slide-number badge, top-right inside the frame ----------------
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("30", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---------------- Content: white card with thin red border ----------------
// Original frame px x 69-896, y 102-485 -> in 0.96/1.42, w 11.48, h 5.32
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.96, y: 1.42, w: 11.48, h: 5.32,
  fill: { color: CARD_WHITE }, line: { color: HOUSE_RED, width: 1.5 },
});

// ---------------- Start node: beige "Training Data" oval, upper-left ----------------
s.addShape(pptx.shapes.OVAL, {
  x: 1.1, y: 2.03, w: 1.79, h: 0.76,
  fill: { color: OVAL_BEIGE }, line: { color: LINE_TAN, width: 0.75 },
});
s.addText("Training Data", {
  x: 1.1, y: 2.03, w: 1.79, h: 0.76, align: "center", valign: "middle",
  fontSize: 12, bold: true, color: TEXT_BLACK, fontFace: FONT, margin: 0,
});

// Curved red arrow: Training Data oval bottom -> left edge of Pre processing box
s.addShape("curvedConnector2", {
  x: 1.39, y: 2.82, w: 0.62, h: 0.58,
  fill: { type: "none" },
  line: { color: ARROW_RED, width: 2, endArrowType: "triangle" },
});

// ---------------- Five process boxes, middle band (y ~3.0-3.8) ----------------
// 1. Pre processing (pale yellow, blue outline; wraps to two lines)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 2.06, y: 3.0, w: 1.39, h: 0.81,
  fill: { color: BOX_YELLOW }, line: { color: LINE_BLUE1, width: 1 },
});
s.addText(
  [
    { text: "Pre", options: { breakLine: true } },
    { text: "processing" },
  ],
  {
    x: 2.06, y: 3.0, w: 1.39, h: 0.81, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: TEXT_BLACK, fontFace: FONT, margin: 0,
  }
);

// 2. Feature Extraction (light blue, blue outline)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.04, y: 3.04, w: 1.85, h: 0.76,
  fill: { color: BOX_BLUE }, line: { color: LINE_BLUE2, width: 1 },
});
s.addText("Feature Extraction", {
  x: 4.04, y: 3.04, w: 1.85, h: 0.76, align: "center", valign: "middle",
  fontSize: 13, bold: true, color: TEXT_BLACK, fontFace: FONT, margin: 0,
});

// 3. Feature Selection (light green, green outline)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 6.19, y: 3.06, w: 1.53, h: 0.74,
  fill: { color: BOX_GREEN }, line: { color: LINE_GREEN, width: 1 },
});
s.addText("Feature Selection", {
  x: 6.19, y: 3.06, w: 1.53, h: 0.74, align: "center", valign: "middle",
  fontSize: 13, bold: true, color: TEXT_BLACK, fontFace: FONT, margin: 0,
});

// 4. Classification (dark red, white text — largest, most saturated box)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 8.17, y: 3.01, w: 1.83, h: 0.82,
  fill: { color: BOX_DARKRED }, line: { color: LINE_DARKRED, width: 1 },
});
s.addText("Classification", {
  x: 8.17, y: 3.01, w: 1.83, h: 0.82, align: "center", valign: "middle",
  fontSize: 13, bold: true, color: CARD_WHITE, fontFace: FONT, margin: 0,
});

// 5. Post processing (lavender, purple outline; wraps to two lines)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 10.44, y: 3.07, w: 1.47, h: 0.71,
  fill: { color: BOX_LAVENDER }, line: { color: LINE_PURPLE, width: 1 },
});
s.addText(
  [
    { text: "Post", options: { breakLine: true } },
    { text: "processing" },
  ],
  {
    x: 10.44, y: 3.07, w: 1.47, h: 0.71, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: TEXT_BLACK, fontFace: FONT, margin: 0,
  }
);

// ---------------- Red arrows between consecutive boxes (row center y ~3.42) ----------------
function hArrow(x, w) {
  s.addShape(pptx.shapes.LINE, {
    x: x, y: 3.42, w: w, h: 0,
    line: { color: ARROW_RED, width: 2, endArrowType: "triangle" },
  });
}
hArrow(3.45, 0.59); // Pre processing -> Feature Extraction
hArrow(5.89, 0.3);  // Feature Extraction -> Feature Selection
hArrow(7.72, 0.45); // Feature Selection -> Classification
hArrow(10.0, 0.44); // Classification -> Post processing

// ---------------- Gray rounded caption boxes under the arrow gaps ----------------
function caption(x, label) {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: x, y: 4.21, w: 1.21, h: 0.57, rectRadius: 0.08,
    fill: { color: CAPTION_GRAY },
  });
  s.addText(label, {
    x: x, y: 4.21, w: 1.21, h: 0.57, align: "center", valign: "middle",
    fontSize: 10, color: CAPTION_TEXT, fontFace: FONT, margin: 0,
  });
}
caption(3.35, "Cleaned Data");       // under Pre processing -> Feature Extraction gap
caption(5.36, "Feature Vectors");    // under Feature Extraction -> Feature Selection gap
caption(7.46, "Final Features");     // under Feature Selection -> Classification gap
caption(9.64, "Predicted Class");    // under Classification -> Post processing gap

// ---------------- End node: yellow "Final Result" oval, lower-right ----------------
s.addShape(pptx.shapes.OVAL, {
  x: 11.06, y: 4.5, w: 1.28, h: 0.57,
  fill: { color: OVAL_RESULT },
});
s.addText("Final Result", {
  x: 11.06, y: 4.5, w: 1.28, h: 0.57, align: "center", valign: "middle",
  fontSize: 11, bold: true, color: TEXT_BLACK, fontFace: FONT, margin: 0,
});

// Red arrow: Post processing box bottom down into the Final Result oval
s.addShape(pptx.shapes.LINE, {
  x: 11.67, y: 3.78, w: 0.02, h: 0.68,
  line: { color: ARROW_RED, width: 2, endArrowType: "triangle" },
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_030_recreated.pptx" })
  .then(() => console.log("done"));
