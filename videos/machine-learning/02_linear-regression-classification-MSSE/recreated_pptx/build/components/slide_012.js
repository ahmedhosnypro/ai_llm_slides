// slide_012.js — "Classification – Two Dimensional Case" (ML lecture 02, MSSE deck)
// CHILD of certified slide 11 (founder edge 12 > 11; chain 9 → 11 → 12).
// PARENT of slide 13: after PASS this module is the banked composition for 13.
//
// Worker ml02-w012-gen4, 2026-10-13/14. Ground truth: PIL-measured from
// unique_slides/slide_012.jpg (960x540, 1px = 1pt); measurements banked in
// scratch/ml02/slide012/measure_1..29.txt.
//
// COMPOSITION — inherit from the certified parent component ./slide_011.js,
// draw only the measured delta:
//
//   INHERITED VERBATIM (crop-verified identical pixels in this frame):
//     - parent.drawTitle      (title ink + "Two" blue, identical)
//     - parent.drawPlotFrame  (L x87-89, R x861-863, T y100-101, B y523-524)
//     - parent.drawAxes11     (y-axis rows 117..492, x-head (626,488)-(639,495),
//                              Weight ink (109,118)-(120,156), Length (611,504)-(646,514))
//     - parent.drawCaption11  (caption glyphs at (574..831, 106..156) match)
//     - parent.drawLegend     (legend rows 1-2 only; row 3 measured ABSENT here)
//     - house chrome          (drawn ONCE, numeral 12 = printed frame number)
//
//   DELTA (this frame vs slide 11's):
//     - drawSteelMarkers12 : parent's 10 steel rings shifted (-36.6,-32)
//                            (measure_17: residual < 0.6px), ring 000000 d9.
//     - drawWoodMarkers12  : 11 own-measured rings (NOT parent's), light warm
//                            gray C4C1B8 (frame core (190..197,190..194,178..189)),
//                            d9.5, incl. the (395.5,320.5) ring missed by measure_19.
//     - drawUnknownMarkers12: ring-style (slide 11 had SOLID red discs):
//                            ?1 (428.5,179.5) open BLACK ring d24.5 + red '?';
//                            ?2 (521,243) / ?3 (306,352) warm-gray ring d25.5,
//                            faint warm fill EAE4DE, muted red '?' 894A55;
//                            glyphs 15pt bold (frame ink ~10x15-17px).
//     - drawModelBox12     : parent's box recipe (same w168 h64, fill FCFCE5,
//                            border 9090A8 0.75pt, same text offsets) at MY
//                            measured position (670,220) = parent's (670,276) - 56y.
//     - drawPlane          : tilted perspective quad — not natively drawable;
//                            generated image plane_s012.png (matplotlib 600dpi,
//                            boundary-sampled polyline, corrected quad
//                            T(478,109) R(640,220) B(273.5,457) L(137,296) —
//                            measure_27/28; the early R(599,195) corner was wrong),
//                            exact-size embed from plane_s012.json.
//     - drawEqBox          : (601,299)-(852,474) fill FCFCE5 border 9090A8 0.75pt.
//                            L1 'Model ( Plane )' red/green TNR bold italic 20pt
//                            + per-word underlines as line shapes (red 605-656,
//                            green 665-732 at y318);
//                            L2/L3 = certified mathtext runs (eq_s012_manifest.json,
//                            baselines 340.5/363.5);
//                            L4-L7 decision rules + params, TNR bold italic 18pt
//                            (s6-certified recipe), runs 'Class'/'rules red'/
//                            'Steel|Wood|Undefined' blue 000080, red 8B0000,
//                            baselines 401/423/446/468.5.
//     - drawPlotLabels     : 'Steel' (381,133)-(406,142) black 12pt;
//                            'Wood' (506,280)-(535,288) 867C66 12pt.
//     - drawCursor         : thin bent stroke tip (419,313)→bend(423,318.5)→
//                            tail(431.5,329.5) + short dash (441.5,306.5)→(436.5,314.5)
//                            + faint parallel trace (measure_24).
//
// Spec-vs-frame notes: badge = house canon (numeral 12); legend row 3 of the
// parent is NOT drawn here (verified absent: measure_23 legend-row3 check found
// only the plot-frame border and the model-box text in that region).

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const parent = require(path.resolve(__dirname, "slide_011.js"));
// slide_011 inherits drawTitle/drawPlotFrame/drawLegend from ITS parent (certified
// slide_009.js) without re-exporting them — require the certified grandparent
// component directly for those three (the same module slide_011 itself composes from).
const gp = require(path.resolve(__dirname, "slide_009.js"));
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

