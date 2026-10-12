// slide_039.js — "Parallel Processing" (Deep Learning DSAI 308, lecture 001_transformers_part1).
// ROOT slide (no parent in slide_dependencies.json) — built from PIL measurements of
// unique_slides/slide_039.jpg (960x540, 1px = 1pt = 1/72in). Scans banked in
// scratch/slide039/m1..m12_out.txt (2026-10-12).
//
// Measured structure (frame = ground truth):
//   - Title 3 bold lines centered at x=320: L1 "Parallel Processing" (y48-64, ~20pt),
//     L2 "Transform Sequence Elements in Parallel" (y68-91, ~17pt), L3
//     "[Calculation of Self Attention of words ( X1..X4)]" (y90-119, ~15pt; the four X
//     symbols + parens red with red subscript digits).
//   - FOUR identical pipeline panels (549x252 px) in a cascading stack:
//     panel1 x[127,676] y[237,489]; each next panel offset (+73,-27). Drawn back
//     (panel4) to front (panel1) so the front clips the rear ones exactly as the frame
//     shows (rear panels visible only right of x=676 / above y=237).
//   - Per-panel pipeline (panel1 coords): pills y[242,255] Similarity x[278,321] /
//     Probabilities x[386,442] / Weighted SUM x[500,562]; left green-dashed X box
//     x[132,187] y[285,401] (4 pale-green cells, green X letters); 4 K-rows at row
//     tops y=290/318/346/376 (row centers 299/327/355/384): green-bordered W^k box
//     x[199,226], 3 pale-yellow cells x[228,251], red K label x[252,265], long red row
//     line from ~x155 through the Dot box to the Scaling box; tan Dot Product box
//     x[268,325] y[265,404] ("Dot"/"Product" header + blue dot scatter with gray mesh);
//     red "K,q" annotation x[329,348] y[264,276] with tiny arrow into the Dot box;
//     red "SQRT d" x[381,401] y[264,288] at the Scaling box's top-right; pink Scaling
//     box x[351,372] y[266,404] (red rotated "Scaling by SQRTd"); lilac Soft max box
//     x[404,425] y[265,404] (purple rotated "Soft max"); pale-cyan Sigma box x[445,536]
//     y[265,280] (blue Sigma glyph); 4 red circle-cross nodes diagonal
//     (455,299)(476,327)(496,354)(519,385) with softmax fan lines + verticals up into
//     Sigma; W^V boxes x[573,607] (blue border, 4 stacked); V labels x[634,646] red;
//     right green-dashed cell box x[611,671] y[283,413]; W^q query branch (thin red
//     line x296 y[405,414], pale-yellow q cell x[300,321] y[413,422], white/red W^q box
//     x[280,310] y[422,445], small red q1 label below); bottom green-dashed X row
//     x[265,479] y[454,484] (cell 1 pink+red highlight, cells 2-4 pale with tiny
//     yellow/pink marks).
//   - Y output groups on a rising diagonal: green-dashed boxes 76x17 at
//     (453,193)(526,166)(602,140)(673,117) each with 4 pale cells + green Y letters,
//     slender red block up-arrow above each box (10x18 at x486+73i), tiny red arrow
//     entering each box from below.
//   - Bottom: 4 thick red block up-arrows (centers x304.5/394/488.5/593.5, y491-513)
//     labeled X1..X4 in bold red below (y516-530).
//   - Dashed light-green connectors (A5D6A7): short curve from the bottom row up the
//     panel's left side into the left X box (arrowhead at (158,401)); long distribution
//     curve along the bottom sweeping right and up, with 4 arrowheads entering each
//     panel's right box from below at (641,~405)(713,~378)(788,~350)(860,~323).
//   - Yellow sticker ~196x20 px rotated -21.8 deg (measured top-edge slope -0.4),
//     centered (790.5,474.5), bold red text "*** Run in Parallel ***".
//   - House chrome (playlist law): shared_patterns/house_chrome.js, numeral 39.
//
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//      videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_039.js

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_039_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

