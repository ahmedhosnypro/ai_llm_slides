// build/slide_029.js — slide 029 "Sequence of 12 words / Positions are defined / as angles"
// (Deep Learning DSAI 308, 002_transformers_part2) — DEPENDENCY-GATED CHILD BUILD
// (founder directive 2026-10-11; edge 29 <- 28; slide_029_final.json PASS_WITH_FIXES).
//
// DEPENDENCY CONTRACT: slide 29 = slide 28's judge-certified component
// (components/slide_028.js, CERTIFIED 2026-10-12 qa/slide028/judge_attempt_1.txt FINAL
// VERDICT: PASS) grown from 9 words / 8 arcs to 12 words / 11 arcs — imported via
// renderBase(pptx, slide, {numeral: 29, wordCount: 12, skip:["arcs","title"]}), NEVER
// re-derived — plus this slide's measured delta. The 028 component itself imports 027
// (chrome/circle/spokes/chips/eqbox) and 026 (zero-block, per its census), so the whole
// certified chain lands here untouched.
//
// FRAME->SLIDE MAPPING (chrome-landmark check, scratch/slide029/probe1.py):
// slide_029.jpg's chrome is pixel-identical to slide_028.jpg's (left border col 58,
// top row 43, black letterbox bar rows 519..539 both frames; badge/numeral band except
// the numeral glyphs), so the parent's certified mapping lands 1:1:
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// (002 capture convention, see build/slide_002.js header). All delta coordinates below
// are TRUE slide points converted from frame px through this transform.
//
// MEASURED DELTA (scratch/slide029/measure1..5.py, PIL on unique_slides/slide_029.jpg
// vs unique_slides/slide_028.jpg; masks calibrated on 028's certified constants —
// label wide-window reproduced the certified centers at bias 0.0, head masks <=1.5pt):
//   * title line 1 "Sequence of 9 words" -> "Sequence of 12 words": ink is CENTER-aligned
//     at slide cx 177.0 on BOTH frames (28 ink 56.6..296.9, 29 ink 51.4..303.1 — same
//     center, +11.4pt width for "12" vs "9"; the certified left-aligned box coincides for
//     28's text but not 29's). Line 1 drawn center-aligned at cx 177.0; lines 2-3 use the
//     certified constants byte-identically (their ink is unchanged — no diff rows).
//   * chips k=9..11: the component's polar rule (chipR 182.5 @ k*30 deg) verified against
//     this frame's measured chip centers to <=1.1pt (measure4.py; k=8 control identical
//     between the two frames at <=1 frame px) — no overrides.
//   * NO arc 11 (Word 11 -> Word 0): no pale-stroke pixels in the 342..358.5 deg sector
//     beyond the axis baseline (22 px vs 21 px on 28), no arrowhead (window n=0), no
//     '+w' label — 11 arcs, k=0..10, exactly the family rule k < wordCount-1. The spec's
//     "12 arcs / Word 11 -> Word 0" is overridden by the frame (SOURCES.md had flagged
//     this as [?]; frame wins).
//   * arcs k=8..10: family polyline rule (arcR 224, pads 12/1.5, 14 segs, F0C9B0 0.75pt;
//     pale-stroke angle bins confirm 252-268.5 / 282-298.5 / 312-328.5 deg present);
//     arrowheads at MEASURED slide-pt centers (full-mask centroids, ALL_HEADS29):
//       k=8 (576.2, 522.7) [polar rule (581.0,521.7) — hand-placed 4.8pt left, like 28's
//                            k=5/k=6 heads 4.5-5.2pt off-rule],
//       k=9 (689.1, 493.4) [polar (693.25,491.6) — hand-placed],
//       k=10 (777.0, 408.7) [polar (775.4,409.45) — on-rule].
//   * '+w' labels (Arial bold 15pt CC0000, 30x16pt centered box), MEASURED ink centroids
//     (measure5.py wide-window — the exact method that reproduced 028's certified label
//     centers at bias 0.0; wh 21-22 x 8-10 px, matching the certified '+w' ink size):
//       k=7 MOVED (414.2, 479.6) — 028's (372.7,489.2) spot shows GRAY on this frame
//            (pixel-probed; the only red there is the callout border column) — the
//            professor re-placed arc 7's label when the callout appeared,
//       k=8 (530.3, 523.7), k=9 (642.8, 527.0), k=10 (749.4, 489.2) — hand-placed
//            (polar auto-rule deviations up to 48pt; NOT used, same law as 28's delta).
//   * NEW callout box (bottom-left, frame-diff blob [64,391,387,511]):
//       - SINGLE rect, white fill, C00000 border (the frame's cols 57-59 stroke is the
//         PANEL border — present on 028 too; the 28v29 diff blob starts at col 64, and
//         on 028's frame the same zone shows only the panel stroke): border cores
//         L col 65 / T row 391.5 / R col 364 / B row 510 frame -> slide
//         48.24 / 409.7 / 359.28 / 533.96, line C00000 2pt. (An earlier "double left
//         edge" reading was a misattribution — corrected after the probe render.)
//       - text, all Arial bold ~14pt centered at slide cx ~203.2 (frame 214):
//         L1 "Using smaller ω value, allow" — blue 0000CC with the word "smaller" on a
//             yellow FFFF00 highlight (frame cols 155-210 -> slide 141.9..199.1) and the
//             ω glyph in RED CC0000 (frame cols 216-228 — measured, frame wins);
//         L2 "representation of longer sequences" — blue 0000CC;
//         L3 "(practically use  ω = 1/10000)" — red CC0000, double space after "use"
//             preserved verbatim (spec + measured 11px word gap).
//         Ink bands (slide pt): L1 y 419.6..433.3, L2 y 438.5..451.0 (pitch ~18.9pt),
//         L3 y 476.2..490.8 (one blank pitch before it). Single-line boxes at measured
//         positions (027-certified pattern); font size closed-loop fitted (selfcheck).
//   * badge numeral 29 = the number printed on THIS original frame (via component).
//   * callout font size: CLOSED-LOOP FITTED — 14pt (spec guess) rendered ink 18.5% too
//     narrow vs the measured bands; 16.5pt matches (L2 rendered 277.8pt vs measured
//     278.8pt). The frame wins over the spec's ~14pt estimate. Line pitch cross-check:
//     measured L1->L2 ink-top pitch 18.9pt = LO single-space at ~16.2-16.5pt font.
//   * mouse cursor overlapping Word 2's box (frame ~(677,156)) is a screen-recording
//     artifact — correctly omitted (judge GROUND RULES (b)/(c)); 028's cursor near
//     Word 1 is likewise absent here (the base component never drew it).
//
// LAWS honored: playlist chrome drawn ONCE inside the certified chain (numeral 29);
// verbatim text; margin:0 + explicit fontFace on every text element; certified
// components NOT edited; single-version deliverable slide_029_recreated.pptx; no '#'
// in hex; no /tmp writes. CONFIRMED DEPENDENTS: none yet (29 <- 28 only; component
// banked at certification per the playlist-scoped obligation).

