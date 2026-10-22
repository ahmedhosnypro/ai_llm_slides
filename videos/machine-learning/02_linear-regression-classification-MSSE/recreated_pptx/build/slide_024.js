// slide_024.js — machine-learning/02_linear-regression-classification-MSSE
// "Some Monotonically increase  Functions" — CHILD of slide 23 (founder graph 24 > 23).
//
// COMPOSITION (dependency law): the judge-certified parent component
//   videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_023.js
// is REQUIRED by absolute path and drawn via
//   P.renderBase(pptx, slide, { numeral: "24" })
// which draws the house chrome ONCE (shared_patterns/house_chrome.js, badge numeral 24)
// + title + all three graph panels. NOTHING here re-derives or re-draws the parent's
// geometry. This build draws ONLY slide 24's own delta at ITS measured geometry.
//
// DELTA VERIFICATION (PIL, slide_024.jpg vs slide_023.jpg, 960x540, 1px=1pt):
//   diff bands: badge numeral glyph (rows 70..81), JPEG noise in the panel band, and
//   rows 347..532. Every inherited block re-measured against THIS frame and confirmed
//   identical: title ink, panel boxes L136..333.5/C375..566.5/R610..884 y132..332,
//   left line path equal at x185..300 (±1px), amber markers equal, center y-axis
//   numerals/curve/labels equal, right curve/ticks/labels equal. The only panel-band
//   diff is slide_023's pen/cursor artifact next to the left label (rows 189..205
//   x289..305) — ABSENT in 24 and already omitted by the certified parent per judge
//   GROUND RULES (c). No skip/replace of parent blocks needed.
//   => delta = badge numeral (via renderBase opts) + the two text structures below.
//
// MEASURED DELTA (all from slide_024.jpg):
//   Cream explanation box: border stroke centers x80.5/x877.5, top y347.5, bottom y532
//     (ONE box y348..532: col-80 border continuous 348..532, rows 348 and 532
//     full-width). Fill (249,251,231) -> FAFCE6 (slide_016 precedent), border CC9999
//     1pt (measured core ~(203,175,168) = CC9999 smeared on cream; slide_016 family).
//     Four text lines, Times New Roman 22pt (cap height 15px = 0.662em), baselines
//     373.5 / 400.5 / 443.5 / 469.5, charSpacing -0.75pt (TNR renders ~8% wider than
//     the original font; -0.75pt/char pins word tails to the measured gaps):
//     L1 (upright)  "Apply monotonically increase function Φ on Loss function L(x) ⇒ Φ(L(x))"
//     L2  "when"(it) "L(x)" "is minimized"(it) ⇒ "Φ(L(x))" "is minimized"(upright)
//     L3  "Conclusion:"(RED BOLD UNDERLINED, underline row 445) "instead of using"(it)
//         "Loss"(BOLD) "function" "L(x)" "during training ,"(it; space-before-comma
//         verbatim) "one can use" "Φ(L(x))"
//     L4  "where" "Φ" "is any monotonically increase function"(it)
//   Nested peach box INSIDE the cream box: x100.5..816.5, y485..524 (the row-485 top
//     border spans ONLY x100..816; cream continues at x90/x830 — verified), fill
//     (246,231,212) -> FAE9D7 (slide_016 note-box precedent), border CC9999 0.75pt.
//     Line (TNR 22pt, baseline 510.7, charSpacing -0.75):
//     "We will use" + STACKED (1/2) + "L(x)" + "instead of"(it) + "L(x)" +
//     "during minimization" + "(to Simplify Math operations)"(BLUE)
//   MATH TOKENS (professional-format law; deck precedent slide_005/018 mathtext-PNG
//     runs): ALL math runs are mathtext PNGs (600dpi transparent, render_eq.py, HASHED
//     hex — unhashed "C00000" parses as matplotlib cycle-color C0, measured bug):
//       Φ   \Phi      F=21   #C00000  ink 14.3x15.5pt (5 instances, ink-left/cy:
//             (433,366) (727,366) (366.5,393) (779,435) (272,462))
//       L(x)   "L(x)"   F=21   #6A5ACD  ink 38.3x18.8pt (5 instances:
//             (609,366) (142,393) (462,435) (232,503.2) (378,503.2))
//       (L(x)) "(L(x))" F=22   #6A5ACD  ink 55.9x19.7pt (3 instances:
//             (745,366) (385,393) (798,435))
//       ⇒  \Rightarrow F=20.5 #000000 ink 15.1x8.8pt, center-anchored (684.5,367) (324,393)
//       ½  \frac{1}{2} F=26   #C00000  ink 11.5x31.8pt, center-anchored (222,504.5)
//         (original: numerator y489..501, bar 503..505, denominator 508..520)
//     Colors: black 000000; red C00000 (measured cores (157,2,9)/(164,8,26)); math
//     blue-violet 6A5ACD (2x2 fully-blue core mean (110,91,202) ≈ SlateBlue — the
//     family-ratified hue; thin-stroke JPEG deep-median (60,43,155) is smear-darkened).
//
// Run: NODE_PATH=$(npm root -g) node videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/slide_024.js
// House chrome check: shared_patterns/house_chrome_check.py on the 150dpi render.

