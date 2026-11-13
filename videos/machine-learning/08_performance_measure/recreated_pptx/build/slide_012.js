// slide_012 — "Recall" — 08_performance_measure — finish-worker rev (judge attempt 1 FAIL fixes, pixel-adjudicated)
// Frame-measured build (960x540 px, 1px = 1pt = 1/72 in). Matrix/tree geometry measured from slide_012.jpg (red/blue line scans + zoom crops).
const pptxgenpkg = require("pptxgenjs");
const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";
const A = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";

let s = pptx.addSlide();
s.background = { color: BG };

// House chrome (root AGENTS.md 2026-10-09 — overrides everything)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("12", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText("Recall", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.95, align: "center", valign: "middle",
  fontSize: 54, bold: true, color: "B00000", fontFace: FONT, margin: 0,
});

// Definition box (gray, red divider): orig band y120-185, divider y146-152
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.97, y: 1.66, w: 8.14, h: 0.91,
  fill: { color: "CBCBCB" }, line: { color: "B0B0B0", width: 0.75 },
});
s.addShape(pptx.shapes.LINE, {
  x: 1.13, y: 2.056, w: 7.83, h: 0,
  line: { color: RED, width: 3 },
});
s.addText("Correctly Classified (as Positive)", {
  x: 0.97, y: 1.65, w: 8.14, h: 0.44, align: "center", valign: "middle",
  fontSize: 16, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("Total objects that should be retrieved (Actually Positive)", {
  x: 0.97, y: 2.10, w: 8.14, h: 0.44, align: "center", valign: "middle",
  fontSize: 16, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});

// Meaning panel (pale yellow): orig panel x73-614 y202-268
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.01, y: 2.81, w: 7.51, h: 0.80,
  fill: { color: "F7FBD6" }, line: { color: "D8D8B0", width: 0.75 },
});
s.addText("Meaning", {
  x: 1.06, y: 2.84, w: 2.5, h: 0.40,
  fontSize: 20, bold: true, color: "B00000", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Does the classified ", options: { fontSize: 15, color: TEXT, fontFace: FONT } },
  { text: "miss", options: { fontSize: 15, color: RED, underline: true, fontFace: FONT } },
  { text: " any of ", options: { fontSize: 15, color: TEXT, fontFace: FONT } },
  { text: "Positive", options: { fontSize: 15, color: "0000CC", underline: true, fontFace: FONT } },
  { text: " Objects ?", options: { fontSize: 15, color: TEXT, fontFace: FONT } },
], {
  x: 1.06, y: 3.26, w: 7.4, h: 0.38, margin: 0, valign: "middle",
});

// Formula box: red rounded rect orig x70-303 y263-321; headroom added (judge MAJOR: numerator touched top edge)
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.97, y: 3.68, w: 3.24, h: 0.84,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 }, round: 0.15,
});
s.addText("Recall =", {
  x: 1.14, y: 3.90, w: 1.35, h: 0.40, valign: "middle",
  fontSize: 18, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addImage({ path: A + "/eq_012_frac.png", x: 2.70, y: 3.78, w: 1.49, h: 0.69667 });

// Precision callout with thin border: orig text x340-500 y294-332
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.72, y: 4.02, w: 2.30, h: 0.68,
  fill: { color: "FFFFFF" }, line: { color: "A6A6A6", width: 0.75 },
});
s.addText("Precision=", {
  x: 4.80, y: 4.08, w: 1.38, h: 0.30, valign: "middle",
  fontSize: 15, color: TEXT, fontFace: FONT, margin: 0,
});
s.addImage({ path: A + "/eq_012_prec.png", x: 6.24, y: 4.06, w: 0.635, h: 0.375 });
s.addText("=100%", {
  x: 4.80, y: 4.44, w: 1.20, h: 0.24, valign: "middle",
  fontSize: 15, color: TEXT, fontFace: FONT, margin: 0,
});

