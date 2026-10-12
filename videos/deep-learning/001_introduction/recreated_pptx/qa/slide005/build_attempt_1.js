// slide_005.js — 001_introduction slide 5 "What is Machine Learning?" — Deep Learning DSAI 308.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_005.jpg (960x540, 1px = 1pt = 1/72 in).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 5 (file number; assumption PENDING FOUNDER VETO,
//   001_introduction/AGENTS.md 2026-10-12).
//
// Measured constants (frame px):
//   content box     x 89..875, y 138..503  (border ~1.5pt C00000, fill FFFFFF)
//   title ink       x 253..704 (advance ~449-451, center 478.5), cap-top 87.5, baseline 112
//                   -> Times New Roman Bold 37.5pt (advance 449.0 exact; deck template = TNR Bold,
//                      cf. certified slide_002 title)
//   header ink      x 101..323 (advance 222; Arial Bold 25pt = 220.9), cap-top 159.5, baseline 177.5
//   bullet lines    text-left x141 (ALL lines — wrapped lines align with first lines, no hanging
//                   indent); baselines 216 / 244 / 284 / 313 / 352 / 381
//                   (wrap pitch 28-29 = single spacing; paragraph pitch 68 = deck template,
//                   same 68px pitch as certified slide_002)
//   bullet dots     black d~7px, centers (113.5, 206.5 / 274.5 / 343.5)
//   black bar       x 38..921, y 518..539 in the ORIGINAL; drawn y 518..537.5 (h 19.5) so the
//                   chrome's half-visible bottom stroke stays visible and house_chrome_check.py
//                   passes (2-frame-px deviation, documented — same as certified slide_002).
//   wrap points     b1: '...from data (and' / 'exploit them)';  b2: '...the machine' / 'learns';
//                   b3: '...and legitimate' / 'emails and let it learn...' (ink-decoded at 1px)
//
// Forensics-driven deviations from the spec's visual estimates (spec estimates lose to ink):
//   - lead-ins 'Approach:'/'Example:' are REGULAR red, not bold (ink density 4.94 px/pt-of-advance
//     = Arial Regular 5.1; Arial Bold would be 7.19 — measured, per deck AGENTS.md pixel law)
//   - blue = 000080 (modal (11,0,127) n=8 core px; spec guessed 1A1ACC)
//   - red = C00000 playlist red for title/header/lead-ins/border (measured modals 141-164,0,0 are
//     JPEG-darkened C00000; deck template + certified slide_002 use C00000)
//   - body = Arial Regular 25pt (x-height 13.0px = 0.519em exact; word advances fit <1-2%;
//     spec guessed ~22pt)
// Fonts metric-solved against the real Arial/Times New Roman TTFs.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_005_recreated.pptx";

// ---- palette (measured) ----
const RED = "C00000";
const BLUE = "000080";
const BLACK = "000000";
const WHITE = "FFFFFF";

const px = (v) => v / 72;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 5)
drawHouseChrome(pres, slide, { numeral: "5" });

// White content box with thin red border (x 89..875, y 138..503)
slide.addShape(pres.ShapeType.rect, {
  x: px(89), y: px(138), w: px(786), h: px(365),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// Black footer bar (over the panel, as in the original; chrome bottom stroke kept visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(518), w: px(884), h: px(19.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Title "What is Machine Learning?" — TNR Bold 37.5pt C00000, ink center 478.5, baseline 112
// box w 12in (single line MUST NOT wrap: advance 449px; 4in box wrapped it in attempt 1),
// h 0.8in (57.6px), lineSpacing 43 -> baseline = top + (57.6-43)/2 + 0.891*37.5 = top + 40.7
slide.addText("What is Machine Learning?", {
  x: px(480) - 6, y: px(71.3), w: 12, h: 0.8,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Times New Roman", fontSize: 38, bold: true, color: RED,
  lineSpacing: 43,
});

// Header "Machine Learning:" — Arial Bold 25pt C00000, text-left 101, baseline 177.5
// box h 0.5in (36px), lineSpacing 30. EMPIRICAL LO offset (closed loop): rendered
// baseline = top + 27.5 -> top = baseline - 27.5 (same-glyph probe deltas, attempt 1).
slide.addText("Machine Learning:", {
  x: px(101), y: px(150.0), w: 4, h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 25.5, bold: true, color: RED,
  lineSpacing: 30,
});

// Bullet lines — Arial 25pt; single-line boxes at measured baselines (top = baseline - 25.63).
// Runs preserve the measured inline coloring (red regular lead-ins, navy phrases).
const LINES = [
  {
    top: 188.5, cs: 0.22,
    runs: [
      { text: "Designing algorithms that can ", options: { color: BLACK } },
      { text: "learn patterns from data", options: { color: BLUE } },
      { text: " (and", options: { color: BLACK } },
    ],
  },
  {
    top: 216.5, cs: 0,
    runs: [{ text: "exploit them)", options: { color: BLACK } }],
  },
  {
    top: 256.5, cs: 0.42,
    runs: [
      { text: "Approach:", options: { color: RED } },
      { text: " human supplies training examples, the machine", options: { color: BLACK } },
    ],
  },
  {
    top: 285.5, cs: 0,
    runs: [{ text: "learns", options: { color: BLACK } }],
  },
  {
    top: 324.5, cs: 0.38,
    runs: [
      { text: "Example:", options: { color: RED } },
      { text: " Show the machine a bunch of spam and legitimate", options: { color: BLACK } },
    ],
  },
  {
    top: 353.5, cs: 0.23,
    runs: [
      { text: "emails and ", options: { color: BLACK } },
      { text: "let it learn to predict if a new email is spam or not", options: { color: BLUE } },
    ],
  },
];
for (const L of LINES) {
  slide.addText(
    L.runs.map((r) => ({ text: r.text, options: r.options })),
    {
      x: px(141), y: px(L.top), w: px(734), h: 0.5,
      align: "left", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 25,
      lineSpacing: 30,
      charSpacing: L.cs || 0,
    }
  );
}

// Bullet dots (black round markers, d~7px) at measured centers
const DOTS = [206.5, 274.5, 343.5];
for (const cy of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(110), y: px(cy - 3.5), w: px(7), h: px(7),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
