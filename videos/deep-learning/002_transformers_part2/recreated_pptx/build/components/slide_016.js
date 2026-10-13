// slide_016_r2.js — "Using  FF NN  for Multiplication of Multiple Vectors by Multiple Matrices"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 16)
//
// r2 = watcher-of-record fix build (claim: .claim_builder zcode-worker
// 2026-10-13T01:57:00+03:00, renewed r2). Copy-then-modify of s16-p1-final-0158's
// slide_016.js (its attempt-1 files are untouched banked evidence). Fixes the four
// points of the divergence audit (qa/slide016/OBJECTION_divergence.md, filed over the
// attempt-1 judge PASS per the visual-precision mandate):
//   FIX 1+4 (bracket shape): the frame's brackets are ALL flat PARENS (per-row ink-run
//     profiles: smooth end-drift, NO horizontal arms, bow 7-8 fx) — the pill-wrapper
//     and embed flank brackets are therefore raster parens (s016r2_pil_L/R.png maroon
//     800000, s016r2_emb_L/R.png blue 0000CC; gen_paren_s016_r2.py, same certified
//     raster mechanism as the mat parens), NOT native leftBracket/rightBracket shapes.
//     Matrix parens were already paren-shaped and stay (s016_paren_L/R.png).
//   FIX 2 (output cells): WHITE fills (FFFFFF — measured mode (255,255,250); 009's
//     y-box idiom) + 8B7B3A rims ~1pt (measured cores (76,52,42)/(98,88,63)), NOT
//     group-tinted fills with 404040 rims. The group-tinted ROW PILLS behind the cells
//     are confirmed frame-true (gaps g1 green/g2 peach/g3 lavender) and stay.
//   FIX 3 (right annotation column): both lines CENTER-aligned at cx fx 846.5 (measured
//     line1 ink 816..877, line2 800..893 — the attempt-1 right-align at fx 902 was the
//     house-border column mistaken for text ink); line1 fs 8.5 (61 px ink, not 12.3);
//     line2 = red "Projection of Word " + NAVY 0000CC "#N" runs (39 navy px measured at
//     fx 883..893, (62,44,143) family) at fs 9.5.
// Circle fill minor: RESOLVED transparent (frame shows pill pink through interiors).
//
// PATTERN GROUP P1#5 (FINAL MEMBER; 9/10/12/14 certified). Family idioms (inherited
// from the attempt-1 build, unchanged here):
//   * house chrome via shared shared_patterns/house_chrome.js (badge numeral 16)
//   * matrix cells == 009/012/14-certified treatment (FCF9C8 / 8B7B3A, N9 row colors)
//   * containers == 012-certified tints (D4FCE6 / F8E6D0 / D5D5FB)
//   * big vector names as separate positioned boxes (012 fix12)
//   * tall parentheses via the certified raster mechanism at exact px/600 size
//
// COMPOSITION (MEASURED, scratch/slide016/ m1 m2 m3 g1-g4 v1 t2-t9 + r2 audit;
// frame px 1px=1pt, THIS-frame deck mapping slide_x=(fx-17.582)/0.962329,
// slide_y=fy/0.955556): see the attempt-1 header + OBJECTION_divergence.md.

const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);
const N9 = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_009.js"
);
const pptxgen = require("pptxgenjs");

const FONT = "Arial";

// ---- palette (frame-measured / family-certified) ------------------------------------
const C = {
  inkRed: "C00000",
  blue: "0000CC",          // deep blue family (014-certified; annotation "#N" runs measured (62,44,143))
  magenta: "CC00CC",       // X_N vector names (012-certified)
  panel: "F2F1EF",
  panelRim: "D0D5DA",
  pillPink: "FFE3F9",
  cellFill: N9.C.cellFill, // FCF9C8 (matrix cells)
  cellRim: N9.C.cellRim,   // 8B7B3A — ALSO the output-cell rim (r2 fix 2; measured cores)
  outCellFill: "FFFFFF",   // output cells white (r2 fix 2; measured mode (255,255,250))
  green: "D4FCE6",
  orange: "F8E6D0",
  lavender: "D5D5FB",
};

// ---- mapping (THIS frame's deck fit, m1_chrome_output.txt) ---------------------------
const fx2sx = (fx) => (fx - 17.582) / 0.962329;
const fy2sy = (fy) => fy / 0.955556;
const px = (v) => v / 72;
const R = (t, o = {}) => ({ text: t, options: o });
const SUB = (t, o = {}) => ({ text: t, options: Object.assign({ subscript: true }, o) });

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/";

