// slide_004.js — "Processing Sequential Data" (Deep Learning DSAI 308, Transformers Part I)
// Build worker: per-slide recreation, attempt 1.
//
// GEOMETRY PROVENANCE — PIL pixel forensics on the original frame
// videos/deep-learning/001_transformers_part1/unique_slides/slide_004.jpg (960x540, 1 px = 1 pt):
//   Panel border core: left x~38-41, top y~43-45, right x~919-922, bottom y~536-539
//     -> rect edge centers: x0.55in, y0.61in, right 12.785in, bottom 7.465in
//   Panel fill measured (231,233,230) ~ E8E8E8; outer bg measured (254,255,253) ~ FFFFFF.
//   Badge outline ellipse bbox x872..914 y54..89 -> x12.11 y0.75 w0.59 h0.49; fill (254,255,156) ~ FFFF99;
//     outline dark purple ~ 9932CC; numeral "4" ink y68..78 -> ~15pt bold black, centered.
//   Title ink: x146..788, cap top y200, descender bottom y247 -> ~49pt bold (3 word-width checks agree:
//     Processing 5.32em=259px, Sequential 4.98em=244px, Data 2.14em=105px -> em ~49); color core ~(178,15,33) ~ C00000.
//   Body lines: L1 cap top y343 baseline y367; L2 cap top y423 baseline y447; pitch 80 px = 1.111 in;
//     ink left x89 both lines; L1 ink width 769px, L2 556px -> em ~35.5 bold (two independent width checks agree);
//     color core (0,0,152) ~ 000099; gap before "(1-D CNN)" = 35px ~ 3 spaces; before "(RNN)" = 22px ~ 2 spaces.
//   Mouse-cursor artifact (~54% width, ~74% height) is a screen-recording overlay -> NOT recreated (spec + ground rule c).
//
// HOUSE CHROME NOTE: this deck's shared outer template (measured identical on slides 1-6:
// white bg + gray panel + thin red border + top-right badge; title-y varies per slide) is the
// deck instantiation of the house rule; ml-intro's literal values (bg E8E8E8 everywhere, 0.15in
// frame, title y0.28) describe the OTHER deck. Badge numeral = printed number = 4. LAYOUT_WIDE.
//
// pptxgenjs laws: no "#" in hex; fontFace everywhere; margin:0; explicit lineSpacing on the
// multi-line body box (pitch 80pt pinned from the original; empty-run pitfall avoided — no empty runs).

const pptxgen = require("pptxgenjs");

const FONT = "Arial";
const TITLE = "Processing Sequential Data";
const BODY_LINE1 = "1-D Convolutional Neural Network   (1-D CNN)"; // three spaces before "(1-D CNN)"
const BODY_LINE2 = "Recurrent Neural Network  (RNN)";              // two spaces before "(RNN)"

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const s = pres.addSlide();

// white slide background (this deck's template: white margin around the gray panel)
s.background = { color: "FFFFFF" };

// content panel: gray fill + thin red border (border centers on the rect edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.55, y: 0.61, w: 12.23, h: 6.86, // bottom edge 7.47in
  fill: { color: "E8E8E8" },
  line: { color: "C00000", width: 1.5 },
});

// title (deck template: measured title-y for THIS slide; box full-width centered)
s.addText(TITLE, {
  x: 0.6, y: 2.59, w: 12.13, h: 0.95,
  align: "center", valign: "top",
  fontSize: 49, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// two-line topic list, pinned pitch 80pt (= measured 80px @72dpi), left ink target x=89px
s.addText(
  [
    { text: BODY_LINE1, options: { breakLine: true } },
    { text: BODY_LINE2, options: {} },
  ],
  {
    x: 1.21, y: 4.09, w: 11.55, h: 2.45,
    align: "left", valign: "top",
    fontSize: 35.5, bold: true, color: "000099", fontFace: FONT,
    lineSpacing: 80, margin: 0,
  }
);

// slide-number badge (top-right, deck template geometry) + numeral 4
s.addShape(pres.shapes.OVAL, {
  x: 12.11, y: 0.75, w: 0.59, h: 0.49,
  fill: { color: "FFFF99" },
  line: { color: "9932CC", width: 1.5 },
});
s.addText("4", {
  x: 12.11, y: 0.75, w: 0.59, h: 0.49,
  align: "center", valign: "middle",
  fontSize: 16, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_004_recreated.pptx" })
  .then(() => console.log("wrote slide_004_recreated.pptx"));
