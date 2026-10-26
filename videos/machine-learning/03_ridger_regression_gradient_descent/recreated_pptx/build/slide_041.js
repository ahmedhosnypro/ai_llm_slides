// Build: slide 041 — "Check Classes of Points: Initial W and Step η = 2"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GROUND TRUTH: unique_slides/slide_041.jpg (960x540, 1px = 1pt = 1/72in).
// Content spec: analysis/slide_041_final.json.
//
// Frame-measured layout (qa/slide041/ + this lane's PIL passes):
//   cream box   blue border x70..718 y54..130, fill FEFFE8 (median 254,255,232)
//   left table  6 columns x1..x6 (PIL: six header groups, six paren pairs, six
//               class labels — the analysis' "3x5 matrix / x1 x2 x4 x5 x6" was a
//               vision misread, flagged in its own uncertain_items). Headers
//               BLACK (b-r test: darkest px have blue as the LOWEST channel).
//               column vectors (top,bot): (1,1)(2,1)(1,2)(5,4)(6,5)(6,6) —
//               glyph-verified per column (gdiff041/tmpl041: L4_r2 '4' 0.905,
//               L5_r2 '5' 0.805, L6_r1/r2 '6'/'6', L3_r2 '2' 0.815, L2_r1 '2'
//               curve+base shape). class row C1 C1 C1 C2 C2 C2
//               (label_colors: x90-146 red, x157-214 blue — c6 measured blue).
//   legend      y110..123: red C1 x239, black "positive," ..x301, blue C2 x313,
//               black "negative," ..x377 (comma ink x376), green "Zero"
//               x394..423, black "is unaccepted" x428..508
//   mid         "Initial W =" x266..323 y75..84; vector parens x330.5/x352.5
//               spanning y58..106; digits (4,-2,-2) rows y61/77/95;
//               "Step η = 2" red italic x366..435 y66..81 (stepeta red 394 px)
//   right       "Check classes of" x499..582 y79..88 (all-dark zone, navy 0);
//               Z1 Z1 Z1 black y64..76 (saturated n=0 — not blue); three
//               2-row column vectors (0,0)(7,6)(3,2) y82..108
//   plot        red border x312..825 y173..482, white interior; 8 horizontal
//               gridlines y214/245/276/306/337/368/398/429 (gray ~215);
//               vertical gridlines ONLY at x362 and x784 (px<235 counts 226/229
//               vs 24-42 at the other ticks — the intermediate verticals do not
//               exist on the frame); x tick labels 0..8 INSIDE the plot at
//               y436..445 centred on x364..783; y tick labels 0..7 at x348..357
//               centred on the gridline rows; markers (measured px centres,
//               ~9px): red solid down-triangles (363,428.5)(521,367.5)(731,244.5)
//               fill ~(216,0,12); dark-blue squares (416.5,367.5)(417,398.5)
//               (469,398.5) fill ~(8,70,128); magenta diamonds (626,306.5)
//               (679,276)(679,245) fill ~(218,0,233). The vision analysis' 4th
//               blue square at (0,0) is refuted: that px cluster is the red
//               triangle (3 red, 3 blue, 3 magenta = 9 markers).
//   mouse cursor near the class-check matrix is a screenshot artifact —
//   recreation_brief step 15 forbids recreating it.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const OUT = path.resolve(__dirname, "../slide_041_recreated.pptx");

const px = (v) => v / 72;

const RED = "FF0000";
const DARKRED = "D60008";
const BLUE = "0000FF";
const BLACK = "000000";
const GREEN = "008000";
const WHITE = "FFFFFF";
const CREAM = "FEFFE8";
const GRID = "D8D8D5";
const SQBLUE = "084680";
const MAGENTA = "DC00E6";
const FONT = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

function txt(text, x, y, w, h, opts = {}) {
  slide.addText(text, Object.assign({
    x: px(x), y: px(y), w: px(w), h: px(h),
    fontFace: FONT, margin: 0, isTextBox: true,
  }, opts));
}

function txtsub(base, sub, x, y, w, h, opts = {}) {
  const subSize = Math.round(((opts.fontSize || 10) * 0.7) * 10) / 10;
  slide.addText([
    { text: base },
    { text: sub, options: { subscript: true, fontSize: subSize } },
  ], Object.assign({
    x: px(x), y: px(y), w: px(w), h: px(h),
    fontFace: FONT, margin: 0, isTextBox: true,
  }, opts));
}

