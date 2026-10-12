// build/slide_049.js — slide 049 "Transformer Stacked Encoder Blocks" (002_transformers_part2)
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slide 049 ← 26 (certified: gen_status=passed,
// visual_check=PASS in this deck's DB). The build IMPORTS the certified parent composition
// components/slide_026.js and calls renderBase(pptx, slide, { numeral: 49, only: [] }):
// the parent contributes the playlist house chrome (shared_patterns/house_chrome.js) with THIS
// slide's badge numeral; slide 49 shares NO content blocks with 26 (pattern-derived dependency,
// "common patterns but not same as them" — see deck AGENTS.md + slide_049_source/SOURCES.md),
// so opts.only = [] draws chrome only and EVERYTHING below is this slide's own measured delta.
//
// GEOMETRY PROVENANCE (PIL-measured 2026-10-12 from unique_slides/slide_049.jpg, 960x540, 1px=1pt,
// through the frame->slide mapping fitted from THIS frame's chrome landmarks — identical to the
// certified 002 build/slide_002.js and components/slide_026.js):
//   frame_x = 18.628 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Cross-checked by vision-gate zoom-crop readings (qa/slide049/crops_sheetA/B/C.txt):
//   - token chips = 5 sub-cells yellow->green->peach->lavender->pink, thin gray outline,
//     dark-red serif-italic labels with subscripts; last X chip reads X_{N-1} (vertical-stroke
//     glyph, matches Y-row symmetry — resolves the spec's X_{N-3}[?]).
//   - NO gray arrows between word row and embedding box (spec hallucination); the real arrows
//     there are navy hatched block arrows, same family as the other blue arrows.
//   - left column: "Encoder Output"/"Encoder Input"/"Input Seq" boxed (cream fill, red border,
//     red bold italic), unboxed 2-line red bold italic "Embedding Words & Pos.", vertical
//     bottom-to-top blue bold italic "Transformer Encoder".
//   - one tall navy container (x164..878, y80..511) wraps the whole token flow; inner pale-blue
//     encoder container (x166..877, y126..365); black-bordered embedding box (x172..871,
//     y417..466) holding the tan + cyan bars; navy rule = the container bottom (y508..511,
//     also present on slide 045 — content, NOT player chrome; the black strip y>=517 IS the
//     player progress bar and is excluded per GROUND RULES (b)/(c)).
// Colors are PIL census cores / vision readings per region (frame wins over spec approximations).

const PARENT = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_026.js");

const { px, x, y, w, h } = PARENT; // frame px -> slide inches (same fitted mapping)

// ---- palette (PIL census cores / vision crop readings) ----
const C = {
  navy: "00008B",        // container borders, stack dots, blue-arrow outlines, tabs (0,0,131)/(0,0,139)
  barBlue: "353BB7",     // encoder block bars (53,59,183)
  stackFill: "C9DFF0",   // encoder container fill (spec; measured D5E3EE)
  red: "C00000",         // title, left-column text/borders, red-arrow outlines
  labelRed: "990000",    // token + word labels (vision ~#990000; PIL cores darker still)
  tanBar: "FDE9D9",      // Word Embedding bar (measured F7E5D1)
  cyanBar: "CCFFFF",     // Positional Encoding bar (measured DAFDF7)
  orange: "E36C0A",      // "Word Embedding" text (spec; measured darkest 8F5E1C is JPEG-darkened)
  greenFill: "BAEDC2",   // green arrow fill (measured (186,237,194))
  greenLine: "2E8B57",   // green arrow outline (vision: forest-green)
  cream: "F9E8D6",       // left-column box fill (measured (249,232,214))
  vertBlue: "333399",    // vertical "Transformer Encoder" (spec)
  gray: "A6A6A6",        // word-row ellipsis dots (measured (166,168,167))
  chipGray: "999999",    // chip thin outline (vision ~#888)
  cellYellow: "FFFFCC", cellGreen: "E4F6DC", cellPeach: "FBE0CC",
  cellLavender: "DEDEF8", cellPink: "F6D8EE", // vision sheetA readings
  white: "FFFFFF",
};
const F = "Arial";
const FS = "Times New Roman"; // serif labels (word + token)

// measured 8-column grid (frame px, from arrow/box/label censuses)
const CX = [205.5, 278.5, 352, 425.5, 499, 571.5, 763.5, 836.5];
const SUBS = ["0", "1", "2", "3", "4", "5", "N-2", "N-1"];

function rect(slide, pptx, fx, fy, fw, fh, opt = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x: x(fx), y: y(fy), w: w(fw), h: h(fh),
    fill: opt.fill ? { color: opt.fill } : { type: "none" },
    line: opt.line === null ? { type: "none" }
      : { color: (opt.line && opt.line.color) || C.navy, width: (opt.line && opt.line.width) || 2,
          dashType: (opt.line && opt.line.dashType) || "solid" },
  });
}

