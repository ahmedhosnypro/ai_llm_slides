// slide_013.js — "Effect of Overfitting on model parameter "W""
// ML lecture 03 (03_ridger_regression_gradient_descent).
//
// CHILD of slide 012 (dependency edge 13 > 12, per slide_dependencies.json).
// Inherits 012's certified TABLE PATTERN via components/slide_012.js — the
// build imports makeTrainTable / makeTestTable / textBox-style helpers and the
// palette; it never copy-pastes and never re-derives 012's values. 013's own
// geometry and values are PIL-measured from unique_slides/slide_013.jpg
// (dossier: qa/slide013/MEASUREMENTS.md).
//
// What is inherited from 012 (block-level): nothing is drawn by renderBase here.
// The table builders (the alternating blue/red ink rule, white fills, bold
// header/label columns) are the shared pattern; 013 supplies 013's own
// gridlines, rows, columns, label boxes, W boxes, ellipses and arrows.
//
// 013's deltas vs 012 (measured, not assumed):
//   - three identical rows, each: Train table | W box | Test table
//   - tables at x92..459 (train) and x719..872 (test) — 012's were x203..571 / x719..873
//   - only ONE "Train"/"Test" label pair, above row 1 (measured: bands 2/3 have none)
//   - the label boxes are BLUE with WHITE text (the analysis claimed a yellow
//     Test box — refuted by pixel measurement: median fill (3,0,166))
//   - W box: RED-bordered WHITE rect holding "W = [ v1; v2; v3 ]" + a yellow
//     ellipse with "||W||^2 = N" beneath it
//   - two hollow blue arrows per band (left into the train table, right toward
//     the test table)
//   - no "Again" callout, no "X5 is Outlier" labels, no question box

const path = require("path");
const pptxgen = require("pptxgenjs");

// ── CERTIFIED PARENT COMPONENT (import, never copy) ───────────────────────────
const P = require(path.resolve(__dirname, "./components/slide_012.js"));

// Parent exports the table builders + palette. 013 uses BOTH builders verbatim
// for the shared table pattern (makeTrainTable for the label tables, makeTestTable
// for the three-column test tables) and supplies its own geometry/content.
const { makeTrainTable, makeTestTable, FONT, SHADE } = P;

const px = (v) => v / 72;

const RED = "C00000";   // title / W-box border / brackets (measured core)
const INKRED = "FF0000"; // analysis's ink colour for red table values
const BLUE = "0000FF";
const WHITE = "FFFFFF";
const BLACK = "000000";
const YELLOW = "FFFF00"; // ellipse + highlighted train cells
const PANEL = "E9E9E7";
const BADGE_FILL = "FDFD96";
const BADGE_RING = "6A5ACD";
const BADGE_NUM = "333333";

const TITLE_TEXT = 'Effect of Overfitting on model parameter \u201cW\u201d';

// ── 013's measured geometry (frame px) ────────────────────────────────────────
const TRAIN_X = 92, TRAIN_W = 367;
const TRAIN_COLS = [41, 41, 40, 41, 41, 41, 40, 41, 40];   // 367 px
const ROWS_31 = [31, 31, 31, 30];
const ROWS_32 = [32, 31, 31, 30];

const BANDS = [
  { y: 126, rows: ROWS_31 },
  { y: 265, rows: ROWS_31 },
  { y: 402, rows: ROWS_32 },
];

const TEST_X = 719, TEST_W = 153;
const TEST_COLS = [51, 51, 51];

// W box (red-bordered white rect) + ellipse, per band
const WBOX = [
  { x: 505, y: 126, w: 120, h: 126, ell: { x: 515, y: 215, w: 100, h: 33 }, v0: 142 },
  { x: 505, y: 265, w: 120, h: 124, ell: { x: 517, y: 353, w: 100, h: 33 } },
  { x: 505, y: 402, w: 120, h: 125, ell: { x: 522, y: 492, w: 99, h: 32 } },
];

// The vector values: [top, mid, bottom] baseline tops per band (measured)
const WVEC = [
  { v: ["0", "2", "0"], tops: [142, 166, 191] },
  { v: ["2.7", "0.67", "0.64"], tops: [279, 304, 329] },
  { v: ["4", "0.29", "0.78"], tops: [425, 442, 467] },
];

const ELL_TEXT = ["||W||^2 = 4", "||W||^2 = 8.11", "||W||^2 = 16.7"];

// Arrows per band: left (into the train table) and right (toward the test table)
const ARROWS = [
  { L: { x: 464, y: 186, w: 40, h: 26 }, R: { x: 627, y: 186, w: 40, h: 25 } },
  { L: { x: 464, y: 319, w: 40, h: 26 }, R: { x: 628, y: 319, w: 40, h: 25 } },
  { L: { x: 464, y: 452, w: 40, h: 26 }, R: { x: 627, y: 452, w: 40, h: 25 } },
];

