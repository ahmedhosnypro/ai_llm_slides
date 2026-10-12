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
