// components/slide_022.js — certified composition of slide 022
// ("[3] Inverse of High Dimension" / "(non-singular) Matrix"),
// ML lecture 03 (03_ridger_regression_gradient_descent). BANKED post-PASS
// (playlist-scoped component-banking obligation, 17_worker_instructions.md):
// no slide in THIS video depends on 022 (root, no children per the founder
// dependency graph — deps output 2026-10-20: 47 roots / 4 blocked, 22 unblocked),
// but a future lecture's recap/variant may import it. Certification: full-slide
// Template A judge PASS (judge_attempt_1.txt) + FOUR Template B crop
// certificates PASS (title, badge, line1, line2) on render_1.png; all three
// MINOR judge findings PIL-adjudicated as refuted (qa/slide022/
// judge_adjudication.txt). Geometry PIL-measured from
// unique_slides/slide_022.jpg (960x540, 1px = 1pt).
//
// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide (house chrome
// with numeral 22 + the two measured title lines; NO underline on this slide —
// measured: the longest solid red run in the title zone is 39 px = glyph
// strokes only). opts:
//   { numeral }         — override the badge numeral (a recap variant passes its
//                         own number; the badge numeral is ALWAYS the number
//                         printed on the VARIANT's own original frame)
//   { skip: { chrome, title } } — omit a block (a child draws only its delta)
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
// components/ sits one level deeper than build/: shared_patterns/ is at the
// video namespace root, i.e. <video>/recreated_pptx/build/components/../../../shared_patterns/
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

const RED = "C00000"; // family nominal (founder-ratified; JPEG frames read darker)
const FONT = "Arial";

const TITLE_L1 = "[3] Inverse of High Dimension";
const TITLE_L2 = "(non-singular) Matrix";

// Measured ink targets (frame px, 1px = 1pt): L1 ink x 189..726 y 235..274,
// ink center (457.5, 254.5); L2 ink x 274..652 y 325..364, ink center
// (463.0, 344.5); band-center pitch 90 px. Font: Arial Bold 38 pt (Liberation
// Sans Bold metric twin advance fit: L1 536 vs measured 538, L2 378 vs 379).
// Closed-loop TUNE values that landed every edge within ~1 px of the
// halo-corrected targets (see build/slide_022.js header + selfcheck records).
const TUNE = {
  l1: { size: 38, charSpacing: 0.09, dx: 0.5, dy: -1.9 },
  l2: { size: 38, charSpacing: null, dx: 0.5, dy: -1.9 },
};

const px = (v) => v / 72;
// Single-line boxes per line (independent placement = exact 90 px pitch
// control; sibling 020 certified pattern). Width = measured advance + ~20%
// wrap budget (boxes wrap at BOX width, not ink width).
const BOX_W = 660;
const BOX_H = 60;

// Ink centers (frame px) — a variant slide re-measures ITS OWN frame and passes
// its own values through opts.centers; defaults are slide 022's measurements.
const CENTERS = { l1: { cx: 457.5, cy: 254.5 }, l2: { cx: 463.0, cy: 344.5 } };

function renderBase(pptx, slide, opts = {}) {
  const skip = opts.skip || {};
  if (!skip.chrome) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral !== undefined ? opts.numeral : 22 });
  }
  if (!skip.title) {
    const centers = opts.centers || CENTERS;
    const c1 = centers.l1 || CENTERS.l1;
    const c2 = centers.l2 || CENTERS.l2;
    const t1 = opts.tune && opts.tune.l1 ? opts.tune.l1 : TUNE.l1;
    const t2 = opts.tune && opts.tune.l2 ? opts.tune.l2 : TUNE.l2;
    const l1opts = {
      x: px(c1.cx - BOX_W / 2 + t1.dx), y: px(c1.cy - 3 - BOX_H / 2 + t1.dy),
      w: px(BOX_W), h: px(BOX_H),
      align: "center", valign: "middle", fontSize: t1.size, bold: true,
      color: RED, fontFace: FONT, margin: 0,
    };
    if (t1.charSpacing !== null) l1opts.charSpacing = t1.charSpacing;
    slide.addText(opts.l1Text || TITLE_L1, l1opts);

    const l2opts = {
      x: px(c2.cx - BOX_W / 2 + t2.dx), y: px(c2.cy - 3 - BOX_H / 2 + t2.dy),
      w: px(BOX_W), h: px(BOX_H),
      align: "center", valign: "middle", fontSize: t2.size, bold: true,
      color: RED, fontFace: FONT, margin: 0,
    };
    if (t2.charSpacing !== null) l2opts.charSpacing = t2.charSpacing;
    slide.addText(opts.l2Text || TITLE_L2, l2opts);
  }
}

module.exports = { renderBase, TUNE, CENTERS, TITLE_L1, TITLE_L2, RED, FONT };
