// slide_008.js — "Self Attention Mechanism (Linear Transformation of Inputs)" /
// "(Self Attention of word X₂ w.r.t All words in Sentence ( X₁, X₂, X₃, X₄ )"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 8)
//
// CROSS-VIDEO CHILD BUILD (founder directive 2026-10-11, dependency law v2):
// parent = deep-learning/001_transformers_part1:33 (CERTIFIED in 001's own DB:
// gen_status=passed + visual_check=PASS). This build IMPORTS the parent's certified
// component by ABSOLUTE PATH and draws only THIS slide's measured delta — never a
// copy-paste of the composition. Ground truth: unique_slides/slide_008.jpg
// (founder frame swap recorded; frame on disk is canonical — new2old_mapping.json).
//
// FRAME->SLIDE MAPPING (video-002 capture zoomed ~0.958 with letterbox; deck fit
// identical within ~1px to the certified slide_002.js / slide_013.js fits; landmarks
// re-verified on THIS frame, scratch/slide008/landmarks.py: left border 58.5,
// right 901.5, top 42.5, bottom stroke 516.5, badge center (875.5, 71.0) raw):
//   slide_x = (frame_x - 17.628) / 0.961232 ;  slide_y = frame_y / 0.955556
// All delta geometry below is written in TRUE SLIDE px (1px = 1pt = 1/72 in),
// measured on the remapped frame (scratch/slide008/delta.py, measure2-6.py).
//
// MEASURED DELTAS vs the parent composition (all PIL-measured on 002:8):
//   * W_k / W_v stages: the parent's YELLOW BANDS + boxes are ABSENT. Instead 4+4
//     narrow boxes: left x161..195 pale-green fill (192,250,200), green border;
//     right x707..741 pale-cyan fill (205,250,244), dark slate border; tops
//     236/277/318/362, h25; BLACK bold labels (frame text cores (0,0,0)).
//   * Multiply circles: PEACH-filled (panel-colored interiors measured), not white —
//     parent's white circles overlaid with peach ones at the same certified centers.
//   * K.q label sits at ink x347..367, y201..212 (parent's certified x332 box) —
//     the dot-product block is redrawn at parent-verified geometry with K.q moved.
//   * Query path: W_q box x275..322, y432..480 (yellow, parent fill/border family);
//     q2 label at ink y383..395 (~26px HIGHER than parent's); W_q->DP arrow x300
//     y404..432; NO X2->W_q arrow and NO q2 mini-vector visible in this frame
//     (step-1 scans found neither — omitted, documented).
//   * Overlays: the parent's dark-red K2 circle is ABSENT. This frame shows a large
//     translucent blue annotation circle, center (300,447) r~60 (diff-tint fit),
//     alpha ~0.36 over yellow/peach (obs=α·4169E1+(1-α)·bg), covering the W_q box,
//     q2 lower half, DP-box bottom-left and the sentence-row top; plus a chunky dark
//     red block arrow x269..289, y513..529 pointing up-right at X2 (smaller than the
//     parent's). Both drawn AFTER the query so the circle tints them, per frame.
//   * Flow/orange lines re-anchored to the measured rows LINEY8 = 249/291/333/375
//     and the narrower box edges (container->W_k tri tips at x160; W_k->DP from
//     x196; right side identical to parent: tri tip x741, line 763->753).
//   * Title: same text/spans/colors as the parent (ink spans match within 2px) but
//     sits +2..3px lower in this deck (002 template drift — badge included, verified
//     against 001:33's own native badge) — redrawn at y56/y83.
//   * Systematic note: ALL 002:8 content sits +2..3px below the parent's certified
//     geometry in true slide coords (verified per-block). The chrome law pins the
//     badge to the house position (founder directive overrides the frame); content
//     stays frame-true. Import-vs-redraw decision per block: differences <=3px
//     import the certified block (closed-loop gate 6 render-px); larger deltas are
//     redrawn at measured values.
//
// IMPORTED parent blocks (renderBase): panel, sentence, connectors, containers,
//   softmax, faintarrows, sigma, y2, pills, legend, title->(redrawn), chrome(8).
// SKIPPED + redrawn: wboxes, flowlines, kvlabels(z-order), dotproduct, query,
//   orangeheads, overlays.
//
// LAWS honored: playlist chrome via the parent's own house_chrome delegate (drawn
// ONCE inside renderBase, numeral 8 = the number printed on THIS frame); verbatim
// text (title/subtitle/pills/labels verbatim from the certified parent + spec);
// margin:0 + explicit fontFace; explicit lineSpacing on the two-line Dot/Product
// box (13pt, parent-certified); no '#' in hex; single-version plain-named
// deliverable; never writes outside this video's namespace.

const pptxgen = require("pptxgenjs");
const P = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_033.js"
);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const px = P.px; // frame/slide px -> inches (1px = 1pt)
const FONT = "Arial";

// ---- measured 002:8 geometry (true slide px) --------------------------------------
const LINEY8 = [249, 291, 333, 375];            // K/V row centerlines (arrowhead rows)
const DOTC8 = [[332, 249], [316, 290], [298, 331], [279, 375]]; // DP dot centers
const DOTX8 = [332, 316, 298, 279];             // dot x per row
const WTOPS = [236, 277, 318, 362];             // W-box tops (both sides)
const WK = { x: 161, w: 34, fill: "C0FAC8", border: "69AC76" };
const WV = { x: 707, w: 34, fill: "CDF9F4", border: "3C3769" };

const s = pres.addSlide();

// ---- 1. parent certified composition (chrome numeral 8 + imported blocks) ----------
P.renderBase(pres, s, {
  numeral: 8,
  skip: ["wboxes", "flowlines", "kvlabels", "dotproduct", "query", "orangeheads", "overlays", "title", "sentence"],
});

// ---- shared helpers (parent's line/tri idioms, re-pointed at measured anchors) ------
function redArrow(x1, y1, x2, y2, width, opts = {}) {
  s.addShape(pres.ShapeType.line, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: {
      color: opts.color || P.C.red, width: width || 1.25,
      endArrowType: opts.head === false ? undefined : "triangle",
      dashType: opts.dash,
    },
  });
}
function tri(x, y, w, h, dir, color) {
  s.addShape(pres.ShapeType.triangle, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    rotate: dir === "right" ? 90 : 270,
    fill: { color: color || P.C.orange }, line: { type: "none" },
  });
}
function wBox8(spec, y, sub) {
  s.addShape(pres.ShapeType.rect, {
    x: px(spec.x), y: px(y), w: px(spec.w), h: px(25),
    fill: { color: spec.fill }, line: { color: spec.border, width: 1 },
  });
  s.addText(
    [
      { text: "W", options: {} },
      { text: sub, options: { subscript: true } },
      { text: "(r)", options: { superscript: true, fontSize: 6 } },
    ],
    {
      x: px(spec.x), y: px(y), w: px(spec.w), h: px(25),
      align: "center", valign: "middle", margin: 0, wrap: false,
      fontFace: FONT, fontSize: 9.5, bold: true, color: "000000",
    }
  );
}

// ---- 2. delta: sentence row (container top measured at y477 in THIS frame vs the
// parent's certified y473; widgets/highlight pixel-verified identical -> parent values)
s.addShape(pres.ShapeType.roundRect, {
  x: px(177), y: px(477), w: px(315), h: px(41), rectRadius: 0.06,
  fill: { color: P.C.containerFill },
  line: { color: P.C.containerBorder, width: 1.25, dashType: "sysDot" },
});
function embedWidget8(x, y, w, h, label, cells) {
  const cw = w / 5;
  const fills = cells || [P.C.cell1, P.C.cell2, P.C.cell3, P.C.cell4, P.C.cell5];
  for (let i = 0; i < 5; i++) {
    s.addShape(pres.ShapeType.rect, {
      x: px(x + i * cw), y: px(y), w: px(cw), h: px(h),
      fill: { color: fills[i] }, line: { color: P.C.divider, width: 0.5 },
    });
  }
  s.addText(
    [
      { text: "X", options: {} },
      { text: label, options: { subscript: true } },
    ],
    {
      x: px(x + 1.5 * cw), y: px(y - 2), w: px(2 * cw), h: px(h + 4),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 11, bold: true, color: P.C.labelRed,
    }
  );
}
embedWidget8(189, 481, 66, 24, "1");
embedWidget8(257, 481, 75, 24, "2", [P.C.x2c1, P.C.x2c2, P.C.x2c3, P.C.x2c4, P.C.x2c5]);
s.addShape(pres.ShapeType.roundRect, {
  x: px(255), y: px(479), w: px(79), h: px(28), rectRadius: 0.04,
  fill: { type: "none" },
  line: { color: P.C.x2border, width: 1.5, dashType: "sysDot" },
});
embedWidget8(335, 481, 66, 24, "3");
embedWidget8(403, 481, 66, 24, "4");

