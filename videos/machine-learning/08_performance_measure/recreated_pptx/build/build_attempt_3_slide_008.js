// slide_008 — "Precision" (08_performance_measure). All geometry measured from
// unique_slides/slide_008.jpg (960x540 px, 1px = 1pt = 1/72 in). P = px/72.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", INK = "000000", BADGE = "FFF9C4", NUM = "333333";
const BLUE = "0070C0", FRAME_BLUE = "0000CC", GREEN = "7CFC00", GRN_TXT = "45B144";
const PURPLE = "7030A0", DOTRED = "F13148", ARROW_BLUE = "0000FF";
const FONT = "Arial";
const P = (px) => px / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE CHROME (root AGENTS.md 2026-10-09) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 }
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("8", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("Precision", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.6, align: "center", valign: "middle",
  fontSize: 46, bold: true, color: RED, fontFace: FONT, margin: 0
});

// --- DEFINITION BAND (gray) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(67), y: P(112), w: P(573), h: P(63),
  fill: { color: "CBCDCA" }, line: { color: "CBCDCA", width: 0.5 }
});
s.addText("Correctly Classified (as Positive)", {
  x: P(67), y: P(118), w: P(573), h: P(22), align: "center", valign: "middle",
  fontSize: 19, bold: true, color: INK, fontFace: FONT, margin: 0
});
s.addShape(pptx.shapes.RECTANGLE, { // red rule
  x: P(81), y: P(139), w: P(558), h: P(3),
  fill: { color: RED }, line: { color: RED, width: 0.5 }
});
s.addText("Total Classified as Positive (either Correct and Erroneous)", {
  x: P(67), y: P(151), w: P(573), h: P(21), align: "center", valign: "middle",
  fontSize: 19, bold: true, color: INK, fontFace: FONT, margin: 0
});

// --- MEANING BAND (pale yellow) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(67), y: P(199), w: P(558), h: P(57),
  fill: { color: "F7FBD6" }, line: { color: "F7FBD6", width: 0.5 }
});
s.addText("Meaning", {
  x: P(80), y: P(205), w: P(92), h: P(25), align: "left", valign: "middle",
  fontSize: 22, bold: true, color: RED, fontFace: FONT, margin: 0
});
s.addText([
  { text: "% of what you ", options: { fontSize: 16, bold: true, charSpacing: 1, color: INK, fontFace: FONT, breakLine: false } },
  { text: "Predicted", options: { fontSize: 16, bold: true, underline: true, charSpacing: 1, color: RED, fontFace: FONT, breakLine: false } },
  { text: " as ", options: { fontSize: 16, bold: true, charSpacing: 1, color: INK, fontFace: FONT, breakLine: false } },
  { text: "POSITIVE", options: { fontSize: 16, bold: true, charSpacing: 2, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: " is Actually Positive", options: { fontSize: 16, bold: true, charSpacing: 1, color: INK, fontFace: FONT, breakLine: false } }
], {
  x: P(76), y: P(228), w: P(548), h: P(24), align: "left", valign: "middle",
  margin: 0, lineSpacing: 20, isTextBox: true, wrap: false
});

// --- FORMULA BOX (white, red outline) ---
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(67), y: P(262), w: P(249), h: P(60),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2.25 }
});
s.addText("Precision =", {
  x: P(86), y: P(283), w: P(140), h: P(30), align: "left", valign: "middle",
  fontSize: 20, bold: true, color: INK, fontFace: FONT, margin: 0
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_008_frac_v2.png",
  x: P(212), y: P(274), w: 1.15167, h: 0.56333
});

// --- WORKED EXAMPLE BOX (pale blue, two lines) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(335), y: P(290), w: P(193), h: P(44),
  fill: { color: "F0FFFF" }, line: { color: "9DC3E6", width: 1 }
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_008_worked_v2.png",
  x: P(345), y: P(291), w: 1.98833, h: 0.58667
});

// --- CALLOUT BOXES ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(114), y: P(336), w: P(98), h: P(40),
  fill: { color: "FFF2CC" }, line: { color: "FFD966", width: 0.75 }
});
s.addText([
  { text: "Positive", options: { fontSize: 11, bold: true, color: INK, fontFace: FONT, breakLine: true } },
  { text: "Classified as +ive", options: { fontSize: 11, bold: true, color: INK, fontFace: FONT, breakLine: false } }
], {
  x: P(114), y: P(336), w: P(98), h: P(40), align: "center", valign: "middle",
  margin: 0, lineSpacing: 15
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(222), y: P(336), w: P(98), h: P(40),
  fill: { color: "FCE4D6" }, line: { color: "F4B183", width: 0.75 }
});
s.addText([
  { text: "Negative", options: { fontSize: 11, bold: true, color: INK, fontFace: FONT, breakLine: true } },
  { text: "Classified as +ive", options: { fontSize: 11, bold: true, color: INK, fontFace: FONT, breakLine: false } }
], {
  x: P(222), y: P(336), w: P(98), h: P(40), align: "center", valign: "middle",
  margin: 0, lineSpacing: 15
});

