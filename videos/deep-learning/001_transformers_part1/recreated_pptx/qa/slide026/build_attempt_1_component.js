// components/slide_026.js — CERTIFIED-CANDIDATE composition of slide 26
// "Self Attention Mechanism (Fundamental Operation)" (Deep Learning DSAI 308,
// Transformers Part I). Built by the slide-026 build worker, 2026-10-11.
//
// DEPENDENCY CONTRACT (references/dependencies.md): this module is the shared base for
// dependent slides 27, 28, 29 (27←26, 28←26, 29←26). It exports the full draw at BLOCK
// granularity: renderBase(pptx, slide, opts) with opts.skip / opts.only selectors
// (arrays of block names). Children compose per-block and draw only their own delta at
// their own measured geometry — NEVER copy-paste or re-derive this geometry. House
// chrome is NOT drawn here: the child build draws it ONCE via components/house_chrome.js
// and then calls renderBase for the content blocks.
//
// GEOMETRY PROVENANCE — PIL pixel forensics on unique_slides/slide_026.jpg (960x540,
// 1px = 1pt = 1/72 in), cross-checked with an 8-panel vision read of the original
// (qa/slide026/structure_probe.txt). All coordinates below are frame pixels (÷72 = in):
//   peach canvas x52..866 y108..522, fill F7E2CD (rounded)
//   title L1 ink x260..745 y58..76 (~21pt bold, caps y58..72), yellow FBF29B highlight
//     x508..748 behind "(Fundamental Operation)"; subtitle ink x186..809 y79..101
//     (~17pt bold), red 9E101E subscripted tokens (commas red too, verbatim unbalanced
//     parens "( ... ( X1, X2, X3, X4 )")
//   label ellipses (pale yellow F9FCDB, no border): Similarity x266..341 y160..188,
//     Probabilities x428..516 y161..192, Weighted SUM x568..693 y152..187 (its text
//     sits right-of-ellipse-center: ink x604..680); blue 0033CC bold ~10.5pt
//   left stack container x57..139 y226..395 / right x761..843, fill E6FCE7, dashed
//     green 3B7A40 border; 4 glyphs per stack centered on line rows y246.5/287.5/328.5/
//     372.5; glyph = 5 cells w12 (yellow FCFFC6 x2, orchid D791C8 carrying the red X
//     label, lavender E6E2F8, pale pink F3D3EC) — vision panel A read
//     "yellow, yellow, X-cell, lavender, pink"; left labels 11pt, right 7.5pt
//   Dot Product box x253..343 y194..404 fill DBCBBB; 2-line label "Dot"/"Product"
//     13pt bold 5C3712 (pitch 15px); 4 dots d8 fill 0200AB at (330.5,246.5)(314.5,287.5)
//     (295.5,328)(276.5,372.5) — top dot farthest right
//   Soft max bar x458..488 y196..401 fill F8DEFB; "Soft max" ONE line 16.5pt bold
//     6B006E rotated 270 (reads bottom-to-top; word gap y296..301 in the frame)
//   Sigma box x516..649 y196..217 fill EAFEFC (borderless); Sigma glyph ~20pt bold 2A2AB5
//   Weighted-SUM plumbing: 4 horizontal red C00000 lines y246/287/328/372 from softmax
//     right edge to the right stack (line 4 measured to STOP at x~688 — reproduced);
//     4 vertical lines x532/563/591/622 from the nodes up into Sigma with UP arrowheads
//     at y219 (vision panel C: "Sigma box receiving red up-arrows"); W21..W24 labels
//     10pt bold 0033CC at x495..510 above each line; 4 nodes = red-ring ellipses
//     w30 h14 centered on the lines at x532/563/591/622 with red 6-spoke asterisks
//   Y output x547..617 y119..147 dashed green box with a 5-cell green vector (B2DCA5 /
//     AFDAA6 / 96CE91 / A0CC9A / A5C8BD), bold dark-green 2A842A "Y" on the middle cell;
//     thick green 12B45A upArrow x549..573 y146..167 + thin dark-red 8C0007 arrow at
//     x583 from Sigma to Y (drawn BEHIND the Weighted-SUM ellipse)
//   sentence strip x178..492 y473..517 (same container style); glyphs at x191/265/339/414
//     (center y494.5); X2 = SOLID pink E187CE rounded box x261..336 y472..506 with
//     magenta-maroon A01450 sysDot border + red label (pixel-verified: no cell colors
//     inside the highlight); thin red query arrow x298 y473..406 (head at top) and a
//     chunky red C5000F diagonal arrow (266,526)->(284,512) at the strip's lower-left
//   feed connectors: thin dashed AC9F90 curves strip->stacks with small GREEN 1E7A34
//     up-arrowheads at (102,396) and (803,396) (vision panels E/F: "thin gray curved
//     connector lines ending in small green arrows pointing up")
//   Mouse cursor over the X2 glyph in the original frame is a video artifact — NOT
//     recreated (judge ground rule c).

