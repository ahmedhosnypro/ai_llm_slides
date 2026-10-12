// slide_008.js — 001_introduction slide 8 "Programming Languages, Platforms, and Libraries"
// — Deep Learning DSAI 308.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_008.jpg (960x540, 1px = 1pt = 1/72 in).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 8 (file number; assumption PENDING FOUNDER VETO,
//   001_introduction/AGENTS.md 2026-10-12).
//
// Measured constants (frame px, from qa/slide008/measure_original{,2,3,4}.py):
//   vertical red rule   1px line centered x=58, y 43..516 (full panel height) — PRESENT IN INK,
//                       absent from the spec (spec's "top rule at 7%" + "top letterbox" are
//                       hallucinated video-frame artifacts: rows 0..41 are pure white, zero red
//                       ink above y43; ink forensics win per building.md).
//   content box         border-centerline x 71..460, y 153..510; stroke ~1.5px, C00000,
//                       fill FFFFFF (interior 254,255,253).
//   title (2 lines)     Arial Bold 42pt C00000 (advance-solved: LiberationSans-Bold 42px =
//                       735.2/263.8 vs measured ink 733/262); L1 cap top 63, baseline ~92;
//                       L2 baseline ~139 (pitch 47 -> lineSpacing 47); ink centers 488 / 487.5.
//   headers             Arial Bold 18.5pt C00000 (advance 262/249/260 vs 256.1/244/254.1 @18px),
//                       text ink-left x97, cap tops 162 / 259 / 331.
//   bullets             Arial Regular 18pt, black 000000 (ink modal (0,1,0)); text ink-left x183,
//                       cap tops 188/213/239 | 285/310 | 357/382/408/434/459/485
//                       (within-section pitch 25-26px).
//   bullet dots         black, d~4.5px, center x 165.5, center y = cap_top + 5.
//   NOT drawn           black bottom player bar (spec step 13: video artifact), mouse cursor
//                       (spec step 14: optional artifact, omitted), letterbox + "top rule"
//                       (not present in ink).
// Fonts metric-solved against Liberation Sans TTFs (Arial-metric-compatible).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_008_recreated.pptx";

// ---- palette (measured) ----
const RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";

const px = (v) => v / 72;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 8)
drawHouseChrome(pres, slide, { numeral: "8" });

// Vertical red rule — 1px line centered x=58, y 43..516 (measured ink)
slide.addShape(pres.ShapeType.rect, {
  x: px(57.25), y: px(43), w: px(1.5), h: px(473),
  fill: { color: RED }, line: { color: RED, width: 0 },
});

// White content box with thin red border (border-centerline x 71..460, y 153..510)
slide.addShape(pres.ShapeType.rect, {
  x: px(71), y: px(153), w: px(389), h: px(357),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// Title — two lines, Arial Bold 42pt C00000, ink center ~488, baselines 92/139, pitch 47.
// Box w 12in (864px) so line 1 (adv ~735px) CANNOT wrap; centered at x 488 -> x = 488-432 = 56.
// valign middle, lineSpacing 47 (explicit per the line-spacing law).
slide.addText(
  [
    { text: "Programming Languages, Platforms,", options: { breakLine: true } },
    { text: "and Libraries", options: {} },
  ],
  {
    x: px(56), y: px(52.9), w: 12, h: px(96),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 42, bold: true, color: RED,
    lineSpacing: 47,
  }
);

// Section headers — Arial Bold 18.5pt C00000, ink-left 97, cap tops 162/259/331.
// Single-line boxes: baseline = top + (h-ls)/2 + 0.9052*size (LO empirical, slide_005 model);
// h=36px, ls=24, size 18.5 -> capTop = top + 6 + 16.746 - 13.246 = top + 9.5 -> top = capTop - 9.5.
const HEADERS = [
  { text: "Popular Languages for ML/DL", capTop: 162 },
  { text: "Popular Platforms for ML/DL", capTop: 259 },
  { text: "Popular Libraries (for python)", capTop: 331 },
];
for (const H of HEADERS) {
  slide.addText(H.text, {
    x: px(96), y: px(H.capTop - 9.5), w: px(340), h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 18.5, bold: true, color: RED,
    lineSpacing: 24,
  });
}

// Bullet lines — Arial Regular 18pt black; single-line boxes at measured cap tops.
// h=36px, ls=24, size 18 -> capTop = top + 6 + 16.294 - 12.888 = top + 9.4 -> top = capTop - 9.4.
const BULLETS = [
  "Python", "R", "Matlab",
  "Tensor Flow", "Pytorch",
  "SciKit Learn", "SciPy", "NLTK", "Spacy", "Gensim", "OpenCV",
];
const CAPTOPS = [188, 213, 239, 285, 310, 357, 382, 408, 434, 459, 485];
for (let i = 0; i < BULLETS.length; i++) {
  slide.addText(BULLETS[i], {
    x: px(182), y: px(CAPTOPS[i] - 9.4), w: px(260), h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 18, color: BLACK,
    lineSpacing: 24,
  });
}

// Bullet dots — black round markers d~4.5px, center (165.5, capTop + 5)
for (const ct of CAPTOPS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(163.25), y: px(ct + 5 - 2.25), w: px(4.5), h: px(4.5),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
