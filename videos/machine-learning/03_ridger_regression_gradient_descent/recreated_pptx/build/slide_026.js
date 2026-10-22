// Build script for slide 026 — "Gradient Descent Solution"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (lecture 03)
//
// GEOMETRY LAW: every value below is a MEASURED frame pixel from the banked 8-pass
// measurement bank (qa/slide026/measure_frame*.py + _out.txt, 2026-10-19/20) — frame
// 960x540, 1px = 1pt = 1/72in. Font fit calibrated against the banked ink widths
// (scratch/tmp/calib2_026.py): Arial/Liberation 17.5pt fits ALL measured text lines
// within +/-2.1% (rowA -0.5%, rowB +2.0%, rowC ~-2.6%, rowD -2.0%, N1 -1.6%,
// N2 +0.8%, N3 +2.1%, N4 +0.9%); title bold 27.5pt (adv 345.3 vs ink 346);
// section headers bold 17.5pt (GD hdr 280.5 vs 283; Notes hdr 51.6 vs 51).
//
// MEASURED TARGETS (frame px, from the bank):
//   Blue content box: border cols 82-83 (L) / 862-864 (R), rows 90-92 (T) / 498-500 (B)
//     => box x82..864, y90..500, white interior (255,255,255), border nominal 0000FF
//     (core (0,0,97)), thin. Title red ink y60..82 x294..639 (center 466.5), no descenders.
//   Algorithm steps start x146; section headers + notes text start x109; bullet discs
//     d=7 at x91..97 (N1 y346..352, N3 y446..451), black.
//   Line bands (ink tops): GD hdr 110 | rowA 143 | rowB 177 | rowC 210 | rowD 243
//     (pitch 33-34) | Notes hdr 310 | N1 342 | N2 376 | N3 441 | N4 475;
//     N2->N3 gap = 65px (an extra blank line between the two Notes bullets).
//   UNDERLINE BARS (measured, solid runs): rowB y192..194 x349..716
//     ("moving along the direction of negative gradient"); rowD y258..260 x287..473
//     ("gradient is almost zero"); N3 y458 x177..277 ("approximately") and
//     x538..728 ("variable number of steps"). Rendered as run-level underline: true
//     (PPT underline sits ~2-3px below the baseline = exactly where the bars are).
//   RED-ON-BLUE: the tail of row C, "AKA Learning Rate" x520..682, is RED (C00000
//     family) in the original (measure_frame2 run classification + the 2026-10-20
//     tiebreak probe; re-verified attempt 7: original RED x520..682 core (129,18,31)).
//     The CLOSING PAREN is a separate BLUE run x684..688 (core (13,4,118)) — the old
//     note's "x518..689, is RED" wrongly swept the paren in; the paren is BLUE in both
//     rowA "(W)" and rowC, and render_6 already drew rowA's blue. RowC's red paren was
//     the single-run error fixed in attempt 7.
//   Bold spans — validated against the banked ink widths (bank run width vs this build's
//   measured advance, calibrated on the regular controls; halo bound +0..+4, kern/gap
//   bound -7..+2 for multi-word runs). Kept bold where the frame agrees with the brief:
//     rowA "Random Weights (W)"; rowB "negative gradient" (underlined);
//     rowC "moving step is a hyper parameter" + "AKA Learning Rate" (red);
//     rowD "almost zero" (underlined); N1 "is a convex function"; N2 "ONE Minimum";
//     N4 "Learning Rate".
//   REGULAR (brief over-claimed bold — the frame wins, measured):
//     rowB "Loss function" (bank ink 5-6px narrower than this build's bold advances);
//     N3 "variable number of steps" (bank w191 = regular sim 191; bold would be 207);
//     rowC "w.r.t. W" (bank w43/w23 = regular; bold would be +3).
//
// DEVIATIONS FROM SPEC (law hierarchy: deck AGENTS.md + judge_protocol_03.md +
// runbook OVERRIDE the analysis spec; frame measurement overrides intuition):
//   1. House chrome (white canvas FFFFFF; gray E9E9E7 panel x54..903 y45..540; thin
//      C00000 1pt strokes LEFT/RIGHT/BOTTOM only — NO TOP STROKE; badge FDFD96 with
//      6A5ACD ring, numeral 26) via shared_patterns/house_chrome.js per deck AGENTS.md.
//      The spec's "#F0F0F0 background / #FFFF00 badge" are vision misreads; house law wins.
//   2. Spec's vague percentage positions replaced by the measured pixel geometry above.
//   3. Spec says step [2] is entirely blue; measured row C tail "AKA Learning Rate)"
//      is red — drawn red (frame wins).
//   4. Spec/N3 verbatim string reads "approximately"; the ORIGINAL FRAME prints
//      "approximatly" (12 glyphs, no 'e' — attempt-8 adjudication, see the N3 note
//      above). Drawn as the frame prints it (fidelity target = the original image).
//   5. Spec's emphasis list for note bullet 1 omits bold on the leading "Least Squares";
//      the ORIGINAL FRAME prints it bold (attempt-9 adjudication, see the N1 note below).
//      Drawn as the frame prints it.
//
// Single version deliverable: recreated_pptx/slide_026_recreated.pptx (no suffixes).

