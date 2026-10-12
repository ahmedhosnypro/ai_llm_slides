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
//
// ATTEMPT 2 (worker takeover 2026-10-12 ~14:00): fleet 13:47 build kept as base where
// measurement-supported (washed borders BE5E62/D2B9B4, left-Channels label 432..441 +
// no-arrow finding, FV x663, GN/INST/RT strip extents); corrections applied from clean
// isolated PIL probes (scratch/slide044/ + this worker's probes, banked in qa report):
//   * TITLE: orig ink (160..750, 55..81) — center 455, advance 590fp=613.8sp. The older
//     "160..849" advance was RECT-BORDER contamination (y92..93 rows). PIL Arial-Bold
//     fit: em 30.5 (612sp). em 34/35.75 WRAPPED/too wide; baseline 76.
//   * HEADER: em 26 (rend-verified at 26: ink matched orig 90..264/90..257 within 3fp).
//   * LEFT cube: a 4th DARK GREEN band y238..251 (xl~87..95 slant, xr~252) was MISSING;
//     front face top is y254 (not 232 — sparse salmon bits above are band-edge noise);
//     face bottom slants 421(x66)..409(x197); side strips measured per-strip
//     (green 239..396, orange 221..379, yellow 200..361, bluegray 186..343).
//   * GN/INST front bands: RIGHT part (above the salmon sub-block) is BRIGHT ORANGE in
//     the frame (GN mean (182,112,25), INST (193,80,33)) — band split drawn as a second
//     para with the slanted channel boundary (336.5→346.5 / 548.5→558.5).
//   * RT: dark magenta band y167..180 EXISTS in the frame ((75,0,77)..(83,0,85) across
//     x700..810) — restored; bright face top y181 (bright-count ramp 169..180 was
//     sparse-noise, full-width only from 181); face pitch 30 (seams measured at
//     210/240/270/300), frontRows last row runs to the face bottom (no tail seam).
//   * ALL faces: row pitch 30 (GN/INST seams measured at +30k: 211/233 dips).
//   * bluegray band color: frame reads (37,54,67) on BOTH 043 and 044 frames — drawn
//     2B3F50 (the certified 042/043 shipped lighter 4C5875; frame wins here, divergence
//     noted for the siblings' future fix round).
//   * bright band edges: each dark band's front 3fp is its BRIGHT family color in the
//     frame (yellow 214..216, orange 146..148/234..237, green 164..166) — drawn.
//   * TEXT ems PIL-fitted on orig ink widths (Arial/Arial Bold/Arial Bold Italic):
//     title 30.5, hdr 26, group 16/16/16.5 (bl 391/410/426), inst title 16.2 (bl 392.5),
//     inst body 16.3 (bl 411/428), layer title 16 (bl 473.5, x86), layer body 17.7
//     (bl 492, ONE line — boxW 800 prevents the attempt-1 wrap), Channels 14.
//   * OVAL: frame dark bbox x734..886 y453..478 (attempt-1 740..882 was 16fp narrow).
//   * Boxes: washed-pink borders D2B9B4 1pt on ALL THREE (frame cores (205..220,177..191,
//     173..185); the layer box border was wrongly dropped in the fleet pass).
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c)): the black letterbox
//     strip (rows 517..539), the white mouse cursor on the left cube's front face.
//
// P3 MEMBER DUTIES: pattern verified against 042/043 builds (band/staircase/seam
// conventions, arrow law, box-fill lesson extended: TINTED fills + washed borders).

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

// exact polygon via custGeom (042 probe-verified contract: repeat the first
// vertex as an extra final point — pptxgenjs drops the close point's x/y).
// uv points are normalized [0..1] onto the box; pass SLIDE-pt x/y/w/h.
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
// yb from xl+OB..xr+OB (oblique), in DARK palette color; bright seam slivers at xs;
// bright = optional front-edge highlight (the frame shows each band's front ~3fp in
// its bright family color).
function band(xl, xr, yf, yb, dark, seamColor, seams, OB, bright) {
  const ob = OB || 10;                       // frame-px inputs; convert here
  const bx = SX(xl), bw = SX(xr + ob) - SX(xl), by = SY(yb), bh = SY(yf) - SY(yb);
  para(bx, by, bw, bh,
    [[0, 1], [(xr - xl) / ((xr + ob) - xl), 1], [1, 0], [ob / ((xr + ob) - xl), 0]], dark);
  (seams || []).forEach(sx => {
    para(SX(sx), SY(yb), SX(sx + 12) - SX(sx), SY(yf) - SY(yb),
      [[0, 1], [2 / 12, 1], [(2 + ob) / 12, 0], [ob / 12, 0]], seamColor);
  });
  if (bright) {
    const H = yf - yb, e = Math.min(3, H * 0.4);
    const sh = e / H * ob;                   // oblique x-shift inside the edge slice
    para(SX(xl), SY(yf - e), bw, SY(yf) - SY(yf - e),
      [[0, 1], [(xr - xl) / ((xr + ob) - xl), 1],
       [(xr + sh - xl) / ((xr + ob) - xl), 0], [sh / ((xr + ob) - xl), 0]], bright);
  }
}

