// components/slide_019.js — slide 019 composition. CHILD of slide 018 (certified,
// frozen): requires ./slide_018.js and calls its renderBase, skipping 18's two banner
// blocks and their connectors (banner1, banner2, connect_h, connect_tan). NEVER
// re-derives or copies parent geometry — the three paper-figure insets, the h
// annotation, the dashed zoom lines, the enc/dec MHA overlay boxes, the fig handles,
// the yellow band, the title and the whole right-side Figure-1 architecture come from
// the parent component untouched.
//
// SLIDE 019 DELTA (PIL-measured on unique_slides/slide_019.jpg, 960x540, 1px=1pt,
// in = px/72; scans in scratch/slide019/m0..m7 + vision probes probe_callouts /
// probe_enc / probe_dec / probe_dectop through the gate):
//   callout1       "Normalization Layer" roundRect x142-341 y103-129.5, fill CCFFFF,
//                  border 6FA8DC, bold 15pt dark-blue 00008B text
//   callout2       "Feed Forward Layer" roundRect x312.5-513 y144.5-170, fill A0A4A0,
//                  border 7F7F7F, bold 15pt black text
//   callout3       "Residual Connections" roundRect x265.5-464 y182.5-208, fill DEFFC4,
//                  border 4A924A, bold 15pt green 38761D text
//   leader1        thin pale-blue curve from callout1's right edge (341,119) to the
//                  figure-frame edge (571,143), color ACD0E2 w0.75 (measured (172,208,226))
//   leader2        thin pale-gray curve from callout2's right edge (513,156) across the
//                  figure frame into the decoder FF box, ending in a small dark
//                  right-pointing arrowhead at (741-748,231-240) (measured black core)
//   leader3        thin pale-gray-green curve from callout3's right end (464,197)
//                  descending to (551,254), color CDD4CE w0.5
//   residual_green BRIGHT-GREEN (#92D050, measured cores (141,203,44)/(146,222,61))
//                  bypass system, ~4.5-5pt strokes: encoder channel x637 y281-403 with
//                  two right-pointing arrowheads (into enc A&N-top y280.5 and enc
//                  A&N-mid y350.5) and two tap jogs (y328.5, y402 to x685); decoder
//                  channel x833.5 y209-405 with a left-pointing head into dec A&N-top
//                  (y212), two left-pointing heads on jogs y257 / y324 (to x787) and a
//                  tap jog y403.5 — one loop per sub-layer (5 total, per SOURCES.md)
//   an_recolor     "Add & Norm" blocks re-measured as STEEL-BLUE rounded boxes
//                  (5F8CAC, measured (95,140,172)): enc-top (655.5,272.5)-(723,288.5),
//                  enc-mid (656,342.5)-(722,355.5), dec-top (753.5,207.5)-(818.5,219.5),
//                  dec-mid (752,264.5)-(818,276.5); the purple container's A&N is a
//                  BLUE-VIOLET box (6D86E2, measured (109,134,226)) at
//                  (751,329.5)-(818,343). The old dec mid compartment (y249.5-264.5)
//                  is EMPTY olive in this frame — parent's text covered.
//   ff_recolor     "Feed Forward" boxes re-measured DARK GRAY rounded boxes: enc
//                  (651,288.5)-(720,317) fill 81755F border 6E4A28 (measured
//                  (129,117,95)); dec (752,221.5)-(820.5,250) fill 6E7E63 border 3F4A33
//                  (measured (110,126,99)); black bold 9.5pt 2-line text re-drawn
//   vkq_enc_v      encoder V circle re-measured GREEN (4A924A, measured (72,144,72));
//                  K blue / Q red and both decoder V/K/Q rows unchanged (frame check:
//                  masked V blue, cross V blue per m5 blobs)
//   spine_tick     small steel-blue flow arrowhead on the decoder spine at (782.5,252.5)
//                  (measured dark+blue mark x784-790 y253-261)
//
// BANK CONTRACT (founder directive 2026-10-11): 002's graph slide references 001:19 —
// this module exports renderBase(pptx, slide, opts) at block granularity with
// opts.skip / opts.only; opts.chrome=false suppresses the house chrome (drawn once
// here via components/house_chrome.js); opts.numeral overrides the badge.

