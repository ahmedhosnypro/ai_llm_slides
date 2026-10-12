const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// House template colors (founder directive 2026-10-09) + spec colors for content
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE_YELLOW = "FFF9C4", INK = "333333";
const TITLE_RED = "CC0000", BOX_RED = "B22222", TEXT = "000000", WHITE = "FFFFFF",
      BLUE = "0000CC";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE FRAME (overrides spec): thin red rectangle inset 0.15in from edges
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});

// ---- HOUSE TITLE: red, bold, centered, box starts y 0.28
s.addText("Other Paradigms: Semi-supervised Learning", {
  x: 0.6, y: 0.28, w: W - 1.2, h: 0.9, align: "center", valign: "top",
  fontSize: 30, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ---- HOUSE BADGE: yellow circle with the slide's own number (21), top-right
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("21", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- CONTENT BOX (geometry measured from the original frame, 72px/in):
// white fill, thin firebrick border; x 69-886px, y 136-517px
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.97, y: 1.89, w: 11.33, h: 5.28,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});

// ---- SIX BULLETS (positions measured from the original frame, 72px/in)
// Text left edge 138px = 1.92in; round black markers centered at x 117px = 1.63in.
// Wrap points are the original's own (PIL-measured + OCR-verified):
//   b1 wraps after "the"        -> "better!)"
//   b4 wraps after "labeled"    -> "data?"
//   b6 wraps after "available)" -> "unlabeled data" (blue, underlined, both lines)
const BODY = 25.5;        // font size in pt (tuned so line widths match the original)
const TX = 1.92, TW = 10.4;
const LINE_SP = 30;       // wrapped-line spacing, measured 30px @72dpi

// marker: filled black circle, 0.17in diameter, center x = 1.63in
function marker(cy) {
  s.addShape(pptx.shapes.OVAL, {
    x: 1.545, y: cy - 0.085, w: 0.17, h: 0.17, fill: { color: TEXT },
  });
}

// bullet text block; lines = array of run-arrays (each inner array = one visual line)
function bullet(yTop, lines, opts) {
  const o = Object.assign({ color: TEXT, underline: false, bold: false }, opts || {});
  const runs = [];
  lines.forEach((ln, i) => {
    if (typeof ln === "string") {
      runs.push({ text: ln, options: {
        color: o.color, bold: o.bold, underline: o.underline,
        breakLine: i < lines.length - 1,
      }});
    } else {
      // line given as run list (for mixed bold prefix)
      ln.forEach((r, j) => runs.push({
        text: r.text,
        options: {
          color: r.color || o.color, bold: !!r.bold, underline: o.underline,
          breakLine: i < lines.length - 1 && j === ln.length - 1,
        },
      }));
    }
  });
  s.addText(runs, {
    x: TX, y: yTop, w: TW, h: 0.45 + (lines.length - 1) * 0.42,
    fontSize: BODY, fontFace: FONT, margin: 0, valign: "top",
    lineSpacing: LINE_SP,
  });
}

// b1 — top of line 1 at 165px (2.29in), marker center 174px (2.42in)
// (text y is shifted -0.10in: LibreOffice adds ~0.09in of line-box leading)
marker(2.42);
bullet(2.19, [
  "Supervised Learning requires labeled data (the more, the",
  "better!)",
]);

// b2 — top 236px (3.28in), marker center 245px (3.40in); bold prefix
marker(3.40);
bullet(3.18, [[
  { text: "Problem 1:", bold: true },
  { text: " Labeling is expensive (usually done by humans)" },
]]);

// b3 — top 278px (3.86in), marker center 286px (3.98in); bold prefix
marker(3.98);
bullet(3.76, [[
  { text: "Problem 2:", bold: true },
  { text: " Sometimes labels are really hard to get" },
]]);

// b4 — top 319px (4.43in), marker center 327px (4.55in); wraps to "data?"
marker(4.55);
bullet(4.33, [
  "How can we learn well even with small amounts of labeled",
  "data?",
]);

// b5 — top 390px (5.42in), marker center 399px (5.54in)
marker(5.54);
bullet(5.32, [
  "One answer: Semi-supervised Learning",
]);

// b6 — top 432px (6.00in), marker center 440px (6.12in); blue hyperlink style
marker(6.12);
bullet(5.90, [
  "Using small amount of labeled + plenty of (freely available)",
  "unlabeled data",
], { color: BLUE, underline: true });

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_021_recreated.pptx" })
  .then(() => console.log("done"));
