// slide_010.js — 001_introduction slide 10 "Pre processing" — Deep Learning DSAI 308.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_010.jpg (960x540, 1px = 1pt = 1/72 in).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 10 (file number; assumption PENDING FOUNDER VETO,
//   001_introduction/AGENTS.md 2026-10-12 — this lecture's originals carry no printed numbers).
//
// Measured constants (frame px):
//   title box    border centerlines x 106..325, y 61..118 (w219 h57); fill modal (250,254,217)
//                = FAFED9; border 000080 ~1.5pt (deck navy, cf. certified slide_005; spec guessed
//                2222CC — ink wins: border core px (41,34,104)/(11,3,80) are JPEG-softened 000080)
//   title ink    "Pre processing" x 125..306 (advance 181 = Arial Bold 25pt EXACT, err 0px),
//                cap-top 80, baseline 98; ink CENTER x=215.5 == box center 215.5 -> centered
//   content box  border centerlines x 95..882, y 127..513 (w787 h386); fill FFFFFF; border
//                000080 ~2pt (core 2 rows; modal (49,41,142) = 000080 + white bleed)
//   lead line    baseline 151.5, ink x 127..676: "Preprocessing" RED BOLD (ink 127..271, advance
//                145 = Arial Bold 21pt err 1), " is " + "Problem dependent and data dependent"
//                BLACK REGULAR 21pt (advance 375 = Arial Regular 21pt err 1)
//                FORENSICS: NO underline (rows 152-155 hold only the four 'p'/'g' descender
//                stems, no horizontal run) and NO italic (vertical 'p' stems) — the spec's
//                "italic and underlined" typography claim is overridden by ink (deck pixel law).
//   intro line   "It may include:" bold, ink x 127..271 (advance 144 = Arial Bold 21pt err 3;
//                stem 3px = bold), cap-top 185, baseline 198
//   bullets      Arial Regular 20pt (9/9 strings metric-solved, err 0-3px), text-left 147,
//                baselines 221.7/253.8/286/318.2/350.3/382.5/414.7/446.8/479 and the trailing
//                "......." line OFF the 32px rhythm at baseline 503 (dot center 495, pitch 24
//                from line 9 — reproduced as measured)
//   bullet dots  black d~5px x 127..131 (center x 129), y-centers 214/246/278.5/311/343/375/
//                407/439/471/495 (each ~7.7px above its baseline)
//   black bar    x 38..921, y 519..539 in the ORIGINAL; drawn y 519..537.5 (h 18.5) so the
//                chrome's half-visible bottom stroke stays visible and house_chrome_check.py
//                passes (same treatment as certified slide_005, 2-frame-px deviation documented)
//   NOT drawn (ink-verified absent / recording artifacts):
//     - the spec's "top rule": rows 42-44 ARE the chrome panel's own red top border position —
//       covered by drawHouseChrome, not a separate element (slide_005 precedent)
//     - the spec's "red square at far bottom-left": 0 red pixels anywhere in bar rows 519..539
//     - mouse cursor near bullet 7: screen-recording artifact (ground rule c)

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_010_recreated.pptx";

// ---- palette (measured) ----
const NAVY = "000080";   // box borders (deck navy, certified slide_005 law)
const RED = "C00000";    // lead word (playlist/deck red; modal (133,15,27)/(150,35,50) = JPEG-darkened C00000)
const BLACK = "000000";
const WHITE = "FFFFFF";
const TITLE_FILL = "FAFED9"; // measured modal (250,254,217)

const px = (v) => v / 72;

// Single-line text placement: baseline = top + (h_px - lineSpacing)/2 + 0.9052*size
// (formula confirmed by certified slide_005's "top = baseline - 25.63" for 25pt/L30/h36).
// CAL (closed-loop attempt 1 -> render_1 measured): LO renders every baseline slightly LOW
// vs the formula — bullets(20pt/L25) +1.8, lead/intro(21pt/L25) +1.1, title(25pt/L30) +2.1
// frame px — so each group's top is shifted up by its measured delta (sub-frame calibration).
const CAL_BULLET = -1.8, CAL_21 = -1.1, CAL_TITLE = -2.1;
const lineTop = (baseline, size, L, cal = 0) =>
  baseline - ((36 - L) / 2 + 0.9052 * size) + cal;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 10)
