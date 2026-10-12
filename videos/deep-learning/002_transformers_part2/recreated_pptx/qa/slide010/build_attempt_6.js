// slide_010.js — "Using  FF NN  for Multiplication of ONE Vector by a Matrix"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 10)
//
// PATTERN GROUP P1#2 (after certified head 9) + CONFIRMED DEPENDENT 10 <- 9.
// Pattern verified against THIS frame (scratch/slide010/measure1/2/3_output.txt):
//   * LEFT-NETWORK BLOCKS IDENTICAL to 009's certified geometry (frame->slide mapping
//     slide_x=(fx-17.628)/0.961232, slide_y=fy/0.955556):
//       inputs  frame c=(101, 156.5/263/368/467.5) -> sx (86.8, 163.8/275.2/385.1/489.2)
//               vs 009 G (88.8, 164.3/275.2/386.2/489.8)  -> within ~2px -> IMPORT
//       neurons frame cy 160/262.5/368/468 -> sy 167.4/274.7/385.1/489.8; n1 row-scan
//               cx 232.5fx -> sx 223.5 vs 009 224.0               -> IMPORT geometry
//       weight stacks row bands == 009 patches (W11 156..162 vs 154..164 etc.) -> IMPORT
//   * MEASURED DELTAS drawn by THIS module (frame wins over 009):
//       - left panel border DARK NAVY (22167E, cores (34,21,129)) vs 009 gray CFD6DC
//       - neurons: center divider + right-half diagonal hatch + halftone dotted circle
//         below; Sigma sits LEFT of divider (009 centered it) -> own drawNeurons10
//       - outputs: GREEN arrow, NO b_i, NO b-arrow (009 had b); y_i labels RED at 009's
//         certified geometry (attempt-6 frame scan: glyphs+subscripts red, arrow green)
//       - title smaller (caps fy 52..66 -> fs 22) + ONE added; NEW subtitle line
//       - TWO stacked mid panels (fill F2F1EF, blue border) + TWO stacked right panels
//       - panel2 = panel1 + 224 slide px (measured deltas 223.8..224.9)
//   * OMITTED AS VIDEO-CAPTURE ARTIFACTS (GROUND RULES (c), spec uncertain_items):
//       black bottom bar rows 518..539 (player progress bar, below chrome bottom 517).
// CONTENT SPEC: analysis/slide_010_final.json (PASS_WITH_FIXES, score 9). Badge = 10.

const { CHROME, drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);
const N9 = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_009.js"
);
const pptxgen = require("pptxgenjs");

const FONT = "Arial";
const SERIF = "Times New Roman"; // Y^T / X display letters are serif bold red in the frame

// ---- frame-measured palette (scratch/slide010/measure*_output.txt) ----------------
const C = {
  titleRed: "C00000",
  inkRed: "C00000",
  navyBorder: "22167E",  // left panel border cores (34,21,129)/(29,20,129)
  panelBlue: "4A3EC4",   // mid/right panel border, bluest core (78,64,203) saturated
  panelFill: "F2F1EF",   // mid+right panel fill (242,241,239) n=large
  braceBlue: "4237B8",   // curly braces (62,50,150) core saturated
  sigmoidBlue: "2438C8", // "= Sigmoid" / "= Linear"
  stadiumPink: "FBCCEF", // pill/stadium fill (248,204,231)/(250,202,254)
  stadiumRim: "E8A8DC",
  boxFill: "FFF7EC",     // y-box fill (255,249,243)
  boxRim: "9C3444",      // y-box rims (144..151, 36..46, 52..58) saturated
  green: "2E9C48",       // y labels + arrows (009's certified green)
  mint: "D8FFE6",        // matrix container (009 value, matches (211,255,231))
  grid: "9CD4AC",
  cellFill: "FCF9C8",    // matrix cells + bias boxes (009 value; (248,254,192))
  cellRim: "8B7B3A",
  parenRed: "A23038",    // bias parens core (100,45,48) saturated
  hatch: "B8B8B8",
  divider: "909090",
  haloFill: "F2F2F2",
  haloRim: "C0C0C0",
};

