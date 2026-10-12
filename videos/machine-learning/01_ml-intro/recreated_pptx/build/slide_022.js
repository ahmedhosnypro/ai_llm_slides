// Slide 022 recreation — "Other Paradigms: Active Learning" — attempt 1
// Spec: analysis/slide_022_final.json (validated, PASS_WITH_FIXES, score 9)
// Started from the old-deck build build/slide_029.js (old id 29), renumbered:
// badge digit 29 -> 22 (which also matches the original frame's printed digit
// "22", per founder directive, deck curation 2026-10-09). No other renumbering.
//
// HOUSE FRAME RULE (founder, 2026-10-09) — overrides spec/judge for these elements:
//   bg E8E8E8; outer frame rect x:0.15 y:0.15 w:13.03 h:7.2, line C00000 w:1.5, no fill;
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5, fill FFF9C4 line FFF9C4, number bold 18pt 333333;
//   title box starts y:0.28, x:0.6, w:12.13, align center.
//
// BULLET IMPLEMENTATION NOTE (why manual glyphs): pptxgenjs 4.0.1 cannot render a
// bullet on a multi-run paragraph — STEP 5 starts a new paragraph for any run that
// carries `bullet`, and every run emits its own <a:pPr>, where a run WITHOUT bullet
// emits <a:buNone/>, which LibreOffice applies over the first run's bullet (this is
// exactly what the old-deck judge attempt 1 flagged: lines 6/7/8 lost their
// markers). So the bullet glyphs are rendered manually in the text ("• " / "– "),
// one text box per line, positioned per level — which also reproduces the
// original's ".. the ones" line ("– .. the ones ..."). No paragraph-level options
// are set on these boxes so multi-run paragraphs emit a single clean pPr.
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", BLUE = "0000CC", BADGE = "FFF9C4", INK = "333333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE outer frame: red rectangle, 0.15in inset from every edge
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});

// HOUSE title box: starts y:0.28, x:0.6, w:12.13, centered
s.addText("Other Paradigms: Active Learning", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "middle",
  fontSize: 32, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// HOUSE slide-number badge — badge numeral is the number PRINTED ON THE ORIGINAL
// SLIDE IMAGE (founder directive, deck curation 2026-10-09). The original frame
// videos/ml-intro/unique_slides/slide_022.jpg prints "22", so the badge reads "22".
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 1 },
});
s.addText("22", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Content box: rounded rectangle, thin red outline; interior matches the canvas
// (in the original the box interior is the same color as the slide background)
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.67, y: 1.88, w: 12.0, h: 5.07,
  fill: { color: BG }, line: { color: RED, width: 1.75 },
  rectRadius: 0.12,
});

// 10 lines, manual bullets, manual per-level x offsets:
//   level 1 (main): bullet "• ", text box x 1.15, fontSize 20
//   level 2 (sub):  bullet "– ", text box x 1.65, fontSize 18
const MAIN_X = 1.15, SUB_X = 1.65;
let y = 2.2;
function line(level, runs) {
  const main = level === 1;
  const size = main ? 20 : 18;
  const h = main ? 0.42 : 0.38;
  s.addText(runs, {
    x: main ? MAIN_X : SUB_X, y, w: main ? 11.0 : 10.5, h,
    valign: "top", fontFace: FONT, color: TEXT, fontSize: size, margin: 0,
  });
  y += h + 0.07;
}

line(1, [{ text: "• Similar motivation as semi-supervised learning (saving data labeling cost)" }]);
line(1, [{ text: "• Standard supervised learning is passive" }]);
line(2, [{ text: "– Learner has no choice for the data it has to learn from" }]);
line(2, [{ text: "– Not all labeled examples are really informative" }]);
line(2, [{ text: "– Spending labeling efforts on uninformative examples isn't really worth it" }]);
line(1, [
  { text: "• Active Learning: ", options: {} },
  { text: "allows the learner to ask for specific labeled", options: { color: BLUE } },
  { text: " examples", options: {} },
]);
line(2, [
  { text: "– .. the ones it considers the ", options: {} },
  { text: "most informative", options: { bold: true, underline: true } },
]);
line(1, [
  { text: "• Active Learning can lead to ", options: {} },
  { text: "several benefits:", options: { bold: true, underline: true } },
]);
line(2, [{ text: "– Less labeled data needed to learn" }]);
line(2, [{ text: "– Better classifiers" }]);

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_022_recreated.pptx" }).then(() => console.log("done"));
