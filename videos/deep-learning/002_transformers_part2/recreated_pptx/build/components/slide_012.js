// slide_012.js — "Using  FF NN  for Multiplication of Vector by a Multiple Matrices"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 12)
//
// PATTERN GROUP P1#3 (after certified 9, 10). Pattern reuse, NOT content dependency:
//   * house chrome via shared shared_patterns/house_chrome.js (badge numeral 12)
//   * matrix-cell treatment == 009-certified (fill FCF9C8, olive rim 8B7B3A, row-colored
//     bold W-labels with two-digit subscripts, row colors = N9.C.stack1..4)
//   * y-box treatment == 010-certified (fill FFF7EC, rim 9C3444, red y_i labels)
//   * curly braces via the 010-certified bezier-PNG pattern (gen_brace_s012.py ->
//     build/assets/s012_brace_*.png, embedded at exact px/600 size)
//   * composition is slide-12-specific (MEASURED, all from scratch/slide012/
//     measure8/9/10/11/12_output.txt, frame px 1px=1pt, deck mapping
//     slide_x=(fx-17.628)/0.961232, slide_y=fy/0.955556):
//       white canvas fx 93..768, fy 121..470 on the gray panel
//       title red fx 159..799 caps fy 58..74 (fs 22.1; "Multiple Matrices" underlined)
//       subtitle blue fx ~100..839 caps fy 81..95 (fs 18.5, = 010's certified density)
//       embed label 2 lines fy 129..137 / 140..155 ("Current Word" red + X_2 blue fs 20)
//       pink box fx 102..230.5 fy 159..191.5, 4 red-rimmed circles d26 cy 174
//         cx 123.5/152.5/176.5/203.5 (fix12 per-circle rim measurement)
//       tall "{" fx 241..253 + tall "}" fx 714..728, both fy 152..337
//       3 pastel panels fx 247/413/572 w ~145, fy 157..332 (green/orange/lavender)
//       headers "W_Q of Head N" maroon caps fy 139..147 ABOVE panel tops
//       16 cells/panel: lefts p+8/44/82/115 w 19.5; rows fy 176.5/214/256/294 h 18
//       "=" fx 206..222 fy 367..378 (fs 28)
//       short "{" ink fx 242..249.5 + short "}" ink fx 722..728.5, both fy 351..387.5
//         (fix12: full-bleed brace PNGs sized so INK lands on the measured span)
//       3 strips (head fills) fy 357..384; 4 y-boxes each (lefts 257/420/582 pitch ~36)
//       captions 2 lines red, line1 caps fy 392..400 / line2 404..411.5 (pitch 12 fx,
//         line2 w ~100 fx -> fs 11.3, lineSpacing 12.5); centers fx 312.5/487.75/656.5
//       results = red y + red sub 2 + blue sup (h): ink fy 426..441, centers fx
//         317/492.5/661, y fs 20 / sub fs 13.5 (RED) / sup fs 11 (blue)  (fix12 map)
//       magenta X_2 micro-annotation fx 518..529 fy 276..289 (below Head-2 W_43)
//   * NOTE (frame-vs-spec deltas, frame wins per fidelity law): y-box labels and
//     captions are RED (measured glyph cores), NOT blue; embed circle X labels RED;
//     result symbols = red y + blue subscript/superscript; NO braces between panels —
//     the frame's braces flank the whole panel band and the strip band.
//   * OMITTED as video-capture artifacts (GROUND RULES (c), spec imagery/animation):
//       black bottom player bar (below chrome bottom), black mouse cursor inside H1.
// CONTENT SPEC: analysis/slide_012_final.json (PASS_WITH_FIXES, score 9). Badge = 12.
// No dependents in EITHER deck's slide_dependencies.json (checked 2026-10-12) ->
// no components/ export required (010 precedent).

const { CHROME, drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);
const N9 = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_009.js"
);
const pptxgen = require("pptxgenjs");

const FONT = "Arial";

