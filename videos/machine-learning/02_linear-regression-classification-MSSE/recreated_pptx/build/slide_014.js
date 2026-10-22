// slide_014.js — "Same Equation for Linear Regression and Classification"
// ML lecture 02 (machine-learning/02_linear-regression-classification-MSSE), ROOT slide.
// Worker ml02-w014-a4 (gen-4, resumed from gen-3 banked measurements), 2026-10-13.
//
// Ground truth: PIL-measured from unique_slides/slide_014.jpg (960x540, 1px=1pt).
// All math glyphs: matplotlib mathtext (STIX) -> 600dpi transparent PNGs -> ink-tight
// -> scaled to the frame's MEASURED ink spans (aspect-fit; parens stretched) ->
// embedded at exact px/600 size, top/baseline-anchored at measured positions.
// Shared trio component (14/15/16): canonical asset eq_shared_141516_core.png
// (minted by ml02-w015-a3, single-color #2108AA) was PIL-verified against THIS
// frame and DIFFERS (this frame's equation is multicolor with verbatim duplicate
// w_2 x_2) -> derived variant eq_014_core.png banked per the dispatch protocol;
// derivation recorded in qa/slide014/worker_report.md.
//
// Measured facts baked in (frame px):
//   title ink x156..752 y68..90 (blue "Same Equation" underlined x157..318 + red rest), center 454
//   modelbox x72..289 y105..183 FBFDE5 (Model, I/P row, O/P row)
//   regbox   x72..483 y226..341 FBFDE5 (Model, eq @baseline267.5, params @308.5, bias)
//   banner1  x72..300 y194..218 0000CC | banner2 x72..299(70..299 meas) y378..402
//   clsbox   x69..502 y411..524 FBFDE5 (Model, eq @baseline452.5, rules, params @516.5)
//   diagbox  x517..886 y212..404 FFFFFF (Input:/X= red, W= blue + underline, Output: (y) dark)
//   rules: y>0 / y<0 / y=0 RED conditions, y + arrows + Class n + Undefined BLUE (measured)
//   X/W columns: 6 rows each (3 entries, two 3-dot rows, final entry), tall parens

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const ASSETS = path.resolve(__dirname, "assets");
const MAN = (n) => JSON.parse(fs.readFileSync(path.resolve(ASSETS, n + ".json"), "utf8"));
const APNG = (n) => path.resolve(ASSETS, n + ".png");
const PX = 1 / 72; // 960x540 frame px -> inches (1px = 1pt)

// ---- measured palette -------------------------------------------------------
const C = {
  titleBlue: "1000A6", titleRed: "971629",
  boxFill: "FBFDE5", boxBorder: "A9A5C2", rightFill: "FFFFFF", rightBorder: "AAA4D1",
  modelRed: "B9111F", modelUnderline: "DE7B77", labelBlack: "1A1A1A",
  bannerBlue: "0000CC",
  eqBlue: "2108AA", eqRed: "C93B47", eqGreen: "559B44", navy: "000080",
  ipRed: "C22433", xRed: "BE2E40", wBlue: "3E32B2", outY: "4D4F4C", inputRed: "A61122",
};

function drawBox(pptx, slide, x, y, w, h, fill, border) {
  slide.addShape(pptx.ShapeType.rect, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    fill: { color: fill }, line: { color: border, width: 1 },
  });
}

// text run helper (left-aligned, vertically centered on measured band center)
function txt(pptx, slide, xPx, cyPx, opts = {}) {
  slide.addText(opts.runs || "", {
    x: xPx * PX, y: (cyPx / 72) - 0.3, w: (opts.wPx || 220) * PX, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontSize: opts.size || 17, bold: !!opts.bold, italic: !!opts.italic,
    color: opts.color || C.labelBlack, fontFace: opts.fontFace || "Arial",
  });
}

// image placement helpers
function imgTop(pptx, slide, name, xPx, topPx) {
  const m = MAN(name);
  slide.addImage({ path: APNG(name), x: xPx * PX, y: topPx * PX, w: m.w_in, h: m.h_in });
}
function imgBase(pptx, slide, name, xPx, basePx) {
  const m = MAN(name);
  slide.addImage({ path: APNG(name), x: xPx * PX, y: (basePx - m.baseline_frac * m.h_frame_px) * PX, w: m.w_in, h: m.h_in });
}