// ── measured table data ──────────────────────────────────────────────────────
const TRAIN_HEADER = ["", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"];
const TEST_HEADER = ["Test1", "Test2", "Test3"];

const ROW_X2 = ["X2", 1, 3, 5, 6, 16, 7, 5, 3];
const ROW_Y = ["y", 2, 4, 6, 8, 16, 18, 20, 22];

// (x8 value of the X1 row is what changes; the yellow highlight rides on it)
const TRAIN_ROWS = [
  [["X1", 1, 2, 3, 4, 8, 9, 10, 11], ROW_X2, ROW_Y],       // band 1 — no highlight
  [["X1", 1, 2, 3, 4, 8, 9, 10, 30], ROW_X2, ROW_Y],       // band 2 — X8 = 30, yellow
  [["X1", 1, 2, 3, 4, 8, 9, 10, 60], ROW_X2, ROW_Y],       // band 3 — X8 = 60, yellow
];

const TEST_ROWS = [
  [[30, 40, 50], [15, 20, 25], [60, 80, 100]],
  [[30, 40, 50], [15, 20, 25], [32.4, 42.3, 52.3]],
  [[30, 40, 50], [15, 20, 25], [24.4, 31.2, 38]],
];

// ── block draw functions (draw order = certified z-order) ────────────────────
function drawChrome(pptx, slide) {
  // This deck's ratified chrome: white canvas, E9E9E7 panel x54..903 y45..540,
  // C00000 1pt LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 (NO top stroke), badge
  // d35 at (876,73) FDFD96 ring 6A5ACD bold 18pt #333333 numeral 13.
  slide.background = { color: WHITE };
  slide.addShape(pptx.ShapeType.rect, {
    x: px(54), y: px(45), w: px(850), h: px(495),
    fill: { color: PANEL }, line: { type: "none" },
  });
  const st = { pt: 1, color: RED };
  slide.addShape(pptx.ShapeType.line, { x: px(58.5), y: px(46), w: 0, h: px(493), line: st });
  slide.addShape(pptx.ShapeType.line, { x: px(901), y: px(46), w: 0, h: px(493), line: st });
  slide.addShape(pptx.ShapeType.line, { x: px(58), y: px(538.5), w: px(844), h: 0, line: st });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(876 - 17.5), y: px(73 - 17.5), w: px(35), h: px(35),
    fill: { color: BADGE_FILL }, line: { color: BADGE_RING, pt: 2 },
  });
  slide.addText("13", {
    x: px(876 - 17.5), y: px(73 - 17.5), w: px(35), h: px(35),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 18, bold: true, color: BADGE_NUM,
  });
}

function drawTitle(pptx, slide) {
  slide.addText(TITLE_TEXT, {
    x: px(154), y: px(68), w: px(640), h: px(34),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 24, bold: true, color: "8B0000",
    lineSpacing: 28,
  });
}

// The one measured "Train"/"Test" label pair, above row 1.
function drawLabelBoxes(pptx, slide) {
  const boxes = [
    { x: 96, y: 96, w: 65, h: 30, text: "Train" },
    { x: 801, y: 96, w: 66, h: 30, text: "Test" },
  ];
  for (const b of boxes) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      fill: { color: BLUE },
    });
    slide.addText(b.text, {
      x: px(b.x), y: px(b.y + 9), w: px(b.w), h: px(14),
      align: "left", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 12, bold: true, color: WHITE,
      lineSpacing: 14,
    });
  }
}

function drawTrainTables(pptx, slide) {
  BANDS.forEach((band, bi) => {
    const rows = TRAIN_ROWS[bi];
    const hl = bi === 0 ? -1 : 0; // band 1 has no highlight
    const data = makeTrainTable(TRAIN_HEADER, rows, hl, 8); // X1 row (body ri 0), X8 col
    slide.addTable(data, {
      x: px(TRAIN_X), y: px(band.y), w: px(TRAIN_W),
      h: px(band.rows.reduce((a, b) => a + b, 0)),
      colW: TRAIN_COLS.map(px), rowH: band.rows.map(px),
      fontFace: FONT, fontSize: 11,
      border: { pt: 1, color: "CCCCCC" },
      autoFit: false,
    });
  });
}

// 013's test table uses the PARENT's exported makeTestTable verbatim — 013's own
// frame measurement confirms the same RED/BLUE/RED complementary phase the parent
// measured for its test table (band 1: col1 RED=646, col2 BLUE=595, col3 RED=711).
// Deviation from the parent's default: 013's test cells are all WHITE-filled (the
// parent shades its y-row pale yellow; 013's frame has no yellow fill in any test
// table — measured), so the fill is overridden to WHITE here.
const TEST_SHADE_ROW = -1; // no shaded row in 013 (measured)

