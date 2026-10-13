// slide_016.js — "Using  FF NN  for Multiplication of Multiple Vectors by Multiple Matrices"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 16)
//
// PATTERN GROUP P1#5 (FINAL MEMBER; 9/10/12/14 certified). Pattern reuse, NOT content
// dependency. Family idioms applied:
//   * house chrome via shared shared_patterns/house_chrome.js (badge numeral 16 —
//     048-protocol verified: tens IoU 1.000 vs '1', units 0.911 vs '6' vs 0.688 max '9')
//   * matrix cells == 009/012/14-certified treatment (fill FCF9C8, olive rim 8B7B3A,
//     bold W + two-digit subscript, row text colors = N9.C.stack1..4). MEASURED on this
//     frame too (m3/g2): ALL 48 cell fills pale-yellow #FFFBC0-#FDFFD6; row text
//     families blue/purple/ORANGE/green — spec's "row1 yellow/row2 pink/row3 orange/
//     row4 green fills" is WRONG, frame wins (same correction as slide 14's worker).
//   * containers == 012-certified tints (D4FCE6 / F8E6D0 / D5D5FB; measured
//     #D8FFE6 / #F8E6D0 / #D5D5F9)
//   * output cells == 010-certified y-box idiom (red y + red sub, centered) with
//     group-tinted fills; borders thin dark 404040 (measured median #B2A39A = 1px
//     dark border JPEG-washed on tinted fills)
//   * big vector names as separate positioned boxes (012 fix12: LO renders
//     baseline-attr runs at 58% — separate boxes keep PowerPoint == LibreOffice)
//   * tall parentheses around the matrices via the certified raster mechanism
//     (gen_paren_s016.py -> s016_paren_L/R.png at exact px/600 size)
//
// COMPOSITION (MEASURED, scratch/slide016/ m1 m2 m3 g1-g4 v1 t2-t9 + vision reads
// vision_subtitle/headers_captions/labels_summary_annot/xname .txt; frame px 1px=1pt,
// THIS-frame deck mapping slide_x=(fx-17.582)/0.962329, slide_y=fy/0.955556):
//   upper panel fx 72..801 fy 111..317 (fill F2F1EF, rim D0D5DA) — embeddings AND
//     matrices in ONE panel; lower panel fx 264..897 fy 322..514 (same treatment)
//   title ink fx 116..805 caps fy 56..71 (fs 20.5 metric-fit; Arial-bold 34.9em)
//   subtitle ink fx 122..836 caps fy 80..91 — ALL deep blue 0000CC (cores #090066),
//     bold italic, W italic + sub k; VERBATIM "Usage: Multiply Vectors of All Words
//     by Multiple  (different) W_k  (Keys of Multiple Heads)" (double spaces; the 5
//     tiny red marks above it are TITLE DESCENDERS, not subtitle runs — vision read)
//   embedding rows (5, pitch 36.5): blue [ ] brackets fx 157..160/297..300 fy 133..315
//     (arms ~14px inward); pink pill fx 163..295 h 32.5 (fill FFE3F9, C00000 rim);
//     4 TRANSPARENT circles d22.5 cx [188.5,215.5,240,264.5] C00000 rims + bold X_i
//     (C00000; measured rose = C00000 washed by pink pill bleed); label L1
//     "Embedding Vector" (red fs 7.5, caps fy 139..143) / L2 "of Word " (red) + "#1"
//     (BLUE 0000CC — 8x vision read) + big italic X_i (CC00CC fs 14.5, cores #AA52AC
//     == CC00CC washed) + sub (CC00CC)
//   matrix headers "W_k of Head N": red "W_k of " + blue "Head N" (vision read), caps
//     fy 118..126, ink centers fx 386.5/547/709.5
//   3 containers + 16 cells each (cols H1 [317,353,390,424] H2 [483,519,557,590]
//     H3 [643,679,717,750] w26.5; rows fy [151.5,189,230.5,269] h18.5)
//   tall ( ) around all three matrices: L ink fx 306..315, R fx 782..790, fy 128..309
//     (middle apex outward-facing... inward apex: L middle-leftmost, R middle-rightmost
//     — normal parentheses; the spec's "[?] brace" = these)
//   "=" fx 268..280 bars fy 404..414 (fs 26 bold red); the vertical red stroke at
//     fx 295..297 fy 339..477 is the OUTPUT BLOCK's left bracket, not part of "="
//   output block: 3 groups x 5 rows x 4 cells (lefts g1 [311.5,348,383.5,419.5],
//     g2 [475,511,546.5,582], g3 [636.5,673,709,745], w24; tops [337,367.5,397.5,428,
//     458] h19.5, pitch 30.2); group tints D4FCE6/F8E6D0/D5D5FB; red y_i labels;
//     block wrapped in tall maroon 9C3444 [ ] end-bars (spines fx 295..297 / 787..790,
//     fy ~334..478, short arms) — spec missed these
//   captions 2 lines centered (vision read): "Corresponding" (red fs 11) /
//     "Projections at " (red fs 9.5) + "Head N" (BLUE 0000CC — spec's [?] resolved);
//     line1 caps fy 486..493, line2 498..504; centers fx 366.5/566.5/735.5
//   right annotations: 5 centered 2-line blocks (pitch 29.9fx, aligned to output rows):
//     "Corresponding" (red fs 11) / "Projection of Word #N" (red fs 8.5), cx ~fx 857
//   summary box fx 64..258 fy 417..496: BLUE 0000CC border w2.25 (core #19125C),
//     fill FAFBEB (pale cream — measured, NOT F0F1EF), round bullets 0000CC at fx ~75,
//     3 lines fs 11 bold (blue with red highlights on lines 1-2; line 3 measured ALL
//     BLUE — spec's red '4' wrong): "Sequence of  5 Words" / "Network with  3 Heads" /
//     "Embedding  Dimension=4"
//   OMITTED as video artifacts (GROUND RULES (c) + m3 artifact note): gray cursor box
//     over Head1 row 3; black bottom letterbox rows 519..539.
// CONTENT SPEC: analysis/slide_016_final.json (PASS_WITH_FIXES, score 9). Badge = 16.

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
  blue: "0000CC",          // deep blue family (cores #090066..#261A88; 014-certified mapping)
  magenta: "CC00CC",       // X_N vector names (012-certified; cores #AA52AC..#B65EC0)
  panel: "F2F1EF",         // content panels (measured #F2F1EF)
  panelRim: "D0D5DA",      // panel borders (009-certified)
  pillPink: "FFE3F9",      // embedding pill fill (measured)
  cellFill: N9.C.cellFill, // FCF9C8
  cellRim: N9.C.cellRim,   // 8B7B3A
  green: "D4FCE6",         // Head1 tint (012-certified)
  orange: "F8E6D0",        // Head2 tint
  lavender: "D5D5FB",      // Head3 tint
  outCellRim: "404040",    // output cell borders (measured dark 1px)
  yBracket: "9C3444",      // output end-bars (010-certified maroon family)
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
  embedBracketL: { spine: [157, 133, 3.5, 182], armW: 15, armH: 4 },
  embedBracketR: { spine: [297, 133, 3.5, 182], armW: 13, armH: 4 },
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
  // header W/k/of parts measured per matrix: W ink / k ink / "of Head N" left edge
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
  outBracketL: { spine: [295, 334, 3, 144], armW: 11, armH: 5 },
  outBracketR: { spine: [787, 335, 3, 143], armW: 11, armH: 5 },
  outCells: {
    lefts: [[311.5, 348, 383.5, 419.5], [475, 511, 546.5, 582], [636.5, 673, 709, 745]],
    cw: 24, rowTops: [337, 367.5, 397.5, 428, 458], ch: 19.5,
    fills: [C.green, C.orange, C.lavender],
  },
  captions: { cxs: [366.5, 566.5, 735.5], l1CapTop: 486, l2CapTop: 498, fs1: 11, fs2: 10.4 },
  annots: { rightFx: 902, pitch: 29.9, l1CapTop: 341, l2CapTop: 351, fs1: 12.3, fs2: 11, n: 5 },
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
  // original hand-styles the math variable: larger italic W (ink fx603..619 h14 ->
  // fs ~20.5) + big lowered k (ink fx619..626 fy89..97 -> fs ~12.5, below the text
  // baseline) — separate positioned boxes (fix12 idiom; vision read + t-art measured).
  // main text caps fy80..91.5 (fs 17.9); left box ends fx601, right starts fx636.
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

