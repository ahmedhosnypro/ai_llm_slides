// slide_028.js — 001_introduction slide 28 "Introduction to Convolutional Neural
// Network (CNN)" (section-title slide) — Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_028.jpg (960x540, 1px = 1pt = 1/72 in).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn, NEVER ml-intro values. Badge numeral = 28 (file number;
//   assumption PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).
//
// Measured constants (frame px):
//   title line 1  'Introduction to'               ink x 301..660 (w 360, center 480.5), cap-top 119, baseline 158
//   title line 2  'Convolutional Neural Network'  ink x 112..847 (w 736, center 479.5), cap-top 235, baseline 274
//   title line 3  '(CNN)'                         ink x 409..550 (w 142, center 479.5), cap-top 295, baseline 331.5
//                 (paren ink 293..342 = 331.5 +/- 0.748em up / 0.212em down at 51.5pt — exact)
//   attribution   'Some of Slides are picked from'            ink x 99..,  cap-top 467, baseline ~477
//                 'UVA Deep Learning Course   EFSTRATIOS GAVVES' ink x 93..426, cap-top 486, baseline ~495
//                 (Course->EFSTRATIOS gap measured x 265..278 = the spec's 3-space wide gap)
//   black bar     x 38..921, y 519..539 in the ORIGINAL (covers the chrome bottom stroke);
//                 here drawn y 519..537.5 so the chrome's half-visible bottom stroke stays
//                 visible (documented bottom deviation, same as certified slide_002/005/021).
//
// Forensics-driven decisions (ink over spec estimates, per deck AGENTS.md pixel law):
//   - font: ALL THREE title lines Arial Bold 51.5pt — metric-solved against the real
//     Arial Bold TTF (/usr/share/fonts/TTF/Arialbd.TTF): t1 ink 359 vs measured 360,
//     t2 734 vs 736, t3 142 vs 142. Equal cap heights (39/39 + paren) kill the spec's
//     "40pt / 48pt" size estimates (spec uncertain_items concede sizes are estimates);
//     "Introduction to" only LOOKS smaller (shorter line).
//   - color C00000: measured title modal (176..180, 0, 8..12) is JPEG-darkened C00000
//     (G=B~0 rules out the spec's #A6191E guess) — same reasoning as certified
//     slide_005/slide_021.
//   - attribution: Arial Italic 14pt (metric-solved vs Ariali.TTF: UVA line ink 331 vs
//     measured 334; 12pt would give 284 — 50px off), color #3A3A3A (spec; measured
//     stroke lum p05=60 on thin italic strokes = lightened 3A3A3A). Two single-line
//     boxes at the measured left edges (99 / 93) — a single left-aligned box would put
//     both lines' ink at the same x, contradicting the measured 6px offset.
//   - the original's thin red inset strokes (top y 42, left x 57-59, NO right stroke)
//     are CONSTANT VIDEO-LEVEL chrome (certified precedent slide_021: present on every
//     frame of this lecture, omitted per slide_002/slide_005); the pre-declared playlist
//     house chrome stands in for the frame element, and the mouse-cursor artifact at
//     x 241..295 y 446..479 is omitted per judge ground rule (c).
//
// Fonts metric-solved against the real Arial Bold / Arial Italic TTFs.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_028_recreated.pptx";

// ---- palette (measured) ----
const RED = "C00000";
const GRAY = "3A3A3A";
const BLACK = "000000";

const px = (v) => v / 72;

// ---- title geometry ----
// Single-line boxes (certified pattern): h 1.0in (72px), lineSpacing 62pt, valign middle.
// Model baseline offset = (72 - 62)/2 + 0.9052*51.5 = 51.62 px; EMPIRICAL closed-loop
// correction from render_1: baseline landed +4.8px low on t1 (model error, same for all
// lines of this font/size/box) -> empirical 4.8. Box widened w 10 -> 12.4 in (893 px,
// > 1.2x the longest advance 734 px) after render_1 showed t2 WRAPPING at w=10 (720 px
// box < 734 px advance) — the wrap also polluted t3's measurement window. Box x centered
// on slide center 480: x = px(33.5).
const TITLE_FONT = 51.5;
const MODEL_OFFSET = (72 - 62) / 2 + 0.9052 * TITLE_FONT; // 51.62
const LINES = [
  { text: "Introduction to", baseline: 158.0, empirical: 4.8 },
  { text: "Convolutional Neural Network", baseline: 274.0, empirical: 4.8 },
  { text: "(CNN)", baseline: 331.5, empirical: 4.8 },
];

// ---- attribution geometry ----
// Single-line boxes: h 0.4in (28.8px), lineSpacing 17pt, valign middle, left-aligned.
const ATTR_FONT = 14;
const ATTR_OFFSET = (28.8 - 17) / 2 + 0.9052 * ATTR_FONT; // 18.57
const ATTR = [
  { text: "Some of Slides are picked from", x: 99, baseline: 477.0, empirical: 0 },
  { text: "UVA Deep Learning Course   EFSTRATIOS GAVVES", x: 92, baseline: 495.0, empirical: 0 },
];

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 28)
drawHouseChrome(pres, slide, { numeral: "28" });

// Black footer bar (over the panel, as in the original; chrome bottom stroke kept visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(884), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Title lines — Arial Bold 51.5pt C00000, centered, at measured baselines
for (const L of LINES) {
  slide.addText(L.text, {
    x: px(33.5), y: px(L.baseline - MODEL_OFFSET - L.empirical), w: 12.4, h: 1,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: TITLE_FONT, bold: true, color: RED,
    lineSpacing: 62,
  });
}

// Attribution — Arial Italic 14pt #3A3A3A, left-aligned, at measured left edges/baselines
for (const A of ATTR) {
  slide.addText(A.text, {
    x: px(A.x), y: px(A.baseline - ATTR_OFFSET - A.empirical), w: 6, h: 0.4,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: ATTR_FONT, italic: true, color: GRAY,
    lineSpacing: 17,
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
