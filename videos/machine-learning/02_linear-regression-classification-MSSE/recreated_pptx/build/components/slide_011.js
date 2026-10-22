// slide_011.js — "Classification – Two Dimensional Case" (ML lecture 02, MSSE deck)
// CHILD of slide 9 (founder edge 11 > 9, founder caution: a component shares position
// AND size with slide 9's — inherit 9's certified component, draw only the delta).
// PARENT of slide 12 (same kind of dependency): after PASS this module is the banked
// composition for slide 12 to import.
//
// COMPOSITION (attempt 1, 2026-10-13) — every block PIL-verified against THIS slide's
// frame unique_slides/slide_011.jpg (measurements: scratch/ml02/slide011/MEASUREMENTS.md):
//
//   INHERITED VERBATIM from the certified parent build/components/slide_009.js
//   (crop-diff vs my frame: title 1.55 mean / 0 px>60; plot frame borders +-1px;
//   legend rows 1-2 2.91 mean / 0 px>60):
//     - parent.drawTitle       (ink (281,60)-(631,74), "Two" blue — identical pixels)
//     - parent.drawPlotFrame   (L x87-89, R x861-863, T y100-101, B y523-524)
//     - parent.drawLegend      (rows 1-2: markers (753,178)/(753,197), labels x770+)
//     - house chrome           (shared_patterns/house_chrome.js, drawn ONCE here, numeral 11)
//
//   REDRAWN AT INHERITED GEOMETRY (my frame differs; geometry = parent's, content mine):
//     - drawAxes11        : parent's axes shifted UP 4px (whole plot content shift (0,-4),
//                           frame unchanged); arrowheads at MY measured size (y-head 8x9 at
//                           apex (134,116); x-head 11.5x8.5, apex (639.5,491.5)); labels 11pt.
//     - drawSteelMarkers11: parent's steel block MINUS capsule fill MINUS 'Steel' plot label
//                           (both absent in my frame), 10 rings d9 = parent's centers + (0,-4),
//                           ring 000000 (frame core (13,14,12); parent's 595959 renders (100,102,100)).
//     - drawWoodMarkers11 : parent's wood block MINUS capsule MINUS label, 11 rings d9
//                           (NOT 12 — spec's (483,290) verified empty), = parent's centers +(0,-4),
//                           ring 917150 (probe-exact: renders (146,114,82) = frame core (146,115,82)).
//     - drawCaption11     : parent's caption geometry (x575,y100,w280,17pt bold,lineSpacing 26)
//                           with frame-true line2 word colors: 'Steel' 000000, 'wood' 917150
//                           (s9's frame line2 has the same pattern; the certified parent drew
//                           all-blue — expressed here as my delta, parent component untouched).
//     - drawModelBox11    : parent's model box SAME SIZE (w168xh64, fill FCFCE5, border 9090A8
//                           0.75pt, same box-relative text offsets) at MY measured position
//                           (670,276) = parent's (678,236) + (-8,+40).
//
//   NEW BLOCKS (not in parent):
//     - drawUnknownMarkers11: 3 solid 8B0000 d23 circles + white bold '?' 13pt at
//                           (429.4,180.1),(521.1,243.0),(306.9,353.3) (frame core (139,0,8)).
//     - drawLegendRow3    : solid 8B0000 d23 circle + white '?' at (751,232) + 2-line red bold
//                           label 'Belongs to' / 'Which Class ??' (x770, y220..241, pitch 13).
//
// Spec-vs-frame corrections applied (frame wins): outer frame = parent's plot frame (not the
// spec's (96,97)-(883,524)); model box border blue-gray 9090A8 + fill FCFCE5 (not spec's red
// FFFEE0); 11 wood markers (not 12); no in-plot Steel/Wood labels; badge = house canon.

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));
const parent = require(path.resolve(__dirname, "slide_009.js"));

// ---- content constants (frame px; 1px = 1pt = 1/72 in) ----------------------
// Values identical to the parent component's internal constants (the parent only
// exports RED/BLUE/STEEL_FILL/WOOD_FILL, so the rest are re-declared here — same
// certified values, re-verified against THIS frame; see MEASUREMENTS.md).
const RED = "8B0000";            // content red (verified: '?' core (139,0,8), title pixels = parent's)
const BLUE = "000080";           // caption blue (core (0,0,107))
const MODEL_FILL = "FCFCE5";     // frame fill mean (251.3,252.6,230.5)
const MODEL_BORDER = "9090A8";   // frame border darkest-15 (167,163,188) vs parent's (156,153,183)
const BLACK = "000000";
const STEEL_RING = "000000";       // s11 steel ring core (13,14,12) — near-black
const WOOD_RING = "917150";        // probe-exact: renders (146,114,82) = frame core (146,115,82)

const PL = 1 / 72; // px -> inch

// ---- per-block draws (component exports; slide 12 imports these) ------------

