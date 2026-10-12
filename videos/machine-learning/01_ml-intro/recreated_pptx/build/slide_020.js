const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// HOUSE FRAME (founder rule 2026-10-09): gray bg, red outer frame 0.15in inset,
// badge = slide id numeral "20", title box starts y:0.28.
const BG = "E8E8E8", RED = "C00000", BADGE_YELLOW = "FFF9C4", INK = "333333";
// Slide content spec colors (analysis/slide_020_final.json)
const BOX_RED = "B03040", WHITE = "FFFFFF", TEXT = "000000", BLUE = "0000CC", GREEN = "00B050";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// House outer frame: thin red rectangle, 0.15in inset from every edge
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// Title: red, bold, centered; house title box starts y:0.28 (x:0.6, w:12.13)
s.addText("Reinforcement Learning (RL)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// House slide-number badge: oval x:12.48 y:0.30 w:0.5 h:0.5, numeral = slide id "20"
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("20", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Content box: white interior, thin red/maroon (#B03040) border.
// Original measured geometry: x 1.0-12.3in, y 1.90-7.17in (spec ~x 7-93%, y 22-95%).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.0, y: 1.9, w: 11.3, h: 5.27,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});

// ---------------------------------------------------------------------------
// Eight bullets, 24pt, drawn deterministically: one text box per line at the
// ORIGINAL's measured line positions (tops at 2.04, 2.98, 3.52, 4.06, 4.60,
// 5.54, 6.08, 6.62in; wrapped continuations at 2.44 and 5.00in), plus explicit
// round bullet dots at x~1.53in (original marker position; text starts 1.88in).
// Wrap points are the original's: bullet 1 wraps after "receive" (line 2 =
// "examples"); bullet 5 wraps after "maximizes" (line 2 = "its reward").
// Text box y = line-top - 0.09 (measured cap-top offset for 24pt, valign top).
// ---------------------------------------------------------------------------
const LINE_X = 1.88, LINE_W = 10.0, LINE_H = 0.5;
function line(runs, yTop) {
  const arr = runs.map((r, i) => ({
    text: r.text,
    options: Object.assign(
      { color: TEXT },
      r.options || {},
      i === runs.length - 1 ? {} : { breakLine: false }
    ),
  }));
  s.addText(arr, {
    x: LINE_X, y: yTop - 0.09, w: LINE_W, h: LINE_H,
    fontSize: 24, color: TEXT, fontFace: FONT, margin: 0,
    align: "left", valign: "top",
  });
}
function dot(yTop) {
  s.addText("\u2022", {
    x: 1.45, y: yTop - 0.09, w: 0.3, h: LINE_H,
    fontSize: 24, color: TEXT, fontFace: FONT, margin: 0,
    align: "center", valign: "top",
  });
}

// Bullet 1 — all black; wraps after "receive" like the original
dot(2.04);
line([{ text: "Unlike supervised/unsupervised learning, RL does not receive" }], 2.04);
line([{ text: "examples" }], 2.44);

// Bullet 2 — 'it learns...' in blue
dot(2.98);
line([
  { text: "Rather, " },
  { text: "it learns (gathers experience) by interacting with the world", options: { color: BLUE } },
], 2.98);

// Bullet 3 — all black
dot(3.52);
line([{ text: "Defined by an agent and an environment the agent acts in" }], 3.52);

// Bullet 4 — bold lead words + underlined 'set A...' / 'set S...'
dot(4.06);
line([
  { text: "Agent", options: { bold: true } },
  { text: " has a " },
  { text: "set A of actions", options: { underline: true } },
  { text: ", " },
  { text: "environment", options: { bold: true } },
  { text: " has a " },
  { text: "set S of states", options: { underline: true } },
], 4.06);

// Bullet 5 — wraps after 'maximizes' like the original
dot(4.60);
line([
  { text: "Goal", options: { bold: true } },
  { text: ": " },
  { text: "Find a sequence of actions by the agent that", options: { underline: true } },
  { text: " " },
  { text: "maximizes", options: { bold: true } },
], 4.60);
line([{ text: "its reward", options: { underline: true } }], 5.00);

// Bullet 6
dot(5.54);
line([
  { text: "Output", options: { bold: true } },
  { text: ": A policy which maps states to actions" },
], 5.54);

// Bullet 7 — all black
dot(6.08);
line([{ text: "RL problems always include time as a variable" }], 6.08);

// Bullet 8 — green examples
dot(6.62);
line([
  { text: "Example", options: { bold: true } },
  { text: " problems: " },
  { text: "Chess, Robot control, autonomous driving", options: { color: GREEN } },
], 6.62);

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_020_recreated.pptx" })
  .then(() => console.log("done"));
