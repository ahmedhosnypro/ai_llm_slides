// Slide 054 recreation — "Example:  Distance with Normalization"
// TALL-PAREN + FONT-FAMILY REBUILD (founder fix #3, 2026-10-10).
//
// Founder complaint (verbatim): "Content is not aligned at all, despite the fact that
// I have reported this problem before, and also the gaps between the content is bad,
// render the screen, zoom it in (crop) and visual analyze vs the original. Also the
// equation doesn't exist."  (The OMML/equation leg is owned by the wrapper-v2 worker —
// out of scope here; this build keeps the certified equation PNG placement.)
//
// This attempt (7th build state, judge attempt 6) fixes what the founder's zoomed
// crop re-report proved, plus the second founder report (paren screenshot):
//
// 1. TALL PARENS: ALL multi-line delimiters are now SINGLE smooth quadratic-Bézier
//    strokes as 600dpi transparent PNGs (build/gen_parens54.py — ADOPTS the
//    slide-053 certified construction VERBATIM per the 2026-10-10 coordinator
//    directive: one glyph per delimiter spanning BOTH lines, embedded at EXACT size
//    w = px/600 in, never rescaled; never font-glyph tall parens, never ARC presets
//    — LO renders ARC presets as double strokes with merged caps, the founder
//    screenshot defect). Anchors = PIL-measured bulge edges (forensics 5-7):
//      feature parens ink y215-263 (inkH 48), LP/RP bulge anchors per column,
//      S=2.5pt, D=2.5pt, class colors (washed strokes measured class-tinted);
//      norm red y324-359 (35), norm blue y324-361 (37), norm green y328-363 (35);
//      test y328-372 (44.5) S=3.0 black; Mean y217-259 (42.5) / S.D y216-259 (43)
//      FAINT GRAY B3B3B3 (att9: original paint lum 155-181, zero sub-170 px —
//      solid black was 3-6x the original ink; PIL-confirmed att8 C2 flag);
//      conclusion parens y446-503 (57) S=3.5 black — geometry-identical to 053's
//      certified callout, so its PNGs are REUSED (assets/parens53).
// 2. FONT FAMILY (empirical, Liberation render match vs original ink, forensics
//    2/4/7): the original is a MIXED-FACE slide. Serif (Times New Roman):
//    feature values 22pt (orig '100' w30 = serif22 EXACT; serif '1' flag+base in
//    the pixel dumps), norm values (red 15.5 / blue 16.5 / green 16.5 — the three
//    class columns genuinely differ: digit core heights 11-12 vs 13-14, line pitch
//    18 vs 20/19), test vector 17pt, sq-dist triplets 17pt (fixes the '11.874'
//    wrap: serif17 '11.874' = 45pt advance in a 56pt box), conclusion 7/100 20pt,
//    row labels 13pt BOLD (serif13b 'Weight (KG)' = 71 vs orig 73), section label
//    25.5pt (serif25.5 'Feature Vector  for bars:' w245 = orig EXACT).
//    Sans (Arial): FT headers 15pt bold ALL (Mean/S.D bumped 13.5->15; orig 'Mean'
//    w36 = sans15b 36), norm headers 15pt bold ('Normalized Red Class' 156 EXACT;
//    underline bars 80-81 = the word's sans15b advance), Mean/S.D VALUES 16pt
//    ('194.44' 47 = sans16 47 EXACT), sq-dist label 16pt bold (594 vs 592),
//    "Belongs to" 13pt, "Blue Class" 16.5pt bold, title/badge = house Arial.
//    Negative values render with U+2212 MINUS SIGN (long bar + gap measured in the
//    original; hyphen-minus is 5-6px and the original's bar is 9-12px).
// 3. CONCLUSION BOX (C6 vision flags, PIL-confirmed this round): cream fill
//    (250,252,228) = FAFCE4 (old BEIGE F5E8C8 was too dark/warm); thin LIGHT
//    border REAL (edge cores ~(215,222,215), 20+ lum darker than both neighbors —
//    not AA; the earlier "JPEG fringe" call was wrong) -> line C8CDC8 1pt; box
//    edges x582-865 / y439-511 (old box was x590-864 / y445-505).
// 4. FORMULA BOX: fill (250,238,224) = F9EDDF (old BEIGE); maroon-brown border
//    certified rect geometry kept; EQUATION PNG UNCHANGED (certified EQUATION
//    ALIGNMENT LAW: x=1.40333in, baseline=6.72222in).
// 5. CONTENT BORDER: 2.5 -> 3.25pt (original core ~3pt vs old render 2.4pt — the
//    C6 "IMG1 bar distinctly heavier... " no: IMG1 was THINNER; measured fix).
//
// Everything else keeps the PIL-measured geometry of the attempt-6 state that the
// zoomed crop comparisons C1-C4/C6 verified within 2-3px (positions faithful).
// Prior builds preserved: qa/slide054/build_attempt_1-6.js (never-delete rule).
//
// LINE SPACING LAW (worker-instructions item 8, 2026-10-10): ZERO multi-line text
// boxes — every stacked pair is two single-line boxes at explicit absolute y:
//   feature 25 (219->244), Mean/S.D 21 (222->243), norm red 18 (327->345),
//   norm blue 20 (327->347), norm green 19 (330->349), test 20 (333->353),
//   conclusion 25 (454->479). Asserted in the closed-loop self-check.
//
// House frame (founder directive 2026-10-09, OVERRIDES spec for outer chrome):
//   background E8E8E8, red frame x:0.15 y:0.15 w:13.03 h:7.2 line C00000 1.5pt,
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill FFF9C4, numeral "54" bold 18pt
//   333333, title box y:0.28 x:0.6 w:12.13 centered.
//
// Spec content VERBATIM (analysis/slide_054_final.json): all values/labels verbatim;
// Normalized Test length -1.244 kept verbatim (validation.uncertain_items — never
// corrected); the x740-755 dark mark between "to" and "Blue" is a video-frame
// artifact (settled, ground rule (c)) — not recreated.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

