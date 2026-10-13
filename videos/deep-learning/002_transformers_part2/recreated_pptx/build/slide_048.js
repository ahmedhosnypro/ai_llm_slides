// build/slide_048.js — slide 048 "Encoder Block" (002_transformers_part2).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slide 48 is a CHILD of slide 047
// (48<-47; 047 certified PASS in this video's DB). This build require()s the certified
// parent component and draws ONLY the measured delta — never re-derives the composition.
//
// DELTA MEASUREMENT CAMPAIGN (scratch/slide048/, 2026-10-12): pixel-diff of frame 048 vs
// certified-parent frame 047 proves the shared composition is pixel-identical outside
// three delta zones (labels/X-row/FFN header/container/MHA-bar text all 0 strong-diff):
//   1. RIGHT INSET PANEL (048 only): white panel + thick green border, frame x607..889,
//      y73..491. Content bottom->top: three red circles V/K/Q (cy~440, d~21.5, fills
//      #B51B2E) -> tan "Multi-Head Attention" box (x691..859, y341..406, fill F4DFBA,
//      2-line black text) -> light-green "Add & Norm" (x652..859, y291..337, fill B5FF63,
//      dark-green text) -> yellow-green "Feed Forward" (x679..865, y169..247, fill
//      DFFC7C, gray 2-line text) -> light-green "Add & Norm" (x652..859, y118..167) ->
//      black exit stub above (x773, y98..119). A thick BLACK ROUNDED RESIDUAL LOOP
//      (x627..876, y110..474, ~3px stroke, corner r~14) encloses the stack (closed rect —
//      measured all four edges) plus two inner left-side black segments (x644..647,
//      y151..264 and y322..450) and a near-full-width black band under the MHA box
//      (y406..408). Short black connectors: x713/x773/x833 y411..430 (circles->MHA),
//      x773 y247..292 (A&N-bot->FF), K stem x773 y449..489.
//   2. THUMBNAIL INSET (bottom-left, 048 only): green-bordered white box x70..152,
//      y426..482 — a MINIATURE POSITIONAL-ENCODING/INPUT-EMBEDDING diagram (vision-read
//      at x6, transcript v3b_thumb_read.txt): gray "Positional/Encoding" two-line label
//      (top-left), white circle with black sine wave + small gray operator circle
//      (upper-right), pink rounded "Input Embedding" box (x108..145, y446..460, bold
//      black 2-line label), short up-arrow, tiny gray "Inputs" (bottom). NOTE: the
//      validated spec's "Transformer Encoder / gray Encoder box" reading is refuted by
//      the zoomed vision read + pixel map (no ink for an 'Encoder' title; pink box and
//      sine circle measured instead) — fidelity law: the frame wins.
//   3. LAYER-NORMALIZATION BAR TEXTS (both bars): 048 shows the LONGER occluded string
//      "Layer Normalization (NOT Batch N|" (vision-read v2b_reads48.txt; new ink starts
//      x~327 vs 047's x~405). Parent's shorter "Layer Normalization" is patched over and
//      redrawn longer; the right tail is occluded by the inset exactly as in the frame
//      (recreation_brief steps 11/17). The bar fills/borders themselves are identical.
//
// BADGE NUMERAL (audit-flagged, RESOLVED): the original frame's badge prints "48".
// Three raw transcriptions claimed "49" and the spec kept "49", but the digits' lower
// halves are occluded by the inset panel's top-right corner (frame badge center ~(875,70)
// is a curation artifact). Pixel-map forensics + two zoomed vision reads
// (v1_badge_read.txt, v1b_badge_read.txt): second digit shows a CLOSED double loop with
// waist pinch at y72 = "8" (excludes 7 — frame 047's diagonal; differs from frame 049's
// known open 9-loop); sequential context 047->"47", 049->"49" agrees. Numeral = 48
// (printed-number law; file id confirmed). No anomaly to escalate.
//
// Z-ORDER: parent renderBase draws everything incl. badge (house chrome, numeral 48);
// the delta is drawn ON TOP so the inset occludes the shared diagram's right side AND
// the badge's bottom-left corner exactly as the frame shows.
//
// opts: none. No dependents — no component bank owed (playlist-scoped banking checked:
// slide_dependencies.json has no edges pointing at 48).