const fx2sx = (fx) => (fx - 17.628) / 0.961232;
const fy2sy = (fy) => fy / 0.955556;
const px = (v) => v / 72;
const R = (t, o = {}) => ({ text: t, options: o });
const SUB = (t, o = {}) => ({ text: t, options: Object.assign({ subscript: true }, o) });

// ---- measured geometry, slide px ---------------------------------------------------
const G = {
  title: { cx: 480, capTop: 54.4, capBot: 69.1, fs: 22 },
  sub: { y: 76.5, h: 30, fs: 18.5 },
  leftPanel: { x: 64.9, y: 105.7, w: 205.5, h: 428.0 }, // fx 80..277.5, fy 101..510
  header: { x: 77, y: 114.2, w: 132, h: 26 },
  mid1: { x: 279.9, y: 102.6, w: 239.5, h: 207.7 },  // fx 287..517.5, fy 98..296.5
  mid2: { x: 279.9, y: 327.0, w: 239.5, h: 207.8 },  // fy 312.5..511
  right1: { x: 526.1, y: 101.5, w: 389.5, h: 207.7 }, // fx 523.5..898, fy 97..295.5
  right2: { x: 526.1, y: 326.0, w: 389.5, h: 207.8 }, // fy 311..510
  yOff: 224.4, // panel2 = panel1 + measured delta
  ytY: { x: 352.0, y: 157.0, w: 22, h: 26 },  // serif Y: fx 358..374, caps fy 155..170
  ytT: { x: 372.5, y: 160.4, w: 9, h: 12 },   // superscript T: fx 376..381, fy 155..163
  bracketL: { x: 285.0, y: 178.5, w: 12, h: 43.5 },  // ink target fy ~174..220 (stadium+4)
  bracketR: { x: 440.4, y: 178.5, w: 12, h: 43.5 },  // fx 441..445
  stadium: { x: 293.9, y: 186.3, w: 144.5, h: 39.8 },// fx 300..439, fy 178..216
  yBoxes: { x0: 305.9, dy: 32.3, w: 23.9, h: 20.9, y: 198.8 }, // fx L 312+31i w23
  sigmoid: { x: 446, y: 193.6, w: 72, h: 26 },       // "= Sigmoid" ink fx 450..511 (row-scan)
  linear: { x: 446, y: 417.4, w: 72, h: 26 },        // "= Linear" (same x as sigmoid + 214fy)
  braceL: { x: 525.3, y: 110.9 },  // bezier PNG: ink-left (vertex) at fx 524-1, top fy 106
  braceR: { x: 835.3, y: 110.9 },  // bezier PNG: ink-right (vertex) at fx ~834.5, top fy 106
  pill: { x: 540.4, y: 108.8, w: 129.7, h: 39.8 },   // fx 537..662 (strict-pink rows), fy 104..142
  xBracketL: { x: 544.9, y: 107.5, w: 10, h: 33 },
  xBracketR: { x: 659.0, y: 107.5, w: 10, h: 33 },
  xCircles: { cxs: [566.4, 592.4, 618.3, 644.3], cy: 128.7, d: 21 },
  bigX: { cx: 598.1, boxY: 156.0 },                  // fx 587..598, fy 153..167
  matrix: { x: 679.5, y: 123.5, w: 156.0, h: 170.0 },// fx ~669..820, fy 119..281
  mCells: { cxs: [707.4, 741.1, 774.9, 808.6], cys: [154.9, 190.5, 226.1, 261.7], w: 32, h: 34 },
  mGridH: [172.7, 208.3, 243.9],
  mGridV: [724.2, 758.0, 791.7],
  plus: { cx: 860.3, cy: 206.7 },                    // fx ~844, fy ~197.5
  parens: { l: 866.9, r: 906.1, y: 122.4, h: 182.0, w: 9 }, // fx 851 / 890, fy 117..291
  bBoxes: { x: 872.2, w: 31.0, h: 22.0, cys: [143.4, 182.1, 225.5, 265.8] },
  bBoxes2: { cys: [367.3, 407.0, 449.4, 490.2] },    // measured panel-2 centers
  arrowC: { x: 475.3, y: 219.8, h: 214.5, w: 5 },    // shaft fx 474.5, fy 210..415
  arrowR: { x: 884.8, y: 279.4, h: 78.5, w: 4 },     // shaft fx 868, fy 267..342
  callout1: { x: 414.1, y: 294.0, w: 110.3, h: 38.7 }, // fx 416..522, fy 281..318
  callout2: { x: 805.5, y: 306.6, w: 92.6, h: 22.0 },  // fx 792..881, fy 293..314
};