// ---- measured geometry, frame px ----------------------------------------------------
const G = {
  title: { cx: 460.5, capTop: 56, fs: 21.25 },
  sub: { cx: 479, capTop: 80, fs: 17.9 },
  panelU: { x: 72, y: 111, w: 729, h: 206 },
  panelL: { x: 264, y: 322, w: 633, h: 192 },
  // r2 fix 1+4: embed flanks are flat paren IMAGES (frame: apex 158..159/298..300,
  // ends 164..166/292..296, bow 7-8 fx, ink fy 133..315; boxes carry 2px pad)
  embedParenL: { x: 155, y: 131, wPt: 14.5480, hPt: 194.6511 },
  embedParenR: { x: 290, y: 131, wPt: 13.5089, hPt: 194.6511 },
  embedRows: {
    pillX: 163, pillW: 132, pillH: 32.5, tops: [134.5, 171, 207.5, 244, 280.5],
    circleCxs: [188.5, 215.5, 240, 264.5], circleD: 22.5,
    labX: 72, labW: 84, l1CapTop: 139, l2CapTop: 151,
    xCx: 137, xCapTop: 146, xCapBot: 156, subCx: 145.5, subTop: 155, subBot: 159.5,
  },
  containers: [
    { x: 311, y: 132, w: 146, h: 176, fill: C.green,    hcx: 386.5 },
    { x: 476, y: 131, w: 147, h: 178, fill: C.orange,   hcx: 547 },
    { x: 637, y: 131, w: 146, h: 178, fill: C.lavender, hcx: 709.5 },
  ],
  headerParts: [
    { wCx: 359, kCx: 366.5, ofX: 371 },
    { wCx: 519, kCx: 526.5, ofX: 531 },
    { wCx: 682, kCx: 689.5, ofX: 694 },
  ],
  header: { capCy: 122, kCy: 128.5, fsW: 12, fsK: 7, fs: 11.5 },
  cells: {
    cols: [[317, 353, 390, 424], [483, 519, 557, 590], [643, 679, 717, 750]],
    cw: 26.5, rowTops: [151.5, 189, 230.5, 269], ch: 18.5,
  },
  parenL: { x: 302, y: 126, wPt: 20.7829, hPt: 193.6046 },
  parenR: { x: 774, y: 126, wPt: 19.7438, hPt: 193.6046 },
  equals: { cx: 274, cy: 409, fs: 26 },
  // r2 fix 1: output wrapper flanks are flat paren IMAGES (frame: apex 295..297/788..790,
  // ends 300..303/781..785, bow 8 fx, ink fy 335..481)
  outParenL: { x: 293, y: 333, wPt: 13.5089, hPt: 156.9767 },
  outParenR: { x: 779, y: 333, wPt: 14.5480, hPt: 156.9767 },
  outCells: {
    lefts: [[311.5, 348, 383.5, 419.5], [475, 511, 546.5, 582], [636.5, 673, 709, 745]],
    cw: 24, rowTops: [337, 367.5, 397.5, 428, 458], ch: 19.5,
    pillFills: [C.green, C.orange, C.lavender],  // row pills BEHIND cells (frame-true)
  },
  captions: { cxs: [366.5, 566.5, 735.5], l1CapTop: 486, l2CapTop: 498, fs1: 11, fs2: 10.4 },
  // r2 fix 3: annotations CENTER-aligned at cx 846.5; line1 fs 8.5 red; line2 red +
  // navy "#N" (frame: line1 ink 816..877, line2 red 800..879 + navy 883..893)
  annots: { cx: 846.5, pitch: 29.9, l1CapTop: 341, l2CapTop: 351, fs1: 8.5, fs2: 9.5, n: 5 },
  summary: {
    x: 64, y: 417, w: 194, h: 79, bulletCx: 75, bulletD: 4.5,
    lineCapTops: [434, 456, 477], textX: 88, textW: 164, fs: 11,
  },
};

// ---- blocks --------------------------------------------------------------------------
function drawTitle(pres, s) {
  s.addText("Using  FF NN  for Multiplication of Multiple Vectors by Multiple Matrices",
    { x: px(fx2sx(G.title.cx) - 372), y: px(fy2sy(G.title.capTop) - 7),
      w: px(744), h: px(30), align: "center", valign: "middle", bold: true,
      fontSize: G.title.fs, color: C.inkRed, fontFace: FONT, margin: 0 });
}