const pptxgenpkg = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const PX = 1 / 72; // frame px -> inches
const RED = "C00000";   // no '#' in pptxgenjs hex
const BLUE = "0000FF";
const BLACK = "000000";
const FONT = "Arial";
const BODY = 17.5;   // measured global fit for all body lines
const TITLE = 27.5;  // measured fit (bold)
const HDR = 17.5;    // section headers: bold + red, measured same pt as body

// ---- measured geometry (frame px) ---------------------------------------------------
const BOX = { x: 82, y: 90, w: 783, h: 411 };            // blue content box x82..864 y90..500
const LINES = {
  gdhdr:   { base: 123, x: 109 },   // "Gradient Descent (GD) Algorithm:" (cap top 110)
  rowA:    { base: 156, x: 146 },   // cap top 143
  rowB:    { base: 190, x: 146 },   // cap top 177
  rowC:    { base: 223, x: 146 },   // cap top 210
  rowD:    { base: 256, x: 146 },   // cap top 243
  noteshdr:{ base: 323, x: 109 },   // "Notes:" (cap top 310)
  N1:      { base: 355, x: 109 },   // cap top 342
  N2:      { base: 390, x: 109 },   // cap top 377, x-height top 380 (attempt-4 re-measure:
                                   // the previous 385 came from reading the ASCENDER top
                                   // 376 as x-height; the original's true N2 baseline is 390
                                   // — identical-predicate profile dump, both images)
  N3:      { base: 454, x: 109 },   // cap top 441
  N4:      { base: 488, x: 109 },   // ascender top 475
};
// title: ink x294..639, no descenders => baseline = ink bottom = 82
const TITLE_BASE = 82, TITLE_X = 294;

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

const slide = pptx.addSlide();

// House chrome: white canvas, gray panel, red L/R/Bottom strokes (NO top), badge "26"
drawHouseChrome(pptx, slide, { numeral: 26 });

// --- blue-bordered white content box -------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: BOX.x * PX, y: BOX.y * PX, w: BOX.w * PX, h: BOX.h * PX,
  fill: { color: "FFFFFF" },
  line: { color: BLUE, width: 1.25 },  // measured border 2-3px @150dpi => ~1.25pt
});

// ---- text helper ---------------------------------------------------------------------
// One text box PER LINE at its measured baseline (immune to PowerPoint-vs-LO auto
// pitch divergence; per-line boxes have no pitch to diverge on). BASELINE_OFFSET is
// the measured box-top -> baseline distance in em (LO natural pitch, valign top,
// margin 0); calibrated closed-loop against the 150dpi render in the selfcheck.
// ATTEMPT 4 (resume worker 2026-10-21): closed the residual line-width deficits the
// attempt-3 selfcheck flagged, PIL-adjudicated against the ORIGINAL frame with
// identical predicates (adjudicate_026.py / probe_halo_026.py):
//   - the original's ink edges are threshold-invariant (no measurable JPEG halo on
//     saturated blue/red/black text), so the render's short right edges were REAL:
//     rowD -14.4, N1 -11.0, gdhdr -5.3, rowC -5.4/-5.2, rowB +2.7, N2 +2.2, title -2.8.
//   - fixed with per-line charSpacing (building.md law: charSpacing, never font size),
//     calibrated closed-loop (calib_cs_026: +0.16pt/char-run ≈ +1px per char at 17.5pt).
//   - rowC: charSpacing on the BLUE runs only, so the red tail "AKA Learning Rate)"
//     lands at x520..682 (measured original red extent x520..682) without widening it.
//   - vertical placement verified UNCHANGED: bracket tops match the original exactly
//     (rowA y144 both), original band heights are halo-inflated ~1.5-2.5px/edge
//     (descender/bracket evidence), the ~1px baseline delta is inside tolerance.