// ---- chrome + headers ----------------------------------------------------------------
function drawTitle(pres, s) {
  s.addText(
    [R("Using  FF NN  for Multiplication of ONE Vector by a Matrix", {})],
    { x: px(G.title.cx - 371), y: px(G.title.capTop - 7.2), w: px(742), h: px(30),
      align: "center", valign: "middle", bold: true, fontSize: G.title.fs,
      color: C.titleRed, fontFace: FONT, margin: 0 }
  );
}

function drawSubtitle(pres, s) {
  // fx 107..851, caps fy ~80..95, underline fy 100 under "Vector of Current Word"
  const B = { bold: true, italic: true, fontSize: G.sub.fs, color: "1F3EC8", fontFace: FONT };
  s.addText([
    R("Example: Multiply ", B),
    R("Vector of Current Word ", Object.assign({}, B, { underline: true })),
    R("X", { bold: true, fontSize: 22, color: C.inkRed, fontFace: SERIF }),
    R(" by ", B),
    R("W", Object.assign({}, B, { color: C.inkRed })),
    SUB("q", { fontSize: 11, color: C.inkRed, bold: true, italic: true }),
    R(" (Query) ", B),
    R("{Remember: W", Object.assign({}, B, { color: "1E9C46" })),
    SUB("q", { fontSize: 11, color: "1E9C46", bold: true, italic: true }),
    R(" is Squared Matrix}", Object.assign({}, B, { color: "1E9C46" })),
  ], { x: px(60), y: px(G.sub.y), w: px(840), h: px(G.sub.h), align: "center",
       valign: "middle", fontFace: FONT, margin: 0 });
}

function drawLeftPanel(pres, s) {
  const p = G.leftPanel;
  s.addShape(pres.ShapeType.roundRect, {
    x: px(p.x), y: px(p.y), w: px(p.w), h: px(p.h), rectRadius: 0.06,
    fill: { color: "FFFFFF" }, line: { color: C.navyBorder, width: 1.5 },
  });
  // header: fx 93..196, caps fy 115..128 -> "Input Word" blkack ~17pt + X red ~22pt
  s.addText([R("Input Word ", { fontSize: 17, color: "000000" }),
             R("X", { fontSize: 22, color: C.inkRed })],
    { x: px(G.header.x), y: px(G.header.y), w: px(G.header.w), h: px(G.header.h),
      align: "left", valign: "middle", bold: true, fontFace: FONT, margin: 0 });
}

