// Slide 035 recreation — "Linearly separable vs. Not linearly separable"
// GRAPED VARIANT of the certified build/slide_035.js (never overwrite the
// certified native build or slide_035_recreated.pptx): the bottom scatter is
// a generated graph image (see section 5 below); everything else unchanged.
// Spec: videos/ml-intro/analysis/slide_035_final.json (validation PASS_WITH_FIXES, fixes applied)
//
// Notes on [?] handling (per spec uncertain_items):
//   - "Data fitting [?]" tooltip on the bottom plot: rendered as "Data fitting"
//     (best reading); [?] is a spec-internal uncertainty marker, not slide
//     content (same convention as slide_018 builds). Spec brief step 13 says it
//     may be omitted in a static recreation, but the spec keeps it in the
//     verbatim labels, so it IS drawn (small gray tooltip-style label near (0.5, 0)).
//   - Bottom-plot numeric tick range -2.5..2.5 is marked [?] in the spec; the
//     tick labels -2.5, -2, -1.5, ..., 2.5 are listed verbatim in visual_elements.
//   - Scatter point counts are unspecified in the source; clusters are
//     approximated per spec uncertain_items (builder approximation allowed).
//   - Upper container border color not stated (assumed black per spec brief).
//   - House frame rule (founder directive 2026-10-09) OVERRIDES the spec's
//     #A02040 frame/badge geometry: outer frame C00000 1.5pt, badge FFF9C4 at
//     x:12.48 y:0.30 w:0.5 h:0.5, title box y:0.28 x:0.6 w:12.13 centered.
//     Badge numeral = 35 (number printed on the original slide).
//
// Layout (spec layout.regions, region coords authoritative):
//   upper container  ~18-75% w, ~10-50% h  -> shifted to y 0.90-3.75 under the
//     house title box; two panels (left: 1 scatter, right: 2 scatters)
//   bottom plot      ~28-60% w, ~52-98% h  -> x 3.73 y 3.95 w 4.27 h 3.35
//   badge            house values          -> x 12.48 y 0.30

const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";       // house slide background
const FRAME_RED = "C00000"; // house outer frame
const DARK_RED = "A02040";  // bottom plot border (spec)
const RED = "C00000";       // red scatter dots
const BLUE = "1F6FB2";     // blue scatter squares
const GREEN = "00B050";    // green scatter dots
const BLK = "000000";
const GRAY = "404040";     // subtitle gray
const TIPGRAY = "808080";  // tooltip gray
const WHITE = "FFFFFF";
const BADGE_YELLOW = "FFF9C4"; // house badge fill
const INK = "333333";      // badge numeral

const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---------- helpers ----------
// Straight segment between two points (pptxgenjs lines are bounding-box based).
function seg(x1, y1, x2, y2, lineOpts) {
  const w = Math.max(Math.abs(x2 - x1), 0.001);
  const h = Math.max(Math.abs(y2 - y1), 0.001);
  s.addShape(pptx.shapes.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w, h,
    flipH: x2 < x1, flipV: y2 < y1,
    line: lineOpts,
  });
}
const txt = (t, o) => s.addText(t, Object.assign({ fontFace: FONT, margin: 0 }, o));
// red filled circle marker (data fraction coords -> absolute)
function redDot(cx, cy, d = 0.09) {
  s.addShape(pptx.shapes.OVAL, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, fill: { color: RED } });
}
// blue filled square marker
function blueSq(cx, cy, d = 0.10) {
  s.addShape(pptx.shapes.RECTANGLE, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, fill: { color: BLUE } });
}

// ---------- 1. HOUSE FRAME (founder directive — overrides spec #A02040) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// ---------- 2. HOUSE badge: yellow oval, numeral 35 (printed on original) ----------
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
txt("35", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK,
});

// ---------- 3. HOUSE title box (y:0.28 x:0.6 w:12.13, centered) ----------
// Spec has no title bar on the original; slide_title is the validator's
// reconstruction from the two panel headings — rendered per house template.
txt("Linearly separable vs. Not linearly separable", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 24, bold: true, color: FRAME_RED,
});

