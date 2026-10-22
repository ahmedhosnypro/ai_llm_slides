// slide_037.js — machine-learning/02_linear-regression-classification-MSSE
// "Assignment #2: Part 2 - Classification" (root slide, no parents)
//
// Geometry PIL-measured from unique_slides/slide_037.jpg (960x540, 1px = 1pt;
// inches = px/72). House chrome from shared_patterns/house_chrome.js.
// Font calibration (closed-loop PIL vs original): body 17pt Arial (sum abs err 136
// across 9 measured line widths vs 166 for 18pt / 37 for 17.5pt), title 21pt bold (red-run/gap/blue
// chain within 5px of measured ink). Text structure: 11 line pitch 33px (lineSpacing 33pt exact), item[4]
// wraps at "...Let your model" / "...classify the input", yellow FFFF00 run
// highlight covers "Positive for Class I and Negative for Others." (ink x182..517
// on line 2 of item 4), item[6] red, curly quotes. NOTE: spec says "Optional:" is
// underlined but the frame shows NO underline (red-ink profile: baseline rows n~31-35,
// descender-only below; a solid underline would read n~100+) — frame wins, no underline.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const NUMERAL = "37";

// measured colors (nominal per validated spec; JPEG-dark cores match the deck's
// ~0.55-0.65x thin-stroke factor, same calibration as the certified DL family)
const RED = "CC0000";
const BLUE = "0000CC";
const BLACK = "000000";
const HIGHLIGHT = "FFFF00";
const WHITE = "FFFFFF";

const FONT = "Arial";

// ---- content blocks (px units, converted /72) ----

function drawTitle(pptx, slide) {
  // title ink measured x312..689, y93..112 (cap top 93/94, descender 112);
  // left-anchored box so the red run starts at the measured ink position.
  slide.addText(
    [
      { text: "Assignment #2:", options: { color: RED } },
      { text: "  Part 2 - Classification", options: { color: BLUE } },
    ],
    {
      x: 311 / 72, y: 75.5 / 72, w: 520 / 72, h: 49 / 72,
      align: "left", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 21, bold: true,
    }
  );
}

function drawContentBox(pptx, slide) {
  // blue border measured: verticals x95-96 & x884-886, horizontals y117-119 & y491-493
  slide.addShape(pptx.ShapeType.rect, {
    x: 96 / 72, y: 118 / 72, w: 789 / 72, h: 374 / 72,
    fill: { color: WHITE },
    line: { color: BLUE, width: 2 },
  });
}

function bodyRuns() {
  const b = { fontFace: FONT, fontSize: 17.5, breakLine: true };
  return [
    { text: "[1] Use IRIS dataset, group samples of class 2 and class 3 together to form new class (Class II)", options: { ...b, color: BLACK, charSpacing: -0.09 } },
    { text: "[2] Split Class I samples into  40 samples for train and 10 samples for test", options: { ...b, color: BLACK } },
    { text: "[3] Split Class II samples into  80 samples for train and 20 samples for test", options: { ...b, color: BLACK } },
    { text: " ", options: { ...b, color: BLACK } },
    { text: "[4] Train your linear classifier model using Least Squares Technique (MSSE). Let your model", options: { ...b, color: BLUE } },
    { text: "output be ", options: { fontFace: FONT, fontSize: 17.5, color: BLUE } },
    { text: "Positive for Class I and Negative for Others.", options: { fontFace: FONT, fontSize: 17.5, color: BLUE, highlight: HIGHLIGHT } },
    { text: " This model is suitable to classify the input", options: { fontFace: FONT, fontSize: 17.5, color: BLUE, breakLine: true } },
    { text: "sample as Class I or \u201cOther classes\u201d", options: { ...b, color: BLUE } },
    { text: " ", options: { ...b, color: BLACK } },
    { text: "[5] Use your trained model to classify test samples (into either Class I or Class II)", options: { ...b, color: BLACK } },
    { text: "[6] ", options: { fontFace: FONT, fontSize: 17.5, color: RED } },
    { text: "Optional:", options: { fontFace: FONT, fontSize: 17.5, color: RED, underline: true } },
    { text: " train two other models to classify IRIS class 2 and IRIS class 3. This approach is", options: { fontFace: FONT, fontSize: 17.5, color: RED, breakLine: true } },
    { text: "called \u201cOne vs All\u201d", options: { ...b, color: RED, charSpacing: 0.45 } },
  ];
}

function drawContent(pptx, slide) {
  // text ink: lines start x105-106, first line ink top y138 (render closed-loop:
  // box y131 put first ink at 148, shifted to y121 -> 138), pitch 33px,
  // text right max x850 (line b) — box widened past the border so explicit
  // line breaks are never re-wrapped (box is invisible).
  slide.addText(bodyRuns(), {
    x: 103 / 72, y: 121 / 72, w: 800 / 72, h: 350 / 72,
    align: "left", valign: "top", margin: 0,
    lineSpacing: 33,
  });
}

function renderBase(pptx, slide) {
  drawHouseChrome(pptx, slide, { numeral: NUMERAL });
  drawTitle(pptx, slide);
  drawContentBox(pptx, slide);
  drawContent(pptx, slide);
}

// ---- direct run ----
if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const slide = pres.addSlide();
  renderBase(pres, slide);
  pres
    .writeFile({ fileName: __dirname + "/../slide_037_recreated.pptx" })
    .then(() => console.log("WROTE slide_037_recreated.pptx"))
    .catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawHouseChrome, drawTitle, drawContentBox, drawContent, NUMERAL };
