// Build: slide 029 recreation — "The Complete Machine Learning Classification Process"
// Spec: videos/ml-intro/analysis/slide_029_final.json (validated PASS_WITH_FIXES, score 9;
//        staged from the pre-curation deck's slide_037_final.json — same image, new id 29)
// Output: videos/ml-intro/recreated_pptx/slide_029_recreated.pptx
//
// Title-only slide: three-line large red bold title centered inside a white
// red-bordered content box. Original frame measured at 960x540 (72 px/in):
//   white box x 69-886 px (0.96-12.31 in), y 104-484 px (1.44-6.72 in);
//   title cap bands y 194-230 / 284-319 / 371-408 px (pitch ~89 pt, caps 36 px
//   -> ~48 pt), line widths 4.64 / 5.92 / 7.47 in.
// House frame (founder directive 2026-10-09) overrides the outer chrome:
//   bg E8E8E8, red frame 0.15 in inset, badge oval 12.48/0.30/0.5/0.5 FFF9C4
//   with numeral "29" (bold 18 pt, 333333), title text box starts y 0.28,
//   x 0.6, w 12.13, centered. The original frame's printed badge digit is
//   ALSO "29" (verified against the original image by the images model), so
//   house numeral and on-slide numeral agree.
// The mouse-cursor artifact (#555555) is a screen-recording overlay and is
// deliberately NOT recreated (spec recreation_brief step 6).
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette (spec + house) — NO '#' prefixes (corrupts file)
const BG = "E8E8E8";   // slide background (house; original panel measured 231,233,230)
const RED = "C00000";  // title text + all borders (spec colors / house frame)
const WHITE = "FFFFFF";
const BADGE_YELLOW = "FFF9C4"; // house badge fill+line
const INK = "333333";  // badge numeral
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// 1. House outer red frame: 0.15 in inset from every edge, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// 2. Inner white content box (measured from the original frame), thin red border
const boxX = 0.96, boxY = 1.44, boxW = 11.35, boxH = 5.28;
s.addShape(pptx.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// 3. Title: house text-box geometry (starts y 0.28, x 0.6, w 12.13, centered).
//    Tall box + valign middle so the three rendered lines sit centered inside
//    the white content box exactly as in the original (cap band center ~4.1 in).
s.addText(
  [
    { text: "The Complete", options: { breakLine: true } },
    { text: "Machine Learning", options: { breakLine: true } },
    { text: "Classification Process", options: {} },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 7.33,
    align: "center", valign: "middle",
    fontSize: 51, bold: true, color: RED, fontFace: FONT, margin: 0,
    lineSpacing: 89,
  }
);

// 4. House slide-number badge: yellow oval top-right, numeral = slide id "29"
//    (also the number printed on the original slide image)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("29", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_029_recreated.pptx" })
  .then(() => console.log("done"));
