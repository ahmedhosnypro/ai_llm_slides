// slide_004.js — "Regression – One Dimensional Case" (ML lecture 02)
// Root slide; PARENT OF slide 5 (banks as build/components/slide_004.js after PASS).
//
// Ground truth: PIL-measured from unique_slides/slide_004.jpg (960x540, 1px=1pt),
// scripts banked in scratch/ml02/slide004/measure*.py (gen-3 resume, verified):
//   - title ink x291..620, caps y61..74 (desc g->78), center x455.5, ~20pt bold
//   - chart box: white rect x87..862, y94..518, red 8B0000 border ~1.5pt
//   - chart title (blue) ink x271..704, caps y115..129, ~14.5pt bold, tight tracking
//   - y-axis red line x134, arrow tip y101, down to x-axis y475; x-axis y475.5
//     x134..638 ending in a dark-red dot (635,475.5) d6.5
//   - 21 orange data dots d~7 (#C67E33 measured core) — centers listed below
//   - purple 800080 dashed: 3 horizontals y259/274/290 (x140..404) + vertical
//     x402.5 (y167..470) ending in a purple dot (402.5,474.5) d8
//   - y-axis dots: (136.5,242.5) RED + (136.5,259/275/291) purple, d7
//   - faint tan dotted horizontals y242.5 (x141..432) and y303.5 (x141..390),
//     ~0.75pt sysDot, washed-out color E9D8D8 (measured median)
//   - 3 bold red '?' at x111, tops y253/269/285 (pitch 16) + 4th taller '?'
//     mark (squiggle in original) at x112..127, y112..150
//   - model box x701..808 y213..276, fill FBFDE9, thin 8F8BAB border; text
//     x709.., 11pt bold, pitch 18: "Model" (red, underlined, y221) /
//     "I/P:  Length" (y239) / "O/P: Weight" (y257)  [double spaces verbatim]
//   - axis label "Length" ~8pt bold red, ink x611..647, caps y488..496
//   - mouse cursor at (368..374, 324..332): video artifact, EXCLUDED per judge
//     GROUND RULES (c) — never draw it.
// House chrome: shared_patterns/house_chrome.js (THIS deck's geometry), numeral 4.

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

// ---- measured constants (frame px; 1px = 1pt = 1/72 in) --------------------
const C = {
  RED: "8B0000",        // title / chart border / axes / ?s / Length / Model
  RED_DOT: "9C000C",    // dark-red dot at the x-axis right end
  ORANGE: "C67E33",     // data dots (measured core median)
  PURPLE: "800080",     // dashed annotation lines + dots
  FAINT: "E9D8D8",      // washed-out tan dotted lines (measured median)
  BLUE: "00008B",       // chart title (measured core (16,4,137))
  BLACK: "000000",
  MB_FILL: "FBFDE9",    // model box fill (measured (251,253,229))
  MB_BORDER: "8F8BAB",  // model box thin border (measured (143,139,171))
};

const TITLE_TEXT = "Regression \u2013 One Dimensional Case";
const CHART_TITLE_TEXT = "Length and Weight of  different samples of Steel Bars";

// closed-loop tuning knobs (frame px offsets applied to text boxes)
const TUNE = {
  title: { size: 19.5, charSpacing: -0.2, dx: 0, dy: 0 },
  chartTitle: { size: 18, charSpacing: -0.5, dx: 0, dy: -2 },
  qmarks: { size: 15, lineSpacing: 16, dx: 0, dy: 0 },
  weightLabel: { size: 12.5, charSpacing: -0.5, dx: 0, dy: 0 },
  modelText: { size: 15, lineSpacing: 18, dx: 1.5, dy: 1 },
  lengthLabel: { size: 11, dx: 1.5, dy: 2.3 },
};

const DOT_D = 7; // data + axis dot diameter (frame px)

const ORANGE_DOTS = [ // PIL-measured centers (x, y)
  [538, 172.5], [511, 182], [477.5, 222.5], [505, 222.5], [432, 241.5],
  [477, 245], [426, 269], [366, 301], [345, 304], [390, 305],
  [314.5, 311], [305.5, 330], [342, 336], [290.5, 339], [317.5, 348],
  [269, 364], [251, 367], [266.5, 380], [278.5, 380], [230, 386], [248, 392],
];

