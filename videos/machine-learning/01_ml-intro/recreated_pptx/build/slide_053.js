// Slide 053 recreation — "Example:  Distance without Normalization"
// FOUNDER-DEFECT FIX build (2026-10-10). Prior certified build banked at
// qa/slide053/build_pre_founder_fix.js; confirmation evidence and measured
// before/after numbers in qa/slide053/founder_defect_check/ (DEFECT_REPORT.md).
//
// Founder defects fixed (all geometry PIL-measured on the original 960x540 frame,
// 1px = 1pt; measured bands include JPEG AA, ~+/-1pt):
//   (a) Vector value lines' inter-line spacing now matches the original:
//       line1 digit ink y219-237, line2 y244-262 (center pitch 25pt, was 24pt with
//       per-line paren glyphs 5.3pt apart). Digit font 23pt (orig cap ~16-17).
//   (b) Tall thin parentheses now wrap BOTH value lines (orig paren ink y212.5-266.5,
//       h54; grid parens; test paren h58 y212-270), with the value text band
//       centered inside (orig top gap ~6.5pt / bottom gap ~4.5pt). Round 2
//       (2026-10-10 founder defect: LO renders the earlier ARC-preset parens as
//       double-stroked blobs with inner curls top+bottom): implemented as ONE
//       smooth quadratic-Bezier stroke per delimiter, 600dpi transparent PNG
//       (S=3.0/4.0/3.5pt, D=2.5pt — see gen_parens53.py; a large-font "(" text
//       glyph is far too fat/wide: Arial delta/H=0.154 vs original 0.04, tips
//       would collide with the digits — measured).
//       Result-box vector (7/100) given the same tall-paren treatment (orig pitch 27,
//       paren h57, top/bottom gaps ~8pt), scaled into the existing judged-pass box.
//   (c) Legend items (Red/Blue/Green Class, Test headers) re-placed at the original's
//       measured ink positions (centers x 250/455.5/690.5/850, y-centers
//       193/192.5/191.5/191) and size 14pt bold (orig cap ~10pt; was 18pt at y156).
//   Row labels "Weight (KG)" / "Length (cm)" aligned to their value lines at the
//       original's measured positions (ink y224-239 / y246-260, x85) — in the old
//       build "Length (cm)" sat ~20pt BELOW line2.
//   "Feature Vector  of bars:" header moved to the original's measured position
//       (ink top y152, ink left x83) so the header->grid gap matches (was leaving a
//       74pt hole after the grid moved to the original's absolute y).
// House frame/badge/title geometry unchanged (founder directive 2026-10-09).
// Spec content verbatim (analysis/slide_053_final.json, PASS_WITH_FIXES; (7,100)
// result vector kept verbatim — validation.uncertain_items, never corrected).
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in = 960 x 540 pt

const BG = "E8E8E8", FRAME_RED = "C00000", INK = "333333",
      BADGE_YELLOW = "FFF9C4", CONTENT_BG = "FFFFFF",
      BOX_RED = "A00000", TITLE_RED = "B00020",
      RED = "C00000", BLUE = "0000CC", GREEN = "2E8B22", BLACK = "000000",
      HILITE_YELLOW = "E8D44D", RESULT_BG = "F5F5DC";
