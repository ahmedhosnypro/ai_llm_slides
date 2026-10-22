// slide_027.js — machine-learning/02_linear-regression-classification-MSSE
// "Minimum Sum Squared Error (MSSE) Technique" (root slide, no parents). Gen 9
// worker ml02-w027-g9, 2026-10-13; rebuilt from gen-7/8 banked measurements
// after the hue-separated reconciliation (scratch/ml02/slide027/).
//
// Ground truth PIL-measured from unique_slides/slide_027.jpg (960x540, 1px=1pt):
//   title ink x148..785 y69..97 (center 466.5,83) bold #9A0E1E ~30pt
//   subtitle "(Least Squares)" ink x364..569 y102..128 center 466.5 bold #030097 ~24pt
//   LT box x82..389 y170..341 white; LB box x82..389 y355..429 pale yellow FFFFCC
//   PB box x493..871 y249..340 pink F8C8DC; RM box x488..795 y374..504 white
//   borders C00000 1pt (measured washed #B5505F..#C87F86 on JPEG)
//   pink round hl F8A5C2: LT x142..278 y188..244; LB x176..328 y364..420
//   blue round hl CCE5FF: RM x498..734 y385..441 (measured fill #DAECFA)
//   big red right-curly-brace: stem x425.5 y180..424, cusp to x447 @y300,
//     tips curl to x~409 @y165/436 — bezier PNG eq_027_brace.png (stroke 2.6px #A61C26)
//   equations = matplotlib mathtext 600dpi PNGs, height-calibrated +
//     width-matched (LANCZOS) to the original's measured ink boxes,
//     baseline-law placed (eq027_manifest.json). Measured token colors:
//     W black / = dark / constructs violet #4F0078/#51006E (LT,LB) and
//     blue #1400A8 (PB) #1A18B8 (RM); PB -1b + RM -1s RED; Y red #A70010/#BD000E
//   underlines: LT W y228 x91..116 black; LT Y y228 x261..277 red;
//     LB W y407 x102..126 black; LB Y y406 x348..367 red
//   sad face x322..375 y192..249 fill E7C420, black eyes + bezier frown PNG
//     (eq_027_frown.png — native arc only reached y231.8 vs orig 236.5);
//   smiley native smileyFace x704 y456 34x37 F2DD49 (slide-018 certified pattern)
//   text: "is non-square matrix" #2B1F9E fs17 @x165 cy275.5;
//     "There is NO Inverse" #A7071D fs19 bold italic @x96 cy302.5;
//     "Remember" #9A122B fs17 bold italic @x505 cy396.5;
//     "In General:" #252525 fs14.5 bold @x506 cy474.5; "<<<" #3A2F97 fs16 bold @x621
//
// House chrome: shared_patterns/house_chrome.js (THIS deck's geometry), numeral 27.

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const NUMERAL = "27";
const PX = (v) => v / 72; // frame px -> inches (1px = 1pt)
const PAD600 = 8 / 600;   // render_eq 8px @600dpi pad

const MANIFEST = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq027_manifest.json"), "utf8"));
const EQ = Object.fromEntries(MANIFEST.map((m) => [m.name, m]));
const ASSETS = path.resolve(__dirname, "assets");

const COL = {
  title: "9A0E1E", subtitle: "030097", heading: "7E1420",
  border: "C00000", ltFill: "FFFFFF", lbFill: "FFFFCC",
  pbFill: "F8C8DC", rmFill: "FFFFFF",
  pinkHl: "F8A5C2", blueHl: "CCE5FF",
  lt2blue: "2B1F9E", lt3red: "A7071D", remember: "9A122B",
  ingeneral: "252525", lll: "3A2F97",
  black: "0A0A0A",
};
const FONT = "Arial";

function eqImg(slide, name) {
  const e = EQ[name];
  if (e.kind === "image") {  // custom-drawn asset (rm_C): x_px/y_px = PNG top-left
    slide.addImage({ path: path.join(ASSETS, e.png), x: PX(e.x_px), y: PX(e.y_px), w: e.w_in, h: e.h_in });
    return;
  }
  const xIn = PX(e.anchor_x_px) - PAD600;
  const yIn = PX(e.baseline_y_px) - e.baseline_frac * e.h_in;
  slide.addImage({ path: path.join(ASSETS, e.png), x: xIn, y: yIn, w: e.w_in, h: e.h_in });
}

function txt(pptx, slide, text, xPx, cyPx, opts = {}) {
  slide.addText(text, {
    x: PX(xPx), y: cyPx / 72 - 0.3, w: PX(opts.wPx || 250), h: 0.6,
    align: opts.align || "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: opts.size || 17, bold: !!opts.bold,
    italic: !!opts.italic, color: opts.color || COL.black,
    ...(opts.charSpacing !== undefined ? { charSpacing: opts.charSpacing } : {}),
  });
}

function underline(pptx, slide, x0, x1, y, color) {
  slide.addShape(pptx.ShapeType.line, {
    x: PX(x0), y: PX(y), w: PX(x1 - x0), h: 0,
    line: { color, width: 1 },
  });
}

// ---- blocks -----------------------------------------------------------------
function drawTitle(pptx, slide) {
  txt(pptx, slide, "Minimum Sum Squared Error (MSSE) Technique", 47, 79.3,
      { wPx: 839, align: "center", size: 28.0, bold: true, color: COL.title });
  txt(pptx, slide, "(Least Squares)", 268, 112.0,
      { wPx: 400, align: "center", size: 27.6, bold: true, color: COL.subtitle });
}

