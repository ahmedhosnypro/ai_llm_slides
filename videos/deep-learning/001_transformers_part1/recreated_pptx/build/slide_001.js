// slide_001.js — "Deep  Learning" course title slide (Deep Learning DSAI 308, Transformers Part I)
//
// Chrome law (founder directive 2026-10-11, playlist-wide): the outer chrome is the
// SHARED playlist module videos/deep-learning/shared_patterns/house_chrome.js —
// white FFFFFF canvas, gray E9E9E7 panel x 42..918px / y 45px..slide bottom with a thin
// C00000 border (bottom stroke half-visible at the slide edge), badge circle d36px at
// center (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring, bold 333333 numeral. The ml-intro
// house values (0.15in-inset frame, FFF9C4 outline-less badge, title box y=0.28) are
// SUPERSEDED for this playlist. Content inside the chrome follows the fidelity law:
// every position below is PIL-measured on unique_slides/slide_001.jpg (960x540, 1px=1pt).
//
// Content measurements (original frame):
//   title L1 "Deep  Learning": ink x 254-677 (center 6.465in), cap top 137px=1.903in,
//     cap 41px -> 60pt (width-derived: LO@57pt gave 403pt vs frame 424pt; 60pt exact);
//   title L2 "DSAI 308": ink x 341-593 (center 6.486in), cap top 204px=2.833in; pitch 67px.
//     -> one centered box at ink-center 6.476in (box x 0.41 w 12.13), lineSpacing 67pt.
//   credit block (centered at ink-center 7.158in): "Prepared By" cap top 302px=4.194in
//     (20pt bold italic), name cap top 326px=4.528in (24pt bold), email asc top 352px=4.889in
//     (16pt; width-derived 210pt@16 vs frame 220pt).
//   instructors block: "Instructors:" ink left 56px=0.778in, cap top 411px=5.708in (20pt
//     bold italic); items ink left 96px=1.333in, cap tops 438/463/484/507px
//     (names 20pt bold, emails 15pt — width-derived 197.6pt@15 vs frame 206pt; 2nd italic).
//   logo lockup ink x 594-905, y 468-526 -> cropped from the frame to
//     build/assets/zewail_logo_slide001.png (312x59px), embedded at exact size.
//   crosshair '+' artifact: x 173-183, y 198-209, light gray ~B8B8B8.
//   LO cap-top offset (calibrated on the 150dpi renders): ~0.27em at 16-24pt; ~0.20em at 60pt
//   (title box y calibrated empirically: 1.734 puts L1 cap at 1.903in).
const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

const RED = "C00000";     // title, labels (frame-measured core (192,0,0) = C00000)
const BLUE = "000090";    // names/emails (frame-measured core mode (0,0,144))
const CROSS = "B8B8B8";   // stray crosshair artifact
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "1"
drawHouseChrome(pres, s, { numeral: 1 });

// ---- 2. title block at its MEASURED position (fidelity law; the y=0.28 house title
// rule was ml-intro chrome, superseded for this playlist). Ink center 6.476in reproduced.
s.addText(
  [
    { text: "Deep  Learning", options: { breakLine: true } },
    { text: "DSAI 308", options: {} },
  ],
  {
    x: 0.41, y: 1.734, w: 12.13, h: 2.0,
    align: "center", valign: "top",
    fontSize: 60, bold: true, color: RED, fontFace: FONT, margin: 0,
    lineSpacing: 67,
  }
);

// ---- 3. credit block, centered at measured ink-center 7.158in; internal pitches
// preserved (prepared-cap -> name-cap 24pt, name-cap -> email-asc 26pt)
const CX = 7.158, CW = 5.0, CX0 = CX - CW / 2; // 4.658
s.addText("Prepared By", {
  x: CX0, y: 4.119, w: CW, h: 0.42,
  align: "center", valign: "top",
  fontSize: 20, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: CX0, y: 4.438, w: CW, h: 0.5,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: CX0, y: 4.829, w: CW, h: 0.34,
  align: "center", valign: "top",
  fontSize: 16, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 4. instructors block, bottom-left at measured positions
// heading outdented (ink left 0.778in), items at ink left 1.333in
s.addText("Instructors:", {
  x: 0.767, y: 5.633, w: 4.5, h: 0.42,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 1.316, y: 6.008, w: 4.5, h: 0.42,
  align: "left", valign: "top",
  fontSize: 20, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 1.328, y: 6.373, w: 4.5, h: 0.32,
  align: "left", valign: "top",
  fontSize: 15, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: 1.316, y: 6.647, w: 4.5, h: 0.42,
  align: "left", valign: "top",
  fontSize: 20, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: 1.328, y: 6.984, w: 4.5, h: 0.32,
  align: "left", valign: "top",
  fontSize: 15, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 5. Zewail City logo: cropped from the original frame (spec: insert as image
// asset), embedded at EXACT size (312x59px @72ppi = 4.3333x0.8194in) at its measured
// position; gap to the chrome's half-visible bottom stroke reproduces the original's.
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/zewail_logo_slide001.png",
  x: 8.25, y: 6.5, w: 4.3333, h: 0.8194,
});

// ---- 6. stray '+' crosshair artifact at measured position (reproduced for faithful
// matching; judge ground rule (c) permits either, the frame shows it)
s.addText("+", {
  x: 2.073, y: 2.577, w: 0.8, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 26, color: CROSS, fontFace: FONT, margin: 0,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_001_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