// ---- per-block draws (component exports; children may call selectively) ----
function drawTitle(pptx, slide, opts = {}) {
  const t = { ...TUNE.title, ...(opts.title || {}) };
  const boxW = 500, boxH = 30;
  slide.addText(opts.titleText || TITLE_TEXT, {
    x: (455.5 - boxW / 2 + t.dx) / 72, y: (67.5 - boxH / 2 + t.dy) / 72,
    w: boxW / 72, h: boxH / 72,
    align: "center", valign: "middle", margin: 0,
    fontSize: t.size, bold: true, color: C.RED, fontFace: "Arial",
    charSpacing: t.charSpacing,
  });
}

function drawChartFrame(pptx, slide) {
  // white chart area + red border (covers the gray panel in this region)
  slide.addShape(pptx.ShapeType.rect, {
    x: 87.5 / 72, y: 94.5 / 72, w: 775 / 72, h: 424 / 72,
    fill: { color: "FFFFFF" }, line: { color: C.RED, width: 1.5 },
  });
  slide.addText(CHART_TITLE_TEXT, {
    x: (487.5 - 280) / 72, y: (124.5 - 13) / 72, w: 560 / 72, h: 26 / 72,
    align: "center", valign: "middle", margin: 0,
    fontSize: TUNE.chartTitle.size, bold: true, color: C.BLUE,
    fontFace: "Arial", charSpacing: TUNE.chartTitle.charSpacing,
  });
}

function drawAxes(pptx, slide) {
  // y-axis: line x134 from below the arrowhead down to the x-axis + tip triangle
  slide.addShape(pptx.ShapeType.line, {
    x: 134 / 72, y: 109 / 72, w: 0, h: (475 - 109) / 72,
    line: { color: C.RED, width: 2 },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: 130.5 / 72, y: 100.5 / 72, w: 7 / 72, h: 10 / 72,
    fill: { color: C.RED }, line: { type: "none" },
  });
  // x-axis: line y475.5 from the y-axis to x638, ending in a dark-red dot
  slide.addShape(pptx.ShapeType.line, {
    x: 134 / 72, y: 475.5 / 72, w: (638 - 134) / 72, h: 0,
    line: { color: C.RED, width: 2 },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: (635 - 3.25) / 72, y: (475.5 - 3.25) / 72, w: 6.5 / 72, h: 6.5 / 72,
    fill: { color: C.RED_DOT }, line: { type: "none" },
  });
}

function drawFaintDotted(pptx, slide) {
  // thin washed-out tan dotted horizontals (y-axis -> data points)
  for (const [y, x1] of [[242.5, 432], [303.5, 390]]) {
    slide.addShape(pptx.ShapeType.line, {
      x: 141 / 72, y: y / 72, w: (x1 - 141) / 72, h: 0,
      line: { color: C.FAINT, width: 0.75, dashType: "sysDot" },
    });
  }
}

function drawDashes(pptx, slide) {
  const L = { color: C.PURPLE, width: 1.5, dashType: "dash" };
  // 3 horizontal dashed: from the y-axis dots to the vertical dashed line
  for (const y of [259, 274, 290]) {
    slide.addShape(pptx.ShapeType.line, {
      x: 138 / 72, y: y / 72, w: (403 - 138) / 72, h: 0, line: { ...L },
    });
  }
  // vertical dashed x402.5 from y167 down to its x-axis dot
  slide.addShape(pptx.ShapeType.line, {
    x: 402.5 / 72, y: 167 / 72, w: 0, h: (470 - 167) / 72, line: { ...L },
  });
  // dots: y-axis (1 red + 3 purple) and the purple dot at the vline foot
  const dots = [
    [136.5, 242.5, C.RED], [136.5, 259, C.PURPLE],
    [136.5, 275, C.PURPLE], [136.5, 291, C.PURPLE],
    [402.5, 474.5, C.PURPLE],
  ];
  for (const [cx, cy, col] of dots) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: (cx - DOT_D / 2) / 72, y: (cy - DOT_D / 2) / 72,
      w: DOT_D / 72, h: DOT_D / 72,
      fill: { color: col }, line: { type: "none" },
    });
  }
}

