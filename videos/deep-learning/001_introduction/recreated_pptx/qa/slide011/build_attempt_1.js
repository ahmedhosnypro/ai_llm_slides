// slide_011.js — 001_introduction slide 11 "Feature Extraction" — Deep Learning DSAI 308.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_011.jpg (960x540, 1px = 1pt = 1/72 in).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 11 (file number; assumption PENDING FOUNDER VETO,
//   001_introduction/AGENTS.md 2026-10-12 — this lecture's originals carry no printed numbers).
//
// Measured constants (frame px):
//   title box    border centerlines x 94..364, y 61..119 (w271 h59); fill modal (226,255,251)
//                = pale cyan (spec #E0FFFF; JPEG channels wobble ±3); border 000080 ~1.5pt
//                (row61 core (29,39,100) = deck navy, cf. certified slide_005/010)
//   title ink    "Feature Extraction" x 123..335 (advance 213 = Arial Bold 24pt err -2; 25pt gives
//                +7 — this slide's title solved 24pt, slide 010's was 25pt), cap-top 80, baseline
//                ~97.5; ink CENTER x=229 == box center 229.5 -> centered
//   content box  border centerlines x 95..881, y 128..499 (w786 h371); fill FFFFFF; border
//                000080 ~2pt (rows 128+129, row 499 core (33,25,134) = 000080 + white bleed)
//   lead line    baseline 151.75 (underline rows 154-155 + 'p' descender 156), ink x 128..527:
//                "Features Types are " RED BOLD (ink 128..314, C00000 — most-saturated core
//                (160,5,23) = JPEG-darkened C00000, same as certified slide_010), " is " BLACK
//                REGULAR (ink 324..336), "Problem dependent" BLACK BOLD ITALIC + UNDERLINED
//                (ink 338..527; underline = continuous 183px faded-gray run y154-155 x345..527,
//                same forensics as certified slide_010's attempt-2 fix)
//   intro line   "Features may include:" bold, ink x 127..346 (advance 220 = Arial Bold 21pt
//                err +2), 'F' stem full-height at x127-129 -> text-left 127 (NO bullet dot),
//                cap-top 185, baseline 198.8 ('y' descender bottom 203)
//   bullets      Arial Regular 21pt (8/8 strings metric-solved, err +0..+3 with JPEG bleed;
//                20pt errs -1..-9 — rejected), text-left 147 (box 145.5), baselines
//                231.8/263.8/295.8/328.2/360.2/392.7/424.7/456.5 (dot-center = baseline-7.7 law,
//                pitch ~32.1 = certified slide_010's 32.14 rhythm)
//   bullet dots  black d~5px x 127..131 (center x 129), y-centers 224/256/288/320.5/352.5/385/
//                417/449/481 (ON the 32px rhythm; slide 010's trailing dots were off-rhythm,
//                this slide's are not)
//   ellipsis     last line = NINE baseline dots x148..204, y486..489, pitch 6.6px — exactly
//                3 x U+2026 at 20pt (Liberation/Arial: 3 dots/glyph at pitch em/3 = 6.67px,
//                ink span 2*20+15.3+3 = 58.3 vs measured 57; 4 ellipsis chars = 12 dots/80px
//                REJECTED by ink; 9 periods at 21pt = pitch 5.83 REJECTED). Spec verbatim said
//                "……" (4 chars) but _meta flagged dot count unverifiable — ink forensics wins
//                (same ink-wins treatment as certified slide_010's trailing dots). 20pt solved
//                by dot pitch (21pt pitch 7.0 vs measured 6.6).
//   left rule    red vertical rule core cols 57-58 (y 43..517), ~2pt, #8B0000 (core (105-124,
//                43-45, 52-53) — darker than the C00000 text red; spec says 8B0000). The
//                original's TOP rule (row 43, x57..901) is the chrome top-border position —
//                covered by drawHouseChrome, NOT drawn separately (certified slide_005/010 law).
//   gray band    the original's own gray band x61..902 y47..517 is subsumed by the chrome panel
//                (E9E9E7 vs measured (231,232,230)); NOT drawn (chrome ground rule (a))
//   black bar    x 38..921, y 518.5..539 in the ORIGINAL; drawn y 519..537.5 (h 18.5) so the
//                chrome's half-visible bottom stroke stays visible and house_chrome_check.py
//                passes (same treatment as certified slides 005/010, 2-frame-px documented)
//   NOT drawn:   mouse cursor artifact near "Number of intersections"/"Moments" (~19%W, ~60%H,
//                band-4 descender pollution x201..206 y338..342) — screen-recording artifact
//                (ground rule c)

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_011_recreated.pptx";

// ---- palette (measured) ----
const NAVY = "000080";   // box borders (deck navy, certified slide_005/010 law)
const RED = "C00000";    // lead phrase (playlist/deck red; certified slide_010 law)
const MAROON = "8B0000"; // left frame rule (spec; measured core darker than C00000)
const BLACK = "000000";
const WHITE = "FFFFFF";
const CYAN = "E0FFFF";   // title box fill (spec; measured modal (226,255,251))

const px = (v) => v / 72;