function drawSubtitle(pres, s) {
  const mainCy = fy2sy(85.75);
  s.addText("Usage: Multiply Vectors of All Words by Multiple  (different) ",
    { x: px(fx2sx(601) - 580), y: px(mainCy - 13), w: px(580), h: px(26),
      align: "right", valign: "middle", bold: true, italic: true, fontSize: G.sub.fs,
      color: C.blue, fontFace: FONT, margin: 0 });
  s.addText("W", { x: px(fx2sx(611) - 12), y: px(fy2sy(85.5) - 12), w: px(24), h: px(24),
    align: "center", valign: "middle", bold: true, italic: true, fontSize: 20.5,
    color: C.blue, fontFace: FONT, margin: 0 });
  s.addText("k", { x: px(fx2sx(622.5) - 5), y: px(fy2sy(93) - 6.5), w: px(10), h: px(13),
    align: "center", valign: "middle", bold: true, fontSize: 12.5, color: C.blue,
    fontFace: FONT, margin: 0 });
  s.addText("  (Keys of Multiple Heads)",
    { x: px(fx2sx(628.5)), y: px(mainCy - 13), w: px(280), h: px(26),
      align: "left", valign: "middle", bold: true, italic: true, fontSize: G.sub.fs,
      color: C.blue, fontFace: FONT, margin: 0 });
}

function drawPanels(pres, s) {
  for (const p of [G.panelU, G.panelL]) {
    s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(p.x)), y: px(fy2sy(p.y)),
      w: px(p.w / 0.962329), h: px(p.h / 0.955556), rectRadius: 0.06,
      fill: { color: C.panel }, line: { color: C.panelRim, width: 1 } });
  }
}

function drawEmbedParens(pres, s) {
  // r2 fix 1+4: blue flat paren images at exact px/600 size (never rescaled)
  s.addImage({ path: ASSETS + "s016r2_emb_L.png",
    x: px(fx2sx(G.embedParenL.x)), y: px(fy2sy(G.embedParenL.y)),
    w: G.embedParenL.wPt / 72, h: G.embedParenL.hPt / 72 });
  s.addImage({ path: ASSETS + "s016r2_emb_R.png",
    x: px(fx2sx(G.embedParenR.x)), y: px(fy2sy(G.embedParenR.y)),
    w: G.embedParenR.wPt / 72, h: G.embedParenR.hPt / 72 });
}

function drawEmbedRows(pres, s) {
  const E = G.embedRows;
  for (let r = 0; r < 5; r++) {
    const top = E.tops[r];
    const dy = top - E.tops[0];
    s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(E.pillX)), y: px(fy2sy(top)),
      w: px(E.pillW / 0.962329), h: px(E.pillH / 0.955556), rectRadius: 0.14,
      fill: { color: C.pillPink }, line: { color: C.inkRed, width: 1.75 } });
    for (let q = 0; q < 4; q++) {
      const cx = E.circleCxs[q], cy = top + 16.3, d = E.circleD;
      s.addShape(pres.ShapeType.ellipse, { x: px(fx2sx(cx - d / 2)), y: px(fy2sy(cy - d / 2)),
        w: px(d), h: px(d), fill: { type: "none" }, line: { color: C.inkRed, width: 1.5 } });
      s.addText([R("X", { fontSize: 10 }), SUB(String(q + 1), { fontSize: 7 })],
        { x: px(fx2sx(cx - d / 2)), y: px(fy2sy(cy - d / 2)), w: px(d), h: px(d),
          align: "center", valign: "middle", bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
    }
    s.addText("Embedding Vector",
      { x: px(fx2sx(77)), y: px(fy2sy(E.l1CapTop + 2 + dy) - 6), w: px(76),
        h: px(12), align: "left", valign: "middle", bold: true, fontSize: 8.2,
        color: C.inkRed, fontFace: FONT, margin: 0 });
    s.addText([R("of Word ", { color: C.inkRed, fontSize: 8.2 }),
               R("#" + (r + 1), { color: C.blue, fontSize: 12 })],
      { x: px(fx2sx(82)), y: px(fy2sy(E.l2CapTop + 2 + dy) - 6.5), w: px(60),
        h: px(13), align: "left", valign: "middle", bold: true,
        fontFace: FONT, margin: 0 });
    s.addText([R("X", { italic: true })],
      { x: px(fx2sx(138) - 9), y: px(fy2sy((E.xCapTop + E.xCapBot) / 2 + dy) - 8.5),
        w: px(18), h: px(17), align: "center", valign: "middle", bold: true, italic: true,
        fontSize: 14.5, color: C.magenta, fontFace: FONT, margin: 0 });
    s.addText(String(r + 1),
      { x: px(fx2sx(E.subCx) - 4), y: px(fy2sy((E.subTop + E.subBot) / 2 + dy) - 5),
        w: px(8), h: px(10), align: "center", valign: "middle", bold: true,
        fontSize: 8.5, color: C.magenta, fontFace: FONT, margin: 0 });
  }
}