function vline(x, y0, y1, width = 0.75) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x), y: px(y0), w: 0, h: px(y1 - y0),
    line: { color: BLACK, width },
  });
}

// P3 tall parens (lefttable crop FAIL attempt 1: straight rules vs the frame's
// bowed glyphs): 600dpi Bezier PNG, ink centered on the old vline anchor,
// ink top landing on the band top, from the sidecar-measured ink bbox.
const fs = require("fs");
const PAREN_DIR = path.resolve(__dirname,
  "../qa/slide041/assets/parens041");
function paren(variant, side, anchorX, bandTopY) {
  const base = path.join(PAREN_DIR, `paren_${variant}_${side}`);
  const sc = JSON.parse(fs.readFileSync(base + ".json", "utf8"));
  const k = sc.pt_per_px;
  const inkLeft = sc.ink_left_px * k, inkRight = sc.ink_right_px * k;
  const inkTop = sc.ink_top_px * k;
  slide.addImage({
    path: base + ".png",
    x: px(anchorX - (inkLeft + inkRight) / 2), y: px(bandTopY - inkTop),
    w: px(sc.px_w * k), h: px(sc.px_h * k),
  });
}

// ---- house chrome (deck 03 values) -----------------------------------------
drawHouseChrome(pptx, slide, { numeral: 41 });

// ---------------------------------------------------------------------------
// 1. CREAM BOX (blue border, x70..718 y54..130)
// ---------------------------------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(54), w: px(649), h: px(77),
  fill: { color: CREAM }, line: { color: BLUE, width: 1 },
});

