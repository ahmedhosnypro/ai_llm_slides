// slide_042.js — "Batch Data (Feature Vectors)" (Deep Learning DSAI 308, Transformers
// Part II — video 002, slide 42). P3 pattern-group HEAD ([42,43,44]). Attempt 3 dispatch
// overall; banked as ATTEMPT 2 here (attempt 1 = the second builder's PNG-based build,
// banked as qa/slide042/build_attempt_1.js + render_1.png + slide_042_recreated_attempt1.pptx;
// it died pre-judge with fatal defects: gray card inside the blue frame, oversized title,
// missing stacking arrow, h-arrow crossing the block, d-label collision, right-box
// overflow). This build replaces the live script with native vector shapes.
//
// CONTENT SPEC: analysis/slide_042_final.json (verbatim; PASS_WITH_FIXES applied).
// PROVENANCE: slide_042_source/SOURCES.md — Wu & He 1803.08494 Fig.2 axis mapping
// (Batch size≡N, Channels≡C, Feature Vector≡feature plane); the course cube style is
// the course's own redraw. Frame = ground truth (fidelity law).
//
// CHROME LAW: shared playlist module shared_patterns/house_chrome.js, numeral 42.
//
// FRAME->SLIDE MAPPING (fitted from THIS frame's four chrome border landmarks —
// left 59, right 902, top 43, bottom-border 516 <-> slide 42, 919, 45, 540; identical
// to certified slide_002/039; badge yellow-bbox center (875.5, 70.5) — same template):
//   slide_x = (frame_x - 18.63) / 0.96123 ;  slide_y = frame_y / 0.95556
// All ink below measured on unique_slides/slide_042.jpg (960x540) and mapped through
// this transform (scratch/slide042/measure2_census.py, measure3_bands.py,
// measure4_disambig.py, using_out.txt, arrowmap_out.txt, crop_bottom/top/diag/leftbox).
//
// MEASURED FACTS honored here (frame wins over spec guesses; spec colors were [?]
// vision-model estimates):
//   * title ink frame (204,72)..(779,111): em 44 (advance 13.725em vs w 598.2pt;
//     height fit 44.0), ink center x 491.9 (NOT slide-centered — measured as-is).
//   * label-box text coloring (PIL word census, beats spec's red/blue guess):
//     LEFT  L1 "Feature Vector of " RED + "One Input" GREEN; L2 "Sample " GREEN +
//           "(Using one filter)" BLUE ("(Using" stems (31,29,78)..(65,57,104) = blue).
//     MID   L1 "Feature Vectors of " RED + "One Input Sample" GREEN; L2 "(Using 4
//           filters)  " BLUE + "[ 4 Channels]" MAGENTA (cores (95..124,17..21,105..127)).
//     RIGHT (left-aligned at frame x637, NOT centered — all three lines start x637):
//           L1 "Feature Vectors of :" RED; L2 "FIVE  Input Samples  " GREEN +
//           "[mini-Batch]" MAGENTA; L3 "Using 4 filters " BLUE + "[ 4 Channels]" MAGENTA.
//   * label boxes: LEFT (76.5,195.5)-(299.5,236.5) — the red stroke at frame x330 is a
//     frozen I-beam text cursor (full-height 1px line between the boxes), NOT a border
//     (the box's horizontal borders end at x299.5); MID (341.5,193.5)-(597.5,234.5);
//     RIGHT (628.5,165.5)-(872,227).
//   * card inside the blue frame is WHITE (interior samples (254,255,253)) — the build
//     paints the blue-frame rect with WHITE fill over the gray panel.
//   * RIGHT BLOCK layer order settled (SOURCES.md open [?]): front-to-back MAGENTA,
//     GREEN, ORANGE, YELLOW, BLUE-GRAY — 5 layers of 4x5 cube grids, layer step
//     (+13, -17.5) frame, per-cube oblique (+12, -12); each layer's DARK top faces
//     (~0.36x front) painted BEFORE its fronts; right faces SAME color as fronts
//     (left-stack bright-quartile front (91,192,8) vs right (97,200,5) — equal).
//     Cross-checked against three independent scans (green front right 790+12=802,
//     orange 803..818, yellow 819..837, bluegray 838..853 at y330/y340/y400).
//   * middle grid 4 cols x 5 rows origin (380,269) pitch (30.7,31.5) front 27x27,
//     oblique (13,14); left stack 1x5 origin (170,277) pitch-y 31.4 front 30x27.
//   * arrows: vertical double-head x642.5 y326.5..466 + rotated-270 label "Feature
//     Vector" (strip x625..641 y330..434); horizontal double-head y486.5 tips
//     x651..814 with "Channels" ABOVE the shaft (cap 473, baseline 483.5) and
//     "(4 Filters)" BELOW (baseline 496) — the shaft passes BETWEEN the two label
//     lines (crop_bottom proof); diagonal double-head (792,474.5)..(861.5,403) with
//     two ~46deg diagonal labels "Batch size" (bbox 795..854/375..446) and
//     "(5 samples)" (bbox 806..865/400..466) above-right of the shaft; small WHITE
//     stacking arrow (803,297)..(814,310) pointing down-right between the green and
//     orange layers near the block top (spec said magenta/yellow — true neighbor is
//     green; visible in crop_top.png).
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c), artifact law):
//     black letterbox strip (frame rows 517..539, below slide bottom 516->540), the
//     I-beam cursor line at x330, and the spec's annotation label "[black horizontal
//     bar ...]" (a spec note, not slide content).
//
// P3 HEAD DUTIES: cube-ladder convention (per-layer paint order, offsets, face
// shading, arrow/label metrics) documented in qa/slide042/worker_report.md for 43/44
// — pattern reuse, NOT a component import.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 960x540 pt
const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "42")
drawHouseChrome(pres, s, { numeral: 42 });

