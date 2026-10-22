// Slide 036 — "Assignment #2: Part 1 - Prediction"
// Deck: machine-learning/02_linear-regression-classification-MSSE
//
// Ground truth: unique_slides/slide_036.jpg (960x540, 1px = 1pt = 1/72 in).
// PIL measurements (workers ml02-w036-a1 measurements banked in scratch/ml02/slide036/,
// re-verified 2026-10-13 by ml02-w036-a3 — outputs in scratch/ml02/slide036/outputs/):
//   - Title: red "Assignment #2:" ink x329..483, blue "Part 1 - Prediction" ink
//     x493..673 (total ink x328..673, center x=501 — 21px RIGHT of panel center 480,
//     frame wins); cap top y~93, baseline ~107.5, descender to 112 -> ~20pt Arial Bold.
//     Blue segment core (2,0,134)/(49,36,135 border) -> navy 000080 (NOT the spec's
//     assumed 0000CC — measured core b~135 excludes 204).
//   - Blue instructions box: rect edges x95.5..884.5, y118..301, ~1.5-2pt border
//     (core rows 117-119, cols 95-96/884-885), fill white.
//   - Body: 4 instructions, L3 wraps after "best fit" (forced breakLine); baselines
//     151.5/184.5/217.5/250.5/283.5 -> exact pitch 33pt; digit/cap height 13px,
//     x-height 9px, L1 advance ~477px @ em18 -> 18pt Arial. Ink left edge x106.
//   - L2 quirk (measured): standalone 'x' (x356..363) and 'y' (x707..713) are RED;
//     the digits of "x1" and "x10" are SUBSCRIPTS (h~7px, rows 179..186, i.e. ~58%
//     size dropped ~1.5px below baseline) but the '2' of "x2" is FULL SIZE (h13,
//     rows 172..184) — an inconsistency in the ORIGINAL slide, reproduced as-is.
//     Sub digits drawn as 10.5pt runs on the shared baseline (closest LO render).
//   - No red anywhere else in the box (L1/L3/L4 variables are black) — frame wins
//     over the spec's "all four lines" claim.
//   - Plot boxes: LEFT x147..430, RIGHT x497..780, both y314..522, ~1pt C00000
//     border, white fill.
//   - Axes (both plots, right = left +350px): thin dusty-pink L (measured v-stroke
//     (203,178,182) @ col193/543, h-stroke (229,198,206) @ rows490-491 -> nominal
//     D8BCC2 ~0.75pt), v x193.5 y331..490.5, h y490.5 x193.5..408; red C00000
//     arrowheads: up-triangle apex(193.5,324) base y330.5 w6; right-triangle apex
//     (415.5,489.5) base x408 h6. Labels italic red ~16pt: 'y' ink ctr (181,340.5),
//     'x' ink ctr (405.5,503).
//   - Dots 5+5, steel blue 5B7FA6, d~8px. LEFT ctrs (204.9,449.9)(237.8,437.4)
//     (270.7,421.2)(297.9,411.8)(337.8,396.0); RIGHT ctrs (554.4,449.5)(587.5,443.2)
//     (620.4,414.7)(647.8,411.7)(687.2,399.3).
//   - Equations: "y = 3x+2" appears inline in the body text exactly as the original
//     (no stacked constructs) -> rendered as plain text, matching the original
//     pixel-for-pixel; professional-2D mechanism not triggered (no fraction/sum/
//     script constructs on this slide).
// House chrome via the deck's shared module (panel x61..899 y46->bottom E9E9E7,
// C00000 1pt border, bottom stroke rows 538-539, badge FDFD96 center (876,73) d35
// ring 6A5ACD, numeral 36 = the number printed on the original).

// Attempt-3 closed-loop corrections (selfcheck_attempt_2 vs render_2.png):
//   - WRAP: instruction [3] wraps after "of the line", NOT after "best fit" —
//     word-by-word advance solve (scratch outputs/wrap_solve.out) gives prefix 741
//     after "line" = measured L3a ink 736; attempt-2's late break spilled [3] to
//     4 lines and pushed [4] below the box. L3b = "that best fit on the ...".
//   - BODY SIZE 19.3pt Calibri (fit over L1/L2/L3a/L3b/L4 advances; 20pt overshot
//     L4 by +41px and wrapped it; 19.3 residuals within +-18px on 960px lines).
//   - TITLE: NOT Calibri Bold (10% too narrow: 138/160 vs 154/180) — Arial Bold
//     21.5pt matches the measured segment widths at +-4px (attempt-1 Arial-20
//     render scaled; box unchanged, ink landed y93.6..112.3 vs orig 93..112).
//   - Subscript digits 11.2pt (58% of 19.3).

