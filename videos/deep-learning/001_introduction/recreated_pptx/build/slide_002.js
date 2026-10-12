// slide_002.js — 001_introduction slide 2 "Agenda" — Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_002.jpg (960x540, 1px = 1pt = 1/72 in).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn, NEVER ml-intro values.
// Badge numeral = 2 (slide file number, no zero-padding) — ASSUMPTION PENDING FOUNDER VETO
//   (001_introduction/AGENTS.md 2026-10-12: originals carry no printed numbers; numeral =
//   file number unless vetoed, in which case rebuilds drop the badge via shared_patterns only).
//
// Measured constants (frame px):
//   blue box        x 106..854, y 138..463  (border ~2.5pt #0000AA, fill FFFFFF)
//   bullet bands    cap-tops y 183 / 251 / 320 / 388 (pitch 68px), ink left x=138
//   bullet dots     black, d~7.5px, cx=122, cy 195 / 263 / 331 / 399
//   title "Agenda"  ink y 81..119 (cap 30px), ink center x=475, color C00000 (modal 192,0,0)
//   black bar       x 38..921, y 518..539 in the ORIGINAL (covers the chrome bottom stroke);
//                   here drawn y 518..537.5 so the chrome's half-visible bottom stroke stays
//                   visible and house_chrome_check.py passes (2-frame-px deviation, documented).
// Fonts (metric-verified vs measured ink):
//   body  Arial Bold 30.6pt (metric solve 30.4 from advances; attempt-1 render measured
//         ~0.8% short on all 4 band advances -> closed-loop bump to 30.6; caps unchanged)
//   title Times New Roman Bold 42pt (Liberation Serif: advance 137.8px vs measured 137)
// Colors: PIL modal measurements override the spec's estimates where they disagree
//   (title C00000 vs spec B22222; body/border 0000AA vs spec 1A1ACC) — measured per the
//   deck AGENTS.md "color claims settle via pixel column-profiles".

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_002_recreated.pptx";

// ---- palette (measured) ----
const TITLE_RED = "C00000";
const BODY_BLUE = "0000AA";
const BLACK = "000000";
const WHITE = "FFFFFF";

// ---- geometry (frame px / 72 = inches) ----
const px = (v) => v / 72;

// Blue bullet box
const BOX = { x: px(106), y: px(138), w: px(749), h: px(326) };

// Bullet lines: cap-top baselines -> box tops (single-line boxes, h 0.6in, valign middle,
// explicit lineSpacing 34pt => baseline = box_top + (43.2-34)/2 + ascent(27.5) = +32.13px)
const BASELINES = [204.77, 272.77, 341.77, 409.77]; // cap-top (183/251/320/388) + capheight 21.77
const LINE_H = 34;                                   // explicit lineSpacing (pt)
const BULLET_BOX_H = 0.6;
const BULLET_BOX_TOPS = BASELINES.map((b) => px(b - 32.13));

// Bullet dots (drawn as shapes; original markers are black round dots, not text bullets)
const DOTS = [195, 263, 331, 399].map((cy) => ({
  x: px(122) - px(3.75), y: px(cy) - px(3.75), w: px(7.5), h: px(7.5),
}));

// Black footer bar (bottom edge at 537.5 to keep the chrome bottom stroke visible)
const BAR = { x: px(38), y: px(518), w: px(884), h: px(19.5) };

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 2)
drawHouseChrome(pres, slide, { numeral: "2" });

// Black footer bar (over the panel, as in the original; chrome bottom stroke kept visible)
slide.addShape(pres.ShapeType.rect, {
  x: BAR.x, y: BAR.y, w: BAR.w, h: BAR.h,
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Blue-bordered white bullet box
slide.addShape(pres.ShapeType.rect, {
  x: BOX.x, y: BOX.y, w: BOX.w, h: BOX.h,
  fill: { color: WHITE }, line: { color: BODY_BLUE, width: 2.5 },
});

// Title "Agenda" — Times New Roman Bold 42pt C00000, ink center (475, ~96) px
slide.addText("Agenda", {
  x: px(475) - 2, y: px(67.3), w: 4, h: 0.8,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Times New Roman", fontSize: 42, bold: true, color: TITLE_RED,
  lineSpacing: 47,
});

// Bullet dots (black, d 7.5px) at measured centers
for (const d of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: d.x, y: d.y, w: d.w, h: d.h,
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

// 4 bullet lines — Arial Bold 30.4pt #0000AA, single-line boxes at measured baselines
const LINES = [
  "Quick revision of Machine Learning",
  "Deep Learning vs Machine Learning",
  "Quick revision of Neural Network",
  "Introduction to Convolutional Neural Network",
];
LINES.forEach((text, i) => {
  slide.addText(text, {
    x: 1.9, y: BULLET_BOX_TOPS[i], w: 10.9, h: BULLET_BOX_H,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 30.6, bold: true, color: BODY_BLUE,
    lineSpacing: LINE_H,
  });
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