const PL = 1 / 72; // frame px -> inches

// ---- content constants (frame-measured) -------------------------------------
const RED = "8B0000";          // deck content red (glyph cores (122..159,0..31,8..31))
const BLUE = "000080";         // eq-box blue (frame core (32,20,119))
const GREEN = "008000";        // L1 '( Plane )' green (frame core (37,125,30); s6-certified)
const BLACK = "000000";
const MODEL_FILL = "FCFCE5";   // eq/model box fill (medians (251,253,229)/(245,246,225))
const MODEL_BORDER = "9090A8"; // box border family (cores (168..198,166..196,188..217))
const STEEL_RING = "000000";   // s12 steel ring core (6,11,13)
const WOOD_RING = "C4C1B8";    // s12 wood ring core (190..197,190..194,178..189)
const Q_WOOD_RING = "C4C1B8";  // ?2/?3 ring = wood-ring color (measure_29)
const Q_WOOD_FILL = "EAE4DE";  // ?2/?3 faint warm interior (median (233,229,224))
const Q_MUTED = "894A55";      // ?2/?3 glyph (cores (135,74,82)/(140,77,88))
const WOOD_LABEL = "867C66";   // 'Wood' plot label core (134,124,102)
const CURSOR_INK = "2F3237";   // cursor core (45,48,55)
const CURSOR_FAINT = "9096A0";

// ---- helpers ----------------------------------------------------------------
function ring(pptx, slide, cx, cy, d, color, width, fill) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: (cx - d / 2) * PL, y: (cy - d / 2) * PL, w: d * PL, h: d * PL,
    fill: fill ? { color: fill } : { type: "none" },
    line: { color, width },
  });
}
function lineSeg(pptx, slide, x1, y1, x2, y2, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: Math.min(x1, x2) * PL, y: Math.min(y1, y2) * PL,
    w: Math.abs(x2 - x1) * PL, h: Math.abs(y2 - y1) * PL,
    line: { color, width },
    flipV: (x2 - x1) * (y2 - y1) < 0, // preserve the measured direction
  });
}
function labelAt(pptx, slide, xPx, cyPx, text, opts = {}) {
  slide.addText(text, {
    x: xPx * PL, y: (cyPx / 72) - 0.3, w: (opts.wPx || 120) * PL, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontSize: opts.size || 12, bold: !!opts.bold, italic: !!opts.italic,
    color: opts.color || BLACK, fontFace: opts.fontFace || "Arial",
  });
}

// ---- delta blocks ------------------------------------------------------------

// Steel: parent's 10 certified centers + measured shift (-36.6,-32) (measure_17).
function drawSteelMarkers12(pptx, slide, opts = {}) {
  const markers = [
    [483.2, 156.6], [510.5, 147.2], [404.7, 222.5], [287.2, 285.4], [317.0, 279.0],
    [262.8, 313.5], [284.1, 317.0], [241.8, 338.7], [223.6, 341.6], [202.4, 360.7],
  ].map(([mx, my]) => [mx - 36.6, my - 32]);
  for (const [mx, my] of markers) ring(pptx, slide, mx, my, 9, STEEL_RING, 1);
}

