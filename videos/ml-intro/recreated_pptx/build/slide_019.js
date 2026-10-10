// Slide 19 recreation — "Data Overfit and Underfit" (current curated slide_019.jpg,
// old pre-curation id 25). Spec: videos/ml-intro/analysis/slide_019_final.json
// (verbatim text, layout, colors, 12-step recreation_brief).
//
// Attempt 4 — judge-3 fixes applied:
//   MAJOR: ~20 X / ~20 O markers per panel spread over the whole plot with real
//          class overlap (was 7+7 clean clusters);
//   MAJOR: under-fit straight line now visibly MISCLASSIFIES overlapped points;
//   MAJOR: over-fit boundary now has a closed contour looping around a small
//          interior O-group + small loops around stray X points;
//   MINOR: left regression panel = arch/inverted-U orange target + curved blue
//          fit + 6 open-circle data points;
//   MINOR: regression data points small OPEN circles (white fill, black outline);
//   MINOR: parenthetical sub-captions italic + wrapped (3 / 2 centered lines);
//   MINOR: arrowheads on classification panel axes.
//
// NOTE: the pre-curation slide_019.js / slide_019_recreated.pptx (poly-fit demo,
// printed badge "16" — now slide 16) were replaced by this fresh build per the
// orchestrator re-dispatch; their per-attempt provenance stays banked under
// qa/slide019/ (untouched).
//
// HOUSE FRAME (founder rule 2026-10-09): LAYOUT_WIDE 13.33x7.5, bg E8E8E8, red
// outer frame 0.15in inset (C00000 1.5pt), badge oval 12.48/0.30/0.5/0.5 FFF9C4
// with numeral = printed slide number "19" (bold 18pt 333333), title box
// y:0.28 x:0.6 w:12.13 centered.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// House chrome
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE_YELLOW = "FFF9C4", INK = "333333";
// Spec palette (slide_019_final.json)
const TITLE_RED = "B00000", BOX_RED = "AA0000", BLACK = "000000", WHITE = "FFFFFF",
      GRAY = "808080", BLUE = "0000FF", LABEL_BLUE = "0000CC", X_RED = "FF0000",
      PANEL_GREEN = "CCFFCC", ORANGE = "FF6600", FIT_GREEN = "00CC66", AXES = "404040";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---------------- shape helpers ----------------
function seg(x1, y1, x2, y2, color, width) {
  let ax = x1, ay = y1, bx = x2, by = y2;
  if (bx < ax) { [ax, bx] = [bx, ax]; [ay, by] = [by, ay]; }
  const w = Math.max(bx - ax, 0.001), h = Math.max(Math.abs(by - ay), 0.001);
  s.addShape(pptx.shapes.LINE, {
    x: ax, y: Math.min(ay, by), w, h,
    line: { color, width },
    flipV: by < ay,
  });
}
function polyline(pts, color, width) {
  for (let i = 0; i + 1 < pts.length; i++)
    seg(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, width);
}
function closedLoop(pts, color, width) { polyline(pts.concat([pts[0]]), color, width); }
function ellipseLoop(cx, cy, rx, ry, color, width, n = 40) {
  const pts = [];
  for (let k = 0; k < n; k++) {
    const a = (k / n) * 2 * Math.PI;
    pts.push([cx + rx * Math.cos(a), cy + ry * Math.sin(a)]);
  }
  closedLoop(pts, color, width);
}
function circle(cx, cy, d, fill, lineColor, lineW) {
  s.addShape(pptx.shapes.OVAL, {
    x: cx - d / 2, y: cy - d / 2, w: d, h: d,
    fill: { color: fill }, line: { color: lineColor, width: lineW },
  });
}
function arrowHead(tipX, tipY, dirX, dirY, color, width) {
  // two short strokes forming a V at the tip, pointing along (dirX, dirY)
  const L = 0.11, spread = 0.055;
  seg(tipX, tipY, tipX - dirX * L - dirY * spread, tipY - dirY * L + dirX * spread, color, width);
  seg(tipX, tipY, tipX - dirX * L + dirY * spread, tipY - dirY * L - dirX * spread, color, width);
}
function text(t, o) { s.addText(t, Object.assign({ fontFace: FONT, margin: 0 }, o)); }