// ---- neurons (own: divider + hatch + Sigma-left; geometry = 009's certified) --------
function drawNeurons10(pres, s) {
  for (const [cx, cy] of N9.G.neurons.c) {
    s.addShape(pres.ShapeType.ellipse, {
      x: px(cx - 17.25), y: px(cy - 17.25), w: px(34.5), h: px(34.5),
      fill: { color: "FFFFFF" }, line: { color: C.inkRed, width: 1.5 },
    });
    // multicolor pie at left rim (as 009)
    const pies = [[90, 210, N9.C.stack1], [210, 330, N9.C.stack2], [330, 90, N9.C.stack4]];
    for (const [a0, a1, col] of pies) {
      s.addShape(pres.ShapeType.pie, {
        x: px(cx - 16.5), y: px(cy - 4), w: px(8), h: px(8), angleRange: [a0, a1],
        fill: { color: col }, line: { type: "none" },
      });
    }
    // right-half diagonal hatch: chords of x+y=d (45deg "/" strokes)
    for (const d of [4, 8, 12, 16, 19.5]) {
      const rr = 14, s2 = Math.sqrt(2 * rr * rr - d * d);
      if (s2 <= 0) continue;
      const u1 = (d - s2) / 2, u2 = (d + s2) / 2;
      s.addShape(pres.ShapeType.line, {
        x: px(cx + u1), y: px(cy + d - u2), w: px(u2 - u1), h: px(u2 - u1),
        line: { color: C.hatch, width: 0.75 },
      });
    }
    // center divider + Sigma left of it
    s.addShape(pres.ShapeType.line, {
      x: px(cx), y: px(cy - 14), w: 0, h: px(28),
      line: { color: C.divider, width: 1 },
    });
    s.addText("\u03A3", { x: px(cx - 15), y: px(cy - 10), w: px(15), h: px(20),
      align: "center", valign: "middle", bold: true, fontSize: 14, color: "1A1A1A",
      fontFace: FONT, margin: 0 });
    // halftone dotted circle below (frame: center cx+5.3, cy+27.8, d~25)
    s.addShape(pres.ShapeType.ellipse, {
      x: px(cx + 5.3 - 12.5), y: px(cy + 27.8 - 12.5), w: px(25), h: px(25),
      fill: { color: C.haloFill }, line: { color: C.haloRim, width: 0.75, dashType: "sysDot" },
    });
  }
}

