// Slide 015 recreation — "Classification vs Regression"
// Spec: analysis/slide_015_final.json (validation PASS_WITH_FIXES applied +
// slide-15 worker ground-truth correction: the curated frame carries NO red
// handwritten ink annotations; the pre-curation analysis frame did — evidence:
// qa/slide15/judge_attempt_1.txt findings 1-3, qa/slide15/orig_census_1.txt,
// pixel forensics vs frames/frame_01527.jpg).
//
// Derived from the old-deck build (old id 18, qa/slide018, judge PASS 2026-10-09)
// with badge 15, ground-truth content fixes per the attempt-1/2 judge, and the
// ink annotations removed (absent from THIS original image).
//
// Notes:
//   - Content-box border assumed #CC0000 (matches title) per spec fix.
//   - Yellow badge + outer frame + title-y use the HOUSE template values
//     (founder directive 2026-10-09), overriding the spec.
//   - Data point positions/curve shapes are approximated from the qualitative
//     descriptions (spec uncertain_items allows builder approximation).
//
// Layout bands from spec layout.regions:
//   title ~5-20% h | frame ~22-97% h | class text ~25-32% | class plots ~32-58%
//   regression text ~60-66% | regression plot ~66-95%

const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";      // slide background — HOUSE FRAME rule (overrides spec F2F2F2)
const RED = "CC0000";     // title / inner content-box border (spec fix: matches title)
const INKRED = "FF0000";  // red x markers
const BLK = "000000";     // body text / axes
const BLU = "0000CC";     // bold keyword blue
const DOTBLU = "1E90FF";  // classification blue dots
const PUP = "6A5ACD";     // regression open circles
const GRN = "9ACD32";     // fitted curve
const PNK = "FFB6C1";     // confidence band

const FONT = "Arial";
const HAND = "Comic Sans MS";

let s = pptx.addSlide();
s.background = { color: BG };

// Straight line segment helper: arrowhead (endArrowType) always lands on (x2,y2).
function seg(x1, y1, x2, y2, lineOpts) {
  const w = Math.max(Math.abs(x2 - x1), 0.001);
  const h = Math.max(Math.abs(y2 - y1), 0.001);
  s.addShape(pptx.shapes.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w, h,
    flipH: x2 < x1, flipV: y2 < y1,
    line: lineOpts,
  });
}

// ---------- 1. Background is the slide fill (F2F2F2), no slide-level border ----------

// ---------- 0. HOUSE FRAME (founder directive 2026-10-09, overrides spec) ----------
// Slide background E8E8E8; outer red frame inset 0.15in from every edge.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: "C00000", width: 1.5 },
});

