// Slide 042 recreation — "K-NN: Computing the distances"
// Spec: videos/ml-intro/analysis/slide_042_final.json (validated PASS_WITH_FIXES, fixes applied;
// re-verified against the CURATED frame unique_slides/slide_042.jpg — the curated frame has NO
// hand-drawn red sketch; the sketch belongs to a later frame of the lecture segment).
// Derived from the pre-curation build (old id 54, judge-PASS attempt 2).
// House frame (founder directive 2026-10-09, OVERRIDES spec for the outer chrome):
//   background E8E8E8, red frame x:0.15 y:0.15 w:13.03 h:7.2 line C00000 w1.5,
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill FFF9C4 line FFF9C4, numeral "42"
//   (bold 18pt, color 333333) — matches the original slide's printed number 42.
//   Title text box y:0.28 x:0.6 w:12.13, centered.
// Spec content (verbatim, no invented facts):
//   - red bold title "K-NN: Computing the distances" (CC0000)
//   - red-bordered content box (~22-95% slide height, ~5-95% width)
//   - 4 black bullets on the left (body serif, Times-like per vision audit); bullet 1 has
//     yellow FFFF00 highlight on "test example" and "each of the training examples";
//     bullet 4 has "Euclidean" underlined
//   - bottom: yellow FFFF99 box with blue 0000CC border spanning the content box
//     width, holding the Euclidean distance equation (italic serif math style)
// MATH REWORK (founder directive 2026-10-09 — professional 2D equations):
//   - The Euclidean distance equation is now a matplotlib-mathtext 600dpi transparent
//     PNG (build/assets/eq_042_distance.png, 26pt, #000000, sidecar eq_042_distance.json)
//     embedded with addImage at EXACT sidecar size (w = px/600 in, never rescaled)
//     — radical vinculum, large ∑ with stacked m=1 / D limits, spatially aligned
//     sub/superscripts. Certified mechanism: qa/scratch_math/ (render_eq.py +
//     scratch_build.js, vision PASS 2026-10-09).
//   - Bullet 4's genuine math token "xi ∈ R^D" is likewise upgraded to a mathtext
//     PNG (build/assets/eq_042_xi_rd.png, 17pt, #000000) placed inline on the first
//     text line.
// ALIGNMENT FIX (founder feedback 2026-10-10 — EQUATION ALIGNMENT LAW): both
// equation images are placed by BASELINE (sidecar baseline_frac) and by the
// ORIGINAL frame's PIL-measured ink position (left ink edge 1.5833 in, math
// baseline 6.4306 in for the boxed equation), replacing the earlier box-center /
// line-center placement that produced the reported horizontal/vertical offsets.
// ATTEMPT-2 FIXES (judge attempt 1 FAIL):
//   (1) removed the nodes-and-arrows diagram — the curated original has NO hand-drawn
//       red sketch (judge MAJOR "invented content"; confirmed by a dedicated audit of
//       unique_slides/slide_042.jpg; spec corrected accordingly);
//   (2) bullet markers now drawn as manual "• " glyphs in per-line text boxes — the
//       rich-text bullet-on-first-run construction dropped markers on the two
//       multi-run paragraphs (bullets 1 and 4);
//   (3) body font switched to Times New Roman (serif) — two vision reads identified
//       the original body text as serif (Times-like).
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ---- Professional 2D equation embedding (certified mechanism, qa/scratch_math) ----
// Load the render_eq.py JSON sidecar; PNG was rendered at 600 dpi with the final
// font size + color baked in. Embed at EXACT sidecar size (w/h = px/600 in) — never
// rescale. Vertical placement per the EQUATION ALIGNMENT LAW (founder feedback
// 2026-10-10, scripts/17_worker_instructions.md item 5): the image's math BASELINE
// sits on the target text baseline, computed from the sidecar's baseline_frac:
//   y_image = target_baseline_in − baseline_frac × h_image_in
// ("center the image on the line" is WRONG for equations taller than the line).
// The PNG's tight bbox has an ~8 px (600 dpi) ink inset on every side (PIL-measured).
function loadEq(name) {
  const eq = JSON.parse(fs.readFileSync(
    path.join(__dirname, "assets", name + ".json"), "utf8"));
  eq.path = path.join(__dirname, "assets", path.basename(eq.path));
  return eq;
}
const EQ_INK_PAD = 8 / 600; // PNG ink inset (in): 8 px of 600-dpi tight bbox
function addEquation(slide, eq, opts) {
  // opts.x        left edge of the equation IMAGE box (inches)
  // opts.baseline target math baseline (inches) the equation must sit on
  slide.addImage({
    path: eq.path,
    x: opts.x,
    y: opts.baseline - eq.baseline_frac * eq.h_in,
    w: eq.w_in,
    h: eq.h_in,
  });
}
// Measured Times New Roman (Liberation Serif metrics) advance widths at BFONT pt,
// inches: "• Real-valued features (" = 2.226, " ): " = 0.262, "Euclidean" = 0.944.
const W_LEAD = 2.226;

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

const BG = "E8E8E8", FRAME_RED = "C00000", TITLE_RED = "CC0000",
      TEXT = "000000", BADGE_YELLOW = "FFF9C4",
      HL_YELLOW = "FFFF00", EQ_FILL = "FFFF99", EQ_BLUE = "0000CC", INK = "333333";
const FONT = "Arial", MATH = "Times New Roman", BODY = "Times New Roman";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House chrome (founder directive; overrides spec) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// Slide-number badge: numeral 42 (the number printed on the original slide image)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("42", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Title (house geometry: y 0.28, x 0.6, w 12.13, centered) ----
s.addText("K-NN: Computing the distances", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.1, align: "center", valign: "middle",
  fontSize: 32, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ---- Content box: red border, no visible fill (~22-95% H, ~5-95% W) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.67, y: 1.65, w: 12.0, h: 5.48,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.25 },
});

