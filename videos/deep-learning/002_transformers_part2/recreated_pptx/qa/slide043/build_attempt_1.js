// slide_043.js — "Batch Normalization" (Deep Learning DSAI 308, Transformers Part II —
// video 002, slide 43). P3 pattern-group MEMBER #2 of [42, 43, 44] — mirrors slide 42's
// certified pattern (cube-grid engine, thin-shaft/large-head arrows, rotated-label and
// baseline laws, mask-artifact lessons) RE-MEASURED on THIS frame (frame = ground truth;
// pattern reuse, NOT a component import — 042's constants were refit from this frame).
//
// CONTENT SPEC: analysis/slide_043_final.json (verbatim; PASS_WITH_FIXES applied; [?]
// kept). PROVENANCE: slide_043_source/SOURCES.md — Ioffe & Szegedy 1502.03167 (BN
// definition) + Wu & He 1803.08494 Fig.2 BatchNorm subplot (axis semantics) — the P3
// family's shared source.
//
// CHROME LAW: shared playlist module shared_patterns/house_chrome.js, numeral 43.
//
// FRAME->SLIDE MAPPING (fitted from THIS frame's four chrome border landmarks —
// left 57..59, right 900..902, top 42..44, bottom 516; identical to certified
// slide_002/039/042; badge yellow-bbox center (875.5, 71) — same template):
//   slide_x = (frame_x - 18.63) / 0.96123 ;  slide_y = frame_y / 0.95556
// All ink below measured on unique_slides/slide_043.jpg (960x540) — probes banked in
// scratch/slide043/probe43*_worker*.py + _out.txt (+ the previous builder's
// measure_*.py corpus).
//
// MEASURED FACTS honored here (frame wins over spec guesses):
//   * title ink (234..639, 56..88): em 44 (width 405px / 9.668em), ink center x 436.5,
//     baseline 87 (no descenders) — NOT slide-centered, placed as measured.
//   * RIGHT STACK = 042's batch block, refit: front 4x5 magenta grid ox 666, oy 165,
//     pitch (30.7, 31.0), Wf/Hf 26.5, oblique (13.4, 13); five layers back->front
//     bluegray/yellow/orange/green/magenta, dy_layer 18 uniform (verified: yellow
//     col-4 right extent 666+55+92.1+26.5+13.4 = 853.1 vs measured 851..853; bluegray
//     854.6..868 vs 855..868; green front-top 147 = 165-18 vs bright sliver 147..149),
//     x-cums {20, 36, 55, 70}, same 042 palette (video-confirmed #759FC9, #2B6100,
//     #525E00, #FDFF0C, #EF7707).
//   * LEFT STACK: front 3x5 magenta grid ox 112, oy 188, pitch (31, 31.1), Wf 26.5,
//     Hf 27, oblique (3.5, 13); rear-layer dark top bands (bluegray/yellow/orange/green
//     tops — video colors match 042's dark palette exactly: #293952->759FC9,
//     #525800=525C00, #572900=5C2E00, #246700=2B5E00) with dy_layer 18 uniform
//     (front tops 170/152/134/116 verified by the band+sliver stack at x190).
//     The right orange mass (x205..316, flat top y104, ~45-deg bottom edge, internal
//     strips [205..245][246..296][297..314] with staircase bottoms 338/284/266) is
//     rendered as the rear layers' front/right peeks + the front layer's deep orange
//     right face per the frame's measured strip geometry (see LEFT_R strip model).
//   * callout box: border rect x331..644.5, y171..265.5 (luminance-dip measured),
//     cream FFFDE0 fill, red CC0000 ~1pt border; text lines at measured baselines
//     192/211.5/234/256, left starts 341/341/347.5/398; C-L3 = "for " BLACK +
//     "ALL Samples in the batch" BLUE (PIL census: blue clusters span 376..598
//     continuously; black cores only at 348..368) — the spec's "'ALL Samples' only
//     blue" reading is overridden by the frame (fidelity law), recorded in SOURCES.md.
//   * bottom box: border x72..879.5, y357..498.5, white fill, green 00AA00 border;
//     four text lines, all bold ~19: L1 wraps after "instead of" (measured L1a
//     x90..808, L1b x90..533 — consistent em ~19 for both; a "Mini-Batch" wrap gives
//     inconsistent ems 22.7/15.5, rejected); L2 blue + black "(Source of Error)."
//     (black cores from x644); L3 red + BLACK "(Constrain)" (red cores end x718,
//     dense black clusters x732..831 with (0,0,0)/(22,22,22) cores — the spec's
//     "entirely red" fix is overridden by the frame, recorded in SOURCES.md).
//   * arrows (right stack), 042 thin-shaft/large-head construction:
//     vertical x656 tips y169..313 + rotated-270 label "Feature Vector" (strip
//     x640..648, ink y192..279, em 13); horizontal y332.5 tips x666..789 with
//     "Channels" ABOVE the shaft (ink x693..747, y318..327, baseline 327); diagonal
//     (808,318)..(880,245) ~45.4deg with "Batch size" rotated 314 (ink center
//     (848.5, 268.5), band 836..861 x 253..284).
//   * pencil icon (x348..404, y232..261) — small; approximated per vision decode.
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c)): the black
//     letterbox strip at the frame bottom (rows 517..539), the full-height pale
//     I-beam cursor line at x615 (spans y42..516 — same artifact class as 042's
//     x330 line), and the spec's "bottom black bar" region note.
//
// P3 MEMBER DUTIES: conventions for slide 44 documented in
// recreated_pptx/qa/slide043/worker_report.md after certification.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 960x540 pt
const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "43")
drawHouseChrome(pres, s, { numeral: 43 });