// Bright side sliver (vertical strip of the staircase).
function stripV(x0, x1, y0, y1, color) {
  box(x0, y0, x1 - x0, y1 - y0, color, null, 0);
}

// Front block with BLACK row seams: black base + colored cells per row; the LAST row
// runs to the face bottom (rows*pitch — the frame shows no seam below the last row).
function frontRows(x0, x1, yTop, rows, pitch, cellH, colorSpec) {
  box(x0, yTop, x1 - x0, rows * pitch, "000000", null, 0);
  for (let r = 0; r < rows; r++) {
    const y = yTop + r * pitch;
    const h = (r === rows - 1) ? pitch : cellH;
    colorSpec.forEach(([cx0, cx1, col]) => {
      if (cx1 > cx0) box(cx0, y, cx1 - cx0, h, col, col, 0.25);
    });
  }
}

// ---- 2. title (Arial Bold 30.5, PIL fit 612sp vs orig 613.8sp; ink center 455, bl 76)
textLine("title", [{ text: "Layer , Group, and Instance Normalization", options: { fontSize: 30.5, color: RED } }],
  { baseline: SY(76), boxX: SX(455) - 350, boxW: 700, align: "center" });

// ---- 3. header (blue bold italic, x90, baselines 132/161; em 26 rend-verified)
textLine("hdr1", [{ text: "Sample Based", options: { fontSize: 26, color: BLUE, italic: true } }],
  { baseline: SY(132), boxX: SX(90) - 2, boxW: 260, align: "left" });
textLine("hdr2", [{ text: "Normalization", options: { fontSize: 26, color: BLUE, italic: true } }],
  { baseline: SY(161), boxX: SX(90) - 2, boxW: 260, align: "left" });

// ---- 4. LEFT cube (input tensor) --------------------------------------------
// bands back->front: bluegray-dark, yellow-dark, orange-dark, GREEN-dark (y238..251)
band(127, 268, 199, 187, "2B3F50", null, null, 10, "759FC9");
band(127, 250, 218, 200, "525C00", "E8E040", [168, 199, 230], 10, "E8E040");
band(127, 244, 236, 221, "5C2E00", "E08030", [168, 199, 230], 10, "E08030");
band(87, 240, 251, 238, "2B5E00", "7CFC00", [168, 199, 230], 10, "7CFC00");
// side staircase strips — measured per-strip extents (top = own band's back edge,
// bottom = the side face's slanted bottom edge)
stripV(SX(202), SX(216), SY(239), SY(396), "7CFC00");
stripV(SX(219), SX(236), SY(221), SY(379), "FF7F00");
stripV(SX(238), SX(254), SY(200), SY(361), "EDFF1A");
stripV(SX(256), SX(270), SY(186), SY(343), "759FC9");
// front: SOLID salmon block, top y254, bottom slanting 421(x66)..409(x197); thin
// right-face sliver (no grid seams in frame)
para(SX(66), SY(254), SX(197) - SX(66), SY(421) - SY(254),
  [[0, 0], [1, 0], [1, (409 - 254) / (421 - 254)],
   [(160 - 66) / (197 - 66), (420 - 254) / (421 - 254)], [0, 1]], SALMON);
stripV(SX(198), SX(201), SY(254), SY(404), SALMON);

// ---- 5. GN cube ---------------------------------------------------------------
band(345, 460, 112, 100, "2B3F50", null, null, 10, "759FC9");
band(333, 443, 130, 115, "525C00", "E8E040", [364, 395, 426], 10, "E8E040");
band(320, 448, 148, 133, "5C2E00", "E08030", [352, 383, 414], 10, "E08030");
band(294, 433, 166, 151, "2B5E00", "7CFC00", [325, 356, 387], 10, "7CFC00");
band(283, 435, 181, 169, "4E0050", "E000E8", [314, 345, 376], 10);
// front band's RIGHT part: bright orange above the salmon sub-block (frame mean
// (182,112,25)); slanted channel boundary 336.5 (front) -> 346.5 (back)
para(SX(340), SY(169), SX(442) - SX(340), SY(181) - SY(169),
  [[0, 1], [1, 1], [1, 0], [(348 - 340) / (442 - 340), 0]], "C26618");