const BASELINE_OFFSET_EM = 1.0;
function line(key, runs, sizePx, widthPx, spc) {
  const g = LINES[key];
  const topPx = g.base - sizePx * BASELINE_OFFSET_EM;
  if (spc) runs.forEach(rr => { rr.options.charSpacing = spc; });
  slide.addText(runs, {
    x: g.x * PX, y: topPx * PX, w: widthPx * PX, h: 30 * PX,
    valign: "top", align: "left", margin: 0, fontFace: FONT,
  });
}
const r = (text, opts) => ({ text: text, options: opts });

// ---- title (red bold 27.5pt, ink x294..639) ------------------------------------------
slide.addText([r("Gradient Descent Solution", { bold: true, charSpacing: 0.11 })], {
  x: TITLE_X * PX, y: (TITLE_BASE - TITLE * BASELINE_OFFSET_EM) * PX,
  w: 380 * PX, h: 34 * PX,
  fontSize: TITLE, bold: true, color: RED, fontFace: FONT,
  valign: "top", align: "left", margin: 0,
});

// ---- section header: "Gradient Descent (GD) Algorithm:" (red bold) --------------------
line("gdhdr", [r("Gradient Descent (GD) Algorithm:", { bold: true, color: RED, fontSize: HDR })], HDR, 300, 0.15);

// ---- algorithm steps (blue 17.5pt) -----------------------------------------------------
// [1] — bold "Random Weights (W)"
line("rowA", [
  r("[1] Start with initial ", { color: BLUE, fontSize: BODY }),
  r("Random Weights (W)", { color: BLUE, fontSize: BODY, bold: true }),
], BODY, 350);

// [2] line 1 — underline "moving along the direction of negative gradient" (measured bar),
// bold "negative gradient" ONLY. "Loss function" is REGULAR in the frame: the banked ink
// runs "Loss" (x742..777, w35) and "function" (x783..846, w63) are 5-6px NARROWER than
// this build's bold advances (41 / 68), while the single-word controls ("Start" w36,
// "weights" w59, "(w.r.t." w70) sit within -1..+4 of their advances — the same test that
// proves the brief's "w.r.t. W" (also claimed bold) is actually regular. Vision over-
// detected bold here; the frame wins.
line("rowB", [
  r("[2] Update the weights by ", { color: BLUE, fontSize: BODY }),
  r("moving along the direction of ", { color: BLUE, fontSize: BODY, underline: true }),
  r("negative gradient", { color: BLUE, fontSize: BODY, bold: true, underline: true }),
  r(" of Loss function", { color: BLUE, fontSize: BODY }),
], BODY, 730, -0.03);