const parent = require("./slide_018.js");

const px = parent.px;

// ---- slide-019 palette (JPEG-core measured, scratch/slide019/m4/m5/m7) -----------
const C = {
  calloutBlueFill: "CCFFFF",   // measured (206,255,255)
  calloutBlueBorder: "6FA8DC",
  calloutBlueText: "00008B",   // measured (0,14,107)
  calloutGrayFill: "A0A4A0",   // measured (159,164,160)
  calloutGrayBorder: "7F7F7F",
  calloutGreenFill: "DEFFC4",  // measured (222,255,196)
  calloutGreenBorder: "4A924A",
  calloutGreenText: "38761D",  // measured (44,132,28)
  leaderBlue: "ACD0E2",        // measured (172,208,226)
  leaderGray: "C8CBC8",        // measured ~(200,203,200)
  leaderGrayGreen: "CDD4CE",   // measured ~(210,215,210)
  anBlue: "5F8CAC",            // A&N steel blue, measured (95,140,172)
  anViolet: "6D86E2",          // purple-container A&N, measured (109,134,226)
  ffEncFill: "81755F",         // enc FF, measured (129,117,95)
  ffEncBorder: "6E4A28",
  ffDecFill: "6E7E63",         // dec FF, measured (110,126,99)
  ffDecBorder: "3F4A33",
  green: "92D050",             // residual arrows, measured cores (141,203,44)/(146,222,61)
  vGreen: "4A924A",            // encoder V circle, measured (72,144,72)
  tanFill: "C8A888",           // parent encoder container fill (for covers)
  oliveFill: "B0B070",         // parent decoder container fill (for covers)
  ink: "1A1A1A",
  dark: "333333",
};
const SANS = "Arial";

// ---- helpers --------------------------------------------------------------------

function addLines(slide, color, width, pts) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i];
    const [x1, y1] = pts[i + 1];
    slide.addShape("line", {
      x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
      w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
      flipV: y1 < y0, flipH: x1 < x0,
      line: { color, width },
    });
  }
}

// right/left-pointing solid triangle (pptxgenjs triangle points up; rotate 90/270)
function sideArrow(slide, x, y, w, h, dir, color) {
  slide.addShape("triangle", {
    x: px(x), y: px(y), w: px(w), h: px(h),
    rotate: dir === "right" ? 90 : 270,
    fill: { color }, line: { color, width: 0.5 },
  });
}

function rrect(slide, x, y, w, h, fill, border, borderColor, radius) {
  slide.addShape("roundRect", {
    x: px(x), y: px(y), w: px(w), h: px(h), rectRadius: radius,
    fill: { color: fill }, line: { color: borderColor, width: 0.75 },
  });
}

function blockText(slide, x, y, w, h, lines, fontSize, color, lineSpacing, bold) {
  const items = lines.map((t, i) => ({ text: t, options: { breakLine: i < lines.length - 1 } }));
  slide.addText(items, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize, bold: bold !== false, color, lineSpacing,
  });
}

// ---- delta blocks (z-order = call order in renderBase) --------------------------

// tan/olive cover patches: erase parent ink this frame does not show
// (17's A&N texts where 19's boxes are smaller, 17's tan residual curves at
// x632/x642 — replaced by the green channel — and the dec stack's faint
// interior verticals' exposed segments + the empty dec mid-A&N text).
function drawCovers(pptx, slide) {
  // encoder stack (tan container C8A888)
  const T = [[629.5, 267.5, 26.5, 21], [629.5, 288, 18.5, 56.5], [629.5, 355, 18.5, 51]];
  for (const [x, y, w, h] of T) {
    slide.addShape("rect", {
      x: px(x), y: px(y), w: px(w), h: px(h),
      fill: { color: C.tanFill }, line: { color: C.tanFill, width: 0.25 },
    });
  }
  // decoder stack (olive container B0B070): strip above dec-top A&N box +
  // the empty mid compartment
  const O = [[746, 201.5, 74, 6.2], [745.5, 249.5, 94.5, 15.5]];
  for (const [x, y, w, h] of O) {
    slide.addShape("rect", {
      x: px(x), y: px(y), w: px(w), h: px(h),
      fill: { color: C.oliveFill }, line: { color: C.oliveFill, width: 0.25 },
    });
  }
}