// ---- frame-measured palette (measure8/9/11/12_output.txt) --------------------------
const C = {
  inkRed: "C00000",
  headerMaroon: "800000",
  blue: "1F3EC8",        // subtitle + result sub/sup (010-certified blue)
  magenta: "CC00CC",
  canvas: "FFFFFF",
  green: "D4FCE6",       // H1 fill (214,255,230)/(206,248,227)
  orange: "F8E6D0",      // H2 fill (248,230,208)
  lavender: "D5D5FB",    // H3 fill (213,213,251)
  pink: "FEE4F7",        // embed box fill core (254,228,247)
  cellFill: "FCF9C8",    // 009-certified
  cellRim: "8B7B3A",     // 009-certified olive
  yBoxFill: "FFF7EC",    // 010-certified
  yBoxRim: "9C3444",     // 010-certified
};

const fx2sx = (fx) => (fx - 17.628) / 0.961232;
const fy2sy = (fy) => fy / 0.955556;
const fw = (w) => w / 0.961232;   // frame-px WIDTH -> slide px (no letterbox offset)
const fh = (h) => h / 0.955556;   // frame-px HEIGHT -> slide px
const px = (v) => v / 72;
const R = (t, o = {}) => ({ text: t, options: o });
const SUB = (t, o = {}) => ({ text: t, options: Object.assign({ subscript: true }, o) });
const SUP = (t, o = {}) => ({ text: t, options: Object.assign({ superscript: true }, o) });

// ---- measured geometry, frame px ----------------------------------------------------
const G = {
  title: { cx: 479, capTop: 58, fs: 22.1 },
  sub: { cx: 470, capTop: 81, fs: 18.5 },
  canvas: { x: 93, y: 121, w: 675, h: 349 }, // fx 93..768, fy 121..470
  embed: {
    l1: { cx: 165.5, capTop: 129, fs: 10 },
    l2: { cx: 167, capTopX: 141, fs: 11, fsX: 20 },
    box: { x: 102, y: 159, w: 128.5, h: 32.5 },
    circles: { cxs: [123.5, 152.5, 176.5, 203.5], cy: 174, d: 26 },
  },
  braceTallL: { x: 241, y: 152, w: 0.1667, h: 2.5817 },
  braceTallR: { x: 714, y: 152, w: 0.1933, h: 2.5750 },
  braceShortL: { x: 242, y: 351, w: 0.1090, h: 0.5313 },
  braceShortR: { x: 722, y: 351, w: 0.0956, h: 0.5313 },
  panels: [
    { x: 247, y: 157, w: 145, h: 175, fill: C.green,   hc: "Head 1", hcx: 324 },
    { x: 413, y: 157, w: 145, h: 175, fill: C.orange,  hc: "Head 2", hcx: 483.5 },
    { x: 572, y: 157, w: 147, h: 175, fill: C.lavender, hc: "Head 3", hcx: 646.5 },
  ],
  header: { capTop: 139, fs: 11.5 },
  grid: { dxs: [8, 44, 82, 115], rowTops: [176.5, 214, 256, 294], cw: 19.5, ch: 18 },
  equals: { cx: 214, cy: 372.5, fs: 28 },
  strips: [
    { x: 253, y: 357, w: 139, h: 27, fill: C.green,    bx: [257, 293, 329, 365] },
    { x: 415, y: 357, w: 142, h: 27, fill: C.orange,   bx: [420, 456, 491, 528] },
    { x: 575, y: 357, w: 149, h: 27, fill: C.lavender, bx: [582, 619, 655, 691] },
  ],
  yBox: { y: 361, w: 23, h: 20 },
  caption: { cxs: [312.5, 487.75, 656.5], top: 388.7, fs: 11.3, lsp: 12.5 },
  result: {
    // separate positioned boxes per glyph (fix12: LO renders baseline-attr sub/sup
    // runs at 58% size — measured; plain runs at measured ink centers instead).
    // org ink: y fx 302..310 fy 428..441 | sub 2 fx 314..319 fy 432..441 (RED)
    //          sup (h) fx 320..332 fy 426..435 (blue)   [centers below, frame px]
    yC: [[306, 430.5], [482, 430.5], [650, 430.5]],
    subC: [[316, 436.5], [491, 436.5], [659.5, 436.5]],
    supC: [[326, 430.5], [500.5, 430.5], [670, 430.5]],
  },
  magenta: { cx: 523.5, cy: 282.5, tipX: 527, tipY: 272 },
};

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/";

