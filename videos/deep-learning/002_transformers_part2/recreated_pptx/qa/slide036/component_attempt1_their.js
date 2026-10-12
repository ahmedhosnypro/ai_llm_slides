// components/slide_036.js — banked composition for slide 036 "Multi Head Self
// Attention Block" (Deep Learning DSAI 308, Transformers Part II — video 002).
//
// BANKED per the dependency law (17 §2): the dependency audit recommends adding
// 38<-36, and 36 is the ancestor of the block-diagram family (38/45/46 reuse).
// renderBase(pptx, slide, opts) draws the slide at BLOCK granularity:
//   blocks: title | infoPanel | diagram | strips | dots | banner | arrows |
//           gutters | caption
//   opts.skip      : array of block names to omit (children draw their own delta)
//   opts.numeral   : badge numeral (default 36 = the number printed on THIS
//                    original frame); chrome drawn via the shared playlist module
//   opts.chrome    : set false to skip the house chrome entirely
// NEVER edit this module once certified — children copy-then-modify (cascade law).
//
// CONTENT SPEC: analysis/slide_036_final.json (PASS_WITH_FIXES) + build-time zoom:
//   - Token labels are 0-BASED per the read of record (SOURCES.md "Subscript
//     reading note": vision transcript Y_0..Y_5 ... Y_{N-2}, Y_{N-1}), re-confirmed
//     at build zoom (qa/slide036/zoom_tail_labels.txt: "not N+1 and not N/2") and
//     by certified-convention slide 020's syms ["0".."5","N-2","N-1"].
//   - Info-panel text verbatim per zoom_texts.txt (indent groups measured).
//   - Upper gutter label "Output of Self / Attention" is BLUE (zoom + PIL blue-core
//     census; the spec's "red" was a mis-read), lower "Input  to Self / Attention"
//     (double space) is RED; both bold italic 2-line.
//   - Token unit anatomy (prior-worker census measure6_out.txt + zoom): a horizontal
//     strip of pastel slots — yellow | green | pink(label cell) | violet(tail units
//     only) — thin gray borders; NOT the spec's guessed stacked yellow/pink cells.
//   - Arrows: 16 HOLLOW blue-outline up block arrows (white fill), aligned to the
//     pink label cells, 8 above + 8 below the banner (measured).
//
// FRAME->SLIDE MAPPING (this frame's chrome landmarks identical to certified 002/
// 035/020 fit): frame_x = 18.628 + 0.961231*slide_x ; frame_y = 0.955556*slide_y
// (fitted left border col 58, right col 901, top row 43, bottom stroke 516, badge
// yellow bbox (859..892, 57..85) center (875.5, 71.0)).
//
// MEASURED COLOR CORES (solid-fill PIL censuses + zoom reads):
//   banner 1A0EAE (solid census (26,14,174); zoom #1D1DAE) | body/border blue
//   2121A5 (zoom #2121A5/#1B1BA6) | title/labels/diagram-border C00000 (title zoom
//   #C00000; 035 precedent) | panel fill FFFFE6 (zoom #FFFFE1, census #FCFDED) |
//   caption text 990000 (spec [?]-estimate; zoom "dark red") on FFFF00 highlight |
//   Y dots 2222CC (zoom) | X dots 22CC22 (zoom #22CC22) | slots: yellow FAFDC3,
//   green F0FFDE, pink FFCCCC, violet E9E5F5 (solid censuses / zoom) | strip border
//   gray AAAAAA (thin, JPEG-washed).

const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

// ---- frame->slide transform (frame px 960x540 -> slide pt; 1pt = 1/72 in) ----
const FX = (fx) => (fx - 18.628) / 0.961231;
const FY = (fy) => fy / 0.955556;
const PT = (v) => v / 72; // pt -> inches