// [2] line 2 — blue until "parameter,", then RED bold "AKA Learning Rate", then a
// BLUE ")" — and NOTHING red after x682.
// ATTEMPT 7 (resume worker 2026-10-21): the previous builds drew the closing paren RED
// on the strength of a stale bank note ("the tail ... x518..689 is RED"). Re-measured
// PIL-FIRST with identical predicates against BOTH images (probe_parens.py /
// probe_rowC_words.py / probe_rowC_paren_out.txt):
//   original RED extent  : x520..682  (1040 ink px, core RGB (129,18,31))
//   original BLUE extent : x146..688  — the paren is a separate blue run x684..688,
//                           y211..227 (h17, descender to the baseline), 53 ink px,
//                           CORE RGB (13,4,118) = BLUE (b-r=107), NOT a JPEG halo
//   render_6 RED extent  : x518.6..682.2 — matched only because the red ")" was
//                           counted in; the actual red tail ends at x676.5, i.e. 5.5px
//                           SHORT of the original's 682
//   the original's rowA "(W)" parens are BLUE too (cores (35,28,122) and (50,43,125))
//     and render_6 draws them blue — so the paren colour is a per-run error in rowC.
// Fix: the ")" is drawn BLUE (frame wins over the stale note) and the red tail carries
// charSpacing 0.32pt (calibrated closed-loop on measure_rowC_cs_out.txt: 0.32pt puts
// the red tail's right edge at x682.0 and the paren at x684..688, both inside +-1px of
// the original). Attempt 4's 0.11pt on the BLUE runs is unchanged (the blue extent
// still lands at x146.8..511.4 vs the original's x146..512).
line("rowC", [
  r("(w.r.t. W) (", { color: BLUE, fontSize: BODY, charSpacing: 0.11 }),
  r("moving step is a hyper parameter,", { color: BLUE, fontSize: BODY, bold: true, charSpacing: 0.11 }),
  r(" ", { color: BLUE, fontSize: BODY, charSpacing: 0.11 }),
  r("AKA Learning Rate", { color: RED, fontSize: BODY, bold: true, charSpacing: 0.32 }),
  r(")", { color: BLUE, fontSize: BODY, charSpacing: 0.32 }),
], BODY, 560);

// ATTEMPT 5 (resume worker 2026-10-21): rowD tracking moved OFF the underlined span
// and ONTO the tail run only. Uniform 0.16pt tracking closed the line's right edge
// (815.6 -> 830.0 = the original's, exact) but ALSO widened the measured underline
// bar from x287..473 to x290..476 (+2/+4): charSpacing adds ~0.2px/char and the bar
// spans 24 chars. Tracking the tail run alone (46 chars) closes the same 14.4px
// without touching the bar. Per-run charSpacing is the same mechanism rowC already
// uses (blue runs only, so the red tail keeps its measured extent).
// [3] — underline "gradient is almost zero" (measured bar x287..473 is CONTINUOUS:
// the space between the runs must be underlined too or the bar splits in two)
line("rowD", [
  r("[3] Stop when the ", { color: BLUE, fontSize: BODY }),
  r("gradient is ", { color: BLUE, fontSize: BODY, underline: true }),
  r("almost zero", { color: BLUE, fontSize: BODY, bold: true, underline: true }),
  r(" (this is at the minimum value of the function)", { color: BLUE, fontSize: BODY, charSpacing: 0.27 }),
], BODY, 700);

// ---- section header: "Notes:" (red bold) ----------------------------------------------
// ATTEMPT 6: -0.15pt charSpacing closes the measured +2.2px right edge (original
// 'Notes:' ink x111..159 = 51px wide vs this build's 51.3px at x109.9; isolated word,
// no runs after it, so no cascade into the line total). Same-mask measurement in
// selfcheck_attempt_5.py (title band moved to the RED mask there — the old
// gray-diff mask caught a faint JPEG ghost under the original's title).
line("noteshdr", [r("Notes:", { bold: true, color: RED, fontSize: HDR, charSpacing: -0.15 })], HDR, 90);

// ---- notes bullets (black 17.5pt, round disc markers d=7px at x91) ---------------------
const bullet = (topPx) => slide.addShape(pptx.ShapeType.ellipse, {
  x: 91 * PX, y: topPx * PX, w: 7 * PX, h: 7 * PX,
  fill: { color: BLACK },
});
bullet(346); // N1 disc y346..352 (measured)
bullet(446); // N3 disc y446..451 (measured)

// Note 1 line 1 — bold "Least Squares" (attempt 9) + bold "is a convex function"
// ATTEMPT 9 (resume worker 2026-10-21): the attempt-8 notes-crop leg (crop_8_notes_judge.txt)
// PASSed but raised one MINOR — "the original's leading phrase 'Least Squares' of the first
// bullet is BOLD (heavier strokes than the adjacent regular 'Linear regression...'); the
// recreation drops the bold". PIL-FIRST adjudication CONFIRMED it (probe_leastsq*.out,
// controlled two-weight render scratch/tmp/lo_boldtest/test_ls_026.js -> sp/ls-1.png, same
// 17.5pt/Arial/x/charSpacing pipeline):
//   * SAME-LETTER stem mass, within the ORIGINAL image (no cross-image/medium confound):
//     the 'L' stem of "Least" measures x111..113 = 3 solid columns x 11/13 zone rows
//     (33 ink px) while the 'L' stem of "Linear" measures x231..232 = 2 columns x 9/13
//     (18 ink px) — a 1.83x mass ratio. The same-letter ruler inside render_8 (regular
//     'Least' L = 1.44 frame px vs BOLD 'Learning' L = 1.92 = 1.33x) shows what a regular
//     pair looks like: "Least"/"Linear" in render_8 are identical (1.44 both).
//   * Phrase-window ink density over the x-height band (composition-controlled — the same
//     phrases in both images), threshold sweep 430/550/650/730:
//       ORIG OKS LS/REG = 1.46 / 1.26 / 1.20 / 1.20   (its own BOLD 'is a convex
//       function' span = 1.38 / 1.23 / 1.20 / 1.13 — the LS span tracks the BOLD class,
//       not the REGULAR class, at every threshold)
//       REN8 (regular LS): LS/REG = 1.01 / 1.02 / 1.03 / 1.06  (the regular class)
//     Controlled sims: regular LS/REG = 1.04, bold LS/REG = 1.32.
//   * Cross-image anchor: the ORIGINAL's regular spans sit at 0.69-0.79 of render_8's
//     density (72dpi video-capture softening), but its LS span sits at 0.99 — an upward
//     outlier of exactly bold magnitude.
//   * The analysis brief is silent on it ("bold 'is a convex function' and 'ONE Minimum'"),
//     but the brief also normalised the original's typo 'approximatly' and over-read bold on
//     'variable number of steps' (banked refutation), so its emphasis list is not authority:
//     the frame is. Drawn BOLD as the frame prints it.
// Fix: "Least Squares " bold. Bold advances ~+6px over the line (measured on the sim), so
// the per-run tracking is re-calibrated closed-loop against the original's measured extents
// (Squares->Linear space x224..230, line right edge inside the +-2.0 text band).
line("N1", [
  r("Least Squares ", { color: BLACK, fontSize: BODY, bold: true, charSpacing: 0.02 }),
  r("Linear regression objective function ", { color: BLACK, fontSize: BODY, charSpacing: 0.06 }),
  r("is a convex function", { color: BLACK, fontSize: BODY, bold: true, charSpacing: 0.06 }),
  r(" (even with", { color: BLACK, fontSize: BODY, charSpacing: 0.06 }),
], BODY, 680);

// Note 1 line 2 — bold "ONE Minimum"
line("N2", [
  r("regularizer). This means it has ", { color: BLACK, fontSize: BODY }),
  r("ONE Minimum", { color: BLACK, fontSize: BODY, bold: true }),
  r(" (good news ).", { color: BLACK, fontSize: BODY }),
], BODY, 500, -0.04);

