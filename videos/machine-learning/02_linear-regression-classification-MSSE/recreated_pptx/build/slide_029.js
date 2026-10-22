// slide_029.js — "Regression Example (worked)" (ML lecture 02, CHILD of slide 28)
//
// Worker ml02-w029-gen6, 2026-10-13. Resumed from gen-2..5 banked state
// (scratch/ml02/slide029/: MEASUREMENTS_rerun.txt m1..m22, p1 color classes,
// cells.json per-cell windows, v1_verify.py frame-diff probes + this session's
// final probes). All geometry is PIL-measured from unique_slides/slide_029.jpg
// (960x540, 1px = 1pt = 1/72 in).
//
// COMPOSITION (dependency law): the judge-certified parent component
//   videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_028.js
// is REQUIRED by absolute path and drawn via
//   P.renderBase(pptx, slide, { numeral: "29" })
// which draws the house chrome ONCE (shared house_chrome.js, badge numeral 29)
// + title + white data panel + row labels + four training vectors + red y-values
// + Predict + query vector + both formula boxes + eq1/eq2. NOTHING here re-derives
// or re-draws the parent's geometry. This build draws ONLY slide 29's delta.
//
// DELTA VERIFICATION (PIL frame diff slide_028.jpg vs slide_029.jpg):
//   y0..185 identical except (i) badge numeral glyph rows 70..79 (renderBase opts),
//   (ii) a faint 10x2px gray smear at x225..234 y81..82 in the ORIGINAL — cursor
//   artifact, EXCLUDED per judge GROUND RULES (c) precedent (parent's '+' crosshair);
//   y90..185 (inherited panel row) has ZERO diffs => parent geometry certified-correct
//   for this frame. All new content lives at y188+. No parent block needs skip/replace.
//
// MEASURED DELTA (slide_029.jpg):
//   White augmented panel: border strokes x72-73 / x678-679, y188 / y302 ->
//     rect x72.5 y188.5 w606 h114, fill FFFFFF (254,255,253), border B4BAC0 1pt.
//   Augmented rows (labels '1 =>' RED, 'x1 =>' 'x2 =>' black; leading '1' row of
//     each vector RED (bias row — matches red W-component 5 / red matrix col 0 /
//     red X^T row 0 measured below), data rows BLUE; y-row = parent's y-values
//     shifted +122px, values 10/15/13/12 RED; magenta italic 'Augmented Vectors'
//     ink x528..661 y231..246 (~16.5pt, #CC00CC family core (193,60,197)).
//   Four cyan matrix panels y310..425: P1 x72..164.5, P2 x180..330, P3 x379..571,
//     P4 x630..831; fill EDFDFA (237,253,250), border B4BAC0 1pt. Contents:
//     P1 red y-vector (10;15;13;12) in parens; P2 blue X + black 4x3 matrix with
//     RED col 0; P3 blue X^T + black 3x4 matrix with RED row 0; P4 blue X^T X +
//     black 3x3 matrix (all-dark, measured). Bracket delimiters are CROPS of the
//     original frame (ink bbox thr<222, pad 1, x600/72) — same pattern as parent.
//   Beige callout: box x760.5..872.5 y234.5..287 (fill F9EDDD (249,237,221), no
//     side borders), tan top stroke y236 x763..870 (216,196,172), gray left stroke
//     x762..763 (lum~210), 3 italic 12pt dark lines centered ~815.5 ("Always" /
//     "Symmetric" / "(and its inverse)", band centers y247/261/274.5), plus a FAINT
//     gray curved pointer from (754,253) to the X^T X panel top-right (708.5,309.5)
//     — drawn as 4 straight 0.75pt #D0CDC6 segments through measured points
//     (754,253)-(740,261)-(726,272)-(719,284)-(708.5,309.5) (curve is straight
//     within 1px on every chord).
//   Bottom-left cyan panel x78.5..411 y434.5..532 (fill EDFDFA): '(X^T X)^{-1} ='
//     label (blue X, blue T, blue X, blue ^{-1}, black =, paren crops) + 3x3 BLACK
//     matrix [4.75 -1.5 -1.5; -1.5 1 0; -1.5 0 1] between bar crops. The '-1.5'
//     tokens are ink-RIGHT aligned to the measured '1.5' right edges (the thin
//     minus tips measure 6..14px wide under JPEG; right-alignment pins the strong
//     '1.5' edges to <=1px and keeps minus tips within ~6px).
//   Green result panel x498..830 y434.5..532 (fill DAFFEA (218,255,234), border
//     B2C6BE 1pt): W-line W = (X^T X)^{-1} X^T Y => W = (5;3;2) with 5 RED / 3 BLUE /
//     2 BLUE (measured: gw5 red cores, gw3/gw2 blue cores), all other tokens black
//     / blue / red per cells; pale-yellow strip x506.5..680.5 y493.5..527.5 fill
//     FFFFCC border BCC3A4 1pt (border rows y493-494 CONTINUOUS x506..680, lum
//     191..205 — no per-symbol underlines; verified full-row runs n=174/175);
//     final equation y = 3x1 + 2x2 + 5 (3/2 BLUE, 5 RED, rest black). The Y token
//     ink x675..687 overflows the strip's right border (x680) exactly as in the
//     original — strip is drawn BEFORE the W-line tokens so Y renders on top.
//
// EQUATIONS: matplotlib mathtext (STIX) 600dpi transparent PNGs via
// scripts/render_eq.py (PASS-1/2 gen_assets*.py, manifest eq029_manifest.json,
// ink_dx/ink_dy anchored placement), embedded at EXACT px/600 size. Delimiters
// are frame crops. Parent tokens (vx1..4, veq, vd1/vd2, vy1..4, vyeq, vp10/15/13/12,
// Xa, T1, inv, eeq + lx/xs1/xs2/arr from eq028_manifest) are REUSED verbatim —
// same measured scale (frame diff proved the inherited band identical).
//
// Run: NODE_PATH=$(npm root -g) node videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/slide_029.js
// House chrome check: shared_patterns/house_chrome_check.py on the 150dpi render.

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

