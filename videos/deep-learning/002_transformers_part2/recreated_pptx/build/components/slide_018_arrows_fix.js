// components/slide_018_arrows_fix.js — FOUNDER-DIRECTED ARROW-ATTACHMENT FIX for
// 002_transformers_part2 slide 005 (defect report 2026-10-12: "the arrows between
// components are not good, and are not attaching items, and need fixes").
//
// COPY-THEN-MODIFY law: the certified 001:18 component is REQUIRED untouched and
// called with skip:{connect_h, connect_tan, h_annot, dash_d1, dash_d2, dash_d3};
// this module redraws ONLY those six connector blocks at geometry PIL-measured on
// THIS slide's ground-truth frame (unique_slides/slide_005.jpg, 960x540). The
// certified component and every other slide composing on it are untouched.
//
// ATTEMPT 5 (2026-10-12, resumed after a provider storm killed the attempt-4
// worker mid-adjudication): attempt-4 crop legs d1end + hassembly FAILed; pixel
// adjudication (m34/m36/m37/m38, banked) refuted the d1 "bent" claim (dash slope
// constant 0.83-0.86 in BOTH images; the flagged verticals are certified bypass
// content present in both) and decoded the h-assembly's true original topology:
//  - connect_h's leader line TERMINATES IN the arrowhead's base ((494,342.5)
//    frame) — attempt 4 ended at (490.7,337.6), 4-5 px short = detached;
//  - two gray leader elbows feed the assembly: LEADER A horizontal (328..483,
//    y330.5) + vertical (x483.5, y331..351) — attempt 4 had only the vertical,
//    merged into the black h_annot; LEADER B horizontal (323..477.5, y336.5)
//    terminating on the certified shadow box's right border (x477.9, which also
//    supplies B's vertical y338..360 within 1 px);
//  - the black hook merges with the rect's right-border ink at (474.5,369.5).
// Fixes applied: leader line extended into the head base, leaders A/B added,
// hook re-anchored to end ON the border. d1/d2/d3/connect_tan UNCHANGED
// (d1/d2 attachment re-verified by m34/m36; corridor already PASSed attempt 4).
//
// FRAME->BUILD MAPPING (certified, build header of slide_005.js):
//   frame_x = 18.0787 + 0.961084*build_x ; frame_y = 0.4700 + 0.957187*build_y
// All geometry below is frame-measured then converted; measured scripts banked in
// scratch/slide005_fix/ (m13..m27). Attachment rule: an arrow "attaches" when its
// endpoint lands on the target component's border ink (<=2-3 frame px).
//
// MEASURED DEFECTS FIXED (before -> after, build pt):
//  1. connect_h pink upper segment [[481,146]->[488,246]]: SPURIOUS — the original
//     has NO stroke from banner1's bottom (corridor x440-520, y144-236 empty at
//     lum<248; m15/m14). DELETED.
//  2. connect_h gray interior line [[486,246],[490,300],[493,350]]: measured faint
//     stroke runs (482,242)->(492,316)->(492,338) frame (drifting RIGHT-down), i.e.
//     build (481.9,252)->(492.2,352), starting at the border junction where
//     connect_tan lands. REDRAWN [[481,248],[487,295],[492,352]].
//  3. connect_tan [[417,182],[445,212],[470,238]]: ended 9-10 pt SHORT of the MHA
//     inset top border in empty space. Measured original: leaves banner2's right
//     border horizontally at frame (418,174) (build 416.5,181.2), curves down
//     steepening (frame slope 0.14 -> 0.56 -> 0.90 -> 1.3 -> 2.3), and ATTACHES to
//     the inset top border at frame (480.5,237.5) = build (480.9,247.3). REDRAWN as
//     a 5-segment curve ending ON the border.
//  4. h circle (484.5,357.5,d19): measured tan circle center frame (493,362.75),
//     d~21.5-22 frame px = build center (493.4,378.6) d22 — the certified build drew
//     it 11 pt too HIGH and 3 pt too SMALL (cross-checked on 001:18's sharp frame:
//     circle center (493,377) d22 there). REDRAWN x482.4 y367.6 d22.
//  5. ghost circle: moved with the circle keeping the certified offset (+4,-4).
//  6. tan arrowhead (489.5,347,7,8) tip (493,355): floated ~10 pt above the circle.
//     Measured head: dark-brown 653716 triangle, base frame y342.5 x490.9-496.1,
//     tip (492.5,350.5) TOUCHING the circle top edge (352). REDRAWN x491.2 y356.7
//     w5.4 h9.6 flipV — tip at (493.9,366.3) vs circle top 367.6 (1.3 pt = the
//     original's own gap).
//  7. h_annot black curve [[477,389],[480,381],[483,374],[486,368]]: lower end
//     floated 2 pt right of the red rect's edge and 8 pt below the measured
//     attachment. Measured: washed-gray upper part frame (483.5,328-351), dark bend
//     (485,352), hook left-down to the red rect's right edge (frame 474.7) at
//     (475-477,364-371), tail down to (476,371). REDRAWN polyline ending ON the
//     rect's right-border ink.
//  8. dash_d1 [[505,245],[576,300],[648,368]]: WRONG SHAPE (bent at 576,300 vs the
//     original's ONE STRAIGHT line, frame dash LSQ slope 0.828 through
//     (519,254)->(643,356.7)) and start/end off. Measured: starts at the MHA inset
//     right edge (frame 506.5, y243.7 extended; first faint ink (511,248)), runs
//     straight (under band (b) from build x~633 — the original's dashes continue
//     under the band: dark-red-orange traces (629-638,344-356) frame) and ATTACHES
//     to the encoder MHA box left border at frame (643,356.7) = build (650,372.4)
//     (cross-checked band-free on 001:18: dashes (637,359),(640,362),(641,363),
//     (644,366) reach the box). REDRAWN [[508,254],[650,372]] single dashed.
//  9. dash_d2 [[191,272],[270,345],[294,356]]: WRONG SHAPE (bent) and ended 10 pt
//     short of the red rectangle. Measured: ONE STRAIGHT dashed line, frame slope
//     0.846 through (205,270), faint dashes continuing (264,320)...(305,357) to the
//     red rect's left border (frame x311) at (311,359.7) = build (304.8,375.5).
//     REDRAWN [[189.5,277.5],[304.8,375.5]] — starts ON the SDPA inset right edge
//     (frame 199.8, y265.8 extended), ends ON the red rect's left border ink.
// 10. dash_d3 [[193,487],[238,433]]: WRONG SLOPE (-1.20 vs measured -0.957) and
//     extent. Measured dashes (259,410),(255,414),(244,423),(241,427),(216,451),
//     (212,455),(208,458): straight, extending to the SDPA inset right edge at
//     (199.8,466.7) = build (189.1,487.2). REDRAWN [[251,428],[189,487]].
//
// Untouched (certified, m8-verified against this frame): all 017 architecture
// arrows, both insets' internal flow arrows, enc/dec MHA boxes, banners, chrome.

const parent = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_018.js");

const px = parent.px;
const C = parent.C; // certified palette (pinkConn C47070, grayLine A6A6A6,
                    // tanArrow 653716, red C00000, black 333333)

// ---- corrected connector blocks (measured on unique_slides/slide_005.jpg) -------

function addLines(slide, color, width, pts, opts = {}) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i];
    const [x1, y1] = pts[i + 1];
    const line = { color, width };
    if (opts.dash) line.dashType = opts.dash;
    slide.addShape("line", {
      x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
      w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
      flipV: y1 < y0, flipH: x1 < x0,
      line,
    });
  }
}

function drawConnectH(slide) {
  // leader line INTO the arrowhead's base (m13/m15/m38: the original's line runs
  // (482,242)->(492,316)->(494,342.5) frame and TERMINATES in the head's base —
  // the head is this leader's terminal arrowhead; attempt 4 ended 4-5 px short
  // of the head = the founder's "not attaching").  Build pts: frame (482,242)
  // -> (482.9,252.6); (492,316) -> (492.3,329.4); (494,342.5) -> (494.4,357.4),
  // which lands INSIDE the head base (head spans x491.2-496.6 from y356.7).
  addLines(slide, C.grayLine, 0.75, [[482.9, 252.6], [492.3, 329.4], [494.4, 357.4]]);
  // LEADER A (m38/m15-measured gray elbow, missing from attempts 1-4): from the
  // shadow box's top-left fade-in (frame 328,330.5) horizontally right to the
  // elbow (483,330.5), then down along the circle's upper-left to (483.5,351)
  // where the black hook takes over.  Build: (322.5,344.9)->(483.5,344.9)->
  // (483.8,366.3).
  addLines(slide, C.grayLine, 0.75, [[322.5, 344.9], [483.5, 344.9], [483.8, 366.3]]);
  // LEADER B (m38-measured second parallel elbow): frame (323,336.5)->(477.5,336.5)
  // horizontal, terminating ON the shadow box's right border ink (x477.9, already
  // rendered by the certified stack, which also supplies this leader's vertical
  // y338-360 — measured to coincide within 1 px).  Build: (317.1,351.7)->(477.7,351.7).
  addLines(slide, C.grayLine, 0.75, [[317.1, 351.7], [477.7, 351.7]]);
  // tan arrowhead pointing DOWN, tip touching the h circle's top edge
  // (measured base frame y342.5 x490.9-496.1, tip (492.5,350.5))
  slide.addShape("triangle", {
    x: px(491.2), y: px(356.7), w: px(5.4), h: px(9.6), flipV: true,
    fill: { color: C.tanArrow }, line: { color: C.tanArrow, width: 0.5 },
  });
}

