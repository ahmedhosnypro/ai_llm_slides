// build/slide_025.js — slide 025 "Encoder – Decoder Transformer" (three-panel zoom ladder).
// ROOT slide (no dependency edge): full redraw at PIL-measured geometry from
// unique_slides/slide_025.jpg (960x540, 1px = 1pt, in = px/72). Measurements:
// scratch/slide025/m0_scan, m1_components, m4_left, m5_left2, m6_cols, m7_ascii
// + raw row/col dumps. Figure family: left panel = paper Fig 2 left, center = Fig 2
// right, right = Fig 1 (banked in slide_18_source/), redrawn in the course style.
//
// Laws honored: playlist house chrome via shared_patterns/house_chrome.js (badge
// numeral 25 = printed number on the original frame); verbatim labels incl. casing
// ("SoftMax" left panel vs "Softmax" decoder, lowercase "q" center); margin:0 +
// fontFace everywhere; explicit lineSpacing on every multi-line box; no '#' hex;
// writeFile({fileName}).

const path = require("path");
const PptxGenJS = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const px = (v) => v / 72;

// ---- palette (JPEG-core measured, scratch/slide025/m1/m5/m6 + mode histograms) --
const C = {
  red: "C00000",
  darkRed: "9E1B1B",       // WE ARE HERE bubble (measured 900012/94051C core)
  white: "FFFFFF",
  // left panel
  panelTan: "DEAA75",      // container fill (225,170,116)
  panelBorder: "9A8E80",
  innerTan: "E9B57F",      // inner chart bg (235,182,128)
  olive: "7A7225",         // inner chart border + corner brackets (122,114,37)
  boxTan1: "C89068",       // MatMul boxes (200,144,104)
  boxTan2: "D0A868",       // SoftMax
  boxTan3: "D89068",       // Mask (opt.) (216,144,104)
  boxTan4: "E0B060",       // Scale
  boxText: "2E1E0A",
  qFill: "B23010",         // Q circle (194,45,12 family)
  kvFill: "682C46",        // K/V circles (dark plum, measured both)
  // center panel
  frameGreen: "1B723F",    // center border (29,113,63) — same asset as slide 18 inset
  linearFill: "E9EDEA",
  linearBorder: "808080",
  shadowFill: "E4E4E4",
  shadowBorder: "ABABAB",
  concatFill: "F8FBC6",
  mauve: "BA90AE",         // SDPA front box (186,144,174)
  mauveText: "8C4423",
  circBlue: "5A55D8",      // center V/K circles (104,97,226 JPEG core)
  circRed: "C85060",       // center q circle (203,100,111)
  // right architecture
  archFrame: "0E8A1E",
  encFill: "FDEEDC",       // peach (253,237,221)
  decFill: "CDFCDF",       // pale green (205,255,222)
  decGreenText: "0E7D10",
  stackTan: "C9AC86",      // encoder container plate (201,172,134)
  stackBorder: "4A3A28",
  ffDark: "6E5C42",        // FF inset (110,92,66)
  ffText: "D8BC92",
  anSteel: "5590AC",       // Add & Norm plates (steel BLUE measured 76-101,133-158,161-185)
  anText: "22262B",
  mhaFill: "C67E54",       // encoder MHA (198,126,87)
  mhaFillDec: "AD8458",    // decoder MHA (173,132,88)
  mhaText: "4A2410",
  residGreen: "7CB531",    // residual bars (116,177,49 / 142,166,49)
  vGreen: "3E9C1F",
  kBlue: "23309A",
  qRed: "B02020",
  // (peBrown/peDecBrown retired: PE halves merged into the embedding containers)
  embedBrown: "A37648",    // encoder PE+Input-Embedding merged container (163,118,72 family)
  embedMaroon: "B4726C",   // Output Embedding (180,114,108)
  embedText: "331111",
  nxTan: "E8CBA8",
  nxBorder: "8A6A48",
  nxOlive: "B9BF9C",       // decoder Nx (185,191,156)
  purpleBox: "D284C6",     // Masked MHA (210,132,198)
  purpleBorder: "5A2A66",
  purpleText: "2A1030",
  spine: "2F2F2F",
  ink: "1A1A1A",
  grayLabel: "404040",
  yellow: "F6FC36",        // highlight + Output-Probabilities band (246,252,54)
  arrowRed: "B03020",
  softmaxFill: "CDFCE2",   // decoder Softmax (measured 202-210,252-255,222-227 = container green)
  softmaxBorder: "316B43", // Softmax/Linear border (measured 38-49,94-107,57-67 dark green)
  softmaxText: "143A1C",   // Softmax/Linear label (measured 14-16,51-60,18-34 dark green)
  linearDecFill: "CDFCE2", // decoder Linear (measured same light green as Softmax)
};
const SANS = "Arial";

