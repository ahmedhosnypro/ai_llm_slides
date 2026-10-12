// slide_044.js — "Layer , Group, and Instance Normalization" (Deep Learning DSAI 308,
// Transformers Part II — video 002, slide 44). P3 pattern-group MEMBER #3 of [42, 43, 44]
// — mirrors the certified 042/043 pattern (thin-shaft/large-head arrows, rotated-label and
// baseline laws, custGeom close-point contract, washed-border reading, artifact omission)
// RE-MEASURED on THIS frame (frame = ground truth; pattern reuse, NOT a component import).
//
// CONTENT SPEC: analysis/slide_044_final.json (verbatim; PASS_WITH_FIXES applied).
// PROVENANCE: slide_044_source/SOURCES.md — Wu & He 1803.08494 Fig.2 (GroupNorm/
// InstanceNorm subplots) per the P3 family's shared source; the course cube style is the
// course's own redraw.
//
// CHROME LAW: shared playlist module shared_patterns/house_chrome.js, numeral 44.
//
// FRAME->SLIDE MAPPING (fitted from THIS frame's chrome landmarks — top 42/44, bottom
// 515/516, right 902, left 57..59 hidden behind content; identical to certified
// slide_002/039/042/043; badge yellow-bbox center (876, 75) — same template):
//   slide_x = (frame_x - 18.63) / 0.96123 ;  slide_y = frame_y / 0.95556
// All ink below measured on unique_slides/slide_044.jpg (960x540) — probes banked in
// scratch/slide044/measure1..9*.py + _out.txt (chrome census, regions, colormap, precise,
// final, pins, samples-arrow, rtchannels).
//
// MEASURED FACTS honored here (frame wins over spec guesses; frame-over-spec
// corrections recorded in slide_044_source/SOURCES.md):
//   * title ink (160..849, 55..79): em 34 (advance 689px / 20.06em), ink center x 504.5,
//     baseline 80 — NOT slide-centered, placed as measured. Verbatim space before the
//     comma in "Layer ," preserved.
//   * header two lines BLUE BOLD ITALIC (spec) at x90, baselines 132/161 (pitch 29):
//     "Sample Based" (90..264) / "Normalization" (90..257).
//   * FOUR voxel stacks (5-layer course style, 042/043 pattern): each = dark top bands
//     back->front (bluegray/yellow/orange/green/front-color) + bright side-sliver
//     staircase (green/orange/yellow/bluegray) + front block. Fronts measured:
//     LEFT  solid salmon F07060 x66..197 y232..421 (NO grid seams in frame), thin
//           salmon right-face sliver 198..201; bands y187..199 (bluegray-dark),
//           200..218 (yellow-dark), 221..236 (orange-dark), xl~127..133, xr 250..268;
//           seams (bright bits) at x~168/199/230.
//     GN    front x277..410 y182..332, 5 rows pitch 31.2 cell 25, BLACK row seams;
//           front split magenta 277..336 | salmon 337..410 (spec's "3/4 magenta"
//           overridden — measured 45/55); bands (front-edge y): 112/130/148/166/181,
//           xl 345/333/320/294/283, xr 460/455/450/445/435; strips green 412..426,
//           orange 429..446, yellow 448..455.
//     INST  front x456..548 y203..351 (5 rows pitch 31) + salmon column 549..575 +
//           salmon right-face 578..588; bands front-edge y 113/152/167/185/200 (from
//           color-bit rows), xl ~440..472, xr ~590..610; strips green 590..608,
//           orange 611..624, yellow 626..641, bluegray 644..656.
//     RT    front x689..819 y169..329 (5 rows pitch 32 cell 27); bands front-edge y
//           112/130/148/164, xl 745/735/728/715, xr 870/865/860/855, magenta top merges
//           into front; strips green 822..838, orange 841..855, yellow 862..872,
//           bluegray 875..885.
//   * red rect around RT: x658..897, y92..363 (top/bottom red y92..93 / y362..364
//     solid-red measured; left 658..660), drawn 1pt CC0000.
//   * arrows (042 thin-shaft + 8.4pt head law, all CC0000):
//     Samples diagonal (79,229)..(135,185) tips, label "Samples" rotated ~322 centered
//     (107,206) — sparse reddish streak measured (measure8); left Channels h-arrow
//     y437 tips x86..162, label "Channels" red baseline 473 center x122; FV vertical
//     x639.5 tips y145..358, label "Feature Vector" rotate 270 strip center (622,251);
//     RT Channels h-arrow y340 tips x660..790, label red baseline 333 center x730;
//     BatchSize diagonal (812,322)..(868,258), label rotate 314 center (846,282).
//   * THREE tinted boxes (fills measured; washed-red borders read pale pink — drawn
//     CC0000 0.75pt):
//     GROUP    x259..449 y371..444 fill FAFBEB: "Group Normalization" red bold 16.5
//              (bl 389, x269) / "(Group of Channels)" blue bold (bl 410) / "General
//              Case" green bold (bl 425).
//     INSTANCE x468..865 y363..441 fill F5FEE3: "Instance Normalization" red bold 16.5
//              (bl 390, x478); body em 15 two lines (bl 411/429): "Calculate (then
//              Normalize) " black + "μ, σ" red + " for " black + "ONE Channel" blue +
//              " in " black // "ONE Sample" blue + " (Output of ONE Filter)" GREEN
//              (frame-over-spec: green measured, spec guessed blue — recorded).
//     LAYER    x62..906 y455..501 fill FED6CA: "Layer Normalization" red bold 16.5
//              (bl 473, x76); body ONE line em 15.5 (bl 496, x75): "Calculate (then
//              Normalize) " black + "μ, σ" red + " for " black + "ALL Channels in the
//              Same Sample" blue + " " + "(Input to Same Layer)" green underlined.
//   * callout oval: solid BLACK ellipse x740..882 y452..478, yellow bold 12 text
//     "Transformer choice" (ink x752..867 y461..468).
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c)): the black letterbox
//     strip (rows 517..539), the white mouse cursor on the left cube's front face
//     (spec imagery: live-recording artifact), the washed full-height cursor-class
//     lines (x642..656 reads as the instance bluegray sliver; nothing drawn).
//
// P3 MEMBER DUTIES: pattern verified against 042/043 builds (band/staircase/seam
// conventions, arrow law, box-fill lesson extended: TINTED fills).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in = 960x540 pt
const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "44")
drawHouseChrome(pres, s, { numeral: 44 });

const RED = "CC0000", BLUE = "0000CC", BLACK = "000000", GREEN = "008000",
      YELLOW = "FFFF00", MAGENTA = "CC00CC", SALMON = "F07060";
const pt = v => v / 72;
const SX = fx => (fx - 18.63) / 0.96123; // frame px -> slide pt (x)
const SY = fy => fy / 0.95556;           // frame px -> slide pt (y)
const KX = 1 / 0.96123, KY = 1 / 0.95556;
const K_AR = 0.9831;                     // Arial ascent->boxTop lead (baseline law)

function textLine(id, runs, opts) {
  const maxSize = Math.max(...runs.map(r => r.options.fontSize));
  s.addText(runs.map(r => ({
    text: r.text,
    options: {
      fontSize: r.options.fontSize, bold: r.options.bold !== false,
      italic: r.options.italic || undefined,
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
    fill: { color: fill }, line: lineColor ? { color: lineColor, width: lineW } : { type: "none" },
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

// ---- cube-stack helpers -----------------------------------------------------
// Dark top band: parallelogram, front (bottom) edge yf from xl..xr, back (top) edge
// yb from xl+OB..xr+OB (oblique), in DARK palette color; bright seam slivers at xs.
function band(xl, xr, yf, yb, dark, seamColor, seams, OB) {
  const ob = OB || 10;                       // frame-px inputs; convert here
  const bx = SX(xl), bw = SX(xr + ob) - SX(xl), by = SY(yb), bh = SY(yf) - SY(yb);
  para(bx, by, bw, bh,
    [[0, 1], [(xr - xl) / ((xr + ob) - xl), 1], [1, 0], [ob / ((xr + ob) - xl), 0]], dark);
  (seams || []).forEach(sx => {
    para(SX(sx), SY(yb), SX(sx + 12) - SX(sx), SY(yf) - SY(yb),
      [[0, 1], [2 / 12, 1], [(2 + ob) / 12, 0], [ob / 12, 0]], seamColor);
  });
}

// Bright side sliver (vertical strip of the staircase).
function stripV(x0, x1, y0, y1, color) {
  box(x0, y0, x1 - x0, y1 - y0, color, null, 0);
}

// Front block with BLACK row seams: black base + colored cells per row.
function frontRows(x0, x1, yTop, rows, pitch, cellH, colorSpec) {
  box(x0, yTop, x1 - x0, (rows - 1) * pitch + cellH + 2, "000000", null, 0);
  for (let r = 0; r < rows; r++) {
    const y = yTop + r * pitch;
    colorSpec.forEach(([cx0, cx1, col]) => {
      if (cx1 > cx0) box(cx0, y, cx1 - cx0, cellH, col, col, 0.25);
    });
  }
}

// ---- 2. title (Arial Bold 34, ink center x 504.5, baseline 80)
textLine("title", [{ text: "Layer , Group, and Instance Normalization", options: { fontSize: 35.75, color: RED } }],
  { baseline: SY(80), boxX: SX(504.5) - 380, boxW: 760, align: "center" });

// ---- 3. header (blue bold italic, x90, baselines 132/161)
textLine("hdr1", [{ text: "Sample Based", options: { fontSize: 27, color: BLUE, italic: true } }],
  { baseline: SY(132), boxX: SX(90) - 2, boxW: 260, align: "left" });
textLine("hdr2", [{ text: "Normalization", options: { fontSize: 27, color: BLUE, italic: true } }],
  { baseline: SY(161), boxX: SX(90) - 2, boxW: 260, align: "left" });

// ---- 4. LEFT cube (input tensor) --------------------------------------------
// bands back->front: bluegray-dark, yellow-dark, orange-dark (measured y extents)
band(127, 268, 199, 187, "4C5875", null, null, 10);
band(127, 262, 218, 200, "525C00", "E8E040", [168, 199, 230], 10);
band(127, 250, 236, 221, "5C2E00", "E08030", [168, 199, 230], 10);
// side staircase strips (green/orange/yellow/bluegray), y ~238..410
stripV(SX(201), SX(216), SY(236), SY(410), "7CFC00");
stripV(SX(219), SX(236), SY(236), SY(410), "FF7F00");
stripV(SX(238), SX(254), SY(236), SY(410), "EDFF1A");
stripV(SX(256), SX(270), SY(236), SY(410), "759FC9");
// front: SOLID salmon block + thin right-face sliver (no grid seams in frame)
box(SX(66), SY(232), SX(197) - SX(66), SY(421) - SY(232), SALMON, SALMON, 0.25);
stripV(SX(198), SX(201), SY(232), SY(421), SALMON);

// ---- 5. GN cube ---------------------------------------------------------------
band(345, 460, 112, 100, "4C5875", null, null, 10);
band(333, 455, 130, 115, "525C00", "E8E040", [364, 395, 426], 10);
band(320, 450, 148, 133, "5C2E00", "E08030", [352, 383, 414], 10);
band(294, 445, 166, 151, "2B5E00", "7CFC00", [325, 356, 387], 10);
band(283, 435, 181, 169, "4E0050", "E000E8", [314, 345, 376], 10);
// side staircase strips
stripV(SX(412), SX(426), SY(176), SY(315), "7CFC00");
stripV(SX(429), SX(446), SY(176), SY(315), "FF7F00");
stripV(SX(448), SX(455), SY(176), SY(315), "EDFF1A");
// front: black base + 5 rows x [magenta 277..336 | salmon 337..410]
(function gnFront() {
  const rows = 5, pitch = 31.2, cellH = 25;
  frontRows(SX(277), SX(410), SY(182), rows, pitch * KY, cellH * KY, [
    [SX(277), SX(336), MAGENTA],
    [SX(337), SX(410), SALMON],
  ]);
})();

// ---- 6. INSTANCE cube ----------------------------------------------------------
band(472, 600, 113, 98, "4C5875", null, null, 10);
band(455, 610, 152, 137, "525C00", "E8E040", [486, 517, 548], 10);
band(448, 608, 167, 155, "5C2E00", "E08030", [479, 510, 541], 10);
band(443, 600, 185, 170, "2B5E00", "7CFC00", [474, 505, 536], 10);
band(438, 590, 200, 188, "4E0050", "E000E8", [469, 500, 531], 10);
// side staircase strips
stripV(SX(590), SX(608), SY(196), SY(335), "7CFC00");
stripV(SX(611), SX(624), SY(196), SY(335), "FF7F00");
stripV(SX(626), SX(641), SY(196), SY(335), "EDFF1A");
stripV(SX(644), SX(656), SY(196), SY(335), "759FC9");
// front: black base + 5 solid magenta rows + salmon column + salmon right-face
(function instFront() {
  const rows = 5, pitch = 31, cellH = 24.5;
  frontRows(SX(456), SX(548), SY(203), rows, pitch * KY, cellH * KY, [
    [SX(456), SX(548), MAGENTA],
  ]);
  for (let r = 0; r < 5; r++) {
    const y = SY(203) + r * 31 * KY;
    box(SX(549), y, SX(575) - SX(549), 24.5 * KY, SALMON, SALMON, 0.25);
    box(SX(578), y, SX(588) - SX(578), 24.5 * KY, SALMON, SALMON, 0.25);
  }
})();

// ---- 7. RIGHT TENSOR + red rect -------------------------------------------------
band(745, 870, 112, 98, "4C5875", null, null, 10);
band(735, 865, 130, 116, "525C00", "E8E040", [766, 797, 828], 10);
band(728, 860, 148, 134, "5C2E00", "E08030", [759, 790, 821], 10);
band(715, 855, 164, 151, "2B5E00", "7CFC00", [746, 777, 808], 10);
// (the front magenta layer's top merges directly into the front — no separate band)
// side staircase strips
stripV(SX(819), SX(837), SY(163), SY(315), "7CFC00");
stripV(SX(841), SX(855), SY(163), SY(315), "FF7F00");
stripV(SX(862), SX(872), SY(163), SY(315), "EDFF1A");
stripV(SX(875), SX(885), SY(163), SY(315), "759FC9");
// front: black base + 5 magenta rows
(function rtFront() {
  const rows = 5, pitch = 32.5, cellH = 28.5;
  frontRows(SX(689), SX(819), SY(169), rows, pitch * KY, cellH * KY, [
    [SX(689), SX(819), MAGENTA],
  ]);
})();
// thin red rect around the RT stack (measured x658..897, y92..363) — OUTLINE only
// (four 1.2pt rects; the original's rect is an unfilled frame — a filled rect would
// cover the stack).
(function rectOutline() {
  const x0 = SX(658), x1 = SX(897), y0 = SY(92), y1 = SY(363), t = 1.2;
  box(x0, y0, x1 - x0, t, "BE5E62", null, 0);
  box(x0, y1 - t, x1 - x0, t, "BE5E62", null, 0);
  box(x0, y0, t, y1 - y0, "BE5E62", null, 0);
  box(x1 - t, y0, t, y1 - y0, "BE5E62", null, 0);
})();

// ---- 8. arrows (042 thin-shaft + 8.4pt-head law, CC0000) ------------------------
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
// Samples diagonal (79,229)..(135,185) — up-right ~38deg
shaft(SX(79) + HEAD * 0.7 * 0.616, SY(229) - HEAD * 0.7 * 0.788,
  SX(135) - HEAD * 0.7 * 0.616, SY(185) + HEAD * 0.7 * 0.788, 1.4);
head(SX(79), SY(229), 232);
head(SX(135), SY(185), 52);
// (NO arrow under the left stack: three mask passes over y415..458 found no shaft or
// heads in the original — only the label block below; the spec's arrow is a vision guess)
// FV vertical x639.5, tips y145..358
shaft(SX(663), SY(145) + HEAD * 0.7, SX(663), SY(362) - HEAD * 0.7, 1.4);
head(SX(663), SY(145), 0);
head(SX(663), SY(362), 180);
// RT Channels h-arrow y340, tips x660..790
shaft(SX(660) + HEAD * 0.7, SY(340), SX(790) - HEAD * 0.7, SY(340), 1.4);
head(SX(660), SY(340), 270);
head(SX(790), SY(340), 90);
// BatchSize diagonal (812,322)..(868,258) — up-right ~49deg
shaft(SX(812) + HEAD * 0.7 * 0.656, SY(322) - HEAD * 0.7 * 0.755,
  SX(868) - HEAD * 0.7 * 0.656, SY(258) + HEAD * 0.7 * 0.755, 1.4);
head(SX(812), SY(322), 217);
head(SX(868), SY(258), 37);

// ---- 9. rotated labels ----------------------------------------------------------
// "Samples" along its arrow (reads up-right; em ~12.5)
s.addText("Samples", {
  x: pt(SX(107) - 60), y: pt(SY(206) - 12), w: pt(120), h: pt(24),
  rotate: 322, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13, color: RED, fontFace: "Arial",
});
// "Feature Vector" rotated 270 (reads bottom-to-top), strip center (622, 251), em 13
s.addText("Feature Vector", {
  x: pt(SX(675) - 75), y: pt(SY(253) - 12), w: pt(150), h: pt(24),
  rotate: 270, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13.5, color: RED, fontFace: "Arial",
});
// left "Channels" (red, measured ink x95..152 y432..441 -> baseline 441, center 124)
textLine("chL", [{ text: "Channels", options: { fontSize: 13, color: RED } }],
  { baseline: SY(441), boxX: SX(124) - 60, boxW: 120, align: "center" });
// RT "Channels" (red, baseline 333, center x730)
textLine("chR", [{ text: "Channels", options: { fontSize: 13.5, color: RED } }],
  { baseline: SY(333), boxX: SX(730) - 60, boxW: 120, align: "center" });
// "Batch size" rotate 314, center (846, 282), em 13
s.addText("Batch size", {
  x: pt(SX(846) - 70), y: pt(SY(282) - 14), w: pt(140), h: pt(28),
  rotate: 314, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13.5, color: RED, fontFace: "Arial",
});

// ---- 10. three tinted boxes + verbatim lines ------------------------------------
// GROUP box x259..449 y371..444 fill FAFBEB
box(SX(259), SY(371), SX(449) - SX(259), SY(444) - SY(371), "FAFBEB", "D89F9B", 1);
textLine("g1", [{ text: "Group Normalization", options: { fontSize: 17, color: RED } }],
  { baseline: SY(389), boxX: SX(269) - 2, boxW: 180, align: "left" });
textLine("g2", [{ text: "(Group of Channels)", options: { fontSize: 17, color: BLUE } }],
  { baseline: SY(408), boxX: SX(269) - 2, boxW: 180, align: "left" });
textLine("g3", [{ text: "General Case", options: { fontSize: 16.5, color: GREEN } }],
  { baseline: SY(424), boxX: SX(269) - 2, boxW: 180, align: "left" });

// INSTANCE box x468..865 y363..441 fill F5FEE3
box(SX(468), SY(363), SX(865) - SX(468), SY(441) - SY(363), "F5FEE3", "D89F9B", 1);
textLine("i0", [{ text: "Instance Normalization", options: { fontSize: 17, color: RED } }],
  { baseline: SY(390), boxX: SX(478) - 2, boxW: 240, align: "left" });
textLine("i1", [
  { text: "Calculate (then Normalize) ", options: { fontSize: 16.8, color: BLACK, bold: false } },
  { text: "\u03bc, \u03c3", options: { fontSize: 16.8, color: RED, bold: false } },
  { text: " for ", options: { fontSize: 16, color: BLACK, bold: false } },
  { text: "ONE Channel", options: { fontSize: 16.8, color: BLUE, bold: true } },
  { text: " in ", options: { fontSize: 16, color: BLACK, bold: false } },
], { baseline: SY(411), boxX: SX(478) - 2, boxW: 430, align: "left" });
textLine("i2", [
  { text: "ONE Sample", options: { fontSize: 16, color: BLUE, bold: true } },
  { text: " ", options: { fontSize: 16, color: BLACK, bold: false } },
  { text: "(Output of ONE Filter)", options: { fontSize: 16.8, color: GREEN, bold: true } },
], { baseline: SY(429), boxX: SX(478) - 2, boxW: 430, align: "left" });

// LAYER box x62..906 y455..501 fill FED6CA
box(SX(62), SY(455), SX(906) - SX(62), SY(501) - SY(455), "FED6CA", null, 0);
textLine("l0", [{ text: "Layer Normalization", options: { fontSize: 17, color: RED } }],
  { baseline: SY(475), boxX: SX(76) - 2, boxW: 240, align: "left" });
textLine("l1", [
  { text: "Calculate (then Normalize) ", options: { fontSize: 17.8, color: BLACK, bold: false } },
  { text: "\u03bc, \u03c3", options: { fontSize: 17.8, color: RED, bold: false } },
  { text: " for ", options: { fontSize: 16, color: BLACK, bold: false } },
  { text: "ALL Channels in the Same Sample", options: { fontSize: 17.8, color: BLUE, bold: true } },
  { text: " ", options: { fontSize: 16, color: BLACK, bold: false } },
  { text: "(Input to Same Layer)", options: { fontSize: 17.8, color: GREEN, bold: true, underline: true } },
], { baseline: SY(496), boxX: SX(75) - 2, boxW: 780, align: "left" });

// ---- 11. callout oval (solid black, yellow bold text) ---------------------------
s.addShape(pres.ShapeType.ellipse, {
  x: pt(SX(742)), y: pt(SY(453)), w: pt(SX(879) - SX(742)), h: pt(SY(477) - SY(453)),
  fill: { color: BLACK }, line: { type: "none" },
});
s.addText("Transformer choice", {
  x: pt(SX(745)), y: pt(SY(457)), w: pt(SX(876) - SX(745)), h: pt(SY(473) - SY(457)),
  align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13, color: YELLOW, fontFace: "Arial",
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_044_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
