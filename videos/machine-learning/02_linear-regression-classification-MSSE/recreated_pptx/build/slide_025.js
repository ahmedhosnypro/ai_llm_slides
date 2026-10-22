// slide_025.js — "Minimization of Loss function to obtain BEST model parameters"
// ML lecture 02 (machine-learning/02_linear-regression-classification-MSSE), ROOT slide.
// Worker ml02-w025-a5, 2026-10-13 (resumed from gen-4 measurement sweep, attempt 1 build).
//
// Ground truth: PIL-measured from unique_slides/slide_025.jpg (960x540, 1px=1pt).
// All equations are matplotlib mathtext (STIX serif) -> 600dpi transparent PNGs
// (scripts/render_eq.py core + mathtext.fontset='stix'), embedded at EXACT px/600
// size, baseline-law + ink-left-law aligned, each run width-matched (LANCZOS@600dpi)
// to the original's measured ink span (slide_015 certified mechanism). Manifest:
// assets/eq025_manifest.json. Banked measurements: scratch/ml02/slide025/measure_*.txt
//
// Measured facts baked in (px, 1px=1pt):
//   title ink x162..808 y68..89 (red 971629; 'BEST' blue 1000A6 at x565..619), baseline ~83.5
//   deriv box  x72..892  y102..277  fill FBFDE5, border ~C2C5C1
//   eq1 ink x98..544  baseline 135 (frac1 x156..168 RED C00000; frac2 x341..352 black)
//   eq2 ink x98..633  baseline 199  eq3 ink x98..524 baseline 256 (fracs black, x156..168)
//   remember box x676..882 y133..238 fill DAECFA border ~9BAFB9 (NESTED inside deriv box)
//     'Remember' hdr ink x681..755 y138..150 (red 971629 italic)
//     line1 "X is a matrix, W is a vector," ink x682..872 caps y158..169 — X RED, W BLUE (measured)
//     line2 "X W is a vector" ink x680..787 caps y179..190 — all black
//     remeq "Y^T (X W) = (X W)^T Y" ink x680..864 baseline 232 — NO underline (measured;
//           the spec's underline claim was the blue box's own bottom border, probe y233-238)
//   pink box x72..507 y287..343 fill F7CFD2 border ~911E30
//     "\frac{dLoss}{dW} = 0" ink x79..164 baseline 321 (stacked \frac, script-size operands)
//     "Get Best W that minimizes the loss" ink x196..501 caps y307..321, W red
//   bottom area y343..538 empty panel gray; mouse cursor artifact EXCLUDED (ground rule (c))

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const MANIFEST = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq025_manifest.json"), "utf8"));
const ASSET = (n) => path.resolve(__dirname, "assets", n);
const PX = 1 / 72; // 960x540 frame px -> inches (1px = 1pt)

// ---- measured palette -------------------------------------------------------
const C = {
  titleRed: "971629", titleBlue: "1000A6",
  ink: "1F1F1F", red: "C00000", blue: "1000A6",
  derivFill: "FBFDE5", derivBorder: "C2C5C1",
  remFill: "DAECFA", remBorder: "9BAFB9",
  pinkFill: "F7CFD2", pinkBorder: "911E30",
};
const SERIF = "Times New Roman";

// ---- equation placement (baseline law + measured ink-left law) ---------------
function drawEq(slide, name, anchorXpx, baselineYpx) {
  const a = MANIFEST[name];
  if (!a) throw new Error("missing manifest entry " + name);
  const inkDxIn = a.ink_dx / 600; // 600dpi px -> inches
  slide.addImage({
    path: ASSET(a.png),
    x: anchorXpx * PX - inkDxIn,
    y: baselineYpx * PX - a.baseline_frac * a.h_in,
    w: a.w_in, h: a.h_in,
  });
}

// vector-notation underline (measured 2px band below baseline; 1pt line shape,
// slide_015 certified mechanism). Original census (measure_10 + thr-233 maps):
// Y/Ŷ/W underlined, X NOT underlined, in every equation; W underlined in the
// remember note lines; remeq carries its 4 measured ink bands.
function drawUnderline(pptx, slide, x0px, x1px, yPx, color) {
  slide.addShape(pptx.ShapeType.line, {
    x: x0px * PX, y: yPx * PX, w: (x1px - x0px) * PX, h: 0,
    line: { color: color, width: 1 },
  });
}