// ---- measured constants (FRAME px unless noted) ----
const MEAS = {
  title: { inkX0: 306, inkX1: 712, capTop: 78, baseline: 97, em: 28.5 },
  infoPanel: { x0: 95, x1: 862, y0: 110, y1: 334 },
  // panel text lines: [capTop, leftFrameX, bold, text]  (spacing verbatim from spec)
  lines: [
    [119, 105, true, "Input:"],
    [137, 181, false, "Word Embedding + Positional Information   [First Transformer Block]"],
    [156, 182, false, "Output of Previous Transformer Block      [Stacked Transformer Blocks]"],
    [196, 105, true, "Output:"],
    [215, 182, false, "Encoded Vectors of Input Sequence   [With Same Input Vectors Dimension]"],
    [256, 105, true, "Remember:"],
    [274, 146, false, "Different Input Sequences should be of Same Length  (Fixed Length Sequences)"],
    [293, 227, false, "[Apply  Pad or Cut]"],
    [312, 144, false, "Output Sequence is of same Length as Input Sequence"],
  ],
  diagram: { x0: 65, x1: 892, y0: 348, y1: 511 },
  banner: { x0: 165, x1: 884, y0: 394, y1: 444, em: 17.5 },
  // token unit strips: [runX0, runX1]; slot layout relative to run start (frame px).
  // ALL units share the same 5-slot anatomy (pixel census units 1/3/6/7/8 + crop
  // check round 1: yellow | green | pink(label) | violet | pale-pink, thin gray
  // separators; strips extend ~60px, pitch 73).
  units: [[176, 236], [249, 309], [322, 382], [395, 455], [468, 528], [541, 601], [731, 791], [803, 863]],
  slotsAll: [[1, 10, "yellow"], [13, 22, "green"], [24, 35, "pink"], [38, 46, "violet"], [50, 57, "palepink"]],
  yBand: { outer0: 359, outer1: 377, slot0: 360, slot1: 376, labelCy: 368 },
  xBand: { outer0: 462, outer1: 480, slot0: 463, slot1: 479, labelCy: 471 },
  symbols: ["0", "1", "2", "3", "4", "5", "N-2", "N-1"],
  dots: { centers: [628.5, 647, 665, 683, 698], yCy: 368, xCy: 470.5, yD: 7, xD: 6.5 },
  arrows: { headW: 18, headH: 6, shaftW: 8, upBand: [378, 395], dnBand: [445, 461] },
  gutters: {
    up: { x: 74, cx: 115, l1Cap: 363, l2Cap: 378, text1: "Output of Self", text2: "Attention" },
    dn: { x: 72, l1Cap: 448, l2Cap: 464, text1: "Input  to Self", text2: "Attention" },
  },
  caption: { x0: 292, x1: 573, y0: 488, y1: 501, capTop: 490, em: 13.5 },
};

const C = {
  blue: "2121A5",      // panel text/border, upper gutter, arrow outline
  bannerBlue: "1A0EAE", // banner fill (solid census)
  red: "C00000",       // title, token labels, lower gutter, diagram border
  darkRed: "990000",   // caption text (spec [?]-estimate)
  panelFill: "FFFFE6",
  dotBlue: "2222CC",
  dotGreen: "22CC22",
  slotYellow: "FAFDC3",
  slotGreen: "F0FFDE",
  slotPink: "FFCCCC",
  slotViolet: "E9E5F5",
  slotPink2: "F7DEF4", // 5th pale-pink cell (census (247,222,244))
  arrowFill: "BCB8F4", // arrow interior (census mean (187,183,244)) — NOT white
  stripLine: "AAAAAA",
  white: "FFFFFF",
  font: "Arial",
};

function drawTitle(pptx, s) {
  const m = MEAS.title;
  const em = m.em;
  const cx = (FX(m.inkX0) + FX(m.inkX1)) / 2; // 510.2 — the original title ink is
  // genuinely ~30pt right of slide center (measured; reproduced, 035 precedent).
  s.addText("Multi Head Self Attention Block", {
    x: PT(cx - 436.7), y: PT(FY(m.capTop) - 0.27 * em), w: 12.13, h: PT(1.5 * em),
    align: "center", valign: "top", wrap: false,
    fontSize: em, bold: true, color: C.red, fontFace: C.font, margin: 0,
  });
}

function drawInfoPanel(pptx, s) {
  const p = MEAS.infoPanel;
  s.addShape(pptx.ShapeType.rect, {
    x: PT(FX(p.x0)), y: PT(FY(p.y0)), w: PT(FX(p.x1) - FX(p.x0)), h: PT(FY(p.y1) - FY(p.y0)),
    fill: { color: C.panelFill }, line: { color: C.blue, width: 1.5 },
  });
  const em = 16.5;
  for (const [capTop, lx, bold, text] of MEAS.lines) {
    s.addText(text, {
      x: PT(FX(lx) - 0.04 * em), y: PT(FY(capTop) - 0.27 * em), w: PT(FX(p.x1 - 8) - FX(lx)), h: PT(1.5 * em),
      align: "left", valign: "top", wrap: false, margin: 0,
      fontSize: em, bold, color: C.blue, fontFace: C.font,
    });
  }
}

