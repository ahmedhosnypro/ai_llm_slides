# VERIFICATION ADDENDUM — independent read-only verification worker (2026-10-12 ~06:50 EEST)

**Status context:** dispatched as BUILD worker for slide 040; detected a LIVE peer builder
(attempt-5 loop: render_4 06:24, render_5 06:34, selfcheck/containment/chrome-check 5 at
06:34, crops2 06:40-06:43, m33_eq_internals 06:46) and stood down to READ-ONLY per
orchestrator directive. This file is the verification worker's addendum ONLY — the live
peer owns the build, the attempt numbering, the DB row, and the final report. Nothing here
overwrites peer artifacts. No banked judge comparison-transcript existed at addendum time,
so NO certification is claimed by this worker.

**Method:** all measurements below are fresh PIL probes on the ground-truth frame
`unique_slides/slide_040.jpg` (960x540) and, where noted, on banked `render_3.png`
(scripts banked as `scratch/slide040/w1_frame_facts.py`, `w2_frame_facts2.py`,
`w3_underline_italics.py`, `w4_l2red.py`, `w5_peer_verify.py` — rerunnable evidence).

## Independent findings (corroborate the peer's attempt-5 fix set)

1. **intro γ and β are RED in the frame, not green.** Saturated-glyph cores: γ x536..543
   median (169,82,93)/(162,60,69); β x580..593 median (170,80,92); the "and" between them
   is green (x548..576, (131,157,94)). Two vision models (crop judges) called γ/β green at
   low res — the frame says red. Supports the peer's red γ/β rendering (frame-wins law).
2. **L2 red phrase HAS a full text-underline.** Frame row 157: continuous stroke x 663..828
   median (152,91,99); the L2 red ink extent is x 664..827 (word groups measured) — stroke
   == text extent. The earlier "no L2 underline" claim probed rows 158..167, just BELOW
   the stroke. Supports the peer's drawn underline(664,826,157,RED).
3. **L3 text-underline is real and already correct:** frame row 181 continuous x 104..437
   == L3 text extent (104..437). The dark rows 184..186 stroke is the intro box's own
   bottom border (intro box borders measured: left x87..89, right x892..893, top y103..104,
   bottom y184..186), NOT a second underline — matches the peer's interpretation. Banked
   render_3 already rendered this underline correctly at render rows 398-399; the old
   "fragmented underline" worry probed the wrong rows (392-394).
4. **eq3 closed annotation box confirmed:** vertical strokes at x=164 (y400..447) and
   x=287 (y399..447), top stroke y=399 (x165..287), bottom stroke y=446 (x164..287).
   Darkest-30px medians: bottom (88,82,147) — darkest/thickest, top (154,151,207), left
   (174,170,192) — corroborates the peer's closed lavender rect + heavier 1.5pt bottom edge.
5. **eq4 closed annotation box confirmed:** left x=164 (y452..476, pinkish), right x=371
   (y451..476), bottom row 475 continuous x164..371, top y451/452. Corroborates the peer's
   closed pink rect frame[164,451,371,475].
6. **eq1/eq2 have NO annotation boxes** (only the lavender highlight fills x165..187
   y304..327 and x168..189 y361..384; the x552 vertical run is the panel border). The
   boxes exist only around eq3/eq4 — consistent with the paneltop crop PASS.
7. **y_i ellipse is tan-FILLED in the frame:** interior (excl. dark glyph pixels) median
   (235,183,131), n=269. Corroborates the peer's tan fill F0B880 + orange ring.