drawHouseChrome(pres, slide, { numeral: "10" });

// Title box (x 106..325, y 61..118), pale yellow fill, navy 1.5pt border
slide.addShape(pres.ShapeType.rect, {
  x: px(106), y: px(61), w: px(219), h: px(57),
  fill: { color: TITLE_FILL }, line: { color: NAVY, width: 1.5 },
});

// Main content box (x 95..882, y 127..513), white fill, navy 2pt border
slide.addShape(pres.ShapeType.rect, {
  x: px(95), y: px(127), w: px(787), h: px(386),
  fill: { color: WHITE }, line: { color: NAVY, width: 2 },
});

// Black footer bar (over the panel, as in the original; chrome bottom stroke kept visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(884), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Title "Pre processing" — Arial Bold 25pt black (advance 181 exact), centered in the
// title box (ink center 215.5 == box center), baseline 98. charSpacing 0.35: closed-loop
// attempt 1 measured LO rendering 176px wide vs the original's 181 (LO hinting compresses
// vs PIL advance prediction); +0.35pt/char restores the measured 181px ink width.
slide.addText("Pre processing", {
  x: px(215.5 - 108), y: px(lineTop(98, 25, 30, CAL_TITLE)), w: 3, h: 0.5,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 25, bold: true, color: BLACK,
  lineSpacing: 30, charSpacing: 0.35,
});

// Lead sentence — baseline 151.5, text-left 127. Runs: red bold "Preprocessing",
// then regular black " is Problem dependent and data dependent" (regular, NOT italic,
// NOT underlined — ink forensics above).
slide.addText(
  [
    { text: "Preprocessing", options: { color: RED, bold: true } },
    { text: " is Problem dependent and data dependent", options: { color: BLACK, bold: false } },
  ],
  {
    x: px(125.3), y: px(lineTop(151.5, 21, 25, CAL_21)), w: 8, h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 21,
    lineSpacing: 25,
  }
);

// Intro line "It may include:" — Arial Bold 21pt black, baseline 198, text-left 127
slide.addText("It may include:", {
  x: px(125.3), y: px(lineTop(198, 21, 25, CAL_21)), w: 4, h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 21, bold: true, color: BLACK,
  lineSpacing: 25,
});

// Bullet lines — Arial Regular 20pt, text-left 147, single-line boxes at measured baselines.
// charSpacing 0.45: closed-loop attempt 1 measured every bullet string ~0.45px/char narrower
// than the original (LO hinting vs PIL advance prediction; consistent across all 9 strings).
const BULLETS = [
  { text: "Gap filling", baseline: 221.7 },
  { text: "Thinning", baseline: 253.8 },
  { text: "Contour", baseline: 286 },
  { text: "Binarization", baseline: 318.2 },
  { text: "Noise Removal", baseline: 350.3 },
  { text: "Color to Gray", baseline: 382.5 },
  { text: "Opening touched points", baseline: 414.7 },
  { text: "Resizing", baseline: 446.8 },
  { text: "Normalization", baseline: 479 },
  { text: ".......", baseline: 503 }, // trailing ellipsis bullet — measured OFF-rhythm (baseline 503)
];
for (const B of BULLETS) {
  slide.addText(B.text, {
    x: px(145.7), y: px(lineTop(B.baseline, 20, 25, CAL_BULLET)), w: 4, h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 20, color: BLACK,
    lineSpacing: 25, charSpacing: 0.45,
  });
}

// Bullet dots (black round markers, d~5px, center x 129) at measured y-centers
const DOTS = [214, 246, 278.5, 311, 343, 375, 407, 439, 471, 495];
for (const cy of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(126.5), y: px(cy - 2.5), w: px(5), h: px(5),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