const pptxgen = require("pptxgenjs");
const path = require("path");

// parent certified component — ABSOLUTE path, never copy-paste
const P = require("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_023.js");

const NUMERAL = "24";
const PX = (v) => v / 72; // frame px -> inches (1px = 1pt)
const ASSETS = path.resolve(__dirname, "assets");

// measured palette (this slide's delta only)
const COL = {
  black: "000000",
  red: "C00000",
  blue: "6A5ACD",
  creamFill: "FAFCE6",
  peachFill: "FAE9D7",
  boxBorder: "CC9999",
};
const FONT = "Times New Roman";
const FS = 22;   // cap 15px / 0.662
const CS = -0.75; // charSpacing pt: pin TNR's +8% width to the measured gaps

// mathtext assets (600dpi, 8px transparent pad; ink sizes verified from the PNGs)
const TOK = {
  frac:  { file: "slide024_frac.png",       inkW: 96,  inkH: 265 },
  arrow: { file: "slide024_rightarrow.png", inkW: 126, inkH: 73 },
  phi:   { file: "slide024_phi.png",        inkW: 119, inkH: 129 },
  lx:    { file: "slide024_lx.png",         inkW: 319, inkH: 157 },
  plx:   { file: "slide024_plx.png",        inkW: 466, inkH: 164 },
};

// ---- helpers ---------------------------------------------------------------
// One left-aligned text segment anchored at the MEASURED ink-left x, single line,
// box vertically centered so the BASELINE lands at baseline - 7.4px (TNR/Liberation
// 22pt: line 24.35px, ascent 19.6px -> baseline = box_cy + 7.4).
function seg(pptx, slide, text, xInkLeft, baseline, opts = {}) {
  const fs = opts.fontSize || FS;
  const cs = opts.charSpacing !== undefined ? opts.charSpacing : CS;
  // vertical: baseline = box_cy + (asc-desc)/2 = box_cy + 0.3375*fs (TNR metrics)
  const cy = baseline - 0.3375 * fs;
  const w = Math.min(500, 900 - xInkLeft);
  slide.addText(text, {
    x: PX(xInkLeft - 1.5), y: PX(cy - 15), w: PX(w), h: PX(30),
    align: "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: fs, color: opts.color || COL.black,
    charSpacing: cs,
    ...(opts.italic ? { italic: true } : {}),
    ...(opts.bold ? { bold: true } : {}),
    ...(opts.underline ? { underline: { style: "sng" } } : {}),
  });
}
// mathtext PNG token: ink-LEFT anchored at xInk, ink vertical CENTER at cy
// (PNGs carry an 8px transparent pad at 600dpi = 1 frame px on every side).
function tok(slide, t, xInk, cy) {
  const wIn = t.inkW / 600, hIn = t.inkH / 600;
  slide.addImage({
    path: path.join(ASSETS, t.file),
    x: PX(xInk) - 8 / 600,
    y: PX(cy) - hIn / 2 - 8 / 600,
    w: wIn, h: hIn,
  });
}