function upArrow(slide, pptx, cx, fyTop, fh, fw, fill, lineColor, lineWidth = 0.75) {
  slide.addShape(pptx.ShapeType.upArrow, {
    x: x(cx - fw / 2), y: y(fyTop), w: w(fw), h: h(fh),
    fill: { color: fill }, line: { color: lineColor, width: lineWidth },
  });
}

function dot(slide, pptx, cx, cy, d, color) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: x(cx - d / 2), y: y(cy - d / 2), w: w(d), h: h(d),
    fill: { color }, line: { type: "none" },
  });
}

// ---- delta blocks -----------------------------------------------------------

function drawWhitePanel(pptx, slide) {
  // white diagram panel on the gray chrome panel: x152..891, y79..516
  slide.addShape(pptx.ShapeType.rect, {
    x: x(152), y: y(79), w: w(891 - 152), h: h(516 - 79),
    fill: { color: C.white }, line: { type: "none" },
  });
}

function drawTitle(pptx, slide) {
  // measured ink x256..782 (center 519), y51..71
  slide.addText("Transformer Stacked Encoder Blocks", {
    x: px((519 - 18.628) / 0.96123 - 420) + 0.021, y: y(48), w: px(840), h: h(26),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 28, bold: true, color: C.red, charSpacing: 1.7, // 28pt cap=20px matches; +1.5pt tracking matches the original's wider advance (526px)
  });
}

function drawTallContainer(pptx, slide) {
  // x164..878, y80..511 — top line doubles as the Y-row top border; bottom = navy rule 508..511
  rect(slide, pptx, 164, 80, 878 - 164, 511 - 80, { line: { color: C.navy, width: 2 } });
  // bottom rule is heavier in the frame (rows 508..511, ~3.5px core)
  slide.addShape(pptx.ShapeType.line, {
    x: x(164), y: y(509.6), w: w(878 - 164), h: 0,
    line: { color: C.navy, width: 3.5 },
  });
}

function drawStack(pptx, slide) {
  // encoder container x166..877, y126..365, pale blue, navy border
  rect(slide, pptx, 166, 127, 877 - 166, 364 - 127, { fill: C.stackFill, line: { color: C.navy, width: 2.5 } });
  // 4 bars x174..870
  const bars = [
    { t: "Encoder Block M", y0: 132, y1: 159 },
    { t: "Encoder Block 2", y0: 238, y1: 266 },
    { t: "Encoder Block 1", y0: 284, y1: 311 },
    { t: "Encoder Block 0", y0: 330, y1: 357 },
  ];
  for (const b of bars) {
    rect(slide, pptx, 174, b.y0, 870 - 174, b.y1 - b.y0, { fill: C.barBlue, line: null });
    slide.addText(b.t, {
      x: x(174), y: y(b.y0), w: w(870 - 174), h: h(b.y1 - b.y0),
      align: "center", valign: "middle", margin: 0,
      fontFace: F, fontSize: 13.5, bold: true, color: C.white,
    });
  }
  // red up-arrows between Block2->1 (y269..283) and Block1->0 (y314..329)
  for (const cx of CX) {
    upArrow(slide, pptx, cx, 269, 14, 10, "F2C9D6", C.red, 0.75);
    upArrow(slide, pptx, cx, 315, 14, 10, "F2C9D6", C.red, 0.75);
  }
  // navy dot columns between Block M and Block 2: 5 dots y172..215 (measured)
  for (const cx of CX) {
    for (const dy of [172, 183, 194, 204.5, 214.5]) dot(slide, pptx, cx, dy, 6, C.navy);
  }
}

function drawGreenArrows(pptx, slide) {
  // container top -> Y row: y107..123
  for (const cx of CX) upArrow(slide, pptx, cx, 107, 16, 15, C.greenFill, C.greenLine, 0.75);
}

