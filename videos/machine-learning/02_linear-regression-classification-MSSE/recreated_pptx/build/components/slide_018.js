// slide_018.js — "Calculation of Model Parameter “W”" (ML lecture 02)
// Deck: machine-learning/02_linear-regression-classification-MSSE (39 slides)
// Worker: ml02-w018-a5, 2026-10-13. ROOT slide (no parents); PARENT of slide 19 —
// banked as build/components/slide_018.js after PASS (renderBase + per-block
// exports; house chrome drawn ONCE here via shared_patterns module).
//
// Ground truth: unique_slides/slide_018.jpg (960x540, 1px = 1pt = 1/72 in).
// PIL measurements: scratch/ml02/slide018/ (gen-4 passes 1-3 + a5 verify + loose
// passes). Frame-wins-over-spec facts: eq1's Y is DARK (46,48,46) not red; eq1's X
// has NO underline (only the right-box X and line-A X are underlined); the arrow
// fill is WHITE (254,253,251, 3 samples) not pink; line pitches are irregular
// (baselines 212.5 / 254.5 / 285.5).
//
// v2 closed-loop fixes vs v1 (selfcheck_v1_out.json):
//   - underlines: mathtext \underline rules hung 5-9px low -> tokens are BARE
//     glyphs; every rule is a 1pt line shape at the measured row/extent.
//   - tokens split (X | subscript, Y | subscript, X | superscript) so both the
//     big raised X (baseline 168.5/210.5/224.5 vs 169.5/210.5?/227.5) and the
//     subscript extents match the original.
//   - title font: Arial bold 22 was 15% narrow on the focal blue “W” (39.3 vs
//     45.5px; probe render). Verdana bold 20 nails “W” (45.2) and cap 15.3~16;
//     red run gets charSpacing -0.65pt to hit the measured 331.5px width.
//   - TNR text runs: LO tracks wider than the original -> per-run charSpacing
//     (-0.4..-2.0pt) pins every run's measured ink width; boxes positioned by
//     measured ink-left minus v1's observed left side bearing.
// Equations: matplotlib mathtext (STIX serif) -> 600dpi transparent PNG ->
// addImage at EXACT size, baseline-law placement (assets/eq_s018_manifest.json).
// House chrome: shared_patterns/house_chrome.js, numeral 18.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require(path.join(
  __dirname, "..", "..", "shared_patterns", "house_chrome.js"
));

const px = (v) => v / 72; // frame px -> inches

const EQ = JSON.parse(
  fs.readFileSync(path.join(__dirname, "assets", "eq_s018_manifest.json"), "utf8")
);

// Place one equation-token PNG: baseline law (kind from manifest) at measured x0.
function addEqRun(slide, name, opts) {
  const m = EQ[name];
  const xIn = px(opts.x0) - m.pad_in;
  const yIn = px(opts.baseline) - m.baseline_frac * m.h_in;
  slide.addImage({
    path: path.join(__dirname, "assets", m.image),
    x: xIn, y: yIn, w: m.w_in, h: m.h_in,
  });
}

// Place a center-anchored token (the ⇒ arrows: vertically symmetric glyphs).
function addEqCenter(slide, name, opts) {
  const m = EQ[name];
  slide.addImage({
    path: path.join(__dirname, "assets", m.image),
    x: px(opts.x0) - m.pad_in,
    y: px(opts.cy) - m.h_in / 2,
    w: m.w_in, h: m.h_in,
  });
}

// A 1pt rule at the measured row/extent (underlines drawn as shapes, not mathtext).
function addRule(pptx, slide, x0, x1, row, color) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x0), y: px(row), w: px(x1 - x0), h: 0,
    line: { color, width: 1 },
  });
}

// A TNR text run placed by measured ink-left x and baseline y (+ per-run tracking).
function addTextRun(slide, text, opts) {
  slide.addText(text, {
    x: px(opts.boxX),
    y: px(opts.baseline - 22),
    w: px(opts.w || 300),
    h: px(34),
    align: "left", valign: "top",
    fontFace: "Times New Roman", fontSize: 24,
    italic: !!opts.italic, bold: !!opts.bold,
    charSpacing: opts.charSpacing || 0,
    color: opts.color || "000000", margin: 0,
  });
}

// ---- per-block draws (component exports; slide 19 composes from these) ----

function drawTitle(pptx, slide, opts = {}) {
  slide.addText([
    { text: "Calculation of Model Parameter ", options: { color: "C00000", charSpacing: -0.65 } },
    { text: "“W”", options: { color: "0000FF" } },
  ], {
    x: px(466) - 4.5, y: px(79.6) - 0.4,
    w: 9.0, h: 0.8,
    align: "center", valign: "middle", bold: true,
    fontFace: "Verdana", fontSize: opts.size || 20, margin: 0,
  });
}