// Wood: 11 own-measured centers (measure_19 + the (395.5,320.5) ring confirmed
// present; (531,244) in that list is ?2's ring, excluded).
function drawWoodMarkers12(pptx, slide, opts = {}) {
  const markers = [
    [578, 232], [551, 234], [494, 254], [551, 256], [438, 311], [463, 317],
    [395.5, 320.5], [394, 358], [341, 390], [352, 390], [321, 402],
  ];
  for (const [mx, my] of markers) ring(pptx, slide, mx, my, 9.5, WOOD_RING, 1);
}

// Unknown-class markers: ring-style this frame (slide 11's were solid red discs).
function drawUnknownMarkers12(pptx, slide, opts = {}) {
  // ?1 — steel side: open black ring + saturated red '?'
  ring(pptx, slide, 428.5, 179.5, 24.5, BLACK, 1.5);
  slide.addText("?", {
    x: (428.5 - 12.25) * PL, y: (179.5 - 12.25) * PL, w: 24.5 * PL, h: 24.5 * PL,
    align: "center", valign: "middle", bold: true, fontSize: 15,
    color: RED, fontFace: "Arial", margin: 0,
  });
  // ?2 / ?3 — wood side: warm-gray ring, faint warm fill, muted red '?'
  for (const [mx, my] of [[521, 243], [306, 352]]) {
    ring(pptx, slide, mx, my, 25.5, Q_WOOD_RING, 1.25, Q_WOOD_FILL);
    slide.addText("?", {
      x: (mx - 12.75) * PL, y: (my - 12.75) * PL, w: 25.5 * PL, h: 25.5 * PL,
      align: "center", valign: "middle", bold: true, fontSize: 15,
      color: Q_MUTED, fontFace: "Arial", margin: 0,
    });
  }
}

// Model box: parent's certified recipe translated to MY measured position.
function drawModelBox12(pptx, slide, opts = {}) {
  const bx = 670, by = 220;
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

// Decision plane: generated image, exact-size embed (single-version law).
function drawPlane(pptx, slide, opts = {}) {
  const info = JSON.parse(fs.readFileSync(path.resolve(__dirname, "../assets/plane_s012.json"), "utf8"));
  slide.addImage({
    path: path.resolve(__dirname, "../assets/plane_s012.png"),
    x: info.x_in, y: info.y_in, w: info.w_in, h: info.h_in,
  });
}

// Equation box + its seven lines.
function drawEqBox(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 601 * PL, y: 299 * PL, w: 251 * PL, h: 175 * PL,
    fill: { color: MODEL_FILL }, line: { color: MODEL_BORDER, width: 0.75 },
  });

  // L1 heading: 'Model ( Plane )' red/green, TNR bold italic 20pt (ink y303..316.5)
  slide.addText([
    { text: "Model ", options: { color: RED } },
    { text: "( Plane )", options: { color: GREEN } },
  ], {
    x: 604 * PL, y: (309.75 / 72) - 0.3, w: 140 * PL, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    bold: true, italic: true, fontFace: "Times New Roman", fontSize: 20,
  });
  // per-word colored underlines (measured rows 317-319, center y318)
  lineSeg(pptx, slide, 605, 318, 656, 318, RED, 1.25);
  lineSeg(pptx, slide, 665, 318, 732, 318, GREEN, 1.25);

  // L2/L3 certified mathtext runs (baselines 340.5 / 363.5 baked into the manifest)
  const EQ = JSON.parse(fs.readFileSync(path.resolve(__dirname, "../assets/eq_s012_manifest.json"), "utf8"));
  for (const ln of ["L2", "L3"]) {
    for (const run of EQ.lines[ln].runs) {
      slide.addImage({
        path: path.resolve(__dirname, "../assets", run.image),
        x: run.x_in, y: run.y_in, w: run.w_in, h: run.h_in,
      });
    }
  }

  // L4-L7 decision rules + parameters (baselines 401 / 423 / 446 / 468.5)
  // 'Class' ink 605-646, rules red 656-674, Steel 689-725, Wood 688-732,
  // Undefined 689-767; L7 blue 608-754 + red a/b/c 758-767/778-788/798-806.
  const rules = [
    [394, "  > 0", "   Steel"],
    [416.5, "  < 0", "   Wood"],
    [439.5, "  = 0", "   Undefined"],
  ];
  for (const [cy, cond, cls] of rules) {
    slide.addText([
      { text: "Class", options: { color: BLUE } },
      { text: cond, options: { color: RED } },
      { text: cls, options: { color: BLUE } },
    ], {
      x: 604 * PL, y: (cy / 72) - 0.3, w: 220 * PL, h: 0.6,
      align: "left", valign: "middle", margin: 0,
      bold: true, italic: true, fontFace: "Times New Roman", fontSize: 18,
    });
  }
  slide.addText([
    { text: "Model Parameters", options: { color: BLUE } },
    { text: " : ", options: { color: BLUE } },
    { text: "a", options: { color: RED } },
    { text: " , ", options: { color: BLUE } },
    { text: "b", options: { color: RED } },
    { text: " , ", options: { color: BLUE } },
    { text: "c", options: { color: RED } },
  ], {
    x: 606 * PL, y: (462 / 72) - 0.3, w: 220 * PL, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    bold: true, italic: true, fontFace: "Times New Roman", fontSize: 18,
  });
}

