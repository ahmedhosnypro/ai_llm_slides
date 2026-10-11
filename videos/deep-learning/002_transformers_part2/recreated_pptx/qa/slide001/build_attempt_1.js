// slide_001.js — PLACEHOLDER COVER "Deep  Learning" (Deep Learning DSAI 308, Transformers Part II)
//
// PLACEHOLDER-COVER LAW (founder directive 2026-10-11; videos/deep-learning/AGENTS.md +
// 002_transformers_part2/AGENTS.md "Special slides" + scripts/17_worker_instructions.md rule 7):
// lecture 002's cover frame is MISSING from the video — there is NO ground-truth frame and NO
// analysis spec for this slide. It is rebuilt as a placeholder MIRRORING lecture 001's
// certified cover: 001_transformers_part1/unique_slides/slide_001.jpg is the visual reference
// and 001's certified build (recreated_pptx/build/slide_001.js) is the structural reference.
// Every element below is copied verbatim from that certified build — no invented text or
// art. Certification = founder sign-off + shared_patterns/house_chrome_check.py (never a
// visual-judge comparison; nothing to compare against).
//
// Chrome law (founder directive 2026-10-11, playlist-wide): the outer chrome is the SHARED
// playlist module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas,
// gray E9E9E7 panel x 42..918px / y 45px..slide bottom with a thin C00000 border (bottom
// stroke half-visible at the slide edge), badge circle d36px at center (893,71)px, FDFD96
// fill + 6A5ACD ~2pt ring, bold 333333 numeral. Badge numeral = 1 (per the placeholder spec).
// The ml-intro house values are SUPERSEDED for this playlist.
//
// Content geometry is 001's MEASURED cover geometry, copied verbatim from its certified
// build (its own PIL selfcheck banked all values within tolerance of the original frame,
// 960x540 px, 1px = 1pt):
//   title L1 "Deep  Learning" (double space VERBATIM) ink center 6.476in, 60pt bold C00000,
//     lineSpacing 67pt; L2 "DSAI 308" — one centered box x 0.41 y 1.734 w 12.13;
//   credit block centered at 7.158in: "Prepared By" 20pt bold italic red, name 24pt bold
//     000090, email 16pt;
//   instructors block: heading 20pt bold italic red at ink-left 0.778in, items at 1.333in
//     (names 20pt bold, emails 15pt, second email italic);
//   logo lockup: exact-size frame crop of 001's slide_001.jpg at its measured rectangle
//     (ink x 594-905, y 468-526 -> 312x59px), re-cropped into THIS build's assets dir
//     (byte-identical to 001's certified asset, verified 0/18408 px differ), embedded at
//     exact size w = px/72 in (4.3333 x 0.8194) at its measured position x 8.25 y 6.5;
//   crosshair '+' artifact: reproduced at 001's measured position (its certified build
//     carries it; the placeholder mirrors the certified cover, so it is inherited, not
//     invented — flagged for founder sign-off).
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

// ---- 2. title block at 001's MEASURED position (copied verbatim from 001's certified
// build; ink center 6.476in reproduced)
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

// ---- 4. instructors block, bottom-left at 001's measured positions
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

// ---- 5. Zewail City logo: exact-size crop of 001's slide_001.jpg at 001's measured
// rectangle (312x59px @72ppi = 4.3333x0.8194in), embedded at EXACT size at 001's
// measured position; gap to the chrome's half-visible bottom stroke reproduces 001's.
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/zewail_logo_slide001.png",
  x: 8.25, y: 6.5, w: 4.3333, h: 0.8194,
});

// ---- 6. stray '+' crosshair artifact inherited from 001's certified cover build at its
// measured position (founder may veto at sign-off; judge ground rule (c) classifies such
// artifacts as omittable — kept here to mirror 001's certified render)
s.addText("+", {
  x: 2.073, y: 2.577, w: 0.8, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 26, color: CROSS, fontFace: FONT, margin: 0,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_001_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
