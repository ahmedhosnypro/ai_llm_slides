// Slide 041 recreation — "K -Nearest Neighbors Algorithm"
// Spec: analysis/slide_041_final.json (validated PASS_WITH_FIXES, fixes applied)
// Ground truth image: unique_slides/slide_041.jpg (md5-identical to the kept frame
//   frame_03552.jpg the spec was validated against; printed badge digit "41").
// House frame (founder directive 2026-10-09, OVERRIDES spec for the outer chrome):
//   background E8E8E8, red frame x:0.15 y:0.15 w:13.03 h:7.2 line C00000 w1.5,
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill FFF9C4 line FFF9C4, numeral "41"
//   (bold 18pt, color 333333) — matches the number printed on the original slide.
//   Title text box y:0.28 x:0.6 w:12.13, centered.
// Started from the old-numbered build slide_053.js (judge-certified PASS under the
//   old deck numbering); badge digit changed 53 -> 41 per deck curation 2026-10-09.
// Spec content (verbatim, [?] markers kept, no invented facts):
//   - split-colored title: "K -Nearest Neighbors" red CC0000, "Algorithm" blue 0000CC
//   - red/maroon B03030 content box, no visible fill, ~15-100% slide height, side margins
//   - 4 round bullets (black, key phrase bold blue 0000CC) in the upper part
//   - blank line, then Note line ('non-parametric' underlined),
//     bullet "Unlike other supervised learning algorithms,",
//     bold red "K -Nearest Neighbors doesn't:" ('doesn't' underlined),
//     two en-dash sub-bullets (smaller).
// Mouse cursor in the original frame is a video artifact — NOT recreated.
// Uncertain per spec: exact point sizes (relative hierarchy only); "Note:" not bolded.
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

const BG = "E8E8E8", FRAME_RED = "C00000", BOX_RED = "B03030",
      TITLE_RED = "CC0000", TITLE_BLUE = "0000CC", TEXT = "000000",
      BADGE_YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House chrome (founder directive; overrides spec) ----
// Outer red frame, 0.15in inset from every edge, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// Slide-number badge with this slide's own id "41" (matches the original's printed digit)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("41", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Title (house geometry: y 0.28, x 0.6, w 12.13, centered) ----
// Split-colored, verbatim including the extracted "K -Nearest" spacing.
s.addText([
  { text: "K -Nearest Neighbors ", options: { color: TITLE_RED } },
  { text: "Algorithm", options: { color: TITLE_BLUE } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 1.0, align: "center", valign: "middle",
  fontSize: 32, bold: true, fontFace: FONT, margin: 0,
});

// ---- Content box: thin red/maroon border, no visible fill ----
// Spec: ~15-100% of slide height, full width with side margins.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.55, y: 1.45, w: 12.23, h: 5.7,
  fill: { color: BG }, line: { color: BOX_RED, width: 1.5 },
});

// ---- Bullets block (upper part of content box, ~25-55% slide height) ----
// pptxgenjs `bullet` on multi-run paragraphs does NOT render in LibreOffice
// (single-string boxes do) — use a literal "•  " prefix run instead (old-deck lesson).
const BULLET_PREFIX = "\u2022  "; // round bullet + two spaces
const bulletLines = [
  [
    { text: BULLET_PREFIX, options: { color: TEXT } },
    { text: "Compute", options: { bold: true, color: TITLE_BLUE } },
    { text: " the test point\u2019s distance from each training point", options: {} },
  ],
  [
    { text: BULLET_PREFIX, options: { color: TEXT } },
    { text: "Sort", options: { bold: true, color: TITLE_BLUE } },
    { text: " the distances in ascending (or descending) order", options: {} },
  ],
  [
    { text: BULLET_PREFIX, options: { color: TEXT } },
    { text: "Use the sorted distances to ", options: {} },
    { text: "select the K nearest neighbors", options: { bold: true, color: TITLE_BLUE } },
  ],
  [
    { text: BULLET_PREFIX, options: { color: TEXT } },
    { text: "Use ", options: {} },
    { text: "majority rule", options: { bold: true, color: TITLE_BLUE } },
    { text: " (for classification) or averaging (for regression)", options: {} },
  ],
];
// One text box per bullet line for exact vertical placement
bulletLines.forEach((runs, i) => {
  const para = runs.map((r) => ({
    text: r.text,
    options: { color: TEXT, fontFace: FONT, ...(r.options || {}) },
  }));
  s.addText(para, {
    x: 1.05, y: 1.95 + i * 0.52, w: 11.2, h: 0.5,
    fontSize: 21, color: TEXT, fontFace: FONT, margin: 0, valign: "top",
  });
});

// ---- Note block (lower part, ~60-100% slide height) ----
const bu = () => ({ code: "2022", indent: 12 }); // works on single-string boxes
// Note line: black, 'non-parametric' underlined ("Note:" left plain — uncertain per spec)
s.addText([
  { text: "Note: K -Nearest Neighbors is called a ", options: {} },
  { text: "non-parametric", options: { underline: true } },
  { text: " method", options: {} },
], {
  x: 1.05, y: 4.4, w: 11.2, h: 0.45,
  fontSize: 20, color: TEXT, fontFace: FONT, margin: 0, valign: "top",
});

// Round bullet "Unlike other supervised learning algorithms,"
s.addText("Unlike other supervised learning algorithms,", {
  x: 1.05, y: 4.98, w: 11.2, h: 0.45,
  fontSize: 20, color: TEXT, fontFace: FONT, margin: 0, valign: "top",
  bullet: bu(),
});

// Emphasis line: bold red, 'doesn't' underlined (no bullet marker per spec)
s.addText([
  { text: "K -Nearest Neighbors ", options: {} },
  { text: "doesn\u2019t", options: { underline: true } },
  { text: ":", options: {} },
], {
  x: 1.05, y: 5.56, w: 11.2, h: 0.45,
  fontSize: 20, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0, valign: "top",
});

// Two indented en-dash sub-bullets (smaller text).
// Spaced en-dash "– " literal prefix (bullet code 2013 renders attached to the
// text in LibreOffice); indentation kept (old-deck lesson).
const subBullets = [
  "\u2013 learn an explicit mapping f from the training data",
  "\u2013 It simply uses the training data at the test time to make predictions",
];
subBullets.forEach((t, i) => {
  s.addText(t, {
    x: 1.75, y: 6.12 + i * 0.44, w: 10.5, h: 0.4,
    fontSize: 18, color: TEXT, fontFace: FONT, margin: 0, valign: "top",
  });
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_041_recreated.pptx" })
  .then(() => console.log("written: videos/ml-intro/recreated_pptx/slide_041_recreated.pptx"));
