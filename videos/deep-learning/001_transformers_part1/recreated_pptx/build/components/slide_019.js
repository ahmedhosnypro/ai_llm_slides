// components/slide_019.js — slide 019 composition. CHILD of slide 018 (certified,
// frozen): requires ./slide_018.js and calls its renderBase, skipping 018's banner
// blocks and their connectors (banner1, banner2, connect_h, connect_tan). NEVER
// re-derives or copies parent geometry — the three paper-figure insets, the h
// annotation, the dashed zoom lines, the MHA overlay boxes, the fig handles, the
// yellow band, the title and the whole right-side Figure-1 architecture come from
// the parent component untouched.
//
// BANK CONTRACT (founder directive 2026-10-11): lecture 002's slides 19 and 37
// reference 001:19 — this module exports renderBase(pptx, slide, opts) at block
// granularity with opts.skip / opts.only; opts.numeral overrides the badge (badge
// numeral = the number printed on the CALLER's original frame; default 19). House
// chrome is drawn ONCE by the 017 component in the parent chain — never redraw it.
//
// CERTIFIED as the judge-PASS composition of 2026-10-12 (qa/slide019/judge_attempt_1.txt,
// FINAL VERDICT PASS on render_4.png; visual_check=PASS, gen_status=passed in the DB).
// Z-ORDER LAW (part of the certified composition): the container repaint patches
// (enc_repaint, dec_repaint) are drawn FIRST — they emulate the container FILL, and
// in the original frame the leader lines/arrowheads sit ON TOP of that fill (drawing
// enc_repaint after leader4 buried its arrowhead: 0 dark px vs orig 18, render_3
// evidence; qa/slide019/render_3.png kept as the demonstration).
//
// SLIDE 019 DELTA (PIL-measured on unique_slides/slide_019.jpg, 960x540, 1px=1pt,
// in = px/72; scans in scratch/slide019/m0..m14 + probe_callouts/probe_enc through
// the gate; 017↔019 and 018↔019 frame diffs localize every change):
//   legend1/2/3    three color-callout boxes replacing the banners:
//                  'Normalization Layer'  x141 y102 w201 h28 (fill C8FCFC, text 00008B)
//                  'Feed Forward Layer'   x311 y143 w203 h28 (fill 9CA0A0, text 000000)
//                  'Residual Connections' x264 y181 w201 h28 (fill DCFCC0, text 2F8C14)
//   leader1..5     thin light hairlines from the callouts into the figure:
//                  L1/L2 from box1 (to Softmax / Linear box left edges),
//                  L3 from box2 (flat run over the encoder panel top),
//                  L4 from box2 (steep dive to the encoder Feed Forward box),
//                  L5 from box3 (steep dive to the 'N x' circle)
//   enc_repaint    tan patch over 017's encoder sub-stack interior (x631-725,
//                  y268-370 over d1's tail) — 019 recolors/re-layouts every
//                  compartment content there
//   enc_addn_top   STEEL-BLUE 'Add & Norm' box x653-720 y273-287.5 (fill 6D99B4)
//   enc_ff         DARK-GRAY 'Feed Forward' box x651-720 y288-316 (fill 807560)
//   enc_addn_bot   STEEL-BLUE 'Add & Norm' box x656-720 y343.5-353.5 (fill 6C99B4)
//   enc_green      thick bright-green residual bus x637 y277-405 + stubs into both
//                  Add & Norm boxes (arrowheads) + pickups y329/y402 to x686
//   enc_vcircle    V circle under encoder MHA recolored GREEN (663.5,400.5) d12
//   dec_repaint    olive patches over 017's decoder container texts/separators
//                  (y203-220, y221-265, y265-277; x746-839)
//   dec_addn_top   STEEL-BLUE 'Add & Norm' x753-817 y206.5-218.5 (fill 5C9CB7)
//   dec_ff         DARK-GRAY 'Feed Forward' x753-817 y223.5-250 (fill 6E7E62)
//   dec_addn_mid   STEEL-BLUE 'Add & Norm' x753-817 y265.5-274.5 (fill 5C9CB6)
//   dec_low        017's purple block KEPT below y347 (masked text/separators
//                  identical 017/019 — measured); its top compartment becomes:
//                  panel-green margin x746-753, khaki margin x817-832, and an
//                  INDIGO 'Add & Norm' box x753-817 y329.5-343.5 (fill 6E87E0)
//   dec_green      thick bright-green trunk x834 y210-404 + horizontal connectors
//                  y212/y258/y272/y320/y338/y402 (measured bands x788/791-838)
//
// Laws honored: house chrome via the parent chain (drawn ONCE by 017's component,
// numeral overridden to 19); verbatim text; margin:0 + explicit fontFace everywhere;
// explicit lineSpacing on the two-line FF boxes; no '#' in hex; PIL-measured geometry.