// Speech bubbles: orig left x105-215 y340-380 (yellow), right x220-325 y340-380 (peach)
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 1.46, y: 4.72, w: 1.53, h: 0.56,
  fill: { color: "FFF2CC" }, line: { color: "D0D0D0", width: 1 }, round: 0.12,
});
s.addText("Positive", {
  x: 1.46, y: 4.76, w: 1.53, h: 0.24, align: "center",
  fontSize: 10.5, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("Classified as +ive", {
  x: 1.46, y: 5.00, w: 1.53, h: 0.24, align: "center",
  fontSize: 10.5, color: TEXT, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 3.06, y: 4.72, w: 1.46, h: 0.56,
  fill: { color: "FBEEDF" }, line: { color: "D0D0D0", width: 1 }, round: 0.12,
});
s.addText("Positive", {
  x: 3.06, y: 4.76, w: 1.46, h: 0.24, align: "center",
  fontSize: 10.5, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("Classified as -ive", {
  x: 3.06, y: 5.00, w: 1.46, h: 0.24, align: "center",
  fontSize: 10.5, color: TEXT, fontFace: FONT, margin: 0,
});
// Pointer lines from formula box down to each bubble
s.addShape(pptx.shapes.LINE, { x: 3.30, y: 4.52, w: -1.10, h: 0.20, line: { color: "808080", width: 1 } });
s.addShape(pptx.shapes.LINE, { x: 3.50, y: 4.52, w: 0.30, h: 0.20, line: { color: "808080", width: 1 } });

// Green brace (cropped from original, white keyed transparent): orig x98-346 y380-408
s.addImage({ path: A + "/brace_012.png", x: 1.36, y: 5.28, w: 3.44444, h: 0.38889 });
s.addText("All Positive Samples in the Dataset", {
  x: 1.22, y: 5.61, w: 3.42, h: 0.30, valign: "middle",
  fontSize: 13, italic: true, underline: true, color: "8B3A3A", fontFace: FONT, margin: 0,
});

// Model box: orig box x57-510 y438-501, thin light-blue border, blue bold-italic line 1
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.79, y: 6.08, w: 6.29, h: 0.88,
  fill: { color: "FFFFFF" }, line: { color: "8EAADB", width: 1 },
});
s.addText("Model Try to catch ALL Positive Samples", {
  x: 0.90, y: 6.14, w: 5.9, h: 0.32, valign: "middle",
  fontSize: 14, bold: true, italic: true, color: "404094", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "(Irrespective of classifying ", options: { fontSize: 13, italic: true, color: TEXT, fontFace: FONT } },
  { text: "NEGATIVE", options: { fontSize: 13, italic: true, bold: true, color: RED, fontFace: FONT } },
  { text: " Objects as Positive)", options: { fontSize: 13, italic: true, color: TEXT, fontFace: FONT } },
], {
  x: 0.90, y: 6.52, w: 5.9, h: 0.30, valign: "middle", margin: 0,
});

// ---- Right column: confusion matrices, explicit measured geometry ----
// Original (px): blue outer box + inner red grid; corner cell spans the header rows;
// vertical red "Actual" sits between blue border and red grid, over the two data rows.
function rect(x, y, w, h, fill, lineColor, lineW) {
  const o = { x, y, w, h };
  if (fill) o.fill = { color: fill };
  if (lineColor) o.line = { color: lineColor, width: lineW || 1 };
  s.addShape(pptx.shapes.RECTANGLE, o);
}
function hline(x, y, w) {
  s.addShape(pptx.shapes.LINE, { x, y, w, h: 0, line: { color: RED, width: 1 } });
}
function vline(x, y, h) {
  s.addShape(pptx.shapes.LINE, { x, y, w: 0, h, line: { color: RED, width: 1 } });
}
function cellText(x, y, w, h, t, opts) {
  s.addText(t, Object.assign({
    x, y, w, h, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: TEXT, fontFace: FONT, margin: 0,
  }, opts || {}));
}
// matrix(gx, gy, gw, gh, cols[3], rowsTop, rowH[3], fills, values, actualCy)
// grid origin (gx,gy); col edges cols = [c1,c2] absolute x; rows: header row (gy..r0), colhdr (r0..r1), data rows (r1..r2, r2..gy+gh)
function matrix(blueX, blueY, blueW, blueH, gx, gy, gw, gh, c1, c2, r0, r1, r2, fills, vals, actualCy) {
  rect(blueX, blueY, blueW, blueH, "FFFFFF", "4472C4", 1.5);       // blue outer border
  const ge = gx + gw, gb = gy + gh;
  // cell fills
  fills.forEach(f => { if (f.fill) rect(f.x, f.y, f.w, f.h, f.fill); });
  // red grid lines
  vline(gx, gy, gh); vline(c1, gy, gh); vline(c2, gy, gh); vline(ge, gy, gh);
  hline(gx, gy, gw); hline(c1, r0, ge - c1); hline(gx, r1, gw); hline(gx, r2, gw); hline(gx, gb, gw);
  // header texts
  cellText(c1, gy, ge - c1, r0 - gy, "Predicted as", { fontSize: 11, bold: true, color: RED });
  cellText(c1, r0, c2 - c1, r1 - r0, vals[0][0], { fontSize: 11 });
  cellText(c2, r0, ge - c2, r1 - r0, vals[0][1], { fontSize: 11 });
  cellText(gx, r1, c1 - gx, r2 - r1, vals[1][0], { fontSize: 11 });
  cellText(gx, r2, c1 - gx, gb - r2, vals[1][1], { fontSize: 11 });
  cellText(c1, r1, c2 - c1, r2 - r1, vals[2][0], {});
  cellText(c2, r1, ge - c2, r2 - r1, vals[2][1], {});
  cellText(c1, r2, c2 - c1, gb - r2, vals[3][0], {});
  cellText(c2, r2, ge - c2, gb - r2, vals[3][1], {});
  // vertical red "Actual" between blue border and red grid, centered over data rows
  const aw = (gb - r1); // unrotated width = data rows height
  cellText(blueX + (gx - blueX) / 2 - aw / 2, actualCy - 0.12, aw, 0.24, "Actual",
    { rotate: 270, fontSize: 10, bold: true, color: RED });
}
// Matrix 1 (orig px): blue x674-868 y53-158; red grid x699-846 y53-151; col edges 738,790; row edges 72,98,125
const M1 = {
  blueX: 674 / 72, blueY: 53 / 72, blueW: 194 / 72, blueH: 105 / 72,
  gx: 699 / 72, gy: 53 / 72, gw: 147 / 72, gh: 98 / 72,
  c1: 738 / 72, c2: 790 / 72, r0: 72 / 72, r1: 98 / 72, r2: 125 / 72,
};
matrix(M1.blueX, M1.blueY, M1.blueW, M1.blueH, M1.gx, M1.gy, M1.gw, M1.gh, M1.c1, M1.c2, M1.r0, M1.r1, M1.r2,
  [ { x: M1.c1, y: M1.r1, w: M1.c2 - M1.c1, h: M1.r2 - M1.r1, fill: "84FC00" },
    { x: M1.c2, y: M1.r2, w: M1.gx + M1.gw - M1.c2, h: M1.gy + M1.gh - M1.r2, fill: "84FC00" } ],
  [["P", "N"], ["P", "N"], ["TP", "FN"], ["FP", "TN"]],
  (M1.r1 + M1.gy + M1.gh) / 2);
// Matrix 2 (orig px): blue x673-867 y168-288; red grid x704-857 y168-283; col edges 747,800; row edges 190,219,252
const M2 = {
  blueX: 673 / 72, blueY: 168 / 72, blueW: 194 / 72, blueH: 120 / 72,
  gx: 704 / 72, gy: 168 / 72, gw: 153 / 72, gh: 115 / 72,
  c1: 747 / 72, c2: 800 / 72, r0: 190 / 72, r1: 219 / 72, r2: 252 / 72,
};
matrix(M2.blueX, M2.blueY, M2.blueW, M2.blueH, M2.gx, M2.gy, M2.gw, M2.gh, M2.c1, M2.c2, M2.r0, M2.r1, M2.r2,
  [ { x: M2.c1, y: M2.r1, w: M2.c2 - M2.c1, h: M2.r2 - M2.r1, fill: "FBD7B3" },
    { x: M2.c2, y: M2.r1, w: M2.gx + M2.gw - M2.c2, h: M2.r2 - M2.r1, fill: "FBD7B3" },
    { x: M2.c2, y: M2.r2, w: M2.gx + M2.gw - M2.c2, h: M2.gy + M2.gh - M2.r2, fill: "84FC00" } ],
  [["P", "N"], ["P", "N"], ["30", "0"], ["70", "0"]],
  (M2.r1 + M2.gy + M2.gh) / 2);
// Blue rounded highlight around the "30" cell (m2, data row P, col P): cell px x747-800 y219-252
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: (743) / 72, y: (215) / 72, w: (61) / 72, h: (41) / 72,
  line: { color: "0000FF", width: 2 }, round: 0.35,
});

