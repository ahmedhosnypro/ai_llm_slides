// slide_001.js — "Linear Regression & Classification" title slide (ML lecture 02)
// Root slide (no parents, no children in this deck's dep graph).
//
// Resumed build (gen 3): previous workers banked PIL measurements under
// scratch/ml02/slide001/ (measure_*.py + outputs); no earlier build/render/qa
// existed for this slide, so this is attempt 1.
//
// Ground truth (PIL-measured from unique_slides/slide_001.jpg, 960x540, 1px=1pt):
//   title L1 "Linear Regression &"   ink x 229..720 (w 492, c 474.5), y 144..194
//   title L2 "Classification"        ink x 310..636 (w 327, c 473),   y 203..243
//   subtitle "CSAI 253  -  Spring 2024" ink x 328..620 (w 293, c 474), y 293..319
//   "Prepared By"                    ink x 436..543 (w 108, c 489.5), y 353..373
//   pb name  "Dr. Khaled Mostafa ElSayed" ink x 352..627 (w 276, c 489.5), y 377..401
//   pb email "kmelsayed@zewailcity.edu.eg" ink x 384..594 (w 211, c 490),  y 403..418
//   "Instructors:"                   ink x 87..203  (w 117, left 87),  y 421..437
//   inst name1 "Dr. Khaled Mostafa ElSayed" ink x 124..377 (w 254, left 124), y 449..469
//   inst email1 "kmelsayed@zewailcity.edu.eg" ink x 125..323 (w 199, left 125), y 471..486
//   inst name2 "Dr. Mohamed Maher Ata" ink x 125..340 (w 216, left 125), y 494..509
//   inst email2 "momaher@zewailcity.edu.eg" ink x 126..314 (w 189, left 126), y 518..529
// Colors: modal ink measurements 2026-10-13 (scratch/ml02/slide001/measure_ink_colors*):
//   title/label red ~= #A00E1C (modal A80C1C/941420, median 9F0E1C — darker than the
//   spec's C00000 approximation; the frame wins), all blue text navy ~= #000080
//   (subtitle 000078, pb name 00008C, inst 000060-00006C). Logo block = image crop.
//   Cursor artifact at ~(816,389) is video capture — excluded per GROUND RULES (c).
// Logo: teal square + white panel + Arabic/English wordmark is 81x71px with ~8px
// Arabic micro-text — hand-building cannot match; recreation_brief step 8 endorses
// inserting the logo as an image. Banked crop of the original frame:
//   build/assets/slide001_logo.png (303x81 from x588,y455 — stops short of the red
//   border x899 and the bottom stroke rows>=536), embedded at exact px/72 size.
//
// House chrome: shared_patterns/house_chrome.js (THIS deck's measured geometry:
// white canvas, gray E9E9E7 panel x61..899 y46->bottom, C00000 1pt border,
// bottom red stroke rows 538-539, badge FDFD96 + 6A5ACD ring, numeral 333333).

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

// ---- content constants (measured) ------------------------------------------
const RED = "A00E1C";
const BLUE = "000080";
const LOGO = {
  path: path.resolve(__dirname, "assets/slide001_logo.png"),
  x: 588 / 72, y: 455 / 72, w: 303 / 72, h: 81 / 72,
};