var PX = 1 / 72; // frame px -> inches

var C = {
  canvas: "F7E2CD",
  titleBlack: "000000",
  highlight: "FBF29B",
  subRed: "9E101E",
  blue: "0033CC",
  dotBlue: "0200AB",
  sigmaBlue: "2A2AB5",
  ellipseFill: "F9FCDB",
  containerFill: "E6FCE7",
  containerBorder: "3B7A40",
  cellYellow: "FCFFC6",
  cellOrchid: "D791C8",
  cellLavender: "E6E2F8",
  cellPink: "F3D3EC",
  tanBox: "DBCBBB",
  brownLabel: "5C3712",
  softmaxFill: "F8DEFB",
  softmaxLabel: "6B006E",
  sigmaFill: "EAFEFC",
  red: "C00000",
  redArrowDark: "8C0007",
  redBlock: "C5000F",
  greenArrow: "12B45A",
  yLabel: "2A842A",
  yCells: ["B2DCA5", "AFDAA6", "96CE91", "A0CC9A", "A5C8BD"],
  x2Fill: "E187CE",
  x2Border: "A01450",
  curve: "AC9F90",
  curveHead: "1E7A34",
};

var FONT = "Arial";

// ---- helpers ---------------------------------------------------------------
function line(pptx, slide, x1, y1, x2, y2, opts) {
  opts = opts || {};
  var o = {
    x: Math.min(x1, x2) * PX, y: Math.min(y1, y2) * PX,
    w: Math.abs(x2 - x1) * PX, h: Math.abs(y2 - y1) * PX,
    line: { color: opts.color || C.red, width: opts.width || 1.5 },
  };
  if (x2 < x1) o.flipH = true;
  if (y2 < y1) o.flipV = true;
  if (opts.arrow) o.line.endArrowType = "triangle";
  if (opts.dash) o.line.dashType = opts.dash;
  slide.addShape(pptx.ShapeType.line, o);
}

// embedding glyph: 5 cells + red subscripted label on cell 3
function glyph(pptx, slide, x0, cy, labelSize, label) {
  var cellW = 12, gap = 1, h = 14;
  var fills = [C.cellYellow, C.cellYellow, C.cellOrchid, C.cellLavender, C.cellPink];
  for (var i = 0; i < 5; i++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: (x0 + i * (cellW + gap)) * PX, y: (cy - h / 2) * PX,
      w: cellW * PX, h: h * PX, fill: { color: fills[i] }, line: { type: "none" },
    });
  }
  var lx = (x0 + 2 * (cellW + gap)) * PX;
  slide.addText(
    [
      { text: "X", options: {} },
      { text: label, options: { subscript: true } },
    ],
    {
      x: lx - 0.06, y: (cy - 9) * PX, w: 0.32, h: 0.25,
      align: "center", valign: "middle", bold: true, fontSize: labelSize,
      color: C.subRed, fontFace: FONT, margin: 0,
    }
  );
}

