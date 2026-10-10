// Slide 061 — "Example of High Dimensional Data (IRIS Dataset)"
// Source spec: videos/ml-intro/analysis/slide_061_final.json (validated, PASS_WITH_FIXES, score 9)
// House frame per 17_worker_instructions.md (founder directive, overrides spec chrome).
// Attempt 2 (judge attempt-1 fixes): left panel is a SINGLE composite crop of the
// original panel (table + braces + labels + flower diagram as one clean element,
// per the judge's explicit recommendation) — eliminates the crop/native seams,
// the Petal-label white patch, the table collision, and the duplicated
// "Class labels (targets)" text. Subtitle moved up to tighten the title gap
// (judge MINOR). Native: house chrome, title, subtitle, photo panel, banner.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// House template colors
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE = "FFF9C4", INK = "333333";
// Content colors (verbatim from spec)
const TITLE_RED = "A00000", SUB_BLUE = "0000CC";
const BAN_RED = "C00000", BAN_BLUE = "0000CC";
const FONT = "Arial";
const ASSETS = "videos/ml-intro/recreated_pptx/build/assets/";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer red frame ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// ---- House slide-number badge: oval 12.48/0.30/0.5/0.5, numeral "61" ----
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("61", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Title (house: y 0.28, x 0.6, w 12.13, centered) ----
s.addText("Example of High Dimensional Data", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.75, align: "center", valign: "top",
  fontSize: 30, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});
// ---- Subtitle "(IRIS Dataset)" directly beneath, bold blue (tight gap, judge MINOR fix) ----
s.addText("(IRIS Dataset)", {
  x: 0.6, y: 0.80, w: 12.13, h: 0.5, align: "center", valign: "top",
  fontSize: 26, bold: true, color: SUB_BLUE, fontFace: FONT, margin: 0,
});

// ---- Left panel: single composite crop of the original panel ----
// (data table with verbatim values, Samples/Features/Class-labels braces,
//  blue iris illustration with Petal/Sepal/length/width annotations)
s.addImage({ path: ASSETS + "slide061_panel.png", x: 1.666, y: 2.611, w: 5.304, h: 4.125 });

// ---- Right panel: iris flower photograph (crop incl. orange border + yellow callouts) ----
s.addImage({ path: ASSETS + "slide061_photo.png", x: 8.02, y: 3.14, w: 3.67, h: 2.88 });

// ---- Bottom banner: white strip with thin border, red lead-in + blue remainder ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.35, y: 6.80, w: 12.63, h: 0.52,
  fill: { color: "FFFFFF" }, line: { color: "808080", width: 1 },
});
s.addText([
  { text: "4 Features: ", options: { color: BAN_RED, bold: true } },
  { text: "Width and Length of both sepal and petal", options: { color: BAN_BLUE, bold: true } },
], {
  x: 0.35, y: 6.80, w: 12.63, h: 0.52, align: "center", valign: "middle",
  fontSize: 20, fontFace: FONT, margin: 0,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_061_recreated.pptx" })
  .then((f) => console.log("written:", f));