const RED = "CC0000", GREEN = "66CC00", BLUE = "000080", MAGENTA = "CC00CC", NAVY = "000080";
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

// exact parallelogram via custGeom (points = ABSOLUTE inches relative to the shape
// origin; first point auto-moveTo, last carries close:true — pptxgenjs contract
// verified by probe: scratch/slide042/probe_shape.pptx). NOTE: pptxgenjs DROPS the
// x/y of the close point (<a:close/> only) — the first vertex is repeated as an
// extra final point so the quad does not collapse to a triangle.
function para(x, y, w, h, uv, fill) {
  const abs = uv.map(([u, v]) => ({ x: u * w / 72, y: v * h / 72 }));
  abs.push({ x: abs[0].x, y: abs[0].y, close: true });
  s.addShape("custGeom", {
    x: pt(x), y: pt(y), w: pt(w), h: pt(h),
    fill: { color: fill }, line: { type: "none" },
    points: abs,
  });
}

// ---- cube-grid engine ------------------------------------------------------
// One cube: front rect (X, Y, Wf, Hf) + top parallelogram offset (+dx, -dy) + right
// parallelogram (right face SAME color as front — measured). THREE paint passes per
// grid — tops, THEN rights, THEN fronts (measured: the bright seams between columns
// are right-face slivers surviving the next column's front, NOT dark top slivers —
// row y280 frame shows bright green at x406-410; and row n+1's top face shows only
// as a ~4.7pt dark sliver between front rows).
function cubeGrid(ox, oy, cols, rows, pitchX, pitchY, Wf, Hf, dx, dy, cFront, cTop) {
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const X = ox + c * pitchX, Y = oy + r * pitchY;
      // top face quad (X,Y)->(X+Wf,Y)->(X+Wf+dx,Y-dy)->(X+dx,Y-dy)
      // in box (X, Y-dy, Wf+dx, dy)
      para(X, Y - dy, Wf + dx, dy,
        [[0, 1], [Wf / (Wf + dx), 1], [1, 0], [dx / (Wf + dx), 0]], cTop);
    }
  }
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const X = ox + c * pitchX, Y = oy + r * pitchY;
      // right face quad (X+Wf,Y)->(X+Wf+dx,Y-dy)->(X+Wf+dx,Y-dy+Hf)->(X+Wf,Y+Hf)
      // in box (X+Wf, Y-dy, dx, Hf+dy)
      para(X + Wf, Y - dy, dx, Hf + dy,
        [[0, dy / (Hf + dy)], [1, 0], [1, Hf / (Hf + dy)], [0, 1]], cFront);
    }
  }
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      box(ox + c * pitchX, oy + r * pitchY, Wf, Hf, cFront, cFront, 0.25);
    }
  }
}

