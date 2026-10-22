// slide_021.js — "Concept of LOSS Function" (ML lecture 02, root slide, no children)
//
// Ground truth: PIL-measured from unique_slides/slide_021.jpg (960x540, 1px = 1pt).
// All frame-px geometry below is from the banked measurement pass
// (scratch/ml02/slide021/{measure_*.py,precise2.py,inkmap*.out,bracket_*.out}).
//
// Equation assets (600 dpi transparent PNGs + sidecars, matplotlib STIX mathtext;
// column vectors PIL-composed from mathtext entries + measured bracket strokes):
//   build/assets/vec_Y.png        frame rect (165,110) 60x106
//   build/assets/vec_Yhat.png     frame rect (541,113) 58x109
//   build/assets/eq_loss_head.png "Loss" red  ink (103,474) 38x14, baseline 487
//   build/assets/eq_loss_body.png black      ink (145,467) 257x27, baseline 488
//   build/assets/eq_remember.png  blue       ink (790,398) 84x21, baseline 416
// Embed law: w = px/600 in exact, y = baseline_in - baseline_frac*h_in.
//
// Identity statements ("Let Y =", "Ŷ = X W", "Ŷ=Y", "Ŷ≠Y", "Ŷ and Y") are typed
// text with precomposed Ŷ (U+0176) + native underline runs — these carry no
// stacked construct (the professional-2D mandate targets fractions/sums/stacked
// scripts), and typed text reproduces the original's own typed look exactly.
// Underlines in the original are segmented (under Y/Ŷ, not under = / ≠) —
// reproduced with per-run underline.
//
// Box alignment per measurement: Objective/If-Error/Remember centered,
// Define + Loss-formula left-anchored (original ink hugs the left).
//
// FOUNDER-DIRECTIVE-021 (2026-10-14, binding): "slide021 render 1 is better than
// render 2." Verified delta render_1 -> render_2 (attempt-1 PDF word bboxes +
// asset forensics): (1) vector assets v1 (straight rect bracket strokes, y_1-
// repeated entries) -> v2/v3 (curved/crescent parens, per-row y_1/y_2/y_n);
// (2) left caption 'from Training Samples' gained charSpacing 0.45; (3) IfError
// tail re-spaced (⇒ run lost a trailing NB; There/is/an/Error charSpacing
// trimmed). THIS build restores the render_1 composition: v1 vector assets
// regenerated via gen_assets.py, left caption without charSpacing, IfError word
// positions fitted to render_1's PDF-measured bboxes. render_2 stays banked
// (qa/slide021/build_attempt_2.js + assets_bank_v2v3/).

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const ASSETS = path.resolve(__dirname, "assets");
const PX = 72; // frame px -> inches divisor (960x540 frame, 1px = 1pt)

// ---- measured constants (frame px) ----------------------------------------
const GEO = {
  title: { inkX: 292, inkX1: 640, capTop: 71, baseline: 90 }, // center x 466
  ldef: { x: 80, y: 100, w: 353, h: 138 },
  rdef: { x: 457, y: 100, w: 354, h: 138 },
  obj: { x: 88, y: 244, w: 223, h: 57 },
  ie: { x: 88, y: 300, w: 409, h: 65 },
  def: { x: 88, y: 380, w: 576, h: 57 },
  lf: { x: 88, y: 456, w: 409, h: 57 },
  rem: { x: 778, y: 372, w: 97, h: 52 },
};
const RED = "C00000", BLUE = "0000CC", BLACK = "000000";
const FONT = "Times New Roman";