const parent = require("./slide_018.js");

const px = parent.px;

// ---- slide-019 palette (JPEG-core measured, scratch/slide019/m7/m14) -----------
const C = {
  tanContainer: "C8A888",     // 017 encoder container fill (204,172,136) — patch color
  oliveContainer: "B0B070",   // 017 decoder container fill (176,176,112) — patch color
  panelGreen: "C8F8E0",       // decoder panel (204,236,221) — low-left margin patch
  khaki: "B5BB97",            // (181,187,151) low-right margin patch
  legend1Fill: "C8FCFC",      // (200,252,252)
  legend1Border: "8FA6BE",    // (169,187,207) smear
  legend1Text: "00008B",      // darkest (0,0,87)
  legend2Fill: "9CA0A0",      // (156,160,160)
  legend2Border: "8E9296",    // (146,149,154)
  legend2Text: "000000",
  legend3Fill: "DCFCC0",      // (220,252,192)
  legend3Border: "A9CC98",    // soft green edge (197,235,186)
  legend3Text: "2F8C14",      // text mode (44,132,28)
  // F7 fix (founder defect batch 2026-10-13): the 5 legend leader hairlines were the
  // certification-era JPEG-core colors (L1/L2 leaderBlue B7CDE0, L3/L4/L5 leaderGray
  // C9CDC9) at 0.75pt — same faint-arrow class as 016/017/018. Family value adopted
  // per the F5-certified 017 fix and VERIFIED on this frame (cores (165,163,184)/
  // (194,195,193)/(195,205,200), path medians (192..204,195..206,185..204); all within
  // the family band C8C8C8..D3D3D3 under JPEG smear): single neutral #C8C8C8 at 2.25pt.
  // Geometry + the L3/L4 black heads (frame-measured 742-746/234-238, 644-648/301-305,
  // color core (17,0,0)=near-black warm) are unchanged — see scratch/slide019/
  // ARROW_COLOR.txt, b01/b02/b03, m16.
  leader: "C8C8C8",           // L1..L5 family faint-leader gray (200,200,200)
  steelFill: "6D99B4",        // encoder Add&Norm boxes (109,153,180)
  steelFillDec: "5C9CB7",     // decoder Add&Norm boxes (92,156,183)
  steelBorder: "2F6476",      // (47,100,118)
  steelText: "1B3A5C",
  indigoFill: "6E87E0",       // decoder low Add&Norm (110,135,224)
  indigoBorder: "3A5697",     // (58,86,151)
  indigoText: "2E3E8C",
  ffFillEnc: "807560",        // (128,117,96)
  ffFillDec: "6E7E62",        // (110,126,98)
  ffBorder: "3E3A28",
  ffTextEnc: "55482E",
  ffTextDec: "3A4A2C",
  green: "7FB421",            // residual bus core (141,203,44)/(116,176,18)
  greenBright: "8CC62E",      // trunk/band core (155,203,94)/(156,224,75)
  redMha: "C00000",           // solid decoder-MHA border (165,40,38)/(153,0,2)
  vGreen: "55A044",           // encoder V circle (80,145,43)
  ink: "333333",
};
const SANS = "Arial";

// ---- helpers --------------------------------------------------------------------

function addLines(slide, color, width, pts, opts = {}) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i];
    const [x1, y1] = pts[i + 1];
    const line = { color, width };
    slide.addShape("line", {
      x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
      w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
      flipV: y1 < y0, flipH: x1 < x0,
      line,
    });
  }
}

function rect(slide, x, y, w, h, fill, border, borderWidth) {
  slide.addShape("rect", {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill }, line: { color: border, width: borderWidth },
  });
}