// In-plot class labels (absent in slide 11, present here).
function drawPlotLabels(pptx, slide, opts = {}) {
  labelAt(pptx, slide, 380, 137.5, "Steel", { size: 12, color: BLACK, wPx: 40 });
  labelAt(pptx, slide, 505, 284, "Wood", { size: 12, color: WOOD_LABEL, wPx: 40 });
}

// Small cursor scribble near the plane center (measure_24).
function drawCursor(pptx, slide, opts = {}) {
  lineSeg(pptx, slide, 419.5, 313, 423.5, 318.5, CURSOR_INK, 1.25);
  lineSeg(pptx, slide, 423.5, 318.5, 431.5, 329.5, CURSOR_INK, 1.25);
  lineSeg(pptx, slide, 427.5, 320.5, 435, 329.5, CURSOR_FAINT, 0.75);
  lineSeg(pptx, slide, 441.5, 306.5, 436.5, 314.5, "6A6F78", 0.75);
}

// ---- composition -------------------------------------------------------------
// opts.numeral overrides the badge numeral (default 12 = printed frame number).
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 12 : opts.numeral });
  gp.drawTitle(pptx, slide, opts);         // inherited verbatim (certified slide_009)
  gp.drawPlotFrame(pptx, slide, opts);     // inherited verbatim (certified slide_009)
  parent.drawAxes11(pptx, slide, opts);     // inherited verbatim
  drawPlane(pptx, slide, opts);             // NEW block (under all markers)
  drawSteelMarkers12(pptx, slide, opts);    // delta: shifted steel rings
  drawWoodMarkers12(pptx, slide, opts);     // delta: own wood rings
  drawUnknownMarkers12(pptx, slide, opts);  // delta: ring-style ?s
  drawCursor(pptx, slide, opts);            // NEW block
  drawPlotLabels(pptx, slide, opts);        // NEW block
  parent.drawCaption11(pptx, slide, opts);  // inherited verbatim
  gp.drawLegend(pptx, slide, opts);        // inherited verbatim (rows 1-2 only;
  //                                          legend row 3 measured ABSENT in this frame)
  drawModelBox12(pptx, slide, opts);        // delta: parent box at (670,220)
  drawEqBox(pptx, slide, opts);             // NEW block
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
    path.resolve(__dirname, "../../slide_012_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = {
  renderBase, drawSteelMarkers12, drawWoodMarkers12, drawUnknownMarkers12,
  drawModelBox12, drawPlane, drawEqBox, drawPlotLabels, drawCursor,
  build, RED, BLUE, GREEN, STEEL_RING, WOOD_RING,
};
