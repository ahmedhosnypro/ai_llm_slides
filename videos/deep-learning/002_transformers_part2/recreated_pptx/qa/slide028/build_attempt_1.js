// build/slide_028.js — slide 028 "Sequence of 9 words / Positions are defined / as angles"
// (Deep Learning DSAI 308, 002_transformers_part2) — DEPENDENCY-GATED CHILD BUILD
// (founder directive 2026-10-11; edge 28 <- [27, 26]; slide_028_final.json PASS_WITH_FIXES).
//
// DEPENDENCY CONTRACT: slide 28 = slide 27's judge-certified composition
// (components/slide_027.js, CERTIFIED 2026-10-12 qa/slide027/judge_attempt_2.txt)
// grown from 5 words / 4 arcs to 9 words / 8 arcs — NEVER re-derived or copy-pasted —
// plus this slide's measured delta. Slide 026's certified component is imported per the
// founder edge, but a full frame-diff census (scratch/slide028/measure6_mine.py:
// diff bands ONLY at title digit cols 225-228, badge numeral cols 875-881, delta
// chips/arcs cols 325-504, and the 27-only mouse cursor cols 578-587) shows ZERO of
// 026's blocks appear on THIS frame, so nothing is drawn from it (only: [] — the
// delta law's full-removal case; the child's frame is ground truth).
//
// FRAME-SWAP NOTE (new2old_mapping.json): slide 28 was swapped mid-group by the founder
// (kept frame_01605.jpg, mid-group state) — this frame on disk is canonical. Chrome
// landmarks are pixel-identical to frame 27 (L col 58 / T row 43 / R ~895.5 / black bar
// rows 519+; h-axis cols 57..902 and v-axis identical), so the parent's certified
// slide-point geometry (fx = 18.63 + 0.96123*slide_x ; fy = 0.95556*slide_y) lands 1:1.
//
// MEASURED DELTA (scratch/slide028/measure6_mine.py + peer campaigns measure4/5.json,
// PIL on unique_slides/slide_028.jpg, cross-verified by two independent workers):
//   * title line 1 text "Sequence of 5 words" -> "Sequence of 9 words" (same certified
//     box/size; diff band confined to the digit glyph cols 225-228).
//   * chips k=5..8: the component's polar rule (chipR 182.5 @ k*30 deg) verified against
//     this frame's measured chip centers to <=1.7pt (measure6_mine.json) — no overrides.
//   * arcs k=4..7: polyline at the family rule (arcR 224, pads 12/1.5, 14 segs,
//     F0C9B0 0.75pt — visually confirmed present on this frame incl. arc 7 bottom-left).
//   * arrowheads k=4..7 (unrotated down-triangles per the family convention), MEASURED
//     slide-pt bbox centers: k=4 (385.7,185.1) [on the polar rule], k=5 (357.0,292.0)
//     and k=6 (385.5,405.2) [hand-placed 4.5-5.2pt ABOVE the polar rule — both
//     measurement campaigns agree within 1.5pt], k=7 (470.3,493.2) [on the rule].
//   * '+w' labels k=4..7 (Arial bold 15pt CC0000, 30x16pt centered box), MEASURED ink
//     centroids (peer measure5.json wide-window method, compatible with the certified
//     k=0..3 convention within 2pt): (407.6,122.8) (328.1,230.0) (329.1,356.5)
//     (372.7,489.2) — hand-placed by the professor, deviations from the polar rule up
//     to 24pt, so the polar auto-rule is NOT used for the delta labels.
//   * badge numeral 28 = the number printed on THIS original frame.
//   * mouse cursor near Word 1 (frame ~ (735,215)) is a screen-recording artifact —
//     correctly omitted (judge GROUND RULES (c)).
//
// LAWS honored: playlist chrome drawn ONCE inside the certified component (numeral 28);
// verbatim text; margin:0 + explicit fontFace everywhere; certified components NOT
// edited; single-version deliverable slide_028_recreated.pptx; no '#' in hex.
// CONFIRMED DEPENDENTS: 29 <- 28, 45 <- 28 (component must be banked at certification).

const path = require("path");
const pptxgen = require("pptxgenjs");
const P27 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_027.js");
const P26 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_026.js");

const IN = (pt) => pt / 72;
const PT = 1 / 72; // slide pt -> inches (NUMERIC factor — the component's PX equivalent)

// ---- measured delta constants (slide pt) ------------------------------------
const M = P27.M; // certified family constants (single source of truth)
const CX = M.circle.cx, CY = M.circle.cy;
const RAD = Math.PI / 180;
const polar = (deg, r) => ({ x: CX + r * Math.cos(deg * RAD), y: CY - r * Math.sin(deg * RAD) });

// arrowheads k=4..7: measured bbox centers (two independent campaigns, agree <=1.5pt)
const headsMeasuredDelta = [[385.7, 185.1], [357.0, 292.0], [385.5, 405.2], [470.3, 493.2]];
// '+w' labels k=4..7: measured ink centroids (peer measure5.json, wide-window)
const labelsMeasuredDelta = [[407.6, 122.8], [328.1, 230.0], [329.1, 356.5], [372.7, 489.2]];

// ---- one delta arc k (Word k -> Word k+1, k>=4): family polyline rule +
//      MEASURED head and label positions ---------------------------------------
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

// ---- title (delta: line-1 text) ------------------------------------------------
// renderBase does NOT forward opts.titleLines to drawTitle (dead option in the
// certified component — measured: render_1 drew the default "Sequence of 5 words"),
// and certified components are never edited. So the child skips the title block and
// re-draws the three boxes with the COMPONENT'S OWN certified constants (M.title),
// overriding only line 1's text — geometry byte-identical to drawTitle.
function drawTitleDelta(pptx, slide) {
  const T = M.title;
  const lines = ["Sequence of 9 words", "Positions are defined", "as angles"];
  for (let i = 0; i < lines.length && i < 3; i++) {
    const [tx, ty] = T.boxes[i];
    slide.addText(lines[i], {
      x: tx * PT, y: ty * PT, w: T.w[i] * PT, h: T.h * PT,
      fontFace: "Arial", fontSize: T.fontPt, bold: true, color: M.colors.title,
      align: "left", valign: "top", margin: 0,
    });
  }
}

// ---- compose ------------------------------------------------------------------
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const pptx = pres;
const slide = pres.addSlide();

// 1. certified 026 component (edge 28 <- 26): imported per contract; THIS frame shows
//    zero of its blocks (measured frame-diff census) — full-removal delta, nothing drawn.
P26.renderBase(pptx, slide, { only: [], chrome: false });

// 2. certified 027 base grown to THIS frame: 9 chips (0..4 certified measured centers,
//    5..8 polar rule verified <=1.7pt), chrome with numeral 28. Arcs + title suppressed
//    here (titleLines is a dead option in renderBase — see drawTitleDelta above).
P27.renderBase(pptx, slide, {
  numeral: 28,
  wordCount: 9,
  skip: ["arcs", "title"],
});
drawTitleDelta(pptx, slide);

// 3. arcs 0..3 — certified measured component blocks (pixel-identical frames, verified)
for (let k = 0; k <= 3; k++) {
  P27.drawArc(pptx, slide, { fromDeg: k * 30, toDeg: (k + 1) * 30 });
}
// 4. arcs 4..7 — THIS slide's measured delta
for (let k = 4; k <= 7; k++) {
  drawArcDelta(pptx, slide, k);
}

pres.writeFile({ fileName: path.join(__dirname, "..", "slide_028_recreated.pptx") })
  .then(() => console.log("WROTE slide_028_recreated.pptx"));