function centerText(slide, x, y, w, h, lines, fontSize, color, lineSpacing) {
  const items = lines.map((t, i) => ({ text: t, options: { breakLine: i < lines.length - 1 } }));
  slide.addText(items, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize, bold: true, color,
    lineSpacing,
  });
}

function arrowHeadRight(slide, cx, cy, color) {
  slide.addShape("triangle", {
    x: px(cx - 2.5), y: px(cy - 3), w: px(6), h: px(6), rotate: 90,
    fill: { color }, line: { color, width: 0.5 },
  });
}

function arrowHeadLeft(slide, cx, cy, color) {
  slide.addShape("triangle", {
    x: px(cx - 2.5), y: px(cy - 3), w: px(6), h: px(6), rotate: 270,
    fill: { color }, line: { color, width: 0.5 },
  });
}

function chevronUp(slide, cx, cy, color, w = 6, h = 4.5) {
  slide.addShape("triangle", {
    x: px(cx - w / 2), y: px(cy - h / 2), w: px(w), h: px(h),
    fill: { color }, line: { color, width: 0.5 },
  });
}

// ---- delta blocks (z-order = call order in renderBase) --------------------------

function drawLegend1(pptx, slide) {
  rect(slide, 141, 102, 201, 28, C.legend1Fill, C.legend1Border, 1);
  centerText(slide, 141, 102, 201, 28, ["Normalization Layer"], 15, C.legend1Text);
}

function drawLegend2(pptx, slide) {
  rect(slide, 311, 143, 203, 28, C.legend2Fill, C.legend2Border, 1);
  centerText(slide, 311, 143, 203, 28, ["Feed Forward Layer"], 15, C.legend2Text);
}

function drawLegend3(pptx, slide) {
  rect(slide, 264, 181, 201, 28, C.legend3Fill, C.legend3Border, 1);
  centerText(slide, 264, 181, 201, 28, ["Residual Connections"], 15, C.legend3Text);
}

function drawLeader1(pptx, slide) {
  // box1 -> Softmax box left edge (light hairline, shallow then descending)
  addLines(slide, C.leader, 2.25, [
    [342, 118], [470, 120], [570, 124], [622, 138], [680, 147], [726, 152], [751, 161],
  ]);
}

function drawLeader2(pptx, slide) {
  // box1 (second hairline, appears x~464) -> Linear box left edge
  addLines(slide, C.leader, 2.25, [
    [464, 122], [538, 134], [570, 143], [622, 167], [700, 172], [726, 173], [740, 181], [751, 186],
  ]);
}

function drawLeader3(pptx, slide) {
  // box2 -> shallow line flattening over the encoder panel top, ending in a BLACK
  // arrowhead into the decoder Feed Forward box (measured (742-746, y234-238), m16)
  addLines(slide, C.leader, 2.25, [
    [514, 157], [570, 161], [622, 183], [654, 193], [676, 224], [700, 231], [738, 236],
  ]);
  arrowHeadRight(slide, 743, 236, "1A1000");
}

function drawLeader4(pptx, slide) {
  // box2 -> steep dive ending in a BLACK arrowhead into the encoder Feed Forward
  // box (measured (644-648, y301-305), m16)
  addLines(slide, C.leader, 2.25, [
    [513, 152], [538, 161], [562, 176], [578, 206], [594, 264], [610, 290], [622, 296], [638, 301],
  ]);
  arrowHeadRight(slide, 645, 303, "1A1000");
}

function drawLeader5(pptx, slide) {
  // box3 -> steep dive to the 'N x' circle left edge
  addLines(slide, C.leader, 2.25, [
    [460, 195], [506, 201], [526, 210], [538, 225], [550, 251], [562, 296], [570, 318], [584, 330], [597, 337],
  ]);
}

function drawEncRepaint(pptx, slide) {
  // tan patch over 017's encoder sub-stack interior (texts, FF inset, residual
  // verticals, separators, sub-arrows). Two rects: the main interior (stops at the
  // salmon MHA box, y353) + a narrow left strip over d1's tail (019's frame shows
  // only the last dash fragment at x644-649 — measured m15) — the salmon box
  // (x650-722) itself is inherited untouched.
  slide.addShape("rect", {
    x: px(631), y: px(268), w: px(94), h: px(85),
    fill: { color: C.tanContainer }, line: { color: C.tanContainer, width: 0.25 },
  });
  slide.addShape("rect", {
    x: px(631), y: px(348), w: px(18), h: px(22),
    fill: { color: C.tanContainer }, line: { color: C.tanContainer, width: 0.25 },
  });
}