// ---- helpers ---------------------------------------------------------------
function sidecar(name) {
  return JSON.parse(fs.readFileSync(path.join(ASSETS, name.replace(/\.png$/, ".json")), "utf8"));
}
// Place an equation image: x at measured frame x0, baseline aligned by the
// sidecar's baseline_frac (EQUATION ALIGNMENT LAW). No rescaling ever.
function placeEq(slide, name, xFrame, baselineFrame) {
  const sc = sidecar(name);
  slide.addImage({
    path: path.join(ASSETS, name),
    x: xFrame / PX,
    y: baselineFrame / PX - sc.baseline_frac * sc.h_in,
    w: sc.w_in,
    h: sc.h_in,
  });
}
// Place a top-anchored image at its measured frame rect (vectors).
function placeImg(slide, name, xFrame, yFrame) {
  const sc = sidecar(name);
  slide.addImage({
    path: path.join(ASSETS, name),
    x: xFrame / PX, y: yFrame / PX, w: sc.w_in, h: sc.h_in,
  });
}
function box(pptx, slide, g, fill, lineColor, lineW) {
  slide.addShape(pptx.ShapeType.rect, {
    x: g.x / PX, y: g.y / PX, w: g.w / PX, h: g.h / PX,
    fill: { color: fill }, line: { color: lineColor, width: lineW },
  });
}
// Single-line text box, vertically centered on the measured ink-band center.
function line(slide, xFrame, centerFrame, wFrame, runs, opts = {}) {
  const h = opts.h || 30;
  const o = {
    x: xFrame / PX, y: (centerFrame - h / 2) / PX, w: wFrame / PX, h: h / PX,
    align: opts.align || "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: opts.size || 20, color: BLACK,
  };
  if (opts.charSpacing !== undefined) o.charSpacing = opts.charSpacing;
  slide.addText(runs, o);
}
const NB = "\u00A0";
const T = (text, o = {}) => ({ text, options: Object.assign({ color: BLACK }, o) });

// ---- per-block draws -------------------------------------------------------
function drawTitle(pptx, slide) {
  // ink x292..640 -> center 466; box = panel span shifted 14px left so a
  // centered render lands on the measured ink center.
  slide.addText([
    T("Concept of ", { color: RED }),
    T("LOSS", { color: BLUE }),
    T(" Function", { color: RED }),
  ], {
    x: 47 / PX, y: (80.5 - 54) / PX, w: 839 / PX, h: 1.5,
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 30, bold: true,
  });
}

function drawLeftDef(pptx, slide) {
  box(pptx, slide, GEO.ldef, "FFFFFF", RED, 2);
  // "Let Y =" ink x86..155, cap band y150..163
  line(slide, 84, 156.5, 100, [
    T("Let" + NB + NB), T("Y", { bold: true, underline: { style: "sng" } }), T(NB + NB + "="),
  ], { size: 20 });
  placeImg(slide, "vec_Y.png", 165, 110);
  // caption line 1 (red bold): ink x263..402, cap y141..154
  line(slide, 263, 147.5, 170, [T("Original Labels", { color: RED, bold: true })], { size: 21 });
  // caption line 2 (black): ink x228..420, cap y167..180
  line(slide, 228, 173.5, 220, [T("from Training Samples")], { size: 20 });
}

function drawRightDef(pptx, slide) {
  box(pptx, slide, GEO.rdef, "FFFFFF", RED, 2);
  // "Let Ŷ =" ink x464..532, band y142..171 (Ŷ hat raises the line)
  line(slide, 462, 162.5, 100, [
    T("Let" + NB + NB), T("Ŷ", { bold: true, underline: { style: "sng" } }), T(NB + NB + "="),
  ], { size: 20 });
  placeImg(slide, "vec_Yhat.png", 541, 113);
  // caption line 1 (blue bold): ink x633..782, cap y142..156
  line(slide, 633, 149, 180, [T("Predicted Labels", { color: BLUE, bold: true })], { size: 21 });
  // caption line 2: ink x609..795, band y172..191; Ŷ/X/W bold, X W underlined
  line(slide, 609, 181.5, 230, [
    T("from Model" + NB + NB), T("Ŷ", { bold: true, underline: { style: "sng" } }),
    T(NB + "=" + NB, { bold: true }),
    T("X", { bold: true, underline: { style: "sng" } }),
    T(NB + NB),
    T("W", { bold: true, underline: { style: "sng" } }),
  ], { size: 20 });
}

function drawObjective(pptx, slide) {
  box(pptx, slide, GEO.obj, "FFFFCC", BLUE, 2);
  // ink x116..277, cap y267..281 (Ŷ hat 262..264), underlines y283..284
  slide.addText([
    T("Objective is" + NB, { bold: true }),
    T("Ŷ", { bold: true, underline: { style: "sng" } }),
    T("=", { bold: true }),
    T("Y", { bold: true, underline: { style: "sng" } }),
  ], {
    x: 90 / PX, y: 246 / PX, w: 219 / PX, h: 53 / PX,
    align: "center", valign: "middle", margin: 0, fontFace: FONT, fontSize: 21, color: BLACK,
    charSpacing: 0.5,
  });
}

