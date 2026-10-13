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
// opts: { numeral: 46 (default), chrome: true, skip: [names], only: [names] }
// Block granularity for children: drawStripRow46(pptx, slide, row, letter, dotCy, dotColor),
// drawNormUnit46(pptx, slide, u), drawCallout46, drawBlkFFN, drawCaption46, drawBadge46,
// drawCurveArrow46, uT/uB unit geometry objects, ROW_FINAL/ROW_POSTLN row objects,
// BLK_FFN, SUBS_46, CURVE_KNOTS, BLOCKS, PAINT_ORDER — exported.
//
// FOUNDER-DEFECT FIX 2026-10-12 (attempt 2, qa/slide046/): "the dark orange arrows have
// small twists around the path — the path itself is correct and perfect." The certified
// attempt-1 build drew these arrows from the raster asset s038_orangearrow.png (a PIL
// ImageDraw.line joint="curve" over a Catmull-Rom, m18): the segment joints left small
// twists along every arrow — measured (afix_trace_2.txt): centerline wobble up to 1.0pt,
// 920 centerline direction reversals across the 16 arrows, stroke width ragged 1..13px.
// Fix: each arrow is now ONE custGeom shape — the SAME uniform Catmull-Rom spline the
// asset encoded (m18's measured knots, path unchanged per founder) converted EXACTLY
// (C1-identical) to a chain of cubic Beziers and stroked natively: identical endpoints,
// endpoint tangents, color E36C09, weight 1.33pt, and arrowhead placement (LO triangle
// tailEnd at the same tip/tangent, measured within 0.7pt of the drawn head). Verified
// against the certified render: path agreement <=0.3pt on every visible row
// (scratch/slide046_afix/afix_check_test1.py); post-fix profile flat (afix_trace_3.txt).

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

// ---- orange residual-curve arrows (founder-defect fix 2026-10-12, see header) ----
const ORANGE_ARROW = "E36C09"; // the asset's own orange (m18), unchanged
const ARROW_LW = 1.33;         // asset stroke = 8px @ 6px/pt, unchanged
const H_ASSET_CURVE = 149.0;   // asset canvas height in pt
// Asset-coords knots (pt; canvas origin = (cx-52, unit.curves.y), canvas 54 x 149) —
// the m18 measured path, EXACTLY as the certified build drew it (path unchanged).
const CURVE_KNOTS = [[17.4, 147.1], [8.4, 134.6], [1.0, 110.0], [1.0, 79.0], [1.0, 55.0],
  [7.4, 38.3], [14.7, 21.6], [22.0, 13.2], [29.8, 9.0], [35.6, 4.8], [46.0, 2.2]];

// Exact conversion of the asset's uniform Catmull-Rom (endpoint-duplicated) to cubic
// Beziers: for segment P1->P2 with neighbours P0/P3: B1 = P1 + (P2-P0)/6, B2 = P2-(P3-P1)/6.
// C1-identical to the spline the raster asset sampled — the path is unchanged by law.
function catmullRomToCubic46(K) {
  const pts = [K[0], ...K, K[K.length - 1]];
  const segs = [];
  for (let i = 1; i < pts.length - 2; i++) {
    const p0 = pts[i - 1], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2];
    segs.push({
      p1, p2,
      b1: [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6],
      b2: [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6],
    });
  }
  return segs;
}

const CURVE_POINTS_CACHE = {};
function curveGeom46(hBox) {
  const key = String(hBox);
  if (!CURVE_POINTS_CACHE[key]) {
    const segs = catmullRomToCubic46(CURVE_KNOTS);
    const sy = (y) => (y * hBox) / H_ASSET_CURVE; // uT box stretches the asset by h_box/149
    const pts = [{ x: pt(segs[0].p1[0]), y: pt(sy(segs[0].p1[1])), moveTo: true }];
    for (const s of segs) {
      pts.push({
        x: pt(s.p2[0]), y: pt(sy(s.p2[1])),
        curve: { type: "cubic", x1: pt(s.b1[0]), y1: pt(sy(s.b1[1])), x2: pt(s.b2[0]), y2: pt(sy(s.b2[1])) },
      });
    }
    // Arrowhead — EXACTLY the certified asset's drawn head (m18): tip = path end + 0.8pt,
    // base vertices 5.2pt back along the end tangent at +/-0.45rad (base width 4.52pt).
    // The end tangent comes from the asset's own last polyline samples: px[-1] = appended
    // P10, px[-3] = CR sample t = 22/23 of the final segment (m18 sampled
    // linspace(0,1,24) — t INCLUSIVE of 1 — per segment, then appended the end point).
    // Final CR segment neighbours: p0 = P8, p1 = P9, p2 = p3 = P10 (endpoint duplicated).
    const P = CURVE_KNOTS;
    const seg = { p0: P[P.length - 3], p1: P[P.length - 2], p2: P[P.length - 1], p3: P[P.length - 1] };
    const smp = (t) => {
      const fx_ = 0.5 * (2 * seg.p1[0] + (-seg.p0[0] + seg.p2[0]) * t + (2 * seg.p0[0] - 5 * seg.p1[0] + 4 * seg.p2[0] - seg.p3[0]) * t * t + (-seg.p0[0] + 3 * seg.p1[0] - 3 * seg.p2[0] + seg.p3[0]) * t * t * t);
      const fy_ = 0.5 * (2 * seg.p1[1] + (-seg.p0[1] + seg.p2[1]) * t + (2 * seg.p0[1] - 5 * seg.p1[1] + 4 * seg.p2[1] - seg.p3[1]) * t * t + (-seg.p0[1] + 3 * seg.p1[1] - 3 * seg.p2[1] + seg.p3[1]) * t * t * t);
      return [fx_, fy_];
    };
    const s3 = smp(22 / 23);           // px[-3] of the asset's smoothed polyline
    const s1 = P[P.length - 1];        // px[-1] = appended path end (46.0, 2.2)
    const ang = Math.atan2(s1[1] - s3[1], s1[0] - s3[0]);
    const tip = [s1[0] + 0.8, s1[1]];
    const b1 = [tip[0] - 5.2 * Math.cos(ang - 0.45), tip[1] - 5.2 * Math.sin(ang - 0.45)];
    const b2 = [tip[0] - 5.2 * Math.cos(ang + 0.45), tip[1] - 5.2 * Math.sin(ang + 0.45)];
    const head = [
      { x: pt(tip[0]), y: pt(sy(tip[1])) },
      { x: pt(b1[0]), y: pt(sy(b1[1])) },
      { x: pt(b2[0]), y: pt(sy(b2[1])) },
      { close: true },
    ];
    CURVE_POINTS_CACHE[key] = { stroke: pts, head };
  }
  return CURVE_POINTS_CACHE[key];
}