// ---- Bottom-right decision trees inside red panel (orig panel x536-905 y~295-503) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 536 / 72, y: 295 / 72, w: 369 / 72, h: 208 / 72,
  line: { color: RED, width: 1.5 },
});
s.addText("Positive", {
  x: 7.90, y: 4.10, w: 1.60, h: 0.26, align: "center",
  fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Negative", {
  x: 10.30, y: 4.10, w: 1.60, h: 0.26, align: "center",
  fontSize: 15, bold: true, color: "00B050", fontFace: FONT, margin: 0,
});
// Airplane icons (cropped from original frame)
s.addImage({ path: A + "/icon_012_left.png", x: 7.57, y: 4.40, w: 2.09722, h: 1.19444 });
s.addImage({ path: A + "/icon_012_right.png", x: 10.58, y: 4.40, w: 1.44444, h: 1.19444 });
// Panels behind trees: positive side solid yellow (orig ~x545-700 y380-500), negative side none
s.addShape(pptx.shapes.RECTANGLE, {
  x: 545 / 72, y: 380 / 72, w: 155 / 72, h: 120 / 72, fill: { color: "FCFF9C" }, line: { color: "FCFF9C", width: 0.5 },
});
// Connectors: positive tree gray, negative tree blue (measured from original)
function link(x1, y1, x2, y2, color) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  s.addShape(pptx.shapes.LINE, {
    x: x, y: y, w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipV: y2 < y1, flipH: x2 < x1,
    line: { color: color, width: 1.25 },
  });
}
link(8.60, 5.55, 7.96, 6.38, "808080");
link(8.60, 5.55, 9.18, 6.40, "808080");
link(11.11, 5.52, 10.47, 6.40, "0000FF");
link(11.11, 5.52, 11.74, 6.38, "0000FF");
function node(cx, cy, fill, label, val) {
  const d = 0.42;
  s.addShape(pptx.shapes.OVAL, {
    x: cx - d / 2, y: cy - d / 2, w: d, h: d,
    fill: { color: fill }, line: { color: fill, width: 1 },
  });
  s.addText(val, {
    x: cx - d / 2, y: cy - d / 2, w: d, h: d, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
  if (label) {
    s.addText(label, {
      x: cx - 0.3, y: cy + d / 2 + 0.02, w: 0.6, h: 0.25, align: "center",
      fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0,
    });
  }
}
node(8.60, 5.55, "C1610A", "", "30");       // Positive root
node(7.96, 6.38, "C1610A", "TP", "30");     // TP
node(9.18, 6.40, "0F8539", "FN", "0");      // FN
node(11.11, 5.52, "0F8539", "", "70");      // Negative root
node(10.47, 6.40, "0F8539", "TN", "0");     // TN
node(11.74, 6.38, "790D1A", "FP", "70");    // FP
// Small red dot beside the Negative root "70"
s.addShape(pptx.shapes.OVAL, {
  x: 11.62, y: 5.46, w: 0.12, h: 0.12,
  fill: { color: "C00000" }, line: { color: "C00000", width: 0.5 },
});

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_012_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done"));