const COMP = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_047.js");

const pt = (v) => v / 72;
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_048_recreated.pptx";
const FONT = "Arial";

// ---- measured palette (frame 048 medians) ----
const INSET_FILL = "F2F2F4";   // inset panel fill (241,242,244)
const INSET_GREEN = "3A8220";  // inset border (43,132,33)/(61,130,20)
const LOOP_BLACK = "0A0A0A";
const AN_FILL = "B5FF63";      // Add & Norm fill (181,255,99)
const AN_LINE = "3C7814";      // its THICK border (dark green, ~5px measured)
const AN_TEXT = "2E6614";      // dark green text (glyph px, frame-measured)
const FF_FILL = "DFFC7C";      // Feed Forward fill (223,252,124)
const FF_LINE = "828F0E";      // its border (130,143,14)
const FF_TEXT = "6E8414";      // FF label ink: dark olive-green (155,180,52 darkest — NOT gray; frame wins over spec)
const MHA_FILL = "F4DFBA";     // inset MHA box fill (244,223,186)
const MHA_LINE = "6E5B40";     // (110,91,64)
const CIRC_FILL = "B51B2E";    // V/K/Q circles (181,27,46)
const CIRC_LINE = "8E1424";
const THUMB_GREEN = "1E7A3C";  // thumbnail border (22,121,59)
const THUMB_PINK = "F6E2E3";   // Input Embedding fill (246,226,227)
const THUMB_GRAY = "8C8C8C";   // tiny gray labels
const LN_PATCH = COMP.COLS ? "EDB671" : "EDB671"; // parent LN_FILL — keep in sync with component

// ---- measured geometry (frame px = slide pt) ----
const INSET = {
  panel: { x: 607, y: 73, w: 282, h: 418 },
  loop: { x: 627, y: 110, w: 249, h: 364, r: 0.19 },
  innerLine: { x: 645.5, segs: [[151, 264], [322, 450]] },
  anTop: { x: 687, y: 119, w: 171, h: 45 },
  ffn: { x: 679, y: 169, w: 186, h: 78 },
  anBot: { x: 687, y: 295, w: 171, h: 41 },
  mha: { x: 691, y: 341, w: 168, h: 65 },
  band: { x0: 645, x1: 867, y: 407 },
  circles: { cy: 440.5, d: 21.5, vs: [{ cx: 666.5, t: "V" }, { cx: 775, t: "K" }, { cx: 842, t: "Q" }] },
  conns: [
    { x: 713, y0: 411, y1: 430, arrow: true },
    { x: 773, y0: 410, y1: 430, arrow: true },
    { x: 833, y0: 411, y1: 429, arrow: true },
    { x: 773, y0: 247, y1: 292, arrow: true },
    { x: 773, y0: 98, y1: 119, arrow: true },
    { x: 773, y0: 449, y1: 489, arrow: false },   // K stem to panel bottom
  ],
};

const THUMB = {
  box: { x: 70.5, y: 426, w: 82, h: 56.5 },
  posLabel: { x: 74, y: 430.5, w: 44, h: 14, lines: ["Positional", "Encoding"] },
  sineCircle: { x: 114.5, y: 431.5, d: 14.5 },
  opCircle: { x: 129.5, y: 433.5, d: 8 },
  pinkBox: { x: 108, y: 446, w: 37.5, h: 14.5, lines: ["Input", "Embedding"] },
  arrow: { x: 127, y0: 461, y1: 469 },
  inputs: { x: 111, y: 472.5, w: 32, h: 8 },
};

// 048's longer Layer-Normalization label (visible part ends "…Batch N" at the inset
// edge; tail occluded). Left ink edge measured at x~327 on both bars.
const LN_TEXT_48 = { left: 322, width: 560 };

