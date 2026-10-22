// slide_017.js — "Multi Head Self Attention of Word X2" (recap, badge numeral 17)
// Deep Learning DSAI 308, video 002_transformers_part2, slide 17.
//
// CROSS-VIDEO CHILD (founder directive 2026-10-11): 17 <- deep-learning/001_transformers_part1:43
// (certified in the parent's own DB: gen_status=passed, visual_check=PASS). The parent's
// certified component is REQUIRED below by ABSOLUTE path; its renderBase supplies the
// playlist house chrome (drawn ONCE in the component) with THIS slide's numeral (17).
//
// DELTA LAW (dependencies.md + dispatch build law): the recap composition is IMPORTED,
// never re-drawn wholesale; blocks whose measured geometry/fill deviate in THIS frame are
// composed per-block (opts.skip) and re-drawn at THIS frame's measured geometry. Evidence:
// scratch/slide017/ — fit_mapping.py (mapping fit + chrome-landmark check), ff-frame PIL
// diff + per-zone census scripts, ASCII zone maps, side-by-side gate sheets s1..s7
// (transcripts sheets/tr/*.txt) + the previous worker's banked crop reads an_*.txt.
//
// MEASURED DELTAS implemented here:
//   1. Title: ONE line only (no '"Wide" Architecture' line — sheet s1, an_title,
//      an_sheetA1). Parent 'title' skipped; line 1 re-drawn at the parent's own geometry.
//   2. Badge numeral 17 (opts.numeral — the number printed on THIS frame).
//   3. W_k column (ff_left): THIS frame adds a continuous GOLD column panel
//      (slide x122..159, y322..438; PIL gold census + ASCII map) behind the four W_k
//      boxes, whose fill reads yellow-green (~D2E455, i.e. the parent's pale boxes as
//      seen through the gold wash — sheet s3 "translucent yellow/orange highlight
//      rectangle enclosing the four green W_k boxes"); K strips shifted right to
//      x163..184 (parent 156..184). ff_left skipped and redrawn at parent geometry for
//      everything else (input container/cells/labels/arrows, Dot Product box, target
//      circles, q1 arrow — frame-vs-frame diff shows no delta there).
//   4. W_v column (ff_right): same gold-panel treatment (panel x~499..537, y322..438;
//      boxes yellow-green x~502..534), V bars shifted right/narrower (x480..502, 4 cells,
//      vs parent 468..504), V labels shifted right (x~464 vs parent 452) and their
//      subscripts run DESCENDING top->bottom (V4,V3,V2,V1 — an_vlab 5x read of THIS
//      frame; sheet s4 reads both frames' columns with the same non-sequential pattern).
//      ff_right skipped and redrawn; nodes, node->Sigma arrows and the dashed X-cells box
//      stay at parent geometry (no frame delta).
//   5. Swoosh label: literal double-quoted «"H" Heads» — THIS lecture's notation
//      (an_rightswoosh 2x; s8 micro-sheet: BOTH frames read «"H" Heads») — AND its
//      measured position: ink at slide x765..805 y340..377 (s8 + PIL blue census) on the
//      swoosh's upper-right segment; the parent hlabel box (x612-708) is skipped and the
//      label redrawn at the measured position.
//   [legend right-icon patch: sheet s6b read — legend IDENTICAL both bands, inherited]
//   KEPT INHERITED (no frame delta): vecbox, pipearrows, ltbox, concatbar, headarrows,
//   cards, headannots, ff_mid, queryrow, bottomcurve, headpanels, wochips, legend.
//   6. Swoosh ARROW redrawn (attempt 2, resume worker 2): THIS frame's return arrow is
//      BRIGHT red (stroke core #C10002, head (195,0,8)) vs the parent's dark-red swoosh
//      image (core #840E07), and runs further: centerline (swoosh_probe_outputs.txt)
//      tail (550,455) -> hook (565,461) -> (600,445) -> (660,416) -> (700,396) ->
//      (745,374) -> (772,358); solid head ink (775..800, 333..356) — the parent's image
//      box (585..760, 325..475) covers neither extent. 'swoosh' skipped + redrawn as
//      thick C00000 segments + triangle head (judge retry1 flagged the path difference,
//      retry2 contradicted; PIL decides for the frame). Evidence:
//      scratch/slide017/swoosh_delta_evidence.md + swoosh_probe_outputs.txt.
//
//   7. F10-CASCADE ALIGNMENT PASS (casc-f10-002-17-20261014, attempt 3): after the
//      parent's F10 rework (component md5 c8b643db...), the 13 inherited blocks pull
//      all parent fixes automatically. Two slide-local redraws still carried
//      pre-F10 copies of parent internals and were aligned to the parent's
//      certified treatment (all edits in THIS file only; parent untouched):
//      ff_right D4 — old diagonal node->Sigma fans removed (they collided with the
//        reworked Sigma box: 68 red px inside 394..454 x 289..323) and replaced by
//        the D4 wiring measured on THIS frame: per-row leftward arrowhead into the
//        W_v face (head x502, shaft ink x538..557), Sigma feed at (440,323..332),
//        bottom node = circled star;
//      ff_left C5/C6 — fan spokes get end-arrowheads at the circles; "Dot/Product"
//        label on two lines. NOT changed (visually inert: the opaque tan box /
//        W_q box occlude both variants identically to the certified parent):
//        C4 arrow-to-rim length, C7 q-feed tail length. NOT changed (recorded
//        suspects / certified choices): C3 cell treatment (gold-panel zone measured
//        by the attempt-2 worker), C1 X/K label order (low-confidence zoomed read
//        says THIS frame keeps X1/K1 top-down), gold-panel widths, swoosh family.
//
// FRAME->SLIDE MAPPING (scratch/slide017/fit_mapping.py, grid-search against the parent's
// certified 150dpi render; verified on four chrome landmarks: left border 58, bottom
// stroke 517, badge center (875.8,70.5), panel top 46):
//   frame_x = 18.250 + 0.96150 * slide_x ;  frame_y = 1.950 + 0.95500 * slide_y
// All geometry below is TRUE slide coords (960x540, 1px = 1pt, in = pt/72).
//
// LAWS honored: playlist chrome via the imported component (numeral = printed 17);
// verbatim text; margin:0 + fontFace everywhere; no '#' in hex; mouse-cursor artifact
// omitted (ground rule (c)); certified component never edited (delta composed here).