// small dark up-arrowhead used as the vertical connector between adjacent stack
// elements (the original links every stack box with tiny arrowheads in the gaps)
function spineHead(slide, cx, y, color) {
  slide.addShape("triangle", {
    x: px(cx - 2.5), y: px(y), w: px(5), h: px(4),
    fill: { color: color || C.spine }, line: { color: color || C.spine, width: 0.25 },
  });
}

// thin vertical connector with a small up-arrowhead (the original's decoder-top
// gaps show 1-2px lines with small heads, e.g. x785 y141-151 / y166-177 / y192-199)
function thinConn(slide, cx, yTop, yBot, color) {
  slide.addShape("line", {
    x: px(cx), y: px(yTop + 4), w: 0, h: px(yBot - yTop - 4),
    line: { color: color || C.spine, width: 0.75 },
  });
  slide.addShape("triangle", {
    x: px(cx - 2.5), y: px(yTop), w: px(5), h: px(4),
    fill: { color: color || C.spine }, line: { color: color || C.spine, width: 0.25 },
  });
}

// ---- helpers --------------------------------------------------------------------

function addLines(slide, color, width, pts, opts = {}) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i];
    const [x1, y1] = pts[i + 1];
    const line = { color, width };
    if (opts.dash) line.dashType = opts.dash;
    if (opts.endArrow && i === pts.length - 2) line.endArrowType = "triangle";
    slide.addShape("line", {
      x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
      w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
      flipV: y1 < y0, flipH: x1 < x0,
      line,
    });
  }
}

function flowBox(slide, x, y, w, h, fill, borderColor, borderW, lines, fontSize, lineSpacing, textColor) {
  slide.addShape("rect", {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill }, line: { color: borderColor, width: borderW },
  });
  const items = lines.map((t, i) => ({ text: t, options: { breakLine: i < lines.length - 1 } }));
  slide.addText(items, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize, bold: true, color: textColor || C.boxText,
    lineSpacing,
  });
}

function letterCircle(slide, cx, cy, d, fill, letter, fontSize, letterColor) {
  slide.addShape("ellipse", {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: fill, width: 0.5 },
  });
  slide.addText(letter, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize, bold: true, color: letterColor || "FFFFFF",
  });
}

function cornerHandle(slide, cx, cy, color) {
  slide.addShape("rect", {
    x: px(cx - 3), y: px(cy - 3), w: px(6), h: px(6),
    fill: { color: color || C.frameGreen }, line: { color: color || C.frameGreen, width: 0.25 },
  });
}

// ---- title ----------------------------------------------------------------------

function drawTitle(slide) {
  slide.addText("Encoder – Decoder Transformer", {
    x: px(186), y: px(48), w: px(588), h: px(44),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 31, bold: true, color: C.red,
  });
}

// ---- LEFT panel: Scaled Dot-Product Attention (paper Fig 2 left, course style) ---