// parent certified component — ABSOLUTE path, never copy-paste
const P = require("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_028.js");

const NUMERAL = "29";
const PX = 1 / 72; // frame px -> inches
const ASSET = (n) => path.resolve(__dirname, "assets", n + ".png");
const M29 = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq029_manifest.json"), "utf8"));
const M28 = JSON.parse(fs.readFileSync(path.resolve(__dirname, "assets/eq028_manifest.json"), "utf8"));
// this slide's lookup: eq029 entries + parent label/arrow glyphs reused verbatim
const MAN = Object.assign({}, M29, {
  lx: M28.lx, xs1: M28.xs1, xs2: M28.xs2, arr: M28.arr,
});

// ---- measured palette (delta only) ------------------------------------------
const C = {
  panelBorder: "B4BAC0",   // same family as parent data panel (cores 173..204)
  cyanFill: "EDFDFA",      // measured (237,253,250)
  greenFill: "DAFFEA",     // measured (218,255,234)
  greenBorder: "B2C6BE",   // measured top stroke avg (178,203,194)
  stripFill: "FFFFCC",     // spec accent; measured (251,255,220)
  stripBorder: "BCC3A4",   // measured rows y493/494 avg (197,207,173), minlum 176
  calloutFill: "F9EDDD",   // measured (249,237,221)
  calloutTop: "D8C4AC",    // measured top stroke core (216,196,172)
  calloutLeft: "CDCDCD",   // measured left stroke lum ~210
  calloutText: "404040",   // text core samples (90,82,71) JPEG-smeared
  pointer: "D0CDC6",       // faint curve; orig body stable rgb(208,205,198), tip (182,188,184)
  augBar: "9C9AC0",        // aug vector bars V2-V4; orig reads lum 170-200 at bar col
  magenta: "CC00CC",       // spec; core (193,60,197)
  vecBlue: "0000CC",
  yRed: "CC0000",
  inkBlack: "000000",
};

