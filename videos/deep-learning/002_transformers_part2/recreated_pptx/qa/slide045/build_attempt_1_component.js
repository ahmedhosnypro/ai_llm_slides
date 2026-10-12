// components/slide_045.js — slide 045 "Feed Forward Neural Network" composition
// (002_transformers_part2, Deep Learning DSAI 308).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11 + dependency audit): slide 45 is a
// CHILD of slide 038 per the corrective audit (45<-38 double-confirmed: 38's composition
// is exactly 45's base — X->MHA->(+)/LN(green-dashed)->Yout with identical left labels,
// caption position, vector style; canonical graph still says 45<-28, un-amended — build
// follows the audit evidence, see qa/slide045/worker_report.md). Slide 46 is a CONFIRMED
// dependent (46 = this composition + a second (+)/LN unit + "Final Output" callout +
// 4th label): it MUST require() this module and call renderBase(pptx, slide, opts) or
// cherry-pick blocks via opts.skip / opts.only — never re-derive this geometry.
//
// Block granularity (001 slide_014 pattern): every visual block is its own function;
// renderBase accepts
//   opts.skip   — array of block names to OMIT (child removes inherited blocks)
//   opts.only   — array of block names to DRAW exclusively (child replaces composition)
//   opts.chrome — draw house chrome (default true; playlist shared module)
//   opts.numeral— badge numeral (default 45)
// Block names: title, annotbox, panel, ffnbox, topRow, blueArrows, midRow, unit,
//   navy, blkArrows, xRow, ann, caption.
// Slide 46 additionally gets drawNormUnit(pptx, slide, u) exported — call it a second
// time with a shifted geometry object u (same shape as T.unit) to add its second
// (+)/LN unit; T.unit documents the field shape.
//
// PARENT REUSE (inheritance law): the certified parent component
// ./slide_038.js is require()d and its exported T supplies the SHARED geometry that is
// pixel-identical here (vector columns T.cols, ellipsis-dot x positions T.dots.x, bar/
// cell widths, palette, strip drawing mechanism, block-arrow + orange-curve ASSETS).
// The parent's monolithic renderBase is NOT called directly: this frame shifts the whole
// shared diagram +12.6pt in y (measured), and six blocks genuinely differ (title
// text/position, defbox->annot swap, panel red->blue + taller, plus style white-ring ->
// dark-red filled, gray-bar text short form, caption underscores, + FFN delta blocks).
// Every 045 position below is THIS frame's own PIL measurement
// (scratch/slide045/m6_full.py, m7_refine.py, m8_compare.py, m10_icons.py, m11_final.py;
// frame->slide mapping SX=0.962329 OX=17.582 SY=0.955556 OY=0 — chrome landmarks
// L58/R901/T43/B516, identical to the certified 038 fit).
//
// CONTENT DECISIONS (evidence in worker_report.md):
//  * Vector labels 1-based Y_1..Y_6, 5 blue dots, Y_{N-1}, Y_N; X row same; NO primes on
//    any row (validated spec + zoom sheet B; supersedes 038's mid-row primes reading).
//  * Plus nodes: DARK-RED FILLED discs (990000) with WHITE bold "+" (pixel-probed center
//    + zoom sheet B zone 3) — differs from 038's white-filled style on purpose.
//  * Panel / FFN / annot borders: deck blue 0000CC (spec; certified 038 family value).
//  * Annot lines 2/3 bracket text is BLUE on this frame (pixel + zoom sheet A) — the
//    spec's "red [Size:...]" is overridden by the frame.
//  * Gray bar text: "Layer Normalization" only (no "(NOT Batch Normalization)" — pixel
//    ink extent 423..604 + zoom sheet A zone 2).
//  * Caption keeps literal underscores: "Word_Embedding + Positional_Information"
//    (spec verbatim + two full-frame transcripts + ink width +5px vs 038's spaced
//    version; the x3 crop zoom read "spaces" — documented, outweighed).
//  * FFN mini-icons: cream tiles (FFE699) with thin dark-red border, 4 green dots
//    (upper) + 8 magenta dots (bottom) + thin green-gray fan lines, red "RELU" top-right
//    (pixel census m10/m11 + zoom sheet B). NO ellipsis dots inside the FFN box
//    (measured empty gap 633..722 — spec's "5 blue dots" is an analyst error).
//  * Omitted as video artifacts (judge GROUND RULES (c)): pen/marker cursor over FFN
//    icon 1's top-left; black letterbox strip at the frame bottom.