const RED = "CC0000", BLUE = "0000CC", BLACK = "000000", GREEN_TXT = "009900",
      BORDER_GREEN = "00AA00", CREAM = "FFFDE0";
const pt = v => v / 72;
const SX = fx => (fx - 18.63) / 0.96123; // frame px -> slide pt (x)
const SY = fy => fy / 0.95556;           // frame px -> slide pt (y)
const K_AR = 0.9831;                     // Arial ascent->boxTop lead (baseline law)

function textLine(id, runs, opts) {
  const maxSize = Math.max(...runs.map(r => r.options.fontSize));
  s.addText(runs.map(r => ({
    text: r.text,
    options: {
      fontSize: r.options.fontSize, bold: r.options.bold !== false,
      color: r.options.color, fontFace: "Arial",
      underline: r.options.underline || undefined,
    },
  })), {
    x: pt(opts.boxX), y: pt(opts.baseline - K_AR * maxSize),
    w: pt(opts.boxW), h: pt(1.6 * maxSize),
    align: opts.align || "left", valign: "top", margin: 0,
  });
}

function box(x, y, w, h, fill, lineColor, lineW) {
  s.addShape(pres.ShapeType.rect, {
    x: pt(x), y: pt(y), w: pt(w), h: pt(h),
    fill: { color: fill }, line: { color: lineColor, width: lineW },
  });
}

// exact parallelogram via custGeom (042 probe-verified contract: repeat the first
// vertex as an extra final point — pptxgenjs drops the close point's x/y).
function para(x, y, w, h, uv, fill) {
  const abs = uv.map(([u, v]) => ({ x: u * w / 72, y: v * h / 72 }));
  abs.push({ x: abs[0].x, y: abs[0].y, close: true });
  s.addShape("custGeom", {
    x: pt(x), y: pt(y), w: pt(w), h: pt(h),
    fill: { color: fill }, line: { type: "none" },
    points: abs,
  });
}

