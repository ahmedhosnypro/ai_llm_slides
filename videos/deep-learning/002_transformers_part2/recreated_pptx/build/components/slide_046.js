// components/slide_046.js — slide 046 "Transformer Encoder Block (reconstructed — original
// slide has no title)" composition (002_transformers_part2, Deep Learning DSAI 308).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slide 46 is a CHILD of slide 045
// (46<-45 CONFIRMED; 45 certified PASS in this video's DB) and the PARENT of slides
// 47<-46, 48<-47, 57<-47. Children MUST require() this module and call
// renderBase(pptx, slide, opts) — never re-derive this geometry.
//
// COMPOSITION (full provenance in the build wrapper + qa/slide046/worker_report.md):
// the certified parent component ./slide_045.js supplies the SHARED diagram — its block
// functions (panel/ffnbox/navy/blkArrows/ann) are called with p45.T mutated to THIS
// frame's measurements (+6.35pt uniform downward shift, verified on the bottom-unit
// container dashes / plus cy / navy bar, all EXACT); its strip/unit mechanisms are forked
// HERE with ONLY the label subscript array changed (this frame is 0-BASED: X_0..X_5,
// N-2, N-1 — vision-confirmed, scratch/slide046/subzoom_xrow.txt + subzoom_xcol12.txt;
// the parent's LABEL_SUBS is module-internal and 1-based). Delta blocks: second (+)/LN
// unit at top (measured compressed container h 72.2), final Y row, pink "Final Output"
// callout, 4th left annotation pair, BLOCK arrows in the FFN gaps (replacing 045's thin
// navy lines), caption with PINK highlight band (045's is yellow).
//
// opts: { numeral: 46 (default), chrome: true }
// Block granularity for children: drawStripRow46(pptx, slide, row, letter, dotCy, dotColor),
// drawNormUnit46(pptx, slide, u), drawCallout46, drawBlkFFN, drawCaption46, drawBadge46,
// uT/uB unit geometry objects, ROW_FINAL/ROW_POSTLN row objects — exported.

const pptxgen = require("pptxgenjs");
const p45 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_045.js");
const chromeMod = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const drawHouseChrome = chromeMod.drawHouseChrome;
const CHROME = chromeMod.CHROME;

const pt = (v) => v / 72;
const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/";

const RED = "C00000", BLUE = "0000CC", NAVY = "00008B", GREEN = "00B050";
const GRAYBAR = "D9D9D9", GRAYLINE = "7F7F7F", CELL_LINE = "595959";
const CONT_FILL = "E2EFDA", YELLOW = "FFFF00", DRED = "990000", DRED_LINE = "7F0000";
const ORANGE = "E8A020", FONT = "Arial";

const T = p45.T;
T.panel = { x: 49.2, y: 52.3, w: 859.4, h: 481.6, lineW: 2 };
T.ffn.y = 215.6;
T.ffn.title.capTop = 220.8;
T.ffn.tile.y = 240.7;
T.ffn.tile.greenCy = 248.6;
T.ffn.tile.purpleCy = 261.1;
T.ffn.tile.relu.capTop = 244.95;
T.navy.y = 438.5;
T.blkArrow.zone1Y = 418.75;
T.blkArrow.zone2Y = 489.35;
T.rows.x = { y: 509.0, h: 17.5 };
T.ann.lines = [
  ["Output of Self", 398.7 + 6.35, BLUE], ["Attention", 415.4 + 6.35, BLUE],
  ["Residual", 447.9 + 6.35, ORANGE], ["Connections", 464.7 + 6.35, ORANGE],
  ["Input to Self", 489.8 + 6.35, RED], ["Attention", 505.5 + 6.35, RED],
  ["Residual", 233.4, ORANGE], ["Connections", 250.1, ORANGE],
];
T.caption.capTop = 524.3 + 6.35;
T.caption.hl.y = 520.1 + 6.35;

const D = 6.35;
const uB = {
  container: { x: T.unit.container.x, y: T.unit.container.y + D, w: T.unit.container.w, h: T.unit.container.h },
  grayBar: { x: T.unit.grayBar.x, y: T.unit.grayBar.y + D, w: T.unit.grayBar.w, h: T.unit.grayBar.h },
  plus: { cy: T.unit.plus.cy + D, d: T.unit.plus.d, style: "filled" },
  row: { y: 401.2, h: 17.0 },
  arrows: {
    red: { y0: T.unit.arrows.red.y0 + D, y1: T.unit.arrows.red.y1 + D },
    green: { y0: T.unit.arrows.green.y0 + D, y1: T.unit.arrows.green.y1 + D },
    navy: { y0: T.unit.arrows.navy.y0 + D, y1: 401.2 },
  },
  curves: { y: T.unit.curves.y + D, h: T.unit.curves.h, dx: T.unit.curves.dx, w: T.unit.curves.w },
};
const uT = {
  container: { x: 128.2, y: 100.5, w: 774.2, h: 72.2 },
  grayBar: { x: 163.6, y: 106.7, w: 715.0, h: 28.0 },
  plus: { cy: 155.4, d: 15.6, style: "filled" },
  row: { y: 180.4, h: 17.0 },
  arrows: {
    red: { y0: 84.6, y1: 106.7 },
    green: { y0: 135.1, y1: 147.6 },
    navy: { y0: 163.2, y1: 180.4 },
  },
  curves: { y: 149.1, h: 151.3, dx: -52.0, w: 54.0 },
};
const ROW_FINAL = { y: 67.3, h: 17.5 };
const ROW_POSTLN = { y: 290.3, h: 17.5 };
const BLK_FFN = { upIntoPostFFN: { y: 198.8, h: 16.8 }, upIntoFFN: { y: 276.3, h: 13.5 }, w: 10.5 };

