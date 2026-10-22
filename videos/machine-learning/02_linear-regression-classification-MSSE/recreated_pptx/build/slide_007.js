// slide_007.js — "Linear Models for 1-D, 2-D, and d-D Input Vectors" (ML lecture 02)
// Root slide (no parents; no children in this deck's dep graph — component banked
// playlist-scoped after PASS).
//
// Ground truth: unique_slides/slide_007.jpg (960x540, 1px = 1pt = 1/72 in).
// All geometry PIL-measured (scratch/ml02/slide007/measure3-11.py, 2026-10-13).
// House chrome: shared_patterns/house_chrome.js (THIS deck: white canvas, gray E9E9E7
// panel x61..899 y46->bottom, C00000 1pt border, badge FDFD96 center (876,73) d35 ring
// 6A5ACD, numeral 7 = the number printed on the original).
//
// Fonts (width-matched against the frame): model/genbox box text = Arial Narrow 10.5pt
// (per-word boxes at measured x — the original uses tab-sized gaps); banner text =
// Arial bold 14.5 single line vertically centered in the banner (judge attempt-1
// MAJOR#1 fix — 21.5pt Narrow wrapped and spilled); General Case = Arial bold 14.5
// (MAJOR#2 fix — 24pt filled the tab and crossed the genbox top border, which the
// original draws BEHIND the banner at row 130); equations + Model(X) + Parameters
// lines = STIX serif mathtext chunks (600dpi transparent PNGs, professional 2D
// format, baseline-law alignment, width-matched per line); stack labels = mathtext
// PNGs. R "Model Parameters" line = per-chunk ink-targeted r4_* placement on the
// measured baseline 492 (MAJOR#4 fix — subscript bottoms 494.9 < box bottom 497);
// R I/P list uses compact subscripts (MINOR#5). Middle plot = generated 3D
// fitted-plane image (graphgen mplot3d ortho, calibrated to the measured axis
// endpoints) + native red ?-ellipse and 2 red dot overlays.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const px = (v) => v / 72; // frame px -> inches (1px = 1pt)
const NUD = 2.5;          // LO valign-middle ink sits ~2.5 frame px high; nudge down

const C = {
  bannerRed: "8B0000", bannerGreen: "006400", white: "FFFFFF",
  boxBorder: "0000A8", softBorder: "8080B0", paleYellow: "FFFFE0",
  genboxFill: "F8F8F8", axisRed: "B97A87", regBlack: "000000",
  dotSienna: "A0522D", magenta: "FF00FF", pointRed: "C00000",
  containerFill: "C0B0A0", containerBorder: "6B4423",
  bannerBlue: "0000A8", bracketRed: "C98494",
  eqBlue: "0000CC", eqRed: "C00000", eqGreen: "006400", textDark: "000000",
};
const NARROW = "Arial Narrow";

const EQ = JSON.parse(fs.readFileSync(path.join(__dirname, "assets/eq/eq_manifest.json"), "utf8"));
function chunks(names) { return names.map((n) => EQ[n]); }
// place mathtext chunks left-to-right on one baseline (inches); returns right edge
function addChunks(slide, chs, xStartIn, baselineIn) {
  let x = xStartIn;
  for (const info of chs) {
    slide.addImage({ path: info.path, x, y: baselineIn - info.baseline_frac * info.h_in,
      w: info.w_in, h: info.h_in });
    x += info.w_in;
  }
  return x;
}
function addTextLine(slide, runs, opts) {
  slide.addText(runs, Object.assign({
    fontFace: NARROW, margin: 0, align: "left", valign: "middle",
  }, opts));
}
// single-line text box pinned by ink-band center y (frame px) + height h (frame px)
function lineBox(cx, cy, w, h, runs, fontSize) {
  return {
    x: px(cx), y: px(cy - h / 2 + NUD), w: px(w), h: px(h),
    fontSize, valign: "middle", align: "left",
  };
}