const path = require("path");
const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const p38 = require(path.join(__dirname, "slide_038.js"));

const pt = (v) => v / 72; // slide pts -> inches

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/";

// ---- palette (parent-certified values + spec) ----
const RED = "C00000";
const BLUE = "0000CC";
const NAVY = "00008B";
const GREEN = "00B050";
const ORANGE = "E8A020";
const GRAYBAR = "D9D9D9";
const GRAYLINE = "7F7F7F";
const CELL_LINE = "595959";
const CONT_FILL = "E2EFDA";
const YELLOW = "FFFF00";
const DRED = "990000";   // plus-disc fill (045 measured style)
const DRED_LINE = "7F0000";
const TILE_FILL = "FFE699";
const TILE_LINE = "C00000";
const FAN_LINE = "5E8C6A";
const FONT = "Arial";

// ---- measured geometry (slide pts) ----
const T = {
  title: { text: "Feed Forward Neural Network", inkCx: 492.4, capTop: 56.5, size: 28.3 },
  annot: {
    x: 74.2, y: 83.7, w: 821.1, h: 77.5, size: 18,
    lines: [ // capTop + [text, inkLeft, color] parts (two boxes per line: measured gap)
      { capTop: 92.1, parts: [["Feed Forward Network for each Vector", 85.6, BLUE], ["(After applying Normalization)", 424.4, RED]] },
      { capTop: 114.1, parts: [["One Hidden Layer with RELU Activation,", 124.1, BLUE], ["[Size: at least double Input dimension]", 502.9, BLUE]] },
      { capTop: 136.0, parts: [["Linear Activation Output Layer", 125.1, BLUE], ["[Size: same Input Vector dimension]", 502.9, BLUE]] },
    ],
  },
  panel: { x: 49.2, y: 166.4, w: 859.4, h: 367.5, lineW: 2 },
  ffn: {
    x: 151.0, y: 209.3, w: 749.3, h: 60.7, lineW: 1.75,
    title: { text: "Feed Forward Networks [ One Hidden with  RELU Activation]", cx: 527.8, capTop: 215.6, size: 16 },
    tile: {
      w: 72.7, y: 234.4, h: 29.4,
      cxs: [193.5, 275.3, 356.6, 439.7, 520.3, 601.9, 769.5, 850.5],
      greenD: 5.2, greenCy: 242.3, greenDx: [-10.3, -2.0, 6.3, 14.6],
      purpleD: 5.7, purpleCy: 254.8, purpleDx: [-28.4, -20.1, -11.7, -3.4, 4.9, 13.2, 21.6, 29.9],
      fanFromCy: 242.3, fanToCy: 254.8,
      relu: { size: 7, capTop: 238.6, rightInset: 8 },
    },
  },
  unit: { // the (+)/LN unit — drawNormUnit geometry (slide 46 reuses with a shift)
    container: { x: 128.2, y: 310.9, w: 774.2, h: 78.5 },
    grayBar: { x: 163.6, y: 322.3, w: 715.0, h: 28.3 },
    plus: { cy: 369.9, d: 15.6, style: "filled" }, // "filled" (045) | "ring" (038 style)
    row: { y: 394.8, h: 18.0 },                    // the unit's own Y row
    arrows: { red: { y0: 302.5, y1: 322.3 }, green: { y0: 351.0, y1: 362.1 }, navy: { y0: 377.7, y1: 394.8 } },
    curves: { y: 363.6, h: 149.0, dx: -52.0, w: 54.0 },
  },
  rows: { top: { y: 175.0, h: 17.5 }, mid: { y: 286.0, h: 16.7 }, x: { y: 502.6, h: 17.2 } },
  navy: { x: 153.1, y: 432.2, w: 747.1, h: 51.3 },
  blkArrow: { w: 10.5, h: 20.0, zone1Y: 412.4, zone2Y: 483.0 },
  blueArrows: { top: { y0: 191.5, y1: 209.3 }, ffn: { y0: 270.0, y1: 286.0 } },
  // SHARED with the certified parent (pixel-identical on this frame):
  cols: p38.T.cols,
  barW: p38.T.barW, cellW: p38.T.cellW,
  dots: { x: p38.T.dots.x, d: p38.T.dots.d },
  ann: { cx: 94, size: 12, lines: [
    ["Output of Self", 398.7, BLUE], ["Attention", 415.4, BLUE],
    ["Residual", 447.9, ORANGE], ["Connections", 464.7, ORANGE],
    ["Input to Self", 489.8, RED], ["Attention", 505.5, RED],
  ] },
  caption: { text: "Word_Embedding + Positional_Information", cx: 412.2, capTop: 524.3, size: 14,
             hl: { x: 266.4, y: 520.1, w: 291.5, h: 13.7 } },
};

