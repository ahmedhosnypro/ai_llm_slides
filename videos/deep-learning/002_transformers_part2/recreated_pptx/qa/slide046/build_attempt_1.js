// slide_046.js — "Transformer Encoder Block (reconstructed — original slide has no title)"
// (002_transformers_part2, Deep Learning DSAI 308). DEPENDENCY-GATED CHILD of slide 045
// (46<-45 CONFIRMED lineage; 45 certified PASS in this video's DB).
//
// COMPOSITION LAW (founder directive 2026-10-11 + 17 §3): the CERTIFIED parent component
// `components/slide_045.js` is require()d by absolute path and its per-block functions are
// COMPOSED — never re-derived, never copy-pasted as a whole. This frame's delta (all values
// are THIS frame's own PIL measurements, scratch/slide046/m1..m27; frame->slide mapping
// verified on the chrome landmarks L58/R901/T43/B516 -> SX=0.962329 OX=17.582 SY=0.955556
// OY=0, identical to the certified 038/045 fit):
//
//   1. The whole shared diagram sits +6.35pt LOWER than 045's (anchors: bottom unit
//      container dashes 303/378 frame = 045's +6.35 EXACT; plus cy 376.25 = 369.9+6.35;
//      navy bar 438.5 = 432.2+6.35 h 51.3 EXACT; X row 509.0; caption/callout/ann follow).
//   2. REMOVED vs 045: title block, yellow annot box, thin-navy blueArrows (this frame
//      shows BLOCK arrows in the two FFN gaps instead — measured ink 8-11px wide outlined
//      arrows in all 4 gaps; 045 had thin lines only in the FFN gaps).
//   3. ADDED: second (+)/LN unit at top (compressed: container h 72.2 vs 78.5, measured),
//      final Y row (y 67.3), pink "Final Output" callout (x 55.5 y 54.4 w 104.0 h 51.3,
//      FFCCCC/C00000, text capTops 64.9/84.8), 4th left annotation pair
//      ("Residual/Connections" orange, capTops 233.4/250.1), block arrows in the FFN gaps.
//   4. Panel: same x/w as 045 (49.2/859.4), top moved up to y 52.3 (blue border row 50
//      frame), bottom unchanged (533.9) -> h 481.6.
//   5. LABELS: this frame is 0-BASED — X_0..X_5, [5 dots], X_{N-2}, X_{N-1} on every row
//      (raw + spec agree; rightmost subscripts VISION-CONFIRMED N-2/N-1 through the gate,
//      scratch/slide046/subzoom_xrow.txt; matches the slide-047-frame resolution in
//      slide_046_source/SOURCES.md). The parent's strip mechanism hardcodes 1-based
//      module-internal labels, so drawStripRow/drawNormUnit are forked HERE with ONLY the
//      subscript array changed; geometry, palette, dot layout and style are inherited from
//      the parent's T (p45.T.cols/barW/cellW/dots read live).
//   6. Caption: SAME ink span as 045's certified underscored caption (273..553 frame px on
//      both frames) -> same string "Word_Embedding + Positional_Information", shifted
//      +6.35; the highlight band behind it is PINK on this frame (measured ~(255,185,195),
//      FFB6C1-family) vs 045's yellow — measured delta, kept.
//   7. X-row ellipsis dots: 5 GREEN dots at the same x as the upper rows' blue dots
//      (measured clusters 628..701 frame; the spec's "4 green dots" is an analyst error).
//   8. Omitted as video artifacts (GROUND RULES (c)): black letterbox strip (frame bottom,
//      rows 516..539), mouse cursor. The old transcript's "last two boxes highlighted
//      yellow" is NOT corroborated by the frame (pastel census m8b) — all 32 cells identical.
//
// Runtime mutation of p45.T (the exported geometry object, by reference) composes the
// parent's certified block functions (panel/ffnbox/navy/blkArrows/ann) with THIS frame's
// measured values. The component FILE is never edited (cascade law, 17 §6).

const pptxgen = require("pptxgenjs");
const p45 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_045.js");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const pt = (v) => v / 72; // slide pts -> inches
const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/";

// ---- palette: the certified parent's values (m8b: this frame's washed cells are
// ---- pixel-equivalent to 045's certified cells at the same slide positions) ----
const RED = "C00000";
const BLUE = "0000CC";
const NAVY = "00008B";
const GREEN = "00B050";
const GRAYBAR = "D9D9D9";
const GRAYLINE = "7F7F7F";
const CELL_LINE = "595959";
const CONT_FILL = "E2EFDA";
const YELLOW = "FFFF00";
const DRED = "990000";
const DRED_LINE = "7F0000";
const ORANGE = "E8A020";
const FONT = "Arial";

