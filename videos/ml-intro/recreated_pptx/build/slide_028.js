// Slide 028 recreation — "Data Representation" (categorical -> one-hot encoding)
// Spec: videos/ml-intro/analysis/slide_028_final.json (verbatim text, layout, colors)
// Validation: PASS_WITH_FIXES, score 9 (glm-5.3)
// Geometry measured from the original frame videos/ml-intro/unique_slides/slide_028.jpg
// (960x540 px == 13.33x7.5in at 72 px/in).
// House frame rule (founder directive 2026-10-09) overrides spec for outer chrome:
// bg E8E8E8, red frame 0.15in inset, badge oval 12.48/0.30/0.5/0.5 with numeral 28,
// title box y:0.28 x:0.6 w:12.13 centered.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// palette constants from the spec JSON (+ house chrome colors)
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE_YELLOW = "FFF9C4", INK = "333333";
const TITLE_RED = "CC0000", BAND_GRAY = "DDDDDD", WHITE = "FFFFFF", BLACK = "000000";
const BLUE = "0000CC", GREEN = "009900", MAGENTA = "FF99FF", ORANGE = "FFCC99",
      LGREEN = "99FF99", LEGEND_FILL = "FFFFCC", GRAY_LINE = "A6A6A6";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---------- HOUSE CHROME ----------
// outer red frame, 0.15in inset, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});
// light gray header band (original: full-width band behind the title, to y=1.74in)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.16, y: 0.16, w: W - 0.32, h: 1.58,
  fill: { color: BAND_GRAY }, line: { color: BAND_GRAY, width: 0.5 },
});
// house title (y 0.28, x 0.6, w 12.13, centered), red bold per spec
s.addText("Data Representation", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "top",
  fontSize: 30, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});
// house slide-number badge: oval 12.48/0.30/0.5/0.5, numeral 28 (original printed number)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("28", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---------- CONTENT BOX ----------
// original: white area x 0.79-12.53in, y 1.74-7.26in, thin red border
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.79, y: 1.74, w: 11.74, h: 5.52,
  fill: { color: WHITE }, line: { color: TITLE_RED, width: 2.25 },
});

// ---------- BULLETS (verbatim; manual glyphs, no pptxgenjs bullet options) ----------
const BODY = 20;                 // pt, tuned to the original glyph size (~19-21px)
const TX1 = 1.89, TXN = 2.89, TW = 10.3;
const DY = 0.07;                 // LibreOffice line-box leading correction

// level-1 marker: solid black circle, 0.14in, center x 1.58in
function marker1(cy) {
  s.addShape(pptx.shapes.OVAL, {
    x: 1.51, y: cy - 0.07, w: 0.14, h: 0.14, fill: { color: BLACK },
  });
}
// nested marker: solid black circle, 0.11in, center x 2.60in
function markerN(cy) {
  s.addShape(pptx.shapes.OVAL, {
    x: 2.545, y: cy - 0.055, w: 0.11, h: 0.11, fill: { color: BLACK },
  });
}
function bullet(yTop, runs, opts) {
  const o = Object.assign({ x: TX1, color: BLACK, lineSpacing: null }, opts || {});
  const t = {
    x: o.x, y: yTop, w: TW, h: 0.45, fontSize: BODY, fontFace: FONT,
    margin: 0, valign: "top", color: o.color,
  };
  if (o.lineSpacing) t.lineSpacing = o.lineSpacing;
  s.addText(runs, t);
}

// b1 — "Well, we could map Sunny to 0, Overcast to 1, Rainy to 2.."
// (text top 137px=1.90in, marker center 145px=2.02in)
marker1(2.02);
bullet(1.90 - DY, "Well, we could map Sunny to 0, Overcast to 1, Rainy to 2..");

// b2 — "But such a mapping may not always be appropriate" (top 176px)
marker1(2.57);
bullet(2.44 - DY, "But such a mapping may not always be appropriate");

// n1 — nested: "Imagine color being a feature in some data" (top 210px)
markerN(3.04);
bullet(2.92 - DY, "Imagine color being a feature in some data", { x: TXN });

// n2 — nested, colored words: Red=0 red, Blue=1 blue, Green=2 green (top 243px)
markerN(3.49);
bullet(3.38 - DY, [
  { text: "Let's code 3 possible colors as ", options: { color: BLACK } },
  { text: "Red=0,", options: { color: TITLE_RED } },
  { text: " Blue=1,", options: { color: BLUE } },
  { text: " Green=2", options: { color: GREEN } },
], { x: TXN });

// n3 — nested, entirely red: "This implies ..." (top 276px)
markerN(3.94);
bullet(3.83 - DY, "This implies Red is more similar to Blue than to Green !",
  { x: TXN, color: TITLE_RED });

// b3 — Solution bullet, two lines at the original's wrap point
// (line 1 top 313px=4.35in, wraps after "create K"; line 2 top ~337px=4.62in;
//  the tail from "create K" onward is bold red — two boxes for exact placement)
marker1(4.47);
bullet(4.35 - DY, [
  { text: "Solution:", options: { color: BLACK, bold: true } },
  { text: " For a feature with K > 2 possible values, we usually ",
    options: { color: BLACK } },
  { text: "create K", options: { color: TITLE_RED, bold: true } },
]);
bullet(4.62 - DY, [
  { text: "binary features, one for each possible value",
    options: { color: TITLE_RED, bold: true } },
]);

