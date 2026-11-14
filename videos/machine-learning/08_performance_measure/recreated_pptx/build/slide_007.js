// slide_007 — "Precision" (08_performance_measure). 1px of the 960x540 original = 1pt.
// Geometry measured from unique_slides/slide_007.jpg with PIL; text from the fresh
// image-analysis read (pool_run/image_analysis/slide_007_analysis.txt), cross-checked
// against analysis/reanalysis/slide_007_raw.json + sources/slide_007_research.md.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const DRED = "8F0000";
const GREEN = "00B050";
const GRN_FILL = "8CFF00";   // CM1 TP/TN cell fills (measured ~#87FF00)
const BLUE = "0070C0";
const ARROW_BLUE = "0000FF";
const BADGE = "FFF9C4";
const INK = "333333";
const BLACK = "000000";
const GRAY_BOX = "CBCDCA";   // definition band (measured ~#CBCDCA)
const PALE_Y = "F7FCD4";     // meaning band (measured ~#F7FCD4)
const PALE_C = "F0FFFD";     // worked-example box (measured ~#F0FFFD)
const CALLOUT = "FCFFE2";    // callout boxes (measured ~#FCFFE2)
const QBOX = "DDFFFF";       // question box (measured ~#DDFFFF)
const FONT = "Arial";

const px = (v) => v / 72;
const s = pptx.addSlide();
s.background = { color: BG };

// ---------- house chrome (root AGENTS.md 2026-10-09, overrides everything) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("7", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText("Precision", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62, align: "center", valign: "middle",
  fontSize: 44, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- helpers ----------
function rect(x0, y0, x1, y1, fill, lineColor, lineW) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: fill ? { color: fill } : { type: "none" },
    line: lineColor ? { color: lineColor, width: lineW || 1.25 } : { type: "none" },
  });
}
function hline(x0, x1, y, color, w) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y), w: px(x1 - x0), h: px(w || 2),
    fill: { color: color }, line: { color: color, width: 0.25 },
  });
}
function vline(x, y0, y1, color, w) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x), y: px(y0), w: px(w || 2), h: px(y1 - y0),
    fill: { color: color }, line: { color: color, width: 0.25 },
  });
}
function text(str, x0, y0, x1, y1, size, color, opts) {
  const o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "center", valign: "middle", fontSize: size, bold: true,
    color: color, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(str, o);
}
function rtext(parts, x0, y0, x1, y1, size, opts) {
  const o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "left", valign: "middle", fontSize: size, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(parts.map(([t, c, b, i]) => ({
    text: t, options: { color: c, bold: b !== false, italic: !!i, fontFace: FONT },
  })), o);
}

// ---------- gray definition band ----------
rect(72, 113, 656, 173, GRAY_BOX, null);
rtext([
  ["Correctly Classified (as ", BLACK],
  ["Positive", RED],
  [")", BLACK],
], 70, 118, 640, 140, 16, { align: "center" });
hline(82, 646, 140, DRED, 2);
rtext([
  ["Total Classified as ", BLACK],
  ["Positive", RED],
  [" (either Correct and Erroneous)", BLACK],
], 70, 150, 640, 171, 19, { align: "center" });

// ---------- Meaning band (pale yellow) ----------
rect(73, 199, 624, 253, PALE_Y, null);
text("Meaning", 78, 205, 178, 227, 16, RED, { align: "left" });
rtext([
  ["% of what you ", BLACK],
  ["Predicted", RED],
  [" as ", BLACK],
  ["POSITIVE", BLUE],
  [" is Actually Positive", BLACK],
], 79, 232, 620, 254, 19, { align: "left" });

// ---------- formula box (white rounded rect, red border; measured x72-316 y263-322) ----------
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: px(72), y: px(263), w: px(244), h: px(59),
  fill: { color: "FFFFFF" }, line: { color: DRED, width: 2 },
  adj: 0.25,
});
text("Precision =", 84, 276, 200, 301, 18, BLACK, { align: "left" });
// stacked fraction: numerator / bar / denominator (professional 2D)
text("TP", 246, 266, 288, 291, 18, BLACK);
hline(218, 310, 295, BLACK, 2.5);
text("TP + FP", 218, 298, 310, 319, 18, BLACK);

// ---------- worked example box (pale cyan) ----------
rect(336, 288, 508, 340, PALE_C, "9DC3E6", 1);
text("Precision= 18/(18+10)", 342, 293, 502, 313, 14, BLACK, { align: "left" });
rtext([["=64.3%", "1F2A8C"]], 392, 316, 470, 336, 12, { align: "left" });

