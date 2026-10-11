// slide_045.js — "Multi Head Self Attention of Word X2 'Narrow' Architecture"
// CHILD of certified slide 043 (45<-43 dependency edge, founder directive 2026-10-11).
//
// Composition law honored: this build REQUIRES the parent's certified component
// (components/slide_043.js) and never re-derives its geometry. The parent's blocks are
// imported and drawn through a measured TRANSLATION PROXY: PIL measurement of
// unique_slides/slide_045.jpg (960x540, 1px=1pt) shows the inherited diagram is drawn
// at a uniform (-7px, -38px) offset vs the parent frame (card tops h1 274->236,
// h2 252->215, h3 233->194; h-tag ovals x564..776 y198..294 -> x557..770 y160..256;
// W-column k-box green comp x668..691 y442..460 -> x661..685 y404..422; token row,
// ff blocks, swoosh all map row-for-row). Blocks whose measured geometry deviates
// from the pure shift are REDRAWN here at their measured geometry (copy-then-modify,
// dependencies.md): title (subtitle Narrow, right-aligned), concat bar (wider, higher),
// head arrows (re-pitched x410..574), pipearrow (single, x428), ltbox (REMOVED —
// Narrow variant has no Linear Transformation; SOURCES.md), legend (MOVED top-right as
// the projection equation box), plus the ADDED delta: Input Sequence ellipse + blue X
// chip bar + "Split vectors into H chunks" black caption bar + 5-row chunk table
// (To Head 5..1) and the head-output chunk strips with 1·d/H labels.
//
// Frame-measured anchors (scratch/slide045/m*.py, an_*.txt gate transcripts):
//   bar base x166..690 y89..114, segments abutting x304..678 (~74.8 each), red 2-line
//   label at left end (line1 y95..100, line2 y101..107); vecbox UNCHANGED at parent
//   x400..470 y50..72 with red 1·d label; single red arrow x428 y72..88 arrowhead top;
//   strips h1..h5 (dashed green, head-color fill, 74x16) at (378,206)(423,184)(469,163)
//   (512,143)(552,124); 1·d/H two-tone labels (red 1·d/ + navy H) at (633,134) and
//   (583,159); equation box x753..921 y108..170 green dashed, strip A (2 lav + 2 orange)
//   x762 y114, W pale-yellow box x809 y112 35x35, = x847, strip B mirrored x861 y124,
//   blue caption "d : Embedding Length" y162..171; Input Sequence ellipse x746..870
//   y347..394; blue X bar x747..876 y397..414; black caption bar x768..920 y418..434
//   with yellow text; 5 lozenge rows x752..918, yTops 440/459/478/497/516 h16, tinted
//   with the five head-card colors h5->h1; red To Head labels x~916..958 per row.
//
// LAWS: playlist chrome via shared module (numeral 45); verbatim text incl. q1
// (frame wins over the slide-37 q2 precedent, SOURCES.md); no '#' in hex; fontFace +
// margin:0 everywhere; explicit lineSpacing on multi-line boxes; middle-dot · in
// dimension labels; single-version deliverable.

const path = require("path");
const parent = require(path.join(__dirname, "components", "slide_043.js"));
const { drawHouseChrome } = require(path.join(__dirname, "components", "house_chrome.js"));

const px = parent.px;            // 1px = 1pt -> inches
const C = parent.C;
const SANS = "Arial";

// measured translation of the inherited composition (slide_045.jpg vs slide_043.jpg)
const DX = -7, DY = -38;         // px

// ---- translation proxy: draw a parent block through a measured offset ----------
function shiftedSlide(slide, dx, dy) {
  const ddx = px(dx), ddy = px(dy);
  const wrap = (o) => {
    const c = Object.assign({}, o);
    if (typeof c.x === "number") c.x += ddx;
    if (typeof c.y === "number") c.y += ddy;
    return c;
  };
  return {
    addShape: (t, o) => slide.addShape(t, wrap(o)),
    addText: (t, o) => slide.addText(t, wrap(o)),
    addImage: (o) => slide.addImage(wrap(o)),
  };
}