// ---------- LEGEND BOX (bottom-left) ----------
// original: pale-yellow box x 1.24-3.99in, y 5.25-6.92in, no visible border
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.24, y: 5.25, w: 2.75, h: 1.67,
  fill: { color: LEGEND_FILL }, line: { color: LEGEND_FILL, width: 0.5 },
});
// six two-column lines; label column x 1.35in, value column x 2.22in, ~10pt
const LEG = 10, LDY = 0.04;
function leg(yTop, x, text, color) {
  s.addText(text, {
    x, y: yTop - LDY, w: 1.7, h: 0.24, fontSize: LEG, color, fontFace: FONT,
    margin: 0, valign: "top",
  });
}
leg(5.31, 1.35, "Replace", TITLE_RED);
leg(5.53, 1.35, "Out", BLACK);
leg(5.53, 2.22, "Outlook", BLACK);
leg(6.00, 1.35, "With", TITLE_RED);
leg(6.22, 1.35, "S", BLACK);
leg(6.22, 2.22, "Sunny", BLACK);
leg(6.47, 1.35, "O", BLACK);
leg(6.47, 2.22, "Overcast", BLACK);
leg(6.70, 1.35, "R", BLACK);
leg(6.70, 2.22, "Rainy", BLACK);

// ---------- ENCODING DIAGRAM (bottom-center/right) ----------
const NB = { type: "none" };
const noBorder = [NB, NB, NB, NB];
const TF = 9;                     // table font pt (original cell text ~8-10px)
const cellMargin = 0.02;

function cells(values, opts) {
  // one column's cells: values[0] = header text
  const o = Object.assign({ fill: WHITE, color: BLACK, bold: false }, opts || {});
  return values.map((v, i) => ({
    text: v,
    options: {
      fill: { color: o.fill }, color: o.color, bold: i === 0 ? true : o.bold,
      fontFace: FONT, fontSize: TF, align: "center", valign: "middle",
      margin: cellMargin, border: noBorder,
    },
  }));
}
function rowOf(cols, i) {
  return cols.map((c) => c[i]);
}

// left table: headers Y, Out, T, R; x 300px=4.17in, y 372px=5.17in
const yCol   = ["P", "N", "N", "P", "P", "P", "N", "P"];
const outCol = ["Sunny", "Sunny", "Sunny", "Overcast", "Overcast", "Overcast", "Rainy", "Rainy"];
const tCol   = ["Low", "High", "High", "Low", "High", "Low", "Low", "Low"];
const rCol   = ["Yes", "Yes", "No", "Yes", "No", "No", "Yes", "No"];

const ltCols = [
  cells(["Y"].concat(yCol), { color: BLUE }),
  cells(["Out"].concat(outCol), { fill: MAGENTA }),
  cells(["T"].concat(tCol), { fill: ORANGE }),
  cells(["R"].concat(rCol), { fill: LGREEN }),
];
s.addTable([0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => rowOf(ltCols, i)), {
  x: 4.17, y: 5.17, w: 2.67,
  colW: [0.50, 0.94, 0.67, 0.56],
  rowH: 0.214,
});

// red rightward arrow between the tables (original ~x 512-545px, y 432-441px)
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 7.11, y: 5.98, w: 0.46, h: 0.16,
  fill: { color: TITLE_RED }, line: { color: TITLE_RED, width: 0.5 },
});

// thin gray vertical separator inside the right table (original x 578px, spans table
// height); drawn AFTER the tables so the table cell fills do not cover it
// (original: light gray rule between the blue Y column and the one-hot columns)
function graySeparator() {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 8.015, y: 5.18, w: 0.02, h: 1.90,
    fill: { color: GRAY_LINE }, line: { type: "none" },
  });
}

// right table: headers Y, S?, O?, R?, T, R; x 552px=7.67in
const ybCol  = ["1", "0", "0", "1", "1", "1", "0", "1"];
const sCol   = ["1", "1", "1", "0", "0", "0", "0", "0"];
const oCol   = ["0", "0", "0", "1", "1", "1", "0", "0"];
const rqCol  = ["0", "0", "0", "0", "0", "0", "1", "1"];
const tbCol  = ["0", "1", "1", "0", "1", "0", "0", "0"];
const rbCol  = ["1", "1", "0", "1", "0", "0", "1", "0"];

const rtCols = [
  cells(["Y"].concat(ybCol), { color: BLUE }),
  cells(["S?"].concat(sCol), { fill: MAGENTA }),
  cells(["O?"].concat(oCol), { fill: MAGENTA }),
  cells(["R?"].concat(rqCol), { fill: MAGENTA }),
  cells(["T"].concat(tbCol), { fill: ORANGE }),
  cells(["R"].concat(rbCol), { fill: LGREEN }),
];
s.addTable([0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => rowOf(rtCols, i)), {
  x: 7.67, y: 5.17, w: 2.36,
  colW: [0.36, 0.44, 0.42, 0.47, 0.36, 0.31],
  rowH: 0.214,
});
graySeparator();

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_028_recreated.pptx" })
  .then(() => console.log("done"))
  .catch((e) => { console.error(e); process.exit(1); });