function drawTokenRow(pptx, slide, kind) {
  const isY = kind === "Y";
  const cellY0 = isY ? 88 : 383, cellY1 = isY ? 103 : 399;
  const labelY0 = isY ? 84 : 379, labelH = isY ? 21 : 21;
  const dotColor = isY ? C.navy : "00B050";
  const dots = isY
    ? [[628, 93], [644, 93], [664, 93], [680, 93], [696, 93]]
    : [[628, 391], [646, 391], [664.5, 391], [682.5, 391], [698, 391]];
  for (let i = 0; i < 8; i++) {
    const cx = CX[i];
    const x0 = cx - 30, x1 = cx + 30; // chip 60px wide (matches word boxes)
    // 5 equal sub-cells
    const cells = [C.cellYellow, C.cellGreen, C.cellPeach, C.cellLavender, C.cellPink];
    for (let k = 0; k < 5; k++) {
      rect(slide, pptx, x0 + (k * 60) / 5, cellY0, 12, cellY1 - cellY0, { fill: cells[k], line: null });
    }
    // thin gray chip outline + label
    rect(slide, pptx, x0, cellY0, 60, cellY1 - cellY0, { line: { color: C.chipGray, width: 0.75 } });
    slide.addText([
      { text: kind, options: { italic: true } },
      { text: SUBS[i], options: { italic: true, subscript: true } },
    ], {
      x: x(cx - 30.5), y: y(labelY0), w: w(61), h: h(labelH),
      align: "center", valign: "middle", margin: 0,
      fontFace: FS, fontSize: 16, color: C.labelRed, // 16pt regular italic: cap ~10.6px, Y+sub ink ~14px (frame 15px w/ halo)
    });
  }
  // ellipsis dots between chip 5 and chip N-2
  for (const [dx, dy] of dots) dot(slide, pptx, dx, dy, 8.5, dotColor);
  if (!isY) {
    // X-row top navy line (y373..375) + small navy marks above each chip:
    // down-triangle y366..372 + stub y375..381 (measured)
    slide.addShape(pptx.ShapeType.line, {
      x: x(164), y: y(374), w: w(878 - 164), h: 0,
      line: { color: C.navy, width: 2.5 },
    });
    for (const cx of CX) {
      slide.addShape(pptx.ShapeType.triangle, {
        x: x(cx - 7.5), y: y(366), w: w(15), h: h(7),
        fill: { color: C.navy }, line: { type: "none" }, rotate: 180,
      });
      rect(slide, pptx, cx - 4.5, 375, 9, 6, { fill: C.navy, line: null });
    }
  }
}

function drawBlueArrowsUp(pptx, slide) {
  // embedding box -> X row: y401..415
  for (const cx of CX) upArrow(slide, pptx, cx, 401, 15, 13, C.white, C.navy, 0.75);
}

function drawEmbBox(pptx, slide) {
  // black-bordered box x172..871, y417..466 with tan + cyan bars filling it
  rect(slide, pptx, 172, 417, 871 - 172, 466 - 417, { fill: C.white, line: { color: "111111", width: 2.5 } });
  rect(slide, pptx, 174, 419, 869 - 174, 442 - 419, { fill: C.tanBar, line: null });
  rect(slide, pptx, 174, 442, 869 - 174, 464 - 442, { fill: C.cyanBar, line: null });
  slide.addText("Word Embedding", {
    x: x(174), y: y(419), w: w(869 - 174), h: h(442 - 419),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 13, bold: true, color: C.orange,
  });
  slide.addText("Positional  Encoding / Embedding", {
    x: x(174), y: y(442), w: w(869 - 174), h: h(464 - 442),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 12, bold: true, color: C.navy,
  });
}

function drawWordArrows(pptx, slide) {
  // word row -> embedding box: y467..481 (navy hatched block arrows per crop vision; NOT gray)
  for (const cx of CX) upArrow(slide, pptx, cx, 467, 15, 13, C.white, C.navy, 0.75);
}