const path = require("path");
const parent = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_043.js");

const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const pptx = pres; // block fns reference pptx.ShapeType (parent-component convention)

const slide = pres.addSlide();

// ---- imported certified base: full composition minus the delta blocks -------------
parent.renderBase(pres, slide, {
  numeral: 17,
  skip: ["title", "ff_left", "ff_right", "hlabel", "swoosh"],
});

const P = parent; // parent module (BLOCKS, C, px re-used for the redrawn blocks)
const px = P.px;
const SANS = "Arial";
const C = {
  ink: "333333", red: "C00000", brick: "A0400E", darkred: "8B1A10",
  blue: "2F55C8", green: "2E8B57", brightgreen: "00AA00",
  gold: "F5CC50", ygreen: "D2E455", boxEdge: "6B6B2A",
  tan: "D8C0A8",
};

function text(slide, str, o) {
  slide.addText(str, Object.assign({ fontFace: SANS, margin: 0 }, o));
}

// W + subscript letter + red "(0)" superscript — THIS lecture's front-card W boxes read
// the same tiny roundish parenthesized glyph on all four boxes (zB1b, an_leftcol; same
// finding certified on sibling slide_015: all four boxes carry (0)).
function wRuns0(letter, subColor, size) {
  return [
    { text: "W", options: { bold: true, fontSize: size, color: C.ink } },
    { text: letter, options: { bold: true, fontSize: size * 0.85, color: subColor, subscript: true } },
    { text: "(0)", options: { bold: true, fontSize: size * 0.8, color: C.red, superscript: true } },
  ];
}
function idxRuns(base, i, color, size) {
  return [
    { text: base, options: { bold: true, fontSize: size, color } },
    { text: String(i), options: { bold: true, fontSize: size * 0.75, color, subscript: true } },
  ];
}

// ---- delta 1: single-line title (parent line-1 geometry, verbatim) ---------------
text(slide, [
  { text: "Multi Head Self Attention of Word ", options: { color: C.ink } },
  { text: "X", options: { color: C.red } },
  { text: "2", options: { color: C.red, subscript: true, fontSize: 14 } },
], {
  x: px(500), y: px(48), w: px(400), h: px(30), align: "center", valign: "middle",
  bold: true, fontSize: 20,
});