// ---- cube-grid engine (042 pattern; + topsOnly mode for the left stack's rear
// layers, whose front/right passes would paint bright peeks the original does not
// show — the original's right mass is drawn explicitly from measured strips below).
function cubeGrid(ox, oy, cols, rows, pitchX, pitchY, Wf, Hf, dx, dy, cFront, cTop, cRight, topsOnly, topLine) {
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const X = ox + c * pitchX, Y = oy + r * pitchY;
      para(X, Y - dy, Wf + dx + 1.2 * KX, dy,
        [[0, 1], [Wf / (Wf + dx + 1.2 * KX), 1], [1, 0],
         [dx / (Wf + dx + 1.2 * KX), 0]], cTop);
      if (topLine) s.addShape(pres.ShapeType.line, {
        x: pt(X + Wf), y: pt(Y - dy), w: pt(dx), h: pt(dy), flipV: true,
        line: { color: topLine, width: 0.5 },
      });
    }
  }
  if (topsOnly) return;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const X = ox + c * pitchX, Y = oy + r * pitchY;
      para(X + Wf, Y - dy, dx, Hf + dy,
        [[0, dy / (Hf + dy)], [1, 0], [1, Hf / (Hf + dy)], [0, 1]], cRight || cFront);
    }
  }
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      box(ox + c * pitchX, oy + r * pitchY, Wf, Hf, cFront, cFront, 0.25);
    }
  }
}

// ---- 2. title (Arial Bold 44, ink center x 436.5, baseline 87 frame)
textLine("title", [{ text: "Batch Normalization", options: { fontSize: 44, color: RED } }],
  { baseline: SY(87.2), boxX: SX(436.5) - 320, boxW: 640, align: "center" });

// ---- 3. RIGHT STACK: five 4x5 cube-grid layers, painted BACK to FRONT
// (bluegray -> yellow -> orange -> green -> magenta); cums/dy refit on THIS frame.
// NOTE: the grid lengths were measured in FRAME px — convert to slide pt
// (x lengths /0.96123, y lengths /0.95556); the origins/cums already go through SX/SY.
const KX = 1 / 0.96123, KY = 1 / 0.95556;
const RB = {
  ox: SX(666), oy: SY(165), cols: 4, rows: 5,
  pitchX: 30.7 * KX, pitchY: 31.0 * KY, Wf: 26.5 * KX, Hf: 26.5 * KY, dx: 13.4 * KX, dy: 13 * KY,
};
const RLAYERS = [ // back to front: [cumX frame px, front, top]
  [70, "759FC9", "4C5875"],  // blue-gray (rear)
  [55, "EDFF1A", "525C00"],  // yellow
  [36, "FF7F00", "5C2E00"],  // orange
  [20, "7CFC00", "2B5E00"],  // green
  [0, "CC00CC", "4E0050"],   // magenta (front)
];
RLAYERS.forEach(([cumX, cFront, cTop], idx) => {
  const kBack = RLAYERS.length - 1 - idx;
  cubeGrid(RB.ox + SX(cumX) - SX(0), RB.oy - SY(18 * kBack) + SY(0),
    RB.cols, RB.rows, RB.pitchX, RB.pitchY, RB.Wf, RB.Hf, RB.dx, RB.dy,
    cFront, cTop);
});