// --- callout pointer tails (triangles up toward the formula box) ---
s.addShape("triangle", {
  x: P(148), y: P(323), w: P(16), h: P(13),
  fill: { color: "FFF2CC" }, line: { color: "FFD966", width: 0.75 }
});
s.addShape("triangle", {
  x: P(256), y: P(323), w: P(16), h: P(13),
  fill: { color: "FCE4D6" }, line: { color: "F4B183", width: 0.75 }
});

// --- GREEN BRACE under the callout boxes + RED italic caption below it ---
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/brace_008.png",
  x: P(108), y: P(385), w: P(224), h: P(16)
});
s.addText([
  { text: "All Samples classified as ", options: { fontSize: 14, italic: true, color: RED, fontFace: FONT, breakLine: false } },
  { text: "Positive", options: { fontSize: 14, italic: true, bold: true, color: RED, fontFace: FONT, breakLine: false } }
], {
  x: P(79), y: P(411), w: P(232), h: P(18), align: "left", valign: "middle",
  margin: 0, wrap: false
});

// --- BLUE NOTE BOX ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(72), y: P(431), w: P(427), h: P(89),
  fill: { color: "D2F4F4" }, line: { color: "2E75B6", width: 1.25 }
});
s.addText([
  { text: "Higher Precision value ", options: { fontSize: 15, italic: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "DOES NOT", options: { fontSize: 15, italic: true, bold: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: " mean you correctly retrieved ", options: { fontSize: 15, italic: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "more", options: { fontSize: 15, italic: true, bold: true, underline: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: " Positive samples.", options: { fontSize: 15, italic: true, color: BLUE, fontFace: FONT, breakLine: true } },
  { text: "It means I ", options: { fontSize: 15, italic: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "HIGHLY", options: { fontSize: 15, italic: true, bold: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: " trust you if you said this sample is ", options: { fontSize: 15, italic: true, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "Positive", options: { fontSize: 15, italic: true, bold: true, color: RED, fontFace: FONT, breakLine: false } }
], {
  x: P(79), y: P(435), w: P(412), h: P(76), align: "left", valign: "top",
  margin: 0, lineSpacing: 19
});

// --- helpers for matrices ---
function vline(x, y0, y1) {
  s.addShape(pptx.shapes.RECTANGLE, { x: P(x), y: P(y0), w: P(2), h: P(y1 - y0), fill: { color: RED }, line: { color: RED, width: 0.25 } });
}
function hline(y, x0, x1) {
  s.addShape(pptx.shapes.RECTANGLE, { x: P(x0), y: P(y), w: P(x1 - x0), h: P(2), fill: { color: RED }, line: { color: RED, width: 0.25 } });
}
function cellText(x, y, w, h, t) {
  s.addText(t, {
    x: P(x), y: P(y), w: P(w), h: P(h), align: "center", valign: "middle",
    fontSize: 15, bold: true, color: INK, fontFace: FONT, margin: 0
  });
}

// --- MATRIX 1 (labels) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(673), y: P(53), w: P(194), h: P(105),
  fill: { color: "FFFFFF" }, line: { color: FRAME_BLUE, width: 1.5 }
});
s.addText("Predicted as", {
  x: P(738), y: P(58), w: P(106), h: P(18), align: "center", valign: "middle",
  fontSize: 13, bold: true, color: RED, fontFace: FONT, margin: 0
});
vline(697, 82, 150); vline(740, 82, 150); vline(790, 82, 150); vline(845, 82, 150);
hline(82, 697, 845); hline(98, 697, 845); hline(124, 697, 845); hline(150, 697, 845);
cellText(740, 84, 50, 14, "P");
cellText(790, 84, 55, 14, "N");
cellText(697, 100, 43, 24, "P");
cellText(697, 127, 43, 23, "N");
// Actual rotated 90, inside the panel left of the grid (orig ink x~683-691)
s.addText("Actual", {
  x: P(674), y: P(118), w: P(30), h: P(14), rotate: 270,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0
});
// cells: TP green, FN white, FP white, TN green
s.addShape(pptx.shapes.RECTANGLE, { x: P(741), y: P(99), w: P(48), h: P(24), fill: { color: GREEN }, line: { color: GREEN, width: 0.25 } });
cellText(740, 100, 50, 24, "TP");
cellText(790, 100, 55, 24, "FN");
cellText(740, 127, 50, 23, "FP");
s.addShape(pptx.shapes.RECTANGLE, { x: P(791), y: P(125), w: P(53), h: P(24), fill: { color: GREEN }, line: { color: GREEN, width: 0.25 } });
cellText(790, 127, 55, 23, "TN");

// --- TREE PANEL (red frame) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(536), y: P(290), w: P(346), h: P(212),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 }
});
s.addText("Positive", {
  x: P(598), y: P(290), w: P(70), h: P(15), align: "left", valign: "middle",
  fontSize: 14, bold: true, color: RED, fontFace: FONT, margin: 0
});
s.addText("Negative", {
  x: P(774), y: P(291), w: P(79), h: P(16), align: "left", valign: "middle",
  fontSize: 14, bold: true, color: "00B050", fontFace: FONT, margin: 0
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/doodle_008_L.png",
  x: P(588), y: P(318), w: P(84), h: P(57)
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/doodle_008_R.png",
  x: P(764), y: P(318), w: P(90), h: P(50)
});
// branch arrows (thin blue lines)
function arrow(x0, y0, x1, y1) {
  const dx = x1 - x0, dy = y1 - y0;
  const len = Math.hypot(dx, dy);
  const ang = Math.atan2(dy, dx) * 180 / Math.PI;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P((x0 + x1) / 2 - len / 2), y: P((y0 + y1) / 2 - 0.75), w: P(len), h: P(1.5),
    rotate: ang, fill: { color: ARROW_BLUE }, line: { color: ARROW_BLUE, width: 0.25 }
  });
}
arrow(619, 394, 574, 456); arrow(619, 394, 661, 457);
arrow(800, 393, 754, 457); arrow(800, 393, 846, 457);
// node circles
function node(x, y, label, fill) {
  s.addShape(pptx.shapes.OVAL, {
    x: P(x), y: P(y), w: P(33), h: P(33),
    fill: { color: fill }, line: { color: fill, width: 0.5 }
  });
  s.addText(label, {
    x: P(x), y: P(y), w: P(33), h: P(33), align: "center", valign: "middle",
    fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0
  });
}
node(603, 379, "30", RED);
node(558, 441, "10", RED);
node(644, 442, "20", "00B050");
node(783, 378, "70", "00B050");
node(738, 442, "68", "00B050");
node(830, 442, "2", RED);
// solid red dot
s.addShape(pptx.shapes.OVAL, {
  x: P(603), y: P(477), w: P(23), h: P(23),
  fill: { color: DOTRED }, line: { color: DOTRED, width: 0.5 }
});
// TP/FN/TN/FP captions
function cap(x, t) {
  s.addText(t, {
    x: P(x), y: P(481), w: P(40), h: P(16), align: "center", valign: "middle",
    fontSize: 11, bold: true, color: INK, fontFace: FONT, margin: 0
  });
}
cap(554, "TP"); cap(641, "FN"); cap(734, "TN"); cap(826, "FP");
// hollow red down-arrows flanking the panel (orig y~408-445)
s.addShape(pptx.shapes.RECTANGLE, { x: P(556), y: P(408), w: P(2), h: P(30), fill: { color: RED }, line: { color: RED, width: 0.25 } });
s.addShape("triangle", {
  x: P(551), y: P(436), w: P(12), h: P(9), rotate: 170,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.25 }
});
s.addShape(pptx.shapes.RECTANGLE, { x: P(866), y: P(408), w: P(2), h: P(30), fill: { color: RED }, line: { color: RED, width: 0.25 } });
s.addShape("triangle", {
  x: P(861), y: P(436), w: P(12), h: P(9), rotate: 190,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.25 }
});

