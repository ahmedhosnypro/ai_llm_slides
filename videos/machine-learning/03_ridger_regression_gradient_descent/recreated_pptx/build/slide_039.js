// slide_039.js — "Gradient Descent (GD) – Stochastic Gradient Descent SGD) and Mini-Batch Gradient Descent"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (lecture 03)
//
// GEOMETRY LAW: every value below is a MEASURED frame pixel taken from the original
// frame unique_slides/slide_039.jpg (960x540, 1px = 1pt = 1/72 in).
// Text content is VERBATIM from analysis/slide_039_final.json.
//
// MEASURED TARGETS (frame px, ink extents / border centerlines / baselines):
//   House chrome (from shared_patterns/house_chrome.js):
//     Canvas: white FFFFFF, 13.333 x 7.5 in
//     Gray panel: x=54, y=45, w=850 (to 903), h=495 (to 540), fill E9E9E7
//     Strokes: C00000 1pt — LEFT x58.5 (y46..539), RIGHT x901 (y46..539), BOTTOM y538.5 (x58..902)
//     Badge: center (876,73), d=35, fill FDFD96, ring 6A5ACD 2pt, numeral 333333 Arial 18pt bold
//
//   Content panel (blue border):
//     Top border: y=142, x=73..867
//     Bottom border: y=482, x=74..868
//     Left border: x=73 (from top border left edge)
//     Right border: x=867-868, y=142..479
//     Interior: white
//     Border color: blue #0000FF (spec), measured ~navy (71,60,191) JPEG-darkened
//     Panel rect: x=73, y=142, w=795, h=340
//
//   Green callout box (filled light green with green border):
//     Interior: light green ~DFFFEB (measured 223,255,235)
//     Top: y=268, Bottom: y=301 (border at y=300-301)
//     Left: x=340, Right: x=865
//     Width: 525, Height: 33 (interior)
//
//   Title line 1 (red C00000): "Gradient Descent (GD) – Stochastic Gradient Descent SGD)"
//     Ink band: y~81..95 (ascender..descender), baseline ~93, center x~479
//     Font: Arial Bold ~32pt (measured advance ~716px for full string)
//
//   Title line 2 (blue 0000FF): "and Mini-Batch Gradient Descent"
//     Ink band: y~108..128, baseline ~118, center x~471
//     Font: Arial Bold ~28pt
//
//   Upper bullets (3 bullets, black text, blue chevron markers):
//     Bullet 1: y~165..175
//     Bullet 2: y~186..193
//     Bullet 3: y~211..218
//     Chevrons at x~103..148, text starts ~x151
//
//   Equation in green callout:
//     Formula: W^(updated)=W^old - η δ_i X_i
//     Position: centered in green box (x~340..865, y~268..301)
//     Equation PNG: eq_039_main.png (2295x246 @600dpi, 3.825 x 0.41 in, baseline_frac=0.79675)
//
//   "Repeat for ALL misclassified Samples" (red C00000):
//     Right of formula in green box, y~283..288, x~605..814
//
//   Why using SGD (red C00000 bold):
//     y~313..317, x~85..211, baseline ~315
//
//   Lower bullets (2 bullets, black text, blue chevron markers):
//     Bullet 4: y~363
//     Bullet 5: y~371 and ~414..418 (wrapped?)
//     Chevrons at x~101..149, text starts ~x154
//
//   Bottom caption:
//     Red line: "Batch GD is a generalization of GD and SGD where weights are updated after passing through "Mini-Batch" of training samples with size n"
//       y~461, x~80..799
//     Blue line (centered): "If n=N (it is GD), and if n=1 (it is SGD)"
//       y~470..473, x~313..627 (centered at ~470)

const pptxgenpkg = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const PX = 1 / 72; // frame px -> inches
const RED = "C00000";
const BLUE = "0000FF";
const BLACK = "000000";
const GREEN_BORDER = "00B050";
const GREEN_FILL = "DFFFEB"; // light green fill measured ~(223,255,235)
const FONT = "Arial";
const FONT_SERIF = "Times New Roman"; // spec says serif, but Arial used in prior slides

// Equation composite (600dpi PNG from render_eq.py)
const EQ = {
  path: path.resolve(__dirname, "assets/eq_039_main.png"),
  wIn: 3.825, hIn: 0.41,
  // Place so ink baseline aligns with text baseline in green box
  // Green box interior y=268..301, center y=284.5
  // Equation baseline_frac = 0.79675, so baseline from top = 0.79675 * 0.41 = 0.327 in
  // We want equation baseline at green box center y=284.5px = 3.95 in
  // So image top = 3.95 - 0.327 = 3.623 in = 261 px
  // But green box top is at y=268px = 3.722 in
  // Let's place image top at green box top + small padding
  x: 340 * PX + 0.05, // left padding inside green box
  y: 268 * PX + 0.02, // top padding
};