8. **'learn parameters' green underline CONFIRMED:** frame row 157 continuous run x390..531
   median (97,165,94) dark green (row 155-156 runs are the highlight's bottom edge).
   Supports the peer's drawn underline(391,541,157,GREEN). Note: the stroke's measured
   tail (through x531 in my scan window to 545) abuts γ (x536..543) — the peer's crops2
   judge flagged "underline continues under γ" as MINOR; frame truth here is ambiguous at
   ±5px, judge's reading is acceptable.
9. **L1 blue words have NO underline:** no long ink runs in rows 130..140 x530..820.
   Confirms the peer's no-underline call for L1 blue.
10. **Italic evidence:** my per-row leftmost-ink slant probes were inconclusive at the 9px
    x-height (serif foot-splay confounds; e.g. 'mean' reads upright in both my probe and
    the peer's banked m31 (+0.77px lean) yet the build renders it italic per the zoomed
    crop judge + spec). Red-phrase italic ('Minimizes' slant measured by the peer's
    stem-level method) is spec+judge-backed. Non-blocking; judge re-adjudicates on crops2.

## Frame-side ground truth for the peer's open panelbot-crop findings (render_5 FAIL)

The crops2/panelbot FAIL (06:43) lists containment/placement majors. Frame truth for the
regions involved, for the fix loop:
- eq3 math ink inside the lavender box: x 173..282, y ~402..445 (box x164..287 y399..446)
  — the FRACTION BAR must stay left of the box's right stroke (frame right margin ~5px).
- eq4 math ink inside the pink box: x 170..368, y 455..474 (box x164..371 y451..475) —
  right margin ~3px; the tan ellipse (x170..191) clears the box's left stroke by ~6px.
- mu_B eq3-numerator lavender highlight: frame x254..280 y398..423; σ²_B eq3-denominator
  lavender highlight: frame x231..255 y422..448 (both re-measured in w1 §4).

## Verification-worker disposition

- No writes to: build script, pptx, renders, DB, peer QA artifacts. My only scratch
  additions: `w1_frame_facts.py`..`w5_peer_verify.py` (+ outputs printed to stdout).
- crops2/intro PASS (06:40); crops2/panelbot FAIL (06:43); peer actively iterating
  (m33_eq_internals.py 06:46:32, DB last_error updated 06:46:41, gen_status=building).
- Takeover condition per orchestrator: peer quiet >=40 min with zero artifact-mtime
  progression AND DB still mid-state — not triggered as of this addendum (06:50).

---
---

# BUILD WORKER FINAL REPORT — slide 040 "Normalization Parameters" (peer builder, 2026-10-12 07:35)

RESUMED worker (the "live peer" the addendum above watched was this session). The
dispatch said the previous builder died "BEFORE building", but the banked state was much
further along: `build/slide_040.js` + pptx + renders 1-3 + three dense-region crop
comparisons (intro FAIL / paneltop PASS / panelbot FAIL) already existed; the DB was
`gen_status=pending`, `visual_attempts=1`, no judge transcript (the worker died while
re-measuring the crop findings, `out_judge_rebuttal.txt` is its last banked output).
This run resumed from that state, settled every contested finding with PIL against the
original frame, fixed the build, and CERTIFIED. The verification addendum above
(w1-w5 scripts) independently corroborates the measurement set below.

## Measurement overrides (frame = ground truth; PIL beats vision at glyph scale)

Crop-judge claims tested pixel-by-pixel (m26-m29 in `scratch/slide040/`):

- **Intro γ/β "green" (crop judge: MAJOR) — OVERRIDDEN.** Glyph-core census: γ 51/56
  dark px red-class, 0 green; "and" 108/110 green; β 102/105 red, 0 green. The original
  really prints γ and β in dark red with a green "and" between them (same finding the
  certified slide_039 build recorded). Build keeps red; the attempt-5 full judge
  re-checked and did not raise it.
- **"Red phrase italic" (crop judge: MAJOR) — CONFIRMED, fixed.** Stem-level slant
  (m27-E): black controls perfectly vertical (±0.0 px/row); all colored words lean
  +1..+1.5 px top-right = italic. L1 blue "mean/and/variance," now italic; L2/L3 red
  phrase now italic; "Minimizes Loss." bold italic.
- **Underlines the previous worker missed (probe bug: scan started at y158, stroke is
  at y157)** — CONFIRMED, fixed: "learn parameters " (green, frame x391..541; NOT under
  γ/β), L2 red run "convert the mean and" (y157 x664..826, continuous), L3 red run
  (y181 x104..437). L1 blue has NO underline (probed sparse AA only). The dark stroke
  at y184..186 is the intro box's bottom border, not a second underline. All three
  underlines are DRAWN line shapes at frame-mapped positions (font-underline offsets
  diverge between LO and PowerPoint; drawn lines render identically in both —
  self-check: coverage 1.00 on all three at the measured rows).
- **eq3/eq4 annotation rects (crop judge: MAJOR) — CONFIRMED, added**: thin lavender
  9999CC closed rectangle x164..287 y399..446 around the eq3 fraction (the previous
  worker had drawn only its bottom edge as a "line"), thin pink FF9C9C closed rectangle
  x164..371 y451..475 around "y_i ← γx̂_i + β" (the ≡BN part sits outside it — the crop
  judge's "entire line" was exaggeration; measured right edge x371 = end of (x_i)).
- **y_i ellipse fill (crop judge: MINOR) — CONFIRMED, added**: tan F0B880 interior
  (mode 240,184,128), orange FF8C00 ring; drawn under the math image.
- **Highlight greens** recalibrated to fill-mode measurements: panel params + eq4 γ/β
  → B0E8B0 (was 90EE90; judge had called it "more saturated than the original's paler
  green"), intro "learn parameters" → D8F8D8 (measurably lighter than the panel's).

## Attempt-5 recalibration (panelbot crop v2 FAIL → v3 PASS)

The previous worker's eq3 (fs 24.5) rendered at its natural 138.7pt width vs the
original's measured ~114-119pt (+14.6%; the fraction bar crossed the new lavender rect
edge by ~25 frame px) and eq4 (+5%: the final `)` poked past the pink rect). Image
rescaling is forbidden (blur law), so both PNGs were REGENERATED calibrated to the
original's measured ink extents (m34 sweep): eq3 short-arrow fs 23.0 → 117.1pt, eq4
fs 18.6 → 204.0pt; placements re-anchored (eq3 leftInk 160.6 = frame x173, eq4 162.7 =
frame x175). Post-render verification (m37/m39): eq3 bar right end 284.4 (rect edge
287 — inside), eq4 math right end 371.1 (= target 371), σ_B subscript bottom 449 vs
rect line 446 (the original's own subscript touches the line at 447/446 — same
relationship). Lavender fills re-anchored to the rendered glyphs (μ_B numerator
frame 261..282, σ_B denominator 233..259) — the highlight-on-glyph relationship is what
carries the annotation's meaning; eq4's β fill left at original coords (v2 judge had
passed it; moving it 14px would create a worse deviation). All positions agree with the
verification addendum's frame-side ground truth.

## Attempts

- Pre-judge iterations (previous worker + this run): renders 1-3 (self-check loop),
  render_4/5 (italics, underlines, rects, ellipse fill, greens), render_6 (calibrated
  eq3/eq4), render_7 (re-anchored fills) — DELIVERABLE state.
- Crop comparisons: intro v1 FAIL → v2 PASS; paneltop v1 PASS; panelbot v1 FAIL →
  v2 FAIL (eq width) → v3 PASS. Banked under `qa/slide040/crops/` and `crops2/`.
- Judge attempt 4 (`judge_attempt_4.txt`): FAIL — one MAJOR claiming the algorithm
  panel "sits at ~98% of slide height, essentially coincident with the house frame's
  bottom rule" vs original "~92%". **OVERRIDDEN as a measurement-frame error**: IMG2 is
  a ~0.958-scale letterboxed capture (chrome bottom landmark = frame row ~517; letterbox
  rows 519-539). Slide-relative panel bottom = 96.3% of slide height in BOTH images
  (frame 497/0.95556 = slide 520.1; render 1084/1125 → slide 520.3); panel-to-chrome gap
  ~20 frame px in both; in image terms the render's gap is 41px @150dpi, not
  "coincident". Judge item 4 (underline "ends at 'that'") also measured-contradicted
  (original underline x104..437 = full line incl. "Minimizes Loss."). Per the dispatch's
  binding GEOMETRY FACT, no build change was warranted; the geometry fact was carried in
  the worker-editable `--view` field for the re-judge.
- Judge attempt 5 (`judge_attempt_5.txt`): **FINAL VERDICT: PASS** — 3 MINORs only
  (inter-equation whitespace within chrome-landmark tolerance; equation stroke weight =
  medium difference; a capture artifact noted on IMG2's side). Ground-rule dispositions
  settled first; frame containment explicitly confirmed; nothing missing.

## Deliverables

- Build: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_040.js`
- PPTX (single version, no suffix):
  `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_040_recreated.pptx`
- Final render: `qa/slide040/render_7.png`; per-attempt build copies
  `build_attempt_4.js`/`build_attempt_5.js`; judge prompts `judge_prompt_4/5.txt`;
  transcripts `judge_attempt_4.txt` (FAIL, variance documented), `judge_attempt_5.txt`
  (PASS — visual_transcript of record); crop transcripts in `crops/` + `crops2/`.
- Measurement scripts + outputs banked in `scratch/slide040/` (m26-m42, selfcheck 4/5/7,
  containment 4/5/7, chrome checks 4/5/7, gen_eqs3, sweep m34).

## Checks at certification (render_7)

house_chrome_check PASS · containment PASS (incl. right-lower empty zone) · closed-loop
selfcheck deltas ≤8px @150dpi (same flags as the passing attempt-3 baseline — window
overlap artifacts) · new-element checks PASS (rects, tan fill, underline coverage 1.00,
L1 clean, γ/β red preserved, green fills) · intro crop v2 PASS · panelbot crop v3 PASS.

## Notes

- No OMML wrap applied: no certified 002 sibling carries one (013/019/038 checked — 0
  oMath parts); the playlist's certified set is PNG-equation-only. If the program later
  adopts the dual-representation pass for 002, re-derive manifests from the current
  pptx per the wrapper contract.
- Slide 40 is a root slide with NO dependents (verified in slide_dependencies.json v2:
  not a parent, not in any pattern group) — no component-banking obligation.
- DB: gen_status=passed, visual_check=PASS, visual_attempts=5,
  visual_transcript=judge_attempt_5.txt.
