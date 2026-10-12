// slide_009.js — "Using  FF NN  for Multiplication of a Vector by a Matrix"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 9)
//
// HEAD OF PATTERN GROUP P1 [9,10,12,14,16] — this build establishes the group
// pattern (chrome + two-panel FF-NN/vector-by-matrix composition). Slides 10/12/14/16
// reuse the PATTERN (not this content): shared blocks must stay pixel-consistent.
//
// CONTENT SPEC: analysis/slide_009_final.json (PASS_WITH_FIXES, score 9).
// Ground truth: unique_slides/slide_009.jpg (960x540). CONFIRMED DEPENDENT: 10 <- 9
// (component banked at recreated_pptx/build/components/slide_009.js, renderBase).
//
// FRAME->SLIDE MAPPING (video-002 capture zoomed ~0.958 with black letterbox; deck
// fit per certified slide_002.js / slide_008.js, identical within ~1px):
//   slide_x = (frame_x - 17.628) / 0.961232 ;  slide_y = frame_y / 0.955556
// Cross-check on THIS frame (scratch/slide009/measure2_output.txt + PIL sweep):
//   chrome left border  fx 58..59  -> sx 42.0..43.1   (house 42)   OK
//   badge yellow bbox   (859..892, 57..85) center (875.5,71) -> (892.5, 74.3)
//   vs house badge (893,71) — within JPEG-bbox noise (same values slide_002 recorded).
//   black letterbox rows ~517..539 = below chrome bottom (sy 541) -> omitted.
// All measurements from scratch/slide009/measure_output.txt + measure2_output.txt
// (banked by the 04:16-07:42 measurement campaigns) — read off the z_*/m2_* crops.
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c), founder artifact law;
// spec validation.uncertain_items flags both as optional):
//   * mouse cursor ~fx(400,255) below the y-row (spec step 24, "may be omitted")
//   * black bottom letterbox strip, frame rows ~517..539 (below the slide bottom).

const { CHROME, drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);
const pptxgen = require("pptxgenjs");

const FONT = "Arial";
const SERIF = "Times New Roman"; // big display letters X / Y^T are serif bold red in the frame

// ---- frame-measured palette (scratch/slide009/measure*_output.txt) ----------------
const C = {
  titleRed: "C00000",
  inkRed: "C00000",
  braceBlue: "574CC2",   // brace core n=60
  sigmoidBlue: "4E43C8", // "= Sigmoid" core #8077D8 JPEG-soft -> saturated
  stack1: "2478D0",      // W-group blue (z_stack1 ink; #2FACDB patch was ellipse bleed)
  stack2: "B04AC8",      // purple
  stack3: "F09828",      // orange
  stack4: "6CB86C",      // green (#7CC27C n=78, darker core)
  neuronRim: "9B404D",   // n=7
  neuronFill: "F6F8FE",
  inputFill: "F5CCF6",   // #F6CCF8 n=20
  inputRim: "D9A8DC",
  cyan: "88FFFF",        // ellipse1 fill n=349
  matrixFill: "D8FFE6",  // n=80
  bFill: "D9FDC8",       // #D4FDC3 n=60
  panelR: "F2F1EF",      // right panel n=300
  panelRim: "D0D5DA",
  leftRim: "CFD6DC",     // left panel border #CFD6DC n=150
  line: "C8C4DC",        // connection lines (#ECECEE core + JPEG halo)
  cellFill: "FCF9C8",    // #F5F7BD text patch reconciled
  cellRim: "8B7B3A",     // olive cell borders (z_matrix_c)
  yBoxFill: "FFF1F0",    // n=110
  yBoxRim: "B0523C",     // brownish-red y-box borders (m2_neuron1_y1b1 crop)
  pillPink: "FFC8EE",    // x pill n=15
  yPill: "EFD4F4",       // y-row pill (m2 crop: pale lavender-pink)
  xCircleFill: "DCD4EC",
  green: "2E9C48",
};

