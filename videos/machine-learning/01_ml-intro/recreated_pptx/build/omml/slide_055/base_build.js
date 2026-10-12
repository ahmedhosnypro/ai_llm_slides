// Slide 55 recreation — "K-NN: Some other distance measures"
// Spec: videos/ml-intro/analysis/slide_055_final.json (validated PASS_WITH_FIXES,
// fixes applied: title normalized to 'K-NN: Some other distance measures').
// NOTE: this file previously held the PRE-CURATION old-deck slide 55 ("blank
// slide") build; that stale build was banked to
// qa/slide55/preexisting_old_deck_slide055_build.js.bak before this fresh
// new-deck build (old deck 87 -> new deck 55; the old-deck 55 build belongs to
// a different curated slide).
// House frame (founder directive 2026-10-09, OVERRIDES spec for the outer chrome):
//   background E8E8E8, red frame x:0.15 y:0.15 w:13.03 h:7.2 line C00000 w1.5,
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill FFF9C4 line FFF9C4, numeral "55"
//   (bold 18pt, color 333333) — matches the number printed on the original image.
//   Title text box y:0.28 x:0.6 w:12.13, centered.
// Spec content (verbatim, no invented facts):
//   - title "K-NN: Some other distance measures" in bold dark red (#8B0000)
//   - white slide body; rounded content box (thin dark-red #8B0000 border,
//     ~5-95% width, ~25-95% height)
//   - left column (~60%): 3 bullet groups; sub-bullets use en-dash markers;
//     'Hamming' underlined in "Use Hamming distance:"; 'Euclidean' yellow
//     FFFF00 highlight and 'Hamming' cyan 00FFFF highlight in the mixed-measures
//     sub-bullet; 'assign weights to features' blue 0000CC underlined
//   - right side: two pale-yellow FFFFCC equation boxes (thin 333333 border):
//     Hamming distance  d(x_i,x_j) = SUM_{m=1}^{D} I(x_im != x_jm)  (upper),
//     weighted distance d(x_i,x_j) = SUM_{m=1}^{D} w_m d(x_im,x_jm)   (lower)
// MATH EQUATION FORMAT RULE (founder directive 2026-10-09, binding): both equations
// are rendered in PROFESSIONAL 2D FORMAT via the certified mechanism (matplotlib
// mathtext -> tight transparent 600dpi PNG -> pptxgenjs.addImage at EXACT sidecar
// size; never rescaled). PNGs + JSON sidecars: build/assets/eq_055_hamming.* and
// build/assets/eq_055_weighted.* (rendered by qa/scratch_math/render_eq.py).
// PIL forensics of unique_slides/slide_055.jpg (960x540, 1px=1pt) verified the
// original's arrangement: a LARGE summation glyph with the limits stacked to its
// RIGHT (superscript D upper-right, subscript m=1 lower-right, same x-range) and
// a blackboard-bold indicator (𝕀) — mathtext `\sum{}_{m=1}^{D}` reproduces that
// arrangement exactly, and `\mathbb{I}` gives the blackboard indicator.
//   - bottom-left footer: very small faint gray "CS 2710 Foundations of AI [?]"
//     ([?] marker kept per spec uncertain_items).
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

const BG = "E8E8E8", FRAME_RED = "C00000", INK = "333333",
      BADGE_YELLOW = "FFF9C4", WHITE = "FFFFFF",
      TITLE_RED = "8B0000", TEXT = "000000", BLUE = "0000CC",
      HL_YELLOW = "FFFF00", HL_CYAN = "00FFFF",
      EQ_FILL = "FFFFCC", EQ_BORDER = "333333", FOOT_GRAY = "999999";
const FONT = "Arial", MATH = "Times New Roman";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House chrome (founder directive; overrides spec) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// ---- Original slide body: white (spec background #FFFFFF) ----
// (drawn BEFORE the badge so the badge stays visible on top of it)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.19, y: 0.19, w: 12.95, h: 7.12,
  fill: { color: WHITE }, line: { color: WHITE, width: 0.25 },
});

// Slide-number badge: numeral 55 (the number printed on the original slide image)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("55", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Title (house geometry: y 0.28, x 0.6, w 12.13, centered) ----
s.addText("K-NN: Some other distance measures", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.1, align: "center", valign: "middle",
  fontSize: 30, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ---- Content box: rounded rectangle, thin dark-red border, ~5-95% W, ~25-95% H ----
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.67, y: 1.875, w: 11.99, h: 5.25, rectRadius: 0.06,
  fill: { color: WHITE }, line: { color: TITLE_RED, width: 1.25 },
});