// ---- per-block draws (component exports) -----------------------------------
function drawBanners(pptx, slide) {
  // Rects measured on the frame: L (103,80)-(254,104), M (338,80)-(489,104),
  // R green (640,80)-(791,104). Text = Arial bold 14.5 single line, ink rows
  // 87..97 (cap ~10px), vertically centered — box nudged +NUD like lineBox.
  const banners = [
    { x: 103, y: 80, w: 152, h: 25, fill: C.bannerRed, text: "Input Vector: 1-D" },
    { x: 338, y: 80, w: 152, h: 25, fill: C.bannerRed, text: "Input Vector: 2-D" },
    { x: 640, y: 80, w: 152, h: 25, fill: C.bannerGreen, text: "Input Vector: d-D" },
  ];
  for (const b of banners) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      fill: { color: b.fill }, line: { color: b.fill, width: 0.5 },
    });
    slide.addText(b.text, {
      x: px(b.x), y: px(b.y - 1.1), w: px(b.w), h: px(b.h),
      align: "center", valign: "middle", fontSize: 14.5, bold: true,
      color: C.white, fontFace: "Arial", margin: 0,
    });
  }
}

function drawPlotBoxes(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(66), y: px(128), w: px(226), h: px(204),
    fill: { color: C.white }, line: { color: C.boxBorder, width: 1 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(314), y: px(128), w: px(242), h: px(204),
    fill: { color: C.white }, line: { color: C.boxBorder, width: 1 },
  });
}

function drawLeftPlot(pptx, slide) {
  const line = (x1, y1, x2, y2, color, width, dash) => {
    const x = Math.min(x1, x2), y = Math.min(y1, y2);
    slide.addShape(pptx.ShapeType.line, {
      x: px(x), y: px(y), w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
      flipV: (x2 - x1) * (y2 - y1) < 0,
      line: { color, width, dashType: dash || "solid" },
    });
  };
  line(78.5, 133, 78.5, 316, C.axisRed, 1);        // y-axis (red-pink)
  line(76, 316.5, 289, 316.5, C.axisRed, 1);       // x-axis
  line(98, 295, 282, 168, C.regBlack, 1.75);       // regression line
  line(80, 216, 209, 216, C.magenta, 1, "sysDot"); // projection horizontal
  line(211, 217, 211, 316, C.magenta, 1, "sysDot");// projection vertical
  const dots = [[277,166],[263,174],[261,190],[249,193],[226,201],[247,203],[222,214],
    [194,231],[184,231],[206,232],[168,234],[164,244],[182,248],[157,249],[170,254],
    [146,260],[138,263],[146,268],[151,269],[127,273],[136,274]];
  for (const [cx, cy] of dots) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(cx - 2.2), y: px(cy - 2.2), w: px(4.4), h: px(4.4),
      fill: { color: C.dotSienna }, line: { color: C.dotSienna, width: 0.25 },
    });
  }
  slide.addShape(pptx.ShapeType.ellipse, { // red point at the projection origin
    x: px(207.5), y: px(213.5), w: px(5), h: px(5),
    fill: { color: C.pointRed }, line: { color: C.pointRed, width: 0.25 },
  });
  for (const [mx, my, mw, mh] of [[76, 132, 5, 5], [69, 149, 5, 5], [271, 322, 13, 5], [281, 314, 5, 5]]) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(mx), y: px(my), w: px(mw), h: px(mh),
      fill: { color: C.axisRed }, line: { color: C.axisRed, width: 0.25 },
    });
  }
  // axis labels (orig ink: "Weight" rotated rows 131..155 cols 69..75, left of the
  // y-axis; "Length" rows 322..328 cols 265..286 under the x-axis) — MAJOR#3 fix
  slide.addText("Weight", {
    x: px(57), y: px(140), w: px(30), h: px(10), rotate: 270,
    align: "center", valign: "middle", fontSize: 7.5,
    color: C.textDark, fontFace: "Arial", margin: 0,
  });
  slide.addText("Length", {
    x: px(260.5), y: px(322), w: px(30), h: px(10),
    align: "center", valign: "middle", fontSize: 7.5,
    color: C.textDark, fontFace: "Arial", margin: 0,
  });
}