// ---- measured geometry, slide px (1px = 1pt = 1/72 in) ----------------------------
const G = {
  title: { cx: 459, capTop: 71.2, capBot: 91.0, fs: 26.5 },
  leftPanel: { x: 67, y: 107, w: 202, h: 426 },
  header: { x: 76, y: 118, w: 130, h: 24 },
  inputs: { cx: 88.8, cy: [164.3, 275.2, 386.2, 489.8], d: 25 },
  neurons: { c: [[224.0, 168.0], [225.0, 275.8], [225.0, 385.1], [220.8, 489.8]], d: 34.5 },
  ellipses: [
    { x: 106.4, y: 151.7, w: 31.2, h: 93.1, fill: C.cyan, rim: "4AB8D8" },
    { x: 106.4, y: 248.0, w: 31.2, h: 88.0, fill: "F8D8F8", rim: "D888D8" },
    { x: 106.4, y: 340.0, w: 31.2, h: 78.0, fill: "FFE4CC", rim: "E8B088" },
    { x: 106.4, y: 421.0, w: 31.2, h: 81.0, fill: "DFF8D8", rim: "98D090" },
  ],
  // weight-label ink tops (slide px), per stack (frame-measured; s3 interpolated)
  wTops: [
    [159.7, 184.8, 209.9, 228.7],
    [250.7, 272.7, 295.7, 313.5],
    [342.0, 363.0, 384.0, 403.0],
    [420.3, 445.4, 468.4, 483.1],
  ],
  rightPanel: { x: 282, y: 104, w: 627, h: 207 },
  yt: { cx: 366, boxY: 156 },
  yPill: { x: 299, y: 191, w: 125, h: 31 },
  yBoxes: { cxs: [312.8, 341.9, 372.1, 403.7], cy: 205.6, w: 18, h: 15 },
  yBrackets: { l: { x: 284.5, y: 183 }, r: { x: 424.5, y: 184 }, w: 14, h: 42 },
  sigmoid: { x: 446, y: 198, w: 76, h: 24 },
  braceL: { x: 524, y: 111, w: 18, h: 191 },
  braceR: { x: 834, y: 111, w: 18, h: 192 },
  xPill: { x: 539, y: 117, w: 132, h: 31 },
  xCircles: { cxs: [564.0, 593.2, 618.3, 643.3], cy: 131.6, d: 23 },
  xBrackets: { l: { x: 543, y: 116 }, r: { x: 650, y: 116 }, w: 11, h: 33 },
  bigX: { cx: 596.8, boxY: 155 },
  matrix: { x: 680, y: 117, w: 151, h: 184 },
  mCells: { cxs: [699.6, 736.2, 772.8, 809.4], cys: [144.4, 186.4, 228.5, 270.5], w: 29, h: 24 },
  mGridH: [163.2, 207.2, 250.1],
  mGridV: [718.6, 756.3, 793.8],
  plus: { x: 850, y: 196, w: 20, h: 20 },
  bBox: { x: 874.5, cys: [144.4, 182.5, 225.4, 265.7], w: 23, h: 13 },
  bContainer: { x: 870, y: 113, w: 43, h: 191 },
  // parens: thin tall arcs (stroke fx ~4px), left ink fx 850..855 / right 887..891,
  // fy 122..279 -> sx h ~161, arc boxes centered on the strokes
  parens: { l: { x: 861.5, y: 128.5 }, r: { x: 901.5, y: 127.5 }, w: 9, h: 161 },
};

const SUB = (t, o = {}) => ({ text: t, options: Object.assign({ subscript: true }, o) });
const R = (t, o = {}) => ({ text: t, options: o });
const px = (v) => v / 72; // slide px -> inches

function drawTitle(pres, s) {
  // ink fx 131..788 (cx 459.2), caps fy 68..87 -> sx 118.0..800.4 / sy 71.2..91.0
  s.addText(
    [R("Using  FF NN  for Multiplication of a Vector by a Matrix", {})],
    { x: px(G.title.cx - 371), y: px(G.title.capTop - 7.2), w: px(742), h: px(36),
      align: "center", valign: "middle", bold: true, fontSize: G.title.fs,
      color: C.titleRed, fontFace: FONT, margin: 0 }
  );
}