const LABEL_SUBS = ["1", "2", "3", "4", "5", "6", "N-1", "N"];

function lead(size) { return 0.273 * size; } // ink-top offset below a valign-top margin-0 box top

// ---- vector strip row (parent mechanism, shared cols/widths) ----
function drawStripRow(pptx, slide, row, letter, dotCy, dotColor) {
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
    const runs = [{ text: letter, options: {} }, { text: LABEL_SUBS[i], options: { subscript: true } }];
    slide.addText(runs, {
      x: pt(cx - 13), y: pt(row.y - 1.5), w: pt(26), h: pt(row.h + 3),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 14, bold: true, italic: true, color: RED,
      lineSpacing: 14,
    });
  }
  for (const dx of T.dots.x) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: pt(dx - T.dots.d / 2), y: pt(dotCy - T.dots.d / 2),
      w: pt(T.dots.d), h: pt(T.dots.d), fill: { color: dotColor },
    });
  }
}

// ---- the (+)/LN unit (exported for slide 46's second unit) ----
function drawNormUnit(pptx, slide, u) {
  // green dashed rounded container
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(u.container.x), y: pt(u.container.y), w: pt(u.container.w), h: pt(u.container.h),
    fill: { color: CONT_FILL }, line: { color: GREEN, width: 1.25, dashType: "dashDot" },
    rectRadius: 0.08,
  });
  // gray LayerNorm bar + two-style bold-italic text
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(u.grayBar.x), y: pt(u.grayBar.y), w: pt(u.grayBar.w), h: pt(u.grayBar.h),
    fill: { color: GRAYBAR }, line: { color: GRAYLINE, width: 1 },
  });
  slide.addText(
    [
      { text: "Layer", options: { color: RED } },
      { text: " Normalization", options: { color: "000000" } },
    ],
    {
      x: pt(u.grayBar.x), y: pt(u.grayBar.y), w: pt(u.grayBar.w), h: pt(u.grayBar.h),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 16, bold: true, italic: true, lineSpacing: 20,
    }
  );
  // orange curved residual arrows BEHIND the rows/block (038 measured layering)
  for (const cx of T.cols) {
    slide.addImage({ path: ASSETS + "s038_orangearrow.png",
      x: pt(cx + u.curves.dx), y: pt(u.curves.y), w: pt(u.curves.w), h: pt(u.curves.h) });
  }
  // the unit's own Y row (labels ON the bar, 1-based, no primes)
  const dotCy = u.row.y + u.row.h / 2;
  drawStripRow(pptx, slide, u.row, "Y", dotCy, BLUE);
  // residual-add nodes: 045 style = dark-red FILLED disc + white "+"
  for (const cx of T.cols) {
    if (u.plus.style === "ring") {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: pt(cx - u.plus.d / 2), y: pt(u.plus.cy - u.plus.d / 2),
        w: pt(u.plus.d), h: pt(u.plus.d),
        fill: { color: "FFFFFF" }, line: { color: RED, width: 2.75 },
      });
      slide.addText("+", {
        x: pt(cx - u.plus.d / 2), y: pt(u.plus.cy - u.plus.d / 2),
        w: pt(u.plus.d), h: pt(u.plus.d),
        align: "center", valign: "middle", margin: 0,
        fontFace: FONT, fontSize: 14, bold: true, color: RED,
      });
    } else {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: pt(cx - u.plus.d / 2), y: pt(u.plus.cy - u.plus.d / 2),
        w: pt(u.plus.d), h: pt(u.plus.d),
        fill: { color: DRED }, line: { color: DRED_LINE, width: 1.5 },
      });
      slide.addText("+", {
        x: pt(cx - u.plus.d / 2), y: pt(u.plus.cy - u.plus.d / 2),
        w: pt(u.plus.d), h: pt(u.plus.d),
        align: "center", valign: "middle", margin: 0,
        fontFace: FONT, fontSize: 14, bold: true, color: "FFFFFF",
      });
    }
  }
  // thin arrows: green (plus->gray bar), navy (row->plus), red (gray bar->row above)
  for (const cx of T.cols) {
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(u.arrows.green.y0), w: 0, h: pt(u.arrows.green.y1 - u.arrows.green.y0),
      line: { color: GREEN, width: 1.75, beginArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(u.arrows.navy.y0), w: 0, h: pt(u.arrows.navy.y1 - u.arrows.navy.y0),
      line: { color: NAVY, width: 1.5, beginArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(u.arrows.red.y0), w: 0, h: pt(u.arrows.red.y1 - u.arrows.red.y0),
      line: { color: RED, width: 1.75, beginArrowType: "triangle" },
    });
  }
}

