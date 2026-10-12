// Build: slide 036 recreation — "Classification"
// Spec: videos/ml-intro/analysis/slide_036_final.json (validated PASS_WITH_FIXES, score 9/10)
// Output: videos/ml-intro/recreated_pptx/slide_036_recreated.pptx
//
// Geometry measured from unique_slides/slide_036.jpg (960x540 px == 13.33x7.5 in,
// 1 px == 1 pt):
//   Dark-red title banner: x 96-363 pt, y 83-141 pt (solid #8B0000), white bold
//   title "Classification" (glyph bbox x 142-316, y 103-120 -> ~24 pt), centered
//   inside the banner. Content box: x 72-885 pt, y 140-520 pt, white fill, thin
//   red (#C00000) outline. Subtitle "Examples of Commonly used classifiers:"
//   bold red, glyph bbox x 124-486, y 153-170 (~20 pt). 8 bullet lines starting
//   x 159 pt, row centers y 204..498 pt (42 pt pitch, ~18 pt bold black; bold
//   per pixel stroke width + the archived old104 analysis of the same kept
//   frame frame_03299.jpg). No red ink check/X marks exist on this kept frame
//   (verified by pixel scan); the faint gray cursor dot near bullet 2 is a
//   video artifact and is intentionally NOT recreated (spec brief step 10).
//   Badge numeral "36" confirmed printed on the original image.
//
// HOUSE FRAME (founder directive 2026-10-09) overrides the outer chrome:
//   bg E8E8E8, red frame x0.15 y0.15 w13.03 h7.2 line C00000 1.5pt, badge oval
//   12.48/0.30/0.5/0.5 FFF9C4 with numeral "36" (bold 18pt, 333333), title text
//   box starts y 0.28, x 0.6, w 12.13, centered. The original's gray header
//   band and outer double frame are superseded by the house values. Because the
//   house title box is full-width centered, the banner is horizontally centered
//   under the centered title (same reconciliation as sibling slide_037); its
//   vertical position is the original's measured y 83-141 pt.

const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;
const PT = 1 / 72; // measured JPG: 1 px == 1 pt

// Palette (spec + house) — NO '#' prefixes (corrupts file)
const BG = "E8E8E8";        // slide background (house)
const FRAME_RED = "C00000"; // house frame line
const BANNER = "8B0000";    // dark-red title banner fill (spec)
const SUB_RED = "C00000";   // subtitle text + content box outline (spec)
const TEXT = "000000";      // bullet text (spec)
const WHITE = "FFFFFF";    // content box fill + title text (spec)
const BADGE_YELLOW = "FFF9C4"; // house badge fill+line
const BADGE_INK = "333333";    // badge numeral (house)
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE FRAME: outer red frame, 0.15in inset from every edge, line C00000 1.5pt,
// no visible fill (gray E8E8E8).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// HOUSE slide-number badge: numeral "36" = the number printed on the original.
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("36", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_INK, fontFace: FONT, margin: 0,
});

// Content box (measured x 72-885 pt, y 140-520 pt): white fill, thin red outline.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 72 * PT, y: 140 * PT, w: (885 - 72) * PT, h: (520 - 140) * PT,
  fill: { color: WHITE }, line: { color: SUB_RED, width: 1.5 },
});

// Dark-red title banner (measured y 83-141 pt, w 267 pt), horizontally centered
// under the house centered title box (original had it at x 96-363; the house
// title geometry forces the centered placement — slide_037 reconciliation).
s.addShape(pptx.shapes.RECTANGLE, {
  x: (480 - 267 / 2) * PT, y: 83 * PT, w: 267 * PT, h: 58 * PT,
  fill: { color: BANNER }, line: { color: BANNER, width: 0.5 },
});

// Slide title — HOUSE text-box geometry (starts y:0.28, x:0.6, w:12.13, centered).
// Tall box + valign middle lands the ~24pt glyph line at the banner's measured
// center (y ~112 pt) inside the dark-red banner.
s.addText("Classification", {
  x: 0.6, y: 0.28, w: 12.13, h: 2.5511, align: "center", valign: "middle",
  fontSize: 24, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// Subtitle: bold red, verbatim (measured glyph top y 153 pt, left x 124 pt).
s.addText("Examples of Commonly used classifiers:", {
  x: 124 * PT, y: 150 * PT, w: 9.5, h: 0.45, align: "left", valign: "top",
  fontSize: 20, bold: true, color: SUB_RED, fontFace: FONT, margin: 0,
});

// Bullet list: 8 verbatim lines, manual bullet glyphs (NO pptxgenjs bullet
// options — known bug workaround), 42pt row pitch (paraSpaceAfter 21),
// first row center at measured y 204 pt.
const bullets = [
  "Linear Regression",
  "Logistic Regression",
  "Neural Network",
  "Support Vector Machine",
  "Hidden Markov Model",
  "Decision Trees",
  "Bayesian classifier",
  ".......",
];
const bulletRuns = bullets.map((t, i) => ({
  text: "\u2022  " + t,
  options: { breakLine: i < bullets.length - 1 },
}));
s.addText(bulletRuns, {
  x: 159 * PT, y: 193.6 * PT, w: 9.0, h: 4.7,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: TEXT, fontFace: FONT, margin: 0,
  paraSpaceAfter: 20,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_036_recreated.pptx" })
  .then(() => console.log("wrote videos/ml-intro/recreated_pptx/slide_036_recreated.pptx"));
