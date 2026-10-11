// slide_020.js — "Pre-processing of Input Sequence" (P2 pattern-group HEAD)
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 20)
//
// CONTENT SPEC: analysis/slide_020_final.json (verbatim; validation.fixes applied).
// Original frame: unique_slides/slide_020.jpg (960x540). Web provenance:
// scratch/webverify + slide_020_source/SOURCES.md (positional-encoding content
// cross-checked against 001's banked Transformer sources; no new figure needed).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the
// SHARED module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF
// canvas, gray E9E9E7 panel x 42..918px / y 45px..slide bottom, thin C00000 border,
// badge circle d36px at (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring, bold 333333
// numeral. Badge numeral = 20 (the number printed on THIS original frame). The
// ml-intro house values are SUPERSEDED for this playlist.
//
// FRAME->SLIDE MAPPING (re-measured 2026-10-11 from THIS frame's four chrome
// border landmarks, scratch/slide020/measure4_output.txt + measure8_output.txt;
// matches certified slide_002/slide_003 fits):
//   stroke centers: left 59.0, right 902.0, top 43.0, bottom 516.0 (frame px)
//   slide_x = (frame_x - 18.628) / 0.961231 ;  slide_y = frame_y / 0.955556
// Cross-check: frame badge yellow-bbox center (875.5, 71.0) -> slide (891.8, 74.3)
// vs house badge (893, 71) — the same 1-4px JPEG-bbox offset class as certified
// 002/003, confirming this frame uses the SAME playlist template.
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c)):
//   * black bottom strip, frame rows 517..539 — video letterbox BELOW the slide
//     bottom (slide y >= 541 under the fitted mapping), not part of the PPT design.
//
// MEASURED STRUCTURE (frame px -> slide pt through the mapping; full derivation in
// scratch/slide020/measure5..10_output.txt):
//   title ink [316,60,693,82]          -> ink [309.4,62.8 .. 701.6,85.8] (center x 505.5;
//                                         the whole content column of this slide sits at
//                                         x ~505-525, NOT at the panel center 480 — measured)
//   row1 word boxes (8): centers fx 211.5+73.4k (gap after k=5; box7 769.5, box8 843.5),
//        box [c-31.5, c+31.5] x [106,127.5], white fill, C00000 border, red italic labels
//   row2 embedding LANE [164,883]x[154.5,192.5], dashed 00A550 border, fill E7FEE9;
//        8 cell strips [pink_left-48, pink_right] x [158,193] (thin C00000 border, no
//        fill), 6 cells y[164,182]: 5x F5E6A3 + F2A7C3 (pink, holds red italic X_k);
//        pink cells measured [204,218],[277,291],[350,364],[423,437],[496,510],[570,583],
//        [758,773],[833,850]; 5 green dots x 630-708 (cy 174)
//   row3 position LANE [164,883]x[217,256], dashed 3333CC border, fill C9C7F6;
//        8 blue-bordered boxes [174,231],[249,309],[322,383],[396,447],[480,530],
//        [544,603],[730,796],[805,871] x [219.5,254.5], blue italic "Pos k" labels;
//        5 blue dots x 630-708 (cy 233.5)
//   6 orange bolts (6x8px) at fx 274.5/348/422/495.5/569/834.5, rows 249-257
//   6 red "+δ" at fx 236/312/387/463/535/800, rows 269-281
//   banner [165,294,882,331] fill 990000, text ~20.5pt bold: "Combine" FFD700 + rest
//        FFFFFF, ink [217..822]x[303,321] (ink center x 519.5)
//   4 thin red shafts (~8px wide): A1 x[611,618] y[264,292]; A2 x[717,723] y[196,294]
//        (from row2 lane through row3's dot gap into the banner); A3 x[516,523]
//        y[331,360]; A4 x[516,523] y[419,446]
//   row4 I/P boxes (8): same centers as row1, [c-31.5,c+31.5] x [358,400], fill FDF1F3,
//        C00000 border, red italic "I/P k" labels; NO dots in the gap (measured)
//   underbrace: curly, x[176,863] y[400,421], cusp DOWN at x~520, arms curl UP
//   caption ink [362,457,676,467] "Input to first Self Attention Layer in Transformer",
//        bold italic 2222CC ~14pt, ink center x 520.6
//   inset green box [66,415,200,513] (white interior): "Positional Encoding" black,
//        white circle + black sine glyph + node circles + connectors, pink
//        "Input Embedding" box + orange bolt, gray "inputs" + black up-arrow
//   green label "Input to / Encoder" 2 lines, ink x[196,262], lines y[469,480]/[484,495]
//
// P2 PATTERN-GROUP CONVENTION (this slide is P2#1 — slides 21/22/34 mirror it):
// the row-lane/banner/palette drawing convention is FACTORED into named helpers
// (drawLane, drawRowBoxes, drawCellStrip, drawDots, drawShaft, drawBolt) with all
// geometry in the G table below in SLIDE PT. Group members: copy the helpers,
// swap G's measured values, keep the palette constants. See qa/slide020/
// p2_row_lane_pattern.js (banked copy) + worker_report.md.
//
// Fonts: diagram box labels/X_i/+δ = Times New Roman (spec typography_notes:
// "slightly serif-italic (Times-Italic-like)"); left labels + banner + caption per
// spec (Arial family, italic/bold as noted). Explicit lineSpacing on every
// multi-line box (PowerPoint-vs-LO divergence law). Subscripts via rich-text
// subscript runs (professional-format law — never caret/underscore text).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