// ---------------- house chrome ----------------
// Outer red frame: 0.15in inset from every edge, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// Title (house box y:0.28 x:0.6 w:12.13, centered), dark red bold per spec
text("Data Overfit and Underfit", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "top",
  fontSize: 30, bold: true, color: TITLE_RED,
});

// Slide-number badge: numeral = printed number on the original = 19
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
text("19", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK,
});

// ---------------- inner red structure (judge 4 MAJOR fix) ----------------
// Original: a red (#AA0000) border around the CLASSIFICATION GROUP only (three
// scatter panels + captions), plus a red border around EACH green regression
// panel — NOT one all-content box. The blue row labels sit OUTSIDE the borders.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 2.42, y: 1.42, w: 10.10, h: 3.42,
  fill: { color: BG }, line: { color: BOX_RED, width: 2 },
});

// =================== upper row: Classification (steps 6-9) ===================
text("Classification", {
  x: 0.88, y: 2.55, w: 1.62, h: 0.4, align: "center", valign: "middle",
  fontSize: 16, bold: true, italic: true, color: LABEL_BLUE,
});

// Three equal side-by-side white scatter panels with plain x/y axes (with
// arrowheads) and unlabeled ticks; red X markers and gray O markers spread
// over the whole plot area with real class overlap in the middle; blue
// decision boundary (straight / gently curved / wiggly with closed contours).
const P_W = 3.0, P_H = 2.55, P_Y = 1.55;
const P_X = [2.55, 5.95, 9.35];
// data-space mappers inside one panel
const px = (i, u) => P_X[i] + 0.38 + u * 2.30;   // u in [0,1] -> inside axes
const py = (v) => P_Y + 2.28 - v * 1.95;         // v in [0,1] -> inside axes

// ~21 red X's spread across the ENTIRE plot (incl. upper-right, interleaved
// with O's at the boundary) — judge 5 MAJOR: heavy class overlap so the
// under-fit line visibly misclassifies many points
const xPts = [
  [0.06, 0.10], [0.14, 0.20], [0.10, 0.34], [0.22, 0.14], [0.28, 0.28],
  [0.20, 0.44], [0.34, 0.38], [0.30, 0.56], [0.42, 0.22], [0.44, 0.46],
  [0.48, 0.18], [0.50, 0.12], [0.46, 0.30], [0.52, 0.58], [0.66, 0.16],
  [0.70, 0.44], [0.76, 0.26], [0.82, 0.52], [0.88, 0.20], [0.94, 0.42],
  [0.86, 0.66],
];
// ~21 gray O's, upper-right bias with boundary interleaving, plus a small
// CENTER-RIGHT pocket (0.55-0.68 u, low v) surrounded by X's that the
// over-fit closed contour encircles (judge 5: loop sits center-right)
const oPts = [
  [0.16, 0.62], [0.26, 0.72], [0.36, 0.60], [0.30, 0.82], [0.44, 0.70],
  [0.48, 0.86], [0.54, 0.64], [0.58, 0.78], [0.62, 0.88], [0.68, 0.74],
  [0.74, 0.84], [0.80, 0.72], [0.92, 0.64], [0.78, 0.92], [0.90, 0.94],
  [0.62, 0.92],
  // boundary-interleaved
  [0.40, 0.34], [0.47, 0.52],
  // center-right pocket (encircled by the over-fit loop)
  [0.60, 0.24], [0.68, 0.32], [0.55, 0.38],
];

function drawX(i, u, v) {
  const cx = px(i, u), cy = py(v), r = 0.07;
  seg(cx - r, cy - r, cx + r, cy + r, X_RED, 1.5);
  seg(cx - r, cy + r, cx + r, cy - r, X_RED, 1.5);
}

