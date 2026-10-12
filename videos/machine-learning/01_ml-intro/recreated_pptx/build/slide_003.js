const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", WHITE = "FFFFFF",
      HL_YELLOW = "FFFF00", BADGE_YELLOW = "FFF9C4", INK = "333333", BLUE = "0000CC";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// 1/2. Outer thin red frame inset slightly from all slide edges
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// 3. Title: red, bold, centered close to the top border
s.addText("What is Machine Learning?", {
  x: 0.6, y: 0.28, w: W - 1.2, h: 0.9, align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. Slide-number badge: small yellow circle, top-right corner of slide frame
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("3", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// 5. Content box: white with thin red border (narrower, ends a bit higher,
//    matching the original's proportions)
const boxX = 1.6, boxY = 1.875, boxW = 10.13, boxH = 5.0;
s.addShape(pptx.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// 6. Bold red lead-in inside the content box
s.addText("Machine Learning:", {
  x: 2.0, y: 2.2, w: 9.3, h: 0.5, fontSize: 26, bold: true, color: RED,
  fontFace: FONT, margin: 0, valign: "top",
});

// 7-9. Three bullets: round black markers + hanging indent, with each line
// split exactly at the original slide's wrap points.
const BODY = 20, LINE_H = 0.42, TX = 2.4, TW = 9.0;
const mk = (y) =>
  s.addText("\u2022", {
    x: 2.0, y, w: 0.35, h: LINE_H, fontSize: BODY, color: TEXT,
    fontFace: FONT, margin: 0, valign: "top",
  });
const line = (y, runs) =>
  s.addText(runs, {
    x: TX, y, w: TW, h: LINE_H, fontSize: BODY, fontFace: FONT,
    margin: 0, valign: "top",
  });

// Bullet 1 — original wraps after "(and"
mk(2.95);
line(2.95, [
  { text: "Designing algorithms that can ", options: { color: TEXT } },
  { text: "learn patterns from data", options: { color: TEXT, highlight: HL_YELLOW } },
  { text: " (and", options: { color: TEXT } },
]);
line(2.95 + LINE_H, [
  { text: "exploit them)", options: { color: TEXT } },
]);

// Bullet 2 — original wraps after "the machine"
mk(3.95);
line(3.95, [
  { text: "Approach: ", options: { color: RED, bold: true } },
  { text: "human supplies training examples, the machine", options: { color: TEXT } },
]);
line(3.95 + LINE_H, [
  { text: "learns", options: { color: TEXT } },
]);

// Bullet 3 — original wraps after "legitimate emails and"
mk(4.95);
line(4.95, [
  { text: "Example: ", options: { color: RED, bold: true } },
  { text: "Show the machine a bunch of spam and legitimate emails and", options: { color: TEXT } },
]);
line(4.95 + LINE_H, [
  {
    text: "let it learn to predict if a new email is spam or not",
    options: { color: BLUE },
  },
]);

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_003_recreated.pptx" })
  .then(() => console.log("done"));