// ---- chrome + text ------------------------------------------------------------------
function drawTitle(pres, s) {
  // ink fx 159..799 -> cx 479; caps fy 58..74; underline ONLY "Multiple Matrices"
  s.addText([
    R("Using  FF NN  for Multiplication of Vector by a ", {}),
    R("Multiple Matrices", { underline: true }),
  ], { x: px(fx2sx(G.title.cx) - 371), y: px(fy2sy(G.title.capTop) - 7.2), w: px(742), h: px(32),
       align: "center", valign: "middle", bold: true, fontSize: G.title.fs,
       color: C.inkRed, fontFace: FONT, margin: 0 });
}

function drawSubtitle(pres, s) {
  // verbatim incl. double spaces; W_q subscript; underline "Queries of Multiple Heads"
  s.addText([
    R("Example: Multiply Vector of Current Word by Multiple  (different) W", {}),
    SUB("q", { fontSize: 12 }),
    R("   (", {}),
    R("Queries of Multiple Heads", { underline: true }),
    R(")", {}),
  ], { x: px(fx2sx(G.sub.cx) - 430), y: px(fy2sy(G.sub.capTop) - 7.2), w: px(860), h: px(26),
       align: "center", valign: "middle", bold: true, italic: true, fontSize: G.sub.fs,
       color: C.blue, fontFace: FONT, margin: 0 });
}

function drawEmbed(pres, s) {
  const e = G.embed;
  // label line 1
  s.addText("Embedding Vector of",
    { x: px(fx2sx(e.l1.cx) - 60), y: px(fy2sy(e.l1.capTop) - 2.5), w: px(120), h: px(14),
      align: "center", valign: "middle", bold: true, fontSize: e.l1.fs, color: C.inkRed,
      fontFace: FONT, margin: 0 });
  // label line 2: "Current Word " red + big blue X_2 (baseline-aligned, ink fx 127..207)
  s.addText([
    R("Current Word ", { fontSize: e.l2.fs, color: C.inkRed }),
    R("X", { fontSize: e.l2.fsX, color: C.blue, italic: true }),
    SUB("2", { fontSize: 11, color: C.blue, italic: true }),
  ], { x: px(fx2sx(e.l2.cx) - 60), y: px(fy2sy(e.l2.capTopX) - 4), w: px(120), h: px(24),
       align: "center", valign: "middle", bold: true, fontFace: FONT, margin: 0 });
  // pink rounded box
  const b = e.box;
  s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(b.x)), y: px(fy2sy(b.y)),
    w: px(fx2sx(b.w)), h: px(b.h), rectRadius: 0.08, fill: { color: C.pink },
    line: { type: "none" } });
  // 4 white circles, red rims, red X_i labels
  const subs = ["1", "2", "3", "4"];
  for (let i = 0; i < 4; i++) {
    const cx = e.circles.cxs[i], cy = e.circles.cy, d = e.circles.d;
    s.addShape(pres.ShapeType.ellipse, { x: px(fx2sx(cx - d / 2)), y: px(fy2sy(cy - d / 2)),
      w: px(d), h: px(d), fill: { color: "FFFFFF" }, line: { color: C.inkRed, width: 1.25 } });
    s.addText([R("X", { fontSize: 11 }), SUB(subs[i], { fontSize: 8 })],
      { x: px(fx2sx(cx - d / 2)), y: px(fy2sy(cy - d / 2)), w: px(d), h: px(d),
        align: "center", valign: "middle", bold: true, color: C.inkRed, fontFace: FONT, margin: 0 });
  }
}