// ---- delta blocks ---------------------------------------------------------------

function drawTitle45(pptx, slide) {
  // line 1 — same text/geometry as the certified parent (ink x531..871 y52..67; box
  // nudged y48->45 per the measured 3px rise). X2 red with true subscript.
  slide.addText([
    { text: "Multi Head Self Attention of Word ", options: { color: C.ink } },
    { text: "X", options: { color: C.red } },
    { text: "2", options: { color: C.red, subscript: true, fontSize: 14 } },
  ], {
    x: px(500), y: px(45), w: px(400), h: px(30), align: "center", valign: "middle",
    bold: true, fontSize: 20, fontFace: SANS, margin: 0,
  });
  // line 2 — '"Narrow" Architecture', RIGHT-aligned (ink right edge x869 ~= line1's
  // 871), glyphs y80..93; "Narrow" navy bold italic on yellow highlight (measured
  // highlight x672..762 incl. quotes).
  slide.addText([
    { text: "\u201CNarrow\u201D", options: { color: C.navy, italic: true, highlight: "FFFF00" } },
    { text: " Architecture", options: { color: C.ink } },
  ], {
    x: px(470), y: px(74), w: px(400), h: px(24), align: "right", valign: "middle",
    bold: true, fontSize: 20, fontFace: SANS, margin: 0,
  });
}

function drawPipearrow(pptx, slide) {
  // single red connector bar -> output vector (ltbox removed in the Narrow variant);
  // measured head at (425..431, y75..80), shaft x428 up to the vecbox bottom.
  slide.addShape(pptx.ShapeType.line, {
    x: px(428.5), y: px(72.5), w: 0, h: px(16),
    line: { color: C.red, width: 1.5, beginArrowType: "triangle" },
  });
}

// concat bar at MEASURED geometry (wider + higher than the parent's)
const SEGS45 = [
  { x: 304, w: 74.8, fill: C.seg1 }, { x: 378.8, w: 74.8, fill: C.seg2 },
  { x: 453.6, w: 74.8, fill: C.seg3 }, { x: 528.4, w: 74.8, fill: C.seg4 },
  { x: 603.2, w: 74.8, fill: C.seg5 },
];

function drawConcatbar45(pptx, slide) {
  // stadium base x166..690, y89..114 (fill rows y92..112, borders ~y90/y113)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(166), y: px(89), w: px(524), h: px(25), rectRadius: 0.163,
    fill: { color: C.barLabel }, line: { color: "3A3A3A", width: 1 },
  });
  for (const s of SEGS45) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(s.x + 1), y: px(91.5), w: px(s.w - 2), h: px(20),
      fill: { color: s.fill }, line: { color: "3A3A3A", width: 0.5 },
    });
    const cxm = s.x + s.w / 2;
    slide.addShape(pptx.ShapeType.rect, {
      x: px(cxm - 8), y: px(95), w: px(16), h: px(12.5),
      fill: { color: "FFFFFF" }, line: { color: "B0B0B0", width: 0.5 },
    });
  }
  SEGS45.forEach((s, i) => {
    const cxm = s.x + s.w / 2;
    slide.addText(parent.BLOCKS ? idxRuns45(i) : idxRuns45(i), {
      x: px(cxm - 8), y: px(95), w: px(16), h: px(12.5),
      align: "center", valign: "middle", fontFace: SANS, margin: 0,
    });
  });
  // re-draw the stadium outline so the pill silhouette stays rounded
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(166), y: px(89), w: px(524), h: px(25), rectRadius: 0.163,
    fill: { type: "none" }, line: { color: "3A3A3A", width: 1 },
  });
  // red two-line label at the bar's left end (measured line1 y95..100 x178..~300,
  // line2 y101..107 x273..305)
  slide.addText("Concatenated Vector", {
    x: px(172), y: px(93.5), w: px(136), h: px(11), align: "left", valign: "middle",
    bold: true, fontSize: 7.5, color: C.red, fontFace: SANS, margin: 0,
  });
  slide.addText([
    { text: "1\u00B7", options: { color: C.red } },
    { text: "d", options: { color: C.red } },
  ], {
    x: px(268), y: px(100.5), w: px(44), h: px(9.5), align: "left", valign: "middle",
    bold: true, fontSize: 7, fontFace: SANS, margin: 0,
  });
}