function drawConnectTan(slide) {
  // banner2 right border -> horizontal stub -> steepening curve -> ATTACHES to the
  // MHA inset top border at build (480.9,247.3)  [frame (480.5,237.5)]
  addLines(slide, C.pinkConn, 0.75, [
    [415, 181], [433, 184], [454, 196], [470, 217], [477, 232], [481, 247],
  ]);
}

function drawHAnnot(slide) {
  // gray ghost circle: certified offset (+4,-4) from the corrected circle
  slide.addShape("ellipse", {
    x: px(486.4), y: px(363.6), w: px(19), h: px(19),
    fill: { type: "none" }, line: { color: C.grayLine, width: 0.75 },
  });
  // h circle at the MEASURED position/size (frame center (493,362.75) d~22)
  slide.addShape("ellipse", {
    x: px(482.4), y: px(367.6), w: px(22), h: px(22),
    fill: { color: "D4BCA0" }, line: { color: "8A6A48", width: 1 },
  });
  slide.addText("h", {
    x: px(482.4), y: px(367.6), w: px(22), h: px(22),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 10, bold: true, italic: true, color: C.black,
  });
  // black hook: CONTINUES leader A's vertical end (build 483.8,366.3) down-left
  // to the red rect's right border (m18/m36 measured: frame (485,348)->(477,361)
  // ->(476,366)->(474.5,369.5), merging with the border ink at its bottom-right
  // corner region).  Build: (483.8,366.3)->(477.8,375.6)->(476.8,381.8)->
  // (474.9,385.0); the last point sits ON the rect's right-border ink (frame
  // 474.5,369.5 vs border x474.8) — attached.
  addLines(slide, C.black, 0.75, [
    [483.8, 366.3], [477.8, 375.6], [476.8, 381.8], [474.9, 385.0],
  ]);
}

function drawDashD1(slide) {
  // ONE STRAIGHT dashed line: MHA inset right edge (508,254) -> encoder MHA box
  // left border (650,372) — attached at BOTH ends (frame slope 0.828 measured)
  addLines(slide, C.red, 1, [[508, 254], [650, 372]], { dash: "dash" });
}

function drawDashD2(slide) {
  // ONE STRAIGHT dashed line: SDPA inset right edge (189.5,277.5) -> red rectangle
  // left border (304.8,375.5) — attached at BOTH ends (frame slope 0.846 measured)
  addLines(slide, C.red, 1, [[189.5, 277.5], [304.8, 375.5]], { dash: "dash" });
}

function drawDashD3(slide) {
  // dashed fragment: measured straight slope -0.957, upper end as in the frame
  // (floating), lower end ON the SDPA inset right edge near its bottom corner
  addLines(slide, C.red, 1, [[251, 428], [189, 487]], { dash: "dash" });
}

const SKIPPED = ["connect_h", "connect_tan", "h_annot", "dash_d1", "dash_d2", "dash_d3"];

/**
 * Draw the full slide-018 composition with THIS slide's corrected connectors:
 * certified component renderBase (arrow blocks skipped) + measured redraw.
 * @param {object} pptx  pptxgenjs instance
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { numeral, ...passthrough to the certified renderBase }
 */
function renderBase(pptx, slide, opts = {}) {
  parent.renderBase(pptx, slide, { ...opts, skip: SKIPPED });
  drawConnectTan(slide);
  drawConnectH(slide);
  drawHAnnot(slide);
  drawDashD1(slide);
  drawDashD2(slide);
  drawDashD3(slide);
}

module.exports = { renderBase, SKIPPED, px, C };