function drawEncAddnTop(pptx, slide) {
  rect(slide, 653, 273, 67, 14.5, C.steelFill, C.steelBorder, 1);
  centerText(slide, 653, 273, 67, 14.5, ["Add & Norm"], 9, "477493");
}

function drawEncFf(pptx, slide) {
  rect(slide, 653, 288, 67, 27, C.ffFillEnc, C.ffBorder, 0.75);
  centerText(slide, 653, 288, 67, 27, ["Feed", "Forward"], 9, C.ffTextEnc, 10.5);
}

function drawEncAddnBot(pptx, slide) {
  rect(slide, 656, 343.5, 64, 10, C.steelFill, C.steelBorder, 1);
  centerText(slide, 656, 343.5, 64, 10, ["Add & Norm"], 8, "477493");
}

function drawEncGreen(pptx, slide) {
  // residual bus + stubs into the two Add & Norm boxes + pickups (measured);
  // green arrowheads: right-pointing at the stub ends, left-pointing at the wide
  // pickup left-ends (measured widenings x634-647, m6/m16)
  addLines(slide, C.green, 3, [[637, 277], [637, 405]]);
  addLines(slide, C.green, 3, [[637, 281], [647, 281]]);
  arrowHeadRight(slide, 650, 281, C.green);
  addLines(slide, C.green, 3, [[637, 350], [647, 350]]);
  arrowHeadRight(slide, 650, 350, C.green);
  addLines(slide, C.green, 3, [[645, 329], [686, 329]]);
  arrowHeadLeft(slide, 642, 329, C.green);
  addLines(slide, C.green, 3, [[645, 402], [687, 402]]);
  arrowHeadLeft(slide, 642, 402, C.green);
}

function drawEncVCircle(pptx, slide) {
  // V circle under the encoder MHA recolored GREEN (K blue / Q red inherited)
  slide.addShape("ellipse", {
    x: px(657.5), y: px(394.5), w: px(12), h: px(12),
    fill: { color: C.vGreen }, line: { color: C.vGreen, width: 0.5 },
  });
  slide.addText("V", {
    x: px(657.5), y: px(394.5), w: px(12), h: px(12),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 7, bold: true, color: "FFFFFF",
  });
}

function drawDecRepaint(pptx, slide) {
  // olive patches over 017's decoder container texts/separators (y203-277)
  slide.addShape("rect", {
    x: px(746), y: px(203), w: px(93), h: px(17),
    fill: { color: C.oliveContainer }, line: { color: C.oliveContainer, width: 0.25 },
  });
  slide.addShape("rect", {
    x: px(746), y: px(221), w: px(93), h: px(44),
    fill: { color: C.oliveContainer }, line: { color: C.oliveContainer, width: 0.25 },
  });
  slide.addShape("rect", {
    x: px(746), y: px(265), w: px(93), h: px(12),
    fill: { color: C.oliveContainer }, line: { color: C.oliveContainer, width: 0.25 },
  });
}

function drawDecAddnTop(pptx, slide) {
  rect(slide, 753, 206.5, 64, 12.5, C.steelFillDec, C.steelBorder, 1);
  centerText(slide, 753, 206.5, 64, 12.5, ["Add & Norm"], 8, "327389");
}

function drawDecFf(pptx, slide) {
  rect(slide, 753, 223.5, 64, 26.5, C.ffFillDec, C.ffBorder, 0.75);
  centerText(slide, 753, 223.5, 64, 26.5, ["Feed", "Forward"], 8.5, C.ffTextDec, 10);
}

function drawDecAddnMid(pptx, slide) {
  rect(slide, 753, 263.5, 64, 11, C.steelFillDec, C.steelBorder, 1);
  centerText(slide, 753, 263.5, 64, 11, ["Add & Norm"], 7.5, "327389");
}