// ---- geometry: parent T, mutated to THIS frame's measurements (runtime only) ----
const T = p45.T;

// panel: same x/w as 045, top raised to the measured blue border (row 50 frame)
T.panel = { x: 49.2, y: 52.3, w: 859.4, h: 481.6, lineW: 2 };

// FFN box: measured border top 206 frame -> 215.6 slide; internals = 045's + 6.35
// (green dot cy 248.6 = 242.3+6.3, magenta cy 261.1 = 254.8+6.3 — EXACT frame matches);
// title capTop measured 220.8 (blue ink rows 211..223 frame)
T.ffn.y = 215.6;
T.ffn.title.capTop = 220.8;
T.ffn.tile.y = 240.7;
T.ffn.tile.greenCy = 248.6;
T.ffn.tile.purpleCy = 261.1;
T.ffn.tile.relu.capTop = 244.95;

// MHA bar: measured 438.5..489.8 (= 045's h 51.3 exactly, +6.35)
T.navy.y = 438.5;

// block arrows: the two navy gaps (outatt->MHA, MHA->X) = 045's zones + 6.35
T.blkArrow.zone1Y = 418.75;
T.blkArrow.zone2Y = 489.35;

// X row: measured lav band 487..503 frame (bias-corrected like the 045 calibration)
T.rows.x = { y: 509.0, h: 17.5 };

// left annotations: 045's three pairs + 6.35 (measured ink tops 405.0/420.7, 454.2/469.9,
// 496.0/512.8) + THIS slide's 4th pair (measured 233.4/250.1, orange)
T.ann.lines = [
  ["Output of Self", 398.7 + 6.35, BLUE], ["Attention", 415.4 + 6.35, BLUE],
  ["Residual", 447.9 + 6.35, ORANGE], ["Connections", 464.7 + 6.35, ORANGE],
  ["Input to Self", 489.8 + 6.35, RED], ["Attention", 505.5 + 6.35, RED],
  ["Residual", 233.4, ORANGE], ["Connections", 250.1, ORANGE],
];

// caption: same string/x as 045's certified underscored caption (ink 273..553 frame on
// BOTH frames), +6.35 in y; highlight band FFB6C1 on this frame (vs 045's yellow)
T.caption.capTop = 524.3 + 6.35;
T.caption.hl.y = 520.1 + 6.35;

// ---- the two (+)/LN units (parent drawNormUnit geometry shape) ----
const D = 6.35;
const uB = { // bottom unit = 045's certified T.unit + D (all three anchors exact)
  container: { x: T.unit.container.x, y: T.unit.container.y + D, w: T.unit.container.w, h: T.unit.container.h },
  grayBar: { x: T.unit.grayBar.x, y: T.unit.grayBar.y + D, w: T.unit.grayBar.w, h: T.unit.grayBar.h },
  plus: { cy: T.unit.plus.cy + D, d: T.unit.plus.d, style: "filled" },
  row: { y: 401.2, h: 17.0 }, // output-of-attention row (measured lav 384..399 frame)
  arrows: {
    red: { y0: T.unit.arrows.red.y0 + D, y1: T.unit.arrows.red.y1 + D },
    green: { y0: T.unit.arrows.green.y0 + D, y1: T.unit.arrows.green.y1 + D },
    navy: { y0: T.unit.arrows.navy.y0 + D, y1: 401.2 },
  },
  curves: { y: T.unit.curves.y + D, h: T.unit.curves.h, dx: T.unit.curves.dx, w: T.unit.curves.w },
};
const uT = { // top unit — THIS frame's own measurements (compressed vs 045's unit)
  container: { x: 128.2, y: 100.5, w: 774.2, h: 72.2 }, // dash rows 96..165 frame
  grayBar: { x: 163.6, y: 106.7, w: 715.0, h: 28.0 },   // bar edges 102..128.5 frame
  plus: { cy: 155.4, d: 15.6, style: "filled" },        // discs 142..155 frame
  row: { y: 180.4, h: 17.0 },                           // post-FFN row (lav 173..188)
  arrows: {
    red: { y0: 84.6, y1: 106.7 },    // bar -> final row (ink 82..101 frame)
    green: { y0: 135.1, y1: 147.6 }, // plus -> bar (ink 128..141 frame)
    navy: { y0: 163.2, y1: 180.4 },  // row -> plus (ink 157..172 frame)
  },
  curves: { y: 149.1, h: 151.3, dx: -52.0, w: 54.0 }, // rise from the post-LN row (spec-resolved origin)
};