// ---- delta 3: ff_left redrawn (gold W_k panel + shifted K strips) ----------------
function drawFfLeft() {
  // dashed input container x 92..128, y 318..442 with 4 pink/lavender cells (parent geom)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(92), y: px(318), w: px(36), h: px(124), rectRadius: 0.05,
    fill: { color: "F3F3F0" }, line: { color: C.green, width: 1.25, dashType: "dash" },
  });
  const cellFills = ["F6DAF3", "EAE4EE", "F6DAF3", "EAE4EE"];
  for (let i = 0; i < 4; i++) {
    const yc = 335 + 28 * i;
    slide.addShape(pptx.ShapeType.rect, {
      x: px(96), y: px(yc - 11), w: px(28), h: px(22),
      fill: { color: cellFills[i] }, line: { color: "C9C9C9", width: 0.5 },
    });
    text(slide, idxRuns("X", i + 1, C.brick, 5), {
      x: px(96), y: px(yc - 11), w: px(28), h: px(22), align: "center", valign: "middle",
    });
    // short strip->W arrow ending at the gold panel edge (measured ink x116..121)
    slide.addShape(pptx.ShapeType.line, {
      x: px(114), y: px(yc), w: px(7), h: 0,
      line: { color: C.darkred, width: 1, endArrowType: "triangle" },
    });
  }
  // continuous gold column panel (measured x122..159, y322..438), boxes drawn on top
  slide.addShape(pptx.ShapeType.rect, {
    x: px(122), y: px(322), w: px(37), h: px(116),
    fill: { color: C.gold }, line: { type: "none" },
  });
  for (let i = 0; i < 4; i++) {
    const yc = 335 + 28 * i;
    // yellow-green W_k^(0) boxes x133..156 (measured ygreen core inside the gold panel)
    slide.addShape(pptx.ShapeType.rect, {
      x: px(133), y: px(yc - 10.5), w: px(23), h: px(21),
      fill: { color: C.ygreen }, line: { color: C.boxEdge, width: 1 },
    });
    text(slide, wRuns0("k", C.ink, 5.5), {
      x: px(133), y: px(yc - 10.5), w: px(23), h: px(21), align: "center", valign: "middle",
    });
    // striped K bar x163..184 (3 cells, measured shift right vs parent 156..184)
    const barFills = ["F9FF96", "FFFFFF", "F08B96"];
    for (let j = 0; j < 3; j++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(163 + j * 7), y: px(yc - 7.5), w: px(7), h: px(15),
        fill: { color: barFills[j] }, line: { color: "B8B8B8", width: 0.5 },
      });
    }
    // red K label above the arrow into the Dot Product box (parent geometry)
    text(slide, idxRuns("K", i + 1, C.brick, 6), {
      x: px(177), y: px(yc - 20), w: px(16), h: px(10), align: "left", valign: "middle",
    });
  }
  // tan Dot Product box x195..253 y301..441 + label + circles + q1 arrow (parent geom)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(195), y: px(301), w: px(58), h: px(140),
    fill: { color: C.tan }, line: { color: "8A6A48", width: 1 },
  });
  // F10-cascade C6: "Dot / Product" on TWO centered lines (parent-certified fix;
  // frames identical in this zone; explicit lineSpacing per the LO/PowerPoint law).
  text(slide, [
    { text: "Dot", options: { breakLine: true } },
    { text: "Product", options: {} },
  ], {
    x: px(195), y: px(303), w: px(58), h: px(14), align: "center", valign: "middle",
    bold: true, fontSize: 6.5, color: "5C2E12", lineSpacing: 7,
  });
  // F10-cascade C4 refresh (judge-flagged child delta, midcols attempt-3 finding 6):
  // red K arrows ENTER the tan panel, heads TERMINATING at the circles' left rims —
  // the parent's certified C4 geometry (186 -> circX-5). Drawn AFTER the tan box so
  // the penetration is visible; the parent's own z-order (C4 before the tan rect)
  // hides its shafts — latent parent defect recorded for the F10 ledger, parent file
  // untouched. Frame evidence: 001:43 frame ink penetrates to x223/229 (rows 1-2);
  // 002:17 frame thin-line ink to x198 + circle-rim clusters (JPEG-compressed).
  const c4circ = [238, 226, 216, 208];
  for (let i = 0; i < 4; i++) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(186), y: px(335 + 28 * i), w: px(c4circ[i] - 5 - 186), h: 0,
      line: { color: C.brick, width: 1, endArrowType: "triangle" },
    });
  }
  const circles = [
    { x: 208, y: 419 }, { x: 216, y: 391 }, { x: 226, y: 363 }, { x: 238, y: 335 },
  ];
  for (const c of circles) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(224), y: px(438), w: px(c.x - 224), h: px(c.y + 4 - 438),
      // F10-cascade C5: small red arrowheads AT the circles (parent-certified fix;
      // frames identical — the pre-F10 copy had bare spokes)
      line: { color: C.darkred, width: 0.9, endArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(c.x - 5), y: px(c.y - 5), w: px(10), h: px(10),
      fill: { color: "BFE0F0" }, line: { color: "5A8AC8", width: 1 },
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(c.x - 2), y: px(c.y - 2), w: px(4), h: px(4),
      fill: { color: "1F2A5C" }, line: { type: "none" },
    });
  }
  slide.addShape(pptx.ShapeType.line, {
    x: px(224), y: px(443), w: 0, h: px(20),
    line: { color: C.red, width: 1.5, beginArrowType: "triangle" },
  });
}
drawFfLeft();

