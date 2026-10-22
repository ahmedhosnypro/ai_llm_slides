// slide_019.js — "Calculation of Model Parameter “W”" variant 2 (ML lecture 02)
// Deck: machine-learning/02_linear-regression-classification-MSSE (39 slides)
// Worker: ml02-w019-a1, 2026-10-13. CHILD of slide 18 (founder graph 19 > 18).
//
// COMPOSITION (dependency law, .agents/skills/slide-recreation/references/dependencies.md):
//   - Parent's CERTIFIED component imported by ABSOLUTE path:
//       /home/ahmed/Projects/ai_llm_slides/videos/machine-learning/
//         02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_018.js
//     renderBase(pptx, slide, { numeral: 19 }) draws house chrome (badge 19,
//     drawn ONCE here), title, left box, arrow, right box — the parent's
//     certified blocks, NEVER re-derived.
//   - THIS slide's ONLY delta: the lower equation box (PIL-measured on MY frame
//     slide_019.jpg, 960x540, 1px = 1pt = 1/72 in; measurements banked in
//     scratch/ml02/slide019/). Frame-diff vs slide_018.jpg: upper content is
//     pixel-identical except the badge numeral (18->19) and ~123 stray JPEG
//     pixels inside the two emoji (original-vs-original antialiasing noise) —
//     every inherited block verified against MY frame's pixels before composing.
//   - Parent mechanisms REUSED (not re-learned): mathtext -> 600dpi transparent
//     PNG -> addImage at exact size with baseline-law placement (manifest
//     assets/eq_s019_manifest.json); underlines as 1pt line shapes at measured
//     rows (parent finding: mathtext \underline hangs low); TNR text runs placed
//     by measured ink-left + baseline with per-run charSpacing; custGeom close
//     collapse irrelevant here (no custom arrows in the delta).
//
// Lower box measured geometry (frame px): red C00000 1pt border, white fill,
// stroke centers x95.5..x471.5, y328..y496 -> rect(95.5, 328, 376, 168).
//   Eq line (baselines 382, sub 391, sup 364):
//     W 000000 ink(102..129, 362..382) + black rule x101.5..129.5 row 385
//     = 000000 ink(133..151, 368..378) cy 373
//     ( 0000FF ink(156..164 core, 350..391) cy 370.75
//     X 0000FF ink(170..196, 357..382) baseline 382
//     N×d 0000FF ink(196..227, 379..391) baseline 391 [resume-corrected:
//     gen-1 header said 201..228; direct PIL measure of the frame: N 196-207,
//     × 210-217, d 219-227]
//     ) 0000FF ink(231..241 core, 350..391) cy 370.5
//     −1 0000FF ink(241..266, 348..364) baseline 364
//     Y C00000 ink(272..290, 360..383) + red rule x271.5..290.5 row 385
//   Line 2 (X baseline 436.5, sub baseline 444): X BOLD UPRIGHT serif TNR text
//     ink(104.5..124, 416..436.5) [frame wins over spec: upright, not italic],
//     sub N×d bold ITALIC with wide letter gaps — three tokens at measured x
//     (N 127-136, × 140-147, d 160-169, y433-444) [frame wins over spec: DARK],
//     "is non-square matrix" 0000FF TNR ink-left 178, ink w 174, charSpacing -0.5.
//   Line 3 (baseline 466): "There is NO Inverse" C00000 TNR bold italic,
//     ink-left 111, ink w 172, cap 14px -> 21pt.
//   Sad face: yellow F2DD49 circle d~57 center(418,444) (no outline — original
//     emoji has no ring), two 000000 eye dots d5.5 at (405,435)/(425.5,435),
//     frown = top-half arc, circle bbox (405,446,26,26), 2pt 000000.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

// PARENT component — certified, imported, never edited (cascade law).
const P18 = require("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_018.js");
const { addRule } = P18; // generic measured-row rule primitive from the parent

const EQ = JSON.parse(
  fs.readFileSync(path.join(__dirname, "assets", "eq_s019_manifest.json"), "utf8")
);

const px = (v) => v / 72; // frame px -> inches

// Place one equation-token PNG by ink-left x0 + baseline (parent's baseline law).
function addEq19(slide, name, opts) {
  const m = EQ[name];
  slide.addImage({
    path: path.join(__dirname, "assets", m.image),
    x: px(opts.x0) - m.pad_in,
    y: px(opts.baseline) - m.baseline_frac * m.h_in,
    w: m.w_in, h: m.h_in,
  });
}

// Place a center-anchored token (=, parens: vertically symmetric in the original).
function addEqCenter19(slide, name, opts) {
  const m = EQ[name];
  slide.addImage({
    path: path.join(__dirname, "assets", m.image),
    x: px(opts.x0) - m.pad_in,
    y: px(opts.cy) - m.h_in / 2,
    w: m.w_in, h: m.h_in,
  });
}

