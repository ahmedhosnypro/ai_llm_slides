// Slide 024 — "Data Sets for Model Training" — pptxgenjs recreation (new numbering, attempt 1)
// Spec: videos/ml-intro/analysis/slide_024_final.json (verbatim text, colors per spec)
// Started from the old-id build (build/slide_031.js, old deck id 31 — judge PASS there);
// renumbered badge 31 -> 24 and smoothed the Bezier arrows (12 segments vs 7).
// HOUSE FRAME rule (founder directive 2026-10-09, overrides spec + judge):
//   background E8E8E8, red frame x:0.15 y:0.15 w:13.03 h:7.2 line C00000 w1.5,
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill FFF9C4 line FFF9C4,
//   title text box y:0.28 x:0.6 w:12.13 align center.
// Badge numeral = number printed on the original slide image = 24 (slide_024.jpg).
// Frame/badge/title-y discrepancies are OVERRIDDEN by the house rule.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", INK = "000000", YELLOW = "FFFF00", ARROW = "C00000";
const BLUE = "0000CC", GREEN = "1E7B34", RED = "B00000", FRAME = "C00000";
const BADGE = "FFF9C4", BADGE_INK = "333333", FOOT = "C00000";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE FRAME: outer red frame, 0.15in inset from every edge, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});

// HOUSE FRAME: slide-number badge (yellow circle). Badge numeral = the number printed
// on the original slide image = slide id "24" (no zero-padding — founder directive
// 2026-10-09); slide_024.jpg is named BY that printed number.
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("24", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_INK, fontFace: FONT, margin: 0,
});

// 3. Title: house text box (y:0.28, x:0.6, w:12.13, centered) with the slide's
// own black-box styling: black rectangle behind, bold yellow text, two lines.
const TBW = 4.7, TBH = 1.0;
s.addShape(pptx.shapes.RECTANGLE, {
  x: (W - TBW) / 2, y: 0.28, w: TBW, h: TBH, fill: { color: INK },
});
s.addText(
  [
    { text: "Data Sets for Model", options: { breakLine: true } },
    { text: "Training", options: {} },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: TBH, align: "center", valign: "middle",
    fontSize: 24, bold: true, color: YELLOW, fontFace: FONT, margin: 0,
  }
);

// 4-6. Three colored boxes (row, mid-slide)
const BOX_Y = 3.55, BOX_H = 1.15;
const boxes = [
  { x: 2.00, w: 2.66, fill: BLUE,  l1: "Training",   l2: "(e.g. 75%)",
    c1: "Used to Train the", c2: "Model" },
  { x: 5.33, w: 2.67, fill: GREEN, l1: "Validation", l2: "(e.g. 10%)",
    c1: "Used for Testing during", c2: "Training (Stopping criteria)" },
  { x: 9.06, w: 2.67, fill: RED,   l1: "Testing",    l2: "(e.g. 15%)",
    c1: "Used to test", c2: "the final Model" },
];
for (const b of boxes) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: b.x, y: BOX_Y, w: b.w, h: BOX_H, fill: { color: b.fill },
  });
  s.addText(
    [
      { text: b.l1, options: { breakLine: true } },
      { text: b.l2, options: {} },
    ],
    {
      x: b.x, y: BOX_Y, w: b.w, h: BOX_H, align: "center", valign: "middle",
      fontSize: 18, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
    }
  );
}
// captions: bold black, centered, two lines, slightly wider than the box
for (const b of boxes) {
  const cx = b.x + b.w / 2, cw = 3.4;
  s.addText(
    [
      { text: b.c1, options: { breakLine: true } },
      { text: b.c2, options: {} },
    ],
    {
      x: cx - cw / 2, y: BOX_Y + BOX_H + 0.15, w: cw, h: 0.75,
      align: "center", valign: "top", fontSize: 14, bold: true,
      color: INK, fontFace: FONT, margin: 0,
    }
  );
}

// 7. Connector arrows: thin red, from title-box bottom to each box top.
// Center arrow straight down; outer two curve outward (cubic-Bezier polylines).
function seg(x1, y1, x2, y2, arrow) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  s.addShape(pptx.shapes.LINE, {
    x, y, w, h,
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: ARROW, width: 1.75, endArrowType: arrow ? "triangle" : "none" },
  });
}
function bez(p0, p1, p2, p3, t) {
  const u = 1 - t;
  return {
    x: u * u * u * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t * t * t * p3.x,
    y: u * u * u * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t * t * t * p3.y,
  };
}
const startX = W / 2;                    // 6.665 — title box bottom center
const startY = 0.28 + TBH + 0.06;        // 1.34 — just below black title box
const endY = BOX_Y - 0.03;               // 3.52 — box top
const centers = boxes.map((b) => b.x + b.w / 2);

// center: straight down
seg(startX, startY, startX, endY, true);
// outer: cubic Bezier — leaves title vertically, bows outward, enters box vertically
for (const cx of [centers[0], centers[2]]) {
  const p0 = { x: startX, y: startY };
  const p1 = { x: startX, y: startY + 1.05 };
  const p2 = { x: cx, y: startY + 0.75 };
  const p3 = { x: cx, y: endY };
  const N = 12;
  let prev = p0;
  for (let i = 1; i <= N; i++) {
    const pt = bez(p0, p1, p2, p3, i / N);
    seg(prev.x, prev.y, pt.x, pt.y, i === N);
    prev = pt;
  }
}

// 9. Footer notes: two left-aligned red lines, bottom-left (raised per judge)
s.addText(
  [
    { text: "Annotated and unannotated data", options: { breakLine: true } },
    { text: "Do you have labels for your Dataset ???", options: {} },
  ],
  {
    x: 0.65, y: 5.85, w: 6.5, h: 0.80, align: "left", valign: "top",
    fontSize: 14, color: FOOT, fontFace: FONT, margin: 0, paraSpaceAfter: 4,
  }
);

// 10. No mouse cursor (video artifact) — deliberately not reproduced.
pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_024_recreated.pptx" })
  .then(() => console.log("done"));
