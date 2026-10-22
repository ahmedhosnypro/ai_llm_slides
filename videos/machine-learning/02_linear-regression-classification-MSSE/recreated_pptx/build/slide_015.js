// slide_015.js — "Vector Notation for Linear Regression and Classification (One Sample)"
// ML lecture 02, root slide (no parents). Worker ml02-w015-a3, 2026-10-13.
//
// Ground truth: PIL-measured from unique_slides/slide_015.jpg (960x540, 1px=1pt).
// All equation/vector glyphs are matplotlib mathtext (STIX serif fontset, matches
// the original's narrow italic serif math) -> 600dpi transparent PNGs, embedded at
// EXACT px/600 size, baseline-law aligned; every token anchored at the ORIGINAL's
// measured ink left edge, and each token PNG width-matched anisotropically
// (LANCZOS@600dpi) to the original's measured ink span — the original uses a
// condensed math font, so plain mathtext runs are too wide and collide.
// Tall/short parens: stretched-glyph delimiter PNGs (pattern
// delimiters-stretched-glyph). Positions in eq015_manifest.json (banked).
//
// Measured facts baked in (px):
//   title ink x94..839 y68..90 (Vector #1000A6 / clause #971629 / (One Sample) #1000A6)
//   box1  x73..376 y106..157  fill FBFDE5 (Model + I/P line)
//   box2  x73..355 y195..245  (Model + eq1, per-token colored runs)
//   box4s x73..190 y259..287  (y = W^T X + b with underlined W, X)
//   box3  x73..352 y317..428  (y = (w1 w2 .... wd)(x1;x2;...;xd) + b — org ellipsis is a
//         horizontal 3-dot row at y390..393, x280..293)
//   right box x421..791 y99..293 fill FFFFFF (Input:/X= + col vec, w= + col vec, Output: (y))
//   vector rows: SIX each (3 entries, two '...' dot rows, final entry) — original style
//   Screen-recording cursor artifact in box3 (~x219..240 y318..380) EXCLUDED per
//   judge GROUND RULES clause (c).

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const MANIFEST = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq015_manifest.json"), "utf8"));
const ASSET = (n) => path.resolve(__dirname, "assets", n);
const PX = 1 / 72; // 960x540 frame px -> inches (1px = 1pt)

// ---- measured palette -------------------------------------------------------
const C = {
  titleBlue: "1000A6", titleRed: "971629",
  boxFill: "FBFDE5", boxBorder: "A9A5C2", rightFill: "FFFFFF", rightBorder: "AAA4D1",
  modelRed: "B9111F", labelBlack: "1A1A1A",
  ipRed: "C22433",
  b4Black: "1A1A1A", b4Blue: "3C2BA4", b4Red: "B7283B", b4Green: "318828",
  b3Black: "1F1F1F", b3Blue: "4A3EC4", b3Red: "C04952", b3Green: "499338",
  rbRed: "BE2E40", rbBlue: "3E32B2", rbBlack: "4D4F4C", inputRed: "A61122",
};

// ---- house boxes ------------------------------------------------------------
function drawBox(pptx, slide, x, y, w, h, fill, border) {
  slide.addShape(pptx.ShapeType.rect, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    fill: { color: fill }, line: { color: border, width: 1 },
  });
}

// ---- equation runs from manifest -------------------------------------------
function drawEqRuns(pptx, slide, names) {
  for (const a of MANIFEST) {
    if (!names.includes(a.name)) continue;
    let xIn, yIn;
    if (a.kind === "eq") {
      // baseline law: y_image = target_baseline - baseline_frac * h
      xIn = a.anchor_x_px * PX;
      yIn = a.baseline_y_px * PX - a.baseline_frac * a.h_in;
    } else {
      // delimiter: top-anchored at measured span top; x = measured ink left
      xIn = a.anchor_x_px * PX;
      yIn = a.top_y_px * PX;
    }
    slide.addImage({ path: ASSET(a.png), x: xIn, y: yIn, w: a.w_in, h: a.h_in });
  }
}

// ---- text run helper (left-aligned, vertically centered on measured band) ---
function txt(pptx, slide, text, xPx, cyPx, opts = {}) {
  slide.addText(text, {
    x: xPx * PX, y: (cyPx / 72) - 0.3, w: (opts.wPx || 200) * PX, h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontSize: opts.size || 17, bold: !!opts.bold, italic: !!opts.italic,
    color: opts.color || C.labelBlack, fontFace: "Arial",
    charSpacing: opts.charSpacing, lineSpacing: opts.lineSpacing,
  });
}

// ---- title ------------------------------------------------------------------
function drawTitle(pptx, slide) {
  // ink x94..839 center 466.5, band y68..90 center 79 (closed-loop attempt-1 fix)
  slide.addText([
    { text: "Vector ", options: { color: C.titleBlue } },
    { text: "Notation for Linear Regression and Classification ", options: { color: C.titleRed } },
    { text: "(One Sample)", options: { color: C.titleBlue } },
  ], {
    x: (467.4 - 419) * PX, y: (76.2 / 72) - 0.3, w: 838 * PX, h: 0.6,
    align: "center", valign: "middle", margin: 0,
    fontSize: 24, color: C.titleRed, fontFace: "Arial",
  });
}