// ---------- palette (measured / spec) ----------
const C = {
  red: "C00000", darkred: "990000", green: "00A550", blue: "3333CC",
  insetGreen: "008000", orange: "FFA500", yellow: "FFD700",
  cellYellow: "F5E6A3", cellPink: "F2A7C3", row4Fill: "FDF1F3",
  lane2Fill: "E7FEE9", lane3Fill: "C9C7F6", gray: "8C8C8C",
  dotGray: "7F7F7F", captionBlue: "2222CC", black: "000000",
  white: "FFFFFF", titleRed: "C00000",
};
const SERIF = "Times New Roman";
const SANS = "Arial";

// ---------- geometry table (SLIDE PT; 1in = 72pt) ----------
const FX = (fx) => (fx - 18.628) / 0.961231; // frame x -> slide x
const FY = (fy) => fy / 0.955556;            // frame y -> slide y

// box centers (frame): 6 at pitch 73.4 from 211.5, ellipsis gap, then 769.5 / 843.5
const CENTERS_F = [211.5, 284.9, 358.3, 431.7, 505.1, 578.5, 769.5, 843.5];
const CENTERS = CENTERS_F.map(FX);

const G = {
  title: { inkCx: (FX(316) + FX(693)) / 2, capTop: FY(60), inkW: FX(693) - FX(316), em: 24.5 },
  row1: { y0: FY(106), y1: FY(127.5), bw: 65.6 },
  lane2: { x: FX(164), y: FY(154.5), w: FX(883) - FX(164), h: FY(192.5) - FY(154.5) },
  lane3: { x: FX(164), y: FY(217), w: FX(883) - FX(164), h: FY(256) - FY(217) },
  // cell strips: frame [pinkLeft-48, pinkRight] x [158,193]; cell band y [164,182]
  stripsF: [[156, 218], [229, 291], [302, 364], [375, 437], [448, 510], [522, 583], [710, 773], [785, 850]],
  stripY0: FY(158), stripY1: FY(193), cellY0: FY(164), cellY1: FY(182),
  // row3 boxes (frame x pairs), y [219.5,254.5]
  posBoxesF: [[174, 231], [249, 309], [322, 383], [396, 447], [480, 530], [544, 603], [730, 796], [805, 871]],
  posBoxY0: FY(219.5), posBoxY1: FY(254.5),
  dots: { cxF: [634, 652, 670.5, 688.5, 703.5], d: 9.4 },
  dotRows: { row1Cy: FY(115), row2Cy: FY(174), row3Cy: FY(233.5) },
  bolts: { cxF: [274.5, 348, 422, 495.5, 569, 834.5], cy: FY(253), w: 6.5, h: 9.5 },
  deltas: { cxF: [236, 312, 387, 463, 535, 800], cy: FY(275), em: 20 },
  banner: { x: FX(165), y: FY(294), w: FX(882) - FX(165), h: FY(331) - FY(294), inkCx: (FX(217) + FX(822)) / 2, capTop: FY(305), em: 20.2 },
  arrows: {
    a1: { cx: FX(614.5), y0: FY(264), y1: FY(292) },
    a2: { cx: FX(720), y0: FY(196), y1: FY(294) },
    a3: { cx: FX(519.5), y0: FY(331), y1: FY(360) },
    a4: { cx: FX(519.5), y0: FY(419), y1: FY(446) },
    w: 8.3,
  },
  row4: { y0: FY(358), y1: FY(400), bw: 65.6 },
  brace: { cx: 509.35, cy: (FY(400) + FY(421)) / 2, w: 771.2, h: FY(421) - FY(400) },
  caption: { inkCx: (FX(362) + FX(676)) / 2, capTop: FY(457), inkW: FX(676) - FX(362), em: 14 },
  inset: { x: FX(66), y: FY(415), w: FX(200) - FX(66), h: FY(513) - FY(415) },
  lab5: { x: FX(196), y: FY(469), w: FX(262) - FX(196), linePitch: FY(484) - FY(469), em: 15.5 },
};

// ---------- P2 shared helpers (the convention group members mirror) ----------

/** Row lane: full-width dashed container behind a diagram row. */
function drawLane(pptx, slide, ln, { border, fill }) {
  slide.addShape(pptx.ShapeType.rect, {
    x: ln.x / 72, y: ln.y / 72, w: ln.w / 72, h: ln.h / 72,
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: border, width: 1, dashType: "dash" },
  });
}

/** A row of labeled boxes at the shared column centers. */
function drawRowBoxes(pptx, slide, { centers, y0, y1, bw, border, fill, labels, font, color, em }) {
  centers.forEach((cx, i) => {
    slide.addShape(pptx.ShapeType.rect, {
      x: (cx - bw / 2) / 72, y: y0 / 72, w: bw / 72, h: (y1 - y0) / 72,
      fill: fill ? { color: fill } : { type: "none" },
      line: { color: border, width: 1 },
    });
    addSubLabel(slide, labels[i], {
      x: (cx - bw / 2) / 72, y: y0 / 72, w: bw / 72, h: (y1 - y0) / 72,
      font, color, em, align: "center",
    });
  });
}

/** Rich text with trailing "N-2"/"N-1"-style subscripts: "Word N-2" etc.
    Renders subscripts spatially aligned (professional format), never "N-2" caret text. */
function addSubLabel(slide, parts, { x, y, w, h, font, color, em, align, valign }) {
  const runs = [];
  let plain = "";
  parts.forEach((p, i) => {
    if (p.sub) {
      if (plain) { runs.push({ text: plain, options: { fontSize: em, color, fontFace: font, italic: true } }); plain = ""; }
      runs.push({ text: p.sub, options: { fontSize: Math.round(em * 0.62), color, fontFace: font, italic: true, subscript: true } });
    } else plain += p.t;
  });
  if (plain) runs.push({ text: plain, options: { fontSize: em, color, fontFace: font, italic: true } });
  slide.addText(runs, {
    x, y, w, h, align: align || "center", valign: valign || "middle", margin: 0,
    lineSpacing: em * 1.0,
  });
}

/** One embedding cell strip: thin red rect + 6 cells (5 yellow + pink last) + X_k. */
function drawCellStrip(pptx, slide, { x0, x1, y0, y1, cy0, cy1, sym }) {
  slide.addShape(pptx.ShapeType.rect, {
    x: x0 / 72, y: y0 / 72, w: (x1 - x0) / 72, h: (y1 - y0) / 72,
    fill: { type: "none" }, line: { color: C.red, width: 0.75 },
  });
  const n = 6, cw = (x1 - x0) / n;
  for (let i = 0; i < n; i++) {
    const isPink = i === n - 1;
    slide.addShape(pptx.ShapeType.rect, {
      x: (x0 + i * cw) / 72, y: cy0 / 72, w: cw / 72, h: (cy1 - cy0) / 72,
      fill: { color: isPink ? C.cellPink : C.cellYellow },
      line: { color: "999999", width: 0.5 },
    });
  }
  // red italic X + subscript in the pink (last) cell
  const px0 = x0 + (n - 1) * cw;
  slide.addText([
    { text: "X", options: { fontSize: 11, color: C.red, fontFace: SERIF, italic: true } },
    { text: sym, options: { fontSize: 7.5, color: C.red, fontFace: SERIF, italic: true, subscript: true } },
  ], { x: px0 / 72, y: cy0 / 72, w: cw / 72, h: (cy1 - cy0) / 72, align: "center", valign: "middle", margin: 0 });
}

/** Ellipsis dots: n dots at fixed pitch, centered on cx band. */
function drawDots(pptx, slide, { centers, cy, d, color }) {
  centers.forEach((cx) => {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: (cx - d / 2) / 72, y: (cy - d / 2) / 72, w: d / 72, h: d / 72,
      fill: { color }, line: { color, width: 0.25 },
    });
  });
}

/** Thin vertical red shaft (the original's arrows are ~8px bars, measured). */
function drawShaft(pptx, slide, { cx, y0, y1, w }) {
  slide.addShape(pptx.ShapeType.rect, {
    x: (cx - w / 2) / 72, y: y0 / 72, w: w / 72, h: (y1 - y0) / 72,
    fill: { color: C.red }, line: { color: C.red, width: 0 },
  });
}

/** Small orange lightning mark (two rotated bars; 6x9pt at this size). */
function drawBolt(pptx, slide, { cx, cy, w, h }) {
  const x = (cx - w / 2) / 72, y = (cy - h / 2) / 72;
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w: w / 72 / 2, h: h / 72, rotate: 18, fill: { color: C.orange }, line: { color: C.orange, width: 0 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: x + w / 72 / 2, y, w: w / 72 / 2, h: h / 72, rotate: -18, fill: { color: C.orange }, line: { color: C.orange, width: 0 },
  });
}

// ---------- build ----------
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// 1. playlist house chrome (white canvas, gray panel + red border, badge "20")
drawHouseChrome(pres, s, { numeral: 20 });

// 2. title (bold red, ink center x 505.5 — measured off-panel-center; box centered on ink)
{
  const em = G.title.em;
  s.addText("Pre-processing of Input Sequence", {
    x: (G.title.inkCx - 430) / 72, y: (G.title.capTop - 0.267 * em) / 72,
    w: 860 / 72, h: (1.5 * em) / 72,
    align: "center", valign: "top", fontSize: em, bold: true,
    color: C.titleRed, fontFace: SANS, margin: 0,
  });
}

// 3. left label column (4 stacked labels + inset-side green label)
//    lab1 gray italic 3 lines, aligned to row1 (frame rows 93-136)
s.addText([
  { text: "Sequence of", options: { breakLine: true } },
  { text: "words with", options: { breakLine: true } },
  { text: "Length N", options: {} },
], {
  x: (FX(69) - 1) / 72, y: FY(92) / 72, w: (FX(165) - FX(69)) / 72, h: (FY(137) - FY(92)) / 72,
  align: "left", valign: "top", fontSize: 14.5, italic: true, color: C.gray,
  fontFace: SANS, margin: 0, lineSpacing: 15.7,
});
//    lab2 green bold 2 lines + regular "e.g. word2vec" (frame rows 156-193)
s.addText([
  { text: "Word", options: { breakLine: true, bold: true } },
  { text: "Embedding", options: { breakLine: true, bold: true } },
  { text: "e.g. word2vec", options: { fontSize: 11.5 } },
], {
  x: (FX(67) - 1) / 72, y: FY(154) / 72, w: (FX(160) - FX(67)) / 72, h: (FY(199) - FY(154)) / 72,
  align: "left", valign: "top", fontSize: 16, color: C.green,
  fontFace: SANS, margin: 0, lineSpacing: 16.7,
});
//    lab3 blue bold 2 lines (frame rows 225-247)
s.addText([
  { text: "Position", options: { breakLine: true } },
  { text: "Information", options: {} },
], {
  x: (FX(69) - 1) / 72, y: FY(223) / 72, w: (FX(150) - FX(69)) / 72, h: (FY(249) - FY(223)) / 72,
  align: "left", valign: "top", fontSize: 14, bold: true, color: C.blue,
  fontFace: SANS, margin: 0, lineSpacing: 14.6,
});
//    lab4 red bold italic 2 lines (frame rows 301-326 — aligned to the BANNER, measured)
s.addText([
  { text: "Final", options: { breakLine: true } },
  { text: "Embedding", options: {} },
], {
  x: (FX(68) - 1) / 72, y: FY(299) / 72, w: (FX(150) - FX(68)) / 72, h: (FY(328) - FY(299)) / 72,
  align: "left", valign: "top", fontSize: 14, bold: true, italic: true, color: C.red,
  fontFace: SANS, margin: 0, lineSpacing: 15.7,
});

// 4. ROW 1 — word boxes (no lane: measured boxes-only band)
drawRowBoxes(pres, s, {
  centers: CENTERS, y0: G.row1.y0, y1: G.row1.y1, bw: G.row1.bw,
  border: C.red, fill: C.white, labels: [
    [{ t: "Word 0" }], [{ t: "Word 1" }], [{ t: "Word 2" }], [{ t: "Word 3" }],
    [{ t: "Word 4" }], [{ t: "Word 5" }], [{ t: "Word " }, { sub: "N-2" }], [{ t: "Word " }, { sub: "N-1" }],
  ], font: SERIF, color: C.red, em: 13.5,
});
//    gray ellipsis dots in the gap
drawDots(pres, s, { centers: G.dots.cxF.map(FX), cy: G.dotRows.row1Cy, d: G.dots.d, color: C.dotGray });

// 5. ROW 2 — embedding lane + 8 cell strips + X_k + green dots
drawLane(pres, s, G.lane2, { border: C.green, fill: C.lane2Fill });
G.stripsF.forEach((pair, i) => {
  const syms = ["0", "1", "2", "3", "4", "5", "N-2", "N-1"];
  drawCellStrip(pres, s, {
    x0: FX(pair[0]), x1: FX(pair[1]), y0: G.stripY0, y1: G.stripY1,
    cy0: G.cellY0, cy1: G.cellY1, sym: syms[i],
  });
});
drawDots(pres, s, { centers: G.dots.cxF.map(FX), cy: G.dotRows.row2Cy, d: G.dots.d, color: C.green });

// 6. ROW 3 — position lane + blue boxes + labels + blue dots
drawLane(pres, s, G.lane3, { border: C.blue, fill: C.lane3Fill });
G.posBoxesF.forEach((pair, i) => {
  const labels = [
    [{ t: "Pos 0" }], [{ t: "Pos 1" }], [{ t: "Pos 2" }], [{ t: "Pos 3" }],
    [{ t: "Pos 4" }], [{ t: "Pos 5" }], [{ t: "Pos " }, { sub: "N-2" }], [{ t: "Pos " }, { sub: "N-1" }],
  ];
  const x0 = FX(pair[0]), x1 = FX(pair[1]);
  s.addShape(pres.ShapeType.rect, {
    x: x0 / 72, y: G.posBoxY0 / 72, w: (x1 - x0) / 72, h: (G.posBoxY1 - G.posBoxY0) / 72,
    fill: { type: "none" }, line: { color: C.blue, width: 1 },
  });
  addSubLabel(s, labels[i], {
    x: x0 / 72, y: G.posBoxY0 / 72, w: (x1 - x0) / 72, h: (G.posBoxY1 - G.posBoxY0) / 72,
    font: SERIF, color: C.blue, em: 13.5, align: "center",
  });
});
drawDots(pres, s, { centers: G.dots.cxF.map(FX), cy: G.dotRows.row3Cy, d: G.dots.d, color: C.blue });

// 7. bolts (6 small orange marks) + red "+δ" row (measured alternating chain)
G.bolts.cxF.forEach((fx) => drawBolt(pres, s, { cx: FX(fx), cy: G.bolts.cy, w: G.bolts.w, h: G.bolts.h }));
G.deltas.cxF.forEach((fx) => {
  s.addText([
    { text: "+", options: {} },
    { text: "δ", options: {} },
  ], {
    x: (FX(fx) - 20) / 72, y: (G.deltas.cy - 12) / 72, w: 40 / 72, h: 24 / 72,
    align: "center", valign: "middle", fontSize: G.deltas.em, bold: true,
    color: C.red, fontFace: SERIF, italic: true, margin: 0,
  });
});

// 8. BANNER — dark red, "Combine" yellow + white sentence
s.addShape(pres.ShapeType.rect, {
  x: G.banner.x / 72, y: G.banner.y / 72, w: G.banner.w / 72, h: G.banner.h / 72,
  fill: { color: C.darkred }, line: { color: C.darkred, width: 0 },
});
s.addText([
  { text: "Combine ", options: { color: C.yellow } },
  { text: "Word Encoding and Position Information (for Each Word)", options: { color: C.white } },
], {
  x: (G.banner.inkCx - 380) / 72, y: (G.banner.capTop - 0.267 * G.banner.em) / 72,
  w: 760 / 72, h: (1.5 * G.banner.em) / 72,
  align: "center", valign: "top", fontSize: G.banner.em, bold: true, fontFace: SANS, margin: 0,
});

// 9. the four thin red shafts (measured: no block-arrow heads in the frame)
[G.arrows.a1, G.arrows.a2, G.arrows.a3, G.arrows.a4].forEach((a) =>
  drawShaft(pres, s, { cx: a.cx, y0: a.y0, y1: a.y1, w: G.arrows.w }));

// 10. ROW 4 — measured dashed red lane (white fill) + I/P boxes
drawLane(pres, s, { x: FX(162), y: FY(358), w: FX(883) - FX(162), h: FY(398) - FY(358) },
  { border: C.red, fill: C.white });
drawRowBoxes(pres, s, {
  centers: CENTERS, y0: FY(361), y1: FY(394.5), bw: G.row4.bw,
  border: C.red, fill: null, labels: [
    [{ t: "I/P 0" }], [{ t: "I/P 1" }], [{ t: "I/P 2" }], [{ t: "I/P 3" }],
    [{ t: "I/P 4" }], [{ t: "I/P 5" }], [{ t: "I/P " }, { sub: "N-2" }], [{ t: "I/P " }, { sub: "N-1" }],
  ], font: SERIF, color: C.red, em: 13.5,
});

// 11. underbrace (curly, cusp DOWN; vertical "{" authored then rotated 270°)
s.addShape(pres.ShapeType.leftBrace, {
  x: (G.brace.cx - G.brace.h / 2) / 72, y: (G.brace.cy - G.brace.w / 2) / 72,
  w: G.brace.h / 72, h: G.brace.w / 72, rotate: 270,
  fill: { type: "none" }, line: { color: C.red, width: 1.5 },
});

// 12. caption
s.addText("Input to first Self Attention Layer in Transformer", {
  x: (G.caption.inkCx - 300) / 72, y: (G.caption.capTop - 0.267 * G.caption.em) / 72,
  w: 600 / 72, h: (1.5 * G.caption.em) / 72,
  align: "center", valign: "top", fontSize: G.caption.em, bold: true, italic: true,
  color: C.captionBlue, fontFace: SANS, margin: 0,
});

// 13. inset schematic (bottom-left, green border, white interior)
s.addShape(pres.ShapeType.rect, {
  x: G.inset.x / 72, y: G.inset.y / 72, w: G.inset.w / 72, h: G.inset.h / 72,
  fill: { color: C.white }, line: { color: C.insetGreen, width: 1 },
});
s.addText("Positional Encoding", {
  x: (G.inset.x + 4) / 72, y: (G.inset.y + 13) / 72, w: (G.inset.w - 8) / 72, h: 16 / 72,
  align: "left", valign: "top", fontSize: 11.5, color: C.black, fontFace: SANS, margin: 0,
});
//    white circle with sine glyph + node + connectors
const icx = G.inset.x + 30, icy = G.inset.y + 49; // circle center (slide pt)
s.addShape(pres.ShapeType.ellipse, {
  x: (icx - 14) / 72, y: (icy - 14) / 72, w: 28 / 72, h: 28 / 72,
  fill: { color: C.white }, line: { color: C.black, width: 1 },
});
s.addText("~", {
  x: (icx - 12) / 72, y: (icy - 12) / 72, w: 24 / 72, h: 24 / 72,
  align: "center", valign: "middle", fontSize: 24, bold: true, color: C.black, fontFace: SERIF, margin: 0,
});
const ncx = G.inset.x + 78, ncy = G.inset.y + 42; // small node circle
s.addShape(pres.ShapeType.ellipse, {
  x: (ncx - 6) / 72, y: (ncy - 6) / 72, w: 12 / 72, h: 12 / 72,
  fill: { color: C.white }, line: { color: C.black, width: 1 },
});
s.addShape(pres.ShapeType.line, {
  x: (icx + 14) / 72, y: icy / 72, w: (ncx - 6 - icx - 14) / 72, h: (ncy - icy) / 72,
  line: { color: C.black, width: 1 },
});
//    pink Input Embedding box + orange bolt
const pbx = G.inset.x + 14, pby = G.inset.y + 68, pbw = 92, pbh = 26;
s.addShape(pres.ShapeType.rect, {
  x: pbx / 72, y: pby / 72, w: pbw / 72, h: pbh / 72,
  fill: { color: "F4B8D0" }, line: { color: "C88AA6", width: 0.75 },
});
s.addText("Input Embedding", {
  x: pbx / 72, y: pby / 72, w: pbw / 72, h: pbh / 72,
  align: "center", valign: "middle", fontSize: 9, color: C.black, fontFace: SANS, margin: 0,
});
drawBolt(pres, s, { cx: pbx + pbw + 8, cy: pby + pbh / 2, w: 6, h: 10 });
//    connector from node down to the pink box
s.addShape(pres.ShapeType.line, {
  x: ncx / 72, y: (ncy + 6) / 72, w: 0, h: (pby - ncy - 6) / 72,
  line: { color: C.black, width: 1 },
});
//    "inputs" gray text + black up-arrow into the pink box
s.addText("inputs", {
  x: pbx / 72, y: (pby + pbh + 2) / 72, w: 50 / 72, h: 12 / 72,
  align: "left", valign: "top", fontSize: 9.5, color: C.gray, fontFace: SANS, margin: 0,
});
s.addShape(pres.ShapeType.line, {
  x: (pbx + 30) / 72, y: (pby + pbh + 1) / 72, w: 0, h: -(pbh - 2) / 72,
  line: { color: C.black, width: 1.25, endArrowType: "triangle" },
});

// 14. green "Input to / Encoder" label (2 lines, right of the inset)
s.addText([
  { text: "Input to", options: { breakLine: true } },
  { text: "Encoder", options: {} },
], {
  x: G.lab5.x / 72, y: (G.lab5.y - 2) / 72, w: (G.lab5.w + 12) / 72, h: ((G.lab5.linePitch * 2) + 6) / 72,
  align: "left", valign: "top", fontSize: G.lab5.em, bold: true, color: C.insetGreen,
  fontFace: SANS, margin: 0, lineSpacing: G.lab5.linePitch,
});

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_020_recreated.pptx" })
  .then(() => console.log("WROTE slide_020_recreated.pptx"));