// ---------- callout notes (plain pale boxes, two-line text) ----------
function calloutNote(x0, y0, x1, y1, line1, fill) {
  rect(x0, y0, x1, y1, fill, "BFBFBF", 0.75);
  s.addText([
    { text: line1, options: { fontSize: 10, bold: true, color: BLACK, fontFace: FONT, breakLine: true } },
    { text: "Classified as +ive", options: { fontSize: 10, bold: true, color: BLACK, fontFace: FONT } },
  ], {
    x: px(x0 + 4), y: px(y0 + 2), w: px(x1 - x0 - 8), h: px(y1 - y0 - 4),
    align: "center", valign: "middle", margin: 0, lineSpacing: 15,
  });
}
calloutNote(116, 340, 208, 389, "Positive", "FCFFE2");
calloutNote(225, 340, 319, 389, "Negative", "FCFFE2");
// broad pale-yellow diagonal callout arrows from the formula box to the notes
// (measured in the original: left ~(208,322)->(178,342), right ~(294,322)->(300,342), fill ~#F5E3CD)
function connector(x0, y0, x1, y1) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: "F5E3CD", width: 4, endArrowType: "triangle" },
  });
}
connector(208, 322, 178, 342);
connector(294, 322, 300, 342);
// smooth continuous green curly underbrace grouping the two callouts
// (original extent x108-335 y385-403, connected central cusp at ~(221,404))
function diag(x0, y0, x1, y1, color, w) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: color, width: w },
  });
}
(function brace() {
  const N = 14, x0 = 108, x1 = 335, yTop = 386, cuspX = 221, cuspY = 404;
  const bez = (p0, c, p1, t) => [
    (1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
    (1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1],
  ];
  const halves = [
    [[x0, yTop], [150, cuspY - 6], [cuspX, cuspY]],
    [[cuspX, cuspY], [292, cuspY - 6], [x1, yTop]],
  ];
  for (const [p0, c, p1] of halves) {
    let prev = p0;
    for (let i = 1; i <= N; i++) {
      const cur = bez(p0, c, p1, i / N);
      diag(prev[0], prev[1], cur[0], cur[1], GREEN, 3);
      prev = cur;
    }
  }
})();
// red italic annotation
rtext([
  ["All Samples ", RED],
  ["classified as Positive", RED],
], 80, 410, 314, 430, 13, { align: "left", italic: true });

// ---------- bottom question box (pale cyan, blue border) ----------
rect(76, 465, 498, 509, QBOX, "2E75B6", 1.25);
s.addText([
  { text: "If you said: the sample is positive,", options: { fontSize: 14, bold: false, italic: true, color: "16336F", fontFace: FONT, breakLine: true } },
  { text: "can I trust you ? At what %?", options: { fontSize: 14, bold: false, italic: true, color: "16336F", fontFace: FONT, breakLine: false } },
], {
  x: px(86), y: px(470), w: px(400), h: px(34), align: "left", valign: "middle",
  margin: 0, lineSpacing: 20,
});

// ---------- confusion matrix helper ----------
// Red grid lines are drawn INSET from the blue panel border (measured: they stop
// ~20px short of the right border and do not touch the blue frame).
const CM_BORDER = "6E68AC";  // measured purple panel border in the original (~#6E68AC), not blue
  const OVAL_HL = "984F7D";    // measured plum hand-drawn highlight ovals (~#984F7D)
function matrix(o) {
  const fP = o.fsPred, fH = o.fsHdr, fC = o.fsCell;
  rect(o.x0, o.y0, o.x1, o.y1, "FFFFFF", CM_BORDER, 1.5);
  text("Predicted as", o.hdrX0, o.y0 + 9, o.hdrX1, o.hy0, fP, RED);
  text("P", o.cellX0, o.hy0, o.splitX, o.hy1, fH, BLACK);
  text("N", o.splitX, o.hy0, o.cellX1, o.hy1, fH, BLACK);
  o.cells.forEach(([cx0, cy0, cx1, cy1, fill]) => { if (fill) rect(cx0, cy0, cx1, cy1, fill, null); });
  o.hlines.forEach(([y, hx0, hx1]) => hline(hx0, hx1, y, RED, 1.5));
  o.vlines.forEach((x) => vline(x, o.hy0, o.ry1, RED, 1.5));
  o.cells.forEach(([cx0, cy0, cx1, cy1, , label]) => { if (label) text(label, cx0, cy0, cx1, cy1, fC, BLACK); });
}
function actualLabel(cx, cy) {
  s.addText("Actual", {
    x: px(cx - 24), y: px(cy - 32), w: px(48), h: px(64), rotate: 270,
    align: "center", valign: "middle", fontSize: 14, bold: true, color: BLACK,
    fontFace: FONT, margin: 0,
  });
}

// matrix 1 (symbolic): panel x673-867 y53-158 (blue border measured); red grid rows
// y73/98/125/151, cell cols x700/738/790/845; TP+TN cells green-filled (#87FF00)
matrix({
  x0: 673, y0: 53, x1: 867, y1: 158,
  hdrX0: 726, hdrX1: 850, hy0: 73, hy1: 98, ry1: 151,
  cellX0: 738, cellX1: 845, splitX: 790,
  fsPred: 12, fsHdr: 13, fsCell: 16,
  hlines: [[73, 698, 846], [98, 698, 846], [125, 698, 846], [151, 698, 846]],
  vlines: [700, 738, 790, 845],
  cells: [
    [738, 98, 790, 125, GRN_FILL, "TP"],
    [790, 98, 845, 125, null, "FN"],
    [738, 125, 790, 151, null, "FP"],
    [790, 125, 845, 151, GRN_FILL, "TN"],
  ],
});
text("P", 712, 104, 734, 122, 13, BLACK);
text("N", 712, 132, 734, 150, 13, BLACK);
actualLabel(688, 127);

// matrix 2 (numeric): panel x673-867 y168-288; red grid rows y190/220/252/283,
// cell cols x704/746/800/856; 60 cell green-filled
matrix({
  x0: 673, y0: 168, x1: 867, y1: 288,
  hdrX0: 726, hdrX1: 850, hy0: 190, hy1: 220, ry1: 283,
  cellX0: 746, cellX1: 856, splitX: 800,
  fsPred: 12, fsHdr: 13, fsCell: 16,
  hlines: [[190, 704, 857], [220, 704, 857], [252, 704, 857], [283, 704, 857]],
  vlines: [704, 746, 800, 856],
  cells: [
    [746, 220, 800, 252, null, "18"],
    [800, 220, 856, 252, null, "12"],
    [746, 252, 800, 283, null, "10"],
    [800, 252, 856, 283, GRN_FILL, "60"],
  ],
});
text("P", 718, 234, 740, 250, 13, BLACK);
text("N", 718, 262, 740, 278, 13, BLACK);
actualLabel(692, 256);
// hand-drawn plum circles around 18 and 10 (the predicted-positive column)
s.addShape(pptx.shapes.OVAL, {
  x: px(752), y: px(222), w: px(42), h: px(26),
  fill: { type: "none" }, line: { color: OVAL_HL, width: 2 },
});
s.addShape(pptx.shapes.OVAL, {
  x: px(752), y: px(255), w: px(42), h: px(26),
  fill: { type: "none" }, line: { color: OVAL_HL, width: 2 },
});

// ---------- Positive/Negative tree panel (red border) ----------
rect(536, 290, 880, 503, "FFFFFF", RED, 1.5);
text("Positive", 590, 296, 670, 316, 18, RED, { align: "left" });
text("Negative", 770, 296, 860, 316, 18, GREEN, { align: "left" });

// aircraft artwork: crops from the original frame (faint gray side-view drawings)
s.addImage({ path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/slide_007_plane_left.png", x: px(585), y: px(323), w: px(91), h: px(49) });
s.addImage({ path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/slide_007_plane_right.png", x: px(761), y: px(317), w: px(95), h: px(49) });

// blue branch arrows with heads
function arrow(x0, y0, x1, y1) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: ARROW_BLUE, width: 1.5, endArrowType: "triangle" },
  });
}
arrow(612, 408, 579, 441);
arrow(624, 408, 657, 440);
arrow(793, 409, 761, 441);
arrow(805, 409, 841, 441);

// tree nodes
function node(cx, cy, d, fill, label) {
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: fill },
  });
  text(label, cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2, 12, "FFFFFF");
}
node(618, 393, 30, RED, "30");
node(799, 393, 33, GREEN, "70");
node(573, 456, 29, RED, "18");
node(661, 456, 32, GREEN, "12");
node(755, 457, 32, GREEN, "60");
node(845, 456, 29, RED, "10");
// leaf labels
text("TP", 578, 482, 604, 498, 10, RED);
text("FN", 658, 482, 684, 498, 10, RED);
text("TN", 748, 482, 774, 498, 10, RED);
text("FP", 838, 482, 864, 498, 10, RED);

// ---------- black footer bar (bottom edge, measured y517-540 x38-921) ----------
rect(38, 517, 921, 540, BLACK, null);

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_007_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