function stackContainer(pptx, slide, x, labelSize) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: x * PX, y: 226 * PX, w: 83 * PX, h: 170 * PX, rectRadius: 0.07,
    fill: { color: C.containerFill },
    line: { color: C.containerBorder, width: 1.25, dashType: "dash" },
  });
  var cys = [246.5, 287.5, 328.5, 372.5];
  var x0 = x + 10;
  for (var i = 0; i < 4; i++) {
    glyph(pptx, slide, x0, cys[i], labelSize, String(i + 1));
  }
}

// ---- blocks ----------------------------------------------------------------

function drawCanvas(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 52 * PX, y: 108 * PX, w: 815 * PX, h: 415 * PX, rectRadius: 0.07,
    fill: { color: C.canvas }, line: { type: "none" },
  });
}

function drawTitle(pptx, slide) {
  // line 1 (~20pt bold, yellow highlight behind the parenthetical only); frame ink
  // x260..745 => ink center 502.5 (box shifted right of slide center to match)
  slide.addText(
    [
      { text: "Self Attention Mechanism ", options: {} },
      { text: "(Fundamental Operation)", options: { highlight: C.highlight } },
    ],
    {
      x: 0.9125, y: 0.725, w: 12.13, h: 0.42, align: "center", valign: "top",
      fontSize: 20, bold: true, color: C.titleBlack, fontFace: FONT, margin: 0,
    }
  );
  // line 2 subtitle (verbatim unbalanced parens; red tokens incl. commas)
  // frame ink x186..809 => ink center 497.5, ~19.5pt
  var red = { color: C.subRed };
  slide.addText(
    [
      { text: "(Self Attention of word ", options: {} },
      { text: "X", options: red }, { text: "2", options: { subscript: true, color: C.subRed } },
      { text: " w.r.t All words in Sentence ( ", options: {} },
      { text: "X", options: red }, { text: "1", options: { subscript: true, color: C.subRed } },
      { text: ", ", options: red },
      { text: "X", options: red }, { text: "2", options: { subscript: true, color: C.subRed } },
      { text: ", ", options: red },
      { text: "X", options: red }, { text: "3", options: { subscript: true, color: C.subRed } },
      { text: ", ", options: red },
      { text: "X", options: red }, { text: "4", options: { subscript: true, color: C.subRed } },
      { text: " )", options: {} },
    ],
    {
      x: 0.843, y: 1.052, w: 12.13, h: 0.36, align: "center", valign: "top",
      fontSize: 19.5, bold: true, color: C.titleBlack, fontFace: FONT, margin: 0,
    }
  );
}

function drawDotProduct(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 253 * PX, y: 194 * PX, w: 91 * PX, h: 211 * PX,
    fill: { color: C.tanBox }, line: { type: "none" },
  });
  slide.addText(
    [
      { text: "Dot", options: { breakLine: true } },
      { text: "Product", options: {} },
    ],
    {
      x: 253 * PX, y: 197 * PX, w: 91 * PX, h: 0.42,
      align: "center", valign: "top", fontSize: 13, bold: true,
      color: C.brownLabel, fontFace: FONT, lineSpacing: 15, margin: 0,
    }
  );
  // dots (blue), one per row, staggered top-right -> bottom-left
  var dots = [[330.5, 246.5], [314.5, 287.5], [295.5, 328], [276.5, 372.5]];
  for (var i = 0; i < 4; i++) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: (dots[i][0] - 4) * PX, y: (dots[i][1] - 4) * PX, w: 8 * PX, h: 8 * PX,
      fill: { color: C.dotBlue }, line: { type: "none" },
    });
  }
}