function drawInset48(pptx, slide) {
  // white panel with thick green border (occludes main diagram's right side + badge BL)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(INSET.panel.x), y: pt(INSET.panel.y), w: pt(INSET.panel.w), h: pt(INSET.panel.h),
    fill: { color: INSET_FILL }, line: { color: INSET_GREEN, width: 2.5 }, rectRadius: 0.06,
  });
  // thick black rounded residual loop (closed; measured all four edges)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(INSET.loop.x), y: pt(INSET.loop.y), w: pt(INSET.loop.w), h: pt(INSET.loop.h),
    fill: { color: INSET_FILL }, line: { color: LOOP_BLACK, width: 2.5 },
    rectRadius: INSET.loop.r,
  });
  // inner left-side black segments (measured x644..647)
  for (const [y0, y1] of INSET.innerLine.segs) {
    slide.addShape(pptx.ShapeType.rect, {
      x: pt(INSET.innerLine.x - 1.5), y: pt(y0), w: pt(3), h: pt(y1 - y0),
      fill: { color: LOOP_BLACK }, line: { type: "none" },
    });
  }
  // connectors (black; arrowheads point UP = flow direction)
  for (const c of INSET.conns) {
    slide.addShape(pptx.ShapeType.line, {
      x: pt(c.x), y: pt(c.y0), w: 0, h: pt(c.y1 - c.y0),
      line: c.arrow
        ? { color: LOOP_BLACK, width: 2, beginArrowType: "triangle" }
        : { color: LOOP_BLACK, width: 2 },
    });
  }
  // near-full-width black band under the MHA box (measured y406..408, x~645..867)
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(INSET.band.x0), y: pt(INSET.band.y - 1.5), w: pt(INSET.band.x1 - INSET.band.x0), h: pt(3),
    fill: { color: LOOP_BLACK }, line: { type: "none" },
  });
  // boxes, top of stack first (later draws sit on top where they overlap)
  const box = (b, fill, line, w) => slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(b.x), y: pt(b.y), w: pt(b.w), h: pt(b.h),
    fill: { color: fill }, line: { color: line, width: w }, rectRadius: 0.08,
  });
  const anText = (b, dy) => slide.addText("Add & Norm", {
    x: pt(b.x), y: pt(b.y + dy), w: pt(b.w), h: pt(b.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 22, bold: true, color: AN_TEXT,
  });
  box(INSET.anTop, AN_FILL, AN_LINE, 4.5);
  anText(INSET.anTop, 5);
  // Feed Forward (two lines, dark olive on yellow-green; pitch 27 measured)
  box(INSET.ffn, FF_FILL, FF_LINE, 1.5);
  slide.addText([
    { text: "Feed", options: { breakLine: true } },
    { text: "Forward" },
  ], {
    x: pt(INSET.ffn.x), y: pt(INSET.ffn.y - 10), w: pt(INSET.ffn.w), h: pt(INSET.ffn.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 21, bold: true, color: FF_TEXT, lineSpacing: 28,
  });
  // Multi-Head Attention (two lines, black on tan; pitch 31, ~22pt measured)
  box(INSET.mha, MHA_FILL, MHA_LINE, 2);
  slide.addText([
    { text: "Multi-Head", options: { breakLine: true } },
    { text: "Attention" },
  ], {
    x: pt(INSET.mha.x), y: pt(INSET.mha.y - 5), w: pt(INSET.mha.w), h: pt(INSET.mha.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 22, bold: true, color: "000000", lineSpacing: 31,
  });
  box(INSET.anBot, AN_FILL, AN_LINE, 4.5);
  anText(INSET.anBot, 0);
  // V/K/Q red circles
  for (const c of INSET.circles.vs) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: pt(c.cx - INSET.circles.d / 2), y: pt(INSET.circles.cy - INSET.circles.d / 2),
      w: pt(INSET.circles.d), h: pt(INSET.circles.d),
      fill: { color: CIRC_FILL }, line: { color: CIRC_LINE, width: 0.75 },
    });
    slide.addText(c.t, {
      x: pt(c.cx - INSET.circles.d / 2), y: pt(INSET.circles.cy - INSET.circles.d / 2),
      w: pt(INSET.circles.d), h: pt(INSET.circles.d),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 12, bold: true, color: "FFFFFF",
    });
  }
}