// ---- outputs (own: NO b_i/b-arrow; labels = 009-certified treatment) -----------------
// MEASURED FIX (attempt 6, frame scan fx 248..274 fy 144..176): y_i glyphs + subscripts
// are RED (cores (125,15,26)/(143,33,46)), NOT green — only the arrow is green. Label
// geometry == 009's 0-px-verified drawOutputs: 19pt red at (cx+18, cy-26.5) valign top
// (slide-10 ink top fy 144 -> sy 150.7 = cy-16.7 == 009's certified cy-17 ink top).
function drawOutputs10(pres, s) {
  const labels = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const [cx, cy] = N9.G.neurons.c[i];
    s.addShape(pres.ShapeType.line, {
      x: px(cx + 18), y: px(cy), w: px(23), h: 0,
      line: { color: C.green, width: 1.75, endArrowType: "triangle" },
    });
    // y_i RED label above the arrow end (009-certified geometry, frame-verified)
    s.addText([R("y", { fontSize: 19 }), SUB(labels[i], { fontSize: 10.5 })],
      { x: px(cx + 18), y: px(cy - 26.5), w: px(26), h: px(24), align: "left", valign: "top",
        bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
  }
}

// ---- one middle panel row (Y^T + bracketed y-boxes + = Sigmoid/Linear) ---------------
function drawMidRow(pres, s, yOff, word) {
  s.addText("Y", { x: px(G.ytY.x), y: px(G.ytY.y + yOff), w: px(G.ytY.w), h: px(G.ytY.h),
    align: "center", valign: "middle", bold: true, fontSize: 22, color: C.inkRed,
    fontFace: SERIF, margin: 0 });
  s.addText("T", { x: px(G.ytT.x), y: px(G.ytT.y + yOff), w: px(G.ytT.w), h: px(G.ytT.h),
    align: "center", valign: "middle", bold: true, fontSize: 11, color: C.inkRed,
    fontFace: SERIF, margin: 0 });
  s.addText("[", { x: px(G.bracketL.x), y: px(G.bracketL.y + yOff), w: px(G.bracketL.w), h: px(G.bracketL.h),
    align: "center", valign: "middle", fontSize: 46, color: C.inkRed, fontFace: FONT, margin: 0, fit: "none" });
  s.addText("]", { x: px(G.bracketR.x), y: px(G.bracketR.y + yOff), w: px(G.bracketR.w), h: px(G.bracketR.h),
    align: "center", valign: "middle", fontSize: 46, color: C.inkRed, fontFace: FONT, margin: 0, fit: "none" });
  const st = G.stadium;
  s.addShape(pres.ShapeType.roundRect, { x: px(st.x), y: px(st.y + yOff), w: px(st.w), h: px(st.h),
    rectRadius: 0.18, fill: { color: C.stadiumPink }, line: { color: C.stadiumRim, width: 1 } });
  const ysub = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const bx = G.yBoxes.x0 + i * G.yBoxes.dy, by = G.yBoxes.y + yOff;
    s.addShape(pres.ShapeType.roundRect, { x: px(bx), y: px(by), w: px(G.yBoxes.w), h: px(G.yBoxes.h),
      rectRadius: 0.05, fill: { color: C.boxFill }, line: { color: C.boxRim, width: 1.25 } });
    s.addText([R("y", { fontSize: 11 }), SUB(ysub[i], { fontSize: 8 })],
      { x: px(bx), y: px(by), w: px(G.yBoxes.w), h: px(G.yBoxes.h), align: "center",
        valign: "middle", bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
  }
  const fn = G[word];
  s.addText(word === "sigmoid" ? "= Sigmoid" : "= Linear",
    { x: px(fn.x), y: px(fn.y), w: px(fn.w), h: px(fn.h), align: "center", valign: "middle",
      bold: true, italic: true, fontSize: 16, color: C.sigmoidBlue, fontFace: FONT, margin: 0 });
}

// ---- one right panel (braceL, X pill, matrix, braceR, +, bias column) ----------------
function drawRightPanel(pres, s, yOff, biasLabels) {
  s.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/s010_braceL.png",
    x: px(G.braceL.x), y: px(G.braceL.y + yOff), w: 0.2083, h: 2.68 });
  const p = G.pill;
  s.addShape(pres.ShapeType.roundRect, { x: px(p.x), y: px(p.y + yOff), w: px(p.w), h: px(p.h),
    rectRadius: 0.14, fill: { color: C.stadiumPink }, line: { color: C.stadiumRim, width: 1 } });
  s.addText("[", { x: px(G.xBracketL.x), y: px(G.xBracketL.y + yOff), w: px(G.xBracketL.w), h: px(G.xBracketL.h),
    align: "center", valign: "middle", fontSize: 34, color: C.inkRed, fontFace: FONT, margin: 0, fit: "none" });
  s.addText("]", { x: px(G.xBracketR.x), y: px(G.xBracketR.y + yOff), w: px(G.xBracketR.w), h: px(G.xBracketR.h),
    align: "center", valign: "middle", fontSize: 34, color: C.inkRed, fontFace: FONT, margin: 0, fit: "none" });
  const xsub = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const cx = G.xCircles.cxs[i], cy = G.xCircles.cy + yOff, d = G.xCircles.d;
    s.addShape(pres.ShapeType.ellipse, { x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
      fill: { color: "FFFFFF" }, line: { color: C.inkRed, width: 1.5 } });
    s.addText([R("x", { fontSize: 10 }), SUB(xsub[i], { fontSize: 7.5 })],
      { x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d), align: "center",
        valign: "middle", bold: true, color: "111111", fontFace: FONT, margin: 0 });
  }
  s.addText("X", { x: px(G.bigX.cx - 20), y: px(G.bigX.boxY + yOff), w: px(40), h: px(26),
    align: "center", valign: "middle", bold: true, fontSize: 22, color: C.inkRed,
    fontFace: SERIF, margin: 0 });
  // matrix: mint container + gridlines + 16 cells
  const m = G.matrix;
  s.addShape(pres.ShapeType.roundRect, { x: px(m.x), y: px(m.y + yOff), w: px(m.w), h: px(m.h),
    rectRadius: 0.08, fill: { color: C.mint }, line: { color: C.grid, width: 0.75 } });
  for (const gy of G.mGridH) s.addShape(pres.ShapeType.line, {
    x: px(m.x), y: px(gy + yOff), w: px(m.w), h: 0, line: { color: C.grid, width: 0.5 } });
  for (const gx of G.mGridV) s.addShape(pres.ShapeType.line, {
    x: px(gx), y: px(m.y + yOff), w: 0, h: px(m.h), line: { color: C.grid, width: 0.5 } });
  const msub = [["11", "21", "31", "41"], ["12", "22", "32", "42"],
                ["13", "23", "33", "43"], ["14", "24", "34", "44"]];
  const mcols = [N9.C.stack1, N9.C.stack2, N9.C.stack3, N9.C.stack4];
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      const bx = G.mCells.cxs[c] - G.mCells.w / 2, by = G.mCells.cys[r] + yOff - G.mCells.h / 2;
      s.addShape(pres.ShapeType.roundRect, { x: px(bx), y: px(by), w: px(G.mCells.w), h: px(G.mCells.h),
        rectRadius: 0.05, fill: { color: C.cellFill }, line: { color: C.cellRim, width: 1 } });
      s.addText([R("W", { fontSize: 9 }), SUB(msub[r][c], { fontSize: 7 })],
        { x: px(bx), y: px(by), w: px(G.mCells.w), h: px(G.mCells.h), align: "center",
          valign: "middle", bold: true, color: mcols[r], fontFace: FONT, margin: 0 });
    }
  }
  s.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/s010_braceR.png",
    x: px(G.braceR.x), y: px(G.braceR.y + yOff), w: 0.21, h: 2.68 });
  s.addText("+", { x: px(G.plus.cx - 10), y: px(G.plus.cy + yOff - 12), w: px(20), h: px(24),
    align: "center", valign: "middle", bold: true, fontSize: 18, color: C.inkRed,
    fontFace: FONT, margin: 0 });
  // bias column: tall red parens + yellow boxes
  s.addShape(pres.ShapeType.arc, { x: px(G.parens.l - G.parens.w / 2), y: px(G.parens.y + yOff),
    w: px(G.parens.w), h: px(G.parens.h), angleRange: [90, 270],
    fill: { type: "none" }, line: { color: C.parenRed, width: 2 } });
  s.addShape(pres.ShapeType.arc, { x: px(G.parens.r - G.parens.w / 2), y: px(G.parens.y + yOff),
    w: px(G.parens.w), h: px(G.parens.h), angleRange: [270, 450],
    fill: { type: "none" }, line: { color: C.parenRed, width: 2 } });
  const cys = yOff === 0 ? G.bBoxes.cys : G.bBoxes2.cys;
  for (let i = 0; i < 4; i++) {
    const by = cys[i] - G.bBoxes.h / 2;
    s.addShape(pres.ShapeType.roundRect, { x: px(G.bBoxes.x), y: px(by), w: px(G.bBoxes.w), h: px(G.bBoxes.h),
      rectRadius: 0.05, fill: { color: C.cellFill }, line: { color: C.cellRim, width: 1 } });
    const lab = biasLabels[i];
    s.addText(lab.length > 1 ? [R(lab[0], { fontSize: 11 }), SUB(lab[1], { fontSize: 8 })]
                             : [R(lab, { fontSize: 11 })],
      { x: px(G.bBoxes.x), y: px(by), w: px(G.bBoxes.w), h: px(G.bBoxes.h), align: "center",
        valign: "middle", bold: true, color: "1A1A1A", fontFace: FONT, margin: 0 });
  }
}

