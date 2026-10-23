// components/slide_012.js — BANKED composition of slide 012
// ("Effect of Overfitting on model parameter "W""), ML lecture 03
// (03_ridger_regression_gradient_descent).

// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide — house chrome
// (numeral 12) + title + the four-colour left label column + the three stacked
// training tables (perfect / first outlier / second outlier) + the Test Data
// label and table + the red "Again" callout and its left-pointing curved arrow +
// the blue-bordered question box. opts:
//   { numeral }       — override the badge numeral (a recap variant passes its own
//                       number; the badge numeral is ALWAYS the number printed on
//                       the VARIANT's own original frame)
//   { skip: {...} }   — omit any block: chrome, title, labels, tables, testBlock,
//                       outlier1Table, againCallout, arrow, outlier2Table, questionBox
//   { only: {...} }   — draw ONLY the listed blocks (a child composes its delta)
//
// Draw order inside BLOCKS is the certified z-order. The three training tables
// are disjoint rectangles (top y127..265, middle y265..404, bottom y404..496) and
// no element of one crosses another's border, so cross-block z-order is
// geometrically irrelevant.
//
// The table builders (makeTrainTable / makeTestTable / TRAIN_COLS / TRAIN_ROWS /
// TRAIN_HEADER / TEST_ROWS) are exported for the child: slide 013 shares this
// slide's table PATTERN and redraws it at 013's own measured geometry with 013's
// own values — it must require() this module, never copy-paste, never re-derive.
//
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette ──────────────────────────────────────────────────────────
const RED    = "FF0000"; // title, red labels, Again callout, arrow
const BLUE   = "0000FF"; // blue labels, table headers, y-row values, question box
const BLACK  = "000000"; // table X1/X2 row values
const WHITE  = "FFFFFF"; // label text, question box fill
const YELLOW = "FFFF00"; // outlier cell highlight
const FONT   = "Arial";

// ── measured table geometry (frame px, from unique_slides/slide_012.jpg) ──────
const TRAIN_X = 203, TRAIN_W = 368;
const TRAIN_COLS  = [41, 41, 41, 41, 40, 41, 41, 41, 41];
const TRAIN_ROWS  = [31, 31, 30, 30];
const OUTLIER1_ROWS = [31, 31, 30, 30];
const OUTLIER2_ROWS = [23, 23, 23, 23];
const TEST_X = 720, TEST_Y = 130, TEST_W = 152, TEST_H = 122;
const TEST_COLS = [38, 38, 38, 38];
const TEST_ROWS = [30, 30, 31, 31];