function drawThumbnail48(pptx, slide) {
  const t = THUMB;
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(t.box.x), y: pt(t.box.y), w: pt(t.box.w), h: pt(t.box.h),
    fill: { color: "FFFFFF" }, line: { color: THUMB_GREEN, width: 2 }, rectRadius: 0.05,
  });
  slide.addText([
    { text: t.posLabel.lines[0], options: { breakLine: true } },
    { text: t.posLabel.lines[1] },
  ], {
    x: pt(t.posLabel.x), y: pt(t.posLabel.y), w: pt(t.posLabel.w), h: pt(t.posLabel.h),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 5, color: THUMB_GRAY, lineSpacing: 6,
  });
  // white circle with black sine wave (two half-arrows approximating the S-curve)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: pt(t.sineCircle.x), y: pt(t.sineCircle.y), w: pt(t.sineCircle.d), h: pt(t.sineCircle.d),
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
  });
  slide.addShape(pptx.ShapeType.arc, {
    x: pt(t.sineCircle.x + 1.5), y: pt(t.sineCircle.y + 2.5), w: pt(6), h: pt(6),
    angleRange: [180, 360], line: { color: "000000", width: 1 },
  });
  slide.addShape(pptx.ShapeType.arc, {
    x: pt(t.sineCircle.x + 6.5), y: pt(t.sineCircle.y + 6), w: pt(6), h: pt(6),
    angleRange: [0, 180], line: { color: "000000", width: 1 },
  });
  // small gray operator circle with plus
  slide.addShape(pptx.ShapeType.ellipse, {
    x: pt(t.opCircle.x), y: pt(t.opCircle.y), w: pt(t.opCircle.d), h: pt(t.opCircle.d),
    fill: { color: "D9D9D9" }, line: { color: "000000", width: 0.75 },
  });
  slide.addText("+", {
    x: pt(t.opCircle.x), y: pt(t.opCircle.y), w: pt(t.opCircle.d), h: pt(t.opCircle.d),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 5, bold: true, color: "000000",
  });
  // pink Input Embedding box (bold black 2-line label)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(t.pinkBox.x), y: pt(t.pinkBox.y), w: pt(t.pinkBox.w), h: pt(t.pinkBox.h),
    fill: { color: THUMB_PINK }, line: { color: "3A3A3A", width: 1 }, rectRadius: 0.06,
  });
  slide.addText([
    { text: t.pinkBox.lines[0], options: { breakLine: true } },
    { text: t.pinkBox.lines[1] },
  ], {
    x: pt(t.pinkBox.x), y: pt(t.pinkBox.y), w: pt(t.pinkBox.w), h: pt(t.pinkBox.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 4.5, bold: true, color: "000000", lineSpacing: 5,
  });
  // short up-arrow below the box
  slide.addShape(pptx.ShapeType.line, {
    x: pt(t.arrow.x), y: pt(t.arrow.y0), w: 0, h: pt(t.arrow.y1 - t.arrow.y0),
    line: { color: "000000", width: 1.25, beginArrowType: "triangle" },
  });
  slide.addText("Inputs", {
    x: pt(t.inputs.x), y: pt(t.inputs.y), w: pt(t.inputs.w), h: pt(t.inputs.h),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 5.5, color: THUMB_GRAY,
  });
}

function redrawLNTexts48(pptx, slide) {
  // Patch the parent's shorter "Layer Normalization" ink, then draw 048's longer
  // occluded label. Patch rect stays strictly inside the bar (no border contact).
  const bars = [COMP.U1, COMP.U2];
  for (const u of bars) {
    const b = u.ln;
    slide.addShape(pptx.ShapeType.rect, {
      x: pt(345), y: pt(b.y + 2), w: pt(290), h: pt(b.h - 4),
      fill: { color: LN_PATCH }, line: { type: "none" },
    });
    slide.addText([
      { text: "Layer", options: { color: "DC7D45" } },
      { text: " Normalization (NOT Batch Norm)", options: { color: "81460E" } },
    ], {
      x: pt(LN_TEXT_48.left), y: pt(b.y), w: pt(LN_TEXT_48.width), h: pt(b.h),
      align: "left", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 19, bold: true, italic: true, lineSpacing: 22,
    });
  }
}

const pptxgen = require("pptxgenjs");
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// 1) certified parent composition (house chrome incl. badge numeral 48)
COMP.renderBase(pptx, slide, { numeral: 48 });

// 2) measured delta: longer LN bar labels (under the inset), then inset + thumbnail on top
redrawLNTexts48(pptx, slide);
drawInset48(pptx, slide);
drawThumbnail48(pptx, slide);

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