function drawAnEncTop(pptx, slide) {
  rrect(slide, 655.5, 272.5, 67.5, 16, C.anBlue, C.anBlue, C.anBlue, 0.05);
  blockText(slide, 655.5, 272.5, 67.5, 16, ["Add & Norm"], 9, C.ink);
}

function drawAnEncMid(pptx, slide) {
  rrect(slide, 656, 342.5, 66, 13, C.anBlue, C.anBlue, C.anBlue, 0.05);
  blockText(slide, 656, 342.5, 66, 13, ["Add & Norm"], 9, C.ink);
}

function drawFfEnc(pptx, slide) {
  rrect(slide, 651, 288.5, 69, 28.5, C.ffEncFill, C.ffEncBorder, C.ffEncBorder, 0.04);
  blockText(slide, 651, 288.5, 69, 28.5, ["Feed", "Forward"], 9.5, C.ink, 11);
}

function drawFfDec(pptx, slide) {
  rrect(slide, 752, 221.5, 68.5, 28.5, C.ffDecFill, C.ffDecBorder, C.ffDecBorder, 0.04);
  blockText(slide, 752, 221.5, 68.5, 28.5, ["Feed", "Forward"], 9.5, C.ink, 11);
}

function drawAnDecTop(pptx, slide) {
  rrect(slide, 753.5, 207.5, 65, 12, C.anBlue, C.anBlue, C.anBlue, 0.05);
  blockText(slide, 753.5, 207.5, 65, 12, ["Add & Norm"], 8, C.ink);
}

function drawAnDecMid(pptx, slide) {
  rrect(slide, 752, 264.5, 66, 12, C.anBlue, C.anBlue, C.anBlue, 0.05);
  blockText(slide, 752, 264.5, 66, 12, ["Add & Norm"], 8, C.ink);
}

function drawAnDecPurple(pptx, slide) {
  rrect(slide, 751, 329.5, 67, 13.5, C.anViolet, C.anViolet, C.anViolet, 0.05);
  blockText(slide, 751, 329.5, 67, 13.5, ["Add & Norm"], 8, C.ink);
}

function drawSpineTick(pptx, slide) {
  slide.addShape("triangle", {
    x: px(782.5), y: px(252.5), w: px(7), h: px(9),
    fill: { color: C.anBlue }, line: { color: C.anBlue, width: 0.5 },
  });
}

function drawResidualGreen(pptx, slide) {
  // ---- encoder: channel on the left interior (x637), two loops ----
  addLines(slide, C.green, 4.5, [[637, 283], [637, 403]]);
  // MHA loop: tap below the MHA block -> channel -> head into A&N-mid
  addLines(slide, C.green, 4.5, [[685, 402], [640, 402]]);
  addLines(slide, C.green, 4.5, [[637, 402], [637, 352]]);
  sideArrow(slide, 647, 345.5, 12.5, 10, "right", C.green);
  // FF loop: tap below the FF block -> channel -> head into A&N-top
  addLines(slide, C.green, 4.5, [[685, 328.5], [640, 328.5]]);
  sideArrow(slide, 645, 275.5, 12, 10, "right", C.green);
  // ---- decoder: channel on the right interior (x833.5), three loops ----
  addLines(slide, C.green, 5, [[833.5, 211], [833.5, 405]]);
  // FF loop head into dec A&N-top
  sideArrow(slide, 824, 206.5, 13, 11, "left", C.green);
  // cross-MHA loop: head-jog into the mid A&N compartment
  addLines(slide, C.green, 4.5, [[789, 257], [833.5, 257]]);
  sideArrow(slide, 786.5, 252, 10, 10, "left", C.green);
  // masked-MHA loop: head-jog into the purple container's A&N
  addLines(slide, C.green, 4.5, [[789, 324], [833.5, 324]]);
  sideArrow(slide, 786, 318.5, 10, 11, "left", C.green);
  // masked-MHA tap below the circle row
  addLines(slide, C.green, 4.5, [[789, 403.5], [833.5, 403.5]]);
}

