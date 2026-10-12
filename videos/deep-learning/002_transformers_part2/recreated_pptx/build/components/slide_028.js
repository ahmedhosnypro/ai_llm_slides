// components/slide_028.js — slide 028 certified composition
// "Sequence of 9 words / Positions are defined / as angles" (002_transformers_part2).
//
// CERTIFICATION: slide 028 passed the visual judge on 2026-10-12, attempt 1
// (qa/slide028/judge_attempt_1.txt, FINAL VERDICT: **PASS**; single-read, default
// route/images; plus corroborating dense-region crop comparisons crop_eqbox_1.txt /
// crop_bottomleft_1.txt, both PASS). This component is build/slide_028.js (the
// judge-certified build, banked as qa/slide028/build_attempt_1.js) re-expressed as
// importable blocks — 0-pixel-diff verified against the certified render
// (qa/slide028/verify_component_0diff.txt). It SUPERSEDES nothing.
//
// CONFIRMED DEPENDENTS: 29 <- 28 and 45 <- 28 (same video, slide_dependencies.json).
// Children MUST require() this module by absolute path and call
// renderBase(pptx, slide, opts) — NEVER re-derive or copy-paste this geometry.
// Block granularity: opts.skip (block names: 'title','eqbox','circle','spokes',
// 'chips','arcs'), opts.numeral (badge numeral; DEFAULT 28 — a child MUST pass its
// own, the number printed on ITS original frame), opts.wordCount (word chips at 30
// deg steps from 0 deg; default 9; arcs drawn for k < wordCount-1).
//
// COMPOSITION PROVENANCE (dependency law, edge 28 <- [27, 26]):
//   * BASE = slide 027's CERTIFIED component (components/slide_027.js) — imported,
//     never re-derived: chrome (numeral), circle, spokes, chips 0..4 (certified
//     measured centers), eqbox. Chips 5..8 use the parent's polar rule (verified
//     <=1.7pt against THIS frame, scratch/slide028/measure6_mine.json).
//   * SLIDE 026's certified component is imported per the founder edge but
//     contributes ZERO blocks (frame-diff census: none of its TIDA composition
//     appears on this frame) — expressed as P26.renderBase(only: [], chrome:false).
//   * DELTA (this slide's own, PIL-measured on unique_slides/slide_028.jpg):
//       - title line 1 text "Sequence of 9 words" (5->9) — drawn by drawTitleDelta
//         with the parent's CERTIFIED title constants (renderBase's opts.titleLines
//         is a dead option in the certified 027 component — never forwarded to
//         drawTitle — so the title block is suppressed and re-drawn here).
//       - arcs 4..7: family polyline rule (arcR 224, pads 12/1.5, 14 segs, F0C9B0
//         0.75pt); arrowheads at MEASURED centers (k=4,7 on the polar rule; k=5,6
//         hand-placed 4.5-5.2pt above it — two measurement campaigns agree <=1.5pt);
//         '+w' labels at MEASURED ink centroids (deviations from polar up to 24pt).
//       - badge numeral 28.
//   * Z-ORDER IS LOAD-BEARING (as certified): chrome -> circle -> spokes -> chips ->
//     eqbox -> title -> arcs (arcs LAST, over chips/spokes).
//   * The 27-only mouse cursor near Word 1 / circle center is a capture artifact,
//     correctly absent (judge GROUND RULES (b)/(c)).
//
// Cascade law: NEVER edit this certified component — copy-then-modify into a new
// module, or express child changes in the child's own delta.

const P27 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_027.js");
const P26 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_026.js");

const PT = 1 / 72; // slide pt -> inches (numeric factor)

// ---- certified measured delta constants (slide pt) ----
const M = P27.M; // certified family constants (single source of truth)
const CX = M.circle.cx, CY = M.circle.cy;
const RAD = Math.PI / 180;
const polar = (deg, r) => ({ x: CX + r * Math.cos(deg * RAD), y: CY - r * Math.sin(deg * RAD) });

// arrowheads k=4..7: measured bbox centers (two independent campaigns, agree <=1.5pt)
const headsMeasuredDelta = [[385.7, 185.1], [357.0, 292.0], [385.5, 405.2], [470.3, 493.2]];
// '+w' labels k=4..7: measured ink centroids (peer measure5.json, wide-window method)
const labelsMeasuredDelta = [[407.6, 122.8], [328.1, 230.0], [329.1, 356.5], [372.7, 489.2]];
const TITLE_LINES = ["Sequence of 9 words", "Positions are defined", "as angles"];