// ---- block functions ----

function drawTitle(pptx, slide) {
  slide.addText(T.title.text, {
    x: pt(T.title.inkCx - 360), y: pt(T.title.capTop - lead(T.title.size)),
    w: pt(720), h: pt(42),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: T.title.size, bold: true, color: RED, lineSpacing: 34,
  });
}

function drawAnnotBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.annot.x), y: pt(T.annot.y), w: pt(T.annot.w), h: pt(T.annot.h),
    fill: { color: "FFFFCC" }, line: { color: BLUE, width: 1.75 },
  });
  for (const line of T.annot.lines) {
    for (const [text, inkLeft, color] of line.parts) {
      slide.addText(text, {
        x: pt(inkLeft - 0.6), y: pt(line.capTop - lead(T.annot.size)), w: pt(640), h: pt(24),
        align: "left", valign: "top", margin: 0,
        fontFace: FONT, fontSize: T.annot.size, bold: true, color,
      });
    }
  }
}

function drawPanel(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.panel.x), y: pt(T.panel.y), w: pt(T.panel.w), h: pt(T.panel.h),
    fill: { color: "FFFFFF" }, line: { color: BLUE, width: T.panel.lineW },
  });
}

function drawFFNBox(pptx, slide) {
  const f = T.ffn, t = f.tile;
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(f.x), y: pt(f.y), w: pt(f.w), h: pt(f.h),
    fill: { color: "DDEBF7" }, line: { color: BLUE, width: f.lineW },
  });
  slide.addText(f.title.text, {
    x: pt(f.title.cx - 330), y: pt(f.title.capTop - lead(f.title.size)),
    w: pt(660), h: pt(22),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: f.title.size, bold: true, italic: true, color: BLUE,
  });
  for (const cx of t.cxs) {
    // cream tile with thin dark-red border
    slide.addShape(pptx.ShapeType.roundRect, {
      x: pt(cx - t.w / 2), y: pt(t.y), w: pt(t.w), h: pt(t.h),
      fill: { color: TILE_FILL }, line: { color: TILE_LINE, width: 0.75 },
      rectRadius: 0.04,
    });
    // fan lines first (under the dots): each green dot -> each magenta dot
    for (const gdx of t.greenDx) {
      for (const pdx of t.purpleDx) {
        slide.addShape(pptx.ShapeType.line, {
          x: pt(cx + gdx), y: pt(t.fanFromCy),
          w: pt(pdx - gdx), h: pt(t.fanToCy - t.fanFromCy),
          line: { color: FAN_LINE, width: 0.5 },
        });
      }
    }
    // green dots (upper)
    for (const gdx of t.greenDx) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: pt(cx + gdx - t.greenD / 2), y: pt(t.greenCy - t.greenD / 2),
        w: pt(t.greenD), h: pt(t.greenD), fill: { color: GREEN },
      });
    }
    // magenta dots (bottom row)
    for (const pdx of t.purpleDx) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: pt(cx + pdx - t.purpleD / 2), y: pt(t.purpleCy - t.purpleD / 2),
        w: pt(t.purpleD), h: pt(t.purpleD), fill: { color: "B871B8" },
      });
    }
    // RELU red text, top-right of the tile
    slide.addText("RELU", {
      x: pt(cx + t.w / 2 - 8 - t.relu.rightInset - 14), y: pt(t.relu.capTop - lead(t.relu.size)),
      w: pt(22), h: pt(10),
      align: "right", valign: "top", margin: 0,
      fontFace: FONT, fontSize: t.relu.size, bold: true, color: RED,
    });
  }
}