// Axes: parent's certified axis positions shifted up 4px (measured: y-axis apex
// (134,116) vs parent's (134,120); x-axis y491.5 vs 495; labels shifted identically),
// arrowheads at MY frame's measured size (smaller than the parent's drawn heads).
function drawAxes11(pptx, slide, opts = {}) {
  // y-axis line: x 133.5, y 117..491.5 (top hidden under the head)
  slide.addShape(pptx.ShapeType.line, {
    x: 133.5 * PL, y: 117 * PL, w: 0, h: (491.5 - 117) * PL,
    line: { color: RED, width: 1.75 },
  });
  // y-axis up arrowhead: apex (134.5,115.5), base y124.5, wings x130.5..138.5 (measured 8x9)
  slide.addShape(pptx.ShapeType.triangle, {
    x: 130.5 * PL, y: 115.5 * PL, w: 8 * PL, h: 9 * PL,
    fill: { color: RED }, line: { type: "none" },
  });
  // x-axis line: y 491.5, x 133.5..628.5
  slide.addShape(pptx.ShapeType.line, {
    x: 133.5 * PL, y: 491.5 * PL, w: (628.5 - 133.5) * PL, h: 0,
    line: { color: RED, width: 1.75 },
  });
  // x-axis right arrowhead: apex (639.5,491.5), base x628, wings y487.25..495.75 (measured 11.5x8.5)
  slide.addShape(pptx.ShapeType.triangle, {
    x: 628 * PL, y: 487.25 * PL, w: 11.5 * PL, h: 8.5 * PL,
    fill: { color: RED }, line: { type: "none" },
    rotate: 90, // apex pointing RIGHT
  });
  // "Weight" label rotated 90deg CCW, ink (110,119)-(119,155) = parent's ink -4px
  slide.addText("Weight", {
    x: (114.5 - 30) * PL, y: (137 - 30) * PL, w: 60 * PL, h: 60 * PL,
    rotate: 270, align: "center", valign: "middle",
    fontSize: 11, color: RED, fontFace: "Arial", margin: 0, bold: false, italic: false,
  });
  // "Length" label under the x-axis arrow end — MY frame ink (612,504)-(646,514),
  // center (629,509): box centered on 629 (parent's box centered 638 put the ink 9px
  // right of this frame's measured position; selfcheck_1 flagged it, fixed).
  slide.addText("Length", {
    x: 591 * PL, y: 500 * PL, w: 76 * PL, h: 18 * PL,
    align: "center", valign: "middle", fontSize: 11, color: RED,
    fontFace: "Arial", margin: 0,
  });
}

// Steel markers: 10 open circles d9, ring BLACK — parent's steel marker centers + (0,-4).
// NO capsule fill, NO 'Steel' plot label (both measured absent in this frame).
function drawSteelMarkers11(pptx, slide, opts = {}) {
  const markers = [
    [483.2, 156.6], [510.5, 147.2], [404.7, 222.5], [287.2, 285.4], [317.0, 279.0],
    [262.8, 313.5], [284.1, 317.0], [241.8, 338.7], [223.6, 341.6], [202.4, 360.7],
  ];
  for (const [mx, my] of markers) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: (mx - 4.5) * PL, y: (my - 4.5) * PL, w: 9 * PL, h: 9 * PL,
      fill: { type: "none" }, line: { color: STEEL_RING, width: 1 },
    });
  }
}

// Wood markers: 11 open circles d9, ring 917150 — parent's wood marker centers + (0,-4).
// NO capsule fill, NO 'Wood' plot label (both measured absent in this frame).
function drawWoodMarkers11(pptx, slide, opts = {}) {
  const markers = [
    [537.8, 267.2], [510.5, 266.9], [511.2, 288.7], [450.3, 288.2], [423.2, 348.0],
    [400.1, 345.8], [353.6, 354.1], [351.0, 392.0], [308.8, 424.0], [302.0, 424.0],
    [281.3, 436.1],
  ];
  for (const [mx, my] of markers) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: (mx - 4.5) * PL, y: (my - 4.5) * PL, w: 9 * PL, h: 9 * PL,
      fill: { type: "none" }, line: { color: WOOD_RING, width: 1 },
    });
  }
}

// Unknown-class markers (NEW vs parent): 3 solid RED (8B0000) circles d23 with a
// centered white bold '?' — measured centers, red core (139,0,8) = 8B0000.
function drawUnknownMarkers11(pptx, slide, opts = {}) {
  const markers = [[429.4, 180.1], [521.1, 243.0], [306.9, 353.3]];
  for (const [mx, my] of markers) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: (mx - 11.5) * PL, y: (my - 11.5) * PL, w: 23 * PL, h: 23 * PL,
      fill: { color: RED }, line: { type: "none" },
    });
    slide.addText("?", {
      x: (mx - 11.5) * PL, y: (my - 11.5) * PL, w: 23 * PL, h: 23 * PL,
      align: "center", valign: "middle", bold: true, fontSize: 13,
      color: "FFFFFF", fontFace: "Arial", margin: 0,
    });
  }
}