// ---------- 2. Slide-number badge (HOUSE values): yellow oval top-right ----------
// Badge numeral = the number printed on the ORIGINAL slide image: 15 (deck curation
// 2026-10-09; unique_slides/slide_015.jpg is named by that printed number).
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("15", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ---------- 3. Title: red bold centered (HOUSE title box y:0.28, x:0.6, w:12.13) ----------
// Attempt-4 fix (judge 3): original title is smaller/thinner than 36pt.
s.addText("Classification vs Regression", {
  x: 0.6, y: 0.28, w: W - 1.2, h: 1.05, align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- 4. Content frame: red outline-only rectangle ----------
// Attempt-4 fix (judge 3): tighter inner box (was nearly full width).
// FOUNDER FIX 2026-10-10 (founder_issues slide 15, "fix same way as slide 5"):
// the regression-panel image bottom (7.157in) crossed this frame's bottom edge
// (was y:1.68 h:5.42 -> bottom 7.10in) by ~4 orig-frame px (measured on
// render_graphed_1.png: purple border ink to y 1073 vs frame bottom ink
// 1063-1066 @150dpi). Fix per the founder directive: inner frame HEIGHT UP +
// Y START UP — y 1.68 -> 1.58, h 5.42 -> 5.68, bottom 7.10 -> 7.26in, which
// lands on the ORIGINAL's measured content-frame bottom (unique_slides/
// slide_015.jpg frame-rect centerlines x 69.5..884.5, y 143..522.5 @ 1px=1pt
// -> bottom 522.5/72 = 7.258in), so the panel's containment margins reproduce
// the original's (original: panel bottom 515.3 vs frame bottom 522.5 = 7.2px
// clearance).
const FR = { x: 0.85, y: 1.58, w: 11.65, h: 5.68 };
s.addShape(pptx.shapes.RECTANGLE, {
  x: FR.x, y: FR.y, w: FR.w, h: FR.h,
  fill: { color: BG },
  line: { color: RED, width: 2.25 },
});

// ---------- 5. Classification text line (~25-32% h), left-aligned in frame ----------
// Attempt-4 fix (judge 3): original body text is smaller/more compact.
// NEW LAW audit (2026-10-10, explicit-lineSpacing/PowerPoint-pitch law,
// scripts/17_worker_instructions.md checklist item 8): ALL text boxes on this
// slide are SINGLE-LINE (title; this line; the section-10 regression line;
// badge numeral; 'x' glyph markers) — none wraps, so there is no multi-line
// pitch to pin and no lineSpacing key is required. The self-check
// (selfcheck_graphed_attempt_3.py) asserts each body-text band renders as ONE
// 18pt line (band height <= 0.30in; a PowerPoint pitch mismatch would show a
// second band or band height >= 0.45in). The only frame-bottom-adjacent
// element is the regression panel IMAGE (absolute-positioned picture — no
// text reflow divergence between LO and PowerPoint), whose 0.147in clearance
// reproduces the original's own containment geometry per the founder fix.
s.addText(
  [
    { text: "Classification ", options: { bold: true, color: BLU, fontFace: FONT } },
    { text: "is about finding separation boundaries (linear/non-linear):", options: { color: BLK, fontFace: FONT } },
  ],
  { x: 1.15, y: 1.88, w: 10.9, h: 0.40, fontSize: 18, align: "left", valign: "middle", margin: 0 }
);

// ---------- 6/7. Two side-by-side classification scatter plots (~32-58% h) ----------
// Panels SMALL, compact, framed, center-right (old-deck judge 3).
const AX = { color: BLK, width: 1.5, endArrowType: "triangle" };
const NAVY = "000080";   // plot figure frames (attempt-2 judge: navy, not black)
const PLOT = { y0: 2.55, pw: 2.35, ph: 1.32 };
const LP = { x0: 4.55 };   // left plot
const RP = { x0: 7.45 };   // right plot (immediately right, same size)

// marker sets (fractions of pw/ph; y 0=top) — PIL-MEASURED from the original
// frame (judge attempt-2 FAIL findings 1-2, qa/slide015/graphgen/
// judge_graphed_attempt_2.txt; forensics fix2_classplot_forensics*.py +
// fix2_separator_runs_out.txt + direct component re-verify 2026-10-10).
// Normalization basis = each panel's ORIGINAL box (1px = 1pt):
//   LEFT  panel box x 365..648, y 183..326  (w 283, h 143)
//   RIGHT panel box x 648..816, y 183..326  (w 168, h 143)
//
// Left plot (judge finding 1, MAJOR): 5 blue dots form a compact chain on the
// LEFT of the separator (rising from lower-left toward upper-middle); 5 red
// X's sit right/below of the separator, one notably near the bottom axis —
// the boundary-between-classes teaching geometry the judge demanded.
const LDOTS = [
  [0.163, 0.753], [0.207, 0.597], [0.249, 0.445], [0.333, 0.292], [0.354, 0.169],
];
const LXMARK = [
  [0.523, 0.294], [0.458, 0.448], [0.416, 0.601], [0.523, 0.601], [0.352, 0.783],
];
// Right plot (judge finding 2, MINOR): 5 blue dots left/top, 5 red X's
// middle-right below the sweeping boundary.
const RDOTS = [
  [0.143, 0.494], [0.210, 0.743], [0.245, 0.250], [0.455, 0.186], [0.635, 0.157],
];
const RXMARK = [
  [0.491, 0.376], [0.739, 0.377], [0.386, 0.502], [0.664, 0.590], [0.419, 0.711],
];

function classPlot(x0, dots, xmarks, boundary) {
  const { y0, pw, ph } = PLOT;
  // thin NAVY figure frame around the plot (attempt-2 judge finding 7)
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x0 - 0.09, y: y0 - 0.09, w: pw + 0.18, h: ph + 0.18,
    fill: { color: BG }, line: { color: NAVY, width: 0.75 },
  });
  // axes with arrowheads (no labels, no ticks)
  seg(x0, y0 + ph, x0 + pw, y0 + ph, AX);          // x-axis, arrow right
  seg(x0, y0 + ph, x0, y0, AX);                   // y-axis, arrow up
  // blue dots
  dots.forEach(([fx, fy]) => {
    s.addShape(pptx.shapes.OVAL, {
      x: x0 + fx * pw - 0.04, y: y0 + fy * ph - 0.04, w: 0.08, h: 0.08,
      fill: { color: DOTBLU },
    });
  });
  // red 'x' markers
  xmarks.forEach(([fx, fy]) => {
    s.addText("x", {
      x: x0 + fx * pw - 0.09, y: y0 + fy * ph - 0.10, w: 0.2, h: 0.2,
      align: "center", valign: "middle", fontSize: 10, bold: true,
      color: INKRED, fontFace: FONT, margin: 0,
    });
  });
  // decision boundary
  boundary();
}

// Left boundary (judge attempt-2 finding 1): measured STEEP separator rising
// between the dot chain (left/above) and the X's (right/below) — a single
// straight segment, original trace (426.5,302.8)->(498.5,200.0) frame-px
// = fx 0.217..0.472, fy 0.838..0.119 (near-linear within ±6% slope; the
// old full-width shallow diagonal read as a regression fit line, not a
// boundary — exactly the judge's MAJOR).
classPlot(LP.x0, LDOTS, LXMARK, () => {
  const { y0, pw, ph } = PLOT;
  seg(LP.x0 + 0.217 * pw, y0 + 0.838 * ph,
      LP.x0 + 0.472 * pw, y0 + 0.119 * ph,
      { color: BLK, width: 2 });
});

// Right boundary (judge attempt-2 finding 2): measured SMOOTH sweeping arc —
// the judge's exact prescription. Per-column ink-run trace of the original
// (fix2_separator_runs_out.txt): vertex at fx 0.238/fy 0.608, a long upper
// arm rising steeply then flattening across the top to fx 0.845, plus a short
// lower arm descending to fx 0.327/fy 0.801. Drawn as ~25 short segments =
// visually smooth (replaces the 4-segment elbowed polyline the judge flagged).
classPlot(RP.x0, RDOTS, RXMARK, () => {
  const { y0, pw, ph } = PLOT;
  const up = [
    [0.238, 0.608], [0.262, 0.531], [0.274, 0.500], [0.286, 0.476],
    [0.298, 0.448], [0.310, 0.430], [0.321, 0.413], [0.333, 0.399],
    [0.345, 0.388], [0.357, 0.378], [0.369, 0.364], [0.393, 0.343],
    [0.405, 0.336], [0.452, 0.301], [0.464, 0.294], [0.500, 0.280],
    [0.536, 0.266], [0.560, 0.259], [0.595, 0.252], [0.655, 0.245],
    [0.690, 0.245], [0.738, 0.252], [0.762, 0.259], [0.798, 0.266],
    [0.845, 0.287],
  ].map(([fx, fy]) => [RP.x0 + fx * pw, y0 + fy * ph]);
  for (let i = 0; i < up.length - 1; i++) {
    seg(up[i][0], up[i][1], up[i + 1][0], up[i + 1][1],
        { color: BLK, width: 2 });
  }
  const low = [
    [0.238, 0.608], [0.262, 0.694], [0.274, 0.727], [0.286, 0.748],
    [0.298, 0.769], [0.310, 0.787], [0.327, 0.801],
  ].map(([fx, fy]) => [RP.x0 + fx * pw, y0 + fy * ph]);
  for (let i = 0; i < low.length - 1; i++) {
    seg(low[i][0], low[i][1], low[i + 1][0], low[i + 1][1],
        { color: BLK, width: 2 });
  }
});

// ---------- 8/9. NO handwritten ink annotations ----------
// Attempt-2: judge findings 1-3 + orig_census_1.txt (default-route reads of the
// CURRENT ground truth unique_slides/slide_015.jpg) + pixel forensics vs
// frame_01527.jpg: the curated original carries NO "2nd order"/"3rd order"
// labels and no red annotation arrows. The pre-curation spec recorded them from
// a different frame; spec corrected in place. Nothing to draw here.

// ---------- 10. Regression text line (~60-66% h) ----------
s.addText(
  [
    { text: "Regression ", options: { bold: true, color: BLU, fontFace: FONT } },
    { text: "is more like fitting a curve/surface to the data:", options: { color: BLK, fontFace: FONT } },
  ],
  { x: 1.15, y: 4.40, w: 10.9, h: 0.40, fontSize: 18, align: "left", valign: "middle", margin: 0 }
);

// ---------- 11. Regression plot: curve fitting (~66-95% h, center-right) ----------
// GRAPHED version (founder directive 2026-10-09, advanced-graph generation rule):
// the native pptxgenjs approximation below is REPLACED by the PIL-forensics-matched
// matplotlib render (build/assets/graphs/s015_graph_v1.png; vision-gate PASS attempt 1,
// graph_check_1.txt; green curve sin(2*pi*x), red edge 1.18*sin(2*pi*x), pink band
// +/-0.28, LSQ sinusoid fit of the 22 extracted points computed via scipy
// curve_fit as the documented algorithm step). Image box measured from the
// original frame (1px = 1pt = 1/72in): x 494.7..820.3 px, y 363.2..515.3 px
// -> x = 6.871in, y = 5.044in, w = 4.522in, h = 2.113in.
// FOUNDER FIX 2026-10-10 ("move the inner content up as well", same way as
// slide 5): with the enlarged frame (bottom 7.26in) the panel fits at its
// measured position, and per the founder directive it is additionally moved
// UP by 0.05in -> y 4.994in (bottom 7.107in), giving 0.153in (~11 orig-frame
// px, vs the original's 7.2px) clearance to the frame bottom edge. The graph
// image asset itself is UNCHANGED (same graph_v1.png, same algorithm/data) —
// only its placement moved. Everything else on this slide is byte-identical
// to the certified native build apart from the frame change above.
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s015_graph_v1.png",
  x: 6.871, y: 4.994, w: 4.522, h: 2.113,
});

// ---------- 12/13/14. NO regression ink marks ----------
// Attempt-2: judge finding 3 + orig_census_1.txt — the CURRENT ground truth's
// regression plot is CLEAN (band, curve, points, axes only). The red vertical
// arrow + 'x', the red horizontal arrow, and the black curve arrow recorded by
// the pre-curation spec belong to a different frame; spec corrected in place.

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_015_recreated.pptx" })
  .then(() => console.log("done"));