// ---- Tuning knobs (frame px deltas) ----
// Will adjust after first render
const TUNE = {
  title1: { size: 32, charSpacing: 0, dx: 0, dy: 0 },
  title2: { size: 28, charSpacing: 0, dx: 0, dy: 0 },
  upper_bullets: { size: 20, charSpacing: 0, dy: 0 },
  eq_annotation: { size: 16, dy: 0 },
  why_sgd: { size: 22, dy: 0 },
  lower_bullets: { size: 20, charSpacing: 0, dy: 0 },
  caption_red: { size: 18, dy: 0 },
  caption_blue: { size: 18, dy: 0 },
};

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

const slide = pptx.addSlide();

// House chrome: white canvas, gray panel, red L/R/Bottom strokes (NO top), badge "39"
drawHouseChrome(pptx, slide, { numeral: 39 });

// ---- Content panel (white rect with blue border) ----
// Panel rect: x=73, y=142, w=795, h=340
slide.addShape(pptx.ShapeType.rect, {
  x: 73 * PX, y: 142 * PX, w: 795 * PX, h: 340 * PX,
  fill: { color: "FFFFFF" },
  line: { color: BLUE, width: 2 }, // thick blue border per spec
});

// ---- Green callout box (filled with green border) ----
// x=340, y=268, w=525, h=33
slide.addShape(pptx.ShapeType.rect, {
  x: 340 * PX, y: 268 * PX, w: 525 * PX, h: 33 * PX,
  fill: { color: GREEN_FILL },
  line: { color: GREEN_BORDER, width: 2 },
});

// ---- Title line 1 (red, bold) ----
// Target: center x~479, baseline ~93px (1.292 in)
// Box: width ~720px (10in), height ~60px
slide.addText("Gradient Descent (GD) \u2013 Stochastic Gradient Descent SGD)", {
  x: (479 - 360 + TUNE.title1.dx) * PX,
  y: (93 - 30 + TUNE.title1.dy) * PX, // baseline - half box height approx
  w: 720 * PX, h: 60 * PX,
  align: "center", valign: "middle",
  fontSize: TUNE.title1.size, bold: true, color: RED, fontFace: FONT, margin: 0,
  ...(TUNE.title1.charSpacing && { charSpacing: TUNE.title1.charSpacing }),
});

// ---- Title line 2 (blue, bold) ----
// Target: center x~471, baseline ~118px (1.639 in)
slide.addText("and Mini-Batch Gradient Descent", {
  x: (471 - 360 + TUNE.title2.dx) * PX,
  y: (118 - 30 + TUNE.title2.dy) * PX,
  w: 720 * PX, h: 60 * PX,
  align: "center", valign: "middle",
  fontSize: TUNE.title2.size, bold: true, color: BLUE, fontFace: FONT, margin: 0,
  ...(TUNE.title2.charSpacing && { charSpacing: TUNE.title2.charSpacing }),
});

// ---- Upper bullets (3 bullets) ----
// Chevron char: ▶ (U+25B6) or ▸ (U+25B8) - use a simple arrow
// Chevrons at x~103..148, text at x~151..695
// We'll use manual bullet prefix with blue color

const BULLET_CHEVRON = "\u25B6 "; // ▶ 
const BULLET_X = 151; // text start
const BULLET_W = 550; // width to right edge

// Bullet 1: "Stochastic Gradient Descent (SGD) is a variant of GD which computes the gradient of the Error function with respect to a single training example"
// y~170 baseline
slide.addText([
  { text: BULLET_CHEVRON, options: { color: BLUE, fontSize: TUNE.upper_bullets.size, fontFace: FONT, bold: false } },
  { text: "Stochastic Gradient Descent (SGD) is a variant of GD which computes the gradient of the Error function with respect to a single training example", options: { color: BLACK, fontSize: TUNE.upper_bullets.size, fontFace: FONT, breakLine: true } },
], {
  x: (103 + TUNE.upper_bullets.dx) * PX, // chevron at x~103
  y: (170 - 15 + TUNE.upper_bullets.dy) * PX,
  w: (BULLET_W + 50) * PX, h: 40 * PX,
  fontFace: FONT, margin: 0, lineSpacing: 24,
});

// Bullet 2: "In other words, it updates the weights using one training sample at a time"
// y~189 baseline
slide.addText([
  { text: BULLET_CHEVRON, options: { color: BLUE, fontSize: TUNE.upper_bullets.size, fontFace: FONT } },
  { text: "In other words, it updates the weights using one training sample at a time", options: { color: BLACK, fontSize: TUNE.upper_bullets.size, fontFace: FONT, breakLine: true } },
], {
  x: (103 + TUNE.upper_bullets.dx) * PX,
  y: (189 - 15 + TUNE.upper_bullets.dy) * PX,
  w: (BULLET_W + 50) * PX, h: 40 * PX,
  fontFace: FONT, margin: 0, lineSpacing: 24,
});