// ---- three head panels with 4x4 grids -----------------------------------------------
function drawPanels(pres, s) {
  const rowCols = [N9.C.stack1, N9.C.stack2, N9.C.stack3, N9.C.stack4];
  const msub = [["11", "21", "31", "41"], ["12", "22", "32", "42"],
                ["13", "23", "33", "43"], ["14", "24", "34", "44"]];
  for (const p of G.panels) {
    s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(p.x)), y: px(fy2sy(p.y)),
      w: px(fx2sx(p.w)), h: px(p.h), rectRadius: 0.08, fill: { color: p.fill },
      line: { type: "none" } });
    // header ABOVE the panel top (measured): "W_Q of Head N", maroon
    s.addText([R("W", { fontSize: 12 }), SUB("Q", { fontSize: 8 }),
               R(" of " + p.hc, { fontSize: G.header.fs })],
      { x: px(fx2sx(p.hcx) - 60), y: px(fy2sy(G.header.capTop) - 3), w: px(120), h: px(16),
        align: "center", valign: "middle", bold: true, color: C.headerMaroon,
        fontFace: FONT, margin: 0 });
    // 16 cells
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 4; c++) {
        const bx = p.x + G.grid.dxs[c], by = G.grid.rowTops[r];
        s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(bx)), y: px(fy2sy(by)),
          w: px(G.grid.cw), h: px(G.grid.ch), rectRadius: 0.04,
          fill: { color: C.cellFill }, line: { color: C.cellRim, width: 0.75 } });
        s.addText([R("W", { fontSize: 9 }), SUB(msub[r][c], { fontSize: 7 })],
          { x: px(fx2sx(bx)), y: px(fy2sy(by)), w: px(G.grid.cw), h: px(G.grid.ch),
            align: "center", valign: "middle", bold: true, color: rowCols[r],
            fontFace: FONT, margin: 0 });
      }
    }
  }
}

// ---- equals + strips + y-boxes + captions + results ---------------------------------
function drawBottom(pres, s) {
  // large red "=" (ink fx 206..222, fy 367..378)
  s.addText("=", { x: px(fx2sx(G.equals.cx) - 14), y: px(fy2sy(G.equals.cy) - 14),
    w: px(28), h: px(28), align: "center", valign: "middle", bold: true,
    fontSize: G.equals.fs, color: C.inkRed, fontFace: FONT, margin: 0 });
  // three head-colored strips with 4 y-boxes each (red labels, 010-certified treatment)
  const subs = ["1", "2", "3", "4"];
  for (const st of G.strips) {
    s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(st.x)), y: px(fy2sy(st.y)),
      w: px(fx2sx(st.w)), h: px(st.h), rectRadius: 0.06, fill: { color: st.fill },
      line: { type: "none" } });
    for (let i = 0; i < 4; i++) {
      const bx = st.bx[i], by = G.yBox.y;
      s.addShape(pres.ShapeType.roundRect, { x: px(fx2sx(bx)), y: px(fy2sy(by)),
        w: px(G.yBox.w), h: px(G.yBox.h), rectRadius: 0.05, fill: { color: C.yBoxFill },
        line: { color: C.yBoxRim, width: 1.25 } });
      s.addText([R("y", { fontSize: 11 }), SUB(subs[i], { fontSize: 8 })],
        { x: px(fx2sx(bx)), y: px(fy2sy(by)), w: px(G.yBox.w), h: px(G.yBox.h),
          align: "center", valign: "middle", bold: true, color: C.inkRed,
          fontFace: FONT, margin: 0 });
    }
  }
  // captions: "Corresponding" / "Projection at Head N", red, 2 lines
  for (let i = 0; i < 3; i++) {
    s.addText([R("Corresponding", { breakLine: true }),
               R("Projection at Head " + (i + 1), {})],
      { x: px(fx2sx(G.caption.cxs[i]) - 60), y: px(fy2sy(G.caption.top)), w: px(120),
        h: px(26), align: "center", valign: "top", bold: true, fontSize: G.caption.fs,
        color: C.inkRed, fontFace: FONT, margin: 0, lineSpacing: G.caption.lsp });
  }
  // results: red y + red sub 2 + blue sup (h) — three positioned plain-run boxes
  // per result (fix12: LO scales baseline-attr runs to 58%, measured — separate
  // boxes reproduce the original's glyph sizes; ink centers calibrated below)
  for (let i = 0; i < 3; i++) {
    const yC = G.result.yC[i], subC = G.result.subC[i], supC = G.result.supC[i];
    s.addText("y", { x: px(fx2sx(yC[0]) - 10), y: px(fy2sy(yC[1]) - 11), w: px(20),
      h: px(22), align: "center", valign: "middle", bold: true, fontSize: 20,
      color: C.inkRed, fontFace: FONT, margin: 0 });
    s.addText("2", { x: px(fx2sx(subC[0]) - 7), y: px(fy2sy(subC[1]) - 8), w: px(14),
      h: px(16), align: "center", valign: "middle", bold: true, fontSize: 13.5,
      color: C.inkRed, fontFace: FONT, margin: 0 });
    s.addText("(" + (i + 1) + ")", { x: px(fx2sx(supC[0]) - 11), y: px(fy2sy(supC[1]) - 8),
      w: px(22), h: px(16), align: "center", valign: "middle", bold: true, fontSize: 11,
      color: C.blue, fontFace: FONT, margin: 0 });
  }
}