// ---------- 4. Upper white container: two side-by-side panels ----------
// Spec regions: ~18-75% w, ~10-50% h -> x 2.4, y 0.90, w 7.6, h 2.85
const CX = 2.4, CY = 0.90, CW = 7.6, CH = 2.85;
s.addShape(pptx.shapes.RECTANGLE, {
  x: CX, y: CY, w: CW, h: CH, fill: { color: WHITE }, line: { color: BLK, width: 0.75 },
});
// panel divider
seg(CX + CW / 2, CY, CX + CW / 2, CY + CH, { color: BLK, width: 0.75 });

// ---- Left panel: "Linearly separable" (one scatter plot) ----
txt("Linearly separable", {
  x: 2.5, y: 0.98, w: 3.6, h: 0.26, align: "center", valign: "top",
  fontSize: 13, bold: true, color: BLK,
});
txt("A linear decision boundary that separates the two classes exists", {
  x: 2.55, y: 1.27, w: 3.5, h: 0.42, align: "center", valign: "top",
  fontSize: 9, color: GRAY,
});

// left-panel plot: axes + x1/x2 labels, clusters, boundary
(function leftPlot() {
  const x0 = 2.95, y0 = 1.82, pw = 2.60, ph = 1.55;
  // axes
  seg(x0, y0, x0, y0 + ph, { color: BLK, width: 1 });
  seg(x0, y0 + ph, x0 + pw, y0 + ph, { color: BLK, width: 1 });
  txt("x2", { x: x0 - 0.30, y: y0 - 0.05, w: 0.26, h: 0.22, align: "right", valign: "middle", fontSize: 8, italic: true, color: BLK });
  txt("x1", { x: x0 + pw + 0.03, y: y0 + ph - 0.11, w: 0.26, h: 0.22, align: "left", valign: "middle", fontSize: 8, italic: true, color: BLK });
  const px = (f) => x0 + f * pw, py = (f) => y0 + f * ph;
  // red circle cluster (left half)
  [[0.18, 0.25], [0.30, 0.15], [0.14, 0.45], [0.32, 0.38], [0.22, 0.62], [0.36, 0.55], [0.27, 0.78]]
    .forEach(([fx, fy]) => redDot(px(fx), py(fy), 0.085));
  // blue square cluster (right half)
  [[0.66, 0.28], [0.79, 0.16], [0.71, 0.50], [0.84, 0.40], [0.63, 0.68], [0.77, 0.78], [0.87, 0.58]]
    .forEach(([fx, fy]) => blueSq(px(fx), py(fy), 0.095));
  // straight solid diagonal boundary between the clusters
  seg(px(0.50), py(0.95), px(0.53), py(0.05), { color: BLK, width: 1.5 });
  // label right of the line's lower half, clear of both clusters
  txt("Linear boundary", {
    x: px(0.55), y: py(0.84), w: 0.95, h: 0.18, align: "left", valign: "middle",
    fontSize: 8, color: BLK,
  });
})();

// ---- Right panel: "Not linearly separable" (two small scatter plots) ----
txt("Not linearly separable", {
  x: 6.3, y: 0.98, w: 3.6, h: 0.26, align: "center", valign: "top",
  fontSize: 13, bold: true, color: BLK,
});
txt("No linear decision boundary that separates the two classes perfectly exists", {
  x: 6.35, y: 1.27, w: 3.5, h: 0.42, align: "center", valign: "top",
  fontSize: 9, color: GRAY,
});

// small-plot frame helper: axes + x1/x2 labels
function smallAxes(x0, y0, pw, ph) {
  seg(x0, y0, x0, y0 + ph, { color: BLK, width: 0.75 });
  seg(x0, y0 + ph, x0 + pw, y0 + ph, { color: BLK, width: 0.75 });
  txt("x2", { x: x0 - 0.28, y: y0 - 0.05, w: 0.24, h: 0.2, align: "right", valign: "middle", fontSize: 7, italic: true, color: BLK });
  txt("x1", { x: x0 + pw + 0.02, y: y0 + ph - 0.10, w: 0.24, h: 0.2, align: "left", valign: "middle", fontSize: 7, italic: true, color: BLK });
}