// Attempt-4 (pre-judge render tuning): per-line charSpacing closes the residual
// progressive width drift of the Calibri fit (orig font is Calibri-like but not
// metric-identical): L2 +0.22pt/char (red x lands 356, red y ~707, right edge 767),
// L3b -0.25pt/char (right edge 619), L4 -0.1pt/char (right edge 863). Content and
// breaks untouched — rendering-only alignment, verified by selfcheck_attempt_4.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require(path.join(
  __dirname, "..", "..", "shared_patterns", "house_chrome.js"
));

const PX = 1 / 72; // frame px -> inches (1px = 1pt)
const FONT = "Calibri"; // body font (measured advances match Calibri, not Arial)
const TITLE_FONT = "Arial"; // title font (measured advances match Arial, not Calibri)

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "slide-recreation";
pres.title = "Assignment #2: Part 1 - Prediction";

const slide = pres.addSlide();

// --- House chrome (shared module; numeral = number printed on the original = 36) ---
drawHouseChrome(pres, slide, { numeral: 36 });

// --- Title: two-color, measured ink center x=501 (not panel center 480), center y 102.5 ---
// LO valign:middle renders the ink ~0.09em (1.9px @20pt) below the box center -> boxCenterY 100.6.
slide.addText(
  [
    { text: "Assignment #2: ", options: { color: "C00000" } },
    { text: "Part 1 - Prediction", options: { color: "000080" } },
  ],
  {
    x: (501 - 838 / 2) * PX, // box centered on measured ink center x=501
    y: (100.6 - 30) * PX,    // box h 60px, center 100.6
    w: 838 * PX,
    h: 60 * PX,
    align: "center",
    valign: "middle",
    bold: true,
    fontSize: 21.5,
    fontFace: TITLE_FONT,
    margin: 0,
  }
);

// --- Instructions box: measured rect edges x95.5..884.5, y118..301, ~1.5pt navy border ---
slide.addShape(pres.ShapeType.rect, {
  x: 95.5 * PX,
  y: 118 * PX,
  w: 789 * PX,
  h: 183 * PX,
  fill: { color: "FFFFFF" },
  line: { color: "000080", width: 1.5 },
});

// --- Body: 4 instructions (5 rendered lines, L3 forced break after "best fit"),
// 18pt Arial, exact 33pt pitch, ink left edge x106 (box x105, margin 0, valign top),
// first baseline 151.5 -> box top 128.75. Subscript digits per measured quirk. ---
slide.addText(
  [
    { text: "[1] Define any linear equation of one variable (e.g. y = 3x+2)", options: { breakLine: true } },
    { text: "[2] Select 5 different values for ", options: { charSpacing: 0.22 } },
    { text: "x", options: { color: "C00000", charSpacing: 0.22 } },
    { text: " (x", options: { charSpacing: 0.22 } },
    { text: "1", options: { fontSize: 11.2, charSpacing: 0.22 } },
    { text: ", x2,… x", options: { charSpacing: 0.22 } },
    { text: "10", options: { fontSize: 11.2, charSpacing: 0.22 } },
    { text: ") and calculate corresponding ", options: { charSpacing: 0.22 } },
    { text: "y", options: { color: "C00000", charSpacing: 0.22 } },
    { text: " values", options: { charSpacing: 0.22, breakLine: true } },
    { text: "[3] Use x and y values as training data , apply MSSE technique to obtain the equation of the line", options: { breakLine: true } },
    { text: "that best fit on the training data (compare to your defined equation)", options: { charSpacing: -0.25, breakLine: true } },
    { text: "[4] Repeat 1,2, and 3 after adding random noise term to the equation (e.g. y = 3x+2 + random(0..1)", options: { charSpacing: -0.1 } },
  ],
  {
    x: 105 * PX,
    y: 123 * PX, // closed-loop: baseline1 = 123 + 33 - desc(Calibri ~19.3pt) ~= 151.5
    w: 780 * PX,
    h: 172 * PX,
    align: "left",
    valign: "top",
    fontSize: 19.3,
    fontFace: FONT,
    color: "000000",
    lineSpacing: 33,
    margin: 0,
  }
);