// ---- delta blocks -------------------------------------------------------------

// Title: the parent's certified title boxes/sizes with line 1 overridden to "9 words".
function drawTitleDelta(pptx, slide) {
  const T = M.title;
  for (let i = 0; i < TITLE_LINES.length && i < 3; i++) {
    const [tx, ty] = T.boxes[i];
    slide.addText(TITLE_LINES[i], {
      x: tx * PT, y: ty * PT, w: T.w[i] * PT, h: T.h * PT,
      fontFace: "Arial", fontSize: T.fontPt, bold: true, color: M.colors.title,
      align: "left", valign: "top", margin: 0,
    });
  }
}

// One delta arc k (Word k -> Word k+1, k in 4..7): family polyline rule +
// MEASURED head and label positions.
function drawArcDelta(pptx, slide, k) {
  const fromDeg = k * 30, toDeg = (k + 1) * 30;
  const a0 = fromDeg + M.arcStartPadDeg, a1 = toDeg - M.arcEndPadDeg;
  const N = M.arcSegs;
  for (let i = 0; i < N; i++) {
    const t0 = a0 + ((a1 - a0) * i) / N, t1 = a0 + ((a1 - a0) * (i + 1)) / N;
    const p1 = polar(t0, M.arcR), p2 = polar(t1, M.arcR);
    slide.addShape(pptx.ShapeType.line, {
      x: Math.min(p1.x, p2.x) * PT, y: Math.min(p1.y, p2.y) * PT,
      w: Math.abs(p2.x - p1.x) * PT, h: Math.abs(p2.y - p1.y) * PT,
      flipH: p2.x < p1.x, flipV: p2.y < p1.y,
      line: { color: M.colors.arcStroke, width: 0.75 },
    });
  }
  const ah = { x: headsMeasuredDelta[k - 4][0], y: headsMeasuredDelta[k - 4][1] };
  slide.addShape(pptx.ShapeType.triangle, {
    x: (ah.x - M.ahW / 2) * PT, y: (ah.y - M.ahH / 2) * PT,
    w: M.ahW * PT, h: M.ahH * PT, flipV: true,
    fill: { color: M.colors.arrowhead }, line: { color: M.colors.arrowhead, width: 0.5 },
  });
  const lp = { x: labelsMeasuredDelta[k - 4][0], y: labelsMeasuredDelta[k - 4][1] };
  slide.addText("+\u03c9", {
    x: (lp.x - M.labelBoxW / 2) * PT, y: (lp.y - M.labelBoxH / 2) * PT,
    w: M.labelBoxW * PT, h: M.labelBoxH * PT,
    fontFace: "Arial", fontSize: M.labelFontPt, bold: true, color: M.colors.label,
    align: "center", valign: "middle", margin: 0,
  });
}

// ---- composition ---------------------------------------------------------------
// Full certified slide-028 composition. opts:
//   numeral   — badge numeral (default 28; child MUST pass its own)
//   wordCount — word chips at 30 deg steps (default 9; arcs for k < wordCount-1)
//   skip      — array of block names to omit: 'title','eqbox','circle','spokes',
//               'chips','arcs'
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  // certified 026 import (edge 28 <- 26): zero of its blocks appear on this frame
  P26.renderBase(pptx, slide, { only: [], chrome: false });
  // certified 027 base (chrome + circle + spokes + chips + eqbox); title/arcs suppressed
  P27.renderBase(pptx, slide, {
    numeral: opts.numeral === undefined ? 28 : opts.numeral,
    wordCount: opts.wordCount === undefined ? 9 : opts.wordCount,
    skip: ["arcs", "title"],
  });
  if (!skip.has("title")) drawTitleDelta(pptx, slide);
  if (!skip.has("arcs")) {
    const arcCount = (opts.wordCount === undefined ? 9 : opts.wordCount) - 1;
    for (let k = 0; k < arcCount; k++) {
      if (k <= 3) P27.drawArc(pptx, slide, { fromDeg: k * 30, toDeg: (k + 1) * 30 });
      else if (k <= 7) drawArcDelta(pptx, slide, k);
      else P27.drawArc(pptx, slide, { fromDeg: k * 30, toDeg: (k + 1) * 30 }); // polar auto rule
    }
  }
}

module.exports = { M, TITLE_LINES, headsMeasuredDelta, labelsMeasuredDelta, drawTitleDelta, drawArcDelta, renderBase };
