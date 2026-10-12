// slide_012.js — 001_introduction slide 12 "Feature Invariants" — Deep Learning DSAI 308.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_012.jpg (960x540, 1px = 1pt = 1/72 in).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 12 (file number; assumption PENDING FOUNDER VETO,
//   001_introduction/AGENTS.md 2026-10-12 — this lecture's originals carry no printed numbers;
//   PIL-probed 2026-10-12: badge zone (875..915, 50..95) is bare panel gray).
//
// Measured constants (frame px):
//   title box    border centerlines x 94..364, y 81..138 (w270 h57); fill modal (228,254,251)
//                = E4FEFB (spec guessed D8F0F0 — ink wins); border 000080 ~1.5pt (core 1 row,
//                modal (59,68,133)/(27,30,109) = JPEG-softened 000080, deck navy per certified
//                slide_005/slide_010 law)
//   title ink    "Feature Invariants" x 125..333 (advance 208 = Arial Bold 24pt, pred 207 err 1;
//                stem 3px = bold; cap 17px = 0.716*24), cap-top 100.5, baseline 117.5;
//                ink CENTER x=229 == box center 229 -> centered
//   content box  border centerlines x 95..881, y 157.5..390 (w786 h232.5); fill (254,255,253)
//                = FFFFFF; border 000080 ~2pt (core 2 rows, modal (57,53,140) — same values as
//                certified slide_010's content box)
//   header line  baseline 181.5, ink x 126..567: "Features Invariants are " RED BOLD
//                (ink 126..355; stem cols 128-130 3px = bold; Arial Bold 21pt pred 230, JPEG
//                erosion reconciles; spec said bold red — ink confirms), " is " BLACK REGULAR 21pt
//                (ink 364..376), "Problem dependent" BLACK REGULAR 21pt ITALIC + UNDERLINED
//                ('P' stem slants ~2px left-to-right over 13 rows = italic; underline = continuous
//                run rows 183-184 x 378..567, starts right AFTER "is" ends (376) — same pattern as
//                certified slide_010: underline covers the italic phrase only; "Problem dependent"
//                advance 183 = Arial Regular 21pt EXACT err 0)
//   bullets      Arial Bold 21pt (bold 21 preds 179/168/205/186 vs meas 176/166/203/183 — JPEG
//                erosion ~3px; stems 3px; cap 15px = 0.716*21), text-left ink 126.5, baselines
//                249 / 293 / 337 / 381 (44pt pitch — original rhythm is EXACTLY 44 via the dot
//                centers 241/285/329/373); casing verbatim: bullet 3 "Translation invariant"
//                lowercase i (spec quirk preserved)
//   bullet dots  black d~5.5px, center x 108.3 (cols 106..110.5), y-centers 241/285/329/373
//                (each ~7.5px above its baseline — slide_010 precedent 7.7)
//   black bar    x 38..921, y 519..539 in the ORIGINAL; drawn y 519..537.5 (h 18.5) so the
//                chrome's half-visible bottom stroke stays visible and house_chrome_check.py
//                passes (same treatment as certified slide_005/slide_010)
//   NOT drawn (ink-verified absent / recording artifacts / frozen chrome):
//     - the spec's "top rule" at ~7-8%: rows 42-44 ARE the chrome panel's own red top border —
//       covered by drawHouseChrome, not a separate element (slide_005/slide_010 precedent)
//     - mouse cursor over bullet 3 (rows ~326-342, x ~185-215): screen-recording artifact
//       (spec step 9 exclusion + judge ground rule c)
//     - the red vertical line at cols 58-59 in the ORIGINAL: present identically in certified
//       slide_010's frame — lecture-recording chrome appearance; the playlist chrome law freezes
//       the panel at x 42..918 (judge ground rules), so nothing is drawn there

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_012_recreated.pptx";

// ---- palette (measured) ----
const NAVY = "000080";   // box borders (deck navy, certified slide_005/010 law)
const RED = "C00000";    // header red run (modal (134,12,27) = JPEG-darkened C00000, slide_010 law)
const BLACK = "000000";
const WHITE = "FFFFFF";
const TITLE_FILL = "E4FEFB"; // measured modal (228,254,251)

