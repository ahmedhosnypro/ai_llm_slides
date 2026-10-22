// components/slide_020.js — certified composition of slide 020
// ("[2] Ridge Regularization to overcome / Inverse Problem of Singular Matrix"),
// ML lecture 03 (03_ridger_regression_gradient_descent). BANKED post-PASS
// (playlist-scoped component-banking obligation, 17_worker_instructions.md):
// no slide in THIS video depends on 020 (root, no children), but a future
// lecture's recap/variant may import it. Certification: full-slide judge
// PASS (judge_attempt_1.txt) + crop certificates PASS (title, badge) on
// render_1.png; geometry PIL-measured from unique_slides/slide_020.jpg.
//
// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide (house chrome
// with numeral 20 + the two title lines + the underline bar). opts:
//   { numeral }  — override the badge numeral (a recap variant passes its own
//                  number; the badge numeral is ALWAYS the number printed on
//                  the VARIANT's own original frame)
//   { skip: { chrome, title } } — omit a block (a child draws only its delta)
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
// components/ sits one level deeper than build/: shared_patterns/ is at the
// video namespace root, i.e. <video>/recreated_pptx/build/components/../../../shared_patterns/
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

const RED = "C00000"; // family nominal (founder-ratified; JPEG frames read darker)
const FONT = "Arial";

const TITLE_L1 = "[2] Ridge Regularization to overcome";
const TITLE_L2 = "Inverse Problem of Singular Matrix";

// Measured ink targets (frame px, 1px = 1pt): L1 x 159..758 y 230..264,
// L2 x 183..744 y 310..344, underline bar rows 338..340. Closed-loop TUNE
// values that landed every edge within ~1px of the halo-corrected targets.
const TUNE = {
  l1: { size: 34, charSpacing: 0.06, dx: 0, dy: -1.4 },
  l2: { size: 34, charSpacing: null, dx: 0, dy: -1.4 },
  underline: { dx: 0, dy: 0 },
};

const px = (v) => v / 72;
const BOX_W = 720; // measured advance (~601/559) + ~20% wrap budget
const BOX_H = 60;

function renderBase(pptx, slide, opts = {}) {
  const skip = opts.skip || {};
  if (!skip.chrome) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral !== undefined ? opts.numeral : 20 });
  }
  if (!skip.title) {
    const t1 = TUNE.l1;
    const l1opts = {
      x: px(458.5 - BOX_W / 2 + t1.dx), y: px(247 - 3 - BOX_H / 2 + t1.dy),
      w: px(BOX_W), h: px(BOX_H),
      align: "center", valign: "middle", fontSize: t1.size, bold: true,
      color: RED, fontFace: FONT, margin: 0,
    };
    if (t1.charSpacing !== null) l1opts.charSpacing = t1.charSpacing;
    slide.addText(TITLE_L1, l1opts);

    const t2 = TUNE.l2;
    const l2opts = {
      x: px(463.5 - BOX_W / 2 + t2.dx), y: px(327 - 3 - BOX_H / 2 + t2.dy),
      w: px(BOX_W), h: px(BOX_H),
      align: "center", valign: "middle", fontSize: t2.size, bold: true,
      color: RED, fontFace: FONT, margin: 0,
    };
    if (t2.charSpacing !== null) l2opts.charSpacing = t2.charSpacing;
    slide.addText(TITLE_L2, l2opts);

    // Underline bar under line 2 — measured band x 183..744, rows 338..340.
    slide.addShape(pptx.ShapeType.rect, {
      x: px(183 + TUNE.underline.dx), y: px(338 + TUNE.underline.dy),
      w: px(562), h: px(3),
      fill: { color: RED },
      // no line option => no outline (house_chrome.js panel pattern)
    });
  }
}

module.exports = { renderBase, TUNE, TITLE_L1, TITLE_L2 };