function drawVkqEncV(pptx, slide) {
  // recolor the encoder V circle (parent drew it blue) — same center/size
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

function drawCallout1(pptx, slide) {
  rrect(slide, 142, 103, 199, 26.5, C.calloutBlueFill, C.calloutBlueBorder, C.calloutBlueBorder, 0.09);
  blockText(slide, 142, 103, 199, 26.5, ["Normalization Layer"], 15, C.calloutBlueText);
}

function drawCallout2(pptx, slide) {
  rrect(slide, 312.5, 144.5, 200.5, 25.5, C.calloutGrayFill, C.calloutGrayBorder, C.calloutGrayBorder, 0.09);
  blockText(slide, 312.5, 144.5, 200.5, 25.5, ["Feed Forward Layer"], 15, C.ink);
}

function drawCallout3(pptx, slide) {
  rrect(slide, 265.5, 182.5, 198.5, 25.5, C.calloutGreenFill, C.calloutGreenBorder, C.calloutGreenBorder, 0.09);
  blockText(slide, 265.5, 182.5, 198.5, 25.5, ["Residual Connections"], 15, C.calloutGreenText);
}

function drawLeader1(pptx, slide) {
  addLines(slide, C.leaderBlue, 0.75, [[341, 119], [470, 119.5], [530, 126], [562, 140], [571, 144]]);
}

function drawLeader2(pptx, slide) {
  addLines(slide, C.leaderGray, 0.5, [
    [513, 156], [545, 162], [572, 171], [640, 200], [700, 223], [737, 232.5],
  ]);
  sideArrow(slide, 741, 231.5, 8, 9, "right", C.dark);
}

function drawLeader3(pptx, slide) {
  addLines(slide, C.leaderGrayGreen, 0.5, [
    [464, 197], [495, 200], [520, 208], [536, 222], [546, 238], [551, 254],
  ]);
}

// ---- composition ----------------------------------------------------------------

// parent blocks this frame does NOT show (the two banners + their connectors)
const PARENT_SKIP = ["banner1", "banner2", "connect_h", "connect_tan"];

const DELTA_BLOCKS = {
  covers: drawCovers,
  an_enc_top: drawAnEncTop,
  ff_enc: drawFfEnc,
  an_enc_mid: drawAnEncMid,
  ff_dec: drawFfDec,
  an_dec_top: drawAnDecTop,
  an_dec_mid: drawAnDecMid,
  an_dec_purple: drawAnDecPurple,
  spine_tick: drawSpineTick,
  residual_green: drawResidualGreen,
  vkq_enc_v: drawVkqEncV,
  callout1: drawCallout1,
  callout2: drawCallout2,
  callout3: drawCallout3,
  leader1: drawLeader1,
  leader2: drawLeader2,
  leader3: drawLeader3,
};

/**
 * Draw the full slide-019 composition: house chrome + slide 18's certified base
 * (minus the banner blocks) + slide 19's delta, selectively.
 * @param {object} pptx  pptxgenjs instance
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[delta names], only:[delta names], chrome:bool, numeral }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  if (opts.chrome !== false) {
    require("./house_chrome.js").drawHouseChrome(pptx, slide, {
      numeral: opts.numeral === undefined ? 19 : opts.numeral,
    });
  }
  parent.renderBase(pptx, slide, { chrome: false, skip: PARENT_SKIP });
  for (const [name, fn] of Object.entries(DELTA_BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, DELTA_BLOCKS, PARENT_SKIP, C, px };