// ---- Bullet list (left ~60% of box, ~25-70% slide height) ----
// One text box per bullet line, manual "• " glyph prefix (attempt-2 fix: the
// rich-text bullet option dropped markers on multi-run paragraphs).
const BX = 1.05, BW = 7.8, BFONT = 17, BCOL = TEXT;

// Bullet 1 — verbatim, yellow highlight on the two phrases (spec visual element)
s.addText(
  [
    { text: "\u2022 ", options: {} },
    { text: "The K-NN algorithm requires computing distances of the ", options: {} },
    { text: "test example", options: { highlight: HL_YELLOW } },
    { text: " from ", options: {} },
    { text: "each of the training examples", options: { highlight: HL_YELLOW } },
  ],
  { x: BX, y: 2.05, w: BW, h: 0.90, valign: "top", align: "left",
    fontSize: BFONT, color: BCOL, fontFace: BODY, margin: 0 }
);

// Bullet 2 — verbatim
s.addText("\u2022 Several ways to compute distances", {
  x: BX, y: 3.02, w: BW, h: 0.45, valign: "top", align: "left",
  fontSize: BFONT, color: BCOL, fontFace: BODY, margin: 0,
});

// Bullet 3 — verbatim
s.addText("\u2022 The choice depends on the type of the features in the data", {
  x: BX, y: 3.56, w: BW, h: 0.45, valign: "top", align: "left",
  fontSize: BFONT, color: BCOL, fontFace: BODY, margin: 0,
});

// Bullet 4 — verbatim, with the genuine math token "xi ∈ R^D" upgraded to a
// professional 2D equation image (sub i, blackboard R, superscript D spatially
// set); 'Euclidean' underlined. Wraps like the original: "...commonly / used".
// Leading fragment before the equation image (measured width 2.226 in at 17pt).
s.addText("\u2022 Real-valued features (", {
  x: BX, y: 4.10, w: W_LEAD + 0.3, h: 0.40, valign: "top", align: "left",
  fontSize: BFONT, color: BCOL, fontFace: BODY, margin: 0,
});
// Inline equation image on bullet 4's first text line. EQUATION ALIGNMENT LAW:
// image baseline on the text line's baseline. The render-measured baseline of the
// "• Real-valued features (" line (bottom of the ascenderless stems, 150 dpi render)
// is 4.3333 in; sidecar baseline_frac 0.82143.
const eqXRD = loadEq("eq_042_xi_rd");           // x_i \in \mathbb{R}^D, 17pt, 000000
addEquation(s, eqXRD, { x: BX + W_LEAD + 0.03, baseline: 4.3333 });
// Trailing fragment: " ): Euclidean distance is commonly" (Euclidean underlined),
// then the original's second line "used" below.
s.addText(
  [
    { text: " ): ", options: {} },
    { text: "Euclidean", options: { underline: true } },
    { text: " distance is commonly", options: {} },
  ],
  { x: BX + W_LEAD + 0.03 + eqXRD.w_in + 0.06, y: 4.10, w: 3.55, h: 0.40,
    valign: "top", align: "left", fontSize: BFONT, color: BCOL, fontFace: BODY,
    margin: 0 }
);
s.addText("used", {
  x: BX, y: 4.42, w: 2.0, h: 0.40, valign: "top", align: "left",
  fontSize: BFONT, color: BCOL, fontFace: BODY, margin: 0,
});

// NOTE (attempt 2): NO hand-drawn sketch — the curated original frame has none.

// ---- Equation box (bottom of content box, full box width, ~72-92% slide height) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.87, y: 5.42, w: 11.6, h: 1.5,
  fill: { color: EQ_FILL }, line: { color: EQ_BLUE, width: 1 },
});

// Equation, verbatim content, PROFESSIONAL 2D rendering (founder directive
// 2026-10-09): mathtext PNG with radical vinculum over the radicand, large ∑ with
// limits m=1 below / D above, and spatially aligned sub/superscripts:
//   d(x_i, x_j) = sqrt( sum_{m=1}^{D} (x_{im} - x_{jm})^2 )
//               = sqrt( ||x_i||^2 + ||x_j||^2 - 2 x_i^T x_j )
// Rendered via qa/scratch_math/render_eq.py at 26pt #000000 (matches the original
// frame's equation ink scale: ~9in-wide linear original, box 11.6in wide),
// embedded at EXACT sidecar size, centered in the yellow box.
// EQUATION ALIGNMENT LAW (founder feedback 2026-10-10): position against the
// ORIGINAL frame's PIL-measured ink position (unique_slides/slide_042.jpg, 72 px/in),
// NOT by centering in the yellow box (the predecessor centered — visual defect).
// Original measurements: equation ink left edge = 114 px = 1.5833 in; math baseline
// (bottom of the 'd' stem in "d(x_i, x_j)", cross-checked against the parenthesis
// band 451–466 px) = 463 px = 6.4306 in. The PNG's ink starts 8 px (0.01333 in) inside
// its image box, so the image x is the target ink left minus that inset.
const eqDist = loadEq("eq_042_distance"); // full Euclidean distance chain, 26pt, 000000
addEquation(s, eqDist, {
  x: 114 / 72 - EQ_INK_PAD,   // image left so ink left edge = original's 1.5833 in
  baseline: 463 / 72,          // original equation math baseline 6.4306 in
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_042_recreated.pptx" })
  .then(() => console.log("done: videos/ml-intro/recreated_pptx/slide_042_recreated.pptx"));