// ONE perfectly smooth stroke per arrow (founder directive 2026-10-12): a single custGeom
// shape — native cubic-bezier chain, solid E36C09 stroke — plus the arrowhead drawn with
// the certified asset's EXACT head geometry (filled custGeom triangle). The built-in
// `triangle` tailEnd was measured (600dpi) ~1.25x the certified head (base 5.4pt vs
// 4.2pt) — a new deviation from the original the founder did not ask for; the drawn head
// keeps the certified pixels. Draw-order position unchanged (still painted inside
// drawNormUnit46, before ffnbox/navy cover the mid-section).
function drawCurveArrow46(pptx, slide, cx, u) {
  const g = curveGeom46(u.curves.h);
  slide.addShape("custGeom", {
    x: pt(cx + u.curves.dx), y: pt(u.curves.y), w: pt(u.curves.w), h: pt(u.curves.h),
    points: g.stroke,
    line: { color: ORANGE_ARROW, width: ARROW_LW },
    fill: { type: "none" },
  });
  slide.addShape("custGeom", {
    x: pt(cx + u.curves.dx), y: pt(u.curves.y), w: pt(u.curves.w), h: pt(u.curves.h),
    points: g.head,
    fill: { color: ORANGE_ARROW },
    line: { type: "none" },
  });
}

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
    drawCurveArrow46(pptx, slide, cx, u);
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
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  for (const name of PAINT_ORDER) {
    if (only ? !only.has(name) : skip.has(name)) continue;
    BLOCKS[name](pptx, slide);
  }
  if (numeral !== null) drawBadge46(pptx, slide, numeral);
}

const BLOCKS = {
  panel: (pptx, slide) => p45.BLOCKS.panel(pptx, slide),
  finalRow: (pptx, slide) => drawStripRow46(pptx, slide, ROW_FINAL, "Y", ROW_FINAL.y + ROW_FINAL.h / 2, BLUE),
  topUnit: (pptx, slide) => drawNormUnit46(pptx, slide, uT),
  ffnbox: (pptx, slide) => p45.BLOCKS.ffnbox(pptx, slide),
  blkFFN: drawBlkFFN,
  postLnRow: (pptx, slide) => drawStripRow46(pptx, slide, ROW_POSTLN, "Y", ROW_POSTLN.y + ROW_POSTLN.h / 2, BLUE),
  bottomUnit: (pptx, slide) => drawNormUnit46(pptx, slide, uB),
  navy: (pptx, slide) => p45.BLOCKS.navy(pptx, slide),
  blkArrows: (pptx, slide) => p45.BLOCKS.blkArrows(pptx, slide),
  xRow: (pptx, slide) => drawStripRow46(pptx, slide, T.rows.x, "X", T.rows.x.y + T.rows.x.h / 2, GREEN),
  ann: (pptx, slide) => p45.BLOCKS.ann(pptx, slide),
  callout: drawCallout46,
  caption: drawCaption46,
};

// Paint order = the certified composition order (z-order matters: ffnbox covers the
// topUnit curves' mid-section, navy covers the bottomUnit curves' mid-section).
const PAINT_ORDER = ["panel", "finalRow", "topUnit", "ffnbox", "blkFFN", "postLnRow",
  "bottomUnit", "navy", "blkArrows", "xRow", "ann", "callout", "caption"];

module.exports = { renderBase, drawStripRow46, drawNormUnit46, drawCallout46, drawBlkFFN,
  drawCaption46, drawBadge46, drawCurveArrow46, uT, uB, ROW_FINAL, ROW_POSTLN, BLK_FFN,
  SUBS_46, CURVE_KNOTS, T, BLOCKS, PAINT_ORDER };
