// slide_043.js — 001_introduction slide 43 "Problem: Image will vanish  if applying more filters in cascade"
// Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_043.jpg (960x540, 1px = 1pt = 1/72 in).
//   Measurement passes: qa/slide043/measure_original{,2,3,4,5}_out.txt + crops (banked).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 43 (001_introduction originals carry no printed
//   numbers — ASSUMPTION PENDING FOUNDER VETO, see video AGENTS.md).
//
// LO single-line baseline offsets (calibrated, qa/slide043/calib*_measure_out.txt):
//   baseline = box_top + offset(font,size,ls)  with ls=25,h=0.6in:
//     Times/TimesB ~29.7-29.8 | URW Gothic 20.7 ~30.1 | Verdana Bold 16 ~30.8 | Comic 26 ~29.9 | Comic 10 ~31.0
//   Text placed by target baseline (or measured ink center for the handwriting labels).
//
// Measured constants (frame px):
//   title   Times New Roman Bold 29pt C00000, ink x99..866 center 482.5->box center 483, baseline 83.7
//           (font forensics: no installed face matches all word widths incl. 'Problem:' 1.40 ratio;
//            TimesB best fit 4/6 words -> documented deviation, ground rule (d)-class MINOR)
//   panel   inner white panel stroke-center rect x81..845 y111..380, fill FFFFFF, border C00000 1pt
//   bullets URW Gothic (=Century Gothic metrics, original face not installed) 20.7pt #3F3F3F,
//           ink left 148 (box 147), baselines 140.3/170.2/199.9; hollow ring markers d9.5 at
//           centers (129.5,133/162.5/192.5), outline D8A800 1pt (spec approx)
//   grid5   x244..438 y228..375 (cell 39 x 29.6), values [[1,1,1,0,0],[0,1,1,1,0],[0,0,1,1,1],
//           [0,0,1,1,0],[0,1,1,0,0]]; top-left 3x3 fill FDFF0B (measured), rest 0DC94F (measured);
//           1pt black borders; numbers Verdana Bold 16 black centered (digit h12 measured)
//   annots  9 tiny red FF0000 'x1'/'x0' (Comic 10pt) at the bottom-right of each yellow cell in a
//           CHECKERBOARD (r+c even -> x1, odd -> x0 — matches the slide-041 filter [[1,0,1],[0,1,0],
//           [1,0,1]]). NOTE: the spec's verbatim_text guessed 3+3 under cols 1/3; the FRAME shows 9
//           (crop_grid5.png) — frame is ground truth, deviation documented.
//   labels  'Image'/'After conv 1'/'After conv 2' Comic Sans MS 26pt black (handwriting face of the
//           original — wider/shorter than Comic — not installed; closest match, ground rule (d)),
//           ink centers y 213/211/210, centers x 341/584.5/754.5
//   arrows  rightArrow x451 y296 w50 h20 and x676 y296.5 w50 h20, white fill, black 1pt outline;
//           head length 20px = full ss -> zip-patch adj2=100000 (pptxgenjs 4.0.1 cannot set
//           preset adjusts; patch_arrow_adj.py runs post-build)
//   grid3   3x3 sage cells 48x37 at x 510/562/614, y 248/287/326 (4-5px white gaps), fill 95A38A,
//           border 887240 1pt (measured orange-tan wash); values 4 3 4 / 2 4 3 / 2 3 4, VerdanaB16
//   cell18  single cell x738..787 y287..323, same fill/border, '18' VerdanaB16 centered
//   box     explanation box stroke-center x77..859 y393..509.5, fill FFFFFF, border 000080 1pt
//           (spec's 2E75B6 is the washed-out reading; measured border wash #7D7898/#8F8AAA = navy)
//   navy    Times New Roman #000080, ink left 88, baselines 418.5/445.4/472.4/499.7 (pitch ~27),
//           L1 'Original 5x5' bold 21pt; L2-L4 21.2pt (LO-width calibrated); VERBATIM text incl.
//           double space 'filter  of' and 'be3x3'
//   NOT recreated (video artifacts, judge ground rule (c)): bottom black strip y518..539, top gray
//   strip, white mouse cursor at (~790, ~90).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_043_recreated.pptx";