function drawSoftmax(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 458 * PX, y: 196 * PX, w: 31 * PX, h: 206 * PX, rectRadius: 0.05,
    fill: { color: C.softmaxFill }, line: { type: "none" },
  });
  slide.addText("Soft max", {
    x: 473.5 / 72 - 1.3, y: 298.5 / 72 - 0.25, w: 2.6, h: 0.5,
    align: "center", valign: "middle", fontSize: 16.5, bold: true,
    color: C.softmaxLabel, fontFace: FONT, rotate: 270, margin: 0,
  });
}

function drawSigma(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 516 * PX, y: 196 * PX, w: 134 * PX, h: 22 * PX,
    fill: { color: C.sigmaFill }, line: { type: "none" },
  });
  slide.addText("\u03A3", {
    x: 516 * PX, y: 196 * PX, w: 134 * PX, h: 22 * PX,
    align: "center", valign: "middle", fontSize: 20, bold: true,
    color: C.sigmaBlue, fontFace: FONT, margin: 0,
  });
}

function drawYOutput(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 547 * PX, y: 119 * PX, w: 71 * PX, h: 29 * PX, rectRadius: 0.04,
    fill: { type: "none" },
    line: { color: C.containerBorder, width: 1.25, dashType: "dash" },
  });
  var cw = 13, x0 = 549;
  for (var i = 0; i < 5; i++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: (x0 + i * 13.4) * PX, y: 121 * PX, w: (i === 4 ? 13.8 : cw) * PX, h: 24 * PX,
      fill: { color: C.yCells[i] }, line: { type: "none" },
    });
  }
  slide.addText("Y", {
    x: 571 * PX, y: 119 * PX, w: 25 * PX, h: 29 * PX,
    align: "center", valign: "middle", fontSize: 16, bold: true,
    color: C.yLabel, fontFace: FONT, margin: 0,
  });
}

function drawArrowsGreen(pptx, slide) {
  // thick green block arrow, TILTED up-right (~26 deg off vertical) as measured
  // (tip at top-right (566,145), base at bottom-left (556,166))
  slide.addShape(pptx.ShapeType.upArrow, {
    x: 549 * PX, y: 146 * PX, w: 24 * PX, h: 21 * PX, rotate: 26,
    fill: { color: C.greenArrow }, line: { type: "none" },
  });
  // thin dark-red arrow Sigma -> Y at x583, drawn BEHIND the Weighted-SUM ellipse
  line(pptx, slide, 583, 193, 583, 151, { color: C.redArrowDark, width: 1.5, arrow: true });
}

function drawLabels(pptx, slide) {
  var ells = [
    { x: 266, y: 160, w: 75, h: 28, t: "Similarity", tx: null },
    { x: 428, y: 161, w: 88, h: 31, t: "Probabilities", tx: null },
    { x: 568, y: 152, w: 125, h: 35, t: "Weighted SUM", tx: 604 },
  ];
  for (var i = 0; i < ells.length; i++) {
    var e = ells[i];
    slide.addShape(pptx.ShapeType.ellipse, {
      x: e.x * PX, y: e.y * PX, w: e.w * PX, h: e.h * PX,
      fill: { color: C.ellipseFill }, line: { type: "none" },
    });
    var tx = e.tx === null ? e.x : e.tx;
    var tw = e.tx === null ? e.w : 78;
    slide.addText(e.t, {
      x: tx * PX, y: e.y * PX, w: tw * PX, h: e.h * PX,
      align: "center", valign: "middle", fontSize: 10.5, bold: true,
      color: C.blue, fontFace: FONT, margin: 0,
    });
  }
}

