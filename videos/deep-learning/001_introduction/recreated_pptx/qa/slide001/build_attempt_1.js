// slide_001.js — "Deep  Learning" course cover (Deep Learning DSAI 308, 001_introduction)
//
// Chrome law (founder directive 2026-10-11, playlist-wide): outer chrome is the SHARED
// module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas,
// gray E9E9E7 panel x 42..918px / y 45px..slide bottom with thin C00000 border (bottom
// stroke half-visible at the slide edge), badge circle d36px at center (893,71)px,
// FDFD96 fill + 6A5ACD ~2pt ring, bold 333333 numeral. Numeral = 1 (this lecture's
// frames carry no printed numbers; numeral = file number per 001_introduction/AGENTS.md,
// assumption pending founder veto). The ml-intro house values are SUPERSEDED.
//
// Frame forensics (PIL, unique_slides/slide_001.jpg, 960x540, 1px=1pt):
//   - The spec's "top rule" (dark row y43, x58-901) is the CHROME panel top border, not
//     content — identical row in the chrome reference frame; NOT drawn separately.
//   - This video's own panel inset is x58..901 (vs the reference x42..918); the playlist
//     law mandates the shared chrome values, so the delta is chrome, not content.
//   - Original frames carry NO badge (PIL-probed 2026-10-12); badge drawn per playlist law.
//   - Bottom black strip y518-539 = video letterbox artifact; correctly omitted (spec
//     recreation_brief step 8). '+' cursor artifact at (837-847, 341-351) omitted (step 8).
//
// Content measurements (MY frame is ground truth; runs ~5% larger than the sibling
// lecture's recording — sizes derived from MY cap heights via Liberation-metrics
// calibration, cap 0.688em, then closed-loop verified on the 150dpi render):
//   title L1 'Deep  Learning': D-cap y128-170 (43px -> 63pt), ink x243-690 (center 6.479in);
//   title L2 'DSAI 308': cap top y198; cap-to-cap pitch 70px -> lineSpacing 70pt.
//   credit block (ink centers ~514px=7.14in): 'Prepared By' cap top 292px=4.056in (21pt
//     bold italic), name cap top 318px=4.417in (25pt bold italic, 17px cap), email asc top
//     344px=4.778in (17.5pt bold, ink x398-628).
//   instructors block: 'Instructors:' ink left 75px=1.042in, cap top 397px=5.514in (21pt
//     bold italic); names ink left 117px=1.625in, D-cap tops 426/473px (23pt bold, 15px
//     cap; widths 276/237px); emails asc tops 449/497px (16pt bold, widths 216/207px).
//   logo lockup (teal emblem x572-661 + white name-box x662-894, y435-511): cropped from
//     the frame to build/assets/zewail_logo_slide001.png (325x79px), embedded at exact
//     size (325/72 x 79/72 in) at its measured position (x571,y434 px).
//   LO box-top -> ink-top offset: ~0.27em at 16-25pt; ~0.20em at 63pt (sibling-calibrated).
const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const RED = "C00000";      // title + red labels (frame core (171-192,0,0..14), spec C00000)
const BLUE = "1414B8";     // names (spec body_text; frame core (27,15,158))
const NAVY = "1F1F8F";     // emails (spec accent; frame core muted (71-82,64-77,140-143))
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "1"
drawHouseChrome(pres, s, { numeral: 1 });

// ---- 2. title block at its MEASURED position: ink center 6.482in, L1 cap top 128px,
// pitch 70pt, single centered box (sibling-certified pattern), explicit lineSpacing 70.
s.addText(
  [
    { text: "Deep  Learning", options: { breakLine: true } },
    { text: "DSAI 308", options: {} },
  ],
  {
    x: 0.417, y: 1.612, w: 12.13, h: 2.1,
    align: "center", valign: "top",
    fontSize: 63, bold: true, color: RED, fontFace: FONT, margin: 0,
    lineSpacing: 70,
  }
);

// ---- 3. credit block, centered at measured ink centers (~7.14in)
s.addText("Prepared By", {
  x: 4.646, y: 3.977, w: 5.0, h: 0.44,
  align: "center", valign: "top",
  fontSize: 21, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 4.639, y: 4.323, w: 5.0, h: 0.52,
  align: "center", valign: "top",
  fontSize: 25, bold: true, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 4.625, y: 4.714, w: 5.0, h: 0.36,
  align: "center", valign: "top",
  fontSize: 17.5, bold: true, color: NAVY, fontFace: FONT, margin: 0,
});

// ---- 4. instructors block, bottom-left at measured positions
s.addText("Instructors:", {
  x: 1.028, y: 5.435, w: 4.5, h: 0.44,
  align: "left", valign: "top",
  fontSize: 21, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 1.614, y: 5.834, w: 4.5, h: 0.46,
  align: "left", valign: "top",
  fontSize: 22, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 1.631, y: 6.176, w: 4.5, h: 0.34,
  align: "left", valign: "top",
  fontSize: 16, bold: true, color: NAVY, fontFace: FONT, margin: 0,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: 1.614, y: 6.487, w: 4.5, h: 0.46,
  align: "left", valign: "top",
  fontSize: 22, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: 1.631, y: 6.843, w: 4.5, h: 0.34,
  align: "left", valign: "top",
  fontSize: 16, bold: true, color: NAVY, fontFace: FONT, margin: 0,
});

// ---- 5. Zewail City logo lockup (teal emblem + bilingual name box): cropped from the
// original frame at its measured box, embedded at EXACT size (325x79px @72ppi).
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/zewail_logo_slide001.png",
  x: 571 / 72, y: 434 / 72, w: 325 / 72, h: 79 / 72,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_001_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