function drawEmbedBrackets(pres, s) {
  // blue [ ] hugging the pill column, arms pointing inward
  const B = G.embedBracketL, B2 = G.embedBracketR;
  for (const [b, dir] of [[B, 1], [B2, -1]]) {
    const [x0, y0, w, h] = b.spine;
    s.addShape(pres.ShapeType.rect, { x: px(fx2sx(x0)), y: px(fy2sy(y0)),
      w: px(w), h: px(h / 0.955556), fill: { color: C.blue }, line: { type: "none" } });
    s.addShape(pres.ShapeType.rect, { x: px(fx2sx(dir > 0 ? x0 : x0 + w - b.armW)),
      y: px(fy2sy(y0)), w: px(b.armW), h: px(b.armH), fill: { color: C.blue }, line: { type: "none" } });
    s.addShape(pres.ShapeType.rect, { x: px(fx2sx(dir > 0 ? x0 : x0 + w - b.armW)),
      y: px(fy2sy(y0 + h - b.armH)), w: px(b.armW), h: px(b.armH), fill: { color: C.blue }, line: { type: "none" } });
  }
}

function drawEmbedRows(pres, s) {
  const E = G.embedRows;
  for (let r = 0; r < 5; r++) {
    const top = E.tops[r];
    // pink pill
    s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(E.pillX)), y: px(fy2sy(top)),
      w: px(E.pillW / 0.962329), h: px(E.pillH / 0.955556), rectRadius: 0.14,
      fill: { color: C.pillPink }, line: { color: C.inkRed, width: 1.75 } });
    // 4 transparent circles with red rims + bold X_i labels
    for (let q = 0; q < 4; q++) {
      const cx = E.circleCxs[q], cy = top + 16.3, d = E.circleD;
      s.addShape(pres.ShapeType.ellipse, { x: px(fx2sx(cx - d / 2)), y: px(fy2sy(cy - d / 2)),
        w: px(d), h: px(d), fill: { type: "none" }, line: { color: C.inkRed, width: 1.5 } });
      s.addText([R("X", { fontSize: 10 }), SUB(String(q + 1), { fontSize: 7 })],
        { x: px(fx2sx(cx - d / 2)), y: px(fy2sy(cy - d / 2)), w: px(d), h: px(d),
          align: "center", valign: "middle", bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
    }
    // label line 1 (red) + line 2 "of Word #N" with BLUE #N — separate positioned boxes
    s.addText("Embedding Vector",
      { x: px(fx2sx(E.labX)), y: px(fy2sy(E.l1CapTop + 2) - 6), w: px(E.labW / 0.962329),
        h: px(12), align: "center", valign: "middle", bold: true, fontSize: 7.5,
        color: C.inkRed, fontFace: FONT, margin: 0 });
    s.addText([R("of Word ", { color: C.inkRed }), R("#" + (r + 1), { color: C.blue })],
      { x: px(fx2sx(E.labX + 8)), y: px(fy2sy(E.l2CapTop + 2) - 6), w: px(E.labW / 0.962329),
        h: px(12), align: "center", valign: "middle", bold: true, fontSize: 7.5,
        fontFace: FONT, margin: 0 });
    // big italic magenta X_(r+1) + subscript — separate boxes (fix12 idiom)
    s.addText([R("X", { italic: true })],
      { x: px(fx2sx(E.xCx) - 9), y: px(fy2sy((E.xCapTop + E.xCapBot) / 2) - 8.5),
        w: px(18), h: px(17), align: "center", valign: "middle", bold: true, italic: true,
        fontSize: 14.5, color: C.magenta, fontFace: FONT, margin: 0 });
    s.addText(String(r + 1),
      { x: px(fx2sx(E.subCx) - 4), y: px(fy2sy((E.subTop + E.subBot) / 2) - 5),
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

function drawOutBrackets(pres, s) {
  for (const [b, dir] of [[G.outBracketL, 1], [G.outBracketR, -1]]) {
    const [x0, y0, w, h] = b.spine;
    s.addShape(pres.ShapeType.rect, { x: px(fx2sx(x0)), y: px(fy2sy(y0)),
      w: px(w), h: px(h / 0.955556), fill: { color: C.yBracket }, line: { type: "none" } });
    s.addShape(pres.ShapeType.rect, { x: px(fx2sx(dir > 0 ? x0 : x0 + w - b.armW)),
      y: px(fy2sy(y0)), w: px(b.armW), h: px(b.armH), fill: { color: C.yBracket }, line: { type: "none" } });
    s.addShape(pres.ShapeType.rect, { x: px(fx2sx(dir > 0 ? x0 : x0 + w - b.armW)),
      y: px(fy2sy(y0 + h - b.armH)), w: px(b.armW), h: px(b.armH), fill: { color: C.yBracket }, line: { type: "none" } });
  }
}

function drawOutCells(pres, s) {
  const O = G.outCells;
  for (let m = 0; m < 3; m++) {
    for (let r = 0; r < 5; r++) {
      for (let c = 0; c < 4; c++) {
        const bx = O.lefts[m][c], by = O.rowTops[r];
        s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(bx)), y: px(fy2sy(by)),
          w: px(O.cw), h: px(O.ch), rectRadius: 0.04,
          fill: { color: O.fills[m] }, line: { color: C.outCellRim, width: 1 } });
        s.addText([R("y", { fontSize: 11 }), SUB(String(c + 1), { fontSize: 8 })],
          { x: px(fx2sx(bx)), y: px(fy2sy(by)), w: px(O.cw), h: px(O.ch),
            align: "center", valign: "middle", bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
      }
    }
  }
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
  const A = G.annots;
  const right = fx2sx(A.rightFx);
  for (let k = 0; k < A.n; k++) {
    s.addText("Corresponding",
      { x: px(right - 115), y: px(fy2sy(A.l1CapTop + A.pitch * k + 3) - 6), w: px(115), h: px(12),
        align: "right", valign: "middle", bold: true, fontSize: A.fs1, color: C.inkRed,
        fontFace: FONT, margin: 0 });
    s.addText("Projection of Word #" + (k + 1),
      { x: px(right - 115), y: px(fy2sy(A.l2CapTop + A.pitch * k + 2.5) - 5.5), w: px(115), h: px(11),
        align: "right", valign: "middle", bold: true, fontSize: A.fs2, color: C.inkRed,
        fontFace: FONT, margin: 0 });
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
 *   { skip }     block names to omit: "title" "subtitle" "panels" "embedBrackets"
 *                "embedRows" "containers" "headers" "cells" "parens" "equals"
 *                "outBrackets" "outCells" "captions" "annotts" "summary"
 *   { only }     draw ONLY these blocks
 * P1 sibling pattern: per-block renderBase + BLOCKS map (014's idiom).
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
  if (want("embedBrackets")) drawEmbedBrackets(pres, slide);
  if (want("embedRows")) drawEmbedRows(pres, slide);
  if (want("parens")) drawParens(pres, slide);
  if (want("equals")) drawEquals(pres, slide);
  if (want("outBrackets")) drawOutBrackets(pres, slide);
  if (want("outCells")) drawOutCells(pres, slide);
  if (want("captions")) drawCaptions(pres, slide);
  if (want("annotts")) drawAnnotts(pres, slide);
  if (want("summary")) drawSummary(pres, slide);
}

const BLOCKS = ["title", "subtitle", "panels", "embedBrackets", "embedRows", "containers",
  "headers", "cells", "parens", "equals", "outBrackets", "outCells", "captions",
  "annotts", "summary"];

module.exports = { G, C, BLOCKS, renderBase, drawTitle, drawSubtitle, drawPanels,
  drawEmbedBrackets, drawEmbedRows, drawContainers, drawHeaders, drawMatrixCells,
  drawParens, drawEquals, drawOutBrackets, drawOutCells, drawCaptions, drawAnnotts,
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