// ---- delta draws -------------------------------------------------------------
function drawExplanationBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: PX(80), y: PX(347.5), w: PX(877.5 - 80), h: PX(532 - 347.5),
    fill: { color: COL.creamFill }, line: { color: COL.boxBorder, width: 1 },
  });
}

function drawPeachBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: PX(100), y: PX(485), w: PX(816.5 - 100), h: PX(524 - 485),
    fill: { color: COL.peachFill }, line: { color: COL.boxBorder, width: 0.75 },
  });
}

function drawLine1(pptx, slide) {
  const B = 373.5;
  seg(pptx, slide, "Apply monotonically increase function", 93, B);
  tok(slide, TOK.phi, 433, 366);
  seg(pptx, slide, "on Loss function", 458, B);
  tok(slide, TOK.lx, 609, 366);
  tok(slide, TOK.arrow, 677, 367);
  tok(slide, TOK.phi, 727, 366);
  tok(slide, TOK.plx, 745, 366);
}

function drawLine2(pptx, slide) {
  const B = 400.5;
  seg(pptx, slide, "when", 93, B, { italic: true });
  tok(slide, TOK.lx, 142, 393);
  seg(pptx, slide, "is minimized", 185, B, { italic: true });
  tok(slide, TOK.arrow, 317, 393);
  tok(slide, TOK.phi, 366.5, 393);
  tok(slide, TOK.plx, 385, 393);
  seg(pptx, slide, "is minimized", 451, B);
}

function drawLine3(pptx, slide) {
  const B = 443.5;
  seg(pptx, slide, "Conclusion:", 93, B, { color: COL.red, bold: true, underline: true });
  seg(pptx, slide, "instead of using", 209, B, { italic: true });
  seg(pptx, slide, "Loss", 345, B, { bold: true });
  seg(pptx, slide, "function", 389, B);
  tok(slide, TOK.lx, 462, 435);
  seg(pptx, slide, "during training ,", 505, B, { italic: true });
  seg(pptx, slide, "one can use", 667, B);
  tok(slide, TOK.phi, 779, 435);
  tok(slide, TOK.plx, 798, 435);
}

function drawLine4(pptx, slide) {
  const B = 469.5;
  seg(pptx, slide, "where", 209, B);
  tok(slide, TOK.phi, 272, 462);
  seg(pptx, slide, "is any monotonically increase function", 299, B, { italic: true });
}

function drawPeachLine(pptx, slide) {
  const B = 510.7;
  seg(pptx, slide, "We will use", 104, B);
  tok(slide, TOK.frac, 217, 504.5); // stacked red (1/2), ink 217..228.5 x 488.6..520.4
  tok(slide, TOK.lx, 232, 503.2);
  seg(pptx, slide, "instead of", 282, B, { italic: true });
  tok(slide, TOK.lx, 378, 503.2);
  seg(pptx, slide, "during minimization", 428, B);
  // the original's blue tail is SMALLER type: cap ~12px (vs 15 body) -> 18pt,
  // ink 610..811 (201px; natural TNR 18pt ~214px -> charSpacing -0.5 pins it)
  seg(pptx, slide, "(to Simplify Math operations)", 610, B, { color: COL.blue, fontSize: 18, charSpacing: -0.5 });
}

// ---- composition -------------------------------------------------------------
function render(pptx, slide) {
  // 1) certified parent composition (chrome ONCE with numeral 24 + title + 3 panels)
  P.renderBase(pptx, slide, { numeral: NUMERAL });
  // 2) slide 24's measured delta
  drawExplanationBox(pptx, slide);
  drawLine1(pptx, slide);
  drawLine2(pptx, slide);
  drawLine3(pptx, slide);
  drawLine4(pptx, slide);
  drawPeachBox(pptx, slide);
  drawPeachLine(pptx, slide);
}

// ---- direct run ----
if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const slide = pres.addSlide();
  render(pres, slide);
  const out = process.argv[2] || path.resolve(__dirname, "../slide_024_recreated.pptx");
  pres.writeFile({ fileName: out })
    .then(() => console.log("WROTE", out))
    .catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { render, drawExplanationBox, drawPeachBox, NUMERAL };