// ---- 4. LEFT STACK (settled across crop-vision rounds 1-5 + fine PIL scans,
// probe43f_mass_out.txt): the 5-layer batch block. Per layer: DEEP top faces
// (dx 44.5 — they extend each top band to ox+133 and form the wall's cube-top
// caps), thin right faces (dx 3.5 — visible as the top-band slivers; colors
// frame-measured per layer: the magenta's are the bright seams E000E8, the
// green/orange/blue-gray slivers are MUTED per the frame), and 3x5 fronts.
// Plus the DEEP RIGHT wall (dx 44.5 parallelograms in engine order, partial
// coverage builds the measured strips/staircase) with subtle row-seam slivers
// (frame: barely-darker bands ~4fp tall) and NO outlines (the frame shows none).
const LB = {
  ox: SX(112), oy: SY(188), cols: 3, rows: 5,
  pitchX: 31.0 * KX, pitchY: 31.1 * KY, Wf: 26.5 * KX, Hf: 27 * KY, dx: 3.5 * KX, dy: 13 * KY,
};
const LLAYERS = [ // back to front: [cumX, front, top, sliverColor, wallColor, wallSeam]
  [69, "759FC9", "4C5875", "5A6E70", "CA8537", "BD7C32"],   // blue-gray (rear)
  [51, "EDFF1A", "525C00", "C5CF18", "F2A614", "E29A12"],   // yellow
  [36, "FF7F00", "5C2E00", "8A6A20", "E47C09", "D67208"],   // orange
  [20, "7CFC00", "2B5E00", "71A43D", "D4A108", "C6970A"],   // green
  [0, "CC00CC", "4E0050", "E000E8", "D05127", "C64D26"],    // magenta (front)
];
function slantBand(XRfp, Ybase_fp, x0fp, x1fp, hfp, colFill, colLine) {
  const t0 = 13 * (x0fp - XRfp) / 44.5, t1 = 13 * (x1fp - XRfp) / 44.5;
  const bx = SX(x0fp), by = SY(Ybase_fp - t1), bw = SX(x1fp) - SX(x0fp),
        bh = SY(Ybase_fp + hfp - t0) - SY(Ybase_fp - t1);
  if (bh <= 0) return;
  const v0 = (t1 - t0) / (hfp + t1 - t0), v2 = hfp / (hfp + t1 - t0);
  const abs = [
    { x: 0, y: v0 * bh / 72 }, { x: bw / 72, y: 0 },
    { x: bw / 72, y: v2 * bh / 72 }, { x: 0, y: bh / 72 },
  ];
  abs.push({ x: 0, y: v0 * bh / 72, close: true });
  s.addShape("custGeom", {
    x: pt(bx), y: pt(by), w: pt(bw), h: pt(bh),
    fill: { color: colFill }, line: colLine ? { color: colLine, width: 0.5 } : { type: "none" },
    points: abs,
  });
}
LLAYERS.forEach(([cumX, cFront, cTop, cSliver, cWall, cWallSeam], idx) => {
  const kBack = LLAYERS.length - 1 - idx;
  const oxL = LB.ox + SX(cumX) - SX(0);
  const oyL = LB.oy - SY(18 * kBack) + SY(0);
  const XRfp = cumX + 112 + 2 * 31.0 + 26.5;
  const Y1fp = 188 - 18 * kBack;
  // DEEP top faces (dx 44.5): three per row, union spans [ox, ox+133]
  for (let r = 0; r < 5; r++) {
    for (let c = 0; c < 3; c++) {
      const X = oxL + c * LB.pitchX, Y = oyL + r * LB.pitchY;
      para(X, Y - LB.dy, LB.Wf + SX(44.5) - SX(0), LB.dy,
        [[0, 1], [LB.Wf / (LB.Wf + SX(44.5) - SX(0)), 1], [1, 0],
         [(SX(44.5) - SX(0)) / (LB.Wf + SX(44.5) - SX(0)), 0]], cTop);
      s.addShape(pres.ShapeType.line, {
        x: pt(X + LB.Wf), y: pt(Y - LB.dy), w: pt(SX(44.5) - SX(0)), h: pt(LB.dy),
        flipV: true, line: { color: "C8CF30", width: 0.6 },
      });
    }
  }
  // (the thin right-face pass is intentionally omitted: the frame's bright
  // top-band slivers come from the FRONTS peeking between the deep tops, and the
  // thin rights rendered as spurious vertical spikes — crop-vision round 6)
  // fronts
  for (let r = 0; r < 5; r++) {
    for (let c = 0; c < 3; c++) {
      box(oxL + c * LB.pitchX, oyL + r * LB.pitchY, LB.Wf, LB.Hf, cFront, cFront, 0.25);
    }
  }
  // DEEP RIGHT wall: one parallelogram per layer (engine order), then subtle seams
  slantBand(XRfp, Y1fp, XRfp + 3.5, XRfp + 44.5, 4 * 31.1 + 27, cWall, null);
  for (let r = 0; r < 4; r++) {
    slantBand(XRfp, Y1fp + 31.1 * r + 27, XRfp + 3.5, XRfp + 44.5, 4.1, cWallSeam, null);
  }
});
// the magenta wall's salmon sub-strip (the frame splits the front layer's deep
// right at x=231.5 — open [?] in SOURCES.md) + its seams
slantBand(200.4, 188, 231.5, 244.9, 4 * 31.1 + 27, "EB4D42", null);
for (let r = 0; r < 4; r++) {
  slantBand(200.4, 188 + 31.1 * r + 27, 231.5, 244.9, 4.1, "D84440", null);
}