function drawContainers(pres, s) {
  for (const p of G.containers) {
    s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(p.x)), y: px(fy2sy(p.y)),
      w: px(p.w / 0.962329), h: px(p.h / 0.955556), rectRadius: 0.06,
      fill: { color: p.fill }, line: { type: "none" } });
  }
}

function drawHeaders(pres, s) {
  for (let i = 0; i < 3; i++) {
    const p = G.headerParts[i], H = G.header;
    s.addText("W", { x: px(fx2sx(p.wCx) - 8), y: px(fy2sy(H.capCy) - 7), w: px(16), h: px(14),
      align: "center", valign: "middle", bold: true, italic: true, fontSize: H.fsW,
      color: C.inkRed, fontFace: FONT, margin: 0 });
    s.addText("k", { x: px(fx2sx(p.kCx) - 4), y: px(fy2sy(H.kCy) - 4.5), w: px(8), h: px(9),
      align: "center", valign: "middle", bold: true, fontSize: H.fsK,
      color: C.inkRed, fontFace: FONT, margin: 0 });
    s.addText([R(" of ", { color: C.inkRed, fontSize: H.fs }),
               R("Head " + (i + 1), { color: C.blue, fontSize: H.fs })],
      { x: px(fx2sx(p.ofX)), y: px(fy2sy(H.capCy) - 7), w: px(70), h: px(14),
        align: "left", valign: "middle", bold: true, fontFace: FONT, margin: 0 });
  }
}

function drawMatrixCells(pres, s) {
  const rowCols = [N9.C.stack1, N9.C.stack2, N9.C.stack3, N9.C.stack4];
  for (let m = 0; m < 3; m++) {
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        const bx = G.cells.cols[m][c], by = G.cells.rowTops[r];
        s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(bx)), y: px(fy2sy(by)),
          w: px(G.cells.cw), h: px(G.cells.ch), rectRadius: 0.03,
          fill: { color: C.cellFill }, line: { color: C.cellRim, width: 0.75 } });
        s.addText([R("W", { fontSize: 9 }), SUB(String(c + 1) + String(r + 1), { fontSize: 7 })],
          { x: px(fx2sx(bx)), y: px(fy2sy(by)), w: px(G.cells.cw), h: px(G.cells.ch),
            align: "center", valign: "middle", bold: true, color: rowCols[r], fontFace: FONT, margin: 0 });
      }
    }
  }
}

function drawParens(pres, s) {
  s.addImage({ path: ASSETS + "s016_paren_L.png",
    x: px(fx2sx(G.parenL.x)), y: px(fy2sy(G.parenL.y)),
    w: G.parenL.wPt / 72, h: G.parenL.hPt / 72 });
  s.addImage({ path: ASSETS + "s016_paren_R.png",
    x: px(fx2sx(G.parenR.x)), y: px(fy2sy(G.parenR.y)),
    w: G.parenR.wPt / 72, h: G.parenR.hPt / 72 });
}

function drawEquals(pres, s) {
  s.addText("=", { x: px(fx2sx(G.equals.cx) - 15), y: px(fy2sy(G.equals.cy) - 15),
    w: px(30), h: px(30), align: "center", valign: "middle", bold: true,
    fontSize: G.equals.fs, color: C.inkRed, fontFace: FONT, margin: 0 });
}