// Bullet 3: "Remember: GD updated the weight vector after passing through ALL training samples."
// y~214 baseline
slide.addText([
  { text: BULLET_CHEVRON, options: { color: BLUE, fontSize: TUNE.upper_bullets.size, fontFace: FONT } },
  { text: "Remember: GD updated the weight vector after passing through ALL training samples.", options: { color: BLACK, fontSize: TUNE.upper_bullets.size, fontFace: FONT, breakLine: true } },
], {
  x: (103 + TUNE.upper_bullets.dx) * PX,
  y: (214 - 15 + TUNE.upper_bullets.dy) * PX,
  w: (BULLET_W + 50) * PX, h: 40 * PX,
  fontFace: FONT, margin: 0, lineSpacing: 24,
});

// ---- Equation in green callout ----
// Place the equation PNG
slide.addImage({
  path: EQ.path,
  x: EQ.x, y: EQ.y, w: EQ.wIn, h: EQ.hIn,
});

// "Repeat for ALL misclassified Samples" - red, right of equation in green box
// Measured at y~283..288, x~605..814
slide.addText("Repeat for ALL misclassified Samples", {
  x: (605 + TUNE.eq_annotation.dx) * PX,
  y: (285 - 10 + TUNE.eq_annotation.dy) * PX,
  w: 220 * PX, h: 20 * PX,
  align: "left", valign: "middle",
  fontSize: TUNE.eq_annotation.size, color: RED, fontFace: FONT, margin: 0,
});

// ---- Why using SGD (red subheading) ----
// y~315 baseline, x~85..211
slide.addText("Why using SGD", {
  x: (85 + TUNE.why_sgd.dx) * PX,
  y: (315 - 18 + TUNE.why_sgd.dy) * PX,
  w: 130 * PX, h: 36 * PX,
  align: "left", valign: "middle",
  fontSize: TUNE.why_sgd.size, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- Lower bullets (2 bullets) ----
// Bullet 4: "SGD is usually more efficient than GD" (with "efficient" in red)
// y~363 baseline
slide.addText([
  { text: BULLET_CHEVRON, options: { color: BLUE, fontSize: TUNE.lower_bullets.size, fontFace: FONT } },
  { text: "SGD is usually more ", options: { color: BLACK, fontSize: TUNE.lower_bullets.size, fontFace: FONT } },
  { text: "efficient", options: { color: RED, fontSize: TUNE.lower_bullets.size, fontFace: FONT } },
  { text: " than GD", options: { color: BLACK, fontSize: TUNE.lower_bullets.size, fontFace: FONT, breakLine: true } },
], {
  x: (103 + TUNE.lower_bullets.dx) * PX,
  y: (363 - 15 + TUNE.lower_bullets.dy) * PX,
  w: (BULLET_W + 50) * PX, h: 40 * PX,
  fontFace: FONT, margin: 0, lineSpacing: 24,
});

// Bullet 5: "SGD converges faster than GD"
// y~371 baseline (and wrapped at y~414)
slide.addText([
  { text: BULLET_CHEVRON, options: { color: BLUE, fontSize: TUNE.lower_bullets.size, fontFace: FONT } },
  { text: "SGD converges faster than GD", options: { color: BLACK, fontSize: TUNE.lower_bullets.size, fontFace: FONT, breakLine: true } },
], {
  x: (103 + TUNE.lower_bullets.dx) * PX,
  y: (371 - 15 + TUNE.lower_bullets.dy) * PX,
  w: (BULLET_W + 50) * PX, h: 40 * PX,
  fontFace: FONT, margin: 0, lineSpacing: 24,
});

// ---- Bottom caption ----
// Red line: left-aligned, y~461
slide.addText('Batch GD is a generalization of GD and SGD where weights are updated after passing through \u201cMini-Batch\u201d of training samples with size n', {
  x: (80 + TUNE.caption_red.dx) * PX,
  y: (461 - 12 + TUNE.caption_red.dy) * PX,
  w: 720 * PX, h: 24 * PX,
  align: "left", valign: "middle",
  fontSize: TUNE.caption_red.size, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Blue line: centered, y~472
slide.addText('If n=N (it is GD), and if n=1 (it is SGD)', {
  x: (313 + TUNE.caption_blue.dx) * PX,
  y: (472 - 12 + TUNE.caption_blue.dy) * PX,
  w: 314 * PX, h: 24 * PX,
  align: "center", valign: "middle",
  fontSize: TUNE.caption_blue.size, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

const OUT = path.resolve(__dirname, "../slide_039_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));