const path = require("path");
const pptxgen = require("pptxgenjs");
const P28 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_028.js");
const P27 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_027.js");

const IN = (pt) => pt / 72;
const PT = 1 / 72; // slide pt -> inches (numeric factor, same as the components)

// ---- measured delta constants (slide pt) ------------------------------------
const M = P27.M; // certified family constants (single source of truth)
const CX = M.circle.cx, CY = M.circle.cy;
const RAD = Math.PI / 180;
const polar = (deg, r) => ({ x: CX + r * Math.cos(deg * RAD), y: CY - r * Math.sin(deg * RAD) });

// arrowheads k=8..10: measured bbox centers (two masks agree <=1.2pt)
const headsMeasured29 = { 8: [576.2, 522.7], 9: [689.1, 493.4], 10: [777.0, 408.7] };
// '+w' labels k=7(moved),8,9,10: measured ink centroids (wide-window, 028-calibrated)
const labelsMeasured29 = { 7: [414.2, 479.6], 8: [530.3, 523.7], 9: [642.8, 527.0], 10: [749.4, 489.2] };
// arrowhead k=7 and label k=0..6 inherit the certified/028-measured values unchanged.

const CALLOUT = {
  // single rect — the frame's cols 57-59 stroke is the PANEL border (present on 028
  // too; the 28v29 diff blob starts at col 64), NOT a callout edge. Border cores:
  // L col 65 / T row 391.5 / R col 364 / B row 510 frame -> slide 48.24/409.7/359.28/533.96.
  x: 48.24, y: 409.7, w: 311.0, h: 124.3,
  lineW: 2,
  textCx: 203.2, textW: 340,
  fontPt: 16.75, // closed-loop fit: 16.5 left L3 10 render-px narrow; 16.75 puts all
                 // three line ink bands within the ~4px tolerance (selfcheck v2)
  // ink-top offsets: LO first-line lead measured 0.257em at 14pt -> 4.24pt at 16.5pt
  l1y: 419.6 - 4.24, l2y: 438.5 - 4.24, l3y: 476.2 - 4.24,
  hl: { x: 141.9, y: 416.5, w: 57.2, h: 17.8 }, // yellow highlight band behind "smaller"
};

