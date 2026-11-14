const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", REDLINE = "FF0000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const GREEN = "0E8641", LIME = "89FF0D", NODERED = "A10003", TXTBLUE = "4847AE", BOTTOMBLUE = "2A37A4";
const ARROWBLUE = "5D58A7", PANELBLUE = "221878", GRAYBAND = "D3D4D3", MEANINGFILL = "F7FBD6";
const PRECFILL = "F0FFFD", CALLOUT1 = "FCFFE2", CALLOUT2 = "F6E2CF", ARROWY = "E0C000";
const PEACH = "F8D8D1", ORANGE = "FFC19C", PURPLE = "7030A0";
const FONT = "Arial";
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";
const A = NS + "/recreated_pptx/build/assets";
// original frame is 960x540 px, 1px = 1/72 in
const P = (px) => px / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE CHROME
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { color: BG }, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 } });
s.addText("10", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0 });
s.addText("Recall", { x: 0.6, y: 0.28, w: 12.13, h: 0.5, align: "center", valign: "middle", fontSize: 40, bold: true, color: RED, fontFace: FONT, margin: 0 });

// 1. GRAY DEFINITION BAND (orig panel x70-656 y111-175; rule x81-643 y139-142; text centered on panel)
s.addShape(pptx.shapes.RECTANGLE, { x: P(70), y: P(111), w: P(586), h: P(64), fill: { color: GRAYBAND }, line: { color: "BFBFBF", width: 0.75 } });
s.addText("Correctly Classified (as Positive)", { x: P(70), y: P(122), w: P(586), h: P(17), fontSize: 20, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center" });
s.addShape(pptx.shapes.LINE, { x: P(81), y: P(139), w: P(562), h: 0, line: { color: RED, width: 2 } });
s.addText("Total objects that should be retrieved (Actually Positive)", { x: P(70), y: P(152), w: P(586), h: P(20), fontSize: 21, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center" });

// 2. MEANING PANEL (orig x70-617 y199-258)
s.addShape(pptx.shapes.RECTANGLE, { x: P(70), y: P(199), w: P(547), h: P(59), fill: { color: MEANINGFILL }, line: { color: "D0C000", width: 0.75 } });
s.addText("Meaning", { x: P(80), y: P(207), w: P(160), h: P(28), fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0 });
s.addText([
  { text: "Does the classifier " },
  { text: "miss", options: { color: RED, bold: true, underline: true } },
  { text: " any of " },
  { text: "Positive", options: { color: TXTBLUE, bold: true, underline: true } },
  { text: " Objects ?" }
], { x: P(80), y: P(235), w: P(527), h: P(20), fontSize: 20, bold: true, color: TEXT, fontFace: FONT, margin: 0 });

// 3. RECALL BOX (orig x69-319 y263-323) — "Recall =" left, stacked fraction inside at x203-304 y275-318
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: P(69), y: P(263), w: P(250), h: P(60), fill: { color: "FFFFFF" }, line: { color: REDLINE, width: 2 } });
s.addText("Recall =", { x: P(84), y: P(283), w: P(110), h: P(24), fontSize: 19, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
s.addImage({ path: A + "/eq_010_fraction.png", x: P(203), y: P(275), w: 1.30833, h: 0.54667 });

// 4. PRECISION BOX (orig x335-528 y290-337) — line1 "Precision=" + stacked dfrac, line2 "=60%" at x414-458 y316-330
s.addShape(pptx.shapes.RECTANGLE, { x: P(335), y: P(290), w: P(193), h: P(47), fill: { color: PRECFILL }, line: { color: PANELBLUE, width: 1 } });
s.addText("Precision=", { x: P(341), y: P(297), w: P(70), h: P(15), fontSize: 13, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
s.addImage({ path: A + "/eq_010_precision.png", x: P(408), y: P(290), w: 0.60167, h: 0.37 });
s.addText("=60%", { x: P(414), y: P(317), w: P(44), h: P(13), fontSize: 14, bold: true, color: TXTBLUE, fontFace: FONT, margin: 0, valign: "middle" });

// 5. CALLOUTS (orig boxes x115-212 / x223-320 y346-376) with shafts to denominator tips (220,318) / (295,318)
function callout(x, fill, line2, tipX, boxCx) {
  s.addShape(pptx.shapes.LINE, { x: P(tipX), y: P(320), w: P(boxCx) - P(tipX), h: P(344) - P(320), line: { color: ARROWY, width: 1.5 } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: P(tipX) - 0.08, y: P(318), w: 0.16, h: 0.16, fill: { color: fill }, line: { color: ARROWY, width: 0.5 }, rotate: 180 });
  s.addShape(pptx.shapes.RECTANGLE, { x: x, y: P(346), w: P(97), h: P(30), fill: { color: fill }, line: { color: ARROWY, width: 0.75 } });
  s.addText([{ text: "Positive", options: { breakLine: true } }, { text: line2 }], { x: x + P(2), y: P(347), w: P(93), h: P(28), fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center", valign: "middle", lineSpacing: 13 });
}
callout(P(115), CALLOUT1, "Classified as +ive", 220, 163);
callout(P(223), CALLOUT2, "Classified as -ive", 295, 271);

// 6. GREEN UNDERBRACE (crop of original x108-335 y387-401) + caption (orig x89 y402)
s.addImage({ path: A + "/brace_010.png", x: P(108), y: P(387), w: 3.15278, h: 0.19444 });
s.addText("All Positive Samples in the Dataset", { x: P(52), y: P(404), w: P(320), h: P(16), fontSize: 15, italic: true, color: RED, fontFace: FONT, margin: 0, align: "center" });

// 7. BOTTOM QUESTION BOX (orig x76-498 y462-511)
s.addShape(pptx.shapes.RECTANGLE, { x: P(76), y: P(462), w: P(422), h: P(49), fill: { color: PRECFILL }, line: { color: PANELBLUE, width: 1.5 } });
s.addText([
  { text: "If you said: I picked " },
  { text: "ALL", options: { bold: true } },
  { text: " Positive objects,", options: { breakLine: true } },
  { text: "can I trust you ?   At what %?" }
], { x: P(86), y: P(466), w: P(402), h: P(41), fontSize: 16, italic: true, color: BOTTOMBLUE, fontFace: FONT, margin: 0, align: "left", valign: "middle", lineSpacing: 20 });

// 8. MATRIX PANELS — blue panel border; red grid with row-label column INSIDE the grid;
//    header row (P/N) sits above the grid top line, spanning the two data columns.
//    m1: panel x672-866 y53-157; grid x698-866 y97-151 (vlines 738/790/844, hline 125);
//        header row x738-844 y73-97 (split 790); rule y73 x738-844; "Predicted as" y59-73.
//    m2: panel x672-866 y168-288; grid x704-866 y220-283 (vlines 746/800/856, hline 252);
//        header row x738-844 y190-220 (split 790); rule y190; "Predicted as" y173-187;
//        purple ring x752-850 y223-250 around the top data row.
function matrix(o) {
  s.addShape(pptx.shapes.RECTANGLE, { x: P(o.px), y: P(o.py), w: P(o.pw), h: P(o.ph), fill: { color: "FFFFFF" }, line: { color: PANELBLUE, width: 1.5 } });
  s.addText("Predicted as", { x: P(738), y: P(o.ruleY - 14), w: P(106), h: P(14), fontSize: 16, bold: true, color: REDLINE, fontFace: FONT, align: "center", margin: 0 });
  s.addShape(pptx.shapes.LINE, { x: P(738), y: P(o.ruleY), w: P(106), h: 0, line: { color: REDLINE, width: 1 } });
  // header row outline + split
  s.addShape(pptx.shapes.RECTANGLE, { x: P(738), y: P(o.ruleY), w: P(106), h: P(o.gridY - o.ruleY), line: { color: REDLINE, width: 1 } });
  s.addShape(pptx.shapes.LINE, { x: P(790), y: P(o.ruleY), w: 0, h: P(o.gridY - o.ruleY), line: { color: REDLINE, width: 1 } });
  s.addText("P", { x: P(738), y: P(o.ruleY), w: P(52), h: P(o.gridY - o.ruleY), fontSize: 16, bold: true, color: REDLINE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText("N", { x: P(790), y: P(o.ruleY), w: P(54), h: P(o.gridY - o.ruleY), fontSize: 16, bold: true, color: REDLINE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  // cell fills
  o.cells.forEach((c) => {
    s.addShape(pptx.shapes.RECTANGLE, { x: P(c.x), y: P(c.y), w: P(c.w), h: P(c.h), fill: { color: c.fill } });
  });
  // grid outline + internal lines
  const gw = o.gridX2 - o.gridX, gh = o.gridY2 - o.gridY;
  s.addShape(pptx.shapes.RECTANGLE, { x: P(o.gridX), y: P(o.gridY), w: P(gw), h: P(gh), line: { color: REDLINE, width: 1 } });
  o.vlines.forEach((vx) => s.addShape(pptx.shapes.LINE, { x: P(vx), y: P(o.gridY), w: 0, h: P(gh), line: { color: REDLINE, width: 1 } }));
  o.hlines.forEach((hy) => s.addShape(pptx.shapes.LINE, { x: P(o.gridX), y: P(hy), w: P(gw), h: 0, line: { color: REDLINE, width: 1 } }));
  // purple annotation ring inside the top data row (m2 only)
  if (o.ring) {
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: P(o.ring[0]), y: P(o.ring[1]), w: P(o.ring[2]), h: P(o.ring[3]), line: { color: PURPLE, width: 2 } });
  }
  // row labels P/N inside the leftmost grid column
  s.addText("P", { x: P(o.gridX), y: P(o.gridY), w: P(o.vlines[0] - o.gridX), h: P(o.hlines[0] - o.gridY), fontSize: 15, bold: true, color: REDLINE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText("N", { x: P(o.gridX), y: P(o.hlines[0]), w: P(o.vlines[0] - o.gridX), h: P(o.gridY2 - o.hlines[0]), fontSize: 15, bold: true, color: REDLINE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  // rotated "Actual" label left of the grid, vertically centered on it
  const acx = P(o.actualX), acy = P((o.gridY + o.gridY2) / 2), run = P(o.gridY2 - o.gridY), th = P(12);
  s.addText("Actual", { x: acx - run / 2, y: acy - th / 2, w: run, h: th, fontSize: 13, bold: true, color: REDLINE, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
  // cell values
  o.cells.forEach((c) => {
    s.addText(c.label, { x: P(c.x), y: P(c.y), w: P(c.w), h: P(c.h), fontSize: 16, bold: true, color: TEXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  });
}
matrix({
  px: 672, py: 53, pw: 194, ph: 104,
  ruleY: 73, gridY: 97, gridY2: 151, gridX: 698, gridX2: 845,
  vlines: [738, 790], hlines: [125], actualX: 684,
  cells: [
    { label: "TP", x: 738, y: 97, w: 52, h: 28, fill: LIME },
    { label: "FN", x: 790, y: 97, w: 54, h: 28, fill: "FFFFFF" },
    { label: "FP", x: 738, y: 125, w: 52, h: 26, fill: "FFFFFF" },
    { label: "TN", x: 790, y: 125, w: 54, h: 26, fill: LIME }
  ]
});
matrix({
  px: 672, py: 168, pw: 194, ph: 120,
  ruleY: 190, gridY: 220, gridY2: 283, gridX: 704, gridX2: 856,
  vlines: [746, 800], hlines: [252], actualX: 684, ring: [752, 223, 98, 27],
  cells: [
    { label: "18", x: 746, y: 220, w: 54, h: 32, fill: PEACH },
    { label: "12", x: 800, y: 220, w: 56, h: 32, fill: ORANGE },
    { label: "10", x: 746, y: 252, w: 54, h: 31, fill: "FFFFFF" },
    { label: "60", x: 800, y: 252, w: 56, h: 31, fill: LIME }
  ]
});

// 9. TREE PANEL (red border; orig x537-882 y289-503)
const tpX = P(537), tpY = P(289), tpW = P(345), tpH = P(214);
s.addShape(pptx.shapes.RECTANGLE, { x: tpX, y: tpY, w: tpW, h: tpH, fill: { color: "FFFFFF" }, line: { color: REDLINE, width: 1.5 } });
s.addText("Positive", { x: P(588), y: P(296), w: P(90), h: P(20), fontSize: 18, bold: true, color: RED, fontFace: FONT, align: "center", margin: 0 });
s.addText("Negative", { x: P(767), y: P(296), w: P(90), h: P(20), fontSize: 18, bold: true, color: GREEN, fontFace: FONT, align: "center", margin: 0 });
s.addImage({ path: A + "/plane_010_pos.png", x: P(588), y: P(318), w: 1.25, h: 0.77778 });
s.addImage({ path: A + "/plane_010_neg.png", x: P(764), y: P(318), w: 1.25, h: 0.77778 });

function node(cx, cy, color, label) {
  const d = P(32);
  s.addShape(pptx.shapes.OVAL, { x: P(cx) - d / 2, y: P(cy) - d / 2, w: d, h: d, fill: { color: color }, line: { color: color, width: 1 } });
  s.addText(label, { x: P(cx) - d / 2, y: P(cy) - d / 2, w: d, h: d, fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
}
function arrow(x1, y1, x2, y2) {
  s.addShape(pptx.shapes.LINE, { x: P(x1), y: P(y1), w: P(x2 - x1), h: P(y2 - y1), line: { color: ARROWBLUE, width: 1.5 } });
  const ang = Math.atan2(P(x2 - x1), -P(y2 - y1)) * 180 / Math.PI;
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: P(x2) - 0.08, y: P(y2) - 0.08, w: 0.16, h: 0.16, fill: { color: ARROWBLUE }, line: { color: ARROWBLUE, width: 0.5 }, rotate: ang });
}
node(624, 393, NODERED, "30");
node(808, 393, GREEN, "70");
arrow(624, 409, 578, 441);
arrow(624, 409, 670, 441);
arrow(808, 409, 762, 441);
arrow(808, 409, 854, 441);
node(578, 455, NODERED, "18");
node(670, 455, GREEN, "12");
node(762, 455, GREEN, "60");
node(854, 455, NODERED, "10");
const leafLabels = [[578, "TP", RED], [670, "FN", GREEN], [762, "TN", GREEN], [854, "FP", RED]];
leafLabels.forEach(([cx, t, c]) => {
  s.addText(t, { x: P(cx) - 0.4, y: P(481), w: 0.8, h: P(18), fontSize: 11, bold: true, color: c, fontFace: FONT, align: "center", margin: 0 });
});

const outFile = NS + "/recreated_pptx/slide_010_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done", outFile));