// ---- equation PNG placement (ink-anchored; 1 png px = 72/600 frame px) -------
function eqTop(name, xPx, topPx) {
  const a = MAN[name];
  return {
    path: ASSET(name),
    x: (xPx - a.ink_dx * (72 / 600)) * PX,
    y: (topPx - a.ink_dy * (72 / 600)) * PX,
    w: a.w_px / 600, h: a.h_px / 600,
  };
}
function eqBaseline(name, xPx, blPx) {
  const a = MAN[name];
  return {
    path: ASSET(name),
    x: (xPx - a.ink_dx * (72 / 600)) * PX,
    y: (blPx - a.baseline_frac * a.h_px * (72 / 600)) * PX,
    w: a.w_px / 600, h: a.h_px / 600,
  };
}
function eqCenter(name, xPx, cyPx) {
  const a = MAN[name];
  return {
    path: ASSET(name),
    x: (xPx - a.ink_dx * (72 / 600)) * PX,
    y: (cyPx - (a.ink_dy + a.ink_h / 2) * (72 / 600)) * PX,
    w: a.w_px / 600, h: a.h_px / 600,
  };
}
// ink-RIGHT anchor (for '-1.5' tokens pinned to the measured '1.5' right edges)
function eqTopR(name, xRightPx, topPx) {
  const a = MAN[name];
  return {
    path: ASSET(name),
    x: (xRightPx - (a.ink_dx + a.ink_w) * (72 / 600)) * PX,
    y: (topPx - a.ink_dy * (72 / 600)) * PX,
    w: a.w_px / 600, h: a.h_px / 600,
  };
}
// delimiter crop: place at its measured frame bbox (pad 1 baked into the PNG)
function dlm(name) {
  const a = MAN[name];
  return {
    path: ASSET(name),
    x: (a.frame.x0 - a.pad) * PX,
    y: (a.frame.y0 - a.pad) * PX,
    w: a.w_px / 600, h: a.h_px / 600,
  };
}
function drawImg(slide, spec) { slide.addImage(spec); }
function vline(pptx, slide, xPx, y0Px, y1Px, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: xPx * PX, y: y0Px * PX, w: 0, h: (y1Px - y0Px) * PX,
    line: { color, width },
  });
}
function hline(pptx, slide, x0Px, x1Px, yPx, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: x0Px * PX, y: yPx * PX, w: (x1Px - x0Px) * PX, h: 0,
    line: { color, width },
  });
}
function dline(pptx, slide, x0, y0, x1, y1, color, width) {
  // diagonal segment (top-right -> bottom-left when x decreases)
  const flipH = x1 < x0;
  slide.addShape(pptx.ShapeType.line, {
    x: Math.min(x0, x1) * PX, y: Math.min(y0, y1) * PX,
    w: Math.abs(x1 - x0) * PX, h: Math.abs(y1 - y0) * PX,
    flipH, line: { color, width },
  });
}

// ---- augmented panel ----------------------------------------------------------
function drawPanel2(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 72.5 * PX, y: 188.5 * PX, w: 606 * PX, h: 114 * PX,
    fill: { color: "FFFFFF" }, line: { color: C.panelBorder, width: 1 },
  });
}
// left labels: red '1' + black x1/x2 with subscripts + double-stroke arrows
function drawAugLabels(pptx, slide) {
  drawImg(slide, eqTop("r1", 87, 198));                 // red '1'
  drawImg(slide, eqBaseline("lx", 82, 238.5));          // x of x1
  drawImg(slide, eqBaseline("xs1", 93.75, 243.5));      // subscript 1
  drawImg(slide, eqBaseline("lx", 82, 266.5));          // x of x2
  drawImg(slide, eqBaseline("xs2", 93.75, 271.5));      // subscript 2
  drawImg(slide, eqCenter("arr", 115, 206));
  drawImg(slide, eqCenter("arr", 119, 231));
  drawImg(slide, eqCenter("arr", 119, 260));
}
// four 3-row vectors: red leading 1 + blue rows, bar delimiters (frame crops)
const AUG_DIGITS = [
  // [r0x, r0y, r1asset, r1x, r1y, r2asset, r2x, r2y]
  [198, 200, "vd1", 197, 225, "vd1", 198, 251],
  [288, 200, "vd2", 287, 225, "vd2", 287, 250],
  [377, 200, "vd2", 375, 225, "vd1", 376, 251],
  [465, 200, "vd1", 464, 225, "vd2", 463, 250],
];
function drawAugVectors(pptx, slide) {
  drawImg(slide, dlm("dAugL"));
  drawImg(slide, dlm("dAugR"));
  AUG_DIGITS.forEach((d) => {
    drawImg(slide, eqTop("r1", d[0], d[1]));
    drawImg(slide, eqTop(d[2], d[3], d[4]));
    drawImg(slide, eqTop(d[5], d[6], d[7]));
  });
}
// V2/V3/V4 are each wrapped in their own thin blue-violet bars (measured
// centers x281/300, 369/388, 457/476, y193..269, rgb ~(186,186,212) typical,
// (150,148,187) darkest — the V1 pair is the dAugL/dAugR frame crops above)
function drawAugBars(pptx, slide) {
  // left centers drawn +1px: the 1pt stroke reads ~0.7px left of its path
  // after the 150dpi render + LANCZOS downscale (measured r3)
  [[282, 300], [370, 389], [458, 477]].forEach((pair) => {
    vline(pptx, slide, pair[0], 193, 269, C.augBar, 1);
    vline(pptx, slide, pair[1], 193, 269, C.augBar, 1);
  });
}
// prefix row X1 = .. X4 = (parent tokens at this frame's measured ink tops)
function drawAugPrefix(pptx, slide) {
  const XS = [150, 240, 328, 415];
  const TOPS = [221, 221, 222, 222];
  const EQX = [175, 265, 352, 441];
  XS.forEach((x, i) => drawImg(slide, eqTop("vx" + (i + 1), x, TOPS[i])));
  EQX.forEach((x) => drawImg(slide, eqCenter("veq", x, 229)));
}
// y-row: parent tokens shifted +122px (measured: identical ink, +122 band shift)
function drawAugYRow(pptx, slide) {
  const YS = [[149, 283], [240, 283], [328, 283], [415, 283]];
  YS.forEach((y, i) => drawImg(slide, eqTop("vy" + (i + 1), y[0], y[1])));
  [171, 262, 349, 437].forEach((x) => drawImg(slide, eqCenter("vyeq", x, 287.25)));
  drawImg(slide, eqTop("vp10", 188.2, 279));
  drawImg(slide, eqTop("vp15", 278.56, 279));
  drawImg(slide, eqTop("vp13", 366.68, 279));
  drawImg(slide, eqTop("vp12", 453.76, 280));
}
// magenta italic label, ink x528..661 y231..246
function drawAugLabel(pptx, slide) {
  slide.addText("Augmented Vectors", {
    x: 526 * PX, y: (236.5 / 72) - 0.2, w: 160 * PX, h: 0.4,
    align: "left", valign: "middle", margin: 0,
    fontSize: 16.5, italic: true, color: C.magenta, fontFace: "Arial",
    charSpacing: -0.7,
  });
}