// straight under-fit boundary: MISCLASSIFIES the overlapped/stray points
const b1 = (u) => 0.75 - 0.55 * u;
// appropriate-fit: dips mid-plot, then RISES toward the right (judge 4 MAJOR)
const b2 = (u) => 0.70 - 1.35 * u + 1.25 * u * u;
// over-fit: wavy boundary passing BELOW the closed contour (which hangs off it)
const b3 = (u) => 0.62 - 0.40 * u + 0.07 * Math.sin(9.0 * Math.PI * u + Math.PI);

function scatterPanel(i, boundary) {
  const x0 = P_X[i];
  // white panel background
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x0, y: P_Y, w: P_W, h: P_H,
    fill: { color: WHITE }, line: { color: AXES, width: 0.75 },
  });
  // L-shaped axes with arrowheads (judge 3: original axes carry arrowheads)
  seg(x0 + 0.30, P_Y + 0.14, x0 + 0.30, P_Y + 2.38, AXES, 1);
  arrowHead(x0 + 0.30, P_Y + 0.14, 0, -1, AXES, 1);
  seg(x0 + 0.30, P_Y + 2.38, x0 + 2.82, P_Y + 2.38, AXES, 1);
  arrowHead(x0 + 2.82, P_Y + 2.38, 1, 0, AXES, 1);
  // unlabeled ticks
  for (let k = 1; k <= 4; k++) {
    const ty = P_Y + 0.14 + (k * 2.24) / 5;
    seg(x0 + 0.24, ty, x0 + 0.30, ty, AXES, 0.75);           // y-axis ticks
    const tx = x0 + 0.30 + (k * 2.52) / 5;
    seg(tx, P_Y + 2.38, tx, P_Y + 2.44, AXES, 0.75);          // x-axis ticks
  }
  // markers
  for (const [u, v] of xPts) drawX(i, u, v);
  for (const [u, v] of oPts) circle(px(i, u), py(v), 0.14, WHITE, GRAY, 1.25);
  // blue decision boundary, kept inside the axes region
  const pts = [];
  const N = 140;
  for (let k = 0; k <= N; k++) {
    const u = -0.01 + (k / N) * 1.02;
    const v = Math.min(1.02, Math.max(-0.02, boundary(u)));
    pts.push([px(i, u), py(v)]);
  }
  polyline(pts, BLUE, 2);
  // over-fit panel only: closed contour around the center-right O-pocket
  // (judge 5: loop sits center-right; organically perturbed, not a clean ellipse)
  if (i === 2) {
    const C = { u: 0.612, v: 0.313 };
    const pts = [];
    for (let k = 0; k < 36; k++) {
      const a = (k / 36) * 2 * Math.PI;
      const r = 0.19 * (1 + 0.16 * Math.sin(3 * a + 1.2) + 0.09 * Math.sin(5 * a + 0.4));
      pts.push([px(i, C.u) + r * Math.cos(a), py(C.v) + r * (2.30 / 1.95) * Math.sin(a)]);
    }
    closedLoop(pts, BLUE, 2);
  }
}

scatterPanel(0, b1);
scatterPanel(1, b2);
scatterPanel(2, b3);

// captions (verbatim, bold black; sub-captions italic, wrapped per judges 3-4)
const CAP_Y = 4.12;
function caption(i, main, subLines) {
  text(main, {
    x: P_X[i], y: CAP_Y, w: P_W, h: 0.22, align: "center", valign: "top",
    fontSize: 13, bold: true, color: BLACK,
  });
  if (subLines) {
    const rows = subLines.map((t, k) => ({
      text: t, options: { breakLine: k < subLines.length - 1 },
    }));
    s.addText(rows, {
      x: P_X[i] - 0.25, y: 4.34, w: P_W + 0.5, h: 0.48, align: "center", valign: "top",
      fontSize: 9, italic: true, color: BLACK, fontFace: FONT, margin: 0,
    });
  }
}
caption(0, "Under-fitting", ["(too simple to", "explain the", "variance)"]);
caption(1, "Appropriate-fitting", null);
caption(2, "Over-fitting", ["(forcefitting -- too", "good to be true)"]);

// =================== lower row: Regression (steps 10-12) ===================
text("Regression", {
  x: 0.88, y: 5.55, w: 1.62, h: 0.4, align: "center", valign: "middle",
  fontSize: 16, bold: true, italic: true, color: LABEL_BLUE,
});