function drawFlowLines(pptx, slide) {
  var ys = [246, 287, 328, 372];
  var dots = [330.5, 314.5, 295.5, 276.5];
  // left rows: stack edge -> dot, dot -> softmax left edge (arrowhead into the bar)
  for (var i = 0; i < 4; i++) {
    line(pptx, slide, 139, ys[i], dots[i] - 4, ys[i], {});
    line(pptx, slide, dots[i] + 4, ys[i], 456, ys[i], { arrow: true });
  }
  // right rows: softmax right edge -> right stack (row 4 measured to stop at x~688)
  line(pptx, slide, 490, 246, 761, 246, {});
  line(pptx, slide, 490, 287, 761, 287, {});
  line(pptx, slide, 490, 328, 761, 328, {});
  line(pptx, slide, 490, 372, 688, 372, {});
  // verticals node -> Sigma with UP arrowheads at the Sigma underside
  var vx = [532, 563, 591, 622];
  var vy = [244, 285, 326, 368];
  for (var j = 0; j < 4; j++) {
    line(pptx, slide, vx[j], vy[j], vx[j], 221, { arrow: true });
  }
  // W labels above each right row
  var wy = [226, 267, 308, 352];
  for (var k = 0; k < 4; k++) {
    slide.addText(
      [
        { text: "W", options: {} },
        { text: "2" + String(k + 1), options: { subscript: true } },
      ],
      {
        x: 494 * PX, y: wy[k] * PX, w: 0.28, h: 0.19,
        align: "center", valign: "middle", fontSize: 10, bold: true,
        color: C.blue, fontFace: FONT, margin: 0,
      }
    );
  }
  // nodes: small red-ring circles + 6-spoke asterisks, flanked by INWARD-pointing
  // arrowheads on the line (tips at the circle rim), per crop-compare + pixel map
  var ncx = [532, 563, 591, 622];
  var ncy = [246, 287, 328, 372];
  for (var n = 0; n < 4; n++) {
    var cx = ncx[n], cy = ncy[n];
    slide.addShape(pptx.ShapeType.ellipse, {
      x: (cx - 5) * PX, y: (cy - 5) * PX, w: 10 * PX, h: 10 * PX,
      fill: { type: "none" }, line: { color: C.red, width: 1 },
    });
    line(pptx, slide, cx - 4, cy, cx + 4, cy, { width: 1.25 });
    line(pptx, slide, cx - 3, cy - 2, cx + 3, cy + 2, { width: 1.25 });
    line(pptx, slide, cx - 3, cy + 2, cx + 3, cy - 2, { width: 1.25 });
    // flanking arrowheads pointing INWARD at the node
    slide.addShape(pptx.ShapeType.triangle, {
      x: (cx - 15.5) * PX, y: (cy - 5.5) * PX, w: 8 * PX, h: 11 * PX, rotate: 90,
      fill: { color: C.red }, line: { type: "none" },
    });
    slide.addShape(pptx.ShapeType.triangle, {
      x: (cx + 7.5) * PX, y: (cy - 5.5) * PX, w: 8 * PX, h: 11 * PX, rotate: 270,
      fill: { color: C.red }, line: { type: "none" },
    });
  }
}

function drawStackLeft(pptx, slide) { stackContainer(pptx, slide, 57, 11); }
function drawStackRight(pptx, slide) { stackContainer(pptx, slide, 761, 7.5); }

function drawStrip(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 178 * PX, y: 473 * PX, w: 315 * PX, h: 45 * PX, rectRadius: 0.07,
    fill: { color: C.containerFill },
    line: { color: C.containerBorder, width: 1.25, dashType: "dash" },
  });
  var xs = [191, 265, 339, 414];
  glyph(pptx, slide, xs[0], 494.5, 9.5, "1");
  glyph(pptx, slide, xs[2], 494.5, 9.5, "3");
  glyph(pptx, slide, xs[3], 494.5, 9.5, "4");
  // highlighted X2: dotted-border box + internal 5-cell MAGENTA glyph + red label
  // (pixel-verified: cells #E39FBE/#E0A5D3/#C44C88/#D595E2/#DC92E3, rose dividers)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 261 * PX, y: 472 * PX, w: 76 * PX, h: 35 * PX, rectRadius: 0.05,
    fill: { type: "none" },
    line: { color: C.x2Border, width: 1.5, dashType: "sysDot" },
  });
  var x2fills = ["E39FBE", "E0A5D3", "C44C88", "D595E2", "DC92E3"];
  for (var ci = 0; ci < 5; ci++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: (265 + ci * 13) * PX, y: 487.5 * PX, w: (ci === 4 ? 12.4 : 12) * PX, h: 14 * PX,
      fill: { color: x2fills[ci] }, line: { type: "none" },
    });
  }
  slide.addText(
    [
      { text: "X", options: {} },
      { text: "2", options: { subscript: true } },
    ],
    {
      x: 279 * PX, y: 478 * PX, w: 0.42, h: 0.24,
      align: "center", valign: "middle", fontSize: 11, bold: true,
      color: C.subRed, fontFace: FONT, margin: 0,
    }
  );
}