function drawBoxes(pptx, slide) {
  const box = (x, y, w, h, fill) => slide.addShape(pptx.ShapeType.rect, {
    x: PX(x), y: PX(y), w: PX(w), h: PX(h),
    fill: { color: fill }, line: { color: COL.border, width: 1 },
  });
  box(82, 170, 307, 171, COL.ltFill);   // left top
  box(82, 355, 307, 74, COL.lbFill);    // left bottom (pale yellow)
  box(493, 249, 378, 91, COL.pbFill);   // right top (pink)
  box(488, 374, 307, 130, COL.rmFill);  // right bottom (Remember)
  const hl = (x, y, w, h, fill) => slide.addShape(pptx.ShapeType.roundRect, {
    x: PX(x), y: PX(y), w: PX(w), h: PX(h),
    fill: { color: fill }, line: { type: "none" }, rectRadius: 0.07,
  });
  hl(142, 188, 136, 56, COL.pinkHl);    // LT equation highlight
  hl(176, 364, 152, 56, COL.pinkHl);    // LB equation highlight
  hl(498, 385, 236, 56, COL.blueHl);    // Remember box highlight
}

function drawBrace(slide) {
  const b = EQ.brace;
  slide.addImage({ path: path.join(ASSETS, b.png),
    x: PX(b.x_px), y: PX(b.y_px), w: b.w_in, h: b.h_in });
}

function drawLeftTop(pptx, slide) {
  eqImg(slide, "lt_W");   eqImg(slide, "lt_eq");
  eqImg(slide, "lt_C1");  eqImg(slide, "lt_Y");
  underline(pptx, slide, 91, 117, 228.5, COL.black);
  underline(pptx, slide, 261, 277, 228.5, "A70010");
  // sad face: yellow ball + eyes + bezier frown
  slide.addShape(pptx.ShapeType.ellipse, {
    x: PX(320), y: PX(192), w: PX(56), h: PX(58),
    fill: { color: "E7C420" }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: PX(334), y: PX(211), w: PX(6.5), h: PX(7.5),
    fill: { color: "140600" }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: PX(354), y: PX(211), w: PX(6.5), h: PX(7.5),
    fill: { color: "140600" }, line: { type: "none" },
  });
  eqImg(slide, "frown");  // bezier frown PNG (native arc too shallow)
  eqImg(slide, "lt2_X");
  txt(pptx, slide, "is non-square matrix", 166.4, 273.1, { wPx: 200, size: 21.6, color: COL.lt2blue, charSpacing: -1.2 });
  txt(pptx, slide, "There is NO Inverse", 93.5, 302.3, { wPx: 220, size: 22.5, bold: true, italic: true, color: COL.lt3red, charSpacing: -1.95 });
}

function drawLeftBottom(pptx, slide) {
  eqImg(slide, "lb_W");   eqImg(slide, "lb_eq");
  eqImg(slide, "lb_C1");  eqImg(slide, "lb_Y");
  underline(pptx, slide, 102, 127, 407, COL.black);
  underline(pptx, slide, 348, 368, 406.5, "BD000E");
}

function drawRightTop(pptx, slide) {
  txt(pptx, slide, "Pseudo Inverse of Non-Square Matrix", 447.5, 230,
      { wPx: 400, align: "center", size: 16, bold: true, color: COL.heading });
  eqImg(slide, "pb_A");   eqImg(slide, "pb_eq");
  eqImg(slide, "pb_C");   eqImg(slide, "pb_D");   eqImg(slide, "pb_E");
}

function drawRemember(pptx, slide) {
  txt(pptx, slide, "Remember", 505.5, 395.5, { wPx: 120, size: 18, bold: true, italic: true, color: COL.remember, charSpacing: -2.8 });
  eqImg(slide, "rm_A");   eqImg(slide, "rm_D1");
  // rm_D1's minus is invisible in the 15.7pt PNG render (thin-stroke alpha
  // dilution through LO downsampling) — native 2pt line, measured orig
  // x626.5..633.5 cy415.0 (gen 9)
  slide.addShape(pptx.ShapeType.line, {
    x: PX(626.2), y: PX(414.9), w: PX(8.0), h: 0,
    line: { color: "C0202F", width: 2 },
  });
  eqImg(slide, "rm_eq");  eqImg(slide, "rm_C");
  eqImg(slide, "rm_D2");
  eqImg(slide, "rm_S1");  eqImg(slide, "rm_S2");  eqImg(slide, "rm_S3");
  txt(pptx, slide, "In General:", 507, 474.5, { wPx: 100, size: 16, bold: true, color: COL.ingeneral });
  eqImg(slide, "rm_d");
  txt(pptx, slide, "<<<", 621.3, 474.5, { wPx: 45, size: 20, bold: true, color: COL.lll });
  eqImg(slide, "rm_N");
  // smiley face (native, slide-018 certified pattern)
  slide.addShape(pptx.ShapeType.smileyFace, {
    x: PX(704), y: PX(456), w: PX(34), h: PX(37),
    fill: { color: "F2DD49" }, line: { color: "000000", width: 1 },
  });
}

// renderBase: full composition (children would import; slide 27 has none).
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? NUMERAL : opts.numeral });
  drawTitle(pptx, slide);
  drawBoxes(pptx, slide);
  drawBrace(slide);
  drawLeftTop(pptx, slide);
  drawLeftBottom(pptx, slide);
  drawRightTop(pptx, slide);
  drawRemember(pptx, slide);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("WROTE", outPath));
}

if (require.main === module) {
  const out = process.argv[2] || path.resolve(__dirname, "../slide_027_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase };
