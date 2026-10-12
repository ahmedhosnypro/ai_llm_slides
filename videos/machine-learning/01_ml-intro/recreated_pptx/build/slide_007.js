// Slide 007 recreation — "Programming Languages, Platforms, and Libraries"
// Built from videos/ml-intro/analysis/slide_007_final.json (validated spec, PASS_WITH_FIXES).
// Started from the prior (old-numbering, attempt-4 PASS) build; new-namespace worker
// applied the actionable findings from the banked attempt-4 judge transcript:
//   - more bottom clearance so the last bullet "OpenCV" clears the content-box border
//   - deeper bullet indent for the heading->bullet hierarchy
//   - "+ Keras" annotation in non-italic handwriting-style font
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node videos/ml-intro/recreated_pptx/build/slide_007.js
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", RED = "C00000", TEXT = "000000",
      DARK = "333333", WHITE = "FFFFFF";
const BADGE_YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// 1. Background: solid light gray #E8E8E8 (set on slide; done above)

// HOUSE FRAME (founder directive 2026-10-09): outer red frame, 0.15in inset
// from every edge, line C00000 width 1.5, no visible fill (gray E8E8E8).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// 2. Title: full width, centered, y per house frame, red bold, wrapped over two lines
//    (banked judge evidence: original breaks after "and", not after "Platforms,")
s.addText([
  { text: "Programming Languages, Platforms, and", options: { breakLine: true } },
  { text: "Libraries", options: {} },
], {
  x: 0.6, y: 0.28, w: W - 1.2, h: H * 0.20, align: "center", valign: "middle",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 3. HOUSE FRAME slide-number badge: oval x:12.48 y:0.30 w:0.5 h:0.5,
//    fill FFF9C4, line FFF9C4 width 0.5; numeral = printed slide number "7",
//    bold 18pt, 333333.
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("7", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// 4. Content box: WHITE interior, thin red outline, bottom stops short of the
//    outer frame's bottom rule (banked judge evidence from the prior run).
const boxX = W * 0.05, boxY = H * 0.28, boxW = W * 0.43, boxH = 4.95;
s.addShape(pptx.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

// Section headers: bold red, smaller than title. Bullet items: black, round dots,
// indented to the right of the headers (banked judge evidence on hierarchy).
const bullet = { code: "2022", indent: 20 };
const innerX = boxX + 0.35, innerW = boxW - 0.6;
function header(y, text) {
  s.addText(text, {
    x: innerX, y, w: innerW, h: 0.4, fontSize: 19, bold: true,
    color: RED, fontFace: FONT, margin: 0, valign: "top",
  });
}
function list(y, items, h) {
  const rows = items.map((t, i) => ({
    text: t, options: { bullet, breakLine: i < items.length - 1 },
  }));
  s.addText(rows, {
    x: innerX, y, w: innerW, h, fontSize: 16, color: TEXT,
    fontFace: FONT, margin: 0, valign: "top",
    paraSpaceAfter: 2, lineSpacingMultiple: 1.0,
  });
}

// 5-6. Section 1: header + 3 bullets (Python, R, Matlab)
header(2.26, "Popular Languages for ML/DL");
list(2.66, ["Python", "R", "Matlab"], 0.90);

// 7-8. Section 2: header + 2 bullets (Tensor Flow, Pytorch)
header(3.52, "Popular Platforms for ML/DL");
list(3.92, ["Tensor Flow", "Pytorch"], 0.60);

// 9. Ink annotation: '+ Keras' beside the 'Tensor Flow' bullet, clearly separated
//    horizontally (~0.28in right of "Flow") and slightly above the baseline
//    (judge attempt 1 flagged the near-touch as an overprint collision).
s.addText("+ Keras", {
  x: 2.75, y: 3.78, w: 1.6, h: 0.35, fontSize: 16,
  color: DARK, fontFace: "Comic Sans MS", margin: 0, valign: "middle",
});

// 10-11. Section 3: header + 6 bullets; rhythm equalized so the list->header gap
//     matches sections 1->2 (judge attempt 1 flagged an irregular blank gap here).
header(4.49, "Popular Libraries (for python)");
list(4.89, ["SciKit Learn", "SciPy", "NLTK", "Spacy", "Gensim", "OpenCV"], 1.60);

// 12. Right region: left empty (gray background only) — no content placed.
// 13. Mouse cursor: intentionally NOT recreated (transient recording artifact).

pptx.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/ml-intro/recreated_pptx/slide_007_recreated.pptx" })
  .then(() => console.log("done"));