// ---- delta 4: ff_right redrawn (gold W_v panel, shifted V bars, descending V labels)
function drawFfRight() {
  const rows = [335, 363, 391, 419];
  rows.forEach((y, i) => {
    // circled-X node (parent geometry — no frame delta)
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(432), y: px(y - 7.5), w: px(15), h: px(15),
      fill: { color: "FCE8E8" }, line: { color: "CC2222", width: 1.25 },
    });
    // F10-cascade D4: the BOTTOM node is a circled STAR/asterisk (parent-certified
    // treatment; frames identical in this zone — pre-F10 copy drew x4)
    text(slide, i === 3 ? "*" : "\u00D7", {
      x: px(432), y: px(y - 7.5), w: px(15), h: px(15), align: "center", valign: "middle",
      bold: true, fontSize: 9, color: "CC2222",
    });
    // F10-cascade D4 (collision fix, measured): the pre-F10 parent drew diagonal
    // node->Sigma fans here; the reworked Sigma box (394..454 x 289..323) moved ONTO
    // their heads (PIL on render_3: 68 red px inside the Sigma box interior; parent
    // render_4: 0). Parent-certified replacement per DEFECTS.md D4 + THIS frame's
    // measured ink: per-row red LEFTWARD arrowhead INTO the W_v box left face
    // (head x502 = THIS frame's W_v face; tail x558 = X-cells box edge; the gold
    // panel + boxes drawn below cover the shaft, same occlusion as the parent).
    // Frame ink on slide_017.jpg: head zone x494..502 + shaft x538..557, all 4 rows.
    slide.addShape(pptx.ShapeType.line, {
      x: px(502), y: px(y), w: px(56), h: 0,
      line: { color: C.red, width: 0.9, beginArrowType: "triangle" },
    });
    // V label shifted right (measured ink x~466..479); subscripts DESCENDING top->bottom
    text(slide, idxRuns("V", 4 - i, C.brick, 5.5), {
      x: px(464), y: px(y - 9), w: px(15), h: px(10), align: "left", valign: "middle",
    });
    // V bar shifted right + narrower (measured x480..498, 3 cells before the gold panel)
    const barFills = ["F9FF96", "FFFFFF", "F08B96"];
    for (let j = 0; j < 3; j++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(480 + j * 6), y: px(y - 7), w: px(6), h: px(14),
        fill: { color: barFills[j] }, line: { color: "B8B8B8", width: 0.5 },
      });
    }
  });
  // F10-cascade D4: short vertical up-arrow feeding the inherited Sigma box's bottom
  // (head at y323; parent-certified geometry; frame ink x436..444 y321..334 measured)
  slide.addShape(pptx.ShapeType.line, {
    x: px(440), y: px(323), w: 0, h: px(9),
    line: { color: C.red, width: 1, beginArrowType: "triangle" },
  });
  // gold column panel + four yellow-green W_v^(0) boxes (measured x499..537 / x502..534)
  for (let i = 0; i < 4; i++) {
    const yc = 335 + 28 * i;
    slide.addShape(pptx.ShapeType.rect, {
      x: px(499), y: px(yc - 10.5), w: px(38), h: px(21),
      fill: { color: C.gold }, line: { type: "none" },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: px(502), y: px(yc - 10.5), w: px(32), h: px(21),
      fill: { color: C.ygreen }, line: { color: C.boxEdge, width: 1 },
    });
    text(slide, wRuns0("v", C.ink, 5.5), {
      x: px(502), y: px(yc - 10.5), w: px(32), h: px(21), align: "center", valign: "middle",
    });
  }
  // dashed X-cells box x558..602 y320..432 + contents (parent geometry — no frame delta)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(558), y: px(320), w: px(46), h: px(112), rectRadius: 0.05,
    fill: { color: "FFFFFF" }, line: { color: C.green, width: 1, dashType: "dash" },
  });
  const rowFills = [
    ["F9FF96", "FFFFF0", "F6DAF3"],
    ["EAE4EE", "F9FF96", "FFFFF0"],
    ["F6DAF3", "EAE4EE", "F9FF96"],
    ["FFFFF0", "F6DAF3", "EAE4EE"],
  ];
  for (let i = 0; i < 4; i++) {
    const yc = 334 + 27 * i;
    text(slide, idxRuns("X", i + 1, C.brick, 5), {
      x: px(561), y: px(yc - 8), w: px(12), h: px(16), align: "left", valign: "middle",
    });
    for (let j = 0; j < 3; j++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: px(574 + j * 9.5), y: px(yc - 8), w: px(9.5), h: px(16),
        fill: { color: rowFills[i][j] }, line: { color: "C9C9C9", width: 0.5 },
      });
    }
  }
}
drawFfRight();

