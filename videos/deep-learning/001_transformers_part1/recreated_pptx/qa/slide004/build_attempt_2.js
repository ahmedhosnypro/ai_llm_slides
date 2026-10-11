// slide_004.js — "Processing Sequential Data" (Deep Learning DSAI 308, Transformers Part I)
// Build worker: per-slide recreation. Attempt 2 — chrome rebuilt to the RATIFIED PLAYLIST
// house-chrome law (founder directive 2026-10-11, videos/deep-learning/AGENTS.md): chrome is
// drawn ONLY via the shared module videos/deep-learning/shared_patterns/house_chrome.js
// (drawHouseChrome). The ml-intro values in 17_worker_instructions.md are superseded for
// this playlist. Attempt 1 (banked: qa/slide004/build_attempt_1.js, render_1.png,
// judge_prompt_1.txt, judge_attempt_1.txt PASS) used pre-ratification chrome values and is
// superseded evidence.
//
// CONTENT GEOMETRY PROVENANCE — PIL pixel forensics on slide_004.jpg (960x540, 1px = 1pt):
//   Title ink: x146..788, cap top y200, descender bottom y247 -> 49pt bold (three word-width
//     checks agree: Processing 5.32em=259px, Sequential 4.98em=244px, Data 2.14em=105px -> em~49);
//     color core ~(178,15,33) ~ C00000. Box y tuned closed-loop so cap top lands at y200.
//   Body lines: L1 cap top y343 baseline y367; L2 cap top y423 baseline y447; pitch 80 px
//     = 1.111 in -> lineSpacing 80pt pinned; ink left x89 both lines; L1 ink width 769px,
//     L2 556px -> 35.5pt bold (two independent width checks agree); color core (0,0,152) ~
//     000099; gap before "(1-D CNN)" 35px ~ 3 spaces, before "(RNN)" 22px ~ 2 spaces.
//   Mouse-cursor artifact (~54% width, ~74% height) is a screen-recording overlay -> NOT
//     recreated (spec + judge ground rule c).
//
// pptxgenjs laws: no "#" in hex; fontFace everywhere; margin:0; explicit lineSpacing on the
// multi-line body box; empty-run pitfall avoided (no empty runs).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const FONT = "Arial";
const TITLE = "Processing Sequential Data";
const BODY_LINE1 = "1-D Convolutional Neural Network   (1-D CNN)"; // three spaces before "(1-D CNN)"
const BODY_LINE2 = "Recurrent Neural Network  (RNN)";              // two spaces before "(RNN)"

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// PLAYLIST HOUSE CHROME (white canvas, gray panel + red border, badge circle d36 @ (893,71))
drawHouseChrome(pres, s, { numeral: 4 });

// title (per-slide measured title-y; box full-width centered per house/spec)
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

pres.writeFile({ fileName: "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_004_recreated.pptx" })
  .then(() => console.log("wrote slide_004_recreated.pptx"));