const SUBS_46 = ["0", "1", "2", "3", "4", "5", "N-2", "N-1"];

function drawStripRow46(pptx, slide, row, letter, dotCy, dotColor) {
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
    const runs = [{ text: letter, options: {} }, { text: SUBS_46[i], options: { subscript: true } }];
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

function drawNormUnit46(pptx, slide, u) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(u.container.x), y: pt(u.container.y), w: pt(u.container.w), h: pt(u.container.h),
    fill: { color: CONT_FILL }, line: { color: GREEN, width: 1.25, dashType: "dashDot" },
    rectRadius: 0.08,
  });
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
  for (const cx of T.cols) {
    slide.addImage({ path: ASSETS + "s038_orangearrow.png",
      x: pt(cx + u.curves.dx), y: pt(u.curves.y), w: pt(u.curves.w), h: pt(u.curves.h) });
  }
  const dotCy = u.row.y + u.row.h / 2;
  drawStripRow46(pptx, slide, u.row, "Y", dotCy, BLUE);
  for (const cx of T.cols) {
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

function drawCallout46(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(55.5), y: pt(54.4), w: pt(104.0), h: pt(51.3),
    fill: { color: "FFCCCC" }, line: { color: RED, width: 1.5 },
  });
  slide.addText([
    { text: "Final", options: { breakLine: true } },
    { text: "Output", options: {} },
  ], {
    x: pt(55.5), y: pt(64.9 - 0.273 * 16), w: pt(104.0), h: pt(40),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 16, bold: true, italic: true, color: RED,
    lineSpacing: 20,
  });
}

function drawBlkFFN(pptx, slide) {
  for (const cx of T.cols) {
    slide.addImage({ path: ASSETS + "s038_blkarrow.png",
      x: pt(cx - BLK_FFN.w / 2), y: pt(BLK_FFN.upIntoPostFFN.y),
      w: pt(BLK_FFN.w), h: pt(BLK_FFN.upIntoPostFFN.h) });
    slide.addImage({ path: ASSETS + "s038_blkarrow.png",
      x: pt(cx - BLK_FFN.w / 2), y: pt(BLK_FFN.upIntoFFN.y),
      w: pt(BLK_FFN.w), h: pt(BLK_FFN.upIntoFFN.h) });
  }
}

function drawCaption46(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(T.caption.hl.x), y: pt(T.caption.hl.y), w: pt(T.caption.hl.w), h: pt(T.caption.hl.h),
    fill: { color: "FFB6C1" },
  });
  slide.addText(T.caption.text, {
    x: pt(T.caption.cx - 300), y: pt(T.caption.capTop - 0.273 * T.caption.size),
    w: pt(600), h: pt(20),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: T.caption.size, bold: true, italic: true, color: RED,
  });
}

function drawBadge46(pptx, slide, numeral = 46) {
  // The diagram panel on this frame reaches y 52.3 (vs 045's 166.4) and its white fill
  // covers the badge zone; the original capture shows NO badge disc here (curation note:
  // "badge numeral cut off/unreadable at this frame"), but the playlist chrome law is
  // founder-directive and playlist-wide — the badge is RE-DRAWN above the content from
  // the shared module's constants (numeral = file id per 002 AGENTS.md).
  const bx = CHROME.badge.cx - CHROME.badge.d / 2;
  const by = CHROME.badge.cy - CHROME.badge.d / 2;
  slide.addShape(pptx.ShapeType.ellipse, {
    x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
    fill: { color: CHROME.badge.fill }, line: { color: CHROME.badge.ring, width: CHROME.badge.ringWidth },
  });
  slide.addText(String(numeral), {
    x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
    align: "center", valign: "middle", bold: true,
    fontSize: CHROME.badge.numeralSize, color: CHROME.badge.numeralColor,
    fontFace: CHROME.badge.fontFace, margin: 0,
  });
}

function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 46 : opts.numeral;
  if (opts.chrome !== false) drawHouseChrome(pptx, slide, { numeral });
  p45.BLOCKS.panel(pptx, slide);
  drawStripRow46(pptx, slide, ROW_FINAL, "Y", ROW_FINAL.y + ROW_FINAL.h / 2, BLUE);
  drawNormUnit46(pptx, slide, uT);
  p45.BLOCKS.ffnbox(pptx, slide);
  drawBlkFFN(pptx, slide);
  drawStripRow46(pptx, slide, ROW_POSTLN, "Y", ROW_POSTLN.y + ROW_POSTLN.h / 2, BLUE);
  drawNormUnit46(pptx, slide, uB);
  p45.BLOCKS.navy(pptx, slide);
  p45.BLOCKS.blkArrows(pptx, slide);
  drawStripRow46(pptx, slide, T.rows.x, "X", T.rows.x.y + T.rows.x.h / 2, GREEN);
  p45.BLOCKS.ann(pptx, slide);
  drawCallout46(pptx, slide);
  drawCaption46(pptx, slide);
  if (numeral !== null) drawBadge46(pptx, slide, numeral);
}

module.exports = { renderBase, drawStripRow46, drawNormUnit46, drawCallout46, drawBlkFFN,
  drawCaption46, drawBadge46, uT, uB, ROW_FINAL, ROW_POSTLN, BLK_FFN, SUBS_46, T };