function drawLeftPanel(slide) {
  // container
  slide.addShape("roundRect", {
    x: px(44), y: px(210), w: px(163), h: px(313), rectRadius: 0.05,
    fill: { color: C.panelTan }, line: { color: C.panelBorder, width: 1 },
  });
  // red italic 2-line title (measured y232-243 / y254-262)
  slide.addText(
    [
      { text: "Scaled Dot-Product", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(48), y: px(226), w: px(156), h: px(42),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 13, bold: true, italic: true, color: C.red,
      lineSpacing: 22,
    }
  );
  // inner chart: lighter tan bg + olive thin border + 4 L corner brackets
  slide.addShape("rect", {
    x: px(58), y: px(268), w: px(133), h: px(224),
    fill: { color: C.innerTan }, line: { color: C.olive, width: 1 },
  });
  const arm = 12, th = 3;
  const corners = [
    [58, 268, 1, 1], [191, 268, -1, 1], [58, 492, 1, -1], [191, 492, -1, -1],
  ];
  for (const [cx, cy, sx, sy] of corners) {
    slide.addShape("rect", {
      x: px(sx > 0 ? cx : cx - arm), y: px(sy > 0 ? cy : cy - th),
      w: px(arm), h: px(th),
      fill: { color: C.olive }, line: { color: C.olive, width: 0.25 },
    });
    slide.addShape("rect", {
      x: px(sx > 0 ? cx : cx - th), y: px(sy > 0 ? cy : cy - arm),
      w: px(th), h: px(arm),
      fill: { color: C.olive }, line: { color: C.olive, width: 0.25 },
    });
    // small lighter inner handle square at each bracket corner (measured in frame)
    slide.addShape("rect", {
      x: px(sx > 0 ? cx + 3 : cx - 8), y: px(sy > 0 ? cy + 3 : cy - 8),
      w: px(5), h: px(5),
      fill: { color: "C9B880" }, line: { color: "C9B880", width: 0.25 },
    });
  }
  // chain boxes (bottom-up flow), measured extents
  flowBox(slide, 105, 296, 68, 16, C.boxTan1, C.olive, 0.75, ["MatMul"], 9, 11);
  flowBox(slide, 79, 330, 64, 16, C.boxTan2, C.olive, 0.75, ["SoftMax"], 8.5, 10);
  flowBox(slide, 76, 363, 70, 16, C.boxTan3, C.olive, 0.75, ["Mask (opt.)"], 8, 10);
  flowBox(slide, 89, 396, 44, 16, C.boxTan4, C.olive, 0.75, ["Scale"], 8.5, 10);
  flowBox(slide, 80, 430, 62, 16, C.boxTan1, C.olive, 0.75, ["MatMul"], 9, 11);
  // circles (bottom row)
  letterCircle(slide, 90.5, 473.5, 20, C.qFill, "Q", 9);
  letterCircle(slide, 128.5, 473.5, 18, C.kvFill, "K", 8.5);
  letterCircle(slide, 166.5, 473.5, 18, C.kvFill, "V", 8.5);
  // arrows bottom-up
  addLines(slide, C.ink, 0.75, [[90.5, 462], [90.5, 448]], { endArrow: true });
  addLines(slide, C.ink, 0.75, [[128.5, 462], [128.5, 448]], { endArrow: true });
  addLines(slide, C.ink, 0.75, [[111, 429], [111, 414]], { endArrow: true });
  addLines(slide, C.ink, 0.75, [[111, 395], [111, 381]], { endArrow: true });
  addLines(slide, C.ink, 0.75, [[111, 362], [111, 348]], { endArrow: true });
  addLines(slide, C.ink, 0.75, [[111, 329], [111, 314]], { endArrow: true });
  // output arrow above the top MatMul (measured head y278-294 at x~139)
  addLines(slide, C.ink, 0.75, [[139, 294], [139, 283]], { endArrow: true });
  // V bypass up the right side into the top MatMul's right edge (bend near V)
  addLines(slide, C.ink, 0.75, [[167, 462], [174, 434], [174, 309]], { endArrow: true });
}

// ---- WE ARE HERE bubble ----------------------------------------------------------

function drawBubble(slide) {
  // tail (triangle pointing down-right onto the left panel's top edge)
  slide.addShape("triangle", {
    x: px(224), y: px(188), w: px(36), h: px(38),
    rotate: 315, fill: { color: C.darkRed }, line: { color: C.darkRed, width: 0.5 },
  });
  // dark-red circle
  slide.addShape("ellipse", {
    x: px(184), y: px(130), w: px(64), h: px(64),
    fill: { color: C.darkRed }, line: { color: C.darkRed, width: 0.5 },
  });
  slide.addText(
    [
      { text: "WE", options: { breakLine: true } },
      { text: "ARE", options: { breakLine: true } },
      { text: "HERE", options: {} },
    ],
    {
      x: px(184), y: px(130), w: px(64), h: px(64),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 12, bold: true, color: C.white, lineSpacing: 14,
    }
  );
}

// ---- CENTER panel: Multi-Head Attention (paper Fig 2 right, course style) --------

function drawCenterPanel(slide) {
  // red italic title above the border (measured glyphs y216-232)
  slide.addText("Multi-Head Attention", {
    x: px(294), y: px(208), w: px(200), h: px(26),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 14, bold: true, italic: true, color: C.red,
  });
  // white panel with green border + corner handles
  slide.addShape("rect", {
    x: px(300), y: px(246), w: px(208), h: px(270),
    fill: { color: C.white }, line: { color: C.frameGreen, width: 2.25 },
  });
  cornerHandle(slide, 300, 246);
  cornerHandle(slide, 508, 246);
  cornerHandle(slide, 300, 516);
  cornerHandle(slide, 508, 516);
  // top Linear with gray shadow copy (offset up-right)
  slide.addShape("rect", {
    x: px(372), y: px(259), w: px(47), h: px(23),
    fill: { color: C.shadowFill }, line: { color: C.shadowBorder, width: 0.75 },
  });
  flowBox(slide, 364, 266, 47, 23, C.linearFill, C.linearBorder, 0.75, ["Linear"], 8, 10, "333333");
  addLines(slide, C.ink, 0.75, [[387, 265], [387, 251]], { endArrow: true });
  // Concat
  flowBox(slide, 364, 312, 46, 14, C.concatFill, C.olive, 0.5, ["Concat"], 7.5, 9);
  addLines(slide, C.ink, 0.75, [[387, 311], [387, 291]], { endArrow: true });
  addLines(slide, "8A8A8A", 0.75, [[379, 311], [379, 292]], { endArrow: true });
  addLines(slide, "8A8A8A", 0.75, [[395, 311], [395, 292]], { endArrow: true });
  // SDPA stack: gray offset copy behind, red rectangle, mauve front box
  slide.addShape("rect", {
    x: px(317), y: px(343), w: px(161), h: px(32),
    fill: { color: C.shadowFill }, line: { color: C.shadowBorder, width: 0.75 },
  });
  slide.addShape("rect", {
    x: px(301), y: px(352), w: px(177), h: px(44),
    fill: { type: "none" }, line: { color: C.red, width: 1.5 },
  });
  flowBox(slide, 307, 354, 166, 40, C.mauve, 0, C.mauve,
    ["Scaled Dot-Product", "Attention"], 8, 11, C.mauveText);
  // three parallel Linear boxes with shadows
  const LX = [[309, 42], [359, 48], [416, 48]];
  for (const [bx, bw] of LX) {
    slide.addShape("rect", {
      x: px(bx + 7), y: px(397), w: px(bw), h: px(18),
      fill: { color: C.shadowFill }, line: { color: C.shadowBorder, width: 0.75 },
    });
    flowBox(slide, bx, 403, bw, 18, C.linearFill, C.linearBorder, 0.75, ["Linear"], 7.5, 9, "333333");
    addLines(slide, C.ink, 0.75, [[bx + bw / 2, 402], [bx + bw / 2, 396]], { endArrow: true });
    addLines(slide, "8A8A8A", 0.75, [[bx + bw / 2 - 6, 402], [bx + bw / 2 - 6, 397]], { endArrow: true });
    addLines(slide, "8A8A8A", 0.75, [[bx + bw / 2 + 6, 402], [bx + bw / 2 + 6, 397]], { endArrow: true });
  }
  // circles (bottom, straddling the lower border) — lowercase q verbatim
  letterCircle(slide, 331, 499, 19, C.circBlue, "V", 8.5);
  letterCircle(slide, 387, 499, 19, C.circBlue, "K", 8.5);
  letterCircle(slide, 444, 499, 18, C.circRed, "q", 8.5);
  // arrows circles -> Linear boxes
  addLines(slide, C.ink, 0.75, [[331, 489], [331, 423]], { endArrow: true });
  addLines(slide, C.ink, 0.75, [[387, 489], [387, 423]], { endArrow: true });
  addLines(slide, C.ink, 0.75, [[444, 489], [444, 423]], { endArrow: true });
  // SDPA stack up into Concat
  addLines(slide, C.ink, 0.75, [[387, 351], [387, 328]], { endArrow: true });
  // "h" annotation: ghost circle + tan circle right of the stack
  slide.addShape("ellipse", {
    x: px(491), y: px(361), w: px(17), h: px(17),
    fill: { type: "none" }, line: { color: "A6A6A6", width: 0.75 },
  });
  addLines(slide, C.ink, 0.75, [[477, 386], [481, 376]]);
  slide.addShape("ellipse", {
    x: px(484), y: px(357), w: px(17), h: px(17),
    fill: { color: "D4BCA0" }, line: { color: "8A6A48", width: 1 },
  });
  slide.addText("h", {
    x: px(484), y: px(357), w: px(17), h: px(17),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, italic: true, color: C.ink,
  });
}


// ---- RIGHT panel: full Transformer architecture (paper Fig 1, course style) -------
// Attempt-5 model (attempt-4 crop-compare fixes, bitmap-verified against the frame):
//   enc container x629-727 y267-412 wraps A&N/FF/A&N + red MHA + V/K/Q;
//   dec gray-sage container x744-840 y202-412 wraps steel-blue A&N + dark FF +
//   steel-blue A&N + red MHA + cross V/K/Q + INDIGO Add&Norm y330-342 (fill
//   6982DE) + violet Masked-MHA y344-408 (one rule y384.5, masked V/K/Q inside);
//   YELLOW highlight = three measured zones: top band y250-266 x678-790 (sage
//   covers x744+), right strip x729-743 y250-322, bottom sliver x746-790 y311-322
//   drawn after the sage rect so it shows between the cross-attention circles;
//   decoder top: yellow band y111-128 x761-813 holds ONE word 'Output',
//   'Probabilities' below the band, thin connectors x785, Softmax y152-165,
//   Linear y178-191 (container-green fills, dark-green border + text);
//   PE + (Input|Output) Embedding = ONE container per side, divider at y446;
//   lime routing enc bar y276-407 + band y398-407 UNDER the V/K/Q circles;
//   dec bar x828-838 y207-407 + legs; 'Nx' badges; red dashed arc measured span
//   y219-484, arrowhead at the BOTTOM end.

function drawRightPanel(slide) {
  // green frame around the whole architecture
  slide.addShape("rect", {
    x: px(572), y: px(104), w: px(323), h: px(421),
    fill: { type: "none" }, line: { color: C.archFrame, width: 1.5 },
  });
  // containers
  slide.addShape("rect", {
    x: px(576), y: px(108), w: px(159), h: px(413), fill: { color: C.encFill },
  });
  slide.addShape("rect", {
    x: px(736), y: px(108), w: px(157), h: px(413), fill: { color: C.decFill },
  });
  // ---- YELLOW highlight: three measured zones (gate+bitmap-verified) —
  // (A) top band y250-266 x678-790 over the peach, covered by the sage container
  // from x744 (visible x678-743 exactly as the frame shows); (C) right strip
  // x729-743 y250-322 between the containers; (B) bottom sliver x746-790 y311-322
  // inside the sage container below the MHA (drawn later, after the sage rect)
  slide.addShape("rect", {
    x: px(678), y: px(250), w: px(112), h: px(17), fill: { color: C.yellow },
  });
  slide.addShape("rect", {
    x: px(729), y: px(250), w: px(15), h: px(72), fill: { color: C.yellow },
  });
  // container labels
  slide.addText("Encoder", {
    x: px(582), y: px(112), w: px(84), h: px(20),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 13, bold: true, italic: true, color: C.red,
  });
  slide.addText("Decoder", {
    x: px(800), y: px(112), w: px(86), h: px(20),
    align: "right", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 13, bold: true, italic: true, color: C.decGreenText,
  });

  // ---- ENCODER stack: tan container x629-727 y267-412 wrapping everything ----
  slide.addShape("roundRect", {
    x: px(629), y: px(267), w: px(98), h: px(145), rectRadius: 0.04,
    fill: { color: C.stackTan }, line: { color: C.stackBorder, width: 1.25 },
  });
  // inset sub-layer boxes (measured: steel-blue A&N plates, dark FF)
  flowBox(slide, 652, 278, 64, 10, C.anSteel, C.stackBorder, 0.5, ["Add & Norm"], 7, 8.5, C.anText);
  flowBox(slide, 652, 290, 64, 26, "5E5E5E", C.stackBorder, 0.5,
    ["Feed", "Forward"], 9, 10.5, "E0E0E0");
  flowBox(slide, 652, 342, 64, 11, C.anSteel, C.stackBorder, 0.5, ["Add & Norm"], 7, 8.5, C.anText);
  // red-outlined Multi-Head Attention (inside the container, measured y354-389)
  slide.addShape("roundRect", {
    x: px(648), y: px(354), w: px(74), h: px(35), rectRadius: 0.04,
    fill: { color: C.mhaFill }, line: { color: C.red, width: 2 },
  });
  slide.addText(
    [
      { text: "Multi-Head", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(648), y: px(354), w: px(74), h: px(35),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9, bold: true, color: C.mhaText, lineSpacing: 10.5,
    }
  );
  // lime band behind the V/K circle row (measured y398-407, x641-687) — drawn
  // BEFORE the circles so they sit on it (an after-the-fact draw buried the V glyph)
  slide.addShape("rect", {
    x: px(641), y: px(398), w: px(46), h: px(9), fill: { color: C.residGreen },
  });
  // V/K/Q beneath (inside the container, on top of the lime band)
  letterCircle(slide, 663, 401.5, 15, C.vGreen, "V", 8);
  letterCircle(slide, 692, 401.5, 14, C.kBlue, "K", 8);
  letterCircle(slide, 711, 401.5, 14, C.qRed, "Q", 8);
  // yellow-green residual routing: vertical bar + horizontal tap leg (measured:
  // bar x633-641 y276-407, tap leg y324-333)
  slide.addShape("rect", {
    x: px(634), y: px(276), w: px(11), h: px(131), fill: { color: C.residGreen },
  });
  slide.addShape("rect", {
    x: px(634), y: px(324), w: px(50), h: px(9), fill: { color: C.residGreen },
  });
  // vertical connector arrowheads in the stack gaps
  spineHead(slide, 686, 288.5);
  spineHead(slide, 686, 317.5);
  spineHead(slide, 686, 341.5);
  spineHead(slide, 686, 352.5);
  spineHead(slide, 686, 390);
  spineHead(slide, 686, 412);
  // PE node + Input Embedding: ONE continuous brown container (measured: no dark
  // top/bottom borders — only an internal full-width divider at y445-447, x654-720)
  slide.addShape("roundRect", {
    x: px(650), y: px(417), w: px(72), h: px(69), rectRadius: 0.05,
    fill: { color: C.embedBrown }, line: { color: "6E4423", width: 1 },
  });
  slide.addShape("ellipse", {
    x: px(654), y: px(421.5), w: px(17), h: px(17),
    fill: { type: "none" }, line: { color: "3A2410", width: 1.25 },
  });
  addLines(slide, "3A2410", 1.25, [[658.5, 430], [666.5, 430]]);
  addLines(slide, "3A2410", 1.25, [[662.5, 426], [662.5, 434]]);
  // smooth sine glyph (12-segment approximation)
  for (let i = 0; i < 12; i++) {
    const x0 = 678 + i * 3.2, x1 = 678 + (i + 1) * 3.2;
    const y0 = 430.5 - 5.5 * Math.sin(i / 12 * 2 * Math.PI);
    const y1 = 430.5 - 5.5 * Math.sin((i + 1) / 12 * 2 * Math.PI);
    addLines(slide, "3A2410", 1, [[x0, y0], [x1, y1]]);
  }
  // internal divider between the symbol half and the label half (measured y446)
  addLines(slide, "6E4423", 1, [[654, 446], [720, 446]]);
  slide.addText(
    [
      { text: "Positional", options: { breakLine: true } },
      { text: "Encoding", options: {} },
    ],
    {
      x: px(575), y: px(414), w: px(58), h: px(28),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9, bold: true, color: C.grayLabel, lineSpacing: 11,
    }
  );
  slide.addShape("ellipse", {
    x: px(598), y: px(329), w: px(26), h: px(26),
    fill: { color: C.nxTan }, line: { color: C.nxBorder, width: 0.75 },
  });
  slide.addText("Nx", {
    x: px(598), y: px(329), w: px(26), h: px(26),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 8, bold: true, color: "333333",
  });
  // 'Input Embedding' label sits in the container's lower half (below the divider)
  slide.addText(
    [
      { text: "Input", options: { breakLine: true } },
      { text: "Embedding", options: {} },
    ],
    {
      x: px(650), y: px(447), w: px(72), h: px(37),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 8.5, bold: true, color: C.embedText, lineSpacing: 10,
    }
  );
  // Inputs red block up-arrow
  slide.addShape("rect", {
    x: px(634), y: px(494), w: px(10), h: px(18),
    fill: { color: C.arrowRed }, line: { color: C.arrowRed, width: 0.5 },
  });
  slide.addShape("triangle", {
    x: px(630), y: px(486), w: px(18), h: px(9),
    fill: { color: C.arrowRed }, line: { color: C.arrowRed, width: 0.5 },
  });
  slide.addText("Inputs", {
    x: px(654), y: px(496), w: px(46), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: "4A2E14",
  });

  // ---- DECODER: gray-sage container y204-412 wrapping the whole stack ----
  slide.addShape("roundRect", {
    x: px(744), y: px(204), w: px(96), h: px(208), rectRadius: 0.04,
    fill: { color: "A8B492" }, line: { color: "47684A", width: 1.25 },
  });
  // yellow highlight zone B: bottom sliver inside the sage container, below the
  // MHA, showing between/around the cross-attention circles (measured y311-322)
  slide.addShape("rect", {
    x: px(746), y: px(311), w: px(45), h: px(12), fill: { color: C.yellow },
  });
  // steel-blue Add & Norm plates + dark-gray Feed Forward (inset, measured)
  flowBox(slide, 748, 206, 69, 13, C.anSteel, C.stackBorder, 0.5, ["Add & Norm"], 8, 9.5, C.anText);
  flowBox(slide, 748, 221, 69, 28, "5E5E5E", C.stackBorder, 0.5,
    ["Feed", "Forward"], 9, 10.5, "E0E0E0");
  flowBox(slide, 748, 251, 69, 23, C.anSteel, C.stackBorder, 0.5, ["Add & Norm"], 8, 9.5, C.anText);
  // decoder Multi-Head Attention (red-outlined, measured x747-821 y276-310)
  slide.addShape("roundRect", {
    x: px(747), y: px(276), w: px(74), h: px(34), rectRadius: 0.04,
    fill: { color: C.mhaFillDec }, line: { color: C.red, width: 2 },
  });
  slide.addText(
    [
      { text: "Multi-Head", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(747), y: px(276), w: px(74), h: px(34),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 8.5, bold: true, color: C.mhaText, lineSpacing: 10,
    }
  );
  // cross-attention V/K/Q (blue/blue/red, straddling below the MHA box)
  letterCircle(slide, 749, 317, 11, C.kBlue, "V", 7);
  letterCircle(slide, 773, 317, 11, C.kBlue, "K", 7);
  letterCircle(slide, 820, 317, 11, C.qRed, "Q", 7);
  // indigo Add & Norm box between the cross-attention circles and the violet box
  // (measured: full-width indigo y330-342, x751-818, fill ~(105,130,222); tiny
  // dark connector mark at x785-787 y324 above it)
  spineHead(slide, 785, 324);
  flowBox(slide, 751, 330, 67, 13, "6982DE", C.stackBorder, 0.5, ["Add & Norm"], 6.5, 8, C.anText);
  // violet Masked Multi-Head Attention container y344-408 (measured) with ONE
  // internal rule at y384.5 above the masked V/K/Q band
  slide.addShape("roundRect", {
    x: px(746), y: px(344), w: px(84), h: px(64), rectRadius: 0.05,
    fill: { color: C.purpleBox }, line: { color: C.purpleBorder, width: 1 },
  });
  addLines(slide, C.purpleBorder, 0.75, [[748, 384.5], [828, 384.5]]);
  slide.addText(
    [
      { text: "Masked", options: { breakLine: true } },
      { text: "Multi-Head", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(748), y: px(347), w: px(80), h: px(36),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 8.5, bold: true, color: C.purpleText, lineSpacing: 10,
    }
  );
  // lime band over the purple box's lower-right, under the masked circles
  // (measured y396-407, x788-833)
  slide.addShape("rect", {
    x: px(788), y: px(396), w: px(45), h: px(11), fill: { color: C.residGreen },
  });
  // masked V/K/Q circles (blue/blue/red, straddling the container's lower band)
  letterCircle(slide, 760, 397, 13, C.kBlue, "V", 7.5);
  letterCircle(slide, 796, 397, 13, C.kBlue, "K", 7.5);
  letterCircle(slide, 812, 397, 12, C.qRed, "Q", 7.5);
  // yellow-green residual routing on the container's right + tap legs (measured:
  // bar x828-838 y207-407, legs y251-261 and y318-327, band y396-407 over the
  // purple box's lower-right)
  slide.addShape("rect", {
    x: px(828), y: px(207), w: px(10), h: px(200), fill: { color: C.residGreen },
  });
  slide.addShape("rect", {
    x: px(790), y: px(251), w: px(48), h: px(10), fill: { color: C.residGreen },
  });
  slide.addShape("rect", {
    x: px(790), y: px(318), w: px(48), h: px(9), fill: { color: C.residGreen },
  });
  // vertical connector arrowheads in the decoder stack gaps (thin lines + small
  // heads in the top gaps, measured x785: y141-151, y166-177, y192-199)
  thinConn(slide, 785, 141, 151);
  thinConn(slide, 785, 166, 177);
  thinConn(slide, 785, 192, 199);
  spineHead(slide, 785, 220);
  spineHead(slide, 785, 250);
  spineHead(slide, 785, 275);
  spineHead(slide, 785, 412);
  // decoder PE node + Output Embedding: ONE continuous maroon container
  // (measured: internal full-width divider at y445-447, x752-818; no outer gaps)
  slide.addShape("roundRect", {
    x: px(750), y: px(417), w: px(74), h: px(69), rectRadius: 0.05,
    fill: { color: C.embedMaroon }, line: { color: "5A2A24", width: 1 },
  });
  slide.addShape("ellipse", {
    x: px(754), y: px(421.5), w: px(17), h: px(17),
    fill: { type: "none" }, line: { color: "3A1810", width: 1.25 },
  });
  addLines(slide, "3A1810", 1.25, [[758, 430], [766, 430]]);
  addLines(slide, "3A1810", 1.25, [[762, 426], [762, 434]]);
  for (let i = 0; i < 12; i++) {
    const x0 = 778 + i * 3.0, x1 = 778 + (i + 1) * 3.0;
    const y0 = 430.5 - 5.0 * Math.sin(i / 12 * 2 * Math.PI);
    const y1 = 430.5 - 5.0 * Math.sin((i + 1) / 12 * 2 * Math.PI);
    addLines(slide, "3A1810", 1, [[x0, y0], [x1, y1]]);
  }
  addLines(slide, "5A2A24", 1, [[754, 446], [822, 446]]);
  slide.addText(
    [
      { text: "Positional", options: { breakLine: true } },
      { text: "Encoding", options: {} },
    ],
    {
      x: px(834), y: px(414), w: px(56), h: px(28),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9, bold: true, color: C.grayLabel, lineSpacing: 11,
    }
  );
  slide.addShape("ellipse", {
    x: px(845), y: px(300), w: px(24), h: px(24),
    fill: { color: C.nxOlive }, line: { color: "6A7A4A", width: 0.75 },
  });
  slide.addText("Nx", {
    x: px(845), y: px(300), w: px(24), h: px(24),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 7.5, bold: true, color: "333333",
  });
  // 'Output Embedding' label in the container's lower half (below the divider)
  slide.addText(
    [
      { text: "Output", options: { breakLine: true } },
      { text: "Embedding", options: {} },
    ],
    {
      x: px(750), y: px(447), w: px(74), h: px(37),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 8.5, bold: true, color: C.embedText, lineSpacing: 10,
    }
  );
  // Output Probabilities: red up-arrow + yellow band with ONE word 'Output';
  // 'Probabilities' sits BELOW the band on the pale green (measured + gate-verified)
  slide.addShape("rect", {
    x: px(743), y: px(121), w: px(5), h: px(17),
    fill: { color: C.red }, line: { color: C.red, width: 0.5 },
  });
  slide.addShape("triangle", {
    x: px(739), y: px(112), w: px(13), h: px(9),
    fill: { color: C.red }, line: { color: C.red, width: 0.5 },
  });
  slide.addShape("rect", {
    x: px(761), y: px(111), w: px(52), h: px(18), fill: { color: C.yellow },
  });
  slide.addText("Output", {
    x: px(761), y: px(111), w: px(52), h: px(18),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 7, bold: true, color: C.ink,
  });
  slide.addText("Probabilities", {
    x: px(747), y: px(128), w: px(74), h: px(13),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 7, bold: true, color: C.ink,
  });
  // Softmax (y152-165) / Linear (y178-191) boxes — measured borders + text rows;
  // container-green fills, dark-green borders + text
  flowBox(slide, 752, 152, 69, 14, C.softmaxFill, C.softmaxBorder, 0.75, ["Softmax"], 6.5, 8, C.softmaxText);
  flowBox(slide, 752, 178, 69, 13, C.linearDecFill, C.softmaxBorder, 0.75, ["Linear"], 6.5, 8, C.softmaxText);
  // Outputs (shifted right): yellow band + green text (yellow measured to y509)
  slide.addShape("rect", {
    x: px(762), y: px(493), w: px(48), h: px(17), fill: { color: C.yellow },
  });
  slide.addText("Outputs", {
    x: px(762), y: px(493), w: px(48), h: px(17),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: C.ink,
  });
  slide.addText("(shifted right)", {
    x: px(748), y: px(509), w: px(76), h: px(13),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 8.5, bold: true, color: "3C8C3C",
  });

  // ---- red dashed zoom lines + arc ----
  // left panel brackets -> center panel left edge (converging)
  addLines(slide, C.red, 1, [[207, 287], [250, 334], [296, 378]], { dash: "dash" });
  addLines(slide, C.red, 1, [[207, 472], [252, 430], [296, 390]], { dash: "dash" });
  // center panel corners -> the two red-outlined MHA boxes
  addLines(slide, C.red, 1, [[509, 254], [570, 302], [646, 360]], { dash: "dash" });
  addLines(slide, C.red, 1, [[509, 514], [630, 396], [745, 280]], { dash: "dash" });
  // red dashed arc: measured dashes (881,219),(884,237),(889,321),(887,363),
  // (846,483) — starts below the Decoder label, arrowhead at the BOTTOM near
  // "Outputs" (the previous y140 start has no counterpart in the original)
  addLines(slide, C.red, 1.25, [
    [880, 219], [888, 270], [890, 320], [887, 368], [877, 420],
    [860, 458], [846, 484],
  ], { dash: "dash", endArrow: true });
}
// ---- composition -----------------------------------------------------------------

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in — house chrome canvas
pptx.author = "slide-recreation worker";
pptx.title = "Encoder – Decoder Transformer (slide 25 recreation)";

const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: 25 });
drawTitle(slide);
drawLeftPanel(slide);
drawBubble(slide);
drawCenterPanel(slide);
drawRightPanel(slide);

const OUT = path.join(__dirname, "..", "slide_025_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch((e) => {
  console.error("BUILD FAILED:", e);
  process.exit(1);
});