function idxRuns45(i) {
  // Y chip label: Y + subscript numeral, brick red (parent chip pattern)
  return [
    { text: "Y", options: { bold: true, fontSize: 6, color: C.brick } },
    { text: String(i + 1), options: { bold: true, fontSize: 4.5, color: C.brick, subscript: true } },
  ];
}

function drawHeadarrows45(pptx, slide) {
  // five thin red arrows, re-pitched x410/451/492/533/574 (pitch 41, matches the
  // strips + W columns), y112.5..151.5 (parent's y-range shifted -39), arrowheads up
  const xs = [410, 451, 492, 533, 574];
  for (const x of xs) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(x), y: px(112.5), w: 0, h: px(39),
      line: { color: C.red, width: 1.1, beginArrowType: "triangle" },
    });
  }
}

// ---- projection equation box (the parent legend MOVED top-right, Narrow form) ----

function drawEqbox45(pptx, slide) {
  // white rounded box, green dashed border, x753..921 y108..170
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(753), y: px(108), w: px(168), h: px(62), rectRadius: 0.06,
    fill: { color: "FFFFFF" }, line: { color: C.green, width: 1, dashType: "dash" },
  });
  // strip A: 4 cells x762..798 y114..126 (lav, lav, orange, amber)
  const fillsA = ["C5C1F4", "C5C1F4", "E8A860", "F0C080"];
  for (let i = 0; i < 4; i++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(762 + i * 9), y: px(114), w: px(9), h: px(12),
      fill: { color: fillsA[i] }, line: { color: "9A9A9A", width: 0.5 },
    });
  }
  // W box: pale yellow x809..844 y112..147
  slide.addShape(pptx.ShapeType.rect, {
    x: px(809), y: px(112), w: px(35), h: px(35),
    fill: { color: "FFF6CC" }, line: { color: "8A8A5A", width: 1 },
  });
  slide.addText("W", {
    x: px(809), y: px(112), w: px(35), h: px(35), align: "center", valign: "middle",
    bold: true, fontSize: 14, color: "1A1A1A", fontFace: SANS, margin: 0,
  });
  // =
  slide.addText("=", {
    x: px(846), y: px(122), w: px(14), h: px(16), align: "center", valign: "middle",
    bold: true, fontSize: 12, color: "1A1A1A", fontFace: SANS, margin: 0,
  });
  // strip B: 4 cells x861..897 y124..136 (orange, orange, lav, lav — mirrored)
  const fillsB = ["E8A860", "E8A860", "C5C1F4", "C5C1F4"];
  for (let i = 0; i < 4; i++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(861 + i * 9), y: px(124), w: px(9), h: px(12),
      fill: { color: fillsB[i] }, line: { color: "9A9A9A", width: 0.5 },
    });
  }
  // two-tone 1·d/H labels under the strips (red "1·d/" + navy "H", midright read)
  const dimRuns = () => ([
    { text: "1\u00B7d/", options: { bold: true, fontSize: 7, color: C.red } },
    { text: "H", options: { bold: true, fontSize: 7, color: C.navy } },
  ]);
  slide.addText(dimRuns(), {
    x: px(770), y: px(128), w: px(46), h: px(11), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
  slide.addText(dimRuns(), {
    x: px(868), y: px(137), w: px(48), h: px(11), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
  // blue caption at the box bottom (measured y162..171 x788..890)
  slide.addText("d : Embedding Length", {
    x: px(768), y: px(159), w: px(170), h: px(13), align: "center", valign: "middle",
    bold: true, fontSize: 7.5, color: C.blue, fontFace: SANS, margin: 0,
  });
}

// ---- head annotations: parent copy-then-modify -----------------------------------
// Kept parts (Similarity/Weighted SUM ovals, h=N tags, Probabilities oval) are the
// certified parent's draw with the measured translation applied; the parent's small
// solid Y chips + green gap chip are REPLACED by the frame's dashed head-output chunk
// strips + Y labels + two-tone 1·d/H labels (Narrow variant: outputs are 1·d/H chunks).

const STRIPS = [
  { x: 378, y: 206, fill: "A0400E" },   // h1 brown
  { x: 423, y: 184, fill: "4A4A4A" },   // h2 dark gray
  { x: 469, y: 163, fill: "E0DC1E" },   // h3 yellow
  { x: 512, y: 143, fill: "8ED08A" },   // h4 green
  { x: 552, y: 124, fill: "F0D8A8" },   // h5 tan
];

function drawHeadannots45(pptx, slide) {
  const BASE_ONLY = typeof process !== "undefined" && process.env && process.env.SLIDE045_BASE_ONLY === "1";
  if (BASE_ONLY) return;
  // ovals + tags: parent geometry + (DX, DY)
  for (let k = 0; k < 5; k++) {
    const yc = 285.5 - 20.5 * k + DY;          // oval center y
    const simX = 206 + 44 * k + DX;
    const wsX = 428 + 44 * k + DX;
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(simX), y: px(yc - 7), w: px(44), h: px(14),
      fill: { color: "FFFFFF" }, line: { color: "9A9A9A", width: 0.75 },
    });
    slide.addText("Similarity", {
      x: px(simX), y: px(yc - 7), w: px(44), h: px(14), align: "center", valign: "middle",
      fontSize: 5.5, color: C.ovalText, fontFace: SANS, margin: 0,
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(wsX), y: px(yc - 7), w: px(63), h: px(14),
      fill: { color: "FFFFFF" }, line: { color: "9A9A9A", width: 0.75 },
    });
    slide.addText("Weighted SUM", {
      x: px(wsX), y: px(yc - 7), w: px(63), h: px(14), align: "center", valign: "middle",
      fontSize: 5.5, color: C.ovalText, fontFace: SANS, margin: 0,
    });
    const tag = { x: 563 + 46 * k + DX, y: 280 - 20.5 * k + DY };
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(tag.x), y: px(tag.y), w: px(30), h: px(14.5),
      fill: { color: C.tagFill }, line: { type: "none" },
    });
    slide.addText(`h=${k + 1}`, {
      x: px(tag.x), y: px(tag.y), w: px(30), h: px(14.5), align: "center", valign: "middle",
      bold: true, fontSize: 7, color: C.tagText, fontFace: SANS, margin: 0,
    });
  }
  // Probabilities oval straddling the h2/h1 top edges (parent 294,250 shifted)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(294 + DX), y: px(250 + DY), w: px(80), h: px(28),
    fill: { color: "FDF3EE" }, line: { color: "C9B8B0", width: 0.75 },
  });
  slide.addText("Probabilities", {
    x: px(294 + DX), y: px(250 + DY), w: px(80), h: px(28), align: "center", valign: "middle",
    fontSize: 6, color: C.ink, fontFace: SANS, margin: 0,
  });
  // the five head-output chunk strips (dashed green border, head-color fill, 74x16)
  for (let i = 0; i < STRIPS.length; i++) {
    const s = STRIPS[i];
    slide.addShape(pptx.ShapeType.rect, {
      x: px(s.x), y: px(s.y), w: px(74), h: px(16),
      fill: { color: s.fill }, line: { color: C.green, width: 1, dashType: "dash" },
    });
    for (let j = 1; j < 5; j++) {
      slide.addShape(pptx.ShapeType.line, {
        x: px(s.x + j * 14.8), y: px(s.y + 1), w: 0, h: px(14),
        line: { color: "FFFFFF", width: 0.5 },
      });
    }
    slide.addText(idxRuns45(i), {
      x: px(s.x), y: px(s.y), w: px(74), h: px(16), align: "center", valign: "middle",
      fontFace: SANS, margin: 0,
    });
  }
  // thin red up-arrows from the strips toward the bar (measured)
  const ups = [
    { x: 503, y: 112, h: 21 }, { x: 547, y: 113, h: 18 }, { x: 589, y: 112, h: 19 },
    { x: 547, y: 162, h: 9 }, { x: 503, y: 180, h: 14 },
  ];
  for (const a of ups) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(a.x), y: px(a.y), w: 0, h: px(a.h),
      line: { color: C.red, width: 1, beginArrowType: "triangle" },
    });
  }
  // two-tone 1·d/H labels beside the two upper strips (measured (633,134) & blue H at (611..631,166..169))
  const dimRuns = () => ([
    { text: "1\u00B7d/", options: { bold: true, fontSize: 7, color: C.red } },
    { text: "H", options: { bold: true, fontSize: 7, color: C.navy } },
  ]);
  slide.addText(dimRuns(), {
    x: px(626), y: px(131), w: px(44), h: px(12), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
  slide.addText(dimRuns(), {
    x: px(576), y: px(157), w: px(52), h: px(12), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
}

// ---- bottom-right additions (the Narrow delta) -----------------------------------

const ROW_TINTS = ["F7E2CD", "D4FFE5", "F8FF9A", "C5C1F4", "EF8C96"]; // h5 -> h1

function drawBottomRight45(pptx, slide) {
  // Input Sequence: red ellipse, white bold 2-line text (x746..870 y347..394)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(746), y: px(347), w: px(124), h: px(47),
    fill: { color: C.red }, line: { type: "none" },
  });
  slide.addText([
    { text: "Input", options: { breakLine: true } },
    { text: "Sequence", options: {} },
  ], {
    x: px(746), y: px(347), w: px(124), h: px(47), align: "center", valign: "middle",
    bold: true, fontSize: 10, color: "FFFFFF", fontFace: SANS, margin: 0, lineSpacing: 11,
  });
  // blue X chip bar: one royal-blue bar x747..876 y397..414, white separators
  slide.addShape(pptx.ShapeType.rect, {
    x: px(747), y: px(397), w: px(129), h: px(17),
    fill: { color: "2743C8" }, line: { color: "1A2F8A", width: 0.75 },
  });
  for (let i = 1; i < 4; i++) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(747 + i * 32.25), y: px(398.5), w: 0, h: px(14),
      line: { color: "FFFFFF", width: 0.75 },
    });
  }
  for (let i = 0; i < 4; i++) {
    slide.addText([
      { text: "X", options: { bold: true, fontSize: 6.5, color: "FFFFFF" } },
      { text: String(i + 1), options: { bold: true, fontSize: 5, color: "FFFFFF", subscript: true } },
    ], {
      x: px(747 + i * 32.25), y: px(397), w: px(32.25), h: px(17),
      align: "center", valign: "middle", fontFace: SANS, margin: 0,
    });
  }
  // black caption bar with yellow bold text (x768..920 y418..434)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(768), y: px(418), w: px(152), h: px(17), rectRadius: 0.08,
    fill: { color: "141414" }, line: { type: "none" },
  });
  slide.addText("Split vectors into \u201CH\u201D chunks", {
    x: px(768), y: px(418), w: px(152), h: px(17), align: "center", valign: "middle",
    bold: true, fontSize: 7, color: "F2E24C", fontFace: SANS, margin: 0,
  });
  // 5 chunk-table rows (lozenges tinted with the head-card colors, h5 -> h1)
  for (let r = 0; r < 5; r++) {
    const yTop = 440 + 19 * r;
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(752), y: px(yTop), w: px(166), h: px(16), rectRadius: 0.08,
      fill: { color: ROW_TINTS[r] }, line: { color: "9A9A9A", width: 0.5 },
    });
    // 4 word boxes: tan field + dark-red X(sub) + two lavender stripes
    for (let b = 0; b < 4; b++) {
      const bx = 782 + 21 * b;
      slide.addShape(pptx.ShapeType.rect, {
        x: px(bx), y: px(yTop + 2), w: px(18), h: px(12),
        fill: { color: "FFF4DC" }, line: { color: "C8B088", width: 0.5 },
      });
      slide.addText([
        { text: "X", options: { bold: true, fontSize: 5, color: "8B1A10" } },
        { text: String(b + 1), options: { bold: true, fontSize: 4, color: "8B1A10", subscript: true } },
      ], {
        x: px(bx + 1), y: px(yTop + 2), w: px(8), h: px(12),
        align: "center", valign: "middle", fontFace: SANS, margin: 0,
      });
      slide.addShape(pptx.ShapeType.rect, {
        x: px(bx + 10), y: px(yTop + 3), w: px(3), h: px(10),
        fill: { color: "9A86C8" }, line: { type: "none" },
      });
      slide.addShape(pptx.ShapeType.rect, {
        x: px(bx + 14), y: px(yTop + 3), w: px(3), h: px(10),
        fill: { color: "C5C1F4" }, line: { type: "none" },
      });
    }
    // red To Head label right of the row
    slide.addText(`To Head ${5 - r}`, {
      x: px(916), y: px(yTop), w: px(42), h: px(16), align: "left", valign: "middle",
      bold: true, fontSize: 6.5, color: "8B1A10", fontFace: SANS, margin: 0,
    });
  }
}

