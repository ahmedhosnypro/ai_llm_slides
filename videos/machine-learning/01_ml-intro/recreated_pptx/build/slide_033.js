// Slide 033 recreation — "Feature Invariants"
// pptxgenjs 4.0.1; house frame rule (founder directive 2026-10-09) + analysis/slide_033_final.json
// Started from old-deck build/slide_042.js (same slide, pre-curation id 42); badge numeral
// corrected to the printed number "33" (house rule, deck curation 2026-10-09).
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Colors (NO "#" prefix — corrupts the file)
const BG = "E8E8E8";       // house background (also spec's header band color)
const RED = "C00000";      // house outer frame
const INK = "333333";      // badge numeral / dark outline
const BADGE = "FFF9C4";    // badge fill (house)
const BLACK = "000000";
const SPECRED = "CC3333";  // spec: content-box border red
const HDRRED = "CC0000";   // spec: bold red header text 'Features Invariants are'
const BLUEBOX = "CCE5FF";  // spec: title box fill
const BLUELINE = "0000CC"; // spec: title box outline
const WHITE = "FFFFFF";    // content frame fill
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer chrome (overrides spec AND judge) ----
// Outer red frame
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
// Slide-number badge: oval, numeral "33" (house rule: number printed on the
// original slide image; slide_033.jpg is named by that printed number)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("33", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Spec content ----
// Content box: red (#CC3333) outlined white box, ~7-93% width, ~20-95% height
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.93, y: 1.50, w: 11.47, h: 5.62,
  fill: { color: WHITE }, line: { color: SPECRED, width: 2 },
});

// Title box (spec): light-blue rect with dark blue outline, bold black text.
// House rule: title text box y:0.28, x:0.6, w:12.13, centered (039 precedent: snug box centered)
// Old-deck judge A1: title glyphs crowded/overflowed the box — smaller font, wider box.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.37, y: 0.28, w: 4.6, h: 0.75,
  fill: { color: BLUEBOX }, line: { color: BLUELINE, width: 1.25 },
});
s.addText("Feature Invariants", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.75,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Header line (multi-run, NO bullet options): 'Features Invariants are' bold red
// + ' Problem dependent' italic underlined black
s.addText(
  [
    { text: "Features Invariants are", options: { bold: true, color: HDRRED, fontFace: FONT } },
    { text: " Problem dependent", options: { italic: true, underline: true, color: BLACK, fontFace: FONT } },
  ],
  {
    x: 1.35, y: 1.80, w: 10.2, h: 0.5, align: "left", valign: "middle",
    fontSize: 20, margin: 0,
  }
);

// Four bullets: one text box per line (bullet-bug workaround: manual "• " glyphs)
// Old-deck judge A1: original bullets are BOLD, start higher, tighter spacing, less indent.
const LX = 1.15; // near left edge of inner box (judge A1: deeper indent was wrong)
const bullets = [
  "Rotation Invariant",
  "Scaling Invariant",
  "Translation invariant", // verbatim lowercase 'i'
  "Mirroring Invariant",
];
let by = 2.60;
for (const b of bullets) {
  s.addText("\u2022 " + b, {
    x: LX, y: by, w: 4.6, h: 0.42, align: "left", valign: "middle",
    fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
  by += 0.48;
}

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_033_recreated.pptx" }).then(() => console.log("done"));