// ---- 3. delta: flow lines UNDER boxes/vectors (parent z-order) ----------------------
// container -> W_k box (short, no head; orange tri added later)
LINEY8.forEach((y) => redArrow(142, y, 153, y, 1.5, { head: false }));
// W_k box -> DP dot (long, arrowhead at the dot)
LINEY8.forEach((y, i) => redArrow(196, y, DOTX8[i] - 8, y, 1.25));
// right container -> W_v box (short, no head) — identical to parent's anchors
LINEY8.forEach((y) => redArrow(763, y, 753, y, 1.5, { head: false }));
// converging lines from the bottom convergence point up to each dot (parent geometry,
// re-pointed at the measured dots; DP bottom 400 like the parent's 399 anchor)
DOTC8.forEach(([cx, cy]) => {
  s.addShape(pres.ShapeType.line, {
    x: px(Math.min(cx, 300)), y: px(cy), w: px(Math.abs(cx - 300)), h: px(399 - cy),
    flipV: cx > 300,
    line: { color: P.C.red, width: 1 },
  });
});

// ---- 3. delta: K/V vectors + labels re-drawn at certified z (ABOVE the flow lines) --
P.BLOCKS.kvlabels(pres, s);

// ---- 4. delta: Dot Product box (parent-verified geometry; K.q moved to x345) --------
s.addShape(pres.ShapeType.rect, {
  x: px(255), y: px(194), w: px(87), h: px(208),
  fill: { color: P.C.dpFill }, line: { color: P.C.dpBorder, width: 1 },
});
s.addText(
  [
    { text: "Dot", options: { breakLine: true } },
    { text: "Product", options: {} },
  ],
  {
    x: px(262), y: px(196), w: px(72), h: px(34),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 11, bold: true, color: P.C.dpTitle, lineSpacing: 13,
  }
);
s.addText("K.q", {
  x: px(347), y: px(196), w: px(30), h: px(20),
  align: "left", valign: "top", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 13, bold: true, color: P.C.kq,
});

DOTC8.forEach(([cx, cy]) => {
  s.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 6.5), y: px(cy - 6.5), w: px(13), h: px(13),
    fill: { color: P.C.dotHalo }, line: { color: "6F8FC0", width: 0.5 },
  });
  s.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 3.5), y: px(cy - 3.5), w: px(7), h: px(7),
    fill: { color: P.C.dotCore }, line: { type: "none" },
  });
});

// ---- 5. delta: W_k / W_v boxes (NO yellow band in this frame) ------------------------
WTOPS.forEach((y) => wBox8(WK, y, "k"));
WTOPS.forEach((y) => wBox8(WV, y, "v"));

// ---- 6. delta: orange arrowheads on the box borders (parent idiom, moved tips) -------
LINEY8.forEach((y) => tri(152, y - 4.5, 8, 9, "right"));   // into W_k left edge (x161)
LINEY8.forEach((y) => tri(741, y - 4.5, 8, 9, "left"));    // into W_v right edge (x741)

// ---- 7. delta: multiply circles are PEACH-filled here — overlay at certified centers --
P.GEO.CIRC.forEach(([cx, cy]) => {
  s.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 9.5), y: px(cy - 9.5), w: px(19), h: px(19),
    fill: { color: P.C.peachPanel }, line: { color: P.C.red, width: 1.5 },
  });
  s.addText("*", {
    x: px(cx - 9.5), y: px(cy - 9.5), w: px(19), h: px(19),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 14, bold: true, color: P.C.red,
  });
});