// --- Scatter plots: boxes + axes + arrowheads + labels + dots ---

// Axis color: thin dusty-pink L-shape (measured (203,178,182)/(229,198,206) -> D8BCC2)
const AXIS = { color: "D8BCC2", width: 0.75 };

function drawPlot(ox) { // ox = 0 for LEFT (box x147), 350 for RIGHT (box x497)
  // white plot box, 1pt C00000 border
  slide.addShape(pres.ShapeType.rect, {
    x: (147 + ox) * PX,
    y: 314 * PX,
    w: 283 * PX,
    h: 208 * PX,
    fill: { color: "FFFFFF" },
    line: { color: "C00000", width: 1 },
  });
  // L-shaped axis (thin pink): vertical x=193.5 from y331 to y490.5; horizontal y=490.5 to x408
  slide.addShape(pres.ShapeType.line, {
    x: (193.5 + ox) * PX, y: 331 * PX, w: 0, h: 159.5 * PX,
    line: { color: AXIS.color, width: AXIS.width },
  });
  slide.addShape(pres.ShapeType.line, {
    x: (193.5 + ox) * PX, y: 490.5 * PX, w: 214.5 * PX, h: 0,
    line: { color: AXIS.color, width: AXIS.width },
  });
  // red arrowheads: up-triangle apex (193.5,324), base y330.5 w6
  slide.addShape(pres.ShapeType.triangle, {
    x: (190.5 + ox) * PX, y: 324 * PX, w: 6 * PX, h: 6.5 * PX,
    fill: { color: "C00000" }, line: { type: "none" },
  });
  // right-triangle apex (415.5,489.5): unrotated bbox w6 h7.5 centered (411.75,489.5), rotate 90 cw
  slide.addShape(pres.ShapeType.triangle, {
    x: (411.75 + ox) * PX - 3 * PX, y: 489.5 * PX - 3.75 * PX, w: 6 * PX, h: 7.5 * PX,
    rotate: 90,
    fill: { color: "C00000" }, line: { type: "none" },
  });
  // red italic axis labels (Arial italic 16 — crop judges: orig label glyphs are a
  // plainer, bolder sans-italic than Calibri's curvier 'y'; Arial matches the title
  // family and the measured ink sizes w7-8/h12; box centers nudged -1.4px for the
  // LO valign-middle ink offset)
  slide.addText("y", {
    x: (181 - 10 + ox) * PX, y: (339.1 - 9) * PX, w: 20 * PX, h: 18 * PX,
    align: "center", valign: "middle", italic: true, fontSize: 16,
    color: "C00000", fontFace: "Arial", margin: 0,
  });
  slide.addText("x", {
    x: (405.5 - 10 + ox) * PX, y: (501.6 - 8) * PX, w: 20 * PX, h: 16 * PX,
    align: "center", valign: "middle", italic: true, fontSize: 16,
    color: "C00000", fontFace: "Arial", margin: 0,
  });
}

// dots (steel blue 5B7FA6, d=8px), measured centers — drawn AFTER drawPlot so the
// white plot fills (z-order) never cover them (attempt-1 lesson)
const DOTS_L = [[204.9, 449.9], [237.8, 437.4], [270.7, 421.2], [297.9, 411.8], [337.8, 396.0]];
const DOTS_R = [[554.4, 449.5], [587.5, 443.2], [620.4, 414.7], [647.8, 411.7], [687.2, 399.3]];

drawPlot(0);   // LEFT plot, box x147..430
drawPlot(350); // RIGHT plot, box x497..780

for (const [cx, cy] of DOTS_L) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: (cx - 4) * PX, y: (cy - 4) * PX, w: 8 * PX, h: 8 * PX,
    fill: { color: "5B7FA6" }, line: { type: "none" },
  });
}
for (const [cx, cy] of DOTS_R) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: (cx - 4) * PX, y: (cy - 4) * PX, w: 8 * PX, h: 8 * PX,
    fill: { color: "5B7FA6" }, line: { type: "none" },
  });
}

const OUT = path.join(__dirname, "..", "slide_036_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE", OUT);
});