function drawTopRow(pptx, slide) {
  drawStripRow(pptx, slide, T.rows.top, "Y", T.rows.top.y + T.rows.top.h / 2, BLUE);
}

function drawBlueArrows(pptx, slide) {
  for (const cx of T.cols) {
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(T.blueArrows.top.y0), w: 0, h: pt(T.blueArrows.top.y1 - T.blueArrows.top.y0),
      line: { color: NAVY, width: 1.5, beginArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(T.blueArrows.ffn.y0), w: 0, h: pt(T.blueArrows.ffn.y1 - T.blueArrows.ffn.y0),
      line: { color: NAVY, width: 1.5, beginArrowType: "triangle" },
    });
  }
}

function drawMidRow(pptx, slide) {
  drawStripRow(pptx, slide, T.rows.mid, "Y", T.rows.mid.y + T.rows.mid.h / 2, BLUE);
}

function drawNavy(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.navy.x), y: pt(T.navy.y), w: pt(T.navy.w), h: pt(T.navy.h),
    fill: { color: NAVY },
  });
  slide.addText("Multi Head Self Attention Block", {
    x: pt(T.navy.x), y: pt(T.navy.y), w: pt(T.navy.w), h: pt(T.navy.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 18, bold: true, color: "FFFFFF", lineSpacing: 24,
  });
}

function drawBlkArrows(pptx, slide) {
  for (const cx of T.cols) {
    slide.addImage({ path: ASSETS + "s038_blkarrow.png",
      x: pt(cx - T.blkArrow.w / 2), y: pt(T.blkArrow.zone1Y), w: pt(T.blkArrow.w), h: pt(T.blkArrow.h) });
    slide.addImage({ path: ASSETS + "s038_blkarrow.png",
      x: pt(cx - T.blkArrow.w / 2), y: pt(T.blkArrow.zone2Y), w: pt(T.blkArrow.w), h: pt(T.blkArrow.h) });
  }
}

function drawXRow(pptx, slide) {
  drawStripRow(pptx, slide, T.rows.x, "X", T.rows.x.y + T.rows.x.h / 2, GREEN);
}

function drawAnn(pptx, slide) {
  for (const [text, capTop, color] of T.ann.lines) {
    slide.addText(text, {
      x: pt(T.ann.cx - 60), y: pt(capTop - lead(T.ann.size)), w: pt(120), h: pt(18),
      align: "center", valign: "top", margin: 0,
      fontFace: FONT, fontSize: T.ann.size, bold: true, italic: true, color,
    });
  }
}

function drawCaption(pptx, slide) {
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

const BLOCKS = {
  title: drawTitle, annotbox: drawAnnotBox, panel: drawPanel, ffnbox: drawFFNBox,
  topRow: drawTopRow, blueArrows: drawBlueArrows, midRow: drawMidRow,
  unit: (pptx, slide) => drawNormUnit(pptx, slide, T.unit),
  navy: drawNavy, blkArrows: drawBlkArrows, xRow: drawXRow, ann: drawAnn, caption: drawCaption,
};

const PAINT_ORDER = ["title", "annotbox", "panel", "ffnbox", "topRow", "blueArrows",
  "midRow", "unit", "navy", "blkArrows", "xRow", "ann", "caption"];

function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 45 : opts.numeral;
  if (opts.chrome !== false) drawHouseChrome(pptx, slide, { numeral });
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  for (const name of PAINT_ORDER) {
    if (only ? !only.has(name) : skip.has(name)) continue;
    BLOCKS[name](pptx, slide);
  }
}

module.exports = { renderBase, drawNormUnit, drawStripRow, T, BLOCKS, PAINT_ORDER };