// rows drawn outside the units
const ROW_FINAL = { y: 67.3, h: 17.5 };  // lav 65..80 frame
const ROW_POSTLN = { y: 290.3, h: 17.5 }; // lav 278..294 frame

// FFN-gap block arrows (this frame's delta: BLOCK arrows, not 045's thin navy lines)
const BLK_FFN = {
  upIntoPostFFN: { y: 198.8, h: 16.8 },  // FFN -> post-FFN row (ink 192..205 frame)
  upIntoFFN: { y: 276.3, h: 13.5 },      // post-LN row -> FFN box (ink 265..277 frame)
  w: 10.5,
};

// ---- forked strip mechanism: ONLY the subscript array differs from the certified parent
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

// ---- forked (+)/LN unit: identical to the certified parent's drawNormUnit except it
// ---- draws its row through drawStripRow46 (0-based labels; parent module-internal subs)
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

// ---- delta blocks (this frame only) ----

// pink "Final Output" callout (top-left; measured box + text)
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

// block arrows in the two FFN gaps (this frame replaces 045's thin navy lines)
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

// caption: 045's certified text/x shifted +6.35; highlight band PINK on this frame
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

// ---- paint order (045's layering logic; curves under navy/FFN box, rows over curves) ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };
const pptx = pres; // the parent's block functions take the pres instance as `pptx`

const { CHROME } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
function drawBadge46() {
  // The diagram panel on this frame reaches y 52.3 (vs 045's 166.4) and its white fill
  // covers the badge zone; the original capture shows NO badge disc here (curation note:
  // "badge numeral cut off/unreadable at this frame"), but the playlist chrome law is
  // founder-directive and playlist-wide (badge position/size constant; numeral = file id
  // per 002 AGENTS.md) — so the badge is RE-DRAWN above the content from the shared
  // module's constants. Never re-derived: CHROME is the shared pattern's own record.
  const bx = CHROME.badge.cx - CHROME.badge.d / 2;
  const by = CHROME.badge.cy - CHROME.badge.d / 2;
  slide.addShape(pptx.ShapeType.ellipse, {
    x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
    fill: { color: CHROME.badge.fill }, line: { color: CHROME.badge.ring, width: CHROME.badge.ringWidth },
  });
  slide.addText("46", {
    x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
    align: "center", valign: "middle", bold: true,
    fontSize: CHROME.badge.numeralSize, color: CHROME.badge.numeralColor,
    fontFace: CHROME.badge.fontFace, margin: 0,
  });
}

drawHouseChrome(pptx, slide, { numeral: 46 });            // playlist chrome, badge 46
p45.BLOCKS.panel(pptx, slide);                            // blue panel (mutated T.panel)
drawStripRow46(pptx, slide, ROW_FINAL, "Y", ROW_FINAL.y + ROW_FINAL.h / 2, BLUE); // final row
drawNormUnit46(pptx, slide, uT);                          // top unit (+ its post-FFN row)
p45.BLOCKS.ffnbox(pptx, slide);                           // FFN box (mutated T.ffn)
drawBlkFFN(pptx, slide);                                  // FFN-gap block arrows (delta)
drawStripRow46(pptx, slide, ROW_POSTLN, "Y", ROW_POSTLN.y + ROW_POSTLN.h / 2, BLUE); // post-LN row
drawNormUnit46(pptx, slide, uB);                          // bottom unit (+ its outatt row)
p45.BLOCKS.navy(pptx, slide);                             // MHA bar (mutated T.navy)
p45.BLOCKS.blkArrows(pptx, slide);                        // 2 navy-gap block arrows (mutated zones)
drawStripRow46(pptx, slide, T.rows.x, "X", T.rows.x.y + T.rows.x.h / 2, GREEN);      // X row
p45.BLOCKS.ann(pptx, slide);                              // 4 annotation pairs (mutated + new)
drawCallout46(pptx, slide);                               // Final Output callout (delta)
drawCaption46(pptx, slide);                               // caption, pink band (delta)
drawBadge46();                                            // badge above the tall panel (chrome law)

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_046_recreated.pptx" })
  .then(() => console.log("WROTE slide_046_recreated.pptx"));