// ---------- certified equation embedding contract (qa/scratch_math) ----------
function loadEq(name) {
  const eq = JSON.parse(fs.readFileSync(path.join(__dirname, "assets", name + ".json"), "utf8"));
  eq.path = path.join(__dirname, "assets", path.basename(eq.path)); // cwd-independent
  return eq;
}
function addEquation(slide, eq, opts) {
  // opts.x left edge of image (in); opts.baseline target MATH BASELINE (in) —
  // EQUATION ALIGNMENT LAW: y = baseline - baseline_frac * h_in.
  slide.addImage({
    path: eq.path,
    x: opts.x,
    y: opts.baseline - eq.baseline_frac * eq.h_in,
    w: eq.w_in,
    h: eq.h_in,
  });
}

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in = 960 x 540 pt

const BG = "E8E8E8", FRAME_RED = "C00000", RED = "CC0000", BLUE = "0000CC",
      GREEN = "2E8B22", BLACK = "000000", INK = "333333", BADGE_Y = "FFF9C4",
      CREAM = "FAFCE4", CREAM_LINE = "C8CDC8", FORMULA_FILL = "F9EDDF",
      YELLOW = "DDDD00", WHITE = "FFFFFF", PLUS_GRAY = "B3B3B3";
const SANS = "Arial", SERIF = "Times New Roman";
const P = (v) => v / 72;                    // pt -> inches
const TOFF = (fs_) => 0.25 * fs_;          // sans: LO box-top -> cap-ink-top (calibrated)
const TOFFS = (fs_) => 0.29 * fs_;         // serif: initial estimate; calibrated from render_9
const M = (v) => (v.startsWith("-") ? "\u2212" + v.slice(1) : v); // U+2212 minus glyph

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House chrome (founder directive; overrides spec frame/badge/title geometry) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_Y }, line: { color: BADGE_Y, width: 0.5 },
});
s.addText("54", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: SANS, margin: 0,
});