// ---- four matrix panels --------------------------------------------------------
const MATY = 310.5, MATH = 114.5;function panelRect(pptx, slide, x, w) {
  slide.addShape(pptx.ShapeType.rect, {
    x: x * PX, y: MATY * PX, w: w * PX, h: MATH * PX,
    fill: { color: C.cyanFill }, line: { color: C.panelBorder, width: 1 },
  });
}
// P1: red y column vector (10;15;13;12) between paren crops
function drawP1(pptx, slide) {
  panelRect(pptx, slide, 72.5, 92);
  drawImg(slide, dlm("dYvL"));
  drawImg(slide, dlm("dYvR"));
  drawImg(slide, eqTop("yv", 81, 364));
  drawImg(slide, eqTop("yeq", 103, 364));
  drawImg(slide, eqTop("vp10", 129, 324));
  drawImg(slide, eqTop("vp15", 130, 349.5));
  drawImg(slide, eqTop("vp13", 129, 375));
  drawImg(slide, eqTop("vp12", 129, 401));
}
// P2: blue X = + 4x3 matrix (col 0 red, cols 1-2 black) between bar crops
const XMAT = [
  // [asset, x, y]
  ["r1", 245, 324], ["k1", 276, 324], ["k1", 305, 324],
  ["r1", 245, 350], ["k2", 274, 349], ["k2", 304, 349],
  ["r1", 245, 375], ["k2", 274, 375], ["k1", 305, 375],
  ["r1", 245, 401], ["k1", 275, 401], ["k2", 304, 400],
];
function drawP2(pptx, slide) {
  panelRect(pptx, slide, 180.5, 150);
  drawImg(slide, dlm("dXmL"));
  drawImg(slide, dlm("dXmR"));
  drawImg(slide, eqTop("Xh", 185, 355));
  drawImg(slide, eqTop("heq", 218, 366));
  XMAT.forEach((m) => drawImg(slide, eqTop(m[0], m[1], m[2])));
}
// P3: blue X^T = + 3x4 matrix (row 0 red, rows 1-2 black) between bar crops
const XTMAT = [
  ["r1", 458, 337], ["r1", 487, 337], ["r1", 517, 337], ["r1", 547, 337],
  ["k1", 458, 362], ["k2", 486, 362], ["k2", 516, 362], ["k1", 547, 362],
  ["k1", 458, 388], ["k2", 486, 387], ["k1", 518, 387], ["k2", 545, 387],
];
function drawP3(pptx, slide) {
  panelRect(pptx, slide, 379.5, 192);
  drawImg(slide, dlm("dXtL"));
  drawImg(slide, dlm("dXtR"));
  drawImg(slide, eqTop("XTh", 384, 347));
  drawImg(slide, eqTop("heq", 431, 366));
  XTMAT.forEach((m) => drawImg(slide, eqTop(m[0], m[1], m[2])));
}
// P4: blue X^T X = + 3x3 black matrix between bar crops
// (header X^T drawn as Xh + hT — the single XTh PNG is 5px too wide here and
//  would collide with the second X at x676; Xh+hT reproduces both measured spans)
const X2MAT = [
  ["k4", 740, 337], ["k6", 772, 337], ["k6", 801, 337],
  ["k6", 735, 362], ["k10", 767, 362], ["k9", 806, 362],
  ["k6", 736, 387], ["k9", 766, 387], ["k10", 797.5, 387],
];
function drawP4(pptx, slide) {
  panelRect(pptx, slide, 630.5, 201);
  drawImg(slide, dlm("dX2L"));
  drawImg(slide, dlm("dX2R"));
  drawImg(slide, eqTop("Xh", 634, 355));
  drawImg(slide, eqTop("hT", 658, 348));
  drawImg(slide, eqTop("Xh", 676, 354));
  drawImg(slide, eqTop("heq", 710, 366));
  X2MAT.forEach((m) => drawImg(slide, eqTop(m[0], m[1], m[2])));
}