// side staircase strips
stripV(SX(412), SX(426), SY(176), SY(315), "7CFC00");
stripV(SX(429), SX(446), SY(176), SY(315), "FF7F00");
stripV(SX(448), SX(455), SY(176), SY(315), "EDFF1A");
// front: black base + 5 rows x [magenta 277..336 | salmon 337..410], pitch 30
(function gnFront() {
  const rows = 5, pitch = 30, cellH = 25;
  frontRows(SX(277), SX(410), SY(182), rows, pitch * KY, cellH * KY, [
    [SX(277), SX(336), MAGENTA],
    [SX(337), SX(410), SALMON],
  ]);
})();

// ---- 6. INSTANCE cube ----------------------------------------------------------
band(472, 600, 113, 98, "2B3F50", null, null, 10, "759FC9");
band(455, 598, 152, 137, "525C00", "E8E040", [486, 517, 548], 10, "E8E040");
band(448, 596, 167, 155, "5C2E00", "E08030", [479, 510, 541], 10, "E08030");
band(443, 588, 185, 170, "2B5E00", "7CFC00", [474, 505, 536], 10, "7CFC00");
band(438, 590, 200, 188, "4E0050", "E000E8", [469, 500, 531], 10);
// front band's RIGHT part: bright orange above the salmon column (frame mean (193,80,33))
para(SX(548.5), SY(188), SX(600) - SX(548.5), SY(200) - SY(188),
  [[0, 1], [(590 - 548.5) / (600 - 548.5), 1], [1, 0],
   [(558.5 - 548.5) / (600 - 548.5), 0]], "C15021");
// side staircase strips
stripV(SX(590), SX(608), SY(196), SY(335), "7CFC00");
stripV(SX(611), SX(624), SY(196), SY(335), "FF7F00");
stripV(SX(626), SX(641), SY(196), SY(335), "EDFF1A");
stripV(SX(644), SX(656), SY(196), SY(335), "759FC9");
// front: black base + 5 solid magenta rows + salmon column + salmon right-face, pitch 30
(function instFront() {
  const rows = 5, pitch = 30, cellH = 24.5;
  frontRows(SX(456), SX(548), SY(203), rows, pitch * KY, cellH * KY, [
    [SX(456), SX(548), MAGENTA],
  ]);
  for (let r = 0; r < 5; r++) {
    const y = SY(203) + r * 30 * KY;
    const h = (r === 4) ? 30 * KY : 24.5 * KY;
    box(SX(549), y, SX(575) - SX(549), h, SALMON, SALMON, 0.25);
    box(SX(578), y, SX(588) - SX(578), h, SALMON, SALMON, 0.25);
  }
})();

// ---- 7. RIGHT TENSOR + red rect -------------------------------------------------
band(745, 870, 112, 98, "2B3F50", null, null, 10, "759FC9");
band(735, 853, 130, 116, "525C00", "E8E040", [766, 797, 828], 10, "E8E040");
band(728, 848, 148, 134, "5C2E00", "E08030", [759, 790, 821], 10, "E08030");
band(715, 837, 166, 151, "2B5E00", "7CFC00", [746, 777, 808], 10, "7CFC00");
band(700, 830, 180, 167, "4E0050", "E000E8", [731, 762, 793], 10);
// side staircase strips
stripV(SX(819), SX(837), SY(163), SY(315), "7CFC00");
stripV(SX(841), SX(855), SY(163), SY(315), "FF7F00");
stripV(SX(862), SX(872), SY(163), SY(315), "EDFF1A");
stripV(SX(875), SX(885), SY(163), SY(315), "759FC9");
// front: black base + 5 magenta rows, top y181 (bright counts full-width only from
// 181), pitch 30 (seams measured 210/240/270/300)
(function rtFront() {
  const rows = 5, pitch = 30, cellH = 25;
  frontRows(SX(689), SX(819), SY(181), rows, pitch * KY, cellH * KY, [
    [SX(689), SX(819), MAGENTA],
  ]);
})();
// thin red rect around the RT stack (measured x658..897, y92..363) — OUTLINE only,
// washed red like the frame's border cores ((182,90,101))
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
// FV vertical x663, tips y145..362
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
// "Samples" along its arrow (reads up-right)
s.addText("Samples", {
  x: pt(SX(107) - 60), y: pt(SY(206) - 12), w: pt(120), h: pt(24),
  rotate: 322, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13, color: RED, fontFace: "Arial",
});
// "Feature Vector" rotated 270 (reads bottom-to-top)
s.addText("Feature Vector", {
  x: pt(SX(675) - 75), y: pt(SY(253) - 12), w: pt(150), h: pt(24),
  rotate: 270, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13.5, color: RED, fontFace: "Arial",
});
// left "Channels" (red, measured ink x95..152 y432..441 -> baseline 441, center 124)
textLine("chL", [{ text: "Channels", options: { fontSize: 14, color: RED } }],
  { baseline: SY(441), boxX: SX(124) - 60, boxW: 120, align: "center" });