// Note 2 line 1 — VERBATIM wrap recovered from the bank: the original's N3 line
// has an ink run at x818..836 AFTER "depending" (measure_frame2 N3 runs), and N4's
// measured width (x109..295 = 186px) fits only "the used Learning Rate" — so line 1
// ends "...depending on" and line 2 is "the used Learning Rate" (the "on" belongs to
// line 1, it is NOT optional: dropping it breaks the verbatim contract).
// underline "approximately", underline "variable number of steps" (REGULAR, not bold:
// banked ink run x538..728 (w191) matches this build's REGULAR simulation exactly (191)
// while a bold simulation is 207 — 16px wider, far beyond the +0..+4 halo bound the
// multi-word controls allow; the brief's bold claim for this span is a vision over-read)
// ATTEMPT 8 (resume worker 2026-10-21): the notes-crop leg (crop_7_notes_judge.txt) FAILED
// with a MAJOR finding — "the original's underlined phrase reads 'approximatly', the
// recreation renders 'approximately' (an added 'e')". PIL-FIRST adjudication CONFIRMED the
// finding against BOTH images (probe_approx.out / probe_approx3.out / probe_n3_spelling4.out
// / probe_approx_final.out), so the frame wins over the analysis brief's normalized spelling:
//   * ORIGINAL word ink x177..277 = 101 frame px, with a NO-ink gap at x278..281 before
//     "find" (x282..) — even at a LOOSE threshold (any pixel < lum 730) nothing sits there.
//   * CONTROLLED two-spelling render (scratch/tmp/lo_boldtest/test_n3_026.js -> sp-1.png,
//     same 17.5pt/Arial/x/charSpacing pipeline): "approximately" measures 110 px of ink
//     (x169..278) and carries FOUR tail clusters — t(251-255) e(256-264, a 9px glyph with
//     a full-width mid-height crossbar) l(266-268) y(270-277); "approximatly" measures
//     100 px (x169..268) with THREE tail clusters — t(251-255) l(256-258) y(260-267).
//   * The ORIGINAL's tail has THREE clusters (x260-263 4px, x265-268 4px, x270-277 8px)
//     with the ascender ("l") at x267-270 and the "y" at x270-277: matching "approximatly"
//     shifted +9px cluster-for-cluster (l 265-267, y 269-276), and leaving NO room for an
//     'e' between the 't' (ends x264) and the 'l' (starts x265). An "approximately" reading
//     would put its last glyph ("y") at x279-286 — the original has no ink there at all.
//   * The analysis brief's verbatim string ("...approximately find...") is a vision-model
//     normalization of the original's typo; fidelity target is the original image.
//   Fix: the run text is "approximatly" (12 glyphs, as printed on the slide).
// ATTEMPT 8b: dropping the 'e' costs ~11px of line width (Arial's 13-glyph
// "approximately" advanced 108.9px; the 12-glyph "approximatly" advances 99.2px), so the
// N3 line's right edge fell 825.2 vs the original's 836 and both bars followed it left
// (selfcheck_attempt_8: N3 -10.8, N3a -6.6/-10.8, N3b -13.6/-12.7). Closed with per-run
// charSpacing (same mechanism as rowC; the line-level `spc` arg would stomp the runs, so
// each run carries its own). The original's typeface is simply WIDER than Arial (its
// "approximatly" advance measures ~104px = the width of its bar, vs Arial's 99), so the
// tracking stands in for the original's font metrics, calibrated closed-loop to land every
// N3 item inside its band: 0.2pt/char on the plain runs overshot the line's right edge to
// +5.5 (selfcheck_attempt_8, text band +-2.0), so the plain runs sit at 0.12pt (+1.3
// measured) with 0.35 on the underlined word (bar1 width +4.2 -> 103 vs the original's 104)
// and 0.05 on bar2's span (+1.25 -> 193 vs 192). Measured on render_8: N3 x90.7..837.3
// (orig 91..836), N3a x170.2..273.4 (orig 176..279), N3b x533.3..726.5 (orig 538..729) —
// every N3 item inside the +-6.6px bar band and the line inside the +-2.0 text band.
line("N3", [
  r("GD will ", { color: BLACK, fontSize: BODY, charSpacing: 0.12 }),
  r("approximatly", { color: BLACK, fontSize: BODY, underline: true, charSpacing: 0.35 }),
  r(" find this minimum value but at a ", { color: BLACK, fontSize: BODY, charSpacing: 0.12 }),
  r("variable number of steps", { color: BLACK, fontSize: BODY, underline: true, charSpacing: 0.05 }),
  r(" depending on", { color: BLACK, fontSize: BODY, charSpacing: 0.12 }),
], BODY, 765);

// Note 2 line 2 — bold "Learning Rate"
line("N4", [
  r("the used ", { color: BLACK, fontSize: BODY }),
  r("Learning Rate", { color: BLACK, fontSize: BODY, bold: true }),
], BODY, 210);

pptx.writeFile({ fileName: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_026_recreated.pptx" })
  .then(() => console.log("wrote slide_026_recreated.pptx"));