// ---- Title (house geometry; verbatim incl. double space; 'with' underlined) ----
s.addText([
  { text: "Example:  Distance ", options: {} },
  { text: "with", options: { underline: true } },
  { text: " Normalization", options: {} },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: SANS, margin: 0,
});

// ---- Content border — MEASURED stroke centers x70/885, y140.5/520, core ~3pt ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(70), y: P(140.5), w: P(815), h: P(379.5),
  fill: { color: WHITE }, line: { color: RED, width: 3.25 },
});

// ---- Section label — serif 25.5 regular (ink x83-326 w245, top y152) ----
s.addText("Feature Vector  for bars:", {
  x: P(81), y: P(152 - TOFFS(25.5)), w: P(300), h: 0.5, align: "left", valign: "top",
  fontSize: 25.5, bold: false, color: BLACK, fontFace: SERIF, margin: 0,
});

// ---- Feature headers — sans 15pt bold ALL, ink band y186-199 ----
const FT_HDRS = [
  { t: "Red Class",   c: RED,   cx: 250 },
  { t: "Blue Class",  c: BLUE,  cx: 437.5 },
  { t: "Green Class", c: GREEN, cx: 642.5 },
  { t: "Mean",        c: BLACK, cx: 770.5 },
  { t: "S.D",         c: BLACK, cx: 844 },
];
FT_HDRS.forEach((h) => {
  s.addText(h.t, {
    x: P(h.cx - 62), y: P(186 - TOFF(15)), w: P(124), h: 0.3,
    align: "center", valign: "top", fontSize: 15, bold: true,
    color: h.c, fontFace: SANS, margin: 0,
  });
});

// ---- Tall-paren PNG embed helper (slide-053 certified construction) ----
// Each PNG is placed from its MEASURED sidecar ink bbox so ink lands exactly on
// the anchor (bulge outer edge), embedded at EXACT size (w = px/600 in, never
// rescaled). side "lp": anchor = ink LEFT edge; "rp": anchor = ink RIGHT edge.
const PAREN54 = "videos/ml-intro/recreated_pptx/build/assets/parens54";
const PAREN53 = "videos/ml-intro/recreated_pptx/build/assets/parens53";
function parenImg(cls, inkH, color, side, anchorEdgeX, inkTopTarget) {
  const base = `${PAREN54}/paren_${cls}_${side}_${inkH}_${color}`;
  const sc = JSON.parse(fs.readFileSync(base + ".json", "utf8"));
  const ppp = 72 / 600; // pt per rendered px
  const inkAnchorPt = (side === "lp" ? sc.ink_left_px : sc.ink_right_px) * ppp;
  const x = anchorEdgeX - inkAnchorPt;
  const y = inkTopTarget - sc.ink_top_px * ppp;
  s.addImage({ path: base + ".png", x: P(x), y: P(y), w: sc.px_w / 600, h: sc.px_h / 600 });
}
function parenImg53(inkH, color, side, anchorEdgeX, inkTopTarget) {
  // conclusion parens REUSE 053's certified callout PNGs (S=3.5, D=2.5, inkH 57)
  const base = `${PAREN53}/paren_${side}_${inkH}_${color}`;
  const sc = JSON.parse(fs.readFileSync(base + ".json", "utf8"));
  const ppp = 72 / 600;
  const inkAnchorPt = (side === "lp" ? sc.ink_left_px : sc.ink_right_px) * ppp;
  const x = anchorEdgeX - inkAnchorPt;
  const y = inkTopTarget - sc.ink_top_px * ppp;
  s.addImage({ path: base + ".png", x: P(x), y: P(y), w: sc.px_w / 600, h: sc.px_h / 600 });
}