function drawLeftPanel(pres, s) {
  const p = G.leftPanel;
  s.addShape(pres.ShapeType.roundRect, {
    x: px(p.x), y: px(p.y), w: px(p.w), h: px(p.h), rectRadius: 0.06,
    fill: { color: "FFFFFF" }, line: { color: C.leftRim, width: 1 },
  });
  // header: "Input Word" black bold 16 + "X" red bold 24 (fx 93..198, fy 113..133)
  s.addText([R("Input Word ", { fontSize: 16, color: "000000" }), R("X", { fontSize: 24, color: C.inkRed })],
    { x: px(G.header.x), y: px(G.header.y), w: px(G.header.w), h: px(G.header.h),
      align: "left", valign: "middle", bold: true, fontFace: FONT, margin: 0 });
}

function drawConnections(pres, s) {
  // 16 thin lines input-center -> neuron-center (ends hidden under circles)
  for (const iy of G.inputs.cy) {
    for (const [nx, ny] of G.neurons.c) {
      s.addShape(pres.ShapeType.line, {
        x: px(G.inputs.cx), y: px(iy), w: px(nx - G.inputs.cx), h: px(ny - iy),
        line: { color: "D0CCE0", width: 0.75 },
      });
    }
  }
}

function drawStacks(pres, s) {
  // colored ellipses behind the 4 weight-label stacks, then the labels
  for (const e of G.ellipses) {
    s.addShape(pres.ShapeType.ellipse, {
      x: px(e.x), y: px(e.y), w: px(e.w), h: px(e.h),
      fill: { color: e.fill }, line: { color: e.rim, width: 1 },
    });
  }
  const names = [["W11", "W21", "W31", "W41"], ["W12", "W22", "W32", "W42"],
                 ["W13", "W23", "W33", "W43"], ["W14", "W24", "W34", "W44"]];
  const cols = [C.stack1, C.stack2, C.stack3, C.stack4];
  for (let g = 0; g < 4; g++) {
    for (let k = 0; k < 4; k++) {
      const top = G.wTops[g][k];
      s.addText([R("W", { fontSize: 9 }), SUB(names[g][k].slice(1), { fontSize: 7 })],
        { x: px(106), y: px(top), w: px(32), h: px(14), align: "center", valign: "top",
          bold: true, color: cols[g], fontFace: FONT, margin: 0 });
    }
  }
}

function drawInputs(pres, s) {
  const labels = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const cy = G.inputs.cy[i];
    s.addShape(pres.ShapeType.ellipse, {
      x: px(G.inputs.cx - 12.5), y: px(cy - 12.5), w: px(25), h: px(25),
      fill: { color: C.inputFill }, line: { color: C.inputRim, width: 1.25 },
    });
    s.addText([R("X", { fontSize: 11 }), SUB(labels[i], { fontSize: 8 })],
      { x: px(G.inputs.cx - 14), y: px(cy - 9), w: px(28), h: px(18),
        align: "center", valign: "middle", bold: true, color: "111111", fontFace: FONT, margin: 0 });
  }
}

function drawNeurons(pres, s) {
  for (const [cx, cy] of G.neurons.c) {
    s.addShape(pres.ShapeType.ellipse, {
      x: px(cx - 17.25), y: px(cy - 17.25), w: px(34.5), h: px(34.5),
      fill: { color: C.neuronFill }, line: { color: C.neuronRim, width: 1.5 },
    });
    // multicolor pie on the left rim (3 wedges: blue/purple/green)
    const pies = [[90, 210, C.stack1], [210, 330, C.stack2], [330, 90, C.stack4]];
    for (const [a0, a1, col] of pies) {
      s.addShape(pres.ShapeType.pie, {
        x: px(cx - 16.5), y: px(cy - 4), w: px(8), h: px(8), angleRange: [a0, a1],
        fill: { color: col }, line: { type: "none" },
      });
    }
    // Sigma + small sigmoid-curve glyph (frame: Sigma + red squiggle)
    s.addText("\u03A3", { x: px(cx - 13), y: px(cy - 10), w: px(26), h: px(20),
      align: "center", valign: "middle", bold: true, fontSize: 14, color: "1A1A1A",
      fontFace: FONT, margin: 0 });
    s.addShape(pres.ShapeType.arc, {
      x: px(cx + 1), y: px(cy + 1), w: px(9), h: px(7), angleRange: [180, 360],
      fill: { type: "none" }, line: { color: C.neuronRim, width: 1.5 },
    });
  }
}