// the front grid's continuous bright vertical seams (frame-measured: 4-5px bright
// magenta bands at x139-143 / 169-173 / 200-203, spanning the front-face height —
// the orig's seams are continuous lines, not per-row slant bands)
[138.7, 169.7, 200.7].forEach(sx => {
  s.addShape(pres.ShapeType.rect, {
    x: pt(SX(sx)), y: pt(SY(187)), w: pt(SX(sx + 4.2) - SX(sx)), h: pt(SY(338.5) - SY(187)),
    fill: { color: "E000E8" }, line: { type: "none" },
  });
});

// ---- 5. callout box + text
box(SX(331), SY(171), SX(644.5) - SX(331), SY(265.5) - SY(171), CREAM, RED, 0.5);
textLine("C-L1", [{ text: "Batch Normalization", options: { fontSize: 20, color: RED } }],
  { baseline: SY(192), boxX: SX(341) - 2, boxW: 280, align: "left" });
textLine("C-L2", [
  { text: "Calculate (then Normalize) ", options: { fontSize: 18, color: BLACK } },
  { text: "\u03bc, \u03c3", options: { fontSize: 18, color: RED } },
], { baseline: SY(211.5), boxX: SX(341) - 2, boxW: 290, align: "left" });
textLine("C-L3", [
  { text: "for ", options: { fontSize: 18, color: BLACK, bold: false } },
  { text: "ALL Samples", options: { fontSize: 18, color: BLUE, bold: true } },
  { text: " in the batch", options: { fontSize: 18, color: BLUE, bold: false } },
], { baseline: SY(234), boxX: SX(347.5) - 2, boxW: 290, align: "left" });
textLine("C-L4", [{ text: "(for each channel)", options: { fontSize: 18, color: GREEN_TXT, underline: true } }],
  { baseline: SY(256.5), boxX: SX(398) - 2, boxW: 200, align: "left" });

// pencil icon (x348..404, y232..261 frame): small neat dark pencil lying ~24 deg,
// tip at the lower right (frame-measured sparse strokes; census grays + navy)
(function pencil() {
  // the frame's icon: a tiny thin diagonal pencil stroke (~15x16fp) left of line 4
  s.addShape(pres.ShapeType.rect, {
    x: pt(SX(356)), y: pt(SY(247)), w: pt(SX(366) - SX(356)), h: pt(SY(252) - SY(247)),
    rotate: 40, fill: { color: "BFBFB0" }, line: { color: "707060", width: 0.5 },
  });
  s.addShape(pres.ShapeType.rect, {
    x: pt(SX(363)), y: pt(SY(254)), w: pt(SX(367) - SX(363)), h: pt(SY(258) - SY(254)),
    rotate: 40, fill: { color: "5A5A4C" }, line: { type: "none" },
  });
})();
// ---- 6. bottom summary box + verbatim lines (wrap after "instead of" measured)
box(SX(72), SY(357), SX(879.5) - SX(72), SY(498.5) - SY(357), "FFFFFF", BORDER_GREEN, 1.5);
const BB_L = SX(90) - 1, BB_W = 812;
textLine("B-L1a", [{ text: "Batch Normalization Calculate Mean and Variance of Each Mini-Batch instead of", options: { fontSize: 19.8, color: BLUE } }],
  { baseline: SY(380.5), boxX: BB_L, boxW: BB_W, align: "left" });