// ---- Feature vectors — serif 22pt values, per-line boxes; Bézier parens ----
// Measured: paren ink y215-263 (inkH 48); value line1 ink top y219, line2 y244
// (pitch 25); every value line is CENTERED on its pair (verified per-pair).
const FEATURE = [
  { c: RED,   hex: "CC0000", cols: [[172, 215], [232, 274], [291, 334]],
    vals: [["2", "100"], ["3", "150"], ["4", "200"]] },
  { c: BLUE,  hex: "0000CC", cols: [[365, 407], [425, 468], [485, 529]],
    vals: [["7", "150"], ["8", "200"], ["9", "250"]] },
  { c: GREEN, hex: "2E8B22", cols: [[564, 606], [624, 666], [684, 727]],
    vals: [["12", "150"], ["13", "250"], ["14", "300"]] },
];
const FT_FS = 22, FT_L1 = 219, FT_L2 = 244, FT_INKTOP = 215, FT_INKH = "48.0";
FEATURE.forEach((grp) => {
  grp.cols.forEach((col, i) => {
    parenImg("feat", FT_INKH, grp.hex, "lp", col[0], FT_INKTOP);
    parenImg("feat", FT_INKH, grp.hex, "rp", col[1], FT_INKTOP);
    const cx = (col[0] + col[1]) / 2, v = grp.vals[i];
    [FT_L1, FT_L2].forEach((top, li) => {
      s.addText(v[li], {
        x: P(cx - 23), y: P(top - TOFFS(FT_FS)), w: P(46), h: P(26),
        align: "center", valign: "top", fontSize: FT_FS, color: grp.c,
        fontFace: SERIF, margin: 0,
      });
    });
  });
});

// ---- Mean / S.D — sans 16pt values + tall Bézier parens (were MISSING) ----
// Measured: paren ink y217-259 (LP bulge 739 / RP 799), S.D y216-259
// (813/874); values '8'/'194.44' centered on 769, '4.163'/'59.835' on 843.5;
// line ink tops y222 / y243 (pitch 21).
// att9: the ORIGINAL's Mean/S.D paren paint is FAINT NEUTRAL GRAY (waist
// transects: darkest lum 155-181, zero sub-170 px; solid >=2pt strokes nearby
// survive dark — Mean '8' 57, S.D '4' 43). Solid black was 3-6x the original
// ink (att8 C2 vision flag, PIL-CONFIRMED) -> parens re-issued in measured
// gray B3B3B3, geometry UNCHANGED (same sidecar extents/anchors).
[
  { cls: "mean", inkH: "42.5", col: [739, 799], cx: 769,   v: ["8", "194.44"] },
  { cls: "sd",   inkH: "43.0", col: [813, 874], cx: 843.5, v: ["4.163", "59.835"] },
].forEach((g) => {
  parenImg(g.cls, g.inkH, "B3B3B3", "lp", g.col[0], g.cls === "mean" ? 217 : 216);
  parenImg(g.cls, g.inkH, "B3B3B3", "rp", g.col[1], g.cls === "mean" ? 217 : 216);
  [222, 243].forEach((top, li) => {
    s.addText(g.v[li], {
      x: P(g.cx - 35), y: P(top - TOFF(16)), w: P(70), h: P(22),
      align: "center", valign: "top", fontSize: 16, color: BLACK,
      fontFace: SANS, margin: 0,
    });
  });
});

// ---- Row labels (feature) — serif 13pt BOLD, ink x84/x85, tops y225 / y248 ----
s.addText("Weight (KG)", {
  x: P(83), y: P(225 - TOFFS(13)), w: P(97), h: 0.28, align: "left", valign: "top",
  fontSize: 13, bold: true, color: BLACK, fontFace: SERIF, margin: 0,
});
s.addText("Length (cm)", {
  x: P(84), y: P(248 - TOFFS(13)), w: P(97), h: 0.28, align: "left", valign: "top",
  fontSize: 13, bold: true, color: BLACK, fontFace: SERIF, margin: 0,
});

// ---- '+' annotation above red '3' — light GRAY (measured ~(185,185,185)) ----
// att8: PIL A/B — original '+' core center (266.5, 214.5); render_9 sat (264, 216).
// Box recentered so the glyph lands on the measured original core.
s.addText("+", {
  x: P(254), y: P(203), w: P(26), h: P(22), align: "center", valign: "middle",
  fontSize: 18, color: PLUS_GRAY, fontFace: SANS, margin: 0,
});

