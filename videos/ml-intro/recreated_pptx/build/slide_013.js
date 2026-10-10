// Slide 013 recreation — "Supervised Learning: Classification"
// Spec: videos/ml-intro/analysis/slide_013_final.json (validation verdict
// PASS_WITH_FIXES, score 9/10; POS output row corrected to bold all-caps from
// direct vision reads of the original — qa/slide014/judge_attempt_1.txt + _2.txt)
// House frame rule (founder directive 2026-10-09) overrides spec for outer chrome:
// bg E8E8E8; red frame x:0.15 y:0.15 w:13.03 h:7.2 line C00000 w1.5; badge oval
// x:12.48 y:0.30 w:0.5 h:0.5 fill/line FFF9C4 with numeral "13" bold 18pt #333333;
// title box y:0.28 x:0.6 w:12.13 centered.
// Started from build/slide_014.js (same slide, old pre-curation numbering 14):
// badge digit 14 -> 13; body lines plain (no bullet dots), 17pt, pitch 0.40;
// POS output row bold all-caps (judge evidence); table tucked up closer to the
// body text and compacted per judge_attempt_2.txt ("original table smaller/
// compact, closer to the body text").

const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

const BG = "E8E8E8";           // house-template background
const HOUSE_RED = "C00000";    // house outer frame line
const BADGE_YELLOW = "FFF9C4"; // house badge fill/line
const INK = "333333";          // house badge digit color
const TITLE_RED = "CC3300";    // 'Supervised Learning:' (spec colors.title_text)
const BLUE = "0000CC";         // 'Classification' + section headers (spec hierarchy)
const EMPH_RED = "CC0000";     // 'When y is a vector...' emphasis (spec hierarchy)
const GREEN = "33CC33";        // 'Image annotation' (spec hierarchy)
const TEXT = "000000";         // body text
const WHITE = "FFFFFF";        // content box fill
const BOX_BORDER = "AA3333";   // content box border (~1pt, spec visual_elements)
const GRID = "CCCCCC";         // table cell borders (~0.5-1pt)
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE FRAME: outer red rectangle, 0.15in inset, fill invisible gray ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: HOUSE_RED, width: 1.5 },
});