// single-line text placed so the rendered baseline lands on baselineYpx
// (box center = baseline - (ascent-descent)/2, valign middle, margin 0)
function line(pptx, slide, runs, xPx, baselineYpx, opts = {}) {
  const fs_ = opts.size || 18;
  const asc = (opts.serif === false ? 0.905 : 0.891) * fs_;
  const desc = (opts.serif === false ? 0.212 : 0.216) * fs_;
  const cy = baselineYpx - (asc - desc) / 2;
  slide.addText(runs, {
    x: xPx * PX, y: cy * PX - 0.3, w: (opts.wPx || 220) * PX, h: 0.6,
    align: opts.align || "left", valign: "middle", margin: 0,
    fontFace: opts.serif === false ? "Arial" : SERIF,
    fontSize: fs_, charSpacing: opts.charSpacing,
  });
}

// ---- title ------------------------------------------------------------------
function drawTitleBox(pptx, slide) {
  const fs_ = 21.4, asc = 0.905 * fs_, desc = 0.212 * fs_;
  const cy = 83.5 - (asc - desc) / 2;
  slide.addText([
    { text: "Minimization of Loss function to obtain ", options: { color: C.titleRed } },
    { text: "BEST", options: { color: C.titleBlue } },
    { text: " model parameters", options: { color: C.titleRed } },
  ], {
    x: (485 - 419) * PX, y: cy * PX - 0.3, w: 838 * PX, h: 0.6,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: fs_, bold: true,
  });
}

// ---- derivation box (pale yellow, full panel width) + 3 equation lines -------
function drawDerivBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 72 * PX, y: 102 * PX, w: 820 * PX, h: 175 * PX,
    fill: { color: C.derivFill }, line: { color: C.derivBorder, width: 1 },
  });
  // eq1: Loss = 1/2 (Y-Ŷ)^T (Y-Ŷ) = 1/2 (Y-XW)^T (Y-XW)   [frac1 RED, frac2 black]
  drawEq(slide, "eq025_loss", 98, 135);
  drawEq(slide, "eq025_eq", 139, 135);
  drawEq(slide, "eq025_frac_red", 156, 135);
  drawEq(slide, "eq025_c1", 172, 135);
  drawEq(slide, "eq025_eq", 320, 135);
  drawEq(slide, "eq025_frac_blk", 341, 135);
  drawEq(slide, "eq025_f1", 357, 135);
  // eq2: Loss = 1/2 [ Y^T Y + (XW)^T (XW) - Y^T (XW) - (XW)^T Y ]
  drawEq(slide, "eq025_loss", 98, 199);
  drawEq(slide, "eq025_eq", 139, 199);
  drawEq(slide, "eq025_frac_blk", 156, 199);
  drawEq(slide, "eq025_d2", 170, 199);
  // eq3: Loss = 1/2 [ Y^T Y + (XW)^T (XW) - 2 (XW)^T Y ]
  drawEq(slide, "eq025_loss", 98, 256);
  drawEq(slide, "eq025_eq", 139, 256);
  drawEq(slide, "eq025_frac_blk", 156, 256);
  drawEq(slide, "eq025_d3", 170, 256);
  // vector-notation underlines — measured in the original (Y/Ŷ/W underlined; X never),
  // spans snapped to MY rendered glyph positions (PIL group map of each PNG)
  // eq1 (line y136.9): Y(180..192.5) Yhat(216..233.5) Y(257..269.5) Yhat(293..310.5)
  const u1 = [[180,192.5],[216,233.5],[257,269.5],[293,310.5]];
  for (const [a, b] of u1) drawUnderline(pptx, slide, a, b, 136.9, C.ink);
  // eq1 group 2 (attempt 2 fix, cropcmp_eq1 BLOCKER): original underlines Y and W in
  // BOTH (Y-XW) factors (census bands y136-137: Y 364..378, W 418..437, Y 464..478,
  // W 518..537; X bare — 10x zoom verified 2026-10-14). Spans snapped to MY f1 PNG
  // glyph map (anchor 357, ink_dx 8): Y 364.9..377.0, W 419.9..436.5,
  // Y 466.2..478.2, W 521.2..537.8 (paren tail excluded).
  const u1b = [[364.9,377.0],[419.9,436.5],[466.2,478.2],[521.2,537.8]];
  for (const [a, b] of u1b) drawUnderline(pptx, slide, a, b, 136.9, C.ink);
  // eq2 (line y200.9): Y(181..193.5) Y(212..224.5) W(288..305.5) W(358..375.5)
  //                    Y(421.5..434.5) W(479.5..496.5) W(570..587.5) Y(613..625.5)
  const u2 = [[181,193.5],[212,224.5],[288,305.5],[358,375.5],[421.5,434.5],[479.5,496.5],[570,587.5],[613,625.5]];
  for (const [a, b] of u2) drawUnderline(pptx, slide, a, b, 200.9, C.ink);
  // eq3 (line y257.9): Y(181..193.5) Y(212..224.5) W(288..304.5) W(357..374.5) W(462..478.5) Y(504..517)
  const u3 = [[181,193.5],[212,224.5],[288,304.5],[357,374.5],[462,478.5],[504,517]];
  for (const [a, b] of u3) drawUnderline(pptx, slide, a, b, 257.9, C.ink);
}