// ---- content blocks ---------------------------------------------------------
function drawBox1(pptx, slide) {
  drawBox(pptx, slide, 73, 106, 304, 52, C.boxFill, C.boxBorder);
  txt(pptx, slide, "Model", 78.5, 116.8, { size: 19, bold: true, italic: true, color: C.modelRed });
  // measured thin light-red underline under 'Model' (org rows 124-125, x78..127)
  slide.addShape(pptx.ShapeType.line, { x: 78 * PX, y: 124.6 * PX, w: 49 * PX, h: 0, line: { color: "DE7B77", width: 1 } });
  txt(pptx, slide, "I/P:", 80, 141, { size: 17, bold: true, color: C.labelBlack });
  txt(pptx, slide, "O/P:", 312, 141, { size: 17, bold: true, color: C.labelBlack });
  drawEqRuns(pptx, slide, ["d_ip_pl", "ip_x1", "ip_x2", "ip_x3", "ip_dots", "ip_xn", "d_ip_pr", "d_ip_pl2", "ip_y", "d_ip_pr2"]);
}

function drawBox2(pptx, slide) {
  drawBox(pptx, slide, 73, 195, 283, 51, C.boxFill, C.boxBorder);
  txt(pptx, slide, "Model", 78.5, 206.8, { size: 19, bold: true, italic: true, color: C.modelRed });
  // measured thin light-red underline under 'Model' (org rows 214-215, x78..124)
  slide.addShape(pptx.ShapeType.line, { x: 78 * PX, y: 214.6 * PX, w: 47 * PX, h: 0, line: { color: "DE7B77", width: 1 } });
  drawEqRuns(pptx, slide, [
    "e1_y", "e1_eq", "e1_w1", "e1_x1", "e1_p1", "e1_w2", "e1_x2", "e1_p2", "e1_w2b", "e1_x2b",
    "e1_p3", "e1_dots", "e1_p4", "e1_wd", "e1_xd", "e1_p5", "e1_b",
  ]);
}

function drawBox4s(pptx, slide) {
  drawBox(pptx, slide, 73, 259, 112, 28, C.boxFill, C.boxBorder); // org right border x184
  drawEqRuns(pptx, slide, ["b4_y", "b4_eq", "b4_WT", "b4_X", "b4_p", "b4_b"]);
  // measured underlines under W^T and X (vector notation, dark ink)
  slide.addShape(pptx.ShapeType.line, { x: 110 * PX, y: 284.8 * PX, w: 17 * PX, h: 0, line: { color: C.b4Black, width: 1 } });
  slide.addShape(pptx.ShapeType.line, { x: 141 * PX, y: 284.8 * PX, w: 14 * PX, h: 0, line: { color: C.b4Black, width: 1 } });
}

function drawBox3(pptx, slide) {
  drawBox(pptx, slide, 73, 317, 279, 112, C.boxFill, C.boxBorder);
  drawEqRuns(pptx, slide, [
    "b3_y", "b3_eq",
    "d_b3_rowl", "b3_w1", "b3_w2", "b3_dots", "b3_wd", "d_b3_rowr",
    "d_b3_coll", "b3_x1", "b3_x2", "b3_vd", "b3_xd", "d_b3_colr",
    "b3_p", "b3_b",
  ]);
}

function drawRightBox(pptx, slide) {
  drawBox(pptx, slide, 421, 99, 371, 195, C.rightFill, C.rightBorder);
  txt(pptx, slide, "Input:", 444, 197.9, { size: 19, color: C.inputRed });
  txt(pptx, slide, "X =", 499, 195.4, { size: 17, color: C.rbRed });
  slide.addShape(pptx.ShapeType.line, { x: 499 * PX, y: 205.8 * PX, w: 14 * PX, h: 0, line: { color: C.rbRed, width: 1 } });
  txt(pptx, slide, "w =", 600, 195.9, { size: 19, color: C.rbBlue });
  slide.addShape(pptx.ShapeType.line, { x: 600 * PX, y: 206.3 * PX, w: 17 * PX, h: 0, line: { color: C.rbBlue, width: 1 } });
  txt(pptx, slide, "Output:", 687, 202, { size: 17, color: C.labelBlack });
  drawEqRuns(pptx, slide, [
    "d_rb_xl", "rb_x1", "rb_x2", "rb_x3", "rb_xd1", "rb_xd2", "rb_xd", "d_rb_xr",
    "d_rb_wl", "rb_w1", "rb_w2", "rb_w3", "rb_wd1", "rb_wd2", "rb_wd", "d_rb_wr",
    "d_rb_yl", "rb_y", "d_rb_yr",
  ]);
}

// ---- component export -------------------------------------------------------
function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 15 : opts.numeral;
  drawHouseChrome(pptx, slide, { numeral });
  drawTitle(pptx, slide);
  drawBox1(pptx, slide);
  drawBox2(pptx, slide);
  drawBox4s(pptx, slide);
  drawBox3(pptx, slide);
  drawRightBox(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out = process.argv[2] || path.resolve(__dirname, "../slide_015_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase };
