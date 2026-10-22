// slide_026.js — "Minimization of Loss function to obtain BEST model parameters" (2nd page)
// ML lecture 02 (machine-learning/02_linear-regression-classification-MSSE), CHILD of slide 25.
// Worker ml02-w026-g3, 2026-10-13. Dependency law: requires the certified parent
// component by ABSOLUTE path, renders it verbatim (numeral 26), then draws ONLY the
// measured delta. Parent composition verified pixel-identical to this frame's top
// region (badge rows 59..88 identical; delta band y355..522 x72..893 = this file).
//
// Delta ground truth: PIL-measured from unique_slides/slide_026.jpg (960x540, 1px=1pt).
// Banked measurements: scratch/ml02/slide026/measure_*.txt. Equations: matplotlib
// mathtext (STIX) -> 600dpi transparent PNGs, each run width-matched (LANCZOS@600dpi)
// to the original's measured ink span; manifest assets/eq026_manifest.json.
//
// Measured facts baked in (px, 1px=1pt):
//   box2 (2nd pale-yellow box) x72..892 y356..522 fill FBFDE5 border ~C2C5C1
//   eq4 line baseline 403.5: head runs dLoss/dW x96, = x164, 0 x183, = x203, 1/2 x223
//     (identical anchors to eq5 -> same PNGs reused); body [ (X W)^T (X) + (X)^T (X W)
//     - 2 (X)^T Y ] ink x239..593, NO underlines
//   eq5 line baseline 487.5: same head runs; body [ 2 X^T X W - 2 X^T Y ] x239..422,
//     NO underlines
//   eq6 "(X^T X) W = X^T Y" baseline 488.5 ink x477..638; underlines y490.2 W 542..560,
//     Y 625..638 (snapped to my rendered glyphs: 542.2..560.3, 626.8..638.9)
//   remember box 2 x655..873 y371..422.5 fill DAECFA border ~9BAFB9 (parent nominal);
//     'Remember' hdr ink x661..735 rows 375..387 (red 971629 italic serif 18pt)
//     remeq "X^T (X W) = (X W)^T X" ink x658..867 baseline 415; underlines y416.2
//     X1 660..673, W1 717..734, W2 813..831, X4 854..867 (X inside parens NOT
//     underlined) -> snapped: X1 658.0..673.6, W1 720.3..738.2, W2 811.6..829.5,
//     X4 852.3..867.9
//   green box x690..878 y465..497 fill CEFCE2 border 40943C (frame-measured; the
//     spec's E2EFDA/00B050 are wrong for this frame); eq "W = (X^T X)^-1 X^T Y"
//     ink x695..873 baseline 488.5; underlines y490.2 W 695..713, Y 860..873
//     -> snapped: 695.1..713.0, 861.9..873.8
//   2 white-fill block arrows (custGeom, certified slide_016 mechanism), outline
//     F4B6C2 1pt (frame-measured core; slide_016's certified FFCCC C family):
//     arrow1 body x429..455 y476..488 head to tip (461,481.5);
//     arrow2 body x646..672 y476..488 head to tip (678,481.5)

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

// Dependency law: parent's certified composition, imported (never copy-pasted).
const PARENT = require("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_025.js");

const MANIFEST = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq026_manifest.json"), "utf8"));
const ASSET = (n) => path.resolve(__dirname, "assets", n);
const PX = 1 / 72; // 960x540 frame px -> inches (1px = 1pt)
const SERIF = "Times New Roman";

// ---- measured palette (delta) -----------------------------------------------
const C = {
  ink: "1F1F1F",
  boxFill: "FBFDE5", boxBorder: "C2C5C1",
  remFill: "DAECFA", remBorder: "9BAFB9",
  greenFill: "CEFCE2", greenBorder: "40943C",
  headerRed: "971629",
  arrowOutline: "F4B6C2",
};

// ---- delta helpers (certified mechanisms, my assets) ------------------------
function drawEq(slide, name, anchorXpx, baselineYpx) {
  const a = MANIFEST[name];
  const inkDxIn = a.ink_dx / 600;
  slide.addImage({
    path: ASSET(a.png),
    x: anchorXpx * PX - inkDxIn,
    y: baselineYpx * PX - a.baseline_frac * a.h_in,
    w: a.w_in, h: a.h_in,
  });
}

function drawUnderline(pptx, slide, x0px, x1px, yPx, color) {
  slide.addShape(pptx.ShapeType.line, {
    x: x0px * PX, y: yPx * PX, w: (x1px - x0px) * PX, h: 0,
    line: { color: color, width: 1 },
  });
}

function line(pptx, slide, runs, xPx, baselineYpx, opts = {}) {
  const fs_ = opts.size || 18;
  const asc = (opts.serif === false ? 0.905 : 0.891) * fs_;
  const desc = (opts.serif === false ? 0.212 : 0.216) * fs_;
  const cy = baselineYpx - (asc - desc) / 2;
  slide.addText(runs, {
    x: xPx * PX, y: cy * PX - 0.3, w: (opts.wPx || 220) * PX, h: 0.6,
    align: opts.align || "left", valign: "middle", margin: 0,
    fontFace: opts.serif === false ? "Arial" : SERIF, fontSize: fs_,
    charSpacing: opts.charSpacing,
  });
}

// hollow block-right arrow as a full-slide custGeom (certified slide_016 mechanism)
function blockArrow(pptx, slide, pts) {
  const p = pts.map(([x, y]) => ({ x: x / 72, y: y / 72 }));
  p[0].moveTo = true;
  p.push({ x: pts[0][0] / 72, y: pts[0][1] / 72, close: true });
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,
    fill: { color: "FFFFFF" }, line: { color: C.arrowOutline, width: 1 },
    points: p,
  });
}

// ---- the delta ---------------------------------------------------------------
function drawDelta(pptx, slide) {
  // box2 (second pale-yellow derivation box)
  slide.addShape(pptx.ShapeType.rect, {
    x: 72 * PX, y: 356 * PX, w: 820 * PX, h: 166 * PX,
    fill: { color: C.boxFill }, line: { color: C.boxBorder, width: 1 },
  });

  // eq4 line — derivative chain, baseline 403.5 (head anchors shared with eq5)
  drawEq(slide, "eq026_h1", 96, 403.5);
  drawEq(slide, "eq026_eq", 164, 403.5);
  drawEq(slide, "eq026_z", 183, 403.5);
  drawEq(slide, "eq026_eq2", 203, 403.5);
  drawEq(slide, "eq026_half", 223, 403.5);
  drawEq(slide, "eq026_b4", 239, 403.5);

  // eq5 line — simplified derivative, baseline 487.5
  drawEq(slide, "eq026_h1", 96, 487.5);
  drawEq(slide, "eq026_eq", 164, 487.5);
  drawEq(slide, "eq026_z", 183, 487.5);
  drawEq(slide, "eq026_eq2", 203, 487.5);
  drawEq(slide, "eq026_half", 223, 487.5);
  drawEq(slide, "eq026_b5", 239, 487.5);

  // eq6 — normal-equation form, baseline 488.5, underlines under W and Y
  drawEq(slide, "eq026_e6", 477, 488.5);
  drawUnderline(pptx, slide, 542.2, 560.3, 490.2, C.ink);
  drawUnderline(pptx, slide, 626.8, 638.9, 490.2, C.ink);

  // remember box 2 (top-right inside box2)
  slide.addShape(pptx.ShapeType.rect, {
    x: 655 * PX, y: 371 * PX, w: 218 * PX, h: 51.5 * PX,
    fill: { color: C.remFill }, line: { color: C.remBorder, width: 1 },
  });
  line(pptx, slide, [
    { text: "Remember", options: { color: C.headerRed, italic: true } },
  ], 658, 388, { size: 18, wPx: 130 });
  // transpose identity; underline X1/W1/W2/X4 (X inside parens NOT underlined)
  drawEq(slide, "eq026_r2", 658, 415);
  drawUnderline(pptx, slide, 658.0, 673.6, 416.2, C.ink);
  drawUnderline(pptx, slide, 720.3, 738.2, 416.2, C.ink);
  drawUnderline(pptx, slide, 811.6, 829.5, 416.2, C.ink);
  drawUnderline(pptx, slide, 852.3, 867.9, 416.2, C.ink);

  // green final box
  slide.addShape(pptx.ShapeType.rect, {
    x: 690 * PX, y: 465 * PX, w: 188 * PX, h: 32 * PX,
    fill: { color: C.greenFill }, line: { color: C.greenBorder, width: 1 },
  });
  drawEq(slide, "eq026_g1", 695, 488.5);
  drawUnderline(pptx, slide, 695.1, 713.0, 490.2, C.ink);
  drawUnderline(pptx, slide, 861.9, 873.8, 490.2, C.ink);

  // 2 white block arrows (on the eq5 row, pointing at eq6 and the green box)
  blockArrow(pptx, slide, [[429, 476], [455, 476], [455, 470], [461, 481.5], [455, 493], [455, 488], [429, 488]]);
  blockArrow(pptx, slide, [[646, 476], [672, 476], [672, 470], [678, 481.5], [672, 493], [672, 488], [646, 488]]);
}

function renderBase(pptx, slide) {
  PARENT.renderBase(pptx, slide, { numeral: 26 });
  drawDelta(pptx, slide);
}

if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const slide = pres.addSlide();
  renderBase(pres, slide);
  const out = path.resolve(__dirname, "..", "slide_026_recreated.pptx");
  pres.writeFile({ fileName: out })
    .then(() => console.log("WROTE", out))
    .catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawDelta };
