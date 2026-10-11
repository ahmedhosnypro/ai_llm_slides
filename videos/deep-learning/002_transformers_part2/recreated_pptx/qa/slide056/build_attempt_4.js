// slide_056.js — "Decoder Final Output" (Deep Learning DSAI 308, Transformers Part II
// — video 002, slide 56; old extraction slide 139).
//
// CONTENT SPEC: analysis/slide_056_final.json (verbatim labels; validated
// PASS_WITH_FIXES). Original frame: unique_slides/slide_056.jpg (960x540).
// Diagram-only slide, bottom-to-top flow: Last Decoder Block bar -> 4 green arrows
// -> 4 green circles -> 64 thin blue lines (4x16 bipartite fan) -> 16 magenta
// circles inside the Linear Projection box -> 16 red arrows -> Softmax bar ->
// 16 blue arrows -> 16 pale output circles -> red curly brace -> blue subtitle.
// Two red "Vocab Size" labels at far left (pale-row and magenta-row alignments).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the
// SHARED module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF
// canvas, gray E9E9E7 panel x 42..918px / y 45px..slide bottom, thin C00000 border,
// badge circle d36px at (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring, bold 333333
// numeral. Badge numeral = 56 (the number printed on THIS original frame; yellow
// badge with "56" verified top-right). The ml-intro house values are SUPERSEDED.
//
// FRAME->SLIDE MAPPING (measured 2026-10-11, scratch/slide056/measure_original2.py +
// debug2/3/4.py): video 002's capture is zoomed OUT with a black letterbox strip
// below the slide bottom. Fitted from the four chrome border landmarks of THIS frame
// (panel left 58, right 901, top 42, bottom-border 516 <-> slide chrome 42, 919, 45,
// 540):
//   slide_x = (frame_x - 17.63) / 0.96123 ;  slide_y = (frame_y + 1.09) / 0.95758
// Cross-check: this frame's badge (yellow-bbox center 875.5, 70.5) maps to slide
// (892.5, 74.8) vs the house badge (893, 71) — within JPEG-bbox noise (~3.8px),
// and scale_x 0.96123 matches the certified slide_002 transform exactly, confirming
// the same playlist template. All content ink below is mapped to TRUE slide
// coordinates through this transform before building.
//
// MEASURED CONTENT INK (slide pt; PIL, JPEG-halo-aware):
//   Title "Decoder Final Output"   ink x 342.7..655.8 (w 313.1) y 64.8..95.1
//      -> Arial Bold advance 10.167em -> em = 30.8..31.1 -> 31pt bold, C00000.
//      Ink cx 499.2 (this deck's content is genuinely ~19pt right of panel center —
//      reproduced as measured; same right-shift as slide_002's "Aug. 2020" line).
//   Subtitle "Probability of each word in Vocab" ink x 380.1..625.6 y 109.7..123.3
//      cx 502.9 -> Arial Bold adv 15.984em -> 15pt bold, 2222CC.
//   Brace: horizontal curly brace, ink x 182.4..819.7 (len 637.3) y 126.5..143.2
//      (thickness 16.7), stroke ~2.5pt, CC0000; measured profile = wide low center
//      bump (~37pt wide, ~7.8pt above the arm), thin arms, short tip curls hooking
//      DOWN-OUTWARD. Rendered as a matplotlib transparent 600dpi PNG
//      (build/assets/slide056_brace.png + sidecar; render_brace.py) embedded at
//      exact size — the leftBrace preset failed the crop comparison (attempt-3
//      dense-region check: read as a squared bracket).
//   Pale output circles: 16, fill-only d ~34pt + ~1pt dark-navy ring, row cy 167.7,
//      centers x 191.5 + 41.05*i (i=0..15) [measured first 191.8/last 806.1 pale,
//      191.3/808.2 magenta — shared grid]. Fill measured mode (229,254,250) ->
//      E5FEFA (spec EAF5FF overridden by PIL measurement); ring measured darkest
//      (0,0,117..133) = dark navy -> 2222AA (spec 7A9CC4 overridden).
//   "Vocab Size" label 1: ink x 62.8..142.9 cy 159.9 -> 15pt bold C00000.
//   Softmax bar: x 152.3..847.3 (w 695.0) y 235.6..276.3 (h 40.7), B00000-family
//      (measured core 159,0,0); white bold "Softmax" ink x 453..541 y 235..251
//      frame -> cx 498.6 cy 254.9, ~22pt.
//   Red arrows (16): heads ~8.4pt tall x ~8.7pt wide, apex touching bar bottom
//      (276.3), bases at 284.7; thin (~0.5pt) shafts down to the green box top.
//      x = the 16-circle grid.
//   Green box: border-stroke centerlines x 152.8 / 846.7, y 315.5 / 450.7
//      (w 693.9 h 135.2), stroke 00A000 ~1.5pt, fill E2FFE3 (measured 224,253,233).
//   Magenta circles: 16, d ~31pt, row cy 351.5, fill EE00EE (measured 236,0,243).
//   Green circles: 4, d ~34pt, row cy 428.9, centers x 397.8/447.2/495.1/544.5
//      (spacing 48.9 — genuinely LEFT of the 16-grid center), fill 22C022
//      (measured 17,206,0).
//   Connector lines: 64 (4x16) thin (~0.5pt) 3366CC lines green-center ->
//      magenta-center, drawn BEHIND the circles (original shows the fan tucked
//      under both rows).
//   "Linear Projection": green bold label inside the box right side, ink
//      x 655.8..816.0 cy 429.3 -> ~18pt bold 00A000.
//   "Vocab Size" label 2: ink x 62.8..144.0 cy 352.0 -> 15pt bold C00000.
//   Blue bar: x 152.3..847.3 (w 695.0) y 483.1..522.7 (h 39.6), 1010B0-family
//      (measured 0,0,167); white bold "Last Decoder Block" ink cx ~500 cy ~503,
//      ~23pt.
//   Green arrows (4): heads apex at the green-circle bottoms (444.2), bases 451.5
//      (straddling the box bottom border), ~0.5pt shafts down to the bar top
//      (483.1); x = green-circle centers; 00AA00.
//   Blue arrows (16): thin (~0.5pt) 2222AA lines from the Softmax bar top (235.6)
//      up to the pale-row bottom (190.5) with small up arrowheads; drawn behind
//      the pale circles (JPEG shows only faint 1px shafts + tiny heads).
//   Text boxes are single-line (no wrap risk): every box width >= ink width +20%,
//   explicit geometry, margin 0; no multi-line blocks, so the line-spacing law is
//   not triggered.
//
// CLOSED-LOOP CORRECTED (attempt 1 -> 2, closed_loop_attempt1.txt): box centers
// shifted by the measured render-vs-target deltas (title cy 80.0->76.2, subtitle
// 116.5->114.7, Linear Projection 429.3->427.1); font sizes re-fit from rendered ink
// width (subtitle/labels 15->15.5, Linear Projection 18->20, Softmax 22->24,
// Last Decoder Block 23->24.5; title 31pt confirmed). Brace, bars, both circle
// grids, and all three arrow bands landed within tolerance on attempt 1.
// Attempt 3 -> 4 (crop-comparison findings, PIL re-measure): pale circles d
// 36->30.2 (original outer ink incl ring = 31.2pt, fill 28.1, gap 8.8 — the
// first fill estimate had swallowed ring anti-aliasing); "Vocab Size" 15.5->16
// (right ink edge was 4.7px short); brace preset -> generated PNG (above).
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c)):
//   * black bottom letterbox strip (frame rows 518..539 full-width) — maps to
//     slide y >= 542 (below the 540pt slide bottom) = player strip, not content.
//   * faint pen/stylus cursor speck right of "Block" (frame ~(610,479), ~2px) —
//     presenter annotation pointer, not slide content.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const PT = 1 / 72; // slide pt -> inches
const FONT = "Arial";

// ---- measured constants (slide pt) -----------------------------------------
const GRID_X0 = 191.5, GRID_DX = 41.05, GRID_N = 16;      // 16-circle x grid
const gridCx = (i) => GRID_X0 + GRID_DX * i;
const GREEN_CX = [397.8, 447.2, 495.1, 544.5];            // 4 green-circle centers

const PALE = { d: 30.2, cy: 167.7, fill: "E5FEFA", ring: "2222AA", ringW: 1 };
const MAG  = { d: 31, cy: 351.5, fill: "EE00EE" };
const GRN  = { d: 34, cy: 428.9, fill: "22C022" };
const SOFTMAX_BAR = { x: 152.3, y: 235.6, w: 695.0, h: 40.7, fill: "B00000", fs: 24 };
const BLUE_BAR    = { x: 152.3, y: 483.1, w: 695.0, h: 39.6, fill: "1010B0", fs: 24.5 };
const GBOX = { x: 152.8, y: 315.5, w: 693.9, h: 135.2, fill: "E2FFE3", line: "00A000", lineW: 1.5 };
const RED_ARROW   = { headW: 8.7, headH: 8.4, headTop: 276.3, shaftTop: 284.7, shaftBot: GBOX.y, color: "CC0000" };
const BLUE_ARROW  = { top: 190.5, bot: SOFTMAX_BAR.y, color: "2222AA" };
const GREEN_ARROW = { headW: 8.0, headH: 7.3, headTop: 444.2, headBot: 451.5, shaftBot: BLUE_BAR.y, color: "00AA00" };
const BRACE = { cx: 501.05, cy: 134.85, len: 637.3, thick: 16.7, color: "CC0000", w: 2.5 };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "56"
drawHouseChrome(pres, s, { numeral: 56 });

// ---- 2. Linear Projection box (fill + green border)
s.addShape(pres.ShapeType.rect, {
  x: GBOX.x * PT, y: GBOX.y * PT, w: GBOX.w * PT, h: GBOX.h * PT,
  fill: { color: GBOX.fill }, line: { color: GBOX.line, width: GBOX.lineW },
});

// ---- 3. 64 connector lines (green centers -> magenta centers), behind circles
for (let gi = 0; gi < GREEN_CX.length; gi++) {
  for (let mi = 0; mi < GRID_N; mi++) {
    const x1 = GREEN_CX[gi], y1 = GRN.cy, x2 = gridCx(mi), y2 = MAG.cy;
    s.addShape(pres.ShapeType.line, {
      x: Math.min(x1, x2) * PT, y: Math.min(y1, y2) * PT,
      w: Math.abs(x2 - x1) * PT, h: Math.abs(y2 - y1) * PT,
      flipH: x2 < x1, flipV: y2 < y1,
      line: { color: "3366CC", width: 0.5 },
    });
  }
}

// ---- 4. magenta circles (16) inside the box top
for (let mi = 0; mi < GRID_N; mi++) {
  s.addShape(pres.ShapeType.ellipse, {
    x: (gridCx(mi) - MAG.d / 2) * PT, y: (MAG.cy - MAG.d / 2) * PT,
    w: MAG.d * PT, h: MAG.d * PT,
    fill: { color: MAG.fill }, line: { color: MAG.fill, width: 0.5 },
  });
}

// ---- 5. green circles (4) inside the box bottom
for (let gi = 0; gi < GREEN_CX.length; gi++) {
  s.addShape(pres.ShapeType.ellipse, {
    x: (GREEN_CX[gi] - GRN.d / 2) * PT, y: (GRN.cy - GRN.d / 2) * PT,
    w: GRN.d * PT, h: GRN.d * PT,
    fill: { color: GRN.fill }, line: { color: GRN.fill, width: 0.5 },
  });
}

// ---- 6. Softmax bar + white bold label
s.addShape(pres.ShapeType.rect, {
  x: SOFTMAX_BAR.x * PT, y: SOFTMAX_BAR.y * PT, w: SOFTMAX_BAR.w * PT, h: SOFTMAX_BAR.h * PT,
  fill: { color: SOFTMAX_BAR.fill },
});
s.addText("Softmax", {
  x: SOFTMAX_BAR.x * PT, y: SOFTMAX_BAR.y * PT, w: SOFTMAX_BAR.w * PT, h: SOFTMAX_BAR.h * PT,
  align: "center", valign: "middle", fontSize: SOFTMAX_BAR.fs, bold: true,
  color: "FFFFFF", fontFace: FONT, margin: 0,
});

// ---- 7. red arrows (16): thin shaft + solid head, apex at the bar bottom
for (let mi = 0; mi < GRID_N; mi++) {
  const cx = gridCx(mi);
  s.addShape(pres.ShapeType.line, {
    x: cx * PT, y: RED_ARROW.shaftTop * PT, w: 0,
    h: (RED_ARROW.shaftBot - RED_ARROW.shaftTop) * PT,
    line: { color: RED_ARROW.color, width: 0.5 },
  });
  s.addShape(pres.ShapeType.triangle, {
    x: (cx - RED_ARROW.headW / 2) * PT, y: RED_ARROW.headTop * PT,
    w: RED_ARROW.headW * PT, h: RED_ARROW.headH * PT,
    fill: { color: RED_ARROW.color }, line: { color: RED_ARROW.color, width: 0.25 },
  });
}

// ---- 8. blue arrows (16): thin line, small up arrowhead at the pale-row end,
//         drawn BEFORE the pale circles so heads tuck behind them
for (let mi = 0; mi < GRID_N; mi++) {
  s.addShape(pres.ShapeType.line, {
    x: gridCx(mi) * PT, y: BLUE_ARROW.top * PT, w: 0,
    h: (BLUE_ARROW.bot - BLUE_ARROW.top) * PT,
    line: { color: BLUE_ARROW.color, width: 0.5, beginArrowType: "triangle" },
  });
}

// ---- 9. green arrows (4): thin shaft + solid head, apex at the circle bottoms
for (let gi = 0; gi < GREEN_CX.length; gi++) {
  const cx = GREEN_CX[gi];
  s.addShape(pres.ShapeType.line, {
    x: cx * PT, y: GREEN_ARROW.headBot * PT, w: 0,
    h: (GREEN_ARROW.shaftBot - GREEN_ARROW.headBot) * PT,
    line: { color: GREEN_ARROW.color, width: 0.5 },
  });
  s.addShape(pres.ShapeType.triangle, {
    x: (cx - GREEN_ARROW.headW / 2) * PT, y: GREEN_ARROW.headTop * PT,
    w: GREEN_ARROW.headW * PT, h: GREEN_ARROW.headH * PT,
    fill: { color: GREEN_ARROW.color }, line: { color: GREEN_ARROW.color, width: 0.25 },
  });
}

// ---- 10. Last Decoder Block bar + white bold label
s.addShape(pres.ShapeType.rect, {
  x: BLUE_BAR.x * PT, y: BLUE_BAR.y * PT, w: BLUE_BAR.w * PT, h: BLUE_BAR.h * PT,
  fill: { color: BLUE_BAR.fill },
});
s.addText("Last Decoder Block", {
  x: BLUE_BAR.x * PT, y: BLUE_BAR.y * PT, w: BLUE_BAR.w * PT, h: BLUE_BAR.h * PT,
  align: "center", valign: "middle", fontSize: BLUE_BAR.fs, bold: true,
  color: "FFFFFF", fontFace: FONT, margin: 0,
});

// ---- 11. pale output circles (16) with thin dark-navy rings
for (let mi = 0; mi < GRID_N; mi++) {
  s.addShape(pres.ShapeType.ellipse, {
    x: (gridCx(mi) - PALE.d / 2) * PT, y: (PALE.cy - PALE.d / 2) * PT,
    w: PALE.d * PT, h: PALE.d * PT,
    fill: { color: PALE.fill }, line: { color: PALE.ring, width: PALE.ringW },
  });
}

// ---- 12. red curly brace: generated transparent PNG (600dpi, matplotlib Path —
//          scripts/mechanism documented in render_brace.py; sidecar
//          build/assets/slide056_brace.json). The preset leftBrace (rotate 90)
//          rendered a narrow spike bump + straight spine + long end strokes and
//          FAILED the dense-region crop comparison ("squared bracket") — the
//          preset cannot reproduce the original's measured curvature (wide low
//          ~37pt bump, thin arms, short down-outward tip curls). Embedded at
//          EXACT size (w = px/600 in), never rescaled.
s.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/slide056_brace.png",
  x: 182.4 * PT, y: 126.5 * PT,
  w: 5310 / 600, h: 139 / 600, // = 637.2 x 16.68 pt, exact measured ink size
});

// ---- 13. title / subtitle / side labels (single-line boxes at MEASURED ink
//          centers; closed-loop render check corrects residual offsets)
function centeredText(txt, cxs, cys, wpt, opts) {
  s.addText(txt, Object.assign({
    x: (cxs - wpt / 2) * PT, y: (cys - 15) * PT, w: wpt * PT, h: 30 * PT,
    align: "center", valign: "middle", margin: 0, fontFace: FONT,
  }, opts));
}
centeredText("Decoder Final Output", 499.2, 76.2, 480,
  { fontSize: 31, bold: true, color: "C00000" });
centeredText("Probability of each word in Vocab", 502.9, 114.7, 320,
  { fontSize: 15.5, bold: true, color: "2222CC" });
centeredText("Linear Projection", 735.9, 427.1, 220,
  { fontSize: 20, bold: true, color: "00A000" });
function leftLabel(cys) {
  s.addText("Vocab Size", {
    x: 61.6 * PT, y: (cys - 15) * PT, w: 150 * PT, h: 30 * PT,
    align: "left", valign: "middle", margin: 0, fontFace: FONT,
    fontSize: 16, bold: true, color: "C00000",
  });
}
leftLabel(159.9);  // aligned with the pale output row (measured cy)
leftLabel(352.0);  // aligned with the magenta row (measured cy)

// ---- output
pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_056_recreated.pptx" })
  .then(() => console.log("WROTE slide_056_recreated.pptx"));