function drawWordRow(pptx, slide) {
  const labels = ["Word 0", "Word 1", "Word 2", "Word 3", "Word 4", "Word 5", "Word N-2", "Word N-1"];
  for (let i = 0; i < 8; i++) {
    const cx = CX[i];
    rect(slide, pptx, cx - 30, 482, 60, 503 - 482, { fill: C.white, line: { color: C.red, width: 1 } });
    slide.addText(labels[i], {
      x: x(cx - 30), y: y(482), w: w(60), h: h(503 - 482),
      align: "center", valign: "middle", margin: 0,
      fontFace: FS, fontSize: 16, bold: true, italic: true, color: C.labelRed, // 16pt: frame label ink 41-52px, cap 10px
    });
  }
  for (const dx of [630, 648, 666, 684, 700]) dot(slide, pptx, dx, 494, 8, C.gray);
}

function drawLeftColumn(pptx, slide) {
  const box = (fy0, fy1) => {
    rect(slide, pptx, 65, fy0, 145 - 65, fy1 - fy0, { fill: C.cream, line: { color: C.red, width: 1.25 } });
  };
  const twoLine = (l1, l2, fy0, fy1) => {
    slide.addText([
      { text: l1, options: { breakLine: true } },
      { text: l2, options: {} },
    ], {
      x: x(65), y: y(fy0), w: w(145 - 65), h: h(fy1 - fy0),
      align: "center", valign: "middle", margin: 0,
      fontFace: F, fontSize: 14, bold: true, italic: true, color: C.red, lineSpacing: 16,
    });
  };
  box(75, 120); twoLine("Encoder", "Output", 75, 120);           // Encoder Output
  box(377, 422); twoLine("Encoder", "Input", 377, 422);          // Encoder Input
  // vertical blue bold italic, reads bottom-to-top, 2 lines, x85..134 y163..320
  slide.addText([
    { text: "Transformer", options: { breakLine: true } },
    { text: "Encoder", options: {} },
  ], {
    x: x(85), y: y(162), w: w(134 - 85), h: h(165),
    align: "center", valign: "middle", margin: 0, vert: "vert270",
    fontFace: F, fontSize: 28.5, bold: true, italic: true, color: C.vertBlue, lineSpacing: 29.5, // 28.5pt: frame ink length 157px, 2-line span 49px (pitch ~24.5 frame px)
  });
  // unboxed 2-line red bold italic (rows 437..444, 454..459)
  slide.addText([
    { text: "Embedding", options: { breakLine: true } },
    { text: "Words & Pos.", options: {} },
  ], {
    x: x(62), y: y(432), w: w(148 - 62), h: h(462 - 432),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 13.5, bold: true, italic: true, color: C.red, lineSpacing: 17, // 13.5pt: 'Embedding' ink ~78px/9 chars
  });
  // Input Seq box: y482..511 (bottom border 508..511, aligned with the container rule;
  // rows 512+ are gray margin then the player-bar artifact — house_chrome_check left band)
  rect(slide, pptx, 65, 482, 145 - 65, 511 - 482, { fill: C.cream, line: { color: C.red, width: 1.25 } });
  slide.addText("Input Seq", {
    x: x(65), y: y(482), w: w(145 - 65), h: h(511 - 482),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 14, bold: true, italic: true, color: C.red,
  });
}

// ---- composition ------------------------------------------------------------

const DELTA = {
  white_panel: drawWhitePanel,
  title: drawTitle,
  tall_container: drawTallContainer,
  stack: drawStack,
  green_arrows: drawGreenArrows,
  y_row: (pptx, slide) => drawTokenRow(pptx, slide, "Y"),
  x_row: (pptx, slide) => drawTokenRow(pptx, slide, "X"),
  blue_arrows_up: drawBlueArrowsUp,
  emb_box: drawEmbBox,
  word_arrows: drawWordArrows,
  word_row: drawWordRow,
  left_column: drawLeftColumn,
};

function compose(pres) {
  const s = pres.addSlide();
  // certified parent composition: house chrome only (numeral 49 — the number printed on
  // slide_049.jpg); slide 49 shares no content blocks with 26 (pattern-derived dependency)
  PARENT.renderBase(pres, s, { numeral: 49, only: [] });
  for (const fn of Object.values(DELTA)) fn(pres, s);
  return s;
}

module.exports = { DELTA, compose };

// Build when run directly
if (require.main === module) {
  const pptxgen = require("pptxgenjs");
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  compose(pres);
  pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_049_recreated.pptx" })
    .then(() => console.log("WROTE slide_049_recreated.pptx"))
    .catch((e) => { console.error(e); process.exit(1); });
}