// ---- composition ------------------------------------------------------------------

function build() {
  const pptxgen = require("pptxgenjs");
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  slide.background = { color: "E9E9E7" };

  // 1. playlist house chrome (numeral = the number printed on the original: 45)
  drawHouseChrome(pptx, slide, { numeral: 45 });

  // 2. output vector box: inherited UNCHANGED (measured at parent position)
  parent.renderBase(pptx, slide, { chrome: false, only: ["vecbox"] });

  // 3. single pipeline arrow (Narrow: no Linear Transformation stage)
  if (process.env.SLIDE045_BASE_ONLY !== "1") drawPipearrow(pptx, slide);

  // 4. concat bar at measured geometry
  if (process.env.SLIDE045_BASE_ONLY !== "1") drawConcatbar45(pptx, slide);

  // 5. head arrows at measured pitch
  if (process.env.SLIDE045_BASE_ONLY !== "1") drawHeadarrows45(pptx, slide);

  // 6. five head cards: inherited, shifted (-7,-38)
  parent.renderBase(pptx, shiftedSlide(slide, DX, DY), { chrome: false, only: ["cards"] });

  // 7. projection equation box (under the h=5 tag, over the cards)
  if (process.env.SLIDE045_BASE_ONLY !== "1") drawEqbox45(pptx, slide);

  // 8. head annotations: parent copy with chips replaced by chunk strips
  drawHeadannots45(pptx, slide);

  // 9. front-card flow + query row + bottom curve: inherited, shifted
  parent.renderBase(pptx, shiftedSlide(slide, DX, DY), {
    chrome: false, only: ["ff_left", "ff_mid", "ff_right", "queryrow", "bottomcurve"],
  });

  // 10. head panels + W chips + swoosh + H-heads label: inherited, shifted
  parent.renderBase(pptx, shiftedSlide(slide, DX, DY), {
    chrome: false, only: ["headpanels", "wochips", "swoosh", "hlabel"],
  });

  // 11. bottom-right Narrow delta
  if (process.env.SLIDE045_BASE_ONLY !== "1") drawBottomRight45(pptx, slide);

  // 12. title (line 2 = Narrow, right-aligned)
  if (process.env.SLIDE045_BASE_ONLY !== "1") drawTitle45(pptx, slide);

  const OUT = process.env.SLIDE045_OUT || path.join(__dirname, "..", "slide_045_recreated.pptx");
  pptx.writeFile({ fileName: OUT }).then(() => {
    console.log("WROTE " + OUT);
  }).catch((e) => { console.error(e); process.exit(1); });
}

build();
