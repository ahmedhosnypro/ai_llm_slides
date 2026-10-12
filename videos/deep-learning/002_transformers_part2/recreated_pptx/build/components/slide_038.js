// slide_038 component — "Residual Connections and Normalization" (002_transformers_part2)
// Deep Learning DSAI 308 — banked for cross-video/in-video children (slide 59 ← 38;
// dependency audit recommends 38←36, 36 unbuilt at build time => STANDALONE build).
//
// CHROME LAW: shared playlist module shared_patterns/house_chrome.js (badge numeral =
// number printed on THIS original frame = 38). ml-intro values superseded.
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide038/m1..m17):
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Verified on THIS frame's chrome landmarks: left border col 58 -> slide 41.0 (house 42),
// right border col 901 -> 917.9 (house 918), top row 43 -> 45.0, bottom stroke 516 -> 540;
// badge yellow-fill bbox center (875.5, 71.0) -> (891.6, 74.3) vs house (893, 71) — same
// accepted JPEG-bbox delta as certified 002/018/035. Diagram panel border: frame
// x 65..893, y 249..511 -> slide x 48.2..909.6, y 260.5..534.8 (centered on 480).
//
// CONTENT DECISIONS (evidence in worker_report.md):
//  * Vector labels 1-based per the transcript of record + raw agreement + pixel-width
//    analysis (tail col7 subscript ~11px = 3 glyphs "N-1", col8 ~5px = 1 glyph "N";
//    col1 subscript shows stem+flag = "1"): Y_1..Y_6, 5 dots, Y_{N-1}, Y_N; X row same;
//    mid row carries PRIMES (Y') per the transcript of record + sheet-B tail reads.
//    (Supersedes the raw's [Y_N3?]/[Y_N2?] -> "likely Y_{N-3}, Y_{N-2}" guess, which
//    SOURCES.md itself flagged for build-time zoom; zoom reads banked under scratch/slide038.)
//  * Each vector bar = 4 sub-cells [FFFF00][92D050][FF9999][D9D9D9] x 12.5pt, thin dark
//    outlines; the red label is printed ON the bar, centered on the column (sheet C:
//    "the peach square contains a dark red Y with a red subscript").
//  * Arrows: thin red up-arrows gray-bar->top-row (8); thin green up-arrows plus->gray-bar
//    (8); thin navy up-arrows mid-row->plus (8) — all through the green dash-dot container
//    border; chunky BLUE OUTLINED BLOCK ARROWS with spiral hatching (16: X-row->block,
//    block->mid-row) as a generated PNG asset; thin ORANGE curved residual arrows entering
//    each plus-circle from the left (8) as a generated PNG asset (path from measured
//    per-y clusters, identical per column, pitch 73.5pt).
//  * Omitted as video artifacts (judge GROUND RULES (c)): mouse cursor near the LayerNorm
//    bar top edge; black letterbox strip at the frame bottom.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const pt = (v) => v / 72; // slide pts -> inches

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/";

// ---- palette (spec + measured cores) ----
const RED = "C00000";     // title, labels, plus circles, red arrows, caption
const BLUE = "0000CC";    // defbox text/border, top/mid dots
const NAVY = "00008B";    // MHSA block, navy arrows
const GREEN = "00B050";   // container border, green arrows, X-row dots
const ORANGE = "E36C09";  // residual curves + annotation
const GRAYBAR = "D9D9D9";
const GRAYLINE = "7F7F7F";
const CELL_LINE = "595959";
const CONT_FILL = "E2EFDA";
const YELLOW = "FFFF00";
const FONT = "Arial";