// ---- 8. delta: query path (measured: box lower/narrower, q2 much higher) -------------
// W_q box (yellow family under the blue tint; parent fill/border — unmeasurable
// through the translucent circle, certified family kept)
s.addShape(pres.ShapeType.rect, {
  x: px(275), y: px(432), w: px(47), h: px(48),
  fill: { color: P.C.band }, line: { color: P.C.boxBorder, width: 1 },
});
s.addText(
  [
    { text: "W", options: {} },
    { text: "q", options: { subscript: true } },
    { text: "(r)", options: { superscript: true, fontSize: 6 } },
  ],
  {
    x: px(275), y: px(432), w: px(47), h: px(48),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 11, bold: true, color: P.C.olive,
  }
);
// q2 label (measured ink y383..395, x280..292; bottom half sits under the circle)
s.addText(
  [
    { text: "q", options: {} },
    { text: "2", options: { subscript: true } },
  ],
  {
    x: px(277), y: px(379), w: px(26), h: px(22),
    align: "left", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 12, bold: true, color: P.C.qRed,
  }
);
// W_q -> DP box arrow (vertical, head at the DP bottom; visible ink x300 y410..414+)
redArrow(300, 432, 300, 404, 1.5);
// NOTE: no X2->W_q arrow and no q2 mini-vector — step-1 scans of the frame found
// neither (box bottom 480 abuts the sentence widget top 481; vector region shows
// only convergence-line ink). Omitted deliberately.

// ---- 9. delta: title redrawn +2..3px lower (002 template drift; text verbatim) -------
s.addText(
  [
    { text: "Self Attention Mechanism ", options: { color: "000000" } },
    { text: "(Linear Transformation of Inputs)", options: { color: P.C.titleBlue } },
  ],
  {
    x: px(183), y: px(56), w: px(650), h: px(24),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 20, bold: true,
  }
);
s.addText(
  [
    { text: "(Self Attention of word ", options: { color: "000000" } },
    { text: "X", options: { color: P.C.titleRed } },
    { text: "2", options: { subscript: true, color: P.C.titleRed } },
    { text: " w.r.t All words in Sentence ( ", options: { color: "000000" } },
    { text: "X", options: { color: P.C.titleRed } },
    { text: "1", options: { subscript: true, color: P.C.titleRed } },
    { text: ", ", options: { color: P.C.titleRed } },
    { text: "X", options: { color: P.C.titleRed } },
    { text: "2", options: { subscript: true, color: P.C.titleRed } },
    { text: ", ", options: { color: P.C.titleRed } },
    { text: "X", options: { color: P.C.titleRed } },
    { text: "3", options: { subscript: true, color: P.C.titleRed } },
    { text: ", ", options: { color: P.C.titleRed } },
    { text: "X", options: { color: P.C.titleRed } },
    { text: "4", options: { subscript: true, color: P.C.titleRed } },
    { text: " )", options: { color: "000000" } },
  ],
  {
    x: px(183), y: px(81), w: px(650), h: px(24),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 20, bold: true,
  }
);

// ---- 10. delta: overlays LAST (the circle tints the query/DP/sentence below it) -------
// translucent blue annotation circle: center (300,447) r60, alpha ~0.36
s.addShape(pres.ShapeType.ellipse, {
  x: px(240), y: px(387), w: px(120), h: px(120),
  fill: { color: "4169E1", transparency: 64 }, line: { type: "none" },
});
// chunky dark-red block arrow pointing up-right at X2 (measured x269..289, y513..529)
s.addShape(pres.ShapeType.rightArrow, {
  x: px(268), y: px(514), w: px(22), h: px(13), rotate: 326,
  fill: { color: P.C.redDark }, line: { type: "none" },
});

// ---- 11. delta: legend W box border is OLIVE-TAN in this frame (measured
// (177,162,115)/(203,187,138) vs the parent's orange C87A2A) — overlay at the
// same rect; fill covers the orange stroke, olive border redrawn on top.
s.addShape(pres.ShapeType.rect, {
  x: px(798), y: px(472), w: px(29), h: px(29),
  fill: { color: P.C.legW }, line: { color: "B4A56E", width: 1.5 },
});
s.addText("W", {
  x: px(798), y: px(472), w: px(29), h: px(29),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 14, bold: true, color: "000000",
});

// ---- write ---------------------------------------------------------------------------
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_008_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