// ---- palette (PIL-measured cores; JPEG wash reconciled) ---------------------------
const C = {
  panelFill: "F0E0C8",     // (240,224,200)
  panelLine: "C9A87C",     // tan outline
  pillFill: "F8F8E2",      // (248,248,226)
  pillLine: "D8D0A8",
  pillText: "1F3FBF",
  greenDash: "00A651",     // dashed X/Y box borders
  cellGreen: "E7FAE7",     // pale green cell fill
  cellLine: "AEB098",
  greenText: "00A651",
  wkFill: "D8F0D0",
  wkLine: "7FC08A",
  kCellFill: "F7E8B8",     // pale-yellow vector cells
  dark: "333333",
  red: "C00000",
  dotFill: "D8C8B8",       // Dot Product box (216,200,184)
  dotLine: "B09078",
  dotHead: "5C4A3A",
  dotBlue: "1F3FBF",
  meshGray: "888888",
  scaleFill: "FFC4CB",     // pink Scaling box (255,196,203)
  scaleLine: "E8A0AC",
  softmaxFill: "F8DEFA",   // lilac Soft max box (248,222,250)
  softmaxLine: "D8B0E0",
  softmaxText: "8B3A94",
  sigmaFill: "E8F8F8",
  sigmaLine: "AEBDB8",
  sigmaGlyph: "3A4AAB",
  wvFill: "EAF1FB",
  wvLine: "1F3FBF",
  stickerFill: "FFFF00",
  connector: "A5D6A7",
  black: "000000",
};

// panel geometry
const PANEL_W = 549, PANEL_H = 252;
const PANEL_X0 = 127, PANEL_Y0 = 237, DX = 73, DY = -27;

// K-row tops (panel1) and centers
const ROW_TOPS = [290, 318, 346, 376];
const ROW_CENTERS = [299, 327, 355, 384];

// ---------------------------------------------------------------- helpers
function rect(slide, x, y, w, h, fill, line, opts = {}) {
  slide.addShape("rect", {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: fill ? { color: fill } : { type: "none" },
    line: line ? { color: line.color || line, width: line.width || 0.75, ...(line.dash ? { dashType: line.dash } : {}) } : { type: "none" },
    ...(opts.rotate ? { rotate: opts.rotate } : {}),
  });
}

function rrect(slide, x, y, w, h, fill, line, radius, opts = {}) {
  slide.addShape("roundRect", {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: fill ? { color: fill } : { type: "none" },
    line: line ? { color: line.color || line, width: line.width || 0.75, ...(line.dash ? { dashType: line.dash } : {}) } : { type: "none" },
    rectRadius: radius,
  });
}

function line(slide, x1, y1, x2, y2, color, width, opts = {}) {
  slide.addShape("line", {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color, width, ...(opts.dash ? { dashType: opts.dash } : {}), ...(opts.head ? { endArrowType: opts.head } : {}) },
  });
}

function txt(slide, text, x, y, w, h, opts = {}) {
  slide.addText(text, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: opts.align || "center", valign: opts.valign || "middle",
    fontFace: "Arial", margin: 0,
    fontSize: opts.fontSize || 8, bold: opts.bold !== false,
    color: opts.color || C.dark,
    ...(opts.rotate !== undefined ? { rotate: opts.rotate } : {}),
    ...(opts.lineSpacing ? { lineSpacing: opts.lineSpacing } : {}),
    ...(opts.charSpacing !== undefined ? { charSpacing: opts.charSpacing } : {}),
  });
}

// "X" + subscript digit label (red), e.g. subLabel(slide, "K", "1", ...)
function subLabel(slide, base, sub, x, y, w, h, opts = {}) {
  slide.addText(
    [
      { text: base, options: { color: opts.color || C.red } },
      { text: sub, options: { subscript: true, fontSize: Math.max(5, Math.round((opts.fontSize || 7.5) * 0.62)), color: opts.color || C.red } },
    ],
    {
      x: px(x), y: px(y), w: px(w), h: px(h),
      align: "center", valign: "middle", fontFace: "Arial", margin: 0,
      fontSize: opts.fontSize || 7.5, bold: true,
    }
  );
}

// "W" + subscript letter + superscript (1) — the course's certified notation
// (slide 37 component pattern: W<sub>k</sub><sup>(1)</sup>)
function wLabel(slide, sub, x, y, w, h, opts = {}) {
  slide.addText(
    [
      { text: "W", options: { color: opts.color || C.dark } },
      { text: sub, options: { subscript: true, fontSize: 5, color: opts.color || C.dark } },
      { text: "(1)", options: { superscript: true, fontSize: 5, color: opts.color || C.dark } },
    ],
    {
      x: px(x), y: px(y), w: px(w), h: px(h),
      align: "center", valign: "middle", fontFace: "Arial", margin: 0,
      fontSize: opts.fontSize || 6.5, bold: true,
    }
  );
}