function drawIfError(pptx, slide) {
  box(pptx, slide, GEO.ie, "FFFFCC", BLUE, 2);
  // ink x112..466, band y322..345; ⇒ is RED in the frame (measured x218..238).
  // FOUNDER-DIRECTIVE-021 revert: word positions restored to RENDER_1 (measured
  // from the banked attempt-1 PDF, scratch/ml02/slide021/r1_words.html):
  // If..⇒ half identical to render_2; ⇒ run carries ONE extra trailing NB
  // (gap ⇒→There 14.2 vs 8.6) and the tail words carry wider charSpacing
  // (There/is/an 0.75, Error 0.72, (Loss) 0.5) — fitted from the r1 word bboxes.
  slide.addText([
    T("If" + NB + NB + NB, { bold: true }),
    T("Ŷ", { color: BLUE, bold: true, underline: { style: "sng" } }),
    T(NB + "≠", { color: BLUE, bold: true }),
    T(NB, {}),
    T("Y", { color: BLUE, bold: true, underline: { style: "sng" } }),
    T(NB + NB + NB + NB + NB + NB + "⇒" + NB + NB, { color: RED, bold: true, charSpacing: 0.6 }),
    T("There", { charSpacing: 0.75 }),
    T(NB + "is", { charSpacing: 0.75 }),
    T(NB + "an", { charSpacing: 0.75 }),
    T(NB + NB, {}),
    T("Error", { color: RED, bold: true, italic: true, charSpacing: 0.72 }),
    T(NB + NB + "(Loss)", { color: RED, bold: true, italic: true, charSpacing: 0.5 }),
  ], {
    x: 90 / PX, y: 302 / PX, w: 405 / PX, h: 61 / PX,
    align: "center", valign: "middle", margin: 0, fontFace: FONT, fontSize: 20, color: BLACK,
  });
}

function drawDefine(pptx, slide) {
  box(pptx, slide, GEO.def, "FCE4D6", RED, 2);
  // ink x93..647, cap y401..415 (Ŷ hat 387..391), underlines y417..419; left-anchored
  slide.addText([
    T("Define" + NB + NB + NB),
    T("Loss", { color: RED, bold: true }),
    T(NB + NB + NB + "function as" + NB + NB + NB),
    T("squared distance", { color: BLUE }),
    T(NB + NB + "between" + NB + NB + NB),
    T("Ŷ", { bold: true, underline: { style: "sng" } }),
    T(NB + NB + "and" + NB + NB),
    T("Y", { bold: true, underline: { style: "sng" } }),
  ], {
    x: 90 / PX, y: 382 / PX, w: 570 / PX, h: 53 / PX,
    align: "left", valign: "middle", margin: 0, fontFace: FONT, fontSize: 21, color: BLACK,
  });
}

function drawLossFormula(pptx, slide) {
  box(pptx, slide, GEO.lf, "FFFFCC", BLUE, 2);
  // "Loss" red bold italic ink (103,474) baseline 487; equation body black
  // ink (145,467) baseline 488 — mathtext PNGs, professional 2D (‖·‖₂, ᵀ, underlines)
  placeEq(slide, "eq_loss_head.png", 103, 487);
  placeEq(slide, "eq_loss_body.png", 145, 488);
}

function drawRemember(pptx, slide) {
  box(pptx, slide, GEO.rem, "D6EAF8", BLUE, 1);
  // line 1 ink x791..863, cap y377..387; line 2 = mathtext PNG ink (790,398) baseline 416
  line(slide, 780, 382, 97, [T("Remember", { color: RED, bold: true, italic: true })],
    { size: 17, align: "center" });
  placeEq(slide, "eq_remember.png", 790, 416);
}

// renderBase: full composition (playlist-scoped component contract)
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 21 : opts.numeral });
  drawTitle(pptx, slide);
  drawLeftDef(pptx, slide);
  drawRightDef(pptx, slide);
  drawObjective(pptx, slide);
  drawIfError(pptx, slide);
  drawDefine(pptx, slide);
  drawLossFormula(pptx, slide);
  drawRemember(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] ||
    path.resolve(__dirname, "../slide_021_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawTitle, GEO, RED, BLUE, BLACK, FONT };