function drawDiagramPanel(pptx, s) {
  const d = MEAS.diagram;
  s.addShape(pptx.ShapeType.rect, {
    x: PT(FX(d.x0)), y: PT(FY(d.y0)), w: PT(FX(d.x1) - FX(d.x0)), h: PT(FY(d.y1) - FY(d.y0)),
    fill: { color: C.white }, line: { color: C.red, width: 1.5 },
  });
}

function drawStrips(pptx, s) {
  const slotFill = { yellow: C.slotYellow, green: C.slotGreen, pink: C.slotPink, violet: C.slotViolet, palepink: C.slotPink2 };
  for (const band of [MEAS.yBand, MEAS.xBand]) {
    MEAS.units.forEach(([ux0, ux1], i) => {
      const slots = MEAS.slotsAll;
      // outer strip rect
      s.addShape(pptx.ShapeType.rect, {
        x: PT(FX(ux0)), y: PT(FY(band.outer0)), w: PT(FX(ux1) - FX(ux0)), h: PT(FY(band.outer1) - FY(band.outer0)),
        fill: { color: C.white }, line: { color: C.stripLine, width: 0.75 },
      });
      for (const [a, b, kind] of slots) {
        s.addShape(pptx.ShapeType.rect, {
          x: PT(FX(ux0 + a)), y: PT(FY(band.slot0)), w: PT(FX(ux0 + b) - FX(ux0 + a)), h: PT(FY(band.slot1) - FY(band.slot0)),
          fill: { color: slotFill[kind] }, line: { color: C.stripLine, width: 0.5 },
        });
      }
      // label centered on the pink cell (red bold, true smaller subscript)
      const pink = slots.find((t) => t[2] === "pink");
      const pcx = FX(ux0 + (pink[0] + pink[1]) / 2);
      const cy = FY(band.labelCy);
      s.addText(
        [
          { text: band === MEAS.yBand ? "Y" : "X", options: { fontSize: 12 } },
          { text: MEAS.symbols[i], options: { fontSize: 8, subscript: true } },
        ],
        {
          x: PT(pcx - 43), y: PT(cy - 9), w: 86 / 72, h: 18 / 72,
          align: "center", valign: "middle", wrap: false, margin: 0,
          bold: true, color: C.red, fontFace: C.font,
        }
      );
    });
  }
}

function drawDots(pptx, s) {
  const { centers, yCy, xCy, yD, xD } = MEAS.dots;
  for (const cx of centers) {
    s.addShape(pptx.ShapeType.ellipse, {
      x: PT(FX(cx) - yD / 2), y: PT(FY(yCy) - yD / 2), w: PT(yD), h: PT(yD),
      fill: { color: C.dotBlue }, line: { color: C.dotBlue, width: 0.25 },
    });
    s.addShape(pptx.ShapeType.ellipse, {
      x: PT(FX(cx) - xD / 2), y: PT(FY(xCy) - xD / 2), w: PT(xD), h: PT(xD),
      fill: { color: C.dotGreen }, line: { color: C.dotGreen, width: 0.25 },
    });
  }
}

function drawBanner(pptx, s) {
  const b = MEAS.banner;
  s.addShape(pptx.ShapeType.rect, {
    x: PT(FX(b.x0)), y: PT(FY(b.y0)), w: PT(FX(b.x1) - FX(b.x0)), h: PT(FY(b.y1) - FY(b.y0)),
    fill: { color: C.bannerBlue },
  });
  s.addText("Multi Head Self Attention Block", {
    x: PT(FX(b.x0)), y: PT(FY(b.y0)), w: PT(FX(b.x1) - FX(b.x0)), h: PT(FY(b.y1) - FY(b.y0)),
    align: "center", valign: "middle", wrap: false, margin: 0,
    fontSize: b.em, bold: true, color: C.white, fontFace: C.font,
  });
}

// hollow up block arrow: apex top-center, head w x headH, shaft shaftW, height h (pt)
function upArrow(pptx, s, cxPt, y0Pt, h, headW, headH, shaftW) {
  const half = headW / 2, sh = shaftW / 2;
  const pts = [
    { x: half, y: 0 }, { x: headW, y: headH }, { x: half + sh, y: headH },
    { x: half + sh, y: h }, { x: half - sh, y: h }, { x: half - sh, y: headH },
    { x: 0, y: headH }, { x: half, y: 0 },
  ].map((p) => ({ x: PT(p.x), y: PT(p.y) }));
  s.addShape("custGeom", {
    x: PT(cxPt - half), y: PT(y0Pt), w: PT(headW), h: PT(h),
    points: pts, fill: { color: C.arrowFill }, line: { color: C.blue, width: 1 },
  });
}

