// slide_001.js — "Deep  Learning DSAI 308" cover (Deep Learning DSAI 308, 001_introduction)
// ATTEMPT 2 (2026-10-12, takeover of attempt 1 — see qa/slide001/WORKER_TAKEOVER_NOTE.txt).
//
// Chrome law (founder directive 2026-10-11, playlist-wide): outer chrome is the SHARED module
// videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas, gray E9E9E7
// panel x 42..918px / y 45px..slide bottom with thin C00000 border (bottom stroke half-visible
// at the slide edge), badge circle d36px at center (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring,
// bold 333333 numeral. Numeral = 1 (this lecture's frames carry no printed numbers and no
// badge — PIL-probed 2026-10-12; numeral = file number per 001_introduction/AGENTS.md,
// assumption PENDING FOUNDER VETO). The ml-intro house values are SUPERSEDED.
//
// NO separate "top rule": the spec's visual_elements[0] dark line (row 43, x 58-901) is the
// chrome panel's TOP BORDER — it sits exactly on this frame's panel gray extent (cols 61-902)
// with no second line below (rows 44+ fade straight to gray). Attempt 1 concluded the same.
// Letterbox (rows 518-539) and '+' cursor (837-847, 341-351) are recording artifacts —
// excluded per spec recreation_brief step 8 and judge ground rule (c).
//
// Content measurements (PIL forensics on unique_slides/slide_001.jpg, 960x540, 1px=1pt;
// typography ground truth from a 2x-crop vision read banked at
// scratch/slide001/typography_read.txt, corroborated by stem-slope + ink-density):
//   title: ADOPTED FROM ATTEMPT 1 verbatim — 63pt bold (their 150dpi render closed-loop
//     PASSed width 445 vs 447 and band 267-387 vs 126-184-frame), lineSpacing 70 (pitch
//     128.5->198.5 = 70px), box x 0.417/y 1.612/w 12.13 centered (ink centers 6.486/6.500in).
//     LibreOffice renders Arial as Liberation Sans (cap 0.688em): 42-43px caps -> 62-63pt.
//   credit block (ink centers ~7.14in): "Prepared By" cap top 292px=4.0556in — 20pt bold
//     ITALIC red (vision: italic; stem slope -0.273). Name cap top 317px=4.4028in — 23.5pt
//     bold ITALIC navy (cap 16.5px/0.688 = 24; width metric+empirical 22.9; split 23.5;
//     attempt 1's 25pt failed width +27px). Email asc top 344px=4.7778in — 16pt BOLD upright
//     (vision: bold; ink density 0.173 = bold; Liberation bold advance 14.30em x 16 = 229px
//     vs original 230px).
//   instructors block: "Instructors:" ink left 75px=1.0417in, cap top 398px=5.5278in — 21pt
//     bold ITALIC red + charSpacing 1.1 (attempt 1's 21pt passed cap/band/position but width
//     114.7 vs original 127.5px: original head is +16% wider per cap than Liberation metrics
//     — tracked heading; 11 gaps x 1.1pt = +12.1px -> 126.8). Names ink left 118px=1.6389in,
//     cap tops 426/472px — 21pt bold ITALIC navy (attempt 1's 21pt upright passed y-band and
//     width at 22: 285.6 vs 276; 21pt -> 272.7; vision read + stem slopes -0.187/-0.180 say
//     ITALIC, which attempt 1 omitted). Emails asc tops 452/498px — 16pt REGULAR (vision:
//     "noticeably thinner" than the bold prepared email; ink density 0.093 vs 0.173; email2
//     ITALIC — vision read + the certified sibling's independent "2nd italic" finding;
//     attempt 1 had both bold upright).
//   logo lockup (teal emblem x 571-661 + bilingual white box, ink y 432-511): cropped from
//     THIS frame to build/assets/zewail_logo_001introduction.png (337x86px incl. 4-5px gray
//     padding), embedded at EXACT size at its measured position.
//   LO box-top offsets (sibling calibration): ~0.27em at 16-24pt; attempt-1 empirical small
//     line y-values retained where they rendered within tolerance.
const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const RED = "C00000";    // title + red headings (spec title_text)
const NAVY = "1414B8";   // names (spec body_text; frame core (27,15,158))
const EBLUE = "1F1F8F";  // emails (spec accent; frame core muted (71,64,143))
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "1"
drawHouseChrome(pres, s, { numeral: 1 });

// ---- 2. title block — attempt 1's empirically closed-loop-PASSed geometry, unchanged
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

// ---- 3. credit block, centered at measured ink center 7.14in
s.addText("Prepared By", {
  x: 4.64, y: 3.9806, w: 5.0, h: 0.42,
  align: "center", valign: "top",
  fontSize: 20, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 4.64, y: 4.3147, w: 5.0, h: 0.5,
  align: "center", valign: "top",
  fontSize: 23, bold: true, italic: true, color: NAVY, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 4.64, y: 4.7178, w: 5.0, h: 0.34,
  align: "center", valign: "top",
  fontSize: 16.5, bold: true, color: EBLUE, fontFace: FONT, margin: 0,
});

// ---- 4. instructors block, bottom-left at measured ink-lefts / cap tops
s.addText("Instructors:", {
  x: 1.03, y: 5.435, w: 4.5, h: 0.44,
  align: "left", valign: "top",
  fontSize: 21, bold: true, italic: true, charSpacing: 1.1, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 1.628, y: 5.834, w: 4.5, h: 0.44,
  align: "left", valign: "top",
  fontSize: 21, bold: true, italic: true, color: NAVY, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 1.628, y: 6.2178, w: 4.5, h: 0.34,
  align: "left", valign: "top",
  fontSize: 16.5, color: EBLUE, fontFace: FONT, margin: 0,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: 1.628, y: 6.487, w: 4.5, h: 0.44,
  align: "left", valign: "top",
  fontSize: 21, bold: true, italic: true, color: NAVY, fontFace: FONT, margin: 0,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: 1.628, y: 6.843, w: 4.5, h: 0.34,
  align: "left", valign: "top",
  fontSize: 16.5, italic: true, color: EBLUE, fontFace: FONT, margin: 0,
});

// ---- 5. Zewail City logo lockup (teal emblem + bilingual white box), cropped from THIS
//      slide's original frame, embedded at EXACT size (337x86px @72ppi = 4.6806x1.1944in).
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/zewail_logo_001introduction.png",
  x: 7.8611, y: 5.9444, w: 4.6806, h: 1.1944,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_001_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