// ---- arrows + callouts ---------------------------------------------------------------
function drawArrows(pres, s) {
  s.addShape(pres.ShapeType.line, {
    x: px(G.arrowC.x), y: px(G.arrowC.y), w: 0, h: px(G.arrowC.h),
    line: { color: C.inkRed, width: G.arrowC.w, endArrowType: "triangle" },
  });
  s.addShape(pres.ShapeType.line, {
    x: px(G.arrowR.x), y: px(G.arrowR.y), w: 0, h: px(G.arrowR.h),
    line: { color: C.inkRed, width: G.arrowR.w, endArrowType: "triangle" },
  });
}

function drawCallouts(pres, s) {
  const c1 = G.callout1;
  s.addShape(pres.ShapeType.roundRect, { x: px(c1.x), y: px(c1.y), w: px(c1.w), h: px(c1.h),
    rectRadius: 0.08, fill: { color: "000000" }, line: { color: "000000", width: 0.5 } });
  s.addText([R("IF No", { breakLine: true }), R("Non-linearity", {})],
    { x: px(c1.x), y: px(c1.y), w: px(c1.w), h: px(c1.h), align: "center", valign: "middle",
      bold: true, fontSize: 11, color: "FFFFFF", fontFace: FONT, margin: 0, lineSpacing: 13 });
  const c2 = G.callout2;
  s.addShape(pres.ShapeType.roundRect, { x: px(c2.x), y: px(c2.y), w: px(c2.w), h: px(c2.h),
    rectRadius: 0.08, fill: { color: "000000" }, line: { color: "000000", width: 0.5 } });
  s.addText("IF No Bias",
    { x: px(c2.x), y: px(c2.y), w: px(c2.w), h: px(c2.h), align: "center", valign: "middle",
      bold: true, fontSize: 11, color: "FFFFFF", fontFace: FONT, margin: 0 });
}