// ---- title ------------------------------------------------------------------
function drawTitle(pptx, slide) {
  // ink x156..752 center 454, band y68..90 center 79
  slide.addText([
    { text: "Same Equation", options: { color: C.titleBlue, underline: { style: "sng" } } },
    { text: " for Linear Regression and Classification", options: { color: C.titleRed } },
  ], {
    x: (454 - 419) * PX, y: (76.6 / 72) - 0.3, w: 838 * PX, h: 0.6,
    align: "center", valign: "middle", margin: 0,
    fontSize: 22.5, bold: true, fontFace: "Arial",
  });
}

// ---- model box --------------------------------------------------------------
function drawModelBox(pptx, slide) {
  drawBox(pptx, slide, 72, 105, 217, 78, C.boxFill, C.boxBorder);
  txt(pptx, slide, 77, 117.5, { runs: "Model", size: 19, bold: true, italic: true, color: C.modelRed });
  slide.addShape(pptx.ShapeType.line, { x: 77.5 * PX, y: 124.6 * PX, w: 50 * PX, h: 0, line: { color: C.modelUnderline, width: 1 } });
  txt(pptx, slide, 77, 141.5, { runs: "I/P:", size: 17, bold: true, color: C.labelBlack });
  txt(pptx, slide, 76, 170, { runs: "O/P:", size: 17, bold: true, color: C.labelBlack });
  imgBase(pptx, slide, "eq_014_ip", 126, 147.5);
  imgBase(pptx, slide, "eq_014_op", 128, 170);
}

// ---- regression section -----------------------------------------------------
function drawRegression(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 72 * PX, y: 194 * PX, w: 231 * PX, h: 25 * PX,
    fill: { color: C.bannerBlue },
  });
  slide.addText("General Case - Regression", {
    x: 72 * PX, y: 194 * PX, w: 231 * PX, h: 25 * PX,
    align: "center", valign: "middle", margin: 0,
    fontSize: 14, bold: true, color: "FFFFFF", fontFace: "Arial",
  });
  drawBox(pptx, slide, 72, 226, 411, 115, C.boxFill, C.boxBorder);
  txt(pptx, slide, 76, 238, { runs: "Model", size: 19, bold: true, italic: true, color: C.modelRed });
  slide.addShape(pptx.ShapeType.line, { x: 77 * PX, y: 245.8 * PX, w: 51 * PX, h: 0, line: { color: C.modelUnderline, width: 1 } });
  imgBase(pptx, slide, "eq_014_core", 76, 267.5);
  txt(pptx, slide, 77, 301, { runs: "Model Parameters :", size: 17, italic: true, color: C.eqBlue });
  imgBase(pptx, slide, "eq_014_params", 229, 308.5);
  txt(pptx, slide, 77, 329.5, { runs: [
    { text: "b", options: { bold: true, color: C.eqGreen } },
    { text: "     is called   ", options: { color: C.eqBlue } },
    { text: "\"bias\"", options: { color: C.eqBlue } },
    { text: "  term as it is independent of  ", options: { color: C.eqBlue } },
    { text: "x", options: { italic: true, color: C.eqRed } },
  ], size: 18, wPx: 460 });
}