function drawMidPlot(pptx, slide) {
  slide.addImage({
    path: path.join(__dirname, "assets/mplot_plane.png"),
    x: px(314), y: px(128), w: px(241), h: px(203),
  });
  // solid red ?-badge on the plane's left edge (measured disc ~(384,227) d~14)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(377), y: px(220), w: px(14), h: px(14),
    fill: { color: C.pointRed }, line: { color: "8B0000", width: 0.75 },
  });
  slide.addText("?", {
    x: px(377), y: px(220), w: px(14), h: px(14),
    align: "center", valign: "middle", fontSize: 9, bold: true,
    color: C.white, fontFace: "Arial", margin: 0,
  });
  // red projection rectangle: the ?-point dropped to the Length axis
  slide.addShape(pptx.ShapeType.rect, {
    x: px(384), y: px(228), w: px(69), h: px(29),
    fill: { color: C.white, transparency: 100 }, line: { color: C.pointRed, width: 0.75 },
  });
  // crosshair red dots on the Length axis (453,257) and Radius axis (326,314)
  for (const [cx, cy] of [[453, 257], [326, 314]]) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(cx - 5), y: px(cy), w: px(10), h: 0, line: { color: C.pointRed, width: 0.75 },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: px(cx), y: px(cy - 5), w: 0, h: px(10), line: { color: C.pointRed, width: 0.75 },
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(cx - 3), y: px(cy - 3), w: px(6), h: px(6),
      fill: { color: C.pointRed }, line: { color: C.pointRed, width: 0.25 },
    });
  }
}

function drawRightContainer(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(570), y: px(113), w: px(324), h: px(403),
    fill: { color: C.containerFill }, line: { color: C.containerBorder, width: 1 },
  });
  slide.addShape(pptx.ShapeType.rect, { // genbox — orig (578,130)-(833,330),
    x: px(578), y: px(130), w: px(256), h: px(200),   // top border passes BEHIND the banner
    fill: { color: C.genboxFill }, line: { color: C.bannerBlue, width: 1 },
  });
  slide.addShape(pptx.ShapeType.rect, { // General Case banner — orig (639,118)-(792,142)
    x: px(639), y: px(118), w: px(154), h: px(25),
    fill: { color: C.bannerBlue }, line: { color: C.bannerBlue, width: 0.5 },
  });
  slide.addText("General Case", { // Arial bold 14.5, ink (670,125)-(761,134)
    x: px(639), y: px(116.9), w: px(154), h: px(25),
    align: "center", valign: "middle", fontSize: 14.5, bold: true,
    color: C.white, fontFace: "Arial", margin: 0,
  });
  // tall pale-red paren pair around the stack (delimiters-spanning-arc pattern:
  // ONE half-turn arc per side; bulge on the measured stroke columns 660/688)
  const CURL = px(6);
  slide.addShape(pptx.ShapeType.arc, {
    x: px(660), y: px(152.4), w: CURL, h: px(163.2), angleRange: [90, 270],
    fill: { transparency: 100 }, line: { color: C.bracketRed, width: 1.5 },
  });
  slide.addShape(pptx.ShapeType.arc, {
    x: px(681.5), y: px(152.4), w: CURL, h: px(163.2), angleRange: [270, 450],
    fill: { transparency: 100 }, line: { color: C.bracketRed, width: 1.5 },
  });
  const stack = [ // mathtext PNGs centered x=674
    ["s_x1", 175.5], ["s_x2", 200.5], ["s_x3", 225.5],
    ["s_dots", 255], ["s_dots", 278.5], ["s_xd", 300.5],
  ];
  for (const [name, cy] of stack) {
    const info = EQ[name];
    slide.addImage({ path: info.path, x: px(674) - info.w_in / 2,
      y: px(cy) - info.h_in / 2, w: info.w_in, h: info.h_in });
  }
  slide.addText([{ text: "Input:", options: { color: C.pointRed, bold: true } }], {
    x: px(604), y: px(222), w: px(52), h: px(16),
    fontFace: "Arial", fontSize: 16, margin: 0,
    align: "left", valign: "middle",
  });
  slide.addText([{ text: "Output: (", options: { color: C.bannerBlue, bold: true } },
  { text: "y", options: { color: C.bannerBlue, bold: true, italic: true } },
  { text: ")", options: { color: C.bannerBlue, bold: true } }], {
    x: px(721), y: px(222), w: px(104), h: px(16),
    fontFace: "Arial", fontSize: 16, charSpacing: 0.7, margin: 0,
    align: "left", valign: "middle",
  });
}