// ---- Normalized headers — sans 15pt bold, ink band y304-318 ----
// The word "Normalized" is UNDERLINED in ALL FOUR headers — att8 re-measure with
// a loose red mask found a CONTINUOUS 178-258px run at y315-316 under the red
// word (same structure as the blue bar's 377-456 run). The earlier "no red
// bar" refutation was a strict-mask artifact — the thin AA'd bar fails r>g+40.
const NT_HDRS = [
  { rest: " Red Class",   c: RED,   cx: 256,   w: 190 },
  { rest: " Blue Class",  c: BLUE,  cx: 456.5, w: 190 },
  { rest: " Green Class", c: GREEN, cx: 652,  w: 190 },
  { rest: " Test",        c: BLACK, cx: 818,  w: 150 },
];
NT_HDRS.forEach((h) => {
  s.addText([
    { text: "Normalized", options: {} },
    { text: h.rest, options: {} },
  ], {
    x: P(h.cx - h.w / 2), y: P(304 - TOFF(15)), w: P(h.w), h: 0.3,
    align: "center", valign: "top", fontSize: 15, bold: true,
    color: h.c, fontFace: SANS, margin: 0,
  });
});
// Underline bars — EXPLICIT RECTANGLES at the original's measured geometry
// (not text underline: LO's run-underline starts ~5pt right of the word's
// advance start). Red bar added att8 (measured x178-258); blue/green y315.5,
// test y316.9; widths = word advance.
[
  { x: 177.5, y: 315.5, w: 80.5, h: 1.8, c: RED },
  { x: 376.5, y: 315.5, w: 80,   h: 1.8, c: BLUE },
  { x: 566.5, y: 315.5, w: 80.5, h: 1.8, c: GREEN },
  { x: 762.5, y: 316.9, w: 79.5, h: 1.9, c: BLACK },
].forEach((b) => {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(b.x), y: P(b.y), w: P(b.w), h: P(b.h),
    fill: { color: b.c }, line: { color: b.c, width: 0.25, transparency: 100 },
  });
});

// ---- Normalized class vectors — serif, per-COLOR size/y (measured), Bézier parens ----
// The original's three class columns genuinely differ: red serif 15.5 / lines
// y327,345 (pitch 18); blue serif 16.5 / y327,347 (20); green serif 16.5 /
// y330,349 (19, whole row sits lower). Value lines are centered on their pairs.
const NORM = [
  { c: RED,   cls: "nred",   hex: "CC0000", inkH: "35.0", fs: 15.5, inkTop: 324,
    l1: 327, l2: 345, cols: [[169, 223], [235, 290], [300, 355]],
    vals: [["-1.441", "-1.578"], ["-1.201", "-0.743"], ["-0.961", "0.093"]] },
  { c: BLUE,  cls: "nblue",  hex: "0000CC", inkH: "37.0", fs: 16.5, inkTop: 324,
    l1: 327, l2: 347, cols: [[368, 427], [438, 484], [496, 542]],
    vals: [["-0.24", "-0.743"], ["0", "0.093"], ["0.24", "0.928"]] },
  { c: GREEN, cls: "ngreen", hex: "2E8B22", inkH: "35.0", fs: 16.5, inkTop: 328,
    l1: 330, l2: 349, cols: [[561, 618], [631, 677], [689, 734]],
    vals: [["0.961", "-0.743"], ["1.201", "0.928"], ["1.441", "1.764"]] },
];
NORM.forEach((grp) => {
  grp.cols.forEach((col, i) => {
    parenImg(grp.cls, grp.inkH, grp.hex, "lp", col[0], grp.inkTop);
    parenImg(grp.cls, grp.inkH, grp.hex, "rp", col[1], grp.inkTop);
    const cx = (col[0] + col[1]) / 2, v = grp.vals[i];
    [[grp.l1, 0], [grp.l2, 1]].forEach(([top, li]) => {
      s.addText(M(v[li]), {
        x: P(cx - 30), y: P(top - TOFFS(grp.fs)), w: P(60), h: P(22),
        align: "center", valign: "top", fontSize: grp.fs, color: grp.c,
        fontFace: SERIF, margin: 0,
      });
    });
  });
});