// tiny multi-color token strip (slide-37 cell palette), n segments left-to-right
function strip(slide, x, y, w, h, segs) {
  const colors = { y: "FCFED0", g: "EDFEE0", w: "F2F2F4", l: "E4E6F5", p: "F8DDEF", c: "C9DFF5" };
  const n = segs.length;
  for (let j = 0; j < n; j++) {
    rect(slide, x + (w / n) * j, y, w / n, h, colors[segs[j]], { color: "9B9B8A", width: 0.4 });
  }
}

// slender block up-arrow: triangle head + shaft (matches the measured silhouette)
function slimUpArrow(slide, cx, tipY, w, h, color) {
  const headH = h * 0.28, shaftW = w * 0.55;
  slide.addShape("triangle", {
    x: px(cx - w / 2), y: px(tipY), w: px(w), h: px(headH), rotate: 0,
    fill: { color }, line: { type: "none" },
  });
  rect(slide, cx - shaftW / 2, tipY + headH - 0.5, shaftW, h - headH + 0.5, color, null);
}

// ---------------------------------------------------------------- title
function drawTitle(pptx, slide) {
  txt(slide, "Parallel Processing", 60, 45, 520, 22, { fontSize: 20, color: C.black });
  txt(slide, "Transform Sequence Elements in Parallel", 60, 63, 520, 28, { fontSize: 20, color: C.black });
  // L3 with red X runs (verbatim, red X's + red parens per frame); measured cap
  // height ~16px = same 20pt as L1/L2 (spec's "decreasing sizes" contradicted by
  // the frame ink — frame wins)
  slide.addText(
    [
      { text: "[Calculation of Self Attention of words ", options: { color: C.black } },
      { text: "( ", options: { color: C.red } },
      { text: "X", options: { color: C.red } },
      { text: "1", options: { subscript: true, fontSize: 12, color: C.red } },
      { text: ", ", options: { color: C.red } },
      { text: "X", options: { color: C.red } },
      { text: "2", options: { subscript: true, fontSize: 12, color: C.red } },
      { text: ", ", options: { color: C.red } },
      { text: "X", options: { color: C.red } },
      { text: "3", options: { subscript: true, fontSize: 12, color: C.red } },
      { text: ", ", options: { color: C.red } },
      { text: "X", options: { color: C.red } },
      { text: "4", options: { subscript: true, fontSize: 12, color: C.red } },
      { text: ")", options: { color: C.red } },
      { text: "]", options: { color: C.black } },
    ],
    {
      x: px(40), y: px(85), w: px(560), h: px(36),
      align: "center", valign: "middle", fontFace: "Arial", margin: 0,
      fontSize: 20, bold: true, color: C.black,
    }
  );
}