// TNR text run placed by measured ink-left + baseline, size-parametrized.
// Offset derived from the parent's calibrated 24pt helper (boxTop = baseline -
// (0.891*fs + 0.6)): TNR ascent ~0.891em, same valign/margin conventions.
function addRun19(slide, text, opts) {
  const fsz = opts.fontSize || 24;
  slide.addText(text, {
    x: px(opts.boxX),
    y: px(opts.baseline - (0.891 * fsz + 0.6)),
    w: px(opts.w || 300),
    h: px(34),
    align: "left", valign: "top",
    fontFace: "Times New Roman", fontSize: fsz,
    italic: !!opts.italic, bold: !!opts.bold,
    charSpacing: opts.charSpacing || 0,
    color: opts.color || "000000", margin: 0,
  });
}

// ---- THIS slide's delta: the lower equation box -----------------------------

function drawLowerBox(pptx, slide) {
  // white rect, C00000 1pt border (stroke centers x95.5..471.5, y328..496)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(95.5), y: px(328), w: px(376), h: px(168),
    fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
  });
  // eq: W = ( X_{N×d} )^{-1} Y
  addEq19(slide, "lb19_W", { x0: 102, baseline: 382 });
  addRule(pptx, slide, 101.5, 129.5, 385, "000000");
  addEqCenter19(slide, "lb19_eq", { x0: 133, cy: 373 });
  addEqCenter19(slide, "lb19_po", { x0: 156.5, cy: 370.75 });
  addEq19(slide, "lb19_X", { x0: 170, baseline: 382 });
  addEq19(slide, "lb19_sub", { x0: 196.5, baseline: 391 }); // RESUME FIX: orig N×d ink 196-227 (was x0=201, ink landed 200.5 = +4.5px out of tolerance)
  addEqCenter19(slide, "lb19_pc", { x0: 230, cy: 370.5 });
  addEq19(slide, "lb19_sup", { x0: 241, baseline: 364 });
  addEq19(slide, "lb19_Y", { x0: 272, baseline: 382 });
  addRule(pptx, slide, 271.5, 290.5, 385, "C00000");
  // line 2: X_{N×d} is non-square matrix — X is BOLD UPRIGHT serif (TNR text,
  // not italic), sub N×d is bold italic with wide letter gaps (three tokens at
  // measured x: N 127-136, × 140-147, d 151-157, baseline 444). RESUME FIX
  // (ml02-w019-a2, 2026-10-14): gen-1's closed-loop selfcheck caught d rendered
  // at 159.8-167.9 vs orig 150-158 -> x0 160->151; "is non-square matrix" was
  // 182.3px wide vs orig 172 -> charSpacing -0.5 -> -1.2 (calibrated on the
  // banked probe_spc render: 406px @0, 386 @-0.5, 347 @-1.5, 287 @-3 @150dpi,
  // linear fit -> -1.2 hits 358.5px = 172 frame px); boxX 177.2->178.7 to put
  // ink-left at 179 per orig.
  addRun19(slide, "X", { boxX: 103.3, baseline: 436.5, bold: true, fontSize: 32, w: 60 });
  addEq19(slide, "lb2s_N", { x0: 127, baseline: 444 });
  addEq19(slide, "lb2s_x", { x0: 140, baseline: 444 });
  addEq19(slide, "lb2s_d", { x0: 151, baseline: 444 });
  addRun19(slide, "is non-square matrix", {
    boxX: 178.7, baseline: 437, color: "0000FF", charSpacing: -1.2, w: 220,
  });
  // line 3: There is NO Inverse (red bold italic)
  addRun19(slide, "There is NO Inverse", {
    boxX: 106.5, baseline: 466, color: "C00000", italic: true, bold: true,
    fontSize: 21, charSpacing: 0, w: 230,
  });
  // sad face: yellow circle, two eyes, frown arc (no ring — original is ringless)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(389.5), y: px(415.5), w: px(57), h: px(57),
    fill: { color: "F2DD49" },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(405), y: px(435), w: px(5.5), h: px(5.5), fill: { color: "000000" },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(425.5), y: px(435), w: px(5.5), h: px(5.5), fill: { color: "000000" },
  });
  slide.addShape(pptx.ShapeType.arc, {
    x: px(405), y: px(446), w: px(26), h: px(26),
    line: { color: "000000", width: 2 }, angleRange: [180, 360],
  });
}

// renderBase19: parent's certified composition + this slide's delta.
function renderBase19(pptx, slide, opts = {}) {
  P18.renderBase(pptx, slide, { numeral: opts.numeral === undefined ? 19 : opts.numeral });
  drawLowerBox(pptx, slide);
}

// ---- build ----------------------------------------------------------------
function build(outPath) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
  pres.author = "slide-recreation";
  pres.title = "Calculation of Model Parameter “W”";
  const slide = pres.addSlide();
  renderBase19(pres, slide);
  return pres.writeFile({ fileName: outPath }).then(() => console.log("WROTE", outPath));
}

if (require.main === module) {
  const out =
    process.argv[2] ||
    path.resolve(__dirname, "..", "slide_019_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase19, drawLowerBox, addEq19, addEqCenter19, addRun19 };