textLine("B-L1b", [{ text: "Calculating Mean and Variance of the Whole Data.", options: { fontSize: 19.8, color: BLUE } }],
  { baseline: SY(400), boxX: BB_L, boxW: BB_W, align: "left" });
textLine("B-L2", [
  { text: "The mean and variance will differ from mini-batch to another  ", options: { fontSize: 19.8, color: BLUE } },
  { text: "(Source of Error).", options: { fontSize: 19.8, color: BLACK } },
], { baseline: SY(443.5), boxX: BB_L, boxW: BB_W, align: "left" });
textLine("B-L3", [
  { text: "Mini Batch Size should be large enough to minimize \u201cbatching\u201d effect.  ", options: { fontSize: 19.8, color: RED } },
  { text: "(Constrain)", options: { fontSize: 19.8, color: BLACK } },
], { baseline: SY(487.5), boxX: BB_L, boxW: BB_W, align: "left" });

// ---- 7. dimension arrows + labels (right stack) — 042 thin-shaft/large-head law
const HEAD = 8.4;
function head(xTip, yTip, deg) {
  const rad = deg * Math.PI / 180;
  const cxT = xTip - HEAD / 2 * Math.sin(rad), cyT = yTip + HEAD / 2 * Math.cos(rad);
  s.addShape(pres.ShapeType.triangle, {
    x: pt(cxT - HEAD / 2), y: pt(cyT - HEAD / 2), w: pt(HEAD * 0.95), h: pt(HEAD),
    rotate: deg, fill: { color: RED }, line: { type: "none" },
  });
}
function shaft(x0, y0, x1, y1, w) {
  const L = Math.hypot(x1 - x0, y1 - y0), deg = Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI;
  s.addShape(pres.ShapeType.rect, {
    x: pt((x0 + x1) / 2 - L / 2), y: pt((y0 + y1) / 2 - w / 2), w: pt(L), h: pt(w),
    rotate: deg, fill: { color: RED }, line: { type: "none" },
  });
}
// vertical double-head x656, tips y169..313
shaft(SX(656), SY(169) + HEAD * 0.7, SX(656), SY(313) - HEAD * 0.7, 1.4);
head(SX(656), SY(169), 0);
head(SX(656), SY(313), 180);
// horizontal double-head y332.5, tips x666..789
shaft(SX(666) + HEAD * 0.7, SY(332.5), SX(789) - HEAD * 0.7, SY(332.5), 1.4);
head(SX(666), SY(332.5), 270);
head(SX(789), SY(332.5), 90);
// diagonal double-head (808,318)..(880,245)
shaft(SX(808) + HEAD * 0.7 * 0.707, SY(318) - HEAD * 0.7 * 0.707,
  SX(880) - HEAD * 0.7 * 0.707, SY(245) + HEAD * 0.7 * 0.707, 1.4);
head(SX(808), SY(318), 226);
head(SX(880), SY(245), 46);
// rotated-270 label "Feature Vector" (strip center (644, 235.5), em 13)
s.addText("Feature Vector", {
  x: pt(SX(644) - 75), y: pt(SY(235.5) - 12), w: pt(150), h: pt(24),
  rotate: 270, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13, color: RED, fontFace: "Arial",
});
// "Channels" above the h-shaft (ink center x720, baseline 327)
textLine("h-L1", [{ text: "Channels", options: { fontSize: 13, color: RED } }],
  { baseline: SY(327), boxX: SX(720) - 60, boxW: 120, align: "center" });
// diagonal label "Batch size" rotated 314, single line, center (848.5, 268.5)
s.addText("Batch size", {
  x: pt(SX(848.5) - 70), y: pt(SY(268.5) - 14), w: pt(140), h: pt(28),
  rotate: 314, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13, color: RED, fontFace: "Arial",
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_043_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