// RT "Channels" (red, baseline 333, center x730)
textLine("chR", [{ text: "Channels", options: { fontSize: 13.5, color: RED } }],
  { baseline: SY(333), boxX: SX(730) - 60, boxW: 120, align: "center" });
// "Batch size" rotate 314, center (846, 282)
s.addText("Batch size", {
  x: pt(SX(846) - 70), y: pt(SY(282) - 14), w: pt(140), h: pt(28),
  rotate: 314, align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13.5, color: RED, fontFace: "Arial",
});

// ---- 10. three tinted boxes + verbatim lines ------------------------------------
// washed-pink borders (frame cores ~(210,185,180)); ems PIL-fitted on ink widths
// GROUP box x259..449 y371..444 fill FAFBEB
box(SX(259), SY(371), SX(449) - SX(259), SY(444) - SY(371), "FAFBEB", "D2B9B4", 1);
textLine("g1", [{ text: "Group Normalization", options: { fontSize: 16.4, color: RED } }],
  { baseline: SY(391), boxX: SX(269) - 2, boxW: 180, align: "left" });
textLine("g2", [{ text: "(Group of Channels)", options: { fontSize: 16.4, color: BLUE } }],
  { baseline: SY(410), boxX: SX(269) - 2, boxW: 180, align: "left" });
textLine("g3", [{ text: "General Case", options: { fontSize: 16.6, color: GREEN } }],
  { baseline: SY(426), boxX: SX(269) - 2, boxW: 180, align: "left" });

// INSTANCE box x468..865 y363..441 fill F5FEE3
box(SX(468), SY(363), SX(865) - SX(468), SY(441) - SY(363), "F5FEE3", "D2B9B4", 1);
textLine("i0", [{ text: "Instance Normalization", options: { fontSize: 16.7, color: RED } }],
  { baseline: SY(392.5), boxX: SX(478) - 2, boxW: 240, align: "left" });
textLine("i1", [
  { text: "Calculate (then Normalize) ", options: { fontSize: 16.6, color: BLACK, bold: false } },
  { text: "\u03bc, \u03c3", options: { fontSize: 16.6, color: RED, bold: false } },
  { text: " for ", options: { fontSize: 16.6, color: BLACK, bold: false } },
  { text: "ONE Channel", options: { fontSize: 16.6, color: BLUE, bold: true } },
  { text: " in ", options: { fontSize: 16.6, color: BLACK, bold: false } },
], { baseline: SY(411), boxX: SX(478) - 2, boxW: 430, align: "left" });
textLine("i2", [
  { text: "ONE Sample", options: { fontSize: 16.6, color: BLUE, bold: true } },
  { text: " ", options: { fontSize: 16.6, color: BLACK, bold: false } },
  { text: "(Output of ONE Filter)", options: { fontSize: 16.6, color: GREEN, bold: true } },
], { baseline: SY(428), boxX: SX(478) - 2, boxW: 430, align: "left" });

// LAYER box x62..906 y455..501 fill FED6CA (washed border present in frame)
box(SX(62), SY(455), SX(906) - SX(62), SY(501) - SY(455), "FED6CA", "D2B9B4", 1);
textLine("l0", [{ text: "Layer Normalization", options: { fontSize: 16.4, color: RED } }],
  { baseline: SY(473.5), boxX: SX(86) - 2, boxW: 240, align: "left" });
textLine("l1", [
  { text: "Calculate (then Normalize) ", options: { fontSize: 17.8, color: BLACK, bold: false } },
  { text: "\u03bc, \u03c3", options: { fontSize: 17.8, color: RED, bold: false } },
  { text: " for ", options: { fontSize: 17.8, color: BLACK, bold: false } },
  { text: "ALL Channels in the Same Sample", options: { fontSize: 17.8, color: BLUE, bold: true } },
  { text: " ", options: { fontSize: 17.8, color: BLACK, bold: false } },
  { text: "(Input to Same Layer)", options: { fontSize: 17.8, color: GREEN, bold: true, underline: true } },
], { baseline: SY(492), boxX: SX(75) - 2, boxW: 800, align: "left" });

// ---- 11. callout oval (solid black, yellow bold text) ---------------------------
// frame dark bbox x734..886 y453..478; text em 13 (PIL fit 12.9)
s.addShape(pres.ShapeType.ellipse, {
  x: pt(SX(734)), y: pt(SY(453)), w: pt(SX(886) - SX(734)), h: pt(SY(478) - SY(453)),
  fill: { color: BLACK }, line: { type: "none" },
});
s.addText("Transformer choice", {
  x: pt(SX(742)), y: pt(SY(457)), w: pt(SX(878) - SX(742)), h: pt(SY(474) - SY(457)),
  align: "center", valign: "middle", margin: 0, bold: true,
  fontSize: 13, color: YELLOW, fontFace: "Arial",
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_044_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