// ---- measured geometry (slide pts) ----
const T = {
  title: { text: "Residual Connections and Normalization", inkCx: 510.2, capTop: 74.3, size: 28.3 },
  defbox: { x: 79.5, y: 115.1, w: 797.9, h: 131.8 },
  defLines: [ // [text, inkLeft, capTop, bold]
    ["Adding Residual Connection:", 90.9, 123.5, true],
    ["Word Embedding + Positional Information   [First Transformer Block]", 168.9, 144.4, false],
    ["Output of Previous Transformer Block      [Stacked Transformer Blocks]", 170.0, 163.3, false],
    ["Adding \u201cLAYER\u201d Normalization", 90.9, 205.1, true],
    ["Encoded Vectors of Input Sequence   [With Same Input Vectors Dimension", 170.0, 225.0, false],
  ],
  panel: { x: 48.2, y: 260.5, w: 861.4, h: 274.3 },
  container: { x: 62.8, y: 297.2, w: 840.6, h: 80.6 },
  grayBar: { x: 162.5, y: 309.8, w: 718.0, h: 25.1 },
  navy: { x: 153.3, y: 419.6, w: 747.0, h: 51.3 },
  cols: [194.9, 270.3, 346.3, 422.8, 499.8, 574.1, 771.8, 848.8],
  barW: 50.0, cellW: 12.5,
  rows: { top: { y: 272.1, h: 17.8 }, mid: { y: 383.0, h: 16.7 }, x: { y: 490.8, h: 15.7 } },
  plusCy: 356.8, plusD: 15.6,
  arrows: { red: { y0: 290.5, y1: 309.8 }, green: { y0: 336.0, y1: 349.5 }, navyA: { y0: 365.0, y1: 383.0 } },
  blkArrow: { w: 10.5, h: 20.0, midY: 399.7, xY: 470.9 },
  orange: { w: 54.0, h: 149.0, y: 351.0, dx: -52.0 },
  dots: { x: [634.6, 654.0, 672.6, 691.3, 707.6], d: 7.8, yTop: 281.0, yMid: 391.4, yX: 498.6 },
  ann: { cx: 100, size: 12, lines: [
    ["Output of Self", 386.2, BLUE], ["Attention", 402.9, BLUE],
    ["Residual", 436.4, ORANGE], ["Connections", 452.1, ORANGE],
    ["Input to Self", 476.2, RED], ["Attention", 491.9, RED],
  ] },
  caption: { text: "Word Embedding + Positional Information", cx: 410.25, capTop: 519.1, size: 14,
             hl: { x: 263.6, y: 517.0, w: 294.4, h: 13.6 } },
  grayBarText: { size: 16 },
  navyText: { size: 18 },
  labelSize: 14,
};

const LABEL_SUBS = ["1", "2", "3", "4", "5", "6", "N-1", "N"];

function lead(size) { return 0.273 * size; } // ink-top offset below a valign-top margin-0 box top