// ---- HOUSE FRAME: title box y:0.28 x:0.6 w:12.13, centered ----
// Spec: 'Supervised Learning:' red-orange CC3300 bold; 'Classification' blue 0000CC
// bold + underlined. ~28pt (spec approximation), largest text on the slide.
s.addText([
  { text: "Supervised Learning: ", options: { color: TITLE_RED } },
  { text: "Classification", options: { color: BLUE, underline: true } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 1.1, align: "center", valign: "middle",
  fontSize: 28, bold: true, fontFace: FONT, margin: 0,
});

// ---- HOUSE FRAME: slide-number badge, numeral is the slide id "13" ----
// (original image badge reads 13; confirmed by qa/slide014/judge_attempt_2.txt)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("13", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Content box: white fill, thin red/maroon AA3333 border, ~5-95% w, ~25-95% h ----
const BOX = { x: 0.67, y: 1.875, w: 12.0, h: 5.25 };
s.addShape(pptx.shapes.RECTANGLE, {
  x: BOX.x, y: BOX.y, w: BOX.w, h: BOX.h,
  fill: { color: WHITE }, line: { color: BOX_BORDER, width: 1 },
});

// ---- 8 body lines, one text box per line, NO bullet glyphs ----
// Judge attempt 1 (direct read of the original, high confidence): the original's
// body lines are PLAIN indented lines with no bullet dots. Section-header lines
// (1 and 6, the "[n] ..." lines) are bold blue. Variables x and y italic
// (spec typography_notes).
const BODY = 17; // body slightly smaller/tighter per judge attempt 1 (spec ~18pt approx)
const LINE_H = 0.40;
let ty = 2.2;

function line(runs, opts) {
  s.addText(runs, Object.assign({
    x: 1.0, y: ty, w: 11.4, h: LINE_H, align: "left", valign: "middle",
    fontSize: BODY, fontFace: FONT, margin: 0,
  }, opts || {}));
}

// 1. '[3] Multi-label Classification:' — bold blue, no bullet
line([{ text: "[3] Multi-label Classification:", options: { bold: true, color: BLUE } }]);
ty += LINE_H;

// 2. 'When y is a vector of discrete variables' — red CC0000, y italic
line([
  { text: "When ", options: { color: EMPH_RED } },
  { text: "y", options: { color: EMPH_RED, italic: true } },
  { text: " is a vector of discrete variables", options: { color: EMPH_RED } },
], { y: ty });
ty += LINE_H;

// 3. 'Each input x has multiple labels' — black, x italic
line([
  { text: "Each input ", options: { color: TEXT } },
  { text: "x", options: { color: TEXT, italic: true } },
  { text: " has multiple labels", options: { color: TEXT } },
], { y: ty });
ty += LINE_H;

// 4. 'Each element of y is one label (individual labels can be binary/multi-class)'
line([
  { text: "Each element of ", options: { color: TEXT } },
  { text: "y", options: { color: TEXT, italic: true } },
  { text: " is one label (individual labels can be binary/multi-class)", options: { color: TEXT } },
], { y: ty });
ty += LINE_H;

// 5. 'Example: Image annotation (each image can have multiple labels)'
line([
  { text: "Example: ", options: { color: TEXT, bold: true } },
  { text: "Image annotation", options: { color: GREEN } },
  { text: " (each image can have multiple labels)", options: { color: TEXT } },
], { y: ty });
ty += LINE_H;

// 6. '[4] Structured Prediction: When y is a vector with a structure' — mixed, no bullet
line([
  { text: "[4] Structured Prediction: ", options: { bold: true, color: BLUE } },
  { text: "When ", options: { color: EMPH_RED } },
  { text: "y", options: { color: EMPH_RED, italic: true } },
  { text: " is a vector with a structure", options: { color: EMPH_RED } },
], { y: ty });
ty += LINE_H;

// 7. 'Elements of y are not independent but related to each-other'
line([
  { text: "Elements of ", options: { color: TEXT } },
  { text: "y", options: { color: TEXT, italic: true } },
  { text: " are not independent but related to each-other", options: { color: TEXT } },
], { y: ty });
ty += LINE_H;

// 8. 'Example: Predicting parts-of-speech (POS) tags for a sentence'
line([
  { text: "Example: ", options: { color: TEXT, bold: true } },
  { text: "Predicting parts-of-speech (POS) tags for a sentence", options: { color: TEXT } },
], { y: ty });

// ---- POS example table: 2 rows x 8 cols, bottom-center of the content box ----
// Header cells 'Input'/'Output' blue 0000CC; input-row cells black title case;
// output-row cells black BOLD ALL-CAPS (judge attempts 1+2, high confidence: the
// original's POS tags are bold caps 'DET NOUN VERB DET ADV ADJ NOUN'); thin gray
// CCCCCC borders; smallest text; compact cells, centered, tucked closer under the
// body text per judge_attempt_2.txt.
const cell = (t, isHeader, caps) => ({
  text: t,
  options: {
    color: isHeader ? BLUE : TEXT,
    bold: !!caps,
    align: "center", valign: "middle",
    fontFace: FONT, fontSize: 13,
    fill: { color: WHITE },
    border: { type: "solid", pt: 0.75, color: GRID },
  },
});
const inputRow = ["Input", "The", "man", "ate", "the", "really", "tasty", "sandwich"]
  .map((t, i) => cell(t, i === 0, false));
const outputRow = ["Output", "DET", "NOUN", "VERB", "DET", "ADV", "ADJ", "NOUN"]
  .map((t, i) => cell(t, i === 0, i > 0));

const TBL_W = 8.25;            // header col 0.90 + 7 word cols at 1.05 — compact
const colW = [0.9, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05];
s.addTable([inputRow, outputRow], {
  x: (W - TBL_W) / 2,        // compact and centered, closer under the body text
  y: 5.85, w: TBL_W,
  rowH: [0.34, 0.34],
  colW: colW,
  margin: 0.02,
  align: "center", valign: "middle",
  fontFace: FONT, fontSize: 13,
});

// NOTE: the mouse-cursor arrow near the '[4] Structured Prediction' line is a
// video-recording overlay and is deliberately NOT recreated (spec animation_state
// + recreation_brief step 16).

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_013_recreated.pptx" })
  .then(() => console.log("written: recreated_pptx/slide_013_recreated.pptx"));
