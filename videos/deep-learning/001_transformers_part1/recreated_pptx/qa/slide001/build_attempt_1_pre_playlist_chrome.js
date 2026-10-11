// slide_001.js — "Deep  Learning" course title slide (Deep Learning DSAI 308, Transformers Part I)
// Build law: scripts/17_worker_instructions.md + patterns/house-chrome/example.js.
//
// Geometry provenance (PIL-measured on unique_slides/slide_001.jpg, 960x540, 1px=1pt=1/72in):
//   original frame strokes: x 39-921, y 43-539  -> OVERRIDDEN by house frame (0.15in inset)
//   original badge: purple-outline oval center (12.40,1.00) -> OVERRIDDEN by house badge
//   title L1 "Deep  Learning": ink x 254-677, cap 'D' rows 137-177 (41px cap -> 57pt)
//   title L2 "DSAI 308":       ink x 341-593, cap 'D' rows 204-244 (41px cap -> 57pt); pitch 67px
//   credit block (centered @ x=7.158in): "Prepared By" cap top 302px (20pt), name cap top 326px
//     (24pt, pitch 24px), email ascender top 352px (14pt, pitch 26px)
//   instructors block: "Instructors:" ink left 56px (0.778in), cap top 411px; items ink left
//     96px (1.333in); cap tops 438/463/484/507px (names 20pt bold, emails 13pt, 2nd italic)
//   logo lockup ink: x 594-905, y 468-526 -> cropped from the original frame to
//     build/assets/zewail_logo_slide001.png (312x59px = 4.3333x0.8194in), embedded at exact size
//   crosshair '+' artifact: x 173-183, y 198-209 (11x12px), light gray ~B8B8B8
// Layout law (ml-intro slide_001.js certified precedent): house title box pinned at y=0.28;
//   upper content stacks below it preserving the original's internal gaps; bottom blocks
//   (instructors, logo) keep their measured bottom-region positions.
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

const BG = "E8E8E8";      // house canvas
const RED = "C00000";     // title, labels, house frame
const BLUE = "000090";    // names/emails (measured core mode (0,0,144) on the frame)
const CROSS = "B8B8B8";   // stray crosshair artifact
const FONT = "Arial";

const s = pres.addSlide();
s.background = { color: BG };

// ---- 1. house outer red frame (0.15in inset from every edge; founder directive 2026-10-09)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// ---- 2. house slide-number badge (numeral = printed number on the original = 1)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("1", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ---- 3. title block at the HOUSE-pinned position (box starts y=0.28, x=0.6, w=12.13).
// Two paragraphs, explicit lineSpacing 67pt (measured pitch 67px; explicit-line-spacing pattern).
// "Deep  Learning" keeps the original's double space VERBATIM.
s.addText(
  [
    { text: "Deep  Learning", options: { breakLine: true } },
    { text: "DSAI 308", options: {} },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 2.0,
    align: "center", valign: "top",
    fontSize: 60, bold: true, color: RED, fontFace: FONT, margin: 0,
    lineSpacing: 67,
  }
);

// ---- 4. credit block, centered at measured x-center 7.158in; internal pitches preserved
// (prepared-cap -> name-cap 24pt, name-cap -> email-asc 26pt); box y = capTop - 0.189em*size
const CX = 7.158, CW = 5.0, CX0 = CX - CW / 2; // 4.658
s.addText("Prepared By", {
  x: CX0, y: 2.644, w: CW, h: 0.42,
  align: "center", valign: "top",
  fontSize: 20, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: CX0, y: 2.967, w: CW, h: 0.5,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: CX0, y: 3.354, w: CW, h: 0.34,
  align: "center", valign: "top",
  fontSize: 16, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 5. instructors block, bottom-left at measured positions
// heading outdented (ink left 0.778in), items at ink left 1.333in
s.addText("Instructors:", {
  x: 0.767, y: 5.634, w: 4.5, h: 0.42,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 1.316, y: 6.009, w: 4.5, h: 0.42,
  align: "left", valign: "top",
  fontSize: 20, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 1.328, y: 6.373, w: 4.5, h: 0.32,
  align: "left", valign: "top",
  fontSize: 15, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: 1.316, y: 6.648, w: 4.5, h: 0.42,
  align: "left", valign: "top",
  fontSize: 20, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: 1.328, y: 6.984, w: 4.5, h: 0.32,
  align: "left", valign: "top",
  fontSize: 15, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 6. Zewail City logo: cropped from the original frame (spec: insert as image asset),
// embedded at EXACT size (312x59px @72ppi = 4.3333x0.8194in); lifted 0.12in off the house
// frame's bottom stroke (original logo-to-frame gap preserved against the house frame)
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/zewail_logo_slide001.png",
  x: 8.25, y: 6.4006, w: 4.3333, h: 0.8194,
});

// ---- 7. stray '+' crosshair artifact at measured position (reproduced for faithful matching)
s.addText("+", {
  x: 2.073, y: 2.577, w: 0.8, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 26, color: CROSS, fontFace: FONT, margin: 0,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_001_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