function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 38 : opts.numeral;

  // ---- 1. playlist house chrome (white canvas, gray panel, red border, badge) ----
  drawHouseChrome(pptx, slide, { numeral });

  // ---- 1b. title: red bold, centered on the MEASURED ink center (510.2pt — the
  //      original title genuinely sits ~30pt right of slide center; frame wins) ----
  slide.addText(T.title.text, {
    x: pt(T.title.inkCx - 360), y: pt(T.title.capTop - lead(T.title.size)),
    w: pt(720), h: pt(42),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: T.title.size, bold: true, color: RED, lineSpacing: 34,
  });

  // ---- 2. definition box (white, blue border) + its five single-line text boxes ----
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.defbox.x), y: pt(T.defbox.y), w: pt(T.defbox.w), h: pt(T.defbox.h),
    fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.75 },
  });
  for (const [text, inkLeft, capTop, bold] of T.defLines) {
    slide.addText(text, {
      x: pt(inkLeft - 0.6), y: pt(capTop - lead(16.5)), w: pt(640), h: pt(24),
      align: "left", valign: "top", margin: 0,
      fontFace: FONT, fontSize: 16.5, bold, color: BLUE,
    });
  }

  // ---- 3. diagram panel (white, thin red border) ----
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.panel.x), y: pt(T.panel.y), w: pt(T.panel.w), h: pt(T.panel.h),
    fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 },
  });

  // ---- 4. green dashed rounded container (behind bar + plus row) ----
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(T.container.x), y: pt(T.container.y), w: pt(T.container.w), h: pt(T.container.h),
    fill: { color: CONT_FILL }, line: { color: GREEN, width: 1.25, dashType: "dashDot" },
    rectRadius: 0.08,
  });

  // ---- 5. gray LayerNorm bar + its two-style bold-italic text ----
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.grayBar.x), y: pt(T.grayBar.y), w: pt(T.grayBar.w), h: pt(T.grayBar.h),
    fill: { color: GRAYBAR }, line: { color: GRAYLINE, width: 1 },
  });
  slide.addText(
    [
      { text: "Layer Normalization", options: { color: RED } },
      { text: "  (NOT Batch Normalization)", options: { color: "000000" } },
    ],
    {
      x: pt(T.grayBar.x), y: pt(T.grayBar.y), w: pt(T.grayBar.w), h: pt(T.grayBar.h),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: T.grayBarText.size, bold: true, italic: true, lineSpacing: 20,
    }
  );

  // ---- 6. orange curved residual arrows (8) — drawn BEFORE the navy block: in the
  //      original the curves pass BEHIND the block (measured: col2+ curve ink vanishes
  //      at frame y 396..452 where the block sits, re-emerging below it) ----
  for (const cx of T.cols) {
    slide.addImage({ path: ASSETS + "s038_orangearrow.png",
      x: pt(cx + T.orange.dx), y: pt(T.orange.y), w: pt(T.orange.w), h: pt(T.orange.h) });
  }

  // ---- 7. navy MHSA block + white bold text ----
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.navy.x), y: pt(T.navy.y), w: pt(T.navy.w), h: pt(T.navy.h),
    fill: { color: NAVY },
  });
  slide.addText("Multi Head Self Attention Block", {
    x: pt(T.navy.x), y: pt(T.navy.y), w: pt(T.navy.w), h: pt(T.navy.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: T.navyText.size, bold: true, color: "FFFFFF", lineSpacing: 24,
  });

  // ---- 7. three vector rows: 4-cell bars + red labels + ellipsis dots ----
  for (const rowKey of ["top", "mid", "x"]) {
    const row = T.rows[rowKey];
    for (let i = 0; i < 8; i++) {
      const cx = T.cols[i];
      const bx = cx - T.barW / 2;
      const cellColors = [YELLOW, "92D050", "FF9999", GRAYBAR];
      for (let c = 0; c < 4; c++) {
        slide.addShape(pptx.ShapeType.rect, {
          x: pt(bx + c * T.cellW), y: pt(row.y), w: pt(T.cellW), h: pt(row.h),
          fill: { color: cellColors[c] }, line: { color: CELL_LINE, width: 0.75 },
        });
      }
      // red label printed ON the bar, centered on the column
      const letter = rowKey === "x" ? "X" : "Y";
      const runs = [{ text: letter, options: {} }];
      if (rowKey === "mid") runs.push({ text: "'", options: {} });
      runs.push({ text: LABEL_SUBS[i], options: { subscript: true } });
      slide.addText(runs, {
        x: pt(cx - 13), y: pt(row.y - 1.5), w: pt(26), h: pt(row.h + 3),
        align: "center", valign: "middle", margin: 0,
        fontFace: FONT, fontSize: T.labelSize, bold: true, italic: true, color: RED,
        lineSpacing: T.labelSize,
      });
    }
    // ellipsis dots (blue in Y rows, green in the X row), centered on the bar band
    const dotColor = rowKey === "x" ? GREEN : BLUE;
    const dotCy = rowKey === "top" ? T.dots.yTop : rowKey === "mid" ? T.dots.yMid : T.dots.yX;
    for (const dx of T.dots.x) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: pt(dx - T.dots.d / 2), y: pt(dotCy - T.dots.d / 2),
        w: pt(T.dots.d), h: pt(T.dots.d), fill: { color: dotColor },
      });
    }
  }

  // ---- 8. plus circles (red ring, white fill, red +) ----
  for (const cx of T.cols) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: pt(cx - T.plusD / 2), y: pt(T.plusCy - T.plusD / 2),
      w: pt(T.plusD), h: pt(T.plusD),
      fill: { color: "FFFFFF" }, line: { color: RED, width: 2.75 },
    });
    slide.addText("+", {
      x: pt(cx - T.plusD / 2), y: pt(T.plusCy - T.plusD / 2),
      w: pt(T.plusD), h: pt(T.plusD),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 14, bold: true, color: RED,
    });
  }

  // ---- 9. thin arrows: red (bar->top row), green (plus->bar), navy (mid row->plus) ----
  for (const cx of T.cols) {
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(T.arrows.red.y0), w: 0, h: pt(T.arrows.red.y1 - T.arrows.red.y0),
      line: { color: RED, width: 1.75, beginArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(T.arrows.green.y0), w: 0, h: pt(T.arrows.green.y1 - T.arrows.green.y0),
      line: { color: GREEN, width: 1.75, beginArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(T.arrows.navyA.y0), w: 0, h: pt(T.arrows.navyA.y1 - T.arrows.navyA.y0),
      line: { color: NAVY, width: 1.5, beginArrowType: "triangle" },
    });
  }

  // ---- 10. spiral-hatched navy block arrows (16) ----
  for (const cx of T.cols) {
    slide.addImage({ path: ASSETS + "s038_blkarrow.png",
      x: pt(cx - T.blkArrow.w / 2), y: pt(T.blkArrow.midY), w: pt(T.blkArrow.w), h: pt(T.blkArrow.h) });
    slide.addImage({ path: ASSETS + "s038_blkarrow.png",
      x: pt(cx - T.blkArrow.w / 2), y: pt(T.blkArrow.xY), w: pt(T.blkArrow.w), h: pt(T.blkArrow.h) });
  }

  // ---- 12. left-margin annotations (two-line, bold italic, color-coded) ----
  for (const [text, capTop, color] of T.ann.lines) {
    slide.addText(text, {
      x: pt(T.ann.cx - 60), y: pt(capTop - lead(T.ann.size)), w: pt(120), h: pt(18),
      align: "center", valign: "top", margin: 0,
      fontFace: FONT, fontSize: T.ann.size, bold: true, italic: true, color,
    });
  }

  // ---- 13. yellow-highlighted caption at the panel bottom ----
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.caption.hl.x), y: pt(T.caption.hl.y), w: pt(T.caption.hl.w), h: pt(T.caption.hl.h),
    fill: { color: YELLOW },
  });
  slide.addText(T.caption.text, {
    x: pt(T.caption.cx - 300), y: pt(T.caption.capTop - lead(T.caption.size)),
    w: pt(600), h: pt(20),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: T.caption.size, bold: true, italic: true, color: RED,
  });
}

module.exports = { renderBase, T };