function drawDecLow(pptx, slide) {
  // 017's purple block stays below y347 (masked text/separators identical);
  // its top compartment is rebuilt: panel-green margin, khaki margin, indigo box
  rect(slide, 746, 326, 7, 22, C.panelGreen, C.panelGreen, 0.25);
  rect(slide, 817, 326, 15, 22, C.khaki, C.khaki, 0.25);
  rect(slide, 753, 329.5, 64, 14, C.indigoFill, C.indigoBorder, 1);
  centerText(slide, 753, 329.5, 64, 14, ["Add & Norm"], 8, "4863BE");
}

function drawDecGreen(pptx, slide) {
  // bright green trunk + horizontal connectors (measured bands) + navy flow
  // chevrons between the decoder layers (measured x781-786 / x767-777, m16/m18)
  addLines(slide, C.greenBright, 4, [[834, 210], [834, 404]]);
  addLines(slide, C.greenBright, 3, [[820, 212], [834, 212]]);
  addLines(slide, C.greenBright, 3.5, [[789, 258], [835, 258]]);
  addLines(slide, C.greenBright, 3, [[819, 272], [834, 272]]);
  addLines(slide, C.greenBright, 3.5, [[788, 320], [835, 320]]);
  addLines(slide, C.greenBright, 3, [[819, 338], [834, 338]]);
  addLines(slide, C.greenBright, 3.5, [[791, 402], [835, 402]]);
  const navy = "05008F";
  chevronUp(slide, 783.5, 197, navy);
  chevronUp(slide, 783.5, 202, navy);
  chevronUp(slide, 783.5, 255.5, navy);
  chevronUp(slide, 783.5, 259.5, navy);
  chevronUp(slide, 772, 313, navy);
  chevronUp(slide, 772, 318, navy);
}

function drawDecMhaSolidBorder(pptx, slide) {
  // 019's frame shows the decoder Multi-Head Attention border SOLID thick red on
  // top/bottom/right (duty 70/70, 28/28; NO left border — m17) while the inherited
  // 018 draw renders dashed with gaps. Over-draw solid; leave the left edge bare.
  addLines(slide, C.redMha, 2.25, [[748, 277], [821, 277]]);
  addLines(slide, C.redMha, 2.25, [[748, 309.5], [821, 309.5]]);
  addLines(slide, C.redMha, 2.25, [[820.5, 277], [820.5, 310]]);
}

// ---- composition ----------------------------------------------------------------

const PARENT_SKIP = ["banner1", "banner2", "connect_h", "connect_tan"];

const DELTA_BLOCKS = {
  // Z-ORDER LAW (resume self-check 2026-10-12, render_3 evidence): the repaint
  // patches emulate the container FILL, and in the original frame the leader
  // lines/arrowheads sit ON TOP of that fill — so repaints must precede every
  // leader block (leader4's head at x642-648 y300-306 is inside the enc patch;
  // drawing enc_repaint after it buried the head: 0 dark px vs orig 18).
  enc_repaint: drawEncRepaint,
  dec_repaint: drawDecRepaint,
  legend1: drawLegend1,
  legend2: drawLegend2,
  legend3: drawLegend3,
  leader1: drawLeader1,
  leader2: drawLeader2,
  leader3: drawLeader3,
  leader4: drawLeader4,
  leader5: drawLeader5,
  enc_addn_top: drawEncAddnTop,
  enc_ff: drawEncFf,
  enc_addn_bot: drawEncAddnBot,
  enc_green: drawEncGreen,
  enc_vcircle: drawEncVCircle,
  dec_repaint: drawDecRepaint,
  dec_addn_top: drawDecAddnTop,
  dec_ff: drawDecFf,
  dec_addn_mid: drawDecAddnMid,
  dec_low: drawDecLow,
  dec_green: drawDecGreen,
  dec_mha_solid_border: drawDecMhaSolidBorder,
};

/**
 * Draw the full slide-019 composition: slide 018's certified base (minus its banner
 * blocks) + slide 019's measured delta, selectively.
 * @param {object} pptx  pptxgenjs instance
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[delta names], only:[delta names], numeral }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  parent.renderBase(pptx, slide, { skip: PARENT_SKIP, numeral: opts.numeral === undefined ? 19 : opts.numeral });
  for (const [name, fn] of Object.entries(DELTA_BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, DELTA_BLOCKS, PARENT_SKIP, C, px };