function drawOutCells(pres, s) {
  const O = G.outCells;
  // group-tinted row pills BEHIND the cells (frame-true: gap samples g1 green / g2 peach /
  // g3 lavender; strips fy rowTop-2..+22.5, x g1 298.5..455.5, g2 462.5..636.5, g3 642.5..786.5)
  const pillX = [[298.5, 455.5], [462.5, 636.5], [642.5, 786.5]];
  for (let m = 0; m < 3; m++) {
    for (let r = 0; r < 5; r++) {
      s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(pillX[m][0])),
        y: px(fy2sy(O.rowTops[r] - 2)), w: px((pillX[m][1] - pillX[m][0]) / 0.962329),
        h: px(24.5 / 0.955556), rectRadius: 0.17,
        fill: { color: O.pillFills[m] }, line: { type: "none" } });
    }
  }
  // r2 fix 2: cells WHITE fill + 8B7B3A rim ~1pt (010-certified y-box idiom; measured
  // interiors (255,255,250) mode, rim cores (76,52,42)/(98,88,63))
  for (let m = 0; m < 3; m++) {
    for (let r = 0; r < 5; r++) {
      for (let c = 0; c < 4; c++) {
        const bx = O.lefts[m][c], by = O.rowTops[r];
        s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(bx)), y: px(fy2sy(by)),
          w: px(O.cw), h: px(O.ch), rectRadius: 0.04,
          fill: { color: C.outCellFill }, line: { color: C.cellRim, width: 1 } });
        s.addText([R("y", { fontSize: 11 }), SUB(String(c + 1), { fontSize: 8 })],
          { x: px(fx2sx(bx)), y: px(fy2sy(by)), w: px(O.cw), h: px(O.ch),
            align: "center", valign: "middle", bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
      }
    }
  }
}

function drawOutParens(pres, s) {
  // r2 fix 1: maroon flat paren images at exact px/600 size (replaces native square
  // leftBracket/rightBracket; drawn AFTER the cells/pills so the ends sit over the
  // pill edges as in the frame)
  s.addImage({ path: ASSETS + "s016r2_pil_L.png",
    x: px(fx2sx(G.outParenL.x)), y: px(fy2sy(G.outParenL.y)),
    w: G.outParenL.wPt / 72, h: G.outParenL.hPt / 72 });
  s.addImage({ path: ASSETS + "s016r2_pil_R.png",
    x: px(fx2sx(G.outParenR.x)), y: px(fy2sy(G.outParenR.y)),
    w: G.outParenR.wPt / 72, h: G.outParenR.hPt / 72 });
}

function drawCaptions(pres, s) {
  for (let i = 0; i < 3; i++) {
    const cx = fx2sx(G.captions.cxs[i]);
    s.addText("Corresponding",
      { x: px(cx - 60), y: px(fy2sy(G.captions.l1CapTop + 3.5) - 6.5), w: px(120), h: px(13),
        align: "center", valign: "middle", bold: true, fontSize: G.captions.fs1,
        color: C.inkRed, fontFace: FONT, margin: 0 });
    s.addText([R("Projections at ", { color: C.inkRed }),
               R("Head " + (i + 1), { color: C.blue })],
      { x: px(cx - 60), y: px(fy2sy(G.captions.l2CapTop + 3) - 6.5), w: px(120), h: px(13),
        align: "center", valign: "middle", bold: true, fontSize: G.captions.fs2,
        fontFace: FONT, margin: 0 });
  }
}

function drawAnnotts(pres, s) {
  // r2 fix 3: CENTER-aligned at cx 846.5 (frame: line1 ink 816..877 -> center 846.5;
  // line2 red 800..879 + navy 883..893 -> center 846.5). line1 fs 8.5 (61 px ink);
  // line2 "Projection of Word " red + "#N" NAVY 0000CC, fs 9.5.
  const A = G.annots;
  const cx = fx2sx(A.cx);
  for (let k = 0; k < A.n; k++) {
    s.addText("Corresponding",
      { x: px(cx - 60), y: px(fy2sy(A.l1CapTop + A.pitch * k + 3) - 6), w: px(120), h: px(12),
        align: "center", valign: "middle", bold: true, fontSize: A.fs1, color: C.inkRed,
        fontFace: FONT, margin: 0 });
    s.addText([R("Projection of Word ", { color: C.inkRed }),
               R("#" + (k + 1), { color: C.blue })],
      { x: px(cx - 60), y: px(fy2sy(A.l2CapTop + A.pitch * k + 2.5) - 5.5), w: px(120), h: px(11),
        align: "center", valign: "middle", bold: true, fontSize: A.fs2, fontFace: FONT, margin: 0 });
  }
}