// ---- title delta --------------------------------------------------------------
// Line 1 re-drawn CENTER-aligned at the measured cx 177.0 (see header); lines 2-3
// byte-identical to the certified drawTitleDelta constants (M.title).
function drawTitleDelta29(pptx, slide) {
  const T = M.title;
  slide.addText("Sequence of 12 words", {
    x: (177.0 - T.w[0] / 2) * PT, y: T.boxes[0][1] * PT, w: T.w[0] * PT, h: T.h * PT,
    fontFace: "Arial", fontSize: T.fontPt, bold: true, color: M.colors.title,
    align: "center", valign: "top", margin: 0,
  });
  for (let i = 1; i < 3; i++) {
    const [tx, ty] = T.boxes[i];
    slide.addText(TITLE29_LINES[i], {
      x: tx * PT, y: ty * PT, w: T.w[i] * PT, h: T.h * PT,
      fontFace: "Arial", fontSize: T.fontPt, bold: true, color: M.colors.title,
      align: "left", valign: "top", margin: 0,
    });
  }
}
const TITLE29_LINES = ["Sequence of 12 words", "Positions are defined", "as angles"];

// ---- one delta arc k in 8..10 (family polyline rule + MEASURED head/label) ----
function drawArcDelta29(pptx, slide, k) {
  const fromDeg = k * 30, toDeg = (k + 1) * 30;
  const a0 = fromDeg + M.arcStartPadDeg, a1 = toDeg - M.arcEndPadDeg;
  const N = M.arcSegs;
  for (let i = 0; i < N; i++) {
    const t0 = a0 + ((a1 - a0) * i) / N, t1 = a0 + ((a1 - a0) * (i + 1)) / N;
    const p1 = polar(t0, M.arcR), p2 = polar(t1, M.arcR);
    slide.addShape(pptx.ShapeType.line, {
      x: Math.min(p1.x, p2.x) * PT, y: Math.min(p1.y, p2.y) * PT,
      w: Math.abs(p2.x - p1.x) * PT, h: Math.abs(p2.y - p1.y) * PT,
      flipH: p2.x < p1.x, flipV: p2.y < p1.y,
      line: { color: M.colors.arcStroke, width: 0.75 },
    });
  }
  const ah = { x: headsMeasured29[k][0], y: headsMeasured29[k][1] };
  slide.addShape(pptx.ShapeType.triangle, {
    x: (ah.x - M.ahW / 2) * PT, y: (ah.y - M.ahH / 2) * PT,
    w: M.ahW * PT, h: M.ahH * PT, flipV: true,
    fill: { color: M.colors.arrowhead }, line: { color: M.colors.arrowhead, width: 0.5 },
  });
  const lp = { x: labelsMeasured29[k][0], y: labelsMeasured29[k][1] };
  slide.addText("+\u03c9", {
    x: (lp.x - M.labelBoxW / 2) * PT, y: (lp.y - M.labelBoxH / 2) * PT,
    w: M.labelBoxW * PT, h: M.labelBoxH * PT,
    fontFace: "Arial", fontSize: M.labelFontPt, bold: true, color: M.colors.label,
    align: "center", valign: "middle", margin: 0,
  });
}

// ---- arc 7 (Word 7 -> Word 8): certified polyline + head, label at the MEASURED
//      moved position (028's drawArcDelta would put the label at the old 28-spot —
//      this frame shows it moved; the old spot is gray on slide_029.jpg).
function drawArc7MovedLabel(pptx, slide) {
  const k = 7, fromDeg = k * 30, toDeg = (k + 1) * 30;
  const a0 = fromDeg + M.arcStartPadDeg, a1 = toDeg - M.arcEndPadDeg;
  const N = M.arcSegs;
  for (let i = 0; i < N; i++) {
    const t0 = a0 + ((a1 - a0) * i) / N, t1 = a0 + ((a1 - a0) * (i + 1)) / N;
    const p1 = polar(t0, M.arcR), p2 = polar(t1, M.arcR);
    slide.addShape(pptx.ShapeType.line, {
      x: Math.min(p1.x, p2.x) * PT, y: Math.min(p1.y, p2.y) * PT,
      w: Math.abs(p2.x - p1.x) * PT, h: Math.abs(p2.y - p1.y) * PT,
      flipH: p2.x < p1.x, flipV: p2.y < p1.y,
      line: { color: M.colors.arcStroke, width: 0.75 },
    });
  }
  const ah = { x: P28.headsMeasuredDelta[k - 4][0], y: P28.headsMeasuredDelta[k - 4][1] };
  slide.addShape(pptx.ShapeType.triangle, {
    x: (ah.x - M.ahW / 2) * PT, y: (ah.y - M.ahH / 2) * PT,
    w: M.ahW * PT, h: M.ahH * PT, flipV: true,
    fill: { color: M.colors.arrowhead }, line: { color: M.colors.arrowhead, width: 0.5 },
  });
  const lp = { x: labelsMeasured29[7][0], y: labelsMeasured29[7][1] };
  slide.addText("+\u03c9", {
    x: (lp.x - M.labelBoxW / 2) * PT, y: (lp.y - M.labelBoxH / 2) * PT,
    w: M.labelBoxW * PT, h: M.labelBoxH * PT,
    fontFace: "Arial", fontSize: M.labelFontPt, bold: true, color: M.colors.label,
    align: "center", valign: "middle", margin: 0,
  });
}