// ---- beige callout + faint pointer ---------------------------------------------
function drawCallout(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 760.5 * PX, y: 234.5 * PX, w: 112 * PX, h: 52.5 * PX,
    fill: { color: C.calloutFill }, line: { color: C.calloutFill, width: 0.25 },
  });
  hline(pptx, slide, 763, 870.5, 236.5, C.calloutTop, 1);
  vline(pptx, slide, 762, 236, 287, C.calloutLeft, 0.75);
  const lines = [
    ["Always", 247], ["Symmetric", 261], ["(and its inverse)", 274.5],
  ];
  lines.forEach((L) => {
    slide.addText(L[0], {
      x: 763 * PX, y: (L[1] / 72) - 0.125, w: 110 * PX, h: 0.25,
      align: "center", valign: "middle", margin: 0,
      fontSize: 12, italic: true, color: C.calloutText, fontFace: "Arial",
    });
  });
}
function drawPointer(pptx, slide) {
  const w = 0.75, col = C.pointer;
  dline(pptx, slide, 754, 253, 740, 261, col, w);
  dline(pptx, slide, 740, 261, 726, 272, col, w);
  dline(pptx, slide, 726, 272, 719, 284, col, w);
  dline(pptx, slide, 719, 284, 708.5, 309.5, col, w);
}

// ---- bottom-left inverse panel ---------------------------------------------------
const INVMAT = [
  // [asset, anchor, x, y]  ('m15r' = km15 ink-right-aligned at x)
  ["k475", "L", 237, 450],
  ["km15", "R", 335.5, 450],
  ["km15", "R", 397.5, 450],
  ["km15", "R", 279.5, 475],
  ["k1", "L", 329, 475],
  ["k0", "L", 378, 475],
  ["km15", "R", 282.5, 501],
  ["k0", "L", 324, 501],
  ["k1", "L", 378, 501],
];
function drawInversePanel(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 78.5 * PX, y: 434.5 * PX, w: 332.5 * PX, h: 98 * PX,
    fill: { color: C.cyanFill }, line: { color: C.panelBorder, width: 1 },
  });
  drawImg(slide, dlm("dIlL"));
  drawImg(slide, eqTop("Xh", 98, 468));
  drawImg(slide, eqTop("Th", 124, 460));
  drawImg(slide, eqTop("Xh", 140, 468));
  drawImg(slide, dlm("dIlR"));
  drawImg(slide, eqTop("invB2", 178, 460));
  drawImg(slide, eqTop("heq", 212, 479));
  drawImg(slide, dlm("dImL"));
  drawImg(slide, dlm("dImR"));
  INVMAT.forEach((m) =>
    drawImg(slide, m[1] === "R" ? eqTopR(m[0], m[2], m[3]) : eqTop(m[0], m[2], m[3]))
  );
}