// ---------------------------------------------------------------- one pipeline panel
// (px0, py0) = panel top-left in frame px. All measured coords below are PANEL1
// ABSOLUTE frame px; X()/Y() rebase them onto the requested panel origin.
function drawPanel(pptx, slide, px0, py0) {
  const X = (v) => px0 + (v - 127); // 127 = panel1 left edge
  const Y = (v) => py0 + (v - 237); // 237 = panel1 top edge

  // panel body
  rrect(slide, px0, py0, PANEL_W, PANEL_H, C.panelFill, { color: C.panelLine, width: 1 }, 0.1);

  // -- pills along the top edge (flat ovals per the frame)
  const pills = [
    ["Similarity", 278, 321],
    ["Probabilities", 386, 442],
    ["Weighted SUM", 500, 562],
  ];
  for (const [label, x0, x1] of pills) {
    slide.addShape("ellipse", {
      x: px(X(x0)), y: px(Y(241.5)), w: px(x1 - x0), h: px(14),
      fill: { color: C.pillFill }, line: { color: C.pillLine, width: 0.5 },
    });
    txt(slide, label, X(x0), Y(242), x1 - x0, 13, { fontSize: 7.5, color: C.pillText });
  }

  // -- left green dashed X input box (4 stacked cells: token strip + X<sub>i</sub>)
  rrect(slide, X(132), Y(285), 55, 116, null, { color: C.greenDash, width: 1, dash: "dash" }, 0.06);
  const XSUBS = ["4", "3", "2", "1"]; // top -> bottom (frame/crop-verified)
  for (let i = 0; i < 4; i++) {
    rect(slide, X(134), Y(288 + 28.5 * i), 51, 26, C.cellGreen, { color: C.cellLine, width: 0.5 });
    strip(slide, X(136.5), Y(294 + 28.5 * i), 17, 12, ["y", "g", "p"]);
    subLabel(slide, "X", XSUBS[i], X(157), Y(292 + 28.5 * i), 24, 17, { fontSize: 9, color: C.greenText });
  }

  // -- Dot Product box (fill first; header + scatter on top)
  rect(slide, X(268), Y(265), 57, 140, C.dotFill, { color: C.dotLine, width: 0.75 });
  slide.addText(
    [
      { text: "Dot", options: { breakLine: true } },
      { text: "Product", options: {} },
    ],
    {
      x: px(X(268)), y: px(Y(266)), w: px(57), h: px(22),
      align: "center", valign: "middle", fontFace: "Arial", margin: 0,
      fontSize: 8, bold: true, color: C.dotHead, lineSpacing: 9.5,
    }
  );

  // -- K rows: W_k^(1) box, cells, K label, long red row lines (arrowheads at dots)
  for (let i = 0; i < 4; i++) {
    const rt = ROW_TOPS[i], rc = ROW_CENTERS[i];
    rect(slide, X(199), Y(rt), 27, 18, C.wkFill, { color: C.wkLine, width: 1 });
    wLabel(slide, "k", X(199), Y(rt), 27, 18);
    for (let j = 0; j < 3; j++) {
      rect(slide, X(228 + 7.8 * j), Y(rt + 2), 7.2, 14, C.kCellFill, { color: C.cellLine, width: 0.4 });
    }
    subLabel(slide, "K", String(4 - i), X(252), Y(rt + 1), 13, 15, { fontSize: 7.5 });
  }
  // long red row lines (over the boxes, under dots): into each dot, then out right
  const DOTX = [318, 307, 293, 281];
  for (let i = 0; i < 4; i++) {
    const rc = ROW_CENTERS[i], dx = DOTX[i];
    line(slide, X(155), Y(rc), X(dx - 4.5), Y(rc), C.red, 1, { head: "triangle" });
    line(slide, X(dx + 4.5), Y(rc), X(366), Y(rc), C.red, 1, { head: "triangle" });
  }

  // -- dot scatter: 4 primary dots on row lines + 4 smaller, gray mesh
  const DOTS = [
    [318, 299, 7], [307, 327, 7], [293, 355, 7], [281, 385, 7],
    [311, 313, 4.5], [299, 341, 4.5], [286, 369, 4.5], [303, 369, 4.5],
  ];
  // mesh lines (under dots)
  const pairs = [[0, 4], [4, 1], [1, 5], [5, 2], [2, 6], [6, 3], [1, 7], [7, 3], [0, 1], [1, 2], [2, 3]];
  for (const [a, b] of pairs) {
    line(slide, X(DOTS[a][0]), Y(DOTS[a][1]), X(DOTS[b][0]), Y(DOTS[b][1]), C.meshGray, 0.5);
  }
  for (const [dx, dy, d] of DOTS) {
    slide.addShape("ellipse", {
      x: px(X(dx) - d / 2), y: px(Y(dy) - d / 2), w: px(d), h: px(d),
      fill: { color: C.dotBlue }, line: { color: "C9DFF5", width: 0.75 },
    });
  }

  // -- "K,q" annotation left of the Scaling box top + tiny arrow into the Dot box,
  //    plus the fraction bar (measured washed bar at y~277 spanning x330-400)
  txt(slide, "K,q", X(328), Y(263), 21, 14, { fontSize: 7.5, color: C.red });
  line(slide, X(327.5), Y(270), X(325), Y(270), C.red, 0.75);
  line(slide, X(330), Y(277), X(400), Y(277), C.red, 1.25);

  // -- "√d" at the Scaling box's top-right (as measured: right of the box top)
  txt(slide, "√d", X(381), Y(264), 21, 24, { fontSize: 9.5, color: C.red });

  // -- pink Scaling box (rotated red text, reads bottom-to-top)
  rect(slide, X(351), Y(266), 21, 138, C.scaleFill, { color: C.scaleLine, width: 0.75 });
  txt(slide, "Scaling by √d", X(351) - 60, Y(266) + 138 / 2 - 8, 141, 16, {
    fontSize: 7.5, color: C.red, rotate: 270,
  });

  // -- lilac Soft max box (rotated purple text)
  rect(slide, X(404), Y(265), 21, 139, C.softmaxFill, { color: C.softmaxLine, width: 0.75 });
  txt(slide, "Soft max", X(404) - 60, Y(265) + 139 / 2 - 8, 139, 16, {
    fontSize: 7.5, color: C.softmaxText, rotate: 270,
  });

  // -- pale-cyan Sigma box
  rect(slide, X(445), Y(265), 91, 15, C.sigmaFill, { color: C.sigmaLine, width: 0.75 });
  txt(slide, "Σ", X(445), Y(265), 91, 15, { fontSize: 13, color: C.sigmaGlyph });

  // -- 4 circle-cross nodes (lines pass THROUGH them, as in the frame) + softmax fan
  const OT = [[455.5, 299], [476.5, 327.5], [496.5, 354.5], [519, 385]];
  const fanFrom = [283, 300, 317, 334];
  for (let i = 0; i < 4; i++) {
    const [mx, my] = OT[i];
    line(slide, X(429), Y(fanFrom[i]), X(mx - 3), Y(my - 1), C.red, 0.9, { head: "triangle" });
    line(slide, X(mx), Y(my - 11), X(mx), Y(282), C.red, 0.9, { head: "triangle" });
  }
  // V lines from the right input box through to the nodes (under the boxes)
  for (let i = 0; i < 4; i++) {
    const [mx, my] = OT[i];
    line(slide, X(650), Y(ROW_CENTERS[i]), X(mx + 3), Y(ROW_CENTERS[i]), C.red, 0.9, { head: "triangle" });
  }
  for (const [mx, my] of OT) {
    slide.addShape("ellipse", {
      x: px(X(mx) - 5.5), y: px(Y(my) - 5.5), w: px(11), h: px(11),
      fill: { type: "none" }, line: { color: C.red, width: 1.25 },
    });
    line(slide, X(mx) - 3, Y(my) - 3, X(mx) + 3, Y(my) + 3, C.red, 1);
    line(slide, X(mx) - 3, Y(my) + 3, X(mx) + 3, Y(my) - 3, C.red, 1);
  }

  // -- right group: V-strip container, V labels, green-dashed X box (strips + X_i)
  rrect(slide, X(612), Y(283), 21, 130, null, { color: C.greenDash, width: 1, dash: "dash" }, 0.05);
  rrect(slide, X(644), Y(283), 25, 130, null, { color: C.greenDash, width: 1, dash: "dash" }, 0.05);
  for (let i = 0; i < 4; i++) {
    const rt = ROW_TOPS[i];
    // W^V box (blue)
    rect(slide, X(573), Y(rt - 4), 34, 24, C.wvFill, { color: C.wvLine, width: 1 });
    wLabel(slide, "v", X(573), Y(rt - 4), 34, 24, { color: C.wvLine, fontSize: 7 });
    // V vector strip (left container cell)
    rect(slide, X(613.5), Y(rt - 3), 18, 22, C.kCellFill, { color: C.cellLine, width: 0.4 });
    strip(slide, X(614.5), Y(rt + 3), 16, 10, ["y", "g"]);
    // V label between the containers (red)
    subLabel(slide, "V", String(4 - i), X(633), Y(rt + 1), 13, 15, { fontSize: 7.5 });
    // X-side box cell: mini strip + X<sub>i</sub>
    rect(slide, X(645.5), Y(rt - 3), 22, 22, C.cellGreen, { color: C.cellLine, width: 0.4 });
    strip(slide, X(646.5), Y(rt + 4), 8, 9, ["y", "l"]);
    subLabel(slide, "X", XSUBS[i], X(655), Y(rt), 11, 15, { fontSize: 6.5, color: C.greenText });
  }

  // -- query branch: line, q cell, W_q^(1) box, q1 label beside the strip
  line(slide, X(296), Y(405), X(296), Y(414), C.red, 1);
  rect(slide, X(300), Y(413), 21, 9, C.kCellFill, { color: C.red, width: 0.5 });
  rect(slide, X(280), Y(422), 30, 23, "FFFFFF", { color: C.red, width: 1 });
  wLabel(slide, "q", X(280), Y(422), 30, 23, { color: C.red, fontSize: 7 });
  subLabel(slide, "q", "1", X(279), Y(413), 13, 11, { fontSize: 6.5 });

  // -- bottom green-dashed X row (cell 1 highlighted)
  rrect(slide, X(265), Y(454), 214, 30, null, { color: C.greenDash, width: 1, dash: "dash" }, 0.05);
  rect(slide, X(267), Y(457), 58, 24, "F2C6DE", { color: C.red, width: 1.25 });
  txt(slide, "X", X(267), Y(457), 58, 24, { fontSize: 9, color: C.greenText });
  const cellsX = [329, 377, 425];
  for (let j = 0; j < 3; j++) {
    const cx = cellsX[j];
    rect(slide, X(cx), Y(457), 44, 24, "F5F0E4", { color: C.cellLine, width: 0.5 });
    rect(slide, X(cx + 1), Y(465), 7, 9, C.kCellFill, null);
    rect(slide, X(cx + 18), Y(465), 18, 8, "F2C6DE", null);
    txt(slide, "X", X(cx + 8), Y(457), 28, 24, { fontSize: 9, color: C.greenText });
  }
}