// --- MATRIX 2 (numbers) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(673), y: P(168), w: P(194), h: P(120),
  fill: { color: "FFFFFF" }, line: { color: FRAME_BLUE, width: 1.5 }
});
s.addText("Predicted as", {
  x: P(738), y: P(172), w: P(106), h: P(16), align: "center", valign: "middle",
  fontSize: 13, bold: true, color: RED, fontFace: FONT, margin: 0
});
vline(697, 192, 282); vline(740, 192, 282); vline(790, 192, 282); vline(845, 192, 282);
hline(190, 697, 845); hline(220, 697, 845); hline(252, 697, 845); hline(282, 697, 845);
cellText(740, 194, 50, 24, "P");
cellText(790, 194, 55, 24, "N");
cellText(697, 220, 43, 32, "P");
cellText(697, 252, 43, 30, "N");
s.addText("Actual", {
  x: P(680), y: P(246), w: P(30), h: P(14), rotate: 270,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0
});
// 10 inside a solid purple filled circle, white text (as in original), contained in the TP cell
s.addShape(pptx.shapes.OVAL, {
  x: P(752), y: P(223), w: P(34), h: P(27),
  fill: { color: PURPLE }, line: { color: PURPLE, width: 0.5 }
});
s.addText("10", {
  x: P(752), y: P(223), w: P(34), h: P(27), align: "center", valign: "middle",
  fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0
});
cellText(790, 220, 55, 32, "20");
// 2 in purple rounded-rect outline
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(748), y: P(255), w: P(34), h: P(24),
  fill: { color: "FFFFFF" }, line: { color: PURPLE, width: 1.5 }
});
cellText(740, 252, 50, 30, "2");
// 68 green
s.addShape(pptx.shapes.RECTANGLE, { x: P(791), y: P(253), w: P(53), h: P(28), fill: { color: GREEN }, line: { color: GREEN, width: 0.25 } });
cellText(790, 252, 55, 30, "68");

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_008_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