const FONT = "Arial";
const IN = 1 / 72; // pt -> in

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House chrome (founder directive; overrides spec for outer chrome) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("53", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Title (house geometry; spec color/underline) ----
s.addText([
  { text: "Example:  Distance ", options: { underline: false } },
  { text: "without", options: { underline: true } },
  { text: " Normalization", options: { underline: false } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "middle",
  fontSize: 30, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ---- Content frame (spec: thin dark-red A00000 border, white fill) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.55, y: 1.45, w: 12.23, h: 5.7,
  fill: { color: CONTENT_BG }, line: { color: BOX_RED, width: 1.5 },
});

// ---- Section header (verbatim double space) — original ink x83, y152-171 ----
s.addText("Feature Vector  of bars:", {
  x: 81.4 * IN, y: 146.24 * IN, w: 6.0, h: 0.45, align: "left", valign: "top",
  fontSize: 22, bold: false, color: BLACK, fontFace: FONT, margin: 0,
});

// ---- Legend / class headers — original measured ink positions, 14pt bold ----
// ink center y = box_y + 8.48 (cal: off_top 3.2 + cap/2 5.28 @14pt bold)
const LEGEND = [
  { text: "Red Class",   color: RED,   cx: 250.0, cy: 193.0 },
  { text: "Blue Class",  color: BLUE,  cx: 455.5, cy: 192.5 },
  { text: "Green Class", color: GREEN, cx: 690.5, cy: 191.5 },
  { text: "Test",        color: BLACK, cx: 850.0, cy: 191.0 },
];
LEGEND.forEach((L) => {
  s.addText(L.text, {
    x: (L.cx - 57.6) * IN, y: (L.cy - 8.48) * IN, w: 1.6, h: 0.3,
    align: "center", valign: "top",
    fontSize: 14, bold: true, color: L.color, fontFace: FONT, margin: 0,
  });
});

// ---- Vector grid: tall thin parens — FOUNDER PAREN FIX round 2 (2026-10-10) ----
// The attempt-4..6 parens used ARC preset shapes with 210-deg sweeps
// (angleRange [75,285] LP / [255,105] RP); LibreOffice renders those as a
// DOUBLE-STROKED blob with merged caps top and bottom — the founder's "inner
// curve on top and bottom, garbage" defect (final-deck review 2026-10-10).
// Evidence: qa/slide053/paren_zoom/{grid_tight,callout}_defect.txt (zoomed
// vision comparisons, both FAIL: "blade/leaf curvature", "pointed/teardrop
// caps", "abrupt inward step/joint at midheight", "extra black bump") and
// qa/slide053/measure_parens_attempt7.out (PIL: two parallel strokes + caps).
//
// Rebuilt per patterns.md P3: ONE smooth quadratic-Bezier stroke per
// delimiter, pre-rendered at 600 dpi transparent PNG by
// build/gen_parens53.py (assets + sidecar JSONs in build/assets/parens53/):
//   - curve: tip(x_t,y0) ctrl(2*x_bulge-x_t, ymid) tip(x_t,y1) — single
//     monotonic bow (hooks geometrically impossible), near-vertical
//     terminals (~10.5deg off vertical, matches the original's profile),
//     bulge at exact mid-height, round caps.
//   - D=2.5pt bulge-to-tip pull; stroke S=3.0pt grid / 4.0pt test col /
//     3.5pt callout (original measured: grid 2-4px washed, test 4-6px,
//     callout 3-4px; original D ~ 2-2.5pt — near-straight tall thin parens).
//   - ink bands UNCHANGED from certified attempt 6: grid y212.5-266.5 (h54),
//     test y212-270 (h58), callout y446-503 (h57); bulge ink edges land on
//     the same anchors (lp / rp per column, callout 601/646).
// Each PNG is placed from its MEASURED sidecar ink bbox so ink lands exactly
// on the anchor, embedded at EXACT size (w = px/600 in, never rescaled).
//
// LINE-SPACING AUDIT (founder law 2026-10-10, checklist item 8): this slide
// has ZERO multi-line text boxes — title/header/legend/labels/caption/
// distance rows/badge are single-line, and the two-line value stacks are
// TWO single-line boxes at explicit y (212.9 / 237.9 grid, 447.9 / 472.9
// callout) so the 25pt line pitch is pinned by construction, not by
// renderer auto-pitch. Self-check asserts the rendered band pitch == 25pt.
const fs = require("fs");
const PAREN_DIR = "videos/ml-intro/recreated_pptx/build/assets/parens53";
function parenImg(side, inkH, hex, anchorEdgeX, inkTopTarget) {
  // side "lp": anchor = ink LEFT edge (bulge outer-left). "rp": ink RIGHT edge.
  const base = `${PAREN_DIR}/paren_${side}_${inkH}_${hex}`;
  const sc = JSON.parse(fs.readFileSync(base + ".json", "utf8"));
  const ppp = 72 / 600; // pt per rendered px
  const inkAnchorPt = (side === "lp" ? sc.ink_left_px : sc.ink_right_px) * ppp;
  const x = anchorEdgeX - inkAnchorPt;
  const y = inkTopTarget - sc.ink_top_px * ppp;
  s.addImage({ path: base + ".png", x: x * IN, y: y * IN, w: sc.px_w / 600, h: sc.px_h / 600 });
}
const GRID = [
  { color: RED,   lp: 172, rp: 217, ctr: 193.75, v: [2, 100],  test: false },
  { color: RED,   lp: 232, rp: 276, ctr: 253.75, v: [3, 150],  test: false },
  { color: RED,   lp: 291, rp: 336, ctr: 313.00, v: [4, 200],  test: false },
  { color: BLUE,  lp: 383, rp: 429, ctr: 406.25, v: [7, 150],  test: false },
  { color: BLUE,  lp: 443, rp: 488, ctr: 465.25, v: [8, 200],  test: false },
  { color: BLUE,  lp: 503, rp: 549, ctr: 525.25, v: [9, 250],  test: false },
  { color: GREEN, lp: 611, rp: 657, ctr: 634.00, v: [12, 150], test: false },
  { color: GREEN, lp: 672, rp: 717, ctr: 694.00, v: [13, 250], test: false },
  { color: GREEN, lp: 731, rp: 777, ctr: 753.75, v: [14, 300], test: false },
  { color: BLACK, lp: 830, rp: 876, ctr: 852.00, v: [7, 120],  test: true  },
];
GRID.forEach((g) => {
  const inkTop = g.test ? 212 : 212.5;
  const inkH = g.test ? 58 : 54;
  // left "(" then right ")" — transparent PNGs, drawn before the digits
  parenImg("lp", inkH, g.color, g.lp, inkTop);
  parenImg("rp", inkH, g.color, g.rp, inkTop);
  // value lines (top = Weight, bottom = Length), centered on the column axis
  s.addText(String(g.v[0]), {
    x: (g.ctr - 30) * IN, y: 212.9 * IN, w: 60 * IN, h: 26 * IN,
    align: "center", valign: "top",
    fontSize: 23, color: g.color, fontFace: FONT, margin: 0,
  });
  s.addText(String(g.v[1]), {
    x: (g.ctr - 30) * IN, y: 237.9 * IN, w: 60 * IN, h: 26 * IN,
    align: "center", valign: "top",
    fontSize: 23, color: g.color, fontFace: FONT, margin: 0,
  });
});

// ---- Row labels at the left of the grid, aligned to the two value lines ----
// Original ink: "Weight (KG)" y224-239, "Length (cm)" y246-260, left edge x85
// (15pt bold, off_top 3.6).
s.addText("Weight (KG)", {
  x: 84.8 * IN, y: 220.4 * IN, w: 1.25, h: 0.28, align: "left", valign: "top",
  fontSize: 15, bold: false, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("Length (cm)", {
  x: 84.8 * IN, y: 242.4 * IN, w: 1.25, h: 0.28, align: "left", valign: "top",
  fontSize: 15, bold: false, color: BLACK, fontFace: FONT, margin: 0,
});

// ---- Caption — judge-4 MAJOR fix (left-align) + judge-5 weight fix (bold:
// original caption ink is ~1.3x denser than its regular-weight label
// calibration -> bold, like judge-5 read). Measured ink x78-408, y283-294;
// 12.5pt bold Arial = 337pt wide / 11.6pt band (orig ~330pt / ~12).
s.addText("Squared distance between each vector and test vector", {
  x: 77.5 * IN, y: 279.6 * IN, w: 5.5, h: 0.3, align: "left", valign: "top",
  fontSize: 12.5, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// ---- Squared-distance groups (X layout byte-identical to certified build —
// judge-4 passed positions/parens/circle; only Y moves per judge-4 issue 5:
// original digit ink y307-322, i.e. ~13pt below the caption band) ----
const DIST_Y = 4.19, DIST_H = 0.5, DIST_PT = 20;
// Yellow circle around 425 — drawn BEFORE the 425 text so the text sits on top.
// Original bbox ink x177-224 y299-334; circle center sits ~2pt below the digit
// line center -> box y 296.7pt. X extent unchanged (certified, passed twice).
s.addShape(pptx.shapes.OVAL, {
  x: 2.46, y: 4.1528, w: 0.64, h: 0.486,
  fill: { color: CONTENT_BG }, line: { color: HILITE_YELLOW, width: 2.25 },
});
const redPieces = [
  ["(", 2.35, 0.2], ["425", 2.55, 0.55], ["916", 3.15, 0.55],
  ["6409", 3.75, 0.7], [")", 4.38, 0.2],
];
redPieces.forEach(([t, x, w]) => {
  s.addText(t, {
    x, y: DIST_Y, w, h: DIST_H, align: "left", valign: "top",
    fontSize: DIST_PT, color: RED, fontFace: FONT, margin: 0,
  });
});
s.addText("(900   6401   16904)", {
  x: 5.6, y: DIST_Y, w: 2.7, h: DIST_H, align: "left", valign: "top",
  fontSize: DIST_PT, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("(925   16936   32449)", {
  x: 8.6, y: DIST_Y, w: 2.9, h: DIST_H, align: "left", valign: "top",
  fontSize: DIST_PT, color: GREEN, fontFace: FONT, margin: 0,
});

// ---- Result box — rebuilt per judge-4 (MAJOR: parens must span both value
// lines; MINOR: compact square-cornered box at the original's geometry).
// Original measured (960x540 frame, 1px=1pt): pale F5F5DC fill x584-895,
// y439-511, square corners, no dark border (edge pixels are the pale fill
// boundary, lum 215-246); tall paren ink y446-503 (h57), LP stroke x601-606,
// RP stroke x640-645; digits "7" ink y454-469, "100" ink y479-495 (23pt
// regular, pitch ~25, paren top/bottom gaps 8/8 — optically centered);
// "Belongs to   Red Class" ink y468-485, x672-844 (~15pt bold; "Red Class"
// red bold). Spec content verbatim ((7,100) is an uncertain item, never
// corrected).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 584 * IN, y: 439 * IN, w: 311 * IN, h: 72 * IN,
  fill: { color: RESULT_BG }, line: { color: RESULT_BG, width: 0.5 },
});
// Tall parens wrapping BOTH lines — FOUNDER PAREN FIX round 2: same smooth
// Bezier-PNG construction as the grid (build/gen_parens53.py, S=3.5pt,
// D=2.5pt, ink y446-503 h57), landing the measured sidecar ink on the same
// certified anchors (LP bulge ink-left x601, RP bulge ink-right x646).
parenImg("lp", 57, "000000", 601, 446);
parenImg("rp", 57, "000000", 646, 446);
// Vertical vector (7 over 100) — verbatim per spec (uncertain item, not corrected).
// judge-5 MAJOR fix: the attempt-5 text boxes were w:30pt but Arial "100" needs
// ~38pt of advance -> LibreOffice WRAPPED the final "0" onto a third line below
// the parens/box. Boxes now 46pt wide (centered on cx 623, over the arcs — text
// draws on top) so "100" renders as ONE value. Digits 22pt regular (orig ink
// h15.5-16 -> em ~21.6; 23pt was a size overshoot that also forced paren contact).
// off_top 22pt = 6.1 -> line1 box 447.9 (ink 454), line2 box 472.9 (ink 479).
s.addText("7", {
  x: 600 * IN, y: 447.9 * IN, w: 46 * IN, h: 26 * IN,
  align: "center", valign: "top",
  fontSize: 22, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("100", {
  x: 600 * IN, y: 472.9 * IN, w: 46 * IN, h: 26 * IN,
  align: "center", valign: "top",
  fontSize: 22, color: BLACK, fontFace: FONT, margin: 0,
});
// "Belongs to   Red Class" — triple space verbatim; "Red Class" in bold red.
// (15pt bold: full phrase = 11.39em = 171pt = original ink width 172pt.)
s.addText([
  { text: "Belongs to   ", options: { color: BLACK } },
  { text: "Red Class", options: { color: RED } },
], {
  x: 670.5 * IN, y: 464.4 * IN, w: 2.55, h: 0.35, align: "left", valign: "top",
  fontSize: 15, bold: true, fontFace: FONT, margin: 0,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_053_recreated.pptx" })
  .then(() => console.log("written: videos/ml-intro/recreated_pptx/slide_053_recreated.pptx"));