// ---- classification section -------------------------------------------------
function drawClassification(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 69 * PX, y: 378 * PX, w: 231 * PX, h: 25 * PX,
    fill: { color: C.bannerBlue },
  });
  slide.addText("General Case - Classification", {
    x: 69 * PX, y: 378 * PX, w: 231 * PX, h: 25 * PX,
    align: "center", valign: "middle", margin: 0,
    fontSize: 14, bold: true, color: "FFFFFF", fontFace: "Arial",
  });
  drawBox(pptx, slide, 69, 411, 433, 113, C.boxFill, C.boxBorder);
  txt(pptx, slide, 74, 422.5, { runs: "Model", size: 19, bold: true, italic: true, color: C.modelRed });
  slide.addShape(pptx.ShapeType.line, { x: 75 * PX, y: 429.8 * PX, w: 49 * PX, h: 0, line: { color: C.modelUnderline, width: 1 } });
  imgBase(pptx, slide, "eq_014_core_b", 74, 452.5);  // byte-identical core copy: distinct rel id for the OMML wrapper (two pics share one media file otherwise)
  // decision rules (measured colors: y blue, conditions red, rest blue)
  txt(pptx, slide, 74, 469.5, { runs: [
    { text: "y", options: { italic: true, color: C.eqBlue } },
    { text: " > 0", options: { color: C.eqRed } },
  ] });
  imgTop(pptx, slide, "dR_arrow", 110, 468);
  txt(pptx, slide, 127, 469.5, { runs: "Class 1", color: C.eqBlue });
  txt(pptx, slide, 214, 469.5, { runs: [
    { text: "y", options: { italic: true, color: C.eqBlue } },
    { text: " < 0", options: { color: C.eqRed } },
  ] });
  imgTop(pptx, slide, "dR_arrow", 250, 468);
  txt(pptx, slide, 273, 469.5, { runs: "Class 2", color: C.eqBlue });
  txt(pptx, slide, 360, 469.5, { runs: [
    { text: "y", options: { italic: true, color: C.eqBlue } },
    { text: " = 0", options: { color: C.eqRed } },
  ] });
  imgTop(pptx, slide, "dR_arrow", 395, 468);
  txt(pptx, slide, 418, 469.5, { runs: "Undefined", color: C.eqBlue });
  txt(pptx, slide, 74, 509, { runs: "Model Parameters :", size: 17, italic: true, color: C.eqBlue });
  imgBase(pptx, slide, "eq_014_params", 226, 516.5);
}

// ---- vector diagram ---------------------------------------------------------
function drawDiagram(pptx, slide) {
  drawBox(pptx, slide, 517, 212, 369, 192, C.rightFill, C.rightBorder);
  txt(pptx, slide, 537, 309.5, { runs: "Input:", size: 18, color: C.inputRed });
  imgTop(pptx, slide, "dX_cap", 594, 303);
  imgTop(pptx, slide, "dX_eq", 610, 307);
  // measured red underline under X (rows ~319-320, x594..608) — vector notation, same as W
  slide.addShape(pptx.ShapeType.line, { x: 594 * PX, y: 319.5 * PX, w: 14 * PX, h: 0, line: { color: C.xRed, width: 1 } });
  imgTop(pptx, slide, "dW_cap", 693, 304);
  imgTop(pptx, slide, "dW_eq", 713, 308);
  // measured blue underline under W (rows 319-320, x693..710)
  slide.addShape(pptx.ShapeType.line, { x: 693 * PX, y: 319.5 * PX, w: 17 * PX, h: 0, line: { color: C.wBlue, width: 1 } });
  txt(pptx, slide, 781, 314, { runs: "Output:", size: 17, bold: true, color: C.labelBlack });
  // X column (red): tall parens + 6 rows (3 entries, two 3-dot rows, final)
  imgTop(pptx, slide, "dX_pl", 625, 239);
  imgTop(pptx, slide, "dX_x1", 631, 247);
  imgTop(pptx, slide, "dX_x2", 631, 273);
  imgTop(pptx, slide, "dX_x3", 631, 300);
  imgTop(pptx, slide, "dX_dots", 631, 333);
  imgTop(pptx, slide, "dX_dots", 631, 356);
  imgTop(pptx, slide, "dX_xd", 631, 372);
  imgTop(pptx, slide, "dX_pr", 650, 239);
  // W column (blue)
  imgTop(pptx, slide, "dW_pl", 727, 246);
  imgTop(pptx, slide, "dW_w1", 733, 252);
  imgTop(pptx, slide, "dW_w2", 733, 275);
  imgTop(pptx, slide, "dW_w3", 733, 299);
  imgTop(pptx, slide, "dW_dots", 733, 332);
  imgTop(pptx, slide, "dW_dots", 733, 352);
  imgTop(pptx, slide, "dW_wd", 733, 363);
  imgTop(pptx, slide, "dW_pr", 756, 246);
  // Output ( y ) in dark gray (measured — not red)
  imgTop(pptx, slide, "dO_pl", 846, 303);
  imgTop(pptx, slide, "dO_y", 853, 310);
  imgTop(pptx, slide, "dO_pr", 865, 303);
}

// ---- component export -------------------------------------------------------
function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 14 : opts.numeral;
  drawHouseChrome(pptx, slide, { numeral });
  drawTitle(pptx, slide);
  drawModelBox(pptx, slide);
  drawRegression(pptx, slide);
  drawClassification(pptx, slide);
  drawDiagram(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] || path.resolve(__dirname, "../slide_014_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase };
