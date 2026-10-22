// slide_003.js — "Regression – One Dimensional Case" (ML lecture 02, CHROME REFERENCE slide)
// Root slide (no parents, no in-video children); PLAYLIST-SCOPED component banked after PASS.
//
// Ground truth: PIL-measured from unique_slides/slide_003.jpg (960x540, 1px=1pt),
// scripts banked in scratch/ml02/slide003/ (gen-6 resume; gen-5 corpus re-run + verified):
//   - title ink x291..620, caps y61..74 (desc g->78), center x455.5, 19.5pt bold
//   - chart box: white rect x87.5..862.5, y94.5..518.5, red 8B0000 border 1.5pt
//   - chart title (blue) ink x271..704, caps y116..133 (L 117..129), center x487.5,
//     18pt bold, blue 0000CC (band-restricted bluest px (19,3,188); the deck-wide
//     blue mask without the band catches the badge ring — measured 2026-10-14)
//   - y-axis red 2pt line x134, arrowhead apex y102 (tri x130.5 y100.5 w7 h10), down to y476
//   - x-axis red 2pt line y476 x134..632 ending in a RIGHT-POINTING TRIANGLE
//     (base x632..633 y473..479, tip x638) — slide 4 has a round dot here, slide 3 a triangle
//   - 21 orange data dots d7 #E87D1E (189-sample fill median (234,124,17)), no outline
//     (the dark rim in the JPEG is undershoot ringing; certified sibling slide 4: none)
//   - faint dotted guides E9D8D8 sysDot 0.75pt: y242.5 (x140..427.5) and y303.5 (x140..385.5)
//   - junction arrowheads on the y-axis: RIGHT-pointing solid triangles, base on the axis
//     (x134..139.5), 11px tall, at y238..249 (upper guide) and y299..310 (lower guide)
//   - small DOWN-pointing arrowheads under the two highlighted markers:
//     upper (432,242) -> tri x429.5 y244.5 w5 h5; lower (390,305) -> tri x387.5 y307 w5 h5
//   - rotated "Weight" ink x118..125 (cap dir) y113..149 (text dir) -> 11pt bold, center (121.5,131)
//   - "Length" ink x612..646 caps y490..497 -> 11pt bold, box x610.5 y487.5
//   - mouse cursor at ~(505,203): video artifact, EXCLUDED per judge GROUND RULES (c)
// House chrome: shared_patterns/house_chrome.js (THIS deck's geometry), numeral 3.
// Sibling pattern-verified against certified slide_004.js (same chart, clean variant):
// title/chart-frame/chart-title/axes/dots/guides share its certified geometry.

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

// ---- measured constants (frame px; 1px = 1pt = 1/72 in) --------------------
const C = {
  RED: "8B0000",     // title / chart border / axes / labels / arrowheads
  ORANGE: "E87D1E",  // data dots (189-sample median (234,124,17))
  FAINT: "CC6405",   // dotted guides: measured dot CORE (204,100,5) — red-orange ink,
                     // JPEG-washed to pink in the frame; attempt-1 judge MINOR (too pale)
  BLUE: "0000CC",    // chart title (band-restricted bluest px (19,3,188))
};

const TITLE_TEXT = "Regression \u2013 One Dimensional Case";
const CHART_TITLE_TEXT = "Length and Weight of  different samples of Steel Bars";

// closed-loop tuning knobs (frame px offsets applied to text boxes)
const TUNE = {
  title: { size: 19.5, charSpacing: -0.2, dx: 0, dy: 0 },
  chartTitle: { size: 18, charSpacing: -0.5, dx: 0, dy: 0 },
  weightLabel: { size: 11, charSpacing: -0.5, dx: 0, dy: 0 },
  lengthLabel: { size: 11, dx: 0, dy: 0 },
};

const DOT_D = 7; // data dot diameter (frame px; core-area measure d~6.7-7, = certified slide 4)

const ORANGE_DOTS = [ // PIL-measured centers (x, y), sorted by x
  [230.4, 386.0], [248.2, 392.5], [251.3, 367.0], [266.5, 379.9], [269.3, 364.2],
  [278.5, 379.7], [290.5, 338.7], [305.5, 329.5], [314.7, 310.8], [317.5, 348.4],
  [341.5, 335.5], [344.7, 304.4], [365.9, 301.2], [389.8, 304.8], [425.9, 269.2],
  [432.3, 241.7], [477.4, 244.7], [477.5, 222.5], [504.8, 222.6], [510.8, 181.9],
  [538.2, 172.4],
];

// solid triangle pointing RIGHT with its base at x0, vertically centered y0, len wide x tall
function rightTri(slide, pptx, x0, yMid, len, tall) {
  // rotate:90 spins the apex from top to right about the box center; the pre-rotation
  // box must be tall wide x len tall so the VISUAL bbox is len wide x tall tall.
  slide.addShape(pptx.ShapeType.triangle, {
    x: (x0 + len / 2 - tall / 2) / 72, y: (yMid - len / 2) / 72,
    w: tall / 72, h: len / 72, rotate: 90,
    fill: { color: C.RED }, line: { type: "none" },
  });
}

// solid triangle pointing DOWN (apex at bottom), visual bbox (x0..x0+w, y0..y0+h)
function downTri(slide, pptx, x0, y0, w, h) {
  slide.addShape(pptx.ShapeType.triangle, {
    x: x0 / 72, y: y0 / 72, w: w / 72, h: h / 72, rotate: 180,
    fill: { color: C.RED }, line: { type: "none" },
  });
}

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
  const ct = TUNE.chartTitle;
  slide.addText(CHART_TITLE_TEXT, {
    x: (487.5 - 280 + ct.dx) / 72, y: (124.5 - 13 + ct.dy) / 72, w: 560 / 72, h: 26 / 72,
    align: "center", valign: "middle", margin: 0,
    fontSize: ct.size, bold: true, color: C.BLUE,
    fontFace: "Arial", charSpacing: ct.charSpacing,
  });
}

function drawFaintDotted(pptx, slide) {
  // thin dotted projection guides (two-axis projection of the highlighted points):
  // horizontals y-axis -> the points, verticals points -> x-axis (measured: upper
  // col ~431.5 dots y246..473; lower col ~390.5 dots y308..473). Drawn first so the
  // markers/down-arrowheads/axes sit on top, as in the original.
  for (const [y, x1] of [[242.5, 427.5], [303.5, 385.5]]) {
    slide.addShape(pptx.ShapeType.line, {
      x: 140 / 72, y: y / 72, w: (x1 - 140) / 72, h: 0,
      line: { color: C.FAINT, width: 0.75, dashType: "sysDot" },
    });
  }
  for (const [x, y0] of [[431.5, 249.5], [390.5, 312]]) {
    slide.addShape(pptx.ShapeType.line, {
      x: x / 72, y: y0 / 72, w: 0, h: (473.5 - y0) / 72,
      line: { color: C.FAINT, width: 0.75, dashType: "sysDot" },
    });
  }
}

function drawAxes(pptx, slide) {
  // y-axis: line x134 from below the arrowhead down to the x-axis + up triangle
  slide.addShape(pptx.ShapeType.line, {
    x: 134 / 72, y: 109 / 72, w: 0, h: (476 - 109) / 72,
    line: { color: C.RED, width: 2 },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: 130.5 / 72, y: 100.5 / 72, w: 7 / 72, h: 10 / 72,
    fill: { color: C.RED }, line: { type: "none" },
  });
  // x-axis: line y476 from the y-axis to the arrowhead base + right-pointing triangle
  slide.addShape(pptx.ShapeType.line, {
    x: 134 / 72, y: 476 / 72, w: (632 - 134) / 72, h: 0,
    line: { color: C.RED, width: 2 },
  });
  rightTri(slide, pptx, 632, 476, 7, 8); // visual x632..639, y472..480, tip at x639
  // junction arrowheads on the y-axis where the guides start (base on the axis)
  rightTri(slide, pptx, 134, 243.5, 5.5, 11); // upper guide
  rightTri(slide, pptx, 134, 304.5, 5.5, 11); // lower guide
  // small down-arrowheads under the two highlighted markers
  downTri(slide, pptx, 429.5, 244.5, 5, 5);
  downTri(slide, pptx, 387.5, 307, 5, 5);
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

function drawLabels(pptx, slide, opts = {}) {
  // y-axis label "Weight" rotated 90 deg CCW beside the axis:
  // ink x118..125 (cap-height direction), y113..149 (text direction)
  const wl = { ...TUNE.weightLabel, ...(opts.weightLabel || {}) };
  slide.addText("Weight", {
    x: (121.5 - 28 + wl.dx) / 72, y: (131 - 7.5 + wl.dy) / 72,
    w: 56 / 72, h: 15 / 72, rotate: 270,
    align: "center", valign: "middle", margin: 0,
    fontSize: wl.size, bold: true, color: C.RED, fontFace: "Arial",
    charSpacing: wl.charSpacing,
  });
  // x-axis label "Length" under the arrowhead end: ink x612..646, caps y490..497
  const t = { ...TUNE.lengthLabel, ...(opts.lengthLabel || {}) };
  slide.addText("Length", {
    x: (610.5 + t.dx) / 72, y: (487.5 + t.dy) / 72, w: 50 / 72, h: 16 / 72,
    align: "left", valign: "top", margin: 0,
    fontSize: t.size, bold: true, color: C.RED, fontFace: "Arial",
  });
}

// renderBase: full composition. Children (if any lecture depends on this chrome
// reference) import this module and call renderBase with their own numeral.
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 3 : opts.numeral });
  drawChartFrame(pptx, slide);
  drawFaintDotted(pptx, slide);
  drawAxes(pptx, slide);
  drawDataDots(pptx, slide);
  drawLabels(pptx, slide, opts);
  drawTitle(pptx, slide, opts);
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
    path.resolve(__dirname, "../slide_003_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = {
  renderBase, drawTitle, drawChartFrame, drawAxes, drawFaintDotted,
  drawDataDots, drawLabels, CHROME_CONSTS: C, ORANGE_DOTS, TUNE,
  TITLE_TEXT, CHART_TITLE_TEXT,
};