// Single-line text placement: baseline = top + (h_px - lineSpacing)/2 + 0.9052*size
// (formula confirmed by certified slide_005's "top = baseline - 25.63" for 25pt/L30/h36).
// LO renders every baseline slightly LOW vs the formula (slide_010 calibration): bullets/
// lead(21pt/L25) -1.1, lead-line(20pt/L25) -1.0, title(24pt/L30) -2.0 (starting values;
// closed-loop recalibrates from the 150dpi render).
const CAL_21 = -1.1, CAL_20 = -1.0, CAL_TITLE = -2.0;
const lineTop = (baseline, size, L, cal = 0) =>
  baseline - ((36 - L) / 2 + 0.9052 * size) + cal;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 11)
drawHouseChrome(pres, slide, { numeral: "11" });

// Left frame rule (content — the original's own L-frame leg; top leg = chrome border)
slide.addShape(pres.ShapeType.rect, {
  x: px(56.8), y: px(42.5), w: px(2.4), h: px(475),
  fill: { color: MAROON }, line: { color: MAROON, width: 0 },
});

// Title box (x 94..364, y 61..119), pale cyan fill, navy 1.5pt border
slide.addShape(pres.ShapeType.rect, {
  x: px(94), y: px(61), w: px(271), h: px(59),
  fill: { color: CYAN }, line: { color: NAVY, width: 1.5 },
});

// Main content box (x 95..881, y 128..499), white fill, navy 2pt border
slide.addShape(pres.ShapeType.rect, {
  x: px(95), y: px(128), w: px(786), h: px(371),
  fill: { color: WHITE }, line: { color: NAVY, width: 2 },
});

// Black footer bar (over the panel, as in the original; chrome bottom stroke kept visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(884), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Title "Feature Extraction" — Arial Bold 24pt black (advance 213 measured), centered in the
// title box (ink center 229 == box center 229.5), baseline ~97.5. Box w 4.5in: attempt-1
// closed-loop caught a TWO-LINE WRAP at w=3in (213px ink + charSpacing > 216pt box) — widened.
// charSpacing 0.2: LO hinting compresses vs PIL advance (certified slide_010 law; 0.35 measured
// +4px wide in the render).
slide.addText("Feature Extraction", {
  x: px(229.5 - 162), y: px(lineTop(97.5, 24, 30, CAL_TITLE)), w: 4.5, h: 0.5,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 24, bold: true, color: BLACK,
  lineSpacing: 30, charSpacing: 0.2,
});

// Lead sentence — baseline 151.75, text-left 128. Runs: red bold "Features Types are ",
// regular black " is ", then "Problem dependent" BOLD ITALIC + UNDERLINED (forensics:
// continuous 183px faded-gray run y154-155 x345..527; underline must NOT cover " is " —
// certified slide_010 attempt-2 law).
slide.addText(
  [
    { text: "Features Types are ", options: { color: RED, bold: true } },
    { text: "is ", options: { color: BLACK, bold: false } },
    {
      text: "Problem dependent",
      options: { color: BLACK, bold: true, italic: true, underline: true },
    },
  ],
  {
    x: px(126.3), y: px(lineTop(151.75, 20, 25, CAL_20)), w: 8, h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 20,
    lineSpacing: 25, charSpacing: 0.25,
  }
);

// Intro line "Features may include:" — Arial Bold 21pt black, baseline 198.8, text-left 127
slide.addText("Features may include:", {
  x: px(125.3), y: px(lineTop(198.8, 21, 25, CAL_21)), w: 4, h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 21, bold: true, color: BLACK,
  lineSpacing: 25, charSpacing: 0.15,
});

// Bullet lines — Arial Regular 21pt, text-left 147 (box 145.5), single-line boxes at measured
// baselines. charSpacing 0.1: closed-loop attempt 1 measured 0.25 → +2..+5px wide per string;
// 0.1 predicts every string within ±0.7px of the original ink.
const BULLETS = [
  { text: "Center of Gravity location,", baseline: 231.8 },
  { text: "Aspect Ratio,", baseline: 263.8 },
  { text: "Length and Width,", baseline: 295.8 },
  { text: "Number of intersections,", baseline: 328.2 },
  { text: "Moments,", baseline: 360.2 },
  { text: "Geometrical Features ,", baseline: 392.7 },
  { text: "Colors,", baseline: 424.7 },
  { text: "Transformations", baseline: 456.5 },
];
for (const B of BULLETS) {
  slide.addText(B.text, {
    x: px(145.5), y: px(lineTop(B.baseline, 21, 25, CAL_21)), w: 4, h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 21, color: BLACK,
    lineSpacing: 25, charSpacing: 0.1,
  });
}

// Ellipsis line — 3 x U+2026 at 20pt (nine baseline dots, pitch 6.67px, span ~58 = measured
// 57; ink forensics over the spec's unverifiable 4-char transcription — see header note).
slide.addText("\u2026\u2026\u2026", {
  x: px(146.5), y: px(lineTop(488.5, 20, 25, CAL_20)), w: 2, h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 20, color: BLACK,
  lineSpacing: 25,
});

// Bullet dots (black round markers, d~5px, center x 129) at measured y-centers
const DOTS = [224, 256, 288, 320.5, 352.5, 385, 417, 449, 481];
for (const cy of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(126.5), y: px(cy - 2.5), w: px(5), h: px(5),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