// Caption (legend header): parent's certified geometry (x575, y100, w280, 17pt bold,
// lineSpacing 26) with frame-true line2 word colors ('Steel' black, 'wood' 917150).
// Line1 text identical to parent's (crop-diff vs frame 2.14 mean, 0 px>60).
function drawCaption11(pptx, slide, opts = {}) {
  slide.addText(
    [
      { text: "Length and Weight of different", options: { color: BLUE, breakLine: true } },
      { text: "samples of ", options: { color: BLUE } },
      { text: "Steel", options: { color: BLACK } },
      { text: " and ", options: { color: BLUE } },
      { text: "wood", options: { color: WOOD_RING } },
      { text: " Bars", options: { color: BLUE } },
    ],
    {
      x: 575 * PL, y: 100 * PL, w: 280 * PL, h: 60 * PL,
      align: "left", valign: "top", bold: true, fontSize: 17,
      fontFace: "Arial", margin: 0, lineSpacing: 26,
    }
  );
}

// Legend row 3 (NEW vs parent): solid red '?' circle d23 at (751,232) + two-line
// red bold label 'Belongs to' / 'Which Class ??' (ink x770..851, y220..241, pitch 13px).
function drawLegendRow3(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: 739.5 * PL, y: 220.5 * PL, w: 23 * PL, h: 23 * PL,
    fill: { color: RED }, line: { type: "none" },
  });
  slide.addText("?", {
    x: 739.5 * PL, y: 220.5 * PL, w: 23 * PL, h: 23 * PL,
    align: "center", valign: "middle", bold: true, fontSize: 13,
    color: "FFFFFF", fontFace: "Arial", margin: 0,
  });
  slide.addText(
    [
      { text: "Belongs to", options: { breakLine: true } },
      { text: "Which Class ??", options: {} },
    ],
    {
      x: 768 * PL, y: 215.5 * PL, w: 95 * PL, h: 32 * PL,
      align: "left", valign: "top", bold: true, fontSize: 11,
      color: RED, fontFace: "Arial", margin: 0, lineSpacing: 13,
    }
  );
}

// Model box: parent's certified box SAME SIZE (w168 h64, fill FCFCE5, border 9090A8
// 0.75pt, same box-relative text offsets) translated to MY measured position (670,276)
// = parent's (678,236) + (-8,+40).
function drawModelBox11(pptx, slide, opts = {}) {
  const bx = 670, by = 276;
  slide.addShape(pptx.ShapeType.rect, {
    x: bx * PL, y: by * PL, w: 168 * PL, h: 64 * PL,
    fill: { color: MODEL_FILL }, line: { color: MODEL_BORDER, width: 0.75 },
  });
  slide.addText("Model", {
    x: (bx + 6) * PL, y: (by + 2) * PL, w: 62 * PL, h: 21 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 15,
    color: RED, fontFace: "Arial", margin: 0, underline: { style: "sng" },
  });
  slide.addText("I/P: Length, Weight", {
    x: (bx + 6) * PL, y: (by + 23) * PL, w: 160 * PL, h: 19 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 13,
    color: BLACK, fontFace: "Arial", margin: 0,
  });
  slide.addText("O/P: Class Type", {
    x: (bx + 6) * PL, y: (by + 42) * PL, w: 160 * PL, h: 19 * PL,
    align: "left", valign: "middle", bold: true, fontSize: 13,
    color: BLACK, fontFace: "Arial", margin: 0,
  });
}

// renderBase: full certified composition of slide 11.
// opts.numeral overrides the badge numeral (default 11 = printed number on the frame).
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 11 : opts.numeral });
  parent.drawTitle(pptx, slide, opts);      // inherited verbatim
  parent.drawPlotFrame(pptx, slide, opts);  // inherited verbatim
  drawAxes11(pptx, slide, opts);            // redrawn at inherited geometry (shift (0,-4))
  drawSteelMarkers11(pptx, slide, opts);    // redrawn: parent's markers, no capsule/label
  drawWoodMarkers11(pptx, slide, opts);     // redrawn: parent's markers, no capsule/label
  drawUnknownMarkers11(pptx, slide, opts);  // new block
  drawCaption11(pptx, slide, opts);         // redrawn: parent geometry + colored words
  parent.drawLegend(pptx, slide, opts);     // inherited verbatim (rows 1-2)
  drawLegendRow3(pptx, slide, opts);        // new block
  drawModelBox11(pptx, slide, opts);        // redrawn: parent box at measured position
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
  const out =
    process.argv[2] ||
    path.resolve(__dirname, "../../slide_011_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = {
  renderBase, drawAxes11, drawSteelMarkers11, drawWoodMarkers11,
  drawUnknownMarkers11, drawCaption11, drawLegendRow3, drawModelBox11,
  build, RED, BLUE, STEEL_RING, WOOD_RING,
};