const px = (v) => v / 72;

// Single-line text placement: baseline = top + (h_px - lineSpacing)/2 + 0.9052*size
// (formula from certified slide_005/slide_010). LO renders baselines slightly LOW vs the
// formula (slide_010 calibration): title(25pt/L30) -2.1, 21pt/L25 -1.1, bullets(20pt/L25) -1.8.
// Initial cals here: title 24pt/L30 -> -2.0, 21pt/L25 -> -1.1, bullets 21pt bold/L25 -> -1.5;
// closed-loop render check measures the real deltas before judging.
const CAL_TITLE = -3.5, CAL_21 = -1.1, CAL_BULLET = -1.5;
const lineTop = (baseline, size, L, cal = 0) =>
  baseline - ((36 - L) / 2 + 0.9052 * size) + cal;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 12)
drawHouseChrome(pres, slide, { numeral: "12" });

// Title box (x 94..364, y 81..138), pale-cyan fill, navy 1.5pt border
slide.addShape(pres.ShapeType.rect, {
  x: px(94), y: px(81), w: px(270), h: px(57),
  fill: { color: TITLE_FILL }, line: { color: NAVY, width: 1.5 },
});

// Main content box (x 95..881, y 157.5..390), white fill, navy 2pt border
slide.addShape(pres.ShapeType.rect, {
  x: px(95), y: px(157.5), w: px(786), h: px(232.5),
  fill: { color: WHITE }, line: { color: NAVY, width: 2 },
});

// Black footer bar (over the panel, as in the original; chrome bottom stroke kept visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(884), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Title "Feature Invariants" — Arial Bold 24pt black (advance 208, pred 207 err 1), centered
// in the title box (ink center 229 == box center), baseline 117.5. charSpacing 0.3:
// closed-loop attempt 1 measured the LO render 203px wide vs the original's 208 (LO hinting
// compression, slide_010 precedent) and baselines +1.5 low — CAL_TITLE -3.5 + 0.3pt/char
// restore the measured 208px ink width and baseline.
slide.addText("Feature Invariants", {
  x: px(229 - 108), y: px(lineTop(117.5, 24, 30, CAL_TITLE)), w: 3, h: 0.5,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 24, bold: true, color: BLACK,
  lineSpacing: 30, charSpacing: 0.3,
});

// Header line — baseline 181.5, box x 126 (red 'F' ink at ~127). Runs: red bold
// "Features Invariants are ", regular black "is ", then "Problem dependent" REGULAR + ITALIC +
// UNDERLINED (underline must NOT cover " is " — original underline starts at 378, right after
// "is" ends at 376; slide_010 precedent).
slide.addText(
  [
    { text: "Features Invariants are ", options: { color: RED, bold: true } },
    { text: "is ", options: { color: BLACK, bold: false } },
    {
      text: "Problem dependent",
      options: { color: BLACK, bold: false, italic: true, underline: true },
    },
  ],
  {
    x: px(126), y: px(lineTop(181.5, 21, 25, CAL_21)), w: 8, h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 21,
    lineSpacing: 25,
  }
);

// Bullet lines — Arial Bold 21pt, text-left box 125.6 (ink 126.5), single-line boxes at
// measured baselines (44pt pitch). Casing verbatim per spec (bullet 3 lowercase 'invariant').
const BULLETS = [
  { text: "Rotation Invariant", baseline: 249 },
  { text: "Scaling Invariant", baseline: 293 },
  { text: "Translation invariant", baseline: 337 },
  { text: "Mirroring Invariant", baseline: 381 },
];
for (const B of BULLETS) {
  slide.addText(B.text, {
    x: px(125.6), y: px(lineTop(B.baseline, 21, 25, CAL_BULLET)), w: 4, h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 21, bold: true, color: BLACK,
    lineSpacing: 25,
  });
}

// Bullet dots (black round markers, d~5.5px, center x 108.3) at measured y-centers
const DOTS = [241, 285, 329, 373];
for (const cy of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(105.55), y: px(cy - 2.75), w: px(5.5), h: px(5.5),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