// ---- green result panel ------------------------------------------------------------
function drawGreenPanel(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 498 * PX, y: 434.5 * PX, w: 332 * PX, h: 98 * PX,
    fill: { color: C.greenFill }, line: { color: C.greenBorder, width: 1 },
  });
  // pale-yellow strip FIRST (the W-line's Y overflows its right border in the
  // original and must render on top of the border)
  slide.addShape(pptx.ShapeType.rect, {
    x: 506.5 * PX, y: 494 * PX, w: 174 * PX, h: 33 * PX,
    fill: { color: C.stripFill }, line: { color: C.stripBorder, width: 1 },
  });
}
// W = (X^T X)^{-1} X^T Y => W = (5;3;2)   — ink tops per measured cells
function drawWLine(pptx, slide) {
  drawImg(slide, eqTop("We", 510, 469));      // W black
  drawImg(slide, eqTop("gEq", 544, 473));     // =
  drawImg(slide, dlm("dGwlL"));               // (
  drawImg(slide, eqTop("gX", 573, 469));      // X blue
  drawImg(slide, eqTop("gT", 590, 464));      // T blue
  drawImg(slide, eqTop("gX", 602, 469));      // X blue
  drawImg(slide, dlm("dGwlr"));               // )
  drawImg(slide, eqTop("ginv", 627, 464));    // ^-1 red
  drawImg(slide, eqTop("gX", 647, 469));      // X blue
  drawImg(slide, eqTop("gT", 663, 464));      // T blue
  drawImg(slide, eqTop("Yb", 675, 469));      // Y red
  drawImg(slide, eqTop("arrr", 705, 473));    // => red
  drawImg(slide, eqTop("Wr", 746, 469));      // W red
  drawImg(slide, eqTop("heq", 773.5, 473));   // =
  drawImg(slide, dlm("dGwL"));                // (
  drawImg(slide, eqTop("gw5r", 800, 447));    // 5 red
  drawImg(slide, eqTop("gw3b", 800, 472));    // 3 blue
  drawImg(slide, eqTop("gw2b", 800, 498));    // 2 blue
  drawImg(slide, dlm("dGwR"));                // )
}
// y = 3x1 + 2x2 + 5  on the strip
function drawStripEq(pptx, slide) {
  drawImg(slide, eqTop("sy", 511, 505));      // y black
  drawImg(slide, eqTop("seq", 528.5, 504));   // =
  drawImg(slide, eqTop("s3b", 549, 499));     // 3 blue
  drawImg(slide, eqTop("sx1", 565, 505));     // x1 black
  drawImg(slide, eqTop("spl", 590, 502));     // +
  drawImg(slide, eqTop("s2b", 607, 499));     // 2 blue
  drawImg(slide, eqTop("sx2", 623, 505));     // x2 black
  drawImg(slide, eqTop("spl", 647, 502));     // +
  drawImg(slide, eqTop("s5", 664, 499));      // 5 red
}

// ---- composition --------------------------------------------------------------------
function render(pptx, slide) {
  // 1) certified parent composition (chrome ONCE with numeral 29 + all top blocks)
  P.renderBase(pptx, slide, { numeral: NUMERAL });
  // 2) slide 29's measured delta
  drawPanel2(pptx, slide);
  drawAugBars(pptx, slide);
  drawAugLabels(pptx, slide);
  drawAugVectors(pptx, slide);
  drawAugPrefix(pptx, slide);
  drawAugYRow(pptx, slide);
  drawAugLabel(pptx, slide);
  drawP1(pptx, slide);
  drawP2(pptx, slide);
  drawP3(pptx, slide);
  drawP4(pptx, slide);
  drawCallout(pptx, slide);
  drawPointer(pptx, slide);
  drawInversePanel(pptx, slide);
  drawGreenPanel(pptx, slide);
  drawWLine(pptx, slide);
  drawStripEq(pptx, slide);
}

// ---- direct run ------------------------------------------------------------------------
if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const slide = pres.addSlide();
  render(pres, slide);
  const out = process.argv[2] || path.resolve(__dirname, "../slide_029_recreated.pptx");
  pres.writeFile({ fileName: out })
    .then(() => console.log("WROTE", out))
    .catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { render, drawPanel2, drawAugVectors, drawP1, drawP2, drawP3, drawP4,
  drawCallout, drawInversePanel, drawGreenPanel, drawWLine, NUMERAL };