// ---- magenta X_2 micro-annotation below Head-2 W_43 ----------------------------------
function drawMagenta(pres, s) {
  const m = G.magenta;
  s.addShape(pres.ShapeType.line, { x: px(fx2sx(m.cx + 2)), y: px(fy2sy(m.tipY)),
    w: 0, h: px(fy2sy(m.cy - 4) - fy2sy(m.tipY)),
    line: { color: C.magenta, width: 0.75, beginArrowType: "triangle" } });
  s.addText([R("X", { fontSize: 6.5 }), SUB("2", { fontSize: 5 })],
    { x: px(fx2sx(m.cx) - 8), y: px(fy2sy(m.cy) - 5), w: px(16), h: px(10),
      align: "center", valign: "middle", bold: true, color: C.magenta,
      fontFace: FONT, margin: 0 });
}

// ---- braces (certified bezier-PNG pattern, exact px/600 size) -------------------------
function drawBraces(pres, s) {
  s.addImage({ path: ASSETS + "s012_brace_tall_L.png",
    x: px(fx2sx(G.braceTallL.x)), y: px(fy2sy(G.braceTallL.y)),
    w: G.braceTallL.w, h: G.braceTallL.h });
  s.addImage({ path: ASSETS + "s012_brace_tall_R.png",
    x: px(fx2sx(G.braceTallR.x)), y: px(fy2sy(G.braceTallR.y)),
    w: G.braceTallR.w, h: G.braceTallR.h });
  s.addImage({ path: ASSETS + "s012_brace_short_L.png",
    x: px(fx2sx(G.braceShortL.x)), y: px(fy2sy(G.braceShortL.y)),
    w: G.braceShortL.w, h: G.braceShortL.h });
  s.addImage({ path: ASSETS + "s012_brace_short_R.png",
    x: px(fx2sx(G.braceShortR.x)), y: px(fy2sy(G.braceShortR.y)),
    w: G.braceShortR.w, h: G.braceShortR.h });
}

/**
 * Full composition. opts:
 *   { numeral }  badge numeral (default 12)
 *   { skip }     array of block names to omit: "title" "subtitle" "canvas" "embed"
 *                "panels" "bottom" "magenta" "braces"
 *   { only }     array of block names — draw ONLY these (canvas auto-included unless
 *                itself skipped/filtered; pass "canvas" in only to get it alone)
 * P1 siblings 14/16 import this and select blocks per their measured deltas.
 */
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 12 : opts.numeral });
  const skip = Array.isArray(opts.skip) ? opts.skip : [];
  const only = Array.isArray(opts.only) ? opts.only : null;
  const want = (name) => (only ? only.indexOf(name) !== -1 : skip.indexOf(name) === -1);
  if (want("title")) drawTitle(pptx, slide);
  if (want("subtitle")) drawSubtitle(pptx, slide);
  // white content canvas on the gray panel
  if (want("canvas")) {
    slide.addShape(pptx.ShapeType.roundRect, { x: px(fx2sx(G.canvas.x)), y: px(fy2sy(G.canvas.y)),
      w: px(fx2sx(G.canvas.w)), h: px(G.canvas.h), rectRadius: 0.08,
      fill: { color: C.canvas }, line: { type: "none" } });
  }
  if (want("embed")) drawEmbed(pptx, slide);
  if (want("panels")) drawPanels(pptx, slide);
  if (want("bottom")) drawBottom(pptx, slide);
  if (want("magenta")) drawMagenta(pptx, slide);
  if (want("braces")) drawBraces(pptx, slide);
}

const BLOCKS = ["title", "subtitle", "canvas", "embed", "panels", "bottom", "magenta", "braces"];

module.exports = { G, C, BLOCKS, renderBase, drawTitle, drawSubtitle, drawEmbed, drawPanels,
  drawBottom, drawMagenta, drawBraces };

if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 960 x 540 px
  pres.author = "ai_llm_slides";
  const s = pres.addSlide();
  renderBase(pres, s, { numeral: 12 });
  const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_012_recreated.pptx";
  pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
}