function drawDataDots(pptx, slide) {
  for (const [cx, cy] of ORANGE_DOTS) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: (cx - DOT_D / 2) / 72, y: (cy - DOT_D / 2) / 72,
      w: DOT_D / 72, h: DOT_D / 72,
      fill: { color: C.ORANGE }, line: { type: "none" },
    });
  }
}

function drawQMarks(pptx, slide, opts = {}) {
  const q = { ...TUNE.qmarks, ...(opts.qmarks || {}) };
  // three stacked bold ?s beside the y-axis (measured pitch 16px)
  slide.addText("?\n?\n?", {
    x: (106 + q.dx) / 72, y: (250 + q.dy) / 72, w: 26 / 72, h: 52 / 72,
    align: "center", valign: "top", margin: 0,
    fontSize: q.size, bold: true, color: C.RED, fontFace: "Arial",
    lineSpacing: q.lineSpacing,
  });
  // y-axis label "Weight" rotated 90° beside the axis (spec: vertical red text;
  // the crop judge identified the original's upper-left mark as this label):
  // ink x115..126 (cap-height direction), y112..150 (text direction)
  const wl = { ...TUNE.weightLabel, ...(opts.weightLabel || {}) };
  slide.addText("Weight", {
    x: (120.5 - 28 + wl.dx) / 72, y: (131 - 7.5 + wl.dy) / 72,
    w: 56 / 72, h: 15 / 72, rotate: 270,
    align: "center", valign: "middle", margin: 0,
    fontSize: wl.size, bold: true, color: C.RED, fontFace: "Arial",
    charSpacing: wl.charSpacing,
  });
}

function drawModelBox(pptx, slide, opts = {}) {
  const m = { ...TUNE.modelText, ...(opts.modelText || {}) };
  slide.addShape(pptx.ShapeType.rect, {
    x: 701 / 72, y: 213 / 72, w: 108 / 72, h: 64 / 72,
    fill: { color: C.MB_FILL }, line: { color: C.MB_BORDER, width: 0.75 },
  });
  slide.addText([
    { text: "Model", options: { color: C.RED, underline: { style: "sng" }, breakLine: true } },
    { text: "I/P:\u00A0\u00A0 Length", options: { color: C.BLACK, breakLine: true } },
    { text: "O/P: Weight", options: { color: C.BLACK } },
  ], {
    x: (706 + m.dx) / 72, y: (216 + m.dy) / 72, w: 100 / 72, h: 58 / 72,
    align: "left", valign: "top", margin: 0,
    fontSize: m.size, bold: true, fontFace: "Arial",
    lineSpacing: m.lineSpacing,
  });
}

function drawLengthLabel(pptx, slide, opts = {}) {
  const t = { ...TUNE.lengthLabel, ...(opts.lengthLabel || {}) };
  slide.addText("Length", {
    x: (609 + t.dx) / 72, y: (483.5 + t.dy) / 72, w: 50 / 72, h: 18 / 72,
    align: "left", valign: "top", margin: 0,
    fontSize: t.size, bold: true, color: C.RED, fontFace: "Arial",
  });
}

// renderBase: full composition. Children (slide 5) import this module and call
// renderBase with { numeral: <their printed number>, skip: {...} }.
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 4 : opts.numeral });
  drawChartFrame(pptx, slide);
  drawFaintDotted(pptx, slide);
  drawAxes(pptx, slide);
  drawDashes(pptx, slide);
  drawDataDots(pptx, slide);
  drawQMarks(pptx, slide, opts);
  drawTitle(pptx, slide, opts);
  drawModelBox(pptx, slide, opts);
  drawLengthLabel(pptx, slide, opts);
}

// ---- build ----------------------------------------------------------------
function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] ||
    path.resolve(__dirname, "../slide_004_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = {
  renderBase, drawTitle, drawChartFrame, drawAxes, drawFaintDotted,
  drawDashes, drawDataDots, drawQMarks, drawModelBox, drawLengthLabel,
  CHROME_CONSTS: C, ORANGE_DOTS, TUNE, TITLE_TEXT, CHART_TITLE_TEXT,
};
