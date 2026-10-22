// Certified component — slide 035 (machine-learning/03_ridger_regression_gradient_descent)
// "Using Gradient Descent to train Linear Regression Model" + "(Problem Formulation)"
//
// Banked per the playlist-scoped component obligation (dependencies.md): slide 035 is a
// root with no same-deck dependents in slide_dependencies.json, but another deck/lecture
// may reference it; children import renderBase + per-block draws and draw only their delta.
//
// Certified: 2026-10-19 — full-slide comparison judge PASS (attempt 1, zero discrepancies;
// transcript qa/slide035/judge_attempt_1.txt) + zoomed crop certificates clean
// (qa/slide035/crop_1_title_judge.txt, crop_1_sub_judge.txt).
//
// MEASURED geometry (unique_slides/slide_035.jpg, 960x540, 1px = 1pt = 1/72in,
// JPEG smear +-2px; closed-loop converged, all deltas <=1.6 frame px):
//   L1 "Using Gradient Descent to train"  ink x 147..813 (center 480), baseline 211
//   L2 "Linear Regression Model"          ink x 217..743 (center 480), baseline 288.5 (pitch 77.5)
//   SUB "(Problem Formulation)"            ink x 271..678 (center 474.5), baseline 357
//   Arial bold; title 45pt C00000; subtitle 38.4pt 0000FF. Two single-line title boxes
//   (pixel-exact pitch, no auto-pitch divergence); lineSpacing pinned on every box
//   (54pt title / 46pt sub; LO first-baseline offset measured +1.6px/+1.1px over the
//   halfLead+ascent model — baked into the y values below).
//   The original's white mouse cursor (video artifact) is intentionally NOT drawn.
//
// House chrome is drawn ONCE here via the deck's shared primitive
// (shared_patterns/house_chrome.js) — children must not re-draw it on top.

const { drawHouseChrome } = require("../../../shared_patterns/house_chrome.js");

const px = (v) => v / 72; // frame px -> inches

const MEASURED = {
  title1: { x: 71.2, y: 166.8, w: 820, h: 70, text: "Using Gradient Descent to train", fontSize: 45, lineSpacing: 54, color: "C00000" },
  title2: { x: 71.0, y: 244.3, w: 820, h: 70, text: "Linear Regression Model", fontSize: 45, lineSpacing: 54, color: "C00000" },
  subtitle: { x: 225.0, y: 319.6, w: 500, h: 60, text: "(Problem Formulation)", fontSize: 38.4, lineSpacing: 46, color: "0000FF" },
};

function _drawTextBox(pptx, slide, spec) {
  slide.addText(spec.text, {
    x: px(spec.x), y: px(spec.y), w: px(spec.w), h: px(spec.h),
    align: "center", valign: "top", margin: 0,
    fontFace: "Arial", fontSize: spec.fontSize, bold: true, color: spec.color,
    lineSpacing: spec.lineSpacing,
  });
}

function drawTitleLine1(pptx, slide) { _drawTextBox(pptx, slide, MEASURED.title1); }
function drawTitleLine2(pptx, slide) { _drawTextBox(pptx, slide, MEASURED.title2); }
function drawSubtitle(pptx, slide) { _drawTextBox(pptx, slide, MEASURED.subtitle); }

/**
 * Render slide 035's full certified composition.
 * opts: { numeral: string|number (badge numeral; default 35 = this slide's printed
 *         number — ALWAYS pass the child's own numeral when reusing the chrome),
 *         skip: ["title1"|"title2"|"subtitle"], only: [same tokens] }
 */
function renderBase(pptx, slide, opts = {}) {
  const blocks = { title1: drawTitleLine1, title2: drawTitleLine2, subtitle: drawSubtitle };
  drawHouseChrome(pptx, slide, {
    numeral: opts.numeral !== undefined ? opts.numeral : 35,
  });
  const names = opts.only || Object.keys(blocks).filter((k) => !(opts.skip || []).includes(k));
  for (const k of names) blocks[k](pptx, slide);
}

module.exports = { renderBase, drawTitleLine1, drawTitleLine2, drawSubtitle, MEASURED };
