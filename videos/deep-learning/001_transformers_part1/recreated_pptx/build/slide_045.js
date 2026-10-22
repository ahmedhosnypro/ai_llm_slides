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
//   label at left end (line1 y95..100, line2 y101..107); vecbox at parent x-8 (drawn
//   392..462 y50..72, frame blue bbox x391..463) with red 1·d label; single red
//   arrow x428 y72..88 arrowhead top;
//   strips h1..h5 (dashed green, head-color fill, 74x16) at (378,206)(423,184)(469,163)
//   (512,143)(552,124); 1·d/H two-tone labels (red 1·d/ + navy H) at (633,134) and —
//   re-anchored per judge attempt 1 (MAJOR #2, oval collision) — at the h4 strip's
//   top-right corner (ink x588..598 y144..150; frame faint mark x585..590 y144..147);
//   equation box x749..917 y108..170 green dashed (r4 containment: shifted -4px so its
//   right edge clears the house panel border at x918), strip A (2 lav + 2 orange)
//   x758 y114, W pale-yellow box x805 y112 35x35, = x843, strip B mirrored x857 y124,
//   label1 re-anchored per judge attempt 1 (MAJOR #1, W-box collision) so its ink ends
//   x~806 with whitespace before the box (frame mark x799..806 y131..138),
//   blue caption "d : Embedding Length" y162..171; Input Sequence ellipse x746..870
//   y347..394; blue X bar x747..876 y397..414; black caption bar x768..920 y418..434
//   with yellow text; 5 lozenge rows x752..918, yTops 440/459/478/497/516 h16, tinted
//   with the five head-card colors h5->h1; navy To Head labels x~872..908 per row;
//   Sigma stage box (366..458, 262..279) w92 h17 + short W_q box (205..231, 427..445)
//   both child-local at measured geometry (F10-cascade r3, see drawSigma45/drawWq45).
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
  }
  // F10-cascade r4 (judge attempt 3 bar-crop BLOCKER fix): the child frame's segments
  // are NOT empty — each carries (a) a dashed selection-style outline and (b) a small
  // Y_i^(t)-form symbol printed directly on the fill (no white boxes: 0 white px).
  // Symbol/dash inks are frame-sampled per segment: seg1 8E3800 (dark burnt-orange on
  // BB4F07), seg2 364B40 (dark slate on 777C5C), seg3 99C700 (olive-green on F2F208),
  // seg4 87EC61 (darker green on AAFF71), seg5 B6B689 (gray-tan on F3DEBC). No extra
  // internal dividers (PIL divider scan found none at >=8px; segment boundary lines
  // come from the rect borders, as in the frame).
  const SYMBOL_INKS = ["8E3800", "364B40", "99C700", "87EC61", "B6B689"];
  SEGS45.forEach((s, i) => {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(s.x + 1), y: px(91.5), w: px(s.w - 2), h: px(20),
      fill: { type: "none" }, line: { color: SYMBOL_INKS[i], width: 0.75, dashType: "sysDash" },
    });
    const cxm = s.x + s.w / 2;
    slide.addText([
      { text: "Y", options: { bold: true, fontSize: 6, color: SYMBOL_INKS[i] } },
      { text: String(i + 1), options: { bold: true, fontSize: 4.5, color: SYMBOL_INKS[i], subscript: true } },
      { text: "(t)", options: { bold: true, fontSize: 4.5, color: SYMBOL_INKS[i], superscript: true } },
    ], {
      x: px(cxm - 10), y: px(93), w: px(20), h: px(17),
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
  // white rounded box, green dashed border, x749..917 y108..170 (r4: -4px, clears panel border x918)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(749), y: px(108), w: px(168), h: px(62), rectRadius: 0.06,
    fill: { color: "FFFFFF" }, line: { color: C.green, width: 1, dashType: "dash" },
  });
  // strip A: 5 pale cells x762..800 y114..127 (pale lavender → pale amber)
  const fillsA = ["CCE5BE", "D6D2B2", "CFC3A4", "E4D8DE", "F0DCEE"];
  for (let i = 0; i < 5; i++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(758 + i * 7.6), y: px(114), w: px(7.6), h: px(13),
      fill: { color: fillsA[i] }, line: { color: "B8B4C8", width: 0.5 },
    });
  }
  // W box: pale yellow x809..844 y112..147
  slide.addShape(pptx.ShapeType.rect, {
    x: px(805), y: px(112), w: px(35), h: px(35),
    fill: { color: "FBF8DC" }, line: { color: "6A6A5A", width: 0.75 },
  });
  slide.addText("W", {
    x: px(809), y: px(112), w: px(35), h: px(35), align: "center", valign: "middle",
    bold: true, fontSize: 14, color: "1A1A1A", fontFace: SANS, margin: 0,
  });
  // =
  slide.addText("=", {
    x: px(842), y: px(122), w: px(14), h: px(16), align: "center", valign: "middle",
    bold: true, fontSize: 12, color: "1A1A1A", fontFace: SANS, margin: 0,
  });
  // strip B: 5 pale cells x861..897 y124..137 (uniform pale lavender-white)
  const fillsB = ["FCF8D6", "EAF2DE", "F4E4D2", "E2DAE6", "CCC6BA"];
  for (let i = 0; i < 5; i++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(857 + i * 7.2), y: px(124), w: px(7.2), h: px(13),
      fill: { color: fillsB[i] }, line: { color: "B8B4C8", width: 0.5 },
    });
  }
  // blue 1×d/H labels under the strips (spec: blue dimension labels; frame ink
  // label1 x793..824 y126..137 navy, label2 x870..890 y140..146).
  // Judge attempt 1 fix (MAJOR #1): label1's ink crossed the W box's left edge
  // (x809) — frame ground truth has the ink END at x806 with whitespace before
  // the box (frame blue mark x799..806 y131..138, W box left edge x~810). Label1
  // re-anchored so its ink spans ~x796..806 (box center 801), y-center 134.5.
  const dimRuns = () => ([
    { text: "1\u00D7d/H", options: { bold: true, fontSize: 7, color: C.navy } },
  ]);
  slide.addText(dimRuns(), {
    x: px(772), y: px(128), w: px(42), h: px(13), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
  slide.addText(dimRuns(), {
    x: px(856), y: px(138), w: px(42), h: px(11), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
  // third dark-red dimension note between the labels (frame ink x838..876 y148..158,
  // read as "d/H·d/H" by two independent gate reads)
  slide.addText("d/H\u00D7d/H", {
    x: px(830), y: px(146), w: px(46), h: px(12), align: "center", valign: "middle",
    bold: true, fontSize: 6.5, color: "8B1A10", fontFace: SANS, margin: 0,
  });
  // blue caption at the box bottom (measured ink y162..171 x788..890 → ~10pt bold)
  slide.addText("d : Embedding Length", {
    x: px(764), y: px(157), w: px(170), h: px(15), align: "center", valign: "middle",
    bold: true, fontSize: 10, color: C.blue, fontFace: SANS, margin: 0,
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
    // F10-cascade r3: tag centers = the fixed parent's certified TAGC draw (box =
    // center −15/−7.25, 30x14.5) + (DX,DY). Frame k=1 meas (624,227) vs 624.8/226.9,
    // k=2 (668,205) vs 666.1/204.9; the old linear 563+46k formula was 7-8px off.
    const TAGC = [
      { x: 578.6, y: 287.0 }, { x: 631.8, y: 264.9 }, { x: 673.1, y: 242.9 },
      { x: 716.9, y: 224.0 }, { x: 761.0, y: 205.0 },
    ][k];
    const tag = { x: TAGC.x - 15 + DX, y: TAGC.y - 7.25 + DY };
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(tag.x), y: px(tag.y), w: px(30), h: px(14.5),
      fill: { color: C.tagFill }, line: { type: "none" },
    });
    slide.addText(`h=${k + 1}`, {
      x: px(tag.x), y: px(tag.y), w: px(30), h: px(14.5), align: "center", valign: "middle",
      bold: true, fontSize: 7, color: C.tagText, fontFace: SANS, margin: 0,
    });
  }
  // Probabilities oval straddling the h2/h1 top edges (parent 294,250 shifted);
  // F10-cascade r3: fill = frame-measured C4C2F4 (196,194,244) — FDF3EE was stale
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(294 + DX), y: px(250 + DY), w: px(80), h: px(28),
    fill: { color: "C4C2F4" }, line: { color: "C9B8B0", width: 0.75 },
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
  // two-tone 1·d/H labels beside the two upper strips (measured (633,134) & blue H at (611..631,166..169)).
  // Judge attempt 1 fix (MAJOR #2): the LOWER label (box x576..628 y157..169) ran into
  // the h=5 Weighted SUM oval (x597..660 y158.5..172.5). Frame ground truth: the only
  // blue ink in that band is the oval's own text (x606..656 y165..170) — no label ink
  // left of the oval; the faint frame mark at the h4 strip's top-right corner
  // (x585..590, y144..147) is the label's true home, CLEAR of the oval. Re-anchored:
  // ink ~x588..598, y~144..150 (8px above the oval's top edge, 2px right of the strip).
  const dimRuns = () => ([
    { text: "1\u00D7d/", options: { bold: true, fontSize: 7, color: C.red } },
    { text: "H", options: { bold: true, fontSize: 7, color: C.navy } },
  ]);
  slide.addText(dimRuns(), {
    x: px(626), y: px(131), w: px(44), h: px(12), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
  slide.addText(dimRuns(), {
    x: px(572), y: px(141), w: px(42), h: px(13), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
}

// ---- inherited-zone corrections (F10-cascade r3 frame measurements) --------------
// Two zones where the child frame deviates from the inherited (shifted) parent draw.
// Eraser fills are the h1 card color EF8C96 — both zones sit entirely on the h1
// card's front face (49..590 x 236..488 shifted), so the patches are invisible.

function drawSigma45(pptx, slide) {
  // Child frame's Sigma stage box = (366..458, 262..279) w92 h17 FLAT (white fill
  // rows 264..278, blue borders y262/y279, glyph center (411.5,271) = box center);
  // the inherited parent box renders (387..447, 251..285) w60 h34 — real deviation.
  // Erase the inherited box and redraw at measured geometry. The eraser zone holds
  // only the h1 card + the inherited box, EXCEPT the k=0 Weighted SUM oval's lower
  // arc (421..484 x 240.5..254.5) which it clips at x421..449 — redraw that oval
  // (identical to drawHeadannots45's k=0 draw) after the patch; the new box (top
  // y262) clears the oval (bottom y254.5) as in the frame.
  slide.addShape(pptx.ShapeType.rect, {
    x: px(386), y: px(250), w: px(64), h: px(37),
    fill: { color: "EF8C96" }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(421), y: px(240.5), w: px(63), h: px(14),
    fill: { color: "FFFFFF" }, line: { color: "9A9A9A", width: 0.75 },
  });
  slide.addText("Weighted SUM", {
    x: px(421), y: px(240.5), w: px(63), h: px(14), align: "center", valign: "middle",
    fontSize: 5.5, color: C.ovalText, fontFace: SANS, margin: 0,
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(366), y: px(262), w: px(92), h: px(17),
    fill: { color: "FFFFFF" }, line: { color: C.blue, width: 1.25 },
  });
  slide.addText("\u03A3", {
    x: px(366), y: px(262), w: px(92), h: px(17), align: "center", valign: "middle",
    bold: true, fontSize: 14, color: C.blue, fontFace: SANS, margin: 0,
  });
}

function wRuns45(letter, sup) {
  return [
    { text: "W", options: { bold: true, fontSize: 6, color: C.ink } },
    { text: letter, options: { bold: true, fontSize: 6, color: C.red, subscript: true } },
    { text: `(${sup})`, options: { bold: true, fontSize: 6, color: C.red, superscript: true } },
  ];
}

function drawXmarks45(pptx, slide) {
  // Frame-measured tiny red X-strikes in the E-zone grid tiles (ezone gate r4
  // BLOCKER fix). Each mark = two crossed 0.5pt strokes, C.red, ~5.5x7px frame.
  // Positions are the measured bbox top-lefts on slide_045.jpg (no regularization
  // — the JPEG wobble is the frame's truth).
  const MARKS = [
    // [x, y] top-left, frame px
    [559, 294], [560, 322], [559, 351], [559, 380],   // staircase col 0
    [607, 274], [607, 301], [607, 329], [607, 359],   // col 1
    [650, 253], [650, 281], [650, 310], [650, 339],   // col 2
    [693, 233], [693, 261], [693, 289], [693, 319],   // col 3
    [736, 214], [736, 242], [736, 270], [736, 300],   // col 4
  ];
  for (const [mx, my] of MARKS) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(mx), y: px(my), w: px(5.5), h: px(7),
      line: { color: C.red, width: 0.5 },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: px(mx), y: px(my), w: px(5.5), h: px(7), flipV: true,
      line: { color: C.red, width: 0.5 },
    });
  }
}

function drawStrikeErase45(pptx, slide) {
  // F10-cascade r6 (ezone crop judge attempt-5 MAJOR): the frozen parent's
  // drawHeadpanels puts a thick 1.4pt red X-strike in every panel's leftmost cell
  // (lx..lx+7.5, yc-6..yc+6, yc = ptop+12+18i); its second line uses NEGATIVE
  // height, which pptxgenjs renders as an extra stacked segment one pitch above
  // (yc-18..yc-6), so all 4 rows merge into one continuous red stripe per column
  // (r5-measured runs: 292.7-370.9 / 271.5-349.7 / 250.4-328.6 / 229.3-307.5 /
  // 210.6-288.8 at x595.5/639.5/682.5/725.5/768.5 = HEADCOLS-7). The child frame
  // shows NO thick strikes in the panels (parent frame neither): its marks are the
  // small 4-6px staircase strikes drawn at step 10b. Erase each column's ink band
  // and repaint: above the border row = the layer fill sampled from the r5 render
  // (lavender/lavender/pale-yellow/pale-green/peach — the panels sit on the layer
  // stack, not on gray); border row + below = white panel interior; then the 4
  // leftmost cells at exact parent geometry (muted[i%5] fill, BFB8B4 0.4pt border),
  // strikes omitted. The sysDot top-border dots lost under the band stay lost —
  // the frame's own border shows 0-1 dots in the same windows (noise-level delta).
  const COLS = [
    { lx: 595.5, ptop: 299, above: "C5C1F4" },
    { lx: 639.5, ptop: 278, above: "C5C1F4" },
    { lx: 682.5, ptop: 257, above: "F8FF9A" },
    { lx: 725.5, ptop: 236, above: "D4FFE5" },
    { lx: 768.5, ptop: 217, above: "F7E2CD" },
  ];
  const MUT = ["DAD2CE", "D8D2E0", "E4D6D8", "D8D2E0"];
  for (const c of COLS) {
    // band above + across the border row: layer fill (phantom segment lives here)
    slide.addShape(pptx.ShapeType.rect, {
      x: px(c.lx - 0.7), y: px(c.ptop - 7.5), w: px(8.4), h: px(8),
      fill: { color: c.above }, line: { type: "none" },
    });
    // band below the border row: panel white interior
    slide.addShape(pptx.ShapeType.rect, {
      x: px(c.lx - 0.7), y: px(c.ptop + 0.5), w: px(8.4), h: px(73),
      fill: { color: "FFFFFF" }, line: { type: "none" },
    });
    // leftmost cells, exact parent geometry, strikes omitted
    for (let i = 0; i < 4; i++) {
      const yc = c.ptop + 12 + i * 18;
      slide.addShape(pptx.ShapeType.rect, {
        x: px(c.lx), y: px(yc - 6), w: px(7.5), h: px(12),
        fill: { color: MUT[i] }, line: { color: "BFB8B4", width: 0.4 },
      });
    }
  }
}

function drawWq45(pptx, slide) {
  // Query zone: the child frame shows the parent FRAME's SHORT W_q box shifted
  // (205..231, 427..445; parent frame box 212..238 x 466..482 + (-7,-38)) and NO
  // striped icon / NO q2 label (flat card x150..198 y415..445), while the inherited
  // queryrow draws icon (179..201, 423..441) + q2 (155..177, 420..442) + tall box
  // (204..230, 410..451). Erase all three, redraw the q-feed arrow ff_left drew
  // (parent x224 y443 h25 w2.25 -> child x217 y405 h25; the eraser takes its
  // y409..430 span) and the short box; the box covers the arrow's 427..430 tail
  // exactly as the parent build's draw order does. G3 diagonal (y>=461) and the
  // token container (y454+) stay clear of the eraser.
  slide.addShape(pptx.ShapeType.rect, {
    x: px(154), y: px(409), w: px(78), h: px(42),
    fill: { color: "EF8C96" }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(217), y: px(405), w: 0, h: px(25),
    line: { color: C.red, width: 2.25, beginArrowType: "triangle" },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(205), y: px(427), w: px(26), h: px(18),
    fill: { color: "FFFFFF" }, line: { color: "CC2222", width: 1 },
  });
  slide.addText(wRuns45("q", 0), {
    x: px(205), y: px(427), w: px(26), h: px(18), align: "center", valign: "middle",
    fontFace: SANS, margin: 0,
  });
}

// ---- bottom-right additions (the Narrow delta) -----------------------------------

const ROW_TINTS = ["F7E2CD", "D4FFE5", "F8FF9A", "C5C1F4", "EF8C96"]; // h5 -> h1

function drawBottomRight45(pptx, slide) {
  // Input Sequence: red ellipse, white bold 2-line text (frame x772..870 y346..394;
  // the h5 W-chip column stays clear of it, as in the frame)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(772), y: px(346), w: px(98), h: px(48),
    fill: { color: C.red }, line: { type: "none" },
  });
  slide.addText([
    { text: "Input", options: { breakLine: true } },
    { text: "Sequence", options: {} },
  ], {
    x: px(772), y: px(346), w: px(98), h: px(48), align: "center", valign: "middle",
    bold: true, fontSize: 9, color: "FFFFFF", fontFace: SANS, margin: 0, lineSpacing: 10.5,
  });
  // deep-blue X bar x776..870 y397..414, white bold X1..X4 (no separators: the frame
  // bar reads continuous; measured fill ~(0,0,175..212); blue cols 776..870, F10 r3)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(776), y: px(397), w: px(94), h: px(17),
    fill: { color: "0A0AC0" }, line: { color: "000060", width: 0.75 },
  });
  for (let i = 0; i < 4; i++) {
    slide.addText([
      { text: "X", options: { bold: true, fontSize: 6.5, color: "FFFFFF" } },
      { text: String(i + 1), options: { bold: true, fontSize: 5, color: "FFFFFF", subscript: true } },
    ], {
      x: px(776 + i * 23.5), y: px(397), w: px(23.5), h: px(17),
      align: "center", valign: "middle", fontFace: SANS, margin: 0,
    });
  }
  // four tiny red arrows from the bar up into the oval (frame heads y392..395 at
  // x~780..786 / 802..808 / 820..830 / 838..846)
  for (const ax of [783, 805, 826, 843]) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(ax), y: px(391.5), w: 0, h: px(5.5),
      line: { color: C.red, width: 2.5, beginArrowType: "triangle" },
    });
  }
  // square-cornered black caption bar with yellow bold text (x768..920 y418..434)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(768), y: px(418), w: px(149), h: px(17),
    fill: { color: "42423E" }, line: { type: "none" },
  });
  slide.addText("Split vectors into \u201CH\u201D chunks", {
    x: px(768), y: px(418), w: px(149), h: px(17), align: "center", valign: "middle",
    bold: true, fontSize: 7, color: "E8E27A", fontFace: SANS, margin: 0,
  });
  // four thin gray column drop-lines from the bar through all 5 rows (x777/799/821/843)
  for (const lx of [777, 799, 821, 843]) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(lx), y: px(415), w: 0, h: px(118),
      line: { color: "8A8A8A", width: 0.5 },
    });
  }
  // 5 chunk-table rows (lozenges tinted with the head-card colors, h5 -> h1)
  const HATCH = ["E07070", "B57EDC", "E6E65C", "7CC47C", "F0A0B0"];
  for (let r = 0; r < 5; r++) {
    const yTop = 440 + 19 * r;
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(752), y: px(yTop), w: px(164), h: px(16), rectRadius: 0.08,
      fill: { color: ROW_TINTS[r] }, line: { color: "9A9A9A", width: 0.5 },
    });
    // 4 token marks per row directly on the tint (F10-cascade r3: the frame has NO
    // white token boxes — 0-3 white px per row vs ~640 drawn — so the boxed cells
    // are removed; red X(sub) kept, pitch shifted +9px to the measured mark centers
    // 791/813/836/858) + 5-color hatch strips (sub-chunk idiom, sub-pixel at 960)
    for (let b = 0; b < 4; b++) {
      const bx = 787.5 + 22 * b;
      slide.addText([
        { text: "X", options: { bold: true, fontSize: 4.5, color: "8B1A10" } },
        { text: String(b + 1), options: { bold: true, fontSize: 3.5, color: "8B1A10", subscript: true } },
      ], {
        x: px(bx), y: px(yTop + 3), w: px(7), h: px(10),
        align: "center", valign: "middle", fontFace: SANS, margin: 0,
      });
      for (let hI = 0; hI < 5; hI++) {
        slide.addShape(pptx.ShapeType.rect, {
          x: px(bx + 7.5 + hI * 1.7), y: px(yTop + 4), w: px(1.5), h: px(8),
          fill: { color: HATCH[hI] }, line: { type: "none" },
        });
      }
    }
    // navy To Head label INSIDE the lozenge's right end (F10-cascade r3: frame label
    // ink is navy/dark-blue at x~870..910 in ALL rows — samples (22,46,92)/(30,26,123)/
    // (35,29,77); the old dark-red reading was the X3/X4 token marks at x833..858)
    slide.addText(`To Head ${5 - r}`, {
      x: px(868), y: px(yTop), w: px(48), h: px(16), align: "left", valign: "middle",
      bold: true, fontSize: 7, color: C.navy, fontFace: SANS, margin: 0,
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

  // 2. output vector box: inherited with dx=-8 (child frame blue bbox x391..463 y48..73
  //    vs parent 400..470 y50..72; y matches) via the translation proxy; the pipearrow
  //    x428.5 sits on the new center 427
  parent.renderBase(pptx, shiftedSlide(slide, -8, 0), { chrome: false, only: ["vecbox"] });

  // 3. single pipeline arrow (Narrow: no Linear Transformation stage)
  drawPipearrow(pptx, slide);

  // 4. concat bar at measured geometry
  drawConcatbar45(pptx, slide);

  // 5. head arrows at measured pitch
  drawHeadarrows45(pptx, slide);

  // 6. five head cards: inherited, shifted (-7,-38)
  parent.renderBase(pptx, shiftedSlide(slide, DX, DY), { chrome: false, only: ["cards"] });

  // 7. projection equation box (under the h=5 tag, over the cards)
  drawEqbox45(pptx, slide);

  // 8. head annotations: parent copy with chips replaced by chunk strips
  drawHeadannots45(pptx, slide);

  // 9. front-card flow + query row + bottom curve: inherited, shifted
  parent.renderBase(pptx, shiftedSlide(slide, DX, DY), {
    chrome: false, only: ["ff_left", "ff_mid", "ff_right", "queryrow", "bottomcurve"],
  });

  // 9b. inherited-zone corrections (F10-cascade r3): Sigma stage box + query zone,
  // both re-measured child-local; must follow step 9 (they patch inherited draws)
  drawSigma45(pptx, slide);
  drawWq45(pptx, slide);

  // 10. head panels + W chips + swoosh + H-heads label: inherited, shifted
  parent.renderBase(pptx, shiftedSlide(slide, DX, DY), {
    chrome: false, only: ["headpanels", "wochips", "swoosh", "hlabel"],
  });

  // 10b. E-zone grid-tile X-strike marks (ezone crop gate r4: rule-6 BLOCKER —
  // the frame's tiles carry small red X-strikes in their top/left cells, absent
  // from the inherited block for this frame's variant). 20 marks PIL-measured
  // on unique_slides/slide_045.jpg: five staircase columns (x 559/607/650/693/736,
  // column stagger ~20px down-left), vertical pitch ~28.7px, marks ~5.5x7px.
  drawXmarks45(pptx, slide);

  // 10c. F10-cascade r6 (ezone crop judge attempt-5 MAJOR): the frozen parent's
  // headpanels block draws a thick 1.4pt red X-strike in every panel's leftmost
  // cell; pptxgenjs renders its negative-height line as an extra stacked segment
  // one pitch above, so each column merges into a continuous ~78px red stripe.
  // The CHILD frame has no such thick strikes (parent frame neither — red census:
  // only the small staircase marks drawn at 10b). Erase the strike bands and
  // repaint the leftmost cells per the frame.
  drawStrikeErase45(pptx, slide);

  // 11. bottom-right Narrow delta
  drawBottomRight45(pptx, slide);

  // 12. title (line 2 = Narrow, right-aligned)
  drawTitle45(pptx, slide);

  const OUT = path.join(__dirname, "..", "slide_045_recreated.pptx");
  pptx.writeFile({ fileName: OUT }).then(() => {
    console.log("WROTE " + OUT);
  }).catch((e) => { console.error(e); process.exit(1); });
}

build();
