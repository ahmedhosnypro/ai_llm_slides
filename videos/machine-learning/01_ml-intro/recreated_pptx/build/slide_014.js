// Slide 014 recreation — "Supervised Learning: Regression"
// Spec: videos/ml-intro/analysis/slide_014_final.json (validation verdict PASS_WITH_FIXES, score 9/10)
// STARTING POINT: the certified-PASS old-numbering build for this same original frame
// (old deck slide 16; banked verbatim at videos/ml-intro/recreated_pptx/qa/slide016/build_attempt_5.js,
// PASS transcript qa/slide016/judge_attempt_9.txt). Changes for the renumbered deck:
// badge numeral 16 -> 14 (founder directive: badge = number printed on the original
// image, which is 14), output path slide_014_recreated.pptx. All content/geometry
// re-verified against the corrected spec and the original frame (unchanged bytes).
// House frame rule (founder directive 2026-10-09) overrides spec for outer chrome:
// bg E8E8E8; red frame x:0.15 y:0.15 w:13.03 h:7.2 line C00000 w1.5; badge oval
// x:12.48 y:0.30 w:0.5 h:0.5 fill/line FFF9C4 with numeral "14" bold 18pt #333333;
// title box y:0.28 x:0.6 w:12.13 centered.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// Colors (never prefixed with '#')
const WHITE = "FFFFFF", RED = "C00000", BLACK = "000000", BLUE = "0000CC",
      GRAY = "E7E6E6", BG = "E8E8E8", BADGE_YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG }; // house frame background

// ---------------------------------------------------------------------------
// GEOMETRY: every content-box and text coordinate below is ANCHORED to PIL
// pixel measurements of the original frame unique_slides/slide_014.jpg
// (960x540 capture; slide inset; outer red frame lines measured at
// x=58/901, y=46.5/538.5; content box borders at x=70/885, y=142.5/522.5;
// all 8 text lines flush at x=101; line band tops at y=165,205,242,279,
// 353,390,427,464; title band y=98..121 center 109.5).
// Mapping onto the house frame rect (x0.15 y0.15 w13.03 h7.2):
//   fx(x) = 0.15 + (x-58)  * 13.03/843
//   fy(y) = 0.15 + (y-46.5)* 7.20 /492
// ---------------------------------------------------------------------------

// Gray interior (spec header band E7E6E6; frame measurement shows the gray
// fills the whole frame interior — gutters left/right/below the white box
// are the same E7E6E6 — so draw it full-interior, box goes on top).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: GRAY }, line: { color: GRAY, width: 0.5 },
});

// House frame: outer red rect (founder directive — overrides spec and judge)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});

// Title — house title box y0.28 x0.6 w12.13 centered; vertical center placed
// at the measured title center fy(109.5)=1.07 via valign middle in a box
// whose mid-point is 1.07 (h 1.56). "Regression" underlined. 28pt = measured
// title em ~26.7px (cap 0.69em, band 24px cap+descender).
s.addText([
  { text: "Supervised Learning: " },
  { text: "Regression", options: { underline: true } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 1.56, align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// House badge: oval x12.48 y0.30 w0.5 h0.5, fill/line FFF9C4, numeral "14"
// = number printed on the original image (deck curation 2026-10-09).
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("14", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Content box — measured from the original frame: borders at x70/885,
// y142.5/522.5 -> x0.336 y1.555 w12.60 h5.56. Border ~3px -> 2.75pt.
const BOX_X = 0.336, BOX_Y = 1.555, BOX_W = 12.60, BOX_H = 5.56;
s.addShape(pptx.shapes.RECTANGLE, {
  x: BOX_X, y: BOX_Y, w: BOX_W, h: BOX_H,
  fill: { color: WHITE }, line: { color: RED, width: 2.75 },
});

// Text lines — ALL FLUSH at x=101px -> fx=0.815 (the original frame shows NO
// indentation hierarchy; every line starts at the same left edge, overriding
// the spec brief's "two-level indent" wording per the rule that the frame is
// ground truth). Line pitch 37px -> 0.54in; one blank line (74px) before
// "Multivariate Regression:". Body em measured 23.5px -> 24pt;
// "Problem Types:" em ~26px -> 27pt. Box y = fy(band_top) - 0.19*em.
const TX = 0.815, TW = 11.7;
function line(y, runs, opts = {}) {
  s.addText(runs, {
    x: TX, y, w: TW, h: 0.55, align: "left", valign: "top",
    fontSize: opts.size || 24, color: opts.color || BLACK,
    bold: opts.bold || false, fontFace: FONT, margin: 0,
  });
}

// 7. "Problem Types:" bold red (band top 165.5 -> y 1.820, 27pt)
line(1.820, "Problem Types:", { color: RED, bold: true, size: 27 });

// 8. "Univariate Regression:" bold blue (band top 205 -> y 2.406)
line(2.406, "Univariate Regression:", { color: BLUE, bold: true });

// 9. "y is a single real-valued number" red (band top 242 -> y 2.947)
line(2.947, "y is a single real-valued number", { color: RED });

// 10. Example (univariate): "Example:" bold, "future price of a stock" underlined
line(3.496, [
  { text: "Example: ", options: { bold: true } },
  { text: "Predicting the " },
  { text: "future price of a stock", options: { underline: true } },
]);

// 11-12. one blank line, then "Multivariate Regression:" bold blue
line(4.572, "Multivariate Regression:", { color: BLUE, bold: true });

// 13. "y is a real-valued vector" red
line(5.114, "y is a real-valued vector", { color: RED });

// 14. "Each element of y tells the value of one response variable" black
line(5.655, "Each element of y tells the value of one response variable");

// 15. Example (multivariate): "Example:" bold, "Torque values in multiple joints" underlined
line(6.206, [
  { text: "Example: ", options: { bold: true } },
  { text: "Torque values in multiple joints", options: { underline: true } },
  { text: " of a robotic arm" },
]);

// 16. Plain left-aligned lines, no bullet markers (none used — original has none)

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_014_recreated.pptx" })
  .then(() => console.log("done: videos/ml-intro/recreated_pptx/slide_014_recreated.pptx"));
