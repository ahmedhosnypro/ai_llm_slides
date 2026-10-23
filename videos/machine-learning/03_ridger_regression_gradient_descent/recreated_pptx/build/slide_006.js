// Build: slide 006 — "Problems of Linear Regression (With Linearly Separable Data)"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GEOMETRY SOURCE: PIL measurement of unique_slides/slide_006.jpg (960x540, 1px=1pt=1/72in)
// Spec: analysis/slide_006_final.json
//
// MEASURED LAYOUT (frame px):
//   Title "Problems of Linear Regression" (red C00000, bold):
//     ink bbox x175..798 y247..290, center ~486, cap-top ~250
//   Subtitle "(With Linearly Separable Data)" (blue 0000FF, italic):
//     ink bbox x241..731 y295..329, center ~486, cap-top ~300
//   House chrome (from house_chrome.js / AGENTS.md):
//     canvas FFFFFF | panel E9E9E7 rect x54..903 y45..540
//     red C00000 1pt strokes: LEFT x58.5 y46..539, RIGHT x901 y46..539, BOTTOM y538.5 x58..902
//     badge: center (876,73) d35 fill FDFD96 ring 6A5ACD 2pt, numeral 6 bold Arial 18pt 333333
//
// NOTE: Notification text is screen-capture artifact (OS notification), omitted per judge ground rule (c).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = __dirname + "/../slide_006_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome: white canvas, gray panel, red L/R/bottom strokes, badge "6" ----
drawHouseChrome(pptx, slide, { numeral: 6 });

const A = "Arial";

// ---- title: single centered line, red C00000, bold ----
// Measured: center x486, cap-top y250 (frame px)
const titleSize = 44;
const titleCtr = 486;
const titleCapTop = 250;
slide.addText("Problems of Linear Regression", {
  x: px(titleCtr - 350),
  y: px(titleCapTop - 0.25 * titleSize),
  w: px(700),
  h: px(titleSize * 1.5),  // tighter box
  align: "center",
  valign: "top",
  fontSize: titleSize,
  bold: true,
  color: "C00000",
  fontFace: A,
  margin: 0,
});

// ---- subtitle: single centered line, blue 0000FF, italic ----
// Measured: center x486, cap-top y300 (frame px)
// Use SAME x/w pattern as title for consistent centering
const subSize = 28;
const subCtr = 486;
const subCapTop = 300;
slide.addText("(With Linearly Separable Data)", {
  x: px(subCtr - 350),  // same half-width as title
  y: px(subCapTop - 0.25 * subSize),
  w: px(700),           // same width as title
  h: px(subSize * 1.5),
  align: "center",
  valign: "top",
  fontSize: subSize,
  bold: false,
  italic: true,
  color: "0000FF",
  fontFace: A,
  margin: 0,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));