function drawModelBoxes(pptx, slide) {
  const boxes = [
    { x: 67, y: 341, w: 176, h: 57 },
    { x: 313, y: 342, w: 236, h: 58 },
    { x: 578, y: 343, w: 231, h: 57 },
  ];
  for (const b of boxes) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      fill: { color: C.paleYellow }, line: { color: C.softBorder, width: 0.75 },
    });
  }
  const word = (x, baseline, text, color, tracking) => {
    // LO puts the 16pt baseline ~5.6px below the box center; box h=16
    slide.addText([{ text, options: { color } }], {
      x: px(x), y: px(baseline - 5.6 - 8), w: px(190), h: px(16),
      fontFace: NARROW, fontSize: 16, charSpacing: tracking || 0,
      margin: 0, align: "left", valign: "middle",
    });
  };
  // L box (bands: Model 348..359, I/P 362..377, O/P 378..396)
  word(76, 359, "Model", C.eqRed);
  word(76, 373.6, "I/P:", C.textDark);
  word(109, 373.6, "Length", C.textDark);
  word(175, 373.6, "[x]", C.eqRed);
  word(76, 392.5, "O/P:", C.textDark);
  word(109, 392.5, "Weight", C.textDark);
  word(177, 392.5, "[y]", C.eqRed);
  // M box (Model 347..365, I/P 364..381, O/P 381..399)
  word(322, 361, "Model", C.eqRed);
  word(322, 378, "I/P:", C.textDark);
  word(354, 378, "Length,", C.textDark);
  word(409, 378, "Radius", C.textDark);
  word(473, 378, "[x,y]", C.eqRed);
  word(322, 395, "O/P:", C.textDark);
  word(355, 395, "Weight", C.textDark);
  word(474, 395, "[z]", C.eqRed);
  // R box (Model 345..363, I/P 363..382, O/P 382..400)
  word(587, 361, "Model", C.eqRed);
  word(587, 376.5, "I/P:", C.textDark);
  // R I/P list with compact subscripts (MINOR#5; orig ink 637..783, main rows
  // 367..375) — subscript runs at reduced size so LO's -40% shift stays compact
  slide.addText([
    { text: "[X", options: { color: C.eqRed } },
    { text: "1", options: { color: C.eqRed, subscript: true, fontSize: 10.5 } },
    { text: ", X", options: { color: C.eqRed } },
    { text: "2", options: { color: C.eqRed, subscript: true, fontSize: 10.5 } },
    { text: ", X", options: { color: C.eqRed } },
    { text: "3", options: { color: C.eqRed, subscript: true, fontSize: 10.5 } },
    { text: ", .... X", options: { color: C.eqRed } },
    { text: "d", options: { color: C.eqRed, subscript: true, fontSize: 10.5 } },
    { text: "]", options: { color: C.eqRed } },
  ], {
    x: px(637), y: px(376.5 - 5.6 - 8), w: px(190), h: px(16),
    fontFace: NARROW, fontSize: 16, charSpacing: 2.0,
    margin: 0, align: "left", valign: "middle",
  });
  word(587, 397, "O/P:", C.textDark);
  word(636, 397, "[Y]", C.eqRed);
}