const px = (v) => v / 72;

// ---- palette (measured) ----
const TITLE_RED = "C00000";
const PANEL_WHITE = "FFFFFF";
const BULLET_GRAY = "3F3F3F";
const MARKER_TAN = "D8A800";
const YELLOW = "FDFF0B";
const GREEN = "0DC94F";
const SAGE = "95A38A";
const SAGE_BORDER = "887240";
const NAVY = "000080";
const ANNOT_RED = "FF0000";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- playlist house chrome (white canvas, gray panel + red border, badge 43) ----
drawHouseChrome(pres, slide, { numeral: "43" });

// ---- inner white panel with red border (stroke-center rect x81..845 y111..380) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(81), y: px(111), w: px(764), h: px(269),
  fill: { color: PANEL_WHITE }, line: { color: TITLE_RED, width: 1 },
});

// ---- title: Times New Roman Bold 29pt C00000, ink center 483, baseline 83.7 ----
slide.addText("Problem: Image will vanish  if applying more filters in cascade", {
  x: px(51), y: px(49.9), w: px(864), h: 0.6,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Times New Roman", fontSize: 29, bold: true, color: TITLE_RED,
  lineSpacing: 37,
});

// ---- bullets (URW Gothic 20.7pt; ring markers) ----
const BULLETS = [
  { text: "Our images get smaller and smaller", baseline: 140.3 },
  { text: "Not too deep architectures", baseline: 170.2 },
  { text: "Details are lost", baseline: 199.9 },
];
BULLETS.forEach((B, i) => {
  slide.addText(B.text, {
    x: px(147), y: px(B.baseline - 30.1), w: px(600), h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontFace: "URW Gothic", fontSize: 20.7, color: BULLET_GRAY,
    lineSpacing: 25,
  });
  const cy = [133, 162.5, 192.5][i];
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(124.75), y: px(cy - 4.75), w: px(9.5), h: px(9.5),
    fill: { type: "none" }, line: { color: MARKER_TAN, width: 1 },
  });
});

// ---- 5x5 Image grid (cells share borders; fills + black 1pt strokes) ----
const G5 = [
  [1, 1, 1, 0, 0],
  [0, 1, 1, 1, 0],
  [0, 0, 1, 1, 1],
  [0, 0, 1, 1, 0],
  [0, 1, 1, 0, 0],
];
const G5X = 244, G5Y = 228, CW = 39, CH = 29.6;
for (let r = 0; r < 5; r++) {
  for (let c = 0; c < 5; c++) {
    const yellow = r < 3 && c < 3;
    slide.addShape(pres.ShapeType.rect, {
      x: px(G5X + c * CW), y: px(G5Y + r * CH), w: px(CW), h: px(CH),
      fill: { color: yellow ? YELLOW : GREEN }, line: { color: "000000", width: 1 },
    });
  }
}
// numbers (Verdana Bold 16, centered; ink-center offset 24.7 from box top)
for (let r = 0; r < 5; r++) {
  for (let c = 0; c < 5; c++) {
    const ccx = G5X + c * CW + CW / 2;
    const ccy = G5Y + r * CH + CH / 2;
    slide.addText(String(G5[r][c]), {
      x: px(ccx - 27), y: px(ccy - 24.7), w: px(54), h: 0.6,
      align: "center", valign: "middle", margin: 0,
      fontFace: "Verdana", fontSize: 16, bold: true, color: "000000",
      lineSpacing: 25,
    });
  }
}

// ---- 9 red x1/x0 checkerboard annotations (Comic 10pt, right-aligned at cell right - 1) ----
// (r+c) even -> 'x1', odd -> 'x0'  [slide-041 filter [[1,0,1],[0,1,0],[1,0,1]]]
for (let r = 0; r < 3; r++) {
  for (let c = 0; c < 3; c++) {
    const lbl = (r + c) % 2 === 0 ? "x1" : "x0";
    const right = G5X + (c + 1) * CW - 1;
    const baseline = G5Y + (r + 1) * CH - 3.6;
    slide.addText(lbl, {
      x: px(right - 24), y: px(baseline - 31.0), w: px(24), h: 0.6,
      align: "right", valign: "middle", margin: 0,
      fontFace: "Comic Sans MS", fontSize: 10, color: ANNOT_RED,
      lineSpacing: 25,
    });
  }
}