/**
 * Full composition. opts: { numeral (default 10) }
 * Importable by P1 members (12/14/16) only as PATTERN reference — geometry is
 * slide-10-specific (verify against your own frame; do not clone).
 */
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 10 : opts.numeral });
  drawTitle(pptx, slide);
  drawSubtitle(pptx, slide);
  drawLeftPanel(pptx, slide);
  N9.drawConnections(pptx, slide);
  N9.drawStacks(pptx, slide);
  N9.drawInputs(pptx, slide);
  drawNeurons10(pptx, slide);
  drawOutputs10(pptx, slide);
  // panels
  for (const [pan, yOff] of [[G.mid1, 0], [G.mid2, G.yOff]]) {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(pan.x), y: px(pan.y), w: px(pan.w), h: px(pan.h), rectRadius: 0.1,
      fill: { color: C.panelFill }, line: { color: C.panelBlue, width: 1.25 },
    });
  }
  for (const [pan, yOff] of [[G.right1, 0], [G.right2, G.yOff]]) {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(pan.x), y: px(pan.y), w: px(pan.w), h: px(pan.h), rectRadius: 0.1,
      fill: { color: C.panelFill }, line: { color: C.panelBlue, width: 1.25 },
    });
  }
  drawMidRow(pptx, slide, 0, "sigmoid");
  drawMidRow(pptx, slide, G.yOff, "linear");
  drawRightPanel(pptx, slide, 0, ["b1", "b2", "b3", "b4"]);
  drawRightPanel(pptx, slide, G.yOff, ["0", "0", "0", "0"]);
  drawArrows(pptx, slide);
  drawCallouts(pptx, slide);
}

module.exports = { G, C, renderBase, drawTitle, drawSubtitle, drawLeftPanel,
  drawNeurons10, drawOutputs10, drawMidRow, drawRightPanel, drawArrows, drawCallouts };

if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 960 x 540 px
  pres.author = "ai_llm_slides";
  const s = pres.addSlide();
  renderBase(pres, s, { numeral: 10 });
  const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_010_recreated.pptx";
  pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
}