// ---------------------------------------------------------------- Y output groups
function drawYGroups(pptx, slide) {
  for (let i = 0; i < 4; i++) {
    const bx = 453 + 73 * i, by = 193 - 27 * i;
    // red slender block arrow above the box
    slimUpArrow(slide, 491 + 73 * i, by - 20, 9, 18, C.red);
    // green dashed box with 4 cells + Y letters
    rrect(slide, bx, by, 76, 17, null, { color: C.greenDash, width: 1, dash: "dash" }, 0.05);
    for (let j = 0; j < 4; j++) {
      rect(slide, bx + 3 + 17.5 * j, by + 2, 15.5, 13, "E3EFE3", { color: C.cellLine, width: 0.5 });
      txt(slide, "Y", bx + 3 + 17.5 * j, by + 2, 15.5, 13, { fontSize: 7.5, color: C.greenText });
    }
    // tiny red arrow entering the box from below
    line(slide, 491 + 73 * i, by + 33, 491 + 73 * i, by + 18, C.red, 1, { head: "triangle" });
    // red Y label beside the arrow head zone (measured: none distinct — the box + arrows carry it)
  }
}

// ---------------------------------------------------------------- bottom arrows
function drawBottomArrows(pptx, slide) {
  const centers = [304.5, 394, 488.5, 593.5];
  const subs = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const cx = centers[i];
    slide.addShape("upArrow", {
      x: px(cx - 5.5), y: px(490), w: px(11), h: px(24),
      fill: { color: C.red }, line: { type: "none" },
    });
    subLabel(slide, "X", subs[i], cx - 12, 515, 24, 17, { fontSize: 14 });
  }
}

