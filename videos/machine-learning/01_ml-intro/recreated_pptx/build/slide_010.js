// Slide 010 recreation — "Supervised Learning"
// Spec: analysis/slide_010_final.json
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const WHITE = "FFFFFF", GRAY = "D9D9D9", RED = "C00000", BLACK = "000000", YELLOW = "FFF2CC";
const BADGE_YELLOW = "FFF9C4", BADGE_INK = "333333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: "E8E8E8" }; // house-template background (founder rule)

// --- Gray header band across the top (~top 15% of the slide) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0, y: 0, w: W, h: 1.1,
  fill: { color: GRAY }, line: { color: GRAY, width: 0 },
});

// --- Title: HOUSE FRAME text box starts y:0.28, x:0.6, w:12.13, align center ---
s.addText("Supervised Learning", {
  x: 0.6, y: 0.28, w: W - 1.2, h: 1.1, align: "center", valign: "middle",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// --- HOUSE FRAME slide-number badge: oval x:12.48 y:0.30 w:0.5 h:0.5,
//      fill FFF9C4, line FFF9C4 width 0.5; digit = slide id "10", bold 18pt, 333333 ---
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("10", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_INK, fontFace: FONT, margin: 0,
});

// --- White content area framed by a thin red border (below the header) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.35, y: 1.4, w: W - 0.7, h: 5.75,
  fill: { color: WHITE }, line: { color: RED, width: 1.75 },
});

// --- Body lines inside the red content box ---
const TX = 0.85, TW = 11.6, FS = 24;
function leadLine(y, lead, rest, h) {
  const runs = [{ text: lead, options: { bold: true, color: BLACK, fontFace: FONT } }];
  for (const r of rest) {
    runs.push({
      text: r.t,
      options: {
        color: BLACK, fontFace: FONT,
        subscript: !!r.sub,
      },
    });
  }
  s.addText(runs, {
    x: TX, y, w: TW, h: h || 0.55, fontSize: FS, valign: "top",
    align: "left", margin: 0,
  });
}

// Given: N labeled training examples {(x_1, y_1), . . . , (x_N, y_N)}
leadLine(1.75, "Given: ", [
  { t: "N labeled training examples {(x" }, { t: "1", sub: true },
  { t: ", y" }, { t: "1", sub: true },
  { t: "), . . . , (x" }, { t: "N", sub: true },
  { t: ", y" }, { t: "N", sub: true },
  { t: ")}" },
]);

// Goal: learn a model that predicts the label y for a test example x
leadLine(2.45, "Goal: ", [
  { t: "learn a model that predicts the label y for a test example x" },
]);

// Assumption: The training and the test examples are drawn from the same data distribution
leadLine(3.15, "Assumption: ", [
  { t: "The training and the test examples are drawn from the same data distribution" },
], 1.05);

// Things to keep in mind: (bold)
s.addText("Things to keep in mind:", {
  x: TX, y: 4.25, w: TW, h: 0.55, fontSize: FS, bold: true, color: BLACK,
  fontFace: FONT, align: "left", valign: "top", margin: 0,
});

// Bulleted list: 3 items + a fourth empty bullet dot (mid-build state)
const bu = { code: "2022", indent: 12 };
const bullets = [
  "No single learning algorithm is universally good (\"no free lunch\")",
  "Different learning algorithms work with different assumptions",
  "Generalization is particularly important for supervised learning",
  " ", // fourth empty bullet dot
];
s.addText(
  bullets.map((t, i) => ({
    text: t,
    options: { bullet: bu, breakLine: i < bullets.length - 1 },
  })),
  {
    x: TX + 0.15, y: 4.95, w: TW - 0.15, h: 2.1, fontSize: FS, color: BLACK,
    fontFace: FONT, align: "left", valign: "top", margin: 0,
    paraSpaceAfter: 10,
  }
);

// --- HOUSE FRAME outer red frame (founder directive 2026-10-09): 0.15in inset
//     from every edge, line C00000 width 1.5, no visible fill (drawn last, on top) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_010_recreated.pptx" })
  .then(() => console.log("done"));