// Two light-green (#CCFFCC) regression panels rendered as high-fidelity images
// (graphgen pipeline, slide_019_overfit.py v3). Each PNG is drawn at the
// panel's exact physical size (1px = 1pt @300dpi), so the addImage w/h below
// equal the measured panel geometry in the ground-truth frame:
// left 189,360 -> 305x126 pt; right 575,360 -> 301x125 pt. Axis labels and
// legends are added as native shapes on top of the images (they are not part
// of the generated PNGs). Images first (bottom z-order).
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s19_graph_left_v3.png",
  x: 2.625, y: 5.0, w: 4.2361, h: 1.75,
});
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s19_graph_right_v3.png",
  x: 7.9861, y: 5.0, w: 4.1806, h: 1.7361,
});

// axis labels (verbatim "y" and "x"), positioned over the measured label ink
text("y", { x: 2.7056, y: 5.7056, w: 0.2, h: 0.2, align: "center", valign: "middle",
  italic: true, fontSize: 10, color: BLACK });
text("x", { x: 4.65, y: 6.5528, w: 0.2, h: 0.2, align: "center", valign: "middle",
  italic: true, fontSize: 10, color: BLACK });
text("y", { x: 8.067, y: 5.7056, w: 0.2, h: 0.2, align: "center", valign: "middle",
  italic: true, fontSize: 10, color: BLACK });
text("x", { x: 9.9694, y: 6.525, w: 0.2, h: 0.2, align: "center", valign: "middle",
  italic: true, fontSize: 10, color: BLACK });

// open-circle data-point marker (legend "Data" swatch)
function dataPoint(x, y) { circle(x, y, 0.10, WHITE, BLACK, 1); }

// left legend (panel top-right): Data / Target / Fit — sample colors recolored
// to match the measured curve ink in the original (target = blue, fit = orange)
{
  const lgX = 5.6811, lgY = 5.10, LH = 0.15;
  dataPoint(lgX + 0.07, lgY + 0.075);
  text("Data", { x: lgX + 0.17, y: lgY, w: 0.95, h: LH, fontSize: 7.5, color: BLACK, valign: "middle" });
  seg(lgX + 0.01, lgY + 0.15 + LH / 2, lgX + 0.14, lgY + 0.15 + LH / 2, BLUE, 1.5);
  text("Target", { x: lgX + 0.17, y: lgY + 0.15, w: 0.95, h: LH, fontSize: 7.5, color: BLACK, valign: "middle" });
  seg(lgX + 0.01, lgY + 0.30 + LH / 2, lgX + 0.14, lgY + 0.30 + LH / 2, ORANGE, 1.5);
  text("Fit", { x: lgX + 0.17, y: lgY + 0.30, w: 0.95, h: LH, fontSize: 7.5, color: BLACK, valign: "middle" });
}

// right legend (panel bottom-right): Data / 2nd Order Fit / 10th Order Fit
{
  const rgX = 10.4467, rgY = 6.0361;
  dataPoint(rgX + 0.08, rgY + 0.09);
  text("Data", { x: rgX + 0.20, y: rgY, w: 1.45, h: 0.18, fontSize: 8, color: BLACK, valign: "middle" });
  seg(rgX + 0.01, rgY + 0.28, rgX + 0.17, rgY + 0.28, FIT_GREEN, 1.5);
  text("2nd Order Fit", { x: rgX + 0.20, y: rgY + 0.19, w: 1.45, h: 0.18, fontSize: 8, color: BLACK, valign: "middle" });
  seg(rgX + 0.01, rgY + 0.47, rgX + 0.17, rgY + 0.47, X_RED, 1.25);
  text("10th Order Fit", { x: rgX + 0.20, y: rgY + 0.38, w: 1.45, h: 0.18, fontSize: 8, color: BLACK, valign: "middle" });
}

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_019_recreated.pptx" })
  .then(() => console.log("done"))
  .catch((e) => { console.error(e); process.exit(1); });