// Right panel, plot A (left): intermixed classes, failing solid line,
// dashed ellipse around the mixed cluster, dashed arc + "Nonlinear boundary"
(function plotA() {
  const x0 = 6.42, y0 = 1.90, pw = 1.50, ph = 1.48;
  smallAxes(x0, y0, pw, ph);
  const px = (f) => x0 + f * pw, py = (f) => y0 + f * ph;
  // intermixed red circles / blue squares
  [[0.22, 0.28], [0.34, 0.18], [0.44, 0.30], [0.30, 0.52], [0.52, 0.58], [0.16, 0.66]]
    .forEach(([fx, fy]) => redDot(px(fx), py(fy), 0.075));
  [[0.36, 0.40], [0.56, 0.14], [0.68, 0.44], [0.46, 0.74], [0.14, 0.44], [0.66, 0.68], [0.78, 0.26]]
    .forEach(([fx, fy]) => blueSq(px(fx), py(fy), 0.085));
  // solid straight line that FAILS to separate (passes through the mix)
  seg(px(0.08), py(0.92), px(0.92), py(0.08), { color: BLK, width: 1 });
  // dashed ellipse around the central mixed cluster
  s.addShape(pptx.shapes.OVAL, {
    x: px(0.20), y: py(0.18), w: 0.52 * pw, h: 0.50 * ph,
    fill: { type: "none" }, line: { color: BLK, width: 0.75, dashType: "dash" },
  });
  // dashed curved line arcing around the upper-left red group
  const arc = [[0.10, 0.55], [0.06, 0.38], [0.10, 0.22], [0.22, 0.12], [0.36, 0.08], [0.48, 0.12]];
  for (let i = 0; i < arc.length - 1; i++) {
    seg(px(arc[i][0]), py(arc[i][1]), px(arc[i + 1][0]), py(arc[i + 1][1]),
        { color: BLK, width: 1, dashType: "dash" });
  }
  txt("Nonlinear boundary", {
    x: x0 + 0.28, y: y0 - 0.18, w: 0.95, h: 0.16, align: "center", valign: "middle",
    fontSize: 7, color: BLK,
  });
})();

// Right panel, plot B (right): red center cluster ringed by blue, dashed
// circle around the red cluster, solid line failing to separate
(function plotB() {
  const x0 = 8.18, y0 = 1.90, pw = 1.50, ph = 1.48;
  smallAxes(x0, y0, pw, ph);
  const px = (f) => x0 + f * pw, py = (f) => y0 + f * ph;
  // blue squares at corners/edges
  [[0.10, 0.12], [0.86, 0.16], [0.14, 0.84], [0.88, 0.78], [0.50, 0.07], [0.07, 0.50], [0.92, 0.48], [0.52, 0.90]]
    .forEach(([fx, fy]) => blueSq(px(fx), py(fy), 0.085));
  // red circles clustered in the middle
  [[0.42, 0.40], [0.56, 0.46], [0.47, 0.56], [0.37, 0.52], [0.51, 0.34], [0.61, 0.56], [0.44, 0.64]]
    .forEach(([fx, fy]) => redDot(px(fx), py(fy), 0.075));
  // dashed circle around the central red cluster
  s.addShape(pptx.shapes.OVAL, {
    x: px(0.28), y: py(0.24), w: 0.44 * pw, h: 0.46 * ph,
    fill: { type: "none" }, line: { color: BLK, width: 0.75, dashType: "dash" },
  });
  // solid straight line that fails to separate
  seg(px(0.10), py(0.14), px(0.88), py(0.86), { color: BLK, width: 1 });
})();

// ---------- 5. Bottom large scatter plot — GENERATED GRAPH IMAGE (graphed build) ----------
// Advanced-graph generation rule (founder directive 2026-10-09): the original's
// bottom multi-class scatter is a dense plotted graph (~147 measured points)
// that native shapes can only approximate, so this build embeds a properly
// generated matplotlib image instead. Image: build/assets/graphs/s35_graph_v1.png
// (300 dpi at the panel's measured physical size), generated by
// qa/slide35/graphgen/slide_035_scatter.py from the point set measured out of
// the original frame (45 green + 31 blue + 71 red blob centers), with the
// measured gray boxed axes, -2.5..2.5 ticks, #A02040 border and "Data fitting"
// tooltip baked in. Placement = the original frame's measured panel region
// (282,283)-(571,528) px, 1px = 1pt = 1/72in (triage plan P-35). Vision gate
// on the standalone graph: PASS attempt 1 (qa/slide35/graphgen/graph_check_1.txt).
// House chrome, badge, title and the upper two-panel container are unchanged
// from the certified native build (slide_035.js).
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s35_graph_v1.png",
  x: 3.9167, y: 3.9306, w: 4.0139, h: 3.4028,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_035_recreated.pptx" })
  .then(() => console.log("done"));