function drawArrows(pptx, s) {
  const a = MEAS.arrows;
  const hh = a.headH / 0.955556, hw = a.headW / 0.961231, sw = a.shaftW / 0.961231;
  MEAS.units.forEach(([ux0, ux1], i) => {
    const slots = MEAS.slotsAll;
    const pink = slots.find((t) => t[2] === "pink");
    const cx = FX(ux0 + (pink[0] + pink[1]) / 2);
    upArrow(pptx, s, cx, FY(a.upBand[0]), FY(a.upBand[1]) - FY(a.upBand[0]), hw, hh, sw);
    upArrow(pptx, s, cx, FY(a.dnBand[0]), FY(a.dnBand[1]) - FY(a.dnBand[0]), hw, hh, sw);
  });
}

function drawGutters(pptx, s) {
  const g = MEAS.gutters, em = 13;
  // upper: blue bold italic, line 2 centered under line 1
  s.addText(g.up.text1, {
    x: PT(FX(g.up.x) - 0.05 * em), y: PT(FY(g.up.l1Cap) - 0.27 * em), w: 2.2, h: PT(1.5 * em),
    align: "left", valign: "top", wrap: false, margin: 0,
    italic: true, bold: true, fontSize: em, color: C.blue, fontFace: C.font,
  });
  s.addText(g.up.text2, {
    x: PT(FX(g.up.cx) - 79), y: PT(FY(g.up.l2Cap) - 0.27 * em), w: 2.2, h: PT(1.5 * em),
    align: "center", valign: "top", wrap: false, margin: 0,
    italic: true, bold: true, fontSize: em, color: C.blue, fontFace: C.font,
  });
  // lower: red bold italic, line 2 left-aligned with line 1 ("Input<2sp>to Self")
  s.addText(g.dn.text1, {
    x: PT(FX(g.dn.x) - 0.05 * em), y: PT(FY(g.dn.l1Cap) - 0.27 * em), w: 2.2, h: PT(1.5 * em),
    align: "left", valign: "top", wrap: false, margin: 0,
    italic: true, bold: true, fontSize: em, color: C.red, fontFace: C.font,
  });
  s.addText(g.dn.text2, {
    x: PT(FX(g.dn.x) - 0.05 * em), y: PT(FY(g.dn.l2Cap) - 0.27 * em), w: 2.2, h: PT(1.5 * em),
    align: "left", valign: "top", wrap: false, margin: 0,
    italic: true, bold: true, fontSize: em, color: C.red, fontFace: C.font,
  });
}

function drawCaption(pptx, s) {
  const cp = MEAS.caption;
  s.addShape(pptx.ShapeType.rect, {
    x: PT(FX(cp.x0)), y: PT(FY(cp.y0)), w: PT(FX(cp.x1) - FX(cp.x0)), h: PT(FY(cp.y1) - FY(cp.y0)),
    fill: { color: "FFFF00" },
  });
  const cx = (FX(cp.x0) + FX(cp.x1)) / 2;
  s.addText("Word  Embedding  +  Positional  Information", {
    x: PT(cx - 160), y: PT(FY(cp.capTop) - 0.27 * cp.em), w: 4.45, h: PT(1.5 * cp.em),
    align: "center", valign: "top", wrap: false, margin: 0,
    italic: true, bold: true, fontSize: cp.em, color: C.darkRed, fontFace: C.font,
  });
}

/**
 * Draw the full slide-036 composition (chrome + all blocks).
 * @param {object} pptx the pptxgenjs instance
 * @param {object} slide the slide returned by pptx.addSlide()
 * @param {object} opts { numeral=36, chrome=true, skip=[] }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  if (opts.chrome !== false) drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 36 : opts.numeral });
  if (!skip.has("title")) drawTitle(pptx, slide);
  if (!skip.has("infoPanel")) drawInfoPanel(pptx, slide);
  if (!skip.has("diagram")) drawDiagramPanel(pptx, slide);
  if (!skip.has("strips")) drawStrips(pptx, slide);
  if (!skip.has("dots")) drawDots(pptx, slide);
  if (!skip.has("banner")) drawBanner(pptx, slide);
  if (!skip.has("arrows")) drawArrows(pptx, slide);
  if (!skip.has("gutters")) drawGutters(pptx, slide);
  if (!skip.has("caption")) drawCaption(pptx, slide);
}

module.exports = { renderBase, MEAS, C, FX, FY, PT };