function drawEqBoxes(pptx, slide) {
  const boxes = [
    { x: 67, y: 408, w: 178, h: 106 },
    { x: 313, y: 410, w: 236, h: 105 },
    { x: 578, y: 411, w: 313, h: 86 },
  ];
  for (const b of boxes) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      fill: { color: C.paleYellow }, line: { color: C.softBorder, width: 0.75 },
    });
  }
  // L_eq (baselines calibrated vs measured bands; see eq_place notes)
  slide.addText([
    { text: "Model ", options: { color: C.eqRed, bold: true, italic: true } },
    { text: "( Line )", options: { color: C.eqGreen, bold: true, italic: true } },
  ], { x: px(75), y: px(409.5), w: px(140), h: px(18),
       fontFace: NARROW, fontSize: 17, margin: 0, align: "left", valign: "middle" });
  slide.addShape(pptx.ShapeType.line, { x: px(70), y: px(426.5), w: px(115), h: 0,
    line: { color: "8B0000", width: 1.5 } });
  addChunks(slide, chunks(["l2_y", "l2_a", "l2_x", "l2_b"]), px(76), px(451));
  addChunks(slide, chunks(["l3_w", "l3_a", "l3_mul", "l3_len", "l3_b"]), px(76), px(479));
  slide.addText([
    { text: "Model Parameters : ", options: { color: C.eqBlue, bold: true } },
    { text: "a", options: { color: C.eqRed, bold: true } },
    { text: " , ", options: { color: C.eqBlue, bold: true } },
    { text: "b", options: { color: C.eqRed, bold: true } },
  ], { x: px(75), y: px(499), w: px(175), h: px(15),
       fontFace: "Arial", fontSize: 13.5, margin: 0, align: "left", valign: "middle" });
  // M_eq
  slide.addText([
    { text: "Model ", options: { color: C.eqRed, bold: true, italic: true } },
    { text: "( Plane )", options: { color: C.eqGreen, bold: true, italic: true } },
  ], { x: px(319), y: px(414.5), w: px(140), h: px(18),
       fontFace: NARROW, fontSize: 17, margin: 0, align: "left", valign: "middle" });
  slide.addShape(pptx.ShapeType.line, { x: px(316), y: px(430.5), w: px(128), h: 0,
    line: { color: "8B0000", width: 1.5 } });
  addChunks(slide, chunks(["m2_z", "m2_a", "m2_x", "m2_b", "m2_y", "m2_c"]), px(319), px(449.5));
  addChunks(slide, chunks(["m3_w", "m3_a", "m3_len", "m3_b", "m3_rad", "m3_c"]), px(319), px(472.5));
  slide.addText([
    { text: "Model Parameters : ", options: { color: C.eqBlue, bold: true } },
    { text: "a", options: { color: C.eqRed, bold: true } },
    { text: " , ", options: { color: C.eqBlue, bold: true } },
    { text: "b", options: { color: C.eqRed, bold: true } },
    { text: " , ", options: { color: C.eqBlue, bold: true } },
    { text: "c", options: { color: C.eqRed, bold: true } },
  ], { x: px(319), y: px(503), w: px(185), h: px(15),
       fontFace: "Arial", fontSize: 13.5, margin: 0, align: "left", valign: "middle" });
  // R_eq
  slide.addText([
    { text: "Model ", options: { color: C.eqRed, bold: true, italic: true } },
    { text: "( Hyperplane )", options: { color: C.eqGreen, bold: true, italic: true } },
  ], { x: px(584), y: px(411.3), w: px(200), h: px(19),
       fontFace: NARROW, fontSize: 19, margin: 0, align: "left", valign: "middle" });
  slide.addShape(pptx.ShapeType.line, { x: px(585), y: px(429.5), w: px(169), h: 0,
    line: { color: "8B0000", width: 1.5 } });
  addChunks(slide, chunks(["r2_y", "r2_w1", "r2_x1", "r2_w2", "r2_x2", "r2_w3",
    "r2_x3", "r2_wd", "r2_xd", "r2_wd1"]), px(584), px(453.5));
  // R "Model Parameters" line — professional 2D mathtext chunks (r4_*), per-chunk
  // ink-targeted placement on the measured baseline 492 (MAJOR#4 fix: the text-run
  // "d+1" subscript hung to 499.3, past the box bottom 497; chunk subscript bottoms
  // land 494.9). Targets = orig ink starts (585/720/740/747/774/779/800/838) minus
  // the 0.96px STIX left bearing.
  const R4B = 492 / 72;
  for (const [name, xInk] of [["r4_mp", 584.04], ["r4_w1", 719.04], ["r4_c1", 739.04],
    ["r4_w2", 746.04], ["r4_c2", 773.04], ["r4_w3", 778.04],
    ["r4_dots_t", 799.04], ["r4_wd1", 837.04]]) {
    const info = EQ[name];
    slide.addImage({ path: info.path, x: px(xInk), y: R4B - info.baseline_frac * info.h_in,
      w: info.w_in, h: info.h_in });
  }
}

function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 7 : opts.numeral });
  drawRightContainer(pptx, slide);
  drawBanners(pptx, slide);
  drawPlotBoxes(pptx, slide);
  drawLeftPlot(pptx, slide);
  drawMidPlot(pptx, slide);
  drawModelBoxes(pptx, slide);
  drawEqBoxes(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "slide-recreation";
  pptx.title = "Linear Models for 1-D, 2-D, and d-D Input Vectors";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] ||
    path.resolve(__dirname, "../slide_007_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawBanners, drawPlotBoxes, drawLeftPlot, drawMidPlot,
  drawRightContainer, drawModelBoxes, drawEqBoxes };