// ---- NEW callout box (bottom-left) ---------------------------------------------
function drawCallout(pptx, slide) {
  const C = CALLOUT;
  // white rect, C00000 border (single stroke — see CALLOUT note above)
  slide.addShape(pptx.ShapeType.rect, {
    x: C.x * PT, y: C.y * PT, w: C.w * PT, h: C.h * PT,
    fill: { color: "FFFFFF" }, line: { color: "C00000", width: C.lineW },
  });
  // yellow highlight band behind the word "smaller" (under the text, z-order)
  slide.addShape(pptx.ShapeType.rect, {
    x: C.hl.x * PT, y: C.hl.y * PT, w: C.hl.w * PT, h: C.hl.h * PT,
    fill: { color: "FFFF00" }, line: { color: "FFFF00", width: 0 },
  });
  // L1: blue with red omega; "smaller" sits over the highlight band
  slide.addText([
    { text: "Using ", options: { color: "0000CC" } },
    { text: "smaller", options: { color: "0000CC" } },
    { text: " \u03c9 ", options: { color: "CC0000" } },
    { text: "value, allow", options: { color: "0000CC" } },
  ], {
    x: (C.textCx - C.textW / 2) * PT, y: C.l1y * PT, w: C.textW * PT, h: 20 * PT,
    fontFace: "Arial", fontSize: C.fontPt, bold: true, align: "center", valign: "top", margin: 0,
  });
  // L2: blue
  slide.addText("representation of longer sequences", {
    x: (C.textCx - C.textW / 2) * PT, y: C.l2y * PT, w: C.textW * PT, h: 20 * PT,
    fontFace: "Arial", fontSize: C.fontPt, bold: true, color: "0000CC",
    align: "center", valign: "top", margin: 0,
  });
  // L3: red, verbatim double space after "use"
  slide.addText("(practically use  \u03c9 = 1/10000)", {
    x: (C.textCx - C.textW / 2) * PT, y: C.l3y * PT, w: C.textW * PT, h: 20 * PT,
    fontFace: "Arial", fontSize: C.fontPt, bold: true, color: "CC0000",
    align: "center", valign: "top", margin: 0,
  });
}

// ---- compose ------------------------------------------------------------------
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const pptx = pres;
const slide = pres.addSlide();

// 1. certified 028 component grown to THIS frame: chrome numeral 29, 12 chips
//    (0..4 certified measured, 5..11 polar rule verified <=1.1pt), circle/spokes/
//    eqbox inherited; arcs + title suppressed here (drawn below at THIS frame's
//    measured geometry).
P28.renderBase(pptx, slide, { numeral: 29, wordCount: 12, skip: ["arcs", "title"] });
drawTitleDelta29(pptx, slide);

// 2. arcs 0..3 — certified measured component blocks (identical on this frame)
for (let k = 0; k <= 3; k++) {
  P27.drawArc(pptx, slide, { fromDeg: k * 30, toDeg: (k + 1) * 30 });
}
// 3. arcs 4..6 — 028's certified measured delta blocks (unchanged on this frame)
for (let k = 4; k <= 6; k++) {
  P28.drawArcDelta(pptx, slide, k);
}
// 4. arc 7 — certified polyline/head + THIS frame's moved label
drawArc7MovedLabel(pptx, slide);
// 5. arcs 8..10 — THIS slide's measured delta (no arc 11: measured absent)
for (let k = 8; k <= 10; k++) {
  drawArcDelta29(pptx, slide, k);
}
// 6. NEW callout box (last — nothing beneath it per the frame census)
drawCallout(pptx, slide);

pres.writeFile({ fileName: path.join(__dirname, "..", "slide_029_recreated.pptx") })
  .then(() => console.log("WROTE slide_029_recreated.pptx"));