const TRAIN_HEADER = ["", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"];
const TEST_HEADER  = ["", "Test1", "Test2", "Test3"];

// Table content, verbatim per analysis/slide_012_final.json.
const PERFECT_ROWS = [
  ["X1", 1, 2, 3, 4, 8, 9, 10, 11],
  ["X2", 1, 3, 5, 6, 16, 7, 5, 3],
  ["y",  2, 4, 6, 8, 16, 18, 20, 22],
];
const OUTLIER1_ROWS_DATA = [
  ["X1", 1, 2, 3, 4, 8, 9, 10, 30],
  ["X2", 1, 3, 5, 6, 16, 7, 5, 3],
  ["y",  2, 4, 6, 8, 16, 18, 20, 22],
];
const OUTLIER2_ROWS_DATA = [
  ["X1", 1, 2, 3, 4, 8, 9, 10, 60],
  ["X2", 1, 3, 5, 6, 16, 7, 5, 3],
  ["y",  2, 4, 6, 8, 16, 18, 20, 22],
];
const TEST_ROWS_DATA = [
  ["X1", 30, 40, 50],
  ["X2", 15, 20, 25],
  ["y",  60, 80, 100],
];

// ── table builders (the PATTERN slide 013 inherits) ───────────────────────────
// Header + row-label cells bold BLUE; X1/X2-row values BLACK; y-row values BLUE.
function makeTrainTable(header, rows, highlightCol = -1, highlightRow = -1) {
  // highlightRow: 0=X1 data row, 1=X2 data row, 2=y data row (header is separate)
  const result = [];
  result.push(header.map((h) => ({
    text: h, options: { bold: true, color: BLUE, fontFace: FONT, fontSize: 11, margin: 2 }
  })));
  rows.forEach((row, ri) => {
    result.push(row.map((cell, ci) => {
      const isHeader = ci === 0;
      const isHighlight = (ci === highlightCol && ri === highlightRow);
      let color = BLACK;
      if (isHeader) color = BLUE;
      else if (ri === 2) color = BLUE; // y row
      const opts = { bold: isHeader, color: color, fontFace: FONT, fontSize: 11, margin: 2 };
      if (isHighlight) opts.fill = { color: YELLOW };
      return { text: String(cell), options: opts };
    }));
  });
  return result;
}

function makeTestTable(header, rows) {
  const result = [];
  result.push(header.map((h) => ({
    text: h, options: { bold: true, color: BLUE, fontFace: FONT, fontSize: 11, margin: 2 }
  })));
  rows.forEach((row, ri) => {
    result.push(row.map((cell, ci) => {
      const isHeader = ci === 0;
      const isYRow = ri === 2;
      let color = isYRow ? BLUE : BLACK;
      if (isHeader) color = BLUE;
      return { text: String(cell), options: { bold: isHeader, color: color, fontFace: FONT, fontSize: 11, margin: 2 } };
    }));
  });
  return result;
}

// ── measured label / callout geometry ────────────────────────────────────────
const LABELS = [
  { x: 60, y: 110, w: 140, h: 30, fill: BLUE, text: "Training Data", lines: 1 },
  { x: 60, y: 175, w: 140, h: 50, fill: RED,  text: "Perfect Data\nY follows x1", lines: 2 },
  { x: 60, y: 325, w: 140, h: 30, fill: RED,  text: "x8 is Outlier", lines: 1 },
  { x: 60, y: 450, w: 140, h: 30, fill: RED,  text: "x8 is Outlier", lines: 1 },
];

const QUESTION = { x: 603, y: 366, w: 267, h: 50, padX: 8, padY: 6 };

function labelBox(pptx, slide, L) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(L.x), y: px(L.y), w: px(L.w), h: px(L.h),
    fill: { color: L.fill },
  });
  slide.addText(L.text, {
    x: px(L.x), y: px(L.y), w: px(L.w), h: px(L.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 14, bold: true, color: WHITE,
    lineSpacing: 14 * 1.2,
  });
}

function calloutBox(pptx, slide, x, y, w, h, fill, textLines, fontSize = 13) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill },
  });
  const totalH = textLines.length * fontSize * 1.2;
  const y0 = y + (h - totalH) / 2;
  textLines.forEach((line, i) => {
    slide.addText(line, {
      x: px(x), y: px(y0 + i * fontSize * 1.2), w: px(w), h: px(fontSize * 1.2),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: fontSize, bold: true, color: WHITE,
      lineSpacing: fontSize * 1.2,
    });
  });
}

function tablePlacement(pptx, slide, data, x, y, w, h, colW, rowH) {
  slide.addTable(data, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    colW: colW.map(px), rowH: rowH.map(px),
    fontFace: FONT, fontSize: 11,
    border: { pt: 1, color: BLACK },
    autoFit: false,
  });
}

// ── BLOCK draw functions (draw order = certified z-order) ────────────────────
function drawChrome(pptx, slide, opts) {
  const n = opts && opts.numeral !== undefined ? opts.numeral : 12;
  drawHouseChrome(pptx, slide, { numeral: n });
}

function drawTitle(pptx, slide) {
  slide.addText('Effect of Overfitting on model parameter \u201cW\u201d', {
    x: px(160), y: px(70), w: px(640), h: px(40),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 28, bold: true, color: RED,
    lineSpacing: 34,
  });
}