// ---- delta 6: swoosh arrow redrawn (attempt 2, measured) ---------------------------
// THIS frame's return arrow is BRIGHT red (core #C10002, head (195,0,8)) vs the parent's
// dark-red swoosh image (core #840E07), and runs further: centerline (slide coords,
// swoosh_probe_outputs.txt) tail (550,455) -> hook (565,461) -> (600,445) -> (660,416)
// -> (700,396) -> (745,374) -> (772,358); solid head ink (775..800, 333..356). The
// parent's swoosh image box (585..760, 325..475) covers neither extent. Drawn as thick
// C00000 segments + triangle head; the label (delta 5) draws on top.
(function drawSwoosh017() {
  const sw = C.red;
  const segs = [
    [552, 452, 568, 461],
    [568, 461, 620, 436],
    [620, 436, 700, 396],
    [700, 396, 770, 361],
  ];
  for (const [x1, y1, x2, y2] of segs) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
      line: { color: sw, width: 7 },
    });
  }
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(774), y: px(334), w: px(24), h: px(20), rotate: 63,
    fill: { color: sw }, line: { type: "none" },
  });
})();

// ---- delta 5: swoosh label «"H" Heads» (literal quotes, this lecture's notation) --
// POSITION (this frame's measurement, s8 sheet + PIL blue-ink census): both 001:43 and
// 002:17 frames show the label ink at slide x765..805, y340..377 — ascending along the
// swoosh's UPPER-RIGHT segment (arrowhead at ~(776,411) sits below-right of it). The
// parent's certified hlabel box (x612-708, y392-408) does NOT match either frame's ink;
// this redraw uses the measured position (box centered on ink centroid ~(785,355)).
text(slide, [
  { text: "\u201C", options: { italic: true, bold: true, fontSize: 10, color: "0033CC" } },
  { text: "H", options: { italic: true, bold: true, fontSize: 10, color: "0033CC" } },
  { text: "\u201D Heads", options: { italic: true, bold: true, fontSize: 10, color: "0033CC" } },
], {
  x: px(734), y: px(360), w: px(96), h: px(16), align: "center", valign: "middle",
  rotate: 322, margin: 0, fontFace: SANS,
});

// ---- output ----------------------------------------------------------------------
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_017_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