function drawLeftBox(pptx, slide) {
  // white rect, C00000 1pt border (stroke centers x95.5..571, y120..312)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(95.5), y: px(120), w: px(475.5), h: px(192.5),
    fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
  });
  // eq1: Y = X W  (Y dark + rule, = dark, X blue RAISED no rule, W red + rule)
  addEqRun(slide, "eq1_Y", { x0: 108, baseline: 169.5 });
  addRule(pptx, slide, 108, 126.5, 172, "000000");
  addEqCenter(slide, "eq1_eq", { x0: 132, cy: 160.25 }); // v1: baseline law sat 1.8px low
  addEqRun(slide, "eq1_X", { x0: 157, baseline: 168.5 });
  addEqRun(slide, "eq1_W", { x0: 187, baseline: 169.5 });
  addRule(pptx, slide, 186.5, 211, 172, "C00000");
  // Where:
  addTextRun(slide, "Where:", { boxX: 106.1, baseline: 212.5, italic: true, charSpacing: 0.3, w: 100 });
  // line A (baseline 212.5; X raised to 210.5, subscript baseline 220.5)
  addEqRun(slide, "A_Xg", { x0: 175.5, baseline: 210.5 });
  addRule(pptx, slide, 175.5, 197, 211.5, "0000FF");
  addEqRun(slide, "A_sub", { x0: 200, baseline: 220.5 });
  addTextRun(slide, "is a matrix", { boxX: 281.2, baseline: 212.5, charSpacing: -0.4 });
  addEqCenter(slide, "A_arrow", { x0: 416, cy: 203 });
  addTextRun(slide, "Given", { boxX: 467.5, baseline: 212.5, bold: true, charSpacing: -2.0 });
  // line B (baseline 254.5; Y baseline 255, subscript baseline 261.5)
  addEqRun(slide, "B_Yg", { x0: 177, baseline: 255 });
  addRule(pptx, slide, 177, 195.5, 256.5, "C00000");
  addEqRun(slide, "B_sub", { x0: 200.5, baseline: 261.5 });
  addTextRun(slide, "is labels vector", { boxX: 237.4, baseline: 254.5, charSpacing: -0.8 });
  addEqCenter(slide, "B_arrow", { x0: 413, cy: 245 });
  addTextRun(slide, "Given", { boxX: 463.3, baseline: 254.5, bold: true, charSpacing: -2.0 });
  // line C (baseline 285.5; W is SMALL here — measured cap 13px, no rule)
  addEqRun(slide, "C_W", { x0: 176.5, baseline: 284.5 });
  addTextRun(slide, "is Model Parameter", { boxX: 210.3, baseline: 285.5, charSpacing: -1.4 });
  addEqCenter(slide, "C_arrow", { x0: 412, cy: 276 });
  addTextRun(slide, "Required", { boxX: 463.8, baseline: 285.5, bold: true, charSpacing: -1.6 });
}

function drawArrow(pptx, slide) {
  // block arrow, white fill, C00000 1pt (custGeom, absolute inch points)
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,
    fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
    // NOTE: in pptxgenjs a point with close:true emits <a:close/> INSTEAD of its
    // lnTo (measured: the v2 tail collapsed to a diagonal). So the last real
    // vertex is a plain lnTo and a repeat of the start point carries the close.
    points: [
      { x: px(575), y: px(209.5), moveTo: true },  // tail top-left
      { x: px(610), y: px(209.5) },                // tail top at head base
      { x: px(610), y: px(204.5) },                // up the head base
      { x: px(622), y: px(216.75) },               // tip
      { x: px(610), y: px(229) },                  // head base bottom
      { x: px(610), y: px(223.5) },                // tail bottom at head base
      { x: px(575), y: px(223.5) },                // tail bottom-left (plain lnTo!)
      { x: px(575), y: px(209.5), close: true },   // close back to start
    ],
  });
}

function drawRightBox(pptx, slide) {
  // white rect, C00000 1pt border (stroke centers x630.5..874, y188..244)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(630.5), y: px(188), w: px(243.5), h: px(56.5),
    fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
  });
  // W = X^-1 Y  (W dark + rule, = dark, X blue + rule with -1 sup, Y red + rule)
  addEqRun(slide, "rb_W", { x0: 648, baseline: 227.5 });
  addRule(pptx, slide, 648, 673.5, 229, "000000");
  addEqCenter(slide, "rb_eq", { x0: 679, cy: 217.75 }); // v1: baseline law sat 2.6px low
  addEqRun(slide, "rb_Xg", { x0: 704, baseline: 224.5 });
  addRule(pptx, slide, 704, 723, 226, "0000FF");
  addEqRun(slide, "rb_sup", { x0: 733, baseline: 208 });
  addEqRun(slide, "rb_Y", { x0: 761, baseline: 227.5 });
  addRule(pptx, slide, 761.5, 778, 229, "C00000");
  // smiley face d~37 at (821.5,198): yellow F2DD49 face, black eyes/smile
  slide.addShape(pptx.ShapeType.smileyFace, {
    x: px(821.5), y: px(198), w: px(37), h: px(37),
    fill: { color: "F2DD49" }, line: { color: "000000", width: 1 },
  });
}

// renderBase: full certified composition. Children (slide 19) import this and pass
// { numeral: <their printed number> }; house chrome is drawn ONCE here.
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 18 : opts.numeral });
  drawTitle(pptx, slide, opts);
  drawLeftBox(pptx, slide);
  drawArrow(pptx, slide);
  drawRightBox(pptx, slide);
}

// ---- build ----------------------------------------------------------------
function build(outPath) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
  pres.author = "slide-recreation";
  pres.title = "Calculation of Model Parameter “W”";
  const slide = pres.addSlide();
  renderBase(pres, slide);
  return pres.writeFile({ fileName: outPath }).then(() => console.log("WROTE", outPath));
}

if (require.main === module) {
  const out =
    process.argv[2] ||
    path.resolve(__dirname, "..", "slide_018_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawTitle, drawLeftBox, drawArrow, drawRightBox, addEqRun, addEqCenter, addRule, addTextRun };