// ---- Left bullet column (~60% of content box width) ----
const BX = 1.05, BW = 6.6, BFONT = 16, BCOL = TEXT;

// Group 1, level-1 lead-in: bold dark red (spec hierarchy)
s.addText("Binary-valued features", {
  x: BX, y: 2.15, w: BW, h: 0.42, align: "left", valign: "top",
  fontSize: 17, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// Sub-bullet: en-dash marker; 'Hamming' underlined (spec typography_notes)
s.addText(
  [
    { text: "\u2013 ", options: {} },
    { text: "Use ", options: {} },
    { text: "Hamming", options: { underline: true } },
    { text: " distance:", options: {} },
  ],
  { x: BX, y: 2.62, w: BW, h: 0.42, align: "left", valign: "top",
    fontSize: BFONT, color: BCOL, fontFace: FONT, margin: 0 }
);

// Sub-bullet, verbatim (wraps to two lines at this column width)
s.addText("\u2013 Hamming distance counts the number of features where the two examples disagree", {
  x: BX, y: 3.07, w: BW, h: 0.85, align: "left", valign: "top",
  fontSize: BFONT, color: BCOL, fontFace: FONT, margin: 0,
});

// Group 2, level-1 line: bold dark-red lead-in + regular black tail (same line)
s.addText(
  [
    { text: "Mixed feature types", options: { bold: true, color: TITLE_RED } },
    { text: " (some real-valued and some binary-valued)?", options: { color: BCOL } },
  ],
  { x: BX, y: 4.20, w: BW, h: 0.85, align: "left", valign: "top",
    fontSize: BFONT, fontFace: FONT, margin: 0 }
);

s.addText("\u2013 Can use mixed distance measures", {
  x: BX, y: 5.08, w: BW, h: 0.42, align: "left", valign: "top",
  fontSize: BFONT, color: BCOL, fontFace: FONT, margin: 0,
});

// Sub-bullet with word highlights: 'Euclidean' yellow, 'Hamming' cyan (spec visual element)
s.addText(
  [
    { text: "\u2013 E.g., ", options: {} },
    { text: "Euclidean", options: { highlight: HL_YELLOW } },
    { text: " for the real part, ", options: {} },
    { text: "Hamming", options: { highlight: HL_CYAN } },
    { text: " for the binary part", options: {} },
  ],
  { x: BX, y: 5.53, w: BW, h: 0.45, align: "left", valign: "top",
    fontSize: BFONT, color: BCOL, fontFace: FONT, margin: 0 }
);

// Group 3, level-1 line: 'assign weights to features' blue + underlined (hyperlink style)
s.addText(
  [
    { text: "Can also ", options: { color: BCOL } },
    { text: "assign weights to features", options: { color: BLUE, underline: true } },
    { text: ":", options: { color: BCOL } },
  ],
  { x: BX, y: 6.08, w: BW, h: 0.42, align: "left", valign: "top",
    fontSize: BFONT, fontFace: FONT, margin: 0 }
);

// ---- Equation boxes (right side of content box, pale yellow, thin 333333 border) ----
// EQUATION ALIGNMENT LAW (founder feedback 2026-10-10, binding): both equation boxes
// and the embedded equation images are positioned against the ORIGINAL frame's
// PIL-measured geometry (unique_slides/slide_055.jpg, 960x540, 1px = 1pt), NOT at the
// judge-accepted-but-deviating positions the math rework had used. Original measurements:
//   EQ1 (Hamming) box: x 456..801pt, y 171..219pt  -> x=6.3333 y=2.3750 w=4.7917 h=0.6667
//     ink: left x=462pt (6.4167in), right x=795pt, top y=176pt, bottom y=209pt,
//     body baseline y=200pt (2.7778in; bottom of the body 'd'/'x' glyphs)
//   EQ2 (weighted) box: x 432..839pt, y 439..501pt -> x=6.0000 y=6.0972 w=5.6528 h=0.8611
//     ink: left x=438pt (6.0833in), right x=825pt, top y=445pt, bottom y=481pt,
//     body baseline y=471pt (6.5417in)
// Font sizes re-derived from the original's ink extents (the 20pt renders were ~25%
// smaller than the original's equations): EQ1 25.7pt -> ink 332.5pt wide vs original
// 333pt; EQ2 27.5pt -> ink 387.0pt wide vs original 387pt. The recreation's bullet ink
// was re-measured in the 150dpi render: NO collision with the restored original box
// positions (closest approach: wrapped sub-bullet line 1 top y=3.127in vs EQ1 box
// bottom y=3.042in; "Mixed feature types" line reaches x=6.32in but sits at y=4.26in
// where no box exists) — the bullet column is unchanged.
const EQ1_BOX = { x: 6.3333, y: 2.3750, w: 4.7917, h: 0.6667 };
const EQ2_BOX = { x: 6.0000, y: 6.0972, w: 5.6528, h: 0.8611 };

// Equation embed contract (certified in qa/scratch_math/, PASS 2026-10-09):
// load the render_eq.py JSON sidecar; place at EXACT w_in/h_in (600dpi PNGs,
// never rescaled — font size and color are baked into the ink at render time).
const ASSETS = path.join(__dirname, "assets");
function loadEq(name) {
  const eq = JSON.parse(fs.readFileSync(path.join(ASSETS, name + ".json"), "utf8"));
  eq.path = path.join(ASSETS, name + ".png"); // absolute, cwd-independent
  return eq;
}
// ALIGNED placement (EQUATION ALIGNMENT LAW): horizontal against the original's
// measured INK left edge (render_eq.py pads the tight crop with PAD_PX=8 at 600dpi
// = 0.01333in); vertical via the sidecar baseline_frac so the equation's math
// baseline lands exactly on the original's body-text baseline:
//   x = ink_left_in - 8/600;  y = baseline_in - baseline_frac * h_in.
const EQ_PAD_IN = 8 / 600;
function addEquationAt(slide, eq, inkLeftIn, baselineIn) {
  slide.addImage({
    path: eq.path,
    x: inkLeftIn - EQ_PAD_IN,
    y: baselineIn - eq.baseline_frac * eq.h_in,
    w: eq.w_in, h: eq.h_in,
  });
}

// Eq box 1 — Hamming distance (ORIGINAL geometry: upper right, level with the
// "Use Hamming distance:" sub-bullet)
s.addShape(pptx.shapes.RECTANGLE, {
  x: EQ1_BOX.x, y: EQ1_BOX.y, w: EQ1_BOX.w, h: EQ1_BOX.h,
  fill: { color: EQ_FILL }, line: { color: EQ_BORDER, width: 1.5 },
});
// d(x_i, x_j) = SUM_{m=1}^{D} I(x_im != x_jm) — professional 2D, 25.7pt, #333333.
// mathtext: 'd(x_i, x_j) = \sum{}_{m=1}^{D} \mathbb{I}(x_{im} \neq x_{jm})'
// ink left 6.4167in (462px), body baseline 2.7778in (200px) — both from the original.
addEquationAt(s, loadEq("eq_055_hamming"), 6.4167, 2.7778);

// Eq box 2 — weighted distance (ORIGINAL geometry: lower right, below the
// "Can also assign weights to features:" line)
s.addShape(pptx.shapes.RECTANGLE, {
  x: EQ2_BOX.x, y: EQ2_BOX.y, w: EQ2_BOX.w, h: EQ2_BOX.h,
  fill: { color: EQ_FILL }, line: { color: EQ_BORDER, width: 1.5 },
});
// d(x_i, x_j) = SUM_{m=1}^{D} w_m d(x_im, x_jm) — professional 2D, 27.5pt, #333333.
// mathtext: 'd(x_i, x_j) = \sum{}_{m=1}^{D} w_m d(x_{im}, x_{jm})'
// ink left 6.0833in (438px), body baseline 6.5417in (471px) — both from the original.
addEquationAt(s, loadEq("eq_055_weighted"), 6.0833, 6.5417);

// ---- Footer: very small, faint gray, bottom-left (verbatim incl. [?] marker) ----
s.addText("CS 2710 Foundations of AI [?]", {
  x: 0.35, y: 7.13, w: 4.5, h: 0.19, align: "left", valign: "middle",
  fontSize: 8, color: FOOT_GRAY, fontFace: FONT, margin: 0,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_055_recreated.pptx" })
  .then(() => console.log("done: videos/ml-intro/recreated_pptx/slide_055_recreated.pptx"));