function drawOutputs(pres, s) {
  // MEASURED (ASCII ink map, scratch/slide009/map_neuron1.txt):
  //   right-arrow ink fx 256..272 @ cy  -> sx (cx+18)..(cx+41), head right
  //   y_i ink fx 250..262 fy (cy-17)..(cy-1)  -> ABOVE the arrow end, at neuron edge
  //   b-arrow vertical fx ~228 from fy cy+19 (tip) down to cy+27.5 (into b_i)
  //   b_i ink fx 229..247 fy (cy+27.7).. -> directly BELOW the neuron
  const labels = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const [cx, cy] = G.neurons.c[i];
    // green right-arrow at neuron mid-height
    s.addShape(pres.ShapeType.line, {
      x: px(cx + 18), y: px(cy), w: px(23), h: 0,
      line: { color: C.green, width: 1.75, endArrowType: "triangle" },
    });
    // y_i red label above the arrow end (frame ink ~20pt em: glyph h 14.6pt)
    s.addText([R("y", { fontSize: 19 }), SUB(labels[i], { fontSize: 10.5 })],
      { x: px(cx + 18), y: px(cy - 26.5), w: px(26), h: px(24), align: "left", valign: "top",
        bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
    // green vertical arrow from b_i up into the neuron bottom (head at top)
    s.addShape(pres.ShapeType.line, {
      x: px(cx - 4.5), y: px(cy + 19), w: 0, h: px(8.5),
      line: { color: C.green, width: 1.5, beginArrowType: "triangle" },
    });
    // b_i black label below the neuron (frame ink ~20pt em: glyph h 15.7pt)
    s.addText([R("b", { fontSize: 19 }), SUB(labels[i], { fontSize: 10.5 })],
      { x: px(cx - 6), y: px(cy + 22.5), w: px(26), h: px(22), align: "left", valign: "top",
        bold: true, color: "1A1A1A", fontFace: FONT, margin: 0 });
  }
}

function drawRightPanel(pres, s) {
  const p = G.rightPanel;
  s.addShape(pres.ShapeType.roundRect, {
    x: px(p.x), y: px(p.y), w: px(p.w), h: px(p.h), rectRadius: 0.06,
    fill: { color: C.panelR }, line: { color: C.panelRim, width: 1 },
  });
  // -- Y^T above the y-row (fx 355..384, fy 154..172; serif bold red) --------------
  s.addText([R("Y", { fontSize: 25 }), R("T", { fontSize: 13, superscript: true })],
    { x: px(G.yt.cx - 20), y: px(G.yt.boxY), w: px(40), h: px(28), align: "center",
      valign: "middle", bold: true, color: C.inkRed, fontFace: SERIF, margin: 0 });
  // -- y-row: pink pill + red square brackets + 4 white/red boxes ------------------
  const yp = G.yPill;
  s.addShape(pres.ShapeType.roundRect, { x: px(yp.x), y: px(yp.y), w: px(yp.w), h: px(yp.h),
    rectRadius: 0.12, fill: { color: C.yPill }, line: { color: "D8A8DC", width: 1 } });
  s.addText("[", { x: px(G.yBrackets.l.x), y: px(G.yBrackets.l.y), w: px(G.yBrackets.w), h: px(G.yBrackets.h),
    align: "center", valign: "middle", fontSize: 48, color: "A85048", fontFace: FONT, margin: 0, fit: "none" });
  s.addText("]", { x: px(G.yBrackets.r.x), y: px(G.yBrackets.r.y), w: px(G.yBrackets.w), h: px(G.yBrackets.h),
    align: "center", valign: "middle", fontSize: 48, color: "A85048", fontFace: FONT, margin: 0, fit: "none" });
  const ysub = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const bx = G.yBoxes.cxs[i] - G.yBoxes.w / 2, by = G.yBoxes.cy - G.yBoxes.h / 2;
    s.addShape(pres.ShapeType.roundRect, { x: px(bx), y: px(by), w: px(G.yBoxes.w), h: px(G.yBoxes.h),
      rectRadius: 0.05, fill: { color: C.yBoxFill }, line: { color: C.yBoxRim, width: 1.25 } });
    s.addText([R("y", { fontSize: 11 }), SUB(ysub[i], { fontSize: 8 })],
      { x: px(bx), y: px(by), w: px(G.yBoxes.w), h: px(G.yBoxes.h), align: "center",
        valign: "middle", bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
  }
  // -- "= Sigmoid" (fx 451..513, fy 193..208) --------------------------------------
  s.addText("= Sigmoid", { x: px(G.sigmoid.x), y: px(G.sigmoid.y), w: px(G.sigmoid.w), h: px(G.sigmoid.h),
    align: "center", valign: "middle", bold: true, italic: true, fontSize: 15,
    color: C.sigmoidBlue, fontFace: FONT, margin: 0 });
  // -- big curly braces (fx 521..538 / 818..835, fy 106..289) ----------------------
  s.addShape(pres.ShapeType.leftBrace, { x: px(G.braceL.x), y: px(G.braceL.y), w: px(G.braceL.w), h: px(G.braceL.h),
    fill: { type: "none" }, line: { color: C.braceBlue, width: 3 } });
  s.addShape(pres.ShapeType.rightBrace, { x: px(G.braceR.x), y: px(G.braceR.y), w: px(G.braceR.w), h: px(G.braceR.h),
    fill: { type: "none" }, line: { color: C.braceBlue, width: 3 } });
  // -- X pill: pink stadium, red brackets, 4 red-rimmed circles, serif X below -----
  const xp = G.xPill;
  s.addShape(pres.ShapeType.roundRect, { x: px(xp.x), y: px(xp.y), w: px(xp.w), h: px(xp.h),
    rectRadius: 0.14, fill: { color: C.pillPink }, line: { color: "E8A8D8", width: 1 } });
  s.addText("[", { x: px(G.xBrackets.l.x), y: px(G.xBrackets.l.y), w: px(G.xBrackets.w), h: px(G.xBrackets.h),
    align: "center", valign: "middle", fontSize: 34, color: "A85048", fontFace: FONT, margin: 0, fit: "none" });
  s.addText("]", { x: px(G.xBrackets.r.x), y: px(G.xBrackets.r.y), w: px(G.xBrackets.w), h: px(G.xBrackets.h),
    align: "center", valign: "middle", fontSize: 34, color: "A85048", fontFace: FONT, margin: 0, fit: "none" });
  const xsub = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const cx = G.xCircles.cxs[i], cy = G.xCircles.cy, d = G.xCircles.d;
    s.addShape(pres.ShapeType.ellipse, { x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
      fill: { color: C.xCircleFill }, line: { color: C.inkRed, width: 1.5 } });
    s.addText([R("X", { fontSize: 10 }), SUB(xsub[i], { fontSize: 7.5 })],
      { x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d), align: "center",
        valign: "middle", bold: true, color: "111111", fontFace: FONT, margin: 0 });
  }
  s.addText("X", { x: px(G.bigX.cx - 21), y: px(G.bigX.boxY), w: px(42), h: px(28),
    align: "center", valign: "middle", bold: true, fontSize: 26, color: C.inkRed,
    fontFace: SERIF, margin: 0 });
  // -- 4x4 weight matrix on mint container with green gridlines --------------------
  const m = G.matrix;
  s.addShape(pres.ShapeType.roundRect, { x: px(m.x), y: px(m.y), w: px(m.w), h: px(m.h),
    rectRadius: 0.08, fill: { color: C.matrixFill }, line: { color: "9CD4AC", width: 0.75 } });
  for (const gy of G.mGridH) s.addShape(pres.ShapeType.line, {
    x: px(m.x), y: px(gy), w: px(m.w), h: 0, line: { color: "9CD4AC", width: 0.5 } });
  for (const gx of G.mGridV) s.addShape(pres.ShapeType.line, {
    x: px(gx), y: px(m.y), w: 0, h: px(m.h), line: { color: "9CD4AC", width: 0.5 } });
  const msub = [["11", "21", "31", "41"], ["12", "22", "32", "42"],
                ["13", "23", "33", "43"], ["14", "24", "34", "44"]];
  const mcols = [C.stack1, C.stack2, C.stack3, C.stack4];
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      const bx = G.mCells.cxs[c] - G.mCells.w / 2, by = G.mCells.cys[r] - G.mCells.h / 2;
      s.addShape(pres.ShapeType.roundRect, { x: px(bx), y: px(by), w: px(G.mCells.w), h: px(G.mCells.h),
        rectRadius: 0.05, fill: { color: C.cellFill }, line: { color: C.cellRim, width: 1 } });
      s.addText([R("W", { fontSize: 9 }), SUB(msub[r][c], { fontSize: 7 })],
        { x: px(bx), y: px(by), w: px(G.mCells.w), h: px(G.mCells.h), align: "center",
          valign: "middle", bold: true, color: mcols[r], fontFace: FONT, margin: 0 });
    }
  }
  // -- red plus (fx 839..848, fy 193..201) -----------------------------------------
  s.addText("+", { x: px(G.plus.x), y: px(G.plus.y), w: px(G.plus.w), h: px(G.plus.h),
    align: "center", valign: "middle", bold: true, fontSize: 18, color: C.inkRed,
    fontFace: FONT, margin: 0 });
  // -- bias column: mint container, tall red parens, 4 yellow b-boxes --------------
  const bc = G.bContainer;
  s.addShape(pres.ShapeType.roundRect, { x: px(bc.x), y: px(bc.y), w: px(bc.w), h: px(bc.h),
    rectRadius: 0.08, fill: { color: C.bFill }, line: { color: "9CD4AC", width: 0.75 } });
  // parens as thin tall arcs (text glyphs are far too fat — frame stroke is ~4px)
  s.addShape(pres.ShapeType.arc, { x: px(G.parens.l.x), y: px(G.parens.l.y), w: px(G.parens.w), h: px(G.parens.h),
    angleRange: [90, 270], fill: { type: "none" }, line: { color: "A85048", width: 2 } });
  s.addShape(pres.ShapeType.arc, { x: px(G.parens.r.x), y: px(G.parens.r.y), w: px(G.parens.w), h: px(G.parens.h),
    angleRange: [270, 450], fill: { type: "none" }, line: { color: "A85048", width: 2 } });
  const bsub = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const by = G.bBox.cys[i] - G.bBox.h / 2;
    s.addShape(pres.ShapeType.roundRect, { x: px(G.bBox.x), y: px(by), w: px(G.bBox.w), h: px(G.bBox.h),
      rectRadius: 0.05, fill: { color: C.cellFill }, line: { color: C.cellRim, width: 1 } });
    s.addText([R("b", { fontSize: 10 }), SUB(bsub[i], { fontSize: 7.5 })],
      { x: px(G.bBox.x), y: px(by), w: px(G.bBox.w), h: px(G.bBox.h), align: "center",
        valign: "middle", bold: true, color: "1A1A1A", fontFace: FONT, margin: 0 });
  }
}

/**
 * Full certified composition. opts: { numeral (default 9), skip: [] }
 * Block names: 'title','leftpanel','connections','stacks','inputs','neurons',
 *              'outputs','rightpanel'
 * Used by dependent slide 10 (P1 + edge 10<-9): require by ABSOLUTE path.
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 9 : opts.numeral });
  drawTitle(pptx, slide);
  if (!skip.has("leftpanel")) drawLeftPanel(pptx, slide);
  if (!skip.has("connections")) drawConnections(pptx, slide);
  if (!skip.has("stacks")) drawStacks(pptx, slide);
  if (!skip.has("inputs")) drawInputs(pptx, slide);
  if (!skip.has("neurons")) drawNeurons(pptx, slide);
  if (!skip.has("outputs")) drawOutputs(pptx, slide);
  if (!skip.has("rightpanel")) drawRightPanel(pptx, slide);
}

module.exports = { G, C, renderBase, drawTitle, drawLeftPanel, drawConnections,
  drawStacks, drawInputs, drawNeurons, drawOutputs, drawRightPanel };

if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 960 x 540 px
  pres.author = "ai_llm_slides";
  const s = pres.addSlide();
  renderBase(pres, s, { numeral: 9 });
  const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_009_recreated.pptx";
  pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
}