function drawSummary(pres, s) {
  const S = G.summary;
  s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(S.x)), y: px(fy2sy(S.y)),
    w: px(S.w / 0.962329), h: px(S.h / 0.955556), rectRadius: 0.07,
    fill: { color: "FAFBEB" }, line: { color: C.blue, width: 2.25 } });
  for (let i = 0; i < 3; i++) {
    const cy = S.lineCapTops[i] + 3.5;
    s.addShape(pres.ShapeType.ellipse, { x: px(fx2sx(S.bulletCx - S.bulletD / 2)),
      y: px(fy2sy(cy - S.bulletD / 2)), w: px(S.bulletD), h: px(S.bulletD),
      fill: { color: C.blue }, line: { type: "none" } });
    const runs = i === 0 ? [R("Sequence of  ", { color: C.blue }), R("5 Words", { color: C.inkRed })]
      : i === 1 ? [R("Network with  ", { color: C.blue }), R("3 Heads", { color: C.inkRed })]
      : [R("Embedding  Dimension=4", { color: C.blue })];
    s.addText(runs, { x: px(fx2sx(S.textX)), y: px(fy2sy(cy) - 7), w: px(S.textW / 0.962329),
      h: px(14), align: "left", valign: "middle", bold: true, fontSize: S.fs,
      fontFace: FONT, margin: 0 });
  }
}

/**
 * Full composition. opts:
 *   { numeral }  badge numeral (default 16)
 *   { skip }     block names to omit: "title" "subtitle" "panels" "embedRows"
 *                "embedParens" "containers" "headers" "cells" "parens" "equals"
 *                "outCells" "outParens" "captions" "annotts" "summary"
 *   { only }     draw ONLY these blocks
 * Parens (embed flanks, output wrapper) draw AFTER their rows/cells so the paren
 * ends sit over the pill edges exactly as in the frame (r2 z-order).
 */
function renderBase(pres, slide, opts = {}) {
  drawHouseChrome(pres, slide, { numeral: opts.numeral === undefined ? 16 : opts.numeral });
  const skip = Array.isArray(opts.skip) ? opts.skip : [];
  const only = Array.isArray(opts.only) ? opts.only : null;
  const want = (name) => (only ? only.indexOf(name) !== -1 : skip.indexOf(name) === -1);
  if (want("title")) drawTitle(pres, slide);
  if (want("subtitle")) drawSubtitle(pres, slide);
  if (want("panels")) drawPanels(pres, slide);
  if (want("containers")) drawContainers(pres, slide);
  if (want("cells")) drawMatrixCells(pres, slide);
  if (want("headers")) drawHeaders(pres, slide);
  if (want("embedRows")) drawEmbedRows(pres, slide);
  if (want("embedParens")) drawEmbedParens(pres, slide);
  if (want("parens")) drawParens(pres, slide);
  if (want("equals")) drawEquals(pres, slide);
  if (want("outCells")) drawOutCells(pres, slide);
  if (want("outParens")) drawOutParens(pres, slide);
  if (want("captions")) drawCaptions(pres, slide);
  if (want("annotts")) drawAnnotts(pres, slide);
  if (want("summary")) drawSummary(pres, slide);
}

const BLOCKS = ["title", "subtitle", "panels", "embedRows", "embedParens", "containers",
  "headers", "cells", "parens", "equals", "outCells", "outParens", "captions",
  "annotts", "summary"];

module.exports = { G, C, BLOCKS, renderBase, drawTitle, drawSubtitle, drawPanels,
  drawEmbedParens, drawEmbedRows, drawContainers, drawHeaders, drawMatrixCells,
  drawParens, drawEquals, drawOutCells, drawOutParens, drawCaptions, drawAnnotts,
  drawSummary };

if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 960 x 540 px
  pres.author = "ai_llm_slides";
  const s = pres.addSlide();
  renderBase(pres, s, { numeral: 16 });
  const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_016_recreated.pptx";
  pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
}

// SHIP-RENAME NOTE (close-out 2026-10-13 05:15): certified build is slide_016_r2.js
// (judge_attempt_3.txt). This entry is the SAME builder with OUT set to the plain
// single-version deliverable name; foreign builder attempt-1 archived at
// qa/slide016/foreign_build_attempt1.js + foreign_attempt1_overridden.pptx.