// ---- diagram labels (Comic Sans MS 26pt, ink-center placement) ----
const LABELS = [
  { text: "Image", cx: 341, cy: 213, off: 24.05 },
  { text: "After conv 1", cx: 584.5, cy: 211, off: 19.25 },
  { text: "After conv 2", cx: 754.5, cy: 210, off: 19.1 },
];
LABELS.forEach((L) => {
  slide.addText(L.text, {
    x: px(L.cx - 150), y: px(L.cy - L.off), w: px(300), h: 0.6,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Comic Sans MS", fontSize: 26, color: "000000",
    lineSpacing: 25,
  });
});

// ---- block arrows (white fill, black 1pt outline; head adj patched post-build) ----
slide.addShape(pres.ShapeType.rightArrow, {
  x: px(451), y: px(296), w: px(50), h: px(20),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});
slide.addShape(pres.ShapeType.rightArrow, {
  x: px(676), y: px(296.5), w: px(50), h: px(20),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});

// ---- 3x3 After-conv-1 grid (separate sage cells with gaps, orange-tan borders) ----
const G3 = [[4, 3, 4], [2, 4, 3], [2, 3, 4]];
const G3X = [510, 562, 614], G3Y = [248, 287, 326], GW = 48, GH = 37;
for (let r = 0; r < 3; r++) {
  for (let c = 0; c < 3; c++) {
    slide.addShape(pres.ShapeType.rect, {
      x: px(G3X[c]), y: px(G3Y[r]), w: px(GW), h: px(GH),
      fill: { color: SAGE }, line: { color: SAGE_BORDER, width: 1 },
    });
    const ccx = G3X[c] + GW / 2, ccy = G3Y[r] + GH / 2;
    slide.addText(String(G3[r][c]), {
      x: px(ccx - 27), y: px(ccy - 24.7), w: px(54), h: 0.6,
      align: "center", valign: "middle", margin: 0,
      fontFace: "Verdana", fontSize: 16, bold: true, color: "000000",
      lineSpacing: 25,
    });
  }
}

// ---- 1x1 output cell '18' ----
slide.addShape(pres.ShapeType.rect, {
  x: px(738), y: px(287), w: px(49), h: px(36),
  fill: { color: SAGE }, line: { color: SAGE_BORDER, width: 1 },
});
slide.addText("18", {
  x: px(762.5 - 30), y: px(305 - 24.7), w: px(60), h: 0.6,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Verdana", fontSize: 16, bold: true, color: "000000",
  lineSpacing: 25,
});

// ---- explanation box (white fill, navy 1pt border; stroke-center x77..859 y393..509.5) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(77), y: px(393), w: px(782), h: px(116.5),
  fill: { color: PANEL_WHITE }, line: { color: NAVY, width: 1 },
});

// ---- navy text lines (Times New Roman; verbatim incl. 'filter  of' + 'be3x3') ----
const NAVY_LINES = [
  { text: "Original 5x5", bold: true, size: 21.0, baseline: 418.5, off: 29.8 },
  { text: "After apply one filter  of size 3x3, output will be3x3", bold: false, size: 21.2, baseline: 445.4, off: 29.7 },
  { text: "After applying second filter on the output (cascaded filters)", bold: false, size: 21.2, baseline: 472.4, off: 29.7 },
  { text: "Output will be 1x1", bold: false, size: 21.2, baseline: 499.7, off: 29.7 },
];
NAVY_LINES.forEach((L) => {
  slide.addText(L.text, {
    x: px(88), y: px(L.baseline - L.off), w: px(700), h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Times New Roman", fontSize: L.size, bold: L.bold, color: NAVY,
    lineSpacing: 25,
  });
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