// ---- 2. title (Arial Bold 44, ink center x 491.9, baseline 107.4)
textLine("title", [{ text: "Batch Data (Feature Vectors)", options: { fontSize: 44, color: RED } }],
  { baseline: 107.4, boxX: 491.9 - 320, boxW: 640, align: "center" });

// ---- 3. blue content frame (navy border, WHITE card fill over the gray panel)
box(SX(69), SY(134.5), SX(889.5) - SX(69), SY(510) - SY(134.5), "FFFFFF", NAVY, 2);

// ---- 4. label boxes (white fill, thin red border) + verbatim runs
box(SX(76.5), SY(195.5), SX(299.5) - SX(76.5), SY(236.5) - SY(195.5), "FFFFFF", RED, 1);   // left
box(SX(341.5), SY(193.5), SX(597.5) - SX(341.5), SY(234.5) - SY(193.5), "FFFFFF", RED, 1); // mid
box(SX(628.5), SY(165.5), SX(872) - SX(628.5), SY(227) - SY(165.5), "FFFFFF", RED, 1);     // right

const LCX = SX(188), MCX = SX(466.5), RLX = SX(637);
// LEFT box: centered on ink center frame x188
textLine("L-L1", [
  { text: "Feature Vector of ", options: { fontSize: 14.8, color: RED } },
  { text: "One Input", options: { fontSize: 14.8, color: GREEN } },
], { baseline: SY(210.2), boxX: LCX - 140, boxW: 280, align: "center" });
textLine("L-L2", [
  { text: "Sample ", options: { fontSize: 14.8, color: GREEN } },
  { text: "(Using one filter)", options: { fontSize: 14.8, color: BLUE } },
], { baseline: SY(227.2), boxX: LCX - 140, boxW: 280, align: "center" });
// MID box: centered on ink center frame x466.5
textLine("M-L1", [
  { text: "Feature Vectors of ", options: { fontSize: 14.5, color: RED } },
  { text: "One Input Sample", options: { fontSize: 14.5, color: GREEN } },
], { baseline: SY(209.5), boxX: MCX - 160, boxW: 320, align: "center" });
textLine("M-L2", [
  { text: "(Using 4 filters)  ", options: { fontSize: 15.3, color: BLUE } },
  { text: "[ 4 Channels]", options: { fontSize: 15.3, color: MAGENTA } },
], { baseline: SY(226.7), boxX: MCX - 160, boxW: 320, align: "center" });
// RIGHT box: LEFT-aligned at frame x637 (all three lines start there — measured)
textLine("R-L1", [{ text: "Feature Vectors of :", options: { fontSize: 14.6, color: RED } }],
  { baseline: SY(182.2), boxX: RLX - 2, boxW: 260, align: "left" });
textLine("R-L2", [
  { text: "FIVE  Input Samples  ", options: { fontSize: 15.4, color: GREEN } },
  { text: "[mini-Batch]", options: { fontSize: 15.4, color: MAGENTA } },
], { baseline: SY(199.2), boxX: RLX - 2, boxW: 280, align: "left" });
textLine("R-L3", [
  { text: "Using 4 filters ", options: { fontSize: 15.4, color: BLUE } },
  { text: "[ 4 Channels]", options: { fontSize: 15.4, color: MAGENTA } },
], { baseline: SY(215.7), boxX: RLX - 2, boxW: 280, align: "left" });

// ---- 5. RIGHT BLOCK: five 4x5 cube-grid layers, painted BACK to FRONT
// (bluegray -> yellow -> orange -> green -> magenta). Layer X offsets are NON-UNIFORM
// (measured from the right-staircase transitions at y330/y340/y400: each layer's total
// right extent = 653+cum+136 frame px -> cum = 12, 28, 49, 64); uniform DY = 18 frame px.
const RB = {
  ox: SX(653), oy: SY(318), cols: 4, rows: 5,
  pitchX: 32.3, pitchY: 33.0, Wf: 31.5, Hf: 28.3, dx: 12.5, dy: 12.6,
};
const LAYERS = [ // back to front: [cumX frame px, front, top]
  [64, "759FC9", "4C5875"],  // blue-gray (rear)
  [49, "EDFF1A", "525C00"],  // yellow
  [28, "FF7F00", "5C2E00"],  // orange
  [12, "7CFC00", "2B5E00"],  // green
  [0, "CC00CC", "4E0050"],   // magenta (front)
];
LAYERS.forEach(([cumX, cFront, cTop], idx) => {
  const kBack = LAYERS.length - 1 - idx;           // 4 for bluegray .. 0 for magenta
  cubeGrid(SX(653 + cumX), SY(318 - 18 * kBack),
    RB.cols, RB.rows, RB.pitchX, RB.pitchY, RB.Wf, RB.Hf, RB.dx, RB.dy,
    cFront, cTop);
});