// ---------------------------------------------------------------------------
// 2. LEFT TABLE: headers, six parenned column vectors, class row
// ---------------------------------------------------------------------------
[96.5, 118, 140, 163, 185.5, 208].forEach((cx, i) => {
  txtsub("x", String(i + 1), cx - 8, 61, 16, 13, {
    fontSize: 10, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});

const COLS = [
  { cx: 96.5,  pl: 90.5,  pr: 102,   vals: [1, 1] },
  { cx: 118,   pl: 112,   pr: 124,   vals: [2, 1] },
  { cx: 140,   pl: 134,   pr: 146.5, vals: [1, 2] },
  { cx: 163,   pl: 156.5, pr: 169.5, vals: [5, 4] },
  { cx: 185.5, pl: 179.5, pr: 192,   vals: [6, 5] },
  { cx: 208,   pl: 202,   pr: 214,   vals: [6, 6] },
];
COLS.forEach((c) => {
  paren("table", "lp", c.pl, 78);
  paren("table", "rp", c.pr, 78);
  txt(String(c.vals[0]), c.cx - 7, 76, 14, 13, {
    fontSize: 11, color: BLACK, bold: true, align: "center", valign: "middle",
  });
  txt(String(c.vals[1]), c.cx - 7, 93, 14, 13, {
    fontSize: 11, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});

[["C1", 96.5, RED], ["C1", 118, RED], ["C1", 140, RED],
 ["C2", 163, BLUE], ["C2", 185.5, BLUE], ["C2", 208, BLUE]]
  .forEach(([lab, cx, color]) => {
    txtsub(lab[0], lab[1], cx - 8, 110, 16, 14, {
      fontSize: 10, color, bold: true, align: "center", valign: "middle",
    });
  });

// ---------------------------------------------------------------------------
// 3. LEGEND row (y110..123)
// ---------------------------------------------------------------------------
const LEGEND = [
  { b: "C", s: "1", c: RED, x: 237, w: 15 },
  { t: " positive,", c: BLACK, x: 252, w: 52 },
  { b: "C", s: "2", c: BLUE, x: 311, w: 14 },
  { t: " negative,", c: BLACK, x: 326, w: 54 },
  { t: "Zero", c: GREEN, x: 392, w: 34 },
  { t: " is unaccepted", c: BLACK, x: 425, w: 86 },
];
LEGEND.forEach((s) => {
  if (s.b) {
    txtsub(s.b, s.s, s.x, 107, s.w, 17, { fontSize: 11.5, color: s.c, valign: "middle", wrap: false });
  } else {
    txt(s.t, s.x, 107, s.w, 17, { fontSize: 11.5, color: s.c, valign: "middle", wrap: false });
  }
});

// ---------------------------------------------------------------------------
// 4. MID: Initial W = (4/-2/-2), Step η = 2 (red italic)
// ---------------------------------------------------------------------------
txt("Initial W =", 263, 72, 64, 16, { fontSize: 12.5, color: BLACK, valign: "middle" });
paren("wvec", "lp", 330.5, 59);
paren("wvec", "rp", 352.5, 59);
txt("4", 335, 59, 16, 13, { fontSize: 12, color: BLACK, align: "center", valign: "middle" });
txt("-2", 335, 75, 16, 13, { fontSize: 12, color: BLACK, align: "center", valign: "middle" });
txt("-2", 335, 93, 16, 13, { fontSize: 12, color: BLACK, align: "center", valign: "middle" });
txt("Step \u03B7 = 2", 363, 63, 78, 20, {
  fontSize: 13.5, color: RED, italic: true, valign: "middle",
});

// ---------------------------------------------------------------------------
// 5. RIGHT: Check classes of + Z1 Z1 Z1 + three parenned column vectors
// ---------------------------------------------------------------------------
txt("Check classes of", 494, 75, 92, 15, { fontSize: 11, color: BLACK, valign: "middle" });
[605.5, 628, 650].forEach((cx) => {
  txtsub("Z", "1", cx - 9, 61, 18, 14, {
    fontSize: 10, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});
const RCOLS = [
  { cx: 605.5, pl: 598.5, pr: 611.5, vals: [0, 0] },
  { cx: 628,   pl: 622,   pr: 634,   vals: [7, 6] },
  { cx: 650,   pl: 643.5, pr: 656,   vals: [3, 2] },
];
RCOLS.forEach((c) => {
  paren("ztab", "lp", c.pl, 82);
  paren("ztab", "rp", c.pr, 82);
  txt(String(c.vals[0]), c.cx - 7, 80, 14, 13, {
    fontSize: 11, color: BLACK, bold: true, align: "center", valign: "middle",
  });
  txt(String(c.vals[1]), c.cx - 7, 94, 14, 13, {
    fontSize: 11, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});

// ---------------------------------------------------------------------------
// 6. PLOT: white area, red border, gridlines, tick labels, 9 markers
// ---------------------------------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: px(312.5), y: px(173.5), w: px(511), h: px(308),
  fill: { color: WHITE }, line: { color: "C00000", width: 1 },
});
// horizontal gridlines y=0..7 (frame rows 214..429)
[214, 245, 276, 306, 337, 368, 398, 429].forEach((y) => {
  slide.addShape(pptx.ShapeType.line, {
    x: px(313), y: px(y), w: px(511), h: 0,
    line: { color: GRID, width: 0.75 },
  });
});
// vertical gridlines ONLY at x=0 and x=8 (measured: the frame carries no
// intermediate vertical gridlines)
[362, 784].forEach((x) => {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x), y: px(174), w: 0, h: px(304),
    line: { color: GRID, width: 0.75 },
  });
});
// x tick labels 0..8, inside the plot just below the y=0 gridline
[364, 416, 468, 520, 573, 625, 677, 730, 783].forEach((cx, i) => {
  txt(String(i), cx - 6, 434, 12, 13, {
    fontSize: 8.5, color: BLACK, align: "center", valign: "middle",
  });
});
// y tick labels 0..7, inside the plot right of the x=0 gridline
[[428.5, "0"], [399, "1"], [368, "2"], [338, "3"], [307, "4"],
 [276, "5"], [245.5, "6"], [214, "7"]].forEach(([cy, lab]) => {
  txt(lab, 346, cy - 6.5, 13, 13, {
    fontSize: 8.5, color: BLACK, align: "center", valign: "middle",
  });
});
// markers at measured px centres (~9px each)
[[363, 428.5], [521, 367.5], [731, 244.5]].forEach(([cx, cy]) => {
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(cx - 4.5), y: px(cy - 4.5), w: px(9), h: px(9),
    fill: { color: DARKRED }, rotate: 180,
  });
});
[[416.5, 367.5], [417, 398.5], [469, 398.5]].forEach(([cx, cy]) => {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(cx - 4.5), y: px(cy - 4.5), w: px(9), h: px(9),
    fill: { color: SQBLUE },
  });
});
[[626, 306.5], [679, 276], [679, 245]].forEach(([cx, cy]) => {
  slide.addShape(pptx.ShapeType.diamond, {
    x: px(cx - 4.5), y: px(cy - 4.5), w: px(9), h: px(9),
    fill: { color: MAGENTA },
  });
});

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE", OUT);
});