function drawLabels(pptx, slide) {
  for (const L of LABELS) labelBox(pptx, slide, L);
}

function drawTrainTable(pptx, slide) {
  const data = makeTrainTable(TRAIN_HEADER, PERFECT_ROWS);
  tablePlacement(pptx, slide, data, TRAIN_X, 127, TRAIN_W, 138, TRAIN_COLS, TRAIN_ROWS);
}

function drawTestBlock(pptx, slide) {
  labelBox(pptx, slide, { x: 780, y: 115, w: 100, h: 30, fill: BLUE, text: "Test Data", lines: 1 });
  const data = makeTestTable(TEST_HEADER, TEST_ROWS_DATA);
  tablePlacement(pptx, slide, data, TEST_X, TEST_Y, TEST_W, TEST_H, TEST_COLS, TEST_ROWS);
}

function drawOutlier1Table(pptx, slide) {
  const data = makeTrainTable(TRAIN_HEADER, OUTLIER1_ROWS_DATA, 8, 0); // X8 col, X1 data row
  tablePlacement(pptx, slide, data, TRAIN_X, 265, TRAIN_W, 139, TRAIN_COLS, OUTLIER1_ROWS);
}

function drawAgainCallout(pptx, slide) {
  calloutBox(pptx, slide, 706, 275, 132, 45, RED, ["Again", "Y follows x1"], 13);
}

function drawArrow(pptx, slide) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(571), y: px(293), w: px(706 - 571), h: 0,
    line: { color: RED, width: 2, endArrowType: "triangle" },
  });
}

function drawOutlier2Table(pptx, slide) {
  const data = makeTrainTable(TRAIN_HEADER, OUTLIER2_ROWS_DATA, 8, 0); // X8 col, X1 data row
  tablePlacement(pptx, slide, data, TRAIN_X, 404, TRAIN_W, 92, TRAIN_COLS, OUTLIER2_ROWS);
}

function drawQuestionBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(QUESTION.x), y: px(QUESTION.y), w: px(QUESTION.w), h: px(QUESTION.h),
    fill: { color: WHITE }, line: { color: BLUE, width: 2 },
  });
  slide.addText("What will be the effect of X8 Outlier values on the trained model ???", {
    x: px(QUESTION.x + QUESTION.padX), y: px(QUESTION.y + QUESTION.padY),
    w: px(QUESTION.w - QUESTION.padX * 2), h: px(QUESTION.h - QUESTION.padY * 2),
    align: "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 11, color: BLUE, bold: false,
    lineSpacing: 14,
  });
}

const BLOCKS = {
  chrome: drawChrome,
  title: drawTitle,
  labels: drawLabels,
  trainTable: drawTrainTable,
  testBlock: drawTestBlock,
  outlier1Table: drawOutlier1Table,
  againCallout: drawAgainCallout,
  arrow: drawArrow,
  outlier2Table: drawOutlier2Table,
  questionBox: drawQuestionBox,
};

function renderBase(pptx, slide, opts = {}) {
  const skip = opts.skip || {};
  const only = opts.only || null;
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (only && !only[name]) continue;
    if (!only && skip[name]) continue;
    fn(pptx, slide, opts);
  }
}

module.exports = {
  renderBase, BLOCKS,
  makeTrainTable, makeTestTable,
  TRAIN_COLS, TRAIN_ROWS, OUTLIER1_ROWS, OUTLIER2_ROWS,
  TEST_COLS, TEST_ROWS,
  TRAIN_HEADER, TEST_HEADER,
  PERFECT_ROWS, OUTLIER1_ROWS_DATA, OUTLIER2_ROWS_DATA, TEST_ROWS_DATA,
  LABELS, QUESTION,
  RED, BLUE, BLACK, WHITE, YELLOW, FONT,
};