// ---- 6. LEFT STACK: 1x5 green cubes
cubeGrid(SX(170), SY(277), 1, 5, 32.9, 32.9, 31.3, 28.3, 11.5, 14.7, "7CFC00", "2B5E00");

// ---- 7. MIDDLE GRID: 4x5 green cubes
cubeGrid(SX(380), SY(269), 4, 5, 31.9, 33.0, 28.1, 28.3, 13.5, 14.7, "7CFC00", "2B5E00");

// ---- 8. small WHITE stacking arrow (down-right, between green & orange layers)
s.addShape(pres.ShapeType.line, {
  x: pt(SX(803)), y: pt(SY(297)), w: pt(SX(814) - SX(803)), h: pt(SY(310) - SY(297)),
  line: { color: "FFFFFF", width: 2.5, endArrowType: "triangle" },
});

// ---- 9. dimension arrows + labels (all CC0000)
// The original arrows are THIN shafts (~1pt) with LARGE separate heads (~8.4pt) —
// LibreOffice's line-arrowheads scale with line width and render too heavy, so each
// arrow = thin rect shaft + two isocelesTriangle heads (apex aimed by rotate).
const HEAD = 8.4;
function head(xTip, yTip, deg) { // deg: compass-like aim of the apex (0=up, cw)
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
// vertical double-head at frame x642.5, y326.5..466
shaft(SX(642.5), SY(326.5) + HEAD * 0.7, SX(642.5), SY(466) - HEAD * 0.7, 1.4);
head(SX(642.5), SY(326.5), 0);
head(SX(642.5), SY(466), 180);
// horizontal double-head at frame y486.5, tips x651..778 (span = the magenta front width)
shaft(SX(651) + HEAD * 0.7, SY(486.5), SX(778) - HEAD * 0.7, SY(486.5), 1.4);
head(SX(651), SY(486.5), 270);
head(SX(778), SY(486.5), 90);
// diagonal double-head (792,474.5)..(861.5,403) — thin shaft, big heads
shaft(SX(792) + HEAD * 0.7 * 0.695, SY(474.5) - HEAD * 0.7 * 0.719,
  SX(861.5) - HEAD * 0.7 * 0.695, SY(403) + HEAD * 0.7 * 0.719, 1.4);
head(SX(792), SY(474.5), 226);
head(SX(861.5), SY(403), 46);
// rotated-270 label "Feature Vector" (reads bottom-to-top); measured: strip x625..634,
// ink y345..434 (89f px long -> em 13.6; the y<340 ink in the wide window is the arrow
// head, not text), strip center (629.5, 389.5)f
s.addText("Feature Vector", {
  x: pt(SX(629.5) - 75), y: pt(SY(389.5) - 12), w: pt(150), h: pt(24),
  rotate: 270, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13.6, color: RED, fontFace: "Arial",
});
textLine("h-L1", [{ text: "Channels", options: { fontSize: 14.6, color: RED } }],
  { baseline: SY(483.5), boxX: SX(704.5) - 90, boxW: 180, align: "center" });
textLine("h-L2", [{ text: "(4 Filters)", options: { fontSize: 14.6, color: RED } }],
  { baseline: SY(496), boxX: SX(704) - 90, boxW: 180, align: "center" });
// diagonal labels "Batch size" / "(5 samples)" rotated 46 deg CCW (reading up-right);
// measured block center frame (830, 421), line pitch ~24.5pt
s.addText([
  { text: "Batch size", options: { fontSize: 15.5, color: RED, breakLine: true } },
  { text: "(5 samples)", options: { fontSize: 15.5, color: RED } },
], {
  x: pt(SX(830) - 85), y: pt(SY(421) - 28), w: pt(170), h: pt(56),
  rotate: 314, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 15.5, color: RED, fontFace: "Arial", lineSpacing: 24.5,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_042_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