// ---------------------------------------------------------------- connectors
function drawConnectors(pptx, slide) {
  const cn = C.connector;
  // short curve: bottom row's left end up the panel's left side into the left X box
  line(slide, 263, 472, 215, 462, cn, 1, { dash: "dash" });
  line(slide, 215, 462, 172, 440, cn, 1, { dash: "dash" });
  line(slide, 172, 440, 158, 410, cn, 1, { dash: "dash", head: "triangle" });
  // long distribution connector: along the bottom, right, then up the right side
  line(slide, 272, 476, 470, 468, cn, 1, { dash: "dash" });
  line(slide, 470, 468, 640, 492, cn, 1, { dash: "dash" });
  line(slide, 640, 492, 800, 480, cn, 1, { dash: "dash" });
  line(slide, 800, 480, 880, 420, cn, 1, { dash: "dash" });
  line(slide, 880, 420, 872, 340, cn, 1, { dash: "dash" });
  // 4 arrowheads entering each panel's right box from below
  const heads = [[641, 430, 407], [713, 400, 380], [788, 370, 352], [860, 340, 325]];
  for (const [x, y1, y2] of heads) {
    line(slide, x, y1, x, y2, cn, 1, { dash: "dash", head: "triangle" });
  }
}

// ---------------------------------------------------------------- sticker
function drawSticker(pptx, slide) {
  const w = 196, h = 20, cx = 790.5, cy = 474.5, rot = -21.8;
  const x = cx - w / 2, y = cy - h / 2;
  rect(slide, x, y, w, h, C.stickerFill, null, { rotate: rot });
  txt(slide, "*** Run in Parallel ***", x, y, w, h, {
    fontSize: 12.5, color: C.red, rotate: rot,
  });
}

// ---------------------------------------------------------------- compose
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

drawHouseChrome(pres, slide, { numeral: 39 });
drawTitle(pres, slide);

// panels back-to-front: panel4 (X4) rearmost ... panel1 (X1) frontmost
for (let i = 3; i >= 0; i--) {
  drawPanel(pres, slide, PANEL_X0 + DX * i, PANEL_Y0 + DY * i);
}

drawYGroups(pres, slide);
drawConnectors(pres, slide);
drawBottomArrows(pres, slide);
drawSticker(pres, slide);

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT)).catch((e) => {
  console.error("BUILD FAILED:", e);
  process.exit(1);
});