// v2 sizes/tracking/positions — closed-loop corrected against the 150dpi render
// (selfcheck_attempt_1_output.txt): title cs -1.6 (Arial renders wider than the
// original font at matched height, same finding as slide_008's -1.15), subtitle
// cs -1.05, pb2 23.5pt, per-line cy shifts. All positions re-verified in v2.
const LINES = [
  // key, text, font, size, bold, italic, color, align, cx|left(px), inkCenterY(px), charSpacing
  { key: "title1", text: "Linear Regression &", font: "Arial", size: 54, bold: true, italic: false, color: RED, align: "center", cx: 474.5, cy: 162.8, cs: -1.6 },
  { key: "title2", text: "Classification", font: "Arial", size: 54, bold: true, italic: false, color: RED, align: "center", cx: 473, cy: 221.2, cs: -1.6 },
  { key: "subtitle", text: "CSAI 253  -  Spring 2024", font: "Arial", size: 28, bold: true, italic: false, color: BLUE, align: "center", cx: 474, cy: 302.6, cs: -1.05 },
  { key: "pb1", text: "Prepared By", font: "Times New Roman", size: 21, bold: false, italic: true, color: RED, align: "center", cx: 489.5, cy: 360, cs: 0 },
  { key: "pb2", text: "Dr. Khaled Mostafa ElSayed", font: "Times New Roman", size: 24, bold: true, italic: true, color: BLUE, align: "center", cx: 489.5, cy: 383.5, cs: -0.3 },
  { key: "pb3", text: "kmelsayed@zewailcity.edu.eg", font: "Arial", size: 15, bold: true, italic: false, color: BLUE, align: "center", cx: 490, cy: 409, cs: 0 },
  { key: "ins0", text: "Instructors:", font: "Arial", size: 21, bold: true, italic: true, color: RED, align: "left", cx: 87, cy: 428.5, cs: 0 },
  { key: "ins1", text: "Dr. Khaled Mostafa ElSayed", font: "Arial", size: 19, bold: true, italic: true, color: BLUE, align: "left", cx: 124, cy: 455.4, cs: 0 },
  { key: "ins2", text: "kmelsayed@zewailcity.edu.eg", font: "Arial", size: 15, bold: false, italic: false, color: BLUE, align: "left", cx: 125, cy: 477, cs: 0 },
  { key: "ins3", text: "Dr. Mohamed Maher Ata", font: "Arial", size: 19, bold: true, italic: true, color: BLUE, align: "left", cx: 125, cy: 501.5, cs: 0 },
  { key: "ins4", text: "momaher@zewailcity.edu.eg", font: "Arial", size: 15, bold: false, italic: false, color: BLUE, align: "left", cx: 126, cy: 523.5, cs: 0 },
];

const BOX_H = 0.9; // single-line boxes, valign middle on the measured ink center
const CENTERED_W = 9.0, LEFT_W = 6.0;

// ---- per-block draws (component exports) -----------------------------------
function drawLogo(pptx, slide) {
  slide.addImage({ path: LOGO.path, x: LOGO.x, y: LOGO.y, w: LOGO.w, h: LOGO.h });
}

function drawLines(pptx, slide, opts = {}) {
  const skip = opts.skip || {};
  for (const L of LINES) {
    if (skip[L.key]) continue;
    const o = {
      x: L.align === "center" ? L.cx / 72 - CENTERED_W / 2 : (L.cx - 2) / 72,
      y: L.cy / 72 - BOX_H / 2,
      w: L.align === "center" ? CENTERED_W : LEFT_W,
      h: BOX_H,
      align: L.align, valign: "middle",
      fontSize: opts.size?.[L.key] ?? L.size,
      bold: L.bold, italic: L.italic, color: L.color,
      fontFace: L.font, margin: 0,
    };
    if (opts.leftDx?.[L.key]) o.x += opts.leftDx[L.key];
    if (opts.cs?.[L.key] !== undefined) o.charSpacing = opts.cs[L.key];
    else if (L.cs) o.charSpacing = L.cs;
    slide.addText(opts.text?.[L.key] ?? L.text, o);
  }
}

// renderBase: full slide composition (chrome + logo + text lines). A future
// dependent would import this and pass { numeral: <its printed number> }.
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 1 : opts.numeral });
  drawLogo(pptx, slide);
  drawLines(pptx, slide, opts);
}

// ---- build ----------------------------------------------------------------
function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out =
    process.argv[2] ||
    path.resolve(__dirname, "../slide_001_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawLogo, drawLines, LINES, LOGO, RED, BLUE };