// ---- Normalized Test vector — serif 17pt, shifted ~8pt down; Bézier parens ----
// Measured: paren ink y328-372 (LP bulge 796 / RP 857, S=3.0); l1 ink top y333,
// l2 y353 (pitch 20); values centered on pair center 826.5.
parenImg("test", "44.5", "000000", "lp", 796, 328);
parenImg("test", "44.5", "000000", "rp", 857, 328);
s.addText(M("-0.24"), {
  x: P(826.5 - 30), y: P(333 - TOFFS(17)), w: P(60), h: P(22),
  align: "center", valign: "top", fontSize: 17, color: BLACK,
  fontFace: SERIF, margin: 0,
});
s.addText(M("-1.244"), { // kept verbatim (spec validation.uncertain_items — never corrected)
  x: P(826.5 - 30), y: P(353 - TOFFS(17)), w: P(60), h: P(22),
  align: "center", valign: "top", fontSize: 17, color: BLACK,
  fontFace: SERIF, margin: 0,
});

// ---- Repeated row labels (normalized) — serif 13pt BOLD, tops y326 / y348 ----
s.addText("Weight (KG)", {
  x: P(86), y: P(326 - TOFFS(13)), w: P(97), h: 0.28, align: "left", valign: "top",
  fontSize: 13, bold: true, color: BLACK, fontFace: SERIF, margin: 0,
});
s.addText("Length (cm)", {
  x: P(87), y: P(348 - TOFFS(13)), w: P(97), h: 0.28, align: "left", valign: "top",
  fontSize: 13, bold: true, color: BLACK, fontFace: SERIF, margin: 0,
});

// ---- Squared-distance label — sans 16pt BOLD, two "Normalized" words RED ----
s.addText([
  { text: "Squared distance between each ", options: { color: BLACK } },
  { text: "Normalized", options: { color: RED } },
  { text: " vector and ", options: { color: BLACK } },
  { text: "Normalized", options: { color: RED } },
  { text: " test vector", options: { color: BLACK } },
], {
  x: P(77.5), y: P(384 - TOFF(16)), w: P(620), h: 0.32, align: "left", valign: "top",
  fontSize: 16, bold: true, fontFace: SANS, margin: 0,
});

// ---- Ellipse behind 0.251 — pale-yellow TRANSLUCENT FILL, NO rim (measured) ----
s.addShape(pptx.shapes.OVAL, {
  x: P(369.5), y: P(399.5), w: P(35), h: P(33),
  fill: { color: YELLOW, transparency: 70 },
  line: { color: YELLOW, width: 0.5, transparency: 100 },
});

// ---- Squared-distance triplets — serif 17pt digits, TALL fs22 glyph parens ----
// att8 PIL A/B vs the original frame: original digits ink y412-422 but parens
// y408-427 (h~20pt, 4pt above / 5pt below the digits); render_9 had digits at
// 408.7 riding the paren top and 14.4pt parens — digits moved to inkTop 412.5,
// parens enlarged to fs22 (ink ~408.5-427) with per-group ink-edge targets
// (pl/pr measured off the original's paren-only columns).
// Values at the original's measured ink-lefts (C4-verified); boxes widened
// 48 -> 56pt so '11.874' (serif17 advance ~45pt) can NEVER wrap — the C4
// wrap defect.
const TRIPLETS = [
  { c: RED,   pl: 175,   pr: 348.3, v: [182, 249, 308], t: ["1.554", "1.175", "2.307"] },
  { c: BLUE,  pl: 365,   pr: 538,   v: [368, 439, 498], t: ["0.251", "1.845", "4.948"] },
  { c: GREEN, pl: 567,   pr: 741,   v: [574, 632, 694], t: ["1.693", "6.794", "11.874"] },
];
const TRIP_FS = 17, TRIP_INKTOP = 412.5, TRIP_Y = TRIP_INKTOP - TOFFS(17);
const TRIP_PFS = 22, TRIP_PY = 408.5 - 0.331 * TRIP_PFS; // '(' ink-top = boxY + 0.331*fs (measured fs17)
TRIPLETS.forEach((grp) => {
  s.addText("(", {
    x: P(grp.pl - 1.3), y: P(TRIP_PY), w: P(10), h: P(26),
    align: "left", valign: "top", fontSize: TRIP_PFS, color: grp.c, fontFace: SERIF, margin: 0,
  });
  grp.v.forEach((vx, i) => {
    s.addText(grp.t[i], {
      x: P(vx - 2), y: P(TRIP_Y), w: P(56), h: P(26),
      align: "left", valign: "top", fontSize: TRIP_FS, color: grp.c, fontFace: SERIF, margin: 0,
    });
  });
  s.addText(")", {
    x: P(grp.pr - 6.2), y: P(TRIP_PY), w: P(10), h: P(26),
    align: "left", valign: "top", fontSize: TRIP_PFS, color: grp.c, fontFace: SERIF, margin: 0,
  });
});