// ---- Remember note box (light blue, nested inside the derivation box) --------
function drawRememberBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 676 * PX, y: 133 * PX, w: 206 * PX, h: 105 * PX,
    fill: { color: C.remFill }, line: { color: C.remBorder, width: 1 },
  });
  line(pptx, slide, [
    { text: "Remember", options: { color: C.titleRed, italic: true } },
  ], 678, 149.5, { size: 18, wPx: 130 });
  // line1 — measured: X red, W blue (frame census; overrides spec's guess)
  line(pptx, slide, [
    { text: "X", options: { color: C.red, italic: true } },
    { text: " is a matrix, ", options: { color: C.ink } },
    { text: "W", options: { color: C.blue, italic: true } },
    { text: " is a vector,", options: { color: C.ink } },
  ], 679, 169.5, { size: 18, wPx: 215 });
  // line2 — all black (census: 0 red / 0 blue pixels)
  line(pptx, slide, [
    { text: "X W", options: { color: C.ink, italic: true } },
    { text: " is a vector", options: { color: C.ink } },
  ], 680, 190.5, { size: 18, wPx: 130 });
  // vector-notation underlines: W underlined in both note lines (measured bands
  // y171-172 x778..793 and y191-192 x696..711); X never underlined
  drawUnderline(pptx, slide, 778, 794, 172.2, C.blue);
  drawUnderline(pptx, slide, 696, 712, 192.2, C.ink);
  // transpose identity, professional 2D mathtext; underlines under MY Y/W tokens
  // (original bands: Y 680..692, W 728..746, W 816..833, Y 852..865; X never underlined)
  drawEq(slide, "eq025_r1", 680, 232);
  const ur = [[680, 692], [732, 748], [814, 830], [852, 864]];
  for (const [a, b] of ur) drawUnderline(pptx, slide, a, b, 232.2, C.ink);
}

// ---- gradient-condition box (pink) -------------------------------------------
function drawPinkBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 72 * PX, y: 287 * PX, w: 435 * PX, h: 56 * PX,
    fill: { color: C.pinkFill }, line: { color: C.pinkBorder, width: 1 },
  });
  drawEq(slide, "eq025_p1", 79, 321.5);
  line(pptx, slide, [
    { text: "Get Best ", options: { color: C.ink } },
    { text: "W", options: { color: C.red, italic: true } },
    { text: " that minimizes the loss", options: { color: C.ink } },
  ], 196, 321.5, { size: 21.8, wPx: 340 });
}

// ---- component export (slide 26 is a child: compose per-block) ---------------
function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 25 : opts.numeral;
  drawHouseChrome(pptx, slide, { numeral });
  drawTitleBox(pptx, slide);
  drawDerivBox(pptx, slide);
  drawRememberBox(pptx, slide);
  drawPinkBox(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] || path.resolve(__dirname, "../slide_025_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawTitleBox, drawDerivBox, drawRememberBox, drawPinkBox, drawEq };