function buildTestTable(rows) {
  return makeTestTable(TEST_HEADER, rows).map((row, ri) =>
    row.map((cell, ci) => ({
      text: cell.text,
      options: Object.assign({}, cell.options, {
        fill: { color: ri === TEST_SHADE_ROW ? SHADE : WHITE },
      }),
    })
  ));
}

function drawTestTables(pptx, slide) {
  BANDS.forEach((band, bi) => {
    const data = buildTestTable(TEST_ROWS[bi]);
    slide.addTable(data, {
      x: px(TEST_X), y: px(band.y), w: px(TEST_W),
      h: px(band.rows.reduce((a, b) => a + b, 0)),
      colW: TEST_COLS.map(px), rowH: band.rows.map(px),
      fontFace: FONT, fontSize: 11,
      border: { pt: 1, color: "CCCCCC" },
      autoFit: false,
    });
  });
}

// Hollow blue arrow: top + bottom strokes, a start bar, and a solid triangle head.
function drawArrow(pptx, slide, a) {
  const LINE = { color: BLUE, width: 1 };
  slide.addShape(pptx.ShapeType.line, {
    x: px(a.x), y: px(a.y), w: px(a.w), h: 0, line: LINE,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(a.x), y: px(a.y + a.h - 1), w: px(a.w), h: 0, line: LINE,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(a.x), y: px(a.y), w: 0, h: px(a.h - 1), line: LINE,
  });
  // head: solid triangle pointing right, at the shaft's right end
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(a.x + a.w - 11), y: px(a.y - 4), w: px(11), h: px(a.h + 8),
    fill: { color: BLUE }, line: { type: "none" }, rotate: 90,
  });
}

function drawArrows(pptx, slide) {
  for (const a of ARROWS) {
    drawArrow(pptx, slide, a.L);
    drawArrow(pptx, slide, a.R);
  }
}

// W box: red-bordered white rect, "W =" + brackets + the 3 stacked values in black.
function drawWBox(pptx, slide, box, vec) {
  const b = box;
  slide.addShape(pptx.ShapeType.rect, {
    x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
    fill: { color: WHITE }, line: { color: RED, pt: 2 },
  });
  // "W =" red label at the box's left interior (measured ink x526..545)
  slide.addText("W =", {
    x: px(526), y: px(vec.tops[1] - 4), w: px(22), h: px(18),
    align: "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 12, bold: true, color: RED,
    lineSpacing: 14,
  });
  // the "=" bar of "W =" (measured: a double-bar at x554..567, spanning the
  // middle value's band — measured y168..175 in band 1)
  const eb = vec.tops[1];
  slide.addShape(pptx.ShapeType.rect, {
    x: px(554), y: px(eb + 2), w: px(14), h: px(2), fill: { color: RED },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(554), y: px(eb + 7), w: px(14), h: px(2), fill: { color: RED },
  });
  // brackets: two red vertical strokes flanking the values (measured x565/585)
  const vTop = vec.tops[0], vBot = vec.tops[2] + 16;
  slide.addShape(pptx.ShapeType.line, {
    x: px(565.5), y: px(vTop), w: 0, h: px(vBot - vTop), line: { color: RED, width: 2 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(585), y: px(vTop), w: 0, h: px(vBot - vTop), line: { color: RED, width: 2 },
  });
  // the three stacked values, black, left-aligned at the measured x573..578
  vec.tops.forEach((t, i) => {
    slide.addText(vec.v[i], {
      x: px(569), y: px(t - 3), w: px(17), h: px(20),
      align: "left", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 11, color: BLACK,
      lineSpacing: 14,
    });
  });
  // the yellow norm-squared ellipse, below the vector
  const e = b.ell;
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(e.x), y: px(e.y), w: px(e.w), h: px(e.h),
    fill: { color: YELLOW }, line: { type: "none" },
  });
  slide.addText(ELL_TEXT[WBOX.indexOf(b)], {
    x: px(e.x), y: px(e.y + 8), w: px(e.w), h: px(e.h - 16),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 11, color: BLACK,
    lineSpacing: 14,
  });
}

function drawWBoxes(pptx, slide) {
  WBOX.forEach((b, i) => drawWBox(pptx, slide, b, WVEC[i]));
}

// ── build ────────────────────────────────────────────────────────────────────
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

drawChrome(pres, slide);
drawTitle(pres, slide);
drawLabelBoxes(pres, slide);
drawTrainTables(pres, slide);
drawTestTables(pres, slide);
drawArrows(pres, slide);
drawWBoxes(pres, slide);

pres.writeFile({ fileName: path.resolve(__dirname, "../slide_013_recreated.pptx") })
  .then((f) => console.log("wrote " + f))
  .catch((e) => { console.error(e); process.exit(1); });