// ---- Formula box — certified rect; fill F9EDDF; MAROON-BROWN border ----
// att8: the original's border core decodes (143,109,103)..(113,78,65) on the
// four edges — never near-black (known-black ink elsewhere in the same JPEG
// reads (0,1,0)); chroma-dilution extrapolation => dark maroon-brown. The
// prior "black" was a dark-mask assumption, never a hue measurement.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.31944, y: 6.26389, w: 3.25, h: 0.75,
  fill: { color: FORMULA_FILL }, line: { color: "8E4E3C", width: 1.25 },
});
const eqNorm = loadEq("eq_054_normalization");
addEquation(s, eqNorm, { x: 1.40333, baseline: 6.72222 });

// ---- Conclusion box — cream FAFCE4 + thin LIGHT border (measured this round) ----
// Edges x582-865 / y439-511; border cores ~(215,222,215) = real thin light line.
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(582), y: P(439), w: P(283), h: P(72),
  fill: { color: CREAM }, line: { color: CREAM_LINE, width: 1 },
});
// Tall parens wrapping BOTH lines — 053's certified callout PNGs REUSED
// (S=3.5, D=2.5, inkH 57); anchors = this slide's measured bulges (LP 600, RP 646).
parenImg53(57, "000000", "lp", 600, 446);
parenImg53(57, "000000", "rp", 646, 446);
// (7 over 100) — verbatim per spec (uncertain item, never corrected); serif 20pt
// ('100' w30 = serif20 EXACT), pitch 25, centered on 623.5.
s.addText("7", {
  x: P(623.5 - 23), y: P(454 - TOFFS(20)), w: P(46), h: P(26),
  align: "center", valign: "top", fontSize: 20, color: BLACK, fontFace: SERIF, margin: 0,
});
s.addText("100", {
  x: P(623.5 - 23), y: P(479 - TOFFS(20)), w: P(46), h: P(26),
  align: "center", valign: "top", fontSize: 20, color: BLACK, fontFace: SERIF, margin: 0,
});
// "Belongs to   Blue Class" — verbatim words at MEASURED positions/sizes.
// att8: original 'Belongs to' ink w=82px at h=13px with ~2x stem weight —
// BOLD 13pt + charSpacing ~2pt reproduces the 80pt span (regular was 59.5pt).
s.addText("Belongs to", {
  x: P(671.9), y: P(468 - TOFF(13)), w: P(100), h: 0.28, align: "left", valign: "top",
  fontSize: 13, bold: true, color: BLACK, fontFace: SANS, margin: 0, charSpacing: 1.7,
});
s.addText("Blue Class", {
  x: P(766.5), y: P(468 - TOFF(16.5)), w: P(110), h: 0.32, align: "left", valign: "top",
  fontSize: 16.5, bold: true, color: BLUE, fontFace: SANS, margin: 0,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_054_recreated.pptx" })
  .then(() => console.log("written: videos/ml-intro/recreated_pptx/slide_054_recreated.pptx"));
