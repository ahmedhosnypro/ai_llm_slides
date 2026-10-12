// slide_006.js — 001_introduction slide 6 "Machine Learning in the real-world" — Deep Learning DSAI 308.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_006.jpg (960x540, 1px = 1pt = 1/72 in).
//   Forensics: qa/slide006/measure_original{,2,3,4,5,6}.py (+ _out.txt banked outputs).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 6 (file number; originals carry no printed
//   numbers — assumption PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).
//
// Measured constants (frame px):
//   content box     outer ink x 87..843, y 132..504; border ~3px (2.25pt) C00000, fill FFFFFF.
//                   Drawn as path rect x 88.5, y 133.5, w 754, h 370 so the 3px stroke covers
//                   exactly the measured ink (87..90 / 132..135 / 841..844 / 502..505).
//   title ink       x 142..833 (advance 692, ink center 487.5), cap-top 84, baseline 116.2
//                   -> Arial REGULAR 45pt (per-word advance fit: spread 44.2..45.3pt vs ArialB
//                      39.4..42.0 with 'in' outlier; span solve 45.4 regular; spec's "bold" is
//                      an estimate — ink wins per deck AGENTS.md pixel law)
//   header          Times New Roman 24pt black (metric-solved: mixed bold+regular L1 = 602.3
//                   vs target 600; L2 regular 631.3 vs 626; Arial/other fits inconsistent).
//                   L1 = BOLD+UNDERLINED "Broadly applicable in many domains" (underline ink
//                   y=158 runs x 93..467; TimesB24 phrase ends 468.7 — exact match) + regular
//                   " (e.g., finance, robotics,"; text-left 93/94; baselines 155 / 182.
//   bullet lines    12 lines, text-left 205 (b2 at 210 = verbatim leading space), Arial
//                   REGULAR 17.5pt (per-string advance fit 17.40..17.73 consistent), pitch
//                   26.2px, baselines 209.5 + 26.18k. Color 1A1ACC (pooled 2x2-max one-param
//                   fit vs certified 000080 [005] / 0000AA [002] references; 000080 excluded
//                   by R-channel ceiling) EXCEPT bullet 12 ".. and many more" = BLACK
//                   (zero bluish px, darkest (0,0,0) — measured, overrides spec's blue claim).
//   bullet dots     black, d~5-6px, cx=182, cy 203..490.5 pitch 26.2 (measured list).
//   black bar       x 38..921, y 518..539 in the ORIGINAL; drawn y 518..537.5 (h 19.5) so the
//                   chrome's half-visible bottom stroke stays visible (certified 002/005 same).
//   cursor          white arrow + black outline at ~(218..325, 355..438) = recording artifact,
//                   NOT recreated (spec step 8; judge ground rule (c)).
//
// Original frame's own chrome note: panel gray sits inset (x ~61..906, red top rule y 42..45,
// red left border x 56..60, no visible right border) — the recreation draws the CANONICAL
// playlist chrome per the 2026-10-11 founder directive; judge ground rule (a) preempts.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_006_recreated.pptx";

// ---- palette (measured) ----
const RED = "C00000";
const BLUE = "1A1ACC";
const BLACK = "000000";
const WHITE = "FFFFFF";

const px = (v) => v / 72;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 6)
drawHouseChrome(pres, slide, { numeral: "6" });

// Black footer bar (over the panel, as in the original; chrome bottom stroke kept visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(518), w: px(884), h: px(19.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// White content box with thin red border (outer ink 87..843 x 132..504, border ~3px)
slide.addShape(pres.ShapeType.rect, {
  x: px(88.5), y: px(133.5), w: px(754), h: px(370),
  fill: { color: WHITE }, line: { color: RED, width: 2.25 },
});

// Title — Arial REGULAR 45.5pt C00000, ink center 487.5, baseline ~116.1 (cap-top ~84).
// Attempt-2 closed-loop: 45pt rendered advance 683 vs orig 691 (-1.1%) -> 45.5; ink sat
// 1.4px low -> top 68.2 -> 66.8. Box w 12in (single line MUST NOT wrap), h 0.9in (64.8px),
// lineSpacing 52 (closed-loop verified after render).
slide.addText("Machine Learning in the real-world", {
  x: px(487.5) - 6, y: px(66.8), w: 12, h: 0.9,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 45.5, color: RED,
  lineSpacing: 52,
});

// Header line 1 — Times New Roman 23.9pt black; bold+underlined phrase then regular rest.
// Attempt-3 closed-loop: 24pt rendered L2 3fp long vs orig (L2 fits 23.9, L1 unaffected
// within 1fp) -> 23.9 both lines. text-left 93, baseline 155 -> top = 155 - 26.1 = 128.9
// (h 0.5in, lineSpacing 28).
slide.addText(
  [
    {
      text: "Broadly applicable in many domains",
      options: { bold: true, underline: { style: "sng" }, color: BLACK },
    },
    { text: " (e.g., finance, robotics,", options: { color: BLACK } },
  ],
  {
    x: px(93), y: px(128.9), w: 9.5, h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Times New Roman", fontSize: 23.9,
    lineSpacing: 28,
  }
);

// Header line 2 — regular; text-left 94, baseline 182 -> top 155.9.
slide.addText("bioinformatics, vision, natural language, etc.). Some applications:", {
  x: px(94), y: px(155.9), w: 9.5, h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Times New Roman", fontSize: 23.9, color: BLACK,
  lineSpacing: 28,
});

// Bullet lines — Arial 17.5pt; single-line boxes at measured baselines
// (top = baseline - 24.06; h 0.5in, lineSpacing 22, explicit pitch pinned).
// Bullet 12 ".. and many more" is BLACK in the original (measured) — not blue.
const BULLETS = [
  { text: "Spam filtering", base: 209.5, color: BLUE },
  { text: " Machine Translation (e.g.,  Google Translate)", base: 235.5, color: BLUE },
  { text: "Speech/handwriting recognition", base: 261.5, color: BLUE },
  { text: "Object detection/recognition", base: 288.5, color: BLUE },
  { text: "Weather prediction", base: 314.5, color: BLUE },
  { text: "Classifying DNA sequences", base: 340.5, color: BLUE },
  { text: "Stock market analysis", base: 366.5, color: BLUE },
  { text: "Automatic vehicle navigation", base: 392.5, color: BLUE },
  { text: "Search engines (e.g., Google)", base: 418.5, color: BLUE },
  { text: "Credit-card fraud detection", base: 444.5, color: BLUE },
  { text: "Webpage clustering (e.g., Google News)", base: 471.5, color: BLUE },
  { text: ".. and many more", base: 497.5, color: BLACK },
];
for (const B of BULLETS) {
  slide.addText(B.text, {
    x: px(205), y: px(B.base - 24.06), w: 9.4, h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 17.5, color: B.color,
    lineSpacing: 22,
  });
}

// Bullet dots (black round markers, d 5px — attempt-3 closed-loop: 6px dots' bottom edges
// ran 2fp past the orig strict bboxes; d5 matches all 12) at measured centers (cx 182)
const DOTS = [203, 229, 256, 281, 308, 334, 360, 386, 412, 439, 465, 491];
for (const cy of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(179.5), y: px(cy - 2.5), w: px(5), h: px(5),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