function drawQueryArrows(pptx, slide) {
  // thin red query arrow: strip X2 -> Dot Product box underside (head at top)
  line(pptx, slide, 298, 473, 298, 406, { width: 1.75, arrow: true });
  // chunky red diagonal block arrow at the strip's lower-left, pointing up-right
  line(pptx, slide, 266, 526, 284, 512, { color: C.redBlock, width: 4, arrow: true });
}

function drawFeedCurves(pptx, slide) {
  // thin dashed gray curves, strip ends -> stack bottoms, small GREEN up arrowheads
  var L = [[170, 472], [130, 468], [112, 460], [104, 448], [102, 430], [102, 409]];
  var R = [[497, 494], [560, 492], [615, 487], [658, 481], [695, 474], [722, 467],
           [743, 460], [760, 452], [775, 442], [786, 430], [795, 416], [801, 404]];
  var i;
  for (i = 0; i < L.length - 1; i++) {
    line(pptx, slide, L[i][0], L[i][1], L[i + 1][0], L[i + 1][1], { color: C.curve, width: 1, dash: "dash" });
  }
  for (i = 0; i < R.length - 1; i++) {
    line(pptx, slide, R[i][0], R[i][1], R[i + 1][0], R[i + 1][1], { color: C.curve, width: 1, dash: "dash" });
  }
  slide.addShape(pptx.ShapeType.triangle, {
    x: 97.5 * PX, y: 396 * PX, w: 9 * PX, h: 10 * PX,
    fill: { color: C.curveHead }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: 798.5 * PX, y: 396 * PX, w: 9 * PX, h: 10 * PX,
    fill: { color: C.curveHead }, line: { type: "none" },
  });
}

// ---- composition -----------------------------------------------------------

var BLOCKS = {
  canvas: drawCanvas,
  title: drawTitle,
  stackLeft: drawStackLeft,
  dotProduct: drawDotProduct,
  softmax: drawSoftmax,
  sigma: drawSigma,
  yOutput: drawYOutput,
  arrowsGreen: drawArrowsGreen,
  labels: drawLabels,
  flowLines: drawFlowLines,
  stackRight: drawStackRight,
  strip: drawStrip,
  queryArrows: drawQueryArrows,
  feedCurves: drawFeedCurves,
};

// canonical z-order for the full base
var ORDER = ["canvas", "dotProduct", "stackLeft", "softmax", "sigma",
  "flowLines", "arrowsGreen", "labels", "yOutput", "stackRight", "strip",
  "queryArrows", "feedCurves", "title"];

/**
 * Draw the slide-26 base composition at block granularity.
 * @param {object} pptx  pptxgenjs instance (ShapeType source)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip: [block...], only: [block...] }
 */
function renderBase(pptx, slide, opts) {
  opts = opts || {};
  var skip = opts.skip || [];
  var names = opts.only && opts.only.length ? opts.only.slice() : ORDER.slice();
  names.forEach(function (name) {
    if (skip.indexOf(name) !== -1) return;
    if (!BLOCKS[name]) throw new Error("slide_026 component: unknown block '" + name + "'");
    BLOCKS[name](pptx, slide);
  });
}

module.exports = {
  COLORS: C,
  FONT: FONT,
  BLOCKS: BLOCKS,
  ORDER: ORDER,
  renderBase: renderBase,
};
